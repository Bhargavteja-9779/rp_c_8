# Selected journal — REVISED 2026-10-21 after topic selection
(The first version selected *J. King Saud Univ. CIS* for a machine-learning topic; that topic was abandoned (Gate C), so the selection was redone for the final topic: meta-research on journal turnaround. The superseded version is in git history.)

> **Status: TIMELINE NOT VERIFIED AS ≤ 72 DAYS — DOES NOT SATISFY THE HARD CONSTRAINT. JCR QUARTILE NOT VERIFIED (secondary sources only).**
> The target is "scope-appropriate, least-deviating among journals publishing peer-review / publication-process meta-research", chosen because no scope-appropriate journal satisfies the constraint.

## Primary target: *Accountability in Research: Policies and Quality Assurance* (Taylor & Francis)
| Field | Value | Verification |
|---|---|---|
| Publisher | Taylor & Francis (Routledge) | aggregator listing; to confirm on publisher site |
| ISSN | 0898-9621 (print); eISSN 1545-5815 | Crossref query by ISSN returned the journal |
| Scope | "examination and critical analysis of practices and systems for promoting integrity in the conduct of research" (interdisciplinary forum for ethics, procedures, standards, policies on research conduct) | secondary (search snippet); official aims & scope page **not retrieved** |
| Evidence that peer-review / publication-process studies are in scope | 2020–2026 articles retrieved from Crossref: e.g. *Author academic influence and manuscript acceptance: Evidence from peer review in Cell Press journals* (10.1080/08989621.2025.2521083); *On the (ab)use of special issues in scholarly journals* (10.1080/08989621.2024.2439434); *Characteristics of blacklisted journals* (10.1080/08989621.2022.2112953); *Cultural distance, gender and praise in peer review* (10.1080/08989621.2024.2409310) | Crossref records |
| JIF / JCR | aggregator: 2024 JIF 4.0; JCR "Medical Ethics" Q1 | **UNVERIFIED** (no Clarivate access) |
| Observed submission→acceptance | median 105.5 d, IQR 71–141, **27.4 % ≤ 72 d** (n=164 papers published ≥ 2024-01; Crossref assertions; survivorship-biased) | own sample `journal_selection/turnaround_samples_infosci.csv` |
| Publisher-reported timeline | not retrieved | – |
| APC / model | hybrid (subscription + OA option); APC not verified | to confirm |
| Data/code policy, length limits, reference style | **not retrieved** (publisher pages return 403) — must be read by the authors before formatting | – |

**Why this journal:** the only scope-appropriate venues examined are slow; this one has the shortest observed median (105 d) and a materially higher share (27 %) of papers accepted within 72 d than the alternatives, while publishing the same genre (bibliometric / meta-research on peer review).

## Alternatives (all non-compliant)
| Journal | Observed median (n) | % ≤72 d | Notes |
|---|---|---|---|
| *Research Integrity and Peer Review* (BMC / Springer Nature) | 133.5 d (104; Crossref) — **publisher-reported median 194 d** | 8.7 | Best scope match; journal page reports JIF 10.7 (2024); JCR Q1 per aggregator (unverified); APC up to €2,190 (DOAJ). Our own sample and the publisher figure disagree (itself an instance of the study's theme) |
| *Scientometrics* (Springer) | 204.5 d (296) | 5.7 | JCR (mirror): Information Science & Library Science Q1; CS Interdisciplinary Applications Q2; observed far from 72 d |
| *Learned Publishing* (Wiley) | 172.5 d (160) | 13.8 | scope fit moderate |
| *JASIST* (Wiley) | 238 d (229) | 3.5 | |
| *Quantitative Science Studies*, *J. Informetrics*, *Research Evaluation* | not measurable (dates not deposited) | – | **TIMELINE UNVERIFIED** |

## Principal rejection / timeline risks
1. Timeline: ≤ 72 d is not supported for any scope-appropriate journal; for the primary target only ~27 % of published papers meet it.
2. Editors may view a descriptive-plus-forecasting bibliometric study as incremental (see `review/`).
3. Quartile/IF unverified; scope statement unverified from the official page.
4. The publisher-defined meaning of "received" varies; some journals' dates look like re-submission dates (limitation stated in the manuscript).

Confidence in this selection: **low-to-moderate**.
