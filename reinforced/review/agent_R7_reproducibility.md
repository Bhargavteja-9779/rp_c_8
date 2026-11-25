# Agent R7 - independent reproducibility audit of cycle 4, Part E

Auditor: agent R7 (fresh scratch copy, no writes to the project other than this report).
Audited code/results state: commit `6335b36` (code and results identical to `af57c85`; HEAD at the time the scratch copy was taken). While the audit was running, commits `b5034d7` (Amendment E-A8, revised `e_analysis7.py`), `757451c` and `bdc4678` appeared in the repository; section 6 covers them briefly.
Environment: Linux, 4 cores, 15 GB RAM, Python 3 with pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, statsmodels 0.15.0 (the repository pins no versions: there is no requirements or environment file).

## 0. Bottom line

* The pipeline from raw Crossref and Retraction Watch files to every committed `E_results*.json` and `E_build_summary.json` reproduces **bit-for-bit**: 0 of about 1,800 numeric leaves differ at all (largest absolute difference 0.0), including every journal-cluster bootstrap interval, the Cox bootstrap intervals and `e_articles.csv.gz` (1,803,587 rows x 38 columns, max numeric difference 0, `rdate` identical).
* `verify_headline_numbers.py` passes (all OK) and `pytest product/tests` gives 14 passed.
* My own short code (no `e_lib`) reproduces the MH odds ratios, the negative control, the ratio of odds ratios and the A26 rate ratio. It also exposed one real defect (duplicated ISSN rows in `collect_crossref_summary.tsv`, section 4) that changes A20 totals and A21 slightly. It does not touch the primary result. It was already being fixed by the author (E-A8) while I worked.
* Protocol order: the original protocol sections E0-E3 were committed before any result file and are unchanged. Amendments E-A3 to E-A7 precede the results they govern. E-A1 and E-A2 were committed in the same commit as the first results, and several scripts were run a few minutes before they were committed (section 5).

## 1. Setup and data (commands)

```
tar cf - --exclude=.git . | tar xf - -C /tmp/audit6        # rsync is not installed; tar used
grep -rl /home/user/rp_c_8 --include=*.py /tmp/audit6 | xargs sed -i 's#/home/user/rp_c_8#/tmp/audit6#g'
rm data/processed/*.gz data/processed/journal_titles.csv   # force rebuild (data/processed is git-ignored)
python3 code/src/prepare_data.py                            # 2 min
```
* Decompressed SHA-256 of rebuilt `articles_clean.csv.gz` = `b0a82942...e3c7ac`, equal to `results/data_manifest.json`. Same for `articles_clean_noC5.csv.gz` (`1e8c19b7...`). PASS.
* Note that the gzip container hash of the original `articles_clean.csv.gz` (88e51062...) is not the manifest value; the manifest correctly says it records decompressed content.
* All inputs needed by Part E are tracked in git (802 raw Crossref files, `retraction_watch.csv.gz`, `coverage_notices.csv`, `collect_crossref_summary.tsv`, `journal_imprint_map.csv`, `defaults.json`, `config.json`, `pubmed_ext`); I checked with `git ls-files` because the scratch copy came from the working tree.
* I confirmed with a script-by-script diff (after reversing the path sed) that every script I ran (`e_build`, `e_lib`, `e_analysis`..`e_analysis7`, `verify_headline_numbers`, `d_lib`, `prepare_data`) is identical to the version in commit `6335b36`.

## 2. e_build and comparison with the originals

`python3 reinforced/code/src/e_build.py` (2 min 44 s). Compared with pandas, all 38 columns:
* shape (1,803,587, 38), same column order, same dtypes, same row order (`doi` identical).
* max absolute numeric difference **0** (tolerance used 1e-9); NaN patterns identical; `rdate` (3,454 non-null) identical.
* `E_build_summary.json`: 48 leaves, 0 differences (flow table, n_retracted 3,454, n_process 2,639, RW snapshot SHA-256 `9d1556fe...`, tau2 0.040133, same-day excluded 10,163 with 2 retracted).

## 3. Analyses

Run in the scratch copy, writing to the scratch results directory (`e_analysis`, `2`, `3`, `4`, `6`, `7`; run in parallel, one OOM kill of an unrelated comparison script, rerun afterwards). `e_analysis5.py` (Cox) was also run (627 s).

| script | wall time | numeric leaves compared | leaves differing >1e-9 | largest abs. difference |
|---|---|---|---|---|
| E_build_summary.json | 2m44 | 41 | 0 | 0 |
| E_results.json (A1-A6) | 80 s | 655 | 0 | 0 |
| E_results2.json (A7-A10) | 214 s | 227 | 0 | 0 |
| E_results3.json (A11-A12) | 36 s | 171 | 0 | 0 |
| E_results4.json (A13) | 28 s | 104 | 0 | 0 |
| E_results5.json (A14 Cox, 200 bootstrap refits) | 627 s | 72 | 0 | 0 |
| E_results6.json (A15-A19) | 36 s | 222 | 0 | 0 |
| E_results7.json (A20-A26, as committed at 6335b36) | 59 s | 293 | 0 | 0 |

No keys missing or extra, no string differences. Bootstrap intervals are also exact, because every script seeds `numpy.random.default_rng` explicitly (module-level generator in `e_lib` for `mh_ci`). The comparison was made against the committed blobs (`git show 6335b36:...`), not the working tree, because the working tree changed during the audit. Scratch outputs were written fresh (file mtimes 00:28-00:43 on the audit day); I verified they were not the copied originals.

Caveat: exact reproduction depends on the identical software stack. I could not test other pandas/numpy/scipy versions; the repository does not pin versions (MINOR, section 7).

## 4. Headline numbers, tests and independent recomputation

* `python3 reinforced/code/src/verify_headline_numbers.py` (scratch): all 8 checks OK (articles 1,803,587; retracted 3,454; process 2,639; OR fastest 5% vs R_process 4.1892; vs R_any 3.1052; slowest 5% 0.1009; negative control 0.8758; flagged share 0.0538; crude unstratified OR 3.05).
* `python3 -m pytest -q product/tests` (scratch, with hard-coded paths rewritten): `14 passed`.
* Independent recomputation (`/tmp/audit6_indep/indep.py`, plain pandas/numpy, no `e_lib`; X1 and N1 re-derived from dates; outcome flags re-derived from the raw Retraction Watch file with my own parsing):

| quantity | my value | committed value |
|---|---|---|
| D recomputed from dates equals `D` column | True | |
| own X1 (D <= 5th percentile of journal x acceptance-year stratum, >=100 articles) equals column X1 | True | |
| own N1 (received on weekend) equals column | True | |
| own R_process / R_any / R_pubother equal columns (counts 2,639 / 3,454 / 382) | True | |
| MH OR, X1 vs R_process | 4.189188905580355 | 4.189188905580355 (A1) |
| MH OR, X1 vs R_any | 3.1051975398758733 | A1 R_any (verify script OK) |
| negative control N1 vs R_process | 0.8757878501990694 | 0.8758 (verify script) |
| negative control N1 vs R_any | 0.9106321 | in E_results.json (not separately printed by me) |
| MH OR X1 vs R_pubother (publisher-investigated, not process-related) | **1.1368** (378 events in X1-defined strata) | **1.1307** (380 events) in committed A21 |
| A21 ratio of ORs | **3.685** | **3.705** in committed A21 (CI 1.64-8.11) |
| A26: journal-months n>=30 / events / flagged months | 20,291 / 2,325 / 494 | identical |
| A26: rate flagged 0.009828, rate other 0.001850, rate ratio | 5.312455 | 5.312455 (CI 0.41-18.03) |
| A26: share of events captured / share of articles | 0.0895 / 0.0182 | identical |

The A26 rate ratio and the primary MH OR agree to full double precision. The A21 discrepancy is the finding below.

### Finding A: duplicated ISSN rows in `collect_crossref_summary.tsv` leak into A20/A21 (as committed at 6335b36)

`data/raw/collect_crossref_summary.tsv` has 808 rows but 802 journals; six ISSNs (1436-2449, 1618-9558, 1432-0851, 1420-9039, 1432-1106, 2198-7793) occur twice. `e_analysis7.py` merges this table into `jc` and then `d1 = d1.merge(jc[...], on="issn", how="left")`, which duplicates every article of those six journals in `d1`. I confirmed by re-running a patched copy (`.drop_duplicates("issn")`, file `reinforced/code/src/e_analysis7_dedup_audit.py` in scratch only). Effects on the committed `E_results7.json` (the 19 changed leaves; everything else, including A22-A26, is unchanged):
* A20: `records_returned_total` 1,956,720 vs correct 1,945,453; `records_dated` 1,840,163 vs 1,829,907 (the correct value equals the dated-record count printed by `prepare_data.py`, 1,829,907); `dated_share_overall` 0.9404 vs 0.9406; Springer Nature notices 5,606 vs 5,583 and cohort retractions 1,624 vs 1,620 (the build summary says 1,620); `exposed` and `n` of four sensitivity rows (coverage<0.5, dated_share >=0.95, >=0.90, <0.90) inflated by 0.4-0.7%.
* A21: `or_pubother` 1.1307 vs 1.1368, `events_pubother` 380 vs 378, `ratio` 3.705 vs 3.685, ratio CI 1.64-8.11 vs 1.63-8.08.
* Primary odds ratio, A20 sensitivity odds ratios and A22-A26 are unaffected to the stated precision.

Severity MODERATE for the record (small numeric effect, wrong denominators in a coverage table, a published ratio off in the second decimal), no effect on conclusions. This is the same issue that Amendment E-A8 (commit `b5034d7`, "A20 corrected. The collection summary contains duplicated ISSN rows") now addresses, so it is already in the author's hands.

## 5. Protocol order of events (git, mtimes)

Commit times (UTC, 2026-11-24 unless stated), from `git log`:

| item | commit | time | first result file it precedes |
|---|---|---|---|
| Original protocol (E0-E3, HE1-5, A1-A6) | c2139be | 19:40:32 | all |
| e_build.py (no associations) | c849493 | 19:43:02 | |
| e_analysis.py ("launched immediately before this commit; unchanged") | 353aab1 | 19:43:10 | |
| E-A1, E-A2, e_lib, modified e_analysis.py **and first E_results.json** | 98549c6 | 19:45:34 | E_results.json (same commit) |
| e_analysis2.py (A7-A10) | 4675d9e | 19:45:55 | E_results2.json (721f0f4, 19:49:59) |
| E-A3 + e_analysis3.py (A11-A12) (E_results2.json also in this commit) | 721f0f4 | 19:49:59 | E_results3.json (802ce5e, 19:50:44) |
| E-A4 + e_analysis4.py (A13) | 85029de | 19:52:18 | E_results4.json (b8adfe1, 19:55:52) |
| E-A5 + e_analysis5.py (Cox) | 6758cf0 | 20:04:28 | E_results5.json |
| E-A5b + modified Cox script + first-run E_results5.json (NaN CIs) | dc6bb6e | 20:05:00 | |
| E-A6 (cohort correction, A15-A19); v1 results renamed `*_v1cohort` | 01535fd | 20:16:42 | corrected-cohort results |
| corrected e_build/e_analysis*, e_analysis6.py, E_build_summary.json | 73e79ce | 20:19:48 | E_results*.json corrected (3b73338, 20:28:48) |
| E-A7 + e_cover_collect.py | 7eb6f28| 20:51:16 | |
| e_build (tau2 variants, publisher flag), e_analysis7.py (A20-A26) | 8b41a99 | 20:55:49 | E_results7.json (2251c27, 20:58:09) |
| A1 bootstrap 2,000 draws (e_analysis.py) | dcefec1 | 21:00:03 | E_results.json rerun, committed at af57c85 (00:22:57, 25 Nov) |

Checks performed:
* **Original sections unchanged.** I extracted the protocol at c2139be and at HEAD; the text up to the "Amendment E-A1" heading is identical (one blank line difference). The original was committed 5 min before the first result file (98549c6) and 3 min before the first analysis script (353aab1); no `E_results*.json` exists in any commit before 98549c6. PASS.
* **E-A3 to E-A7 precede the results they govern** (commit order above; `E_results3/4/5/6/7` first appear in later commits than their amendments; mtimes of the v1-cohort outputs, for example `E_results3_v1cohort.json` 19:50:17 and `E_results4_v1cohort.json` 19:52:43, fall between amendment commit and results commit). PASS, with the qualification that the amendments from E-A3 onward were written after the author had seen earlier results (this is stated in each amendment and E-A6/E-A7 openly say they respond to reviews).
* **E-A1 and E-A2 were not committed before the first results.** They are in the same commit as `E_results.json`. The text of E-A1 says it was written after the first run; E-A2 says its analyses were specified before they were run, which is supported for A7-A10 (script committed 4675d9e before E_results2.json), but the git history alone cannot show that E-A2 was written before the first results were looked at. The first-run (pre-E-A1, diverged logistic) output was never committed. MODERATE for the pre-registration claim, already disclosed in the protocol text; the headline MH results do not depend on the E-A1 optimiser.
* **E-A5 vs the Cox run.** The first Cox output (NaN confidence intervals) was committed together with E-A5b (dc6bb6e), 32 seconds after the E-A5 commit; the amended script and rerun came afterwards. Consistent with the E-A5b wording. MINOR.
* **Script run before commit.** `e_build.py` mtime 20:51:54 and `e_articles.csv.gz` / `E_build_summary.json` mtime 20:54:50 are after the E-A7 commit (20:51:16) but before the commit that contains the modified build (8b41a99, 20:55:49), so the E-A7 build changes (tau2 variants, publisher-investigated flag) were committed about one minute after they were run. The same applies to e_analysis7.py (coverage file `coverage_notices.csv` mtime 20:53:38). No associations were computed by the build; I regard this as MINOR, and the commit message says "before running" for e_analysis7, which I cannot confirm from mtimes alone (the file now has a later mtime because of E-A8).
* **E_results.json mtime vs commit.** The rerun with 2,000 bootstrap draws has file mtime 21:00:56 and the script commit is 21:00:03, but the results were committed only at 00:22:57 on 25 November, after manuscript v3 text was built from them. MINOR (results existed on disk and were used before being committed).
* The mtimes themselves are file-system times in the working tree and can be altered; git commit timestamps can also be set by the committer. They are consistent with each other but are not tamper-proof evidence.

## 6. Commits that appeared during the audit (E-A8)

* b5034d7 (00:35:18, 25 Nov) adds Amendment E-A8 and a revised `e_analysis7.py` before the rerun; the E_results7.json modification in the working tree followed at 00:36:27, and 757451c / bdc4678 (manuscript v4) at 00:39. Order: amendment+script, then results, as required.
* I ran the HEAD `e_analysis7.py` against my scratch rebuild (`/tmp/audit6/reinforced/code/src/e_analysis7_EA8_audit.py`, 41 s, output in `/tmp/audit6_fix/results8`) and compared with HEAD `E_results7.json`: 336 numeric leaves, 0 differences, no missing keys. So the E-A8 rerun also reproduces exactly. I did not audit the new manuscript text, the new A26 negative result, or the new RW-side coverage logic beyond reproducing the numbers.

## 7. Issues

FATAL: none.

MAJOR: none.

MODERATE
1. Duplicated ISSN rows in `data/raw/collect_crossref_summary.tsv` inflated A20 totals/sensitivity counts and A21 (OR pubother 1.1307 vs 1.1368; ratio of ORs 3.705 vs 3.685) in the results committed at af57c85/6335b36 (details in Finding A). Fixed in E-A8 (reproduced).
2. Amendments E-A1 and E-A2 were committed together with the first results, so git cannot show that they predate the first look at the results; E-A2's A7-A10 are post hoc in that sense (the protocol says so). Any pre-registration claim should be limited to the original E0-E3 text and to E-A3 onward for the "specified before running" scripts.

MINOR
3. No pinned software versions (no requirements or environment file); exact reproduction here relied on the same stack as the original run.
4. Every script hard-codes `/home/user/rp_c_8`; `product/tests/test_core.py` also hard-codes it, so the test suite only runs at that path. I had to sed paths to run in scratch.
5. `e_build.py` / `e_analysis7.py` were run about one to two minutes before being committed, and `E_results.json` (A1, 2,000 draws) was committed 3.4 hours after it was produced.
6. The first-run (pre-E-A1) result of `e_analysis.py` and the first-run MH results the E-A1 text mentions were never committed.
7. The scratch run of `prepare_data.py` takes 2 min, `e_build` 2.7 min, A7-A10 3.6 min, Cox 10.5 min; the README does not state the run order with run times (not checked in detail).

## 8. What I could not run or did not check

* Not run: `e_cover_collect.py` (needs the live Crossref API; its output `coverage_notices.csv` is tracked and was used as is, I did not re-collect it); `collect_pubmed_external.py` and other collectors; `e_tables.py`, `e_figures.py` and the manuscript/docx/PDF builders (not part of the request); cycle 1-3 code (`d_*`, `y*`, `z_*`, `run_*`); `probe_preprint_dates.py` (network).
* The raw Crossref and PubMed files could not be checked against the live APIs (data are time-dependent); only the repository copies and the manifest hashes were used. The manifest's raw-collection digest (`70e2becc...`) was not recomputed.
* The Retraction Watch snapshot is the committed one (SHA-256 of the gz `9d1556fe...` matches `E_build_summary.json`, produced by my rebuild); I could not verify the download date or provenance.
* The optional fixed-effects logistic regression was not independently recomputed (it reproduces bit-for-bit via the committed code, but I wrote no separate implementation). AUC, PIT, Cox and meta-analysis results were verified only by re-execution of the authors' code, not by independent re-implementation. The independent checks are: MH ORs (X1 vs R_process, R_any; N1), the A21 ratio (including R_pubother), the A26 journal-month flag rate ratio and its components, and the derivation of X1, N1 and outcome flags.
* Other pandas/numpy versions or platforms were not tried.
* The protocol-order analysis is limited to git commit metadata and file mtimes; I cannot verify what was run before 98549c6 beyond the commit messages.

## 9. Files created (scratch only)

`/tmp/audit6` (scratch project copy and outputs), `/tmp/audit6_indep/indep.py` (independent recomputation), `/tmp/audit6_fix/` (dedup and E-A8 reruns), `/tmp/audit6_git/` (committed JSON blobs used for comparison), logs `/tmp/audit6_an*.log`. Nothing in `/home/user/rp_c_8` was modified except this report.
