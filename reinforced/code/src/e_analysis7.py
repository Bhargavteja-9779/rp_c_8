"""Part E analyses A20-A26 (amendment E-A7)."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src"); sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm
from e_lib import strata_tables, mh_ci, informative
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; rng = np.random.default_rng(20261127); CUT = pd.Timestamp("2026-11-24")
df = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", parse_dates=["received", "accepted", "rdate"], low_memory=False)
for c in ("R_any", "R_process", "R_ai", "R_other", "R_nopub", "R_thirdparty", "R_pubother"): df[c] = df[c].astype(bool)
d1 = df[df.X1.notna()].copy(); res = {}
def boot_or(t, B):
    js = t.j.unique(); arr = {j: g[["a", "b", "c", "e"]].to_numpy(float) for j, g in t.groupby("j")}; out = []
    for _ in range(B):
        M = np.vstack([arr[js[i]] for i in rng.integers(0, len(js), len(js))]); a_, b_, c_, e_ = M.T; n_ = a_ + b_ + c_ + e_; den = (b_ * c_ / n_).sum(); out.append((a_ * e_ / n_).sum() / den if den > 0 else np.nan)
    return np.array(out)
# ---------------- A20 coverage and date availability
cov = pd.read_csv(f"{ROOT}/data/raw/coverage_notices.csv"); summ = pd.read_csv(f"{ROOT}/data/raw/collect_crossref_summary.tsv", sep="\t", header=None, names=["issn", "member", "total", "dated"], dtype={"issn": str})
jc = df.groupby("issn").agg(cohort_ret=("R_any", "sum"), cohort_proc=("R_process", "sum"), articles=("doi", "size")).reset_index().merge(cov, on="issn", how="left").merge(summ, on="issn", how="left")
jc["coverage"] = (jc.cohort_ret / jc.retraction_notices.replace(0, np.nan)).clip(upper=1.0); jc["dated_share"] = jc.dated / jc.total
res["A20"] = {"records_returned_total": int(summ.total.sum()), "records_dated": int(summ.dated.sum()), "dated_share_overall": float(summ.dated.sum() / summ.total.sum()), "notices_total": int(cov.retraction_notices.sum()), "cohort_retractions": int(df.R_any.sum()),
              "coverage_overall": float(min(1.0, df.R_any.sum() / cov.retraction_notices.sum())), "by_member": {}, "top_journals": []}
for m, g in jc.merge(summ[["issn"]].assign(_=1), on="issn").merge(df.drop_duplicates("issn")[["issn", "member"]], on="issn").groupby("member"): res["A20"]["by_member"][m] = {"notices": int(g.retraction_notices.sum()), "cohort_retractions": int(g.cohort_ret.sum()), "dated_share": float(g.dated.sum() / g.total.sum())}
top = jc.sort_values("cohort_proc", ascending=False).head(10); titles = pd.read_csv(f"{ROOT}/data/processed/journal_titles.csv", index_col=0).iloc[:, 0]
for _, r in top.iterrows(): res["A20"]["top_journals"].append({"issn": r.issn, "title": str(titles.get(r.issn, "")), "cohort_process": int(r.cohort_proc), "cohort_retracted": int(r.cohort_ret), "notices": int(r.retraction_notices), "dated_share": float(r.dated_share)})
d1 = d1.merge(jc[["issn", "coverage", "dated_share"]], on="issn", how="left"); res["A20"]["sens"] = {}
for name, mask in (("coverage>=0.8", d1.coverage >= .8), ("coverage>=0.5", d1.coverage >= .5), ("coverage<0.5", d1.coverage < .5), ("dated_share>=0.95", d1.dated_share >= .95), ("dated_share>=0.90", d1.dated_share >= .90), ("dated_share<0.90", d1.dated_share < .90)):
    x = d1[mask]; t = strata_tables(x, "X1", "R_process"); res["A20"]["sens"][name] = mh_ci(t, B=500) | {"journals": int(x.issn.nunique()), "events": int(x.R_process.sum())}
# ---------------- A21 ratio of ORs (process vs publisher-investigated other)
t1 = strata_tables(d1, "X1", "R_process"); t2 = strata_tables(d1, "X1", "R_pubother"); js = np.union1d(t1.j.unique(), t2.j.unique()); ar1 = {j: g[["a", "b", "c", "e"]].to_numpy(float) for j, g in t1.groupby("j")}; ar2 = {j: g[["a", "b", "c", "e"]].to_numpy(float) for j, g in t2.groupby("j")}; z = np.zeros((1, 4))
def mh_arr(M): a_, b_, c_, e_ = M.T; n_ = a_ + b_ + c_ + e_; return (a_ * e_ / n_).sum() / (b_ * c_ / n_).sum()
rat = []; o1s = []; o2s = []
for _ in range(2000):
    pick = js[rng.integers(0, len(js), len(js))]; M1 = np.vstack([ar1.get(j, z) for j in pick]); M2 = np.vstack([ar2.get(j, z) for j in pick]); M1 = M1[M1.sum(axis=1) > 0]; M2 = M2[M2.sum(axis=1) > 0]
    try: r1, r2 = mh_arr(M1), mh_arr(M2); rat.append(r1 / r2); o1s.append(r1); o2s.append(r2)
    except Exception: pass
rat = np.array(rat); rat = rat[np.isfinite(rat)]; res["A21"] = {"or_process": mh_ci(t1, B=10)["or_mh"], "or_pubother": mh_ci(t2, B=10)["or_mh"], "events_pubother": int(d1.R_pubother.sum()), "exposed_events_pubother": int(t2.a.sum()), "ratio": float(mh_ci(t1, B=10)["or_mh"] / mh_ci(t2, B=10)["or_mh"]), "ratio_ci": [float(np.quantile(rat, .025)), float(np.quantile(rat, .975))], "n_boot": int(len(rat))}
# ---------------- A22 exposure definition
x = df[df.stratum.map(df.groupby("stratum").size()) >= 100].copy(); q_all = x.groupby("stratum").D.transform(lambda s: s.quantile(.05)); nr = x[~x.R_any].groupby("stratum").D.quantile(.05); q_nr = x.stratum.map(nr)
x["Xnr"] = x.D <= q_nr; x["Xstrict"] = x.D < q_all; x["Xtb"] = (x.groupby("stratum").D.transform(lambda s: (s + rng.random(len(s))).rank(pct=True))) <= .05
res["A22"] = {"primary": mh_ci(strata_tables(x.assign(Xp=x.D <= q_all), "Xp", "R_process"), B=300) , "thresholds_nonretracted_only": mh_ci(strata_tables(x, "Xnr", "R_process"), B=300), "strict_less_than": mh_ci(strata_tables(x, "Xstrict", "R_process"), B=300), "random_tiebreak_exact_5pct": mh_ci(strata_tables(x, "Xtb", "R_process"), B=300), "flagged_share_primary": float((x.D <= q_all).mean()), "flagged_share_strict": float(x.Xstrict.mean())}
res["A22"]["same_day_excluded"] = json.load(open(f"{OUT}/E_build_summary.json")).get("same_day_excluded")
# ---------------- A23 cluster-aware year heterogeneity
yrs = [2021, 2022, 2023, 2024]; tabs = {y: strata_tables(d1[d1.acc_year == y], "X1", "R_process") for y in yrs}; ju = sorted(set().union(*[set(t.j) for t in tabs.values()])); arr = {y: {j: g[["a", "b", "c", "e"]].to_numpy(float) for j, g in t.groupby("j")} for y, t in tabs.items()}
def mh_year(pick, y):
    M = np.vstack([arr[y].get(j, z) for j in pick]); M = M[M.sum(axis=1) > 0]; return mh_arr(M)
obs = np.array([np.log(mh_arr(tabs[y][["a", "b", "c", "e"]].to_numpy(float))) for y in yrs]); bl = []; bratio = []; early = {2021, 2022}
for _ in range(2000):
    pick = np.array(ju)[rng.integers(0, len(ju), len(ju))]
    try:
        v = [np.log(mh_year(pick, y)) for y in yrs]; Me = np.vstack([arr[y].get(j, z) for y in (2021, 2022) for j in pick]); Ml = np.vstack([arr[y].get(j, z) for y in (2023, 2024) for j in pick]); Me = Me[Me.sum(axis=1) > 0]; Ml = Ml[Ml.sum(axis=1) > 0]
        if np.all(np.isfinite(v)): bl.append(v); bratio.append(mh_arr(Ml) / mh_arr(Me))
    except Exception: pass
bl = np.array(bl); se = bl.std(axis=0, ddof=1); w = 1 / se ** 2; pooled = (w * obs).sum() / w.sum(); Q = float((w * (obs - pooled) ** 2).sum()); slopes = [np.polyfit(yrs, r, 1)[0] for r in bl]
Me = np.vstack([tabs[y][["a", "b", "c", "e"]].to_numpy(float) for y in (2021, 2022)]); Ml = np.vstack([tabs[y][["a", "b", "c", "e"]].to_numpy(float) for y in (2023, 2024)])
res["A23"] = {"years": yrs, "or": [float(np.exp(o)) for o in obs], "boot_se_log": [float(s) for s in se], "Q": Q, "df": 3, "p": float(1 - stats.chi2.cdf(Q, 3)), "slope_per_year": float(np.polyfit(yrs, obs, 1)[0]), "slope_ci": [float(np.quantile(slopes, .025)), float(np.quantile(slopes, .975))], "ratio_late_early": float(mh_arr(Ml) / mh_arr(Me)), "ratio_ci": [float(np.quantile(bratio, .025)), float(np.quantile(bratio, .975))], "n_boot": int(len(bl)),
              "min_followup_months_A11": float((CUT - pd.Timestamp("2024-10-31")).days / 30.44)}
# ---------------- A24 journal-level meta-analysis, revised
rows = []
for j, g in d1.groupby("issn"):
    if g.R_process.sum() < 10: continue
    t = strata_tables(g, "X1", "R_process"); a, b, c, e = (t[k].to_numpy(float) + .5 for k in ("a", "b", "c", "e")); n = a + b + c + e; R = a * e / n; S = b * c / n; P = (a + e) / n; Q_ = (b + c) / n
    lo = np.log(R.sum() / S.sum()); var = (P * R).sum() / (2 * R.sum() ** 2) + (P * S + Q_ * R).sum() / (2 * R.sum() * S.sum()) + (Q_ * S).sum() / (2 * S.sum() ** 2); rows.append(dict(issn=j, events=int(g.R_process.sum()), exposed_events=int(t.a.sum()), log_or=lo, se=float(np.sqrt(var))))
M = pd.DataFrame(rows)
def dl(M):
    w = 1 / M.se ** 2; fe = (w * M.log_or).sum() / w.sum(); Q = (w * (M.log_or - fe) ** 2).sum(); k = len(M); tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())); wr = 1 / (M.se ** 2 + tau2); re = (wr * M.log_or).sum() / wr.sum(); sre = np.sqrt(1 / wr.sum())
    qhk = (wr * (M.log_or - re) ** 2).sum() / (k - 1); se_hk = np.sqrt(qhk / wr.sum()); tq = stats.t.ppf(.975, k - 1); tp = stats.t.ppf(.975, k - 2)
    return dict(k=int(k), pooled=float(np.exp(re)), ci=[float(np.exp(re - 1.96 * sre)), float(np.exp(re + 1.96 * sre))], ci_hk=[float(np.exp(re - tq * se_hk)), float(np.exp(re + tq * se_hk))], tau2=float(tau2), I2=float(max(0, (Q - (k - 1)) / Q)) if Q > 0 else 0.0, pi_t=[float(np.exp(re - tp * np.sqrt(tau2 + sre ** 2))), float(np.exp(re + tp * np.sqrt(tau2 + sre ** 2)))], share_gt1=float((M.log_or > 0).mean()))
res["A24"] = {"all": dl(M), "exposed_events_ge3": dl(M[M.exposed_events >= 3]), "journals": M.sort_values("events", ascending=False).head(12).to_dict("records")}
# ---------------- A25 screening revised
d3 = df[(df.acc_year.between(2022, 2024)) & df.pit.notna()].copy(); res["A25"] = {"n": int(len(d3))}
def strat_parts(d, score, out):
    inf = informative(d, out).copy(); inf["r"] = inf.groupby("stratum")[score].rank(method="average"); rows = []
    for s, g in inf.groupby("stratum", sort=False):
        pos = g[g[out]]; npos, nneg = len(pos), len(g) - len(pos); U = pos.r.sum() - npos * (npos + 1) / 2; rows.append((s, U, npos * nneg))
    return pd.DataFrame(rows, columns=["s", "U", "N"])
for sc_ in ("pit", "pit_tau0", "pit_tau10"): d3["neg_" + sc_] = -d3[sc_]
d3["neg_D"] = -d3.D; parts = strat_parts(d3, "neg_pit", "R_process"); big = parts.sort_values("N", ascending=False).iloc[0]
res["A25"]["stratified_auc_weighted"] = float(parts.U.sum() / parts.N.sum()); res["A25"]["stratified_auc_equal_weight_mean"] = float((parts.U / parts.N).mean()); res["A25"]["stratified_auc_median"] = float((parts.U / parts.N).median()); res["A25"]["largest_stratum"] = {"stratum": big.s, "pair_share": float(big.N / parts.N.sum())}
res["A25"]["auc_without_largest_stratum"] = float(parts[parts.s != big.s].U.sum() / parts[parts.s != big.s].N.sum()); res["A25"]["n_informative_strata"] = int(len(parts))
res["A25"]["auc_by_tau2"] = {sc_: float(strat_parts(d3, "neg_" + sc_, "R_process").pipe(lambda p: p.U.sum() / p.N.sum())) for sc_ in ("pit", "pit_tau0", "pit_tau10")}
# journal-history baseline: process-related retraction rate among the journal's articles accepted before year y, counting retractions dated before 1 January of y
def pooled_auc(y_, s_):
    r = stats.rankdata(s_); n1 = y_.sum(); n0 = len(y_) - n1; return float((r[y_].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
res["A25"]["pooled_auc_by_year"] = {}
for yv in (2023, 2024):
    d = d3[d3.acc_year == yv].copy(); prior = df[(df.acc_year < yv)]; ev = prior[prior.R_process & (prior.rdate < pd.Timestamp(f"{yv}-01-01"))].groupby("issn").size(); nn = prior.groupby("issn").size(); h = (ev.reindex(nn.index).fillna(0) / nn); d["hist"] = d.issn.map(h).fillna(0.0)
    y_ = d.R_process.to_numpy(); res["A25"]["pooled_auc_by_year"][yv] = {"neg_pit": pooled_auc(y_, d.neg_pit.to_numpy()), "neg_D": pooled_auc(y_, d.neg_D.to_numpy()), "journal_history": pooled_auc(y_, d.hist.to_numpy()), "events": int(y_.sum())}
# ---------------- A26 group level (journal-month)
g = df[df.X1.notna()].groupby("month_stratum").agg(issn=("issn", "first"), n=("doi", "size"), fast=("X1", "mean"), batch=("X4b", "mean"), ev=("R_process", "sum"), evany=("R_any", "sum")).reset_index(); g = g[g.n >= 30].copy(); res["A26"] = {"journal_months": int(len(g)), "journals": int(g.issn.nunique()), "events": int(g.ev.sum())}
inf_j = g.groupby("issn").ev.sum(); gi = g[g.issn.isin(inf_j[inf_j > 0].index)].copy(); D_ = pd.get_dummies(gi.issn, drop_first=True).astype(float); X = pd.concat([(gi.fast * 10).rename("fast10"), D_], axis=1); X = sm.add_constant(X)
fit = sm.GLM(np.column_stack([gi.ev, gi.n - gi.ev]), X, family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(gi.issn)[0]}); b = fit.params["fast10"]; ci = fit.conf_int().loc["fast10"]
res["A26"]["fe_logit_per_10pts_fast_share"] = {"or": float(np.exp(b)), "ci": [float(np.exp(ci[0])), float(np.exp(ci[1]))], "p": float(fit.pvalues["fast10"]), "journals_in_model": int(gi.issn.nunique()), "journal_months_in_model": int(len(gi))}
g["flag"] = g.fast >= .15; tot_ev = g.ev.sum(); res["A26"]["flag_fast_ge_15pct"] = {"flagged_months": int(g.flag.sum()), "articles_flagged": int(g[g.flag].n.sum()), "events_flagged": int(g[g.flag].ev.sum()), "rate_flagged": float(g[g.flag].ev.sum() / g[g.flag].n.sum()), "rate_other": float(g[~g.flag].ev.sum() / g[~g.flag].n.sum()), "share_events_captured": float(g[g.flag].ev.sum() / tot_ev), "share_articles": float(g[g.flag].n.sum() / g.n.sum())}
js_ = g.issn.unique(); gj = {j: g[g.issn == j][["n", "ev", "flag"]].to_numpy(float) for j in js_}; lifts = []
for _ in range(1000):
    M_ = np.vstack([gj[js_[i]] for i in rng.integers(0, len(js_), len(js_))]); f = M_[:, 2] == 1
    if f.sum() and (~f).sum() and M_[~f, 1].sum() > 0: lifts.append((M_[f, 1].sum() / M_[f, 0].sum()) / (M_[~f, 1].sum() / M_[~f, 0].sum()))
res["A26"]["rate_ratio_flagged_vs_other"] = {"est": res["A26"]["flag_fast_ge_15pct"]["rate_flagged"] / res["A26"]["flag_fast_ge_15pct"]["rate_other"], "ci": [float(np.quantile(lifts, .025)), float(np.quantile(lifts, .975))]}
json.dump(res, open(f"{OUT}/E_results7.json", "w"), indent=1, default=float); print("done")
f = lambda v: (round(v["or_mh"], 2), [round(x, 2) for x in v["ci_cluster"]], v["exposed_events"], v["events"])
print("A20", {k: v for k, v in res["A20"].items() if k not in ("sens", "top_journals")}); print({k: (f(v), v["journals"]) for k, v in res["A20"]["sens"].items()}); print("A21", res["A21"]); print("A22", {k: (f(v) if isinstance(v, dict) and "or_mh" in v else v) for k, v in res["A22"].items()}); print("A23", res["A23"]); print("A24", res["A24"]["all"], res["A24"]["exposed_events_ge3"]); print("A25", {k: v for k, v in res["A25"].items()}); print("A26", res["A26"])
