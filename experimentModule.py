# Imported libraries
import csv
import os
import random
import time

# Experiment settings
BUTTON_LABELS = ["Purchase", "Add to Cart", "Wishlist", "Back"]
NUM_LEVELS = 4
TRIALS_PER_LEVEL = 4
TRIAL_TIMEOUT_S = 60
PAUSE_BETWEEN_TRIALS_S = 1.5
RATING_SCREEN_VIBRATES = True

# Vibration intensity for each button (0.0 = off, 1.0 = strongest).
# Each button keeps its own intensity every trial, so participants can learn
# to tell buttons apart by feel.
BUTTON_INTENSITY = {
    "Purchase": 1.0,
    "Add to Cart": 0.7,
    "Wishlist": 0.45,
    "Back": 0.25,
}
RATING_INTENSITY = 1.0

# Random button sizes, as fractions of screen width / height.
# The minimums keep every button comfortably touchable.
BUTTON_WIDTH_RANGE = (0.20, 0.45)
BUTTON_HEIGHT_RANGE = (0.08, 0.22)
SCREEN_MARGIN = 0.03   # keep buttons this far from the screen edges
BUTTON_GAP = 0.03      # minimum space between two buttons


def _overlaps(a: dict, b: dict, gap: float) -> bool:
    """True if two buttons (center x/y, width w, height h) overlap or are too close."""
    return (abs(a["x"] - b["x"]) < (a["w"] + b["w"]) / 2 + gap and
            abs(a["y"] - b["y"]) < (a["h"] + b["h"]) / 2 + gap)


def random_layout(labels: list) -> dict:
    """Places each button at a random spot with a random size, without overlaps.

    Returns {label: {"x", "y", "w", "h"}} where x/y is the button center and
    every value is a fraction of the screen (0-1).
    """
    for _attempt in range(200):
        placed = {}
        for label in labels:
            for _try in range(300):
                w = random.uniform(*BUTTON_WIDTH_RANGE)
                h = random.uniform(*BUTTON_HEIGHT_RANGE)
                box = {
                    "x": random.uniform(SCREEN_MARGIN + w / 2, 1 - SCREEN_MARGIN - w / 2),
                    "y": random.uniform(SCREEN_MARGIN + h / 2, 1 - SCREEN_MARGIN - h / 2),
                    "w": w,
                    "h": h,
                }
                if not any(_overlaps(box, other, BUTTON_GAP) for other in placed.values()):
                    placed[label] = {k: round(v, 3) for k, v in box.items()}
                    break
            else:
                break  # couldn't fit this button; start the layout over
        if len(placed) == len(labels):
            return placed
    raise RuntimeError("Could not fit buttons; lower BUTTON_WIDTH_RANGE / BUTTON_HEIGHT_RANGE")


def build_level_trials(level: int) -> list:
    """Randomized trial setup for a level."""
    # generate evenly distributed target sequence
    labels = BUTTON_LABELS[:level]
    targets = []
    while len(targets) < TRIALS_PER_LEVEL:
        batch = labels[:]
        random.shuffle(batch)
        targets.extend(batch)
    targets = targets[:TRIALS_PER_LEVEL]

    # new random positions and sizes for every trial
    trials = []
    for i, target in enumerate(targets, start=1):
        trials.append({"level": level, "trial": i, "target": target,
                       "layout": random_layout(labels)})

    return trials


class ResultLogger:
    """Appends results to CSV files that survive between sessions."""

    # CSV column headers
    TRIAL_FIELDS = [
        "session_id", "condition", "level", "num_buttons", "trial", "target",
        "target_x", "target_y", "target_w", "target_h", "target_intensity", "completed", "time_from_prompt_s", "time_from_first_touch_s",
        "wrong_selections", "empty_lifts", "buttons_entered", "timestamp",
    ]
    RATING_FIELDS = ["session_id", "condition", "level", "comfort_rating", "timestamp"]

    def __init__(self, folder: str, condition: str):
        """Initializes logging directories and file paths."""
        # configure session metadata
        os.makedirs(folder, exist_ok=True)
        self.session_id = time.strftime("%Y%m%d-%H%M%S")
        self.condition = condition

        # set output file paths
        self.trials_path = os.path.join(folder, "trials.csv")
        self.ratings_path = os.path.join(folder, "ratings.csv")
        print(f"RESULTS FOLDER: {folder}")

    def _append(self, path: str, fields: list, row: dict) -> None:
        """Writes a row to a CSV file."""
        # if an older file has different columns, keep it under a new name
        if os.path.exists(path):
            with open(path, newline="") as f:
                header = next(csv.reader(f), [])
            if header != fields:
                stem, ext = os.path.splitext(path)
                os.rename(path, f"{stem}_old_{time.strftime('%Y%m%d-%H%M%S')}{ext}")

        # write row and add header if file is new
        new_file = not os.path.exists(path)
        with open(path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            if new_file:
                writer.writeheader()
            writer.writerow(row)

        # print console backup
        print("RESULT," + ",".join(str(row[k]) for k in fields))

    def log_trial(self, row: dict) -> None:
        """Formats and saves trial metric data."""
        # attach session metadata
        row = dict(row, session_id=self.session_id, condition=self.condition,
                   timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))

        # append to trials csv
        self._append(self.trials_path, self.TRIAL_FIELDS, row)

    def log_rating(self, level: int, rating: int) -> None:
        """Formats and saves user comfort rating data."""
        # build rating record
        row = {"session_id": self.session_id, "condition": self.condition,
               "level": level, "comfort_rating": rating,
               "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}

        # append to ratings csv
        self._append(self.ratings_path, self.RATING_FIELDS, row)