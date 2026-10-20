import requests, time
def get(params):
    for k in range(6):
        r=requests.get("https://api.crossref.org/works",params=params,timeout=90,headers={"User-Agent":"research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"})
        if r.status_code==200 and r.text.startswith("{"): return r.json()
        time.sleep(3*(k+1))
    return None
for issn in ["1319-1578","0941-0643","0924-669X","1868-8071","1110-0168","2590-1230","0010-4825","1746-8094","2169-3536","0957-4174","0950-7051","1568-4946","0952-1976","1573-0565","2215-0986"]:
    r=get({"filter":f"issn:{issn},from-pub-date:2025-01-01,type:journal-article","rows":20,"select":"DOI,assertion,container-title,published"})
    if not r: print(issn,"fail"); continue
    items=r["message"]["items"]
    n=sum(1 for i in items if any(a["name"]=="accepted" for a in i.get("assertion",[])))
    names=set(a["name"] for i in items for a in i.get("assertion",[]))
    print(issn, items[0]["container-title"][0] if items else None, len(items),"with accepted:",n, sorted(names)[:10],flush=True)
