# Review 06 — Baselines and fairness
*Mode: simulated pass. Not an external or human review.*

**[MODERATE]** No stronger baseline such as quantile regression on journal-level features (trend, size, publisher) or a simple 'last year's median × inflation factor'; F0 is effectively the naive baseline.
- Evidence: Table 2
- Corrective action: Add as limitation; optional extra experiment (OPEN).

**[MINOR]** F2 pools within publisher; a global pool might be a fairer 'no-information' baseline.
- Evidence: protocol §6
- Corrective action: Acknowledge.

**[INFO]** All forecasters share the same visible set, windows and targets; no tuning on targets (half-life, windows fixed).
- Evidence: protocol
- Corrective action: –
