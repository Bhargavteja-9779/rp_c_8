#!/usr/bin/env bash
# Cycle-2 pipeline. Requires the cycle-1 processed data (data/processed/articles_clean.csv.gz, gitignored) and cycle-1 results. Paths are absolute (/home/user/rp_c_8).
set -euo pipefail
cd "$(dirname "$0")/src"
python3 forensics.py
python3 cal_and_meta.py
# probe_preprint_dates.py queries Crossref (~30 min, network); the committed result is partial. Uncomment to recollect:
# python3 probe_preprint_dates.py
python3 x1_analysis.py
python3 dependence_quality_calibration.py
python3 y0_imprint_inference.py
python3 y1_rolling_panel.py
python3 y2_null_and_simulation.py
python3 y3_type_robustness.py
python3 y4_y5.py
python3 z_experiments.py
python3 cycle2_metrics_and_figures.py
python3 build_revised_manuscript.py
python3 consistency_check.py
