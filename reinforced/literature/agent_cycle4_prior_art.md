# Cycle 4 prior-art search: editorial handling times as predictors of retraction / paper-mill / peer-review-manipulation involvement

Search date: 2026-11-24. Machine-readable references: `verified_references_cycle4.json` (34 entries; DOIs resolved through Crossref, except five arXiv DOIs resolved through DataCite because Crossref does not index them).

## 1. Plain verdict

**I found no published or preprinted study that does what you describe: an article-level, journal-year-adjusted, out-of-time evaluation of timing anomalies as predictors of later retraction (overall or by Retraction Watch reason) on a corpus of roughly 1.7M articles from Springer Nature, Wiley and Taylor & Francis.** This is an absence in my searches, not proof of absence (see section 8 for coverage limits). In particular I could not rule out unpublished publisher-internal analyses. Wiley's Hindawi whitepaper says suspect turnaround times were among its screening signals, but I read only a search snippet of it.

The hypothesis itself is **not novel**. "Very short submission-to-acceptance time is a red flag" is stated in COPE/STM-style guidance, in the Wiley whitepaper, and in several empirical papers. These cover editors, journals and special issues, but nobody has tested it at article level with controls for journal and year.

The closest prior work, with where it stops:

| Closest work | What it did | Where it stops |
|---|---|---|
| Bishop 2023 (PsyArXiv) | All 2022 Hindawi articles; special issue vs regular articles in the same journal; editors with PubPeer-flagged papers had shorter response times | Editor-level, descriptive, a single publisher and year; PubPeer is the outcome, not Retraction Watch reasons; no out-of-time test |
| Richardson et al. 2025 (PNAS) | Flagged editors at PLOS ONE and Hindawi by anomalous retractions, PubPeer comments and short turnaround (30 days or fewer) | Editor-level; short turnaround is a parallel marker, not a validated predictor; the authors call it a less robust marker at PLOS ONE |
| Mascato Fontaina et al. 2025 (RIPR) | Journal-level comparison of journals with 1, 2-9 and 10 or more paper-mill retractions against journal-reported editorial times | Journal level only; editorial times came from just 9 of the top group's 35 journals; the difference was not significant |
| Schonhaut et al. 2022 (RPSP) | COVID-19 articles in 2020 (n = 31,319) had a median 8 days to acceptance; 82 retractions or withdrawals | Descriptive; no model; 27 of the retractions came from one journal |
| Arjomandi 2026 (arXiv) | **Design precedent**: frozen T0 and journal-by-year strata on Retraction Watch | Predictor is citation of retracted work, not timing |

## 2. What is and is not novel for your design

**Not novel (cite, do not claim):**
- The thesis that fast acceptance is an integrity red flag. Sources: Bishop 2023, Scanff 2021, Richardson 2025, Schonhaut 2022, Mascato 2025, COPE/STM 2022 and Parker 2024 (as guidance).
- Special issues being accepted faster and more homogeneously than regular articles. Sources: Hanson 2024, which includes Taylor & Francis via Crossref and a partial Springer sample; Bishop 2023; Petrou 2025 (Scholarly Kitchen); Sridharan 2026.
- Retraction Watch paper-mill and fake-peer-review studies that report peer-review time descriptively (Kocyigit 2023, Abo-Elnour 2025, Sridharan 2026).
- Machine-learning retraction prediction with Retraction Watch labels (Fletcher 2025, Scancar 2026, Farquhar 2026).
- A frozen-T0, journal-by-year-stratified, out-of-sample retraction test as a method (Arjomandi 2026).

**Novel (as far as I could find):**
1. **Article-level association between timing and retraction with journal-by-year fixed effects or strata.** Every timing study I found is descriptive, journal-level or editor-level, unadjusted, or has no non-retracted comparator.
2. **Out-of-time validation of timing predictors.** None of the timing studies uses a temporal split. The ML retraction studies use random or period-matched designs.
3. **Outcome disaggregated by Retraction Watch reason** (fake or compromised peer review, paper mill, and so on) against timing. Existing reason-by-time work is limited to retracted-only samples.
4. **Scale and publisher mix** (Springer Nature, Wiley, Taylor & Francis; about 1.7M articles). Hanson 2024 covers these publishers' turnaround but has no retraction outcome. Bishop and Richardson use only Hindawi and PLOS ONE.
5. **Specific timing features.** I found no study testing any of these as retraction predictors: same-day or batch acceptance, weekend or holiday acceptance, accepted-to-published lag, or within-special-issue clustering of acceptance dates. Weekend or day-of-week work exists (Ausloos 2016), but it concerns population-level submission and acceptance patterns, not integrity.
6. **A possible null or weak-signal result.** Prior evidence is mixed. Richardson says short turnaround is less robust than retractions or PubPeer comments. Mascato's journal-level direction is not significant. A calibrated "weak but real" or "null after journal adjustment" finding would be informative.

## 3. Evidence table: studies that touch timing and integrity outcomes

"Read" states how much I opened. Abbreviations: RW = Retraction Watch, SI = special issue, T-A = submission-to-acceptance.

| # | Authors, year, venue | DOI / URL and Crossref title | Design; data | Exposure / outcome | Main finding | Adjusts for journal? | Read |
|---|---|---|---|---|---|---|---|
| 1 | Bishop DVM, 2023, PsyArXiv | 10.31234/osf.io/6mbgv. "Red flags for paper mills need to go beyond the level of individual articles: a case study of Hindawi special issues" | Descriptive; all Hindawi articles dated 2022 (N not extracted by me), scraped from the Hindawi site; 10 journals flagged by sleuths | Exposure: "Editor RT" = receipt to first revision date; 22-day cutoff = 2nd percentile of regular articles. Outcome: PubPeer-flagged editors; share retracted | Some SIs had 50% or more of response times under 22 days. Editors with PubPeer-flagged papers handled more articles and had significantly shorter response times. No-revision share and email-domain diversity did not separate the groups | Partly: SI vs regular articles compared within the same journals; no regression | Full text (OSF docx) |
| 2 | Richardson RAK, Hong SS, Byrne JA, Stoeger T, Amaral LAN, 2025, PNAS 122(32) | 10.1073/pnas.2420092122. "The entities enabling scientific fraud at scale are large, resilient, and growing rapidly" | Network and anomaly analysis; PLOS ONE (metadata to Nov 2023) and Hindawi (to Apr 2024); RW 47,387 records; PubPeer 105,325 articles | Editor-level markers: anomalous retractions, PubPeer comments, T-A of 30 days or fewer (FDR 0.05) | 22, 33 and 88 PLOS ONE editors flagged for retractions, PubPeer and short turnaround. Short turnaround gave a "comparatively small number" of authors enriched for flagged editors, so it is a "less robust marker" for collusion at PLOS ONE | No (editor-level) | Full text (PMC12358853) |
| 3 | Scanff A, Naudet F, Cristea IA, Moher D, Bishop DVM, Locher C, 2021, PLOS Biology 19(11) | 10.1371/journal.pbio.3001133. "A survey of biomedical journals to detect editorial bias and nepotistic behavior" | Journal-level survey; 5,468 NLM journals, 4,986,335 papers, 2015-2019 | Exposure: PPMP and Gini concentration. Outcome: lag from submission to acceptance | Papers by the most prolific authors were more likely accepted within 3 weeks (277 journals, 10.2%, with median lag under 3 weeks vs 51, 1.9%, for other authors). Lag was uncomputable for 50.2% of journals because dates are not reported | Journal is the unit; within-journal comparison; no retraction outcome | Abstract and search snippets |
| 4 | Hanson MA, Gomez Barreiro P, Crosetto P, Brockington D, 2024, QSS 5(4) | 10.1162/qss_a_00327. "The strain on scientific publishing" | Publisher-level metrics; scrapes and Crossref; T-A computed for MDPI, Frontiers, Hindawi, Wiley, Springer, Nature, Taylor & Francis (via Crossref), BMC, PLOS; Elsevier SI data too sparse | T-A and SI share; no retraction outcome | MDPI mean T-A about 37 days, Frontiers 72, Hindawi 83, others over 130. SI articles are accepted faster and more homogeneously; Springer is the exception in Fig. S7 | No (publisher-year t-tests) | Full text (arXiv 2309.15884) |
| 5 | Mascato Fontaina N, Candal-Pedreira C, Garcia G, Ross JS, Ruano-Ravina A, Martin-Gisbert L, 2025, RIPR 10:21 | 10.1186/s41073-025-00177-9. "Identifying common patterns in journals that retracted papers from paper mills: a cross-sectional study" | Journal-level; RW paper-mill retractions Jan 2020 to Dec 2022 (142 journals, 2,051 articles); JCR and WoS covariates | Exposure: journal-reported days to 2nd editorial decision. Outcome: journals grouped as 1, 2-9, 10 or more paper-mill retractions | Median 116, 103.5 and 86 days across the three groups (available for only 25, 16 and 9 journals). No significant association in ordinal or binary logistic models. The abstract's wording ("short editorial times may indicate...") over-reads this, and its 86 vs 116 order is reversed relative to the table | No (journal-level) | Full text (PMC12487316) |
| 6 | Schonhaut L, Costa-Roldan I, Oppenheimer I, Pizarro V, Han D, Diaz F, 2022, RPSP 46 | 10.26633/rpsp.2022.25. "Scientific publication speed and retractions of COVID-19 pandemic original articles" | Descriptive; PubMed, 31,319 COVID-19 and 4,287 influenza articles from 2020 | T-A; counts of retractions and withdrawals | Median T-A 8 vs 92 days; 47.0% accepted within one week and 19.5% within one day; 82 retractions or withdrawals vs 1 for influenza; 27 came from one group in one journal | No | Abstract (Crossref) |
| 7 | Sridharan K, Sivaramakrishnan G, 2026, Front Res Metr Anal 10 | 10.3389/frma.2025.1737168. "Artificial intelligence in the retraction spotlight: ..." | Bibliometric review; Scopus; 335 retracted AI-related articles | T-A; special-issue status; compromised peer review was the most common reason | SI articles had significantly faster T-A (p = 0.016) (one secondary source gives about 46 vs 80 days) | No; retracted-only sample, no non-retracted comparator | Abstract; the day figures are secondhand |
| 8 | Kocyigit BF, Zhaksylyk A, Akyol A, Yessirkepov M, 2023, JKMS 38(46) | 10.3346/jkms.2023.38.e390. "Characteristics of Retracted Publications From Kazakhstan: ..." | Descriptive; RW; 91 retracted papers | "Peer review time" = accepted minus submitted dates; reasons | Median 58 days (16-316); fake or biased peer review was the leading reason (n = 38) | No; no comparator | Full text (PMC10681843) |
| 9 | Abo-Elnour DE et al., 2025, Eur J Pediatr 184(12):740 | 10.1007/s00431-025-06578-8. "Comprehensive bibliometric analysis of ... retractions in pediatric literature" | Descriptive bibliometric analysis | T-A vs time to retraction | Per a search-engine summary only: median T-A about 50 days for 590 retracted papers; no meaningful correlation with time to retraction. **I could not open the abstract.** | No | Not verified |
| 10 | Lemarchand C, Naudet F, Pencole M-A, Ropers L, Scanff A, Cristea IA, Locher C, 2026, medRxiv | 10.64898/2026.08.17.26360597. "Editors and research articles: a retrospective study of self-publication in biomedical research" | Journal-level; 1,623 journals via Open Editors, 2020-2023 | Editor authorship; publication lags | Median publication lag 99 days for authors, 95 for editors and 84 for editors-in-chief | Journal-level indicators; unclear whether lags are compared within journal | Abstract (Crossref) |
| 11 | Crosetto P, Gomez Barreiro P, Hanson MA, 2026, arXiv 2601.07563 | 10.48550/arxiv.2601.07563 (DataCite). "The Issue with Special Issues: when Guest Editors Publish in Support of Self" | Special-issue-level; more than 100,000 SIs, 2015-2025, 5 publishers | Endogeny above 33% ("SI-hacked") | More than 1,000 hacked SIs per year; no timing or retraction outcome in the abstract | n/a | Abstract |
| 12 | Petrou C, 2025, Scholarly Kitchen (grey literature, no DOI) | https://scholarlykitchen.sspnet.org/2025/05/29/guest-post-reading-the-leaves-of-publishing-speed-the-cases-of-hindawi-frontiers-and-plos/ | Hindawi data dump 2019-2022 (no longer available); Frontiers in Oncology and PLOS ONE from PubMed | T-A, SI vs regular | By 2022 Hindawi SI papers were accepted 56 days faster (67 vs 123), and 38 days faster already in Q2 2020. The author frames this as a missed early warning; there is no statistical link to retractions | Descriptive | WebFetch summary only |
| 13 | Dianovics D, Varga MA, Bognar M, Aczel B, 2025, Lifecycle Journal | 10.71240/lcyc.084124. "Acceptance and publication lags in scholarly journals between 2016 and 2025" | Research plan; about 6.6M PubMed articles; random 80/20 split; CatBoost and GAM | Lag is the outcome, not a retraction predictor | Exploratory plan, no results found. Per cycle-2 notes it links RW as a covariate | Journal characteristics as predictors; random split | Record read earlier (cycle 2) |
| 14 | Fletcher AHA, Stevenson M, 2025, RIPR 10:9 | 10.1186/s41073-025-00168-w. "Predicting retracted research: a dataset and machine learning approaches" | Case-control; 9,028 articles (2000-2020) from RW and OpenAlex, matched on period | Features: text, topic, author country, citations, year. No timing features | Best precision about 0.69; the publication-year feature dominated the ablation | Matched on period, not journal | Full text (PMC12153192) |
| 15 | Arjomandi HM, 2026, arXiv 2611.10474 | 10.48550/arxiv.2611.10474 (DataCite). "Do links to retracted papers predict future retractions? An out-of-sample test on the open biomedical citation graph" | Pre-specified; 10.5M biomedical papers; T0 = January 2024 OpenCitations graph; outcome = RW retractions from Feb 2024 to Oct 2026 | Citing retracted work | Within-journal-year OR 2.99 (95% CI 2.73-3.27). As a screen it is weak, and the journal's own retraction rate becomes the better screen when T0 sits inside the 2023 retraction wave | Yes (journal-by-year strata) | Full text |

## 4. Coverage by question

- **Very fast acceptance, article level.** Only Schonhaut 2022 (descriptive, COVID-19) and Sridharan 2026 (retracted-only sample).
- **Very fast acceptance, journal level.** Mascato 2025 (not significant, journal-reported times) and Scanff 2021 (lags only).
- **Very fast acceptance, special-issue level.** Bishop 2023, Hanson 2024 and Petrou 2025 show faster SI acceptance. None validates timing against retraction at SI level; Bishop's PubPeer link is at editor level.
- **Batch or same-day acceptance.** Only anecdotes (Hindawi notices with same-day received and accepted dates; search-result examples, not a dataset). No study.
- **Weekend acceptance.** Day-of-week papers only (Ausloos et al. 2016; related arXiv and Scientometrics work), with no integrity outcome.
- **Accepted-to-published lag.** Descriptive only (Petrou 2025; the Hindawi and PLOS ONE production-time figures). The autism-paper accepted-to-published case is a single anecdote. No predictive study.
- **Peer-review manipulation, text-based.** Day 2022 (duplicated referee text), Cabanac's Problematic Paper Screener, Scancar 2026 and Sabel 2025 use content or author features, not timing.

## 5. Screening and red-flag tools based on editorial metadata

- **Published:**
  - Scanff 2021: PPMP, Gini and lag.
  - Bishop 2023: Editor RT plus volume per editor.
  - Richardson 2025: editor anomaly detection.
  - Sabel 2025: a tallying rule for fake publications; its indicators are author and affiliation based, and I found no timing variable in the abstract.
  - Scancar 2026 (BMJ): a BERT screen of titles and abstracts.
- **Guidance only:** COPE and STM 2022 (10.24318/jtbG8IHL; Crossref gives no author list) and Parker 2024 (JCE). Both mention rapid or superficial review as a sign; I could not read the full text of either for a specific threshold.
- **Grey literature and vendors:** the Wiley/Hindawi whitepaper (snippet only), the Retraction Watch Hijacked Journal Checker, and the Problematic Paper Screener. I found no validated timing-based tool with published sensitivity or specificity.

## 6. Studies using Retraction Watch reasons with publication-process variables

- **Journal-level:** Mascato 2025 (reason: paper mill).
- **Retracted-only:** Kocyigit 2023 (Kazakhstan; reasons and review time), Sridharan 2026 (AI; reason and SI status), Abo-Elnour 2025 (unverified).
- **No timing:** Candal-Pedreira 2022 (BMJ, paper mills), Cheng 2026 (Scientometrics, 10,409 paper-mill papers), Oppenlaender 2026 (ten publishers' retraction lags and reasons), Sebo 2024 (country over-representation in fake peer review and paper mill; abstract not read).
- **Outcome-definition hazard (important for your design):** Singh 2026 (MetaArXiv, 10.31222/osf.io/9wgpy_v2) replayed 39 snapshots of the Retraction Watch database. Pre-2024 retractions grew 9.1% and "Paper Mill" records grew 80.6%. The "Fake Peer Review" label fell from 4,654 records to zero when it was renamed. Most of the growth was late cataloguing, 3,921 of 4,482 added records being Hindawi retractions. Reason-level outcomes therefore need snapshot pinning and a label crosswalk. Arjomandi 2026 adds that the RW export does not record when a notice entered the database, which leaks into backtests.

## 7. Publisher-specific findings

- **Hindawi/Wiley.** Bishop 2023 and Petrou 2025 are the only quantitative timing sources. The Wiley whitepaper and Retraction Watch news describe 8,000 or more retractions, special-issue guest editors and peer-review rings, but contain no statistical test of timing.
- **MDPI.** Hanson 2024 reports T-A of about 37 days and 88% of articles in special issues. Oviedo-Garcia 2021 (Res Eval, 10.1093/reseval/rvab020) covers self-citation, not timing, and was retracted and replaced (Retraction Watch coverage). Fränti 2024 (arXiv) is an experience-based discussion. I found no MDPI retraction-by-timing study.
- **Frontiers.** Petrou 2025 covers Frontiers in Oncology T-A. The 2025 peer-review-manipulation network retractions (122 articles) come from press releases, not studies.
- **Springer Nature.** The Arabian Journal of Geosciences and the Journal of Ambient Intelligence and Humanized Computing cases are documented in news and editorials, with no timing analysis. Hanson 2024 has a partial Springer sample and a Nature sample.
- **Taylor & Francis.** Only Hanson 2024's Crossref-derived turnaround. I found no T&F retraction-timing study.
- **Preprints and grey literature.** Bishop (PsyArXiv), Lemarchand (medRxiv), Singh and Farquhar (MetaArXiv), Crosetto and Arjomandi (arXiv). Searches of SSRN, Zenodo and bioRxiv found no additional timing-and-retraction preprint, but those servers were reachable only through web search and Europe PMC, so this is weak evidence of absence.

## 8. What I could not verify, and search limits

- **Not searched:** Scopus, Web of Science, Google Scholar and Dimensions. The arXiv API handled only simple queries.
- **Blocked or paywalled (Springer, PNAS, Wiley, Taylor & Francis, ScienceOpen):** Where I used PMC or arXiv full text, the table says so; elsewhere I relied on abstracts via Crossref or Europe PMC. Items 3, 6, 7, 9, 10, 11 are abstract-level; Abo-Elnour (item 9) is not verified at all.
- **Items I could not read at all:**
  - Harvey 2026 (SSP annual meeting, "Quantity vs Quality: What do low submission to acceptance times really say about your peer review?"; 10.14293/s2199-ssp-am26-01008). Only the title and Crossref record, which is on point.
  - Toraih et al. 2025 (INPLASY 2025.5.0088), a COVID-19 rapid-publication retraction review. A registration listing only, marked "completed but not published", with no methods text.
  - Gomez 2026 (Philippine J Allied Health Sci). I read it: an editorial, not an empirical study.
- **Wiley whitepaper and Retraction Watch news items:** read only as search snippets.
- **Date metadata caveat:** Crossref publication-history assertions are optional, free-form and sparse, and an old study found the accepted field near-empty in 2019. Hanson 2024 used Crossref for T&F turnaround. Coverage for your 1.7M-article corpus should be reported by publisher and year, because missingness is itself correlated with journal type.
- **Crossref metadata notes:** Gleasner & Sood and Mills et al. have Crossref online-first year 2024, issue year 2025. The Singh DOI resolves to a versioned record (`_v2`).

## 9. Eight to twelve references to cite

All are in `verified_references_cycle4.json` under the slugs given.

1. `bishop2023_hindawi_si`: the nearest design, editor and special-issue timing red flags at Hindawi.
2. `richardson2025_pnas`: editor-level anomaly detection that includes a short-turnaround marker; reports it as less robust.
3. `scanff2021_plosbiol`: journal-level lag as a red flag, with a 50.2% date-missingness caveat.
4. `hanson2024_qss`: special issues and turnaround at publisher scale, including Taylor & Francis through Crossref.
5. `mascato2025_ripr`: journal-level paper-mill retractions against editorial times; not significant.
6. `schonhaut2022_rpsp`: fast COVID-19 acceptance with retractions, descriptive.
7. `sridharan2026_frma`: special-issue timing among retracted AI papers; retracted-only.
8. `arjomandi2026_arxiv`: frozen-T0, journal-by-year design on Retraction Watch; the method precedent, with a non-timing predictor.
9. `singh2026_rw_revisions`: outcome-label instability in Retraction Watch; the reason-level analysis must pin snapshots.
10. `dianovics2025_lifecycle`: the overlapping lag-prediction plan (random split); say so, and say it is not a retraction study.
11. `fletcher2025_ripr`: machine-learning retraction prediction on Retraction Watch and OpenAlex without timing features.
12. `crosetto2026_arxiv`: special-issue-level integrity metric (endogeny) as a complementary special-issue signal.

Grey-literature additions (no DOI): Petrou 2025 (Scholarly Kitchen URL in section 3, item 12) and the Wiley/Hindawi whitepaper (https://www.wiley.com/content/dam/wiley-com/en/pdfs/insights/tackling-publication-manipulation-at-scale-a-whitepaper.pdf; snippet-level read).

## 10. Suggested manuscript wording

"We found no earlier article-level analysis that tests submission-to-acceptance timing anomalies against later retraction with journal-by-year adjustment and out-of-time evaluation. Earlier work is descriptive, editor-level, journal-level or special-issue-level (Bishop 2023; Richardson et al. 2025; Scanff et al. 2021; Mascato Fontaina et al. 2025), or lacks a non-retracted comparator (Sridharan and Sivaramakrishnan 2026)."

Do not say "first" without the qualifier "to our knowledge, after a documented search that did not cover Scopus, Web of Science or Google Scholar."
