# Bug-fix review of v40.5

Reviewed base: `213c20c06170b470487c02d58f8beaab715f37e5`.

## Confirmed bugs and repairs

1. **Descriptor standardization can underflow or overflow.** For
   `x = scale * arange(1, 11)` and `y = 2 * arange(1, 11) + 3`, the former
   baseline implementation returned NaN for the prediction at `11 * scale`
   when `scale` was `1e-200` or `1e200`; inner LOO returned about 6.38 RMSE
   instead of zero. Extreme rows are now rescaled before variance arithmetic.
   The prediction is 25 and inner RMSE is below `1e-12`. Ordinary descriptor
   rows retain their previous arithmetic. Constancy checks also avoid range
   overflow and tolerance underflow.

2. **CSV tolerance was inferred by excluding header patterns.** A tiny change
   to a floating-point raw-data cell or an unknown numeric parameter could
   pass the replay comparison. Tolerance now applies only to an explicit
   allowlist of result columns. Raw data, unknown columns, parameters, counts,
   and integer literals compare exactly. Empty, duplicate-header and ragged
   CSVs fail closed. Non-finite tokens cannot obtain equality through numeric
   tolerance. Identical undefined correlations such as `r_pred=nan` still
   compare exactly. The external verifier now has a main guard, so its
   comparator can be tested without starting a lengthy experiment replay.

3. **Distributed Overleaf projects were stale.** The bundled manuscript was
   107,084 bytes while the canonical root manuscript was 111,595 bytes; the
   bundles omitted the latest data-quality appendix and other v40.5 changes.
   The bundled supplement and heatmap also differed from the canonical files.
   All three folders and ZIPs now use the canonical manuscripts and figures.
   `package_overleaf.py` rebuilds them; `--check` verifies both canonical-file
   agreement and every archived file without writing. The combined-project
   README now correctly states 40 main-paper pages.

## Regression protection

`python3 external/test_regressions.py` tests extreme scaling, the previously
reported `1e13` translation case, result-roundoff tolerance, exact parameter
and raw-data comparisons, non-finite tokens, and malformed CSVs. The GitHub
workflow also runs the existing baseline reproduction/leakage tests, package
synchronization check, and manifest check.

Validation completed for this patch:

- Six targeted regression tests pass.
- The full core verifier passes with zero failures, including fresh reruns of
  all eight bundled core analyses, manuscript-table checks, and canonical
  artifact comparisons.
- The existing baseline test passes with zero failures: all 1,000 recorded
  robustness rows reproduce within its `1e-9` tolerance, and held-out-label
  perturbations change no selections or predictions.
- All Overleaf folders and ZIP contents match their canonical sources.
- The synchronized combined project compiles with pdfLaTeX: main paper
  40 pages, supplement 21 pages.
- `git diff --check` and the regenerated SHA-256 manifest pass.

## Scope

These repairs address reproducible software and distribution defects. They
do not establish that every theorem, provenance claim, or scientific decision
is correct. No canonical dataset, recorded experimental result, manuscript
claim, or Lean theorem was edited. Lean was not rebuilt in this environment.
The manuscript's unresolved primary-source provenance items remain scientific
limitations rather than bugs that can be repaired by guessing replacement data.
