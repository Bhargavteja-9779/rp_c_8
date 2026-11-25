# Cycle-2 code (reinforced/code/src)
These scripts import the cycle-1 library `tdelay` from `/home/user/rp_c_8/code/src` and read cycle-1 data/results; paths are absolute (`ROOT=/home/user/rp_c_8`) — edit `ROOT` to run elsewhere. Run order and dependencies:
0. Prerequisite: `data/processed/` is gitignored. Build it first with `python3 /home/user/rp_c_8/code/src/prepare_data.py` (about 2 minutes; reproduces the SHA-256 in `results/data_manifest.json`). Cycle-1 outputs used as inputs are committed; regenerating them needs `code/run_all.py` and `code/src/revision_analyses.py`. Python/library versions: `code/requirements.txt`.
1. `forensics.py` (Phase 1 checks) — needs `data/processed/articles_clean.csv.gz`, `results/metrics_journal_origin.csv`.
2. `cal_and_meta.py` (X2 look-ahead recalibration F9, X3 learned forecaster F10) — writes `reinforced/results/cal_meta_*`.
3. `dependence_quality_calibration.py` (X4, X5, X6) — needs `results/revision_R1_metrics_4origins_EXPLORATORY.csv`; writes `X5_flagged_journals.json`.
4. `probe_preprint_dates.py` (X1; ~30 min, live Crossref; **do not rerun casually: it overwrites the committed partial file `preprint_probe.csv.partial`, and live results drift**) then `x1_analysis.py` (needs `X5_flagged_journals.json`).
5. `y0_imprint_inference.py` (writes `journal_imprint_map.csv`), then `y1_rolling_panel.py`, `y2_null_and_simulation.py`, `y3_type_robustness.py` (~7 min), `y4_y5.py`.
6. `z_experiments.py` (Z1–Z6; ~5 min; needs `journal_imprint_map.csv`, cycle-1 `results/drift_pairs.csv`, `variance_components.json`).
7. `cycle2_metrics_and_figures.py` (collects `metrics_cycle2.json`, draws cycle-2 figures; needs `Z_summary.json`, `X1_summary.json`), then `build_revised_manuscript.py` and `consistency_check.py` (writes `review/final_consistency_audit.md`). The PDF is made manually with LibreOffice (`soffice --headless --convert-to pdf`).
Paths: `ROOT=/home/user/rp_c_8` is hard-coded in every cycle-2 script (known limitation); edit it to run elsewhere.
Seeds: `seed` from `code/configs/config.json`. See `../research_design/revised_experimental_protocol.md` for specification and order of events.
