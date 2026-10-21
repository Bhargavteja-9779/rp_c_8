"""Cycle-2 experiments X4 (dependence-robust checks), X5 (data-quality exclusions), X6 (calibrated event probabilities). Specified in revised_experimental_protocol.md before running."""
import json, sys, os
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from tdelay import experiments as E, forecasters as F, scoring as S, stats as ST, variance as V
ROOT = "/home/user/rp_c_8"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); OUT = f"{ROOT}/reinforced/results"; B = 5000; seed = cfg["seed"]; rng = np.random.default_rng(seed)
met = pd.read_csv(f"{ROOT}/results/metrics_journal_origin.csv"); m4 = pd.read_csv(f"{ROOT}/results/revision_R1_metrics_4origins_EXPLORATORY.csv")
fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; res = {}
def summarize(m, tag, strat=False):
    w = m.groupby(["issn", "method"]).pinball.mean().unstack(); mem = pd.Series({i: member[i] for i in w.index}); cov = m[m.method == "F0"].groupby("issn").cov80.mean().sub(0.8)
    def boot(vals, groups):
        out = []
        for _ in range(B):
            idx = np.concatenate([rng.choice(np.where(groups == g)[0], (groups == g).sum()) for g in np.unique(groups)]) if strat else rng.integers(0, len(vals), len(vals))
            out.append(vals[idx].mean())
        return float(vals.mean()), float(np.quantile(out, .025)), float(np.quantile(out, .975))
    d = {}
    for name, v in (("F0_cov80_minus_nominal", cov), ("F4_minus_F0", (w.F4 - w.F0).dropna()), ("F0_minus_F2", (w.F0 - w.F2).dropna()), ("F6_minus_F0", (w.F6 - w.F0).dropna())):
        g = mem.loc[v.index].to_numpy(); d[name] = dict(zip(["est", "lo", "hi"], boot(v.to_numpy(), g)))
    d["n_journals"] = int(len(w)); d["skill_F0_vs_F2"] = float(1 - w.F0.mean() / w.F2.mean()); res[tag] = d
# X4a single origin 2024 (target cohort does not overlap any later training window used here)
summarize(met[met.origin == "2024-01-01"], "X4a_single_origin_2024"); summarize(met[met.origin == "2023-01-01"], "X4a_single_origin_2023")
# X4b stratified (within-publisher) bootstrap, and leave-one-publisher-out point estimates
summarize(met, "X4b_stratified_bootstrap_all", strat=True)
for p in ["Springer Nature", "Wiley", "Taylor & Francis"]:
    summarize(met[met.issn.map(member) != p], f"X4b_leave_out_{p}")
# ICC leave-one-publisher-out
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); df["acc_year"] = df.accepted.dt.year; df = df[df.issn.isin(member)]
d5 = df[df.acc_year.isin(cfg["vc_years"])]; icc = {}
for p in [None, "Springer Nature", "Wiley", "Taylor & Francis"]:
    x = d5 if p is None else d5[d5.issn.map(member) != p]; c = V.cell_table(V.capped_sample(x, cfg["vc_cap_per_journal_year"], seed)); icc["all" if p is None else f"without {p}"] = V.components(c)["icc_journal"]
res["X4b_ICC_leave_one_publisher_out"] = icc
# X5 flagged journals
flag = set(); g = df[df.acc_year.between(2021, 2025)].groupby(["issn", "acc_year"]).D.agg(med="median", p10=lambda x: (x <= 10).mean())
flag |= set(g[(g.p10 > 0.10) | (g.med <= 30)].reset_index().issn); json.dump(sorted(flag), open(f"{OUT}/X5_flagged_journals.json", "w"))
summarize(met[~met.issn.isin(flag)], "X5_excluding_flagged"); res["X5_n_flagged"] = len(flag)
gg = met[(met.method == "F0") & ~met.issn.isin(flag)]; res["X5_share_P72_ge_0_5"] = float((gg.real_72 >= .5).mean()); res["X5_share_P72_ge_0_8"] = float((gg.real_72 >= .8).mean())
d5x = d5[~d5.issn.isin(flag)]; res["X5_ICC_excl_flagged"] = V.components(V.cell_table(V.capped_sample(d5x, cfg["vc_cap_per_journal_year"], seed)))["icc_journal"]
# X6 calibrated event probabilities (map from earlier cohorts only; same ordering as X2)
tabs = {}
for t0 in ["2022-01-01", "2023-01-01"]:
    per, _, _ = E._prep_origin(df, member, t0, cfg); rows = []
    for i, (tr12, tr24, te) in per.items():
        if len(tr12) >= cfg["min_train"] and len(te) >= cfg["min_test"]: rows.append((tr12.y.to_numpy(), te.y.to_numpy()))
    tabs[t0] = rows
def Gmap(origins):
    P, W = [], []
    for o in origins:
        for ytr, yte in tabs[o]:
            p = S.pit_ecdf(yte, ytr, rng); P.append(p); W.append(np.full(len(p), 1 / len(p)))
    P = np.concatenate(P); W = np.concatenate(W); o = np.argsort(P); return P[o], np.cumsum(W[o]) / W.sum()
x6 = {}
for t_test, orig in (("2024-01-01", ["2022-01-01"]), ("2025-01-01", ["2022-01-01", "2023-01-01"])):
    P, C = Gmap(orig); m = m4[(m4.method == "F0") & (m4.origin == t_test)].copy()
    for T in cfg["thresholds_days"]:
        p = m[f"phat_{T}"].to_numpy(); o = m[f"real_{T}"].to_numpy(); pc = np.interp(p, P, C, left=0, right=1)       # calibrated probability G(u)
        br = lambda q: q ** 2 - 2 * q * o + o                                                                    # exact per-journal Brier for binary outcomes with realised share o
        d = pd.Series(br(pc) - br(p), index=m.issn.to_numpy()); pj = d.groupby(level=0).mean(); mm, lo, hi = ST.cluster_bootstrap_mean(pj.to_numpy(), B, seed)
        w = np.ones(len(p)); sl = lambda q: np.polyfit(q, o, 1)
        x6[f"{t_test}_T{T}"] = dict(brier_raw=float(br(p).mean()), brier_cal=float(br(pc).mean()), diff_cal_minus_raw=dict(est=mm, lo=lo, hi=hi), slope_raw=float(sl(p)[0]), slope_cal=float(sl(pc)[0]), n=int(len(p)))
res["X6_calibrated_event_probabilities"] = x6
json.dump(res, open(f"{OUT}/X4_X5_X6_summary.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float)[:6500])
