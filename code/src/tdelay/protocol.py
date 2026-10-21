"""Out-of-time split logic with leakage assertions (protocol section 5)."""
import numpy as np, pandas as pd

def split_journal_origin(dj: pd.DataFrame, t0: pd.Timestamp, cfg: dict):
    """dj: cleaned records of ONE journal. Returns (train12, train24, test) DataFrames.
    Visibility: a paper is visible at t0 iff first online (V) < t0 AND it was accepted and received before t0."""
    t0 = pd.Timestamp(t0)
    visible = dj[(dj["V"] < t0) & (dj["accepted"] < t0) & (dj["received"] < t0)]
    tr12 = visible[visible["V"] >= t0 - pd.Timedelta(days=cfg["train_window_days"])]
    tr24 = visible[visible["V"] >= t0 - pd.Timedelta(days=cfg["long_window_days"])]
    test = dj[(dj["received"] >= t0) & (dj["received"] < t0 + pd.Timedelta(days=cfg["horizon_days"]))]
    assert set(test["doi"]).isdisjoint(set(tr24["doi"])), "leakage: target paper visible at origin"
    assert (tr24["accepted"] < t0).all() and (tr24["V"] < t0).all()
    return tr12, tr24, test
