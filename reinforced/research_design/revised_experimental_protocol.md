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

---
# Part C (written 2026-10-21 after `review/agent_R2_adversarial.md`; committed before Z-experiments were run)
Results of Y0–Y5 and X1–X6 were already known. Each Z-experiment responds to a finding of the second-round reviewer (R2-xx) and is run once as specified.
| ID | Finding | Specification | Interpretation rule |
|---|---|---|---|
| Z1 (Y2d) | R2-01/06/11: v1 null worlds circular; shortfall may be the expected consequence of the journal×year variance component | Generative null with independent random cohort location shifts N(0, σ²) for the training cohort and the target cohort, σ² = journal × year variance estimated in RQ1 (0.0321; also ×0.5 and ×2), journal-specific residual shape = the journal's visible ln D centred, n_train/n_test as observed; "visible" world (both shifted) and "oracle" world (target shift halved); compare simulated and observed shortfall, by imprint and with a per-journal σ² proxy | If the simulated shortfall lies inside the observed CI, the shortfall is the expected consequence of cohort-level variance (variance-inflation result) |
| Z2 | R2-07: recalibration labels looked ahead of the origin and the 2025 target was censored | Strict rule: map learned only from origins whose targets are complete at t0 (t'+91+480 ≤ t0), common D cap 480 d, 91-day cohorts, 2023-10 … 2024-04 origins; compare F0, R (map), F0 width-inflated by a constant learned the same way (V), F4; Brier for P(D≤72/120/180) raw vs calibrated; reliability slope with journal-cluster CI | X2/X6 numbers of cycle 2 are demoted to "look-ahead variant" |
| Z3 | R2-10: imprint-cluster CIs anti-conservative (7 clusters; 3 publishers) | t(6) intervals on imprint means, publisher-level (3-cluster) sign/t checks, Holm over 7 contrasts for imprint t-tests | report which contrasts survive |
| Z4 | R2-13: X1 inference overstated | journal-weighted shares; by received-year medians; 14-day resolution caveat | Table label "pre-set criterion failed; post-hoc statistics compatible" |
| Z5 | R2-20/R2-08 | backward-oracle script (F0 trained on the complete cohort submitted after the target, origins 2022-01, 2023-01); eligibility from pre-origin data only (no minimum on target size beyond 10) | report |
| Z6 | R2-09 | moving-block bootstrap over ordered origins for the panel's pooled shortfall; describe U-shape | report |
Text corrections regardless of outcomes: X6 count (4 of 6), hypothesis-list wording, Table 5 labels, "hard to beat", fast-end claim, F2 described as straw baseline, 2025 origin and journal-set sizes stated, title with journal count and three publishers.

## Part D (cycle 3): a calibrated forecaster for cohort shift — specified before any Part D code was run or any external data were fetched
Motivation. Cycle 2 characterised the shortfall as compatible with random cohort-to-cohort location shifts but did not turn that into a method, and its remedies (R, V) were learned from a few early origins and over-covered. Part D builds a forecaster that estimates the cohort-shift variance from **earlier, complete** cohorts only, and tests it on ten strictly out-of-time origins plus an external set of journals from publishers outside the frame. Nothing is tuned on evaluation data; all constants below are fixed here.

**D0 Data and rule.** Durations are capped at 365 days (D365 = min(D, 365); y = ln D365) for training and scoring. Panel origins are quarterly, 2022-01-01 … 2025-07-01. At origin t0 the visible set is papers first online and accepted before t0 within the preceding 12 months; the target cohort is papers received in [t0, t0+91). Eligibility ≥ 100 visible and ≥ 30 target papers (frame journals); the frame data are those of cycles 1–2. **Evaluation origins**: 2023-04-01 … 2025-07-01 (ten). A method at origin t0 may use *only* earlier origins o with o + 91 + 365 ≤ t0 ("complete at t0"), see D6 for the number available. Targets of an evaluation origin are complete by 2026-09-30.

**D1 Forecasters (quantile levels 0.1,…,0.9).**
- F0: empirical quantiles (Hazen) of the visible 12-month sample. F6: time-decayed (half-life 182.5 d).
- V: half-widths about the median multiplied by one constant c ∈ {1.000, 1.025, …, 1.400}, chosen on earlier complete origins to bring pooled 80 % coverage closest to 0.80.
- R: F0 quantile levels replaced through the PIT map learned from earlier complete origins.
- **CV0 (proposed): cohort-shift smoothed empirical forecaster.** Predictive CDF G(q) = (1/n) Σ_i Φ((q − y_i)/h), with h² = τ̂²_pub + s²/n (s² the visible sample variance; n the visible size), quantiles by bisection. τ̂²_pub is estimated per publisher (Springer Nature, Wiley, Taylor & Francis) from earlier complete origins as τ̂² = max(0, Var_j(Δ_j) − mean_j(s²_tr/n_tr + s²_te/n_te)), Δ_j = mean(y_target) − mean(y_visible) of journal-origin j, variance centred on the publisher mean.
- **CVb (secondary):** CV0 with the visible sample shifted by the publisher mean of Δ over earlier complete origins.
- **CVg (secondary):** CV0 with a single global τ̂² pooled over publishers.
- **ACI (secondary, interval only):** adaptive conformal-type update of the miscoverage level of the F0 80 % interval, α_0 = 0.20; for each earlier complete origin o in time order, α ← clip(α + γ(0.20 − m_o), 0.02, 0.60) with m_o the pooled miscoverage of the interval at level α_o on the targets of o, γ = 0.05 (not tuned).
Journal identity (not only publisher) is used by every forecaster through the visible sample.

**D2 Metrics.** Primary: (a) journal-mean absolute error of 80 % coverage |cov − 0.80|, (b) mean pinball loss over nine levels, (c) mean 80 % interval (Winkler) score. Secondary: signed coverage, lower and upper tail coverage (0.1/0.9 quantiles), width, Brier scores for D ≤ 72/120/180.

**D3 Hypotheses (confirmatory).**
- HD1: CV0 has lower mean absolute coverage error than F0 (journal-cluster paired bootstrap, 3,000 draws; pooled over the ten origins, journal averaged first).
- HD2: CV0's pinball loss is not more than 0.5 % above F0's (non-inferiority; upper CI bound).
- HD3: CV0's signed coverage lies within ±1.5 points of 80 % in the pooled evaluation.
- HD4: CV0 has lower mean absolute coverage error than each of V, R and ACI (Holm over the three).
- HD5 (mechanism, not circular because τ̂² uses earlier cohorts only): the shortfall predicted for each journal-origin as G(q90_F0) − G(q10_F0) − 0.80 (with the same CV0 G) correlates positively with the observed shortfall across journal-origins aggregated by journal; calibration slope of observed on predicted by decile bins reported with journal-cluster CI.
- HD6 (external): on external journals (D5), CV0 with the *frame's* pooled τ̂² (transfer) has lower mean absolute coverage error than F0 and V (V's constant likewise transferred).
Consequences: if HD1 or HD3 fail the method is reported as not supported and the paper remains a measurement paper.

**D4 Inference.** Journal-cluster bootstrap (3,000 draws) for all contrasts; imprint-mean t(6) and publisher-level checks for HD1/HD4; origin dependence by a moving-block bootstrap over the ten ordered origins (block length 2). Holm over the HD4 contrasts. Results are reported whether or not hypotheses are supported.

**D5 External set.** `collect_pubmed_external.py` (journal list fixed in the script before fetching). PubMed History received/accepted dates; first-online proxy = PubMed entry date. Journals kept by rule if ≥ 600 dated records (not by outcome). The same D0 rule, origins and eligibility are applied (target cohort ≥ 30 papers, visible ≥ 100). τ̂² (and V's c) for the transfer analysis are taken from the frame's evaluation at the matching origin (earlier complete frame origins only), pooled over publishers; a secondary "own-history" analysis learns them from earlier complete external origins.

**D6 Practical constraint disclosed in advance.** With the completeness rule the number of earlier complete origins available is 1 at the first evaluation origin and grows by one per quarter (maximum 10 at the last; counts reported).

**D7 Deliverable.** An open-source package and a single-page browser tool implementing CV0 with the final frame τ̂²; unit tests must reproduce the pipeline's CV0 quantiles for at least 20 journal-origins to 1e-6.
