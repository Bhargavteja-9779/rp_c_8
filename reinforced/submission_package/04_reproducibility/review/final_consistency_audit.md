# Final consistency audit of `Revised_Manuscript.docx` (cycle 2)

Script: `reinforced/code/src/consistency_check.py` (re-derives each value from the results file, then searches the DOCX text). 26/26 found.

| Quantity | Source | Expected string | Result |
|---|---|---|---|
| records | `results/metrics.json` | 1,737,272 | found |
| target papers | `results/metrics.json` | 298,469 | found |
| journal ICC % | `metrics.json vc` | 26.5% | found |
| residual share % | `metrics.json vc` | 69.1% | found |
| F0 skill vs F2 % | `metrics.json forecasters.F0.skill` | 15.7% | found |
| F0 coverage 80 shortfall (points) | `metrics.json` | −3.0 | found |
| Z1 base_visible | `Z_summary.json` | −4.9 | found |
| Z1 half_visible | `Z_summary.json` | −2.8 | found |
| Z1 double_visible | `Z_summary.json` | −8.9 | found |
| Z1 base_oracle | `Z_summary.json` | −1.6 | found |
| Z2 R shortfall | `Z_summary.json` | +1.9 | found |
| Z2 V shortfall | `Z_summary.json` | +1.1 | found |
| Z2 F4 shortfall | `Z_summary.json` | +1.3 | found |
| Z2 F0 shortfall | `Z_summary.json` | −1.9 | found |
| Z2 slope raw 72 | `Z_summary.json` | 0.91 | found |
| Z2 slope cal 72 | `Z_summary.json` | 0.97 | found |
| Z4 journal-weighted ≤14 d % | `Z_summary.json` | 82% | found |
| Z4 journal-weighted >90 d % | `Z_summary.json` | 8.9% | found |
| Z5 pre-origin eligibility | `Z_summary.json` | −3.1 | found |
| Z6 pooled panel | `Z_summary.json` | −2.4 | found |
| Z6 block CI lo | `Z_summary.json` | −2.9 | found |
| Z6 lag1 | `Z_summary.json` | 0.76 | found |
| Z3 F0 shortfall imprint CI lo | `Z_summary.json` | −4.2 | found |
| Z3 F0−F2 Holm | `Z_summary.json` | <0.001 | found |
| X1 share ≤ +14 d (Springer Nature) | `X1_summary.json` | 95% | found |
| panel journal-origins | `Y1_panel_summary.json` | 7,417 | found |

- Unresolved markers (`⟦`, `nan`, `None`, braces): 0 ([])
- Reference list entries: 29; distinct numbers cited in text: 29; cited but missing from list: []; listed but never cited: []
- Placeholders left for authors (4 distinct): ['[Author names, affiliations, ORCID iDs and corresponding−author details to be supplied by the authors]', '[to be completed by the authors; none is recorded]', '[to be completed by the authors]', '[to be completed]']
- Abstract word count and main-text length are printed by `build_revised_manuscript.py`.
