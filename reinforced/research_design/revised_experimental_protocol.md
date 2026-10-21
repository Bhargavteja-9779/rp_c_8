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

---
# Part B (written 2026-10-21 after the methods-audit report `review/agent_DEF_methods.md`; committed before Y0–Y5 were run)
Results of X4–X6 were seen before Part B was written (they are in `reinforced/results/X4_X5_X6_summary.json`). Part B experiments respond to agent DEF's CRITICAL/MAJOR findings and are executed once each, as specified.

| ID | Finding addressed | Specification | Pass criterion / interpretation |
|---|---|---|---|
| Y0 | C1 (imprint clustering, origin overlap), C2 (H2 aggregation) | Imprint = modal DOI prefix of the journal's articles (10.1007, 10.1186, 10.1038, 10.1002, 10.1111, 10.1080, other). (a) imprint-cluster bootstrap CIs (5,000) and across-imprint t-tests/sign tests for all seven v1 contrasts and the F0 shortfall; (b) H2 specification curve (journal mean, paper-weighted, imprint-cluster); (c) shortfall by imprint. | Report which v1 conclusions survive imprint clustering; relabel H2 'inconclusive' if the CI straddles the −3-point boundary under the pre-specified rule |
| Y1 | M1 (shortfall trend is a follow-up artefact; 'optimism' vs symmetric instability) | Rolling quarterly origins 2022-01-01 … 2024-04-01 (10), target = received within 91 days, all targets truncated at the same follow-up D ≤ 480 d, eligibility n_train ≥ 100 and n_test ≥ 30; forecasters F0, F6, F2; coverage, skill, width by origin and imprint; two-way (imprint × origin) cluster bootstrap; predictive interval for a future origin; out-of-time recalibration learned only from origins whose targets are complete (t' + 91 + 480 d ≤ t0) | Pre-declared claim: F0's 80 % interval under-covers in the pooled panel; recalibrated F0 coverage within 78–82 % |
| Y2 | C2, M1 | Null/simulation: (a) permute target cohorts across journals within imprint → skill vs F2 ≈ 0; (b) exchangeable benchmark: random split inside one journal's received-cohort at the observed n_train/n_test → shortfall ≈ finite-sample value; (c) generative model with no drift: arrivals with the journal's observed volume growth, D drawn from the journal's own target-cohort ln D distribution, visibility rule applied | If (c) reproduces the visible-set shortfall within 0.5 points, truncation + growth explain it without any drift |
| Y3 | M3 (article-type / fast-lane mixture) | Variants: refs ≥ 10, refs ≥ 15, excluding batch-accepted records (≥ 10 same-journal papers on one accepted date and ≥ 5× journal daily rate), excluding journals with ≥ 10 % of papers ≤ 14 d; re-compute shortfall, skill, F4−F0, F6−F0, P72 shares, ICC | Report H4 share and ICC by variant; H4 conclusion stands if share > 5 % |
| Y4 | E7 not strictly out of time | LightGBM quantile models trained on origin-2022 targets (complete labels), tested on 2024 targets; features: pre-submission {authors, month, weekday} ± ln refs, journal-demeaned; control: same learner with the journal quantile only | Gain vs control with journal-cluster CI; not claimed unless CI excludes 0 |
| Y5 | D1 (shortfall predictable?) | Out-of-time: regress per-journal-origin shortfall at 2023 on imprint, log volume change (+ square), n_train, fast-lane share, instability; predict 2024; compare out-of-sample R² with the best constant | Exploratory |
Corrections to v1 text required regardless of outcomes: E9 journal count, follow-up statement for the 2024 origin (minimum 842 d), 'concurrent registered study' wording, drift ratio wording (robust ratio), 'secular slowing' interpretation.
