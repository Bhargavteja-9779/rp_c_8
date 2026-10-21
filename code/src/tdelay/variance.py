"""Method-of-moments variance components for the nested model  y_ijk = mu + u_j + v_jk + e_ijk  (journal j, acceptance-year k, article i).
Cells with n_jk >= 2; journals need >= 2 cells. Capped sampling per cell is done by the caller."""
import numpy as np, pandas as pd

def cell_table(df, journal="issn", year="acc_year", y="y"):
    g = df.groupby([journal, year])[y]
    t = g.agg(n="size", mean="mean", var="var").reset_index()
    return t[t["n"] >= 2]

def components(cells: pd.DataFrame, journal="issn"):
    """Return dict(sigma2_journal, sigma2_year, sigma2_resid, icc_journal, icc_journal_year, n_journals, n_cells)."""
    cells = cells.copy(); cells["inv_n"] = 1.0 / cells["n"]
    sw = np.sum(cells["var"] * (cells["n"] - 1)) / np.sum(cells["n"] - 1)             # pooled within-cell variance
    per = []
    for j, c in cells.groupby(journal):
        K = len(c)
        if K < 2: continue
        s2 = c["mean"].var(ddof=1); per.append((K, s2, c["inv_n"].mean(), c["mean"].mean()))
    per = np.array(per)
    K, s2, invn, jm = per[:, 0], per[:, 1], per[:, 2], per[:, 3]
    sv = max(0.0, float(np.mean(s2 - sw * invn)))                                       # year-within-journal variance
    var_jm = np.var(jm, ddof=1)
    su = max(0.0, float(var_jm - np.mean(sv / K + sw * invn / K)))                     # between-journal variance
    tot = su + sv + sw
    return dict(sigma2_journal=su, sigma2_year=sv, sigma2_resid=float(sw), icc_journal=su / tot, icc_journal_year=(su + sv) / tot,
                n_journals=int(len(per)), n_cells=int(len(cells)))

def capped_sample(df, cap, seed, journal="issn", year="acc_year"):
    """Random cap on records per journal-year (reproducible): shuffle, then keep the first `cap` of each cell."""
    sh = df.sample(frac=1.0, random_state=seed)
    return sh[sh.groupby([journal, year]).cumcount() < cap]
