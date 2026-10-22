# Reinforcement review (Phase 8): what the cycle-2 evidence changed

## Hypotheses supported / rejected / inconclusive
| Item | Result |
|---|---|
| H1 journal share < 50 % | supported, robust (24.5–29.0 % leaving out any publisher; 25.9–27.4 % across article-type variants) |
| H2 shortfall > 3 points | **inconclusive** (journal mean −3.0; paper-weighted −3.6; imprint t(6) CI −4.2…−1.1); v1 said "not supported" |
| H3 shrinkage helps small journals | not supported; **small-n regime untestable** (only 6 journals with 30–99 visible papers); F7/F8/L also no gain |
| H4 < 5 % of journal-origins fast | not supported (12.0 %; 8.9–12.6 % in variants) — partly a fast-lane (article-type) effect |
| H5 covariates < 2 % | **specification-dependent**: pre-submission features 0.8–1.0 % (supported); with references 3.0 % (acts as article-type detector) |
| H6 drift > noise | supported; magnitude restated (robust ratio 5.3, not 7.3) |
| H7 12 vs 24 months | not supported (imprint t(6) CI −0.0001…+0.0011) |
| X1 received ≈ original submission | pre-set criterion (±14 d, 70 %) **failed**; post-hoc statistics compatible for Springer Nature (95 % paper-weighted, 82 % journal-weighted ≤ +14 d; offset shifts by year; 14-day resolution); **untestable for Wiley/T&F** |
| X2 recalibration | **not supported under the strict rule** (R +1.9, V +1.05, F4 +1.3 vs F0 −1.9; loss unchanged); look-ahead variant (+1.4) demoted |
| X3 learned forecaster | no gain (supports "simple wins") |

## What was robust
Skill of journal-specific vs pooled forecasts (≈15–16 % in every variant), the existence of a ~2–3 point under-coverage in all robustness variants and all leave-one-publisher-out estimates, F0 ≥ F3/F4, the 12 % share of journal-origins with ≥ half of papers ≤ 72 d (variants 9–13 %).

## What depended on conditions / was weakened
* "Optimism due to slow papers not yet visible" (v1) **withdrawn**: a stationary world with growth + visibility is calibrated (+0.05 pts), a random split is calibrated (−0.02), but cohorts are non-exchangeable in both time directions (oracle −1.5; backward oracle −1.4 to −2.5). Random cohort shifts of the size of the journal×year variance (Z1) reproduce the magnitude (σ²/2 −2.8, σ² −4.9; oracle −1.6) but not the spread across journals or imprints, and σ² comes from the same data: a consistency check, not identification. The shortfall is instability, not a one-way bias; it is not predictable journal by journal (R² ≈ 0.001).
* "Stable across origins" replaced by a rolling panel: U-shaped (−3.4 → −1.4 → −2.5), pooled −2.4, moving-block CI [−2.9, −1.8].
* F1 − F0 ("12 months beats 24") no longer claimed.
* RQ5 narrowed: article-level information is worth about 1 % when strictly pre-submission.
* Generalisation: the PubMed check is inconclusive (shortfall −0.7 [−3.6, +2.1]) and is no longer called replication.

## What had no benefit
Learned meta-forecaster L (n.s. vs F0), skew-normal/pooled-shape/blend forecasters (worse), empirical-Bayes shrinkage (worse), 6-month persistence (not better).

## Central contribution after reinforcement
Unchanged in type (empirical meta-research), changed in content: (i) an out-of-time benchmark; (ii) a finding that journal history is informative but over-confident because cohorts are non-exchangeable; (iii) a **negative result on simple remedies** (strictly out-of-time recalibration and width inflation over-correct) with improved reliability of event probabilities, and a reporting recommendation; (iv) a validity test of the received date for one publisher; (v) a documented negative result on elaborate forecasters. The paper answers a more cautious question than v1 and offers a variance-inflation account of the shortfall as consistent with, not proven by, the data.

## New limitations that emerged
Over-correction of every remedy tried; only the value of journal information and the shortfall are robust at the 3-publisher level; unpredictable instability; the received-date validation covers only a self-selected Springer Nature subset; fast-lane/article-type mixture inflates the "fast journal" share; X-experiments X1–X3 are not independently pre-specified.
