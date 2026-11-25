"""Part E analyses A11-A12 (amendment E-A3)."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
import numpy as np, pandas as pd
from e_lib import strata_tables, mh_ci
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"
df = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", parse_dates=["received", "accepted", "rdate"], low_memory=False)
for c in ("R_any", "R_process", "R_ai", "R_other"): df[c] = df[c].astype(bool)
res = {}; d = df[(df.accepted >= "2020-01-01") & (df.accepted <= "2024-10-31") & df.X1.notna()].copy(); lag = (d.rdate - d.accepted).dt.days
d["R_process_24"] = d.R_process & (lag <= 730); d["R_any_24"] = d.R_any & (lag <= 730); res["A11"] = {"n": int(len(d)), "events_process_24": int(d.R_process_24.sum()), "events_any_24": int(d.R_any_24.sum())}
for out in ("R_process_24", "R_any_24"):
    res["A11"][out] = {"overall": mh_ci(strata_tables(d, "X1", out), B=300), "by_year": {}}
    for y, g in d.groupby("acc_year"):
        if g[out].sum() >= 8: res["A11"][out]["by_year"][int(y)] = mh_ci(strata_tables(g, "X1", out), B=200)
pj = df[df.R_process].groupby("issn").size().sort_values(ascending=False); tot = pj.sum(); res["A12"] = {"n_journals_with_process_retractions": int(len(pj)), "share_top": {str(k): float(pj.head(k).sum() / tot) for k in (1, 5, 10, 20)}, "top_journals_events": {k: int(v) for k, v in pj.head(10).items()}, "excl_top": {}}
d1 = df[df.X1.notna()]
for k in (1, 3, 5, 10, 20): res["A12"]["excl_top"][str(k)] = mh_ci(strata_tables(d1[~d1.issn.isin(pj.head(k).index)], "X1", "R_process"), B=300)
json.dump(res, open(f"{OUT}/E_results3.json", "w"), indent=1, default=float)
f = lambda v: (round(v["or_mh"], 2), [round(x, 2) for x in v["ci_cluster"]], v["exposed_events"], v["events"])
print(res["A11"]["n"], res["A11"]["events_process_24"], {o: (f(res["A11"][o]["overall"]), {y: f(v) for y, v in res["A11"][o]["by_year"].items()}) for o in ("R_process_24", "R_any_24")}); print(res["A12"]["share_top"], res["A12"]["top_journals_events"]); print({k: f(v) for k, v in res["A12"]["excl_top"].items()})
