"""Loading, parsing and cleaning of article-level date records (protocol sections 3-4)."""
import glob, gzip, json, os, re
import numpy as np, pandas as pd

NONRESEARCH = re.compile(r"editorial|erratum|correction|corrigendum|retraction|publisher.?s note|expression of concern|withdrawal|book review|announcement|preface|in this issue|comment on|reply to", re.I)

def _parse_dates(s: pd.Series) -> pd.Series:
    """Parse ISO 'YYYY-MM-DD' or 'D Month YYYY' strings to datetime64; unparsable -> NaT."""
    s = s.astype("string").str.strip()
    out = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
    miss = out.isna() & s.notna() & (s != "")
    if miss.any():
        out[miss] = pd.to_datetime(s[miss], format="%d %B %Y", errors="coerce")
    miss = out.isna() & s.notna() & (s != "")
    if miss.any():
        out[miss] = pd.to_datetime(s[miss], format="%d %b %Y", errors="coerce")
    return out

def _parse_issued(s: pd.Series) -> pd.Series:
    """Crossref 'issued' joined as Y, Y-M or Y-M-D (no zero padding). Missing month -> July, missing day -> 15th."""
    parts = s.astype("string").str.split("-", expand=True).reindex(columns=[0, 1, 2])
    y = pd.to_numeric(parts[0], errors="coerce"); m = pd.to_numeric(parts[1], errors="coerce").fillna(7); d = pd.to_numeric(parts[2], errors="coerce").fillna(15)
    ok = y.notna() & m.between(1, 12) & d.between(1, 31)
    df = pd.DataFrame({"year": y[ok], "month": m[ok], "day": d[ok]})
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    out[ok] = pd.to_datetime(df, errors="coerce")
    return out

def read_crossref_dir(path: str, member_map: dict | None = None, max_journals: int | None = None) -> pd.DataFrame:
    files = sorted(glob.glob(os.path.join(path, "*.csv.gz")))
    if max_journals: files = files[:max_journals]
    frames = []
    for f in files:
        df = pd.read_csv(f, dtype=str, keep_default_na=False)
        if len(df): frames.append(df)
    raw = pd.concat(frames, ignore_index=True)
    for c in ["n_authors", "n_refs", "cited_by", "has_funder", "n_license"]:
        raw[c] = pd.to_numeric(raw[c], errors="coerce")
    raw["received"] = _parse_dates(raw["received"]); raw["accepted"] = _parse_dates(raw["accepted"])
    raw["first_online"] = _parse_dates(raw["first_online"]); raw["issued"] = _parse_issued(raw["issued"])
    raw["V"] = raw["first_online"].fillna(raw["issued"])
    if member_map is not None: raw["member"] = raw["issn"].map(member_map)
    return raw

def clean(raw: pd.DataFrame, cfg: dict, apply_c5: bool = True):
    """Apply cleaning rules C1-C6 in order; returns (clean_df, log_df) with counts removed per rule."""
    log = [("start", len(raw))]
    df = raw.drop_duplicates("doi", keep="first"); log.append(("C6_duplicate_doi_removed", len(raw) - len(df)))
    n = len(df); df = df[df["received"].notna() & df["accepted"].notna() & df["V"].notna()]; log.append(("C1_unparsable", n - len(df)))
    df = df.assign(D=(df["accepted"] - df["received"]).dt.days)
    n = len(df); df = df[(df["D"] >= cfg["d_min"]) & (df["D"] <= cfg["d_max"])]; log.append(("C2_D_out_of_range", n - len(df)))
    n = len(df); df = df[(df["accepted"] - df["V"]).dt.days <= cfg["accept_after_pub_tol_days"]]; log.append(("C3_accepted_after_pub", n - len(df)))
    n = len(df); df = df[df["received"] >= pd.Timestamp(cfg["received_min"])]; log.append(("C4_received_before_min", n - len(df)))
    if apply_c5:
        n = len(df)
        bad = df["title"].fillna("").str.contains(NONRESEARCH) | (df["n_refs"].notna() & (df["n_refs"] < cfg["min_refs"]))
        df = df[~bad]; log.append(("C5_nonresearch", n - len(df)))
    df = df.assign(y=np.log(df["D"].astype(float)))
    log.append(("final", len(df)))
    return df.reset_index(drop=True), pd.DataFrame(log, columns=["rule", "n"])
