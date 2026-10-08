# Pre-registration v40: measured boiling-point tests (decanes; pooled C6-C10)

Written 2026-10-05 and committed BEFORE any dataset below was assembled and
before any model was fitted to it. Disclosure: NIST WebBook phase-change pages
for all acyclic alkanes C4-C16 were downloaded and archived on 2026-10-03 during
a data-availability audit (counts of available values only); no C6, C7 or C10
boiling point has been used in any model. Octane and nonane boiling points were
used in earlier analyses of this project (in-sample for octanes, pre-registered
test for nonanes); they enter test (B) only as part of the pooled set, which is
why (B) is labelled a size-adjusted pooled analysis rather than a fresh
external test.

## Data rule (all molecules, all tests; fixed now)
Source: the archived NIST WebBook phase-change page of each acyclic alkane.
Normal boiling point T_B (K -> degC, 0.1 precision):
1. If NIST gives an averaged value ("AVG"), use it.
2. Otherwise take all listed experimental determinations, excluding handbook
   compilations (Weast & Grasselli 1989; Majer & Svoboda 1985). If at least one
   remains and their spread (max - min) is <= 3 K, use their median.
3. If the spread exceeds 3 K, or no non-compilation determination exists, the
   molecule is EXCLUDED (recorded with the reason).
Structures: each NIST InChI skeleton is converted to a carbon tree; identity is
checked by isomorphism against the enumerated trees with max degree <= 4.

## Test A: external decane T_B (n expected about 34-44 after the rule)
Models, all with fully nested leave-one-out selection, seeds 0-49, 2000
candidates per model:
- GM12: parent, (alpha, beta) ~ U(-12,12)^2 (non-binding box);
- LOh: Loyola hybrid, (alpha, beta) ~ U(-12,12)^2, gamma ~ U(-2,2);
- also reported: GM and LO in the box (-2,2) (the original protocol);
- baselines: training-fold mean; best of the ten classical indices; IRLA;
  ridge on degree-pair counts (inner-LOO penalty); fixed LO(0,0,1).
Primary contrast: dQ2 = Q2(LOh) - Q2(GM12), median over seeds.
Decision: "gamma adds value on decane T_B" if LOh beats GM12 in >= 40/50
seeds AND the 95% molecule-bootstrap interval (2000 resamples, conditional on
fitted predictions) of the median dQ2 excludes 0. Otherwise "no evidence".

## Test B: pooled size-adjusted T_B, C6-C10 (all molecules passing the rule)
Model for every descriptor x: T_B = a + b * n_C + c * x(G), fitted by OLS
inside each training fold; for GM/LO the candidate is chosen by inner-LOO
RMSE of this two-predictor model (same streams and boxes as Test A).
Compared: size only (a + b n_C); size + best classical index; size + IRLA;
size + GM12; size + LOh; size + LO(0,0,1); ridge on degree-pair counts
(which encode size through their sum). Outer leave-one-out over molecules.
Primary contrast and decision rule as in Test A (LOh vs GM12, both with n_C).
Secondary: whether any imbalance-containing model beats size + best classical.

## Reporting
All results reported whatever they show; deviations recorded with date and
reason before the affected analysis runs. Counts are optimizer-variance
summaries; bootstrap intervals do not account for refitting/selection
uncertainty.

## Deviation D5 (recorded 2026-10-05, AFTER the v40/v40.2 results had been seen)
An external audit of commit 0844d6b found that `build_bp_data.py` read only the
first NIST page of a skeleton with several entries sharing one InChI. For
3-ethyl-4-methylhexane the second entry (C500006531, Lukes & Langthaler 1957,
407.15 K) was therefore not seen; together with the first (C3074779, Fenske
et al. 1947, 413.55 K) the spread is 6.40 K > 3 K, so under the rule above the
molecule must be EXCLUDED. Policy now fixed: all pages of a grouped skeleton
are pooled before the rule is applied (NIST averages on grouped pages must
agree within 3 K and are averaged). Effect on the dataset: 3-ethyl-4-
methylhexane excluded (pooled n = 100), 3-methylhexane 91.9 -> 91.7 degC
(second page pooled); 3-methylheptane and 2,4-dimethylhexane gain a second
page without a change of value. Test B was rerun on the corrected cohort; the
v40.2 results on the original cohort are preserved in git history (commit
0844d6b) and in the changelog, and both are reported. Test A (decanes) is
unaffected by the policy.

## Reporting note (recorded 2026-10-05, after the results)
The "also reported" GM and LO results in the box (-2,2) (Tests A and B) are in
external/bp/bp_results_summary.csv (columns median_Q2_GM2, median_Q2_LO2) and
are now quoted in Section 6.4 of the manuscript (decanes 0.469 / 0.465; pooled
0.976 / 0.980). No analysis was changed.

## Deviation D6 (recorded 2026-10-07, after the results)

The Test B least-squares solver was re-conditioned (column scaling) after the first
results had been seen (commit 0844d6b); on the uncorrected 101-molecule cohort this moved
the Test B summary from -0.0004 / 23 of 50 to -0.0001 / 24 of 50 and changes no verdict.
Recorded here so that the protocol file lists every post hoc change.
