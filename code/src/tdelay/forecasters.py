"""Distributional forecasters of y = ln(D) built from visible training data (protocol section 6).
Each forecaster returns a `Forecast` with quantiles on the tau grid and a callable cdf(y)."""
from dataclasses import dataclass
import numpy as np
from scipy import stats

@dataclass
class Forecast:
    taus: np.ndarray
    q: np.ndarray            # quantiles of y at taus
    cdf: callable            # cdf(y) -> probability

def wquantile(values, weights, taus):
    """Hazen-type (type 5) weighted quantile: positions (cumw - w/2)/W with linear interpolation, clamped at the extremes (deviation D1)."""
    v = np.asarray(values, float); w = np.asarray(weights, float)
    o = np.argsort(v, kind="mergesort"); v, w = v[o], w[o]
    cw = np.cumsum(w); pos = (cw - 0.5 * w) / cw[-1]
    return np.interp(taus, pos, v)

def _wcdf(values, weights):
    v = np.asarray(values, float); w = np.asarray(weights, float)
    o = np.argsort(v, kind="mergesort"); v, w = v[o], w[o]; cw = np.cumsum(w) / w.sum()
    def cdf(y):
        i = np.searchsorted(v, y, side="right")
        return np.where(i == 0, 0.0, cw[np.clip(i - 1, 0, len(v) - 1)])
    return cdf

def empirical(y_train, taus):
    """F0 / F1: unweighted empirical quantiles and ECDF."""
    w = np.ones(len(y_train)); return Forecast(np.asarray(taus), wquantile(y_train, w, taus), _wcdf(y_train, w))

def pooled(y_list, taus):
    """F2: publisher-pooled forecaster; each journal's sample gets total weight 1 (weights 1/n_j)."""
    vals = np.concatenate(y_list); w = np.concatenate([np.full(len(y), 1.0 / len(y)) for y in y_list])
    return Forecast(np.asarray(taus), wquantile(vals, w, taus), _wcdf(vals, w))

def lognormal_mle(y_train, taus):
    """F3: normal on y = ln D (lognormal on D) with MLE parameters."""
    m, s = float(np.mean(y_train)), float(np.std(y_train, ddof=0)); s = max(s, 1e-6)
    return Forecast(np.asarray(taus), m + s * stats.norm.ppf(taus), lambda y: stats.norm.cdf(y, m, s))

def decayed(y_train, age_days, half_life, taus):
    """F6: exponentially time-decayed weighted empirical quantiles; age_days = days between visibility date and origin."""
    w = 0.5 ** (np.asarray(age_days, float) / half_life)
    return Forecast(np.asarray(taus), wquantile(y_train, w, taus), _wcdf(y_train, w))

def _dl_tau2(est, var):
    """DerSimonian-Laird between-journal variance and the resulting random-effects mean."""
    est, var = np.asarray(est, float), np.asarray(var, float)
    w = 1 / var; mbar = np.sum(w * est) / w.sum(); Q = np.sum(w * (est - mbar) ** 2)
    denom = w.sum() - np.sum(w ** 2) / w.sum()
    tau2 = max(0.0, (Q - (len(est) - 1)) / denom) if denom > 0 else 0.0
    ws = 1 / (tau2 + var); mu0 = np.sum(ws * est) / ws.sum()
    return tau2, mu0

class EBPrior:
    """Empirical-Bayes prior over journals estimated ONLY from visible training summaries (m_j, s2_j, n_j)."""
    def __init__(self, m, s2, n):
        m, s2, n = map(lambda a: np.asarray(a, float), (m, s2, n))
        ok = (n >= 5) & (s2 > 0)
        v_mu = s2[ok] / n[ok]
        self.tau2_mu, self.mu0 = _dl_tau2(m[ok], v_mu)
        l = 0.5 * np.log(s2[ok]); v_l = 1.0 / (2.0 * (n[ok] - 1))
        self.tau2_l, self.l0 = _dl_tau2(l, v_l)

    def forecast(self, y_train, taus):
        y = np.asarray(y_train, float); n = len(y); m = y.mean(); s2 = max(y.var(ddof=1), 1e-8)
        v_mu = s2 / n; B = self.tau2_mu / (self.tau2_mu + v_mu) if (self.tau2_mu + v_mu) > 0 else 0.0
        m_post = B * m + (1 - B) * self.mu0
        l = 0.5 * np.log(s2); v_l = 1.0 / (2.0 * (n - 1)); Bl = self.tau2_l / (self.tau2_l + v_l) if (self.tau2_l + v_l) > 0 else 0.0
        l_post = Bl * l + (1 - Bl) * self.l0
        var_pred = np.exp(2 * l_post) + (1 - B) * v_mu
        sd = float(np.sqrt(var_pred))
        return Forecast(np.asarray(taus), m_post + sd * stats.norm.ppf(taus), lambda yy: stats.norm.cdf(yy, m_post, sd))

def recent_holdout_interval(y_train, V_days_before_origin, taus_pair=(0.10, 0.90), alpha=0.2, recent_days=91):
    """F5 (interval only): quantiles from the older part of the window, symmetric expansion delta from the conformal quantile of
    nonconformity scores max(lo - y, y - hi) on the most recent `recent_days`. Returns (lo, hi)."""
    y = np.asarray(y_train, float); age = np.asarray(V_days_before_origin, float)
    old, rec = y[age > recent_days], y[age <= recent_days]
    if len(old) < 20 or len(rec) < 20: return np.nan, np.nan
    lo, hi = wquantile(old, np.ones(len(old)), list(taus_pair))
    s = np.maximum(lo - rec, rec - hi)
    k = int(np.ceil((1 - alpha) * (len(rec) + 1))); k = min(k, len(rec))
    delta = np.sort(s)[k - 1]
    return lo - delta, hi + delta
