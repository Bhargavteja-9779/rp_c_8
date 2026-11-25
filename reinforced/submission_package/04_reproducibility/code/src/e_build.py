"""Part E dataset assembly with the corrected E-cohort (protocol amendment E-A6). Writes data/processed/e_articles.csv.gz and results/E_build_summary.json."""
import json, sys, time, hashlib
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from scipy.special import ndtr
from tdelay import data as D
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json"))
fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}
raw = D.read_crossref_dir(f"{ROOT}/data/raw/crossref", member); raw["doi"] = raw.doi.str.lower().str.strip()
# ---------------- outcomes (Retraction Watch)
rw = pd.read_csv(f"{ROOT}/data/raw/retraction_watch/retraction_watch.csv.gz", low_memory=False); rw["doi"] = rw.OriginalPaperDOI.str.lower().str.strip()
rein = set(rw[rw.RetractionNature == "Reinstatement"].doi.dropna()); ret = rw[(rw.RetractionNature == "Retraction") & rw.doi.notna()].copy()
ret["reasons"] = ret.Reason.fillna("").str.split(";").apply(lambda L: [x.strip().lstrip("+").strip().lower() for x in L if x.strip().lstrip("+").strip()])
g = ret.groupby("doi").agg(reasons=("reasons", lambda s: sorted({r for L in s for r in L})), rdate=("RetractionDate", "first")); g["rdate"] = pd.to_datetime(g.rdate, errors="coerce", format="mixed"); g = g[~g.index.isin(rein)]
PROC = ("peer review", "rogue editor", "paper mill", "concerns/issues about third party involvement"); AI = "computer-aided content or computer-generated content"
g["R_process"] = g.reasons.apply(lambda L: any(any(p in r for p in PROC) for r in L)); g["R_ai"] = g.reasons.apply(lambda L: AI in L)
g["R_nopub"] = g.R_process & g.reasons.apply(lambda L: not any("investigation by journal/publisher" in r for r in L)); g["R_thirdparty"] = g.R_process & g.reasons.apply(lambda L: any("investigation by third party" in r for r in L))
g["R_pubother"] = ~g.R_process & g.reasons.apply(lambda L: any("investigation by journal/publisher" in r for r in L))
ret_set = set(g.index)
# ---------------- E-cohort cleaning (no rule depends on retraction status or on the 'issued' fallback)
flow = []
def step(name, d): flow.append(dict(step=name, n=int(len(d)), retracted=int(d.doi.isin(ret_set).sum())))
df = raw.drop_duplicates("doi"); step("Crossref records, unique DOI (800 journals)", df)
df = df[df.received.notna() & df.accepted.notna()]; step("received and accepted dates parsable", df)
df = df.assign(D=(df.accepted - df.received).dt.days); d0 = df[df.D == 0]; summ_d0 = dict(n_same_day=int(len(d0)), retracted_same_day=int(d0.doi.isin(ret_set).sum())); df = df[(df.D >= cfg["d_min"]) & (df.D <= cfg["d_max"])]; step("1 <= D <= 1,460 days", df)
df = df[df.received >= pd.Timestamp(cfg["received_min"])]; step("received on or after minimum date", df)
fo = df.first_online.notna(); bad = fo & ((df.accepted - df.first_online).dt.days > cfg["accept_after_pub_tol_days"]); df = df[~bad]; step("accepted not > 7 days after a TRUE first-online date", df)
df = df[~df.title.fillna("").str.contains(D.NONRESEARCH)]; step("title not non-research pattern", df)
art = df.copy(); art["true_fo"] = art.first_online.notna(); art["acc_year"] = art.accepted.dt.year; art["stratum"] = art.issn + "_" + art.acc_year.astype(str)
art = art.merge(g[["rdate", "R_process", "R_ai", "R_nopub", "R_thirdparty", "R_pubother"]], left_on="doi", right_index=True, how="left")
art["R_any"] = art.doi.isin(ret_set); 
for c in ("R_process", "R_ai", "R_nopub", "R_thirdparty", "R_pubother"): art[c] = art[c].fillna(False).astype(bool)
art["R_other"] = art.R_any & ~art.R_process
# ---------------- exposures
art["D"] = art.D.astype(float); sz = art.groupby("stratum").D.transform("size")
q05 = art.groupby("stratum").D.transform(lambda s: s.quantile(.05)); q95 = art.groupby("stratum").D.transform(lambda s: s.quantile(.95))
art["X1"] = np.where(sz >= 100, art.D <= q05, np.nan); art["X2"] = np.where(sz >= 100, art.D >= q95, np.nan); art["X3"] = (art.D <= 7).astype(float)
cnt = art.groupby(["issn", "accepted"]).doi.transform("size"); art["batch_n"] = cnt; art["X4"] = (cnt >= 5).astype(float); art["X4b"] = (cnt >= 10).astype(float)
art["X5"] = (art.accepted.dt.dayofweek >= 5).astype(float); art["N1"] = (art.received.dt.dayofweek >= 5).astype(float); art["ln_auth"] = np.log1p(art.n_authors.fillna(art.n_authors.median()))
art["lag"] = np.where(art.true_fo, (art.first_online - art.accepted).dt.days, np.nan); lg = art[art.true_fo].copy(); szl = lg.groupby("stratum").lag.transform("size")
art["L1"] = np.nan; art["L2"] = np.nan; art.loc[lg.index, "L1"] = np.where(szl >= 100, lg.lag <= lg.groupby("stratum").lag.transform(lambda s: s.quantile(.05)), np.nan); art.loc[lg.index, "L2"] = np.where(szl >= 100, lg.lag >= lg.groupby("stratum").lag.transform(lambda s: s.quantile(.95)), np.nan)
art["month_stratum"] = art.issn + "_" + art.accepted.dt.strftime("%Y-%m"); art["quarter_stratum"] = art.issn + "_" + art.accepted.dt.year.astype(str) + "Q" + art.accepted.dt.quarter.astype(str)
# ---------------- X6 out-of-time PIT under CV0 (frame tau2)
tau2 = json.load(open(f"{ROOT}/product/turnaround_forecast/defaults.json"))["tau2_global"]; CAP = 480; H = 91; art["yc"] = np.log(art.D.clip(upper=CAP)); TAUS = {"pit": tau2, "pit_tau0": 0.0, "pit_tau10": 0.10}
for c in TAUS: art[c] = np.nan
origins = pd.date_range("2022-01-01", "2025-07-01", freq="QS"); t_start = time.time()
for issn, dj in art.groupby("issn"):
    idx_all = dj.index.to_numpy(); y = dj.yc.to_numpy(); V = dj.V.to_numpy("datetime64[ns]"); A = dj.accepted.to_numpy("datetime64[ns]"); Rv = dj.received.to_numpy("datetime64[ns]")
    for t0 in origins:
        t0n = np.datetime64(t0); vis = (V < t0n) & (A < t0n) & (Rv < t0n) & (V >= t0n - np.timedelta64(365, "D"))
        if vis.sum() < 100: continue
        tgt = (Rv >= t0n) & (Rv < t0n + np.timedelta64(H, "D"))
        if tgt.sum() == 0: continue
        yv = y[vis]
        for c, t2 in TAUS.items(): h = np.sqrt(t2 + yv.var(ddof=1) / len(yv)); art.loc[idx_all[tgt], c] = ndtr((y[tgt][:, None] - yv[None, :]) / h).mean(axis=1)
art["X6_fast"] = np.where(art.pit.notna(), art.pit <= 0.05, np.nan); art["X6_slow"] = np.where(art.pit.notna(), art.pit >= 0.95, np.nan)
imp = pd.read_csv(f"{OUT}/journal_imprint_map.csv", index_col=0).iloc[:, 0]; art["imprint"] = art.issn.map(imp).fillna("other"); art["journal_true_fo_share"] = art.groupby("issn").true_fo.transform("mean")
keep = ["doi", "issn", "member", "imprint", "acc_year", "stratum", "month_stratum", "quarter_stratum", "received", "accepted", "D", "batch_n", "X1", "X2", "X3", "X4", "X4b", "X5", "N1", "L1", "L2", "lag", "true_fo", "pit_tau0", "pit_tau10", "journal_true_fo_share", "ln_auth", "pit", "X6_fast", "X6_slow", "R_any", "R_process", "R_ai", "R_other", "R_nopub", "R_thirdparty", "R_pubother", "rdate"]
art[keep].to_csv(f"{ROOT}/data/processed/e_articles.csv.gz", index=False)
summ = dict(flow=flow, n_articles=int(len(art)), n_retracted=int(art.R_any.sum()), n_process=int(art.R_process.sum()), n_ai=int(art.R_ai.sum()), n_other=int(art.R_other.sum()), n_nopub=int(art.R_nopub.sum()), n_thirdparty=int(art.R_thirdparty.sum()), n_pit=int(art.pit.notna().sum()), n_journals=int(art.issn.nunique()),
            n_strata=int(art.stratum.nunique()), true_first_online_share=float(art.true_fo.mean()), by_member_retracted=art[art.R_any].member.value_counts().to_dict(), by_year_retracted=art[art.R_any].acc_year.value_counts().sort_index().to_dict(), tau2=tau2,
            rw_snapshot_sha256_gz=hashlib.sha256(open(f"{ROOT}/data/raw/retraction_watch/retraction_watch.csv.gz", "rb").read()).hexdigest(), median_refs_retracted=float(art[art.R_any].n_refs.median()), median_refs_other=float(art[~art.R_any].n_refs.median()), same_day_excluded=summ_d0)
json.dump(summ, open(f"{OUT}/E_build_summary.json", "w"), indent=1, default=int); print(json.dumps({k: v for k, v in summ.items() if k != "flow"}, default=int)); print(flow)
