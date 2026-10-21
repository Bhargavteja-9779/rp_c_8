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
