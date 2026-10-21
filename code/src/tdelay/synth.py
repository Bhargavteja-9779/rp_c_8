"""Synthetic article-level data with known generating process, used ONLY for pipeline tests / quick mode (never reported as evidence)."""
import numpy as np, pandas as pd

def make(n_journals=30, per_year=400, seed=1, sd_u=0.5, sd_v=0.0, sd_e=0.6, start="2021-01-01", end="2026-09-30"):
    rng = np.random.default_rng(seed); rows = []
    for j in range(n_journals):
        mu = 4.8 + sd_u * rng.normal()
        for yr in range(2021, 2027):
            mu_y = mu + sd_v * rng.normal(); n = per_year
            acc = pd.to_datetime(f"{yr}-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")
            D = np.maximum(1, np.round(np.exp(mu_y + sd_e * rng.normal(size=n)))).astype(int)
            rec = acc - pd.to_timedelta(D, unit="D"); V = acc + pd.to_timedelta(rng.integers(1, 30, n), unit="D")
            rows.append(pd.DataFrame(dict(doi=[f"10.0/{j}.{yr}.{i}" for i in range(n)], issn=f"J{j:03d}", title="A study", received=rec, accepted=acc, first_online=V,
                                          issued=V, V=V, n_authors=rng.integers(1, 8, n), n_refs=rng.integers(5, 80, n), D=D)))
    df = pd.concat(rows, ignore_index=True)
    df = df[(df.V <= pd.Timestamp(end)) & (df.received >= pd.Timestamp("2010-01-01"))].copy()
    df["y"] = np.log(df["D"].astype(float)); df["acc_year"] = df["accepted"].dt.year
    return df.reset_index(drop=True)
