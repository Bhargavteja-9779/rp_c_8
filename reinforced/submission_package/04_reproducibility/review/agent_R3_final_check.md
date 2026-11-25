# R3 final methods check of Revised_Manuscript.docx (rewritten sections)

Scope: abstract, RQ2 text (where Table 2 is discussed), Calibration and its causes (RQ3), RQ4, Tables 2, 3, 5, Discussion, Limitations, Conclusions. Sources: reinforced/results/{Z_summary.json, metrics_cycle2.json, Z1_cohort_effect_null.csv, Z2_strict_recal.csv, Y1_panel_summary.json, X1_summary.json} and results/metrics.json (plus code in reinforced/code/src/z_experiments.py and cal_and_meta.py where a definition mattered).

Numbers that DO match (checked, no action): Table 1 all cells; Table 2 journal-cluster CIs, Holm p and publisher-level p; Table 3 all point estimates and CIs; the 77.0/76.4/-3.6 coverage figures; the panel figures (7,417 / 787, -3.4/-1.4/-2.5, lag-1 0.76, -2.4 [-2.9,-1.8], two-way [-3.4,-1.3], predictive -4.0 to -0.8, skill 16.2%); Z2 (F0 -1.9, R +1.9, V +1.1, F4 +1.3, pinball diffs, F2 +0.041); Z5 direction checks; RQ4 counts, CIs and reliability slopes (0.91 [0.88,0.94], 0.97 [0.93,1.00], Brier -0.0004); X1 shares (95%/2.6%/82%/8.9%/47%); drift 7.3/5.3/53%.

## Findings

1. **MAJOR - Journal-mean point estimates paired with imprint-mean intervals (abstract, RQ3, Table 2, Table 5).**
   - Abstract: "covered 77.0% of later papers (journal average; imprint-level interval for the shortfall -4.2 to -1.1 points)"; RQ3: "shortfall of -3.0 points ... widened to -4.2 to -1.1 with a t(6) interval over imprints"; Table 5 H2: "journal mean -3.0; paper-weighted -3.6; imprint t(6) CI [-4.2, -1.1]".
   - Source: Z_summary.json Z3 `F0_shortfall_journal_mean_imprint_cluster`: mean of imprint means = **-2.68 points**, t6 CI [-4.23, -1.14]. The interval is centred on -2.7, not -3.0. The imprint-cluster bootstrap around the journal mean (Y0 H2_spec_curve) is [-3.96, -2.00].
   - The same mismatch runs through Table 2: the "Mean difference" column is the journal mean (F0-F2 -0.0376, F4-F0 +0.0025, F3-F0 +0.0028, F6-F0 -0.0008, F1-F0 +0.0008, F4-F6 +0.0033) while the "Imprint t(6) CI" column is centred on the mean of imprint means (-0.0331, +0.0030, +0.0032, -0.0007, +0.0005, +0.0037). Visible symptoms: F1-F0 +0.0008 sits near the top of [-0.0001, +0.0011]; F0-F2 -0.0376 sits near the lower end of [-0.0396, -0.0267]. The RQ2 text repeats it ("-0.0376; ... imprint t(6) CI -0.0396 to -0.0267").
   - Fix: add a column (or footnote) "mean of 7 imprint means" and give the t-interval with its own centre (-2.7 points; -0.0331, ...), or state in every caption/sentence that the t interval is for the imprint-averaged quantity. In the abstract write "imprint-averaged shortfall -2.7 points, t(6) interval -4.2 to -1.1".

2. **MODERATE - "reproduced its order of magnitude (-2.8 to -4.9)" misstates what was simulated (abstract).**
   - Quote: "random cohort-level shifts of the size of the journal x year variance reproduced its order of magnitude (-2.8 to -4.9 points)".
   - Source: Z1: sigma^2 -> -4.9 [-5.0,-4.7]; sigma^2/2 -> -2.8; 2sigma^2 -> -8.9; observed -3.0. The "size of the variance" simulation overshoots by 63%; -2.8 is the half-variance run. Also 2sigma^2 (-8.9) is omitted from the range.
   - Fix: "shifts with the variance of the journal x year component gave -4.9 points and with half that variance -2.8, against -3.0 observed; this is a consistency check, not identification". Drop "reproduced".

3. **MODERATE - Causal/explanatory language contradicts the "no causal claims" statement and outruns a sigma^2 estimated from the same data.**
   - Quotes: Background "(RQ3) why do such forecasts miscalibrate ... The study ... makes no causal claims"; Discussion "we read the shortfall as a variance-inflation effect (a forecast that ignores the variance of the next cohort's location is too narrow)"; RQ3 "Direction and selection checks were consistent with this reading".
   - Evidence: Z1 is a forward simulation with sigma^2 = sigma2_year from the same data (z_experiments.py: `sigma2_year`); the journal proxy `jp` is also built from the same drift pairs. Observed spread (SD 8.6 vs 2.8 points), imprint pattern (-5.6 to -1.0 vs about -4.6 to -5.2 simulated) and journal-level correlation (0.16 common, 0.36 proxy, in-sample) are not reproduced. Any real nonstationarity yields a journal x year component, so "shifts of that size produce a shortfall" is close to tautological.
   - Fix: replace "we read the shortfall as a variance-inflation effect" with "a cohort-shift mechanism of the observed size is sufficient to produce a shortfall of this order, but the data do not identify it"; reword RQ3 in the Background as "what accounts for / is compatible with"; delete "consistent with this reading" or say the backward-oracle result only argues against a one-directional trend.

4. **MODERATE - The "oracle" simulation is a tuned construction, not the stated one, and its match to -1.5 is weak support.**
   - Quote: "with the target shift halved (an oracle information set) it was -1.6 points, close to the -1.5 observed with the complete submission cohort"; same in Methods and Table 3.
   - Source: z_experiments.py, mode "orc": training shift a = 0 and target shift b ~ N(0, sigma^2 x 0.5), i.e. the target VARIANCE is halved (sd x 0.71, not "halved") and the training shift is removed. The 0.5 factor is a free choice made to represent the oracle set.
   - Fix: describe it exactly ("no training-cohort shift; target-cohort shift variance sigma^2/2") and say the 0.5 was an assumption, so the agreement with -1.5 is not an independent confirmation. Note that the observed value (-3.0) also lies much nearer sigma^2/2 than sigma^2.

5. **MODERATE - "robust at the level of three publishers" for the shortfall is not supported by the cited test.**
   - Quotes: RQ2 "only two findings were robust at the level of the three publishers: the value of journal information (F0 - F2) and the coverage shortfall below"; Discussion "only the value of journal information and the existence of a shortfall were robust"; Limitations "at publisher level only ... the shortfall were clearly nonzero".
   - Source: Z3 `F0_shortfall_journal_mean_imprint_cluster`: publisher-level p = 0.024 (t, 2 df, no Holm; it is not one of the "seven contrasts"), publisher means -3.3/-3.6/-2.1. The sentence places it inside "Holm adjustment over seven contrasts (Table 2)", which it is not.
   - Fix: "the shortfall had the same sign in all three publishers (publisher-level p = 0.024, unadjusted, 2 df)"; replace "robust"/"clearly nonzero" with "consistent in sign" and say the shortfall is not in Table 2 nor Holm-adjusted.

6. **MODERATE - "All three therefore over-corrected, because the maps were learned from early origins" does not apply to F4 and is an untested causal reading.**
   - Quote: "R +1.9, V +1.1 and the empirical-Bayes F4 +1.3 ... All three therefore over-corrected, because the maps were learned from early origins at which the shortfall was larger (-3.4 to -2.4 points) than at the evaluation origins (-1.4 to -2.5)".
   - Source: F4 has no map learned from earlier origins (Z2 F4 = ordinary empirical-Bayes lognormal; it over-covers at +1.0 in the main analysis too). The range comparison picks endpoints: the last evaluation origin (-2.5, April 2024) equals the 4th early origin (-2.4, October 2022).
   - Also: R's absolute coverage error equals F0's (1.9 vs 1.9); V reduces it (1.1 vs 1.9; by origin V +1.5/+1.1/+0.4 vs F0 -1.4/-1.9/-2.5). "Over-corrected" and "unstable" (3 overlapping origins) overstate relative to "R did not reduce the coverage error; V reduced it but overshot at the early origin".
   - Fix: restrict "over-corrected" to R and V; treat F4 separately; say the early-origin explanation is a hypothesis; add the by-origin V/R numbers.

7. **MODERATE - L (learned forecaster) coverage is omitted although it contradicts "no dependable remedy", and L shares the look-ahead caveat.**
   - Quotes: Discussion "a simple correction is not a dependable remedy"; Table 5 X3 "Supported (L trained on one or two cohorts, untuned: weak test) +0.0002 [-0.0002, +0.0007]".
   - Source: metrics_cycle2.json cal_meta: F10 (= L) `cov80_minus_nominal` mean -0.0002 (-0.02 points; CI -0.47 to +0.41), width 1.65, vs F0 -2.46 and F9 (look-ahead R) +1.36 at the same origins (2024-01, 2025-01; 771 journals). So an out-of-time-trained model reached nominal coverage at no pinball cost. This is from the same cal_and_meta.py run whose labels the Methods say were not restricted to complete cohorts, and the 2025 target is censored; neither caveat is attached to X3.
   - Fix: report L's coverage next to its loss, state the look-ahead/censoring caveat for X3, and soften "no dependable remedy" to "the simple corrections tested here over-corrected at three origins; a learned correction reached nominal coverage in a look-ahead-affected run".

8. **MODERATE - Table 5 H5 and H7 verdicts differ from the pre-specified tests.**
   - H5 quote: "Specification-dependent; pre-submission features 1.0% (supported); with references 3.0% (not supported)". Source: the pre-specified H5 test (metrics.json hyp H5, covariates including reference count) was rel_gain 3.36% [2.56, 4.13], `supported: False`. The 1.0% figure is a post hoc strict-OOT specification (Y4) and the in-sample pre-submission-only variant was 1.6% (R2). Fix: report "Not supported (3.4%, pre-specified); 1.0% with pre-submission-only features in a post hoc strictly out-of-time model".
   - H7 quote: "12-month window beats 24-month window: Not supported; F1 - F0 +0.0008; imprint t(6) CI -0.0001 to +0.0011". Source: Table 2 itself has journal-cluster CI [+0.0003, +0.0013] and metrics.json F1-F0 Holm p 2.4e-6 (journal-level Wilcoxon, the pre-specified test); only the imprint-level and publisher-level tests (p 0.071 / 0.57) fail. Also +0.0008 is paired with an interval centred on +0.0005 (see item 1). The RQ2 text "F1 - F0 was not distinguishable from zero" ignores the journal-cluster CI. Fix: "Supported at journal level (+0.0008, CI +0.0003 to +0.0013), not at imprint/publisher level", or label the verdict "inconclusive".

9. **MODERATE - Journal-set / origin-set mixing in the abstract and RQ4 reliability statements.**
   - Quote (abstract): "12.0% of journal-origins accepted at least half ... within 72 days ...; forecast probabilities for this event were too extreme (reliability slope 0.91)".
   - Source: 12.0% is from the main 2-origin, 182-day evaluation (1,531 journal-origins); the slope 0.91 is from Z2 strict origins (Oct 2023/Jan 2024/Apr 2024, 480-day cap, 91-day cohorts, n = 2,258). The "highest bin 23 journal-origins, forecast 86%, realised 75%" is again from the main set (metrics.json high_bin_72) and is presented in the same paragraph as the strict-origin slope. The abstract's recalibration figures (+1.9, +1.1) are likewise strict-set values with a different F0 baseline (-1.9) than the -3.0 quoted just before.
   - Fix: add "(strict-evaluation origins)" in the abstract after the slope and after the +1.9/+1.1 figures, and state F0's baseline in that set (-1.9).

10. **MODERATE - Overstated attribution of the fast-journal share (RQ4).**
    - Quote: "A substantial part of this share is therefore due to journals with a fast lane for some article types."
    - Source: 12.0% -> 9.5% (no fast-lane journals) or 8.9% (75 flagged excluded): roughly one quarter removed; three quarters remain, and every variant still exceeds the 5% threshold. Fast-lane exclusion also changes the journal set (733/708 of 781).
    - Fix: "about a quarter of this share is attributable to flagged or fast-lane journals; the remainder persists in every variant" and note the set change.

11. **MINOR - X1 "same pattern" for fast-looking journals mixes weightings and publishers.**
    - Quote: "Journals whose medians looked fast (30 journals, 391 articles; median D 70 days) showed the same pattern (93% and 4.6%)", following Springer-Nature-only numbers (95%, 2.6%).
    - Source: X1 `ResearchSquare_fast_looking` (all Research Square preprints, not SN-only) 0.926/0.046; Z4 gives n_fast_journals 24 (SN) with journal-weighted <=14 d share 0.735 (vs 0.82 overall). Fix: state the set (all publishers, paper-weighted) or give the SN journal-weighted 73%.
    - Related, abstract: "95% ... (journal-weighted 82%)" omits the journal-weighted 8.9% >90 days (1 in 11), which is given in Results. Median offset "from -22 to -7" excludes 2020 (-29, n = 9); say "2021-2025".

12. **MINOR - "U-shaped" and pooled-vs-two-way centres in the panel description.**
    - Quote: "a U-shaped course ... The pooled panel shortfall was -2.4 points ... two-way imprint x origin CI -3.4 to -1.3".
    - Source: Z6 origin means decline monotonically to -1.4 (Spearman 0.98 over the first 8 origins) then a two-point rebound; the two-way estimate is -2.23, so [-3.4,-1.3] is not centred on -2.4. Fix: "declined from -3.4 to -1.4 and partly rebounded to -2.5"; quote -2.2 with the two-way CI.

13. **MINOR - Sentence fusing two different analyses.**
    - Quote: "A journal-specific proxy for sigma^2 correlated 0.36 with the observed journal shortfall ... and was out-of-time unpredictive in the earlier analysis (R^2 0.001)".
    - Source: Y4_Y5 `Y5` is a LightGBM on logvol/fastshare/instability/sd/n_train/imprint predicting 2024 shortfall from 2023 (R^2 0.0011, corr 0.18); it is not the sigma^2 proxy, and the 0.36 correlation is in-sample on the same data. Fix: separate the two statements and name the Y5 predictors.

14. **MINOR - H2 wording.** "Under the pre-specified rule (a CI excluding +-3 points) the verdict ... is therefore inconclusive" implies the widening caused it; the journal-cluster CI [-3.5,-2.6] already contained -3 (metrics.json H2 `supported: False`). Say "the pre-specified criterion was not met at either level; inconclusive rather than negative".

15. **MINOR - Other wording/overclaim.**
    - Abstract/Conclusions: "three publishers (the effective number of independent clusters)" asserts what is a conservative assumption; write "treated as".
    - X2 row: V (+1.1) lies inside the +-1.5 criterion and R's loss difference is non-positive; "Not supported" rests on R's +1.9 and V's +0.0001 loss, so say which part failed.
    - RQ3: "A one-parameter correction ... is thus a partial and unstable remedy" - R is a quantile map, not one parameter; "unstable" rests on 3 overlapping origins.
    - Discussion: "across three publishers and all fields" (frame is the high-volume 150-3,000 article journals of three publishers; Elsevier excluded) and "our results quantify how much a single past statistic can mislead" (they quantify forecast error, not reporting inconsistency).
    - Conclusions: "supported for a minority of journals" - the measured quantity is journal-origins (12.0%; 15.2% of journals in any origin, metrics.json post).
    - Skewness quoted (-0.79) is from 787 journals (`shape`), not the 781 evaluated.

## Verdict

The rewritten sections are numerically careful: I found no figure in Tables 1-3, the panel, Z2, RQ4 or X1 that disagrees with its source file, and the manuscript is commendably explicit that the cohort-shift simulation is a consistency check. The problems are interpretive. The largest is the systematic pairing of journal-mean point estimates with intervals centred on imprint-mean quantities (abstract, RQ3, Table 2, Table 5), which should be fixed before submission. The abstract then says the simulation "reproduced" the shortfall at "the size of" the variance when that run overshoots by 63%, the Discussion adopts a variance-inflation "reading" that sits uneasily with the "no causal claims" statement, and the oracle simulation's match is partly tuned. The claim that the shortfall and journal information are "robust" at publisher level rests on an unadjusted 2-df p of 0.024. The remedy narrative ("over-corrected ... because early origins") is untested, does not apply to F4, and omits the learned forecaster's near-nominal coverage from the same look-ahead-affected run. Table 5's H5 and H7 verdicts depart from the pre-specified tests and read more favourably or neutrally than the confirmatory result. None of this overturns the main empirical findings (journal information helps by about 16%, intervals are wide, 80% intervals cover about 77%). After the edits above, I would consider the text defensible as an observational description with an explicitly speculative mechanism.
