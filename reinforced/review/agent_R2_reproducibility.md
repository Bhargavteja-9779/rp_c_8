# Reproducibility audit R2 (cycle 2) – independent cold-start check
Scope: HEAD 5c96910 (manuscript v3, sha256 e17a37e3…); scratch copy in `/tmp/audit2` (paths rewritten with `sed`). Only this file was written in the repo. Environment: Python 3.13.16 and the library versions pinned in `code/requirements.txt`.

## Verdict
No FATAL or CRITICAL issue. Every cycle-2 script I re-ran reproduced the committed outputs byte-for-byte, and the numbers I checked agree with their sources except as listed. Weak points: the X1 order-of-events statement, README order, absolute paths, and some unlogged deviations.

## 1. Commands I executed and results
All runs: `cd /tmp/audit2/reinforced/code/src && python3 -I <script>.py`, then MD5/SHA-256/numeric comparison with a copy of the committed outputs (`/tmp/audit2/cmp.py`).

| Script | Wall time | Result vs committed |
|---|---|---|
| `y0_imprint_inference.py` | 16 s | Y0 json + `journal_imprint_map.csv` BYTE-IDENTICAL |
| `forensics.py` | 22 s | identical |
| `cal_and_meta.py` | 8 m 20 s (contended) | `cal_meta_metrics.csv`, `cal_meta_summary.json` identical |
| `y1_rolling_panel.py` | 77 s | identical (not "long") |
| `y2_null_and_simulation.py` | 40 s | identical |
| `y3_type_robustness.py` | 6 m 39 s | identical |
| `y4_y5.py` | first attempt killed by my own `timeout 100` (the file was not rewritten; I caught this from mtimes). Re-run to completion | identical |
| `dependence_quality_calibration.py` | 49 s | `X4_X5_X6_summary.json`, `X5_flagged_journals.json` identical |
| `x1_analysis.py` | seconds | `X1_summary.json` identical |
| `z_experiments.py` | 4 m 33 s | SHA-256 identical for `Z1_cohort_effect_null.csv` (6d122d98…), `Z2_strict_recal.csv` (8f645e6b…), `Z_summary.json` (4023927a…) |
| `cycle2_metrics_and_figures.py` (v3 version) | seconds | `metrics_cycle2.json` identical; the three PNGs are `cmp`-identical |
| `build_revised_manuscript.py` | seconds | `pandoc -t plain` of the rebuilt DOCX has 0 diff lines against the committed DOCX |
| `pytest -q code/tests` (in repo, `-p no:cacheprovider`) | 19 s | 10 passed |
| `prepare_data.py` in a scratch copy | killed by my `timeout 110` after the primary file was written | decompressed SHA-256 of `articles_clean.csv.gz` = b0a82942…c7ac, equal to `results/data_manifest.json` and to the local file; `cleaning_log.csv` identical. The noC5 variant was not completed |

Not run: `probe_preprint_dates.py` in full (30 min live API; would overwrite the partial file), `consistency_check.py` (writes into the repo), and the cycle-1 pipeline producing `results/metrics_journal_origin.csv`, `revision_R1_*` and `results/external/e9_metrics.csv`. These were used as committed, not regenerated. Probe spot-check: I queried live Crossref for 2 of 8 sampled journals before a call failed: 30/30 and 29/30 committed DOIs returned, so new deposits already shift the "first 30". The C2-1 query (`rows`+`sample`) does return HTTP 400.

## 2. Order-of-events claims against git and mtimes
Commits: af19c71 (16:10:22) = X1–X3 code and results, forensics, protocol first part (X4–X6 specified); 2aaa51e (16:21:44) = X4–X6 code and results, Part B; e55346c (20:57) = Y0–Y5, X1 data; 8df8eed (21:08:25) = Part C; 9014105 (02:24 next day) = Z results, v3.

Supported:
- X4–X6 were specified in af19c71 (16:10:22). The script mtime is 16:10:50 and the results 16:11:27.
- Part B was committed at 16:21:44, before the Y scripts (mtimes 16:22:19–16:26:08) and results.
- Part C was committed at 21:08:25, before `z_experiments.py` (21:09:21) and its outputs (21:10–21:14).
- The cycle-1 protocol (6a9c4a9, 2026-10-20) predates the pipeline (4cc4d98, 2026-10-21 01:48). It was later edited in c759300 and bc40a94, as logged in D8.
- X2/X3 outputs (15:56) predate the protocol text (16:10), as disclosed.

Contradicted or not verifiable:
- **MAJOR – X1 "designed in code and run once before the protocol text was written"** (Methods, v2 and v3; protocol line 4; C2-4; the `cal_and_meta` docstring is limited to X2/X3). The probe in af19c71 contained the failing `sample` query and produced no data (C2-1). The data come from a relaunch with edited code (`rows` 60→30, `sample` removed, shuffle, incremental writes, 6→8 threads). That script's mtime is 16:30:01 and the partial file's last write is 16:41:47, which is 20–30 minutes after the protocol commit and during the Y runs. So X1 was run at least twice, and its data were collected after the protocol text. Only "started" is true. Fix: state this in Methods and C2-4.
- **MODERATE – `reinforcement_plan.md` is retrospective.** Its mtime is 16:32, after Y0–Y5 outputs (16:22–16:30). Its "Expected if true" cells reproduce results (Y1 "−1.5…−3.5 pts"; X1 "threshold later found too tight"). Fix: relabel it as written after the fact.
- **MODERATE – `cal_and_meta.py` mtime (16:07:32) is later than its outputs (15:56:04).** "Single run, no edits" cannot be verified from git, because there is one commit. My re-run is byte-identical, so any later edit did not change the outputs.
- **MODERATE – C2-8 "Y3/Y4/Y5 run once as specified" is not exact.** Part B/common rules say 5,000 bootstrap draws. The code uses 2,000 (Y3) and 3,000 (Y4). Y5 is a LightGBM model, not a regression, with an extra feature `sd`. Y2 uses n_test ≥ 50 (not specified).
- **MINOR:** `research_design/deviations.md` reads "described as pre-specified, not pre-specified" (mechanical replace of "pre-registered"). C2-3 reports all-publisher Research Square figures (45%, 91%, 4.8%), while the manuscript reports Springer Nature only (47%, 95%, 2.6%). The restriction to Springer Nature was made after seeing the by-publisher results (Wiley and Taylor & Francis fail) and is not logged as post hoc.

The v2 "seven hypotheses pre-specified" wording is fixed in v3.

## 3. Numeric verification (v3 DOCX; PASS unless noted)
Own code (no `tdelay`) from `articles_clean.csv.gz`: `/tmp/audit2/indep.py`, `indep_z1.py`.
1. 1,737,272 records / 800 journals / median D 124 / 22.8% ≤72 d: PASS (own count; `data_audit.json`).
2. F0 shortfall −3.0 points, journal mean over 1,531 journal-origins and 781 journals: −3.034 PASS (own recomputation; Hazen quantiles, visibility rule coded independently). Origin 2023: −3.348; origin 2024: −2.652 (Table 4 "−3.3", "−2.7") PASS.
3. Paper-weighted −3.6 / 76.4% coverage: −3.627 PASS. 298,469 target papers PASS.
4. 184/1,531 = 12.0%; 25 (1.6%); 7 (0.5%): PASS (own count).
5. Z2 strict F0: origins 2023-10/2024-01/2024-04 gave 751/754/753 journal-origins (2,258 total = manuscript n) and −1.45/−1.90/−2.49 points: PASS (Z_summary −1.9 [−2.4,−1.3]).
6. Z2 V: own grid search gives c = 1.075 and coverage +1.5/+1.1/+0.4 (manuscript +1.1): PASS.
7. Z2 R (own randomised-PIT map): +2.4/+2.0/+1.3 (manuscript +1.9): PASS.
8. Z1 (own simulation, 10 reps): σ²/2 −2.77, σ² −4.81, 2σ² −8.87, oracle −1.58 vs manuscript −2.8, −4.9, −8.9, −1.6: PASS (Monte Carlo difference ≤0.09).
9. Z1 SD observed 8.6 vs simulated 2.8; correlations 0.36 / 0.16; proxy −2.1: PASS (`Z_summary.json`).
10. X1: 4,222 Research Square articles; 4,018 Springer Nature in 212 journals; SN 95.1% ≤+14 d, 2.6% >+90 d, 46.6% |Δ|≤14 (47%): PASS (own csv parse of `preprint_probe.csv.partial`). Wiley median +79 d and Taylor & Francis +100 d: PASS (a first `dayfirst` parse mis-read ISO dates; fixed with explicit formats). Journal-weighted 82% / 8.9%: PASS (Z4).
11. Variance shares 26.5 / 4.4 / 69.1%, CI 24.7–28.3: PASS (`variance_components.json`).
12. Table 1 (pinball, skill, coverage, width, F0–F6): PASS (`pinball_by_method.csv`, `coverage_summary.csv`).
13. Table 2 journal-cluster CIs: PASS (`contrasts_pinball.csv`). t(6) CIs, Holm p and publisher p: PASS (`Z3`). MINOR: the mean column is the journal mean (+0.0025) but the t(6) interval is centred on the imprint mean (+0.0030).
14. Table 3: oracle −1.5, truncated −12.9, random split −0.0, stationary sim +0.1: PASS (`oracle_diagnostic_E10`, `Y2_summary`).
15. Panel: 7,417 / 787, −3.4 / −1.4 / −2.5, pooled −2.4 (block CI −2.9 to −1.8), lag-1 0.76, two-way CI −3.4 to −1.3, predictive −4.0 to −0.8, skill 16.2%: PASS.
16. Backward oracle (−4.1/−2.3/−2.5; −3.3/−1.4/−1.4) and pre-origin eligibility (789 journals, −3.1): PASS (Z5).
17. Slopes 0.91 (0.88–0.94) → 0.97 (0.93–1.00), 120 d 0.93→0.98, 180 d 0.92→0.95, Brier −0.0004 (−0.0006,−0.0002): PASS (Z2). R −0.0002, V +0.0001, F4 +0.0033, F2 +0.041: PASS.
18. Table 4 (all 9 rows, journals, shortfall, skill, P72 share, ICC): PASS (`Y3_type_robustness.json`, `X4_X5_X6_summary.json`). Leave-one-out −3.5…−2.5 and ICC 24.5–29.0%: PASS.
19. RQ5: 158,735 papers / 766 journals; 1.0% (0.6–1.4), 0.8%, 3.0% (2.3–3.6), τ=0.10 5.8%, τ=0.90 0.5%: PASS (`Y4_Y5_summary.json`).
20. Drift 7.3/5.3/53%/0.09/18.8%; skewness −0.79; field shares 28/23/7%; high bin 23, 19, 86%, 75%; 99.997% of 59,885; PubMed 14.8%, −0.7 [−3.6,+2.1]: PASS.
21. Recalibration look-ahead variant +1.4 / −2.5 / −0.00008: PASS (`cal_meta_summary.json`). L−F0 +0.0002: PASS. Share of Springer Nature 56%: PASS (56.3%).

FAIL or unsupported:
- **MINOR – "Thirty non-frame PubMed journals gave 27.4% (17.2–34.5%)"**: `metrics.json vc_ext.n_journals` = 32. (Thirty is the E9 forecasting set.)
- **MINOR – "maps were learned from early origins at which the shortfall was larger (−3.4 to −2.4 points)"**: the origins actually used by the strict rule are 2022-01, 2022-04 and 2022-07, with shortfalls −3.37, −3.33 and −2.85. −2.4 belongs to 2022-10, which is never used.
- **MINOR – "median offset varied from −22 to −7 days by received year"**: Z4 also lists 2020 at −29 (n = 9); 2024 is −22.
- **MINOR – H5 row** shows Y4 variants (1.0%, 3.0%), not the confirmatory v1 value (3.4%, `hypothesis_summary.json`).
- **Not traceable to a results file:** the skew-normal / pooled-shape / blended forecasters "tested by an independent reviewer" exist only in review prose (`review/independent_review_agentA.md`, `agent_DEF_methods.md`). Introductory facts ("2,700 papers from 135 journals", MetaROR April 2026, vendor statement) are external and unchecked; F7/F8 rely on cycle-1 `revision_R3_F7F8_EXPLORATORY.csv`, not recomputed.
- The v2 hard-coded "3 of 6" (actual 4 of 6) is gone in v3.

## 4. Placeholders, dangling references
- Author placeholders are intentional: title-page authors; competing interests; funding; authors' contributions; acknowledgements; authors' information (6 bracketed strings).
- References: 29 entries, 29 distinct numbers cited, 0 dangling and 0 uncited. Figures 1–6 and Tables 1–5 are all captioned and cited. The 8 embedded images match the repo PNGs by MD5. 25 of 29 entries have DOIs. 24 of those DOIs are in the verified-reference JSONs; ref 11 (10.59350/j755k-m0247) is only in the literature CSVs. I did not resolve DOIs online.
- The repository URL in the data statement (`github.com/Bhargavteja-9779/rp_c_8`, branch `claude/autonomous-research-institute-nz8co5`) matches `git remote` and the current branch. Visibility not checked. "Z2" is used in Methods without definition.

## 5. Docstrings and design claims
- **MODERATE – `cal_and_meta.py` docstring ("strict time ordering… labels complete before the test origin… accepted by 2023-07") is false in the tail.** Training cohorts include every paper received in the window, whenever accepted (data to 2026-10). For the 2022-H1 cohort, 0.94% were accepted after the 2024-01-01 origin and 3.1% after 2023-07-01. For the 2023-H1 cohort, 0.97% were accepted after 2025-01-01. This affects X2, X3, X6 and Y4 ("complete labels"). The effect is probably small, and the manuscript now demotes X2/X6 as "look-ahead variant". Fix: correct the docstring and the Y4/X6 spec text, or truncate labels at the origin.
- Docstrings of `dependence_quality_calibration.py` and `z_experiments.py` are supported by timestamps. `y0` labels the "other" imprint (26 journals) `note_hindawi_journals_in_800`; Hindawi is not established (MINOR).

## 6. Can an outsider reproduce cycle 2 from the repository?
Mostly yes, with the fixes below; the Research Square probe is only partly reproducible.
- **MAJOR – absolute paths.** `ROOT="/home/user/rp_c_8"` and `sys.path.insert(0,"/home/user/rp_c_8/code/src")` are hard-coded in all 12 cycle-2 scripts (19 occurrences) plus `consistency_check.py`. The README says to edit them. Fix: derive ROOT from `__file__` as `prepare_data.py` does.
- **MAJOR – README ordering error.** Step 3 runs `x1_analysis.py` before step 4, which creates `X5_flagged_journals.json`. I tested this on a clean directory and it fails with FileNotFoundError. Similarly `y1`, `y4_y5` and `z_experiments` need `journal_imprint_map.csv` from `y0` (documented). `cycle2_metrics_and_figures` needs `Z_summary.json` and `X1_summary.json` (it was undocumented before step 7 was added). Correct order: forensics → cal_and_meta → dependence_quality → x1_analysis → y0 → y1–y5 → z → cycle2 metrics → builder.
- **MAJOR – `data/processed/` is git-ignored** (`.gitignore`), but the reinforced README never says that `articles_clean.csv.gz` must first be built with `code/src/prepare_data.py` (verified to reproduce the manifest hash, about 2 minutes). Cycle-1 inputs (`metrics_journal_origin.csv`, `revision_R1_*`, `e9_metrics.csv`, `drift_pairs.csv`, `variance_components.json`) are committed, but regenerating them needs `run_all.py` and `revision_analyses.py` (not run by me).
- **MODERATE – the probe is not reproducible.** It queries live Crossref. The "first 30 linked articles" depends on Crossref's ordering and on deposits to date (my spot-check shows drift). The working run was cut by a worker restart and uses only the incremental `.partial` file. A rerun would overwrite that file in "w" mode and destroy the committed evidence. The number of journals attempted before the restart was not logged (388 had data). `probe_preprint_dates.py` sends a personal e-mail address in its User-Agent.
- **MINOR:** the PDF is not produced by any script (LibreOffice is presumably used manually). The reinforced README does not mention `code/requirements.txt`. All runs were deterministic; other core counts were not tested.
