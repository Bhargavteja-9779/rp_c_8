# tdelay — out-of-time forecasting of journal submission-to-acceptance times

Code for the study "How well do a journal's past turnaround times predict the next paper's?".

## Quick check (synthetic data, ~20 s; NOT evidence)
    pip install -r requirements.txt
    python -m pytest -q tests          # 10 unit tests (scoring, visibility/leakage assertions, calibration, variance-component recovery, cleaning)
    python run_all.py --mode quick     # runs every experiment on synthetic journals -> ../results_quick_primary (git-ignored)

## Full run (real data)
Requires `data/processed/articles_clean.csv.gz` (build with `src/prepare_data.py` from `data/raw/crossref/`, which `src/collect_crossref.py` downloads from the Crossref REST API for the 802-journal frame in `data/raw/frame_eligible.json`).
    python run_all.py --mode full      # confirmatory analysis, ~7 min on 4 cores -> ../results/
See `run_pipeline.sh` for the complete sequence including sensitivity analyses, external validation (PubMed), tables and manuscript.

## Layout
- `src/tdelay/` library: `data.py` (parsing, cleaning), `protocol.py` (visibility rule + leakage assertions), `forecasters.py` (F0–F6), `scoring.py`, `stats.py`, `variance.py`, `experiments.py` (E1–E7), `synth.py` (synthetic data for tests only)
- `src/*.py` collection, preparation, external validation, ablation, tables, manuscript builders
- `configs/config.json` frozen protocol parameters; `tests/` unit tests; `archive_abandoned_direction/` scripts of abandoned work (kept for audit)

## Reproducibility notes
- Seeds fixed (`seed` in config); two consecutive full runs produced byte-identical CSV/JSON outputs.
- Live API data change over time (late-deposited metadata); `results/data_manifest.json` records SHA-256 of the cleaned files used in the paper and the collection date.
- Hardware: CPU only; Python 3.13.
