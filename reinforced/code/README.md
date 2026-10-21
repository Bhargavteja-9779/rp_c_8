# Cycle-2 code (reinforced/code/src)
These scripts import the cycle-1 library `tdelay` from `/home/user/rp_c_8/code/src` and read cycle-1 data/results; paths are absolute (`ROOT=/home/user/rp_c_8`) — edit `ROOT` to run elsewhere. Run order and dependencies:
1. `forensics.py` (Phase 1 checks) — needs `data/processed/articles_clean.csv.gz`, `results/metrics_journal_origin.csv`.
2. `cal_and_meta.py` (X2 recalibration F9, X3 learned forecaster F10) — writes `reinforced/results/cal_meta_*`.
3. `probe_preprint_dates.py` (X1; ~30 min, Crossref API; the committed result is a **partial** file `preprint_probe.csv.partial` because a worker restart interrupted it) then `x1_analysis.py`.
4. `dependence_quality_calibration.py` (X4, X5, X6) — needs `results/revision_R1_metrics_4origins_EXPLORATORY.csv` from cycle-1 `code/src/revision_analyses.py`.
5. `y0_imprint_inference.py` (writes `journal_imprint_map.csv`, needed by y1, y4_y5), `y1_rolling_panel.py`, `y2_null_and_simulation.py`, `y3_type_robustness.py` (~15 min), `y4_y5.py`.
6. `cycle2_metrics_and_figures.py` (collects `metrics_cycle2.json`, draws cycle-2 figures) then `build_revised_manuscript.py`.
Seeds: `seed` from `code/configs/config.json`. See `../research_design/revised_experimental_protocol.md` for specification and order of events.
