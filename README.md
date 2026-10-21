# Autonomous research-office project: out-of-time predictability of journal turnaround

Status: **NOT READY FOR SUBMISSION — see `review/final_audit.md`** (readiness decision and unresolved items).

| Folder | Contents |
|---|---|
| `journal_selection/` | Journal landscape (100 journals sampled with publisher-deposited dates), verification report, comparison, selected (best-available, non-compliant) journal, journal-fit audit |
| `literature_review/` | literature matrix (evidence level per item), novelty map, research-gap chain, reference verification |
| `research_design/` | candidate directions, abandoned directions, research questions, hypotheses, pre-registered protocol, leakage audit, deviations log |
| `code/` | `tdelay` package, tests, entry point `run_all.py`, pipeline script, README |
| `results/` | metrics, statistics, figures, sensitivity, external validation, `metrics.json` (source of every manuscript number) |
| `tables/`, `figures/` | manuscript tables and schematic |
| `manuscript/` | `Final_Manuscript.docx/.pdf`, `cover_letter.docx` |
| `review/` | ten adversarial review passes, independent-agent reviews, review-response ledger, claim–evidence matrix, consistency, reproducibility and rejection-risk reports |

Honesty notes: the hard 72-day constraint could not be met by any scope-appropriate journal; JCR quartiles were not verifiable (no Clarivate access); the journal's current author guidelines could not be retrieved; reviews labelled "simulated" were produced by the same system in separate passes, "independent agent" reviews were produced by separately launched agents (still the same underlying model family); no human expert has reviewed the work.
