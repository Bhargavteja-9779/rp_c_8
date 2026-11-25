"""Part D external-validity collection (specified in revised_experimental_protocol.md Part D before any data were fetched).
Journal list fixed here by title abbreviation, drawn from memory of high-volume non-MDPI, non-frame PubMed journals (Elsevier, Cell Press, OUP, PLOS, CUP, society journals), NOT by looking at turnaround times.
Journals without enough History-dated records are dropped by rule (>=600 dated records), never by outcome. Output: data/raw/pubmed_ext/<journal>.csv (same columns as data/raw/pubmed)."""
import requests, time, csv, os, sys, xml.etree.ElementTree as ET
from datetime import date
B = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"; OUT = "/home/user/rp_c_8/data/raw/pubmed_ext/"; os.makedirs(OUT, exist_ok=True)
J = ["Lancet Oncol", "Lancet Infect Dis", "J Hepatol", "Gastroenterology", "J Am Coll Cardiol", "Cell", "Cell Metab", "Neuron", "Immunity", "Mol Cell", "Cancer Cell", "Eur J Cancer", "Ann Oncol", "Radiother Oncol", "Clin Nutr",
 "Int J Cardiol", "Atherosclerosis", "Biomaterials", "Acta Biomater", "J Control Release", "Bioresour Technol", "Water Res", "Chemosphere", "Environ Pollut", "J Hazard Mater", "Food Chem", "Toxicol Appl Pharmacol", "Neuropharmacology",
 "Brain Res", "Neurosci Biobehav Rev", "Psychoneuroendocrinology", "J Affect Disord", "Schizophr Res", "Eur J Pharmacol", "Biochem Pharmacol", "Int J Biol Macromol", "Carbohydr Polym", "J Ethnopharmacol", "Phytomedicine", "Life Sci",
 "Biomed Pharmacother", "Gene", "Mol Immunol", "Cell Immunol", "Vaccine", "Antiviral Res", "J Infect", "Clin Microbiol Infect", "Int J Infect Dis", "Am J Surg", "Surgery", "J Surg Res", "Injury", "Burns", "Resuscitation", "Am J Emerg Med",
 "Int J Nurs Stud", "Midwifery", "Nurse Educ Today", "Soc Sci Med", "Health Place", "Prev Med", "Public Health", "Appetite", "Nutrition", "Sleep Med", "Pain", "Eur J Pain", "Eur Urol", "J Urol", "Urology", "Gynecol Oncol", "Fertil Steril",
 "Eur J Obstet Gynecol Reprod Biol", "J Pediatr", "Early Hum Dev", "Eur J Paediatr Neurol", "Clin Neurophysiol", "Epilepsy Res", "Seizure", "J Neurol Sci", "Parkinsonism Relat Disord", "Neurobiol Aging", "Neurobiol Dis", "Cortex",
 "Neuropsychologia", "Brain Stimul", "Dent Mater", "J Dent", "Ophthalmology", "Exp Eye Res", "Clin Biochem", "Clin Chim Acta", "Talanta", "Anal Chim Acta", "J Chromatogr A", "Forensic Sci Int",
 "Nucleic Acids Res", "Hum Mol Genet", "Brain", "Cereb Cortex", "Eur Heart J", "Clin Infect Dis", "J Infect Dis", "Am J Epidemiol", "Int J Epidemiol", "J Gerontol A Biol Sci Med Sci", "Mol Biol Evol",
 "Psychol Med", "Br J Psychiatry", "Epidemiol Infect", "Public Health Nutr", "PLoS Med", "PLoS Pathog", "PLoS Genet", "PLoS Negl Trop Dis", "PLoS Biol", "J Neurosci", "J Biol Chem", "Proc Natl Acad Sci U S A", "Cancer Res",
 "Clin Cancer Res", "Blood", "Circulation", "Hypertension", "Stroke", "J Clin Invest", "J Immunol", "Am J Physiol Endocrinol Metab", "Diabetes", "Diabetes Care", "Kidney Int", "Hepatology", "Gut", "Thorax", "Anesthesiology", "J Bone Miner Res"]
def req(path, params):
    for k in range(8):
        try:
            r = requests.get(B + path, params=params, timeout=120)
            if r.status_code == 200: return r
        except Exception: pass
        time.sleep(2 * (k + 1))
def fetch_journal(j, per_year=1500):
    fn = OUT + j.replace(" ", "_").replace("(", "").replace(")", "") + ".csv"
    if os.path.exists(fn): return
    ids = []
    for yr in range(2021, 2027):
        r = req("esearch.fcgi", {"db": "pubmed", "term": f'"{j}"[ta] AND ("{yr}/01/01"[dp]:"{yr}/12/31"[dp]) AND journal article[pt] NOT review[pt]', "retmax": per_year, "retmode": "json", "sort": "pub_date"})
        if r: ids += r.json()["esearchresult"]["idlist"]
        time.sleep(0.35)
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
            if "received" in h and "accepted" in h: rows.append([pm, doi, j, title, h["received"], h["accepted"], pub, na, nref])
        time.sleep(0.35)
    with open(fn + ".tmp", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["pmid", "doi", "journal", "title", "received", "accepted", "pubmed_date", "n_authors", "n_refs"]); w.writerows(rows)
    os.rename(fn + ".tmp", fn); print(j, len(ids), len(rows), flush=True)
if __name__ == "__main__":
    for j in J: fetch_journal(j)
