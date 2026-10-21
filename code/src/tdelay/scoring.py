"""Proper scoring rules and calibration diagnostics for quantile / interval / event forecasts (protocol section 7)."""
import numpy as np

def pinball(y: np.ndarray, q: np.ndarray, tau: float) -> float:
    """Mean pinball (check) loss of quantile forecast q at level tau against observations y."""
    d = y - q
    return float(np.mean(np.maximum(tau * d, (tau - 1) * d)))

def mean_pinball(y: np.ndarray, qmat: np.ndarray, taus) -> float:
    """Average of pinball losses over quantile levels; qmat has shape (len(taus),) for a single forecast distribution."""
    return float(np.mean([pinball(y, qmat[i], t) for i, t in enumerate(taus)]))

def interval_coverage(y, lo, hi) -> float:
    return float(np.mean((y >= lo) & (y <= hi)))

def winkler(y, lo, hi, alpha: float) -> float:
    """Mean interval (Winkler) score for a central (1-alpha) interval; lower is better."""
    w = (hi - lo) + (2 / alpha) * np.maximum(lo - y, 0) + (2 / alpha) * np.maximum(y - hi, 0)
    return float(np.mean(w))

def brier(p: float, outcomes: np.ndarray) -> float:
    return float(np.mean((p - outcomes) ** 2))

def pit_ecdf(y: np.ndarray, train: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Randomised PIT values for an empirical-CDF forecast built from `train`."""
    s = np.sort(train); lo = np.searchsorted(s, y, side="left") / len(s); hi = np.searchsorted(s, y, side="right") / len(s)
    return lo + rng.random(len(y)) * (hi - lo)
