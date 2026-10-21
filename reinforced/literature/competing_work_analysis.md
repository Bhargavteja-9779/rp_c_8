# Competing-work analysis and novelty stress test (cycle 2)
Source: independent prior-art investigation by a separately launched agent (Reviewer C; report `agent_C_prior_art.md`, matrix `agent_C_matrix.csv`) using web search, Crossref and primary pages, run 2026-10-21; plus my own DOI verification (`verified_references_cycle2.json`). Scopus, Web of Science and Google Scholar were not searchable, so coverage after October 2025 is incomplete. Most scholarly sources were read at abstract/record level because publisher pages were blocked; the exceptions are noted in the matrix (`evidence_level_read`).

## What exists (closest work)
| Work | Relation to this project |
|---|---|
| Dianovics, Varga, Bognar, Aczel — acceptance and publication lags 2016–2025 (OSF registration 30 Nov 2025; Lifecycle Journal DOI 10.71240/lcyc.084124; evaluation complete 13 Apr 2026) | PubMed-wide (6.64 M) descriptive GAM + CatBoost/SHAP with a **random 80/20 split**; article-level point prediction; the plan states it was **not preregistered** and all analyses are exploratory; no results found as of 2026-10-21. v1 text calling it a "concurrent registered study" was wrong. |
| Björk & Solomon 2013 | 2,700 papers/135 journals; within-journal variance dominates submission→acceptance. Our variance partition replicates this at larger scale — not a new finding. |
| Phillips & Horn 2025 (JAMA Netw Open) | audit of how 57 health-policy journals *report* times; not actual times. Previously un-cited. |
| Himmelstein (blog 2016) | per-journal drift for 3,086 PubMed journals; descriptive. |
| Hanson et al. 2024 (QSS), Luwel et al. 2020, Hadavand et al. 2024, Sebo et al. 2019–23, Petrou 2025, Royle 2026 | descriptive lag trends/determinants; none evaluates forecasts. Previously un-cited. |
| Bilalli et al. 2021 | publisher-reported vs article-metadata averages for 10 CS journals. |
| Vendor tools (GradSummit "Journal Clock", Manusights timelines) | present historical medians as planning aids; no validation described — they instantiate the use case our paper tests. |

## Stress test
| Question | Answer |
|---|---|
| Is the main contribution already known? | The *out-of-time, proper-scoring evaluation of journal-level turnaround forecasts and of "within T days" claims* was not found. The variance partition and the existence of drift are known. |
| Genuinely new principle? | No. Standard forecast-evaluation tools applied to an unfilled gap — incremental but real. |
| Only a combination of standard components? | Yes (empirical quantiles, pinball loss, bootstrap). The value is the design, the calibration finding and the practical remedy. |
| Application of a standard model to a new dataset? | Partly; the dataset (Crossref publication-history assertions at scale) is itself a moderate novelty — no published study using these assertions at scale was found. |
| Is the gap supported by primary evidence? | The absence of prior forecasting evaluations is an absence claim; supported by a documented but non-systematic search. Wording must be "we found no". |
| Would removing the claimed novelty invalidate the paper? | The paper survives as an empirical measurement/benchmark paper; its framing as "first" would not. |
| Risk | If the MetaROR group publishes a temporal-split version, the article-covariate result would overlap. |

## Consequence for the manuscript
Cite and position against Phillips & Horn, Hanson, Luwel, Hadavand, Sebo, Himmelstein, Petrou/Royle (blogs labelled as such), vendor tools (as use-case evidence, labelled non-scholarly); describe MetaROR correctly; replace "not addressed in earlier work" by "we found no earlier out-of-time evaluation".
