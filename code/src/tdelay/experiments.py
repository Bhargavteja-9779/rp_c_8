"""Experiments E1-E7 (protocol section 8). All functions are deterministic given cfg['seed']."""
import numpy as np, pandas as pd
from scipy import stats
from . import forecasters as F, scoring as S, stats as ST, variance as V, protocol as P

METHODS = ["F0", "F1", "F2", "F3", "F4", "F6"]

def _prep_origin(df, issn_member, t0, cfg):
    """Visible training summaries for every journal at origin t0 (visibility-only eligibility, deviation D2)."""
    t0 = pd.Timestamp(t0); per = {}
    for issn, dj in df.groupby("issn"):
        tr12, tr24, test = P.split_journal_origin(dj, t0, cfg)
        per[issn] = (tr12, tr24, test)
    summ = {i: (t[0]["y"].mean(), t[0]["y"].var(ddof=1), len(t[0])) for i, t in per.items() if len(t[0]) >= max(cfg["prior_min_n"], 2)}
    prior = F.EBPrior(*zip(*summ.values())) if len(summ) > 5 else None
    pools = {}
    for i, t in per.items():
        if len(t[0]) >= cfg["prior_min_n"]: pools.setdefault(issn_member[i], []).append(t[0]["y"].to_numpy())
    return per, prior, pools

def run_forecast_experiment(df, issn_member, cfg, apply_eligibility=None):
    """E3/E4/E6 core: returns (metrics rows DataFrame, PIT counts DataFrame, interval-only F5 rows)."""
    taus = np.asarray(cfg["taus"]); rows, pit_rows, f5_rows = [], [], []
    ia, ib = [int(np.argmin(abs(taus - a))) for a in (0.10, 0.90)]; ic, id_ = [int(np.argmin(abs(taus - a))) for a in (0.25, 0.75)]
    minTr, minTe = (apply_eligibility or (cfg["min_train"], cfg["min_test"]))
    rng = np.random.default_rng(cfg["seed"])
    for t0 in cfg["origins"]:
        per, prior, pools = _prep_origin(df, issn_member, t0, cfg); t0ts = pd.Timestamp(t0)
        pooled_fc = {m: F.pooled(v, taus) for m, v in pools.items()}
        for issn, (tr12, tr24, test) in per.items():
            if len(tr12) < minTr or len(test) < minTe: continue
            y12, y24, yt = tr12["y"].to_numpy(), tr24["y"].to_numpy(), test["y"].to_numpy()
            age24 = (t0ts - tr24["V"]).dt.days.to_numpy()
            fcs = {"F0": F.empirical(y12, taus), "F1": F.empirical(y24, taus), "F2": pooled_fc[issn_member[issn]],
                   "F3": F.lognormal_mle(y12, taus), "F4": prior.forecast(y12, taus),
                   "F6": F.decayed(y24, age24, cfg["decay_half_life_days"], taus)}
            for m, fc in fcs.items():
                r = dict(issn=issn, member=issn_member[issn], origin=t0, method=m, n_train=len(y12), n_test=len(yt),
                         pinball=S.mean_pinball(yt, fc.q, taus),
                         pinball_days=S.mean_pinball(np.exp(yt), np.exp(fc.q), taus),
                         cov80=S.interval_coverage(yt, fc.q[ia], fc.q[ib]), cov50=S.interval_coverage(yt, fc.q[ic], fc.q[id_]),
                         width80=float(fc.q[ib] - fc.q[ia]), winkler80=S.winkler(yt, fc.q[ia], fc.q[ib], 0.2),
                         median_fc_days=float(np.exp(fc.q[int(np.argmin(abs(taus - 0.5)))])), test_median_days=float(np.median(test['D'])))
                for T in cfg["thresholds_days"]:
                    ph = float(fc.cdf(np.log(T))); out = (test["D"].to_numpy() <= T).astype(float)
                    r[f"phat_{T}"] = ph; r[f"real_{T}"] = float(out.mean()); r[f"brier_{T}"] = S.brier(ph, out)
                rows.append(r)
                if m in ("F0", "F3", "F4"):
                    pit = (np.array([fc.cdf(v) for v in yt]) if m != "F0" else S.pit_ecdf(yt, y12, rng))
                    h, _ = np.histogram(pit, bins=10, range=(0, 1)); pit_rows.append(dict(issn=issn, origin=t0, method=m, **{f"b{k}": int(c) for k, c in enumerate(h)}))
            lo, hi = F.recent_holdout_interval(y12, (t0ts - tr12["V"]).dt.days.to_numpy())
            if not np.isnan(lo):
                f5_rows.append(dict(issn=issn, member=issn_member[issn], origin=t0, method="F5", n_train=len(y12), n_test=len(yt),
                                    cov80=S.interval_coverage(yt, lo, hi), width80=float(hi - lo), winkler80=S.winkler(yt, lo, hi, 0.2)))
    return pd.DataFrame(rows), pd.DataFrame(pit_rows), pd.DataFrame(f5_rows)

def per_journal(metrics, col):
    """Average a metric over origins within journal -> wide table journal x method."""
    return metrics.groupby(["issn", "method"])[col].mean().unstack("method")

def contrasts(metrics, cfg, col="pinball"):
    """Confirmatory paired contrasts (protocol section 7) with Holm correction and cluster-bootstrap CI of mean difference."""
    w = per_journal(metrics, col); pairs = [("F4", "F0"), ("F3", "F0"), ("F1", "F0"), ("F6", "F0"), ("F0", "F2"), ("F4", "F6"), ("F4", "F3")]
    out = []
    for a, b in pairs:
        d = (w[a] - w[b]).dropna(); t = ST.paired_wilcoxon(w[a].loc[d.index], w[b].loc[d.index])
        m, lo, hi = ST.cluster_bootstrap_mean(d.to_numpy(), B=cfg["bootstrap_B"], seed=cfg["seed"])
        rel = float(np.median((w[a].loc[d.index] - w[b].loc[d.index]) / w[b].loc[d.index]))
        out.append(dict(contrast=f"{a} - {b}", n_journals=t["n"], mean_diff=m, ci_lo=lo, ci_hi=hi, median_rel_diff=rel, rbc=t["rbc"], p=t["p"]))
    o = pd.DataFrame(out); o["p_holm"] = ST.holm(o["p"].to_numpy()); return o

def size_strata(metrics, cfg):
    """H3: F4 vs F0 by training-size stratum (per journal mean n_train across origins)."""
    n = metrics.groupby("issn")["n_train"].mean(); lo, hi = cfg["size_strata"]
    st = pd.cut(n, [0, lo, hi, np.inf], labels=[f"<{lo}", f"{lo}-{hi}", f">={hi}"], right=False)
    w = per_journal(metrics, "pinball"); res = []
    for s in st.cat.categories:
        ids = st.index[st == s]
        if len(ids) < 5: continue
        t = ST.paired_wilcoxon(w.loc[ids, "F4"], w.loc[ids, "F0"]); m, a, b = ST.cluster_bootstrap_mean((w.loc[ids, "F4"] - w.loc[ids, "F0"]).to_numpy(), cfg["bootstrap_B"], cfg["seed"])
        res.append(dict(stratum=s, n_journals=len(ids), mean_diff=m, ci_lo=a, ci_hi=b, p=t["p"], rbc=t["rbc"]))
    r = pd.DataFrame(res); r["p_holm"] = ST.holm(r["p"].to_numpy()) if len(r) else []; return r

def coverage_summary(metrics, f5, cfg):
    """H2: mean out-of-time coverage minus nominal, with cluster-bootstrap CI, per method."""
    out = []
    allm = pd.concat([metrics[["issn", "method", "origin", "cov80", "cov50", "width80", "winkler80"]], f5[["issn", "method", "origin", "cov80", "width80", "winkler80"]]])
    for m, g in allm.groupby("method"):
        pj = g.groupby("issn")["cov80"].mean(); a, lo, hi = ST.cluster_bootstrap_mean(pj.to_numpy() - 0.8, cfg["bootstrap_B"], cfg["seed"])
        c50 = g.groupby("issn")["cov50"].mean().mean() if "cov50" in g and g["cov50"].notna().any() else np.nan
        out.append(dict(method=m, n_journals=len(pj), cov80_minus_nominal=a, ci_lo=lo, ci_hi=hi, mean_cov50=c50, mean_width80=g["width80"].mean(), mean_winkler80=g["winkler80"].mean()))
    return pd.DataFrame(out)

def guarantee_feasibility(metrics, cfg, T=72):
    """H4/E6: realised P(D<=T) per journal-origin from the target cohort with Clopper-Pearson CIs (method-independent: use F0 rows)."""
    g = metrics[metrics.method == "F0"][["issn", "origin", "n_test", f"real_{T}"]].copy(); g["k"] = (g["n_test"] * g[f"real_{T}"]).round().astype(int)
    ci = g.apply(lambda r: ST.clopper_pearson(int(r.k), int(r.n_test)), axis=1); g["cp_lo"] = [c[0] for c in ci]; g["cp_hi"] = [c[1] for c in ci]
    res = []
    for thr in (0.5, 0.8, 0.9):
        k = int((g[f"real_{T}"] >= thr).sum()); n = len(g); lo, hi = ST.clopper_pearson(k, n)
        res.append(dict(T=T, threshold=thr, n_journal_origins=n, k=k, share=k / n, cp_lo=lo, cp_hi=hi,
                        k_lowerbound=int((g.cp_lo >= thr).sum())))
    return pd.DataFrame(res), g

def reliability_table(metrics, T=72, method="F0", bins=(0, .05, .2, .4, .6, .8, .95, 1.0001)):
    m = metrics[metrics.method == method]; b = pd.cut(m[f"phat_{T}"], list(bins), right=False)
    return m.groupby(b, observed=True).agg(n=("issn", "size"), mean_forecast=(f"phat_{T}", "mean"), mean_realised=(f"real_{T}", "mean")).reset_index()

def brier_skill(metrics, T=72):
    w = per_journal(metrics, f"brier_{T}"); return (1 - w.mean() / w["F2"].mean()).rename("brier_skill_vs_F2")

def variance_components(df, cfg, B=None):
    d = df[df["acc_year"].isin(cfg["vc_years"])]
    d = V.capped_sample(d, cfg["vc_cap_per_journal_year"], cfg["seed"])
    cells = V.cell_table(d); est = V.components(cells)
    B = cfg["bootstrap_B"] if B is None else B; rng = np.random.default_rng(cfg["seed"]); js = cells["issn"].unique()
    byj = {j: c for j, c in cells.groupby("issn")}; boots = []
    for _ in range(min(B, 1000)):
        pick = rng.choice(js, len(js)); c = pd.concat([byj[j].assign(issn=f"{j}_{k}") for k, j in enumerate(pick)]); boots.append(V.components(c))
    bd = pd.DataFrame(boots); ci = {k: (float(bd[k].quantile(.025)), float(bd[k].quantile(.975))) for k in ["icc_journal", "icc_journal_year", "sigma2_journal", "sigma2_year", "sigma2_resid"]}
    return est, ci

def drift_analysis(df, cfg, seed=None):
    """E5 (exploratory): year-to-year change in journal median ln D vs permutation-null sampling variance."""
    rng = np.random.default_rng(cfg["seed"] if seed is None else seed); rows = []
    for issn, dj in df[df.acc_year.between(2021, 2025)].groupby("issn"):
        by = {k: g["y"].to_numpy() for k, g in dj.groupby("acc_year") if len(g) >= 50}
        for k in sorted(by):
            if k + 1 in by:
                a, b = by[k], by[k + 1]; d = np.median(b) - np.median(a); u = np.concatenate([a, b]); nulls = []
                for _ in range(200):
                    p = rng.permutation(u); nulls.append(np.median(p[len(a):]) - np.median(p[:len(a)]))
                rows.append(dict(issn=issn, year=k, delta=d, null_var=float(np.var(nulls)), n_a=len(a), n_b=len(b)))
    r = pd.DataFrame(rows); return r

def article_level_experiment(df, issn_member, cfg, metrics, n_folds=5):
    """E7: does adding article covariates improve quantile forecasts over the journal-level F4 quantile? Grouped CV by journal."""
    import lightgbm as lgb
    from sklearn.model_selection import GroupKFold
    taus5 = [0.1, 0.25, 0.5, 0.75, 0.9]; taus = np.asarray(cfg["taus"]); recs = []
    for t0 in cfg["origins"]:
        per, prior, _ = _prep_origin(df, issn_member, t0, cfg)
        for issn, (tr12, tr24, test) in per.items():
            if len(tr12) < cfg["min_train"] or len(test) < cfg["min_test"]: continue
            fc = prior.forecast(tr12["y"].to_numpy(), taus); t = test.copy()
            for tau in taus5: t[f"q{tau}"] = fc.q[int(np.argmin(abs(taus - tau)))]
            t["origin"] = t0; recs.append(t)
    d = pd.concat(recs, ignore_index=True)
    d["rec_month"] = d["received"].dt.month; d["rec_wd"] = d["received"].dt.weekday; d["lref"] = np.log1p(d["n_refs"].fillna(d["n_refs"].median()))
    d["n_authors"] = d["n_authors"].fillna(d["n_authors"].median())
    feats = ["n_authors", "rec_month", "rec_wd", "lref"]; groups = d["issn"].to_numpy(); gkf = GroupKFold(n_splits=n_folds)
    res = {}
    for tau in taus5:
        base = np.zeros(len(d)); ctrl = np.zeros(len(d)); cov = np.zeros(len(d))
        for tr, te in gkf.split(d, groups=groups):
            for name, cols, store in (("ctrl", [f"q{tau}"], ctrl), ("cov", [f"q{tau}"] + feats, cov)):
                m = lgb.LGBMRegressor(objective="quantile", alpha=tau, n_estimators=200, max_depth=3, learning_rate=0.05, verbose=-1, random_state=cfg["seed"], n_jobs=2)
                m.fit(d.iloc[tr][cols], d.iloc[tr]["y"]); store[te] = m.predict(d.iloc[te][cols])
        d[f"pred_ctrl_{tau}"] = ctrl; d[f"pred_cov_{tau}"] = cov
        yv = d["y"].to_numpy(); b = d[f"q{tau}"].to_numpy()
        res[tau] = dict(base=S.pinball(yv, b, tau), ctrl=S.pinball(yv, ctrl, tau), cov=S.pinball(yv, cov, tau))
    r = pd.DataFrame(res).T; r["rel_gain_cov_vs_base"] = 1 - r["cov"] / r["base"]; r["rel_gain_cov_vs_ctrl"] = 1 - r["cov"] / r["ctrl"]
    pooled = dict(base=r["base"].mean(), ctrl=r["ctrl"].mean(), cov=r["cov"].mean()); pooled["rel_gain_cov_vs_base"] = 1 - pooled["cov"] / pooled["base"]; pooled["rel_gain_cov_vs_ctrl"] = 1 - pooled["cov"] / pooled["ctrl"]
    return r, pooled, d

def article_level_ci(d, cfg, taus5=(0.1, 0.25, 0.5, 0.75, 0.9)):
    """Journal-cluster bootstrap CI for the pooled relative pinball gain of covariates vs journal-only F4 (H5) and vs the learner-only control."""
    loss = {}
    for k in ("base", "ctrl", "cov"):
        cols = []
        for t in taus5:
            pred = d[f"q{t}"] if k == "base" else d[f"pred_{k}_{t}"]
            dd = d["y"] - pred; cols.append(np.maximum(t * dd, (t - 1) * dd))
        loss[k] = pd.concat(cols, axis=1).mean(axis=1)
    g = pd.DataFrame(loss).assign(issn=d["issn"].to_numpy()).groupby("issn").mean()
    arr = [tuple(r) for r in g[["base", "ctrl", "cov"]].to_numpy()]
    fn = lambda items: (lambda a: (1 - a[:, 2].mean() / a[:, 0].mean(), 1 - a[:, 2].mean() / a[:, 1].mean()))(np.array(items))
    rng = np.random.default_rng(cfg["seed"]); reps = []
    for _ in range(min(cfg["bootstrap_B"], 2000)):
        idx = rng.integers(0, len(arr), len(arr)); reps.append(fn([arr[i] for i in idx]))
    reps = np.array(reps); est = fn(arr)
    return dict(rel_gain_vs_base=est[0], ci_vs_base=[float(np.quantile(reps[:, 0], .025)), float(np.quantile(reps[:, 0], .975))],
                rel_gain_vs_ctrl=est[1], ci_vs_ctrl=[float(np.quantile(reps[:, 1], .025)), float(np.quantile(reps[:, 1], .975))], n_journals=len(arr))
