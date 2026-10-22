import csv
import os
import random
import time

# ---------------- Experiment settings (edit these) ----------------
BUTTON_LABELS = ["Purchase", "Add to Cart", "Wishlist", "Back"]
NUM_LEVELS = 4              # level N shows N buttons
TRIALS_PER_LEVEL = 4        # how many "find the button" tasks per level
TRIAL_TIMEOUT_S = 60        # give up on a trial after this many seconds
PAUSE_BETWEEN_TRIALS_S = 1.5

# 2x2 grid of slots (center_x, center_y). Buttons are placed in random slots
# each trial so participants can't memorise positions. Button size stays the
# same at every level, so only the number of buttons changes.
SLOTS = [(0.28, 0.68), (0.72, 0.68), (0.28, 0.32), (0.72, 0.32)]
BUTTON_SIZE = (0.40, 0.25)


def build_level_trials(level: int) -> list:
    """Returns a list of trials for a level.

    Each trial is a dict: target label + where each button goes.
    Targets are spread evenly across the level's buttons.
    """
    labels = BUTTON_LABELS[:level]
    targets = []
    while len(targets) < TRIALS_PER_LEVEL:
        batch = labels[:]
        random.shuffle(batch)
        targets.extend(batch)
    targets = targets[:TRIALS_PER_LEVEL]

    trials = []
    for i, target in enumerate(targets, start=1):
        slots = random.sample(range(len(SLOTS)), level)
        layout = dict(zip(labels, slots))  # label -> slot index
        trials.append({"level": level, "trial": i, "target": target, "layout": layout})
    return trials


class ResultLogger:
    """Appends results to CSV files that survive between sessions."""

    TRIAL_FIELDS = [
        "session_id", "condition", "level", "num_buttons", "trial", "target",
        "target_slot", "completed", "time_from_prompt_s", "time_from_first_touch_s",
        "wrong_selections", "empty_lifts", "buttons_entered", "timestamp",
    ]
    RATING_FIELDS = ["session_id", "condition", "level", "comfort_rating", "timestamp"]

    def __init__(self, folder: str, condition: str):
        os.makedirs(folder, exist_ok=True)
        self.session_id = time.strftime("%Y%m%d-%H%M%S")
        self.condition = condition
        self.trials_path = os.path.join(folder, "trials.csv")
        self.ratings_path = os.path.join(folder, "ratings.csv")
        print(f"RESULTS FOLDER: {folder}")

    def _append(self, path: str, fields: list, row: dict) -> None:
        new_file = not os.path.exists(path)
        with open(path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            if new_file:
                writer.writeheader()
            writer.writerow(row)
        # also print to the log as a backup you can read with adb logcat
        print("RESULT," + ",".join(str(row[k]) for k in fields))

    def log_trial(self, row: dict) -> None:
        row = dict(row, session_id=self.session_id, condition=self.condition,
                   timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))
        self._append(self.trials_path, self.TRIAL_FIELDS, row)

    def log_rating(self, level: int, rating: int) -> None:
        row = {"session_id": self.session_id, "condition": self.condition,
               "level": level, "comfort_rating": rating,
               "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
        self._append(self.ratings_path, self.RATING_FIELDS, row)
