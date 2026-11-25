"""Y4 strictly out-of-time article-level model; Y5 predictability of the per-journal coverage shortfall."""
import json, sys
sys.path.insert(0, "/home/user/rp_c_8/code/src")
import numpy as np, pandas as pd, lightgbm as lgb
from tdelay import experiments as E, forecasters as F, scoring as S, stats as ST
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results"; cfg = json.load(open(f"{ROOT}/code/configs/config.json")); seed = cfg["seed"]
df = pd.read_csv(f"{ROOT}/data/processed/articles_clean.csv.gz", parse_dates=["received", "accepted", "V"]); fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); member = {j["issn"]: j["member"] for j in fr}; df = df[df.issn.isin(member)].copy()
imprint = pd.read_csv(f"{OUT}/journal_imprint_map.csv", index_col=0).iloc[:, 0]; taus5 = [.1, .25, .5, .75, .9]
def article_table(t0):
    per, _, _ = E._prep_origin(df, member, t0, cfg); T0 = pd.Timestamp(t0); rows = []
    for i, (tr12, tr24, te) in per.items():
        if len(tr12) < 100 or len(te) < 50: continue
        q = F.wquantile(tr12.y.to_numpy(), np.ones(len(tr12)), taus5); a_mean = tr12.n_authors.mean(); r_mean = np.log1p(tr12.n_refs).mean()
        t = te.copy()
        for k, tau in enumerate(taus5): t[f"q{tau}"] = q[k]
        t["issn"] = i; t["auth_dm"] = t.n_authors - a_mean; t["lref_dm"] = np.log1p(t.n_refs.fillna(tr12.n_refs.median())) - r_mean; t["rec_month"] = t.received.dt.month; t["rec_wd"] = t.received.dt.weekday; t["n_authors"] = t.n_authors.fillna(tr12.n_authors.median()); rows.append(t)
    return pd.concat(rows, ignore_index=True)
tr, te = article_table("2022-01-01"), article_table("2024-01-01"); res = {}
def fit_eval(cols_extra, name):
    losses = {"base": [], "ctrl": [], name: []}; pj = {}
    for tau in taus5:
        for key, cols in (("ctrl", [f"q{tau}"]), (name, [f"q{tau}"] + cols_extra)):
            m = lgb.LGBMRegressor(objective="quantile", alpha=tau, n_estimators=200, max_depth=3, learning_rate=0.05, min_child_samples=200, verbose=-1, random_state=seed, n_jobs=3).fit(tr[cols], tr.y); p = m.predict(te[cols])
            d = te.y - p; te[f"loss_{key}_{tau}"] = np.maximum(tau * d, (tau - 1) * d)
        d = te.y - te[f"q{tau}"]; te[f"loss_base_{tau}"] = np.maximum(tau * d, (tau - 1) * d)
    g = te.groupby("issn")[[f"loss_{k}_{t}" for k in ("base", "ctrl", name) for t in taus5]].mean(); L = {k: g[[f"loss_{k}_{t}" for t in taus5]].mean(axis=1) for k in ("base", "ctrl", name)}
    arr = np.array([[L["base"].loc[i], L["ctrl"].loc[i], L[name].loc[i]] for i in g.index]); rng = np.random.default_rng(seed); reps = []
    for _ in range(3000):
        k = rng.integers(0, len(arr), len(arr)); a = arr[k].mean(axis=0); reps.append((1 - a[2] / a[1], 1 - a[2] / a[0]))
    reps = np.array(reps); a = arr.mean(axis=0)
    res[name] = dict(rel_gain_vs_control=float(1 - a[2] / a[1]), ci_vs_control=[float(np.quantile(reps[:, 0], .025)), float(np.quantile(reps[:, 0], .975))], rel_gain_vs_base=float(1 - a[2] / a[0]), ci_vs_base=[float(np.quantile(reps[:, 1], .025)), float(np.quantile(reps[:, 1], .975))], control_vs_base=float(1 - a[1] / a[0]), n_papers=int(len(te)), n_journals=int(len(arr)), by_tau_gain_vs_control={str(t): float(1 - te[f"loss_{name}_{t}"].mean() / te[f"loss_ctrl_{t}"].mean()) for t in taus5})
fit_eval(["n_authors", "rec_month", "rec_wd"], "presubmission_raw"); fit_eval(["auth_dm", "rec_month", "rec_wd"], "presubmission_journal_demeaned"); fit_eval(["n_authors", "rec_month", "rec_wd", "lref_dm"], "with_reference_count_demeaned")
# Y5 predictability of shortfall: fit on 2023 journal-origins, predict 2024
met = pd.read_csv(f"{ROOT}/results/metrics_journal_origin.csv"); f0 = met[met.method == "F0"].copy(); f0["shortfall"] = f0.cov80 - 0.8; f0["imprint"] = f0.issn.map(imprint).astype("category")
per_feat = {}
for t0 in ["2023-01-01", "2024-01-01"]:
    T0 = pd.Timestamp(t0)
    for i, d in df.groupby("issn"):
        v = d[(d.V < T0) & (d.accepted < T0) & (d.V >= T0 - pd.Timedelta(days=365))]; p = d[(d.V < T0 - pd.Timedelta(days=365)) & (d.V >= T0 - pd.Timedelta(days=730))]
        per_feat[(i, t0)] = dict(logvol=np.log(max(len(v), 1) / max(len(p), 1)), fastshare=(v.D <= 14).mean() if len(v) else np.nan, instab=abs(v.y.median() - p.y.median()) if len(v) > 20 and len(p) > 20 else np.nan, sd=v.y.std() if len(v) > 5 else np.nan)
X = f0.apply(lambda r: pd.Series(per_feat.get((r.issn, r.origin), {})), axis=1); f0 = pd.concat([f0.reset_index(drop=True), X.reset_index(drop=True)], axis=1); f0["logvol2"] = f0.logvol ** 2; f0["imp_code"] = f0.imprint.cat.codes
cols = ["logvol", "logvol2", "fastshare", "instab", "sd", "n_train", "imp_code"]; a = f0[f0.origin == "2023-01-01"].dropna(subset=cols); b = f0[f0.origin == "2024-01-01"].dropna(subset=cols)
m = lgb.LGBMRegressor(n_estimators=150, max_depth=3, learning_rate=0.05, min_child_samples=30, verbose=-1, random_state=seed).fit(a[cols], a.shortfall); pred = m.predict(b[cols]); const = a.shortfall.mean()
res["Y5"] = dict(oos_R2_vs_constant=float(1 - ((b.shortfall - pred) ** 2).sum() / ((b.shortfall - const) ** 2).sum()), n_train=int(len(a)), n_test=int(len(b)), corr_pred_actual=float(np.corrcoef(pred, b.shortfall)[0, 1]), sd_shortfall_2024=float(b.shortfall.std()), binomial_sd_expected=float(np.sqrt(0.16 / b.n_test).mean()))
json.dump(res, open(f"{OUT}/Y4_Y5_summary.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float))
