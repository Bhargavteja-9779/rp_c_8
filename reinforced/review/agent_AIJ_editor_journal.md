# Editor / journal-fit review (Reviewers A, I, J) — 2026-10-21

Scope: manuscript/Final_Manuscript.docx vs. *Research Integrity and Peer Review* (RIPR, BMC/Springer Nature) and alternatives. No existing file was modified. "R" = retrieved fact; "J" = my judgement.

Tool caveat: WebFetch summarises pages with a small model, so quotes below are from its output and may be trimmed. The Springer Link pages only opened after a manual idp.springer.com cookie redirect; the old BMC URLs now 301 to Springer Link. Nothing was read from JCR/Clarivate. Aggregator figures (journalmetrics.org, Peeref, SciJournal, Researcher.Life) are secondary and often disagree with each other.

---

## 1. RIPR official instructions (retrieved 2026-10-21)

**Aims and scope (R, link.springer.com/journal/41073/aims-and-scope):** "an international, open access, peer reviewed journal that encompasses all aspects of integrity in research publication"; "Particular consideration is given to submissions that address current controversies and limitations in the field and offer potential solutions"; "We welcome research into peer review and editorial decision making, [but] reports of individual journal or publisher decisions or actions will not be considered." Peer-review scope: "research into the peer review of articles for publication (by journals), or presentation (by conferences), and the peer review of grant proposals by funders." Research reporting: interventions to improve completeness/accuracy of reports, reporting guidelines, publication bias, selective reporting. Not found: any explicit exclusion of "descriptive bibliometrics" or of turnaround/publication-delay studies (the page was searched; the only exclusion is individual journal/publisher decisions).

**Article types (R, /submission-guidelines):** Research, Methodology, Review, Comment, Correspondence, Study protocol, Matters Arising.

**Research and Methodology pages (R, /submission-guidelines/research, /methodology):**
- Abstract: max 350 words; "Background, Methods, Results, Conclusions" (plus Trial registration for health-care interventions); no references in abstract, minimal abbreviations.
- Research article: "should stay under 5,000 words" (encouraged, not a hard cap). Methodology: no word limit stated; must describe a "demonstrable advance" over existing methods and be "well tested".
- Body order: Background, Methods, Results, Discussion, **Limitations (explicit section between Discussion and Conclusions)**, Conclusions; keywords 3–10; list of abbreviations if used.
- References: **Vancouver style**; journal abbreviations per Index Medicus/MEDLINE.
- Declarations (mandatory; "Not applicable" if inapplicable): Ethics approval and consent to participate; Consent for publication; Availability of data and materials; Competing interests; Funding; Authors' contributions; Acknowledgements; Authors' information (optional).
- Data: "Availability of data and materials" required for all manuscripts; deposit in public repository with persistent identifier encouraged; software needs name, home page, archived version DOI, licence.
- Reporting guidelines: CONSORT for RCTs; otherwise "CHERRIES, PRISMA, STROBE, and others" via EQUATOR; checklists are "an aid ... not a criterion for publication decisions".
- LLMs: "cannot be authors. Any LLM use must be documented in the Methods section."
- Peer review: "transparent peer review"; reviewer reports published with the article (CC BY 4.0), reviewers unnamed. Usually two or more reviewers assessing "scientific robustness, originality, and clarity".
- Preprints: no dedicated policy found; page says preprints "may be cited".
- APC: £1,990 / US$2,590 / €2,190 (+VAT); waivers for lowest-income countries. Licence CC BY(-NC-ND) 4.0.
- Not retrieved: any desk-rejection/pre-screening policy (page says nothing), a statement on AI-use beyond the above, the BMC editorial-policies page, and the submission system.

**Metrics (R):** Springer Link journal page: JIF "9.6 (2025)", 5-year "9.9 (2025)", submission to first decision "10 days" (median); **submission-to-acceptance is not listed there**. The pre-migration BMC page (via search snippet, not re-fetched): JIF 10.7 (2024), 5-year 11.0, first decision 8 days, **submission to acceptance median 194 days**; indexed ESCI/PubMed/PMC/DOAJ. So journal-reported JIF is internally inconsistent across two pages (10.7 vs 9.6) and neither is JCR-verified.

**JCR quartile (R/J):** I found **no** Clarivate JCR category or quartile for RIPR. The "Q1" in journalmetrics.org is computed from OpenAlex mean citedness ("Journal Metrics Score 2.5"), not JCR; the repo's phrase "aggregator lists Q1" must not be read as JCR Q1. Status: **UNVERIFIED — do not state Q1.**

---

## 2. Timeline evidence and comparable articles

**Own re-sample (Crossref, run today, ISSN 2058-8615, 97 research-type items published 2024-06 to 2026-10, received/accepted assertions):** median **132 d** (IQR 99–178; range 3–406); **8.2% (8/97) ≤72 d**. PubMed History dates (n=60, 2025-06 onward): median 141 d, 5.0% ≤72 d. Repo sample (n=104): 133.5 d, 8.7%. Official 194 d (BMC page) is consistent only if long-tail items dominate. **72-day verdict: NOT MET** (published-paper median already 1.8x the limit; selection-biased toward accepted papers).

**Recent RIPR papers (existence verified in Crossref with DOI, received/accepted dates; abstracts read from the Crossref abstract field, first ~1,100 characters only; full texts not read):**

| # | DOI / title (short) | Design and size (from abstract) |
|---|---|---|
| 1 | 10.1186/s41073-026-00252-9 Linguistic inequity in philosophy | 103,595 articles, 223 journals, 1975–2021; automated classifiers (accuracy >89%) |
| 2 | 10.1186/s41073-026-00257-4 AI-generated text in Lancet Regional Health comments | full corpus 993 comments; detector validated on 50 controls |
| 3 | 10.1186/s41073-026-00248-5 Do data availability statements increase sharing? | 1,400 randomly selected oceanography articles (200/yr 2018–24); corresponding authors contacted |
| 4 | 10.1186/s41073-026-00229-8 Why researchers cut corners (QRPs) | survey N=3,050 of 18,376 invited |
| 5 | 10.1186/s41073-026-00234-x IHU-Mi ethics approvals follow-up | 2,674 publications assessed against regulations |
| 6 | 10.1186/s41073-026-00246-7 Distributed peer review trial | 140 proposals, 323 applicant-reviewers, mixed methods |
| 7 | 10.1186/s41073-024-00146-8 Peer review trends in six fisheries journals | **6,606 manuscripts (2011–21) from editorial-system records**: review times, invitations, rejection by blinding |
| 8 | 10.1186/s41073-026-00259-2 Robot pen pals (letters to the editor) | >780,000 letter records |

(Titles of 10.1186/s41073-026-00238-7 on predatory-journal acceptance and 00254-7 on retraction gender imbalance exist; their Crossref abstracts were empty, so not assessed.)

**Comparison (J):** On sample size and statistical machinery this manuscript (1,737,272 articles, 800 journals, 298,469 scored papers, pre-specified contrasts, cluster bootstrap, proper scoring) **exceeds** every comparator; sample size is not a rejection ground. What differs: every RIPR comparator addresses an integrity, ethics, reporting, AI-misuse or peer-review-behaviour question. The closest (#7) uses editorial-system records including rejected manuscripts and reviewer behaviour; this manuscript uses only publisher-deposited dates of accepted papers and observes no peer-review process, reviewer, rejection or misconduct. I found no RIPR article on journal turnaround forecasting (Crossref searches: "turnaround time peer review", "time to acceptance publication delay", "submission to acceptance" returned only #7, an ecology reviewer-availability paper from 2016, and tangential items).

---

## 3. Desk-rejection simulation (strongest evidence-based reasons)

**Reviewer A (hostile editor):**
1. **Scope (strongest).** RIPR covers "integrity in research publication". Forecasting calendar days from received to accepted is metadata benchmarking; the manuscript's own text states it "makes no causal claims", has no integrity, ethics, reporting-quality or reviewer-behaviour variable, and conditions on acceptance. It is a scientometrics paper (Scientometrics/QSS/JOI audience). The scope clause "research into peer review and editorial decision making" arguably admits it, but the paper never measures peer review.
2. **The motivating use case is the project's, not the literature's.** The "72-day" framing arises from an external brief ("evaluative or funder policies sometimes require a stated maximum time"), supported by no citation. Reviewers will ask who uses it.
3. **Weak positive result.** Four of five pre-specified hypotheses unsupported (H2 borderline by rule; H3, H4, H5 not supported); the headline is that simple empirical quantiles are not beaten; article-level gain 1.4–3.4%. A "demonstrable advance" is not shown (Methodology type) and "originality" (stated reviewer criterion) rests on an unsystematic search (manuscript: "full texts of most prior studies could not be read").
4. **Data validity.** Publisher-defined "received" dates are unverified; some journals show 10–30 day medians likely reflecting resubmission; Crossref–PubMed agreement is not independent. This also bites RIPR itself: official 194 d vs. Crossref 132 d.
5. **Survivorship.** Rejected/withdrawn papers are invisible, so the paper cannot say how long a submission takes, which is what authors want.
6. **Format non-compliance (fixable, but signals unreadiness).** Author-year citations instead of Vancouver; Limitations inside 4.1 not a separate section; no list of abbreviations; Declarations lack Acknowledgements, Authors' information; Funding/Competing interests/Contributions are placeholders; AI-assistance disclosed in Declarations not Methods; authors/affiliations missing; data "private repository ... Zenodo NOT yet made"; title page says the target was "chosen by the author for impact factor; timeline and format requirements unverified" (must be removed; reads as an impact-factor-driven submission).
7. Transparent peer review will publish reviewer reports, including any criticism that the paper is out of scope.

**Reviewer I (RIPR associate editor):** Would return a scope-fit query ("what integrity or peer-review question does this answer?") and likely reject without review unless the cover letter re-frames around reporting of editorial-process statistics (publishers' "average days to acceptance" claims) as a reporting-integrity issue. The paper's discussion sentence on publishers stating cohort, desk-rejection inclusion and quantiles is the only link and is one paragraph. Probability of passing triage: my judgement is lower than 50%; I cannot quantify it.

**Reviewer J (final committee) — strongest rejection argument:** The journal was chosen for impact factor, as the title page admits, not for scope; the only JIF evidence is journal-reported and contradictory (10.7 vs 9.6), no JCR quartile is verified, and observed time to acceptance (median 132 d, 8% ≤72 d; official 194 d) fails the project's ≤72-day brief by a wide margin. The scope clause that RIPR "will not consider" individual-journal decisions or actions is dangerously close: the manuscript's headline findings include named-journal observations about turnaround, and the paper's contribution (calibration of journal-level statistics) is of interest to scientometrics, not to research-integrity readers. A comparable RIPR author would have reviewer or editorial data, not accepted-paper date stamps. Its four unsupported hypotheses, borderline H2 and exploratory post hoc diagnostics make it a negative-result methods note. The waiver does not repair the fit problem; it only removes a constraint. **The journal should not be retained as primary target in its current form.**

---

## 4. Alternative journals (72-day constraint = submission to FINAL ACCEPTANCE ≤72 d)

Own samples (today): Crossref assertions for papers published from 2025-06 unless noted; "—" = dates not deposited (0 of N records had both). Sampling is survivorship-biased and cannot prove a guarantee.

| Journal (publisher) | JCR / IF (source, secondary unless stated) | Timeline evidence | Scope fit (J) | 72-d verdict |
|---|---|---|---|---|
| *Quantitative Science Studies* (MIT Press) | ISLS Q1; IF 3.5 vs 5.6 (journalmetrics.org, conflicting labels; unverified in JCR); APC US$800 (Researcher.Life) | No Crossref dates (0/69); no official figure found | Excellent | **UNVERIFIED** |
| *Journal of Informetrics* (Elsevier) | IF 3.5 (2024), 3.9 (2025) per journalmetrics/bioxbio; SciJournal 4.5 (conflict); quartile not retrieved | Elsevier page via snippet: first decision 7 d, **submission to acceptance 246 d** (2024-dated page); no Crossref dates | Excellent | **NOT MET** (publisher-reported) |
| *Scientometrics* (Springer) | Springer page via snippet: JIF 3.5, 5-y 3.8 (2023); ISLS Q1 per mirror (repo; unverified) | First decision 19 d (publisher); Crossref n=291: median 229 d, 2.7% ≤72 | Very good | **NOT MET** |
| *JASIST* (Wiley) | ISLS Q1 (Peeref JCR-2024 mirror); IF 4.3 vs 6.85 conflict | Crossref n=105: median 223 d, 2.9% ≤72 | Good | **NOT MET** |
| *Research Evaluation* (OUP) | ISLS Q2; IF 2.7 (journalmetrics) | No Crossref dates (0/62); no official figure | Good | **UNVERIFIED** (Q2) |
| *Learned Publishing* (Wiley/ALPSP) | Q2; IF 2.4 (journalmetrics; SciJournal 4.29 outlier) | Crossref n=78: median 204 d, 10.3% ≤72 | Moderate | **NOT MET** |
| *PLOS ONE* (PLOS) | IF 2.6–2.8, Q2 (conflicting) | PLOS metrics page via snippet: first decision 32 d, time to publication 209 d (2025; alignment uncertain); PubMed n=238: median 160 d, 6.7% ≤72 | Weak-moderate (generalist) | **NOT MET** |
| *Accountability in Research* (T&F) | Medical Ethics Q1; IF ~4.0 (aggregator; unverified) | Crossref n=78: median 118 d, 23.1% ≤72 (repo n=164: 105.5 d, 27.4%); official figure not retrieved | Moderate-good | **NOT MET** (median >72 d) |
| *eLife* | Clarivate excluded it from JIF after the 2024 SCIE hold (eLife statement via search); reviewed-preprint model has no accept decision | PubMed dates unusable (n=1) | Poor | **NOT APPLICABLE / UNVERIFIED** |
| *J. Data and Information Science* | ISLS Q2, ESCI (journalmetrics); IF 2.7 vs 2.93 | No Crossref dates (0/75) | Good | **UNVERIFIED** (Q2) |
| *Frontiers in Research Metrics and Analytics* (Frontiers) | ISLS Q2, ESCI, IF 3.1 (journalmetrics) vs 2.8 (SciJournal) vs 1.6 (Frontiers page) | PubMed History n=126: **median 77 d**, 40.5% ≤72 d | Good | **NOT MET** by median (closest, still above 72); Q2 only |
| *Journal of Documentation* (Emerald) | ISLS Q2; IF 1.8 (journalmetrics) | No Crossref dates (0/220) | Moderate | **UNVERIFIED** (Q2) |
| *Royal Society Open Science* | not checked | Crossref n=96: median 120 d, 24.0% ≤72 | Moderate (meta-research welcome; not verified) | **NOT MET** |
| *PeerJ* | not checked | PubMed n=249: median 165 d, 5.2% ≤72 | Weak | **NOT MET** |

Cross-check with the manuscript's own finding: fast (≤72 d) journals exist only in chemistry/materials/physics/clinical medicine; "none was a computing, information-science or meta-research journal". My samples are consistent with that.

**Result (J): no scope-appropriate journal reaches VERIFIED.** Journals with deposited dates are all NOT MET; journals with the best scope (QSS, Research Evaluation, JDIS, Journal of Documentation) cannot be measured and so remain UNVERIFIED. No official statement of submission-to-acceptance ≤72 d was found for any candidate. JCR placement could not be verified for any candidate; do not print any quartile in the cover letter.

---

## 5. Recommendation

**NO VERIFIED JOURNAL MATCH** (against the brief: ≤72 d to final acceptance, JCR Q1 preferred, non-MDPI). RIPR specifically is rejected as a primary target on current evidence: the 72-day constraint is NOT MET (observed median 132 d; official 194 d), JCR quartile is unverified, impact-factor figures are inconsistent (10.7 vs 9.6), and the scope fit is the weakest link. The author's waiver for impact factor is recorded as a waiver, not compliance.

Conditional guidance (J), if the author keeps the waiver and wants a journal anyway:
1. Better scope than RIPR: *Quantitative Science Studies* (Q1 by aggregator; timeline UNVERIFIED) then *Journal of Informetrics* / *Scientometrics* (Q1-class by aggregators, but 246 d and 229 d). Choosing QSS gives up the headline JIF of RIPR but not on the ground of fit.
2. If RIPR is still preferred, it must be treated as a gamble: remove the title-page remark about impact-factor selection; re-frame explicitly around reporting/meta-research of editorial-process statistics; convert to BMC format (Vancouver, separate Limitations, abbreviations, full Declarations, LLM use in Methods); deposit data and code in a public archive before submission; ask the editor for a pre-submission scope enquiry. This is the only form of "RETAIN AFTER REINFORCEMENT" I could defend, and the label does not apply because the constraint failure remains.
3. Faster fallback with partial scope fit: *Accountability in Research* (median 105–118 d; ~23–27% of papers ≤72 d) — still NOT MET.

Open items I could not close: the official RIPR submission-to-acceptance figure on the current Springer Link site; any Clarivate JCR record for any journal; official timelines for QSS, Research Evaluation, JDIS, Journal of Documentation, Accountability in Research; full texts of the eight comparator articles.
