# RIPR benchmark, 2023-2026 (ISSN 2058-8615): what the journal publishes, at what scale and length

Prepared 2026-11-24 for the retractions / editorial-timing manuscript. Companion file: `ripr_benchmark_papers.csv` (138 rows, one per Crossref record, 46 columns including classification, full-text metrics and abstract).

## 0. Bottom line

1. The corpus is small. Crossref lists **138 records** with issued date 2023-01-01 or later (2023: 15, 2024: 16, 2025: 26, 2026 to 24 Nov: 81). Ten are corrections, leaving **128 substantive items**: 79 labelled Research, 1 Brief report, 14 Review, 18 Letter/Comment, 16 with no type label yet. Europe PMC returns 126 for the same window, 124 shared DOIs.
2. A typical RIPR research article is **about 5,100 words of main text (IQR 4,000-6,470; p90 8,910), 35 references (26-48; p90 66), 3 tables, 2 figures, a structured abstract of about 315 words**. Reviews are longer (about 6,100 words, 50 references).
3. The typical analysis sample is **median N = 187 (IQR 55-689; p90 5,539; n = 94 empirical papers)**. For document-level meta-research (audits, bibliometric, editorial-record, ML papers) it is **N = 610 (172-2,051; p90 18,231; n = 41)**. People-based studies: **N = 246 (77-460; p90 1,033; n = 23)**.
4. Retraction-focused empirical work is rare: **7 of 128 items (5.5%)** carry a retraction tag, only 4 analyse more than 2,000 units (2,051 paper-mill retractions; 9,028 articles; 9,323 Cochrane reviews; 2,674 publications from one institute). **I found no paper whose main outcome is time-to-retraction or retraction latency** (from titles and abstracts; full text not read for all). Notice type vs citations (a 172-RCT cohort, 18 Nov 2026) and CoI-related notices (886) are the nearest. This is a gap, and also the bar to clear.
5. Large-scale papers at RIPR are not long. The 15 closest "large-scale integrity / editorial-process" papers with full text have median **4,883 words (IQR 4,124-5,566) and 29 references (24-36)**. One 16,006-manuscript editorial-records paper has 2,379 words and 14 references. Scale and a clean design matter more than length.
6. Topic drift: AI/LLM papers rose from 1 of 14 items in 2023 and 0 of 12 in 2024 to 5 of 24 in 2025 and **19 of 78 in 2026**; peer review stays the most common topic (35 of 128, 27%). A live "Artificial intelligence and research integrity" collection exists (section 6).

## 1. Method and provenance

- **Crossref** `works?filter=issn:2058-8615,type:journal-article,from-pub-date:2023-01-01`, cursor paging, 138 of 138 records retrieved. Fields kept: DOI, title, abstract, reference count, is-referenced-by-count, issued, authors, volume, article number. `reference-count` is not a valid `select` key on this route; `references-count` was used instead. `subject` is empty for all records.
- **Europe PMC** `ISSN:2058-8615 AND FIRST_PDATE:[2023-01-01 TO 2026-12-31]`, `resultType=core` (126 hits, 123 with PMCID). **Full-text XML downloaded for all 123 PMCIDs** (the service returned 502/503 under parallel load; re-fetched with back-off, none missing). 121 of the 138 Crossref records have matched XML: 94 research/review items, 17 letters/comments, 10 corrections. The 17 without XML are all dated 2026-06-28 or later (15 from September 2026).
- **Classification** (design, data source, N, unit, topic tags) was done by me by reading each abstract (title and abstract only for 11 items with no abstract). N is the primary analytic unit named in the abstract, or full text for 9 items. Single coder, no double coding, no reliability estimate.
- **Full-text metrics** (words, references, tables, figures, headings, abstract structure, limitations, repositories, statistics) were extracted by script from the JATS XML. Definitions: main-text words = paragraph text in top-level sections excluding Declarations, Funding, Data availability, Supplementary, Abbreviations, References (tables and captions excluded); references = `<ref>` count; tables/figures = `<table-wrap>`/`<fig>` in the body; abstract words exclude headings. Statistics and repository flags are regex keyword hits and were not hand-validated.
- **Citations** are Crossref `is-referenced-by-count` as of 2026-11-24 (Europe PMC `citedByCount` also in the CSV). Counts for 2026 papers are mostly 0-2 and carry no information.
- Publisher pages (biomedcentral.com, springer.com) were not reachable (301 to an authentication redirect); journal-level facts that would only be there (word limits, article-type definitions, decision times, APCs) are **not verified**.

## 2. What RIPR publishes

### 2.1 Type, design and topic (128 substantive items)

| Design (my coding) | n | Notes |
|---|---|---|
| Cross-sectional audit of articles, journals, policies or websites | 25 | median N 253 (128-672); the modal RIPR meta-research design |
| Commentary, conceptual, guidance, workshop report | 19 | 15 of them in 2026 |
| Survey of people | 15 | median N 382 (254-783) |
| Systematic/scoping/narrative review | 15 | median N 53 studies (40-81) |
| Bibliographic-database or large corpus study | 13 | median N 6,047 (966-48,332) |
| Experiment, RCT, before-after, LLM experiment | 11 | median N 58 (50-110) |
| Case study / case series | 9 | |
| Tool, framework or method development | 6 | |
| Retrospective analysis of editorial or funder records | 5 | median N 388 (350-6,606), up to 16,006 manuscripts |
| Mixed methods | 5 | |
| Qualitative interviews | 3 | N = 25-27 |
| ML on bibliographic data, Delphi | 1 each | |

Journal type labels (Europe PMC): 2023 Research 11, Review 1, Letter 2; 2024 Research 11, Letter 1; 2025 Research 19 (+1 Brief report), Review 2, Letter 2; 2026 Research 38, Review 11, Letter 13, 16 unlabelled. The journal's "Research" label includes opinion-like pieces (for example the ChatGPT-and-peer-review paper, which I coded as commentary), so label and design do not map one to one.

### 2.2 Topics (non-exclusive tags, n = 128)

peer review 35; AI/LLM 25; reporting quality 14; conflicts of interest/funding 11; equity-diversity-gender 10; policy 10; fraud 9; misconduct 8; research ethics oversight 8; reporting/publication bias 8; authorship 7; education/training 7; **retraction 7**; editorial timing 6; QRPs 4; reproducibility 4; data sharing 4; plagiarism 2; paper mills 2; preprints 2; citation accuracy 2.

By year (AI / retraction+paper mill / peer review): 2023 (n=14) 1 / 0 / 6; 2024 (n=12) 0 / 0 / 4; 2025 (n=24) 5 / 2 / 6; 2026 (n=78) 19 / 5 / 19.

Retraction-related items, all years: ethics-approval case study of 456 IHU-MI trials (2023, letter); ML prediction of retraction (2025, N = 9,028); journals that retracted paper-mill papers (2025, 2,051 retractions); the homeopathy trial retraction saga (2026, letter); retracted-author studies in Cochrane reviews (2026, 9,323 reviews); CoI-related retractions and corrections (2026, 886 notices); IHU-MI follow-up (2026, 2,674 publications); gender and retraction prevalence (2026, N unverified); notice type vs citations of RCTs (2026-11-18, 172 index RCTs).

### 2.3 RIPR's own editorial timing (useful as a reference point for the timing manuscript)

Received/accepted dates exist in the XML history for 46 papers only (mostly 2025-2026, so biased towards recent output):

| Interval | n | Median days | IQR | p90 |
|---|---|---|---|---|
| Received to accepted | 46 | 150 | 100-180 | 220 |
| Accepted to first online | 46 | 35 | 18-74 | 94 |
| Received to online | 46 | 198 | 124-248 | 275 |

By year, received-to-accepted medians are 165 (2023, n=6), 177 (2024, n=6), 84 (2025, n=9), 143 (2026, n=25). Not verified against any official journal statistic.

## 3. Closest comparators: large-scale meta-research on retractions or editorial/peer-review processes

Selection rule (coded in CSV column `closeness`, 0-5): topic score 2 if retraction / paper mill / editorial timing / journal response to concerns, 1 if peer review, fraud, misconduct, COI, policy, authorship, plagiarism; data score 2 if bibliographic database, editorial-record or ML study, 1 if audit or case series; plus 1 if N >= 500. Pool = closeness >= 3 and no commentary, survey, experiment, qualitative or method papers: **23 papers**. Lists below take the top 15 by Crossref citations and the 15 latest by date; 7 papers appear in both. Closeness is my judgement and is not validated.

### 3a. Fifteen most-cited (Crossref count / Europe PMC count; ranks 9-15 are ties at 0-2 citations)

| # | Date | Cites | Title | Sample | Method | Claimed contribution |
|---|---|---|---|---|---|---|
| 1 | 2023-08-03 | 14/9 | Raising concerns on questionable ethics approvals – a case study of 456 trials from the Institu | 456 IHU-MI trials (case series) | Manual comparison of stated ethics approval numbers/IRB with French legal framework; journals contacted; no inferential statistics | Documents shared/absent approval numbers (248 with one number; 39 with none) and journal responses (PLOS EoCs) |
| 2 | 2023-09-05 | 12/4 | Authorship and citation patterns of highly cited biomedical researchers: a cross-sectional stud | 18,231 highly cited health researchers (Scopus, 1990-2019) | Cross-sectional bibliometric; partial Pearson correlations of authorship-position counts with H and Hm index, adjusted for career length | H-index rewards mid-list/last authorship and penalises single/first authorship; Hm index does not |
| 3 | 2023-10-24 | 11/7 | Peer reviewers' willingness to review, their recommendations and quality of reviews after the F | 118 double-blind vs 232 single-blind first-round reviews (59 manuscripts) at one journal | Before/after on editorial records; chi-square, t-test; Review Quality Instrument scored by two reviewers | Effect of single- to double-blind switch on reviewer willingness, recommendations and review quality |
| 4 | 2025-06-11 | 10/2 | Predicting retracted research: a dataset and machine learning approaches | 9,028 articles 2000-2020 (4,514 retracted, matched controls) | Retraction Watch + OpenAlex; case-control; feature-based classifiers vs language models; accuracy/precision/recall/F1; ablation | Open dataset and benchmark: precision about 0.68-0.69, i.e. modest predictability of retraction |
| 5 | 2025-10-01 | 10/2 | Identifying common patterns in journals that retracted papers from paper mills: a cross-section | 2,051 paper-mill retractions in 142 journals (2020-2022) | Retraction Watch + WoS/JCR; cross-sectional; journals binned by retraction count (1, 2-9, >=10); logistic regression on journal traits | Journal-level profile of paper-mill retractions (mostly Q2-Q3 by impact factor; 61% medicine/health) |
| 6 | 2025-07-11 | 5/5 | Misidentified cell lines: failures of peer review, varying journal responses to misidentificati | 4 publications on misidentified cell lines | ICLAC registry + PubMed; letters to editors; narrative | Variation in journal responses (corrections vs declining to act); failure of peer review |
| 7 | 2024-09-30 | 3/3 | Differences in the reporting of conflicts of interest and sponsorships in systematic reviews wi | 924 dental systematic reviews | PubMed abstracts vs journal website vs full text; logistic regression on COI reporting | COI/sponsorship statements missing from abstracts (69-88% no COI statement) though present in 87% of full texts |
| 8 | 2026-06-09 | 2/1 | Reviewer recommendations and editorial outcomes in peer review: a longitudinal analysis of agre | 16,006 manuscripts (12,187 published, 3,819 rejected; 26,686 review-round records), MDPI Healthcare 2021-2025 | Single-journal editorial records; majority-recommendation vs outcome; discordance by round; sensitivity analyses; bootstrap | Manuscript-level evidence on reviewer disagreement and its editorial resolution (14 references, 2,379 words: the leanest paper in the pool) |
| 9 | 2026-02-05 | 2/1 | Most science is published from countries lacking in democracy and freedom of press | 4,185,853 Scopus publications (2024); countries | Bibliometric cross-linking with Democracy Index and press-freedom indices; correlations (r=0.02, 0.00) | Full democracies produce 22% of 2024 output vs 66% in 2006 |
| 10 | 2024-06-25 | 2/0 | Peer review trends in six fisheries science journals | 6,606 manuscripts, 6 American Fisheries Society journals, 2011-2021 | Editorial-system data; trends in invitations, review time, agreement, rejection by blinding; model-based trend tests (data on request) | Rising reviewer invitations; review time stable (+/-2 weeks); about 20% higher rejection under double-blind |
| 11 | 2026-06-22 | 1/0 | Research integrity within systematic reviews: investigating the prevalence of studies by author | 9,323 Cochrane reviews; authors with >=24 retractions in Retraction Watch | Custom Stata code on RW leaderboard; manual checks; descriptive | 81 (0.9%) reviews included/cited; 32 included in meta-analyses; 6/32 ran sensitivity analyses |
| 12 | 2026-09-30 | 1/n/a | Gender imbalances of retraction prevalence among highly cited authors and among all authors | Not verified (no abstract in Crossref/EPMC) | Per bioRxiv preprint snippet: Scopus + Retraction Watch, retraction prevalence by gender among highly cited authors and all authors with >=5 publications | Minimal gender difference after adjustment (preprint figures only; not verified against RIPR version) |
| 13 | 2026-06-04 | 1/0 | Linguistic shifts in dental scientific writing in the large language model era | 2,770 abstracts, 6 dental journals | Vocabulary-based AI-marker scores before/after LLM era | AI-detection score +20.4%; high-suspicion abstracts 18.0% to 25.8% |
| 14 | 2026-09-28 | 1/n/a | Trends in artificial intelligence-generated and -assisted content in comment pieces in The Lanc | 993 comment articles, Lancet Regional Health (2020-2025) | Pangram AI detector; detector validation on 50 pre-2023 comments; citation comparison | AI-flagged comments first appear in 2023 (7/185, 3.7%) and rise to 23/203 (11.3%) the next year; 100% of 376 pre-2023 comments classed human |
| 15 | 2026-07-08 | 0/0 | Retraction and correction of scientific articles due to conflicts of interest: a cross‑sectiona | 886 CoI-related notices (748 retractions, 39 corrections, 97 EoC, 2 reinstatements) | Retraction Watch via Crossref to 23 Apr 2026; descriptive plus bootstrap CIs; manual verification | CoI as sole reason in 10.7% of notices; first mapping of CoI-driven editorial actions |

### 3b. Fifteen most recent (same pool)

| # | Date | Cites | Title | Sample | Method | Claimed contribution |
|---|---|---|---|---|---|---|
| 1 | 2026-11-18 | 0/n/a | Publishers’ responses to integrity concerns – does the type of notice influence subsequent cita | 172 index RCTs with integrity concerns (41 notices, 38 EoC, 23 retracted) + 3,330 matched controls; 10,603 citations | Monthly citation rates +/-60 months around notice vs matched controls (abstract only; full text not yet in PMC) | No significant difference in post-notice citation decline across notice types |
| 2 | 2026-10-09 | 0/n/a | Linguistic inequity in academia: evidence from publication patterns in philosophy, 1975–2021 | 103,595 articles, 223 philosophy journals (1975-2021) | Two automated classifiers (accuracy >89%) on affiliation and PhD country | Severe under-representation of non-native-English authors in top journals |
| 3 | 2026-10-06 | 0/n/a | Robot pen pals: a systematic analysis of recent trends in scientific correspondence | About 780,000 PubMed letters-to-editor records (2005-2025) | Descriptive time-series; epidemiological framing of high-output authors | Growth years 2013, 2020, 2023-; more high-output authors post-LLM |
| 4 | 2026-09-30 | 1/n/a | Gender imbalances of retraction prevalence among highly cited authors and among all authors | Not verified (no abstract in Crossref/EPMC) | Per bioRxiv preprint snippet: Scopus + Retraction Watch, retraction prevalence by gender among highly cited authors and all authors with >=5 publications | Minimal gender difference after adjustment (preprint figures only; not verified against RIPR version) |
| 5 | 2026-09-28 | 1/n/a | Trends in artificial intelligence-generated and -assisted content in comment pieces in The Lanc | 993 comment articles, Lancet Regional Health (2020-2025) | Pangram AI detector; detector validation on 50 pre-2023 comments; citation comparison | AI-flagged comments first appear in 2023 (7/185, 3.7%) and rise to 23/203 (11.3%) the next year; 100% of 376 pre-2023 comments classed human |
| 6 | 2026-08-12 | 0/0 | Follow-up investigation of ethics approvals and regulatory compliance in publications from the  | 2,674 IHU-MI publications assessed; 853 with concerns; 374 with obtained approvals | PubMed/GScholar/PubPeer plus transparency requests; comparison with French legal framework | 81.3% (304/374) of documented approvals inconsistent with described sampling; follow-up to 2023 letter |
| 7 | 2026-07-08 | 0/0 | Retraction and correction of scientific articles due to conflicts of interest: a cross‑sectiona | 886 CoI-related notices (748 retractions, 39 corrections, 97 EoC, 2 reinstatements) | Retraction Watch via Crossref to 23 Apr 2026; descriptive plus bootstrap CIs; manual verification | CoI as sole reason in 10.7% of notices; first mapping of CoI-driven editorial actions |
| 8 | 2026-06-22 | 1/0 | Research integrity within systematic reviews: investigating the prevalence of studies by author | 9,323 Cochrane reviews; authors with >=24 retractions in Retraction Watch | Custom Stata code on RW leaderboard; manual checks; descriptive | 81 (0.9%) reviews included/cited; 32 included in meta-analyses; 6/32 ran sensitivity analyses |
| 9 | 2026-06-13 | 0/0 | Data integrity of the 223 randomized controlled clinical trials produced by multiple groups cen | 223 RCTs by one author network + 103 control RCTs | Systematic search; preregistered Bayesian tests of baseline/dropout patterns (BF10, proportion even dropout 0.76, 95% CI 0.70-0.81) | Statistical evidence of non-random patterns; OSF-registered analyses |
| 10 | 2026-06-09 | 2/1 | Reviewer recommendations and editorial outcomes in peer review: a longitudinal analysis of agre | 16,006 manuscripts (12,187 published, 3,819 rejected; 26,686 review-round records), MDPI Healthcare 2021-2025 | Single-journal editorial records; majority-recommendation vs outcome; discordance by round; sensitivity analyses; bootstrap | Manuscript-level evidence on reviewer disagreement and its editorial resolution (14 references, 2,379 words: the leanest paper in the pool) |
| 11 | 2026-06-04 | 1/0 | Linguistic shifts in dental scientific writing in the large language model era | 2,770 abstracts, 6 dental journals | Vocabulary-based AI-marker scores before/after LLM era | AI-detection score +20.4%; high-suspicion abstracts 18.0% to 25.8% |
| 12 | 2026-06-01 | 0/0 | An observational study of the Patient-Centered Outcomes Research Institute’s switch from in-per | 388 survey responses; 8,599 panelist-level score records (PCORI) | Repeated cross-sectional funder data; linear/logistic regression; thematic analysis | Virtual and in-person review panels broadly equivalent in scores |
| 13 | 2026-05-15 | 0/0 | A portrait of commissioned literature: connecting the dots between medical education and commun | 29,911 commissioned papers (WoS, company sites, Industry Documents Library) | Semi-automated metadata collection (R); network of medical-writing companies, authors, funders, publishers | Only 33.6% of companies in bylines; 18% acknowledged |
| 14 | 2026-02-16 | 0/0 | Trials and tribulations of responsible people trying to uphold scientific standards | 1 trial (case) | Chronology of concerns, institutional investigation (OeAWI, Sept 2022 retraction recommendation) and journal's expression of concern | Documents slow/incomplete editorial response to a misconduct finding |
| 15 | 2026-02-05 | 2/1 | Most science is published from countries lacking in democracy and freedom of press | 4,185,853 Scopus publications (2024); countries | Bibliometric cross-linking with Democracy Index and press-freedom indices; correlations (r=0.02, 0.00) | Full democracies produce 22% of 2024 output vs 66% in 2006 |
Reading the pool: 13 bibliographic-database studies (6 use Retraction Watch/Crossref data), 4 editorial-record studies (journal or funder), 4 case series, 1 audit, 1 ML paper. **Only 2 of 15 pool papers with full text declare an OSF/Zenodo/GitLab-type repository and 1 of 15 declares pre-registration**, so declaring them would put a new paper ahead of its nearest comparators. The pool's N (excluding 1-case reports; n = 21): median 2,674 (IQR 456-16,006; p90 103,595).

## 4. Distributions

### 4.1 Length and structure (from full-text XML)

Median (Q1-Q3; p90). Research = journal label Research or Brief report.

| Measure | Research, all years (n=80) | Research 2024-26 (n=69) | Research 2026 (n=38) | Reviews (n=14) | Letters/comment (n=17) | Closest-pool (n=15) |
|---|---|---|---|---|---|---|
| Main-text words | 5,140 (4,000-6,469; 8,914) | 5,226 (4,067-6,561; 8,921) | 5,715 (4,766-7,740; 9,299) | 6,122 (5,057-7,051; 8,623) | 3,254 (2,096-4,705; 6,377) | 4,883 (4,124-5,566; 5,972) |
| References | 35 (26-48; 66) | 36 (27-50; 67) | 40 (28-50; 64) | 50 (32-68; 82) | 34 (21-50; 64) | 29 (24-36; 41) |
| Tables | 3 (2-4; 6) | 3 (2-4; 6) | 3 (2-4; 6) | 1 (1-3; 4) | 0 (0-1; 2) | 3 |
| Figures | 2 (1-3; 4) | 2 (1-4; 4) | 2 (1-3; 4) | 2 (1-3; 6) | 0 (0-1; 2) | 2 |
| Abstract words | 316 (266-356; 391) | 317 (268-359; 393) | 336 (281-370; 411) | 300 (258-322; 382) | 252 (206-320; 340), n=14 | not computed |
| Sub-headings below level 1 | 12 (7-18; 23) | 13 (7-18; 23) | 15 (9-20; 27) | 14 (10-25; 32) | 1 (0-7; 17) | not computed |
| Authors | 4.5 (2-7; 9) | 5 (2-7; 9) | 5 (2-8; 9) | 2.5 (2-5; 8) | 5 (2-7; 15) | not computed |

Research length rose from 4,085 words / 29 references / 291 abstract words (2023, n=11) to 5,715 / 40 / 336 in 2026. Crossref's reference count matches the XML count to within 2 in 79 of 80 research papers, so Crossref counts can be used as a proxy for the 11 recent items without XML.

Tables range 0-11 and figures 0-13 (the maximum is a single outlier).

### 4.2 Sample size (analysis unit as defined in section 1)

| Group | n papers | Median | IQR | p90 |
|---|---|---|---|---|
| All empirical papers with a stated N | 94 | 187 | 55-689 | 5,539 |
| Same, excluding single-case reports (N > 1) | 92 | 212 | 55-739 | 6,250 |
| Document/record-based (audit, bibliographic, editorial-records, ML) | 41 | 610 | 172-2,051 | 18,231 |
| of which audits | 23 | 253 | 128-672 | 1,079 |
| of which bibliographic-database studies | 12 | 6,047 | 966-48,332 | 712,360 |
| People-based (surveys, interviews, Delphi, participants) | 23 | 246 | 77-460 | 1,033 |
| Systematic/scoping reviews (studies included) | 13 | 53 | 40-81 | 207 |
| Experiments/RCTs | 10 | 58 | 50-110 | 203 |
| Closest-comparator pool, N > 1 | 21 | 2,674 | 456-16,006 | 103,595 |
| 2023 (N > 1) | 10 | 203 | 34-392 | 2,234 |
| 2024 | 10 | 66 | 39-730 | 9,916 |
| 2025 | 21 | 150 | 53-559 | 860 |
| 2026 | 51 | 276 | 99-1,035 | 9,323 |

Mixed units (articles, journals, respondents, notices) are pooled in the first rows, so read the document/people split rather than the pooled line. 34 of 128 items have no usable N (commentary, method papers, corrections excluded, or N not stated). Ambiguous Ns: the 2024 QRP survey is entered as 39,699 respondents from a figure caption ("weighted distribution ... for 39,699 respondents"), which I could not reconcile with the abstract, so treat it as unverified; the Iranian unmatched-count survey and the IRIS framework paper state no N in the abstract.

Largest Ns: 4,185,853 Scopus publications; about 780,000 PubMed letters; 103,595 philosophy articles; 29,911 commissioned papers; 18,231 authors; 16,006 manuscripts (editorial records).

### 4.3 Citations (Crossref, 2026-11-24; research + review items)

| Year | n | Median | IQR | p90 | Max |
|---|---|---|---|---|---|
| 2023 | 12 | 11.5 | 7.8-35 | 139 | 245 |
| 2024 | 11 | 5 | 2.5-15 | 21 | 24 |
| 2025 | 22 | 4.5 | 1.3-10.8 | 15.9 | 31 |
| 2026 | 49 | 0 | 0-1 | 2 | 6 |

Most cited overall: ChatGPT and peer review (245), the TRACT trial-trustworthiness checklist (147), gender differences in grant peer review (66), AI chatbot policies of publishers (31), AI-generated false authorship (28), cost of peer review (25), QRPs and organisational culture (24). All are either AI-related, a reusable instrument, or a headline quantity; none is a retraction analysis. Among the closest comparators the best are 14 (IHU-MI ethics case) and 12 (authorship patterns, 18,231 authors).

### 4.4 Other structural measures (research + review, n = 94 with XML; empirical subset n = 87)

- Structured abstract: 87 of 94 (93%). Headings Background / Methods / Results / Conclusions(s): 64 of 94 (68%); with Objective added: 3; with Trial registration: 2; Objectives/Design/Outcome: 1; unstructured: 7.
- Abstract section length, median words (Q1-Q3): Background 61 (51-85), Methods 69 (54-98), Results 100 (76-135), Conclusions 56 (45-68).
- Level-1 headings: Introduction (50) or Background (44), Methods (76, plus about 10 variants such as Materials and methods), Results (85), Discussion (88), Conclusion(s) (81); a separate "Limitations" heading in 15, "Strengths and limitations" in 3, otherwise as a Discussion sub-section. Most common full skeletons: Introduction/Methods/Results/Discussion/Conclusion (15), Background/Methods/Results/Discussion/Conclusion (14), then variants with Limitations.
- Limitations text found for 70 of 87 empirical papers (80%); among those, median 240 words (127-434; p90 747).
- Back matter: Declarations (ethics, consent, competing interests), Funding, Authors' contributions, Acknowledgements, Availability of data and materials, Abbreviations (31 of 94).
- Reporting guideline named: 32 of 87 empirical papers (37%): PRISMA family 31 mentions, CONSORT 11, STROBE 9, CHERRIES 4, SPIRIT 4, STARD 3, TRIPOD 3.
- Pre-registration, PROSPERO or OSF registration mentioned: 40 of 87 (46%), keyword-based and generous (an OSF mention for data counts).
- Repository link of any kind in non-reference text: 40 of 87 (46%; OSF dominates); **repository DOI (OSF 10.17605 x8, Zenodo 10.5281 x4, figshare x2, Mendeley Data x1): 12 of 87 (14%)**; GitHub or GitLab: 4. Data statements (n=94 by keyword): in article or supplement about 65%, "on reasonable request" about 18%, repository about 15%, restricted/confidential about 4% (categories overlap).
- Statement of AI use in writing: 25 of 94 (27%); 24 of 82 in 2024-26 (29%).
- Statistics keywords in methods/results/abstract (n=94; keyword hits, not validated): 95% CI 39%, p-values 40%, linear/mixed/Poisson-type regression 28%, OR/RR/HR 22%, chi-square/Fisher 21%, t-test/ANOVA 29%, named effect size (Cohen, Cliff, Cramer, SMD, eta) 20%, kappa/ICC 15%, bootstrap or sensitivity analysis 18%, logistic regression 12%, non-parametric 9%, multiplicity correction 7%, machine learning 5%, survival/Cox 4%, Bayesian 3%. Qualitative coding 21%, meta-analysis 30% (inflated: many audits mention "meta-analysis" as their subject). Any inferential or uncertainty statistic: 64 of 87 empirical papers (74%); audits 16 of 21; bibliographic studies 7 of 8; editorial-record studies 4 of 5; case series 1 of 5.

## 5. One-page style and level guide

**Titles.** Median 14.5 words (IQR 12-19; p90 22; range 8-26). 71% (67 of 94) use "finding or topic: a design label"; 9% are questions (8 of 94); 29% have no colon. Subtitle design words, in order: "study" (10), cross-sectional (8), analysis (6), scoping review (5), survey (4), randomised (4), systematic review (3), qualitative (3), case study (2), mixed methods (1), other descriptive subtitles (18). Retraction/editorial exemplars: "Identifying common patterns in journals that retracted papers from paper mills: a cross-sectional study"; "Retraction and correction of scientific articles due to conflicts of interest: a cross-sectional analysis of ..."; "Predicting retracted research: a dataset and machine learning approaches"; "Peer review trends in six fisheries science journals"; "Reviewer recommendations and editorial outcomes in peer review: a longitudinal analysis of agreement and disagreement ...". The count (a number) is in the title only occasionally ("a case study of 456 trials", "the 223 randomized controlled clinical trials", "six ... journals").

**Abstract.** Four headings (Background, Methods, Results, Conclusions), about 315 words (p90 390; the field never exceeds about 570). Background is 2-4 sentences (median 61 words). Methods names data source, dates and analysis method (69 words); Results are the longest (about 100 words); 47% of abstracts state the N explicitly; 71% quote percentages, usually as "n (%)"; only 13% give a CI, 15% a median with IQR, 13% a p-value, 14% a named effect size, Bayes factor, beta or correlation; 10% mention registration (PROSPERO/OSF). Conclusions (56 words) are cautious ("suggest", "may": 43%) and 46% end with a call or recommendation ("need", "should", "warrant"). Only 3% mention limitations in the abstract.

**Background states the gap in one sentence.** Pattern (3 steps, 40-60 words): (1) importance of the phenomenon; (2) a contrast sentence, "However ... evidence remains limited" (34% of backgrounds contain However/Yet/Despite; about 20% use an explicit gap phrase such as "remains limited", "lack of", "little is known", "unclear", "gap"); (3) an aim sentence, "This study aimed to characterise ..." (about 40% of abstract Backgrounds). Two real examples: "...However, manuscript-level evidence describing how reviewer disagreement unfolds across review rounds ... remains limited." (reviewer-recommendation paper) and "...yet empirical evidence on how often CoI lead to editorial action and how journals respond remains limited. This study aimed to characterise the frequency, patterns, and editorial handling of CoI-related notices ..." (CoI notices paper). The gap is usually a missing empirical description, not a missing theory.

**Limitations.** A named Limitations (or "Strengths and limitations") sub-section in about 80% of papers, median 240 words where present (IQR 127-434; p90 747). Structure: "Several limitations should be acknowledged. First, ... Second, ..." (24% of limitation sections). Content most often: generalisability (21%), strengths paired with limitations (29%), response/selection/self-report bias (16%), manual or single-person coding (16%). For retraction work the established wording concerns database coverage: results "depend directly on how journals decide and manage to retract" (paper-mill paper, 769 words of limitations), "stealth retractions", English-language skew, Retraction Watch incomplete coverage, retrospective data that cannot assess prospective use; a single-journal design is flagged as a generalisability limit (MDPI paper). Strength statements typically cite the open data source (Retraction Watch via Crossref) and manual verification.

**Effect-size and uncertainty reporting.** Descriptive proportions with counts ("n/N (%)") dominate, particularly in audits. When inferential, the dominant forms are adjusted odds ratios from logistic regression with 95% CI (journal-characteristic models), medians with IQR, correlation coefficients (r), standardised differences or Cliff's delta (for example delta = 0.126 in the image-duplication survey), Bayes factors (BF10 in the 223-RCT paper) and bootstrap CIs (CoI notices paper). Machine learning papers report accuracy, precision, recall, F1. Multiplicity correction is rare (7%). p-values appear in 40% of papers; pure descriptive papers are accepted (23 of 87 empirical papers, 26%, have no inferential or uncertainty statistic by keyword). Recommendation: report "n/N (%), 95% CI" for every headline proportion and an adjusted OR or rate ratio with CI for each association.

**Sections and apparatus.** Introduction or Background; Methods with data sources, dates, definitions, unit of analysis, Statistical analysis sub-section; Results with 3 tables and 2 figures; Discussion; Limitations; Conclusion. Declarations block with ethics (usually "not applicable" for database studies), competing interests, funding, authors' contributions, data availability.

## 6. "Artificial intelligence and research integrity" collection

Found through search only; the Springer/BMC collection page (link.springer.com/collections/eeehcjfdha) and the journal's collections list could not be opened (redirect to an authentication endpoint), so the wording below is **a search-result summary, not verified against the page**:

- Status open; submission deadline **30 January 2027**.
- Focus on responsible use of large language models by authors, reviewers and editors, including where assistance becomes inappropriate use; listed topics: AI-assisted literature review, authorship and accountability, detection and disclosure of inappropriate AI use, ethical risks in peer review.
- "All submissions welcome, preference for original articles with an empirical basis"; standard peer review.
- Guest editors and any word-limit or format rules: not found.
- In my corpus, papers that appear to belong to it include the AI-chatbot peer-review survey (1,077 respondents; 72,851 invited) and the concrete-ML reproducibility-assets audit (419 articles); 25 AI-tagged items have appeared since 2023, of which 19 in 2026. Empirical designs in that stream: surveys of editors/reviewers (510 and 1,077), policy audits (162 publishers; 230 journals), detector evaluations (120 manuscripts), LLM experiments (180 manuscripts x 4 models x 3 runs), bibliometric trend studies (2,770 abstracts; 993 comments; 780,000 letters).

Implication: a retraction-and-editorial-timing paper is outside this collection unless it analyses AI-related retractions or AI-assisted editorial handling; it competes in the general stream.

## 7. What a paper must look like to sit above the median (2024-2026 benchmark)

Targets, each stated against a median/upper quartile from section 4:

| Dimension | Median bar | Upper-quartile bar | Remarks |
|---|---|---|---|
| Analysis N (document-level meta-research) | 610 | 2,051 | Closest-comparator pool median 2,674; retraction/editorial-record studies in the pool run 886-16,006 |
| Main-text words | 5,100-5,200 | 6,500 | Pool median 4,900 is shorter; 2,400 has been published |
| References | 35-36 | 48-50 | Pool median 29; 14-17 appears |
| Tables / figures | 3 / 2 | 4 / 3 | |
| Abstract | structured B/M/R/C, 315 words | 355-360 words | state N, dates, data source, main estimate with CI |
| Limitations | named sub-section, about 200-240 words | about 430 words | include a strengths statement |
| Statistics | at least one inferential or uncertainty statistic (74% of empirical papers do) | adjusted OR/rate ratio with 95% CI, effect size, sensitivity/bootstrap analysis (about 20%) | |
| Registration | OSF/PROSPERO mention (46%) | pre-registered analysis plan | the 223-RCT paper is the only pool paper with OSF DOI plus pre-registration |
| Open data/code | availability statement with supplement (about 65%) | repository with DOI (14%) | pool: 2 of 15 declare a repository |
| Reporting guideline | named in 37% (STROBE, PRISMA, CHERRIES, RECORD) | | for retraction work, STROBE/RECORD plus a data-source description |
| AI-use statement | 27-29% | | include if any LLM assistance |
| Authors | 4-5 | 7-9 | |

Practical reading: a paper with several thousand retraction/notice records from Retraction Watch/Crossref plus journal or publisher metadata, an adjusted regression or time-to-event model with CIs, a pre-registered or OSF-deposited protocol, a DOI-bearing data and code repository, 5,000-6,500 words, 30-45 references, 3-4 tables and 2-3 figures, a four-heading abstract of about 320 words, and a 250-word limitations section about database coverage would be above the median on every measured dimension and above the closest comparators on the openness dimensions. No survival or time-to-event retraction analysis exists in the corpus (Cox/survival keywords in 4 of 94 papers, none about retraction latency, from keyword search), so it is also the least-crowded niche.

## 8. What I could not verify

- Journal-level facts: author instructions, abstract/word limits, article-type definitions, APC, impact factor, official decision times. Publisher pages are blocked; the 2023 volume count (15) looks low for a journal of this profile, so Crossref/Europe PMC may under-cover early records; I did not test this against another index.
- The collection details in section 6 rest on a single search result and could not be cross-checked on the page; guest editors unknown.
- All classification (design, source, N, topic, closeness) is single-coder from abstracts; N for 6 items came from full text; no N could be obtained for the IRIS framework paper, the Iranian unmatched-count survey, and the three recent items without abstracts (gender-retraction, observational-study registration, AI transparency statements). 11 recent items have no abstract in Crossref or Europe PMC (8 not yet in PMC): the gender-and-retraction paper's content comes from a bioRxiv search snippet (the full fetch returned HTTP 429), and the observational-study registration paper's from a Peer Review Congress abstract snippet; both are unverified as published.
- Europe PMC abstract text drops characters after "<" (for example "p < 0.05"); I used the XML abstract wherever XML exists (123 records), but p-value counts in abstracts for the records without XML are unreliable. The 17 records without XML are all from 2026-06-28 or later.
- Word counts exclude tables and captions and depend on my section filter; they are comparable across papers but will not match a manuscript word processor count exactly.
- Statistics, repository, pre-registration, guideline and AI-statement flags are keyword matches; no precision/recall was measured. "Meta-analysis" and "OSF" flags in particular over-count.
- Received/accepted dates exist for only 46 papers; no sampling check of whether they are representative.
- Citations are Crossref counts only; I did not compare against Scopus, Web of Science or Google Scholar.
- The claim that no paper analyses retraction latency rests on titles and abstracts of 128 items.
