# Journal strategy, title and desk-rejection assessment

Prepared 2026-11-25. **Nothing here guarantees acceptance or protects against desk rejection.** Journal metrics below are OpenAlex "2-year mean citedness" (a free proxy computed from citations, retrieved 2026-11-25); they are **not** the Clarivate Impact Factor. Look up the real JCR value yourselves. I could not open any publisher's author-guidelines page from this environment (HTTP 403 / login redirect), so **article types, word limits, reference style and each journal's AI policy are unverified: read them before submitting.**

## 1. Recommended journal (and why)

**First choice: Scientometrics** (Springer Nature; OpenAlex 2-yr mean citedness 5.56; hybrid, APC listed 3,190 USD for open access, a subscription route also exists; verify).
* It publishes retraction analyses regularly. Recent examples found in Crossref (all 2026):
  * Tracking the retracted paper mill articles: a bibliometric study, doi:10.1007/s11192-026-05751-6
  * Understanding prolonged retraction lag among retracted biomedical papers: an explainable machine-learning analysis, doi:10.1007/s11192-026-05808-6
  * Does retraction interrupt knowledge-claims diffusion? Evidence from retracted papers in Nature and Science, doi:10.1007/s11192-026-05741-8
  * Citation dynamics and altmetric trends of retracted publications in Indian-funded research, doi:10.1007/s11192-025-05527-4
* Its readers are meta-researchers, so a cohort study built on Crossref and Retraction Watch data with heavy statistical reporting fits the scope better than a medical-publishing ethics venue.
* Caveat: the project's own earlier (different) manuscript was handled by a BMC journal; Springer Nature journals run similar AI-use screens. Disclosure in the methods and cover letter is required, not optional.

**Second choice: Learned Publishing** (Wiley; mean citedness 5.67; publisher/editor audience, the people who would use a screening idea). 2026 papers on retraction found: doi:10.1002/leap.2102 (China's price of retraction), doi:10.1002/leap.2133 (silent retraction). Shorter, more practical articles; the long statistical supplement would need trimming.

**Stretch: Quantitative Science Studies** (MIT Press, open access, mean citedness 9.31, APC listed 800 USD). The best topical match for rigor (it published Hanson et al. 2024 on publishing strain, doi:10.1162/qss_a_00327, which this paper cites, and doi:10.1162/qss_a_00353 on the retraction gender gap). Highest bar, so highest desk-rejection risk.

**Other options:** Journal of Informetrics (Elsevier, 5.46; e.g. doi:10.1016/j.joi.2025.101745 on retraction drivers), Accountability in Research (T&F, 5.62; e.g. doi:10.1080/08989621.2026.2640012 on a review mill in medicine), Journal of Clinical Epidemiology (5.61; published doi:10.1016/j.jclinepi.2026.112429 on paper mills in evidence synthesis, but it prefers clinical-methods angles).

**Do not** resubmit to Research Integrity and Peer Review (rejected the earlier manuscript on 2026-11-24 for novelty/impact and AI use).

Submit to **one journal at a time**.

## 2. Title

Current title (in the files): **Fast editorial handling and later retraction for peer-review-related reasons: a retrospective stratified analysis of Crossref and Retraction Watch records**

Alternatives:
* Fast acceptance and later retraction for peer-review-related reasons: a within-journal, within-year analysis of 1.8 million articles (shorter; best for Scientometrics or QSS)
* Is unusually fast acceptance a marker of compromised peer review? Evidence from retractions in 800 journals (question form; good for Learned Publishing)

If you change the title, change it in the manuscript, cover letter and submission system, and keep the abstract identical in the system and in the file.

## 3. Why I think it has a fair chance of getting past a desk check (and why it may not)

Honest framing: a desk rejection is a judgement by one editor in a few minutes. I cannot predict it. These are the features an editor will see:

For:
1. Question matches the scope: peer review, editorial speed, retraction; a "warning sign" widely used in practice but rarely tested.
2. Scale and design: 1.8 million dated articles, 3,454 retractions, comparisons inside journal × year, 2,000-draw cluster-bootstrap intervals, a negative control, reason-specific contrasts.
3. Candour: the paper reports what did not work (circular journal-month analysis, weak screening yield, association faded in 2024, only ~43% of retractions covered).
4. Verifiable: an independent audit reproduced every result number exactly; a 30-line script re-derives the headline odds ratio; protocol history is in git.
5. Positioning against the closest prior work (a non-peer-reviewed within-journal comparison, Manusights 2026, doi:10.5281/zenodo.23353186) is now explicit in the Introduction and the cover letter.

Against (these can still cause rejection):
1. **Incremental novelty.** The closest prior analysis (PubMed, same journal and year) found the same direction. Our additions are the full-cohort design, negative control, heterogeneity, year pattern and out-of-time test. An editor may judge this incremental, as RIPR did for the earlier paper.
2. **Generative AI use.** The editor who rejected the earlier version flagged it. Springer Nature and other publishers generally do not forbid disclosed AI assistance but do forbid AI authorship and expect human accountability. The more the final text is rewritten, checked and understood by you, the safer this is. I cannot change this by editing.
3. **Effect is uneven and weakening**, concentrated in a few journals and publishers, with weak screening value. A referee may call the practical impact limited.
4. **Possible circularity**: publishers may investigate fast papers.
5. **Pre-registration is only partial** (amendments after seeing results; disclosed).
6. The three publishers are the only ones with deposited dates in Crossref; Taylor & Francis contributes few retractions.

My estimate (judgement, not computed): at Scientometrics a desk rejection is plausible but not likely if the text is rewritten by the authors, the AI disclosure is clean and the journal's formatting rules are followed; at QSS it is more likely than not.

## 4. Steps before you submit

1. Run `python3 reinforced/code/src/verify_headline_numbers.py` (needs the data rebuild in HANDOFF.md) and look at the result files.
2. Rewrite the manuscript in your own words; cut it toward the journal's length; format references to its style.
3. Check every reference; add anything you know that is missing.
4. Deposit code and derived data on Zenodo (get a DOI) and put the DOI in the Data/Code availability statement. The cover letter says this will be done: do it.
5. Complete the funding, competing-interest, author-contribution, ethics (public data; confirm exemption wording) and AI-use statements; read the journal's current AI policy and follow its wording.
6. Replace the cover-letter placeholders (date, journal name is already filled in the Scientometrics version).
7. Have one human colleague (statistics or research integrity) read it critically.
8. Submit only after you are satisfied with 1–7.

## 5. What would raise the odds (further work, not done)

* Rebuild the cohort from all Crossref journal articles, not only a pre-selected 800-journal set, to address selection.
* A frozen-threshold test on articles accepted after this snapshot.
* Two-way (publisher × journal) cluster inference and a human biostatistician's sign-off.
* Replicate with another publisher's deposited dates when available.
