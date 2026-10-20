"""Sample submission->acceptance intervals from Crossref 'received'/'accepted' assertions (Springer Nature deposits these).
Observed turnaround of PUBLISHED articles only (survivorship bias: rejected papers are not observed)."""
import requests, time, json, sys, csv, statistics as st
from datetime import datetime
UA={"User-Agent":"research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"}
J={"Expert Systems":"0266-4720","Computational Intelligence":"0824-7935","IET Image Processing":"1751-9659","Int J Intell Syst":"0884-8173",
"Engineering with Computers":"0177-0667","Stat Anal Data Min":"1932-1864","Int J Remote Sens":"0143-1161","J Appl Stat":"0266-4763","Technometrics":"0040-1706",
"Biomed Eng Online":"1475-925X","npj Comput Mater":"2057-3960","J Cheminform":"1758-2946","Phil Trans R Soc A":"1364-503X","Proc R Soc A":"1364-5021",
"Applied Artificial Intelligence":"0883-9514","Comput-Aided Civil Infrastruct Eng":"1093-9687","Struct Control Health Monit":"1545-2255","Int J Prod Res":"0020-7543",
"Int J Numer Methods Eng":"0029-5981","Quality & Reliability Eng Int":"0748-8017","J Comput Graph Stat":"1061-8600","J Stat Comput Simul":"0094-9655",
"Software Pract Exper":"0038-0644","Concurr Comput":"1532-0626","Eng Optim":"0305-215X","Int J Climatol":"0899-8418","Earth Sci Inform":"1865-0473",
"Hydrological Sciences J":"0262-6667","Transactions in GIS":"1361-1682","Int J Digital Earth":"1753-8947","GIScience & Remote Sensing":"1548-1603",
"Int J Geog Info Sci":"1365-8816","Remote Sens Lett":"2150-704X","Neural Process Lett":"1370-4621","Pattern Anal Appl":"1433-7541","Mach Vis Appl":"0932-8092",
"Mathematics-of-Comp-ex":"0025-5718","J Sci Comput":"0885-7474","Stat Comput":"0960-3174","Adv Data Anal Classif":"1862-5347","Comput Stat":"0943-4062",
"Environ Sci Pollut Res":"0944-1344","Env Monit Assess":"0167-6369","Stoch Environ Res Risk Assess":"1436-3240","Nat Hazards":"0921-030X","Landslides":"1612-510X",
"Acta Geotechnica":"1861-1125","Bull Eng Geol Environ":"1435-9529","Arab J Geosci":"1866-7511","Appl Water Sci":"2190-5487","Environ Earth Sci":"1866-6280"}
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
with open("../turnaround_samples_crossref2.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["journal","issn","doi","received","accepted","days"]); w.writerows(rows)
