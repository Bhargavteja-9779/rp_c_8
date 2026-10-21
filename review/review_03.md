# Review 03 — Experimental design and statistics
*Mode: simulated pass. Not an external or human review.*

**[MAJOR]** Clopper–Pearson intervals for the share of journal-origins treat the two origins of a journal as independent; CI too narrow.
- Evidence: results/guarantee_feasibility.csv
- Corrective action: Computed journal-cluster bootstrap CI (post-hoc D6): 9.9–14.2 % for ≥0.5, 0.9–2.4 % for ≥0.8; report it in the paper (to do in revision).

**[MODERATE]** Pre-registered thresholds (±3 pts, 5 %, 2 %) were arbitrary; H2 failed by a CI straddling −3.0.
- Evidence: hypotheses.md
- Corrective action: Already reported honestly; add sentence that the thresholds were judgement calls (present).

**[MODERATE]** PIT histogram pooled over journal-origins ignores dependence; no CI.
- Evidence: Fig 4
- Corrective action: Describe as descriptive; add caution.

**[MODERATE]** Manuscript says 5,000 bootstrap resamples overall but variance-component CI used 1,000 and E7 2,000.
- Evidence: code/src/tdelay/experiments.py
- Corrective action: Correct Methods text (revision).

**[MINOR]** Wilcoxon on journal-averaged losses is appropriate, but effect sizes are tiny (≈0.2 % relative) and statistically-significant ordering of F0/F1/F3/F4/F6 has little practical meaning.
- Evidence: Table 2
- Corrective action: Already noted in limitations.
