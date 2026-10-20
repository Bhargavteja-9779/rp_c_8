# Novelty map and prior-art audit (Gate C)

Searches performed (this session, 2026-10-20): web/extended searches for publication-delay studies, forecasting of review times, Crossref/PubMed date-based analyses, MetaROR plan; Crossref title look-ups for each cited paper. **Limitations:** full texts of most items were not read (paywalls, blocked publisher pages); evidence level is stated per item in `literature_matrix.csv`. Patent databases were not searched (not relevant to this topic).

| Prior work | What it established | What remains open |
|---|---|---|
| Björk & Solomon 2013 | Delays differ by field; **within-journal article variance dominates submission→acceptance** | 2012 data, 135 journals; no forecasting; variance not partitioned by year; no uncertainty on journal-level quantiles |
| Bilalli et al. 2021 | Publisher-reported averages differ massively from article-metadata values (10 CS journals) | No predictive validity; no distributional / quantile view |
| Mrowinski et al. 2016 | Mechanistic stage model of review time | Single journal, 58 papers |
| Horbach 2020; Argilés-Bosch 2023; Ellison 2002 | Turnaround is non-stationary (COVID speed-up; upward trends) | Magnitude of drift relative to forecast error not assessed |
| Andersen 2021 | Huge between-study heterogeneity of definitions | – |
| Himmelstein 2015 (blog) | PubMed dates usable at scale; medians ~100 d | Not peer reviewed; no forecasting |
| Dianovics et al. (MetaROR plan, 2026) | Planned PubMed-wide GAM + CatBoost with **random** train/test split | Results not available; random split is not out-of-time; biomedical only |

## Contribution claims and their differentiating features
1. **Out-of-time, visibility-respecting forecasting benchmark** of journal turnaround with proper scoring rules (not found in searched literature). *Falsifier:* a prior study that evaluates journal-level turnaround forecasts on later cohorts — none found; **risk: unseen competing work (e.g., the MetaROR study once published)**.
2. **Calibration of "≤ T-day" evidence** for journals at scale (RQ4) — not found.
3. **Variance partition with year-level component and cluster-bootstrap uncertainty at ~800 journals** — extends Björk & Solomon; *not* claimed as a new finding.
4. **Cross-source (Crossref vs PubMed) date validation** — partially novel; modest.

Claims **not** made: first study of publication delays; new theory; causal explanation of delays; guarantees about future individual papers.

## Closest-work comparison (Phase 3 table)
| Dimension | Björk & Solomon 2013 | Bilalli 2021 | MetaROR plan | **This study** |
|---|---|---|---|---|
| Unit | article | journal average | article | journal + article |
| Out-of-time evaluation | no | no | no (random split) | **yes** |
| Distributional forecasts | no | no | no | **yes (19 quantiles, intervals, P(D≤T))** |
| Calibration analysis | no | no | no | **yes** |
| Scale | 2,700 articles / 135 journals | 10 journals | ~6.6 M PubMed | ~1.6 M Crossref records / ~800 journals + PubMed validation |
| Coverage beyond biomedicine | yes | CS | no | yes (Springer Nature, Wiley, T&F) |

## Honest assessment
The contribution is an **empirical meta-research study with a methodologically sound evaluation design**. Skeptical-editor view: "descriptive bibliometrics with a forecasting wrapper; findings (journal explains little variance; past medians are noisy) are plausible a priori." The study is publishable only if (i) data quality is shown to be sound, (ii) the forecasting comparison yields non-trivial, calibrated, quantitative results (e.g., how many journals' intervals fail), and (iii) limitations (accepted-only, three publishers) are prominent. Approval status: **Director conditionally approves** (novelty moderate; feasibility high); the novelty auditor records the objection "risk of incrementality" as OPEN.
