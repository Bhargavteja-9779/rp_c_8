"""Multi-source literature search helper (Crossref + arXiv + Europe PMC). Prints title/year/venue/DOI for manual screening and appends to a search log."""
import requests, sys, time, json, re, html, datetime
import xml.etree.ElementTree as ET
UA={"User-Agent":"research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"}
LOG="/home/user/rp_c_8/literature_review/search_log.jsonl"
def crossref(q,n=8,since=None):
    p={"query.bibliographic":q,"rows":n,"select":"DOI,title,issued,container-title,author,type,is-referenced-by-count"}
    if since: p["filter"]=f"from-pub-date:{since}"
    for k in range(5):
        try:
            r=requests.get("https://api.crossref.org/works",params=p,headers=UA,timeout=60)
            if r.status_code==200: break
        except Exception: pass
        time.sleep(2*(k+1))
    else: return []
    out=[]
    for i in r.json()["message"]["items"]:
        a=i.get("author",[{}]); au=(a[0].get("family","?") + (" et al." if len(a)>1 else "")) if a else "?"
        out.append(("CR",(i.get("title") or ["?"])[0][:140],i.get("issued",{}).get("date-parts",[[None]])[0][0],(i.get("container-title") or [""])[0][:45],au,i["DOI"],i.get("is-referenced-by-count")))
    return out
def arxiv(q,n=8):
    for k in range(4):
        try:
            r=requests.get("https://export.arxiv.org/api/query",params={"search_query":f"all:{q}","max_results":n,"sortBy":"relevance"},timeout=60)
            if r.status_code==200: break
        except Exception: pass
        time.sleep(3*(k+1))
    else: return []
    ns={"a":"http://www.w3.org/2005/Atom"}; root=ET.fromstring(r.content); out=[]
    for e in root.findall("a:entry",ns):
        t=re.sub(r"\s+"," ",e.findtext("a:title",namespaces=ns)); au=e.find("a:author/a:name",ns)
        out.append(("arXiv",t[:140],e.findtext("a:published",namespaces=ns)[:4],"preprint",(au.text.split()[-1] if au is not None else "?"),e.findtext("a:id",namespaces=ns).split("abs/")[-1],None))
    return out
def epmc(q,n=8):
    try:
        r=requests.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search",params={"query":q,"format":"json","pageSize":n,"sort":"RELEVANCE"},timeout=60).json()
    except Exception: return []
    return [("EPMC",x.get("title","?")[:140],x.get("pubYear"),x.get("journalTitle","")[:45],(x.get("authorString","?").split(",")[0]),x.get("doi") or x.get("id"),x.get("citedByCount")) for x in r.get("resultList",{}).get("result",[])]
if __name__=="__main__":
    for q in sys.argv[1:]:
        print(f"\n### {q}")
        res=crossref(q)+arxiv(q.replace('"',''))+epmc(q)
        for r in res: print(" | ".join(str(x) for x in r))
        with open(LOG,"a") as f: f.write(json.dumps({"date":datetime.date.today().isoformat(),"query":q,"n":len(res),"results":res})+"\n")
