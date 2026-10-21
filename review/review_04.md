# Review 04 — Methodology and implementation
*Mode: simulated pass. Not an external or human review.*

**[MODERATE]** EB forecaster F4 shrinks log-SD using a normal-theory sampling variance 1/(2(n−1)), wrong for heavy-tailed data (excess kurtosis ≈2.1); shrinkage may be mis-calibrated.
- Evidence: forecasters.py EBPrior
- Corrective action: Acknowledge; F4 is a baseline not a proposed method; heavy-tail-robust variants not explored (limitation).

**[MODERATE]** Drift permutation null uses only 200 permutations per pair.
- Evidence: experiments.drift_analysis
- Corrective action: Variance ratio (7.3) is far from 1.5 threshold so conclusion robust; note.

**[MINOR]** E7 imputes missing n_refs/n_authors with medians.
- Evidence: experiments.article_level_experiment
- Corrective action: Report share missing (not done).

**[INFO]** Unit tests cover scoring, visibility assertions, calibration under iid lognormal, drift detection, variance-component recovery, cleaning.
- Evidence: tests/test_tdelay.py
- Corrective action: –
