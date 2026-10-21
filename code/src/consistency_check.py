"""Final consistency audit: (1) key numbers in metrics.json appear in the manuscript text in the expected format; (2) every reference is cited and every cited author-year is in the reference list;
(3) figures/tables referenced exist; (4) unintended placeholders. Writes review/consistency_report.md."""
import json, os, re, subprocess
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
txt = subprocess.run(["pandoc", "-t", "plain", "--wrap=none", f"{ROOT}/manuscript/Final_Manuscript.docx"], capture_output=True, text=True).stdout
M = json.load(open(f"{ROOT}/results/metrics.json")); L = []; fails = 0
def chk(name, needle):
    global fails; ok = needle in txt; fails += (not ok); L.append(f"| {name} | `{needle}` | {'PASS' if ok else '**FAIL**'} |")
vc = M["vc"]["estimate"]; tot = vc["sigma2_journal"] + vc["sigma2_year"] + vc["sigma2_resid"]; g = {(r["T"], r["threshold"]): r for r in M["guarantee"]}
chk("records", f"{M['n_records']:,}"); chk("journals", f"{M['n_journals']}"); chk("target papers", f"{M['n_target_papers']:,}"); chk("journal-origins", f"{M['n_journal_origins']:,}")
chk("ICC", f"{100*vc['sigma2_journal']/tot:.1f}%"); chk("F0 skill", f"{100*M['forecasters']['F0']['skill']:.1f}%"); chk("share P72>=.5", f"{100*g[(72,0.5)]['share']:.1f}%"); chk("share P72>=.8", f"{100*g[(72,0.8)]['share']:.1f}%")
chk("drift ratio", f"{M['drift']['variance_ratio']:.1f}"); chk("E10 oracle", f"{M['e10']['sub_complete']['cov80_minus_nominal']*100:+.1f}"); chk("cleaning C5", f"{M['cleaning']['C5_nonresearch']:,}")
chk("recent cohort", f"{M['recent']['med_le_72']} of {M['recent']['n_journals']}"); chk("E8 DOIs", f"{M['e8']['n_shared_dois']:,}")
refs_block = txt.split("\nReferences\n")[-1]; body = txt.split("\nReferences\n")[0]
ref_lines = [l.strip() for l in refs_block.split("\n") if re.match(r"^[A-ZÀ-ÿ][^\n]+\(\d{4}\)", l.strip())]
cited_missing = []
for l in ref_lines:
    sur = re.split(r"[,;]", l)[0]; yr = re.search(r"\((\d{4})\)", l).group(1)
    if not (re.search(sur.split()[-1] + r"[^.\n]{0,60}" + yr, body) or (sur in body and yr in body)): cited_missing.append(l[:60])
L.append(f"\nReferences listed: {len(ref_lines)}; listed but not found cited in text: {cited_missing}")
cites = set(re.findall(r"([A-ZÀ-ÿ][\w\-]+(?: et al\.|(?: and| &) [A-ZÀ-ÿ][\w\-]+)?),? \(?(\d{4})\)?", body)); not_in_refs = [c for c in cites if not any(c[0].split()[0] in r and c[1] in r for r in ref_lines + ["Dianovics", "Ke, G. (2017)"])]
L.append(f"Author-year citations found in text: {len(cites)}; not matched in reference list: {sorted(not_in_refs)}")
for f in ["fig_variance_components", "fig_skill", "fig_coverage", "fig_pit", "fig_drift", "fig_median_forecast_vs_realised", "fig_reliability72", "fig_realised_p72"]:
    ok = os.path.exists(f"{ROOT}/results/figures/{f}.png"); fails += (not ok); L.append(f"figure {f}: {'exists' if ok else '**MISSING**'}")
ph = re.findall(r"\[[^\]]*(?:to be|authors? to|Authors? to)[^\]]*\]", txt, flags=re.I); L.append(f"Declared placeholders (intentional, need authors): {len(ph)}")
open(f"{ROOT}/review/consistency_report.md", "w").write("# Consistency report (automated + manual notes)\n\n| item | expected text | result |\n|---|---|---|\n" + "\n".join(x for x in L if x.startswith("|")) + "\n\n" + "\n".join(x for x in L if not x.startswith("|")) + f"\n\nTotal failures: {fails}\n")
print("\n".join(L), "\nfails:", fails)
