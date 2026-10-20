"""Build the journal sampling frame (pre-registered, see research_design/protocol.md section 3).
Frame = for each of three Crossref members (Springer Nature 297, Wiley 311, Taylor & Francis 301) the 1000 ISSNs with the most
journal-article records published in calendar 2023 (facet=issn:1000), de-duplicated to journals (print/online ISSN pairs merged via /journals/{issn}).
Then: coverage screen (>=80% of 40 random 2023 records carry both `received` and `accepted` assertions), then volume screen (150..3000 dated articles in 2023)."""
import requests, json, time, random, sys
from concurrent.futures import ThreadPoolExecutor
UA={"User-Agent":"research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"}
OUT="/home/user/rp_c_8/data/raw/"
def g(url,params=None):
    for k in range(7):
        try:
            r=requests.get(url,params=params,headers=UA,timeout=120)
            if r.status_code==200: return r.json()
            if r.status_code==404: return None
        except Exception: pass
        time.sleep(2*(k+1))
members={297:"Springer Nature",311:"Wiley",301:"Taylor & Francis"}
cands={}
for mid,name in members.items():
    r=g(f"https://api.crossref.org/members/{mid}/works",{"filter":"type:journal-article,from-pub-date:2023-01-01,until-pub-date:2023-12-31","rows":0,"facet":"issn:1000"})
    for url,cnt in r["message"]["facets"]["issn"]["values"].items():
        cands[url.split("/")[-1]]=(mid,name,cnt)
    print(name,len(r["message"]["facets"]["issn"]["values"]),flush=True)
def meta(issn):
    r=g(f"https://api.crossref.org/journals/{issn}")
    if not r: return issn,None
    m=r["message"]; return issn,dict(title=m.get("title"),issns=m.get("ISSN",[]),subjects=[s.get("name") for s in m.get("subjects",[])],publisher=m.get("publisher"))
with ThreadPoolExecutor(6) as ex: metas=dict(ex.map(meta,list(cands)))
journals={}
for issn,(mid,name,cnt) in cands.items():
    m=metas.get(issn)
    if not m: continue
    key=tuple(sorted(m["issns"])) or (issn,)
    if key not in journals: journals[key]=dict(issn=issn,issns=list(key),member=name,mid=mid,title=m["title"],subjects=m["subjects"],n2023=0,publisher=m["publisher"])
    journals[key]["n2023"]=max(journals[key]["n2023"],cnt)
print("unique journals in raw frame:",len(journals),flush=True)
def screen(j):
    r=g("https://api.crossref.org/works",{"filter":f"issn:{j['issn']},type:journal-article,from-pub-date:2023-01-01,until-pub-date:2023-12-31","sample":40,"select":"DOI,assertion"})
    if not r: return j["issn"],None
    it=r["message"]["items"]
    ok=sum(1 for x in it if {"received","accepted"}<={a["name"] for a in x.get("assertion",[])})
    return j["issn"],(ok/len(it) if it else 0)
with ThreadPoolExecutor(6) as ex: cov=dict(ex.map(screen,[j for j in journals.values()]))
rows=[]
for j in journals.values():
    j["coverage"]=cov.get(j["issn"]); j["dated_2023_est"]=round(j["n2023"]*(j["coverage"] or 0))
    rows.append(j)
json.dump(rows,open(OUT+"frame_raw.json","w"),indent=1)
import pandas as pd
d=pd.DataFrame(rows); print(d.groupby("member").agg(n=("issn","size"),cov80=("coverage",lambda x:(x>=.8).sum()),med_vol=("n2023","median")))
