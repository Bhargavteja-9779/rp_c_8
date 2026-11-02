"""Learns the shipped default cohort-shift variances (all quarterly origins 2022-01-01..2025-01-01, whose targets are complete by 2026-10-20) and computes the noise-floor of the per-journal-origin coverage error."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/reinforced/code/src")
from d_lib import *
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json"))
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)].copy()
df["D"] = df.D.clip(upper=CAP); df["y"] = np.log(df.D.astype(float)); origins = [o for o in pd.date_range("2022-01-01", "2025-01-01", freq="QS").strftime("%Y-%m-%d")]
store = build_store(df, member, origins, cfg); par = learn(store, origins, np.random.default_rng(5)); d = {k: v for k, v in par.items() if k != "G"}
json.dump(dict(tau2_global=par["tau2_g"], tau2_by_publisher=par["tau2_pub"], mean_shift_by_publisher=par["b_pub"], c_width_scale=par["c"], cap_days=CAP, n_origins=par["n_origins"], n_journal_origins=par["n_items"],
               note="learned from all earlier quarterly cohorts (91 days, received 2022-01-01..2025-01-01 starts) whose targets were complete by 2026-10-20; Crossref dates of Springer Nature, Wiley and Taylor & Francis journals"), open(f"{ROOT}/product/turnaround_forecast/defaults.json", "w"), indent=1)
R = pd.read_csv(f"{OUT}/D_panel_rows.csv"); f0 = R[R.method == "F0"]; fl = np.sqrt(2 / np.pi) * np.sqrt(.8 * .2 / f0.n_te)  # expected |binomial error| under perfect calibration (normal approx)
fl_j = fl.groupby(f0.issn).mean(); res = dict(noise_floor_abs_err=float(fl_j.mean()), tau2_global=par["tau2_g"], tau2_pub=par["tau2_pub"], b_pub=par["b_pub"], c=par["c"])
for m in ("F0", "CV0", "CVb", "V", "R"):
    a = R[R.method == m].assign(a=lambda x: (x.cov80 - .8).abs()).groupby("issn").a.mean(); res[f"excess_abs_err_{m}"] = float((a - fl_j.reindex(a.index)).mean())
json.dump(res, open(f"{OUT}/D_defaults_and_floor.json", "w"), indent=1, default=float); print(res)
