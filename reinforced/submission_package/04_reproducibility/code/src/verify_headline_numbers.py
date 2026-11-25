"""Independent, deliberately short re-computation of the headline numbers of the Part E manuscript from data/processed/e_articles.csv.gz.
Run:  python3 verify_headline_numbers.py   (about 1 minute). It prints each number next to the value reported in the manuscript and says OK/DIFF.
Written so that a human author can read it in five minutes and see what the main result means: odds of retraction for the fastest 5% of papers, compared WITHIN the same journal and acceptance year."""
import json
import numpy as np, pandas as pd
ROOT = "/home/user/rp_c_8"
d = pd.read_csv(f"{ROOT}/data/processed/e_articles.csv.gz", low_memory=False)
rep = json.load(open(f"{ROOT}/reinforced/results/E_results.json")); summ = json.load(open(f"{ROOT}/reinforced/results/E_build_summary.json"))
def mh_or(df, exposure, outcome):
    """Mantel-Haenszel odds ratio over strata (journal x acceptance year): sum(a*d/n) / sum(b*c/n) for the 2x2 table of exposure vs outcome in each stratum."""
    e = df[exposure].astype(bool); o = df[outcome].astype(bool)
    t = pd.DataFrame({"s": df.stratum, "a": e & o, "b": e & ~o, "c": ~e & o, "d": ~e & ~o}).groupby("s").sum(); n = t.sum(axis=1)
    return float(((t.a * t.d / n).sum()) / ((t.b * t.c / n).sum()))
checks = []
def check(name, mine, reported, tol): checks.append((name, mine, reported, "OK" if abs(mine - reported) <= tol else "DIFF"))
check("articles", len(d), summ["n_articles"], 0); check("retracted (any)", int(d.R_any.sum()), summ["n_retracted"], 0); check("peer-review-related retractions", int(d.R_process.sum()), summ["n_process"], 0)
x = d[d.X1.notna()]; check("OR fastest 5% vs process-related retraction", mh_or(x, "X1", "R_process"), rep["A1"]["R_process"]["X1"]["or_mh"], 0.01)
check("OR fastest 5% vs any retraction", mh_or(x, "X1", "R_any"), rep["A1"]["R_any"]["X1"]["or_mh"], 0.01)
check("OR slowest 5% vs process-related", mh_or(x, "X2", "R_process"), rep["A1"]["R_process"]["X2"]["or_mh"], 0.01)
check("OR negative control (weekend receipt)", mh_or(d, "N1", "R_process"), rep["A1"]["R_process"]["N1"]["or_mh"], 0.01)
# fastest-5% flag recomputed from scratch: duration <= 5th percentile of the journal x acceptance-year stratum (strata with >= 100 articles)
sz = d.groupby("stratum").D.transform("size"); q05 = d.groupby("stratum").D.transform(lambda s: s.quantile(.05)); flag = (d.D <= q05) & (sz >= 100)
check("share of articles flagged fastest 5%", float(flag[sz >= 100].mean()), float(d.X1.mean()), 1e-9)
# crude (unstratified) odds ratio, to show why stratification matters
a = ((flag) & d.R_process).sum(); b = ((flag) & ~d.R_process).sum(); c = ((~flag) & (sz >= 100) & d.R_process).sum(); e = ((~flag) & (sz >= 100) & ~d.R_process).sum(); print("crude (unstratified) OR for comparison:", round(a * e / (b * c), 2))
for n_, m_, r_, s_ in checks: print(f"{n_:<48} computed {m_:>12.4f}  reported {r_:>12.4f}  {s_}")
