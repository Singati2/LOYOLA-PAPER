# Pre-registration template: measured external dHvap test (not yet run)

To be completed, committed and time-stamped BEFORE any value of the new
dataset is collected. Nothing in this file has been executed.

## Dataset (fix before collection)
- Population: acyclic alkanes C_a..C_b (state the range and why), all
  constitutional isomers or a stated subset chosen by a rule independent of
  the properties.
- Inclusion: only calorimetric (or directly measured) standard vaporization
  enthalpies at 298.15 K from primary sources; compilation, estimated or
  group-additivity values excluded. Record per value: source, method,
  temperature, uncertainty, conversion.
- Minimum size: n >= 40 measured values (state the number expected); if fewer
  are found, report the shortfall and do not run the confirmatory test.
- No overlap with the octane development set; isomers of any size used in
  development listed and excluded.

## Models and baselines (fixed)
Training-fold mean; best classical index; IRLA; ridge on degree-pair counts
(penalty by inner LOO); GM and LO random search (seeds 0..99, budgets 200 and
500, candidate stream as in the v37 analysis); and the frozen-parameter
transfer of the octane-selected LO/GM directions with recalibration.

## Evaluation (fixed)
- Outer leave-one-out (or grouped by carbon number if several sizes are
  pooled), all selection inside training folds.
- Primary contrast: dQ2 = Q2_LO - Q2_GM (median over seeds).
- Uncertainty: paired bootstrap over molecules (B = 2000) with model
  selection repeated inside every resample (full nested bootstrap), giving a
  95% interval for the primary contrast and for LO - ridge.
- Confirmation rule: LO better in >= 80/100 seeds at both budgets AND the 95%
  interval for dQ2 excludes 0. Report LO - ridge whatever its sign.

## Reporting
All outcomes reported, including null or negative ones; any deviation
recorded with its date and reason before the affected analysis is run.
