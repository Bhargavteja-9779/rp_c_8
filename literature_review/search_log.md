# Literature and prior-art search log (reconstructed from the session; machine log `search_log.jsonl` only captured the first Crossref/arXiv/EuropePMC sweeps)
Searches were run with the session's web-search tool (standard/extended modes), Crossref, arXiv and Europe PMC APIs on 2026-10-20/21. No Google Scholar, Web of Science, Scopus or patent database was queried. Full texts were generally not read.

| # | Purpose | Query theme | Outcome |
|---|---|---|---|
| 1 | Candidate #1 novelty | subject-wise vs record-wise CV optimism; ICC and CV | 2026 preprints already cover (arXiv 2607.10634; medRxiv 2026); direction rejected |
| 2 | Candidate #4 novelty | duplicates in tabular benchmarks (OpenML/UCI), contamination, ranking | overlapping public preprint (Zenodo 23119065, 2026-10-03), arXiv 2604.04199, TabReD; direction abandoned |
| 3 | Candidate #2 | conformal prediction under subject shift | crowded 2025–26; rejected |
| 4 | Candidates | prequential code length for tabular model comparison; hidden row-order non-exchangeability; cross-dataset overlap in tabular foundation models | related work found (ICML 2025 TabPFN description length; arXiv 2604.04199; Real-TabPFN/TabPFN-2.5 dedup); not pursued |
| 5 | Final topic novelty | publication delay / submission-to-acceptance large-scale analyses (Crossref/PubMed, heavy tails) | Björk & Solomon 2013, Himmelstein blog, Andersen 2021, ophthalmology/accounting/health-policy studies, MetaROR research plan 2026 |
| 6 | Final topic novelty | predictability / forecasting of journal turnaround; reliability of reported medians | none found; Bilalli 2021 (reported vs computed averages); health-policy RPT reporting study 2025 |
| 7 | Citation verification | title look-ups in Crossref for each cited paper; DOIs checked for 49 references (two guessed DOIs were wrong and corrected: Engelen 2021 [not cited], Lones 2024 [not cited]) | `verified_references_crossref*.json` |
| 8 | Journal scope | Crossref title/venue checks of recent *Accountability in Research* and *RIPR* articles | `journal_fit_audit.md` |
Limitations: the search was not systematic (no protocol, no screening log); absence-of-prior-work claims are therefore stated as "did not find".
