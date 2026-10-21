# Independent reproducibility audit (Agent B)

Scope: snapshot of HEAD 568e8b0 plus uncommitted edits at about 03:00 UTC on 2026-10-21. Other agents were editing the repo concurrently; later commits (e.g. c759300) were not audited. All execution took place in a scratch tree, /tmp/audit_root. Nothing was written to the repo except this report. Python 3.13.16, with numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, lightgbm 4.7.0, statsmodels 0.15.0, 4 cores.

## 1. Steps actually executed

| # | Command | Result |
|---|---|---|
| 1 | `python -m pytest -q tests` | 10 passed in 10.9 s. |
| 2 | `python run_all.py --mode quick` | Completed in 14 s and wrote 25 files plus figures. Synthetic generator truth is ICC about 0.37 (sd 0.5/0.25/0.6). The recovered ICC is 0.41 with 95% CI [0.30, 0.49], which covers the truth. Skill, coverage and Brier outputs are plausible. F0 coverage is -6 points. Output is not evidence, as the README says. |
| 3 | `python run_all.py --mode full` | Completed in 422 s (the repo log says 428 s). It ran effectively single-core, not on 4 cores. |
| 3b | `--variant noC5` (573 s) and `--variant min60_30` (567 s), run concurrently | Completed. |
| 3c | `src/run_external.py`, `src/run_ablation.py`, `src/summarize_sensitivity.py`, `src/make_tables.py`, `src/prepare_data.py`, `src/build_manuscript.py` | All completed. Details in section 2. |
| 4 | Independent recomputation (own script, `np.quantile(method="hazen")`) | See section 3. |

## 2. Byte-identity (item 3)

- **Primary full run.** run_all writes 34 files: 33 CSV/JSON/PNG outputs plus `run_info.json`. Compared with the repo's `results/`, 33 are SHA-256 identical, including all 9 PNGs. Only `run_info.json` differs, in `elapsed_s` (428.5 against 422.4). The manuscript claims every table and JSON reproduced "byte for byte". That holds for the scientific outputs but is literally false for `run_info.json`, which holds wall-clock time.
- **Other result files.** `external/*` (6 files), `sensitivity_summary.csv` and `article_level_ablation_EXPLORATORY.csv` are identical after re-running their scripts.
- **make_tables.** `results/metrics.json` and `tables/*` are identical (cmp).
- **Variant runs.** `results_full_noC5` and `results_full_min60_30` are identical except for `run_info.json` and a few PNGs (noC5: fig_variance_components, fig_coverage, fig_skill, fig_pit; min60_30: fig_coverage, fig_skill, fig_pit). All CSV/JSON are identical. I did not diagnose the PNG differences. The repo's variant PNGs may predate a later plotting edit; that is unverified.
- **prepare_data.py re-run on `data/raw/crossref/`.** The decompressed content is byte-identical for `articles_clean` and `articles_clean_noC5`, and cleaning counts match (1,737,272). However, the **gzip files' SHA-256 differ** (4d8a31... against dcfc23... in `data_manifest.json`), probably because of the gzip header timestamp or filename. The manifest hashes therefore cannot be re-verified after a rebuild, only by comparing to the shipped files. I did not confirm the gzip-header cause.
- **build_manuscript.py (snapshot-time copy).** Regenerated from my results copy, it gave docx text identical (pandoc plain diff empty) to the committed `Final_Manuscript.docx`. The live `build_manuscript.py` was edited at 03:04, after the docx (02:59), and contains additional abstract text, so the committed docx is stale relative to the live script at audit time.

Verdict: the "byte-identical re-run" claim holds for all scientific CSV/JSON outputs (my run against the repo's results; the README's earlier two-run claim was not independently observed) with the exceptions above.

## 3. Independent recomputation (item 4)

From `data/processed/articles_clean.csv.gz` (read directly with pandas):

- **Counts.** 1,737,272 records, 800 journals, 0 duplicate DOIs, and D = accepted - received for every row. All match `data_audit.json` and the abstract.
- **Median D.** 124 days; share D <= 72 is 0.22794. Both match.
- **F0, single journal-origin.** Journal 1475-2840, origin 2023-01-01: n_train 289, n_test 181, mean pinball over 19 tau 0.1716355634828848, against 0.1716355634828848 in `metrics_journal_origin.csv`. Forecast median 55.0 d, matching. Three more journal-origins (1749-8090, 1806-3691, 1097-007X) agree to within 3e-17.
- **F0, all rows.** For all 1,531 F0 journal-origin rows, n_train and n_test match exactly and the maximum pinball difference is 2.2e-16.
- **Protocol §5 rule.** The 12-month window ([t0-365, t0) on V) is implemented correctly. The code additionally requires accepted < t0 and received < t0 (logged as D2). That gave no difference from the naive window in the cases I checked.

F2 to F6, the bootstrap and the E7 LightGBM results were checked only through byte-identical re-execution, not independently re-derived.

## 4. Abstract claims traced (item 5)

Source: `pandoc -t plain manuscript/Final_Manuscript.docx` (the committed v1).

| Claim | Source |
|---|---|
| 1,737,272 records; 800 journals | metrics.json n_records, n_journals |
| 298,469 papers; 781 journals | n_target_papers, n_journals_forecast |
| ICC 26.5% [24.7, 28.3] | vc.estimate.icc_journal, ci95 |
| 69.1% between articles within journal-year | derived: sigma2_resid / (sum of 3 components) = 0.5027 / 0.7276 |
| 15.7% pinball reduction | forecasters.F0.skill = 0.157 |
| 77.0% coverage | derived: 0.8 + F0.cov80_minus (-0.0303) |
| "five-fold range" | F0.width80 = 1.604 on log scale, exp(1.604) = 4.97 (derived, loosely worded) |
| 12.0%; 1.6% | guarantee T=72, thresholds 0.5 and 0.8 |
| 75% realised | high_bin_72.realised = 0.750 (n = 23 only; n not stated) |
| "about 3%" | e7.bootstrap.rel_gain_vs_ctrl = 0.032 |
| 58 journal-origins | e9.F0.n_journal_origins |

No number in the abstract is untraceable. Caveats:
- "About 3%" is the journal-cluster-bootstrap estimate against a learner-only control. The pooled point estimate is 2.66% vs control and 2.75% vs F4. The ablation run gives 2.2%. Which figure is meant is ambiguous.

## 5. Issues

### FATAL
None for re-running the analysis from the processed data present in the working tree.

### MAJOR
1. **Raw and processed data are gitignored; a fresh clone cannot reproduce the pipeline.** `.gitignore` excludes `data/raw/crossref/`, `data/raw/pubmed/` and `data/processed/`; `git ls-files data` returns only 4 small files. `run_pipeline.sh` step 3 (`prepare_data.py`) and `run_all.py --mode full` fail without these. I could run them only because the working tree holds about 318 MB of data. The code README discloses the dependency. The top-level README does not say the data are absent from the repo, and there is no DOI/Zenodo archive. The live Crossref API changes over time (disclosed), so regeneration will not match. The manifest's SHA-256 values are for gzip files that do not even rebuild bit-for-bit (section 2). Fix: archive the raw and processed data (or at least the processed files) with a DOI, record hashes of the decompressed content, and say so in the top-level README.
2. **Orphan results file.** `results/shape_diagnostics_EXPLORATORY.json` is read by `make_tables.py` and feeds `metrics.json["shape"]` and the Discussion (skewness, kurtosis). No script in the repo produces it (grep across the repo). The pipeline cannot regenerate `metrics.json` from scratch without it. Fix: add the generating script and call it in `run_pipeline.sh`.

### MODERATE
3. **Bootstrap size differs from protocol and manuscript, and is undisclosed.** Protocol §7 and the manuscript's methods section state B = 5000 for the cluster bootstrap. `experiments.variance_components` uses `min(B, 1000)`, and `article_level_ci` uses `min(B, 2000)`. The ICC CI (abstract) and the H5 CI (E7 gain) therefore rest on 1000 and 2000 resamples. I found no deviation entry for this in D1 to D7 (the log as it stood at audit time). Fix: log it or use 5000.
4. **Drift null differs from protocol.** Protocol §8 specifies "bootstrap null from within-year resampling". The code (`drift_analysis`) uses 200 permutations of the pooled two-year values. The manuscript says "permutation null", so it is partly disclosed, but the protocol text was never amended (and the permutation null is not what was registered).
5. **Frame duplicates.** The frame has 802 journals but the cleaned data has 800. The two missing ISSNs, 1590-3478 and 1434-6079, are duplicate keys of 1590-1874 and 1434-6060 (identical DOIs: 4,308 and 1,211 records). C6 ("duplicate DOIs") then removed exactly these 5,519 records, not genuine within-journal duplicates. ISSN merging therefore failed for 2 journals. Deviation D3 says the collection "covers all 802 frame journals", and manuscript §2.2 says "All 802 resulting journals were [collected]" while also saying "merged print and online ISSNs". The effect is small but the cleaning-log C6 count is misleading as a duplicate-quality statistic. Fix: dedupe the frame and report 800.
6. **Manuscript amendment count is stale.** The manuscript (v1 docx) says "Five post-freeze amendments". The deviations log at audit time had D1 to D7, with D6 and D7 explicitly post-hoc, after results. Neither is mentioned in the v1 text I read. Also, `run_pipeline.sh` does not include `post_hoc_analyses.py` or `oracle_diagnostic.py`, whose outputs are in `results/` (post_hoc_D6_*, oracle_diagnostic_E10_*). The pipeline therefore does not reproduce all tracked results. Later commits may have addressed parts of this.
7. **Protocol text vs implementation.** Protocol §6 still says F0 uses type-7 quantiles and F2 uses "all eligible journals". The code uses Hazen (D1) and visibility-only eligibility (D2). Both are logged as deviations, but the protocol document itself was not amended, so a reader of the protocol alone cannot reproduce the numbers.

### MINOR
8. **Dependencies.** `requirements.txt` omits `statsmodels`, which §11 of the protocol lists (no code imports it), and leaves `requests` and `pytest` unpinned. There is no Python lockfile; a Python 3.13 requirement is stated only in the README.
9. **"~7 min on 4 cores".** The run was effectively single-core (about 7 min on one core; LightGBM uses n_jobs=2 only in E7). Timing (422 s) matches, but the 4-core claim is misleading. The variant runs took 567 to 573 s when run three at a time.
10. **Dangling README references.** The top-level README refers to `review/final_audit.md` and to ten review passes, consistency, reproducibility and rejection-risk reports. Only `review_01` to `review_10.md`, `claim_evidence_matrix.csv` and `independent_review_agentA.md` existed when I last listed `review/` (`final_audit.md` was absent).
11. **Hidden choices in code.** Missing `n_authors` and `n_refs` are median-imputed in E7. The "recent" cohort window (accepted >= 2025-04-20) is hard-coded in `make_tables.py`. Neither is stated in the protocol.

## 6. Outsider barriers (item 7)

- **Raw data.** Not in git (see issue 1). Crossref collection takes 1 to 2 h and PubMed about 30 min, and returns the then-current state of late-deposited metadata, so exact numbers will drift (disclosed in the code README).
- **API dependence.** `build_frame.py` depends on live Crossref member facets, so the 802-journal frame can be reproduced only from the checked-in `frame_eligible.json`. This is disclosed as a comment in `run_pipeline.sh`.
- **Blocked validation.** Deviation D4 discloses that the spot-check against publisher pages was blocked.
- **"Pre-registered".** The protocol freeze is a git commit in the same repository, not an external registry timestamp. Data collection started before the freeze, and Step 0 used data overlapping the study period (protocol §10, disclosed). An outsider cannot verify that the freeze preceded the forecast runs except via git history.

## 7. Bottom line

From the processed data present in the working tree (not in git), the analysis is reproducible: the unit tests pass, all main outputs re-run to identical bytes (apart from timing metadata), and independent code reproduces F0 for all 1,531 journal-origins to 1e-16. Reproducing the data themselves is not possible from the repository alone. Several documentation and traceability gaps remain, listed above as issues 2 to 7.
