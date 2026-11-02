"""Part D main experiment: strict out-of-time panel on the frame (781-journal data), ten evaluation origins 2023-04-01..2025-07-01.
Run once as specified in revised_experimental_protocol.md Part D."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
from d_lib import *
from scipy import stats
sys.path.insert(0, "/home/user/rp_c_8/code/src")
from tdelay import stats as ST
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); SEED = cfg["seed"] + 30
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)].copy()
df["D"] = df.D.clip(upper=CAP); df["y"] = np.log(df.D.astype(float))
imprint = pd.read_csv(f"{OUT}/journal_imprint_map.csv", index_col=0).iloc[:, 0]
origins = list(pd.date_range("2022-01-01", "2025-07-01", freq="QS").strftime("%Y-%m-%d")); eval_origins = [o for o in origins if o >= "2023-04-01"]
store = build_store(df, member, origins, cfg); rng = np.random.default_rng(SEED); rows = []; params = {}
for t0 in eval_origins:
    use = [o for o in origins if complete(o, t0)]; par = learn(store, use, rng); params[t0] = {k: (v if k != "G" else None) for k, v in par.items()}
    rows += forecast_rows(store[t0], t0, par); print(t0, "complete origins", len(use), "items", len(store[t0]), "c", par["c"], "tau2_g", round(par["tau2_g"], 4), "alpha", round(par["alpha_aci"], 3), flush=True)
D = pd.DataFrame(rows); D["imprint"] = D.issn.map(imprint); D.to_csv(f"{OUT}/D_panel_rows.csv", index=False); json.dump(params, open(f"{OUT}/D_params_by_origin.json", "w"), indent=1)
# ---------------- summaries
def jm(m, col): return D[D.method == m].groupby("issn")[col].mean()
D["abs_err"] = (D.cov80 - 0.8).abs(); res = {"n_origins": len(eval_origins), "n_journals": int(D.issn.nunique()), "n_journal_origins": int(len(D[D.method == "F0"])), "n_target_papers": int(D[D.method == "F0"].n_te.sum())}
meths = ["F0", "F6", "V", "R", "CV0", "CVb", "CVg", "ACI"]; res["summary"] = {}
for m in meths:
    d = D[D.method == m]; r = {"signed_cov": dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean((jm(m, "cov80") - .8).to_numpy(), 3000, SEED))), "abs_err": dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(jm(m, "abs_err").to_numpy(), 3000, SEED))),
         "winkler": float(jm(m, "winkler").mean()), "width": float(jm(m, "width").mean()), "below": float(jm(m, "below").mean()), "above": float(jm(m, "above").mean())}
    if d.pinball.notna().any(): r["pinball"] = float(jm(m, "pinball").mean())
    res["summary"][m] = r
def contrast(a, b, col, seed=SEED):
    x = (jm(a, col) - jm(b, col)).dropna(); est = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(x.to_numpy(), 3000, seed)))
    # imprint-mean t(6), publisher-level
    xi = x.groupby(imprint.reindex(x.index).fillna("other")).mean(); se = xi.std(ddof=1) / np.sqrt(len(xi)); tq = stats.t.ppf(.975, len(xi) - 1)
    est["imprint_mean"] = float(xi.mean()); est["imprint_t_ci"] = [float(xi.mean() - tq * se), float(xi.mean() + tq * se)]; est["n_imprints_same_sign"] = int(max((xi > 0).sum(), (xi < 0).sum())); est["n_imprints"] = int(len(xi))
    pub = x.groupby(pd.Series(member).reindex(x.index)).mean(); est["publisher_means"] = pub.round(5).to_dict(); est["publishers_same_sign"] = int(max((pub > 0).sum(), (pub < 0).sum()))
    # moving-block bootstrap over ordered origins (block 2) on the origin-level mean contrast
    oo = (D[D.method == a].groupby("origin")[col].mean() - D[D.method == b].groupby("origin")[col].mean()).sort_index().to_numpy(); r = np.random.default_rng(seed); k = len(oo); nb = int(np.ceil(k / 2)); bs = []
    for _ in range(3000):
        st = r.integers(0, k - 1, nb); idx = np.concatenate([[s, s + 1] for s in st])[:k]; bs.append(oo[idx].mean())
    est["origin_block_ci"] = [float(np.quantile(bs, .025)), float(np.quantile(bs, .975))]; est["origin_means"] = [float(v) for v in oo]; return est
res["HD1_CV0_vs_F0_abs_err"] = contrast("CV0", "F0", "abs_err"); res["HD2_CV0_vs_F0_pinball"] = contrast("CV0", "F0", "pinball"); res["HD2_rel_pinball"] = float(jm("CV0", "pinball").mean() / jm("F0", "pinball").mean() - 1)
x = (jm("CV0", "pinball") / jm("F0", "pinball") - 1).dropna(); res["HD2_rel_pinball_ci"] = list(ST.cluster_bootstrap_mean(x.to_numpy(), 3000, SEED)[1:])
res["HD4"] = {m: contrast("CV0", m, "abs_err", SEED + k) for k, m in enumerate(["V", "R", "ACI"])}; p = [2 * (1 - stats.norm.cdf(abs(res["HD4"][m]["est"]) / max((res["HD4"][m]["hi"] - res["HD4"][m]["lo"]) / 3.92, 1e-12))) for m in ["V", "R", "ACI"]]; res["HD4_p_normal_approx"] = dict(zip(["V", "R", "ACI"], p)); res["HD4_p_holm"] = dict(zip(["V", "R", "ACI"], [float(v) for v in ST.holm(p)]))
for m in ["V", "R", "CVb", "CVg", "F6"]: res.setdefault("secondary_vs_F0_abs_err", {})[m] = contrast(m, "F0", "abs_err", SEED + 9)
res["interval_score_CV0_vs_F0"] = contrast("CV0", "F0", "winkler")
# HD5 mechanism
f0 = D[D.method == "F0"].copy(); f0["obs"] = f0.cov80 - .8; jj = f0.groupby("issn")[["obs", "pred_shortfall"]].mean(); res["HD5"] = {"corr_journal": float(jj.obs.corr(jj.pred_shortfall)), "spearman_journal": float(stats.spearmanr(jj.obs, jj.pred_shortfall)[0]),
    "mean_pred": float(jj.pred_shortfall.mean()), "mean_obs": float(jj.obs.mean())}
ids = jj.index.to_numpy(); r = np.random.default_rng(SEED + 5); sl, cr = [], []
for _ in range(2000):
    s = jj.loc[r.choice(ids, len(ids))]; sl.append(np.polyfit(s.pred_shortfall, s.obs, 1)[0]); cr.append(s.obs.corr(s.pred_shortfall))
res["HD5"]["slope"] = float(np.polyfit(jj.pred_shortfall, jj.obs, 1)[0]); res["HD5"]["slope_ci"] = [float(np.quantile(sl, .025)), float(np.quantile(sl, .975))]; res["HD5"]["corr_ci"] = [float(np.quantile(cr, .025)), float(np.quantile(cr, .975))]
q = pd.qcut(f0.pred_shortfall, 10, duplicates="drop"); res["HD5"]["deciles"] = f0.groupby(q, observed=True)[["pred_shortfall", "obs"]].mean().round(4).values.tolist()
# by-origin table and by-publisher
res["by_origin_signed_cov"] = D.groupby(["origin", "method"]).cov80.mean().sub(.8).unstack().round(4).to_dict(); res["by_pub_signed_cov"] = D.groupby(["pub", "method"]).cov80.mean().sub(.8).unstack().round(4).to_dict()
res["tau2_last_origin"] = {k: v for k, v in params[eval_origins[-1]].items()}; res["tau2_by_origin_global"] = {o: params[o]["tau2_g"] for o in eval_origins}; res["n_complete_by_origin"] = {o: params[o]["n_origins"] for o in eval_origins}
# event probabilities
ev = {}
for T in (72, 120, 180):
    for m in ("F0", "CV0", "CVb"):
        e = D[D.method == m]; br = ((e[f"p{T}"] - e[f"o{T}"]) ** 2); ev[f"{m}_T{T}"] = dict(brier=float(br.mean()), slope=float(np.polyfit(e[f"p{T}"], e[f"o{T}"], 1)[0]))
res["events"] = ev; json.dump(res, open(f"{OUT}/D_summary.json", "w"), indent=1, default=float); print(json.dumps({k: res[k] for k in ["summary"]}, default=float)[:3000])
