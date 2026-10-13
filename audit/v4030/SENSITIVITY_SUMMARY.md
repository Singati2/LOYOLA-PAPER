# Source-quality sensitivity audit (v40.30; exploratory, not pre-registered)

Frozen commit `01ad6c6`. Every script output stamps the commit and the count of modified tracked files; each stage recorded 0.

**Scripts.**
- `uncertain_source_sensitivity.py` is the analysis.
- `uncertain_source_crosscheck.py` is the independent check, using pandas, scipy and scikit-learn.

**Tables.**
- `sensitivity_filters.csv`: tier counts and retained n per scenario, checked against the ledger. No molecule lacks a provenance record.
- `sensitivity_octane.csv`
- `sensitivity_bp.csv`
- `sensitivity_ridge_crosscheck.csv`

## Definitions

**Scenarios.**
- **Original:** all values.
- **Broad:** tiers A, B, A-AGG and B?. A-AGG is a NIST/TRC average and does not establish independent groups; B? is not a verified primary determination.
- **Strict:** tiers A and B only.

**Estimability** (fixed before the restricted results were read; all n are reported so another rule can be applied):
- A correlation ranking needs n ≥ 10, a non-constant property and non-constant descriptors.
- A leave-one-out regression needs n ≥ 10 and a centred count rank ≥ 2.
- Otherwise the analysis is NOT ESTIMABLE and no statistic is quoted.

**Intervals.** These are paired compound-level percentile bootstraps: 2000 resamples, seed 20261013. Both models are scored on the same resample, and the Q² denominator is recomputed on each replicate. The intervals are **conditional on the fixed out-of-fold predictions**; models are not refitted inside the bootstrap.

**Three numbers per regression endpoint.**
- **Full data:** the original analysis.
- **Matched:** the original out-of-fold predictions, evaluated on the retained compounds.
- **Refit:** models refitted on the retained compounds.

**Equivalence.** An interval that includes 0 means NOT RESOLVED. No equivalence is claimed anywhere, because no margin was pre-specified.

## Independent reconstruction of the nested ridge

The scikit-learn pipeline is written separately from the audited `baselines.fold_ridge`. It uses outer and inner LeaveOneOut, StandardScaler with Ridge, and the same 41-value grid (checked equal).

| Decanes | Q² (sklearn) | Q² (audited) | Max prediction difference | Folds choosing the same penalty |
|---|---|---|---|---|
| all values | 0.859871 | 0.859871 | 2.8e-14 °C | 34 of 34 |
| strict | 0.851470 | 0.851470 | 2.8e-14 °C | 28 of 28 |

The octane subset sizes and correlations were recomputed with scipy from a separate SMILES parser, and agree.

## Results

**Survives.** A linear model on degree-pair counts outperforms every single-index model (ridge minus the best single index):

| Set | Original | Strict |
|---|---|---|
| decanes | +0.684, CI [+0.46, +1.11] | n = 28: +0.856, CI [+0.63, +1.21] |
| pooled | +0.024, CI [+0.014, +0.041] | n = 42: +0.278, CI [+0.14, +0.47] |

The matched values agree with the refits: strict decanes give a matched ridge Q² of 0.846 against a refit 0.851.

**Unresolved.** The column leaders of octane Table 4. For every property the leader-minus-runner-up interval includes 0, even on the full data:

| Property | Full data | Strict |
|---|---|---|
| ΔH_vap | +0.003, CI [−0.005, +0.007] | n = 11: leader flips by 0.001 |
| ΔH_f | +0.032, CI [−0.018, +0.105] | n = 16: same leader, CI includes 0 |
| T_B | +0.026, CI [−0.042, +0.162] | n = 0: not estimable |
| S | +0.001, CI [−0.017, +0.017] | not estimable |
| ω | +0.005, CI [−0.017, +0.034] | not estimable |

The rankings are therefore descriptive only, which the paper already states.

**Materially changes.** None of the paper's claims. The only ranking that flips (ΔH_vap at n = 11) was already unresolved on the full data.

**Not estimable.**
- octane T_B strict (n = 0)
- octane S broad and strict (n = 5 and 2)
- octane ω broad and strict (n = 0)
- nonane ΔH_vap strict (n = 4)

**Not run.**
- The registered γ test (GM vs LO over 50 seeds) on the restricted subsets.
- The nonane T_B strict subset (n = 15), for which no single-index-vs-ridge endpoint is registered.
- Refitting bootstrap intervals; all intervals are conditional.
