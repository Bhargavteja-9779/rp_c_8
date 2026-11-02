# turnaround_forecast

Calibrated forecasts of the time from submission to acceptance for the **next accepted paper** of a journal, from that journal's own recent records. Implements method **CV0** of the accompanying paper (see `reinforced/manuscript/`): the empirical distribution of the last 12 months of visible papers, smoothed with a Gaussian kernel whose variance is the estimated cohort-to-cohort shift variance τ² plus the sampling variance of the mean.

```
G(q) = (1/n) Σ_i Φ((q − y_i)/h),  h² = τ² + s²/n,  y = ln(days, capped at 480)
```

Python (numpy, pandas, scipy):

```python
import pandas as pd
from turnaround_forecast import forecast, claim_check
rec = pd.read_csv("records.csv")            # columns: received, accepted, first_online (optional)
forecast(rec, origin="2026-01-01")          # quantiles in days, 80% interval, P(D <= 72/120/180)
claim_check(rec, "2026-01-01", days=72, share=0.5)
```

Command line: `python -m turnaround_forecast records.csv --origin 2026-01-01 --claim 72 0.5`.

Browser: open `web/index.html` (self-contained; the data never leave the page). The JavaScript implements the same formulas; `web/` was checked against the Python output on the bundled synthetic example.

## What it is and is not
* Defaults (`turnaround_forecast/defaults.json`) were learned from Crossref dates of 774 Springer Nature, Wiley and Taylor & Francis journals; they are cohort-shift variances for log-days, not properties of any individual journal. Use `tau2=0` for the plain empirical forecast.
* Conditional on acceptance. It says nothing about the probability that a submission is accepted, and it is not a promise about any journal's future speed.
* Validated for journals with ≥ 100 visible papers; the code warns below that and refuses below 30.
* Tests: `python -m pytest product/tests` (includes a comparison with the study pipeline on 20+ journal-origins when the study data are present).
