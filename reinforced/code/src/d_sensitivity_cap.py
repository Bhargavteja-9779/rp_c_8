"""EXPLORATORY (post hoc, not in the Part D protocol): sensitivity of the F0 80% coverage shortfall to the duration cap and the target-cohort length, at origins 2023-07-01..2024-07-01 where all targets are complete for every setting."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
import d_lib as L
from d_lib import *
sys.path.insert(0, "/home/user/rp_c_8/code/src")
from tdelay import stats as ST
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json"))
df0 = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df0 = df0[df0.issn.isin(member)].copy()
origins = ["2023-07-01", "2023-10-01", "2024-01-01", "2024-04-01", "2024-07-01"]; res = {}
for cap in (270, 365, 480, 1460):
    for H in (91, 182):
        L.H = H; df = df0.copy(); df["D"] = df.D.clip(upper=cap); df["y"] = np.log(df.D.astype(float)); st = L.build_store(df, member, origins, cfg, min_tr=100, min_te=30 if H == 91 else 50); vals = {}
        for o in origins:
            for it in st[o]:
                q = F.wquantile(it["ytr"], np.ones(len(it["ytr"])), [.1, .9]); vals.setdefault(it["issn"], []).append(np.mean((it["yte"] >= q[0]) & (it["yte"] <= q[1])) - .8)
        pj = np.array([np.mean(v) for v in vals.values()]); res[f"cap{cap}_H{H}"] = dict(zip(["est", "lo", "hi"], ST.cluster_bootstrap_mean(pj, 2000, 7))); res[f"cap{cap}_H{H}"]["n_journals"] = len(pj); print(cap, H, res[f"cap{cap}_H{H}"], flush=True)
json.dump(res, open(f"{OUT}/D_sensitivity_cap_EXPLORATORY.json", "w"), indent=1, default=float)
