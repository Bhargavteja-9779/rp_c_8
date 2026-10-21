# Final audit, rejection-risk report and readiness decision (2026-10-21)

## READINESS DECISION: **NOT READY — ADDITIONAL WORK REQUIRED**

Reasons (each is a hard blocker or a disclosed unresolved item):
1. **Hard journal constraint unmet.** No scope-appropriate journal could be verified at ≤ 72 days submission-to-acceptance; the target (*Accountability in Research*) is best-available only (observed median 105 d; 27 % ≤ 72 d). JCR quartile/JIF **unverified** (no Clarivate access). Current author guidelines **not retrieved**.
2. **No public data/code deposit** (no DOI). Raw snapshot is committed to the project repository (if the push succeeded; see README) but the manuscript's data-availability statement cannot be finalised until a persistent public archive exists.
3. **Author-specific items are placeholders** (names, affiliations, contributions, funding, COI, originality confirmations, ethics confirmation).
4. **No human or external expert review.** The ten review passes are same-system simulations; two further reviews (agents A and B) were separately launched model agents — not independent humans.
5. **Novelty is moderate and unverified at full-text level** (abstract/snippet-level reading of the closest prior work; non-systematic search). An editor may judge the paper descriptive/incremental.

No FATAL scientific flaw was identified by any pass after revisions; the quantitative results re-run byte-identically from the shipped processed data and independent code reproduced the F0 forecasts for all 1,531 journal-origins.

## Quality gates
| Gate | Status | Note |
|---|---|---|
| A Journal feasibility | **FAIL (disclosed)** | 72-d constraint unmet for scope-appropriate journals; quartile unverified |
| B Research opportunity | Pass (moderate) | gap chain in `research_gap.md` |
| C Novelty | Conditional pass | absence claims hedged; first topic abandoned at this gate |
| D Experimental feasibility | Pass | executed |
| E Methodological validity | Pass with caveats | `received` semantics, frame, accepted-only |
| F Evidence | Pass | experiments executed; 4 of 5 confirmatory hypotheses not supported |
| G Statistical validity | Pass | clustered CIs, Holm; exploratory items labelled |
| H Independent review | Partial | simulated + 2 agent reviews; all MAJOR items addressed or disclosed (ledger) |
| I Reproducibility | Partial | code/results reproducible from processed data; raw data via API drift; no DOI |
| J Submission readiness | **FAIL** | blockers above |

## Rejection-risk report (severity of residual risk after corrections)
| # | Risk | Evidence | Severity | Fixed? | Further experiments? | Residual |
|---|---|---|---|---|---|---|
| 1 | Journal-scope mismatch | scope text unverified; ethics/integrity venue | Medium | Framed as meta-research | No | Medium |
| 2 | Insufficient novelty | closest work descriptive; novelty map | **High** | Hedged claims | Read full texts; systematic search | High |
| 3 | Insufficient significance | modest effects, partly negative | Medium | Honest framing | No | Medium |
| 4 | Weak gap justification | gap chain; absence claim | Medium | Hedged | Systematic search | Medium |
| 5 | Methodological weaknesses | dependence of origins, accepted-only | Medium | Cluster CIs, limitations | More origins done (exploratory) | Medium |
| 6 | Dataset limitations | 3 publishers, size window, `received` semantics | **High** | Disclosed; sensitivity | Verify dates vs publisher pages (blocked) | High |
| 7 | Data leakage | visibility rule, tests, oracle diagnostic | Low | Yes | No | Low |
| 8 | Weak baselines | simple baselines only | Medium | F7/F8 added; limitation | Richer meta-model forecasters | Medium |
| 9 | Statistical uncertainty | CIs; H2 borderline | Low-Med | Yes | No | Low |
| 10 | Insufficient robustness | variants, 4 origins, external | Low-Med | Yes | More publishers | Medium |
| 11 | Limited generalisation | frame limits | Medium | Stated | Elsevier/IEEE data if obtainable | Medium |
| 12 | Incomplete experiments | all protocol experiments run; E8 independent verification blocked | Low-Med | Disclosed | – | Low-Med |
| 13 | Computational feasibility | 7 min | Low | – | – | Low |
| 14 | Reproducibility | raw data not archived with DOI | **High** | Raw committed; manifest | Zenodo deposit | Medium |
| 15 | Citation accuracy | 26 DOIs verified; abstract-level reading | Medium | Verified metadata | Read full texts | Medium |
| 16 | Manuscript clarity | dense Methods; 15 pp | Low-Med | – | Plain-language summary | Low-Med |
| 17 | Author-guideline compliance | guidelines not retrieved | **High** | – | Authors read instructions | High |
| 18 | Ethics/integrity compliance | placeholders; AI-use disclosure included | Medium | Disclosure drafted | Author confirmation | Medium |
| 19 | Timeline uncertainty | ≤72 d unsupported (27 % of published papers) | **High** | Disclosed | None possible | High |
| 20 | Remaining technical limitations | `received` semantics, truncation, unexplained residual drift | Medium | Disclosed | – | Medium |

No zero-risk claim and no acceptance prediction is made.

## What was actually executed (vs. proposed)
* Executed: journal date sampling (Crossref/PubMed; 29,873 + 5,646-record screens), frame construction and download (1.83 M records, 802 entries), cleaning, the full protocol (E1–E7), external checks (E8, E9), sensitivity variants, post-hoc diagnostics (D6, D7, D10), unit tests (10), manuscript/cover-letter generation, DOCX→PDF conversion and visual inspection, automated consistency check, two agent audits.
* Not executed / blocked: Clarivate JCR verification; publisher-page validation of dates; reading of most prior full texts; external public deposit; human expert review.
* Files generated and verified: see `README.md` table. `Final_Manuscript.docx`/`.pdf` and `cover_letter.docx` exist and were re-opened (PDF rendered to images and inspected).
