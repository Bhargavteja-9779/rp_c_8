"""Part E dataset assembly (protocol cycle4_protocol_partE.md): merges Retraction Watch outcomes and timing exposures into data/processed/e_articles.csv.gz."""
import json, re, sys, time
import numpy as np, pandas as pd
from scipy.special import ndtr
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"
art = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); art["doi"] = art.doi.str.lower().str.strip()
fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); art = art[art.issn.isin({j["issn"] for j in fr})].copy()
art = art.drop_duplicates("doi"); art["acc_year"] = art.accepted.dt.year; art["stratum"] = art.issn + "_" + art.acc_year.astype(str)
# ---------------- outcomes
rw = pd.read_csv(f"{ROOT}/data/raw/retraction_watch/retraction_watch.csv.gz", low_memory=False); rw["doi"] = rw.OriginalPaperDOI.str.lower().str.strip()
rein = set(rw[rw.RetractionNature == "Reinstatement"].doi.dropna()); ret = rw[(rw.RetractionNature == "Retraction") & rw.doi.notna()].copy()
ret["reasons"] = ret.Reason.fillna("").str.split(";").apply(lambda L: [x.strip().lstrip("+").strip().lower() for x in L if x.strip().lstrip("+").strip()])
g = ret.groupby("doi").agg(reasons=("reasons", lambda s: sorted({r for L in s for r in L})), rdate=("RetractionDate", "first")); g["rdate"] = pd.to_datetime(g.rdate, errors="coerce", format="mixed")
g = g[~g.index.isin(rein)]
PROC = ("peer review", "rogue editor", "paper mill", "concerns/issues about third party involvement"); AI = "computer-aided content or computer-generated content"
g["R_process"] = g.reasons.apply(lambda L: any(any(p in r for p in PROC) for r in L)); g["R_ai"] = g.reasons.apply(lambda L: AI in L)
art = art.merge(g[["rdate", "R_process", "R_ai"]], left_on="doi", right_index=True, how="left"); art["R_any"] = art.rdate.notna() | art.R_process.notna()
art["R_any"] = art.R_any.astype(bool); art["R_process"] = art.R_process.fillna(False).astype(bool); art["R_ai"] = art.R_ai.fillna(False).astype(bool); art["R_other"] = art.R_any & ~art.R_process
# ---------------- exposures
art["D"] = art.D.astype(float); sz = art.groupby("stratum").D.transform("size")
q05 = art.groupby("stratum").D.transform(lambda s: s.quantile(.05)); q95 = art.groupby("stratum").D.transform(lambda s: s.quantile(.95))
art["X1"] = np.where(sz >= 100, art.D <= q05, np.nan); art["X2"] = np.where(sz >= 100, art.D >= q95, np.nan); art["X3"] = (art.D <= 7).astype(float)
cnt = art.groupby(["issn", "accepted"]).doi.transform("size"); art["batch_n"] = cnt; art["X4"] = (cnt >= 5).astype(float); art["X4b"] = (cnt >= 10).astype(float)
art["X5"] = (art.accepted.dt.dayofweek >= 5).astype(float); art["N1"] = (art.received.dt.dayofweek >= 5).astype(float)
art["ln_refs"] = np.log1p(art.n_refs.fillna(art.n_refs.median())); art["ln_auth"] = np.log1p(art.n_authors.fillna(art.n_authors.median()))
# ---------------- X6 out-of-time PIT under CV0 (frame tau2)
tau2 = json.load(open(f"{ROOT}/product/turnaround_forecast/defaults.json"))["tau2_global"]; CAP = 480; H = 91; art["yc"] = np.log(art.D.clip(upper=CAP)); art["pit"] = np.nan
origins = pd.date_range("2022-01-01", "2025-07-01", freq="QS"); t_start = time.time()
for issn, dj in art.groupby("issn"):
    idx_all = dj.index.to_numpy(); y = dj.yc.to_numpy(); V = dj.V.to_numpy("datetime64[ns]"); A = dj.accepted.to_numpy("datetime64[ns]"); Rv = dj.received.to_numpy("datetime64[ns]")
    for t0 in origins:
        t0n = np.datetime64(t0); vis = (V < t0n) & (A < t0n) & (Rv < t0n) & (V >= t0n - np.timedelta64(365, "D"))
        if vis.sum() < 100: continue
        tgt = (Rv >= t0n) & (Rv < t0n + np.timedelta64(H, "D"))
        if tgt.sum() == 0: continue
        yv = y[vis]; h = np.sqrt(tau2 + yv.var(ddof=1) / len(yv)); art.loc[idx_all[tgt], "pit"] = ndtr((y[tgt][:, None] - yv[None, :]) / h).mean(axis=1)
print("pit available", int(art.pit.notna().sum()), "secs", round(time.time() - t_start))
art["X6_fast"] = np.where(art.pit.notna(), art.pit <= 0.05, np.nan); art["X6_slow"] = np.where(art.pit.notna(), art.pit >= 0.95, np.nan)
imp = pd.read_csv(f"{OUT}/journal_imprint_map.csv", index_col=0).iloc[:, 0]; art["imprint"] = art.issn.map(imp).fillna("other")
keep = ["doi", "issn", "member", "imprint", "acc_year", "stratum", "received", "accepted", "D", "batch_n", "X1", "X2", "X3", "X4", "X4b", "X5", "N1", "ln_refs", "ln_auth", "pit", "X6_fast", "X6_slow", "R_any", "R_process", "R_ai", "R_other", "rdate"]
art[keep].to_csv(f"{ROOT}/data/processed/e_articles.csv.gz", index=False)
summ = dict(n_articles=int(len(art)), n_retracted=int(art.R_any.sum()), n_process=int(art.R_process.sum()), n_ai=int(art.R_ai.sum()), n_other=int(art.R_other.sum()), n_reinstated_excluded=int(len(rein & set(art.doi))), n_pit=int(art.pit.notna().sum()),
            n_strata=int(art.stratum.nunique()), n_strata_ge100=int((art.groupby("stratum").size() >= 100).sum()), by_member_retracted=art[art.R_any].member.value_counts().to_dict(), by_year_retracted=art[art.R_any].acc_year.value_counts().sort_index().to_dict(), tau2=tau2)
json.dump(summ, open(f"{OUT}/E_build_summary.json", "w"), indent=1, default=int); print(json.dumps(summ, default=int))
