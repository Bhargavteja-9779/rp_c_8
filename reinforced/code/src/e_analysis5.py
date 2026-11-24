"""Part E analysis A14 (amendment E-A5): stratified Cox models for time from acceptance to retraction."""
import json, sys, warnings
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
import numpy as np, pandas as pd
from statsmodels.duration.hazard_regression import PHReg
warnings.filterwarnings("ignore")
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; CUT = pd.Timestamp("2026-11-24")
df = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", parse_dates=["received", "accepted", "rdate"], low_memory=False)
for c in ("R_any", "R_process"): df[c] = df[c].astype(bool)
d = df[df.X1.notna()].copy(); res = {}
for out in ("R_process", "R_any"):
    t = np.where(d[out], (d.rdate - d.accepted).dt.days, (CUT - d.accepted).dt.days).astype(float); ev = d[out].to_numpy() & (t > 0); n_bad = int((d[out].to_numpy() & ~(t > 0)).sum())
    x = d.assign(t=t, ev=ev.astype(int)); x = x[(x.t > 0)]
    inf = x.groupby("stratum").ev.sum(); x = x[x.stratum.isin(inf[inf > 0].index)]
    X = x[["X1", "X2", "X4", "X5", "ln_refs", "ln_auth"]].astype(float); mod = PHReg(x.t.to_numpy(), X.to_numpy(), status=x.ev.to_numpy(), strata=x.stratum.to_numpy(), ties="breslow"); fit = mod.fit(groups=pd.factorize(x.issn)[0], disp=False)
    hr = np.exp(fit.params); ci = np.exp(fit.conf_int()); res[out] = {"n_rows": int(len(x)), "n_events": int(x.ev.sum()), "n_strata": int(x.stratum.nunique()), "excluded_nonpositive_time": n_bad, "median_follow_up_days": float((CUT - x.accepted).dt.days.median())}
    for i, name in enumerate(["X1", "X2", "X4", "X5", "ln_refs", "ln_auth"]): res[out][name] = {"hr": float(hr[i]), "ci": [float(ci[i, 0]), float(ci[i, 1])], "p": float(fit.pvalues[i])}
json.dump(res, open(f"{OUT}/E_results5.json", "w"), indent=1); print({o: {k: (round(v["hr"], 2), [round(c, 2) for c in v["ci"]]) if isinstance(v, dict) and "hr" in v else v for k, v in res[o].items()} for o in res})
