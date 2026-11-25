# Author guide: understand, verify and own this work before submitting

A journal rejected the earlier version partly for "substantial use of generative AI". Editors do not mind a tool that helps with code or wording if the authors understand, verify and are accountable for the work and disclose the tool. They do mind a paper that the authors cannot explain. This guide is written so that you can do that. Use it, reproduce the numbers, and then **write the manuscript text in your own words** (the draft is a scaffold, not the finished paper).

## 1. The study in five sentences
1. Publishers deposit, for each article, the date a manuscript was *received* and the date it was *accepted*. We have these for about 1.8 million articles in 800 Springer Nature, Wiley and Taylor & Francis journals.
2. Retraction Watch lists retracted articles and the reasons; we link the two by DOI. About 3,450 of the articles were retracted, about 2,640 for reasons connected with the editorial process (compromised peer review, rogue editor, paper mill, third-party involvement).
3. Within the same journal and the same year, we compare articles accepted unusually fast (fastest 5%) with the rest. Comparing inside a journal-year removes the fact that some journals are simply faster or retract more.
4. Result: the fastest 5% were about four times as likely (odds ratio ≈ 4.2) to be retracted for process-related reasons; the slowest 5% were much less likely (≈ 0.10); an irrelevant exposure (weekend receipt) showed nothing (≈ 0.88).
5. But: it varies a lot between journals and years (strong 2020–2022, nothing detectable for 2024 articles), most events come from a handful of journals, and as a screening tool it is weak (about 1 in 150 of the fastest 1% was retracted). So the honest message is: "a real but uneven association; useful at most to prioritise editorial-office review of groups of articles, never to judge a single paper."

## 2. Words you must be able to explain
* **Odds ratio (OR)**: how many times higher the odds of retraction are in the fast group than in the comparison group (1 = no difference).
* **Mantel–Haenszel (MH)**: an odds ratio computed inside each journal-year and then combined, so journals are never compared with each other.
* **Journal-cluster bootstrap CI**: repeatedly resample whole journals to get an honest interval, because articles of one journal are not independent.
* **Negative control**: an exposure that should have no effect (receipt on a weekend); finding none supports that the method is not producing associations from nothing.
* **Out-of-time score (PIT)**: for each article, how unusual its duration is compared with the same journal's earlier articles only; it avoids using the future.
* **AUC**: the chance that a randomly chosen retracted article scores as "faster" than a randomly chosen non-retracted one in the same stratum (0.5 = chance).
* **Positive predictive value / lift / number needed to screen**: of the articles flagged, what share was retracted; how many times that is the base rate; how many flagged articles you must examine to find one retraction.
* **Heterogeneity (I², prediction interval)**: the association differs between journals; the prediction interval says what a new journal might show (0.3 to 23, i.e. anything from slightly protective to strongly risky).
* **Circular ascertainment**: if a publisher used fast turnaround to decide which papers to investigate and retract, the link between speed and retraction is partly built in. We can only show that the estimate is similar when that label is absent (small numbers), not exclude it.

## 3. Reproduce the numbers yourself (about 15 minutes of work)
```
git clone https://github.com/Bhargavteja-9779/rp_c_8.git && cd rp_c_8 && git checkout claude/autonomous-research-institute-nz8co5
pip install -r code/requirements.txt statsmodels
python3 code/src/prepare_data.py                      # rebuilds data/processed (sha256 is checked against results/data_manifest.json)
python3 reinforced/code/src/e_build.py                # corrected cohort + exposures + outcomes
python3 reinforced/code/src/verify_headline_numbers.py  # short script; prints computed vs reported headline numbers (should all say OK)
```
Read `verify_headline_numbers.py` first (about 30 lines): it recomputes the central odds ratio from the processed data. Then read `reinforced/research_design/cycle4_protocol_partE.md` (what was decided in advance and what was added later) and `reinforced/review/` (the reviews and what they found, including the cohort error that was corrected).

## 4. Questions a reviewer will ask, and honest answers
* *Isn't this circular, since publishers retract what looks suspicious?* Partly possible. Say so; point to the analysis without the "investigation by journal/publisher" label (OR ≈ 4.0, but only 107 events) and to the limitation paragraph.
* *Why only three publishers, and why so few Taylor & Francis retractions?* Journals had to deposit received/accepted dates; the T&F set contains 24 retractions, so the results speak for Springer Nature and Wiley.
* *Why did the association shrink in recent years?* We do not know: less manipulation that shows up as speed, slower detection, or other reasons dominating. Do not claim more.
* *Why should editors care if the screen is weak?* Because relative speed is a cheap, available signal that can help rank journals or collections for review, and because the paper documents how large and how uneven the association is, and how easily such analyses go wrong (e.g. a cleaning rule removed 28% of retracted articles).
* *What did the AI do?* Wrote and ran the code, drafted text, searched literature, and ran review and audit passes. You must state this and show that you verified results (this guide and the verification script are meant for that).

## 5. What you must do yourself before submitting
1. Run the verification script and at least the main analysis; open the result files and look at the numbers.
2. Rewrite the manuscript in your own words; shorten where you can; make sure every sentence is something you can defend.
3. Check the references yourself (all DOIs were resolved through Crossref/DataCite by script, but you should open the ones you cite).
4. Deposit code and data with a DOI (e.g. Zenodo); complete funding, competing interests, authors' contributions, and the AI-use statement according to the target journal's policy.
5. Choose the journal after reading its AI policy and its scope; consider a scientometrics or meta-research venue if the target journal has just rejected the same project. Timelines and impact factors in earlier files are not verified.
6. Ask a colleague who works in research integrity or statistics to read it critically; no human outside this project has reviewed it so far.
