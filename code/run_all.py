"""Single entry point.  python run_all.py --mode quick   (synthetic data; pipeline check only, NOT evidence)
                        python run_all.py --mode full    (real cleaned data; confirmatory protocol v1.0)"""
import argparse, json, os, sys, time, platform
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "src"))
from tdelay import experiments as E, synth, stats as ST
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(HERE, ".."))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mode", choices=["quick", "full"], default="quick"); ap.add_argument("--variant", default="primary", help="primary|noC5|min60_30")
    a = ap.parse_args(); cfg = json.load(open(os.path.join(HERE, "configs/config.json")))
    out = os.path.join(ROOT, "results" if a.mode == "full" and a.variant == "primary" else f"results_{a.mode}_{a.variant}"); fig = os.path.join(out, "figures"); os.makedirs(fig, exist_ok=True)
    t_start = time.time(); elision = None
    if a.mode == "quick":
        df = synth.make(40, 400, seed=cfg["seed"], sd_u=0.5, sd_v=0.25, sd_e=0.6); member = {i: ("A" if k % 2 else "B") for k, i in enumerate(df.issn.unique())}; cfg["bootstrap_B"] = cfg["quick"]["bootstrap_B"]
    else:
        f = "articles_clean_noC5.csv.gz" if a.variant == "noC5" else "articles_clean.csv.gz"
        df = pd.read_csv(os.path.join(ROOT, "data/processed", f), parse_dates=["received", "accepted", "V"])
        fr = json.load(open(os.path.join(ROOT, "data/raw/frame_eligible.json"))); member = {j["issn"]: j["member"] for j in fr}
        if a.variant == "min60_30": elision = (60, 30)
    df = df[df.issn.isin(member)].copy(); df["acc_year"] = df["accepted"].dt.year
    # --- E1 data audit
    audit = dict(mode=a.mode, variant=a.variant, n_records=int(len(df)), n_journals=int(df.issn.nunique()), D_quantiles={str(q): float(df.D.quantile(q)) for q in (.05, .25, .5, .75, .95, .99)},
                 share_D_le_72=float((df.D <= 72).mean()), share_D_eq_1=float((df.D == 1).mean()), by_member=df.groupby(df.issn.map(member)).size().to_dict(), python=platform.python_version())
    # --- E3/E4/E6 forecasting
    met, pit, f5 = E.run_forecast_experiment(df, member, cfg, elision)
    met.to_csv(os.path.join(out, "metrics_journal_origin.csv"), index=False); pit.to_csv(os.path.join(out, "pit_counts.csv"), index=False); f5.to_csv(os.path.join(out, "f5_intervals.csv"), index=False)
    con = E.contrasts(met, cfg); con.to_csv(os.path.join(out, "contrasts_pinball.csv"), index=False)
    con_days = E.contrasts(met, cfg, "pinball_days"); con_days.to_csv(os.path.join(out, "contrasts_pinball_days.csv"), index=False)
    strata = E.size_strata(met, cfg); strata.to_csv(os.path.join(out, "size_strata_F4_vs_F0.csv"), index=False)
    cov = E.coverage_summary(met, f5, cfg); cov.to_csv(os.path.join(out, "coverage_summary.csv"), index=False)
    gsum = []; gall = None
    for T in cfg["thresholds_days"]:
        s, g = E.guarantee_feasibility(met, cfg, T); gsum.append(s)
        if T == 72: gall = g
    pd.concat(gsum).to_csv(os.path.join(out, "guarantee_feasibility.csv"), index=False); gall.to_csv(os.path.join(out, "realised_p72_by_journal_origin.csv"), index=False)
    rel = {m: E.reliability_table(met, 72, m) for m in ("F0", "F4")}; rel["F0"].to_csv(os.path.join(out, "reliability_p72_F0.csv"), index=False); rel["F4"].to_csv(os.path.join(out, "reliability_p72_F4.csv"), index=False)
    bs = pd.concat({T: E.brier_skill(met, T) for T in cfg["thresholds_days"]}, axis=1); bs.to_csv(os.path.join(out, "brier_skill_vs_F2.csv"))
    skill = (1 - E.per_journal(met, "pinball").mean() / E.per_journal(met, "pinball")["F2"].mean()).rename("pinball_skill_vs_F2"); skill.to_csv(os.path.join(out, "pinball_skill_vs_F2.csv"))
    summ = E.per_journal(met, "pinball").agg(["mean", "median"]).T; summ.to_csv(os.path.join(out, "pinball_by_method.csv"))
    # per-origin and per-member breakdowns (sensitivity)
    met.groupby(["origin", "method"])[["pinball", "cov80", "winkler80"]].mean().to_csv(os.path.join(out, "by_origin.csv"))
    met.groupby(["member", "method"])[["pinball", "cov80", "winkler80"]].mean().to_csv(os.path.join(out, "by_member.csv"))
    # --- E2 variance components
    vc, vci = E.variance_components(df, cfg); json.dump(dict(estimate=vc, ci95=vci), open(os.path.join(out, "variance_components.json"), "w"), indent=1)
    # --- E5 drift
    dr = E.drift_analysis(df, cfg); dr.to_csv(os.path.join(out, "drift_pairs.csv"), index=False)
    drift = dict(n_pairs=int(len(dr)), variance_ratio=float((dr.delta ** 2).mean() / dr.null_var.mean()), share_abs_delta_gt_0_2=float((dr.delta.abs() > 0.2).mean()), median_abs_delta=float(dr.delta.abs().median()))
    json.dump(drift, open(os.path.join(out, "drift_summary.json"), "w"), indent=1)
    # --- E7 article-level
    r7, pooled7, d7 = E.article_level_experiment(df, member, cfg, met); ci7 = E.article_level_ci(d7, cfg)
    r7.to_csv(os.path.join(out, "article_level_by_tau.csv")); json.dump(dict(pooled=pooled7, bootstrap=ci7), open(os.path.join(out, "article_level_summary.json"), "w"), indent=1)
    # --- leakage checks (assertions executed inside split_journal_origin for every journal-origin)
    json.dump(dict(visibility_assertions_executed=True, n_journal_origins=int(len(met[met.method == "F0"])), share_target_D_gt_730=float((d7.D > 730).mean()),
                   note="split_journal_origin asserts target/train DOI disjointness and train accepted<t0, V<t0 for every journal-origin"), open(os.path.join(out, "leakage_checks.json"), "w"), indent=1)
    json.dump(audit, open(os.path.join(out, "data_audit.json"), "w"), indent=1)
    # --- figures
    _figures(met, pit, cov, gall, rel, vc, vci, dr, df, fig, cfg)
    # --- hypotheses summary
    hyp = _hypotheses(vci, vc, cov, strata, pd.concat(gsum), ci7, drift, cfg); json.dump(hyp, open(os.path.join(out, "hypothesis_summary.json"), "w"), indent=1)
    json.dump(dict(elapsed_s=round(time.time() - t_start, 1), python=platform.python_version(), platform=platform.platform(), numpy=np.__version__, pandas=pd.__version__, cfg=cfg), open(os.path.join(out, "run_info.json"), "w"), indent=1)
    print("done", a.mode, a.variant, round(time.time() - t_start), "s ->", out)

def _hypotheses(vci, vc, cov, strata, gsum, ci7, drift, cfg):
    h = {}
    h["H1"] = dict(icc_journal=vc["icc_journal"], ci95=vci["icc_journal"], supported=bool(vci["icc_journal"][1] < 0.5))
    c0 = cov[cov.method == "F0"].iloc[0]
    h["H2"] = dict(F0_cov80_minus_nominal=c0.cov80_minus_nominal, ci95=[c0.ci_lo, c0.ci_hi], supported=bool(c0.ci_lo > 0.03 or c0.ci_hi < -0.03))
    h["H3"] = strata.to_dict("records")
    g = gsum[(gsum["T"] == 72) & (gsum.threshold == 0.5)].iloc[0]; h["H4"] = dict(share_ge_0_5=g.share, cp95=[g.cp_lo, g.cp_hi], supported=bool(g.cp_hi < 0.05))
    h["H5"] = dict(rel_gain_vs_base=ci7["rel_gain_vs_base"], ci95=ci7["ci_vs_base"], supported=bool(ci7["ci_vs_base"][1] < 0.02))
    h["H6_exploratory"] = dict(variance_ratio=drift["variance_ratio"], supported=bool(drift["variance_ratio"] > 1.5))
    return h

def _figures(met, pit, cov, gall, rel, vc, vci, dr, df, fig, cfg):
    cols = {"F0": "#1b6ca8", "F1": "#7a5195", "F2": "#8c8c8c", "F3": "#e08a1e", "F4": "#2a9d4e", "F6": "#c0392b"}
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
    # Fig: PIT
    f, ax = plt.subplots(1, 3, figsize=(7.2, 2.4), sharey=True)
    for a_, m in zip(ax, ("F0", "F3", "F4")):
        c = pit[pit.method == m][[f"b{k}" for k in range(10)]].sum().to_numpy(); a_.bar(range(10), c / c.sum(), color=cols[m]); a_.axhline(0.1, color="k", lw=.8, ls="--"); a_.set_title(m); a_.set_xlabel("PIT decile")
    ax[0].set_ylabel("share of test papers"); f.tight_layout(); f.savefig(os.path.join(fig, "fig_pit.png")); plt.close(f)
    # Fig: coverage distribution
    f, a_ = plt.subplots(figsize=(4.2, 2.8)); ms = ["F0", "F1", "F2", "F3", "F4", "F6"]
    a_.boxplot([met[met.method == m].groupby("issn")["cov80"].mean() for m in ms], tick_labels=ms, showfliers=False); a_.axhline(0.8, color="k", ls="--", lw=.8); a_.set_ylabel("out-of-time coverage of nominal 80% interval"); f.tight_layout(); f.savefig(os.path.join(fig, "fig_coverage.png")); plt.close(f)
    # Fig: skill by method
    f, a_ = plt.subplots(figsize=(4.2, 2.8)); w = E.per_journal(met, "pinball"); sk = [(1 - w[m] / w["F2"]).dropna() for m in ms]
    a_.boxplot(sk, tick_labels=ms, showfliers=False); a_.axhline(0, color="k", lw=.8); a_.set_ylabel("pinball skill vs publisher-pooled (F2)"); f.tight_layout(); f.savefig(os.path.join(fig, "fig_skill.png")); plt.close(f)
    # Fig: reliability of P(D<=72)
    f, a_ = plt.subplots(figsize=(3.6, 3.4))
    for m, r in rel.items(): a_.plot(r.mean_forecast, r.mean_realised, "o-", color=cols[m], label=m)
    a_.plot([0, 1], [0, 1], "k--", lw=.8); a_.set_xlabel("forecast P(D ≤ 72 d)"); a_.set_ylabel("realised share"); a_.legend(frameon=False); f.tight_layout(); f.savefig(os.path.join(fig, "fig_reliability72.png")); plt.close(f)
    # Fig: distribution of realised P72
    f, a_ = plt.subplots(figsize=(4.2, 2.8)); a_.hist(gall["real_72"], bins=np.linspace(0, 1, 21), color="#1b6ca8"); a_.set_xlabel("realised share of target papers accepted ≤ 72 d"); a_.set_ylabel("journal-origins"); f.tight_layout(); f.savefig(os.path.join(fig, "fig_realised_p72.png")); plt.close(f)
    # Fig: variance components
    f, a_ = plt.subplots(figsize=(3.8, 2.6)); parts = ["sigma2_journal", "sigma2_year", "sigma2_resid"]; tot = sum(vc[p] for p in parts)
    vals = [vc[p] / tot for p in parts]; a_.bar(["journal", "journal×year", "residual"], vals, color=["#1b6ca8", "#e08a1e", "#8c8c8c"])
    for i, p in enumerate(parts): a_.errorbar(i, vals[i], yerr=[[0], [0]], color="k")
    a_.set_ylabel("share of Var(ln D)"); f.tight_layout(); f.savefig(os.path.join(fig, "fig_variance_components.png")); plt.close(f)
    # Fig: drift
    f, a_ = plt.subplots(figsize=(4.2, 2.8)); a_.hist(dr.delta, bins=40, color="#7a5195"); a_.set_xlabel("Δ median ln D, year→year"); a_.set_ylabel("journal-year pairs"); f.tight_layout(); f.savefig(os.path.join(fig, "fig_drift.png")); plt.close(f)
    # Fig: D distribution
    f, a_ = plt.subplots(figsize=(4.2, 2.8)); a_.hist(df["y"], bins=60, color="#1b6ca8"); a_.axvline(np.log(72), color="k", ls="--", lw=.8); a_.set_xlabel("ln D (72 d dashed)"); a_.set_ylabel("articles"); f.tight_layout(); f.savefig(os.path.join(fig, "fig_distribution.png")); plt.close(f)
    # Fig: forecast median vs realised median
    f0 = met[met.method == "F0"]; f, a_ = plt.subplots(figsize=(3.6, 3.4)); a_.scatter(f0.median_fc_days, f0.test_median_days, s=6, alpha=.4, color="#1b6ca8")
    lim = [min(f0.median_fc_days.min(), f0.test_median_days.min()), max(f0.median_fc_days.max(), f0.test_median_days.max())]; a_.plot(lim, lim, "k--", lw=.8)
    a_.set_xscale("log"); a_.set_yscale("log"); a_.set_xlabel("F0 forecast median (days)"); a_.set_ylabel("realised median, target cohort (days)"); f.tight_layout(); f.savefig(os.path.join(fig, "fig_median_forecast_vs_realised.png")); plt.close(f)

if __name__ == "__main__": main()
