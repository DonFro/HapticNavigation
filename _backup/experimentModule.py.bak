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

# 2x2 grid of slots (center_x, center_y)
SLOTS = [(0.28, 0.68), (0.72, 0.68), (0.28, 0.32), (0.72, 0.32)]
BUTTON_SIZE = (0.40, 0.25)


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

    # assign random button layouts for each trial
    trials = []
    for i, target in enumerate(targets, start=1):
        slots = random.sample(range(len(SLOTS)), level)
        layout = dict(zip(labels, slots))
        trials.append({"level": level, "trial": i, "target": target, "layout": layout})
        
    return trials


class ResultLogger:
    """Appends results to CSV files that survive between sessions."""

    # CSV column headers
    TRIAL_FIELDS = [
        "session_id", "condition", "level", "num_buttons", "trial", "target",
        "target_slot", "completed", "time_from_prompt_s", "time_from_first_touch_s",
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