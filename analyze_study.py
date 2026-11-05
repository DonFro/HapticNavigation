"""Statistical analysis for the Haptic Navigation user study.

Usage (run on your PC, in the project folder):
    py -m pip install pandas scipy statsmodels matplotlib
    py analyze_study.py trials.csv ratings.csv                    # session mode
    py analyze_study.py trials.csv ratings.csv participants.csv   # paired mode

Session mode (no participants.csv): every session is its own unit, and
Haptic + Audio sessions are compared with Audio only sessions using
independent-samples tests (Mann-Whitney U, Welch t-test on log time).

Paired mode (with participants.csv): each participant's two sessions are
compared with repeated-measures tests (RM-ANOVA, Wilcoxon signed-rank).

participants.csv links each app session to a participant. One row per session:
    participant_id,session_id,order
    P01,20261110-140512,HA-first
    P01,20261110-141530,HA-first
    ...
Sessions that are not listed (e.g. your own test runs) are ignored.

Outputs go to the results/ folder:
    summary.md                 descriptive tables + every test result + H0 decisions
    descriptives_*.csv         the same tables as CSV (paste into Word/Excel)
    per_participant.csv        one row per participant x condition x level
    fig1..fig4 *.png           graphs for the report
"""
import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.multitest import multipletests

ALPHA = 0.05
OUT = "results"
COND_NAMES = {"haptic_audio": "Haptic + Audio", "audio_only": "Audio only"}
COND_COLORS = {"haptic_audio": "#1f6f8b", "audio_only": "#e07a1f"}
CONDS = ["haptic_audio", "audio_only"]

# Sessions left out of every analysis (pilot/test runs by the researcher).
EXCLUDE_SESSIONS = ["20261103-154558", "20261103-161152"]
# Sessions kept in the main analysis but re-run without in a sensitivity check
# (20261106-043325: 16 trials in ~71 s, mean 0.69 s per trial -> likely random tapping).
SENSITIVITY_EXCLUDE = ["20261106-043325"]
FULL_SESSION_TRIALS = 16   # sessions with fewer trials (quit early) are dropped
PAIRED = True              # set automatically in main()


# ---------------------------------------------------------------- loading
def read_csv_any(path: str) -> pd.DataFrame:
    """Reads a CSV saved as UTF-8 or UTF-16 (Windows PowerShell's `>` makes UTF-16)."""
    with open(path, "rb") as f:
        data = f.read()
    enc = "utf-16" if data.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig"
    text = data.decode(enc).replace("\r\n", "\n").replace("\r", "\n")
    # PowerShell exports sometimes wrap every line in quotes
    lines = [ln.strip().strip('"').strip() for ln in text.split("\n") if ln.strip()]
    df = pd.read_csv(io.StringIO("\n".join(lines)), dtype={"session_id": str})
    df.columns = [c.strip() for c in df.columns]
    return df


def load(trials_path, ratings_path, participants_path=None, extra_exclude=()):
    trials = read_csv_any(trials_path)
    ratings = read_csv_any(ratings_path)
    for df in (trials, ratings):
        df["session_id"] = df["session_id"].astype(str).str.strip()
    trials = trials.drop_duplicates(subset=["session_id", "level", "trial"])
    ratings = ratings.drop_duplicates(subset=["session_id", "level"])

    excluded = set(EXCLUDE_SESSIONS) | set(extra_exclude)
    counts = trials.groupby("session_id").size()
    short = set(counts[counts < FULL_SESSION_TRIALS].index)
    if short - excluded:
        print(f"Dropping incomplete sessions (< {FULL_SESSION_TRIALS} trials): {', '.join(sorted(short - excluded))}")
    excluded |= short
    trials = trials[~trials["session_id"].isin(excluded)]
    ratings = ratings[~ratings["session_id"].isin(excluded)]

    if participants_path:
        parts = read_csv_any(participants_path)
        parts["session_id"] = parts["session_id"].astype(str).str.strip()
        skipped = sorted(set(trials["session_id"]) - set(parts["session_id"]))
        if skipped:
            print(f"Ignoring {len(skipped)} session(s) not in participants.csv: {', '.join(skipped)}")
    else:
        # session mode: each session is its own unit
        parts = trials[["session_id"]].drop_duplicates()
        parts["participant_id"] = parts["session_id"]

    keep = ["session_id", "participant_id"] + (["order"] if "order" in parts else [])
    trials = trials.merge(parts[keep], on="session_id")
    ratings = ratings.merge(parts[keep], on="session_id")
    trials["completed"] = trials["completed"].astype(str).str.strip().str.lower() == "true"
    trials["time_s"] = pd.to_numeric(trials["time_from_first_touch_s"], errors="coerce")
    trials["time_s"] = trials["time_s"].fillna(pd.to_numeric(trials["time_from_prompt_s"]))
    for col in ["level", "wrong_selections", "empty_lifts", "target_w", "target_h", "target_intensity"]:
        trials[col] = pd.to_numeric(trials[col])
    ratings["level"] = pd.to_numeric(ratings["level"])
    ratings["comfort_rating"] = pd.to_numeric(ratings["comfort_rating"])
    return trials, ratings, parts


def per_participant(trials, ratings) -> pd.DataFrame:
    """One row per participant x condition x level (the unit for all tests)."""
    rows = []
    for (pid, cond, lvl), g in trials.groupby(["participant_id", "condition", "level"]):
        done = g[g["completed"]]
        wrong = g["wrong_selections"].sum()
        picks = wrong + len(done)
        rows.append({
            "participant_id": pid, "condition": cond, "level": int(lvl),
            "mean_time_s": done["time_s"].mean() if len(done) else np.nan,
            "error_rate": wrong / picks if picks else 0.0,
            "completion_rate": len(done) / len(g),
            "empty_lifts": g["empty_lifts"].sum(),
            "trials": len(g),
        })
    cells = pd.DataFrame(rows)
    comfort = (ratings.groupby(["participant_id", "condition", "level"])["comfort_rating"]
               .mean().reset_index())
    cells = cells.merge(comfort, on=["participant_id", "condition", "level"], how="left")
    cells["log_time"] = np.log(cells["mean_time_s"])
    return cells


def complete_participants(cells: pd.DataFrame, col: str) -> pd.DataFrame:
    """Keeps participants with a value in every condition x level cell (needed for RM tests)."""
    n_cells = cells.groupby("participant_id")[col].count()
    full = n_cells[n_cells == len(CONDS) * cells["level"].nunique()].index
    dropped = sorted(set(cells["participant_id"]) - set(full))
    if dropped:
        print(f"[{col}] dropping participants with missing cells: {', '.join(map(str, dropped))}")
    return cells[cells["participant_id"].isin(full)]


# ---------------------------------------------------------------- descriptives
def describe(cells: pd.DataFrame, col: str) -> pd.DataFrame:
    t = (cells.groupby(["condition", "level"])[col]
         .agg(n="count", mean="mean", median="median", sd="std").reset_index())
    t["condition"] = t["condition"].map(COND_NAMES)
    return t.round(3)


def describe_overall(cells: pd.DataFrame, col: str) -> pd.DataFrame:
    p = cells.groupby(["participant_id", "condition"])[col].mean().reset_index()
    t = p.groupby("condition")[col].agg(n="count", mean="mean", median="median", sd="std").reset_index()
    t["condition"] = t["condition"].map(COND_NAMES)
    return t.round(3)


# ---------------------------------------------------------------- tests
def fmt_p(p):
    return "< .001" if p < 0.001 else f"= {p:.3f}"


def wilcoxon_pair(a, b):
    """Wilcoxon signed-rank on paired samples. Returns dict (or None if all differences are 0)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.allclose(a - b, 0):
        return None
    res = stats.wilcoxon(a, b, zero_method="wilcox")
    p = res.pvalue
    z = stats.norm.isf(p / 2)
    return {"W": res.statistic, "p": p, "r": z / np.sqrt(len(a)), "n": len(a),
            "median_diff": float(np.median(a - b))}


def mannwhitney_pair(a, b):
    """Mann-Whitney U for independent groups (session mode)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return None
    if np.allclose(np.r_[a, b], np.r_[a, b][0]):
        return None
    res = stats.mannwhitneyu(a, b, alternative="two-sided")
    return {"U": res.statistic, "p": res.pvalue, "n1": len(a), "n2": len(b),
            "r": 2 * res.statistic / (len(a) * len(b)) - 1,   # rank-biserial (+ = haptic higher)
            "median_diff": float(np.median(a) - np.median(b))}


def compare(cells, col, lvl=None):
    """Haptic vs audio: Wilcoxon (paired mode) or Mann-Whitney (session mode)."""
    d = cells if lvl is None else cells[cells["level"] == lvl]
    p = d.groupby(["participant_id", "condition"])[col].mean().unstack()
    if not all(c in p for c in CONDS):
        return None
    if PAIRED:
        p = p.dropna()
        return wilcoxon_pair(p["haptic_audio"], p["audio_only"]) if len(p) >= 2 else None
    return mannwhitney_pair(p["haptic_audio"], p["audio_only"])


def rm_anova(cells: pd.DataFrame, col: str) -> list:
    data = complete_participants(cells, col)
    if data["participant_id"].nunique() < 2:
        return []
    res = AnovaRM(data, depvar=col, subject="participant_id",
                  within=["condition", "level"]).fit().anova_table
    out = []
    for effect, r in res.iterrows():
        F, d1, d2, p = r["F Value"], r["Num DF"], r["Den DF"], r["Pr > F"]
        out.append({"effect": effect, "F": F, "df1": d1, "df2": d2, "p": p,
                    "partial_eta_sq": F * d1 / (F * d1 + d2)})
    return out


def paired_by_level(cells, col):
    """Haptic vs audio at every level, Holm-corrected."""
    rows = []
    for lvl in sorted(cells["level"].unique()):
        r = compare(cells, col, lvl)
        if r is None:
            continue
        rows.append({"level": lvl, **r})
    if rows:
        adj = multipletests([r["p"] for r in rows], method="holm")[1]
        for r, pa in zip(rows, adj):
            r["p_holm"] = pa
    return rows


def friedman_levels(cells, col, cond):
    w = (cells[cells["condition"] == cond]
         .pivot(index="participant_id", columns="level", values=col).dropna())
    if len(w) < 2 or w.shape[1] < 3:
        return None
    if np.allclose(w.values, w.values[0, 0]):
        return None
    chi, p = stats.friedmanchisquare(*[w[c] for c in w.columns])
    return {"chi2": chi, "df": w.shape[1] - 1, "p": p, "n": len(w),
            "kendall_w": chi / (len(w) * (w.shape[1] - 1))}


def overall_pair(cells, col):
    p = cells.groupby(["participant_id", "condition"])[col].mean().unstack()
    if not all(c in p for c in CONDS):
        return None, None
    if PAIRED:
        p = p.dropna()
        diff = p["haptic_audio"] - p["audio_only"]
        shapiro = stats.shapiro(diff) if len(diff) >= 3 and diff.std() > 0 else None
        return wilcoxon_pair(p["haptic_audio"], p["audio_only"]), shapiro
    return mannwhitney_pair(p["haptic_audio"], p["audio_only"]), None


def welch_log_time(cells):
    """Session mode parametric check: Welch t-test on each session's mean log time."""
    p = cells.groupby(["participant_id", "condition"])["log_time"].mean().unstack()
    a, b = p["haptic_audio"].dropna(), p["audio_only"].dropna()
    res = stats.ttest_ind(a, b, equal_var=False)
    pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return {"t": res.statistic, "df": res.df, "p": res.pvalue,
            "d": (a.mean() - b.mean()) / pooled if pooled else 0.0,
            "ratio": float(np.exp(a.mean() - b.mean()))}


# ---------------------------------------------------------------- figures
def line_by_level(cells, col, ylabel, fname, title, ylim=None):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for i, cond in enumerate(CONDS):
        g = cells[cells["condition"] == cond].groupby("level")[col]
        m, se = g.mean(), g.sem()
        x = m.index + (i - 0.5) * 0.08
        ax.errorbar(x, m.values, yerr=se.values, marker="o", capsize=4, lw=2,
                    color=COND_COLORS[cond], label=COND_NAMES[cond])
    ax.set_xticks(sorted(cells["level"].unique()))
    ax.set_xlabel("Level (number of buttons on screen)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if ylim:
        ax.set_ylim(*ylim)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(frameon=False)
    ax.text(0.99, 0.01, "Points = mean, bars = ±1 SE", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=8, color="#555")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=200)
    plt.close(fig)


def bars_by_level(cells, col, ylabel, fname, title, ylim=None):
    levels = sorted(cells["level"].unique())
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    width = 0.38
    for i, cond in enumerate(CONDS):
        g = cells[cells["condition"] == cond].groupby("level")[col]
        m, se = g.mean().reindex(levels), g.sem().reindex(levels)
        ax.bar(np.array(levels) + (i - 0.5) * width, m.values, width, yerr=se.values,
               capsize=4, color=COND_COLORS[cond], label=COND_NAMES[cond])
    ax.set_xticks(levels)
    ax.set_xlabel("Level (number of buttons on screen)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if ylim:
        ax.set_ylim(*ylim)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=200)
    plt.close(fig)


def scatter_size(trials, fname):
    d = trials[trials["completed"]].copy()
    d["area_pct"] = d["target_w"] * d["target_h"] * 100
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for cond in CONDS:
        g = d[d["condition"] == cond]
        ax.scatter(g["area_pct"], g["time_s"], s=18, alpha=0.6,
                   color=COND_COLORS[cond], label=COND_NAMES[cond])
    ax.set_xlabel("Target button area (% of screen)")
    ax.set_ylabel("Time to complete task (s)")
    ax.set_title("Target size vs. completion time (exploratory)")
    ax.grid(alpha=0.3)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=200)
    plt.close(fig)
    rho, p = stats.spearmanr(d["area_pct"], d["time_s"]) if len(d) > 2 else (np.nan, np.nan)
    rho_i, p_i = (stats.spearmanr(d["target_intensity"], d["time_s"])
                  if len(d) > 2 and d["target_intensity"].nunique() > 1 else (np.nan, np.nan))
    return rho, p, rho_i, p_i


# ---------------------------------------------------------------- report
def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def decision(p):
    return "**reject H0**" if p < ALPHA else "fail to reject H0"


def run(trials_path, ratings_path, parts_path, out_dir, extra_exclude=(), note=""):
    global OUT, PAIRED
    OUT = out_dir
    PAIRED = parts_path is not None
    os.makedirs(OUT, exist_ok=True)

    trials, ratings, parts = load(trials_path, ratings_path, parts_path, extra_exclude)
    cells = per_participant(trials, ratings)
    cells.round(4).to_csv(os.path.join(OUT, "per_participant.csv"), index=False)
    unit = "participant" if PAIRED else "session"
    n_by_cond = cells.groupby("condition")["participant_id"].nunique()
    sessions = trials.groupby("condition")["session_id"].nunique()

    md = ["# Haptic Navigation Study – Results\n"]
    if note:
        md.append(note + "\n")
    md += [f"Mode: **{'paired (within-subject)' if PAIRED else 'session (independent groups)'}**  |  "
           f"alpha = {ALPHA}\n",
           f"Sessions analysed: Haptic + Audio = **{sessions.get('haptic_audio', 0)}**, "
           f"Audio only = **{sessions.get('audio_only', 0)}**  |  Trials: **{len(trials)}**  |  "
           f"Ratings: **{len(ratings)}**\n",
           f"Excluded sessions: {', '.join(sorted(set(EXCLUDE_SESSIONS) | set(extra_exclude)))} "
           f"(plus any session with fewer than {FULL_SESSION_TRIALS} trials).\n",
           f"All tests use one value per {unit} per condition x level "
           f"(the mean of that {unit}'s trials).\n"]
    if not PAIRED:
        md.append("Because sessions are not yet linked to participants, the two conditions are compared "
                  "as independent groups. Once participants.csv exists, run in paired mode for the "
                  "within-subject tests.\n")

    # descriptive tables
    metrics = [("mean_time_s", "Time to complete task (s)"),
               ("error_rate", "Error rate (wrong picks / all picks)"),
               ("comfort_rating", "Comfort rating (1-5)"),
               ("completion_rate", "Completion rate")]
    md.append("## Descriptive statistics\n")
    for col, name in metrics:
        t = describe(cells, col)
        t.to_csv(os.path.join(OUT, f"descriptives_{col}.csv"), index=False)
        o = describe_overall(cells, col)
        o.to_csv(os.path.join(OUT, f"descriptives_overall_{col}.csv"), index=False)
        md += [f"### {name}\n", "By condition and level:\n", md_table(t), "",
               f"Overall ({unit} mean across levels):\n", md_table(o), ""]

    md.append("## Inferential statistics\n")
    # H1 time
    if PAIRED:
        md.append("### H1, H4, H5 – Time to complete task (2 x 4 repeated-measures ANOVA on log time)\n")
        md.append("Time is log-transformed because completion times are right-skewed.\n")
        anova = rm_anova(cells, "log_time")
        if anova:
            tbl = pd.DataFrame([{"Effect": a["effect"], "F": round(a["F"], 3),
                                 "df": f"{a['df1']:.0f}, {a['df2']:.0f}", "p": fmt_p(a["p"]),
                                 "partial eta²": round(a["partial_eta_sq"], 3),
                                 "Decision": decision(a["p"])} for a in anova])
            md += [md_table(tbl), ""]
        w, sh = overall_pair(cells, "log_time")
        if sh is not None:
            md.append(f"Shapiro-Wilk on paired differences (haptic - audio, log time): "
                      f"W = {sh.statistic:.3f}, p {fmt_p(sh.pvalue)} "
                      f"({'normality OK' if sh.pvalue >= ALPHA else 'not normal → rely on the Wilcoxon result'}).\n")
        md.append(_wilcoxon_line("Overall time, haptic vs audio (non-parametric check)", w))
    else:
        md.append("### H1 – Time to complete task, Haptic + Audio vs Audio only\n")
        wl = welch_log_time(cells)
        md.append(f"Welch t-test on session mean log time: t({wl['df']:.1f}) = {wl['t']:.2f}, "
                  f"p {fmt_p(wl['p'])}, Cohen's d = {wl['d']:.2f}. Haptic + Audio times were "
                  f"{wl['ratio']:.2f}x the Audio only times (geometric mean ratio) → {decision(wl['p'])}.\n")
        w, _ = overall_pair(cells, "mean_time_s")
        md.append(_wilcoxon_line("Overall time, haptic vs audio (non-parametric check)", w))
    md += _paired_level_table(cells, "mean_time_s", "Time")
    md.append("### H4 – Effect of the number of buttons on time (Friedman across levels)\n")
    md += _friedman_lines(cells, "mean_time_s")

    # H2 errors
    md.append("### H2 – Error rate (non-parametric: error rates are bounded and usually not normal)\n")
    w, _ = overall_pair(cells, "error_rate")
    md.append(_wilcoxon_line("Overall error rate, haptic vs audio", w))
    md += _paired_level_table(cells, "error_rate", "Error rate")
    md += _friedman_lines(cells, "error_rate")

    # H3 comfort
    md.append("### H3 – Comfort rating (non-parametric: ordinal Likert data)\n")
    w, _ = overall_pair(cells, "comfort_rating")
    md.append(_wilcoxon_line("Overall comfort, haptic vs audio", w))
    md += _paired_level_table(cells, "comfort_rating", "Comfort")
    md += _friedman_lines(cells, "comfort_rating")

    # figures
    line_by_level(cells, "mean_time_s", "Time to complete task (s)",
                  "fig1_time_by_level.png", "Completion time by level and condition")
    bars_by_level(cells, "error_rate", "Error rate", "fig2_error_rate_by_level.png",
                  "Error rate by level and condition", ylim=(0, None))
    bars_by_level(cells, "comfort_rating", "Mean comfort rating (1-5)",
                  "fig3_comfort_by_level.png", "Comfort by level and condition", ylim=(0, 5.5))
    rho, p, rho_i, p_i = scatter_size(trials, "fig4_time_vs_target_size.png")

    md.append("### Exploratory – target size and vibration intensity\n")
    md.append(f"Spearman correlation, target area vs time: rho = {rho:.2f}, p {fmt_p(p)}.\n")
    if not np.isnan(rho_i):
        hap = trials[(trials["condition"] == "haptic_audio") & trials["completed"]]
        r2, p2 = stats.spearmanr(hap["target_intensity"], hap["time_s"])
        md.append(f"Spearman correlation, target vibration intensity vs time (Haptic + Audio trials only): "
                  f"rho = {r2:.2f}, p {fmt_p(p2)}.\n")
    md += ["## Figures\n",
           "![Completion time](fig1_time_by_level.png)\n",
           "![Error rate](fig2_error_rate_by_level.png)\n",
           "![Comfort](fig3_comfort_by_level.png)\n",
           "![Target size vs time](fig4_time_vs_target_size.png)\n"]

    with open(os.path.join(OUT, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"Done. Open {OUT}/summary.md and the figures in {OUT}/")


def main():
    trials_path = sys.argv[1] if len(sys.argv) > 1 else "trials.csv"
    ratings_path = sys.argv[2] if len(sys.argv) > 2 else "ratings.csv"
    parts_path = sys.argv[3] if len(sys.argv) > 3 else None
    run(trials_path, ratings_path, parts_path, "results")
    if SENSITIVITY_EXCLUDE:
        run(trials_path, ratings_path, parts_path, os.path.join("results", "sensitivity"),
            extra_exclude=SENSITIVITY_EXCLUDE,
            note=f"Sensitivity check: same analysis without session(s) "
                 f"{', '.join(SENSITIVITY_EXCLUDE)}.")


def _wilcoxon_line(label, w):
    if w is None:
        return f"{label}: no differences between conditions; test not applicable.\n"
    if "U" in w:
        return (f"{label}: Mann-Whitney U = {w['U']:.1f}, p {fmt_p(w['p'])}, rank-biserial r = {w['r']:.2f}, "
                f"n = {w['n1']} vs {w['n2']} sessions, median difference (H+A - A) = {w['median_diff']:.3f} "
                f"→ {decision(w['p'])}.\n")
    return (f"{label}: Wilcoxon W = {w['W']:.1f}, p {fmt_p(w['p'])}, r = {w['r']:.2f}, "
            f"n = {w['n']}, median difference = {w['median_diff']:.3f} → {decision(w['p'])}.\n")


def _paired_level_table(cells, col, name):
    rows = paired_by_level(cells, col)
    if not rows:
        return []
    if PAIRED:
        t = pd.DataFrame([{"Level": r["level"], "n": r["n"],
                           "Median diff (H+A - A)": round(r["median_diff"], 3),
                           "W": round(r["W"], 1), "p (Holm)": fmt_p(r["p_holm"]),
                           "r": round(r["r"], 2)} for r in rows])
        test = "Wilcoxon signed-rank"
    else:
        t = pd.DataFrame([{"Level": r["level"], "n (H+A / A)": f"{r['n1']} / {r['n2']}",
                           "Median diff (H+A - A)": round(r["median_diff"], 3),
                           "U": round(r["U"], 1), "p (Holm)": fmt_p(r["p_holm"]),
                           "rank-biserial r": round(r["r"], 2)} for r in rows])
        test = "Mann-Whitney U"
    return [f"{name}, haptic vs audio at each level ({test}, Holm-corrected):\n", md_table(t), ""]


def _friedman_lines(cells, col):
    out = []
    for cond in CONDS:
        f = friedman_levels(cells, col, cond)
        if f is None:
            out.append(f"Friedman across levels ({COND_NAMES[cond]}): no variation; not applicable.\n")
        else:
            out.append(f"Friedman across levels ({COND_NAMES[cond]}): chi²({f['df']}) = {f['chi2']:.2f}, "
                       f"p {fmt_p(f['p'])}, Kendall's W = {f['kendall_w']:.2f} → {decision(f['p'])}.\n")
    return out


if __name__ == "__main__":
    main()
