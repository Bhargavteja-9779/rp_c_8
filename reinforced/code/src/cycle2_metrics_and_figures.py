"""Collects all cycle-2 results into reinforced/results/metrics_cycle2.json and draws cycle-2 figures (reinforced/figures)."""
import json, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT = "/home/user/rp_c_8"; R = f"{ROOT}/reinforced/results"; FIG = f"{ROOT}/reinforced/figures"; L = lambda n: json.load(open(f"{R}/{n}"))
M = dict(forensics=L("forensics.json"), cal_meta=L("cal_meta_summary.json"), x456=L("X4_X5_X6_summary.json"), y0=L("Y0_imprint_inference.json"), y1=L("Y1_panel_summary.json"), y2=L("Y2_summary.json"), y3=L("Y3_type_robustness.json"), y45=L("Y4_Y5_summary.json"), x1=L("X1_summary.json"), z=L("Z_summary.json"))
dr = pd.read_csv(f"{ROOT}/results/drift_pairs.csv"); mad = 1.4826 * np.median(np.abs(dr.delta - np.median(dr.delta)))
M["drift_robust"] = dict(ratio_mean_sq=float((dr.delta ** 2).mean() / dr.null_var.mean()), ratio_robust_mad=float(mad ** 2 / np.median(dr.null_var)), top5pct_share_of_sumsq=float(np.sort(dr.delta ** 2)[::-1][:int(0.05 * len(dr))].sum() / (dr.delta ** 2).sum()))
f0 = pd.read_csv(f"{ROOT}/results/metrics_journal_origin.csv"); f0 = f0[f0.method == "F0"]; M["paper_level_coverage_F0"] = float((f0.cov80 * f0.n_test).sum() / f0.n_test.sum()); M["journal_mean_coverage_F0"] = float(f0.cov80.mean())
json.dump(M, open(f"{R}/metrics_cycle2.json", "w"), indent=1, default=float)
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 160}); col = {"F0": "#1b6ca8", "F0cal": "#2a9d4e", "g": "#8c8c8c", "o": "#e08a1e"}
# Fig A: rolling panel
P = pd.read_csv(f"{R}/Y1_panel_metrics.csv"); f, ax = plt.subplots(1, 2, figsize=(7.2, 2.7))
o = P[P.method == "F0"].groupby("origin").cov80.mean(); ax[0].plot(range(len(o)), (o - 0.8) * 100, "o-", color=col["F0"], label="F0 (empirical, 12 mo)")
oc = P[P.method == "F0cal"].groupby("origin").cov80.mean()
if len(oc): ax[0].plot([list(o.index).index(i) for i in oc.index], (oc - 0.8) * 100, "s-", color=col["F0cal"], label="F0 recalibrated (out of time)")
ax[0].axhline(0, color="k", lw=.8); ax[0].set_xticks(range(len(o))); ax[0].set_xticklabels([x[2:7] for x in o.index], rotation=60); ax[0].set_ylabel("coverage − 80 (points)"); ax[0].legend(frameon=False, fontsize=7); ax[0].set_title("Quarterly origins, equal follow-up (D ≤ 480 d)", fontsize=8)
im = P[P.method == "F0"].groupby("imprint").agg(s=("cov80", "mean"), n=("issn", "nunique")); im["s"] = (im.s - 0.8) * 100; im = im.sort_values("s"); ax[1].barh(im.index, im.s, color=col["F0"]); ax[1].axvline(0, color="k", lw=.8); ax[1].set_xlabel("shortfall (points)"); ax[1].set_title("By imprint (DOI prefix)", fontsize=8)
f.tight_layout(); f.savefig(f"{FIG}/fig_c2_panel.png"); plt.close(f)
# Fig B: observed shortfall vs null worlds and cohort-variance simulations
z = M["z"]; z1 = z["Z1"]; y2 = M["y2"]; e10 = json.load(open(f"{ROOT}/results/oracle_diagnostic_E10_EXPLORATORY.json")); f, a = plt.subplots(figsize=(6.2, 3.0))
items = [("Observed:\nvisible set", y2["cov_visible"]["est"], y2["cov_visible"]["lo"], y2["cov_visible"]["hi"], col["F0"]), ("Observed:\ncomplete cohort", e10["sub_complete"]["cov80_minus_nominal"], e10["sub_complete"]["ci95"][0], e10["sub_complete"]["ci95"][1], col["F0"]),
         ("Null: random\nsplit", y2["cov_exchangeable"]["est"], y2["cov_exchangeable"]["lo"], y2["cov_exchangeable"]["hi"], col["g"]), ("Null: growth +\nvisibility, no drift", y2["cov_sim_nodrift"]["est"], y2["cov_sim_nodrift"]["lo"], y2["cov_sim_nodrift"]["hi"], col["g"]),
         ("Cohort effects\nσ²/2", z1["half_visible"]["est"], z1["half_visible"]["lo"], z1["half_visible"]["hi"], col["o"]), ("Cohort effects\nσ² (RQ1)", z1["base_visible"]["est"], z1["base_visible"]["lo"], z1["base_visible"]["hi"], col["o"]), ("Cohort effects\nσ², oracle", z1["base_oracle"]["est"], z1["base_oracle"]["lo"], z1["base_oracle"]["hi"], col["o"])]
v = np.array([x[1] for x in items]) * 100; lo = np.array([x[2] for x in items]) * 100; hi = np.array([x[3] for x in items]) * 100
a.bar(range(len(items)), v, yerr=[v - lo, hi - v], color=[x[4] for x in items], capsize=3); a.axhline(0, color="k", lw=.8); a.set_xticks(range(len(items))); a.set_xticklabels([x[0] for x in items], fontsize=6); a.set_ylabel("coverage − 80 (points)"); f.tight_layout(); f.savefig(f"{FIG}/fig_c2_null.png"); plt.close(f)
# Fig C: preprint probe
d = pd.read_csv(f"{R}/preprint_probe.csv.partial").drop_duplicates("doi"); d["delta"] = (pd.to_datetime(d.received, format="mixed", errors="coerce") - pd.to_datetime(d.preprint_posted, errors="coerce")).dt.days
rs = d[(d.preprint_doi.str.startswith("10.21203")) & (d.member == "Springer Nature")]; f, a = plt.subplots(figsize=(4.4, 2.8)); a.hist(rs.delta.clip(-120, 240), bins=np.arange(-120, 245, 6), color=col["F0"]); a.axvline(0, color="k", lw=.8); a.set_xlabel("received − preprint posting date (days; clipped to −120…240)"); a.set_ylabel("articles"); a.set_title("Springer Nature articles with a Research Square preprint", fontsize=8); f.tight_layout(); f.savefig(f"{FIG}/fig_c2_preprint.png"); plt.close(f)
print(json.dumps(M["drift_robust"]), M["paper_level_coverage_F0"], M["journal_mean_coverage_F0"])
