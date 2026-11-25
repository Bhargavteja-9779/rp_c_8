"""Cycle-2 experiments X2 (calibration correction F9) and X3 (learned journal-feature meta-forecaster F10, stronger baseline).
Intended time ordering (NOTE: not strictly met; training cohorts include every paper received in the window whenever accepted, so 0.9-3.1% of labels were accepted after the origin; see reinforcement_deviations C2-13 and the strict re-analysis in z_experiments.py Z2):
  test origin 2024-01-01 <- fitted on target cohort of origin 2022-01-01 (received 2022H1; accepted by 2023-07)
  test origin 2025-01-01 <- fitted on cohorts of origins 2022-01-01 and 2023-01-01 (the latter complete by 2024-07)
Design (levels, features, hyper-parameters, time ordering) was fixed in this script before its single run (no re-runs or tuning); the protocol document was written AFTER the run, so this is not an independently time-stamped pre-specification."""
import json, os, sys
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd, lightgbm as lgb
from scipy import stats as sps
from tdelay import experiments as E, forecasters as F, scoring as S, stats as ST
ROOT = "/home/user/rp_c_8"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); OUT = f"{ROOT}/reinforced/results"; os.makedirs(OUT, exist_ok=True)
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); df["acc_year"] = df.accepted.dt.year
fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)]
taus = np.asarray(cfg["taus"]); T9 = np.array([.1, .2, .3, .4, .5, .6, .7, .8, .9]); rng = np.random.default_rng(cfg["seed"])
def feats(y, age, vol_now, vol_prev, m):
    q = F.wquantile(y, np.ones(len(y)), [.05, .1, .25, .5, .75, .9, .95]); rec, old = y[age <= 182], y[age > 182]
    trend = (np.median(rec) - np.median(old)) if len(rec) >= 20 and len(old) >= 20 else 0.0
    return dict(q05=q[0], q10=q[1], q25=q[2], q50=q[3], q75=q[4], q90=q[5], q95=q[6], n=len(y), sd=y.std(), skew=sps.skew(y), trend=trend, logvol=np.log(vol_now + 1) - np.log(vol_prev + 1), pub=m)
def origin_tables(t0, minTr=cfg["min_train"], minTe=cfg["min_test"]):
    per, prior, pools = E._prep_origin(df, member, t0, cfg); t0ts = pd.Timestamp(t0); rows = []
    for i, (tr12, tr24, te) in per.items():
        if len(tr12) < minTr or len(te) < minTe: continue
        y = tr12.y.to_numpy(); age = (t0ts - tr12.V).dt.days.to_numpy(); prev = df[(df.issn == i) & (df.V >= t0ts - pd.Timedelta(days=730)) & (df.V < t0ts - pd.Timedelta(days=365))]
        f = feats(y, age, len(tr12), max(len(prev), 1), {"Springer Nature": 0, "Wiley": 1, "Taylor & Francis": 2}[member[i]])
        rows.append(dict(issn=i, origin=t0, y_train=y, age=age, test=te, feat=f, tr24=tr24))
    return rows
tabs = {t: origin_tables(t) for t in ["2022-01-01", "2023-01-01", "2024-01-01", "2025-01-01"]}
def pits(rows):  # randomised PIT of F0 for each target paper, equal weight per journal
    v, w = [], []
    for r in rows:
        p = S.pit_ecdf(r["test"].y.to_numpy(), r["y_train"], rng); v.append(p); w.append(np.full(len(p), 1.0 / len(p)))
    return np.concatenate(v), np.concatenate(w)
def train_meta(rows_list):
    X, Y = [], []
    for rows in rows_list:
        for r in rows:
            f = r["feat"]; m0 = f["q50"]; base = {k: (v - m0 if k.startswith("q") else v) for k, v in f.items()}; yt = r["test"].y.to_numpy()
            X += [base] * len(yt); Y += list(yt - m0)
    X = pd.DataFrame(X); Y = np.array(Y); models = {}
    for tau in T9:
        models[tau] = lgb.LGBMRegressor(objective="quantile", alpha=tau, n_estimators=200, max_depth=3, learning_rate=0.05, min_child_samples=300, subsample=0.8, subsample_freq=1, colsample_bytree=0.8, verbose=-1, random_state=cfg["seed"], n_jobs=3).fit(X, Y)
    return models
res = []
for t_test, train_origins in (("2024-01-01", ["2022-01-01"]), ("2025-01-01", ["2022-01-01", "2023-01-01"])):
    P, W = pits(sum([tabs[o] for o in train_origins], [])); o = np.argsort(P); cw = np.cumsum(W[o]) / W.sum(); Pq = P[o]
    G_inv = lambda t: float(np.interp(t, cw, Pq))                                   # recalibrated level for nominal t
    models = train_meta([tabs[o_] for o_ in train_origins])
    for r in tabs[t_test]:
        y = r["y_train"]; yt = r["test"].y.to_numpy(); f = r["feat"]; m0 = f["q50"]
        q0 = F.wquantile(y, np.ones(len(y)), T9); q9 = F.wquantile(y, np.ones(len(y)), [min(max(G_inv(t), 0.005), 0.995) for t in T9])
        base = pd.DataFrame([{k: (v - m0 if k.startswith("q") else v) for k, v in f.items()}]); q10 = np.sort(np.array([m0 + models[t].predict(base)[0] for t in T9]))
        age24 = (pd.Timestamp(t_test) - r["tr24"].V).dt.days.to_numpy(); q6 = F.decayed(r["tr24"].y.to_numpy(), age24, cfg["decay_half_life_days"], T9).q
        q2 = F.pooled([x["y_train"] for x in tabs[t_test] if member[x["issn"]] == member[r["issn"]]], T9).q
        for m, q in (("F0", q0), ("F2", q2), ("F6", q6), ("F9", q9), ("F10", q10)):
            res.append(dict(issn=r["issn"], origin=t_test, method=m, n_train=len(y), pinball=S.mean_pinball(yt, q, T9), cov80=S.interval_coverage(yt, q[0], q[-1]), width80=float(q[-1] - q[0])))
R = pd.DataFrame(res); R.to_csv(f"{OUT}/cal_meta_metrics.csv", index=False)
summ = {}
w = R.groupby(["issn", "method"]).pinball.mean().unstack()
for m in ("F6", "F9", "F10", "F2"):
    d = (w[m] - w["F0"]).dropna(); mm, lo, hi = ST.cluster_bootstrap_mean(d.to_numpy(), 5000, cfg["seed"]); t = ST.paired_wilcoxon(w[m].loc[d.index], w["F0"].loc[d.index])
    summ[f"{m}_minus_F0"] = dict(mean=mm, ci=[lo, hi], p=t["p"], rbc=t["rbc"], median_rel=float(np.median(d / w["F0"].loc[d.index])), n_journals=int(len(d)))
for m in ("F0", "F2", "F6", "F9", "F10"):
    g = R[R.method == m]; pj = g.groupby("issn").cov80.mean(); mm, lo, hi = ST.cluster_bootstrap_mean(pj.to_numpy() - 0.8, 5000, cfg["seed"])
    summ[f"{m}_cov80_minus_nominal"] = dict(mean=mm, ci=[lo, hi]); summ[f"{m}_mean_pinball9"] = float(w[m].mean()); summ[f"{m}_mean_width"] = float(g.width80.mean())
for o, g in R.groupby("origin"):
    ww = g.groupby(["issn", "method"]).pinball.mean().unstack(); summ[f"by_origin_{o}"] = dict(n_journals=int(len(ww)), **{f"{m}_cov80": float(g[g.method == m].cov80.mean()) for m in ("F0", "F6", "F9", "F10")}, **{f"{m}_minus_F0": float((ww[m] - ww.F0).mean()) for m in ("F6", "F9", "F10")})
# the recalibration map itself (for the paper): level to use for the nominal 10th and 90th percentile
P, W = pits(sum([tabs[o] for o in ["2022-01-01", "2023-01-01"]], [])); o_ = np.argsort(P); cw = np.cumsum(W[o_]) / W.sum(); summ["recal_map_2022_2023"] = {str(t): float(np.interp(t, cw, P[o_])) for t in (.05, .1, .25, .5, .75, .9, .95)}
json.dump(summ, open(f"{OUT}/cal_meta_summary.json", "w"), indent=1, default=float); print(json.dumps(summ, indent=1, default=float)[:3500])
