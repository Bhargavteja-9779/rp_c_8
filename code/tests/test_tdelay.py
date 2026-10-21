import json, sys, numpy as np, pandas as pd, pytest
sys.path.insert(0, "src")
from tdelay import scoring as S, forecasters as F, protocol as P, variance as V, stats as ST, data as Dm, synth, experiments as E
CFG = json.load(open("configs/config.json"))

def test_pinball_known_value():
    assert S.pinball(np.array([1.0, 3.0]), np.array([2.0, 2.0]), 0.5) == pytest.approx(0.5)
    assert S.pinball(np.array([3.0]), np.array([2.0]), 0.9) == pytest.approx(0.9)
    assert S.pinball(np.array([1.0]), np.array([2.0]), 0.9) == pytest.approx(0.1)

def test_winkler_and_coverage():
    assert S.winkler(np.array([5.0]), 0.0, 4.0, 0.2) == pytest.approx(4 + 10 * 1)
    assert S.interval_coverage(np.array([1, 5]), 0, 4) == 0.5

def test_wquantile_equal_weights_median():
    assert F.wquantile([1, 2, 3, 4, 5], np.ones(5), [0.5])[0] == pytest.approx(3.0)

def test_holm_and_cp():
    assert list(ST.holm([0.01, 0.04, 0.03])) == pytest.approx([0.03, 0.06, 0.06])
    lo, hi = ST.clopper_pearson(0, 10); assert lo == 0 and hi == pytest.approx(0.3085, abs=1e-3)

def test_visibility_no_overlap_and_assertions():
    df = synth.make(3, 300, seed=2)
    for issn, dj in df.groupby("issn"):
        for t0 in CFG["origins"]:
            tr12, tr24, te = P.split_journal_origin(dj, pd.Timestamp(t0), CFG)
            assert set(te.doi).isdisjoint(tr24.doi)
            assert tr24["accepted"].max() < pd.Timestamp(t0) and te["received"].min() >= pd.Timestamp(t0)

def test_eb_prior_depends_only_on_training():
    df = synth.make(12, 300, seed=3); m = {i: "A" for i in df.issn.unique()}
    per, prior1, _ = E._prep_origin(df, m, "2023-01-01", CFG)
    df2 = df.copy(); mask = df2.received >= pd.Timestamp("2023-01-01"); df2.loc[mask, "y"] += 5.0   # perturb ALL post-origin outcomes
    per2, prior2, _ = E._prep_origin(df2, m, "2023-01-01", CFG)
    assert (prior1.mu0, prior1.l0, prior1.tau2_mu) == (prior2.mu0, prior2.l0, prior2.tau2_mu)

def test_calibration_under_iid_lognormal():
    df = synth.make(40, 500, seed=4, sd_u=0.5, sd_v=0.0, sd_e=0.6); m = {i: "A" for i in df.issn.unique()}
    cfg = dict(CFG)
    met, pit, f5 = E.run_forecast_experiment(df, m, cfg)
    cov = met.groupby("method")["cov80"].mean()
    for k in ["F0", "F3", "F4"]: assert abs(cov[k] - 0.8) < 0.03, cov
    pj = met.groupby("method")["pinball"].mean(); assert pj["F3"] < pj["F2"] and pj["F4"] <= pj["F3"] * 1.01
    assert abs(f5["cov80"].mean() - 0.8) < 0.05

def test_drift_breaks_coverage_and_is_detected():
    df = synth.make(40, 500, seed=5, sd_u=0.5, sd_v=0.4, sd_e=0.6); m = {i: "A" for i in df.issn.unique()}
    met, _, _ = E.run_forecast_experiment(df, m, CFG); assert met[met.method == "F0"]["cov80"].mean() < 0.74
    r = E.drift_analysis(df, CFG); assert (r.delta ** 2).mean() / r.null_var.mean() > 1.5

def test_variance_components_recovery():
    df = synth.make(150, 300, seed=6, sd_u=0.5, sd_v=0.3, sd_e=0.6)
    est = V.components(V.cell_table(V.capped_sample(df[df.acc_year.between(2021, 2025)], 300, 1)))
    assert est["sigma2_journal"] == pytest.approx(0.25, rel=0.25) and est["sigma2_year"] == pytest.approx(0.09, rel=0.25) and est["sigma2_resid"] == pytest.approx(0.36, rel=0.1)

def test_cleaning_rules():
    raw = pd.DataFrame(dict(doi=["a", "a", "b", "c", "d", "e"], issn="X", title=["T", "T", "Editorial note", "T", "T", "T"],
        received=pd.to_datetime(["2023-01-01"] * 6), accepted=pd.to_datetime(["2023-03-01", "2023-03-01", "2023-03-01", "2023-01-01", "2023-03-01", "2030-01-01"]),
        first_online=pd.to_datetime(["2023-03-10"] * 5 + ["2023-03-10"]), issued=pd.NaT, V=pd.to_datetime(["2023-03-10"] * 6), n_refs=[30, 30, 30, 30, 2, 30]))
    out, log = Dm.clean(raw, CFG)
    assert list(out.doi) == ["a"], (out.doi.tolist(), log)
