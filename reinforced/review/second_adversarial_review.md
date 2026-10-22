# Second adversarial round: findings, fixes and revalidation

Reviewer of record: `agent_R2_adversarial.md` (separately launched instance of the same model family, ten passes, 22 findings R2-01…R2-22; not a human and not independent of the authors' model family). A third check of the rewritten text by another instance is in `agent_R3_final_check.md`. The corrective experiments Z1–Z6 were specified (protocol Part C) before running.

## Disposition of the R2 findings

| R2 finding | Severity | Response | Evidence | Status |
|---|---|---|---|---|
| 01, 06, 11 Cause of shortfall nearly tautological; Y2 null circular; SD benchmark wrong | MAJOR/CRITICAL | Z1: generative null with random cohort shifts at σ² = journal×year variance (also σ²/2, 2σ², oracle, journal proxy); Z5 backward oracle | σ²/2 −2.8, σ² −4.9, oracle −1.6 vs observed −3.0 / −1.5; observed journal and imprint spread not reproduced; σ² is estimated from the same data | **Partly resolved**: magnitude explained, mechanism not identified; text says so |
| 02 Headline skill vs F2 is mechanical | MODERATE | F2 labelled deliberately weak, non-published baseline | text | Partly resolved (no field-pooled or published-statistic baseline built) |
| 03 Reporting-integrity framing lacks evidence | MODERATE | vendor page and Royle cited as non-peer-reviewed; framing narrowed to "reporting of statistics" | text | Partly resolved |
| 04 No integrity/peer-review variable (F for RIPR) | FATAL for venue | cannot be fixed by analysis | `audit/journal_fit_assessment.md` | **Open** |
| 05 Dianovics status misdescribed | MODERATE | wording corrected (evaluated at MetaROR April 2026; no results found) | text | Resolved |
| 07 Recalibration labels looked ahead; 2025 target censored | MAJOR | Z2 strict rule (complete-at-origin cohorts, 480-day cap, 3 origins); X2/X6 demoted and labelled look-ahead variant | R +1.9, V +1.05, F4 +1.3 vs F0 −1.9; remedy not supported | **Resolved** (negative result) |
| 08 Forward frame selection | MODERATE | Z5 pre-origin-only eligibility | −3.1 vs −3.0 | Resolved |
| 09 Time-ordering / "no trend" | MODERATE | Z6 moving-block bootstrap; U-shape described | pooled −2.4 [−2.9, −1.8]; lag-1 0.76 | Resolved |
| 10 Imprint-cluster inference anti-conservative | MAJOR | Z3 t(6) CIs, publisher-level checks, Holm | only F0−F2 and shortfall robust | **Resolved** |
| 12, 19 Multiplicity; "3 vs 4 of 6" | MODERATE | Holm in Table 2; X6 sentence replaced by strict slopes with CIs | tables regenerated | Resolved |
| 13 X1 inference overstated | MAJOR | Z4 journal-weighted and by-year deltas; criterion labelled failed | 82 % / 8.9 %; offset −7…−22 d by year; 14-day resolution | Resolved (disclosed; still one publisher) |
| 14 "Supported" for exploratory/post-hoc items | MODERATE | Table 5 relabelled; H1–H5 confirmatory, H6–H7 exploratory | table | Resolved |
| 15 Fast-end claim (n = 23, winner's curse) | MODERATE | removed as a finding; reliability slope with CI instead | text | Resolved |
| 16 L under-trained | MODERATE | disclosed in Table 5 and Limitations; not re-run | text | Partly resolved |
| 17 Methods omit 2025 origin / journal sets | MINOR | look-ahead variant described and demoted; panel and Z2 origins/eligibility defined in Methods | text | Resolved |
| 18 Generalisation | MAJOR | limitations; abstract states three publishers | text | Open (inherent) |
| 20 Backward oracle had no script | MINOR | Z5 script and result | `Z_summary.json` | Resolved |
| 21 Wrong docstring; no run script; no manifest hash for partial probe | MINOR | `run_cycle2.sh`, deviations C2-9…C2-12; docstring problem disclosed in Methods and protocol | files | Partly resolved (no DOI, no probe hash) |
| 22 Normative AI sentence; cover letter wording | MINOR | reworded | text | Resolved |

## Revalidation after the rewrite

- `final_consistency_audit.md`: 26 headline quantities re-derived from result files and found in the manuscript; no unresolved markers; 29/29 references cited.
- Abstract 348 words (limit 350); main text about 5,000 words.
- Independent reproducibility audit: `agent_R2_reproducibility.md`.

## Residual rejection risk (judgement, not computed)

- Desk rejection at RIPR on scope: more likely than not.
- At a scientometrics journal: major revision likely; points would be the unidentified mechanism, the three-publisher frame, validation of dates beyond Springer Nature, and incremental novelty.
- Fatal scientific flaws: none identified by the reviewers; the review set contains no human.
