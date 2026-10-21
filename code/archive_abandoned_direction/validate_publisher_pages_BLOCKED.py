"""E8b: compare Crossref-deposited received/accepted with the dates printed on Springer article pages for a random sample of DOIs
from fast-looking and typical journals. Reads static HTML only."""
import re, sys, json, time, random, requests, pandas as pd
sys.path.insert(0, "/home/user/rp_c_8/code/src")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36"}
d = pd.read_csv("/home/user/rp_c_8/data/processed/articles_clean.csv.gz", usecols=["doi", "issn", "received", "accepted", "member"], parse_dates=["received", "accepted"])
rng = random.Random(20261020)
fast = ["1557-1963", "2522-011X", "1869-1870", "2199-4501", "1573-7373"]; typical = ["1588-2861", "2045-2322", "1471-2458", "1433-3015", "1573-482X", "1432-1084"]
rows = []
for grp, lst in (("fast", fast), ("typical", typical)):
    for issn in lst:
        sub = d[(d.issn == issn) & (d.received >= "2023-01-01")]
        for doi in rng.sample(list(sub.doi), min(6, len(sub))):
            r = None
            for k in range(3):
                try:
                    r = requests.get("https://link.springer.com/article/" + doi, headers=UA, timeout=40)
                    if r.status_code == 200: break
                except Exception: pass
                time.sleep(2)
            if r is None or r.status_code != 200: rows.append(dict(doi=doi, issn=issn, grp=grp, status=getattr(r, "status_code", None))); continue
            t = re.sub(r"<[^>]+>", " ", r.text)
            rc = re.search(r"Received\s*:?\s*(\d{1,2} \w+ \d{4})", t); ac = re.search(r"Accepted\s*:?\s*(\d{1,2} \w+ \d{4})", t)
            rv = re.search(r"Revised\s*:?\s*(\d{1,2} \w+ \d{4})", t)
            row = d[d.doi == doi].iloc[0]
            rows.append(dict(doi=doi, issn=issn, grp=grp, status=200, page_received=rc and rc.group(1), page_revised=rv and rv.group(1), page_accepted=ac and ac.group(1),
                             cr_received=str(row.received.date()), cr_accepted=str(row.accepted.date())))
            time.sleep(1)
o = pd.DataFrame(rows); o.to_csv("/home/user/rp_c_8/results/validation_publisher_pages.csv", index=False)
ok = o[o.status == 200].copy()
for c in ("page_received", "page_accepted"): ok[c + "_d"] = pd.to_datetime(ok[c], format="%d %B %Y", errors="coerce")
ok["match_r"] = ok.page_received_d == pd.to_datetime(ok.cr_received); ok["match_a"] = ok.page_accepted_d == pd.to_datetime(ok.cr_accepted)
print(len(o), "requested;", len(ok), "retrieved; received match", ok.match_r.mean(), "accepted match", ok.match_a.mean()); print(ok.groupby("grp")[["match_r", "match_a"]].mean())
print(ok[["issn", "page_received", "page_revised", "page_accepted", "cr_received", "cr_accepted"]].head(12).to_string())
