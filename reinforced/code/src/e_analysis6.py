"""Part E analyses A15-A19 (amendment E-A6)."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
import numpy as np, pandas as pd
from scipy import stats
from e_lib import strata_tables, mh_ci, informative
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; rng = np.random.default_rng(20261126)
df = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", parse_dates=["received", "accepted", "rdate"], low_memory=False)
for c in ("R_any", "R_process", "R_ai", "R_other", "R_nopub", "R_thirdparty"): df[c] = df[c].astype(bool)
d1 = df[df.X1.notna()].copy(); res = {}
# ---- A15 ascertainment
res["A15"] = {o: mh_ci(strata_tables(d1, "X1", o), B=300) | {"n_events": int(d1[o].sum())} for o in ("R_nopub", "R_thirdparty")}
d1["R_pub"] = d1.R_process & ~d1.R_nopub; res["A15"]["R_with_publisher_investigation"] = mh_ci(strata_tables(d1, "X1", "R_pub"), B=300) | {"n_events": int(d1.R_pub.sum())}
# ---- A16 journal-level random-effects meta-analysis
rows = []
for j, g in d1.groupby("issn"):
    if g.R_process.sum() < 10: continue
    t = strata_tables(g, "X1", "R_process"); a, b, c, e = (t[k].sum() for k in ("a", "b", "c", "e")); n = a + b + c + e
    num = (t.a * t.e / (t.a + t.b + t.c + t.e)).sum(); den = (t.b * t.c / (t.a + t.b + t.c + t.e)).sum()
    if a == 0 or c == 0 or b == 0 or e == 0 or den == 0 or num == 0: a, b, c, e = a + .5, b + .5, c + .5, e + .5; lo = np.log(a * e / (b * c))
    else: lo = np.log(num / den)
    se = np.sqrt(1 / a + 1 / b + 1 / c + 1 / e); rows.append(dict(issn=j, events=int(g.R_process.sum()), exposed_events=int(t.a.sum()), log_or=float(lo), se=float(se)))
M = pd.DataFrame(rows); w = 1 / M.se ** 2; fe = (w * M.log_or).sum() / w.sum(); Q = (w * (M.log_or - fe) ** 2).sum(); k = len(M); tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())); wr = 1 / (M.se ** 2 + tau2); re = (wr * M.log_or).sum() / wr.sum(); sre = np.sqrt(1 / wr.sum())
pi = (re - 1.96 * np.sqrt(tau2 + sre ** 2), re + 1.96 * np.sqrt(tau2 + sre ** 2)); loo = [float(np.exp(((1 / (M.se.drop(i) ** 2 + tau2)) * M.log_or.drop(i)).sum() / (1 / (M.se.drop(i) ** 2 + tau2)).sum())) for i in M.index]
res["A16"] = {"n_journals": int(k), "pooled_or": float(np.exp(re)), "ci": [float(np.exp(re - 1.96 * sre)), float(np.exp(re + 1.96 * sre))], "tau2": float(tau2), "I2": float(max(0, (Q - (k - 1)) / Q)) if Q > 0 else 0.0, "prediction_interval": [float(np.exp(pi[0])), float(np.exp(pi[1]))], "share_journals_or_gt1": float((M.log_or > 0).mean()), "loo_range": [min(loo), max(loo)], "journals": M.sort_values("events", ascending=False).head(15).to_dict("records")}
# ---- A17 finer strata
res["A17"] = {}
for name, col in (("year", "stratum"), ("quarter", "quarter_stratum"), ("month", "month_stratum")):
    x = d1.copy(); x["stratum"] = x[col]; res["A17"][name] = mh_ci(strata_tables(x, "X1", "R_process"), B=300)
# ---- A18 screening robustness
d3 = df[(df.acc_year.between(2022, 2024)) & df.pit.notna()].copy(); d3["neg_pit"] = -d3.pit; res["A18"] = {"n": int(len(d3))}
top5 = df[df.R_process].groupby("issn").size().sort_values(ascending=False).head(5).index
def strat_auc(d, score, out):
    inf = informative(d, out).copy(); inf["r"] = inf.groupby("stratum")[score].rank(method="average"); rows = []
    for (s, j), g in inf.groupby(["stratum", "issn"], sort=False):
        pos = g[g[out]]; npos, nneg = len(pos), len(g) - len(pos); rows.append((j, pos.r.sum() - npos * (npos + 1) / 2, npos * nneg))
    t = pd.DataFrame(rows, columns=["j", "U", "N"]).groupby("j").sum(); arr = t.to_numpy(float); bs = []
    for _ in range(300): M_ = arr[rng.integers(0, len(arr), len(arr))]; bs.append(M_[:, 0].sum() / M_[:, 1].sum())
    return dict(auc=float(arr[:, 0].sum() / arr[:, 1].sum()), ci=[float(np.quantile(bs, .025)), float(np.quantile(bs, .975))], n_events=int(inf[out].sum()), n_journals=int(len(t)))
res["A18"]["auc_all"] = strat_auc(d3, "neg_pit", "R_process"); res["A18"]["auc_2023_2024"] = strat_auc(d3[d3.acc_year >= 2023], "neg_pit", "R_process"); res["A18"]["auc_excl_top5"] = strat_auc(d3[~d3.issn.isin(top5)], "neg_pit", "R_process"); res["A18"]["auc_true_first_online_journals"] = strat_auc(d3[d3.journal_true_fo_share >= .8], "neg_pit", "R_process")
res["A18"]["auc_any_all"] = strat_auc(d3, "neg_pit", "R_any")
jt = d3.groupby("issn").agg(n=("doi", "size"), ev=("R_process", "sum")); flags = {"pit_le_0.01": d3.pit <= .01, "pit_le_0.05": d3.pit <= .05, "D_le_7": d3.D <= 7, "batch_ge_10": d3.batch_n >= 10, "batch_ge_5": d3.batch_n >= 5}
jf = {k: d3.assign(f=v).groupby("issn").apply(lambda g: pd.Series({"fl": int(g.f.sum()), "fe": int((g.f & g.R_process).sum())}), include_groups=False) for k, v in flags.items()}; res["A18"]["screen_ci"] = {}
for k in flags:
    arr = jt.join(jf[k]).to_numpy(float); bs = []
    for _ in range(500): M_ = arr[rng.integers(0, len(arr), len(arr))]; bs.append((M_[:, 3].sum() / M_[:, 2].sum(), (M_[:, 3].sum() / M_[:, 2].sum()) / (M_[:, 1].sum() / M_[:, 0].sum()), M_[:, 3].sum() / M_[:, 1].sum()))
    bs = np.array(bs); base = jt.ev.sum() / jt.n.sum(); res["A18"]["screen_ci"][k] = {"ppv": float(arr[:, 3].sum() / arr[:, 2].sum()), "ppv_ci": [float(np.nanquantile(bs[:, 0], .025)), float(np.nanquantile(bs[:, 0], .975))], "lift": float(arr[:, 3].sum() / arr[:, 2].sum() / base), "lift_ci": [float(np.nanquantile(bs[:, 1], .025)), float(np.nanquantile(bs[:, 1], .975))], "sens": float(arr[:, 3].sum() / arr[:, 1].sum()), "sens_ci": [float(np.nanquantile(bs[:, 2], .025)), float(np.nanquantile(bs[:, 2], .975))], "events_flagged": int(arr[:, 3].sum()), "flagged": int(arr[:, 2].sum()), "top_journal_share_of_flagged_events": float(arr[:, 3].max() / arr[:, 3].sum())}
# ---- A19 year heterogeneity
ys = {}
for y, g in d1.groupby("acc_year"):
    if g.R_process.sum() >= 10 and 2020 <= y <= 2024:
        v = mh_ci(strata_tables(g, "X1", "R_process"), B=50); ys[int(y)] = (np.log(v["or_mh"]), (np.log(v["ci_mh"][1]) - np.log(v["ci_mh"][0])) / (2 * 1.96), v["or_mh"])
ll = np.array([v[0] for v in ys.values()]); se = np.array([v[1] for v in ys.values()]); w = 1 / se ** 2; pooled = (w * ll).sum() / w.sum(); Qy = float((w * (ll - pooled) ** 2).sum()); res["A19"] = {"years": {k: v[2] for k, v in ys.items()}, "Q": Qy, "df": int(len(ll) - 1), "p": float(1 - stats.chi2.cdf(Qy, len(ll) - 1))}
json.dump(res, open(f"{OUT}/E_results6.json", "w"), indent=1, default=float); print("done")
f = lambda v: (round(v["or_mh"], 2), [round(x, 2) for x in v["ci_cluster"]], v["n_events"] if "n_events" in v else "")
print("A15", {k: f(v) for k, v in res["A15"].items()}); print("A16", {k: v for k, v in res["A16"].items() if k != "journals"}); print("A17", {k: f(v) for k, v in res["A17"].items()}); print("A18", {k: (round(v["auc"], 3), [round(x, 3) for x in v["ci"]]) for k, v in res["A18"].items() if isinstance(v, dict) and "auc" in v}); print("A19", res["A19"])
