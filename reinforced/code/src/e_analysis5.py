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
    cols = ["X1", "X2", "X4", "X5", "ln_auth"]; X = x[cols].astype(float).to_numpy(); tt = x.t.to_numpy(); st = x.ev.to_numpy(); sa = x.stratum.to_numpy(); jn = x.issn.to_numpy()
    fit = PHReg(tt, X, status=st, strata=sa, ties="breslow").fit(disp=False); hr = np.exp(fit.params); ci = np.exp(fit.conf_int())
    res[out] = {"n_rows": int(len(x)), "n_events": int(x.ev.sum()), "n_strata": int(x.stratum.nunique()), "excluded_nonpositive_time": n_bad, "median_follow_up_days": float((CUT - x.accepted).dt.days.median())}
    rng = np.random.default_rng(5); js = np.unique(jn); idx = {a: np.where(jn == a)[0] for a in js}; bs = []
    for b in range(200):
        picks = rng.choice(js, len(js)); pick = np.concatenate([idx[a] for a in picks]); lab = np.concatenate([np.char.add(sa[idx[a]].astype(str), f"|{k}") for k, a in enumerate(picks)])
        try: bs.append(np.exp(PHReg(tt[pick], X[pick], status=st[pick], strata=lab, ties="breslow").fit(disp=False).params))
        except Exception: pass
    bs = np.array(bs)
    for i, name in enumerate(cols): res[out][name] = {"hr": float(hr[i]), "ci_model": [float(ci[i, 0]), float(ci[i, 1])], "p": float(fit.pvalues[i]), "ci_boot": [float(np.quantile(bs[:, i], .025)), float(np.quantile(bs[:, i], .975))] if len(bs) > 20 else None}
    res[out]["n_boot"] = int(len(bs))
json.dump(res, open(f"{OUT}/E_results5.json", "w"), indent=1); print({o: {k: (round(v["hr"], 2), [round(c, 2) for c in v["ci_model"]], v["ci_boot"]) if isinstance(v, dict) and "hr" in v else v for k, v in res[o].items()} for o in res})
