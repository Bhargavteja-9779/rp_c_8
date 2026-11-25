"""Part E analyses A7-A10 (amendment E-A2): external replication, reason subtypes, score calibration, pooled AUC, time to retraction."""
import glob, json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src"); sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from scipy import stats
from e_lib import strata_tables, mh_ci, informative
from tdelay import data as Dm
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; rng = np.random.default_rng(20261125); cfg = json.load(open(f"{ROOT}/code/configs/config.json"))
df = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", parse_dates=["received", "accepted", "rdate"], low_memory=False)
for c in ("R_any", "R_process", "R_ai", "R_other"): df[c] = df[c].astype(bool)
res = {}
# ------------- reasons for A8 (rebuild reason flags from RW)
rw = pd.read_csv(f"{ROOT}/data/raw/retraction_watch/retraction_watch.csv.gz", low_memory=False); rw["doi"] = rw.OriginalPaperDOI.str.lower().str.strip(); ret = rw[(rw.RetractionNature == "Retraction") & rw.doi.notna()]
def flag(sub): return set(ret[ret.Reason.fillna("").str.lower().str.contains(sub, regex=False)].doi)
SUBS = {"compromised peer review": "compromised peer review", "rogue editor": "rogue editor", "paper mill": "paper mill", "concerns/issues about peer review": "concerns/issues about peer review"}
d1 = df[df.X1.notna()].copy(); res["A8"] = {}
for k, sub in SUBS.items():
    fl = flag(sub); d1["_o"] = df.loc[d1.index, "doi"].isin(fl) if False else d1.doi.isin(fl); n = int(d1._o.sum())
    if n >= 30: res["A8"][k] = mh_ci(strata_tables(d1, "X1", "_o"), B=300) | {"n_events": n}
res["A8"]["R_other"] = mh_ci(strata_tables(d1, "X1", "R_other"), B=300) | {"n_events": int(d1.R_other.sum())}
# ------------- A9 PIT bands and pooled AUC
d3 = df[(df.acc_year.between(2022, 2024)) & df.pit.notna()].copy(); bands = pd.cut(d3.pit, [-1, .01, .05, .20, .80, .95, 1.01], labels=["<=0.01", "0.01-0.05", "0.05-0.20", "0.20-0.80", "0.80-0.95", ">=0.95"])
res["A9"] = {"bands": {o: d3.groupby(bands, observed=True)[o].agg(["mean", "sum", "size"]).round(6).to_dict("index") for o in ("R_process", "R_any")}}
def pooled_auc(d, score, out, B=300):
    y = d[out].to_numpy(); s = d[score].to_numpy(); r = stats.rankdata(s); n1 = y.sum(); n0 = len(y) - n1; auc = (r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0); js = d.issn.to_numpy(); u = np.unique(js); idx = {j: np.where(js == j)[0] for j in u}; bs = []
    for _ in range(B):
        pick = np.concatenate([idx[j] for j in rng.choice(u, len(u))]); yy = y[pick]; rr = stats.rankdata(s[pick]); a = yy.sum(); b = len(yy) - a; bs.append((rr[yy].sum() - a * (a + 1) / 2) / (a * b))
    return dict(auc=float(auc), ci=[float(np.quantile(bs, .025)), float(np.quantile(bs, .975))])
d3["neg_pit"] = -d3.pit; d3["neg_D"] = -d3.D; d3["bn"] = d3.batch_n; res["A9"]["pooled_auc"] = {o: {s: pooled_auc(d3, s, o) for s in ("neg_pit", "neg_D", "bn")} for o in ("R_process", "R_any")}
# ------------- A10 time to retraction
dr = df[df.R_any & df.rdate.notna()].copy(); dr["months"] = (dr.rdate - dr.accepted).dt.days / 30.44; f = dr[dr.X1 == 1]; o = dr[dr.X1 == 0]
res["A10"] = {"fast_n": int(len(f)), "other_n": int(len(o)), "fast_median_months": float(f.months.median()), "other_median_months": float(o.months.median()), "mwu_p": float(stats.mannwhitneyu(f.months, o.months).pvalue)}
# ------------- A7 external replication
pm = pd.concat([pd.read_csv(g, dtype={"pmid": str}) for g in sorted(glob.glob(f"{ROOT}/data/raw/pubmed_ext/*.csv"))], ignore_index=True)
for c in ("received", "accepted", "pubmed_date"): pm[c] = pd.to_datetime(pm[c], errors="coerce")
pm["doi"] = pm.doi.fillna("").str.lower().str.strip(); cnt = pm.groupby("journal").size(); pm = pm[pm.journal.isin(cnt[cnt >= 600].index)]
e = pm[pm.received.notna() & pm.accepted.notna() & pm.pubmed_date.notna() & (pm.doi != "")].copy(); e["D"] = (e.accepted - e.received).dt.days
e = e[(e.D >= 1) & (e.D <= cfg["d_max"]) & (((e.accepted - e.pubmed_date).dt.days) <= cfg["accept_after_pub_tol_days"]) & ~e.title.fillna("").str.contains(Dm.NONRESEARCH)].drop_duplicates("doi")
e["issn"] = e.journal; e["acc_year"] = e.accepted.dt.year; e["stratum"] = e.issn + "_" + e.acc_year.astype(str); sz = e.groupby("stratum").D.transform("size")
e["X1"] = np.where(sz >= 100, e.D <= e.groupby("stratum").D.transform(lambda s: s.quantile(.05)), np.nan); e["X2"] = np.where(sz >= 100, e.D >= e.groupby("stratum").D.transform(lambda s: s.quantile(.95)), np.nan)
e["X3"] = (e.D <= 7).astype(float); c4 = e.groupby(["issn", "accepted"]).doi.transform("size"); e["X4"] = (c4 >= 5).astype(float); e["X4b"] = (c4 >= 10).astype(float); e["N1"] = (e.received.dt.dayofweek >= 5).astype(float)
rein = set(rw[rw.RetractionNature == "Reinstatement"].doi.dropna()); rr = ret[~ret.doi.isin(rein)].copy(); rr["reasons"] = rr.Reason.fillna("").str.lower()
PROC = ("peer review", "rogue editor", "paper mill", "concerns/issues about third party involvement"); rproc = set(rr[rr.reasons.apply(lambda s: any(p in s for p in PROC))].doi); rany = set(rr.doi)
e["R_any"] = e.doi.isin(rany); e["R_process"] = e.doi.isin(rproc); res["A7"] = {"n_articles": int(len(e)), "n_journals": int(e.issn.nunique()), "events_any": int(e.R_any.sum()), "events_process": int(e.R_process.sum()), "by_journal_top_events": e[e.R_any].groupby("issn").size().sort_values(ascending=False).head(8).to_dict()}
for out in ("R_process", "R_any"):
    res["A7"][out] = {}
    for exp in ("X1", "X2", "X3", "X4", "X4b", "N1"):
        d = e[e[exp].notna()]
        if d[out].sum() >= 10: res["A7"][out][exp] = mh_ci(strata_tables(d, exp, out), B=300)
json.dump(res, open(f"{OUT}/E_results2.json", "w"), indent=1, default=float); print("done")
f_ = lambda v: (round(v["or_mh"], 2), [round(x, 2) for x in v["ci_cluster"]], v["exposed_events"], v["events"])
print("A7", res["A7"]["n_articles"], res["A7"]["events_any"], res["A7"]["events_process"], {o: {k: f_(v) for k, v in res["A7"][o].items()} for o in ("R_process", "R_any") if o in res["A7"]})
print("A8", {k: f_(v) for k, v in res["A8"].items()}); print("A10", res["A10"]); print("A9 auc", res["A9"]["pooled_auc"]); print(res["A9"]["bands"]["R_process"])
