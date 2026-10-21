"""Y3: article-type / batch / fast-lane robustness of the headline quantities."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from tdelay import experiments as E, stats as ST, variance as V
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); cfg["bootstrap_B"] = 2000
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)].copy(); df["acc_year"] = df.accepted.dt.year
cnt = df.groupby(["issn", "accepted"]).doi.transform("size"); span = df.groupby("issn").accepted.transform(lambda x: (x.max() - x.min()).days + 1); rate = df.groupby("issn").doi.transform("size") / span
df["batch"] = (cnt >= 10) & (cnt >= 5 * rate)
fl = df[df.acc_year.between(2021, 2025)].groupby("issn").D.apply(lambda x: (x <= 14).mean()); fastlane = set(fl[fl >= .10].index)
variants = {"base": df, "refs>=10": df[df.n_refs.fillna(0) >= 10], "refs>=15": df[df.n_refs.fillna(0) >= 15], "no_batch_records": df[~df.batch], "no_fastlane_journals": df[~df.issn.isin(fastlane)],
            "combined(refs>=15,no_batch,no_fastlane)": df[(df.n_refs.fillna(0) >= 15) & ~df.batch & ~df.issn.isin(fastlane)]}
out = {"n_batch_records": int(df.batch.sum()), "share_batch": float(df.batch.mean()), "n_fastlane_journals": len(fastlane)}
for name, d in variants.items():
    met, _, _ = E.run_forecast_experiment(d, member, cfg); f0 = met[met.method == "F0"]; w = met.groupby(["issn", "method"]).pinball.mean().unstack()
    cov = f0.groupby("issn").cov80.mean().sub(0.8); icc = V.components(V.cell_table(V.capped_sample(d[d.acc_year.isin(cfg["vc_years"])], cfg["vc_cap_per_journal_year"], cfg["seed"])))["icc_journal"]
    out[name] = dict(n_records=int(len(d)), n_journal_origins=int(len(f0)), n_journals=int(f0.issn.nunique()), shortfall=dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(cov.to_numpy(), 2000, cfg["seed"]))), skill_F0_vs_F2=float(1 - w.F0.mean() / w.F2.mean()),
                     F4_minus_F0=float((w.F4 - w.F0).mean()), F6_minus_F0=float((w.F6 - w.F0).mean()), share_P72_ge_0_5=float((f0.real_72 >= .5).mean()), share_P72_ge_0_8=float((f0.real_72 >= .8).mean()), icc_journal=float(icc), median_D=float(d.D.median()))
    print(name, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out[name].items() if k != "shortfall"}, round(out[name]["shortfall"]["est"], 4), flush=True)
json.dump(out, open(f"{OUT}/Y3_type_robustness.json", "w"), indent=1, default=float)
