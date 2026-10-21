#!/usr/bin/env bash
# Full reproduction pipeline (see README.md). Steps 1-3 need internet; with a data snapshot in data/raw/ start at step 4.
set -euo pipefail
cd "$(dirname "$0")"
# 1. journal frame (Crossref members facets) -- the checked-in data/raw/frame_eligible.json is the frame used in the paper; skip to reuse it
#    python src/build_frame.py
# 2. download article dates (Crossref ~1-2 h; PubMed ~30 min)
#    python src/collect_crossref.py ; python src/collect_pubmed.py
# 3. clean
python src/prepare_data.py
# 4. unit tests, then the confirmatory analysis (~7 min on 4 cores) and variants
python -m pytest -q tests
python run_all.py --mode full
python run_all.py --mode full --variant noC5
python run_all.py --mode full --variant min60_30
python src/run_external.py
python src/run_ablation.py
python src/summarize_sensitivity.py
python src/shape_diagnostics.py
python src/post_hoc_analyses.py        # D6 (exploratory)
python src/oracle_diagnostic.py        # D7 (exploratory)
python src/revision_analyses.py        # D10 (exploratory)
# 5. tables, schematic, manuscript
python src/make_tables.py
python src/make_protocol_figure.py
python src/build_manuscript.py
