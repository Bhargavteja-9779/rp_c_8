"""Load all Crossref per-journal files, parse and clean (protocol section 4); writes data/processed/articles_clean.csv.gz and cleaning log."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import pandas as pd
from tdelay import data as D
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
cfg = json.load(open(os.path.join(ROOT, "code/configs/config.json")))
fr = json.load(open(os.path.join(ROOT, "data/raw/frame_eligible.json"))); member = {j["issn"]: j["member"] for j in fr}; title = {j["issn"]: j["title"] for j in fr}
raw = D.read_crossref_dir(os.path.join(ROOT, "data/raw/crossref"), member)
print("raw dated records:", len(raw), "journals:", raw.issn.nunique())
for tag, c5 in (("", True), ("_noC5", False)):
    clean, log = D.clean(raw, cfg, apply_c5=c5)
    clean["acc_year"] = clean["accepted"].dt.year
    clean.drop(columns=["first_online", "issued", "page", "cited_by", "has_funder", "n_license"]).to_csv(os.path.join(ROOT, f"data/processed/articles_clean{tag}.csv.gz"), index=False)
    log.to_csv(os.path.join(ROOT, f"results/cleaning_log{tag}.csv"), index=False); print(tag or "primary"); print(log.to_string(index=False))
pd.Series(title).rename("title").to_csv(os.path.join(ROOT, "data/processed/journal_titles.csv"))
