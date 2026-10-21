"""E8 (Crossref vs PubMed agreement on shared DOIs) and E9 (external validation of the forecasting protocol on PubMed-history journals of non-frame publishers)."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
from tdelay import data as Dm, experiments as E
ROOT = os.path.abspath(os.path.join(HERE, "..", "..")); cfg = json.load(open(os.path.join(ROOT, "code/configs/config.json"))); out = os.path.join(ROOT, "results", "external"); os.makedirs(out, exist_ok=True)
E8 = {"Sci Rep", "BMC Bioinformatics", "BMC Med Res Methodol", "BMC Public Health", "BMC Health Serv Res", "BMC Infect Dis", "BMC Geriatr", "J Med Case Rep", "Clin Epigenetics", "Harm Reduct J"}
pm = pd.concat([pd.read_csv(f, dtype={"pmid": str}) for f in sorted(glob.glob(os.path.join(ROOT, "data/raw/pubmed/*.csv")))], ignore_index=True)
for c in ("received", "accepted", "pubmed_date"): pm[c] = pd.to_datetime(pm[c], errors="coerce")
pm["doi"] = pm["doi"].fillna("").str.lower(); print("pubmed records:", len(pm), "journals:", pm.journal.nunique())
# ---- E8
cr = pd.read_csv(os.path.join(ROOT, "data/processed/articles_clean_noC5.csv.gz"), usecols=["doi", "issn", "received", "accepted"], parse_dates=["received", "accepted"]); cr["doi"] = cr["doi"].str.lower()
m = pm[pm.doi != ""].merge(cr, on="doi", suffixes=("_pm", "_cr"))
res = dict(n_shared_dois=int(len(m)), journals=sorted(m.journal.unique().tolist()))
if len(m):
    dr = (m.received_pm - m.received_cr).dt.days; da = (m.accepted_pm - m.accepted_cr).dt.days
    res.update(received_exact=float((dr == 0).mean()), accepted_exact=float((da == 0).mean()), received_within1=float((dr.abs() <= 1).mean()), accepted_within1=float((da.abs() <= 1).mean()),
               D_diff_median=float(((m.accepted_pm - m.received_pm).dt.days - (m.accepted_cr - m.received_cr).dt.days).median()), received_diff_abs_gt30=float((dr.abs() > 30).mean()))
    m.groupby("journal").apply(lambda g: pd.Series(dict(n=len(g), received_exact=(g.received_pm == g.received_cr).mean(), accepted_exact=(g.accepted_pm == g.accepted_cr).mean())), include_groups=False).to_csv(os.path.join(out, "e8_by_journal.csv"))
json.dump(res, open(os.path.join(out, "e8_crossref_vs_pubmed.json"), "w"), indent=1); print(json.dumps(res)[:600])
# ---- E9
overlap = m.groupby("journal").size().div(pm.groupby("journal").size()).fillna(0); frame_like = set(overlap[overlap > 0.5].index)   # journals whose DOIs are largely in the Crossref frame are NOT external
json.dump(sorted(frame_like), open(os.path.join(out, "e9_excluded_frame_overlap.json"), "w"))
e9 = pm[~pm.journal.isin(E8 | frame_like)].copy(); e9 = e9[e9.received.notna() & e9.accepted.notna() & e9.pubmed_date.notna()]
e9 = e9.assign(D=(e9.accepted - e9.received).dt.days, V=e9.pubmed_date, issn=e9.journal, member="PubMed-other", n_refs=np.nan, first_online=pd.NaT, issued=pd.NaT)
n0 = len(e9); e9 = e9[(e9.D >= 1) & (e9.D <= cfg["d_max"]) & ((e9.accepted - e9.V).dt.days <= cfg["accept_after_pub_tol_days"]) & ~e9.title.fillna("").str.contains(Dm.NONRESEARCH)]
e9["y"] = np.log(e9.D.astype(float)); e9["acc_year"] = e9.accepted.dt.year; e9 = e9.drop_duplicates("pmid")
print("E9 records", n0, "->", len(e9), "journals", e9.issn.nunique())
member = {j: "PubMed-other" for j in e9.issn.unique()}
met, pit, f5 = E.run_forecast_experiment(e9, member, cfg); met.to_csv(os.path.join(out, "e9_metrics.csv"), index=False)
summ = met.groupby("method").agg(n_journal_origins=("issn", "size"), pinball=("pinball", "mean"), cov80=("cov80", "mean"), winkler80=("winkler80", "mean")); w = E.per_journal(met, "pinball")
summ["skill_vs_F2"] = 1 - w.mean() / w["F2"].mean(); summ.to_csv(os.path.join(out, "e9_summary.csv")); print(summ.round(4))
vc, vci = E.variance_components(e9, dict(cfg, bootstrap_B=300)); json.dump(dict(estimate=vc, ci95=vci, n_records=int(len(e9)), n_journals=int(e9.issn.nunique()), n_journal_origins=int((met.method == "F0").sum())), open(os.path.join(out, "e9_variance_components.json"), "w"), indent=1)
print(vc)
