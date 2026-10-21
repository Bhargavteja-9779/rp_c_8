# Experimental protocol v1.0 (pre-specified before any forecast-error computation)

Protocol frozen: 2026-10-20 (git commit recorded in `deviations.md`). Data collection (descriptive download of article dates, no model evaluation) started before this freeze; see §10 for the disclosure on prior exposure.

## 1. Data sources
* **S1 – Crossref REST API** (`received`, `accepted`, `first_online` assertions deposited by Springer Nature, Wiley, Taylor & Francis). Primary dataset.
* **S2 – PubMed E-utilities** (`History/PubMedPubDate` with `PubStatus` received/accepted). External validation and cross-source checks only.
* Data cutoff: **2026-10-20**. Collection windows: Crossref records with publication date 2021-01-01 … 2026-10-20.

## 2. Estimand and outcome
D = accepted − received (calendar days), conditional on acceptance. `received` is the date deposited by the publisher (publisher-specific definition: normally the original submission date). Outcome modelled on the log scale, y = ln D.

## 3. Journal frame (census, not a sample)
1. For members Springer Nature (297), Wiley (311) and Taylor & Francis (301) take the 1000 ISSNs with most `journal-article` records published in calendar 2023 (Crossref facet); merge print/online ISSNs to journals (`/journals/{issn}`).
2. Coverage screen: ≥ 80 % of 40 random 2023 records carry both `received` and `accepted`.
3. Volume screen: estimated dated 2023 articles between 150 and 3000.
4. **All** journals passing 1–3 are collected (no further sampling). Implemented in `code/src/build_frame.py`; eligible list `data/raw/frame_eligible.json` (802 journals at freeze).
5. Known frame limitation: journals with < ~150 dated articles/year, mega-journals (> 3000/yr), and all Elsevier/IEEE/ACS/etc. journals are outside the frame (publishers that do not deposit dates).

## 4. Record cleaning (fixed rules; counts reported)
C1 unparsable dates → drop. C2 D < 1 or D > 1460 → drop. C3 `accepted` later than first online/issued date by > 7 days → drop. C4 `received` before 2010-01-01 → drop. C5 non-research items: title matches /editorial|erratum|correction|corrigendum|retraction|publisher.?s note|expression of concern|withdrawal|book review|announcement|preface|in this issue|comment on|reply to/i, **or** `references-count` < 5 (when reported) → drop (primary). Sensitivity: no C5. C6 duplicate DOIs → keep first. Visibility date V = `first_online` if present else `issued` (month-level `issued` is set to the 15th).

## 5. Forecasting task (E3–E7)
Origins t0 ∈ {2023-01-01 (O1), 2024-01-01 (O2)}.
* **Visible training set** T12 = cleaned papers with V ∈ [t0 − 365 d, t0). T24 = V ∈ [t0 − 730 d, t0).
* **Target cohort** = cleaned papers with `received` ∈ [t0, t0 + 182 d) (all observed by the data cutoff; follow-up ≥ 2.8 y).
* Journal-origin eligibility: |T12| ≥ 100 and |target| ≥ 50 (sensitivity: 60/30).
* **No-leakage rules**: a paper in the target cohort cannot enter any training set (its `received` ≥ t0 > V of every training paper); hyper-parameters are fixed here, not tuned on targets; the empirical-Bayes prior is estimated only from T12 across journals.

## 6. Forecasters (distribution of y = ln D, quantile levels τ = 0.05, 0.10 … 0.95)
* **F0** empirical quantiles of T12 (type-7).
* **F1** empirical quantiles of T24.
* **F2** publisher-pooled quantiles: weighted quantiles of T12 over all eligible journals of the same member, weights 1/n_j (ignores journal identity).
* **F3** lognormal MLE on T12.
* **F4** empirical-Bayes lognormal: journal means m_j and log-SDs l_j shrunk to cross-journal weighted means with DerSimonian–Laird between-journal variance (estimated on T12 only); predictive variance = shrunk σ² + posterior variance of the mean.
* **F5** (interval only) recent-holdout adjusted interval: quantiles from the older 9 months of T12, symmetric expansion δ from the conformal quantile of nonconformity scores on the most recent 3 months at level 0.8.
* **F6** exponentially time-decayed empirical quantiles (half-life 182.5 d) on T24.
Exploratory only: none.

## 7. Metrics and aggregation
Primary: **mean pinball loss** over the 19 τ levels on the ln-D scale (≈ CRPS), per journal-origin, then averaged over origins within journal. Secondary: absolute error of central-80 %/50 % coverage; Winkler interval score (80 %); Brier score for events D ≤ T (T = 72, 120, 180); PIT histograms; skill = 1 − L/L(F2). Unit of analysis = journal. CIs: cluster bootstrap over journals, B = 5000, seed 20261020. Paired tests: Wilcoxon signed-rank on per-journal loss differences; Holm correction over the 7 confirmatory contrasts {F4–F0, F3–F0, F1–F0, F6–F0, F0–F2, F4–F6, F4–F3}; report median relative difference and rank-biserial effect size.

## 8. Other experiments
* **E1 data audit**: coverage, cleaning losses, D distributions, heaping.
* **E2 variance components (RQ1)**: nested random-effects ANOVA for ln D with journal, journal×acceptance-year and residual; records capped at 300 per journal-year (random, seed 20261020); accepted year 2021–2025; cluster-bootstrap CIs over journals; sensitivity with raw-day rank transform.
* **E5 drift (RQ3, exploratory)**: Δ = median ln D(year y+1) − median ln D(year y) per journal; compare Var(Δ) with its bootstrap null from within-year resampling.
* **E6 guarantee feasibility (RQ4)**: realised P(D ≤ 72) per journal-origin with Clopper–Pearson 95 % CIs; counts at 0.5/0.8/0.9; reliability of F0/F4 probability forecasts.
* **E7 article-level information (RQ5)**: LightGBM quantile regression (τ = .1,.25,.5,.75,.9; 200 trees, depth 3, lr .05) predicting y − (F4 median) from {n_authors, received month, received weekday, ln(1+refs)} on target cohorts, 5-fold CV grouped by journal; compare pooled pinball loss with journal-only F4. (`references-count` is a property of the final version; flagged as not strictly pre-submission.)
* **E8 cross-source validation**: for DOIs/PMIDs in both Crossref and PubMed, agreement of received/accepted days.
* **E9 external validation**: apply E3 protocol to ≥ 20 PubMed-history journals of non-frame publishers (Elsevier, OUP, Frontiers, …) with sufficient n.
* **Sensitivity**: window 6/12/24 mo; C5 off; eligibility 60/30; per-publisher results; origin O1 vs O2 separately; D in days vs log.

## 9. Success/failure interpretation
Hypotheses in `hypotheses.md`. Results are reported regardless of direction. Any change to this protocol after freeze is logged in `deviations.md` with reason and timestamp; confirmatory claims affected are relabelled exploratory.

## 10. Disclosures of prior exposure
* The **journal-selection step** (Step 0) used separate samples of recent articles (published ≥ 2025-07-01, ~30 000 records over 100 journals) and viewed journal-level medians/quantiles. Those articles can overlap the target cohorts only if accepted ≥ 2025-07 after a submission in 2023–24; no forecast error or model comparison was computed from them.
* No forecaster was run on any real data before this freeze.

## 11. Compute and software
Python 3.13, numpy 2.5.3, pandas 3.0.5, SciPy 1.18.1, statsmodels 0.15.0, LightGBM 4.7.0, 4 CPU cores; all code in `code/`; entry point `code/run_all.py` (`--mode quick|full`).
