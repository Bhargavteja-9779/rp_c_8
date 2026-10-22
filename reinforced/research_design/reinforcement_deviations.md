# Cycle-2 deviations and order-of-events log
| ID | Event | Note |
|---|---|---|
| C2-1 | X1 probe first run used Crossref `sample` with `rows`, which Crossref rejects (HTTP 400): zero data; relaunched without `sample` | infrastructure |
| C2-2 | X1 probe was interrupted by a worker restart after ≈6,800 records; analysis uses the incrementally written partial file (388 journals, random order of journals, first 30 linked articles per journal) | sample is partial and not random within journal |
| C2-3 | X1 pre-set threshold "≥70 % of Research Square articles within ±14 d" was mis-specified (In Review preprints post ≈2 weeks *after* receipt; observed 45 %); the analysis reports the more informative share received ≤ posted+14 d (91 %) and received > posted+90 d (4.8 %), flagged as post-hoc | honest failure of the stated threshold |
| C2-4 | X2/X3 run once with design fixed in code; protocol text written afterwards | see `revised_experimental_protocol.md` |
| C2-5 | X4–X6 and Y0–Y5 specified (committed) before running; Y-experiments responded to agent DEF | commits af19c71 and following |
| C2-6 | Y1 recalibration evaluable only for three origins (maps require targets complete at t0) | design limitation |
| C2-7 | Y2(a) permutation null from the protocol was not run (judged uninformative); (b), (c) run | deviation |
| C2-8 | Y3/Y4/Y5 run once as specified | — |
| C2-9 | Part C experiments Z1–Z6 specified and committed (protocol Part C) after the second adversarial review and before running; `z_experiments.py` was run once, then the manuscript text was rewritten around its output | the rewrite followed the results; the σ²-based account was chosen because Z1 matched the magnitude, so its explanatory weight is limited |
| C2-10 | Z2 evaluates only three origins (October 2023–April 2024) with a 480-day cap; maps use only targets complete at the origin | design limitation of any strictly out-of-time recalibration with this horizon |
| C2-11 | Z1 uses σ² = journal×year component estimated from the same data; the journal-specific σ² proxy also uses the same data | circularity disclosed in Results and Limitations |
| C2-12 | Numbers of X2/X6 (look-ahead variant) retained in `cal_meta_summary.json` and `X4_X5_X6_summary.json` but demoted in the manuscript | preserved, not deleted |
| C2-13 | `cal_and_meta.py` (X2/X3/X6) and Y4 used training cohorts defined by *received* date, with labels whenever accepted (data to 2026-10): 0.94–3.1 % of labels of the training cohorts were accepted after the test origin; the 2025 target cohort was censored | found by second adversarial review and independent reproducibility audit; X2/X6 demoted to "look-ahead variant"; strict re-analysis Z2 |
| C2-14 | the X1 probe was started before the protocol text but its first run returned no data (C2-1); the data come from a relaunch with edited code (rows 60 → 30, `sample` removed, shuffled, incremental writes, 8 threads) whose output was written 20–30 minutes after the protocol commit, i.e. X1 ran at least twice and its data were collected after the protocol text | corrects the earlier "designed in code and run once" statement; `reinforcement_plan.md` was written after Y0–Y5 outputs and is retrospective |
| C2-15 | Y3/Y4 bootstrap draws were 2,000/3,000, not 5,000; Y5 is a LightGBM model with an extra feature; Y2 used n_test ≥ 50 | C2-8 ("run once as specified") is accurate only for the number of runs |
| C2-16 | C2-3 reports all-publisher Research Square figures (45 %, 91 %, 4.8 %); the manuscript restricts to Springer Nature (47 %, 95 %, 2.6 %) after seeing that Wiley and Taylor & Francis fail; the restriction is post hoc | stated in the manuscript as untestable elsewhere |
