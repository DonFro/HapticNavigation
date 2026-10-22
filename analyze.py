"""Summarise trials.csv and ratings.csv per condition and level.

Run on your PC (not the phone):  python analyze.py trials.csv ratings.csv
"""
import csv
import statistics
import sys
from collections import defaultdict

trials_path = sys.argv[1] if len(sys.argv) > 1 else "trials.csv"
ratings_path = sys.argv[2] if len(sys.argv) > 2 else "ratings.csv"

groups = defaultdict(list)
with open(trials_path, newline="") as f:
    for row in csv.DictReader(f):
        groups[(row["condition"], int(row["level"]))].append(row)

ratings = defaultdict(list)
try:
    with open(ratings_path, newline="") as f:
        for row in csv.DictReader(f):
            ratings[(row["condition"], int(row["level"]))].append(int(row["comfort_rating"]))
except FileNotFoundError:
    pass

print(f"{'condition':<14}{'lvl':>4}{'trials':>8}{'done%':>8}{'mean_t':>9}{'sd_t':>8}"
      f"{'err_rate':>10}{'empty':>7}{'comfort':>9}")
for key in sorted(groups):
    rows = groups[key]
    done = [r for r in rows if r["completed"] == "True"]
    times = [float(r["time_from_first_touch_s"] or r["time_from_prompt_s"]) for r in done]
    wrong = sum(int(r["wrong_selections"]) for r in rows)
    # error rate = wrong selections / all button selections (wrong + correct)
    err_rate = wrong / (wrong + len(done)) if (wrong + len(done)) else 0
    empty = sum(int(r["empty_lifts"]) for r in rows)
    mean_t = statistics.mean(times) if times else float("nan")
    sd_t = statistics.stdev(times) if len(times) > 1 else 0.0
    comfort = statistics.mean(ratings[key]) if ratings[key] else float("nan")
    print(f"{key[0]:<14}{key[1]:>4}{len(rows):>8}{100*len(done)/len(rows):>7.0f}%"
          f"{mean_t:>9.2f}{sd_t:>8.2f}{err_rate:>10.2f}{empty:>7}{comfort:>9.2f}")
