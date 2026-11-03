# Haptic Navigation Study – Experiment Design

## Task
Each trial the app says "Find <target>". The participant slides a finger
around the screen. Entering a button vibrates (Haptic + Audio condition only)
and speaks its name. Lifting the finger on a button selects it.

- Correct button: "Correct", next trial after 1.5 s
- Wrong button: "Wrong. Find <target>" (counted as an error, trial continues)
- Lift on empty space: repeats the prompt (counted as an empty lift, not an error)
- No correct selection in 60 s: trial marked not completed

## Levels
| Level | Buttons on screen                         |
|-------|-------------------------------------------|
| 1     | Purchase                                  |
| 2     | Purchase, Add to Cart                     |
| 3     | Purchase, Add to Cart, Wishlist           |
| 4     | Purchase, Add to Cart, Wishlist, Back     |

- 4 trials per level (16 per session); targets spread evenly over the level's buttons
- Buttons are placed in random cells of a 2x2 grid every trial, so positions can't be memorised
- Button size is the same at every level, so only the number of buttons changes

## Conditions
- Haptic + Audio: vibration + speech on entering a button
- Audio only: speech only (baseline to show what the vibration adds)

Run each participant in both conditions and alternate which one comes first
(participant 1: haptic first, participant 2: audio first, ...) so learning
doesn't favour one condition.

## Metrics
Quantitative (trials.csv)
- Time to complete task: time_from_first_touch_s (first touch to correct selection).
  time_from_prompt_s also includes the time spent listening to the prompt.
- Error rate: wrong_selections / (wrong_selections + correct selections), per level
- Also logged: completed, empty_lifts, buttons_entered (how much exploring was needed)

Qualitative (ratings.csv)
- Comfort rating 1-5 after every level (participant says it, facilitator taps it)
- Recommended after each condition: a short interview, and optionally the
  System Usability Scale (SUS) questionnaire on paper

## Procedure (per participant)
1. Explain the task; 1-2 minutes of free practice
2. Facilitator picks the condition on the start screen and hands over the phone
3. Participant completes levels 1-4, giving a comfort rating after each
4. Repeat with the other condition
5. Note the session IDs shown on the end screen next to the participant's number

To simulate users who can't see the screen, have participants close their
eyes or wear a blindfold, or cover the screen.

## Getting the data off the phone
```bash
adb.exe shell run-as <package.domain>.<package.name> cat files/trials.csv > trials.csv
adb.exe shell run-as <package.domain>.<package.name> cat files/ratings.csv > ratings.csv
python analyze.py trials.csv ratings.csv
```
Backup: every row is also printed to the log as a line starting with RESULT,
```bash
adb.exe logcat -d -s python | grep RESULT
```
