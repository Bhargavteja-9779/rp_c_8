"""POST-HOC diagnostic E10 (deviation D7), exploratory: separate right-truncation of the visible information set from genuine drift.
Variants of the F0 empirical forecaster per journal-origin (same eligibility and targets as E3):
  visible      : papers first online in the 12 months before t0 (the pre-registered information set)
  sub_trunc    : papers RECEIVED in [t0-365, t0) and already accepted before t0 (submission cohort, truncated at t0)
  sub_complete : papers RECEIVED in [t0-365, t0), accepted whenever (ORACLE: uses information from after t0)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
from tdelay import forecasters as F, scoring as S, stats as ST
ROOT = os.path.abspath(os.path.join(HERE, "..", "..")); cfg = json.load(open(f"{ROOT}/code/configs/config.json")); R = f"{ROOT}/results"
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); taus = np.asarray(cfg["taus"]); ia, ib = int(np.argmin(abs(taus - .1))), int(np.argmin(abs(taus - .9)))
rows = []
for t0s in cfg["origins"]:
    t0 = pd.Timestamp(t0s)
    for issn, dj in df.groupby("issn"):
        vis = dj[(dj.V < t0) & (dj.accepted < t0) & (dj.received < t0) & (dj.V >= t0 - pd.Timedelta(days=365))]
        test = dj[(dj.received >= t0) & (dj.received < t0 + pd.Timedelta(days=182))]
        if len(vis) < cfg["min_train"] or len(test) < cfg["min_test"]: continue
        sub = dj[(dj.received >= t0 - pd.Timedelta(days=365)) & (dj.received < t0)]
        trn = {"visible": vis, "sub_trunc": sub[sub.accepted < t0], "sub_complete": sub}
        yt = test.y.to_numpy()
        for k, tr in trn.items():
            if len(tr) < 30: continue
            fc = F.empirical(tr.y.to_numpy(), taus); rows.append(dict(issn=issn, origin=t0s, variant=k, n_train=len(tr), pinball=S.mean_pinball(yt, fc.q, taus), cov80=S.interval_coverage(yt, fc.q[ia], fc.q[ib]), median_train=float(np.median(tr.D)), median_test=float(np.median(test.D))))
o = pd.DataFrame(rows); o.to_csv(f"{R}/oracle_diagnostic_E10_EXPLORATORY.csv", index=False)
res = {}
for k, g in o.groupby("variant"):
    pj = g.groupby("issn")[["cov80", "pinball"]].mean(); m, lo, hi = ST.cluster_bootstrap_mean(pj.cov80.to_numpy() - 0.8, 2000, cfg["seed"]); res[k] = dict(n_journals=int(len(pj)), cov80_minus_nominal=m, ci95=[lo, hi], mean_pinball=float(pj.pinball.mean()), mean_n_train=float(g.n_train.mean()), median_ratio_train_to_test_median=float((g.median_train / g.median_test).median()))
json.dump(res, open(f"{R}/oracle_diagnostic_E10_EXPLORATORY.json", "w"), indent=1); print(json.dumps(res, indent=1))
