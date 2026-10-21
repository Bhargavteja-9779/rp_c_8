# Reinforced research project (cycle 2) — see `submission_readiness_report.md`
Original evidence is preserved unchanged under git tag `v1-original-research-office` and in the repository root (`manuscript/`, `results/`, `review/` …). This folder adds cycle-2 work only; nothing in it overwrites cycle-1 files.

| Path | Contents |
|---|---|
| `audit/` | `project_integrity_report.md`, `rejection_risk_register.md`, `novelty_reassessment.md`, `journal_fit_assessment.md` |
| `literature/` | `updated_literature_matrix.csv`, `competing_work_analysis.md`, `agent_C_prior_art.md` (+ matrix), `verified_references_cycle2.json` |
| `research_design/` | `reinforcement_plan.md`, `revised_experimental_protocol.md`, `reinforcement_deviations.md` |
| `code/` | cycle-2 scripts and `README.md` (they reuse the cycle-1 library in `/code`) |
| `results/` | raw and summary results of cycle-2 experiments (`metrics_cycle2.json` is the source of manuscript numbers). Files named in the prompt's template but **not generated**: `raw_results.csv`, `statistics.json`, `experiment_logs/` (per-journal-origin metric CSVs, e.g. `Y1_panel_metrics.csv`, `cal_meta_metrics.csv`, serve as raw results) |
| `figures/` | cycle-2 figures (v1 figures remain in `/results/figures`) |
| `manuscript/` | `Revised_Manuscript.docx/.pdf`, `Revised_Cover_Letter.docx` |
| `review/` | agent reports (A/I/J, D/E/F, second-round reviewer and reproducibility auditor), `reinforcement_review.md`, `second_adversarial_review.md`, `final_consistency_audit.md` |
| `submission_readiness_report.md` | final decision |
