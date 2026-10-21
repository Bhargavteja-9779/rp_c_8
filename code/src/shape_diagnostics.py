"""EXPLORATORY: within-journal skewness/kurtosis of ln D (acceptance years 2022-2024, journals with >=300 papers). Writes results/shape_diagnostics_EXPLORATORY.json."""
import json, os
import pandas as pd
from scipy import stats
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
d = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", usecols=["issn", "y", "accepted"], parse_dates=["accepted"]); d = d[d.accepted.dt.year.between(2022, 2024)]
g = d.groupby("issn").y.agg(n="size", sk=lambda x: stats.skew(x), ku=lambda x: stats.kurtosis(x)); g = g[g.n >= 300]
out = dict(n_journals=int(len(g)), median_skew=float(g.sk.median()), share_skew_gt0_5=float((g.sk > 0.5).mean()), share_skew_lt_neg0_5=float((g.sk < -0.5).mean()), median_excess_kurt=float(g.ku.median()))
json.dump(out, open(f"{ROOT}/results/shape_diagnostics_EXPLORATORY.json", "w"), indent=1); print(out)
