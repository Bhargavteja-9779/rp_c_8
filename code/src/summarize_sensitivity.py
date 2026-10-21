import json, os, pandas as pd
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
rows = []
for name, d in [("primary", "results"), ("no C5 filter", "results_full_noC5"), ("eligibility 60/30", "results_full_min60_30")]:
    p = os.path.join(ROOT, d)
    if not os.path.exists(p + "/hypothesis_summary.json"): continue
    h = json.load(open(p + "/hypothesis_summary.json")); c = pd.read_csv(p + "/contrasts_pinball.csv").set_index("contrast"); cov = pd.read_csv(p + "/coverage_summary.csv").set_index("method")
    sk = pd.read_csv(p + "/pinball_skill_vs_F2.csv").set_index("method")["pinball_skill_vs_F2"]; g = pd.read_csv(p + "/guarantee_feasibility.csv")
    g72 = g[(g["T"] == 72) & (g.threshold == 0.5)].iloc[0]; n = pd.read_csv(p + "/metrics_journal_origin.csv"); 
    rows.append(dict(variant=name, n_journals=int(c.loc["F4 - F0", "n_journals"]), icc_journal=h["H1"]["icc_journal"], F0_cov80_minus_nominal=cov.loc["F0", "cov80_minus_nominal"], F4_cov80_minus_nominal=cov.loc["F4", "cov80_minus_nominal"],
                     F4_minus_F0_pinball=c.loc["F4 - F0", "mean_diff"], F6_minus_F0_pinball=c.loc["F6 - F0", "mean_diff"], F1_minus_F0_pinball=c.loc["F1 - F0", "mean_diff"], skill_F0_vs_F2=sk["F0"], skill_F6_vs_F2=sk["F6"],
                     share_P72_ge_0_5=g72.share, e7_rel_gain_vs_base=h["H5"]["rel_gain_vs_base"], drift_variance_ratio=h["H6_exploratory"]["variance_ratio"]))
o = pd.DataFrame(rows); o.to_csv(os.path.join(ROOT, "results", "sensitivity_summary.csv"), index=False); print(o.round(4).T.to_string())
