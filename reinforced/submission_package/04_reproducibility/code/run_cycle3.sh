#!/usr/bin/env bash
# Cycle 3 (Part D). Needs data/processed/articles_clean.csv.gz (python3 ../code/src/prepare_data.py) and the cycle 1-2 outputs.
set -euo pipefail
cd "$(dirname "$0")/src"
# python3 collect_pubmed_external.py     # live NCBI E-utilities, several hours; committed output is in data/raw/pubmed_ext
D_CAP=480 python3 d_experiments.py        # primary: cap 480 days, six origins (writes D_summary.json ...)
D_CAP=365 python3 d_experiments.py        # as first run: cap 365 days, nine origins (writes *_cap365.*)
python3 d_sensitivity_cap.py              # exploratory cap sensitivity
python3 d_defaults.py                     # shipped tau2 and noise floor
python3 d_external.py                     # external validation, cap 480 (primary)
D_CAP=365 python3 d_external.py           # external validation, cap 365
python3 d_extras.py                       # post hoc robustness analyses (review R4)
python3 d_figures.py
python3 build_methods_manuscript.py
python3 consistency_check_methods.py
