# Candidate research directions (STEP 2–3, internal portfolio)

Scoring is the Director's judgement (1 = poor, 5 = excellent) from (a) literature searches actually run in this session (marked **S**) and (b) prior knowledge only (marked **K**, *not searched, therefore novelty scores are provisional and optimistic-risk*). Feasibility = can the claim be tested on 4 CPU cores / 15 GB RAM / public data within this session.

| # | Direction | Evidence | Importance | Novelty headroom | Feasibility | Reproducibility | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Optimism of record-wise CV predicted by intraclass correlation (ICC) | **S** – 2026 preprints already cover ICC-vs-optimism (arXiv 2607.10634 "When Does Survey-Aware CV Matter? The ICC, not the design effect"; a 2026 medRxiv simulation on repeated-measures predictors; Roberts 2017; Saeb 2017) | 4 | 1 | 5 | 5 | **Rejected – already covered/scooped** |
| 2 | Conformal prediction coverage under subject shift / subject-level calibration | **S** – active 2025–26 work (EEG personalised calibration preprint, group-aware CP, Dunn et al. hierarchical CP) | 4 | 2 | 4 | 4 | Rejected – crowded |
| 3 | Subject-wise vs record-wise validation changes model ranking (HAR) | **S** – Dehghani 2019, Saeb 2017 cover inflation; ranking-change across datasets not found but low incremental value | 3 | 2 | 5 | 5 | Rejected – incremental |
| 4 | **Duplicate / near-duplicate contamination in tabular benchmarks: prevalence, memorisation-dependent inflation, ranking effects, and a closed-form decomposition predicting the inflation** | **S** – no published measurement on OpenML/UCI found; related: TabReD (leaks, time splits), Gorla 2026 (tabular LMs), Barz & Denzler 2020 (CIFAR), Lee 2022 (text), Kapoor & Narayanan 2023 (taxonomy) | 4 | 3–4 | 5 | 5 | **Selected for deep novelty audit** |
| 5 | Time-series CV validity (blocked vs random) | **K** – Cerqueira 2020, Bergmeir 2018 | 3 | 1 | 5 | 5 | Rejected – known |
| 6 | Spatial CV for geo-ML | **K** – Roberts 2017, Meyer 2019, Ploton 2020 | 3 | 1 | 4 | 4 | Rejected – known |
| 7 | SMOTE / resampling vs calibration | **K** – van den Goorbergh 2022 and many others | 3 | 1 | 5 | 5 | Rejected – saturated |
| 8 | Imputation quality vs downstream accuracy | **K** – Jäger 2021, Shadbahr 2023 | 3 | 2 | 5 | 5 | Rejected – crowded |
| 9 | SHAP / feature-attribution instability across seeds (Rashomon) | **K** – many 2020–25 papers | 3 | 2 | 4 | 5 | Rejected – crowded |
| 10 | Benchmark minimisation (few datasets reproduce rankings) | **K** – tinyBenchmarks (LLM), TabArena | 3 | 3 | 4 | 5 | Backup |
| 11 | Sample-size planning from learning curves with uncertainty | **K** – Riley 2020, Figueroa 2012 | 3 | 2 | 5 | 5 | Rejected – known |
| 12 | Time-series anomaly-detection metric inflation (point-adjust) | **K** – Kim et al. AAAI 2022 | 3 | 1 | 4 | 5 | Rejected – known |
| 13 | CMAPSS RUL evaluation-protocol audit | **K** – Ramasso & Saxena 2014; data hosting uncertain | 3 | 2 | 3 | 3 | Rejected – data access risk |
| 14 | Cost-/energy-aware tabular model comparison | **K** – energy measurement unavailable in container (no RAPL) | 3 | 3 | 1 | 2 | Rejected – infeasible measurement |
| 15 | Calibration-drift sequential monitoring (e-values) | **K** – recent theory work | 3 | 3 | 3 | 4 | Rejected – theory-heavy, high risk |
| 16 | Statistical-power analysis of multi-dataset model comparison tests | **K** – Demšar 2006, Benavoli 2017 | 3 | 2 | 5 | 5 | Rejected – largely settled |
| 17 | Intrusion-detection dataset duplicate/leakage audit | **K** – Tavallaee 2009, Engelen 2021 | 3 | 1 | 4 | 5 | Rejected – known (but cited as precedent for #4) |

Direction 4 is retained because (i) it has a falsifiable, quantitative core (a decomposition that either predicts the measured inflation or does not), (ii) it needs only public data and CPU, (iii) literature searches did not find the measurement, and (iv) a null or small effect would still be an informative, publishable result. Its weaknesses are noted in `novelty_map.md`: duplicates in low-cardinality data can be *legitimate* repeated samples (Feldman 2020 long-tail argument), so the study is framed as a **sensitivity analysis between two estimands**, not as proof that random splits are "wrong".
