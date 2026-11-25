# HANDOFF: how to continue this project in a new account or session

Repository: https://github.com/Bhargavteja-9779/rp_c_8, branch `claude/autonomous-research-institute-nz8co5` (everything is committed there; no pull request was opened). Local state in a cloud session is lost when the container is reclaimed, so **always work from the repository**.

## What the project is (four cycles)
1. **Cycle 1** (`journal_selection/`, `literature_review/`, `research_design/`, `code/`, `results/`, `manuscript/`, `review/`): original study of out-of-time forecasting of journal time to acceptance. Tag `v1-original-research-office`.
2. **Cycle 2** (`reinforced/`): forensic audit, 21-item rejection-risk register, corrective experiments X/Y/Z, `Revised_Manuscript`.
3. **Cycle 3** (`reinforced/` Part D, `product/`, `submission/`): the calibrated forecaster CV0, external validation, the Python package and browser tool; manuscript `Methods_Manuscript` — **rejected by *Research Integrity and Peer Review* (2026-11-24)**: "novelty and potential impact too low", "substantial use of generative AI".
4. **Cycle 4** (`reinforced/` Part E): new study re-aimed at research integrity: editorial timing and later retraction (Retraction Watch data). Protocol `reinforced/research_design/cycle4_protocol_partE.md`; code `reinforced/code/src/e_*.py`; results `reinforced/results/E_*.json`; manuscript in `reinforced/manuscript/`.

## Rebuild the working environment (about 10 minutes)
```
git clone https://github.com/Bhargavteja-9779/rp_c_8.git && cd rp_c_8 && git checkout claude/autonomous-research-institute-nz8co5
pip install -r code/requirements.txt statsmodels
python3 code/src/prepare_data.py          # rebuilds data/processed/articles_clean.csv.gz from the committed raw Crossref files (sha256 matches results/data_manifest.json)
python3 reinforced/code/src/e_build.py    # Part E dataset (needs data/raw/retraction_watch/retraction_watch.csv.gz, committed)
python3 reinforced/code/src/e_analysis.py && python3 reinforced/code/src/e_analysis2.py && python3 reinforced/code/src/e_analysis3.py
python3 reinforced/code/src/e_figures.py
```
Paths in scripts are absolute (`/home/user/rp_c_8`); edit `ROOT` or clone to that path. `data/processed/` is git-ignored because it is regenerable (about 190 MB).

## What is NOT in the repository
* Live-API collections can drift if re-run (Crossref, PubMed); the committed raw files are the frozen record.
* Nothing secret; no credentials were used.
* The author-side fields (competing interests, funding, contributions, ORCID, data DOI) must be completed by the human authors.

## Honest status and what a human must do
* All analysis code, drafts and reviews were produced by AI instances (Claude) with automated reviews and audits; **no human has reviewed the work**. A journal rejected the cycle-3 paper partly for this. Before any submission the human authors must re-run the pipeline, check the key numbers, understand and be able to defend every analysis, rewrite the text in their own words, and disclose the AI use as the target journal's policy requires. Acceptance cannot be guaranteed.
* Venue: `reinforced/audit/journal_fit_assessment.md` lists candidates; submission-to-acceptance times for most are unverifiable.

## Cycle 4 status (2026-11-25)
* Main manuscript to work on: `reinforced/manuscript/Integrity_Manuscript.docx` (+ supplement, cover letter, RECORD/STROBE checklist). Protocol: `reinforced/research_design/cycle4_protocol_partE.md`. Code: `reinforced/code/src/e_build.py`, `e_analysis.py` … `e_analysis7.py`, `e_figures.py`, `build_integrity_manuscript.py`, `build_integrity_cover_letter.py`, `build_record_checklist.py`, `verify_headline_numbers.py`. Results: `reinforced/results/E_*.json` (the `*_v1cohort.json` files are the superseded first cohort). Reviews: `reinforced/review/agent_R5…R8_*.md`.
* Additional raw data: `data/raw/retraction_watch/retraction_watch.csv.gz` (snapshot 2026-11-24), `data/raw/coverage_notices.csv`, `data/raw/pubmed_ext/`.
* Order to run: prepare_data.py → e_build.py → e_analysis.py, e_analysis2.py, e_analysis3.py, e_analysis4.py, e_analysis6.py, e_analysis7.py, (e_analysis5.py, ~10 min), e_tables.py → e_figures.py → build_integrity_manuscript.py. `e_cover_collect.py` needs the live Crossref API.
* Read `reinforced/AUTHOR_GUIDE.md` first. Rejected submission on record: RIPR, 2026-11-24 (cycle-3 manuscript).
