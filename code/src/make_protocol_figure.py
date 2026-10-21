"""Figure 1: CONCEPTUAL schematic of the out-of-time protocol (not data)."""
import os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
plt.rcParams.update({"font.size": 8}); f, ax = plt.subplots(figsize=(7.2, 2.8))
ax.set_xlim(-26, 14); ax.set_ylim(-0.6, 3.4); ax.axis("off")
ax.annotate("", xy=(13.8, 0.2), xytext=(-25.5, 0.2), arrowprops=dict(arrowstyle="->", lw=1))
ax.plot([0, 0], [0.2, 3.0], color="k", lw=1.2); ax.text(0, 3.25, "origin $t_0$ (1 Jan 2023 or 1 Jan 2024)", ha="center", va="center")
ax.add_patch(plt.Rectangle((-12, 2.2), 12, 0.45, color="#1b6ca8")); ax.text(-12.4, 2.42, "T12: papers first online in the last 12 months\n(already accepted, visible to authors)", ha="right", va="center")
ax.add_patch(plt.Rectangle((-24, 1.4), 24, 0.45, color="#7a5195")); ax.text(-12, 1.62, "T24: 24-month window (used by F1, F6)", ha="center", va="center", color="w")
ax.add_patch(plt.Rectangle((0, 0.55), 6, 0.45, color="#e08a1e")); ax.text(3, 0.33, "target cohort: submitted in next 6 months", ha="center", va="center", color="k")
ax.annotate("", xy=(13.5, 0.77), xytext=(6.1, 0.77), arrowprops=dict(arrowstyle="->", color="#e08a1e", lw=1.2)); ax.text(9.8, 1.15, "accepted later: D = accept − submit", ha="center", color="#b36b00")
ax.text(0.2, 0.3, "", ha="left"); ax.text(-25.5, -0.25, "time", fontsize=8)
f.savefig(os.path.join(ROOT, "figures", "fig1_protocol_schematic.png"), dpi=200, bbox_inches="tight")
