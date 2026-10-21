# Reviewer C: prior-art investigation (2026-10-21)

Matrix: `agent_C_matrix.csv` (15 rows, all fields). Evidence level is stated per item; "read" means what I actually opened.

## 1. Bottom line

I found **no study that does the project's core task**: forecasting a journal's submission-to-acceptance distribution from its visible past, scoring it out of time with proper scoring rules, and testing "within X days" claims. That is an absence in my searches, not proof of absence. The searches covered Crossref, OSF, PubMed-derived work and the open web, but not Scopus, Web of Science or Google Scholar full text.

The project's narrow claim survives. Its wider framing is weaker than the manuscript implies, because several vendor and blog sources already state the thesis ("a journal median cannot predict an individual paper's wait") and already show drift. I judge the contribution **incremental but real**: a careful application of standard components to a gap nobody has filled. It is not a conceptual advance.

## 2. Closest works

### 2.1 Dianovics, Varga, Bognar, Aczel (the MetaROR / Lifecycle plan), which you asked about specifically
- **Records verified.**
  - Lifecycle Journal v1, DOI 10.71240/lcyc.084124, posted 12 Dec 2025. Its status reads "Evaluation Complete", dated 13 Apr 2026.
  - OSF registration 6a8kg, dated 30 Nov 2025, article type "Research Plan".
  - Crossref lists a MetaROR Editorial Assessment and two reviews (10.70744/metaror.315.1.ea, rv1, rv2), all dated 29 Apr 2026.
- **Read.** The OSF registration metadata and the full text of the Research Plan .docx (downloaded from OSF).
- **Plan content.** Descriptives; GAMs of lag on year, month and weekday (REML); and a CatBoost regression with SHAP. The text says "Train and test data will be a random 80/20 split" with MAE, RMSE and R². The data are 6,642,176 PubMed articles from 2016 to 2025, linked to SCImago, DOAJ, WoS, NPI and Retraction Watch. The project's description of this plan is correct.
- **Status caveats the manuscript does not mention.**
  - The registration answers "OSF registration exists, we did not preregister the study".
  - It also says the authors had already accessed key variables and run some analyses (level 0), and that all analyses are exploratory. The manuscript's phrase "a concurrent registered bibliometric study" is therefore a stretch.
  - I could not read the MetaROR assessment or reviews (login wall), so I do not know what reviewers said about the random split.
- **Results.** I found none, as of 21 Oct 2026. The OSF project xht57 file listing came back empty through the API. The GitHub repo `martonaronvarga/pubdelays` (README read) holds only pipeline code and no findings. I cannot rule out results on OSF or in a v2 that I could not see.
- **Overlap.** Article-level prediction of acceptance lag, drift description, and the use of acceptance-lag data at scale.
- **Differences.** Random split, point prediction, PubMed only, exploratory. Nothing on journal-level distributional forecasts, calibration or claim reliability.
- **Risk.** If its CatBoost results appear with a temporal split, RQ5 (article features add about 3%) would overlap directly.

### 2.2 Phillips & Horn, JAMA Netw Open 2025 (full text read, PMC12117454)
- **Design.** A cross-sectional audit of how 57 health policy journals report review and publication times.
- **Findings.** Reported total times range from 35 to 353 days, 16% of journals report none, and definitions are inconsistent.
- **Limit.** It did not measure actual times, so there is no reported-versus-actual comparison.
- **Relevance.** It is the nearest scholarly study of publisher-reported turnaround claims. It supports the project's motivation, and it is **not cited by the project**.

### 2.3 Hanson et al., QSS 2024 (abstract read, arXiv 2309.15884 and Crossref; full text blocked)
- **Design.** Five publisher-strain metrics, including processing times, from scrapes and publisher data.
- **Finding.** Special issues with short turnaround drove growth at some publishers.
- **Relevance.** It is context for "fast journal" claims and publisher-level non-stationarity. It does no forecasting and is **not cited by the project**.

### 2.4 Himmelstein blog, 2016 (read)
- **Design.** Per-journal regression of delay on date for 3,086 PubMed journals.
- **Finding.** The median acceptance delay has stayed near 100 days since 1981, and journals split roughly evenly between getting faster and slower.
- **Relevance.** It is the first journal-level drift evidence at scale. It is a blog, and it does not compare drift with forecast error.

### 2.5 Luwel et al. 2020 and Hadavand, Hamermesh & Wilson, JEL 2024
- **Verification.** Both exist (Crossref DOIs 10.1007/978-3-030-47665-6_4 and 10.1257/jel.20221653).
- **What I read.** Only the Dianovics plan's descriptions of them, not the works themselves.
- **Luwel.** More than 3M Elsevier articles from 2000 to 2016, with receipt-to-acceptance stagnant at a median of about 120 days.
- **Hadavand.** Top-five economics journals take at least a year to accept, and authors and journals hold the manuscript for comparable times.
- **Relevance.** Both are large or field-level drift or variance evidence, and neither is cited by the project. The Luwel citation is secondary and needs checking against the chapter.

### 2.6 Sebo and colleagues, 2019 to 2023
- **Verification.** Three Scientometrics and Internal and Emergency Medicine papers, confirmed by Crossref record only.
- **Design.** Regressions of PubMed acceptance and publication lags on journal factors in 18 to 117 medical journals.
- **Relevance.** They are journal-level descriptive correlates, with no forecasting. Not cited by the project.

### 2.7 Bilalli et al. 2021 and Björk & Solomon 2013
- **Verification.** I could not read either (Springer blocked). I confirmed the Crossref records and rely on the project's own characterisation, which I did not verify.
- **Relevance.** Björk & Solomon is the variance-partition ancestor of RQ1. Bilalli is the nearest reported-versus-computed comparison, but it covers only 10 journals.

### 2.8 Industry and blog sources, which are not scholarly
- **Manusights "Peer Review Timelines" v2026.2 (page read).**
  - Data: PubMed received-to-accepted dates, with up to 300 records per journal for 104 selected journals.
  - Finding: a median of journal medians of 153 days, and a within-journal change since 2014–15 of +32.5% (+13.8% excluding Cell Press).
  - It states that a journal median "cannot predict an individual paper's wait". It does not test this.
- **GradSummit "Journal Clock" (page read).**
  - 4,252 journals and 5.6M articles from PubMed.
  - A "submission planner" uses past medians and a three-in-four point. No validation is described.
  - This is the practical use case the project evaluates, and it is untested.
- **Petrou, Scholarly Kitchen 2025 (read).** Frontiers in Oncology acceptance time went from 77 to about 120 days in 2022–24, and PLOS ONE peaked at 221 days then fell to about 180. This is evidence of non-stationarity over short spans.
- **Royle, quantixed 2026 (read).** Descriptive PubMed lags at 20 cell biology journals, "creeping up at some journals, but not at others". No forecasting.

## 3. Answers to the seven angles

1. **Forecasting review duration.** Nothing found at journal or article level, in ML or statistics. Searches on pinball loss, prediction intervals, survival with temporal validation and gradient boosting returned nothing relevant. The only forward-looking item is the Dianovics random-split plan.
2. **Variance decomposition or hierarchical models across journals.** Nothing beyond Björk & Solomon (2013) and single-journal regressions. A Journal of Communication study (n = 42) explained about 26% of variance in one journal, which is not cross-journal. I found no published multilevel ICC for submission-to-acceptance, though I did not read the Sebo papers closely enough to rule out partial analyses.
3. **Publisher-reported versus article-level.** Phillips & Horn (reported only), Bilalli (10 journals) and the Manusights hold-for-review rule (a 25% discrepancy flag against publisher-reported medians) are the nearest. No large-scale systematic comparison found.
4. **Drift.** Himmelstein, Luwel (via secondary), Hadavand (via secondary), Petrou, Royle, Manusights and Horbach 2020 all show non-stationarity. None compares drift magnitude with forecast error or sampling noise.
5. **MetaROR plan.** Covered in 2.1: verified as a plan, no results found, review text unreadable.
6. **Crossref received/accepted at scale.** I found no published study using Crossref publication-history assertions at scale. A Crossref forum answer (found by search, not opened) says received dates are not core metadata and are optional Crossmark publication-history assertions. The 2026 PLOS ONE completeness paper (read) covers six elements and **not** received/accepted dates, and excludes Springer Nature. A claim that Crossref's accepted field is sparse and often wrong (975 of about 800,000) comes from a search-engine summary. The arXiv paper it was attributed to (1906.03307) has an abstract that does not mention it, so treat the claim as **unverified**. Most PubMed-based work above uses PubMed rather than Crossref. The data-source novelty (Crossref publication-history assertions from three publishers) therefore appears genuine, and the manuscript's cross-check against PubMed is sensible.
7. **Bibliometric studies of speed claims.** Oviedo-García 2021 (MDPI; the paper carries an expression of concern; I saw only secondary summaries) and Hanson 2024 concern speed as a feature of fast publishers. I found no study testing the reliability of a stated "within X days" claim. Phillips & Horn audit reporting, not accuracy.

## 4. Novelty stress test

**Is the main contribution already known?** The qualitative message is known and has been stated several times: journal medians are noisy, within-journal variance dominates, and turnaround drifts. Björk & Solomon, Himmelstein, Manusights and Petrou all point at this. The quantified, out-of-time test is not known.

**Is it a combination of standard components?** Yes. Pinball loss, interval coverage, empirical-quantile forecasters, shrinkage, cluster bootstrap and a visibility rule are textbook forecast-evaluation methods (Gneiting and others). The domain application is new; the toolkit is not.

| Project claim | Verdict |
|---|---|
| 1. Out-of-time, visibility-respecting benchmark of journal turnaround with proper scoring rules | **Survives.** Nothing found. Strongest claim. |
| 2. Calibration of "within T days" evidence (RQ4) | **Survives, narrowly.** No competitor found, but it is a thin extension of claim 1 using binary event scores. |
| 3. Variance partition with year component (RQ1) | **Incremental.** Björk & Solomon ancestry, and the project already says so. A journal/journal-year/article ICC is routine. |
| 4. Drift versus noise (RQ3) | **Partly known.** Drift is documented widely. Quantifying it against forecast error is new. |
| 5. Publisher-reported versus article-level | **Not a project claim**, and only weakly addressed. The manuscript tests past article-level data, not publisher statements. |
| 6. Data source: Crossref assertions | **Moderate.** No prior Crossref study found, but the data are not new in kind, since PubMed has the same dates. |
| RQ5 (article features add about 3%) | **Contested ground.** The Dianovics plan targets the same question with CatBoost, random split. Whoever reports first with a proper split owns it. |

**Where the manuscript overreaches or under-cites.**
- It never cites Phillips & Horn 2025, Hanson 2024, Luwel 2020, Hadavand 2024, Sebo 2019–2023, Petrou 2025 or Royle 2026. Searching the project's `literature_matrix.csv` and `search_log.md` shows no trace of any of them except Himmelstein.
- It says RQ2–RQ5 are "not addressed in earlier work" while acknowledging it did not read every full text. That is fairly hedged, but the omissions above weaken the "what these studies do not provide" paragraph, which should cite them.
- "Registered bibliometric study" for the Dianovics plan should be changed (see 2.1).
- The abstract's headline "26.5% between journals" sits beside Björk & Solomon's finding that most variance is within journals. This is consistent, but it is not a new finding.

**Verdict.** I would not call this a major methodological advance. The defensible framing is a first out-of-time evaluation, with a clearly stated finding that simple empirical quantiles are hard to beat and that intervals under-cover mainly because slow papers are not yet visible. I would soften "not addressed in earlier work" to "we found no earlier out-of-time evaluation".

## 5. What I could not verify
- Content of the MetaROR editorial assessment and both reviews (login wall).
- Whether Dianovics et al. have posted results (OSF file listing empty; GitHub has code only; Lifecycle page gives metadata only).
- Full texts of Björk & Solomon 2013, Bilalli 2021, the three Sebo papers, Luwel 2020, Hadavand 2024 and Hanson 2024 (publisher pages blocked or paywalled). Their characterisations in the matrix come from Crossref records, abstracts, the Dianovics plan text or the project itself, as flagged per row.
- The Tóth et al. 2025 Journal of Communication study cited by the Dianovics plan (not located).
- The claim that Crossref's accepted date is sparse (975 of about 800,000): unconfirmed.
- Oviedo-García 2021 figures (secondary summaries only).
- Manusights and Journal Clock are vendor pages with no peer review; I read their stated methods but could not audit the data.
- The SSP 2026 abstract "Quantity vs Quality: What do low submission to acceptance times really say about your peer review?" (Harvey; Crossref DOI 10.14293/s2199-ssp-am26-01008): the record exists but I could not retrieve content, so I cannot say whether it overlaps.
- No search of Scopus, Web of Science, Google Scholar or Dimensions was possible, so literature after October 2025 is incompletely covered.
