"""Figures for the Part E manuscript."""
import json, os
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = "/home/user/rp_c_8/reinforced/results"; FIG = "/home/user/rp_c_8/reinforced/figures"; os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 8.5, "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 9, "figure.dpi": 200})
BLUE, ORANGE, GREY, RED, GREEN = "#1f5fa8", "#d9822b", "#8a8f98", "#b5453a", "#2a8c5a"
A = json.load(open(f"{R}/E_results.json")); B = json.load(open(f"{R}/E_results2.json")); C6 = json.load(open(f"{R}/E_results6.json")); BS = json.load(open(f"{R}/E_build_summary.json"))
# ---- Fig 2 dose response + forest
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw={"width_ratios": [1.15, 1]})
ks = sorted((int(k) for k in A["A2"])); x = [5 * k + 2.5 for k in ks]; est = [A["A2"][str(k)]["or_mh"] for k in ks]; lo = [A["A2"][str(k)]["ci_cluster"][0] for k in ks]; hi = [A["A2"][str(k)]["ci_cluster"][1] for k in ks]
ax[0].errorbar(x, est, yerr=[np.array(est) - np.maximum(lo, 1e-2), np.array(hi) - est], fmt="o-", color=BLUE, ms=3.5, lw=1, capsize=1.5); ax[0].axhline(1, color="k", lw=.6); ax[0].set_yscale("log"); ax[0].set_ylim(0.03, 40)
ax[0].set_xlabel("Within journal-year percentile of time to acceptance"); ax[0].set_ylabel("Odds ratio of peer-review-process retraction\n(vs 45th–55th percentile)"); ax[0].set_title("a  Dose-response", loc="left"); ax[0].set_xticks([0, 25, 50, 75, 100])
labs = [("X1", "Fastest 5% in journal-year"), ("X2", "Slowest 5%"), ("X3", "Accepted ≤ 7 days"), ("X4", "Batch ≥ 5 same day"), ("X4b", "Batch ≥ 10 same day"), ("X5", "Weekend acceptance"), ("N1", "Received on weekend (neg. control)")]
for off, out, col in ((0.16, "R_process", BLUE), (-0.16, "R_any", ORANGE)):
    for i, (k, lab) in enumerate(labs):
        v = A["A1"][out][k]; y = len(labs) - 1 - i + off; ax[1].plot([max(v["ci_cluster"][0], 0.02), v["ci_cluster"][1]], [y, y], color=col, lw=1.3); ax[1].plot(v["or_mh"], y, "o", color=col, ms=3.5, label=("process-related retraction" if out == "R_process" else "any retraction") if i == 0 else None)
ax[1].axvline(1, color="k", lw=.6); ax[1].set_xscale("log"); ax[1].set_xlim(0.02, 20); ax[1].set_yticks(range(len(labs))); ax[1].set_yticklabels([l for _, l in labs][::-1], fontsize=7.5); ax[1].set_xlabel("Odds ratio (journal-cluster 95% CI)"); ax[1].legend(frameon=False, fontsize=7, loc="upper right"); ax[1].set_title("b  Timing exposures", loc="left")
fig.tight_layout(); fig.savefig(f"{FIG}/fig_e_doseresponse_forest.png"); plt.close(fig)
# ---- Fig 3 PIT bands and subtype/heterogeneity
fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.9), gridspec_kw={"width_ratios": [1.1, 1, 1]})
bands = list(B["A9"]["bands"]["R_process"].keys()); w = .38; xb = np.arange(len(bands))
for off, out, col, lab in ((-w / 2, "R_process", BLUE, "process-related"), (w / 2, "R_any", ORANGE, "any")): ax[0].bar(xb + off, [1000 * B["A9"]["bands"][out][b]["mean"] for b in bands], w, color=col, label=lab)
ax[0].set_xticks(xb); ax[0].set_xticklabels(bands, rotation=40, ha="right", fontsize=7); ax[0].set_ylabel("Retractions per 1,000 articles"); ax[0].set_xlabel("Out-of-time timing score (PIT) band"); ax[0].legend(frameon=False, fontsize=7); ax[0].set_title("a  Retraction rate by score", loc="left")
sub = [("compromised peer review", "Compromised\npeer review"), ("rogue editor", "Rogue editor"), ("paper mill", "Paper mill"), ("concerns/issues about peer review", "Peer-review\nconcerns"), ("R_other", "All other\nreasons")]
for i, (k, lab) in enumerate(sub[::-1]):
    v = B["A8"][k]; ax[1].plot([max(v["ci_cluster"][0], .2), v["ci_cluster"][1]], [i, i], color=BLUE if k != "R_other" else GREY, lw=1.4); ax[1].plot(v["or_mh"], i, "o", color=BLUE if k != "R_other" else GREY, ms=4)
ax[1].axvline(1, color="k", lw=.6); ax[1].set_xscale("log"); ax[1].set_xlim(.4, 30); ax[1].set_yticks(range(len(sub))); ax[1].set_yticklabels([l for _, l in sub][::-1], fontsize=7); ax[1].set_xlabel("OR, fastest 5% (cluster CI)"); ax[1].set_title("b  Retraction reason", loc="left")
yrs = sorted(A["A4"]["by_year"], key=int); ax[2].errorbar(range(len(yrs)), [A["A4"]["by_year"][y]["or_mh"] for y in yrs], yerr=[[A["A4"]["by_year"][y]["or_mh"] - max(A["A4"]["by_year"][y]["ci_cluster"][0], .05) for y in yrs], [A["A4"]["by_year"][y]["ci_cluster"][1] - A["A4"]["by_year"][y]["or_mh"] for y in yrs]], fmt="o-", color=BLUE, capsize=2, ms=4)
ax[2].axhline(1, color="k", lw=.6); ax[2].set_yscale("log"); ax[2].set_xticks(range(len(yrs))); ax[2].set_xticklabels(yrs); ax[2].set_xlabel("Acceptance year"); ax[2].set_ylabel("OR, fastest 5%"); ax[2].set_title("c  By acceptance year", loc="left")
fig.tight_layout(); fig.savefig(f"{FIG}/fig_e_score_reasons_years.png"); plt.close(fig)
# ---- Fig 1 design schematic
fig, ax = plt.subplots(figsize=(7.4, 2.4)); ax.axis("off")
boxes = [(0.00, f"Crossref deposit\nreceived and accepted dates\n{BS['n_articles']:,} articles,\n800 journals\n(Springer Nature, Wiley,\nTaylor & Francis)"), (0.26, "Timing exposures\nwithin journal × acceptance year:\nfastest 5%, slowest 5%, ≤ 7 d,\nbatch days, weekend;\nout-of-time score (PIT)"), (0.55, f"Retraction Watch database\n{BS['n_retracted']:,} matched retractions;\nreasons (peer review,\nrogue editor, paper mill,\ncomputer-generated content)"), (0.82, "Analyses\nstratified odds ratios,\nfixed-effects logistic model,\nout-of-time AUC, lift,\nnumber needed to screen")]
for x0, t in boxes: ax.text(x0 + .085, .5, t, ha="center", va="center", fontsize=7.5, bbox=dict(boxstyle="round,pad=0.5", fc="#eef3fa", ec=BLUE, lw=1))
for x0, x1 in ((0.17, 0.215), (0.43, 0.49), (0.70, 0.76)): ax.annotate("", xy=(x1, .5), xytext=(x0, .5), arrowprops=dict(arrowstyle="->", color=GREY))
fig.savefig(f"{FIG}/fig_e_design.png", bbox_inches="tight"); plt.close(fig)
# ---- Fig 4 heterogeneity across journals and strata definitions
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.4), gridspec_kw={"width_ratios": [1.35, 1]}); J = C6["A16"]["journals"][:15][::-1]
for i, v in enumerate(J):
    lo, hi = np.exp(v["log_or"] - 1.96 * v["se"]), np.exp(v["log_or"] + 1.96 * v["se"]); ax[0].plot([max(lo, .03), min(hi, 300)], [i, i], color=BLUE, lw=1.2); ax[0].plot(np.exp(v["log_or"]), i, "s", color=BLUE, ms=3 + 2 * np.sqrt(v["events"] / 100))
ax[0].axvline(1, color="k", lw=.6); ax[0].axvline(C6["A16"]["pooled_or"], color=ORANGE, lw=1.2, ls="--"); ax[0].set_xscale("log"); ax[0].set_yticks(range(len(J))); ax[0].set_yticklabels([f"{v['issn']} ({v['events']})" for v in J], fontsize=6.5)
ax[0].set_xlabel("Odds ratio of the fastest 5% (journal level)"); ax[0].set_title(f"a  Journals with most events (pooled {C6['A16']['pooled_or']:.1f}; I² {100*C6['A16']['I2']:.0f}%)", loc="left", fontsize=8)
names = [("year", "Journal × year\n(primary)"), ("quarter", "Journal × quarter"), ("month", "Journal × month")]
for i, (k, lab) in enumerate(names[::-1]):
    v = C6["A17"][k]; ax[1].plot([max(v["ci_cluster"][0], .5), v["ci_cluster"][1]], [i, i], color=BLUE, lw=1.4); ax[1].plot(v["or_mh"], i, "o", color=BLUE, ms=4)
ax[1].axvline(1, color="k", lw=.6); ax[1].set_xlim(.5, 9); ax[1].set_yticks(range(3)); ax[1].set_yticklabels([l for _, l in names][::-1], fontsize=7.5); ax[1].set_xlabel("OR of the fastest 5% (cluster CI)"); ax[1].set_title("b  Finer strata", loc="left")
fig.tight_layout(); fig.savefig(f"{FIG}/fig_e_heterogeneity.png"); plt.close(fig); print("figs ok")
