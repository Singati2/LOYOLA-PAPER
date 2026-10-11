# Final code and statistics audit (LOYOLA-PAPER, commit 0817f35)

Disposition of every finding in v40.29: see `MATCH_SUBMISSION_READINESS.md` in this folder.

The audit was run on 0817f35 with the candidate patch applied in a separate worktree. The
adversarial tests and the exploratory bootstrap are kept in `audit/final/scripts/`
(`adversarial.py`, `ridge_vs_index_boot.py`, with their `_out.txt` files); the patch is now part of
v40.29 (Section A4).

## Part A. The degeneracy guard of `external/baselines.py`

### A1. The defect (confirmed)
`fold_select_ols` (baselines.py:192-197) and `degenerate_rows` (baselines.py:150-156, used by
`bp/bp_tests.py:110` and `transfer_exploratory.py:47`) reject a candidate if
`is_constant(x)` or `max(x) - min(x) <= 1e-9 * max|x|`. The second clause depends on the
offset. In the adversarial runs the old guard rejects x = 1..18 shifted by 1e12 (about 77,000
resolvable steps) and rejects 1 + 1e-10 s (about a million steps). For x = 1..10 it already raises
`RuntimeError: every candidate descriptor is degenerate` at an offset of 1e10. The
`@unittest.expectedFailure` test (test_regressions.py:66-77) is a real failure on 0817f35. It is
not a pass.

### A2. Exact translation invariance cannot coexist with noise rejection (proved)
Consider any test that depends only on the stored doubles and does not change when the vector is
translated or rescaled exactly. Such a test cannot separate rounding noise from a valid descriptor.
The vector 7 + k ulp(7) (k = 0..9) is a constant with k-ulp jitter. Subtracting 7 is exact
(Sterbenz), and dividing by ulp(7) gives exactly k = 0..9, which is a valid integer descriptor.
`adversarial.py` checks this identity bit for bit. Centring or standardising the range, or an SVD
condition test on the centred design [1, x - mean], are all exactly invariant. Each of them
therefore accepts pure jitter, or else rejects 0..9. The question in the brief, "a translation
invariant replacement that still rejects quantisation noise", has a negative answer in its strict
form.

### A3. The best achievable repair: a resolution (step-count) guard
The quantity that separates noise from signal is the number of representable steps across the
range, range / (eps * max|x|). Rounding error scales with the magnitude of the stored value, not
with the centred range. The guard rejects a row with fewer than K = 1024 steps (relative range at
most 2.3e-13). It never depends on units. It is unchanged by any translation that leaves at least
1024 steps, so it is translation invariant "as far as double precision resolves the values".
That is the same sense that `is_constant` already claims. Beyond that point a translation destroys
the information itself (x + 1e16 keeps 8 steps).

Adversarial results (`adversarial_out.txt`; references from mpmath at 80 digits, computed on the
exact stored doubles):

| case | steps | old | new | intended |
|---|---|---|---|---|
| constant c(1 + k eps/2), k up to 1, 4, 16, 64, 512 ulps; c = 1e-300 ... 1e300 (40 cases) | 0.5 to 513 | reject | reject | reject |
| same number summed in permuted order, m = 7 to 200 terms | 1 to 5 | reject | reject | reject |
| octane LO(a, a, 0), a = 3.6e-15 / 1e-13 | 13 / 346 | reject | reject | reject |
| octane LO(a, a, 0), a = 1e-12 ... 1e-9 | 3.5e3 to 3.5e6 | **reject** | accept | accept |
| 1 + d s, d = 1e-10, 1e-12 | 1e6, 1e4 | **reject** | accept | accept |
| 1 + d s, d = 1e-13, 1e-14 | 998, 100 | reject | reject | reject (sub-resolution) |
| s scaled by 1e-200 ... 1e200 | 3e15 | accept | accept | accept |
| integers + 1e12, 1e13 | 7.7e4, 7.7e3 | **reject** | accept | accept |
| integers + 1e14, 1e15, 1e16 | 766, 77, 8 | reject | reject | boundary (information lost) |
| real s + 1e13 | 998 | reject | reject | boundary |
| ones with last entry + 1e-10 / + 1e-13 | 4.5e5 / 450 | reject / reject | accept / reject | accept / reject |

For every accepted candidate the inner-LOO RMSE agrees with mpmath to at most 4.5e-15 relative
error. Scoring is therefore exact on the stored values, and the guard's only role is to reject
values that carry no signal. Secondary limitation (optional): the error of `fit_predict` relative
to mpmath grows like 1/steps (1.4e-4 at 7,700 steps, 3e-3 near 1,000). The cause is that the
training mean of a large-offset vector is rounded to ulp(offset). The fix is to centre on a pivot
(xc = x - x[0]) before taking the mean. Every committed candidate has at least 1e11 steps, so this
error is below 1e-11 there.

### A4. Exact patch (applied in v40.29)
`external/baselines.py`:
```python
RESOLUTION_LEVELS = 1024   # v40.29: minimum number of representable steps (ulps of max|x|) across the range

def degenerate_rows(Xt):
    """... (docstring states the step-count rule and the impossibility of exact invariance) ..."""
    Xt = np.asarray(Xt, float)
    const = np.array([is_constant(Xt[k]) for k in range(Xt.shape[0])], bool)
    Xs = _rescale_extreme_rows(Xt)
    rng_ = Xs.max(axis=1) - Xs.min(axis=1); scale_ = np.abs(Xs).max(axis=1)
    return const | (rng_ <= RESOLUTION_LEVELS * np.finfo(float).eps * scale_)
```
In `fold_select_ols` the five lines that build `const` with the 1e-9 floor become
`const = degenerate_rows(Xt)`. The selection and the bp tests therefore share one guard.

`external/test_regressions.py`: delete `@unittest.expectedFailure` and test offsets 1e6, 1e10,
1e12 and 1e13. Add `test_rounding_noise_rejected` (512-ulp jitter at magnitudes 1e-300 to 1e300,
and 1..10 + 1e15) and `test_small_relative_range_accepted` (1 + 1e-10 s, 1e-200 s, 1e200 s,
s + 1e10). Result: 16 tests, OK, with no expected failures. On 0817f35 the suite reports an
expected failure.

Also update README.md:25-28, which says the defect is deferred. As written it also claims that
"on the package data correcting it changes no selected fold". The branch audit supports that claim
only for bp Tests A and B, and the run below now supports it for every caller.

### A5. Effect on committed outputs (complete run of every caller; selection_resampling 2216 s)
The patched worktree ran the following: `baselines.py` (octane and nonane),
`nonane_validation.py`, `transfer_exploratory.py`, `uncertainty_exploratory.py`,
`box_sensitivity.py`, `wide_box_diagnostics.py`, `bp/bp_tests.py`, `bp/selection_resampling.py`,
`nonane_tb_conflict.py`, `structural/fractional_points.py` and `test_baselines.py` (0 failures).
After those it ran `make_bp_table.py`, `make_box_table.py` and `make_v37_table.py`. Every script
exited 0. `git status` shows no committed output changed, and every CSV, TeX row file and text
output is byte-identical.

The reason is structural. An instrumented guard compared the old and new masks at each of 395,987
guard calls covering 346.7 million candidate rows (selection_resampling included). They never differed. The only rejected rows (416)
were exact constants of the wide_box D3 grid, which `is_constant` already catches. The smallest
relative range of any non-constant candidate was 2.4e-4. That is six orders of magnitude above the
old floor and nine above the new threshold. Two parts of the pipeline do not use this guard:
`structural_checks.py` and `permutation_pipeline_audit.py` use only `fit_predict` and
`fold_ridge`, which the patch does not touch. The ablation and robustness scripts at the root use
their own copies with `is_constant` only.

**Verdict:** a safe repair exists in the resolution sense of A3, and exact translation invariance
is unattainable (A2). No committed number changes, so no manuscript number, table, verdict or
conclusion changes. Disposition: should fix (code hygiene and README honesty). It is not
submission critical. Optionally add a row "Both tests | degeneracy guard counts resolvable
steps | No value changes" to Table 7 (main.tex:1809 region).

## Part B. Statistical referee review of Section 6 and the supplement
Preregistered analyses are left as they are, and everything proposed below is labelled exploratory.

1. **Abstract and conclusion present a post hoc result without qualification.** Severity: should
   fix. Status: confirmed. Location: main.tex:195-197 and 1834-1836. The wide-box disappearance of
   the vaporisation-enthalpy gain comes from Table S6. That analysis was not preregistered, and the
   box was chosen after inspecting the curves (Discussion (iv) says so). Abstract wording: "and a
   gain on vaporisation enthalpies seen in a narrow search box disappears, in an exploratory
   analysis, once the parent is searched over a box that does not truncate it." Conclusion wording:
   "but disappeared in a post hoc analysis once the parent was searched over a box that did not
   truncate it". Both edits stay qualitative, which matches the co-author abstract rule.
2. **The step from the permutation test to "thus" overreaches.** Severity: should fix. Status:
   confirmed. Location: main.tex:1745-1754. The permutation test shows that ridge's Q2 of 0.860 is
   not chance. It does not compare ridge with the index models. An exploratory conditional
   bootstrap (`ridge_vs_index_boot_out.txt`, same construction as `boot_ci`) gives ridge minus the
   median GM12 = +0.346 [+0.160, +0.747] on the decanes and +0.014 [+0.008, +0.024] on the pooled
   set. Against LO_h the figures are +0.454 [+0.269, +0.823] and +0.015 [+0.008, +0.024]. Replace
   "Under the stated boxes and candidate budgets, ridge regression thus predicts" with "Under the
   stated boxes and candidate budgets, ridge regression predicts". Then add: "In an exploratory
   molecule bootstrap conditional on the fitted predictions, ridge minus the median GM model is
   $+0.346$ $[+0.160, +0.747]$ on the decanes and $+0.014$ $[+0.008, +0.024]$ on the pooled set."
   The conclusion survives the check.
3. **The nonane ridge claim reads as a ranking.** Severity: should fix. Status: confirmed.
   Location: main.tex:1666-1668 (and the matching passage in the supplement). On
   $\Delta H_{\mathrm{vap}}$ the conditional interval for LO minus ridge is [-0.101, +0.032], which
   includes zero. Wording: "...has the highest point estimate among all models on the nonanes
   ($Q^2 = 0.927$ for $\Delta H_{\mathrm{vap}}$, $0.682$ for $T_B$); for
   $\Delta H_{\mathrm{vap}}$ the conditional bootstrap interval for LO minus ridge,
   $[-0.101, +0.032]$, includes zero."
4. **"Optimiser variance" mislabels a protocol change.** Severity: should fix. Status: confirmed.
   Location: main.tex:1623-1624. The S count moves from 11 (LO against GM, half-width 2) to 38
   (LO_h against GM, half-width 12). That is a change of box and model, not a change of seed.
   Wording: "and octane $S$ moves from $11$ to $38$ wins, which shows how strongly the seed counts
   depend on the search protocol."
5. **The Table 5 caption says $n_C$ is "in every model".** Severity: optional. Status: confirmed.
   Location: main.tex:1700-1702 and bp_tests.py:179. Ridge receives the counts only. Their sum is
   $n_C - 1$, so size enters through them but is penalised. Add: "Ridge uses the counts alone;
   their sum is $n_C - 1$."
6. **The Table 4 caption points to the wrong place.** Severity: optional. Location:
   main.tex:1531. It says "(see the text)", but the bootstrap of the top-two margins is described
   only in Supplementary Section S1. Replace with "(Supplementary Section S1)".
7. **Refit replication and frozen transfer.** Severity: optional. The supplement keeps the two
   apart correctly (lines 655-670), but main §6.3 never mentions the frozen-transfer result. Add
   one sentence: "The nested design re-tunes on the nonanes, so it tests whether the procedure
   replicates; with octane parameters and calibration frozen, both models extrapolate poorly
   (Supplementary Section S4)." Test B is leave-one-molecule-out, not grouped by carbon number.
   The text already calls it "pooled size-adjusted ... rather than a fresh external test", which is
   adequate. It could add "not grouped by carbon number".
8. **Fairness of the GM and LO comparison.** Status: confirmed fair as described. Budgets are equal
   (B pairs against B triples, 2000 against 2000 in Table 5). The narrow boxes are identical. In
   the wide box LO_h shares the parent's (α, β) box, and PREREG_v40 fixes LO_h, so it was not
   chosen post hoc for the bp tests. The text already says that equal budgets do not give equally
   thorough searches (main.tex:1629-1631), and it qualifies the claims as protocol specific
   ("Under these protocols", "Under the stated boxes and candidate budgets"). No change needed.
9. **Intervals and their estimands.** Every quoted interval matches its CSV:
   uncertainty_exploratory.csv, bp_results_summary.csv, and selection resampling in the logs. Each
   is described correctly as conditional on the fitted predictions, or as a central range that is
   not a confidence interval. The p-value 1/201 is correct. The one-sided reading is listed as a
   deviation. No change needed.
10. **Source-quality alternatives.** Status: confirmed. Location: `source_sensitivity.py`. With the
    ω alternatives the winner stays M2. With the compilation entropies HM stays the winner. With
    the 1947 API entropies the winner changes from HM to M1, a 0.004 change that the text reports
    and declines to interpret. Under the TMB variants LO(0,0,1) leads in all four. Nonane
    3-ethyl-4-methylhexane gives a verdict that stays mixed (55/60 and 61/66). None of these values
    enters a preregistered test. The text describes every case accurately. No change needed.

No submission-critical issue was found.
