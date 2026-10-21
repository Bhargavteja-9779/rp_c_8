"""Statistical utilities: cluster bootstrap over journals, paired Wilcoxon with rank-biserial effect size, Holm, Clopper-Pearson."""
import numpy as np
from scipy import stats

def cluster_bootstrap_mean(values, B=5000, seed=0, alpha=0.05):
    """Percentile CI for the mean of per-journal values (journal = cluster, one value per journal)."""
    v = np.asarray(values, float); v = v[~np.isnan(v)]; rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(v), size=(B, len(v))); means = v[idx].mean(axis=1)
    return float(v.mean()), float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))

def cluster_bootstrap_stat(arrays, stat_fn, B=5000, seed=0, alpha=0.05):
    """General percentile bootstrap over journals; `arrays` is a list of per-journal items passed to stat_fn(list_of_items)."""
    rng = np.random.default_rng(seed); n = len(arrays); est = stat_fn(arrays); reps = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, n); reps[b] = stat_fn([arrays[i] for i in idx])
    return float(est), float(np.quantile(reps, alpha / 2)), float(np.quantile(reps, 1 - alpha / 2))

def paired_wilcoxon(a, b):
    """Two-sided Wilcoxon signed-rank test on paired per-journal values a, b. Returns dict(p, rbc, median_diff, n).
    rbc = rank-biserial correlation = (W+ - W-)/(W+ + W-) over non-zero differences (positive: a > b)."""
    d = np.asarray(a, float) - np.asarray(b, float); d = d[~np.isnan(d)]; nz = d[d != 0]
    if len(nz) == 0: return dict(p=1.0, rbc=0.0, median_diff=0.0, n=len(d))
    r = stats.rankdata(np.abs(nz)); wp, wm = r[nz > 0].sum(), r[nz < 0].sum()
    p = stats.wilcoxon(nz, zero_method="wilcox", alternative="two-sided", method="auto").pvalue
    return dict(p=float(p), rbc=float((wp - wm) / (wp + wm)), median_diff=float(np.median(d)), n=int(len(d)))

def holm(pvals):
    """Holm-Bonferroni adjusted p-values (monotone)."""
    p = np.asarray(pvals, float); m = len(p); o = np.argsort(p); adj = np.empty(m); run = 0.0
    for rank, i in enumerate(o):
        run = max(run, (m - rank) * p[i]); adj[i] = min(1.0, run)
    return adj

def clopper_pearson(k, n, alpha=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - alpha / 2, k + 1, n - k)
    return float(lo), float(hi)
