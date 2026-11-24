"""Part E analysis A13 (amendment E-A4): accepted-to-first-online lag."""
import json, sys, hashlib
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
import numpy as np, pandas as pd
from e_lib import strata_tables, mh_ci, fe_logit
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"
df = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", parse_dates=["received", "accepted"], low_memory=False)
for c in ("R_any", "R_process", "R_ai", "R_other"): df[c] = df[c].astype(bool)
v = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", usecols=["doi", "V"], parse_dates=["V"]); v["doi"] = v.doi.str.lower(); df = df.merge(v.drop_duplicates("doi"), on="doi", how="left"); df["lag"] = (df.V - df.accepted).dt.days
d = df[df.lag.notna()].copy(); sz = d.groupby("stratum").lag.transform("size"); q05 = d.groupby("stratum").lag.transform(lambda s: s.quantile(.05)); q95 = d.groupby("stratum").lag.transform(lambda s: s.quantile(.95))
d["L1"] = np.where(sz >= 100, d.lag <= q05, np.nan); d["L2"] = np.where(sz >= 100, d.lag >= q95, np.nan); d = d[d.L1.notna() & d.X1.notna()].copy(); res = {"n": int(len(d)), "lag_median_days": float(d.lag.median())}
for out in ("R_process", "R_any"):
    res[out] = {k: mh_ci(strata_tables(d, k, out), B=300) for k in ("L1", "L2", "X1")}; res[out]["joint"] = fe_logit(d, out, ["X1", "X2", "L1", "L2", "ln_refs", "ln_auth"])
sha = hashlib.sha256(open(f"{ROOT}/data/raw/retraction_watch/retraction_watch.csv.gz", "rb").read()).hexdigest(); res["rw_snapshot_sha256_gz"] = sha
json.dump(res, open(f"{OUT}/E_results4.json", "w"), indent=1, default=float); f = lambda v: (round(v["or_mh"], 2), [round(x, 2) for x in v["ci_cluster"]], v["exposed_events"], v["events"])
print({o: {k: f(res[o][k]) for k in ("L1", "L2", "X1")} for o in ("R_process", "R_any")}); print({o: {k: (round(x["or_"], 2), [round(y, 2) for y in x["ci"]]) for k, x in res[o]["joint"].items() if isinstance(x, dict)} for o in ("R_process", "R_any")}); print(sha)
