"""Builds tables/*.md and results/metrics.json (every number quoted in the manuscript is read from metrics.json)."""
import json, os
import numpy as np, pandas as pd
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")); R = os.path.join(ROOT, "results"); T = os.path.join(ROOT, "tables"); os.makedirs(T, exist_ok=True)
cfg = json.load(open(os.path.join(ROOT, "code/configs/config.json")))
def md(df, path, floatfmt="{:.3f}"):
    cols = list(df.columns); lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows(): lines.append("| " + " | ".join(floatfmt.format(v) if isinstance(v, (float, np.floating)) else str(v) for v in r) + " |")
    open(path, "w").write("\n".join(lines) + "\n")
M = {}
audit = json.load(open(f"{R}/data_audit.json")); cl = pd.read_csv(f"{R}/cleaning_log.csv").set_index("rule")["n"]
M["n_journals"] = audit["n_journals"]; M["n_records"] = audit["n_records"]; M["n_raw_dated"] = int(cl["start"]); M["cleaning"] = cl.to_dict(); M["D_quantiles"] = audit["D_quantiles"]; M["share_D_le_72"] = audit["share_D_le_72"]; M["by_member"] = audit["by_member"]
fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); M["frame_journals"] = len(fr); M["frame_raw_journals"] = len(json.load(open(f"{ROOT}/data/raw/frame_raw.json")))
met = pd.read_csv(f"{R}/metrics_journal_origin.csv"); f0 = met[met.method == "F0"]
M["n_journal_origins"] = int(len(f0)); M["n_journals_forecast"] = int(met.issn.nunique()); M["n_target_papers"] = int(f0.n_test.sum()); M["n_train_papers_f0"] = int(f0.n_train.sum())
con = pd.read_csv(f"{R}/contrasts_pinball.csv"); cov = pd.read_csv(f"{R}/coverage_summary.csv"); pb = pd.read_csv(f"{R}/pinball_by_method.csv"); sk = pd.read_csv(f"{R}/pinball_skill_vs_F2.csv")
names = {"F0": "F0 empirical (12 mo)", "F1": "F1 empirical (24 mo)", "F2": "F2 publisher-pooled", "F3": "F3 lognormal MLE", "F4": "F4 empirical-Bayes lognormal", "F5": "F5 recent-holdout interval", "F6": "F6 time-decayed empirical"}
t3 = cov.merge(pb.rename(columns={"Unnamed: 0": "method", "mean": "mean_pinball"})[["method", "mean_pinball"]], on="method", how="left").merge(sk, on="method", how="left")
t3["Forecaster"] = t3.method.map(names); t3["Coverage of 80% interval minus 0.80 [95% CI]"] = t3.apply(lambda r: f"{r.cov80_minus_nominal:+.3f} [{r.ci_lo:+.3f}, {r.ci_hi:+.3f}]", axis=1)
t3o = t3[["Forecaster", "n_journals", "mean_pinball", "pinball_skill_vs_F2", "Coverage of 80% interval minus 0.80 [95% CI]", "mean_width80", "mean_winkler80"]].rename(columns={"n_journals": "Journals", "mean_pinball": "Mean pinball (ln-days)", "pinball_skill_vs_F2": "Skill vs F2", "mean_width80": "80% width (ln-days)", "mean_winkler80": "Winkler 80%"})
md(t3o, f"{T}/table3_forecasters.md"); t3o.to_csv(f"{T}/table3_forecasters.csv", index=False)
M["forecasters"] = {r.method: dict(pinball=float(r.mean_pinball), skill=float(r.pinball_skill_vs_F2) if pd.notna(r.pinball_skill_vs_F2) else None, cov80_minus=float(r.cov80_minus_nominal), ci=[float(r.ci_lo), float(r.ci_hi)], width80=float(r.mean_width80)) for r in t3.itertuples()}
c4 = con.copy(); c4["Mean difference [95% CI]"] = c4.apply(lambda r: f"{r.mean_diff:+.4f} [{r.ci_lo:+.4f}, {r.ci_hi:+.4f}]", axis=1); c4["p (Holm)"] = c4.p_holm.map(lambda v: "<0.001" if v < 0.001 else f"{v:.3f}")
c4o = c4[["contrast", "n_journals", "Mean difference [95% CI]", "median_rel_diff", "rbc", "p (Holm)"]].rename(columns={"contrast": "Contrast (loss A − loss B)", "n_journals": "Journals", "median_rel_diff": "Median relative diff.", "rbc": "Rank-biserial"})
md(c4o, f"{T}/table4_contrasts.md"); M["contrasts"] = con.set_index("contrast").to_dict("index")
vc = json.load(open(f"{R}/variance_components.json")); ve = json.load(open(f"{R}/external/e9_variance_components.json")); M["vc"] = vc; M["vc_ext"] = ve
t2 = pd.DataFrame([["Between journals", vc["estimate"]["sigma2_journal"], vc["estimate"]["sigma2_journal"] / sum(vc["estimate"][k] for k in ("sigma2_journal", "sigma2_year", "sigma2_resid"))],
                   ["Journal × acceptance year", vc["estimate"]["sigma2_year"], vc["estimate"]["sigma2_year"] / sum(vc["estimate"][k] for k in ("sigma2_journal", "sigma2_year", "sigma2_resid"))],
                   ["Residual (between articles)", vc["estimate"]["sigma2_resid"], vc["estimate"]["sigma2_resid"] / sum(vc["estimate"][k] for k in ("sigma2_journal", "sigma2_year", "sigma2_resid"))]], columns=["Component", "Variance of ln D", "Share"]); md(t2, f"{T}/table2_variance.md")
g = pd.read_csv(f"{R}/guarantee_feasibility.csv"); t6 = g.assign(**{"Share of journal-origins [95% CI]": g.apply(lambda r: f"{r.share:.3f} [{r.cp_lo:.3f}, {r.cp_hi:.3f}]", axis=1)})[["T", "threshold", "n_journal_origins", "k", "Share of journal-origins [95% CI]"]].rename(columns={"T": "T (days)", "threshold": "Realised P(D ≤ T) ≥", "k": "Journal-origins"}); md(t6, f"{T}/table6_guarantee.md"); M["guarantee"] = g.to_dict("records")
rel = pd.read_csv(f"{R}/reliability_p72_F0.csv"); M["reliability_F0_72"] = rel.to_dict("records"); md(rel, f"{T}/table6b_reliability_F0.md")
hyp = json.load(open(f"{R}/hypothesis_summary.json")); M["hyp"] = hyp
M["drift"] = json.load(open(f"{R}/drift_summary.json")); a7 = json.load(open(f"{R}/article_level_summary.json")); M["e7"] = a7
abl = pd.read_csv(f"{R}/article_level_ablation_EXPLORATORY.csv"); M["ablation"] = abl[["model", "rel_gain_cov_vs_ctrl"]].set_index("model")["rel_gain_cov_vs_ctrl"].to_dict(); md(abl[["model", "base", "ctrl", "cov", "rel_gain_cov_vs_base", "rel_gain_cov_vs_ctrl"]], f"{T}/table8b_ablation_exploratory.md", "{:.4f}")
ss = pd.read_csv(f"{R}/sensitivity_summary.csv"); md(ss.set_index("variant").T.reset_index().rename(columns={"index": "quantity"}), f"{T}/table7_sensitivity.md", "{:.4f}"); M["sensitivity"] = ss.set_index("variant").to_dict("index")
e8 = json.load(open(f"{R}/external/e8_crossref_vs_pubmed.json")); e9 = pd.read_csv(f"{R}/external/e9_summary.csv"); M["e8"] = e8; M["e9"] = e9.set_index("method").to_dict("index"); md(e9, f"{T}/table9_external.md", "{:.4f}")
M["by_origin"] = pd.read_csv(f"{R}/by_origin.csv").to_dict("records"); M["by_member"] = pd.read_csv(f"{R}/by_member.csv").to_dict("records")
st = pd.read_csv(f"{R}/size_strata_F4_vs_F0.csv"); M["strata"] = st.to_dict("records"); md(st, f"{T}/table5b_size_strata.md", "{:.4f}")
# descriptive recent-cohort statistics (exploratory, used in the Discussion)
d = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", usecols=["issn", "D", "accepted", "member"], parse_dates=["accepted"]); r = d[d.accepted >= "2025-04-20"]
gg = r.groupby("issn").D.agg(n="size", med="median", p72=lambda x: (x <= 72).mean()); gg = gg[gg.n >= 100]
M["recent"] = dict(n_journals=int(len(gg)), med_le_72=int((gg.med <= 72).sum()), p72_ge_50=int((gg.p72 >= .5).sum()), p72_ge_80=int((gg.p72 >= .8).sum()), window="accepted 2025-04-20..2026-10-20", share_by_member=gg.join(d.drop_duplicates("issn").set_index("issn").member).groupby("member").apply(lambda x: float((x.med <= 72).mean()), include_groups=False).to_dict())
dr = pd.read_csv(f"{R}/drift_pairs.csv"); M["drift_extra"] = dict(share_abs_gt_0_2=float((dr.delta.abs() > .2).mean()), share_abs_gt_0_5=float((dr.delta.abs() > .5).mean()), n_pairs=int(len(dr)))
f0 = f0.assign(over=f0.phat_72 >= .8); M["high_bin_72"] = dict(n_journals=int(f0[f0.over].issn.nunique()), n=int(f0.over.sum()), forecast=float(f0[f0.over].phat_72.mean()), realised=float(f0[f0.over].real_72.mean()))
pit = pd.read_csv(f"{R}/pit_counts.csv"); pf = pit[pit.method == "F0"][[f"b{k}" for k in range(10)]].sum(); M["pit_F0_top_decile"] = float(pf.iloc[-1] / pf.sum())
brier = pd.read_csv(f"{R}/brier_skill_vs_F2.csv"); M["brier_skill"] = brier.set_index("method").to_dict("index")
M["post"] = json.load(open(f"{R}/post_hoc_D6_EXPLORATORY.json")); M["e10"] = json.load(open(f"{R}/oracle_diagnostic_E10_EXPLORATORY.json")); M["sens_lt30"] = json.load(open(f"{R}/sensitivity_excl_median_lt30_EXPLORATORY.json"))
M["rev"] = json.load(open(f"{R}/revision_analyses_EXPLORATORY.json"))
M["shape"] = json.load(open(f"{R}/shape_diagnostics_EXPLORATORY.json"))
json.dump(M, open(f"{R}/metrics.json", "w"), indent=1, default=float)
rows = [(k, v["supported"] if isinstance(v, dict) and "supported" in v else None) for k, v in hyp.items() if k != "H3"]; print(rows); print("tables:", sorted(os.listdir(T)))
