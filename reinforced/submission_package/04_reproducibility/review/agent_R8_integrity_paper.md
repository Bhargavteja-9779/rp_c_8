# Referee report R8 (hostile but fair): "Fast editorial handling and later retraction for peer-review-related reasons: a retrospective stratified analysis of Crossref and Retraction Watch records" (E-cohort manuscript after amendment E-A7)

Reviewer role: Research Integrity and Peer Review; meta-research / epidemiology / statistics. Inputs read: current `Integrity_Manuscript.docx` and `Integrity_Supplement.docx` (pandoc plain text), `Integrity_Cover_Letter.docx`, RECORD checklist, R5 and R6 reports, `cycle4_protocol_partE.md`, `e_build.py`, `e_analysis.py`, `e_analysis7.py`, `build_integrity_manuscript.py`, all `E_results*.json`, `E_build_summary.json`, `E_tables.json`. My own recomputations (scratch code outside the repo, run read-only on `data/processed/e_articles.csv.gz`, `data/raw/collect_crossref_summary.tsv`, `data/raw/coverage_notices.csv`, the Retraction Watch file): A24 meta-analysis (reproduced exactly), journal-month analysis A26 and variants, left truncation of the score, coverage against Retraction Watch with original-paper date. No repository file was modified except this report.

Bottom line: the arithmetic is accurate and the rewrite repaired most of R6's wording and reporting problems. But (i) the new journal-month result that the abstract, Discussion, Conclusions and cover letter use as the "useful framing" is circular and rests on one journal-month, (ii) the date-availability selection problem (R6 M1) is disclosed but not resolved, the new "coverage index" is misleading, and two pre-specified sensitivity rows are missing from Table 3, and (iii) a cluster of stale or wrong statements was introduced by the rewrite.

---

## 1. Disposition of R6 MAJOR and MODERATE findings

| R6 | Topic | Status | Comment |
|---|---|---|---|
| M1 | Selection on availability of received/accepted assertions | PARTLY. Disclosed, not resolved | Table 1 now starts from all records returned; coverage and dated-share analyses added. But the retracted column for the first two rows is "–", the coverage index is confounded (see F2), two of the pre-specified A20 sensitivities were dropped from Table 3, "no exclusion depended on retraction status" is unchanged, the RECORD checklist was not regenerated. |
| M2 | "1.8 million", effective sample, one Hindawi-legacy cluster | MOSTLY | Title changed; abstract states 111 journal-years / 71 journals; Table S1 lists the top ten journals. The main text still never states that one journal (BioMed Research International) holds 30% of events (E_results3 A12 share_top["1"] = 0.3024) and 36% of the flagged 1% score events. |
| M3 | Circular ascertainment | MOSTLY | Ratio of ORs 3.7 (1.6-8.1) added; label-free estimate reported with 21 exposed events; "specific to the editorial process" removed. But the abstract's Conclusions sentence still has no ascertainment caveat (it is only in the final Conclusions section). |
| M4 | AUC dominated by one stratum, tau2 look-ahead, no baseline | MOSTLY | 0.70 without largest stratum, 0.71 equal weights, tau2 variants, journal-history and raw-D baselines all added. New problems in F6. |
| M5 | Exposure definition (threshold including retracted articles; ties; D = 0) | YES | Table 3 rows and the Results sentence; 10,163 same-day records and 2 retracted reported. |
| Mo1 | Negative control wording | YES | "no clear association", both CIs, 10-20% residual bias statement; Table S2 HE4 "Cluster CI yes; MH CI no". |
| Mo2 | 2020 artefact, Q ignoring clustering, "21 months" | YES, with residuals | 2020 dropped from abstract and flagged as truncated; cluster-aware Q = 12.7, p = 0.005 (my R6 value 14.6 differs only by bootstrap noise; both fine). "At least 25 months" is 24.8 (E_results7 A23 min_followup_months_A11 = 24.77): say "about 25". |
| Mo3 | Meta-analysis design | MOSTLY | Robins SE, common correction, t-PI, HK, >= 3 exposed events done; "probably" -> "possibly". New artefact introduced by the common 0.5 correction (F5). |
| Mo4 | Bootstrap B, intervals | PARTLY | A1 now B = 2,000; X3 sentence fixed; PPV described as lower bound. Method and Table 2 text about B is wrong (F4); Cox "cause-specific" claim has no repository code (F9); percentile intervals retained. |
| Mo5 | Imprints omitted | YES | Table 3 rows and text. |
| Mo6 | "weak", "graded", "robust", "specific" wording | YES | Wording now matches evidence. |
| Mo7 | Prior art | NO | Google Scholar still absent from the list of unsearched sources; the "publishers that screen by turnaround" claim is still uncited; [5] still cited for PLOS ONE; four preprint/blog references still carry the design argument (F12). |
| Mo8 | Pre-specification description | NO | Abstract: "The protocol predated the analysis"; Strengths: "a protocol that predates the analysis" (F3). |

R6 minor items: C1 (107 vs 113 events) not explained; C2 (5,625 vs 4,668 strata) unchanged; C3 ("no exclusion depended on retraction status": the title rule removes 70 of 3,524 = 2.0% of retracted vs 0.57% of others, Table 1) unchanged; C4 fixed (Fig. 4b now takes the primary from A1, e_figures.py line 47); C5 not fixed (checklist dated before E-A7: still says "Crossref records 2020-2026", "coverage and unmatched counts in Table 1"); C8 placeholders and AI-named branch remain (acceptable at this stage, listed in section 6); C9, C10, C11 fixed.

---

## 2. Number verification (abstract and Results against result files)

Legend: OK = matches the file to the printed precision; the file is named in the right column.

| # | Manuscript value | Source value | Verdict |
|---|---|---|---|
| 1 | 1,803,587 articles, 800 journals, 3,454 retracted, 2,639 process | E_build_summary n_articles, n_journals, n_retracted, n_process | OK |
| 2 | 111 journal-years, 71 journals, 66,969 articles, 2,560 events | E_results A1 joint_fe_logit n_strata 111, n_clusters 71, n_rows 66,969, n_events 2,560 | OK |
| 3 | Table 2: 377/95,230, MH OR 4.19, cluster 2.07-7.07, MH 3.65-4.80; any 3.11 (1.63-4.88) | E_results A1 | OK |
| 4 | Table 2: slowest 15/91,477, 0.10 (0.04-0.23; 0.06-0.17); any 0.35 (0.20-0.65) | A1 X2 | OK |
| 5 | Table 2: <= 7 days 53/27,030, 1.09 (0.00-2.56; 0.78-1.53); any 1.22 (0.59-2.39) | A1 X3 | OK |
| 6 | Table 2: batch >= 5 1,964/719,977 1.67 (1.30-2.05; 1.49-1.88), any 1.48 (1.17-1.74); batch >= 10 1,176/265,786 1.96 (1.58-2.67; 1.76-2.18), any 1.76 (1.42-2.12) | A1 X4, X4b | OK |
| 7 | Weekend acceptance 505/296,962 1.14 (0.81-1.71; 1.03-1.28), any 1.11 (0.84-1.50); negative control 464/310,140 0.88 (0.70-1.17; 0.78-0.98), any 0.91 | A1 X5, N1 | OK |
| 8 | Joint FE logistic 3.9 (2.4-6.2) and 2.7 (1.7-4.2); Holm p < 0.001 | A1 joint (3.85, 2.69), primary_holm 9e-8, 9e-6 | OK |
| 9 | Cox HR 3.2 (1.5-4.5), 2,560 events, median follow-up 4.5 years | E_results5 hr 3.159, ci_boot 1.53-4.55, 1,650 days | OK |
| 10 | Dose-response 5.5, 6.1, 0.07 (90th-95th); slowest 5% 0.10 | A2 bins 0, 1, 18 (5.48, 6.07, 0.074) | OK |
| 11 | Negative control in cycle-1 cohort 1.09 | E_results_v1cohort N1 1.085 | OK |
| 12 | Reason subtypes 4.0, 7.0, 3.9, 3.1, other 1.06 (0.73-1.45) | E_results2 A8 | OK |
| 13 | Publisher-investigated other: 380 events, 23 exposed, OR 1.13; ratio 3.7 (1.6-8.1) | E_results7 A21 | OK |
| 14 | Label-free: 107 events, OR 4.0 (1.2-9.5), 21 exposed; third party 3.8 (0.8-5.8) | E_results6 A15 | OK |
| 15 | Table 3: Cox 3.2; quarter 3.6 (1.9-6.0); month 3.3 (1.8-5.1); 24-month 310, 4.5 (1.8-8.6); non-retracted threshold 735, 6.9 (2.5-12.9); strict 4.1; tie-break 4.3; mass-event removal 60, 3.2 (1.8-4.9); R_ai removal 212, 3.2 (2.0-5.6); label-free 21, 4.0 | A17, A11, A22, A4, A15 | OK |
| 16 | Table 3: remove 1/5/10/20 journals 3.8/2.8/3.9/6.4, 39 exposed after 20 | A12 excl_top | OK |
| 17 | Table 3: coverage >= 80% (52 j) 139, 4.7 (0.8-12.1); < 50% 93, 3.6 (2.0-6.4) | A20 sens | OK |
| 18 | Table 3: dated >= 90% 290, 6.1 (3.0-9.9); < 90% 87, 2.0 (0.9-4.5) | A20 sens | OK (but see F2: sister rows omitted) |
| 19 | Table 3: Springer Nature 203, 6.7 (3.0-12.7); Wiley 174, 2.8 (1.1-5.0); imprints Springer 197 6.7; Wiley 22 4.6 (1.4-13.2); BMC 6 7.8 (1.8-30.6); Blackwell 24 0.9 (0.0-1.6); other 128 4.2 (0.2-6.3); cycle-1 267, 4.4 (2.1-8.2) | A4, v1cohort | OK |
| 20 | 10,163 same-day records, 2 retracted; 5.4% flagged | E_build_summary; A22 flagged_share_primary 0.0538 | OK |
| 21 | Cohort: 113 without label; 14,239 notices (5,606 / 8,241 / 403) | E_build_summary n_nopub; A20 | OK |
| 22 | Cohort retractions by publisher "1,624, 1,810 and 24" | E_build_summary and E_tables: Springer Nature 1,620 (A20 by_member 1,624 is a merge artefact) | **WRONG** (F6); 1,624 + 1,810 + 24 = 3,458, not 3,454 |
| 23 | Table 1 rows "1,956,720" and "1,840,163" | Unique-ISSN sums: 1,945,453 and 1,829,907 (the summary TSV has 808 rows, 6 duplicated ISSNs) | **WRONG** (F6) |
| 24 | Rest of Table 1 (1,824,388/3,526; 1,813,858/3,524; ...; 1,803,587/3,454) | E_build_summary flow | OK |
| 25 | 67% of events in five journals, 93% in twenty; 55% of AUC pairs from one journal-year; 1,312 retractions accepted 2021; median lag 17.2 months; 40% batch days | A12, A25, E_build_summary, E_tables | OK |
| 26 | Hindawi-legacy journal "36% of records" dated | A20 top_journals 1687-5273 dated_share 0.364 | OK |
| 27 | Heterogeneity: pooled 3.6 (2.3-5.7), HK 2.2-5.9, I2 87%, PI 0.5-25.5, 90% > 1, 5.4 among 12 journals | A24 (I reproduced pooled 3.629, I2 0.871, PI 0.516-25.53, ee>=3 5.38 exactly) | OK numerically; "90%" see F5 |
| 28 | "journal-specific odds ratios ranged from below 0.2 to above 20" | my reproduction of A24 per-journal ORs: min 0.27 (1600-0846), max 21.1 (1866-7538) | **WRONG** minimum (F5) |
| 29 | Year ORs 5.4, 9.6, 2.1, 0.79; 2024 CI 0.19-2.69, 12 exposed; Q 12.7, 3 df, p 0.005; slope -0.73 (-1.21 to -0.12); ratio 0.24 (0.08-0.81); 2020 on 7 exposed events | A23, A4 by_year | OK |
| 30 | 24-month restriction 7.1, 11.3, 2.2, 0.78; "at least 25 months" | A11 by_year; min follow-up 24.77 | OK; "25" rounds 24.8 up |
| 31 | Journal-month: 20,291 months, 727 journals, 59 journals, OR 2.6 (2.1-3.2) per 10 points; 494 months, 1.8% of articles, 0.98% vs 0.18%, ratio 5.3 (0.4-18.0), 9% of events | A26 | OK numerically; the "9% of all such retractions" is 208 of the 2,325 events in eligible journal-months, i.e. 7.9% of the 2,639 (F1) |
| 32 | Table 4 (all five rows: flagged, events, rate, CI, lift, sensitivity, NNS) and base rate 0.18% | E_results.json A3 screen; E_results6 A18 screen_ci | OK (all rows) |
| 33 | AUC 0.78 (0.65-0.83), 1,341 events, 36 journals; 0.70 without largest; 0.71 equal weight (54 strata); 0.71 2023-24; 0.66 without top five; 0.69 true first-online | A18, A25 | OK |
| 34 | Pooled AUC 2023 0.81 / 0.85; 2024 0.65 / 0.85; history 0.49 / 0.46 | A25 pooled_auc_by_year | OK |
| 35 | tau2 variants 0.78/0.78/0.78 | A25 auc_by_tau2 (0.7817, 0.7816, 0.7814) | OK |
| 36 | 6.8 per 1,000 vs 0.11 per 1,000; 36% of flagged events from one journal; 19% sensitivity at 5%; 16 vs 18 months | A9 bands, A18, A10 | OK |
| 37 | Batch after mass removal 0.93 (0.62-1.25); 3,109 journal-years; rho -0.08 and 0.17 | A4, A5 | OK (rho are for any retraction) |
| 38 | Lag analysis 1,125,461; 0.44 (0.25-1.11); 0.50 (0.17-1.10) | E_results4 | OK |
| 39 | External: 312,602, 122 journals, 150/44 events; 1.34 (0.00-3.76), 3 exposed; any 0.62; batch >= 10 4.7 (1.3-16.9) | E_results2 A7 | OK |
| 40 | Table S1 (dated shares, notices, exposed events, journal ORs) and S2 | A20 top_journals, A24 | OK |
| 41 | "37% of articles have only a month-level issue date instead of a true first-online date" | true_first_online_share 0.634 (36.6%) | OK, but see F8: 63% of process-related retractions lack one |
| 42 | Abstract: "protocol predated the analysis"; "six amendments, five responding to results" (Limitations) | Methods and S3 list E-A1 to E-A7 (seven; six post hoc) | **STALE** (F3) |
| 43 | Table 2 caption "500 resamples, 2,000 for the primary estimate"; Methods "2,000 ... 200-500 for other analyses" | e_analysis.py A1 loop: B = 2,000 for every exposure in Table 2; A21/A23 2,000, A26 1,000, A17/A22 300, A20 500, A2/A4 200, A14 200 | **WRONG** (F4) |

All abstract numbers (about 25 values) were traced and agree with the files, with the exceptions flagged above. I found no transcription error in Tables 2-4.

---

## 3. MAJOR findings

### F1. The journal-month "group-level" result is circular, is carried by a single journal-month, and disappears when the exposure is computed without the retracted articles

- Quoted text. Abstract: "Journal-months with at least 15% fast acceptances (1.8% of articles) held 9% of such retractions"; Abstract conclusion: "may help prioritise groups of articles, such as journal-months, for editorial-office review"; Results: "each 10 percentage points of articles in the fastest 5% were associated with 2.6 times the odds ... rate ratio 5.3 ... contained 9% of all such retractions"; Discussion: "The group-level analysis suggests a more useful framing ... which is the kind of signal editorial offices can use to prioritise a collection or an editor's decisions for review"; Cover letter: "a journal-month analysis suggests that groups of articles are the more useful unit"; Methods: "binomial model with journal fixed effects for the share of articles in the fastest 5%" (this sentence does not even say what the outcome is).
- Why it is circular. The journal-month "fast share" is computed over all articles of the month, including those later retracted, and retracted articles are by the primary result about four times as likely to be in the fastest 5%. A month with many retracted articles therefore has a high fast share by construction, and the month-level association is the article-level association re-aggregated. It cannot be offered as independent support for a group-level screen.
- My recomputation from `e_articles.csv.gz` (same 20,291 journal-months, same 15% rule, same model as `e_analysis7.py`; the authors' numbers are reproduced exactly: 494 months, 21,164 articles, 208 events, 0.983% vs 0.185%, ratio 5.31, OR 2.586 (2.089-3.202)):
  1. One journal-month produces 80% of the events in flagged months: Arabian Journal of Geosciences (1866-7538), July 2021, 337 articles, 166 process-related retractions (49%), fast share 30.9%. The other 493 flagged months contain 42 events in 20,827 articles (0.20%) against 0.185% in unflagged months: rate ratio 1.09, and 1.9% (not 9%) of the events. The percentile interval 0.4-18.0 in the manuscript is the symptom ("includes values near one": it includes 0.4).
  2. Per-10-point odds ratio without that month: 1.92 (1.15-3.21), down from 2.59.
  3. Fast share recomputed from the non-retracted articles only (the legitimate test of whether fast acceptance of other articles in a month predicts later retraction): in that month the share falls from 30.9% to 4.7%; 98 events fall in flagged months (0.47% vs 0.19%, ratio 2.4, 4.2% of events), and the fixed-effects model gives OR 0.97 (0.55-1.72) per 10 points (0.91, 0.49-1.71 without the single month).
  4. 164 of the 494 flagged months are in 2025-2026 (events 0) and 72 in 2022 (events 0): the flag does not identify the months in which retractions happened except in 2021 (179 events in 80 months, 166 of them the one month) and 2023 (22).
- Denominator: 208/2,325 = 8.9% is the share of events in journal-months with at least 30 articles in journals with X1 defined, not "all such retractions" (2,639; 7.9%).
- Fix: either (a) drop the journal-month analysis from the abstract, Discussion, Conclusions and cover letter and report it as a failed attempt (the data show no group-level signal beyond the article-level one), or (b) redo it with the exposure computed from non-retracted (or leave-own-out) articles, report the single-month dependence, a leave-one-journal-out analysis and a bootstrap that resamples journals, and do not use "useful framing" language. Remove "an editor's decisions" (no editor data exist). Rewrite the Methods sentence so that the outcome and the flag rule are stated. Also stop naming the section "Group level" in the abstract as support for the stated use.

### F2. Date-availability selection (R6 M1) is disclosed but not resolved; the coverage index is misleading; two pre-specified sensitivity rows were omitted from Table 3

- Quoted text. Results: "the Crossref count of retraction notices is 14,239 ... against 1,624, 1,810 and 24 retracted articles in the cohort. The notices include articles published before 2021 ... the ratio is a rough index, but most retractions are missing, notably in journals that deposited ... only part of their articles"; Table 3 (coverage rows, dated-share rows); Methods: "no exclusion depended on retraction status".
- Problems:
  1. The index (cohort retractions / all-years Crossref notices) is confounded by vintage. Taylor & Francis shows 24/403 = 6%, yet in Retraction Watch 20 of 22 (91%) of the T&F frame-journal retractions of articles originally published from 2021 are in the cohort: the T&F "shortfall" is old notices, not missing dates (T&F dated share is 97%). The coverage subsets in Table 3 (>= 80%, < 50%) therefore mix two different things.
  2. A better index is available inside the repository: Retraction Watch with `OriginalPaperDate` >= 2021 matched to the 800 journals. By my own title matching (approximate): 7,776 retractions, 3,276 (42%) in the cohort; Springer Nature 96% (1,538 records), Wiley 29% (6,216); by journal dated share, < 50%: 5% of 4,260 retractions in the cohort; 50-90%: 66% (1,135); >= 90%: 96-98% (2,381). The retractions that never entered are 98% peer-review-related, those that entered 79%. So the data lose precisely the outcome of interest, and almost all of it in Wiley / Hindawi-legacy journals with partial dating.
  3. Whether partial dating inside a journal-year depends on retraction status or on speed cannot be tested with the stored data (undated records were discarded); R6 showed that at least three missing JHE articles exist as ordinary Crossref records with an empty `assertion` list. The manuscript neither quantifies this (a sample of missing RW DOIs checked against the Crossref API would do) nor says what the stratified MH estimate needs (missingness non-differential in speed within journal-year).
  4. Selective reporting. The protocol amendment E-A7 promises dated-share sensitivity at >= 90%, < 90% and >= 95%, and coverage >= 80% and >= 50%. Table 3 shows only >= 90%, < 90%, >= 80% and < 50%. The omitted rows (E_results7 A20 sens) are: dated share >= 95% (523 journals) OR 3.1 (cluster 2.06-4.91; 45 exposed events); coverage >= 50% (111 journals) OR 4.4 (1.68-8.86; 284 exposed events). The >= 95% row halves the >= 90% estimate (6.1): the difference is two journals (BioMed Research International 91% dated, Arabian J. Geosciences 93%; together 210 of 377 exposed events). That is the single most informative selection sensitivity and it was left out.
  5. The sentence "no exclusion depended on retraction status" is still literally untrue in effect: the title rule removes 70 of 3,524 retracted (2.0%) against 0.57% of others (Table 1 last row); the D rule removes 2 of 3,526 against 0.58%.
  6. "Journals with at least 80% dated records" (Methods) was applied to 2023 articles; 28 of the 802 frame journals have an all-years dated share below 80% and 9 below 50% (collect_crossref_summary.tsv). Say so.
  7. "The association was present in subsets with high and low coverage" (Limitations): in the >= 80% coverage subset the interval is 0.8-12.1.
- Fix: replace the notice-based index by the Retraction Watch-based one (original date >= 2021, ISSN-level), give it by publisher and by dated-share band in Table 3 or S1, show all six pre-specified A20 rows, check a random sample of 100 missing RW DOIs against the Crossref API and report how many are truly undated, correct the "no exclusion" sentence, and state the MH non-differential-missingness assumption. If the authors want a statement about the cohort's representativeness, say that about 58% of Retraction Watch retractions of 2021+ articles in the frame journals are not in it, concentrated in journals with partial dating.

---

## 4. MODERATE findings

### F3. Pre-specification claims overstate what happened (abstract, Strengths, Methods, cover letter)

- Quoted: Abstract "The protocol predated the analysis; amendments are disclosed."; Strengths "a protocol that predates the analysis"; Methods "Each amendment was written before the analysis it describes was run"; Limitations "six amendments, five of them responding to results"; Cover letter "The protocol was committed before the analysis".
- Source: the protocol (c2139be, 19:40) predates only the first association run; E-A1 was written after the first run and after the MH results were seen ("The Mantel-Haenszel results of the first run ... were seen before the fix"), E-A5b after the first Cox run failed; the analyses that carry the heterogeneity, ascertainment, year, coverage, screening-robustness and group-level claims (A15-A26) are all post hoc (S3), and E-A7 (A20-A25) was written after the reviewer had already reported the same quantities (ratio of ORs 3.94, Q = 14.6, AUC 0.70 without the largest stratum, dated-share ORs 6.1/2.0/3.1; R6 sections A and B). The "before running" statement is formally true, but the analyses were designed to reproduce known numbers and the paper does not say so. There are seven amendments, six of them responding to results (S3); Methods lists E-A1 to E-A7, the Limitations still says six/five. Methods also lists "a negative-control ... analysis" among the post hoc additions, but N1 and HE4 are in the original protocol (E1, E2).
- Fix: Abstract: "The protocol (no external registration) predated the first association analysis; seven amendments, six of them responding to results, are listed." Methods: state that A20-A25 were specified after a reviewer reported the same quantities; delete the negative control from the list of additions; correct the Limitations count.

### F4. Bootstrap description is wrong in Methods and Table 2; the A23 bootstrap discards draws silently

- Quoted: Table 2 caption "journal-cluster bootstrap with 500 resamples, 2,000 for the primary estimate"; Methods "2,000 draws for the primary estimate, 200-500 for other analyses".
- Source: `e_analysis.py` line 55 (commit dcefec1) runs B = 2,000 for every exposure and both outcomes in A1, so every interval in Table 2 uses 2,000. Elsewhere: A21 and A23 2,000; A26 1,000; A17, A22 300; A20 500; A2, A4, A14 200 (not "200-500"). A23 retained 1,996 of 2,000 draws (non-finite draws dropped), not stated.
- Fix: one sentence listing B by analysis (or "2,000 for A1, A21, A23; 200-1,000 otherwise"), the seed protocol, and the number of dropped draws.

### F5. Meta-analysis (A24): stale range statement and continuity-correction artefacts

- Quoted: "journal-specific odds ratios ranged from below 0.2 to above 20 (Figure 4a)"; "90% of the journals had an odds ratio above one".
- Source: with the revised estimator the per-journal ORs run from 0.27 to 21.1 (my reproduction; the list of 20 is not in the JSON). The "below 0.2" is carried over from the old A16 (OR 0.08 for one exposed event). Worse, three of the 20 journals have zero exposed events (1468-0394, 1875-6883, 2398-8835) and seven have at most one; the common 0.5 correction makes the three zero-exposed journals look like ORs of 1.7, 1.9 and 3.4, and they count among the "90% above one" (18 of 20; 15 of the 17 journals with at least one exposed event = 88%). Excluding the three, the pooled OR is 3.89 (2.40-6.30), I2 89%, PI 0.52-29.2. The pooled value is therefore not the problem; the descriptive statements are.
- Fix: "from 0.3 to 21"; state that 7 of 20 journals have at most one exposed event and that the "share above one" is not interpretable for them; report the 12-journal analysis (100% above one) next to it.

### F6. Wrong or inflated counts in Table 1 and in the coverage paragraph (duplicate-row artefact in `e_analysis7.py`)

- Quoted: Table 1 "Crossref journal-article records returned for the 802 frame entries 1,956,720"; "with both received and accepted assertions 1,840,163"; Results "1,624, 1,810 and 24 retracted articles in the cohort".
- Source: `collect_crossref_summary.tsv` has 808 rows for 802 ISSNs (six ISSNs duplicated: 1436-2449, 1618-9558, 1432-0851, 1420-9039, 1432-1106, 2198-7793). `summ.total.sum()` double-counts them: unique sums are 1,945,453 and 1,829,907 (dated share 94.06%, not 94.04%). The same merge duplicated those six journals' articles in `jc`, giving Springer Nature 1,624 cohort retractions in A20 by_member instead of 1,620 (E_build_summary, E_tables); the three numbers printed no longer sum to 3,454. The duplicated journals have no process events, so the MH estimates in A20 sens are unaffected (events 2,560 and exposed events 377 reconcile), but `n` and `exposed` columns in E_results7 A20 sens are inflated (for example 1,641,882 + 138,316 > 1,770,173).
- Fix: `drop_duplicates("issn")` before the merge; regenerate; replace 1,624 by 1,620 and the first two Table 1 numbers.

### F7. The "time-ordered score" adds nothing to raw duration, and the AUC evaluation is on a left-truncated, outcome-selected set (abstract headline)

- Quoted: Abstract "A time-ordered score had a stratified AUC of 0.78 (0.70 without the largest stratum)"; Methods "For prospective screening we computed an out-of-time score"; Background "tests a score out of time"; Limitations "retrospective and time-ordered rather than a prospective test".
- Source and reasoning:
  1. A stratified AUC within journal x acceptance-year is invariant to any monotone transformation of the score within a stratum. The stratified AUC of raw duration is 0.789 (E_results A3 neg_D) against 0.782 for the PIT score, with the same strata. The "time-ordered" reference distribution therefore contributes nothing to the headline AUC; it only matters for pooling across journals, and there the raw duration wins: pooled AUC 0.85 vs 0.81 (2023) and 0.85 vs 0.65 (2024). The manuscript prints these figures but concludes only that the score is modest. The abstract and Background should not suggest that the time-ordered construction is what produces discrimination.
  2. The evaluation set is outcome-selected (54 journal-years with at least one event and one non-event) and left-truncated: a score exists only for articles received on or after 2022-01-01 and in journal-origins with at least 100 visible articles (e_build.py). In acceptance year 2022 only 158,197 of 263,985 articles (60%) have a score; in the largest stratum (2314-6141, 2022, 55% of AUC pairs) 1,472 of 1,962 articles have one and those without have a median duration of 151 days against 66 days. The long-duration comparators are removed from exactly the stratum that dominates the AUC. "Left truncation" is not mentioned anywhere in the manuscript, although the RECORD checklist claims "left truncation discussed".
  3. Methods still says "for prospective screening" and "out-of-time" in the Exposures paragraph and names the evaluation "prospective" in the heading of the analysis plan (A3), while Limitations says it is not. Make them consistent.
  4. The statement that the history baseline scored 0.49 and 0.46 "because retractions are public with a lag of about 17 months" is an untested explanation (alternative: retraction risk is not persistent at journal level because it is episodic).
- Fix: report in the abstract AUC of raw duration next to the score (0.79 vs 0.78 stratified), name the truncation, remove "prospective/out-of-time" wording or demonstrate it with a frozen threshold applied to a later cohort, soften "because".

### F8. Availability of a true first-online date is strongly outcome-associated and is not described as such

- Quoted: Limitations "37% of articles have only a month-level issue date instead of a true first-online date, which affects the visibility rule of the score and the lag analysis, which was restricted to true dates".
- Source (my count): the true first-online share is 63% overall but 47% among retracted and 37% among process-related retracted articles. The lag analysis (L1, L2) rests on 973 of 2,560 process events (38%), and the "journals with at least 80% true first-online dates" AUC variant on 312 of 1,341 events. These are the same journals whose fallback date caused the cycle-1 cohort error. The lag result ("not associated with retraction") and that AUC row are selected on a feature that predicts the outcome.
- Fix: state the 38% and the 37%-vs-63% contrast, and label the lag analysis as not representative.

### F9. Cluster inference and one claim without repository support

- Journal clusters assume independence between journals, but the retraction waves are calendar-time and publisher-level (shared management, shared mills; the manuscript itself says waves cannot be separated from the year decline). With 71 informative clusters, 30% of events in one cluster and 67% in five, percentile bootstrap intervals for a ratio estimator are fragile; the excluding-top-journal ORs range 2.8-6.4. Add a publisher-by-year or two-way bootstrap (or a studentised/BCa interval), report leave-one-journal-out influence for the primary, and state that CIs are conditional on journal independence.
- "retractions for other reasons were not treated as competing events, which changed the estimate in the third decimal" (Results): the only evidence is R6's scratch run (3.153 vs 3.159); nothing in `e_analysis5.py` or `E_results5.json` reproduces it. Add the cause-specific variant to the code or delete the clause.
- The year-heterogeneity Q uses bootstrap variances of each year's log OR as if independent, although the same journals contribute to several years; the covariance is available in the bootstrap matrix `bl` and should be used (a Wald test with the bootstrap covariance of the four log ORs, or a pooled bootstrap of the slope, which is already reported and sufficient).

### F10. Cover letter statements are inaccurate

- "An earlier, different manuscript from the same project ... was rejected by another journal ... the present study addresses a different question with new data." The protocol (line 3) says the earlier paper was rejected by *Research Integrity and Peer Review* itself, and that Part E "re-aims the same data and machinery"; the Crossref dates are the same cohort, only the Retraction Watch outcome is new. "Another journal" is false if the target is RIPR; "new data" is overstated. "a journal-month analysis suggests that groups of articles are the more useful unit" is unsupported (F1). The cover letter also still says the protocol "was committed before the analysis" (F3).
- Fix: disclose the earlier RIPR decision and the shared data plainly.

### F11. Residual circularity statement missing from the abstract's conclusion; conclusions slightly beyond the data

- Abstract conclusion says "mainly in 2021-2022 and in a limited number of journals" and nothing about ascertainment, although the Conclusions section says "could not be separated from possible publisher-led ascertainment". Add one clause to the abstract.
- "concentrated ... in a limited number of journals" (Conclusions) conflicts with "Removal of the journals with most events did not remove the association" (OR 6.4 without the top 20, 39 exposed events). The *events* are concentrated; the association is heterogeneous (I2 87%) but not confined to few journals. Reword.
- The label-free estimate (21 exposed events) and the pubother ratio (23 exposed events) carry the specificity claim; the abstract reports 1.1 without the 23.

### F12. References and prior art (R6 Mo7 not addressed)

- Discussion: "extends to individual articles the editor-level and special-issue-level observations made for Hindawi and PLOS ONE [5]": [5] (Bishop) concerns Hindawi; PLOS ONE is [10], which the Background describes as calling short turnaround "a less robust marker". The sentence claims agreement with a source the paper elsewhere says disagrees.
- Background: "median review times ... [14, 15]": [15] (Horbach) is about speed of publication, not retractions.
- "Studies in this journal have mapped retraction reasons and notices with Retraction Watch data [17, 18, 19]": [18] is about multiple-retraction authors in Cochrane reviews and [19] about notice type and citations; neither maps reasons. "machine-learning models of retraction have not used timing features [20]" rests on one study.
- "publishers that screen by turnaround" (Discussion) is uncited; Google Scholar is still absent from the list of unsearched sources; Hartung-Knapp and prediction-interval methods are not cited (only DerSimonian-Laird [31]); [9] lists "2026;10:1737168" with DOI year 2025.
- Four preprint/blog references ([5], [6], [21], [22]) still carry design-precedent and novelty arguments.

---

## 5. MINOR findings

1. Results: "Absolute speed was not informative ... (cluster CI 0.00-2.56, too wide to be informative)": the first clause reads as a null; keep only "the data are uninformative".
2. Results: "journal-years with many very fast articles are often fast-lane or short-item journals": no article-type data exist (Limitations say so); delete or label as conjecture.
3. Results: "113 of the latter did not carry the label" vs "107 ... without the investigation label" (and 1,124 vs 1,054 third party): the difference is X1-defined strata; say it once.
4. Methods: "(5,625 strata)": X1 is defined in 4,668; 111 are informative.
5. Methods: "The primary analysis ... fixed-effects logistic ... journal-clustered sandwich": with 71 clusters use the t-based or small-sample sandwich (immaterial, 2.34-6.33 per R6).
6. Results: "5.4 ... 2021"; "0.79 in 2024" in the abstract without CI or exposed events (12); add "(95% CI 0.2-2.7)".
7. Abstract: "3.3 within journal-months" (the X1 OR with month strata) shares a name with the separate journal-month group analysis; rename "journal-month strata" vs "journal-month level".
8. Discussion: "the ecological association of very fast articles and retraction even has the opposite sign to the within-journal one": the within-journal OR for the same exposure (<= 7 days) is 1.09 (0.00-2.56), not opposite; the comparison mixes X1 and X3.
9. HE3 as pre-specified compares R_other with R_process; the paper reports the ratio against a different comparator (publisher-investigated other). Report both ratios and say the comparator changed.
10. Table 4 and text use "retraction rate" for PPV; the text sentence "an enrichment of 3.8 times" should state the CI (1.5-9.8).
11. HE5 "exceeded 0.55 in every variant": the lower cluster limit of the without-top-five variant is 0.54.
12. Companion tool: `product/turnaround_forecast/audit.py` header says "only about 1 in 200 of the fastest 1% was retracted"; the manuscript says 1 in 147. Update, and consider removing `group_alerts` from the advertised functionality until F1 is resolved.
13. RECORD checklist (not regenerated after E-A7): "Crossref records 2020-2026" (collection used from-pub-date 2021-01-01), "coverage and unmatched counts in Table 1", "left truncation discussed".
14. Declarations: competing interests, funding, contributions, acknowledgements are placeholders; the data statement still contains the instruction "a DOI-bearing deposit ... must be created before submission" and names the AI-labelled branch; the note on journal abbreviation remains at the end.
15. S1 caption: "Counts reflect large retraction episodes after publisher investigations": an assertion, not a result.

---

## 6. Remaining design flaws a statistician would still seize on

1. Journal-month analysis: circular (F1). This is the most likely point at which a statistical reviewer rejects the practical-use claim.
2. Selection on date availability (F2, F8): journal-level availability is proven to be associated with the outcome and with the effect estimate (6.1 vs 2.0 vs 3.1). Within-journal availability is unknown. MH conditions on journal-year but not on availability within it.
3. Time-ordered score: not time-ordered in any way that matters for the headline statistic (F7); outcome-selected strata; left truncation; dominant stratum.
4. Exposure definition uses the outcome: in mass-retraction strata (36% retracted in 2314-6141 2022) the 5th percentile of the stratum is partly set by retracted articles; thresholds from non-retracted articles only double the exposed events (377 to 735) and raise the OR to 6.9. The paper correctly says the primary "attenuates", but a clean exposure would use the journal's previous-year threshold (as the PIT does), and the estimate would differ again. Present the 4.2-6.9 range as the effect size, not 4.2 with a footnote.
5. Cluster bootstraps: journal-level only; 71 clusters; one cluster 30% of events; no crossed cluster for time waves (F9).
6. Many forking paths: 26 analyses, two primary tests, Holm over a pair with p = 9e-8 and 9e-6 is decorative; honest, but the abstract numbers are a selection (for example, "3.3 within journal-months" and "1.1" are favourable; the omitted rows in Table 3 are not).
7. Unretracted problematic articles and publisher-defined labels: acknowledged; the pubother ratio does not remove the label circularity, as stated.

---

## 7. Is it now suitable for submission to a meta-research journal (after human verification)?

Not as it stands, but it is close, and the remaining work is bounded. The core article-level result (fast within journal-year, odds about four times higher for peer-review-related retraction, 2.1-7.1 cluster CI, 3.7-fold higher than for publisher-investigated other retractions, strongly heterogeneous across journals and years, decaying after 2022) is reproducible, honestly hedged and of interest to a research-integrity readership. What prevents submission is: the group-level claim (F1) that the abstract, Discussion, Conclusions and cover letter use to justify the practical use is not supported once the circularity and the single journal-month are removed; the selection problem is still unresolved and one key sensitivity (dated share >= 95%, OR 3.1) is missing from Table 3 (F2); the pre-specification wording is stale/overstated (F3); and several statements are wrong or stale (F4-F6, F10, F12). A named human statistician must also re-run `e_build.py` to `e_analysis7.py` from raw files and sign off the results (this has not happened; the AI-only chain of build, review and rewrite is still the weak point for an AI-sceptical journal). If F1 is removed or redone as described, F2 is repaired with the Retraction Watch-based coverage and all six sensitivity rows are shown, and the stale statements are corrected, I would regard the paper as a legitimate, modest, exploratory descriptive study of a historical episode, suitable for a meta-research journal after human verification. Recommended decision on the present file: major revision (reject if the journal-month claim is retained in the abstract).

### Five most valuable remaining improvements, ranked

1. Redo or delete the journal-month analysis: exposure from non-retracted (or leave-own-out) articles, leave-one-journal-month-out, no "useful framing" sentence in abstract/Discussion/Conclusions/cover letter; correct the "9% of all retractions" denominator (F1).
2. Resolve the cohort selection with the Retraction Watch frame: ISSN-level coverage for articles originally published from 2021, sample-verify missing DOIs against Crossref, show all six A20 sensitivity rows (including dated share >= 95% = 3.1 and coverage >= 50% = 4.4), and correct "no exclusion depended on retraction status" (F2, F6).
3. Make the screening section honest: report raw-duration AUC next to the score (0.79 vs 0.78), disclose left truncation and outcome-selected strata, drop "out-of-time/prospective" or add a genuinely frozen-threshold test on a later cohort, and give the abstract the 0.70/0.66-0.78 range (F7).
4. Strengthen inference: two-way/publisher-level cluster bootstrap or studentised intervals for the primary, leave-one-journal-out influence, bootstrap-covariance test for the year trend, the cause-specific Cox variant in the code, and one sentence per analysis giving B (F4, F5, F9).
5. Correct all stale and overstated text and have a human reproduce the numbers: seven amendments (six post hoc), "predated the first analysis", Table 1 and 1,620, "0.3 to 21", cover letter (earlier RIPR rejection, same data), checklist regeneration, citations ([5]/[10]/[15]/[18]), archived release with DOI, completed declarations (F3, F6, F10, F12).
