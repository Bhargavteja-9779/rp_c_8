"""Sample submission->acceptance intervals from PubMed History dates (PubStatus received/accepted) for PubMed-indexed journals.
Observed turnaround of PUBLISHED research articles only."""
import requests, time, csv, xml.etree.ElementTree as ET
from datetime import date
B="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
J=["Comput Biol Med","Comput Methods Programs Biomed","Artif Intell Med","J Biomed Inform","Brief Bioinform","Bioinformatics",
"J Am Med Inform Assoc","JAMIA Open","BMC Bioinformatics","BMC Med Res Methodol","Med Image Anal","Neural Netw","IEEE J Biomed Health Inform",
"IEEE Trans Med Imaging","Patterns (N Y)","NPJ Digit Med","J Med Internet Res","JMIR Med Inform","JMIR AI","PLoS Comput Biol","PLoS One","Sci Rep",
"Stat Med","Biometrics","Front Artif Intell","Front Neuroinform","Neuroimage","Comput Med Imaging Graph","Int J Med Inform","Eur J Med Res","Sci Data",
"Gigascience","Bioinform Adv","Nat Commun","Digit Health","J Imaging Inform Med","Neural Comput","Phys Med Biol","Med Phys","Neurocomputing"]
def req(path,params):
    for k in range(6):
        try:
            r=requests.get(B+path,params=params,timeout=120)
            if r.status_code==200: return r
        except Exception: pass
        time.sleep(2*(k+1))
rows=[]
for j in J:
    q=f'"{j}"[ta] AND ("2025/07/01"[dp]:"2026/09/30"[dp]) AND journal article[pt] NOT review[pt]'
    r=req("esearch.fcgi",{"db":"pubmed","term":q,"retmax":400,"retmode":"json","sort":"pub_date"})
    if not r: print(j,"search fail"); continue
    ids=r.json()["esearchresult"]["idlist"]; got=0
    for k in range(0,len(ids),100):
        x=req("efetch.fcgi",{"db":"pubmed","id":",".join(ids[k:k+100]),"retmode":"xml"})
        if not x: continue
        root=ET.fromstring(x.content)
        for art in root.findall(".//PubmedArticle"):
            h={}
            for d in art.findall(".//PubmedData/History/PubMedPubDate"):
                try: h[d.get("PubStatus")]=date(int(d.findtext("Year")),int(d.findtext("Month")),int(d.findtext("Day")))
                except Exception: pass
            if "received" in h and "accepted" in h and h["accepted"]>=h["received"]:
                pmid=art.findtext(".//MedlineCitation/PMID"); 
                rows.append((j,pmid,h["received"].isoformat(),h["accepted"].isoformat(),(h["accepted"]-h["received"]).days)); got+=1
        time.sleep(0.4)
    print(j,len(ids),got,flush=True)
with open("../turnaround_samples_pubmed.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["journal","pmid","received","accepted","days"]); w.writerows(rows)
