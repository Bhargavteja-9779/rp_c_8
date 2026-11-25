"""Y1: rolling quarterly-origin panel with equal follow-up (D capped at 480 d), two-way (imprint x origin) cluster bootstrap and out-of-time recalibration."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from tdelay import experiments as E, forecasters as F, scoring as S
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); rng = np.random.default_rng(cfg["seed"]); CAP = 480; H = 91
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)].copy()
imprint = pd.read_csv(f"{OUT}/journal_imprint_map.csv", index_col=0).iloc[:, 0]
df["D"] = df.D.clip(upper=CAP); df["y"] = np.log(df.D.astype(float)); c = dict(cfg, horizon_days=H)
origins = list(pd.date_range("2022-01-01", "2024-04-01", freq="QS").strftime("%Y-%m-%d")); taus9 = np.array([.1, .2, .3, .4, .5, .6, .7, .8, .9]); rows = []; pit_store = {}
for t0 in origins:
    per, prior, pools = E._prep_origin(df, member, t0, c); t0ts = pd.Timestamp(t0); pooled = {m: F.pooled(v, taus9) for m, v in pools.items()}; P, Wt = [], []; kept = []
    for i, (tr12, tr24, te) in per.items():
        if len(tr12) < 100 or len(te) < 30: continue
        kept.append((i, tr12, tr24, te)); p = S.pit_ecdf(te.y.to_numpy(), tr12.y.to_numpy(), rng); P.append(p); Wt.append(np.full(len(p), 1 / len(p)))
    pit_store[t0] = (np.concatenate(P), np.concatenate(Wt)); tcomplete = pd.Timestamp(t0) + pd.Timedelta(days=H + CAP)
    # recalibration map from origins whose targets were complete at t0
    use = [o for o in origins if pd.Timestamp(o) + pd.Timedelta(days=H + CAP) <= t0ts and o in pit_store]; G = None
    if use:
        Pp = np.concatenate([pit_store[o][0] for o in use]); Ww = np.concatenate([pit_store[o][1] for o in use]); o_ = np.argsort(Pp); G = (Pp[o_], np.cumsum(Ww[o_]) / Ww.sum())
    for i, tr12, tr24, te in kept:
        y = tr12.y.to_numpy(); yt = te.y.to_numpy(); q0 = F.wquantile(y, np.ones(len(y)), taus9); q2 = pooled[member[i]].q
        age24 = (t0ts - tr24.V).dt.days.to_numpy(); q6 = F.decayed(tr24.y.to_numpy(), age24, cfg["decay_half_life_days"], taus9).q; cand = [("F0", q0), ("F2", q2), ("F6", q6)]
        if G is not None:
            lv = [float(np.interp(t, G[1], G[0])) for t in taus9]; cand.append(("F0cal", F.wquantile(y, np.ones(len(y)), [min(max(l, .005), .995) for l in lv])))
        for m, q in cand: rows.append(dict(origin=t0, issn=i, imprint=imprint.get(i, "other"), method=m, n_train=len(y), n_test=len(yt), pinball=S.mean_pinball(yt, q, taus9), cov80=S.interval_coverage(yt, q[0], q[-1]), width80=float(q[-1] - q[0]), recal_available=G is not None))
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/Y1_panel_metrics.csv", index=False)
res = {}
f0 = R[R.method == "F0"]; cell = f0.groupby(["imprint", "origin"]).cov80.mean().sub(0.8).unstack("origin")
res["F0_shortfall_by_origin_journal_mean"] = f0.groupby("origin").cov80.mean().sub(0.8).round(4).to_dict(); res["F0_shortfall_by_imprint"] = f0.groupby("imprint").cov80.mean().sub(0.8).round(4).to_dict()
res["n_journal_origins"] = int(len(f0)); res["n_journals"] = int(f0.issn.nunique())
def twoway(cellmat, B=5000):
    M = cellmat.to_numpy(); out = []
    for _ in range(B):
        ri = rng.integers(0, M.shape[0], M.shape[0]); co = rng.integers(0, M.shape[1], M.shape[1]); out.append(np.nanmean(M[np.ix_(ri, co)]))
    return float(np.nanmean(M)), float(np.quantile(out, .025)), float(np.quantile(out, .975))
res["F0_shortfall_twoway_cluster"] = dict(zip(["est", "lo", "hi"], twoway(cell)))
om = f0.groupby("origin").cov80.mean().sub(0.8); res["origin_level_sd"] = float(om.std(ddof=1)); res["predictive_interval_future_origin_95"] = [float(om.mean() - 2.26 * om.std(ddof=1) * np.sqrt(1 + 1 / len(om))), float(om.mean() + 2.26 * om.std(ddof=1) * np.sqrt(1 + 1 / len(om)))]
w = R.groupby(["issn", "method"]).pinball.mean().unstack(); res["skill_F0_vs_F2"] = float(1 - w.F0.mean() / w.F2.mean()); res["F6_minus_F0"] = float((w.F6 - w.F0).mean())
rc = R[R.recal_available & R.method.isin(["F0", "F0cal"])]; res["recalibrated_origins"] = sorted(rc.origin.unique().tolist())
if len(rc):
    c1 = rc.groupby(["imprint", "origin", "method"]).cov80.mean().sub(0.8).unstack("method")
    for m in ("F0", "F0cal"):
        mm = c1[m].unstack("origin"); res[f"recal_window_{m}_shortfall_twoway"] = dict(zip(["est", "lo", "hi"], twoway(mm)))
    ww = rc.groupby(["issn", "method"]).pinball.mean().unstack(); res["recal_window_pinball_F0cal_minus_F0"] = float((ww.F0cal - ww.F0).mean()); res["recal_window_cov_by_origin"] = rc.groupby(["origin", "method"]).cov80.mean().unstack().round(4).to_dict()
json.dump(res, open(f"{OUT}/Y1_panel_summary.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float))
