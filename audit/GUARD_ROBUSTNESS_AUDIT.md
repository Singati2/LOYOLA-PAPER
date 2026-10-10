# Guard robustness audit (boiling-point tests)

Scripts: `audit/guard_robustness_audit.py` (about 1 hour), then `audit/guard_robustness_causes.py`.
The manuscript is unchanged.

## Guards compared
- Guard 1, degeneracy (`external/baselines.py`): old = `is_constant` or relative range below 1e-9;
  corrected = `is_constant` only.
- Guard 2, rank (`external/bp/bp_tests.py`, `press_size`): old = `|det(A'A)| > 1e-9 max|A'A|^3`
  with raw n_C; corrected = n_C centred and scaled, full rank by singular values
  (smallest/largest > 1e-10).

## Results
- Outer folds compared: 26,800 (50 seeds, streams GM2/LO2/GM12/LOh, Tests A and B).
- Folds with a different selected candidate: 101, all in Test B, stream LO2
  (seed 32: 100 folds, seed 13: 1 fold). No difference in Test A or in GM2, GM12, LOh.
- Cause: in all 101 the old rank guard rejected the candidate the corrected guard selects.
  Correcting guard 2 alone reproduces every corrected choice; correcting guard 1 alone
  changes none. No difference is a near-tie or a rounding effect.
- Stable reference (inner-LOO RMSE by explicit `numpy.linalg.lstsq` refits): prefers the
  corrected choice in 101 of 101, relative RMSE gap median 0.130, max 0.147.
- Effect: Q2 of LO2 seed 32 rises from 0.9787 to 0.9851, seed 13 from 0.98186 to 0.98217;
  median LO2 Q2 0.97998 to 0.98001. Only 2 of 400 seed/stream runs change any prediction.

## Table 5 and decisions, old vs corrected (identical)
| Test | GM | LO_h | median dQ2 | LO_h ahead | 95% CI | narrow box GM / LO | decision |
|---|---|---|---|---|---|---|---|
| A | 0.514 | 0.406 | -0.072 | 15/50 | [-0.156, +0.001] | 0.469 / 0.465 | no evidence |
| B | 0.977 | 0.977 | -0.000 | 25/50 | [-0.003, +0.002] | 0.976 / 0.980 | no evidence |

These agree with Table 5 of the manuscript. The pre-registered rule (LO_h ahead in at least
40 of 50 seeds and the interval excluding 0) fails in both tests under both guards.

## Files
`guard_robustness_audit_out.txt`, `guard_robustness_diffs.csv` (every differing fold with
old/new scores), `guard_robustness_predictions.npz` (all old and corrected outer predictions),
`guard_robustness_causes_out.txt`, `guard_robustness_causes.csv`.
