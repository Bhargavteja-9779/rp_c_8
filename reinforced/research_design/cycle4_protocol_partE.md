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

## Amendment E-A1 (after the first analysis run; numerical only)
The first run of `e_analysis.py` produced non-converged coefficients (overflow, odds ratios of 0 or infinity) in the joint fixed-effects logistic regression because plain Newton–Raphson diverged. The optimiser was replaced by Newton–Raphson with step-halving and a ridge penalty of 0.001 on the stratum dummies only; exposures, outcomes, strata and all other analyses are unchanged. The Mantel–Haenszel results of the first run (which do not depend on this model) were seen before the fix.

## Amendment E-A2 (written after seeing the first Part E results; the analyses below were specified before they were run)
The first run showed: fastest 5 % within journal-year, Mantel–Haenszel OR 4.4 for R_process (journal-cluster CI 2.1–8.2); slow articles OR 0.13; negative control N1 OR 1.09 (0.92–1.23); batch acceptance OR 1.4 (≥ 5) and 2.0 (≥ 10) but 0.9 after excluding mass-retraction journal-years; out-of-time stratified AUC of the PIT score 0.71 for R_process; the association weaker in later acceptance years and for Wiley; a negative journal-year-level correlation of the share of D ≤ 7 days with retraction. Added, all secondary and post hoc in the sense that they respond to these results:
* **A7 external replication**: the same definitions (X1, X2, X3, X4, N1; strata journal × acceptance year; MH odds ratios with journal-cluster bootstrap) applied to the external PubMed-dated journals of other publishers (`data/raw/pubmed_ext`), with retraction outcomes from Retraction Watch matched on DOI (R_process, R_any).
* **A8 reason subtypes**: MH odds ratios of X1 for retractions whose reasons contain (separately) "compromised peer review", "rogue editor", "paper mill", "concerns/issues about peer review"; and for R_other.
* **A9 score calibration and pooled discrimination**: retraction rate (R_process, R_any) by PIT band (≤ 0.01, 0.01–0.05, 0.05–0.20, 0.20–0.80, 0.80–0.95, ≥ 0.95) in the A3 population; pooled (not stratified) AUC of −PIT, −D and batch size for the same population, with journal-cluster bootstrap CI.
* **A10 time to retraction**: median months from acceptance to retraction for fast (X1) versus other retracted articles.
* The follow-up dependence of the effect (OR by acceptance year) is reported as observed; a formal follow-up-adjusted analysis is not claimed.

## Amendment E-A3 (specified before running; responds to the year pattern and event concentration seen in the first results)
* **A11 equal follow-up**: outcomes R_process_24 and R_any_24 = retracted with a retraction date ≤ 730 days after the acceptance date; articles accepted 2020-01-01 to 2024-12-31 only (every article then has at least 21 months of follow-up before the 2026-11-24 data cut; the 24-month window is applied to the retraction date, and articles accepted after 2024-10-31 are excluded to guarantee a full window). MH odds ratio of X1 overall and by acceptance year.
* **A12 event concentration**: share of process-related retractions in the 1, 5, 10 and 20 journals with most such events; MH odds ratio of X1 for R_process after removing the 1, 3, 5, 10 and 20 journals with most process-related retractions.

## Amendment E-A4 (specified before running; prompted by the prior-art search)
* **A13 accepted-to-first-online lag**: lag = first-online date minus acceptance date (days). **L1** lag ≤ the 5th percentile of the journal × acceptance-year stratum; **L2** lag ≥ the 95th percentile (strata with ≥ 100 articles with a lag defined). MH odds ratios (journal-cluster bootstrap) for R_process and R_any, and the joint fixed-effects model with X1, X2, L1, L2, ln refs, ln authors.
* **Reason-label snapshot**: Retraction Watch labels are revised over time ("Fake Peer Review" has been renamed in recent snapshots); the substring "peer review" used for R_process covers both. The snapshot used is `data/raw/retraction_watch/retraction_watch.csv.gz`, downloaded 2026-11-24, with its SHA-256 recorded in `results/E_build_summary.json`.

## Amendment E-A5 (specified before running; prompted by the benchmark of the target journal, which found no time-to-event analysis of retraction)
* **A14 stratified Cox model**: time from the acceptance date to retraction (event) or to the data cut 2026-11-24 (censoring), for R_process and R_any separately; strata = journal × acceptance year; covariates X1, X2, X4, X5, ln references, ln authors jointly (same coding as the logistic model); Breslow ties; journal-cluster robust standard errors; articles with a retraction date on or before the acceptance date are excluded from the model (their number is reported). Hazard ratios are reported with 95% CI; also the model restricted to strata with X1 defined.
* Reporting follows the STROBE and RECORD checklists; a completed RECORD checklist is supplied as a supplement.
