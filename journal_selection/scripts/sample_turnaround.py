"""Sample submission->acceptance intervals from Crossref 'received'/'accepted' assertions (Springer Nature deposits these).
Observed turnaround of PUBLISHED articles only (survivorship bias: rejected papers are not observed)."""
import requests, time, json, sys, csv, statistics as st
from datetime import datetime
UA={"User-Agent":"research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"}
J={"Complex & Intelligent Systems":"2199-4536","Journal of Big Data":"2196-1115","J King Saud Univ CIS":"1319-1578",
"Neural Computing and Applications":"0941-0643","Applied Intelligence":"0924-669X","Int J Mach Learn Cybern":"1868-8071",
"Machine Learning":"1573-0565","Scientific Reports":"2045-2322","Artificial Intelligence Review":"0269-2821",
"Knowledge and Information Systems":"0219-1377","Journal of Cloud Computing":"2192-113X","Soft Computing":"1432-7643",
"Journal of Intelligent Manufacturing":"0956-5515","Cluster Computing":"1386-7857","Data Min Knowl Discov":"1384-5810",
"Journal of Supercomputing":"0920-8542","Evolving Systems":"1868-6478","Health Information Science and Systems":"2047-2501",
"BMC Medical Informatics":"1472-6947","Journal of Ambient Intelligence & Humanized Computing":"1868-5137"}
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
    while got<300:
        r=get({"filter":f"issn:{issn},from-pub-date:2025-07-01,type:journal-article","rows":100,"cursor":cursor,"select":"DOI,title,assertion,published,type"})
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
with open("../turnaround_samples.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["journal","issn","doi","received","accepted","days"]); w.writerows(rows)
