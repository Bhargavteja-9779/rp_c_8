# Research problem, questions and contributions

## Central problem
Authors choose journals partly on stated or hearsay turnaround ("fast journal", "median 60 days"). Whether *past turnaround of a journal* is a usable, calibrated forecast of *the turnaround a newly submitted paper will experience* is untested out-of-time. Existing studies (Björk & Solomon 2013; Himmelstein 2015 blog; Huisman & Smits 2017; Argilés-Bosch 2023; a registered PubMed-wide descriptive study on MetaROR) are descriptive/associational; none (that I could find; see `literature_review/novelty_map.md`) evaluates journal-level turnaround statistics as **forecasts** under a realistic information set, measures how much of the article-level variance journals actually explain, or quantifies how far "≤ T-day" guarantees are from what past data support.

## Estimand
For a manuscript submitted to journal *j* at time *s* and eventually accepted, D = (acceptance date − original submission date) in calendar days, **conditional on acceptance** (rejected/withdrawn papers are unobservable in publisher-deposited metadata).

## Research questions
* **RQ1 (variance structure)** How much of the variance of log D lies between journals, between years within journals, and within journal-years (residual)?
* **RQ2 (out-of-time forecast accuracy and calibration)** If an author forecasts the distribution of D for a paper submitted in the next six months using only the journal's visible, already-published papers, how accurate and calibrated is the forecast, and which estimator is best (empirical, longer window, time-decay, parametric, hierarchical shrinkage, recent-holdout adjustment)?
* **RQ3 (drift)** How large is temporal drift in journal turnaround between consecutive years relative to sampling noise, and does drift explain forecast miscalibration?
* **RQ4 (guarantee feasibility)** For T = 72 days (and other T), what share of journals have a past-supported P(D ≤ T) ≥ 0.5/0.8/0.9, and how reliable are such past-based probability forecasts out-of-time?
* **RQ5 (article-level information)** Do pre-submission-observable article features (author count, submission month/weekday) improve forecasts beyond the journal-level forecast?

## Contributions (each tied to an experiment)
1. A reproducible, openly derived article-level dataset of dated submission→acceptance records for a frame of ~800 journals (E1 data audit; E2 variance decomposition).
2. A realistic out-of-time forecasting protocol (visibility rule, cohort definition) and benchmark of six forecasters with proper scoring rules (E3, E4).
3. Quantification of drift and of guarantee feasibility (E5, E6).
4. A negative/positive finding on article-level covariates (E7).
5. Cross-source validation of publisher-deposited dates (Crossref vs PubMed) and external validation on non-frame publishers (E8, E9).

No claim of a new theory is made. This is an empirical meta-research contribution; its value rests on scale, design realism and honest uncertainty.
