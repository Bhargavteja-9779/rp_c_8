"""Sample submission->acceptance intervals from Crossref 'received'/'accepted' assertions (Springer Nature deposits these).
Observed turnaround of PUBLISHED articles only (survivorship bias: rejected papers are not observed)."""
import requests, time, json, sys, csv, statistics as st
from datetime import datetime
UA={"User-Agent":"research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"}
J={"Scientometrics":"0138-9130","Quantitative Science Studies":"2641-3337","JASIST":"2330-1635","Learned Publishing":"0953-1513","Research Evaluation":"0958-2029",
"Profesional de la Informacion":"1699-2407","Frontiers Res Metrics Analytics":"2504-0537","Journal of Documentation":"0022-0418","Journal of Informetrics":"1751-1577",
"Research Policy":"0048-7333","Online Information Review":"1468-4527","Info Processing & Management":"0306-4573","J Librarianship & Inf Sci":"0961-0006",
"Information Research":"1368-1613","Aslib J Inf Manag":"2050-3806","Library & Inf Sci Research":"0740-8188","Science and Public Policy":"0302-3427",
"Minerva":"0026-4695","Higher Education":"0018-1560","Research Integrity & Peer Review":"2058-8615","Journal of Data and Information Science":"2543-683X",
"Publications-ex":"2304-6775","Science and Engineering Ethics":"1353-3452","Accountability in Research":"0898-9621","BMC Med Res Methodol":"1471-2288"}
def get(params):
    for k in range(8):
        try:
            r=requests.get("https://api.crossref.org/works",params=params,timeout=90,headers=UA)
            if r.status_code==200 and r.text.startswith("{"): return r.json()
        except Exception: pass
        time.sleep(3*(k+1))
def pdate(s):
    for f in ("%d %B %Y","%d %b %Y","%Y-%m-%d"):
        try: return datetime.strptime(s.strip(),f)
        except Exception: pass
rows=[]
for name,issn in J.items():
    cursor="*"; got=0
    while got<200:
        r=get({"filter":f"issn:{issn},from-pub-date:2024-01-01,type:journal-article","rows":100,"cursor":cursor,"select":"DOI,title,assertion,published,type"})
        if not r: break
        items=r["message"]["items"]
        if not items: break
        for i in items:
            a={x["name"]:x["value"] for x in i.get("assertion",[]) if x["name"] in("received","accepted")}
            if len(a)==2:
                d1,d2=pdate(a["received"]),pdate(a["accepted"])
                if d1 and d2 and d2>=d1:
                    rows.append((name,issn,i["DOI"],d1.date().isoformat(),d2.date().isoformat(),(d2-d1).days)); got+=1
        cursor=r["message"].get("next-cursor")
        if not cursor: break
    print(name,got,flush=True)
with open("../turnaround_samples_infosci.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["journal","issn","doi","received","accepted","days"]); w.writerows(rows)
