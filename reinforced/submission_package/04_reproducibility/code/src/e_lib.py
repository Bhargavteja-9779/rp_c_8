"""Helper functions for Part E analyses (extracted unchanged from e_analysis.py)."""
import numpy as np, pandas as pd, scipy.sparse as sp
from scipy import stats
rng = np.random.default_rng(20261124)
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

