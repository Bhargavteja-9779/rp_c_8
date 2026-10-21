# Independent review (Agent A): "How well do a journal's past turnaround times predict the next paper's?"

Reviewer stance: skeptical, no prior knowledge of the project. I did not read `review/` (earlier review passes). I read the manuscript (docx), `research_design/`, `code/src/tdelay`, `results/`, `literature_review/novelty_map.md` and `journal_selection/`. I wrote nothing outside this file. My scratch scripts read `data/processed/articles_clean.csv.gz` only.

## 0. Verdict in brief
The engineering is careful and the headline numbers reproduce. I found no look-ahead bug in F0-F6. The weaknesses are in interpretation, in how "pre-registered" is represented, in one confirmatory test (H5) that rests on a non-pre-submission covariate, and in an untested causal attribution (drift). The contribution is modest. Recommendation: **major revision**.

## 1. Recomputation of headline numbers
These all match the manuscript:
- `metrics_journal_origin.csv`: 1,531 journal-origins, 781 journals, 298,469 target papers.
- Journal-mean pinball for F0 / F2 / F4 / F6 is 0.2019 / 0.2395 / 0.2044 / 0.2011. Skill of F0 over F2 is 15.70%.
- F0 80% coverage is 0.7697, so the shortfall is 3.03 points (bootstrap CI [-3.49, -2.57]).
- exp(mean width) = 4.97. The "five-fold" claim is right, but it is a geometric mean (arithmetic mean ratio 7.2, median 4.2).
- Realised P(D<=72) >= 0.5 / 0.8 / 0.9 in 184 / 25 / 7 origins. The 23 origins with forecast >= 0.8 have mean forecast 0.864 and realised share 0.750.
- Brier skill at 72 d is 0.172. Drift ratio is 7.338 over 3,105 pairs, with median |delta| 0.088 and 18.8% above 0.2.
- Variance components: I re-ran `variance.components` and got ICC 0.2650. An independent one-way unbalanced ANOVA gives 0.271, so the estimator is sound.
- Contrasts, Holm p-values, H3 strata, Table 3 and E8 agree with the CSV/JSON files.
- Step-0 numbers for Accountability in Research (median 105.5 d, 27.4% <= 72 d, n = 164) reproduce.

## 2. Code audit
No look-ahead found.
- `split_journal_origin` restricts training to V, accepted and received all before t0. The F2 pool and F4 prior use visible data only (D2), and the unit test perturbs post-origin outcomes and the prior is unchanged.
- The Hazen weighted quantile, Winkler, pinball, Holm, Clopper-Pearson and DerSimonian-Laird formulas are correct.
- The runtime "no leakage" assertion (`set(test.doi)` disjoint from `set(tr24.doi)`) is **tautological**. A target paper has received >= t0 and D >= 1, so it can never satisfy accepted < t0. It says nothing about real leakage (see MD5). The synthetic tests have no publication lag, so they cannot detect truncation effects.
- Minor: F3/F4 use a continuous CDF at ln(72) without continuity correction while F0 uses an exact discrete ECDF, slightly favouring F0 in Brier scores. Bootstrap B is 1,000 (variance), 2,000 (E7) and 5,000 elsewhere, whereas the manuscript states 5,000.

## 3. Issues

### MAJOR

**M1. "Pre-registered" is overstated and the deviation record is incomplete.**
- Evidence:
  - The registration is a local git commit (6a9c4a9, 2026-10-20 18:10), written by the same agent that wrote the code and manuscript. There is no external time-stamp. Commits span about 9 hours in total.
  - The manuscript says "Five post-freeze amendments (all before the confirmatory run...)". `deviations.md` now has D1-D7. D5 was made after E9 output was seen. D6 and D7 were made after the results.
  - H7 was silently substituted. `hypotheses.md` says 12 mo vs **36 mo**; the manuscript's Table 4 reports 12 vs **24 mo** (F1 - F0 = +0.0008). `hypothesis_summary.json` has no H7, and no deviation is logged.
  - E7 differs from protocol §8. The protocol predicts y minus the F4 median. The code feeds the F4 quantile as a feature and predicts y. This is not logged.
  - Thresholds (5%, 3 pt, 2%) were set after the author had seen Step-0 medians for 100 journals.
- Fix:
  - Retitle as "pre-specified (time-stamped in project repository)".
  - Deposit the frozen protocol externally (OSF or Zenodo).
  - Correct the deviation count to D1-D7 and log the H7 and E7 changes.
  - Report H7 as pre-specified (36 mo, not run) plus a 24-month exploratory contrast.

**M2. The attribution of under-coverage to "drift" is untested and partly contradicted by the project's own diagnostic.**
- Evidence:
  - The Discussion says "Drift appears to be the main reason". RQ3 asks whether drift explains miscalibration, but no analysis answers it.
  - The repo's E10 diagnostic (`results/oracle_diagnostic_E10_EXPLORATORY.json`) gives a visible-set shortfall of -3.03 points. An oracle F0 trained on the complete received-cohort of the prior 12 months has -1.51 [-1.88, -1.15].
  - I replicated this independently (-1.5 for the complete cohort, same visible value). So about half of the shortfall is lag/truncation of the visible set, not cohort drift.
  - About 0.5 point is expected from finite-sample bias: Hazen [q10, q90] coverage is about 80/(n+1) at n = 100-400. This is unmentioned and sits close to the 3-point H2 threshold.
  - The median is nearly unbiased. The mean log gap (realised minus forecast median) is +0.007, the median gap +0.020, and the mean year-to-year delta +0.015. "Biased towards optimism" overstates a tail effect.
  - The top-decile PIT excess differs by origin: 12.2% at O1 and 14.0% at O2 (`pit_counts.csv`).
  - Mean ln D rises from 4.70 to 4.78 over 2021-2025 (+8%). With two origins, both in 2023-24, the "optimism" cannot be separated from one period's trend.
  - The docx (02:59) predates D7 (03:02), so it does not reflect E10.
- Fix: report E10 and decompose the shortfall into finite-sample, information lag/truncation and cohort drift. Replace "main reason" with a quantified statement. Add origins (2022 and 2025 six-month cohorts are observable), or restrict the claim to this period.

**M3. H5 / RQ5 depend on a covariate not available before submission, and the abstract does not say so.**
- Evidence:
  - H5 is defined for "pre-submission covariates", yet reference count (flagged in the protocol as a final-version property) is in the confirmatory model.
  - Single-feature gains over the control (`article_level_ablation_EXPLORATORY.csv`): authors 0.85%, month 0.01%, weekday 0.01%, refs 1.31%.
  - The pre-submission set (authors + month + weekday) was never fit as a set. The single-feature gains suggest it is below 2%, which would make H5 **supported**, the opposite of the reported outcome.
  - The abstract says "Author count and reference count improved forecasts by about 3%" with no caveat.
  - Aggregation differs from the protocol. The reported 3.36% [2.56, 4.13] is a journal-averaged ratio. The article-pooled estimate is 2.75% vs F4 and 2.66% vs control (`article_level_summary.json`, "pooled"), with no CI. The protocol says "pooled".
  - The ablation used only tau in {0.25, 0.5, 0.75}, so its "all" gain is 2.2%, against a 3.2% headline. This is undisclosed in the text.
  - The no-C5 sensitivity raises the E7 gain from 3.4% to 5.4% (`sensitivity_summary.csv`). The reference count is acting as an article-type proxy.
  - E7 is not out-of-time. LightGBM is trained on same-period target papers of other journals (grouped CV), and "received month" only spans Jan-Jun by construction.
  - The 60/30 sensitivity row repeats the primary E7 value (0.0336), so E7 was not re-run there.
- Fix: fit and report the strictly pre-submission model, state H5 separately for the two feature sets, give the pooled-article CI, and put the E7 caveats in the abstract.

**M4. The shrinkage/parametric conclusion (H3, abstract) is not diagnostic of shrinkage.**
- Evidence:
  - F4 shrinks a **lognormal**, and the manuscript reports left-skewed ln D (median skew -0.79, 61% of journals below -0.5). The test confounds misspecification with shrinkage.
  - Eligibility (n_train >= 100) removes the small-n regime where shrinkage matters. Only 29 journals have n < 150.
  - The text says "F4 was worse than F0 in every size stratum", but the <150 stratum has Holm p = 0.053, so it is inconclusive.
  - The abstract's "Parametric and shrinkage forecasters did not improve" is broader than the evidence.
- Fix: add shrinkage of empirical quantiles (an F0/F2 blend) and a skewed family (skew-normal or log-logistic). Reword to "a lognormal and its empirical-Bayes version". Report the <150 stratum as not significant.

**M5. "Results replicated" (abstract) is overstated and the validation evidence is thin.**
- Evidence:
  - E9 is 58 journal-origins from 32 journals, drawn from the non-random, computing/biomedical-oriented Step-0 list. It includes *Nature Communications* (Springer Nature, a frame publisher), although the text says "publishers outside the frame".
  - External F0 coverage is 79.2%, so the shortfall does **not** replicate. No CIs or tests are given.
  - E8 covers 14 journals, mostly BMC / Springer Nature (`e8_crossref_vs_pubmed.json`), none from Wiley or T&F. Both channels carry the same publisher feeds.
  - D4 (check against publisher pages) failed, so no independent verification of dates exists.
- Fix: say "directionally consistent for F0 vs F2 skill; calibration not replicated", add CIs, describe the journal-selection mechanism, and drop "replicated" from the abstract.

**M6. Not submission-ready.**
- Authors, funding, conflicts, ethics, originality and the data DOI are placeholders. The repository is private.
- The "byte for byte" re-run claim rests on a README sentence with no hash log.
- Fix: complete the declarations, deposit data and code publicly, and add the hash comparison.

### MODERATE

**MD1. Weak benchmark and effectively two time points.**
- The headline 15.7% skill is against F2, which ignores journal identity. With ICC = 26.5% a gain of this size is close to mechanical.
- There is no persistence baseline (last-year median) and no subject-level pool.
- The journal-cluster bootstrap and Wilcoxon tests ignore common shocks (two shared origins, shared publisher systems). The CIs hold for these two periods only.

**MD2. The 72-day threshold has no stated rationale.**
- It appears to come from the project's journal-timeline constraint (`journal_verification.md`), not a cited policy. The manuscript says only that "policies sometimes require a stated maximum time", with no reference.
- RQ4, the abstract and the discussion are built around it.
- The abstract says "Only 12.0%", while the pre-specified H4 was < 5%, so the wording conflicts with the test outcome.
- Fix: justify 72 days or report several T (Table 3 already has 120 and 180).

**MD3. The "fast end overstated" result is a small-n selection effect.**
- It rests on 23 origins from 19 journals, with no CI.
- Selecting on a high noisy estimate (phat >= 0.8) gives a winner's-curse shortfall even for stable journals. This is not quantified.
- Fix: add a permutation or simulation null for regression to the mean, plus a CI.

**MD4. The field claim is contradicted by the repo's own table, and CIs ignore clustering.**
- The manuscript says fast journals are "concentrated in chemistry, materials, clinical medicine and engineering".
- `post_hoc_D6_field_table.csv` shows engineering/computing has 5 of 68 fast journals (7.4%), the **lowest** share. Chemistry/materials/physics is 28.3% and clinical is 22.6%. The coding is by title keyword and unvalidated.
- Table 3 and the H4 CI use Clopper-Pearson over 1,531 origins, treating a journal's two origins as independent. The D6 cluster CI is [9.9%, 14.2%] and is not what is reported.
- Fix: remove "engineering" or recode. Use cluster intervals throughout.

**MD5. Frame selection and eligibility are outcome-linked.**
- The frame is built from 2023 data: top-1000 by 2023 article count, a 2023 date-deposit screen and a 2023 volume screen. O1 (2023-01-01) is therefore evaluated on a frame defined with post-origin information.
- Eligibility needs >= 50 accepted target papers, which is itself an outcome. Survivorship in journal existence and date deposit is unaddressed.
- Fix: rebuild the frame from pre-origin volumes, or list this under limitations.

**MD6. Publisher-defined "received" dates and accepted-only data affect the fastest journals most.**
- 4.7% of D are <= 30 d and 1.5% are <= 10 d. Only title and reference filters remove non-research items.
- Left skew is attributed to "a minority of very quick acceptances" without checking whether they are resubmission dates or fast-track items.
- A sensitivity excluding median < 30 d journals exists (6 journals, share 11.3%) but is not in the manuscript.
- Fix: include it, and add a within-journal analysis restricted to D > 30 d.

**MD7. Novelty is stated as fact but the prior-art search is thin.**
- The Introduction says "such statistics have not been tested out of time". `search_log.jsonl` has 3 lines, and the novelty map says most full texts were unread. The map itself hedges ("not found in searched literature") and records "risk of incrementality" as OPEN.
- The core idea is a straightforward application, and the findings (ICC about 26%, drift, wide intervals) mostly confirm known results.
- Fix: soften to "to our knowledge", broaden the search (editorial-delay prediction, survival analysis of review times), and frame the contribution as a calibration benchmark.

### MINOR
- Weekly heaping in D (D mod 7 = 0 is 15.3% against 14.3% expected) is unreported. Ties on integer days slightly inflate coverage.
- For Wiley, 22.5% of V values are imputed to day 15 from month-level `issued`. This is conservative, but not disclosed.

## 4. Journal-selection files
- `selected_journal.md` says the chosen journal has "the shortest observed median (105 d)" among alternatives. That rests on four or five comparators, while QSS, J. Informetrics and Research Evaluation were unmeasurable.
- The 27.4% (n = 164) is a survivor sample of accepted papers, the weakness the manuscript criticises. Sampling windows are inconsistent: `journal_verification.md` §3 says publication from 2025-07-01, `selected_journal.md` says from 2024-01, and the CSV has accepted dates from 2023-12-11 and received dates from 2023-07-04.
- `journal_comparison.md` still says "0/100 pass" and "JKSU-CIS is chosen". It was not updated for the revised selection or the addendum (61 of 773 journals with median <= 72 d). A reader of that file alone is misled.
- The verification §1 headline ("none of 100") applies only to a hand-assembled, computing-biased list. The addendum corrects it, but §1 should be edited in place.
- Positive: the non-compliance banner is honest, JCR quartile is marked unverified, and I found no fabricated figures.

## 5. What is solid
- Variance components and ICC (checked two ways).
- The out-of-time design and visibility rule.
- Honest reporting that H2-H5 were not supported.
- F0 under-coverage is consistent across both origins (76.7% / 77.4%).

## 6. Overall recommendation
**Major revision.** The core results are reproducible and the design is sound. The paper needs a re-framing of "pre-registered", a quantified account of why intervals under-cover, a strict pre-submission H5 analysis, and softened claims on shrinkage and replication. The contribution is incremental and should be positioned as a calibration benchmark. With those changes it could be acceptable in a mid-tier meta-research journal.

## 7. Three most important fixes
1. **Decompose and qualify the under-coverage (M2).** Report E10 and finite-sample effects, add origins beyond 2023 and 2024, and replace "drift is the main reason" and "optimistic bias" with quantified statements.
2. **Repair the confirmatory record (M1, M3).** Retitle "pre-registered", log all deviations (H7 36 → 24 months, E7 specification, D5-D7), and re-report H5 on a strictly pre-submission covariate set with pooled and journal-averaged CIs.
3. **Rebuild the shrinkage and replication claims (M4, M5).** Test shrinkage on empirical quantiles and with a skewed family, remove "replicated" from the abstract, and add stronger baselines (persistence, subject-level pool) so the 15.7% figure has a meaningful reference.
