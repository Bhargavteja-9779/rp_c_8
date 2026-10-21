"""EXPLORATORY (not pre-registered as confirmatory): single-feature and leave-one-out ablations of the E7 article-level model, tau in {0.25,0.5,0.75}."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pandas as pd
from tdelay import experiments as E
ROOT = os.path.abspath(os.path.join(HERE, "..", "..")); cfg = json.load(open(os.path.join(ROOT, "code/configs/config.json")))
df = pd.read_csv(os.path.join(ROOT, "data/processed/articles_clean.csv.gz"), parse_dates=["received", "accepted", "V"]); df["acc_year"] = df.accepted.dt.year
fr = json.load(open(os.path.join(ROOT, "data/raw/frame_eligible.json"))); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)]
allf = ["n_authors", "rec_month", "rec_wd", "lref"]; rows = []
for name, fs in [("all", allf)] + [(f"only_{f}", [f]) for f in allf] + [(f"drop_{f}", [g for g in allf if g != f]) for f in allf]:
    r, pooled, _ = E.article_level_experiment(df, member, cfg, None, feats=fs, taus5=(0.25, 0.5, 0.75)); rows.append(dict(model=name, **pooled)); print(name, round(pooled["rel_gain_cov_vs_ctrl"], 4), flush=True)
pd.DataFrame(rows).to_csv(os.path.join(ROOT, "results", "article_level_ablation_EXPLORATORY.csv"), index=False)
