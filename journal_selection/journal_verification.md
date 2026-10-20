# Journal verification report (STEP 0 / Gate A)

Date of verification: 2026-10-20. Prepared by the Journal-Intelligence pass of the research office (single analyst, sequential passes; no independent human or agent verification occurred).

## 1. Outcome in one paragraph

**No journal could be verified as satisfying the hard constraint (≤ 72 calendar days from submission to final acceptance).**
Of 100 journals/venues whose publisher-deposited `received`/`accepted` dates I could sample (29,873 article records across the three samples, see §3), **none has an observed median submission→acceptance time ≤ 72 days; the fastest has a median of 73.5 days and none has ≥ 50 % of papers accepted within 72 days.** Publisher-reported Elsevier "submission to acceptance" figures that I could read (via a secondary mirror) are 138–207 days. Per the prompt's rules, every journal is therefore classified **TIMELINE UNVERIFIED — DOES NOT SATISFY THE HARD CONSTRAINT**. The constraint has *not* been relaxed. A "best-available" target is nevertheless named in `selected_journal.md` so that the project can proceed; it is explicitly **not** compliant.

## 2. What could and could not be verified

| Item | Status | Evidence / limitation |
|---|---|---|
| Observed submission→acceptance (Springer Nature, BMC, Wiley, T&F, Royal Soc.) | Verified (sampled) | Crossref `assertion` fields `received`, `accepted`; scripts in `scripts/` |
| Observed submission→acceptance (Elsevier-/OUP-/Cell-/Frontiers-published, PubMed-indexed) | Verified (sampled) | PubMed `History` dates (`received`/`accepted`) |
| Cross-source consistency | Checked for *Scientific Reports* only | Crossref median 137 d (n=397) vs PubMed median 132 d (n=385) |
| Official Elsevier "submission to acceptance" | Partly (secondary mirror) | ScienceDirect Insights pages return HTTP 403 to this environment; values read from Peeref mirror and one web-search snippet: ESWA 147 d, KBS 165 d, EAAI 207 d, Energy 163 d, Ecological Informatics 138 d. One mirror entry (*Measurement*) duplicates ESWA's string verbatim and is treated as a data error |
| Elsevier journals not in PubMed (e.g. Alexandria Eng. J., Results in Eng., ESWA) | **Not measurable** here | Elsevier does not deposit `received`/`accepted` in Crossref; ScienceDirect blocked |
| IEEE journals (IEEE Access etc.) | **Not measurable** here | No dates in Crossref; IEEE Xplore not machine-readable here. IEEE J-BHI / IEEE T-MI have no history dates in PubMed |
| JCR quartile / JIF (Clarivate) | **Unverified (no access)** | JCR requires a subscription; only secondary mirrors (Peeref "JCR 2026" categories) could be read. Where a mirror is cited it is labelled secondary. Scopus/SCImago/CiteScore were **not** substituted |
| Current author guidelines of the chosen journal | **Partially verified** | Guide-for-authors page returned HTTP 403; word/structure/APC facts come from DOAJ (API) and web-search snippets and must be re-confirmed by the authors before submission |

## 3. Method of the observed-turnaround study

* Population: research articles with publication date ≥ 2025-07-01 (through the verification date).
* Crossref: up to ~400 most recent records per journal with both `received` and `accepted` assertions (`scripts/sample_turnaround*.py`).
* PubMed: up to 400 records per journal (`journal article`, not `review`) with `PubStatus=received` and `accepted` (`scripts/sample_turnaround_pubmed.py`).
* Statistic: calendar days between `received` and `accepted`. For revised manuscripts `received` is the original submission date as deposited by the publisher.
* **Biases (important):** (i) survivorship — only *accepted* papers are observed, so desk-rejected and rejected papers are invisible; (ii) recency — the sampling window truncates very long reviews, biasing toward shorter times for the most recent months; (iii) special issues/invited papers can shorten times; (iv) a past distribution does not guarantee a future individual outcome. **These data can falsify a claim of "≤ 72 days is typical" but cannot establish a guarantee.**
* Result tables: `journal_turnaround_summary.csv` (100 journals, n ≥ 50). Raw samples: `turnaround_samples*.csv`.

## 4. Key observed numbers (shortest medians)

See `raw/observed_table_top25.md` and `journal_comparison.md`.

| Journal | n | Median (d) | IQR | % ≤ 72 d |
|---|---|---|---|---|
| Frontiers in Artificial Intelligence (PubMed dates) | 400 | 73.5 | 54–110 | 48.2 |
| Frontiers in Neuroinformatics | 56 | 84 | 65–114 | 35.7 |
| **J. King Saud Univ. – Comput. Inf. Sci.** | 399 | **87** | 68–112 | 31.1 |
| Int. J. Medical Informatics | 400 | 90.5 | 56–151 | 36.5 |
| J. Imaging Informatics in Medicine | 399 | 97 | 74–125 | 23.8 |

## 5. Consequence for the project

Because the hard constraint cannot be met by any journal that could be examined, the Director records this as an **open, disclosed Gate-A failure** (not a pass). The project continues with a *best-available, non-compliant* target so the scientific work is not blocked, and the author must decide whether to accept that deviation. If the author insists on a literal ≤72-day guarantee, no honest journal choice exists, since no journal can guarantee it.
