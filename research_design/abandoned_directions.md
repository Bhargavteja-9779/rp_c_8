# Abandoned directions (audit trail)

## A. Duplicate / near-duplicate contamination in tabular ML benchmarks (abandoned 2026-10-20, Gate C failure)
* Initially selected (see `candidate_directions.md`, #4) because early searches found no measurement on OpenML/UCI.
* A deeper novelty search found a directly overlapping public preprint dated 2026-10-03 — *"Rows Are Not Samples: Duplicate Records, Evaluation Bias, and Ranking Distortion in Standard Tabular Benchmarks"* (H. Li, Zenodo record 23119065; not peer-reviewed) — which audits 156 datasets from two OpenML suites plus UCI, measures random-vs-duplicate-aware protocol gaps by model family, and reports leader changes; plus arXiv 2604.04199 (leakage types across 2,047 datasets) and TabReD (temporal-split effects). The planned contribution would have been incremental.
* A partial feasibility script (`code/archive_abandoned_direction/feasibility_scan.py`) was started to count duplicates in OpenML-CC18; it was **killed before completion and produced no output file**. No model performance was ever computed for this direction.

## B. ICC-based prediction of record-wise CV optimism; conformal coverage under subject shift
Rejected after searches showed 2026 preprints already covering both (arXiv 2607.10634; a 2026 medRxiv simulation; EEG personalised conformal calibration preprint).

## C. Prequential code-length as split-free tabular evaluation; hidden row-order non-exchangeability
Not pursued: related ICML-2025 TabPFN-description-length work and arXiv 2604.04199 (temporal/row-order leakage) reduce headroom; no experiments run.
