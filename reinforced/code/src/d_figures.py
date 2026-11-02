"""Figures for the Part D manuscript."""
import json, os
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = "/home/user/rp_c_8/reinforced/results"; FIG = "/home/user/rp_c_8/reinforced/figures"; os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 8.5, "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 9, "figure.dpi": 200})
BLUE, ORANGE, GREY, GREEN, RED = "#1f5fa8", "#d9822b", "#8a8f98", "#2a8c5a", "#b5453a"
S = json.load(open(f"{R}/D_summary.json")); S365 = json.load(open(f"{R}/D_summary_cap365.json")); sens = json.load(open(f"{R}/D_sensitivity_cap_EXPLORATORY.json"))
# Fig A: cap sensitivity
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1, 1.25]})
caps = [270, 365, 480, 1460]; lab = ["270", "365", "480", "none"]; x = np.arange(4)
for k, (H, col, off) in enumerate([(91, BLUE, -0.17), (182, ORANGE, 0.17)]):
    e = [100 * sens[f"cap{c}_H{H}"]["est"] for c in caps]; lo = [100 * sens[f"cap{c}_H{H}"]["lo"] for c in caps]; hi = [100 * sens[f"cap{c}_H{H}"]["hi"] for c in caps]
    ax[0].errorbar(x + off, e, yerr=[np.array(e) - lo, np.array(hi) - e], fmt="o", color=col, capsize=2, label=f"{H}-day target cohorts")
ax[0].axhline(0, color="k", lw=.6); ax[0].set_xticks(x); ax[0].set_xticklabels(lab); ax[0].set_xlabel("Duration cap (days)"); ax[0].set_ylabel("F0 80% coverage − 80 (points)"); ax[0].legend(frameon=False, loc="lower left", fontsize=7.5); ax[0].set_title("a  Shortfall depends on the cap", loc="left")
orig = sorted(S["by_origin_signed_cov"]["F0"].keys()); xo = np.arange(len(orig))
for m, c, ls in [("F0", GREY, "-"), ("V", ORANGE, "--"), ("R", RED, ":"), ("CV0", BLUE, "-")]:
    ax[1].plot(xo, [100 * S["by_origin_signed_cov"][m][o] for o in orig], ls, color=c, marker="o", ms=3, label=m)
ax[1].axhline(0, color="k", lw=.6); ax[1].set_xticks(xo); ax[1].set_xticklabels([o[:7] for o in orig], rotation=40, ha="right"); ax[1].set_ylabel("Coverage − 80 (points)"); ax[1].legend(frameon=False, ncol=4, fontsize=7.5, loc="upper center"); ax[1].set_title("b  Strict out-of-time origins (cap 480)", loc="left"); ax[1].set_ylim(-3.2, 3.2)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_d_cap_origins.png"); plt.close(fig)
# Fig B: mechanism deciles
d = np.array(S["HD5"]["deciles"]) * 100; fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.9))
ax[0].plot([d.min(), d.max()], [d.min(), d.max()], color=GREY, lw=.8, ls="--"); ax[0].plot(d[:, 0], d[:, 1], "o-", color=BLUE, ms=4); ax[0].set_xlabel("Predicted shortfall of F0 (points)\ncohort-shift model, earlier cohorts only"); ax[0].set_ylabel("Observed shortfall (points)"); ax[0].set_title("a  Deciles of journal-origins", loc="left")
ax[0].text(0.03, 0.95, "dashed: perfect prediction", transform=ax[0].transAxes, fontsize=7, va="top", color=GREY)
meths = ["F0", "F6", "V", "R", "ACI", "CV0", "CVb"]; ab = [100 * S["summary"][m]["abs_err"]["est"] for m in meths]; lo = [100 * S["summary"][m]["abs_err"]["lo"] for m in meths]; hi = [100 * S["summary"][m]["abs_err"]["hi"] for m in meths]
ax[1].bar(meths, ab, color=[GREY, GREY, GREY, GREY, GREY, BLUE, BLUE], yerr=[np.array(ab) - lo, np.array(hi) - ab], capsize=2); fl = 100 * json.load(open(f"{R}/D_defaults_and_floor.json"))["noise_floor_abs_err"]
ax[1].axhline(fl, color=RED, lw=1); ax[1].text(6.45, fl + .2, "sampling-noise floor", color=RED, fontsize=7, ha="right", bbox=dict(fc="white", ec="none", alpha=.85, pad=1)); ax[1].set_ylim(0, 8); ax[1].set_ylabel("Mean |coverage − 80| (points)"); ax[1].set_title("b  Per journal-origin error", loc="left")
fig.tight_layout(); fig.savefig(f"{FIG}/fig_d_mechanism_error.png"); plt.close(fig)
if os.path.exists(f"{R}/D_external_summary.json"):
    E = json.load(open(f"{R}/D_external_summary.json")); fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.9)); ms = ["F0", "F6", "V", "CVg", "CVb"]
    s_ = [100 * E["transfer"][m]["signed"]["est"] for m in ms]; l_ = [100 * E["transfer"][m]["signed"]["lo"] for m in ms]; h_ = [100 * E["transfer"][m]["signed"]["hi"] for m in ms]
    ax[0].bar(ms, s_, color=[GREY, GREY, GREY, BLUE, BLUE], yerr=[np.array(s_) - l_, np.array(h_) - s_], capsize=2); ax[0].axhline(0, color="k", lw=.6); ax[0].set_ylabel("Coverage − 80 (points)"); ax[0].set_title("a  Signed coverage error", loc="left")
    a_ = [100 * E["transfer"][m]["abs_err"]["est"] for m in ms]; l_ = [100 * E["transfer"][m]["abs_err"]["lo"] for m in ms]; h_ = [100 * E["transfer"][m]["abs_err"]["hi"] for m in ms]
    ax[1].bar(ms, a_, color=[GREY, GREY, GREY, BLUE, BLUE], yerr=[np.array(a_) - l_, np.array(h_) - a_], capsize=2); ax[1].set_ylabel("Mean |coverage − 80| (points)"); ax[1].set_title("b  Absolute error", loc="left"); ax[1].set_ylim(0, max(a_) * 1.25)
    fig.suptitle("External journals (frozen frame parameters)", fontsize=8.5, x=0.01, ha="left"); fig.tight_layout(); fig.savefig(f"{FIG}/fig_d_external.png"); plt.close(fig)
print("figures ok")
