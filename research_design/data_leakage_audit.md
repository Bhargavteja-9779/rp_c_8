# Leakage and validity audit plan (Phase 6, adapted to forecasting)

Leakage in this study is **temporal / information leakage**: a forecaster must use only information an author could see at origin t0.

| Risk | Control | Verification |
|---|---|---|
| Target papers used in training | Visibility rule V < t0 for training; target defined by `received` ≥ t0; disjoint by construction | unit test `test_visibility_no_overlap`; runtime assertion on every journal-origin |
| Empirical-Bayes prior estimated from target data | prior estimated only from T12 across journals | unit test with synthetic data where targets are shifted; prior must be unchanged |
| Hyper-parameters tuned on targets | none tuned; half-life, windows fixed in protocol | code review; config file frozen |
| Duplicate DOIs across ISSN variants | DOI dedup | assertion |
| Same paper in two journals | impossible (DOI unique) | – |
| Right-censoring of target cohort | follow-up ≥ 2.8 y at cutoff; sensitivity: restrict D ≤ 730 | report share of target with D > 730 |
| Look-ahead in cleaning thresholds | cleaning rules fixed in protocol | – |
| Survivorship (accepted-only) | acknowledged in estimand; not correctable with available data | limitation |
| Article covariates unavailable pre-submission | restricted to author count, month, weekday; refs flagged | table in manuscript |
| Selection into frame | census of frame; limitations stated | frame table |

Results of the executed checks are recorded in `results/leakage_checks.json` by `run_all.py`.
