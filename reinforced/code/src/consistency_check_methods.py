"""Consistency audit of Methods_Manuscript.docx: each listed value is re-derived from a result file and searched for in the text."""
import json, re, subprocess
ROOT = "/home/user/rp_c_8"; RR = f"{ROOT}/reinforced"; RS = f"{RR}/results"
txt = subprocess.run(["pandoc", "-t", "plain", "--wrap=none", f"{RR}/manuscript/Methods_Manuscript.docx"], capture_output=True, text=True).stdout.replace("-", "−")
S = json.load(open(f"{RS}/D_summary.json")); S3 = json.load(open(f"{RS}/D_summary_cap365.json")); E = json.load(open(f"{RS}/D_external_summary.json")); SE = json.load(open(f"{RS}/D_sensitivity_cap_EXPLORATORY.json")); DF = json.load(open(f"{RS}/D_defaults_and_floor.json")); M = json.load(open(f"{ROOT}/results/metrics.json"))
sg = lambda x, d=1: f"{100*x:+.{d}f}".replace("-", "−"); f = lambda x, d=1: f"{100*x:.{d}f}".replace("-", "−")
sm = S["summary"]; ev = S["events"]; tr = E["transfer"]; h5 = S["HD5"]
checks = [("records", f"{M['n_records']:,}"), ("target papers (original)", f"{M['n_target_papers']:,}"), ("D-480 journals", f"{S['n_journals']}"), ("D-480 journal-origins", f"{S['n_journal_origins']:,}"), ("D-480 papers", f"{S['n_target_papers']:,}"),
 ("F0 signed", sg(sm["F0"]["signed_cov"]["est"])), ("CV0 signed", sg(sm["CV0"]["signed_cov"]["est"])), ("V signed", sg(sm["V"]["signed_cov"]["est"])), ("R signed", sg(sm["R"]["signed_cov"]["est"])), ("ACI signed", sg(sm["ACI"]["signed_cov"]["est"])),
 ("F0 abs", f(sm["F0"]["abs_err"]["est"], 2)), ("CV0 abs", f(sm["CV0"]["abs_err"]["est"], 2)), ("CVb abs", f(sm["CVb"]["abs_err"]["est"], 2)), ("floor", f(DF["noise_floor_abs_err"])),
 ("HD1 diff", f(S["HD1_CV0_vs_F0_abs_err"]["est"], 2)), ("HD1 imprint lo", f(S["HD1_CV0_vs_F0_abs_err"]["imprint_t_ci"][0], 2)), ("HD4 V", f(S["HD4"]["V"]["est"], 2)), ("HD4 R", f(S["HD4"]["R"]["est"], 2)), ("HD4 ACI", f(S["HD4"]["ACI"]["est"], 2)),
 ("HD5 r", f"{h5['corr_journal']:.2f}"), ("HD5 slope", f"{h5['slope']:.2f}"), ("HD5 r cap365", f"{S3['HD5']['corr_journal']:.2f}".replace("-", "−")),
 ("cap270", sg(SE["cap270_H91"]["est"])), ("cap365", sg(SE["cap365_H91"]["est"])), ("cap480", sg(SE["cap480_H91"]["est"])), ("cap none", sg(SE["cap1460_H91"]["est"])),
 ("T72 F0 slope", f"{ev['F0_T72']['slope']:.2f}"), ("T72 CV0 slope", f"{ev['CV0_T72']['slope']:.2f}"), ("T72 CV0 Brier", f"{ev['CV0_T72']['brier']:.5f}"),
 ("ext journals", f"{E['n_journals_evaluated']}"), ("ext journal-origins", f"{E['n_journal_origins']}"), ("ext papers", f"{E['n_target_papers']:,}"), ("ext F0 abs", f(tr["F0"]["abs_err"]["est"], 2)), ("ext CVg abs", f(tr["CVg"]["abs_err"]["est"], 2)), ("ext HD6 vs F0", f(E["HD6"]["CVg_vs_F0_abs_err"]["est"], 2)), ("ext HD6 vs V", f(E["HD6"]["CVg_vs_V_abs_err"]["est"], 2)),
 ("tau2 global", f"{DF['tau2_global']:.3f}")]
rows = []; bad = 0
for name, val in checks: ok = val in txt; bad += (not ok); rows.append(f"| {name} | {val} | {'found' if ok else '**NOT FOUND**'} |")
unres = re.findall(r"⟦|\bnan\b|None\b|\{[a-z_]+\}", txt); body, refs = txt.rsplit("References", 1); nrefs = len(re.findall(r"^\d+\. ", refs, flags=re.M)); cites = {int(n) for grp in re.findall(r"\[(\d+(?:, \d+)*)\]", body) for n in grp.split(", ")}
out = ["# Consistency audit of `Methods_Manuscript.docx` (cycle 3)", "", f"Script `reinforced/code/src/consistency_check_methods.py`: {len(checks) - bad}/{len(checks)} quantities found.", "", "| Quantity | Expected string | Result |", "|---|---|---|"] + rows + ["", f"- Unresolved markers: {len(unres)} {unres[:5]}", f"- References: {nrefs} listed, {len(cites)} distinct cited; cited but missing {sorted(c for c in cites if c > nrefs)}; listed but never cited {sorted(set(range(1, nrefs + 1)) - cites)}"]
open(f"{RR}/review/final_consistency_audit_methods.md", "w").write("\n".join(out) + "\n"); print("\n".join(out[:4]), "\n", "\n".join(out[-2:]), "\n", [r for r in rows if "NOT FOUND" in r])
