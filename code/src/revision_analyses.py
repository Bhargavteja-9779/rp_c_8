"""EXPLORATORY revision analyses (deviations D8-D10) prompted by the independent review:
 R1 extra origins (2022-01-01, 2025-01-01 added; F1/F6 windows are clipped at the 2021-01-01 data start for 2022);
 R2 article-level model on a strictly pre-submission covariate set (no reference count) with journal-cluster CI;
 R3 shrinkage tested on empirical quantiles (F7) and a short-window persistence baseline (F8) incl. small-n journals (n_train>=30);
 R4 finite-sample under-coverage expected under iid sampling at the observed training sizes;
 R5 secular trend of ln D by acceptance year."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
from tdelay import experiments as E, forecasters as F, scoring as S, stats as ST, protocol as P
ROOT = os.path.abspath(os.path.join(HERE, "..", "..")); R = f"{ROOT}/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json"))
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); df["acc_year"] = df.accepted.dt.year
fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)]
out = {}
# ---- R1 extra origins
c4 = dict(cfg, origins=["2022-01-01", "2023-01-01", "2024-01-01", "2025-01-01"])
met, pit, f5 = E.run_forecast_experiment(df, member, c4); met.to_csv(f"{R}/revision_R1_metrics_4origins_EXPLORATORY.csv", index=False)
r1 = {}
for o, g in met.groupby("origin"):
    w = g.groupby(["issn", "method"]).pinball.mean().unstack(); c = g[g.method == "F0"]
    r1[o] = dict(n_journals=int(c.issn.nunique()), cov80_F0=float(c.cov80.mean()), cov80_F4=float(g[g.method == "F4"].cov80.mean()), skill_F0_vs_F2=float(1 - w.F0.mean() / w.F2.mean()), F4_minus_F0=float((w.F4 - w.F0).mean()), F6_minus_F0=float((w.F6 - w.F0).mean()),
                 share_P72_ge_0_5=float((c.real_72 >= .5).mean()), median_train_days=float(c.median_fc_days.median()), median_test_days=float(c.test_median_days.median()))
out["R1_by_origin"] = r1
pj = met[met.method == "F0"].groupby("issn").cov80.mean(); out["R1_pooled_F0_cov80_minus_nominal"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(pj.to_numpy() - .8, 2000, cfg["seed"])))
# ---- R2 pre-submission covariates only
r, pooled, d7 = E.article_level_experiment(df, member, cfg, None, feats=["n_authors", "rec_month", "rec_wd"]); out["R2_presubmission_only"] = dict(pooled=pooled, bootstrap=E.article_level_ci(d7, cfg))
# ---- R3 F7 / F8 with small-n journals
c3 = dict(cfg, min_train=30, min_test=30); taus = np.asarray(c3["taus"]); rng = np.random.default_rng(cfg["seed"]); rows = []
for t0 in cfg["origins"]:
    per, prior, pools = E._prep_origin(df, member, t0, c3); t0ts = pd.Timestamp(t0)
    vis = {i: t[0] for i, t in per.items() if len(t[0]) >= c3["prior_min_n"]}
    # bootstrap sampling variance of each journal's empirical quantiles, then DerSimonian-Laird shrinkage per quantile level
    qs = {}; vq = {}
    for i, t in vis.items():
        y = t["y"].to_numpy(); qs[i] = F.wquantile(y, np.ones(len(y)), taus)
        bq = np.array([F.wquantile(y[rng.integers(0, len(y), len(y))], np.ones(len(y)), taus) for _ in range(60)]); vq[i] = bq.var(axis=0, ddof=1) + 1e-8
    ids = list(qs); Q = np.array([qs[i] for i in ids]); V = np.array([vq[i] for i in ids]); mu0 = np.zeros(len(taus)); tau2 = np.zeros(len(taus))
    for k in range(len(taus)): tau2[k], mu0[k] = F._dl_tau2(Q[:, k], V[:, k])
    pooled_fc = {m: F.pooled(v, taus) for m, v in pools.items()}
    for i, (tr12, tr24, test) in per.items():
        if len(tr12) < c3["min_train"] or len(test) < c3["min_test"]: continue
        y = tr12["y"].to_numpy(); yt = test["y"].to_numpy(); q0 = F.wquantile(y, np.ones(len(y)), taus)
        v0 = vq[i] if i in vq else np.array([F.wquantile(y[rng.integers(0, len(y), len(y))], np.ones(len(y)), taus) for _ in range(60)]).var(axis=0, ddof=1) + 1e-8
        B = tau2 / (tau2 + v0); q7 = np.sort(B * q0 + (1 - B) * mu0)
        age = (t0ts - tr12["V"]).dt.days.to_numpy(); rec = y[age <= 182]; q8 = F.wquantile(rec, np.ones(len(rec)), taus) if len(rec) >= 20 else np.full(len(taus), np.nan)
        for m, q in (("F0", q0), ("F2", pooled_fc[member[i]].q), ("F7", q7), ("F8", q8)):
            if np.isnan(q).any(): continue
            ia, ib = int(np.argmin(abs(taus - .1))), int(np.argmin(abs(taus - .9)))
            rows.append(dict(issn=i, origin=t0, method=m, n_train=len(y), pinball=S.mean_pinball(yt, q, taus), cov80=S.interval_coverage(yt, q[ia], q[ib])))
m3 = pd.DataFrame(rows); m3.to_csv(f"{R}/revision_R3_F7F8_EXPLORATORY.csv", index=False)
ntr = m3[m3.method == "F0"].groupby("issn").n_train.mean(); strata = pd.cut(ntr, [0, 100, 200, 400, np.inf], right=False, labels=["30-99", "100-199", "200-399", ">=400"])
w = m3.groupby(["issn", "method"]).pinball.mean().unstack(); r3 = []
for s in strata.cat.categories:
    ids = strata.index[strata == s]
    if len(ids) < 5: continue
    row = dict(stratum=s, n_journals=len(ids))
    for a in ("F7", "F8"):
        d = (w.loc[ids, a] - w.loc[ids, "F0"]).dropna(); mm, lo, hi = ST.cluster_bootstrap_mean(d.to_numpy(), 2000, cfg["seed"]); row[f"{a}_minus_F0"] = mm; row[f"{a}_ci"] = [lo, hi]
    r3.append(row)
out["R3_strata"] = r3; out["R3_overall"] = {a: float((w[a] - w.F0).mean()) for a in ("F7", "F8")}
# ---- R4 finite-sample deficit: iid sampling at the observed sizes
f0 = met[(met.method == "F0") & met.origin.isin(cfg["origins"])]; rng = np.random.default_rng(1); cov = []
for n_tr, n_te in zip(f0.n_train, f0.n_test):
    sd = 0.8; tr = rng.normal(0, sd, n_tr); te = rng.normal(0, sd, n_te); q = F.wquantile(tr, np.ones(n_tr), [.1, .9]); cov.append(np.mean((te >= q[0]) & (te <= q[1])))
out["R4_finite_sample_cov80_minus_nominal_iid"] = float(np.mean(cov) - 0.8)
# ---- R5 secular trend
tr = df[df.acc_year.between(2021, 2025)].groupby(["issn", "acc_year"]).y.median().unstack(); out["R5_median_lnD_by_acc_year"] = tr.mean().to_dict(); out["R5_change_2021_to_2025_lnD"] = float((tr[2025] - tr[2021]).mean())
json.dump(out, open(f"{R}/revision_analyses_EXPLORATORY.json", "w"), indent=1, default=float); print(json.dumps(out, indent=1, default=float)[:5000])
