"""Part D library: strictly out-of-time panel machinery and the cohort-shift smoothed forecaster CV (protocol Part D). All constants are fixed in the protocol."""
import sys
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from scipy.special import ndtr
from tdelay import protocol as P, forecasters as F, scoring as S
TAUS = np.array([.1, .2, .3, .4, .5, .6, .7, .8, .9]); H = 91; CAP = 365; GAMMA = 0.05; GRID = np.linspace(1.0, 1.4, 17); WIN = H + CAP
def complete(o, t0): return pd.Timestamp(o) + pd.Timedelta(days=WIN) <= pd.Timestamp(t0)
def build_store(df, pub_of, origins, cfg, min_tr=100, min_te=30):
    """store[o] = list of items with visible 12-month sample, 24-month sample and ages, and target sample; target = received in [o, o+91)."""
    c = dict(cfg, horizon_days=H); store = {}
    for o in origins:
        T0 = pd.Timestamp(o); items = []
        for i, dj in df.groupby("issn"):
            tr12, tr24, te = P.split_journal_origin(dj, T0, c)
            if len(tr12) < min_tr or len(te) < min_te: continue
            items.append(dict(issn=i, pub=pub_of[i], ytr=tr12.y.to_numpy(), y24=tr24.y.to_numpy(), age24=(T0 - tr24["V"]).dt.days.to_numpy(), yte=te.y.to_numpy(), Dte=te["D"].to_numpy()))
        store[o] = items
    return store
def _delta(it):
    n1, n2 = len(it["ytr"]), len(it["yte"]); v1, v2 = it["ytr"].var(ddof=1), it["yte"].var(ddof=1)
    return it["yte"].mean() - it["ytr"].mean(), v1 / n1 + v2 / n2
def learn(store, origins_complete, rng):
    """Parameters learned from earlier complete origins only."""
    items = [dict(it, o=o) for o in origins_complete for it in store[o]]; par = dict(n_origins=len(origins_complete), n_items=len(items))
    if not items: return None
    dl = pd.DataFrame([dict(pub=it["pub"], d=_delta(it)[0], sv=_delta(it)[1]) for it in items])
    par["tau2_pub"] = {}; par["b_pub"] = {}
    for p_, g in dl.groupby("pub"): par["tau2_pub"][p_] = float(max(0.0, g.d.var(ddof=1) - g.sv.mean())) if len(g) > 5 else np.nan; par["b_pub"][p_] = float(g.d.mean())
    par["tau2_g"] = float(max(0.0, dl.d.var(ddof=1) - dl.sv.mean())); par["b_g"] = float(dl.d.mean())
    # V: constant half-width scale
    def covc(cc):
        v = []
        for it in items:
            q = F.wquantile(it["ytr"], np.ones(len(it["ytr"])), [.1, .5, .9]); lo, hi = q[1] + cc * (q[0] - q[1]), q[1] + cc * (q[2] - q[1]); v.append(np.mean((it["yte"] >= lo) & (it["yte"] <= hi)))
        return np.mean(v)
    cov = [covc(x) for x in GRID]; par["c"] = float(GRID[int(np.argmin([abs(x - .8) for x in cov]))])
    # R: PIT map
    Pp, Ww = [], []
    for it in items: p = S.pit_ecdf(it["yte"], it["ytr"], rng); Pp.append(p); Ww.append(np.full(len(p), 1 / len(p)))
    Pp = np.concatenate(Pp); Ww = np.concatenate(Ww); k = np.argsort(Pp); par["G"] = (Pp[k], np.cumsum(Ww[k]) / Ww.sum())
    # ACI: adaptive miscoverage level, delayed feedback
    a = 0.20
    for o in origins_complete:
        v = []
        for it in store[o]:
            q = F.wquantile(it["ytr"], np.ones(len(it["ytr"])), [a / 2, 1 - a / 2]); v.append(1 - np.mean((it["yte"] >= q[0]) & (it["yte"] <= q[1])))
        a = float(np.clip(a + GAMMA * (0.20 - np.mean(v)), 0.02, 0.60))
    par["alpha_aci"] = a
    return par
def smoothed_quantiles(y, h, taus=TAUS):
    """Quantiles of (1/n) sum Phi((q - y_i)/h) by bisection."""
    lo = np.full(len(taus), y.min() - 8 * h - 1e-9); hi = np.full(len(taus), y.max() + 8 * h + 1e-9)
    for _ in range(60):
        mid = (lo + hi) / 2; Fm = ndtr((mid[:, None] - y[None, :]) / h).mean(axis=1); up = Fm < taus; lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
    return (lo + hi) / 2
def wink(y, lo, hi, a=0.2): return float(np.mean((hi - lo) + (2 / a) * np.clip(lo - y, 0, None) + (2 / a) * np.clip(y - hi, 0, None)))
def _row(base, m, y, q, extra=None):
    lo, hi = q[0], q[-1]; r = dict(base, method=m, pinball=S.mean_pinball(y, q, TAUS) if len(q) == 9 else np.nan, cov80=float(np.mean((y >= lo) & (y <= hi))), below=float(np.mean(y < lo)), above=float(np.mean(y > hi)), winkler=wink(y, lo, hi), width=float(hi - lo))
    if extra: r.update(extra)
    return r
def forecast_rows(items, o, par, use=("F0", "F6", "V", "R", "CV0", "CVb", "CVg", "ACI"), thresholds=(72, 120, 180)):
    rows = []
    for it in items:
        ytr, y = it["ytr"], it["yte"]; n = len(ytr); s2 = ytr.var(ddof=1); base = dict(origin=o, issn=it["issn"], pub=it["pub"], n_tr=n, n_te=len(y)); q0 = F.wquantile(ytr, np.ones(n), TAUS)
        tp = par["tau2_pub"].get(it["pub"]); tp = par["tau2_g"] if (tp is None or np.isnan(tp)) else tp; bp = par["b_pub"].get(it["pub"], par["b_g"])
        hp, hg = np.sqrt(tp + s2 / n), np.sqrt(par["tau2_g"] + s2 / n)
        ev = lambda yy, h, shift=0.0: {f"p{T}": float(ndtr((np.log(T) - (yy + shift)) / h).mean()) for T in thresholds}
        out = {}
        if "F0" in use: out["F0"] = (q0, {f"p{T}": float((ytr <= np.log(T)).mean()) for T in thresholds})
        if "F6" in use: out["F6"] = (np.asarray(F.decayed(it["y24"], it["age24"], 182.5, TAUS).q), None)
        if "V" in use: out["V"] = (q0[4] + par["c"] * (q0 - q0[4]), None)
        if "R" in use:
            lv = [float(np.interp(t, par["G"][1], par["G"][0])) for t in TAUS]; out["R"] = (F.wquantile(ytr, np.ones(n), [min(max(l, .005), .995) for l in lv]), None)
        if "CV0" in use: out["CV0"] = (smoothed_quantiles(ytr, hp), ev(ytr, hp))
        if "CVb" in use: out["CVb"] = (smoothed_quantiles(ytr + bp, hp), ev(ytr, hp, bp))
        if "CVg" in use: out["CVg"] = (smoothed_quantiles(ytr, hg), ev(ytr, hg))
        if "ACI" in use:
            a = par["alpha_aci"]; qa = F.wquantile(ytr, np.ones(n), [a / 2, 1 - a / 2]); out["ACI"] = (np.array([qa[0], qa[1]]), None)
        pred = float(ndtr((q0[-1] - ytr) / hp).mean() - ndtr((q0[0] - ytr) / hp).mean() - 0.8) if "CV0" in use else np.nan
        for m, (q, e) in out.items():
            ex = {"pred_shortfall": pred} if m == "F0" else {}
            if e:
                for T in thresholds: ex[f"p{T}"] = e[f"p{T}"]; ex[f"o{T}"] = float((it["Dte"] <= T).mean())
            rows.append(_row(base, m, y, q, ex))
    return rows
