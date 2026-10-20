"""Look up secondary-source (Peeref) journal metadata: JCR categories/quartiles as displayed by Peeref and the
publisher-reported 'Peer Review Turnaround Time' string (Elsevier Journal Insights definition). Binary search over alphabetical IDs."""
import requests, re, html, json, sys, time
S=requests.Session(); S.headers["User-Agent"]="Mozilla/5.0 Chrome/120"
cache={}
def page(i):
    if i in cache: return cache[i]
    for k in range(3):
        try:
            r=S.get(f"https://www.peeref.com/journals/{i}",timeout=30)
            if r.status_code==200: cache[i]=r.text; return r.text
            if r.status_code==404: cache[i]=None; return None
        except Exception: pass
        time.sleep(1)
def title(t):
    m=re.search(r"<title>(.*?)\s+—",t or "",re.S)
    return html.unescape(m.group(1)).strip().lower() if m else None
def norm(s): return re.sub(r"[^a-z0-9 ]","",s.lower().replace("&amp;","&").replace("&","and")).strip()
def find(name,lo=1,hi=9000):
    n=norm(name)
    while hi-lo>12:
        mid=(lo+hi)//2; j=mid
        t=None
        for d in range(0,10):
            t=title(page(mid+d))
            if t: j=mid+d; break
        if not t: hi=mid; continue
        if norm(t)<n: lo=j+1
        else: hi=j
    for i in range(max(1,lo-15),hi+16):
        t=title(page(i))
        if t and norm(t)==n: return i
def facts(i):
    t=page(i); s=re.sub(r'<(script|style)[^>]*>.*?</\1>','',t,flags=re.S); s=html.unescape(re.sub(r'<[^>]+>','\n',s)); s=re.sub(r'\n\s*\n+','\n',s)
    d={"id":i,"title":title(t)}
    m=re.search(r"Peer Review Turnaround Time\s*\n\s*(.*)",s); d["turnaround"]=m.group(1).strip() if m else None
    m=re.search(r"Category \(Journal Citation Reports (\d{4})\)\s*\nQuartile\s*\n(.*?)\n\s*Advertisement",s,re.S)
    d["jcr_year"]=m.group(1) if m else None
    d["jcr_cats"]=[x.strip() for x in m.group(2).split("\n") if x.strip()] if m else None
    m=re.search(r"Publisher\s*\n\s*(.*)",s); d["publisher"]=m.group(1).strip() if m else None
    m=re.search(r"ISSN\s*\n\s*(.*)",s); d["issn"]=m.group(1).strip() if m else None
    m=re.search(r"Publication Fee\s*\n\s*(.*)",s); d["fee"]=m.group(1).strip() if m else None
    return d
if __name__=="__main__":
    out=[]
    for name in sys.argv[1:]:
        i=find(name)
        out.append(facts(i) if i else {"query":name,"id":None})
        print(json.dumps(out[-1]),flush=True)
