"""Validity probe for the Crossref `received` date (cycle 2, experiment X1).
For frame journals, take published articles that Crossref links to a preprint (relation has-preprint) and compare `received` with the preprint's posting date.
Research Square 'In Review' preprints (DOI prefix 10.21203) are posted when the manuscript enters the journal's peer review, so received-minus-posted should be near 0 if `received` is the original submission date."""
import requests, json, time, csv, os, re, threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
ROOT = "/home/user/rp_c_8"; OUT = f"{ROOT}/reinforced/results/preprint_probe.csv"; UA = {"User-Agent": "research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"}
fr = json.load(open(f"{ROOT}/data/raw/frame_eligible.json"))
def get(url, params=None):
    for k in range(6):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=90)
            if r.status_code == 200: return r.json()["message"]
            if r.status_code == 404: return None
        except Exception: pass
        time.sleep(2 * (k + 1))
def pdate(s):
    for f in ("%d %B %Y", "%Y-%m-%d"):
        try: return datetime.strptime(s.strip(), f)
        except Exception: pass
def journal(j):
    m = get("https://api.crossref.org/works", {"filter": f"issn:{j['issn']},relation.type:has-preprint,from-pub-date:2022-01-01,type:journal-article", "rows": 60, "sample": 60, "select": "DOI,relation,assertion"})
    out = []
    if not m: return out
    for it in m["items"]:
        a = {x["name"]: x["value"] for x in it.get("assertion", []) if x["name"] in ("received", "accepted")}
        pp = [r["id"] for r in it.get("relation", {}).get("has-preprint", []) if r.get("id-type") == "doi"]
        if len(a) == 2 and pp:
            p = get(f"https://api.crossref.org/works/{pp[0]}")
            if not p: continue
            d = (p.get("posted") or p.get("issued") or {}).get("date-parts", [[None]])[0]
            if d and d[0] and len(d) >= 3:
                out.append([j["issn"], j["member"], it["DOI"], pp[0], a["received"], a["accepted"], f"{d[0]}-{d[1]:02d}-{d[2]:02d}", p.get("publisher", "")])
    return out
rows = []
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(journal, fr): rows += r
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["issn", "member", "doi", "preprint_doi", "received", "accepted", "preprint_posted", "preprint_publisher"]); w.writerows(rows)
print(len(rows), "records")
