# Cycle 3: adversarial review of the methods paper and what was done

Reviewer: `agent_R4_methods_paper.md` (separately launched instance of the same model family; 13 findings). Numbers in Tables 1–5 and the Results prose matched the result files; the criticisms concerned over-claiming, design status and robustness. New post hoc analyses (labelled exploratory) are in `code/src/d_extras.py` → `results/D_extras_EXPLORATORY.json`; the external run at cap 365 is `results/D_external_summary_cap365.json`.

| # | Finding (severity) | Response |
|---|---|---|
| 1 | "calibrated"/"consistent improvement" unsupported: T&F +2.05 vs HD3 band; CV0 beats F0 at 42 %, ties 20 %, loses 38 % of journal-origins; only 80 % interval checked (MAJOR) | confirmed by recomputation; abstract, Results, Discussion, Conclusions reworded; per-publisher and win/tie/loss reported; Limitations state only the 80 % interval was assessed |
| 2 | D-A2 compromises confirmatory status (MAJOR) | accepted: manuscript now says hypotheses are pre-specified, the cap is a post-hoc design choice made after seeing cap-365 outcomes and after using cap 480 in an earlier cycle; both caps co-primary; "confirmed" only where both agree; HD6 now also run at cap 365 |
| 3 | HD5 uninterpretable (MAJOR) | accepted: criterion called lenient, sign depends on cap, conflation with definition mismatch/truncation stated; mechanism "not established" |
| 4 | external result driven by five outlier journals; "frozen" mislabelled (MAJOR) | confirmed: excluding the five journals CV0 − F0 −0.32 [−0.68, +0.05], CV0 − V −0.17 [−0.43, +0.10] (post hoc); at cap 365 CV0 beats F0 and V (−0.63, −0.49, CIs exclude 0); text and abstract state both; "frozen" replaced by "learned on the frame only" |
| 5 | noise floor is only a lower bound (MODERATE) | exchangeable-null simulation: 4.45 points (binomial lower bound 3.6); excess-error share recomputed (16 %) |
| 6 | ACI effectively F0; F6 beats CV0 on loss; no τ = 0 ablation (MODERATE) | ACI explanation corrected (tiny steps); F6 comparison reported; ablation: τ² = 0 gives F0-like coverage (−2.5), constant τ² equals publisher-specific τ² |
| 7 | cap sensitivity clips both; "none" censored; no CI on bias (MODERATE) | caveats added; bias given as approximate with overlapping intervals |
| 8 | inference (nested imprints, Holm, block bootstrap, tiny p) (MODERATE) | caveats added to Limitations; p printed as <0.001 |
| 9 | "Brier" is MSE vs realised share; slope errors-in-variables; "CVb lowest" false at 180 d (MODERATE) | renamed Brier-type; CIs added (all exclude 0); statement corrected |
| 10 | mixed designs in abstract (MODERATE) | abstract separates the two-origin benchmark from the strict six-origin results |
| 11–13 | label "strictly out-of-time"; paper-weighted vs journal-average; wrong phrase attachments; 9–12 % vs 12.5 %; docstring; shipped global τ² (MINOR) | limitation on strictness added; paper-weighted values reported; wording and docstring fixed; "9–13 %"; shipped tool uses global τ² and the text says so |

Not done: a combination of CV0 with time decay, other conformal-under-shift methods, calibration of other quantile levels, and an independent human review.
