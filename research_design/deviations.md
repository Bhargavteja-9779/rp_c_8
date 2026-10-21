# Deviations and amendments log

| ID | Date (UTC) | Change | Reason | Made before any real-data forecast evaluation? | Affected claims |
|---|---|---|---|---|---|
| D0 | 2026-10-20 | Protocol v1.0 frozen (commit "Journal selection evidence, candidate portfolio, pre-registered protocol…") | – | yes | – |
| D1 | 2026-10-20 | Empirical quantiles (F0, F1, F2, F6) all use the Hazen (type-5) definition, with weights for F2/F6 (position (cumw − w/2)/W, linear interpolation). Protocol §6 said "type-7" for F0 only. | A single quantile definition across weighted/unweighted forecasters is needed for a fair comparison; type-7 has no natural weighted analogue. | yes (code written, no real-data run) | none |
| D2 | 2026-10-21 | F2 (publisher-pooled) pool and the F4 empirical-Bayes prior use all journals with ≥20 visible training papers at the origin (visibility-only eligibility), not the outcome-dependent "eligible" set. Training windows additionally require accepted<t0 and received<t0. | Eligibility based on test-cohort size would use future information. | yes | none |
| D3 | 2026-10-21 | Crossref download re-launched twice after worker processes terminated early (27 journals missing); final collection covers all 802 frame journals (1,829,907 dated records). Cleaning yields 1,737,272 records. | infrastructure | yes (no forecasts run) | none |
