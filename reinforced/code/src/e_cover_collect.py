"""A20: number of Crossref retraction notices per frame journal (filter=issn,update-type:retraction, rows=0). Output: data/raw/coverage_notices.csv"""
import json, csv, time, concurrent.futures as cf
import requests
ROOT = "/home/user/rp_c_8"; fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json")); issns = [j["issn"] for j in fr]
def get(i):
    for k in range(6):
        try:
            r = requests.get("https://api.crossref.org/works", params={"filter": f"issn:{i},update-type:retraction", "rows": 0}, timeout=60, headers={"User-Agent": "turnaround-forecast-research/0.2"})
            if r.status_code == 200: return i, r.json()["message"]["total-results"]
        except Exception: pass
        time.sleep(2 * (k + 1))
    return i, None
with cf.ThreadPoolExecutor(6) as ex: res = list(ex.map(get, issns))
with open(f"{ROOT}/data/raw/coverage_notices.csv", "w", newline="") as f: w = csv.writer(f); w.writerow(["issn", "retraction_notices"]); w.writerows(res)
print("done", sum(1 for _, n in res if n is None), "failed")
