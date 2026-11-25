"""Part C experiments Z1-Z6 (specified in revised_experimental_protocol.md Part C before running). Separate seeded generators per experiment."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from scipy import stats
from tdelay import experiments as E, forecasters as F, scoring as S, stats as ST
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); SEED = cfg["seed"]; res = {}
df0 = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df0 = df0[df0.issn.isin(member)].copy()
imprint = pd.read_csv(f"{OUT}/journal_imprint_map.csv", index_col=0).iloc[:, 0]; met = pd.read_csv(f"{ROOT}/results/metrics_journal_origin.csv"); f0 = met[met.method == "F0"]
taus9 = np.array([.1, .2, .3, .4, .5, .6, .7, .8, .9]); H = 91; CAP = 480
# ------------------------------------------------------------- Z1 generative null with random cohort effects
rng = np.random.default_rng(SEED + 1); sig_jy = json.load(open(f"{ROOT}/results/variance_components.json"))["estimate"]["sigma2_year"]
dr = pd.read_csv(f"{ROOT}/results/drift_pairs.csv"); jp = dr.groupby("issn").apply(lambda g: max(0.0, (np.mean(g.delta ** 2) - np.mean(g.null_var)) / 2), include_groups=False)
rows = []
for t0 in cfg["origins"]:
    per, _, _ = E._prep_origin(df0, member, t0, cfg)
    for i, (tr12, tr24, te) in per.items():
        if len(tr12) < 100 or len(te) < 50: continue
        ytr = tr12.y.to_numpy(); resid = ytr - ytr.mean(); ntr, nte = len(tr12), len(te); r = {"issn": i, "origin": t0}
        for tag, sv, mode in (("base_visible", sig_jy, "vis"), ("half_visible", sig_jy * .5, "vis"), ("double_visible", sig_jy * 2, "vis"), ("base_oracle", sig_jy, "orc"), ("journal_proxy_visible", float(jp.get(i, sig_jy)), "vis")):
            cs = []
            for _ in range(20):
                a = rng.normal(0, np.sqrt(sv)) if mode == "vis" else 0.0; b = rng.normal(0, np.sqrt(sv)) if mode == "vis" else rng.normal(0, np.sqrt(sv * 0.5))
                tr = rng.choice(resid, ntr) + a; tt = rng.choice(resid, nte) + b; q = F.wquantile(tr, np.ones(ntr), [.1, .9]); cs.append(S.interval_coverage(tt, q[0], q[1]))
            r[tag] = np.mean(cs) - 0.8
        r["obs"] = float(f0[(f0.issn == i) & (f0.origin == t0)].cov80.iloc[0] - 0.8); rows.append(r)
Z1 = pd.DataFrame(rows); Z1.to_csv(f"{OUT}/Z1_cohort_effect_null.csv", index=False); z1 = {}
for k in ["obs", "base_visible", "half_visible", "double_visible", "base_oracle", "journal_proxy_visible"]:
    pj = Z1.groupby("issn")[k].mean(); z1[k] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(pj.to_numpy(), 3000, SEED)))
pj = Z1.groupby("issn")[["obs", "journal_proxy_visible", "base_visible"]].mean(); z1["corr_obs_vs_proxy_sim_journal_level"] = float(pj.obs.corr(pj.journal_proxy_visible)); z1["corr_obs_vs_base_sim"] = float(pj.obs.corr(pj.base_visible))
z1["by_imprint_obs_vs_base_sim"] = Z1.assign(imprint=Z1.issn.map(imprint)).groupby("imprint")[["obs", "base_visible"]].mean().round(4).to_dict(); z1["sigma2_jy_used"] = sig_jy
sd_obs = Z1.obs.std(); z1["sd_obs_journal_origin"] = float(sd_obs); z1["sd_sim_base_journal_origin"] = float(Z1.base_visible.std()); res["Z1"] = z1
# ------------------------------------------------------------- Z2 strict recalibration, variance inflation baseline, F4, event probabilities
rng2 = np.random.default_rng(SEED + 2); df = df0.copy(); df["D"] = df.D.clip(upper=CAP); df["y"] = np.log(df.D.astype(float)); c = dict(cfg, horizon_days=H)
origins = list(pd.date_range("2022-01-01", "2024-04-01", freq="QS").strftime("%Y-%m-%d")); store = {}; rows = []
def complete(o, t0): return pd.Timestamp(o) + pd.Timedelta(days=H + CAP) <= pd.Timestamp(t0)
for t0 in origins:
    per, prior, pools = E._prep_origin(df, member, t0, c); T0 = pd.Timestamp(t0); pooled = {m: F.pooled(v, taus9) for m, v in pools.items()}; items = []
    for i, (tr12, tr24, te) in per.items():
        if len(tr12) < 100 or len(te) < 30: continue
        items.append((i, tr12.y.to_numpy(), te.y.to_numpy(), te["D"].to_numpy())); 
    store[t0] = dict(items=items, prior=prior, pooled=pooled)
    P, W = [], []
    for i, ytr, yte, _ in items: p = S.pit_ecdf(yte, ytr, rng2); P.append(p); W.append(np.full(len(p), 1 / len(p)))
    store[t0]["pit"] = (np.concatenate(P), np.concatenate(W))
    use = [o for o in origins if complete(o, t0) and o in store and o != t0]; G = None; cscale = None
    if use:
        Pp = np.concatenate([store[o]["pit"][0] for o in use]); Ww = np.concatenate([store[o]["pit"][1] for o in use]); k = np.argsort(Pp); G = (Pp[k], np.cumsum(Ww[k]) / Ww.sum())
        # variance-inflation factor learned from the same earlier complete origins: multiply (q - median) by c to reach 80% pooled coverage
        def covc(cc):
            v = []
            for o in use:
                for i, ytr, yte, _ in store[o]["items"]:
                    q = F.wquantile(ytr, np.ones(len(ytr)), [.1, .5, .9]); lo, hi = q[1] + cc * (q[0] - q[1]), q[1] + cc * (q[2] - q[1]); v.append(np.mean((yte >= lo) & (yte <= hi)))
            return np.mean(v)
        grid = np.linspace(1.0, 1.4, 17); cscale = float(grid[np.argmin([abs(covc(x) - 0.8) for x in grid])])
    if G is None: continue
    for i, ytr, yte, Dte in items:
        q0 = F.wquantile(ytr, np.ones(len(ytr)), taus9); lv = [float(np.interp(t, G[1], G[0])) for t in taus9]; qr = F.wquantile(ytr, np.ones(len(ytr)), [min(max(l, .005), .995) for l in lv])
        qv = q0[4] + cscale * (q0 - q0[4]); q4 = prior.forecast(ytr, taus9).q if prior is not None else q0; q2 = store[t0]["pooled"][member[i]].q
        base = dict(origin=t0, issn=i, imprint=imprint.get(i, "other"), n_test=len(yte), cscale=cscale)
        for m, q in (("F0", q0), ("R", qr), ("V", qv), ("F4", q4), ("F2", q2)): rows.append(dict(**base, method=m, pinball=S.mean_pinball(yte, q, taus9), cov80=S.interval_coverage(yte, q[0], q[-1])))
        for T in cfg["thresholds_days"]:
            p = float((ytr <= np.log(T)).mean()); pc_ = float(np.interp(p, G[0], G[1], left=0, right=1)); o = float((Dte <= T).mean()); rows.append(dict(**base, method=f"ev{T}", pinball=np.nan, cov80=np.nan, p_raw=p, p_cal=pc_, realised=o))
Z2 = pd.DataFrame(rows); Z2.to_csv(f"{OUT}/Z2_strict_recal.csv", index=False); z2 = {"evaluation_origins": sorted(Z2.origin.unique().tolist()), "cscale_by_origin": Z2.groupby("origin").cscale.first().round(3).to_dict()}
ev = Z2[Z2.method.isin(["F0", "R", "V", "F4", "F2"])]; w = ev.groupby(["issn", "method"]).pinball.mean().unstack()
for m in ("R", "V", "F4", "F2"):
    pj = ev[ev.method == m].groupby("issn").cov80.mean().sub(0.8); z2[f"{m}_shortfall"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(pj.to_numpy(), 3000, SEED)))
    d = (w[m] - w["F0"]).dropna(); z2[f"{m}_pinball_minus_F0"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(d.to_numpy(), 3000, SEED)))
pj = ev[ev.method == "F0"].groupby("issn").cov80.mean().sub(0.8); z2["F0_shortfall"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(pj.to_numpy(), 3000, SEED))); z2["by_origin_cov_minus_80"] = ev.groupby(["origin", "method"]).cov80.mean().sub(0.8).unstack().round(4).to_dict()
for T in cfg["thresholds_days"]:
    e = Z2[Z2.method == f"ev{T}"].copy(); br = lambda p, o: p ** 2 - 2 * p * o + o; e["d"] = br(e.p_cal, e.realised) - br(e.p_raw, e.realised); pj = e.groupby("issn").d.mean()
    slopes = []; ids = e.issn.unique(); g_ = {k: v for k, v in e.groupby("issn")}
    for _ in range(1000):
        pick = rng2.choice(ids, len(ids)); x = pd.concat([g_[k] for k in pick]); slopes.append((np.polyfit(x.p_raw, x.realised, 1)[0], np.polyfit(x.p_cal, x.realised, 1)[0]))
    s = np.array(slopes); z2[f"brier_T{T}"] = dict(raw=float(br(e.p_raw, e.realised).mean()), cal=float(br(e.p_cal, e.realised).mean()), diff=dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(pj.to_numpy(), 3000, SEED))),
                                                   slope_raw=float(np.polyfit(e.p_raw, e.realised, 1)[0]), slope_raw_ci=[float(np.quantile(s[:, 0], .025)), float(np.quantile(s[:, 0], .975))], slope_cal=float(np.polyfit(e.p_cal, e.realised, 1)[0]), slope_cal_ci=[float(np.quantile(s[:, 1], .025)), float(np.quantile(s[:, 1], .975))], n=int(len(e)))
res["Z2"] = z2
# ------------------------------------------------------------- Z3 imprint t(6) intervals, publisher-level check, Holm
y0 = json.load(open(f"{OUT}/Y0_imprint_inference.json")); z3 = {}; pubmap = {"Springer": "SpringerNature", "BMC": "SpringerNature", "Nature": "SpringerNature", "Wiley": "Wiley", "Blackwell": "Wiley", "T&F": "T&F", "other": "other"}; ps = []
tq = stats.t.ppf(.975, 6)
for k in ["F4-F0", "F3-F0", "F1-F0", "F6-F0", "F0-F2", "F4-F6", "F4-F3", "F0_shortfall_journal_mean_imprint_cluster"]:
    m = np.array(list(y0[k]["imprint_means"].values())); se = m.std(ddof=1) / np.sqrt(len(m)); r = dict(mean_of_imprint_means=float(m.mean()), t6_ci=[float(m.mean() - tq * se), float(m.mean() + tq * se)], p_t=float(stats.ttest_1samp(m, 0).pvalue))
    pubm = pd.Series(y0[k]["imprint_means"]).groupby(pd.Series(y0[k]["imprint_means"]).index.map(pubmap)).mean(); pubm = pubm[pubm.index != "other"]; r["publisher_means"] = pubm.round(5).to_dict(); r["publishers_same_sign"] = int(max((pubm > 0).sum(), (pubm < 0).sum())); r["publisher_level_p_t2"] = float(stats.ttest_1samp(pubm.to_numpy(), 0).pvalue); z3[k] = r
pv = [z3[k]["p_t"] for k in ["F4-F0", "F3-F0", "F1-F0", "F6-F0", "F0-F2", "F4-F6", "F4-F3"]]; adj = ST.holm(pv)
for k, a in zip(["F4-F0", "F3-F0", "F1-F0", "F6-F0", "F0-F2", "F4-F6", "F4-F3"], adj): z3[k]["p_t_holm"] = float(a)
res["Z3"] = z3
# ------------------------------------------------------------- Z4 X1 journal-weighted and by-year
d = pd.read_csv(f"{OUT}/preprint_probe.csv.partial").drop_duplicates("doi"); d["received"] = pd.to_datetime(d.received, format="mixed", errors="coerce"); d["posted"] = pd.to_datetime(d.preprint_posted, errors="coerce"); d["delta"] = (d.received - d.posted).dt.days
rs = d[(d.preprint_doi.str.startswith("10.21203")) & (d.member == "Springer Nature")].copy(); rs["le14"] = rs.delta <= 14; rs["gt90"] = rs.delta > 90; jw = rs.groupby("issn").agg(le14=("le14", "mean"), gt90=("gt90", "mean"), n=("doi", "size"))
met_fast = set(f0[(f0.test_median_days <= 60) | (f0.median_fc_days <= 60)].issn)
z4 = dict(articles=int(len(rs)), journals=int(len(jw)), paper_weighted_le14=float(rs.le14.mean()), journal_weighted_le14=float(jw.le14.mean()), journal_weighted_gt90=float(jw.gt90.mean()), journal_weighted_le14_fastlooking=float(jw[jw.index.isin(met_fast)].le14.mean()), n_fast_journals=int(jw.index.isin(met_fast).sum()),
          median_delta_by_received_year=rs.groupby(rs.received.dt.year).delta.median().to_dict(), share_le14_by_received_year=rs.groupby(rs.received.dt.year).le14.mean().round(3).to_dict(), n_by_year=rs.groupby(rs.received.dt.year).size().to_dict(), resolution_note="a systematic shift of up to 14 days cannot be excluded (about 11% of median D)")
res["Z4"] = z4
# ------------------------------------------------------------- Z5 backward oracle and pre-origin-only eligibility
z5 = {}
for t0 in ["2022-01-01", "2023-01-01"]:
    T0 = pd.Timestamp(t0); per, _, _ = E._prep_origin(df0, member, t0, cfg); rowsb = []
    for i, d_ in df0.groupby("issn"):
        if i not in per: continue
        tr12, tr24, te = per[i]
        if len(tr12) < 100 or len(te) < 50: continue
        fwd = d_[(d_.received >= T0 - pd.Timedelta(days=365)) & (d_.received < T0)].y.to_numpy(); bwd = d_[(d_.received >= T0 + pd.Timedelta(days=182)) & (d_.received < T0 + pd.Timedelta(days=547))].y.to_numpy(); yt = te.y.to_numpy()
        if len(fwd) < 50 or len(bwd) < 50: continue
        cov = lambda tr: S.interval_coverage(yt, *F.wquantile(tr, np.ones(len(tr)), [.1, .9]))
        rowsb.append(dict(issn=i, fwd=cov(fwd) - .8, bwd=cov(bwd) - .8, vis=cov(tr12.y.to_numpy()) - .8))
    B_ = pd.DataFrame(rowsb); z5[t0] = {k: dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(B_[k].to_numpy(), 3000, SEED))) for k in ("vis", "fwd", "bwd")}; z5[t0]["n_journals"] = int(len(B_))
m10, _, _ = E.run_forecast_experiment(df0, member, cfg, (100, 10)); g10 = m10[m10.method == "F0"].groupby("issn").cov80.mean().sub(0.8); z5["eligibility_pre_origin_only_n_test_ge_10"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(g10.to_numpy(), 3000, SEED))); z5["eligibility_pre_origin_only_n_journals"] = int(len(g10)); res["Z5"] = z5
# ------------------------------------------------------------- Z6 moving-block bootstrap over ordered panel origins
P1 = pd.read_csv(f"{OUT}/Y1_panel_metrics.csv"); om = (P1[P1.method == "F0"].groupby("origin").cov80.mean() - 0.8).to_numpy(); rng6 = np.random.default_rng(SEED + 6); L_ = 3; nb = int(np.ceil(len(om) / L_)); reps = []
for _ in range(5000):
    st = rng6.integers(0, len(om) - L_ + 1, nb); x = np.concatenate([om[s:s + L_] for s in st])[:len(om)]; reps.append(x.mean())
r1 = np.corrcoef(om[:-1], om[1:])[0, 1]; res["Z6"] = dict(origin_means=om.tolist(), pooled=float(om.mean()), moving_block_ci=[float(np.quantile(reps, .025)), float(np.quantile(reps, .975))], lag1_autocorr=float(r1), spearman_first8_vs_time=float(stats.spearmanr(range(8), om[:8])[0]))
json.dump(res, open(f"{OUT}/Z_summary.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float)[:9000])
