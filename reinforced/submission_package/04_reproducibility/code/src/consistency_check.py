"""Final consistency audit: every listed manuscript number is re-derived directly from a results file (not via the builder) and searched for in the DOCX text. Writes review/final_consistency_audit.md."""
import json, re, subprocess
ROOT = "/home/user/rp_c_8"; RR = f"{ROOT}/reinforced"
txt = subprocess.run(["pandoc", "-t", "plain", "--wrap=none", f"{RR}/manuscript/Revised_Manuscript.docx"], capture_output=True, text=True).stdout.replace("-", "−")
M = json.load(open(f"{ROOT}/results/metrics.json")); Z = json.load(open(f"{RR}/results/Z_summary.json")); X1 = json.load(open(f"{RR}/results/X1_summary.json")); Y1 = json.load(open(f"{RR}/results/Y1_panel_summary.json"))
f = lambda x, d=1: f"{100*x:.{d}f}".replace("-", "−"); sg = lambda x, d=1: f"{100*x:+.{d}f}".replace("-", "−")
vc = M["vc"]["estimate"]; tot = vc["sigma2_journal"] + vc["sigma2_year"] + vc["sigma2_resid"]
checks = [
 ("records", "results/metrics.json", f"{M['n_records']:,}"), ("target papers", "results/metrics.json", f"{M['n_target_papers']:,}"),
 ("journal ICC %", "metrics.json vc", f(vc["sigma2_journal"] / tot) + "%"), ("residual share %", "metrics.json vc", f(vc["sigma2_resid"] / tot) + "%"),
 ("F0 skill vs F2 %", "metrics.json forecasters.F0.skill", f(M["forecasters"]["F0"]["skill"]) + "%"),
 ("F0 coverage 80 shortfall (points)", "metrics.json", sg(M["forecasters"]["F0"]["cov80_minus"])),
 ("Z1 base_visible", "Z_summary.json", sg(Z["Z1"]["base_visible"]["est"])), ("Z1 half_visible", "Z_summary.json", sg(Z["Z1"]["half_visible"]["est"])), ("Z1 double_visible", "Z_summary.json", sg(Z["Z1"]["double_visible"]["est"])), ("Z1 base_oracle", "Z_summary.json", sg(Z["Z1"]["base_oracle"]["est"])),
 ("Z2 R shortfall", "Z_summary.json", sg(Z["Z2"]["R_shortfall"]["est"])), ("Z2 V shortfall", "Z_summary.json", sg(Z["Z2"]["V_shortfall"]["est"])), ("Z2 F4 shortfall", "Z_summary.json", sg(Z["Z2"]["F4_shortfall"]["est"])), ("Z2 F0 shortfall", "Z_summary.json", sg(Z["Z2"]["F0_shortfall"]["est"])),
 ("Z2 slope raw 72", "Z_summary.json", f"{Z['Z2']['brier_T72']['slope_raw']:.2f}"), ("Z2 slope cal 72", "Z_summary.json", f"{Z['Z2']['brier_T72']['slope_cal']:.2f}"),
 ("Z4 journal-weighted ≤14 d %", "Z_summary.json", f(Z["Z4"]["journal_weighted_le14"], 0) + "%"), ("Z4 journal-weighted >90 d %", "Z_summary.json", f(Z["Z4"]["journal_weighted_gt90"]) + "%"),
 ("Z5 pre-origin eligibility", "Z_summary.json", sg(Z["Z5"]["eligibility_pre_origin_only_n_test_ge_10"]["est"])),
 ("Z6 pooled panel", "Z_summary.json", sg(Z["Z6"]["pooled"])), ("Z6 block CI lo", "Z_summary.json", sg(Z["Z6"]["moving_block_ci"][0])), ("Z6 lag1", "Z_summary.json", f"{Z['Z6']['lag1_autocorr']:.2f}"),
 ("Z3 F0 shortfall imprint CI lo", "Z_summary.json", sg(Z["Z3"]["F0_shortfall_journal_mean_imprint_cluster"]["t6_ci"][0])), ("Z3 F0−F2 Holm", "Z_summary.json", "<0.001" if Z["Z3"]["F0-F2"]["p_t_holm"] < 0.001 else ""),
 ("X1 share ≤ +14 d (Springer Nature)", "X1_summary.json", f(X1["ResearchSquare_by_member"]["Springer Nature"]["share_received_le_posted_plus_14"], 0) + "%"),
 ("panel journal-origins", "Y1_panel_summary.json", f"{Y1['n_journal_origins']:,}"),
]
rows = []; bad = 0
for name, src, val in checks:
    ok = bool(val) and val in txt; bad += (not ok); rows.append(f"| {name} | `{src}` | {val} | {'found' if ok else '**NOT FOUND**'} |")
ph = sorted(set(re.findall(r"\[[^\]]*(?:to be completed|to be supplied|Authors to confirm|Date|Corresponding author)[^\]]*\]", txt)))
unres = re.findall(r"⟦|\bnan\b|None\b|\{[a-z_]+\}", txt)
nrefs = len(re.findall(r"^\d+\. ", txt.rsplit("References", 1)[-1], flags=re.M)); cites = {int(n) for grp in re.findall(r"\[(\d+(?:, \d+)*)\]", txt.rsplit("References", 1)[0]) for n in grp.split(", ")}
out = ["# Final consistency audit of `Revised_Manuscript.docx` (cycle 2)", "", f"Script: `reinforced/code/src/consistency_check.py` (re-derives each value from the results file, then searches the DOCX text). {len(checks) - bad}/{len(checks)} found.", "",
       "| Quantity | Source | Expected string | Result |", "|---|---|---|---|"] + rows + ["", f"- Unresolved markers (`⟦`, `nan`, `None`, braces): {len(unres)} ({unres[:5]})",
       f"- Reference list entries: {nrefs}; distinct numbers cited in text: {len(cites)}; cited but missing from list: {sorted(c for c in cites if c > nrefs)}; listed but never cited: {sorted(set(range(1, nrefs + 1)) - cites)}",
       f"- Placeholders left for authors ({len(ph)} distinct): {ph}", "- Abstract word count and main-text length are printed by `build_revised_manuscript.py`."]
open(f"{RR}/review/final_consistency_audit.md", "w").write("\n".join(out) + "\n"); print("\n".join(out)); 
