import json, os, sys
import numpy as np, pandas as pd, pytest
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from scipy.special import ndtr
from turnaround_forecast import forecast, claim_check, smoothed_quantiles, visible_sample, DEFAULT_TAU2

def synthetic(n=400, seed=0, median=120, sd=0.6):
    r = np.random.default_rng(seed); rec = pd.Timestamp("2025-01-01") + pd.to_timedelta(r.integers(0, 330, n), unit="D"); d = np.exp(np.log(median) + sd * r.standard_normal(n)).round().clip(1, 400)
    acc = rec + pd.to_timedelta(d, unit="D"); return pd.DataFrame(dict(received=rec - pd.Timedelta(days=0), accepted=acc, first_online=acc + pd.Timedelta(days=5)))

def test_smoothed_cdf_matches_levels():
    y = np.log(np.array([30, 60, 90, 120, 200, 300.])); q = smoothed_quantiles(y, 0.3)
    assert np.all(np.diff(q) > 0)
    for lev, v in zip(np.arange(.1, 1, .1), q): assert abs(ndtr((v - y) / 0.3).mean() - lev) < 1e-9

def test_zero_bandwidth_limit_is_empirical_like():
    y = np.log(np.linspace(20, 300, 500)); q = smoothed_quantiles(y, 1e-6); e = np.quantile(y, np.arange(.1, 1, .1)); assert np.max(np.abs(q - e)) < 0.02

def test_visibility_rule_excludes_future_and_unaccepted():
    rec = synthetic(); origin = "2025-09-01"; D = visible_sample(rec, origin)
    r = rec.copy(); ok = (r.first_online < pd.Timestamp(origin)) & (r.accepted < pd.Timestamp(origin)) & (r.first_online >= pd.Timestamp(origin) - pd.Timedelta(days=365)); assert len(D) == int(ok.sum())

def test_forecast_widens_with_tau2_and_orders_quantiles():
    rec = synthetic(); a = forecast(rec, "2025-12-01", tau2=0.0); b = forecast(rec, "2025-12-01", tau2=0.04)
    assert all(np.diff(a["quantiles_days"]) > 0) and all(np.diff(b["quantiles_days"]) > 0)
    assert (b["interval80_days"][1] - b["interval80_days"][0]) > (a["interval80_days"][1] - a["interval80_days"][0])

def test_claim_check_flags_fast_claims():
    rec = synthetic(median=60); ok = claim_check(rec, "2025-12-01", 200, 0.5); no = claim_check(rec, "2025-12-01", 30, 0.8)
    assert ok["supported_by_forecast"] and not no["supported_by_forecast"]

def test_too_few_papers_raises():
    with pytest.raises(ValueError): forecast(synthetic(n=20), "2025-12-01")

def test_default_tau2_is_positive():
    assert 0.0 < DEFAULT_TAU2 < 0.2

DATA = "/home/user/rp_c_8/data/processed/articles_clean.csv.gz"
@pytest.mark.skipif(not os.path.exists(DATA), reason="processed study data not available")
def test_matches_study_pipeline_on_20_journal_origins():
    sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src"); import d_lib
    df = pd.read_csv(DATA, parse_dates=["received", "accepted", "V"]); cfg = json.load(open("/home/user/rp_c_8/code/configs/config.json")); df["D"] = df.D.clip(upper=d_lib.CAP); df["y"] = np.log(df.D.astype(float))
    from tdelay import protocol as P
    rng = np.random.default_rng(3); n = 0
    for issn in rng.choice(df.issn.unique(), 60, replace=False):
        dj = df[df.issn == issn]
        for o in ("2024-01-01", "2024-07-01"):
            tr12, _, _ = P.split_journal_origin(dj, pd.Timestamp(o), dict(cfg, horizon_days=91))
            if len(tr12) < 100: continue
            ref = d_lib.smoothed_quantiles(tr12.y.to_numpy(), float(np.sqrt(0.04 + tr12.y.var(ddof=1) / len(tr12))))
            got = forecast(dj.rename(columns={"V": "first_online"})[["received", "accepted", "first_online"]], o, tau2=0.04)
            assert abs(got["n_visible"] - len(tr12)) == 0 and np.max(np.abs(np.log(got["quantiles_days"]) - ref)) < 6e-3  # output quantiles are rounded to 0.01 day
            n += 1
    assert n >= 20
