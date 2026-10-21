# Forensic methods audit (Reviewers D/E/F)

Scope: I read `independent_review_agentA.md`, `review_response_ledger.csv` and `deviations.md` first, so A1-A15 and B1-B8 are not repeated. Every number below was recomputed from `articles_clean.csv.gz`, `data/raw/crossref` and `results/`, using scratch scripts outside the project. I re-ran the package's own `run_forecast_experiment` on perturbed data. It reproduces `metrics_journal_origin.csv` to 1e-16, so the variants are like-for-like. No project file was modified.

**Verdict: no FATAL issue.** The directional findings survive every check: F0 beats F2, F3 and F4 are slightly worse than F0, F6 is marginally better, F0 under-covers, and drift exceeds noise. Two CRITICAL items (inference and H2), three MAJOR items (multi-origin interpretation, generalisation, article-type mixture) and several MODERATE items would drive a major revision.

## 1. CRITICAL

**C1. Inference ignores imprint/publisher correlation and the overlap between origins.**
- Evidence:
  - Imprints (DOI prefix: Springer 10.1007, BMC 10.1186, Nature 10.1038, Wiley 10.1002, Blackwell 10.1111, T&F 10.1080) have ICC 0.037 for the per-journal F0 shortfall. With mean cluster size about 115 the design effect is about 5.
  - Journal-cluster CI of the shortfall: [-3.51, -2.58] points. Imprint-cluster CI: [-4.04, -2.00], 2.2 times wider.
  - The shortfall differs by imprint (ANOVA p = 4e-5): BMC -5.7 (n = 86), T&F -3.4, Springer -3.1, Wiley -3.0, Blackwell -1.1, Nature -1.0.
  - Contrast ICCs by imprint: F4-F0 0.11 (design effect about 14), F4-F6 0.09, F6-F0 about 0.
  - Imprint-level t-tests (6 clusters) give p = 0.034 (F4-F0), 0.030 (F3-F0), 0.095 (F1-F0), 0.0035 (F6-F0), 0.012 (F4-F6), 0.017 (F4-F3). The manuscript's Wilcoxon p-values run from 1e-6 to 1e-91. F1-F0 ("24 months marginally worse") is not significant once imprints are clustered.
  - Signs are identical in all 7 imprints for every contrast except F1-F0 (6 of 7); the sign-flip minimum p is 2/128 = 0.016.
  - The origins overlap: 80.7% of O1 target papers re-enter O2's training set, and 41.9% of O2's training set is the O1 target cohort. Per-journal coverage correlates 0.03 across origins, but loss differences correlate (F4-F0 0.42, F0-F2 0.69).
  - Journal-origin coverage has SD 0.086 against 0.034 under binomial sampling.
- Why it matters: precision such as p about 1e-90 cannot come from 2 origins and 3 to 6 publisher blocks.
- New experiment: yes (X1).
- Verification: two-way (imprint x origin) cluster CIs for all of Tables 2 and 4. The expected outcome is that F0 > F2 and F6 < F0 survive, F4/F3 > F0 survives at p about 0.03, and F1-F0 becomes "no difference".

**C2. The H2 verdict, and "covered 77.0% of later papers", depend on aggregation choices.**
- Evidence (shortfall in points; journal-cluster 95% CI unless stated):

| Specification | Shortfall | CI |
|---|---|---|
| Pre-specified (journal mean, closed interval) | -3.03 | [-3.51, -2.58] |
| Randomised PIT, journal mean | -3.24 | [-3.69, -2.79] |
| Paper-weighted, closed | -3.63 | [-4.27, -3.00] |
| Paper-weighted, randomised PIT | -3.85 | [-4.49, -3.24] |
| Imprint-cluster, journal mean | -3.03 | [-4.04, -2.00] |

  - Only the paper-weighted randomised-PIT row would "support" H2 under the pre-specified rule; the rest are inconclusive.
  - The 77.0% is a journal average. Paper-level coverage is 76.4% (76.15% by randomised PIT).
  - Closed intervals on integer days inflate coverage by 0.2 to 0.25 points, and D shows weekly heaping (D mod 7 = 0 is 15.3% against 14.3%).
  - The rule has three outcomes (supported, falsified, inconclusive). The text reads "inconclusive" as "not supported".
- New experiment: no (a specification curve on existing data).
- Verification: add the table, label H2 "inconclusive", and write "77.0% (journal average; 76.4% of papers)".

## 2. MAJOR

**M1. The multi-origin "stable" and "optimism" narrative is not supported at equal follow-up.**
- Four-origin trend. R1 gives -4.06, -3.35, -2.65, -2.29 for 2022 to 2025, but later cohorts have less follow-up before the 2026-10-20 cutoff. Capping every target at D <= L for all origins (I re-ran R1):

| L (days) | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| none | -4.06 | -3.35 | -2.65 | -2.29 |
| 500 (2025 is 99.5% complete) | -2.57 | -1.83 | -1.19 | -2.01 |
| 400 | -1.26 | -0.67 | +0.21 | -0.93 |

  The monotone improvement disappears, and the 2025 origin is worse than 2024. "Stable" understates a range of -1.2 to -2.6.
- Direction of the oracle residual. E10 gives -1.5 and the text reads it as drift or slowing. I ran a time-reversal test on complete submission cohorts.
  - A forward oracle (previous year predicts the next 6 months) gives -1.19, -1.49, -0.95, -1.45 at origins 2022-07 to 2024-01.
  - A backward oracle (the following year predicts the earlier 6 months) gives -1.14, -1.38, -1.59, -2.59.
  - Mass above q90 (10.2 to 11.5%) and below q10 (10.0 to 11.3%) is balanced.
  - The oracle residual is therefore symmetric non-exchangeability (about -0.3 finite-sample plus cohort-to-cohort variance in location and shape), not secular slowing. Only the visibility-truncation part (upper-tail PIT 13.1%) is directional "optimism".
  - Seasonality is excluded: the H1 cohort differs from the previous full year by -0.019 and +0.026 ln-units in 2023 and 2024.
- New experiments: X1, X2.
- Verification: per-origin shortfall at common follow-up with an origin-block CI. Decompose it into finite-sample (about 0.3), truncation (about 1.5, directional) and symmetric non-stationarity (about 1.2). Use "optimism" only for the truncation component.

**M2. Generalisation is narrower than stated, and E8/E9 do not test it.**
- Frame composition:
  - Springer Nature supplies 440 of 781 evaluated journals (56%), Wiley 255, T&F 86.
  - 73% of Springer candidates, 49% of Wiley and 18% of T&F pass the frame (about 57%, 46% and 34% of their 2023 articles). Of 1,684 candidates, 530 fail the date-deposit screen and 826 fail the under-150-articles screen.
  - The "T&F" results describe a deposit-compliant minority.
- E9:
  - It has 30 journals and 58 journal-origins (the Methods say 32).
  - The F0 shortfall is -0.67 points, CI [-3.55, +2.03], compatible with both 0 and -3. The abstract's "smaller shortfall (-0.8)" is noise.
  - Skill 14.8% (F0-F2 CI [-0.046, -0.008]) is consistent with the main result.
  - Its F2 pools all external journals (Elsevier, Frontiers, PLOS, Cell, OUP, Nature Communications) as one "publisher", which is not the main benchmark.
- E8: 99.997% agreement on 59,885 DOIs from 14 BMC/Springer-type journals compares two channels carrying the same publisher XML. It cannot detect publisher-side defects.
- Hindawi (prefix 10.1155) defects:
  - 8 journals lose 82 to 97% of records (D < 1 in 30 to 95%; accepted more than 7 days after publication in 82 to 96%).
  - All 8 are ineligible, but they sit in the "800 journals" and the variance-component run. BioMed Research International keeps 12.8% as a survivor set.
  - Six eligible journals keep only 30 to 69% of records (HLA 30%, Indian J Pediatrics 42%, J Plant Pathol 56%, JMRI 64%, Autophagy 66%, Colorectal Disease 69%).
- Verification: state frame composition and imprint-specific shortfalls in the abstract or limitations. Report E9 with its CI and call it uninformative on calibration. Report the ICC with and without the Hindawi journals.

**M3. "Journal turnaround" is a mixture of article types and batches.**
- 49 journals (48 eligible) have at least 10% of papers with D <= 14 days.
  - Their fast papers have median 11 references, 3 authors and 3 pages, against 31, 6 and 9 for slower papers. 44% have at most 3 pages, against 7%.
  - Within these journals Spearman(D, references) is 0.35, against 0.06 elsewhere. These are short items (letters, brief reports) that pass C5.
- C5 itself selects on speed. References below 5 remove 5.1% (O1) and 5.5% (O2) of papers with D <= 72, against 0.6% for D of 73 to 180 and 0.3% beyond.
- The H5 gain sits in the fast tail (5.7% at tau 0.10 against 0.5% at 0.90, `article_level_by_tau.csv`), so the covariates act as an article-type detector.
- Batch acceptance:
  - 7.1% of records share an accepted date with at least 10 same-journal papers and at least 5 times the journal's daily rate.
  - Integrated Ferroelectrics has 54% of its papers on one accepted date, Ferroelectrics 35%, and Arch Dermatol Res has 193 on 2024-04-26 (a supplement).
- Robustness (recomputed through the package):

| Variant | Journal-origins | Shortfall | F0 skill vs F2 | H4: share >= 0.5 |
|---|---|---|---|---|
| Base | 1,531 | -3.03 | 15.70% | 12.0% |
| Excl. batch records | 1,514 | -2.91 | 15.94% | 12.5% |
| Excl. 65 mixed/batchy journals | 1,406 | -2.96 | 15.40% | 9.7% |
| Refs >= 10 / >= 15 | 1,520 / 1,500 | -3.09 / -3.21 | 15.73% / 15.91% | 11.1% / 11.0% |

  Conclusions hold, and H4 stays far above 5%. But "share of journals accepting half of papers within 72 days" is partly a share of journals with a fast lane.
- New experiment: X3.
- Verification: add this table as a sensitivity analysis and describe the mixture in the Limitations.

## 3. MODERATE

**D1. Volume change and outcome-linked eligibility.** The log ratio of received counts (target half-year over the previous half-year) has a U-shaped relation to the shortfall: -5.6 (O1) and -4.2 (O2) in the top quintile, -2.1 and -1.5 in the middle (quadratic p = 0.007, journal-clustered). Eligibility needs n_test >= 50, a future quantity, and the frame is selected on 2023 volume. The O1-minus-O2 shortfall gap is only 0.76 points (CI -0.07 to +1.59), so I see no material contamination of O1. See X5.

**D2. Units, families and the drift ratio.**
- H3 small stratum: Wilcoxon p = 0.053 is called "borderline", but the direction is F4 worse (+0.0041) and the bootstrap CI of the mean difference [0.0003, 0.0081] excludes zero on the wrong side. The two tests disagree.
- Holm is applied separately to 3 strata and to 7 contrasts, so the family definition is inconsistent.
- H4 is stated per journal but tested per journal-origin. It survives: the Clopper-Pearson lower bound is at least 0.5 in 111 of 1,531 journal-origins (7.2%).
- H6's ratio of 7.3 is an uncentred mean ratio dominated by tails (the top 5% of pairs carry 53% of the sum of squares). The robust MAD-based ratio is 5.25.
- A date-block permutation null (whole accepted-date batches relabelled, 200-journal subsample) is about 41% larger than the iid null (ratio 8.3 to 5.9, so roughly 5.2 on the full sample and about 3.7 robust). H6 (> 1.5) holds, but "7.3 times" is overstated by 30 to 50%.
- Verification: one family definition, journal-level H4, robust and block-null drift ratios.

**D3. Right truncation is real but small and conservative.** D > 843 days is 0.25% of the O1 target and 0.08% of O2. Capping every target at D <= 730 moves the shortfall from -3.03 to -2.73, so primary-analysis truncation is at most 0.3 points, understating under-coverage. Springer 2026 records lack references in 10.9% of cases, so C5 drops 16% of O2's slowest bin (D > 730, 123 papers). The "follow-up at least 2.8 years" sentence is wrong for O2 (minimum 842 days = 2.3 years).

**D4. ICC and frame.** F0-F2 skill is positive in all 7 imprints (-0.028 to -0.044), so it is robust. The 26.5% ICC CI ignores imprint structure and includes the Hindawi survivors.

## 4. Checked and sound

- **Fairness of Hazen F0 (question e).** I added F9 (skew-normal MLE), F10 (publisher-pooled standardised shape with each journal's own median and IQR) and F11 (50/50 blend of F0 and F10). Mean pinball: F0 0.2019, F11 0.2022, F9 0.2034, F10 0.2035, F4 0.2044, F3 0.2047. Differences from F0 are +0.16%, +0.74%, +0.78%, +1.25%, +1.38%, all with CIs above zero; F0 beats F10 in 63% of journals. F0 does not win only through parametric misspecification, and shape borrowing is no better than own-sample quantiles.
- **Brier continuity correction.** Agent A's note that its absence "favours F0" has the wrong sign. F3 and F4 overstate P(D <= 72) (27.2% against 24.0% realised; F0 24.2%), and correcting at ln(72.5) widens the gap slightly (0.0034 to 0.0036). The lognormal families should not be used for "72-day" statements.
- **Duplicates.** Cross-listed DOIs occur only in the two known ISSN pairs (4,308 and 1,211 DOIs). 198 records in 95 groups share title and dates (0.01%, mostly co-published guidelines).
- D = 1 is 0.2%. Weekend acceptance is 16.6%. D <= 14 with accepted-to-online lag above 90 days shows no systematic pattern (5.6% against 4.3%).

## 5. Five new experiments (CPU-feasible, ranked by reduction in rejection risk)

1. **X1. Rolling-origin panel with equal follow-up and two-way block inference** (C1, C2, M1, M2).
   - Quarterly origins 2022-Q1 to 2024-Q2, 91-day targets, a common cap D <= 480. Estimate shortfall, width and skill per origin and imprint. Bootstrap imprint x origin blocks and give a predictive interval for a future origin.
   - Add an out-of-time recalibration: learn a widening factor up to t and test it on t+1. About 10 CPU-minutes.
   - Pass: a pre-declared claim with a CI covering origin and imprint variation, and a recalibrated F0 with 78 to 82% coverage.
2. **X2. Null calibration and a generative simulation** (C2, M1).
   - Permute target cohorts across journals within imprint; skill versus F2 should be about 0, which calibrates the 15.7%. Run a random split inside one cohort, which should give about -0.3.
   - Simulate Poisson arrivals growing at 0, 10 or 30%, lognormal D and the visibility rule, and check whether truncation and growth alone reproduce -1.5. Repeat the time reversal across all quarter pairs.
   - Pass: the no-drift simulation reproduces the visible-set shortfall within 0.5 points.
3. **X3. Article-type purification and a mixture forecaster** (M3).
   - Classify type by a two-component mixture on (ln refs, ln pages, ln authors) within each journal, plus title and DOI rules for supplements. Re-run F0/F4, coverage, the 72-day share and the ICC on research articles only.
   - Add a forecaster mixing the two lanes.
   - Pass: H4 and ICC reported by type, and a stated change in coverage.
4. **X4. Strictly out-of-time H5/E7.** Train LightGBM on O1 targets and earlier cohorts, test on O2 targets, with pre-submission features and journal-demeaned covariates, against a recalibration-only control, reported by tau. Pass: a gain quoted for a model that never saw the scored period. Expect about 1.4% or less.
5. **X5. Miscalibration model with out-of-time validation** (D1, M2). Regress the per-journal shortfall on imprint, log volume change and its square, batch share, fast-lane share and n_train using O1, then predict O2 against the best constant. Pass: either a gain in out-of-time mean squared error, or an explicit statement that the residual is irreducible.
