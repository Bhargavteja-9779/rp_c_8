"""Part D external validation (protocol D5): frozen frame parameters (tau2, c) transferred to PubMed journals outside the frame; secondary own-history variant.
Run once after collect_pubmed_external.py has finished."""
import glob, json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
from d_lib import *
sys.path.insert(0, "/home/user/rp_c_8/code/src")
from tdelay import data as Dm, stats as ST
from scipy import stats
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); SEED = cfg["seed"] + 31
pm = pd.concat([pd.read_csv(f, dtype={"pmid": str}) for f in sorted(glob.glob(f"{ROOT}/data/raw/pubmed_ext/*.csv"))], ignore_index=True)
for c in ("received", "accepted", "pubmed_date"): pm[c] = pd.to_datetime(pm[c], errors="coerce")
n_att = pm.journal.nunique(); cnt = pm.groupby("journal").size(); keep = cnt[cnt >= 600].index; pm = pm[pm.journal.isin(keep)]
e = pm[pm.received.notna() & pm.accepted.notna() & pm.pubmed_date.notna()].copy(); e = e.assign(D=(e.accepted - e.received).dt.days, V=e.pubmed_date, issn=e.journal, doi=e.pmid, member="PubMed-ext")
n0 = len(e); e = e[(e.D >= 1) & (e.D <= cfg["d_max"]) & ((e.accepted - e.V).dt.days <= cfg["accept_after_pub_tol_days"]) & ~e.title.fillna("").str.contains(Dm.NONRESEARCH)].drop_duplicates("pmid")
e["D"] = e.D.clip(upper=CAP); e["y"] = np.log(e.D.astype(float)); pub_of = {j: "PubMed-ext" for j in e.issn.unique()}
origins = list(pd.date_range("2022-01-01", "2025-07-01", freq="QS").strftime("%Y-%m-%d")); eval_origins = [o for o in origins if o >= "2023-07-01"]
store = build_store(e, pub_of, origins, cfg); params = json.load(open(f"{OUT}/D_params_by_origin.json")); rng = np.random.default_rng(SEED); rows = []; own = []
for t0 in eval_origins:
    fp = params[t0]; par = dict(tau2_pub={}, b_pub={}, tau2_g=fp["tau2_g"], b_g=fp["b_g"], c=fp["c"], G=None, alpha_aci=fp["alpha_aci"])
    for r_ in forecast_rows(store[t0], t0, par, use=("F0", "F6", "V", "CVg", "CVb")): r_["variant"] = "transfer"; rows.append(r_)
    use = [o for o in origins if complete(o, t0)]; pl = learn(store, use, rng) if use and sum(len(store[o]) for o in use) > 20 else None
    if pl is not None:
        for r_ in forecast_rows(store[t0], t0, pl, use=("V", "CV0", "CVb", "R")): r_["variant"] = "own_history"; own.append(r_)
D = pd.DataFrame(rows + own); D["abs_err"] = (D.cov80 - 0.8).abs(); D.to_csv(f"{OUT}/D_external_rows.csv", index=False)
res = dict(n_journals_attempted=int(n_att), n_journals_kept_ge600=int(len(keep)), n_dated_records=int(n0), n_clean_records=int(len(e)), n_journals_evaluated=int(D.issn.nunique()), n_journal_origins=int(len(D[(D.method == "F0")])), n_target_papers=int(D[D.method == "F0"].n_te.sum()))
def jm(v, m, col): d = D[(D.variant == v) & (D.method == m)]; return d.groupby("issn")[col].mean()
def summ(v, m): return dict(signed=dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean((jm(v, m, "cov80") - .8).to_numpy(), 3000, SEED))), abs_err=dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(jm(v, m, "abs_err").to_numpy(), 3000, SEED))), pinball=float(jm(v, m, "pinball").mean()) if D[(D.variant == v) & (D.method == m)].pinball.notna().any() else None, winkler=float(jm(v, m, "winkler").mean()), width=float(jm(v, m, "width").mean()))
res["transfer"] = {m: summ("transfer", m) for m in ["F0", "F6", "V", "CVg", "CVb"]}; res["own_history"] = {m: summ("own_history", m) for m in ["V", "CV0", "CVb", "R"] if len(D[(D.variant == "own_history") & (D.method == m)])}
def con(v, a, b, col):
    x = (jm(v, a, col) - jm(v, b, col)).dropna(); r = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(x.to_numpy(), 3000, SEED)))
    r["n_journals"] = int(len(x)); return r
res["HD6"] = {"CVg_vs_F0_abs_err": con("transfer", "CVg", "F0", "abs_err"), "CVg_vs_V_abs_err": con("transfer", "CVg", "V", "abs_err"), "CVg_vs_F0_pinball": con("transfer", "CVg", "F0", "pinball"), "CVb_vs_F0_abs_err": con("transfer", "CVb", "F0", "abs_err")}
res["by_origin_signed_cov_transfer"] = D[D.variant == "transfer"].groupby(["origin", "method"]).cov80.mean().sub(.8).unstack().round(4).to_dict()
f0 = D[(D.variant == "transfer") & (D.method == "F0")]; jj = f0.assign(obs=f0.cov80 - .8).groupby("issn")[["obs", "pred_shortfall"]].mean(); res["HD5_external"] = dict(corr_journal=float(jj.obs.corr(jj.pred_shortfall)), mean_pred=float(jj.pred_shortfall.mean()), mean_obs=float(jj.obs.mean()))
ev = {}
for T in (72, 120, 180):
    for m in ("F0", "CVg", "CVb"):
        d = D[(D.variant == "transfer") & (D.method == m)]; ev[f"{m}_T{T}"] = dict(brier=float(((d[f"p{T}"] - d[f"o{T}"]) ** 2).mean()), slope=float(np.polyfit(d[f"p{T}"], d[f"o{T}"], 1)[0]))
res["events_transfer"] = ev; res["by_journal_f0_signed"] = (jm("transfer", "F0", "cov80") - .8).round(4).to_dict(); json.dump(res, open(f"{OUT}/D_external_summary.json", "w"), indent=1, default=float); print(json.dumps({k: res[k] for k in ["n_journals_attempted", "n_journals_kept_ge600", "n_journals_evaluated", "n_journal_origins", "n_target_papers"]}), json.dumps(res["transfer"], default=float)[:1500])
