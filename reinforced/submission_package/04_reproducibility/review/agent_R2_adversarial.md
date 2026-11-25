# Adversarial review R2 of the revised manuscript (cycle 2)
Reviewer: independent agent, same model family as the authors' assistant; no human involved. Own computations: `/tmp/claude-0/scr/c1-c4.py` (nothing written to the repo; pipeline not re-run). Items the register marks RESOLVED are re-raised only where the fix is wrong or incomplete.

## Verdict
The numbers are traceable (28 checked, 3 discrepancies, all small). The science is honest, but cycle 2 introduced four new weaknesses. Three are fixable with cheap, local re-analyses:
1. The Y2 "null worlds" do not test the null they claim, and the paper's own variance component predicts the unexplained shortfall.
2. The recalibration labels look ahead of the origin, and the 2025 test cohort is right-censored.
3. The imprint-cluster CI with 7 clusters is anti-conservative.

The fourth, scope fit with RIPR, is not fixable by analysis. Residual rejection risk: **high at RIPR triage (editorial), moderate at a scientometrics journal (QSS)**. Fatal: none to the science; FATAL for the chosen venue is the scope question (R2-10).

Severity: F FATAL, C CRITICAL, MJ MAJOR, MO MODERATE, MI MINOR.

---
## Pass 1. Novelty and contribution
**R2-01 (MJ) The headline "cause" is nearly tautological and was left unexplained by a mis-specified null.** The central RQ3 result, "non-exchangeability between cohorts", says a forecast fails because the future differs from the past.
- Evidence (my calculation, c3.py): the manuscript's own variance components (journal × year 0.0321, within-journal residual 0.5027; `results/variance_components.json`) predict the shortfall. Simulate a train cohort and a test cohort, each with an independent N(0, 0.0321) location shift, n_train 350, n_test 150, and a 10-90 empirical interval. This gives **-3.2 points**, against -3.0 observed. If the test cohort shifts only half as far (the oracle's average half-year offset), it gives -1.2, against -1.5 observed.
- This is a normal-approximation calculation, not a fit, but it shows the shortfall is the expected consequence of RQ1's 4.4 % journal × year share. The discussion never links the two, so "unpredictable instability" and "characterised not identified" overstate the mystery.
- RQ3 reduces to "interval width ignores cohort variance", a small effect of about 3 points.
- New experiment: Y2(d), a generative null with random cohort effects at the estimated σ²_jy (journal-specific if possible), with the visibility rule. Corrective action: report predicted against observed shortfall (overall, by imprint, oracle and truncated variants) and recast RQ3 as a variance-inflation result. Verification: the simulated shortfall falls inside the observed CI, and the revised abstract drops the "stationary simulation, indicating non-exchangeability" phrasing.

**R2-02 (MO) The headline skill (15.7 % vs F2) is mechanical.** F2 ignores journal identity, so the gain is the ICC (26.5 %) in loss units; it is a straw baseline, and no statistic a journal actually publishes is compared. Action: add a field-pooled baseline or reword.

**R2-03 (MO) The reporting-integrity framing has no evidence behind it.** No journal's published speed claim is collected or evaluated, and the "commercial tools ... we found no validation" sentence is uncited. The 2026 aggregator pages (Manusights, ilovephd) are exactly such statistics. Action: cite them and score at least one against realised outcomes.

## Pass 2. Domain significance for RIPR readers
**R2-04 (F for RIPR) No integrity or peer-review variable.** Peer review is never observed (accepted-only date stamps), and the editor will see that. The register already marks this OPEN. My additional points:
- A 3-point under-coverage is of little practical consequence; forecaster differences are below 2 % of loss; four of five original hypotheses failed; one discussion paragraph carries the integrity link.
Action: pre-submission scope enquiry, or retarget (QSS, Journal of Informetrics).

## Pass 3. Competing literature (search through Oct 2026)
Web searches found **no new out-of-time forecasting study**, only 2026 commercial aggregator "benchmarks" (Manusights, ilovephd), a 2026 PMC piece on delays and early-career harm (PMC12913549), uncited, and Royle 2026, in the matrix but not cited.

**R2-05 (MO)** The manuscript says the PubMed-wide plan (Dianovics et al.) had "no results available when we searched", but `competing_work_analysis.md` records "evaluation complete 13 Apr 2026". Either results exist and must be compared (that study uses a random split, so it is directly contrasted), or the sentence should say the status could not be established. My search did not retrieve the record, so this is unverified. Action: re-check the Lifecycle Journal/OSF record; cite Royle 2026.

## Pass 4. Experimental design
**R2-06 (C) Y2 does not test the null it claims.** Three problems:
- (a) Y2(b), the random split inside a pooled cohort, returns about 0 by construction for any iid sample. It rules out finite-sample error only, which was never plausible at n ≥ 100.
- (b) Y2(c) draws durations from the journal's own target-cohort ln D (`rng.choice(yt, ...)`). Train and test are therefore identical in distribution by design. It is circular. It can only show that growth plus truncation produce zero bias if there is no drift; it cannot show that drift or cohort effects produce the bias.
- (c) The sim's correlation with the observed journal-level shortfall is 0.04 (`Y2_summary.json`). The simulation does not reproduce the cross-sectional pattern, only a mean of about 0.
The positive test is Y2(d) from R2-01. The authors' own conclusion ("cause not identified") is therefore right but needlessly weak. Verification: Y2(d) reproduces the mean (-3.0), the oracle (-1.5) and the correlation with journal-level σ²_jy.

**R2-07 (C) Recalibration labels look ahead of the origin, and the 2025 test is censored.**
- `cal_and_meta.py` says labels were "complete before the test origin (accepted by 2023-07)". That is false for the tail. The maps use whole target cohorts (data to 20 Oct 2026). In the 2022H1 cohort **0.94 %** of papers (2023H1: 0.97 %) were accepted on or after the test origin (my c1.py), and they are all above the 90th percentile. This inflates the correction by about 0.7 points (0.766/0.991). The raw +1.4 over-correction therefore partly reflects the leak. The leak widens the intervals, so it is conservative, but it breaks the stated "earlier cohorts only" rule.
- At the 2025 origin the target cohort has follow-up of only 476-660 days. The share with D > 480 d is **0.66 %**, against 2.4-2.8 % in complete cohorts. Maps learned on complete cohorts are applied to a truncated cohort, which raises coverage by roughly 0.6-1.3 points. With a common 476-d cap, my recomputation gives F0 shortfalls of -2.84 (2023), -2.22 (2024) and -2.22 (2025), against -3.35 / -2.65 / -2.29 uncapped.
- Why it matters: abstract and Table 5 report "+1.4 restored coverage, X2 supported". Part of the over-correction, and the 2025 half of every X2/X3/X6 number, is design artefact. Y1 applied the completeness rule properly; X2/X3/X6 did not.
- New experiment: rerun X2/X6 with labels restricted to accepted < t0 and with a common cap (or drop 2025). Verification: corrected R coverage reported with CI; the "within ±1.5" criterion is evaluated on the corrected run.

**R2-08 (MO) Frame selection uses future information.** Journals were chosen by 2023 volumes and dating completeness, yet are evaluated from January 2022, and eligibility requires ≥ 50 target papers in the future window. Survivorship and volume-growth selection are not discussed (the simulation's mechanism is volume growth). Action: sensitivity run with eligibility from pre-origin data only.

**R2-09 (MO) Time ordering and trend claim.** The text says the panel shortfall "ranged from -1.5 to -3.4 ... without a monotone trend". The ten origin means are -3.37, -3.33, -2.85, -2.41, -2.64, -2.31, -1.48, -1.45, -1.90, -2.49. Over the first eight origins Spearman ρ = 0.98 (monotone shrinkage) before a reversal. Lag-1 autocorrelation is 0.76, so the origin bootstrap treats strongly dependent units as iid, and the "predictive interval for a future origin" (t with 9 df) is too narrow. Action: describe the pattern as a U-shape, use a block or AR-adjusted interval. A moving-block bootstrap I ran gives about [-3.2, -1.2], close to the reported interval, so this is mostly wording.

## Pass 5. Statistical validity
**R2-10 (MJ) Imprint-cluster inference with 7 clusters is anti-conservative.**
- The percentile bootstrap resamples only 7 clusters. For the F0 shortfall, a t(6) interval on the 7 imprint means is **[-4.2, -1.1]**, against the reported [-4.0, -2.0].
- Table 2 shows its own inconsistency: F1-F0 has an imprint-bootstrap CI of [+0.0001, +0.0012] (excludes 0) next to t-test p = 0.071.
- The 7 imprints are not independent. Springer, BMC and Nature belong to one publisher, Wiley and Blackwell to another. The effective cluster count is 3 (publishers), so "7/7 imprints" is really 3 publishers.
- The H2 verdict ("inconclusive") survives, but the CIs in the abstract and Table 2 are too tight.
- Action: report t(6) intervals and state the effective cluster number.

**R2-11 (MO) The "SD 8.4 vs binomial 3.2 points" comparison uses the wrong benchmark.** The binomial formula ignores the sampling noise of the training quantiles. An iid simulation at the observed sizes gives SD 3.9; adding the random cohort effects of R2-01 gives 5.6 (c4.py). The excess over 8.4 is real but smaller than shown; heterogeneous σ²_jy could close the rest. Y5's R² of 0.001 is probably null because the cohort effect is unpredictable by construction.

**R2-12 (MO) Multiplicity.** Imprint-level contrasts and Table 4 variants are not Holm-adjusted (cycle 1 did adjust). The X6 text says CIs "excluded zero in 3 of 6", but `X4_X5_X6_summary.json` shows **4 of 6** (2024-T72 and the three 2025 thresholds), a discrepancy and an unadjusted count. Action: correct the count, apply Holm or call the results descriptive.

**R2-13 (MJ) The X1 probe inference is overstated.**
- Sampling: up to 30 per journal, from an interrupted, time-limited pull; restricted to self-selected Research Square "In Review" authors in 212 Springer Nature journals.
- "95 % of received dates ≤ posting + 14 d" is paper-weighted (top journals contribute up to 30 articles each). The **journal-weighted share is 82 %** (my c-script on the partial file). The paper's own principle is journal as unit of analysis.
- Temporal instability, unreported: the median of received minus posted moves from -7 to -10 d (received 2021-2023) to **-22 and -21 d** (2024 and 2025). The relationship used to validate `received` shifted by about two weeks during the forecast period. The forecasting design needs temporal stability of the date definition, which X1 does not test.
- The "posted about two weeks after receipt" explanation is inferred from the same data that it is then used to explain.
- The test cannot detect a systematic shift of up to 14 d (about 11 % of median D), which matters for 72-d claims.
- Table 5 gives X1 "Supported" while the pre-set criterion (≥ 70 % within ±14 d) failed at 47 %. This is relabelling after the fact (HARKing), and C2-3 admits it.
- Action: Table 5 should read "pre-set criterion failed; post hoc statistics compatible"; add journal-weighted and by-year results.

**R2-14 (MO) "Supported" for exploratory and post hoc X-hypotheses.**
- X2 "Supported" although the CI [+0.9, +1.8] is not within ±1.5 and the panel over-corrected.
- H5 is flipped to "specification-dependent" after the original pre-specified model (with reference counts, 3.4 %) failed. The strictly out-of-time model replaced it.
- H6/H7 are labelled exploratory in the rows, yet the Table 5 caption says "H1-H7 pre-specified in cycle 1", and Methods says "five hypotheses" and later "Seven of the first-cycle hypotheses were evaluated as pre-specified". Fix the caption and the text.

**R2-15 (MO) The "past evidence overstated future speed at the fast end" claim.** 23 journal-origins (19 journals) were selected on forecast ≥ 0.8; realised 75 % against mean forecast 86 %. This is selection on a noisy predictor (winner's curse), with no CI and no correction. It is used in the Discussion as a substantive finding. Action: use the reliability regression with a CI, or shrinkage-adjusted expectations; otherwise delete.

## Pass 6. Baseline fairness (F0 vs R vs L)
**R2-16 (MO)** L is trained on 1 cohort (about 770 journals) for the 2024 test and 2 cohorts for 2025, with `min_child_samples = 300` on rows replicated per paper, run once with no tuning. A negative result there ("learned forecasters did not beat F0") is weak evidence: the effective n is small and the learner cannot learn a time-varying bias. R is effectively F0 widened by a constant.
- Fair comparators for R are a constant width inflation and F4 (coverage +1.0 without any map, 1.2 % loss cost).
- F6 beats F0 in 7/7 imprints (p = 0.002), yet the text says "the simplest estimator was hard to beat".
- Action: add a variance-inflation baseline and a comparison of R with F4; soften "hard to beat"; state L's effective n.

**R2-17 (MI)** The Methods define origins as January 2023 and 2024 only, while R, L and X6 results use a 2025 origin and a different journal set (755-766). The text mixes the 1,531 journal-origins of Table 1 with these. Add the 2025 origin to the Methods and label the sets in each table.

## Pass 7. Generalization
**R2-18 (MJ)** Frame: three publishers that deposit dates, 56 % Springer Nature, no Elsevier, IEEE or society publishers; dates validated only for Springer Nature journals with Research Square. A claim in the abstract ("a journal's last year of acceptance times ...") is stated for journals in general. E9 (30 PubMed journals) gives a CI [-3.6, +2.1] that cannot distinguish zero from the main result; the manuscript correctly does not call it replication. Leave-one-publisher-out ranges -3.5 to -2.5, which supports stability inside the frame only. The title says "800 journals" while 781 were evaluable, 708 after exclusions, and 787 in the panel. Action: put "three publishers" in the title or abstract first line, and use 781 in the title.

## Pass 8. Reproducibility
Checked against files, all matching: 1,737,272 / 1,829,907 records, median 124 d, 22.8 % <= 72 d; ICC 26.5 % [24.7, 28.3], jy 4.4 %, residual 69.1 %; all Table 1 values; 1,531 journal-origins; F0-F2 and its imprint CI; paper-weighted 76.4 %; imprint extremes; panel 7,417 / 787 / -2.2 / PI / 16.2 %; Y2, oracle and truncated rows; recalibration map and +1.4 [+0.9, +1.8]; loss differences; drift 7.3 / 5.26 / 53 % / 18.8 %; 184 (12.0 %) and 25 (1.6 %); field shares; Table 4 (Y3 JSON); 8.9 %; Y4 gains; X1 counts and shares; E9 -0.7; skewness -0.79; Y5 R2. Total 28.

Discrepancies and traceability gaps:
- **R2-19 (MI)** X6 "3 of 6" should be 4 of 6 (see R2-12).
- **R2-20 (MI)** The "backward oracle found by an independent reviewer" appears only in `agent_DEF_methods.md` ("-1.14 to -2.59"), with no result file or script. It sits in the main text next to reproducible numbers. Add a script and result file, or remove it.
- **R2-21 (MI)** `cal_and_meta.py`'s docstring is factually wrong (see R2-07). There is no single cycle-2 run script, no persistent-identifier deposit (R19 open), and no manifest hash for the partial probe file.
- Y1/Y2 share one `rng` across loops, so results depend on execution order; pin seeds per experiment.

## Pass 9. Journal fit and RIPR compliance
Checks (the RIPR guideline page returned an authentication redirect when I fetched it, so I relied on the AIJ report's retrieved text and my own counts):
- Abstract 345 words (limit 350; thin margin); main text about 4,000 words (< 5,000 guidance); numeric Vancouver citations (journal names unabbreviated, acknowledged); separate Limitations; LLM use in Methods; abbreviations list present.
- Remaining: no persistent-identifier deposit; author-specific placeholders; the abbreviations list defines "Q1 ... not asserted", an odd item.
- **R2-22 (MI)** The Methods sentence "The authors must verify the analyses and take responsibility" is normative, not a disclosure; reword. The cover letter should not call the AI-run reviews independent peer review.
- The timeline brief (≤ 72 d) is not met by RIPR (median 132 d); this is recorded as OPEN (R10), not repairable.

## Pass 10. Overall rejection risk and strongest argument
**Strongest rejection argument (reviewer view):** "This is a descriptive scientometric exercise on accepted-only date stamps from three publishers, whose date semantics are validated for one publisher in a self-selected subset, and whose own variance decomposition predicts the principal 'finding' (a 3-point under-coverage) that the authors present as an unexplained phenomenon. The proposed remedy was evaluated on a cohort with look-ahead labels and a censored 2025 target, and over-corrected. Four of five original hypotheses failed and several 'supported' verdicts were re-defined after the data. Peer review itself is never observed, so the paper does not belong to a research-integrity journal."

Probabilities (judgement, not computed): desk rejection at RIPR on scope is more likely than not; if reviewed, major revision is the best case. At QSS or Journal of Informetrics: major revision likely, with R2-06, R2-07 and R2-10 as the main points.

## Prioritised corrective plan (cheapest first)
| # | Action | New experiment | Verification |
|---|---|---|---|
| 1 | Y2(d): random cohort effect null at estimated σ²_jy; rewrite RQ3 and abstract (R2-01, 06, 11) | yes, hours | simulated shortfall within observed CI; correlation with σ²_jy |
| 2 | Re-run X2/X6/L with labels restricted to accepted < t0 and a common follow-up cap; drop or flag the 2025 origin (R2-07) | yes | corrected coverage and CI; docstring fixed |
| 3 | t(6) imprint CIs, publisher-level clusters; fix the 3 vs 4 of 6 count; Holm; fix Table 5 caption, "five vs seven" hypotheses, X1/X2/H5 labels (R2-10, 12, 14, 19) | no | tables regenerated |
| 4 | X1: journal-weighted and by-year deltas; temporal stability caveat; state the 14-d resolution limit (R2-13) | no (existing file) | new rows in Results; limitation text |
| 5 | Soften or delete the fast-end claim, "hard to beat", "characterised not identified" (R2-15, 16) | no | text diff |
| 6 | Sensitivity for forward frame selection; baselines (field pool, width inflation, R vs F4) (R2-02, 08, 16) | yes, modest | new Table 4 rows |
| 7 | Scope enquiry or retarget; persistent-identifier deposit; Dianovics status; cite Royle and aggregator pages (R2-03, 04, 05) | no | editor reply; DOI in the statement |
