"""Verify candidate references against Crossref (by DOI) and arXiv (by id). Writes verified metadata to ../verified_references.json"""
import requests, json, time, re, xml.etree.ElementTree as ET
UA={"User-Agent":"research-office/1.0 (mailto:bhargavteja5098171@gmail.com)"}
DOIS={
"kapoor2023":"10.1016/j.patter.2023.100804","kaufman2012":"10.1145/2382577.2382579","vanschoren2014":"10.1145/2641190.2641198",
"lee2022":"10.18653/v1/2022.acl-long.577","elangovan2021":"10.18653/v1/2021.eacl-main.113","lewis2021":"10.18653/v1/2021.eacl-main.86",
"feldman2020":"10.1145/3357713.3384290","belkin2019":"10.1073/pnas.1903070116","bates2024":"10.1080/01621459.2023.2197686",
"nadeau2003":"10.1023/A:1024068626366","varoquaux2018":"10.1016/j.neuroimage.2017.06.061","roberts2017":"10.1111/ecog.02881",
"saeb2017":"10.1093/gigascience/gix019","breiman2001":"10.1023/A:1010933404324","geurts2006":"10.1007/s10994-006-6226-1",
"cover1967":"10.1109/TIT.1967.1053964","friedman2001":"10.1214/aos/1013203451","tavallaee2009":"10.1109/CISDA.2009.5356528",
"engelen2021":"10.1109/EuroSPW54576.2021.00008","kendall1938":"10.1093/biomet/30.1-2.81","good1953":"10.1093/biomet/40.3-4.237",
"barz2020":"10.3390/jimaging6060041","bouckaert2003":None,"dietterich1998":"10.1162/089976698300017197","wilcoxon1945":"10.2307/3001968",
"holm1979":None,"efron1979":"10.1214/aos/1176344552","benjamini1995":"10.1111/j.2517-6161.1995.tb02031.x","cliff1993":"10.1037/0033-2909.114.3.494",
"zhang2021":"10.1145/3446776","broder1997":"10.1109/SEQUEN.1997.666900","littlemann2017":"10.1109/TBME.2008.2005954","lones2024":"10.1016/j.patter.2024.100933",
"shwartz2022":"10.1016/j.inffus.2021.11.011","kuhn":None,
}
out={}
for k,d in DOIS.items():
    if not d: continue
    for a in range(4):
        try:
            r=requests.get(f"https://api.crossref.org/works/{d}",headers=UA,timeout=40)
            if r.status_code==200:
                m=r.json()["message"]; au=[(x.get("family","")+", "+x.get("given","")[:1]) for x in m.get("author",[])][:4]
                out[k]=dict(doi=d,title=(m.get("title") or ["?"])[0],year=(m.get("issued",{}).get("date-parts") or [[None]])[0][0],venue=(m.get("container-title") or [""])[0],authors=au,volume=m.get("volume"),page=m.get("page") or m.get("article-number"))
                break
            if r.status_code==404: out[k]=dict(doi=d,error="404 not found"); break
        except Exception as e: pass
        time.sleep(2)
    print(k, json.dumps(out.get(k,{"error":"fail"}))[:260],flush=True)
json.dump(out,open("../verified_references_crossref.json","w"),indent=1)
