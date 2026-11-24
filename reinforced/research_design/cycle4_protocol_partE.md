# Cycle 4 — Part E protocol: editorial timing as an integrity signal (written and committed before any association between timing and retraction was computed)

**Why this study.** The cycle-3 paper (turnaround forecasting) was rejected by *Research Integrity and Peer Review* for low novelty and impact for its readers and for substantial use of generative AI. Part E re-aims the same data and machinery at a question inside the journal's scope: whether unusual editorial handling times are associated with later retraction, and in particular with retractions for compromised peer review, editor misconduct and paper mills. The forecasting machinery of cycle 3 is used only to define an out-of-time "timing surprise" score.

**What was looked at before this protocol.** Only counts: the Retraction Watch (RW) file has 74,000 records (68,539 retractions); 2,399 of our 1,737,272 articles match a retraction; reason-string frequencies among them (e.g. 1,308 'Compromised Peer Review', 700 'Rogue Editor', 166 'Paper Mill', 522 'Computer-Aided Content or Computer-Generated Content'); acceptance-year counts of retracted articles. No timing variable was compared between retracted and non-retracted articles.

## E0 Data
* Articles: `data/processed/articles_clean.csv.gz` (1,737,272 research articles of 800 Springer Nature, Wiley and Taylor & Francis journals, dates from Crossref; cleaning as cycle 1).
* Outcome: Retraction Watch database (Crossref-distributed `retraction_watch.csv`, downloaded 2026-11-24, `data/raw/retraction_watch/retraction_watch.csv.gz`). An article is **retracted** if its DOI (lower case) equals `OriginalPaperDOI` of a record with `RetractionNature == "Retraction"`. Expressions of concern and corrections are not retractions. DOIs with a later `Reinstatement` record are treated as not retracted.
* Outcome sets (reason strings are semicolon-separated, matched case-insensitively after removing a leading '+'): **R_any** all retractions; **R_process** reasons containing any of "peer review", "rogue editor", "paper mill", "concerns/issues about third party involvement"; **R_ai** reason "computer-aided content or computer-generated content"; **R_other** = R_any and not R_process.
* Retracted articles are matched to their journal-year stratum (journal × acceptance year).

## E1 Timing exposures (computed only from received/accepted dates of the article and of other articles of the same journal; no outcome information)
* **X1 fast_rel**: D ≤ the 5th percentile of D within the journal × acceptance-year stratum (strata with ≥ 100 articles only).
* **X2 slow_rel**: D ≥ the 95th percentile of the stratum.
* **X3 fast_abs**: D ≤ 7 days.
* **X4 batch**: at least 5 articles of the same journal (including this one) accepted on the same calendar day; secondary threshold 10.
* **X5 weekend**: accepted on a Saturday or Sunday.
* **X6 surprise (out-of-time)**: the probability integral transform (PIT) of ln D under the cycle-3 forecaster CV0 (smoothed empirical distribution of the journal's papers visible at the quarterly origin preceding receipt, bandwidth h² = τ̂² + s²/n with the frame τ² of 0.040), flagged if PIT ≤ 0.05 (fast surprise) or ≥ 0.95. Available for papers received from 2022-01-01 in journal-origins with ≥ 100 visible papers; cap 480 days.
* **Negative-control exposure N1**: article *received* on a Saturday or Sunday (no mechanism for a causal link to retraction).
* Covariates: ln(1 + references), ln(1 + authors), publisher imprint.

## E2 Analyses and hypotheses
* **A1 (primary)**: stratified association between X1 and **R_process** (primary 1) and **R_any** (primary 2): Mantel–Haenszel odds ratio over journal × acceptance-year strata, plus a fixed-effects logistic regression with stratum dummies (X1, X2, X4, X5, ln refs, ln authors jointly); standard errors clustered by journal; Holm over the two primary tests. All other contrasts are secondary and marked as such.
* **HE1** X1 is associated with higher odds of R_process (odds ratio > 1). **HE2** X4 (batch) is associated with higher odds of R_process. **HE3** the association of X1 with R_other is smaller than with R_process (ratio of odds ratios < 1). **HE4** the negative-control exposure N1 is null (95% CI includes 1) for all outcomes. **HE5** out-of-time discrimination of the fast-surprise score for R_process is above chance (stratified AUC > 0.55).
* **A2 dose–response**: odds of R_process by 20 bins of the within-stratum percentile of D (Mantel–Haenszel against the median bin).
* **A3 prospective screening performance**: articles accepted 2022-01-01 to 2024-12-31 with X6 available (at least 22 months of follow-up for every article). Stratified (within journal × acceptance-year) AUC of −PIT for R_process and R_any, with journal-cluster bootstrap CI (500 draws); positive predictive value, lift and number needed to screen for the fastest 1% and 5% by PIT, by X3 and by X4, with the overall rate as comparator.
* **A4 heterogeneity and robustness**: by imprint; by acceptance year; excluding journal-years with ≥ 25 retractions in the data (mass-retraction events); excluding R_ai; with X4 threshold 10.
* **A5 journal-year level**: Spearman correlation between the share of articles with D ≤ 7 days (or batch) and the retraction rate across journal-years with ≥ 100 articles.
* **A6 outcome R_ai** (computer-generated content): Mantel–Haenszel odds ratios for X1, X2, X4, X5 (secondary).
* Null or negative results will be reported as such; no exposure definition will be added or changed after the first analysis run. Any change is logged as an amendment before the rerun.

## E3 Interpretation rules fixed in advance
* Associations are conditional on journal and acceptance year, not causal. A retraction is a lagging, incomplete and publisher-dependent marker of problems, and unretracted problematic articles exist.
* Timing flags must never be presented as evidence of misconduct for an individual paper; screening results are reported as enrichment (lift, PPV) with the number of flagged non-retracted articles.
* Retraction Watch coverage and the publishers' retraction practices differ, so publisher-specific results are shown separately.
