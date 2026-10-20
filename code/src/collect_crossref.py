"""Bulk collection of article-level submission/acceptance dates for the pre-registered journal frame (Crossref).
Resumable: one gzip CSV per journal in data/raw/crossref/. Records without BOTH received and accepted assertions are counted but not stored."""
import requests, json, time, gzip, csv, os, sys, threading
from concurrent.futures import ThreadPoolExecutor
UA={"User-Agent":"research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"}
RAW="/home/user/rp_c_8/data/raw/"; OUT=RAW+"crossref/"; os.makedirs(OUT,exist_ok=True)
SEL="DOI,assertion,issued,references-count,is-referenced-by-count,author,funder,license,page,title,type"
FROM,UNTIL="2021-01-01","2026-10-20"
lock=threading.Lock(); log=open(RAW+"collect_crossref.log","a")
def say(*a):
    with lock: print(*a,file=log,flush=True)
def fetch(params):
    for k in range(8):
        try:
            r=requests.get("https://api.crossref.org/works",params=params,headers=UA,timeout=180)
            if r.status_code==200: return r.json()["message"]
            if r.status_code in (400,404): return None
        except Exception: pass
        time.sleep(3*(k+1))
def do(j):
    issn=j["issn"]; fn=OUT+issn+".csv.gz"
    if os.path.exists(fn): return
    cursor="*"; total=0; rows=[]
    while True:
        m=fetch({"filter":f"issn:{issn},type:journal-article,from-pub-date:{FROM},until-pub-date:{UNTIL}","rows":1000,"cursor":cursor,"select":SEL})
        if not m or not m["items"]: break
        for it in m["items"]:
            total+=1
            a={x["name"]:x["value"] for x in it.get("assertion",[]) if x["name"] in("received","accepted","first_online")}
            if "received" in a and "accepted" in a:
                dp=(it.get("issued",{}).get("date-parts") or [[None]])[0]
                rows.append([it["DOI"],issn,(it.get("title") or [""])[0][:90].replace("\n"," "),a["received"],a["accepted"],a.get("first_online",""),"-".join(str(x) for x in dp if x),
                    len(it.get("author",[])),it.get("references-count"),it.get("is-referenced-by-count"),int(bool(it.get("funder"))),len(it.get("license",[])),it.get("page","")])
        cursor=m.get("next-cursor")
        if not cursor: break
    tmp=fn+".tmp"
    with gzip.open(tmp,"wt",newline="") as f:
        w=csv.writer(f); w.writerow(["doi","issn","title","received","accepted","first_online","issued","n_authors","n_refs","cited_by","has_funder","n_license","page"]); w.writerows(rows)
    os.rename(tmp,fn)
    with lock: open(RAW+"collect_crossref_summary.tsv","a").write(f"{issn}\t{j['member']}\t{total}\t{len(rows)}\n")
    say("done",issn,j["title"],total,len(rows))
if __name__=="__main__":
    fr=json.load(open(RAW+"frame_raw.json"))
    elig=[j for j in fr if (j["coverage"] or 0)>=0.8 and 150<=j["dated_2023_est"]<=3000]
    json.dump(elig,open(RAW+"frame_eligible.json","w"),indent=1)
    say("eligible journals",len(elig))
    with ThreadPoolExecutor(4) as ex: list(ex.map(do,elig))
    say("ALL DONE")
