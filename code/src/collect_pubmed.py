"""PubMed History-date collection for E8 (cross-source) and E9 (external validation). Pre-registered journal list: non-frame publishers plus
frame journals that are also PubMed-indexed (for E8 matching by DOI). Window: articles with publication date 2021-01-01..2026-10-20."""
import requests, time, csv, os, sys, xml.etree.ElementTree as ET
from datetime import date
B = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"; OUT = "/home/user/rp_c_8/data/raw/pubmed/"; os.makedirs(OUT, exist_ok=True)
# E9: non-frame publishers (Elsevier, OUP, Frontiers, Cell, JMIR, PLOS, IOP/AIP-type, etc.)
E9 = ["Comput Biol Med", "Comput Methods Programs Biomed", "J Biomed Inform", "Brief Bioinform", "Bioinformatics", "J Am Med Inform Assoc", "Med Image Anal", "Neural Netw",
      "Neuroimage", "J Med Internet Res", "Front Artif Intell", "Int J Med Inform", "PLoS One", "PLoS Comput Biol", "Eur J Med Res", "Phys Med Biol", "Med Phys",
      "Nat Commun", "NPJ Digit Med", "Sci Data", "Digit Health", "Gigascience", "Bioinform Adv", "J Imaging Inform Med", "Artif Intell Med", "Cell Rep", "Front Neurosci", "Front Immunol",
      "Front Psychol", "Front Oncol", "Heliyon", "Environ Int", "Sci Total Environ", "Lancet Digit Health", "BMJ Open", "J Clin Epidemiol", "Stat Med", "Biometrics"]
E8 = ["Sci Rep", "BMC Bioinformatics", "BMC Med Res Methodol", "BMC Public Health", "BMC Health Serv Res", "BMC Infect Dis", "BMC Geriatr", "J Med Case Rep", "Clin Epigenetics", "Harm Reduct J"]
def req(path, params):
    for k in range(8):
        try:
            r = requests.get(B + path, params=params, timeout=120)
            if r.status_code == 200: return r
        except Exception: pass
        time.sleep(2 * (k + 1))
def fetch_journal(j, cap=12000):
    fn = OUT + j.replace(" ", "_").replace("(", "").replace(")", "") + ".csv"
    if os.path.exists(fn): return
    ids = []
    for yr in range(2021, 2027):
        r = req("esearch.fcgi", {"db": "pubmed", "term": f'"{j}"[ta] AND ("{yr}/01/01"[dp]:"{yr}/12/31"[dp]) AND journal article[pt] NOT review[pt]', "retmax": cap // 6, "retmode": "json", "sort": "pub_date"})
        if r: ids += r.json()["esearchresult"]["idlist"]
    rows = []
    for k in range(0, len(ids), 200):
        x = req("efetch.fcgi", {"db": "pubmed", "id": ",".join(ids[k:k + 200]), "retmode": "xml"})
        if not x: continue
        for art in ET.fromstring(x.content).findall(".//PubmedArticle"):
            h = {}
            for d in art.findall(".//PubmedData/History/PubMedPubDate"):
                try: h[d.get("PubStatus")] = date(int(d.findtext("Year")), int(d.findtext("Month")), int(d.findtext("Day")))
                except Exception: pass
            doi = next((a.text for a in art.findall(".//PubmedData/ArticleIdList/ArticleId") if a.get("IdType") == "doi"), "")
            pm = art.findtext(".//MedlineCitation/PMID"); title = "".join(art.find(".//ArticleTitle").itertext())[:90] if art.find(".//ArticleTitle") is not None else ""
            na = len(art.findall(".//AuthorList/Author")); nref = len(art.findall(".//ReferenceList/Reference"))
            pub = h.get("pubmed") or h.get("entrez")
            if "received" in h and "accepted" in h:
                rows.append([pm, doi, j, title, h["received"], h["accepted"], pub, na, nref])
        time.sleep(0.35)
    with open(fn + ".tmp", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["pmid", "doi", "journal", "title", "received", "accepted", "pubmed_date", "n_authors", "n_refs"]); w.writerows(rows)
    os.rename(fn + ".tmp", fn); print(j, len(ids), len(rows), flush=True)
if __name__ == "__main__":
    for j in E9 + E8: fetch_journal(j)
