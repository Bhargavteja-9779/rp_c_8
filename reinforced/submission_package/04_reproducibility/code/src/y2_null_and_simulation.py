"""Y2: (b) exchangeable benchmark (random split inside the complete submission cohort at observed sizes) and (c) generative no-drift simulation with observed volume growth and the visibility rule."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from tdelay import experiments as E, forecasters as F, scoring as S, stats as ST
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); rng = np.random.default_rng(cfg["seed"])
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)].copy()
lag = float(np.median((df.V - df.accepted).dt.days)); res = {"median_accept_to_online_lag_days": lag}
rows = []
for t0 in cfg["origins"]:
    per, _, _ = E._prep_origin(df, member, t0, cfg); T0 = pd.Timestamp(t0); g_all = {i: d for i, d in df.groupby("issn")}
    for i, (tr12, tr24, te) in per.items():
        if len(tr12) < 100 or len(te) < 50: continue
        ntr, nte = len(tr12), len(te); yv, yt = tr12.y.to_numpy(), te.y.to_numpy(); d = g_all[i]
        cov_vis = S.interval_coverage(yt, *F.wquantile(yv, np.ones(len(yv)), [.1, .9]))
        # (b) exchangeable benchmark: complete submission cohort received in [t0-365, t0+182)
        pool = d[(d.received >= T0 - pd.Timedelta(days=365)) & (d.received < T0 + pd.Timedelta(days=182))].y.to_numpy(); cb = np.nan
        if len(pool) >= 60:
            k = len(pool); a = max(int(round(k * ntr / (ntr + nte))), 20); perm = rng.permutation(k); tr, te2 = pool[perm[:a]], pool[perm[a:]]
            if len(te2) >= 20: cb = S.interval_coverage(te2, *F.wquantile(tr, np.ones(len(tr)), [.1, .9]))
        # (c) generative no-drift simulation: true ln D distribution = this journal's target cohort; arrivals grow at the journal's observed annual rate
        prev = d[(d.V >= T0 - pd.Timedelta(days=730)) & (d.V < T0 - pd.Timedelta(days=365))]; gr = float(np.clip(np.log(max(ntr, 1) / max(len(prev), 1)), -0.7, 1.0)); cs = []
        for _ in range(12):
            span_days = 1095 + 182; t_rel = np.linspace(-1095, 182, 2000); lam = np.exp(gr * t_rel / 365); lam = lam / lam.sum()
            rate_target = nte / (lam[t_rel >= 0].sum() + 1e-12); n_arr = rng.poisson(rate_target); s = rng.choice(t_rel, n_arr, p=lam) + rng.random(n_arr)
            Dsim = np.exp(rng.choice(yt, n_arr)); acc = s + Dsim; vis = (acc < 0) & (acc + lag < 0) & (acc + lag >= -365); tg = (s >= 0) & (s < 182)
            if vis.sum() >= 30 and tg.sum() >= 30: cs.append(S.interval_coverage(np.log(Dsim[tg]), *F.wquantile(np.log(Dsim[vis]), np.ones(vis.sum()), [.1, .9])))
        rows.append(dict(issn=i, origin=t0, cov_visible=cov_vis, cov_exchangeable=cb, cov_sim_nodrift=np.mean(cs) if cs else np.nan, growth=gr))
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/Y2_null_sim.csv", index=False)
for k in ("cov_visible", "cov_exchangeable", "cov_sim_nodrift"):
    pj = R.groupby("issn")[k].mean().dropna().sub(0.8); res[k] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(pj.to_numpy(), 5000, cfg["seed"]))); res[k]["n_journals"] = int(len(pj))
both = R.dropna(subset=["cov_visible", "cov_sim_nodrift"]); res["paired_visible_minus_sim"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(both.groupby("issn").apply(lambda g: (g.cov_visible - g.cov_sim_nodrift).mean(), include_groups=False).to_numpy(), 5000, cfg["seed"])))
res["corr_visible_vs_sim_across_journal_origins"] = float(both.cov_visible.corr(both.cov_sim_nodrift)); res["corr_shortfall_vs_growth"] = float(R.cov_visible.corr(R.growth)); res["sim_shortfall_vs_growth_corr"] = float(R.cov_sim_nodrift.corr(R.growth))
json.dump(res, open(f"{OUT}/Y2_summary.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float))
