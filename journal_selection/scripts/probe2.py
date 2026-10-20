import requests, time
UA={"User-Agent":"research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"}
def get(p):
    for k in range(6):
        try:
            r=requests.get("https://api.crossref.org/works",params=p,timeout=90,headers=UA)
            if r.status_code==200 and r.text.startswith("{"): return r.json()
        except Exception: pass
        time.sleep(3*(k+1))
L={"ML:Sci&Tech":"2632-2153","Expert Systems":"0266-4720","Computational Intelligence":"0824-7935","IET Image Proc":"1751-9659","Int J Intell Syst":"0884-8173",
"PeerJ CS":"2376-5992","Front Big Data":"2624-909X","J Comput Des Eng":"2288-5048","Engineering with Computers":"0177-0667","Stat Anal Data Min":"1932-1864",
"IEEE Access":"2169-3536","Information Sciences":"0020-0255","Pattern Recognition":"0031-3203","Eng Sci Tech Int J":"2215-0986","Egypt Inform J":"1110-8665",
"Applied Sciences-ex":"2076-3417","Taylor&Francis: Int J Remote Sens":"0143-1161","J Appl Stat":"0266-4763","Quality Eng":"0898-2112","Phil Trans A":"1364-503X","Proc R Soc A":"1364-5021",
"JRSS-C":"0035-9254","Technometrics":"0040-1706","Comput Stat Data Anal":"0167-9473","Biomed Eng Online":"1475-925X","Frontiers Neurosci":"1662-453X","Environmental Modelling&Software":"1364-8152",
"Comput. Geosci":"0098-3004","Applied Energy":"0306-2619","Energy and AI":"2666-5468","Journal of Hydrology":"0022-1694","Water Research":"0043-1354","Hydrol Earth Syst Sci":"1027-5606","Geosci Model Dev":"1991-959X","J Chem Inf Model":"1549-9596","Machine Learning: Sci Tech":"2632-2153","npj Comput Mater":"2057-3960","Digital Discovery":"2635-098X","J Cheminform":"1758-2946"}
for n,i in L.items():
    r=get({"filter":f"issn:{i},from-pub-date:2025-07-01,type:journal-article","rows":30,"select":"DOI,assertion"})
    if not r: print(n,"fail"); continue
    it=r["message"]["items"]; c=sum(1 for x in it if {"received","accepted"}<= {a["name"] for a in x.get("assertion",[])})
    print(f"{n:35s}{i} n={len(it)} with_dates={c}",flush=True)
