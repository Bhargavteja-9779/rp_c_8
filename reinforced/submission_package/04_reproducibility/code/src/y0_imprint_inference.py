"""Y0: imprint-cluster inference for v1 contrasts, H2 specification curve, shortfall by imprint, E9 journal count."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd
from tdelay import stats as ST
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); rng = np.random.default_rng(cfg["seed"]); B = 5000
d = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", usecols=["doi", "issn"]); d["pre"] = d.doi.str.split("/").str[0]
mode = d.groupby("issn").pre.agg(lambda x: x.value_counts().index[0]); names = {"10.1007": "Springer", "10.1186": "BMC", "10.1038": "Nature", "10.1002": "Wiley", "10.1111": "Blackwell", "10.1080": "T&F"}
imprint = mode.map(lambda p: names.get(p, "other")); imprint.to_csv(f"{OUT}/journal_imprint_map.csv")
met = pd.read_csv(f"{ROOT}/results/metrics_journal_origin.csv"); met["imprint"] = met.issn.map(imprint)
w = met.groupby(["issn", "method"]).pinball.mean().unstack(); imp = imprint.loc[w.index]; res = {}
def imprint_boot(v, g):
    v = pd.Series(v); g = pd.Series(g, index=v.index); cl = {k: v[g == k].to_numpy() for k in g.unique()}; ks = list(cl); out = []
    for _ in range(B):
        pick = rng.choice(ks, len(ks)); x = np.concatenate([cl[k] for k in pick]); out.append(x.mean())
    means = {k: float(cl[k].mean()) for k in ks}
    return dict(est=float(v.mean()), lo=float(np.quantile(out, .025)), hi=float(np.quantile(out, .975)), imprint_means=means, n_imprints=len(ks), sign_consistent=int(max((np.array(list(means.values())) > 0).sum(), (np.array(list(means.values())) < 0).sum())))
pairs = [("F4", "F0"), ("F3", "F0"), ("F1", "F0"), ("F6", "F0"), ("F0", "F2"), ("F4", "F6"), ("F4", "F3")]
from scipy import stats
for a, b in pairs:
    dd = (w[a] - w[b]).dropna(); r = imprint_boot(dd.to_numpy(), imp.loc[dd.index].to_numpy()); m = np.array(list(r["imprint_means"].values())); r["imprint_ttest_p"] = float(stats.ttest_1samp(m, 0).pvalue); res[f"{a}-{b}"] = r
f0 = met[met.method == "F0"]; pj = f0.groupby("issn").cov80.mean().sub(0.8); res["F0_shortfall_journal_mean_imprint_cluster"] = imprint_boot(pj.to_numpy(), imprint.loc[pj.index].to_numpy())
pw = f0.assign(wt=f0.n_test); res["H2_spec_curve"] = {"journal_mean_journal_cluster": dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(pj.to_numpy(), B, cfg["seed"]))),
    "paper_weighted_point": float((pw.cov80 * pw.wt).sum() / pw.wt.sum() - 0.8), "journal_mean_imprint_cluster": {k: res["F0_shortfall_journal_mean_imprint_cluster"][k] for k in ("est", "lo", "hi")}}
jg = f0.groupby("issn").apply(lambda g: pd.Series(dict(num=(g.cov80 * g.n_test).sum(), den=g.n_test.sum())), include_groups=False)
nu, de = jg.num.to_numpy(), jg.den.to_numpy(); vals = []
for _ in range(2000):
    k = rng.integers(0, len(jg), len(jg)); vals.append(nu[k].sum() / de[k].sum() - 0.8)
res["H2_spec_curve"]["paper_weighted_journal_cluster_ci"] = [float(np.quantile(vals, .025)), float(np.quantile(vals, .975))]
tab = pj.groupby(imprint.loc[pj.index]).agg(["mean", "size"]); tab.columns = ["shortfall", "n_journals"]; res["shortfall_by_imprint"] = tab.round(4).reset_index().to_dict("records")
res["imprint_counts_all_800"] = imprint.value_counts().to_dict()
e9 = pd.read_csv(f"{ROOT}/results/external/e9_metrics.csv"); res["E9_eligible_journals"] = int(e9.issn.nunique()); res["E9_journal_origins"] = int((e9.method == "F0").sum())
g9 = e9[e9.method == "F0"].groupby("issn").cov80.mean().sub(0.8); res["E9_F0_shortfall"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(g9.to_numpy(), B, cfg["seed"])))
fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); res["note_hindawi_journals_in_800"] = int((imprint == "other").sum())
json.dump(res, open(f"{OUT}/Y0_imprint_inference.json", "w"), indent=1, default=float)
for k in ["F4-F0", "F3-F0", "F1-F0", "F6-F0", "F0-F2", "F4-F6", "F4-F3"]: print(k, {x: (round(v, 5) if isinstance(v, float) else v) for x, v in res[k].items() if x != "imprint_means"})
print(json.dumps({k: res[k] for k in ["F0_shortfall_journal_mean_imprint_cluster", "H2_spec_curve", "shortfall_by_imprint", "imprint_counts_all_800", "E9_eligible_journals", "E9_journal_origins", "E9_F0_shortfall"]}, indent=1, default=float))
