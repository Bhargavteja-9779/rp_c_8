"""Cohort-shift smoothed empirical forecasts of time to acceptance (method CV0 of the accompanying paper).

Forecast distribution of ln(D), D = days from received to accepted (capped at 365):
    G(q) = (1/n) * sum_i Phi((q - y_i) / h),   h^2 = tau2 + s^2 / n
where y_i are the visible papers of the previous 12 months (first online and accepted before the origin), s^2 their variance
and tau2 the variance of the cohort-to-cohort location shift (default: learned from earlier complete cohorts, see defaults.json).
"""
import json, os
import numpy as np, pandas as pd
from scipy.special import ndtr

LEVELS = np.array([.1, .2, .3, .4, .5, .6, .7, .8, .9]); CAP = 365; WINDOW_DAYS = 365
_DEF = json.load(open(os.path.join(os.path.dirname(__file__), "defaults.json")))
DEFAULT_TAU2 = _DEF["tau2_global"]

def smoothed_quantiles(y, h, levels=LEVELS):
    y = np.asarray(y, float); levels = np.asarray(levels, float)
    lo = np.full(len(levels), y.min() - 8 * h - 1e-9); hi = np.full(len(levels), y.max() + 8 * h + 1e-9)
    for _ in range(60):
        mid = (lo + hi) / 2; Fm = ndtr((mid[:, None] - y[None, :]) / h).mean(axis=1); up = Fm < levels; lo = np.where(up, mid, lo); hi = np.where(up, hi, mid)
    return (lo + hi) / 2

def visible_sample(records, origin):
    """records: DataFrame with received, accepted (dates) and optionally first_online. Visible at origin: first online < origin, accepted < origin,
    received < origin, first online within the 12 months before origin. If first_online is missing the accepted date is used."""
    r = records.copy()
    for c in ("received", "accepted", "first_online"):
        if c in r: r[c] = pd.to_datetime(r[c], errors="coerce")
    if "first_online" not in r: r["first_online"] = r["accepted"]
    r["first_online"] = r["first_online"].fillna(r["accepted"]); origin = pd.Timestamp(origin)
    v = r[(r.first_online < origin) & (r.accepted < origin) & (r.received < origin) & (r.first_online >= origin - pd.Timedelta(days=WINDOW_DAYS))].dropna(subset=["received", "accepted"])
    d = (v.accepted - v.received).dt.days.clip(lower=1, upper=CAP)
    return d[d >= 1].to_numpy(float)

def forecast(records, origin, tau2=None, thresholds=(72, 120, 180), min_n=30):
    """Return dict with n_visible, quantiles (days) at LEVELS, 80% interval, and P(D <= T) from the smoothed forecast and from the raw empirical share."""
    tau2 = DEFAULT_TAU2 if tau2 is None else float(tau2); D = visible_sample(records, origin); n = len(D)
    if n < min_n: raise ValueError(f"only {n} visible papers; at least {min_n} are needed (the paper's evaluation used >= 100)")
    y = np.log(D); h = float(np.sqrt(tau2 + y.var(ddof=1) / n)); q = smoothed_quantiles(y, h); q0 = np.quantile(y, LEVELS, method="hazen")
    out = dict(origin=str(pd.Timestamp(origin).date()), n_visible=n, tau2=tau2, bandwidth=h, levels=LEVELS.tolist(), quantiles_days=np.exp(q).round(1).tolist(), raw_empirical_quantiles_days=np.exp(q0).round(1).tolist(),
               interval80_days=[float(np.exp(q[0]).round(1)), float(np.exp(q[-1]).round(1))], median_days=float(np.exp(q[4]).round(1)), capped_at_days=CAP)
    out["p_within_days"] = {int(T): float(ndtr((np.log(T) - y) / h).mean()) for T in thresholds}; out["raw_share_within_days"] = {int(T): float((D <= T).mean()) for T in thresholds}
    if n < 100: out["warning"] = "fewer than 100 visible papers: intervals were not validated in this regime"
    return out

def claim_check(records, origin, days, share, tau2=None):
    """Is a claim 'at least `share` of papers are accepted within `days` days' supported for the NEXT paper? Returns the smoothed probability and the raw past share."""
    f = forecast(records, origin, tau2, thresholds=(int(days),)); p = f["p_within_days"][int(days)]; raw = f["raw_share_within_days"][int(days)]
    return dict(claim=f"{share:.0%} within {days} d", forecast_probability_within=p, past_share_within=raw, supported_by_forecast=bool(p >= share), supported_by_past_share=bool(raw >= share), n_visible=f["n_visible"],
                note="Conditional on acceptance; a probability for the next accepted paper, not the chance that a submission is accepted.")
