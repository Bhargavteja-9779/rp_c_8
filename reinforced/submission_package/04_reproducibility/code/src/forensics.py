"""Phase-1 forensic checks: independent re-implementation of F3/F4/F6 for random journal-origins, and descriptive data-quality scan."""
import json, sys, os
import numpy as np, pandas as pd
from scipy import stats
ROOT = "/home/user/rp_c_8"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); out = {}
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); taus = np.array(cfg["taus"])
met = pd.read_csv(f"{ROOT}/results/metrics_journal_origin.csv"); rng = np.random.default_rng(7)
def pin(y, q, t): d = y - q; return np.mean(np.maximum(t * d, (t - 1) * d))
def hazen_w(v, w, t):                     # independent weighted Hazen quantile via explicit cumulative weights
    o = np.argsort(v, kind="stable"); v, w = v[o], w[o]; c = np.cumsum(w); p = (c - w / 2) / c[-1]
    return np.array([v[0] if x <= p[0] else v[-1] if x >= p[-1] else v[np.searchsorted(p, x) - 1] + (x - p[np.searchsorted(p, x) - 1]) / (p[np.searchsorted(p, x)] - p[np.searchsorted(p, x) - 1]) * (v[np.searchsorted(p, x)] - v[np.searchsorted(p, x) - 1]) for x in t])
f0 = met[met.method == "F0"].sample(25, random_state=3); errs = {"F3": [], "F6": [], "F4": []}
g = {k: d for k, d in df.groupby("issn")}
# prior for F4 recomputed independently at each origin from all journals with >=20 visible papers
priors = {}
for t0 in cfg["origins"]:
    T0 = pd.Timestamp(t0); m, s2, n = [], [], []
    for i, d in g.items():
        v = d[(d.V < T0) & (d.accepted < T0) & (d.received < T0) & (d.V >= T0 - pd.Timedelta(days=365))].y
        if len(v) >= 20: m.append(v.mean()); s2.append(v.var(ddof=1)); n.append(len(v))
    m, s2, n = map(np.array, (m, s2, n)); ok = n >= 5
    def dl(est, var):
        w = 1 / var; mb = (w * est).sum() / w.sum(); Q = (w * (est - mb) ** 2).sum(); den = w.sum() - (w ** 2).sum() / w.sum(); tau2 = max(0, (Q - (len(est) - 1)) / den); ws = 1 / (tau2 + var); return tau2, (ws * est).sum() / ws.sum()
    priors[t0] = (dl(m[ok], s2[ok] / n[ok]), dl(0.5 * np.log(s2[ok]), 1 / (2 * (n[ok] - 1))))
for _, r in f0.iterrows():
    T0 = pd.Timestamp(r.origin); d = g[r.issn]; vis = d[(d.V < T0) & (d.accepted < T0) & (d.received < T0)]
    t12 = vis[vis.V >= T0 - pd.Timedelta(days=365)]; t24 = vis[vis.V >= T0 - pd.Timedelta(days=730)]; te = d[(d.received >= T0) & (d.received < T0 + pd.Timedelta(days=182))]; yt = te.y.to_numpy()
    y = t12.y.to_numpy(); mu, sd = y.mean(), y.std(ddof=0)
    l3 = np.mean([pin(yt, mu + sd * stats.norm.ppf(t), t) for t in taus])
    age = (T0 - t24.V).dt.days.to_numpy(); q6 = hazen_w(t24.y.to_numpy(), 0.5 ** (age / cfg["decay_half_life_days"]), taus); l6 = np.mean([pin(yt, q6[k], t) for k, t in enumerate(taus)])
    (t2m, mu0), (t2l, l0) = priors[r.origin]; n = len(y); s2 = y.var(ddof=1); v = s2 / n; B = t2m / (t2m + v); mp = B * mu + 0 * 0 + 0; mp = B * y.mean() + (1 - B) * mu0
    lp = 0.5 * np.log(s2); Bl = t2l / (t2l + 1 / (2 * (n - 1))); lpost = Bl * lp + (1 - Bl) * l0; sdp = np.sqrt(np.exp(2 * lpost) + (1 - B) * v)
    l4 = np.mean([pin(yt, mp + sdp * stats.norm.ppf(t), t) for t in taus])
    for k, val in (("F3", l3), ("F6", l6), ("F4", l4)):
        rep = met[(met.issn == r.issn) & (met.origin == r.origin) & (met.method == k)].pinball.iloc[0]; errs[k].append(abs(val - rep))
out["independent_recompute_25_journal_origins_max_abs_pinball_diff"] = {k: float(max(v)) for k, v in errs.items()}
# data-quality scan
d = df[df.accepted.dt.year.between(2021, 2025)].copy()
out["share_D_le_7"] = float((d.D <= 7).mean()); out["share_D_le_14"] = float((d.D <= 14).mean())
out["accept_weekday_share"] = d.accepted.dt.weekday.value_counts(normalize=True).sort_index().round(4).to_dict()
out["received_weekday_share"] = d.received.dt.weekday.value_counts(normalize=True).sort_index().round(4).to_dict()
cnt = d.D.value_counts(); out["heaping_ratio_D_multiple_of_30_vs_neighbours"] = float(np.mean([cnt.get(k, 0) / ((cnt.get(k - 1, 1) + cnt.get(k + 1, 1)) / 2) for k in range(30, 361, 30)]))
out["heaping_ratio_D_multiple_of_7_vs_others"] = float(d.D[d.D % 7 == 0].shape[0] / (d.D.shape[0] / 7))
pj = d.groupby("issn").D.agg(med="median", p_le_10=lambda x: (x <= 10).mean(), n="size")
out["journals_with_median_le_30"] = int((pj.med <= 30).sum()); out["journals_with_share_D_le_10_gt_30pct"] = int((pj.p_le_10 > .3).sum())
out["journals_with_bimodal_flag_share_D_le_10_between_10_and_30pct"] = int(((pj.p_le_10 > .1) & (pj.p_le_10 <= .3)).sum())
json.dump(out, open(f"{ROOT}/reinforced/results/forensics.json", "w"), indent=1); print(json.dumps(out, indent=1))
