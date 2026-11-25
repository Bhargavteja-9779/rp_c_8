# Reproducibility audit R4 (cycle 3, Part D) - independent cold-start check

Scope: Part D (cycle 3) of the repository at the working tree copied at 4341fab plus the staged files of 568c108 (results and manuscript files are identical in both). Scratch copy: `/tmp/audit3` (made with `cp -r`; the hard-coded `/home/user/rp_c_8` in `reinforced/code/src/d_*.py` and `product/tests/test_core.py` was rewritten with `sed` to `/tmp/audit3`). Pristine copies of the committed results are in `/tmp/audit3_orig`. My own code is in `/tmp/audit3_own/` (`indep.py`, `leak.py`, `poison.py`). The only file written inside `/home/user/rp_c_8` is this report. Python 3.13.16, 4 cores.

## Verdict
The central Part D computation reproduces exactly, and the manuscript numbers I checked agree with the result files. There is no FATAL issue. One MAJOR issue: the committed external-validation outputs cannot be regenerated from the committed raw data, because a 128th journal file was written seconds after the script started. Order-of-events claims are largely supported by git and file mtimes, with the qualifications listed in section 5.

## 1. Commands run and results

| # | Command (in `/tmp/audit3`) | Wall time | Result |
|---|---|---|---|
| 1 | `D_CAP=480 python3 -I reinforced/code/src/d_experiments.py` | 3 m 40 s | `D_summary.json`, `D_params_by_origin.json`, `D_panel_rows.csv` are BYTE-IDENTICAL to the committed files (`cmp`). SHA-256: summary a920a1c1..., params 3e5bb06b..., rows 4153fe69... |
| 1b | `D_CAP=365 python3 -I .../d_experiments.py` (extra) | about 5 min | `D_summary_cap365.json`, `D_params_by_origin_cap365.json`, `D_panel_rows_cap365.csv` are BYTE-IDENTICAL. The current code therefore also regenerates the "as first run" results, and the cap-480 files were not touched. |
| 2a | `python3 -I .../d_defaults.py` | 1 m 29 s | `D_defaults_and_floor.json` and `product/turnaround_forecast/defaults.json` BYTE-IDENTICAL. |
| 2b | `python3 -I .../d_external.py` | 45 s | NOT identical: `D_external_summary.json` and `D_external_rows.csv` differ (issue M1). After moving `data/raw/pubmed_ext/PLoS_Genet.csv` out of the scratch copy and re-running, both files are BYTE-IDENTICAL to the committed ones. The file was moved back afterwards. |
| 3 | `python3 -m pytest -q -p no:cacheprovider product/tests` | 24 s | 8 passed. |
| 4 | `python3 -I /tmp/audit3_own/indep.py /home/user/rp_c_8` | seconds | See section 2. |

I did not run `d_figures.py`, `d_sensitivity_cap.py`, `collect_pubmed_external.py` (live NCBI API) or `build_methods_manuscript.py`. I did not check the PNG figures or the PDF/DOCX build. I did not re-run `consistency_check_methods.py`, which was added in the later commit 568c108.

## 2. Independent recomputation (no `d_lib` import)
The code reads `articles_clean.csv.gz` and `frame_eligible.json`. It applies the visibility rule (V, accepted and received before t0, V within 365 days), the target rule (received in [t0, t0+91)) and eligibility (at least 100 visible and 30 target papers). It caps D at 480, uses `np.quantile(method="hazen")`, and solves G(q) = mean Phi((q - y_i)/h) with `scipy.optimize.brentq`.

- **F0 signed coverage error, origin 2024-01-01, cap 480, journal mean.** My value is -0.019017 (-1.90 points), the committed value is -0.019017, and the journal sets are identical (754 journals). The maximum per-journal difference in coverage is 1.1e-16. This is also the 2024-01-01 by-origin entry (-0.019) in `D_summary.json`.
- **CV0 quantiles for 5 journal-origins** (one random eligible journal at each of 2023-10-01, 2024-01-01, 2024-04-01, 2024-07-01 and 2025-01-01, with h^2 = tau2_pub (from `D_params_by_origin.json` for that origin) + s^2/n). The journals are 1532-4087 (T&F), 1548-2634 (Wiley), 1863-2491, 2366-0058 and 1006-706X (Springer Nature). I compared my quantiles' derived cov80, below, above, width and pinball with the committed panel rows. The maximum absolute difference over all 25 comparisons is 4.7e-15 (width up to 4.7e-15, others smaller). The h values are 0.178 to 0.219 and my q10/q90 give widths of 1.2 to 1.9 ln-days. The panel CSV does not store the quantiles themselves, so the comparison is through those derived quantities.
- **Noise floor.** From my own target sizes for all 4,486 journal-origins I get 0.036175, and from the committed `n_te` column also 0.036175. This equals `D_defaults_and_floor.json` (0.0361751) and rounds to the manuscript's 3.6 points. The manuscript's quoted "0.0362" in the task is the same number rounded.
- **tau2_g, bonus.** I recomputed the global tau2 for all six evaluation origins from my own delta and sampling variances. All agree with `D_params_by_origin.json` to five decimals (for example 0.03815 at 2023-10-01 and 0.04289 at 2025-01-01).

## 3. Does `complete()` prevent use of outcomes not complete at t0 in `learn()`?
Code reading of `d_lib.py` and `d_experiments.py`:
- `complete(o, t0)` is `o + (91 + CAP) days <= t0`. `d_experiments.py` builds `use = [o for o in origins if complete(o, t0)]` and passes only `use` to `learn()`. Inside `learn()` every parameter (tau2_pub, b_pub, tau2_g, b_g, c, G for the PIT map, alpha_aci for ACI) is computed from `store[o]` for `o in origins_complete` only. The ACI loop iterates `origins_complete` in time order. Nothing in `learn()` touches `store[t0]` or any other origin.
- `forecast_rows()` uses the evaluation origin's own visible sample (`ytr`, `y24`) and the parameters, and uses `yte` only for scoring.
- Empirical test (`poison.py`, in scratch with the real `learn()`): at t0 = 2024-01-01 the complete origins are 2022-01-01 and 2022-04-01 (2022-04-01 + 571 d = 2023-10-24 <= t0; 2022-07-01 + 571 d = 2024-01-23 > t0). I replaced both the visible and target samples of every non-complete origin by random garbage. The learned parameters (tau2, b, c, G, alpha) were identical. As a control, poisoning one complete origin changed tau2_g from 0.0374 to 7.42. So `learn()` uses nothing outside `use`.
- Subtlety (MODERATE, issue M2): "complete" here means that the capped duration is determined, which needs the target paper to be received by o+91 and a wait of CAP days. It does not mean the paper was observable (accepted and published) at t0. The target sets in `build_store` are defined from the final dataset, so they include papers that, at t0, were not yet accepted (true D > cap, recorded as the cap) or were accepted but not yet online. With my own code, the share of target papers in the learning cohorts that were not both accepted and online before t0 is 1.2 to 1.3% at every evaluation origin (98.7 to 99.4% were). Re-estimating tau2_g with only target papers that were visible at t0 changes it from 0.03815 to 0.03635 (2023-10), 0.03737 to 0.03679 (2024-01), 0.03862 to 0.03824, 0.03860 to 0.03846, 0.04014 to 0.04013 and 0.04289 to 0.04295 (2025-01). That is at most 5% of tau2 at the first origin and below 1% later. The mean shift b_g changes by 0.006 to 0.013, which affects only the secondary CVb. The headline CV0 results are insensitive, but the rule's description ("outcomes that would not yet have been known") is slightly stronger than what is implemented.
- The sample of eligible journals (frame_eligible.json) and the data cleaning were fixed with data through 2026-10-20 (hindsight). This applies to all methods equally; I note it as a limitation, not a leak in `learn()`.

## 4. Spot-check of 10 manuscript numbers (`pandoc -t plain Methods_Manuscript.docx` against result files)
All PASS unless noted.
1. Table 1 sample: 6 origins, 774 journals, 4,486 journal-origins, 482,065 papers, from `D_summary.json`. PASS.
2. F0 signed -1.9 [-2.3, -1.5] (file: -1.91 [-2.34, -1.47]); CV0 +0.5 [+0.1, +0.9] (file: +0.54 [0.149, 0.941]); mean absolute error F0 7.18 [6.88, 7.49], CV0 6.75 [6.51, 7.02], CVb 6.71, V 7.05, R 7.03, ACI 7.11, F6 6.96. PASS.
3. HD1: -0.42 [-0.54, -0.30]; imprint t(6) [-0.70, -0.02]; block CI [-0.57, -0.28]; 6 of 7 imprints; 3 of 3 publishers. PASS.
4. HD2: -0.14% (CI -0.15% to -0.09%), -0.0003 ln-days; interval score -0.007 [-0.009, -0.004]. PASS.
5. Table 2 contrasts and Holm p (2.9e-11, 2.8e-07, 8.0e-11) and imprint intervals. PASS.
6. HD5: r = 0.15 (CI 0.03 to 0.26), Spearman 0.20, slope 0.46 (0.09 to 0.94), mean predicted -3.2 and observed -1.9 points. PASS.
7. Table 3 Brier and slopes for F0, CV0 and CVb at 72, 120 and 180 days. PASS (all 18 values).
8. "12% of F0's excess error removed": (0.03558 - 0.03135)/0.03558 = 11.9%. PASS. Fitted tau2 0.041 / 0.038 / 0.041 matches `D_defaults_and_floor.json` (learned from all complete cohorts, 13 origins), and alpha stayed at 0.193 (0.19269 at the last origin). PASS. Note: at the last evaluation origin (6 complete cohorts) the values are 0.047 / 0.033 / 0.048, so the phrase "all complete cohorts" refers to the shipped defaults, not to the evaluation (see m3).
9. Table 4 and text for external journals: 117 journals, 652 journal-origins, 74,787 papers, F0 -2.0 [-3.3, -0.8], V +1.0 [-0.3, +2.1], CV0 +1.1 [-0.1, +2.2], CVb +1.3 [+0.2, +2.4]; HD6 -0.50 [-0.91, -0.11], vs V -0.25 [-0.51, 0.03], pinball -0.00025; Brier 72-day 0.01105 to 0.01088 and slope 0.87 to 0.90. PASS against the committed files. These do not reproduce from the committed raw data (M1).
10. Cap sensitivity (exploratory): +2.2 / -0.9 / -2.0 / -2.4 points for caps 270 / 365 / 480 / 1460 at H = 91 (file: +2.15 / -0.87 / -1.99 / -2.42); 182-day cohorts differ by at most 0.2 points; bias of cap 480 against no cap +0.4. PASS, with the qualification in m1. Table 5 values for the cap-365 run (HD1 -0.37 [-0.47, -0.26]; HD2 -0.11%; HD3 +1.2 [+0.8, +1.6]; HD5 r = -0.12) also PASS against `D_summary_cap365.json`.

## 5. Order of events (git history and file mtimes)
Timeline (all 2026-11-02, UTC; commit times from `git log`, file mtimes from the original working tree):
- 4f1a17d 08:31:09 protocol Part D plus `collect_pubmed_external.py` with the 137-journal list. The collector has no later commit, so the list is unchanged.
- 322af8f 08:33:01 `d_lib.py` and `d_experiments.py`.
- 3f50988 08:34:59 amendment D-A1 (origin list, deviation C2-17); 114933f 08:37:05 F6 array fix (C2-18).
- `D_panel_rows_cap365.csv` mtime 08:41:18; dbd963b 08:43:51 (first results and `d_sensitivity_cap.py`, mtime 08:42:43); exploratory output mtime 08:46:58.
- b4ff392 08:47:33 amendment D-A2 plus the protocol text; `d_lib.py` and `d_experiments.py` mtimes identical to the commit time.
- Cap-480 files `D_panel_rows.csv` 08:50:54, `D_summary.json` 08:51:00, `D_defaults_and_floor.json` 08:53:03; committed in 4459a9b at 16:10:14.
- `d_external.py` fix eeba96e 16:20:22 (file mtime 16:20:10); external results mtime 16:20:56; commit 4341fab 16:24:26.

Supported:
- The Part D protocol (hypotheses, forecasters, metrics, external list) was committed before the Part D code (about 2 minutes) and before any result file existed (about 10 minutes); the code was committed before the first run's results. `git diff` shows the original protocol sections D0-D7 were not edited afterwards; the amendments D-A1 and D-A2 were appended.
- D-A1 (arithmetic): 2022-01-01 + 91 + 365 days = 2023-04-02, so no earlier origin is complete at 2023-04-01. Correct. It was committed before any result existed.
- D-A2: the cap-480 result files carry mtimes 3 to 6 minutes after the D-A2 commit, and none exist in any earlier commit, so "committed before any cap-480 result" holds for the primary analysis. D-A2 states, and the manuscript discloses, that the first full run (cap 365) was seen first, that HD5 failed, and that the cap choice is post hoc. In the cap-365 run HD1, HD2 and HD4 were supported and HD3 held for the point estimate, so the rerun did not rescue the headline hypotheses; only HD5 changed from fail to weak pass.
- The cap-365 outputs are labelled and reproducible (1b above).

Not supported or only partly supported:
- M1 (below): the external-analysis run order contradicts the protocol line "run once after collect_pubmed_external.py has finished".
- Crashes and "no output" claims (the arithmetic slip, the F6 bug, the `d_external` origin bug) cannot be verified from git; there are no logs, only the corrective commits. The manuscript says "two programming errors and one arithmetic slip stopped runs before any output". Git shows one code error before the first result (F6, 114933f) and the arithmetic slip; deviation C2-18 lists "missing complete origin" as one of its two errors, which is the same event as D-A1/C2-17 (double counted). The second programming error is the `d_external` origin list (C2-20, 16:20:22), which happened after the frame results. See m2.
- "Choice of 480 days was made from the cap sensitivity of F0 alone": the decision to rerun followed CV0's over-coverage and the HD5 failure at cap 365 (stated in D-A2 itself), and 480 was the cycle-2 cap, so prior knowledge existed. Honest but the word "alone" is stronger than the record. The exploratory analysis was run at caps 270/365/480/1460 only, and `d_sensitivity_cap.py` (committed 08:43:51) predates its output, which is good.
- The statement "committed before any cap-480 result" is loosely worded: `D_sensitivity_cap_EXPLORATORY.json` (committed in the same commit as D-A2) already contains an F0 cap-480 estimate (-2.0 points). The statement holds only for the Part D panel analysis.
- Git commit times are the sandbox clock and are not independently attested; mtimes and git timestamps are mutually consistent.

## 6. Issues

### MAJOR
- **M1 - external results are not regenerable from the committed data.** `d_external.py` globs `data/raw/pubmed_ext/*.csv` at start. It ran at about 16:20:11-16:20:56, while the collector was still writing: `PLoS_Genet.csv` has mtime 16:20:41 and is added in the same commit as the results (4341fab). The committed `D_external_summary.json` reports 127 journals attempted, 121 kept, 117 evaluated, 652 journal-origins and 74,787 papers (manuscript Methods and Table 4 use these). Re-running on the committed data gives 128 / 122 / 118 / 658 / 75,279. Deleting `PLoS_Genet.csv` reproduces the committed files byte for byte (verified). The effect on results is small (F0 signed -1.97 in both, CV0-vs-F0 absolute error -0.502 to -0.501 points, CI [-0.906, -0.111] to [-0.899, -0.119]) but counts and the last decimals in the manuscript differ. The protocol (D5 and the script docstring) says "run once after collection finished"; commit c4b018b is titled "External collection complete" yet two more journal files were written later. Fix: re-run `d_external.py` on the final data, update Methods, Table 4 and the text (117 to 118 journals, 652 to 658 journal-origins, 74,787 to 75,279 papers), or remove `PLoS_Genet.csv` and document why. Also log it as a deviation. The 137-journal list yielded 128 files with records (9 empty files) and 122 with at least 600 records; the manuscript says 127 and 121 and does not mention the 9 empty journals.

### MODERATE
- **M2 - "complete" is not "observable".** See section 3. About 1.2 to 1.3% of the target papers in learning cohorts were not yet accepted or online at t0 (capped durations); effect on tau2 up to 5% at the first evaluation origin, below 1% later. Add one sentence to the Methods and, ideally, a sensitivity row. Also the description "prevents information about outcomes that would not yet have been known from reaching any forecast" is slightly stronger than the code.
- **M3 - D7 deliverable test deviates from the protocol.** D7 requires the package to reproduce the pipeline's CV0 quantiles for at least 20 journal-origins to 1e-6. `test_matches_study_pipeline_on_20_journal_origins` asserts a log-scale tolerance of 6e-3 against `d_lib.smoothed_quantiles` with a constant tau2 = 0.04 (not the pipeline's learned per-publisher values). I measured a maximum log error of 1.7e-3 over 118 journal-origins; it comes only from output rounding to 0.01 day (`np.exp(q).round(2)`). The unrounded function `smoothed_quantiles` matches `d_lib` exactly (difference 0 over 50 samples). So the numerics are right, but the stated 1e-6 criterion was not met as specified and the change is not logged. The test is also skipped silently if the data file is missing, and has hard-coded absolute paths.

### MINOR
- m1. `d_sensitivity_cap.py` docstring and the manuscript say all targets are complete for every setting. For cap 1460 ("no cap") this is false: with data ending 2026-10-20, papers received around 2024-07 can only be observed up to about 750 days (2023-07 up to about 1,100 days). Share of D above 750 days is 0.44% for the 2023-07 cohort and 0.04% for 2024-07. The "no cap" estimate (-2.4) and the "+0.4" bias of cap 480 are therefore somewhat optimistic about the tail; the effect is at most a few tenths of a point.
- m2. The count of "two programming errors and one arithmetic slip" is not verifiable and is partly double counted (section 5).
- m3. "Fitted tau2 ... when learned from all complete cohorts" refers to the 13-origin shipped defaults (0.041/0.038/0.041); the tau2 in force at the last evaluation origin is 0.047/0.033/0.048. Say which.
- m4. The machine paths are hard-coded in every `d_*.py` and in the test (`/home/user/rp_c_8`); `sed` was needed, as in cycle 2. `python3 -I` is used, which does not matter because the scripts insert paths themselves. `D_CAP` defaults to 480, so running without the variable reproduces the primary analysis, and `D_CAP=365` the first run.
- m5. HEAD advanced to 568c108 (README, `run_cycle3.sh`, `consistency_check_methods.py`, a consistency audit) while I worked; these do not change any Part D result file, and I audited the earlier snapshot.

## 7. What I could not run or verify
- `collect_pubmed_external.py` (live NCBI), so the raw PubMed files and the exclusion by outcome (journal list fixed "from memory, not by turnaround times") are taken as committed.
- `d_figures.py` and the figure content, `build_methods_manuscript.py`, and the PDF. I checked the DOCX text only.
- Earlier-cycle numbers quoted in the Part D manuscript (1,531 journal-origins, 26.5% variance share, Research Square probe, 12.0% of journals accepting half of papers within 72 days). I did not recompute them.
- The `data/processed` file was not regenerated from raw data (`prepare_data.py`); I used the committed gzip.
- Whether the sandbox clock behind git and mtimes is reliable; timing arguments are only as good as that clock.
