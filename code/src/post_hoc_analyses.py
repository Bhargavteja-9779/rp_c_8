"""POST-HOC (labelled deviation D6) analyses prompted by internal review: (a) journal-cluster bootstrap CI for the share of journals with realised P(D<=72)>=0.5 (origins within a journal are not independent);
(b) coarse title-keyword field coding of fast journals. Exploratory."""
import json, os, re
import numpy as np, pandas as pd
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")); R = os.path.join(ROOT, "results")
met = pd.read_csv(f"{R}/metrics_journal_origin.csv"); f0 = met[met.method == "F0"]
t = pd.read_csv(f"{ROOT}/data/processed/journal_titles.csv", index_col=0)["title"]; rng = np.random.default_rng(20261020)
out = {}
for thr in (0.5, 0.8):
    per = f0.groupby("issn").real_72.apply(lambda x: (x >= thr).mean())          # share of this journal's origins that reach thr
    est = float((f0.real_72 >= thr).mean()); reps = [(f0.set_index("issn").loc[rng.choice(per.index, len(per))].real_72 >= thr).mean() for _ in range(2000)]
    jany = float((f0.groupby("issn").real_72.max() >= thr).mean())
    out[f"thr{thr}"] = dict(share_origins=est, cluster_ci95=[float(np.quantile(reps, .025)), float(np.quantile(reps, .975))], share_journals_any_origin=jany)
FIELD = [("chemistry/materials/physics", r"chem|materials|polymer|physic|optic|plasmon|catal|nano|metal|ceram|laser|spectro|crystal|astronom|nuclear|fluoresc"),
         ("clinical medicine", r"oncolog|cancer|surg|cardi|clinic|medic|neuro|dermat|ophthalm|wound|ultrasound|rheumat|echocard|radiol|therapy|thorac|health|hepat|otolaryng|orthop|toxicol"),
         ("engineering/computing", r"engineer|comput|information|robot|civil|network|software|technolog|signal"), ]
def field(s):
    s = s.lower()
    for name, rx in FIELD:
        if re.search(rx, s): return name
    return "other/unclassified"
j = f0.groupby("issn").agg(max72=("real_72", "max")).reset_index(); j["field"] = j.issn.map(t).map(field)
fast = j[j.max72 >= .5]; tab = pd.DataFrame({"n_journals": j.field.value_counts(), "n_fast_ge_0.5": fast.field.value_counts()}).fillna(0).astype(int); tab["share_fast"] = tab["n_fast_ge_0.5"] / tab["n_journals"]
out["field_table"] = tab.reset_index().rename(columns={"index": "field"}).to_dict("records"); out["note"] = "coarse title-keyword coding by the analyst; not validated; exploratory"
json.dump(out, open(f"{R}/post_hoc_D6_EXPLORATORY.json", "w"), indent=1); print(json.dumps(out, indent=1)[:1800]); tab.to_csv(f"{R}/post_hoc_D6_field_table.csv")
