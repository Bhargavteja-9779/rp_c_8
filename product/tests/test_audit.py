import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from turnaround_forecast import timing_flags, group_alerts, batch_days

def journal(n=3000, seed=1, planted=None):
    r = np.random.default_rng(seed); rec = pd.Timestamp("2023-01-01") + pd.to_timedelta(r.integers(0, 700, n), unit="D"); d = np.exp(np.log(110) + 0.6 * r.standard_normal(n)).round().clip(3, 480)
    editor = r.integers(0, 12, n)
    if planted is not None: m = editor == planted; d[m] = (d[m] * 0.15).round().clip(2, None)
    acc = rec + pd.to_timedelta(d, unit="D"); return pd.DataFrame(dict(received=rec, accepted=acc, editor=editor))

def test_fast5_share_is_about_five_percent():
    f = timing_flags(journal()); s = f.fast5.dropna().mean(); assert 0.03 < s < 0.09

def test_no_alerts_without_planted_cluster():
    a = group_alerts(timing_flags(journal(seed=2)), "editor"); assert len(a) > 0 and not a.alert.any()

def test_planted_fast_editor_is_flagged():
    a = group_alerts(timing_flags(journal(seed=3, planted=5)), "editor"); assert a.iloc[0].group == 5 and bool(a.iloc[0].alert)

def test_small_strata_are_not_flagged():
    f = timing_flags(journal(n=150), min_stratum=1000); assert f.fast5.isna().all()

def test_batch_days_counts():
    j = journal(n=500, seed=4); j.loc[:29, "accepted"] = pd.Timestamp("2024-03-05"); j.loc[:29, "received"] = pd.Timestamp("2023-12-01")
    b = batch_days(timing_flags(j), threshold=10); assert b.iloc[0].n >= 30
