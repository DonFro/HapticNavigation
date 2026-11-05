# Imported libraries
import csv
import io
import statistics
import sys
from collections import defaultdict

# Input file paths
trials_path = sys.argv[1] if len(sys.argv) > 1 else "trials.csv"
ratings_path = sys.argv[2] if len(sys.argv) > 2 else "ratings.csv"


def open_csv(path: str) -> io.StringIO:
    """Opens a CSV saved as UTF-8 or UTF-16.

    Windows PowerShell's `>` saves files as UTF-16, which plain open() can't read.
    """
    with open(path, "rb") as f:
        data = f.read()
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = data.decode("utf-16")
    else:
        text = data.decode("utf-8-sig")
    return io.StringIO(text, newline="")


# Load trial data
groups = defaultdict(list)
with open_csv(trials_path) as f:
    for row in csv.DictReader(f):
        groups[(row["condition"], int(row["level"]))].append(row)

# Load rating data
ratings = defaultdict(list)
try:
    with open_csv(ratings_path) as f:
        for row in csv.DictReader(f):
            ratings[(row["condition"], int(row["level"]))].append(int(row["comfort_rating"]))
except FileNotFoundError:
    pass

# Print summary header
print(f"{'condition':<14}{'lvl':>4}{'trials':>8}{'done%':>8}{'mean_t':>9}{'sd_t':>8}"
      f"{'err_rate':>10}{'empty':>7}{'comfort':>9}")

# Calculate and display metrics per group
for key in sorted(groups):
    # filter completed trials and extract times
    rows = groups[key]
    done = [r for r in rows if r["completed"] == "True"]
    times = [float(r["time_from_first_touch_s"] or r["time_from_prompt_s"]) for r in done]

    # calculate error rate and empty lifts
    wrong = sum(int(r["wrong_selections"]) for r in rows)
    err_rate = wrong / (wrong + len(done)) if (wrong + len(done)) else 0
    empty = sum(int(r["empty_lifts"]) for r in rows)

    # compute summary statistics
    mean_t = statistics.mean(times) if times else float("nan")
    sd_t = statistics.stdev(times) if len(times) > 1 else 0.0
    comfort = statistics.mean(ratings[key]) if ratings[key] else float("nan")

    # print formatted row
    print(f"{key[0]:<14}{key[1]:>4}{len(rows):>8}{100*len(done)/len(rows):>7.0f}%"
          f"{mean_t:>9.2f}{sd_t:>8.2f}{err_rate:>10.2f}{empty:>7}{comfort:>9.2f}")