"""Descriptive tables for the Part E manuscript."""
import json
import numpy as np, pandas as pd
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"
df = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", parse_dates=["received", "accepted"], low_memory=False)
for c in ("R_any", "R_process", "R_ai", "R_other"): df[c] = df[c].astype(bool)
res = {}
res["by_member"] = df.groupby("member").agg(articles=("doi", "size"), journals=("issn", "nunique"), retracted=("R_any", "sum"), process=("R_process", "sum"), ai=("R_ai", "sum"), median_D=("D", "median")).to_dict("index")
res["by_year"] = df[df.acc_year.between(2020, 2026)].groupby("acc_year").agg(articles=("doi", "size"), retracted=("R_any", "sum"), process=("R_process", "sum"), ai=("R_ai", "sum"), median_D=("D", "median")).to_dict("index")
res["prevalence"] = {k: float(df[k].mean()) for k in ("X3", "X4", "X4b", "X5", "N1")} | {"X1": float(df.X1.mean()), "X2": float(df.X2.mean())}
res["D_quantiles"] = {str(q): float(df.D.quantile(q)) for q in (.05, .25, .5, .75, .95)}
res["strata"] = {"n": int(df.stratum.nunique()), "n_ge100": int((df.groupby("stratum").size() >= 100).sum()), "median_size": float(df.groupby("stratum").size().median())}
res["retraction_lag_months_median"] = float(((pd.to_datetime(df.rdate) - df.accepted).dt.days / 30.44)[df.R_any].median())
tt = pd.read_csv(f"{ROOT}/data/raw/frame_eligible.json".replace("frame_eligible.json", "../processed/journal_titles.csv"), index_col=0).iloc[:, 0] if False else None
json.dump(res, open(f"{OUT}/E_tables.json", "w"), indent=1, default=float); print(json.dumps(res, default=float)[:1500])
