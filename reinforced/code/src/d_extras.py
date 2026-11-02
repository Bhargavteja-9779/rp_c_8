"""Post-hoc robustness analyses requested by the adversarial review of the cycle-3 manuscript (NOT in the Part D protocol; all labelled exploratory):
exchangeable-null noise floor, paper-weighted coverage, win/tie/loss of CV0 vs F0, tau=0 ablation, Brier-type CIs, external outlier-journal sensitivity, per-publisher table."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
from d_lib import *
sys.path.insert(0, "/home/user/rp_c_8/code/src")
from tdelay import stats as ST
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); SEED = cfg["seed"] + 77; rng = np.random.default_rng(SEED)
D = pd.read_csv(f"{OUT}/D_panel_rows.csv"); res = {}
f0 = D[D.method == "F0"].set_index(["origin", "issn"]); cv = D[D.method == "CV0"].set_index(["origin", "issn"])
# paper-weighted signed coverage
for m in ("F0", "CV0", "V", "R", "CVb"):
    d = D[D.method == m]; res[f"paper_weighted_signed_{m}"] = float(np.average(d.cov80 - .8, weights=d.n_te))
# win / tie / loss at journal-origin level
a = (f0.cov80 - .8).abs(); b = (cv.cov80 - .8).abs(); dd = (b - a).dropna(); res["winloss_CV0_vs_F0"] = dict(better=float((dd < -1e-9).mean()), tie=float((dd.abs() <= 1e-9).mean()), worse=float((dd > 1e-9).mean()), n=int(len(dd)))
# per-publisher table (signed and abs)
res["by_publisher"] = {m: D[D.method == m].groupby("pub").apply(lambda g: dict(signed=float((g.cov80 - .8).mean()), abs=float((g.cov80 - .8).abs().mean())), include_groups=False).to_dict() for m in ("F0", "CV0", "CVg", "V")}
# Brier-type CI (MSE between forecast probability and realised share), journal-cluster bootstrap of CV0 - F0
for T in (72, 120, 180):
    x = {m: D[D.method == m].assign(se=lambda d: (d[f"p{T}"] - d[f"o{T}"]) ** 2).groupby("issn").se.mean() for m in ("F0", "CV0", "CVb")}
    res[f"brier_diff_CV0_minus_F0_T{T}"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean((x["CV0"] - x["F0"]).dropna().to_numpy(), 3000, SEED))); res[f"brier_diff_CVb_minus_F0_T{T}"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean((x["CVb"] - x["F0"]).dropna().to_numpy(), 3000, SEED)))
# store for ablation and exchangeable null (cap 480 primary origins)
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)].copy()
df["D"] = df.D.clip(upper=CAP); df["y"] = np.log(df.D.astype(float)); eval_origins = sorted(D.origin.unique()); store = build_store(df, member, eval_origins, cfg); params = json.load(open(f"{OUT}/D_params_by_origin.json"))
rows = []; nul = []
for o in eval_origins:
    for it in store[o]:
        ytr, y = it["ytr"], it["yte"]; n = len(ytr); h0 = np.sqrt(ytr.var(ddof=1) / n); q = smoothed_quantiles(ytr, h0)
        rows.append(dict(origin=o, issn=it["issn"], method="CVtau0", cov80=float(np.mean((y >= q[0]) & (y <= q[-1]))), pinball=S.mean_pinball(y, q, TAUS)))
        tp = params[o]["tau2_g"]; qg = smoothed_quantiles(ytr, np.sqrt(tp + ytr.var(ddof=1) / n)); rows.append(dict(origin=o, issn=it["issn"], method="CVconst", cov80=float(np.mean((y >= qg[0]) & (y <= qg[-1]))), pinball=S.mean_pinball(y, qg, TAUS)))
        e = []
        for _ in range(20):
            tr = rng.choice(ytr, n); te = rng.choice(ytr, len(y)); qq = F.wquantile(tr, np.ones(n), [.1, .9]); e.append(abs(np.mean((te >= qq[0]) & (te <= qq[1])) - .8))
        nul.append(dict(issn=it["issn"], e=np.mean(e)))
A = pd.DataFrame(rows); A["abs_err"] = (A.cov80 - .8).abs(); res["ablation"] = {}
for m in ("CVtau0", "CVconst"):
    d = A[A.method == m]; pj = d.groupby("issn").abs_err.mean(); res["ablation"][m] = dict(signed=float((d.cov80 - .8).mean()), abs_err=dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(pj.to_numpy(), 3000, SEED))), pinball=float(d.groupby("issn").pinball.mean().mean()))
res["floor_exchangeable_null"] = float(pd.DataFrame(nul).groupby("issn").e.mean().mean())
# external outlier sensitivity
EX = pd.read_csv(f"{OUT}/D_external_rows.csv"); tf = EX[EX.variant == "transfer"]; jf = tf[tf.method == "F0"].groupby("issn").cov80.mean() - .8; out_j = jf[jf < -0.15].index.tolist(); res["external_outlier_journals"] = {k: float(jf[k]) for k in out_j}
keep = tf[~tf.issn.isin(out_j)]; res["external_excl_outliers"] = {}
for m in ("F0", "V", "CVg", "CVb"):
    d = keep[keep.method == m]; res["external_excl_outliers"][m] = dict(signed=dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean((d.groupby("issn").cov80.mean() - .8).to_numpy(), 3000, SEED))), abs_err=dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(d.assign(a=(d.cov80 - .8).abs()).groupby("issn").a.mean().to_numpy(), 3000, SEED))))
def jmx(m): d = keep[keep.method == m]; return d.assign(a=(d.cov80 - .8).abs()).groupby("issn").a.mean()
for a_, b_ in (("CVg", "F0"), ("CVg", "V")): res["external_excl_outliers"][f"{a_}_minus_{b_}"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean((jmx(a_) - jmx(b_)).dropna().to_numpy(), 3000, SEED)))
json.dump(res, open(f"{OUT}/D_extras_EXPLORATORY.json", "w"), indent=1, default=float); print(json.dumps({k: v for k, v in res.items() if k not in ("by_publisher",)}, default=float)[:2500])
