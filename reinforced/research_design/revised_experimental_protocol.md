# Cycle-2 protocol (written 2026-10-21; committed to git before experiments X4–X6 were run)

## Disclosure of order of events
* X1 (preprint-date validity probe), X2 (quantile-level recalibration F9) and X3 (learned meta-forecaster F10) had **already been started/executed when this document was written**. Their designs were fixed in their scripts before a single run each (no tuning, no re-runs). They are reported as *cycle-2 experiments with design fixed in code*, not as independently pre-specified.
* X4–X6 below are specified here **before** being run. Deviations will be logged in `reinforcement_deviations.md`.

## Weaknesses → experiments
| ID | Weakness (evidence) | Experiment | Hypothesis | If false |
|---|---|---|---|---|
| X1 | `received` semantics unverified (reviewers D,F; v1 limitation) | Compare `received` with posting date of the linked preprint (Crossref `has-preprint`). For Research Square "In Review" preprints (DOI 10.21203; posted at submission) expect received − posted ≈ 0. Compare journals that look fast with the rest. | H-X1: among Research Square-linked articles, ≥ 70 % have |received − posted| ≤ 14 d, and the share with received > posted + 90 d is no larger in fast-looking journals than elsewhere | `received` is not reliably the original submission date for some journals → restrict claims |
| X2 | F0 under-covers by ~3 pts (v1) | Learn a quantile-level recalibration map from PITs of earlier cohorts only; apply at 2024 and 2025 origins | H-X2: coverage of the nominal 80 % interval is within ±1.5 pt of 0.80 with no pinball loss increase > 0.5 % | bias is not stable over time |
| X3 | only simple baselines (v1, reviewers D,G) | LightGBM quantile regression on journal-level features (past quantiles, n, trend, volume growth, publisher), trained on earlier cohorts only | H-X3: not better than F0 by more than 1 % of loss (simple-method challenge) | learned model improves → report |
| X4 | dependence between origins/journals (reviewer E) | (a) single-origin analysis (2024 only, no overlap of target cohort with later training windows); (b) publisher-block bootstrap (resample the 3 publishers' journals within strata, 5,000 reps) for H2, F0−F2, F4−F0, ICC; (c) journal-cluster bootstrap for P72 shares (done in cycle 1) | H-X4: conclusions on H1–H5 unchanged | report which change |
| X5 | data-quality flags (forensics) | Re-run primary contrasts excluding flagged journals (any year with > 10 % of papers ≤ 10 d, or median ≤ 30 d; list written by script) | H-X5: conclusions unchanged | report |
| X6 | "≤ T days" claims overstate speed (v1 E6) | Apply the X2 map to event probabilities P(D ≤ 72/120/180) and compare Brier score and reliability (2024, 2025 origins) | H-X6: calibrated probabilities have lower Brier score than raw and a reliability slope closer to 1 | no gain |

## Common rules
Same eligibility (≥100 visible, ≥50 target), same data, same visibility rule; unit = journal; journal-cluster bootstrap 5,000, seed 20261020; Holm over the pre-listed contrasts within each experiment; negative results reported. Outputs in `reinforced/results/`.

## Limits that remain regardless of results
Accepted-only conditioning; three date-depositing publishers; no access to submission-system records; no human expert review.
