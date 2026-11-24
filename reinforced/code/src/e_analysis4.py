"""Part E analysis A13 (amendments E-A4, E-A6): accepted-to-first-online lag, articles with a TRUE first-online date only."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
import numpy as np, pandas as pd
from e_lib import strata_tables, mh_ci, fe_logit
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"
df = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", parse_dates=["received", "accepted"], low_memory=False)
for c in ("R_any", "R_process", "R_ai", "R_other"): df[c] = df[c].astype(bool)
d = df[df.L1.notna() & df.X1.notna()].copy(); res = {"n": int(len(d)), "lag_median_days": float(d.lag.median())}
for out in ("R_process", "R_any"):
    res[out] = {k: mh_ci(strata_tables(d, k, out), B=300) for k in ("L1", "L2", "X1")}; res[out]["joint"] = fe_logit(d, out, ["X1", "X2", "L1", "L2", "ln_auth"])
json.dump(res, open(f"{OUT}/E_results4.json", "w"), indent=1, default=float); f = lambda v: (round(v["or_mh"], 2), [round(x, 2) for x in v["ci_cluster"]], v["exposed_events"], v["events"])
print({o: {k: f(res[o][k]) for k in ("L1", "L2", "X1")} for o in ("R_process", "R_any")})
