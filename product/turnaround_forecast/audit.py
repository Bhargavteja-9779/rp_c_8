"""Editorial timing audit (companion to the retraction study).

Computes, for the records of ONE journal, the within-journal-year timing percentile of every article, the same-day batch size and weekend flags used in the study,
and optional group-level alerts (for example by handling editor or special issue) when a group has more unusually fast acceptances than expected.

IMPORTANT: in the study, unusually fast acceptance relative to the same journal and year was associated with later retraction for peer-review-related reasons,
but only about 1 in 200 of the fastest 1% was retracted; flags are for prioritising editorial-office review of groups of articles, never evidence about a single paper.
"""
import numpy as np, pandas as pd
from scipy import stats

FAST_Q = 0.05

def timing_flags(records, min_stratum=100):
    """records: DataFrame with 'received' and 'accepted' (dates). Returns a copy with D, acceptance year, within-year percentile, fast5/slow95 flags,
    same-day batch size and weekend-acceptance flag. Strata with fewer than `min_stratum` articles get NaN percentile and flags."""
    r = records.copy(); r["received"] = pd.to_datetime(r["received"]); r["accepted"] = pd.to_datetime(r["accepted"])
    r["D"] = (r["accepted"] - r["received"]).dt.days; r = r[r.D >= 1].copy(); r["acc_year"] = r.accepted.dt.year
    size = r.groupby("acc_year").D.transform("size"); r["pct"] = r.groupby("acc_year").D.rank(pct=True, method="average").where(size >= min_stratum)
    q05 = r.groupby("acc_year").D.transform(lambda s: s.quantile(FAST_Q)); q95 = r.groupby("acc_year").D.transform(lambda s: s.quantile(1 - FAST_Q))
    r["fast5"] = np.where(size >= min_stratum, r.D <= q05, np.nan); r["slow95"] = np.where(size >= min_stratum, r.D >= q95, np.nan)
    r["batch_size"] = r.groupby("accepted").D.transform("size"); r["weekend_accept"] = (r.accepted.dt.dayofweek >= 5).astype(int)
    return r

def group_alerts(flags, group_col, min_group=20, alpha=0.05):
    """For each group (e.g. handling editor, special issue) compare the number of fast5 articles with the expected share given the stratum rates (exact binomial test,
    Bonferroni over groups tested). Returns a DataFrame sorted by p value; 'alert' is True where the adjusted p < alpha AND the group has more fast5 than expected."""
    f = flags[flags.fast5.notna()].copy(); f["fast5"] = f.fast5.astype(bool); exp = f.groupby("acc_year").fast5.mean(); f["exp"] = f.acc_year.map(exp); rows = []
    for g, d in f.groupby(group_col):
        if len(d) < min_group: continue
        k = int(d.fast5.sum()); n = len(d); p0 = float(d.exp.mean()); p = stats.binomtest(k, n, p0, alternative="greater").pvalue; rows.append(dict(group=g, n=n, fast5=k, expected=n * p0, ratio=k / (n * p0) if p0 > 0 else np.nan, p=p))
    out = pd.DataFrame(rows)
    if len(out): out["p_adj"] = np.minimum(1.0, out.p * len(out)); out["alert"] = out.p_adj < alpha; out = out.sort_values("p")
    return out

def batch_days(flags, threshold=10):
    """Calendar days on which at least `threshold` articles were accepted (candidate batch acceptances); a prompt for a look at the editorial log, not a finding."""
    d = flags.groupby("accepted").agg(n=("D", "size"), median_D=("D", "median")); return d[d.n >= threshold].sort_values("n", ascending=False)
