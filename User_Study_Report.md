# User Study: Vibrotactile and Audio Feedback for Non-Visual Touchscreen Navigation

Project: HapticNavigation  
Course: [course name and number]  
Team: [names]  
Date: [date]

Text in [brackets] still needs to be filled in. The Results and Discussion sections are filled in after the sessions, using the output of `analyze_study.py`.

---

## 1. Research Questions

Our project explores how well vibration helps visually impaired users navigate touchscreen interfaces when it is paired with audio cues. The study asks:

- **RQ1:** Does adding vibrotactile feedback to audio cues reduce the time needed to find and select a target button on a touchscreen without vision?
- **RQ2:** Does adding vibrotactile feedback reduce selection errors?
- **RQ3:** Does adding vibrotactile feedback change how comfortable users feel while navigating?
- **RQ4:** How does interface complexity (the number of buttons on screen) affect time, errors and comfort, and does the benefit of vibration grow as the interface becomes more complex?

## 2. Variables

### Independent variables

| Variable | Levels | Type |
|---|---|---|
| Feedback modality | (1) Haptic + Audio: the phone vibrates continuously while the finger is on a button, at an intensity specific to that button, and speaks the button's name. (2) Audio only: the button's name is spoken with no vibration. | Within-subject |
| Interface complexity | Level 1, 2, 3 or 4 buttons on screen | Within-subject |

### Dependent variables

| Variable | Definition | How it is measured |
|---|---|---|
| Time to complete task | Seconds from the participant's first touch to lifting the finger on the correct button | Logged automatically by the app (`time_from_first_touch_s`) with a high-resolution timer |
| Error rate | Wrong-button selections divided by all button selections (wrong + correct), per level | Logged automatically (`wrong_selections`, `completed`) |
| Comfort | "How comfortable was this level?", rated 1 (very uncomfortable) to 5 (very comfortable) | Rated in the app after every level (`comfort_rating`) |

Secondary measures, also logged automatically: completion rate (trials finished within 60 s), empty lifts (finger lifted on blank space), buttons entered (how much exploring was needed), and the target's size, position and vibration intensity on every trial.

## 3. Hypotheses

| | Null hypothesis (H0) | Alternative hypothesis (H1) | Why we expect H1 |
|---|---|---|---|
| H1 Time | Mean completion time is the same in both conditions: μ(H+A) = μ(A) | Completion time is lower with haptic feedback: μ(H+A) < μ(A) | Vibration starts the instant the finger crosses a button's edge, while speech takes a moment to start and finish. Vibration also tells users they are on a button before the label is spoken. |
| H2 Errors | Error rate is the same in both conditions | Error rate is lower with haptic feedback | Continuous vibration confirms the finger is still on the button before lifting. Per-button intensities give a second cue to the button's identity. |
| H3 Comfort | Comfort ratings are the same in both conditions | Comfort is higher with haptic feedback | Two confirming channels should reduce uncertainty while searching without vision. |
| H4 Complexity | Completion time is the same at all four levels | Completion time increases with the number of buttons | More buttons means more area to explore and more labels to listen to before finding the target. |
| H5 Interaction | The effect of feedback modality on time is the same at every level | The haptic advantage grows as the number of buttons increases | With one button the target is easy to find either way; with four, faster edge detection should save more time. |

## 4. Method

### 4.1 Apparatus

- One Android smartphone, used for every participant: [phone model, Android version, screen size]. Using the same device for everyone controls vibration motor strength, screen size and audio quality.
- The HapticNavigation app (Kivy/Python). On each trial the app says "Find [target]". The participant slides one finger across the screen. Entering a button speaks its name and, in the Haptic + Audio condition, vibrates continuously until the finger leaves the button. Lifting the finger on a button selects it.
- Buttons: Purchase, Add to Cart, Wishlist and Back, styled after an online-shopping interface. Each trial places every button at a random position, with a random size (20–45% of screen width, 8–22% of screen height) and no overlap, so positions can't be memorized.
- Vibration intensity per button: Purchase 1.0, Add to Cart 0.7, Wishlist 0.45, Back 0.25.
- A blindfold or sleep mask, so sighted participants complete the task without vision.

### 4.2 Location

Sessions take place in a quiet, closed room on campus ([building/room]). One facilitator and one participant are present. The participant sits at a table with the phone in portrait orientation, flat on the table in front of them. The room, lighting, seating and phone position are the same for every session.

### 4.3 Participants

- **Target:** at least 10 participants, aiming for 12 so the two condition orders have equal groups (6 and 6).
- **Population:** university students aged 18 or older, with an even split of men and women where possible. Participants must have normal hearing and be able to feel phone vibrations. Anyone who uses a screen reader daily is recorded separately, since that experience could affect performance.
- **Why students:** students are readily available on campus, and the study tests a basic interaction technique (finding a target by touch) rather than a full assistive product. Using blindfolded sighted students for early-stage haptic interface studies is common; for example, Kokkonis et al. evaluated smartphone vibration patterns with 20 blindfolded university students. We acknowledge the limitation that blindfolded sighted users are not the same as people who are blind or visually impaired (see 4.9 Validity), and validating the design with visually impaired users is named as future work.

### 4.4 Recruitment

Participants are recruited through [class announcements, department email lists, flyers in campus buildings, and word of mouth]. The message describes a roughly 30-minute study about using a phone without looking at it. Participation is voluntary and unpaid [or: compensated with ___]. Volunteers pick a time slot through [a sign-up sheet or form].

### 4.5 Study design and counterbalancing

The study uses a **2 × 4 within-subject design** (feedback modality × interface complexity): every participant completes both conditions at all four levels. A within-subject design suits a small sample (10–12 people), because each participant serves as their own control, which removes differences in skill and touch sensitivity between people.

- **Counterbalancing of condition:** half the participants start with Haptic + Audio and half start with Audio only, alternating by participant number (odd numbers start with Haptic + Audio, even numbers with Audio only). This balances learning and fatigue effects across the two conditions.
- **Levels:** levels always run from 1 to 4, so the interface grows gradually more complex, as it would in a real app. Because this order is fixed, practice could partly mix with the level effect. To reduce that, participants get a practice round before data collection, and layouts change randomly every trial, so participants can't learn positions.
- **Trials:** 4 trials per level × 4 levels × 2 conditions = 32 measured trials per participant. Within each level, every button is the target equally often, in random order.

### 4.6 Controlled variables

| Variable | How it is controlled |
|---|---|
| Device, screen size, vibration motor | Same phone for all participants |
| Speech voice, rate and volume | Same text-to-speech settings; volume fixed at [__]% |
| Vibration intensities | Fixed values for each button, the same for all participants |
| Phone position and grip | Portrait, flat on the table; dominant index finger only |
| Vision | Blindfold for every participant during all trials |
| Button labels and number of trials | Identical for every participant and condition |
| Button positions and sizes | Randomized every trial, to prevent memorization |
| Instructions | Read from the same script to every participant |
| Environment | Same quiet room, same time limit (60 s per trial), same break length |

### 4.7 Procedure (about 30 minutes)

1. **Welcome and consent (3 min):** explain the study, answer questions, and have the participant sign the consent form (Appendix C).
2. **Background questionnaire (3 min):** on paper or [Google Forms] (Appendix A). The facilitator assigns a participant ID (P01, P02, …) and notes the condition order.
3. **Instructions and practice (3 min):** the facilitator reads the script. The participant then does a short practice run without the blindfold, then with it. Practice sessions are not added to `participants.csv`, so they are left out of the analysis.
4. **Condition 1 (about 5 min):** the facilitator selects the condition on the start screen and puts on the participant's blindfold. The participant completes levels 1–4. After each level, the app asks for a comfort rating; the participant says or chooses a number from 1 to 5.
5. **Post-condition questionnaire (3 min):** with the blindfold off (Appendix B, Part 1). The facilitator writes down the session ID shown on the end screen.
6. **Break (2 min).**
7. **Condition 2 (about 5 min):** same as step 4 with the other condition.
8. **Post-condition and final questionnaires (5 min):** Appendix B, Part 1 for condition 2, then Part 2, which compares the two conditions.
9. **Debrief (1 min):** thank the participant, explain the hypotheses, and answer questions.

### 4.8 When and how the questionnaires are given

| When | What | How |
|---|---|---|
| Before the experiment | Background questionnaire (Appendix A) | Paper or online form, no blindfold |
| After each level | Comfort rating, 1–5 | In the app: the question is spoken, and the participant slides to a number and lifts to choose it |
| After each condition | Post-condition questionnaire (Appendix B, Part 1) | Paper or online form, blindfold removed |
| At the end | Comparison questionnaire (Appendix B, Part 2) | Paper or online form |

### 4.9 Validity

**Internal validity**

- *Order and learning effects:* condition order is counterbalanced, a practice round comes before the measured trials, and random layouts prevent learning positions.
- *Fatigue:* sessions are short (about 10 minutes of trials in total), with a break between conditions.
- *Fixed level order:* levels always increase from 1 to 4, so practice could add to the level effect; this is acknowledged as a limitation.
- *Experimenter bias:* scripted instructions; timing and errors are recorded by the app, not by the facilitator.
- *Audible vibration:* the vibration motor makes a faint sound, so participants may partly hear the vibration as well as feel it. This is noted as a limitation.
- *Device differences:* removed by using one phone.

**External validity**

- *Population:* blindfolded sighted students lack the touch skills, strategies and screen reader experience of people who are blind or visually impaired, so results may not transfer directly to that group.
- *Task realism:* the task uses 1–4 labelled buttons on an otherwise empty screen. Real apps have more elements, scrolling and text.
- *Sample and device:* a small student sample and one phone model limit how far the results generalize to other people and phones.

### 4.10 Measuring the dependent variables

- **Time and errors:** the app logs every trial to `trials.csv` on the phone: time from the first touch and from the spoken prompt, wrong selections, empty lifts, buttons entered, whether the trial was completed within 60 s, and the target's position, size and vibration intensity.
- **Comfort:** stored in `ratings.csv`, one rating per level per condition.
- **Questionnaires:** typed into a spreadsheet by participant ID.
- **Linking the data:** `participants.csv` maps each app session ID to a participant ID, as recorded by the facilitator.

## 5. Data Analysis Plan

`analyze_study.py` runs every analysis below and saves the tables, graphs and test results to `results/`.

1. **Unit of analysis:** for each participant, condition and level, the mean completion time of completed trials, the error rate and the comfort rating.
2. **Descriptive statistics:** mean, median and standard deviation of every dependent variable, by condition and level and overall.
3. **Completion time (H1, H4, H5):** a 2 × 4 repeated-measures ANOVA (modality × complexity) on log-transformed time (log time because completion times are right-skewed). Reported: F, degrees of freedom, p and partial eta². The normality of paired differences is checked with Shapiro-Wilk, and a Wilcoxon signed-rank test is reported as a non-parametric check. Haptic vs audio is also compared at each level with Wilcoxon tests, Holm-corrected for 4 comparisons.
4. **Error rate (H2) and comfort (H3):** these are bounded or ordinal and usually not normally distributed, so they use non-parametric tests. A Wilcoxon signed-rank test compares the two conditions overall and at each level (Holm-corrected), and a Friedman test checks for differences across the four levels within each condition. Effect sizes: r for Wilcoxon, Kendall's W for Friedman.
5. **Exploratory:** Spearman correlations between target size and completion time, and between target vibration intensity and completion time.
6. **Decision rule:** α = .05. H0 is rejected when p < .05.
7. **Questionnaires:** Likert items are summarized with medians and compared between conditions with Wilcoxon tests. Open-ended answers are grouped into common themes.

To run it:

```
py -m pip install pandas scipy statsmodels matplotlib
py analyze_study.py trials.csv ratings.csv participants.csv
```

## 6. Pilot Test

A researcher completed one full Haptic + Audio session to test the app and the data pipeline. Mean completion times were 3.37 s (level 1), 2.98 s (level 2), 3.33 s (level 3) and 6.18 s (level 4), with no wrong selections. The jump at level 4 suggests complexity has a measurable effect. Pilot data is excluded from the analysis.

## 7. Results

[After the sessions, paste the tables from `results/summary.md` and insert the figures below.]

### 7.1 Participants

[N = __ (__ men, __ women, __ other / prefer not to say), aged __–__ (M = __, SD = __). __ participants used a screen reader regularly. __ started with Haptic + Audio and __ with Audio only.]

### 7.2 Descriptive statistics

[Tables: time, error rate and comfort by condition and level, from `results/descriptives_*.csv`.]

### 7.3 Inferential statistics

[ANOVA table for time; Wilcoxon and Friedman results for errors and comfort, from `results/summary.md`.]

Figures:

- Figure 1. Completion time by level and condition (`results/fig1_time_by_level.png`)
- Figure 2. Error rate by level and condition (`results/fig2_error_rate_by_level.png`)
- Figure 3. Comfort by level and condition (`results/fig3_comfort_by_level.png`)
- Figure 4. Target size vs completion time (`results/fig4_time_vs_target_size.png`)

### 7.4 Can we reject the null hypotheses?

| Hypothesis | Test | Result | Decision |
|---|---|---|---|
| H1 Time | RM-ANOVA, modality effect | F(1, __) = __, p = __ | [Reject / Fail to reject H0] |
| H2 Errors | Wilcoxon signed-rank | W = __, p = __ | [ ] |
| H3 Comfort | Wilcoxon signed-rank | W = __, p = __ | [ ] |
| H4 Complexity | RM-ANOVA, level effect | F(3, __) = __, p = __ | [ ] |
| H5 Interaction | RM-ANOVA, modality × level | F(3, __) = __, p = __ | [ ] |

## 8. Discussion

[Points to cover:]

- What the data indicate for each research question, using means and effect sizes as well as p-values.
- Whether the haptic advantage grew with the number of buttons (Figure 1).
- Whether participants used the different vibration intensities to tell buttons apart (from the questionnaire and the intensity correlation).
- Subjective findings: the preference question and themes from the open-ended answers.
- Limitations: blindfolded sighted students, fixed level order, audible vibration motor, one phone, small sample.
- Future work: test with blind and visually impaired participants, compare vibration patterns as well as intensities, and use more realistic app screens.

---

## Appendix A – Background Questionnaire

Participant ID: ______ (filled in by the facilitator)

1. Age: ______
2. Gender: ☐ Woman ☐ Man ☐ Non-binary ☐ Prefer to self-describe: ______ ☐ Prefer not to say
3. Current status: ☐ Undergraduate ☐ Graduate student ☐ Staff/Faculty ☐ Other: ______
4. Field of study: ______
5. Dominant hand: ☐ Right ☐ Left ☐ Both
6. How would you describe your vision (with glasses or contacts if you wear them)? ☐ Normal ☐ Low vision ☐ Blind ☐ Prefer not to say
7. Do you have any difficulty hearing speech from a phone speaker? ☐ No ☐ Yes
8. Do you have any condition that reduces touch sensitivity in your fingers? ☐ No ☐ Yes ☐ Prefer not to say
9. Which phone do you use most? ☐ Android ☐ iPhone ☐ Other ☐ None
10. How many hours per day do you use a smartphone? ☐ Less than 1 ☐ 1–3 ☐ 3–5 ☐ More than 5
11. How often have you used a screen reader (TalkBack, VoiceOver)? ☐ Never ☐ Tried once or twice ☐ Sometimes ☐ Daily
12. How often do you play games or use apps that rely on vibration feedback? ☐ Never ☐ Rarely ☐ Sometimes ☐ Often
13. How comfortable are you using a phone without looking at it? (1 = not at all, 5 = very) 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 ☐

## Appendix B – Experiment Feedback Questionnaire

### Part 1 – After each condition

Participant ID: ______ Condition: ☐ Haptic + Audio ☐ Audio only

Rate how much you agree (1 = strongly disagree, 5 = strongly agree):

| Statement | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 1. It was easy to find the button I was asked for. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2. I always knew when my finger was on a button. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3. I was confident I was selecting the correct button. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4. The feedback was fast enough. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 5. The task required a lot of mental effort. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 6. I felt comfortable using the app without seeing the screen. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7. The feedback was annoying or distracting. | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8. (Haptic + Audio only) I could tell buttons apart by how strongly they vibrated. | ☐ | ☐ | ☐ | ☐ | ☐ |

9. What made finding the buttons easier or harder in this condition? ____________________

### Part 2 – At the end (comparing both conditions)

10. Which condition did you prefer? ☐ Haptic + Audio ☐ Audio only ☐ No preference
11. In which condition did you feel faster? ☐ Haptic + Audio ☐ Audio only ☐ No difference
12. As more buttons appeared, which condition stayed easier? ☐ Haptic + Audio ☐ Audio only ☐ No difference
13. Did you rely more on the vibration or on the speech when both were available? ☐ Mostly vibration ☐ Both equally ☐ Mostly speech
14. Would you want vibration feedback like this in apps you use every day? ☐ Yes ☐ Maybe ☐ No
15. What would you change about the vibration or audio feedback? ____________________
16. Any other comments? ____________________

## Appendix C – Consent Form

**Study title:** Vibrotactile and Audio Feedback for Non-Visual Touchscreen Navigation  
**Researchers:** [names], [department], [university]. Contact: [email]  
**Supervisor:** [instructor name], [email]

**Purpose.** This study tests whether phone vibration, combined with spoken audio, helps people find buttons on a touchscreen without looking. The results will be used in a course project report.

**What you will do.** You will fill in a short background questionnaire. Then, wearing a blindfold, you will slide your finger across a phone screen to find buttons named by the app, under two feedback conditions. After each part you will rate your comfort and answer a short questionnaire. The session takes about 30 minutes.

**Risks and discomfort.** Risks are minimal. You may find the blindfold or the vibration uncomfortable. You can remove the blindfold, take a break or stop at any time.

**Benefits.** There is no direct benefit to you. Your participation helps improve accessible interface design for people with visual impairments.

**Voluntary participation.** Taking part is voluntary. You may skip any question, and you may withdraw at any time without giving a reason and without any penalty. If you withdraw, your data will be deleted on request.

**Confidentiality.** You will be identified only by a participant ID (for example, P04). Your name appears only on this form, which is stored separately from the data. The app records touch timing, button selections and ratings. No audio, video, photos or personal data are recorded. Data are stored on [password-protected device/storage] and reported only as group results. Data will be deleted [at the end of the semester / date].

**Compensation.** [None / describe]

**Questions.** Contact [researcher email] or [instructor email]. [If required: questions about your rights as a participant can go to the university IRB at ___.]

By signing below, I confirm that I am at least 18 years old, have read and understood this form, have had the chance to ask questions, and agree to take part.

Participant name: ________________________ Signature: ________________________ Date: ________

Researcher name: ________________________ Signature: ________________________ Date: ________

## Appendix D – Facilitator Session Sheet

| Participant ID | Order | Session 1 ID | Session 2 ID | Notes |
|---|---|---|---|---|
| P01 | Haptic + Audio first | | | |
| P02 | Audio only first | | | |
| P03 | Haptic + Audio first | | | |
| P04 | Audio only first | | | |
| P05 | Haptic + Audio first | | | |
| P06 | Audio only first | | | |
| P07 | Haptic + Audio first | | | |
| P08 | Audio only first | | | |
| P09 | Haptic + Audio first | | | |
| P10 | Audio only first | | | |
| P11 | Haptic + Audio first | | | |
| P12 | Audio only first | | | |

After the sessions, copy this into `participants.csv` with one row per session: `participant_id,session_id,order`.

### Instruction script (read to every participant)

"In this study you'll use a phone without looking at it. The phone will say 'Find' and then a button name, for example 'Find Wishlist'. Keep one finger on the screen and slide it around. When your finger is on a button, you'll hear its name, and in some rounds the phone will also vibrate. When you find the button you were asked for, lift your finger to select it. If you pick the wrong one, the phone will tell you, and you can keep searching. The buttons move and change size every time. Try to be quick and accurate. After each level, you'll rate how comfortable it felt from 1 to 5. Any questions?"
