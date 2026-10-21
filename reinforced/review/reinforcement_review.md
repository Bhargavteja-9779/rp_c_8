# Reinforcement review (Phase 8): what the cycle-2 evidence changed

## Hypotheses supported / rejected / inconclusive
| Item | Result |
|---|---|
| H1 journal share < 50 % | supported, robust (24.5–29.0 % leaving out any publisher; 25.9–27.4 % across article-type variants) |
| H2 shortfall > 3 points | **inconclusive** (journal mean −3.0; paper-weighted −3.6; imprint-cluster CI −4.0…−2.0); v1 said "not supported" |
| H3 shrinkage helps small journals | not supported; **small-n regime untestable** (only 6 journals with 30–99 visible papers); F7/F8/L also no gain |
| H4 < 5 % of journal-origins fast | not supported (12.0 %; 8.9–12.6 % in variants) — partly a fast-lane (article-type) effect |
| H5 covariates < 2 % | **specification-dependent**: pre-submission features 0.8–1.0 % (supported); with references 3.0 % (acts as article-type detector) |
| H6 drift > noise | supported; magnitude restated (robust ratio 5.3, not 7.3) |
| H7 12 vs 24 months | not robust after imprint clustering |
| X1 received ≈ original submission | supported for Springer Nature "In Review" papers; threshold as set (±14 d, 70 %) not met because those preprints are posted ~2 weeks after receipt; **untestable for Wiley/T&F** |
| X2 recalibration | works at 2024–25 (+1.4 points, loss unchanged); over-corrects in the panel (+1.8) |
| X3 learned forecaster | no gain (supports "simple wins") |

## What was robust
Skill of journal-specific vs pooled forecasts (≈15–16 % in every variant), the existence of a ~2–3 point under-coverage in all robustness variants and all leave-one-publisher-out estimates, F0 ≥ F3/F4, the 12 % share of journal-origins with ≥ half of papers ≤ 72 d (variants 9–13 %).

## What depended on conditions / was weakened
* "Optimism due to slow papers not yet visible" (v1) **withdrawn**: a stationary world with growth + visibility is calibrated (+0.05 pts), a random split is calibrated (−0.02), but cohorts are non-exchangeable in both time directions (oracle −1.5, backward oracle −1.1…−2.6). The shortfall is *instability*, not a one-way bias; it is not predictable journal by journal (R² ≈ 0.001).
* "Stable across origins" replaced by a rolling panel (range −1.4…−3.4, pooled −2.2, predictive interval −4.0…−0.8).
* F1 − F0 ("12 months beats 24") no longer claimed.
* RQ5 narrowed: article-level information is worth about 1 % when strictly pre-submission.
* Generalisation: the PubMed check is inconclusive (shortfall −0.7 [−3.6, +2.1]) and is no longer called replication.

## What had no benefit
Learned meta-forecaster L (n.s. vs F0), skew-normal/pooled-shape/blend forecasters (worse), empirical-Bayes shrinkage (worse), 6-month persistence (not better).

## Central contribution after reinforcement
Unchanged in type (empirical meta-research), changed in content: (i) an out-of-time benchmark; (ii) a finding that journal history is informative but over-confident because cohorts are non-exchangeable; (iii) a **tested, partial remedy** (quantile-level recalibration) and a reporting recommendation; (iv) a validity test of the received date for one publisher; (v) a documented negative result on elaborate forecasters. The paper answers a more cautious question than v1 and no longer claims an explanation of the shortfall.

## New limitations that emerged
Over-correction of the remedy; unpredictable instability; the received-date validation covers only a self-selected Springer Nature subset; fast-lane/article-type mixture inflates the "fast journal" share; X-experiments X1–X3 are not independently pre-specified.
