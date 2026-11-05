# Haptic Navigation Study – Results

Sensitivity check: same analysis without session(s) 20261106-043325.

Mode: **session (independent groups)**  |  alpha = 0.05

Sessions analysed: Haptic + Audio = **9**, Audio only = **9**  |  Trials: **288**  |  Ratings: **72**

Excluded sessions: 20261103-154558, 20261103-161152, 20261106-043325 (plus any session with fewer than 16 trials).

All tests use one value per session per condition x level (the mean of that session's trials).

Because sessions are not yet linked to participants, the two conditions are compared as independent groups. Once participants.csv exists, run in paired mode for the within-subject tests.

## Descriptive statistics

### Time to complete task (s)

By condition and level:

| condition | level | n | mean | median | sd |
|---|---|---|---|---|---|
| Audio only | 1 | 9 | 11.219 | 8.942 | 8.004 |
| Audio only | 2 | 9 | 9.156 | 6.45 | 7.123 |
| Audio only | 3 | 9 | 10.187 | 9.714 | 4.471 |
| Audio only | 4 | 9 | 7.308 | 7.431 | 3.662 |
| Haptic + Audio | 1 | 9 | 11.013 | 9.091 | 6.241 |
| Haptic + Audio | 2 | 9 | 7.896 | 8.164 | 4.775 |
| Haptic + Audio | 3 | 9 | 8.944 | 7.854 | 6.447 |
| Haptic + Audio | 4 | 9 | 9.07 | 8.17 | 5.849 |

Overall (session mean across levels):

| condition | n | mean | median | sd |
|---|---|---|---|---|
| Audio only | 9 | 9.468 | 9.448 | 4.185 |
| Haptic + Audio | 9 | 9.231 | 9.65 | 4.17 |

### Error rate (wrong picks / all picks)

By condition and level:

| condition | level | n | mean | median | sd |
|---|---|---|---|---|---|
| Audio only | 1 | 9 | 0.0 | 0.0 | 0.0 |
| Audio only | 2 | 9 | 0.115 | 0.0 | 0.214 |
| Audio only | 3 | 9 | 0.194 | 0.0 | 0.264 |
| Audio only | 4 | 9 | 0.044 | 0.0 | 0.088 |
| Haptic + Audio | 1 | 9 | 0.0 | 0.0 | 0.0 |
| Haptic + Audio | 2 | 9 | 0.178 | 0.2 | 0.145 |
| Haptic + Audio | 3 | 9 | 0.169 | 0.2 | 0.137 |
| Haptic + Audio | 4 | 9 | 0.221 | 0.2 | 0.209 |

Overall (session mean across levels):

| condition | n | mean | median | sd |
|---|---|---|---|---|
| Audio only | 9 | 0.089 | 0.083 | 0.087 |
| Haptic + Audio | 9 | 0.142 | 0.15 | 0.109 |

### Comfort rating (1-5)

By condition and level:

| condition | level | n | mean | median | sd |
|---|---|---|---|---|---|
| Audio only | 1 | 9 | 2.778 | 3.0 | 0.833 |
| Audio only | 2 | 9 | 2.333 | 2.0 | 0.707 |
| Audio only | 3 | 9 | 2.0 | 2.0 | 0.866 |
| Audio only | 4 | 9 | 2.0 | 2.0 | 1.0 |
| Haptic + Audio | 1 | 9 | 4.222 | 4.0 | 0.667 |
| Haptic + Audio | 2 | 9 | 3.556 | 4.0 | 0.882 |
| Haptic + Audio | 3 | 9 | 3.556 | 4.0 | 0.882 |
| Haptic + Audio | 4 | 9 | 3.778 | 4.0 | 0.667 |

Overall (session mean across levels):

| condition | n | mean | median | sd |
|---|---|---|---|---|
| Audio only | 9 | 2.278 | 2.25 | 0.775 |
| Haptic + Audio | 9 | 3.778 | 3.75 | 0.631 |

### Completion rate

By condition and level:

| condition | level | n | mean | median | sd |
|---|---|---|---|---|---|
| Audio only | 1 | 9 | 1.0 | 1.0 | 0.0 |
| Audio only | 2 | 9 | 1.0 | 1.0 | 0.0 |
| Audio only | 3 | 9 | 1.0 | 1.0 | 0.0 |
| Audio only | 4 | 9 | 1.0 | 1.0 | 0.0 |
| Haptic + Audio | 1 | 9 | 1.0 | 1.0 | 0.0 |
| Haptic + Audio | 2 | 9 | 1.0 | 1.0 | 0.0 |
| Haptic + Audio | 3 | 9 | 0.972 | 1.0 | 0.083 |
| Haptic + Audio | 4 | 9 | 1.0 | 1.0 | 0.0 |

Overall (session mean across levels):

| condition | n | mean | median | sd |
|---|---|---|---|---|
| Audio only | 9 | 1.0 | 1.0 | 0.0 |
| Haptic + Audio | 9 | 0.993 | 1.0 | 0.021 |

## Inferential statistics

### H1 – Time to complete task, Haptic + Audio vs Audio only

Welch t-test on session mean log time: t(15.0) = 0.08, p = 0.934, Cohen's d = 0.04. Haptic + Audio times were 1.02x the Audio only times (geometric mean ratio) → fail to reject H0.

Overall time, haptic vs audio (non-parametric check): Mann-Whitney U = 41.0, p = 1.000, rank-biserial r = 0.01, n = 9 vs 9 sessions, median difference (H+A - A) = 0.202 → fail to reject H0.

Time, haptic vs audio at each level (Mann-Whitney U, Holm-corrected):

| Level | n (H+A / A) | Median diff (H+A - A) | U | p (Holm) | rank-biserial r |
|---|---|---|---|---|---|
| 1 | 9 / 9 | 0.149 | 43.0 | = 1.000 | 0.06 |
| 2 | 9 / 9 | 1.713 | 36.0 | = 1.000 | -0.11 |
| 3 | 9 / 9 | -1.859 | 29.0 | = 1.000 | -0.28 |
| 4 | 9 / 9 | 0.739 | 47.0 | = 1.000 | 0.16 |

### H4 – Effect of the number of buttons on time (Friedman across levels)

Friedman across levels (Haptic + Audio): chi²(3) = 1.80, p = 0.615, Kendall's W = 0.07 → fail to reject H0.

Friedman across levels (Audio only): chi²(3) = 3.00, p = 0.392, Kendall's W = 0.11 → fail to reject H0.

### H2 – Error rate (non-parametric: error rates are bounded and usually not normal)

Overall error rate, haptic vs audio: Mann-Whitney U = 51.5, p = 0.348, rank-biserial r = 0.27, n = 9 vs 9 sessions, median difference (H+A - A) = 0.067 → fail to reject H0.

Error rate, haptic vs audio at each level (Mann-Whitney U, Holm-corrected):

| Level | n (H+A / A) | Median diff (H+A - A) | U | p (Holm) | rank-biserial r |
|---|---|---|---|---|---|
| 2 | 9 / 9 | 0.2 | 54.0 | = 0.427 | 0.33 |
| 3 | 9 / 9 | 0.2 | 40.5 | = 1.000 | 0.0 |
| 4 | 9 / 9 | 0.2 | 61.5 | = 0.133 | 0.52 |

Friedman across levels (Haptic + Audio): chi²(3) = 11.79, p = 0.008, Kendall's W = 0.44 → **reject H0**.

Friedman across levels (Audio only): chi²(3) = 6.64, p = 0.084, Kendall's W = 0.25 → fail to reject H0.

### H3 – Comfort rating (non-parametric: ordinal Likert data)

Overall comfort, haptic vs audio: Mann-Whitney U = 75.5, p = 0.002, rank-biserial r = 0.86, n = 9 vs 9 sessions, median difference (H+A - A) = 1.500 → **reject H0**.

Comfort, haptic vs audio at each level (Mann-Whitney U, Holm-corrected):

| Level | n (H+A / A) | Median diff (H+A - A) | U | p (Holm) | rank-biserial r |
|---|---|---|---|---|---|
| 1 | 9 / 9 | 1.0 | 74.5 | = 0.007 | 0.84 |
| 2 | 9 / 9 | 2.0 | 69.0 | = 0.010 | 0.7 |
| 3 | 9 / 9 | 2.0 | 72.0 | = 0.008 | 0.78 |
| 4 | 9 / 9 | 2.0 | 74.0 | = 0.008 | 0.83 |

Friedman across levels (Haptic + Audio): chi²(3) = 7.00, p = 0.072, Kendall's W = 0.26 → fail to reject H0.

Friedman across levels (Audio only): chi²(3) = 12.47, p = 0.006, Kendall's W = 0.46 → **reject H0**.

### Exploratory – target size and vibration intensity

Spearman correlation, target area vs time: rho = -0.24, p < .001.

Spearman correlation, target vibration intensity vs time (Haptic + Audio trials only): rho = 0.00, p = 0.983.

## Figures

![Completion time](fig1_time_by_level.png)

![Error rate](fig2_error_rate_by_level.png)

![Comfort](fig3_comfort_by_level.png)

![Target size vs time](fig4_time_vs_target_size.png)
