# Pre-specified hypotheses (confirmatory unless marked exploratory)

Thresholds were fixed **before** any forecast-error computation. Journals are the unit of analysis for H2–H5.

| ID | RQ | Hypothesis | Support rule | Falsified if |
|---|---|---|---|---|
| H1 | RQ1 | The journal-level random effect explains < 50 % of Var(log D) (ICC_journal < 0.5) | ICC_journal point estimate and 95 % cluster-bootstrap CI upper bound < 0.5 | upper CI bound ≥ 0.5 |
| H2 | RQ2 | Nominal 80 % central intervals from the plain empirical-quantile forecaster (F0) have mean out-of-time coverage that differs from 0.80 by more than 3 percentage points | 95 % bootstrap CI of (mean coverage − 0.80) excludes [−0.03, +0.03] | CI inside [−0.03,0.03] |
| H3 | RQ2 | Empirical-Bayes shrinkage (F4) has lower mean pinball loss (log scale) than F0 for journals with train n < 150, but not for journals with n ≥ 400 | Holm-adjusted paired Wilcoxon p<0.05 favouring F4 in small stratum; no significant improvement in large stratum | either part fails |
| H4 | RQ4 | Fewer than 5 % of journals have an out-of-time realised P(D ≤ 72) ≥ 0.5 | proportion with 95 % Clopper–Pearson upper bound < 0.05 | upper bound ≥ 0.05 |
| H5 | RQ5 | Adding article-level pre-submission covariates to the journal-level forecast reduces pooled pinball loss by < 2 % (relative) | bootstrap CI upper bound of relative reduction < 2 % | upper bound ≥ 2 % |
| H6 (exploratory) | RQ3 | Year-to-year change in journal median log D exceeds what sampling noise alone produces (variance ratio > 1.5) | exploratory, no multiplicity claim | – |
| H7 (exploratory) | RQ2 | Shorter visibility windows (12 mo) beat 24-month windows on average (text originally said 36 mo; see deviations D8) | descriptive | – |

Heuristic expectations (not hypotheses): the best forecaster will differ by journal size; drift will matter more for fast-growing mega-journals.

Negative results will be reported with the same prominence as confirmed ones.
