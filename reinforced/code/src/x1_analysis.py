"""X1 analysis of the preprint-date validity probe (uses the partial file written incrementally; the probe process was interrupted by a worker restart, so the sample is whatever was written)."""
import json, numpy as np, pandas as pd
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"
d = pd.read_csv(f"{OUT}/preprint_probe.csv.partial"); d = d.drop_duplicates("doi")
d["received"] = pd.to_datetime(d.received, format="mixed", errors="coerce"); d["accepted"] = pd.to_datetime(d.accepted, format="mixed", errors="coerce"); d["posted"] = pd.to_datetime(d.preprint_posted, errors="coerce"); d["delta"] = (d.received - d.posted).dt.days; d["D"] = (d.accepted - d.received).dt.days
d["server"] = np.where(d.preprint_doi.str.startswith("10.21203"), "ResearchSquare", np.where(d.preprint_doi.str.startswith("10.1101"), "bioRxiv/medRxiv", np.where(d.preprint_doi.str.startswith("10.48550"), "arXiv", "other")))
met = pd.read_csv(f"{ROOT}/results/metrics_journal_origin.csv"); f0 = met[met.method == "F0"]; fastj = set(f0[f0.test_median_days <= 60].issn) | set(f0[f0.median_fc_days <= 60].issn)
flag = set(json.load(open(f"{OUT}/X5_flagged_journals.json"))); d["fast_looking"] = d.issn.isin(fastj); d["flagged"] = d.issn.isin(flag)
def summ(g):
    return dict(n=int(len(g)), n_journals=int(g.issn.nunique()), median_delta=float(g.delta.median()), q25=float(g.delta.quantile(.25)), q75=float(g.delta.quantile(.75)), share_abs_le_14=float((g.delta.abs() <= 14).mean()), share_received_le_posted_plus_14=float((g.delta <= 14).mean()),
                share_received_gt_posted_plus_90=float((g.delta > 90).mean()), share_received_gt_posted_plus_180=float((g.delta > 180).mean()), median_D=float(g.D.median()))
res = {"n_records": int(len(d)), "n_journals": int(d.issn.nunique()), "by_server": {s: summ(g) for s, g in d.groupby("server")}}
rs = d[d.server == "ResearchSquare"]; res["ResearchSquare_fast_looking"] = summ(rs[rs.fast_looking]) if rs.fast_looking.any() else None; res["ResearchSquare_not_fast"] = summ(rs[~rs.fast_looking]); res["ResearchSquare_flagged"] = summ(rs[rs.flagged]) if rs.flagged.any() else None
res["ResearchSquare_by_member"] = {m: summ(g) for m, g in rs.groupby("member")}
# journal-level: share of journals (>=5 RS articles) whose median delta > 60 (received long after posting)
jj = rs.groupby("issn").delta.agg(["median", "size"]); jj = jj[jj["size"] >= 5]; res["ResearchSquare_journals_ge5"] = dict(n=int(len(jj)), median_of_medians=float(jj["median"].median()), share_median_gt_60=float((jj["median"] > 60).mean()), share_median_gt_30=float((jj["median"] > 30).mean()))
# among all servers excluding preprints posted before submission by design: negative delta fraction (preprint posted AFTER received)
res["note"] = "Research Square 'In Review' preprints are posted after the manuscript enters review; a median received-minus-posted of about -10 d is therefore expected if `received` is the original submission date."
json.dump(res, open(f"{OUT}/X1_summary.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float)[:4500])
