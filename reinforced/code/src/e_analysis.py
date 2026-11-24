"""Part E analyses A1-A6 as specified in research_design/cycle4_protocol_partE.md. Run once after e_build.py."""
import json, sys
import numpy as np, pandas as pd, scipy.sparse as sp
from scipy import stats
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; rng = np.random.default_rng(20261124)
df = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", parse_dates=["received", "accepted"])
for c in ("R_any", "R_process", "R_ai", "R_other"): df[c] = df[c].astype(bool)
res = {}
# ---------------------------------------------------------------- helpers
def strata_tables(d, exp, out):
    """2x2 per stratum: a exposed&event, b exposed&nonevent, c unexposed&event, e unexposed&nonevent; journal id per stratum."""
    x = d[exp].astype(bool); y = d[out].astype(bool)
    t = pd.DataFrame({"s": d.stratum.values, "j": d.issn.values, "a": (x & y).values, "b": (x & ~y).values, "c": (~x & y).values, "e": (~x & ~y).values}).groupby(["s", "j"], sort=False).sum().reset_index()
    return t
def mh(t, journal_idx=None):
    a, b, c, e = (t[k].to_numpy(float) for k in ("a", "b", "c", "e")); n = a + b + c + e; ok = n > 0
    num = (a * e / np.where(ok, n, 1))[ok].sum(); den = (b * c / np.where(ok, n, 1))[ok].sum(); return num / den if den > 0 else np.nan
def mh_ci(t, B=1000):
    est = mh(t); a, b, c, e = (t[k].to_numpy(float) for k in ("a", "b", "c", "e")); n = a + b + c + e
    R = a * e / n; S = b * c / n; P = (a + e) / n; Q = (b + c) / n
    var = (P * R).sum() / (2 * R.sum() ** 2) + ((P * S + Q * R).sum()) / (2 * R.sum() * S.sum()) + (Q * S).sum() / (2 * S.sum() ** 2)
    lo_mh, hi_mh = np.exp(np.log(est) - 1.96 * np.sqrt(var)), np.exp(np.log(est) + 1.96 * np.sqrt(var))
    # journal-cluster bootstrap
    js = t.j.unique(); grp = {j: g for j, g in t.groupby("j")}; arr = {j: g[["a", "b", "c", "e"]].to_numpy(float) for j, g in grp.items()}; bs = []
    for _ in range(B):
        pick = rng.choice(len(js), len(js)); M = np.vstack([arr[js[i]] for i in pick]); a_, b_, c_, e_ = M.T; n_ = a_ + b_ + c_ + e_; num = (a_ * e_ / n_).sum(); den = (b_ * c_ / n_).sum(); bs.append(num / den if den > 0 else np.nan)
    bs = np.array(bs); bs = bs[np.isfinite(bs)]
    return dict(or_mh=float(est), ci_mh=[float(lo_mh), float(hi_mh)], ci_cluster=[float(np.quantile(bs, .025)), float(np.quantile(bs, .975))], exposed=int((a + b).sum()), exposed_events=int(a.sum()), events=int((a + c).sum()), n=int(n.sum()))
def informative(d, out):
    ev = d.groupby("stratum")[out].agg(["sum", "size"]); keep = ev[(ev["sum"] > 0) & (ev["sum"] < ev["size"])].index; return d[d.stratum.isin(keep)]
def fe_logit(d, out, exps, cluster="issn", iters=25):
    """Fixed-effects (stratum) logistic regression by Newton-Raphson with journal-cluster sandwich SE; informative strata only."""
    d = informative(d.dropna(subset=exps), out); X = d[exps].astype(float).to_numpy(); y = d[out].astype(float).to_numpy()
    codes, _ = pd.factorize(d.stratum); S = sp.csr_matrix((np.ones(len(d)), (np.arange(len(d)), codes))); Z = sp.hstack([sp.csr_matrix(X), S]).tocsr(); k = Z.shape[1]
    lam = np.concatenate([np.zeros(len(exps)), np.full(Z.shape[1] - len(exps), 1e-3)]); beta = np.zeros(k); beta[len(exps):] = np.log(y.mean() / (1 - y.mean()))
    def ll(b): eta = np.clip(Z @ b, -30, 30); return float(np.sum(y * eta - np.log1p(np.exp(eta))) - 0.5 * np.sum(lam * b * b))
    cur = ll(beta)
    for it in range(60):
        eta = Z @ beta; p = 1 / (1 + np.exp(-np.clip(eta, -30, 30))); W = p * (1 - p); H = (Z.T @ sp.diags(W) @ Z).toarray() + np.diag(lam) + 1e-9 * np.eye(k); g = Z.T @ (y - p) - lam * beta; step = np.linalg.solve(H, g); t = 1.0
        while t > 1e-6 and ll(beta + t * step) < cur - 1e-9: t /= 2
        beta = beta + t * step; new = ll(beta)
        if abs(new - cur) < 1e-9 and np.max(np.abs(t * step)) < 1e-6: cur = new; break
        cur = new
    p = 1 / (1 + np.exp(-np.clip(Z @ beta, -30, 30))); Hinv = np.linalg.inv((Z.T @ sp.diags(p * (1 - p)) @ Z).toarray() + np.diag(lam) + 1e-9 * np.eye(k)); sc = Z.multiply((y - p)[:, None]).tocsr(); cl, _ = pd.factorize(d[cluster])
    G = sp.csr_matrix((np.ones(len(d)), (cl, np.arange(len(d))))); sg = (G @ sc).toarray(); meat = sg.T @ sg; V = Hinv @ meat @ Hinv; se = np.sqrt(np.diag(V))[:len(exps)]
    return {e: dict(or_=float(np.exp(beta[i])), ci=[float(np.exp(beta[i] - 1.96 * se[i])), float(np.exp(beta[i] + 1.96 * se[i]))], p=float(2 * (1 - stats.norm.cdf(abs(beta[i] / se[i]))))) for i, e in enumerate(exps)} | {"n_rows": int(len(d)), "n_strata": int(len(np.unique(codes))), "n_events": int(y.sum()), "n_clusters": int(len(np.unique(cl)))}
d1 = df[df.X1.notna()].copy()  # strata with >=100 articles
res["base_rates"] = {o: float(df[o].mean()) for o in ("R_any", "R_process", "R_ai", "R_other")}; res["n"] = {"articles": int(len(df)), "articles_X1_defined": int(len(d1)), "events_any": int(df.R_any.sum()), "events_process": int(df.R_process.sum()), "events_ai": int(df.R_ai.sum())}
# ---------------------------------------------------------------- A1 primary
res["A1"] = {}
for out in ("R_process", "R_any"):
    res["A1"][out] = {}
    for exp in ("X1", "X2", "X3", "X4", "X4b", "X5", "N1"):
        d = df[df[exp].notna()] if exp in ("X1", "X2") else df
        res["A1"][out][exp] = mh_ci(strata_tables(d, exp, out), B=500)
    res["A1"][out]["joint_fe_logit"] = fe_logit(d1, out, ["X1", "X2", "X4", "X5", "ln_refs", "ln_auth"])
p1 = [res["A1"]["R_process"]["joint_fe_logit"]["X1"]["p"], res["A1"]["R_any"]["joint_fe_logit"]["X1"]["p"]]; order = np.argsort(p1); adj = [0, 0]; m = 2
for r, i in enumerate(order): adj[i] = min(1.0, (m - r) * p1[i])
res["A1"]["primary_holm"] = dict(R_process=adj[0], R_any=adj[1])
# ---------------------------------------------------------------- A2 dose response (20 bins of within-stratum percentile of D)
d2 = df[df.stratum.map(df.groupby("stratum").size()) >= 100].copy(); d2["pct"] = d2.groupby("stratum").D.rank(pct=True, method="average"); d2["bin"] = np.minimum((d2.pct * 20).astype(int), 19); d2["ref"] = d2.bin.isin([9, 10]); res["A2"] = {}
for k in range(20):
    if k in (9, 10): continue
    dd = d2[(d2.bin == k) | d2.ref].copy(); dd["E"] = (dd.bin == k); res["A2"][str(k)] = mh_ci(strata_tables(dd, "E", "R_process"), B=200) | {"bin_lo_pct": 5 * k}
# ---------------------------------------------------------------- A3 prospective screening, accepted 2022-2024 with PIT
d3 = df[(df.acc_year.between(2022, 2024)) & df.pit.notna()].copy(); res["A3"] = {"n": int(len(d3)), "events_process": int(d3.R_process.sum()), "events_any": int(d3.R_any.sum()), "rate_process": float(d3.R_process.mean()), "rate_any": float(d3.R_any.mean())}
def strat_auc(d, score, out, B=500):
    inf = informative(d, out).copy(); inf["r"] = inf.groupby("stratum")[score].rank(method="average"); rows = []
    for (s, j), g in inf.groupby(["stratum", "issn"], sort=False):
        pos = g[g[out]]; neg = g[~g[out]]; npos, nneg = len(pos), len(neg)
        U = pos.r.sum() - npos * (npos + 1) / 2; rows.append((j, U, npos * nneg))
    t = pd.DataFrame(rows, columns=["j", "U", "N"]).groupby("j").sum(); auc = t.U.sum() / t.N.sum(); arr = t.to_numpy(float); bs = []
    for _ in range(B): M = arr[rng.integers(0, len(arr), len(arr))]; bs.append(M[:, 0].sum() / M[:, 1].sum())
    return dict(auc=float(auc), ci=[float(np.quantile(bs, .025)), float(np.quantile(bs, .975))], n_strata=int(inf.stratum.nunique()), n_events=int(inf[out].sum()))
d3["neg_pit"] = -d3.pit; d3["neg_D"] = -d3.D; d3["batch_score"] = d3.batch_n; res["A3"]["auc"] = {}
for out in ("R_process", "R_any"):
    res["A3"]["auc"][out] = {"neg_pit": strat_auc(d3, "neg_pit", out), "neg_D": strat_auc(d3, "neg_D", out), "batch_n": strat_auc(d3, "batch_score", out)}
res["A3"]["screen"] = {}
for out in ("R_process", "R_any"):
    base = d3[out].mean(); r_ = {"base_rate": float(base)}
    for name, flag in (("pit_le_0.01", d3.pit <= .01), ("pit_le_0.05", d3.pit <= .05), ("D_le_7", d3.D <= 7), ("batch_ge_5", d3.batch_n >= 5), ("batch_ge_10", d3.batch_n >= 10), ("pit_ge_0.95", d3.pit >= .95)):
        f = d3[flag]; r_[name] = dict(flagged=int(len(f)), flagged_events=int(f[out].sum()), ppv=float(f[out].mean()) if len(f) else None, lift=float(f[out].mean() / base) if len(f) else None, nns=float(1 / f[out].mean()) if len(f) and f[out].mean() > 0 else None, sensitivity=float(f[out].sum() / d3[out].sum()))
    res["A3"]["screen"][out] = r_
# ---------------------------------------------------------------- A4 robustness
res["A4"] = {"by_imprint": {}, "by_year": {}, "by_member": {}}
for k, g in df.groupby("imprint"):
    if g.R_process.sum() >= 10 and g.X1.notna().any(): res["A4"]["by_imprint"][k] = mh_ci(strata_tables(g[g.X1.notna()], "X1", "R_process"), B=200)
for k, g in df.groupby("acc_year"):
    if g.R_process.sum() >= 10 and g.X1.notna().any(): res["A4"]["by_year"][int(k)] = mh_ci(strata_tables(g[g.X1.notna()], "X1", "R_process"), B=200)
for k, g in df.groupby("member"):
    if g.R_process.sum() >= 10 and g.X1.notna().any(): res["A4"]["by_member"][k] = mh_ci(strata_tables(g[g.X1.notna()], "X1", "R_process"), B=200)
cnt = df.groupby("stratum").R_any.sum(); mass = cnt[cnt >= 25].index; res["A4"]["n_mass_strata"] = int(len(mass)); dm = d1[~d1.stratum.isin(mass)]
res["A4"]["excl_mass_X1_process"] = mh_ci(strata_tables(dm, "X1", "R_process"), B=200); res["A4"]["excl_mass_X4_process"] = mh_ci(strata_tables(df[~df.stratum.isin(mass)], "X4", "R_process"), B=200)
res["A4"]["excl_ai_X1_process"] = mh_ci(strata_tables(d1[~d1.R_ai], "X1", "R_process"), B=200)
# ---------------------------------------------------------------- A5 journal-year level
jy = df.groupby("stratum").agg(n=("doi", "size"), fast7=("X3", "mean"), batch=("X4", "mean"), ret=("R_any", "mean"), proc=("R_process", "mean"), acc_year=("acc_year", "first")); jy = jy[(jy.n >= 100) & jy.acc_year.between(2021, 2024)]
res["A5"] = {"n_journal_years": int(len(jy))}
for a_ in ("fast7", "batch"):
    for b_ in ("ret", "proc"): r_, p_ = stats.spearmanr(jy[a_], jy[b_]); res["A5"][f"{a_}_vs_{b_}"] = dict(rho=float(r_), p=float(p_))
# ---------------------------------------------------------------- A6 computer-generated content outcome
res["A6"] = {exp: mh_ci(strata_tables(df[df[exp].notna()], exp, "R_ai"), B=200) for exp in ("X1", "X2", "X4", "X5")}
json.dump(res, open(f"{OUT}/E_results.json", "w"), indent=1, default=float); print("done"); print(json.dumps({k: res["A1"]["R_process"][k] for k in ("X1", "X2", "X3", "X4", "N1")}, default=float)[:1800])
