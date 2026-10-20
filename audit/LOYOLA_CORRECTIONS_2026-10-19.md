# LOYOLA-PAPER: resumed audit and prioritized corrections

Review date: October 19, 2026 (America/New_York).

## Scope and evidence

Reviewed the current checkout of `Singati2/LOYOLA-PAPER`, branch `revision/v40.31-scientific`, commit `67e36ad` (October 17). `main` remains at `0c4a4db` (commit date October 12). Inspected all six remote branch tips and recent history, and targeted the latest manuscript, supplement, provenance table, verification code, Colab pipeline, and revision report.

This is a targeted continuation, not certification of every file or every account repository. The earlier paused audit's final report and logs were not recovered. Its statements about full fast-suite passes, archived-source reconstruction, PDF inspection, and 16 experiment-seed replays are user-supplied history, not fresh verification in this review. Do not cite those as tests rerun here.

The account inventory also includes `LOYOLA-FINAL-PAPER`, `topological-index-orthogonality`, `TopoQSPR`, and other projects. These are separate repositories, not branches of this paper. A README request for LOYOLA-FINAL-PAPER returned 404; this alone does not establish that the repository is inaccessible or empty. Their code and experiments are not covered by this report.

Source: https://github.com/Singati2/LOYOLA-PAPER/tree/67e36ad

## Overall assessment

The latest revision has substantive improvements and reproducible mathematical computations. Submission should wait for the specific workflow and reporting repairs below and a clean verification of the final submission commit. None of the checks here establishes that a registered scientific result is wrong. Reproducible computation also does not settle novelty or source-measurement quality.

## Corrections, in priority order

### 1. High: checkpoint reuse does not validate inputs or outputs

Location: `colab/pipeline.py`, `check_commit`, `restore`, `run_stage`, `report`.

The commit identity is checked, but uncommitted source changes do not change HEAD. Local changes trigger only a warning before the first stage. A task is skipped solely when its marker contains `ok: true`. Saved outputs are restored if present, but missing files are silently ignored. No per-task source, input, environment, or output digest validates reuse.

Fresh isolated test: created a successful marker claiming a missing output, replaced execution with a sentinel that would fail if called, and invoked `run_stage`. It printed “skip (already finished)” and returned 0. Thus a missing saved output does not invalidate the task's success marker.

Fix: record each task's source/input/environment fingerprint and expected output paths with hashes. Validate all before skipping. Reject dirty source inputs or explicitly fingerprint them. Invalidate dependent stages when an upstream input changes. Save state atomically. Final reporting must check every expected output, not only the files present in a saved index.

Acceptance: changing source without committing, deleting a saved output, altering an output, and changing a dependency must each invalidate the affected marker. An unchanged completed run should resume successfully.

### 2. High: notebook setup can expose a GitHub token on failure

Location: `colab/make_notebooks.py`, SETUP block, lines 34–37 and generated notebooks.

The token is interpolated into the clone URL and passed in the subprocess argument list. `check=True` can surface that URL in a raised exception. Resetting the remote URL happens only after clone succeeds. No real token was used or exposed during this review.

Fix: use a credential mechanism that keeps the token out of command arguments and notebook outputs; clean up credentials in a `finally` block, and sanitize captured error messages. Regenerate all notebooks from the generator.

Acceptance: a forced clone failure using a dummy marker secret must not display or retain the marker in notebook output or Git configuration.

### 3. High: current setup is not an immutable, self-validating reproduction entry point

Location: `colab/make_notebooks.py` and `REVIEWER_START_HERE.md`.

The new setup uses a moving branch. If WORK already exists it does not validate the requested revision before using it. An existing environment is reused based on the interpreter path alone. The older reviewer workflow instead points to `v40.30`; no tags were returned by the fresh clone, and the document acknowledges those links do not work until tagging.

Fix: select one documented workflow pinned to the exact approved SHA, verify existing workspaces and lockfile/environment fingerprints, and make notebooks execute that SHA. Keep public release/tag creation separate from review approval.

Acceptance: start from an empty Colab runtime, then repeat with a stale checkout and a partially installed environment. Wrong source or dependencies must be repaired or explicitly rejected.

### 4. Medium: distinguish 57 direct averages from 58 aggregate-derived values

Location: `supplement.tex` near line 1037, `REVIEWER_START_HERE.md`, and any mirrored prose/provenance summaries.

Fresh CSV count: `external/bp/bp_provenance.csv` has 100 INCLUDED rows: 57 with rule `AVG`, one with rule `mean of 2 NIST averages (agreeing within 3 K)`, and 42 other rows. Therefore 57 is correct only for the exact AVG category; 58 is the number derived from NIST aggregates.

Suggested wording: “Of the 100 values, 57 are direct NIST averages and one is the mean of two agreeing NIST averages.” Do not change the numerical datasets to fix this prose issue.

Acceptance: derive these category counts in a checker and verify all manuscript and README copies against them.

### 5. Medium: remove the unsupported quantitative uncertainty comparison

Location: `main.tex` Table 5 caption near line 1720 and discussion near lines 1750–1770.

The caption says conditional intervals “understate the uncertainty several-fold.” The discussion correctly explains that the full-procedure subsampling ranges differ in training size and seed averaging and are not directly comparable to the registered intervals; they are not confidence intervals for the full-sample statistic.

Replace the caption with: “The registered intervals are conditional on fitted predictions and omit uncertainty from refitting and model selection.” Retain the separate exploratory subsampling ranges with their limitations. A width ratio across these two procedures is not an estimate of how much the registered intervals underestimate uncertainty.

Acceptance: no quantitative inflation factor remains unless supported by a methodologically comparable calculation.

### 6. Medium: exact-reference comparison needs mandatory coverage checks

Location: `structural/exact_ties.py`, `committed()` and `main()`.

Correction to the paused summary: missing files themselves raise an error. The narrower confirmed weakness is missing or unparsed reference rows: high-precision and chi comparisons are conditional (`if ref`, `if n in chi_ref`). Empty reference files parse into empty dictionaries without an error. Fractional references later use mandatory indexing and would fail if absent; do not claim all missing references pass.

Fix: require the complete expected key sets and unique records for each reference table before enumeration; distinguish exact counts computed from reference comparisons completed. Report comparison coverage explicitly.

Acceptance: remove a required hp or chi row, truncate a reference file, or break a row's format; every mutation must return nonzero. The unmodified files must pass.

### 7. Medium: correct “trees” versus “profiles” in the revision report

Location: `audit/V4031_REVISION_REPORT.md`, exact-tie discussion.

It describes LO(3/10,1/5,0) as separating all 4069 trees of order 16. The script reports 4069 distinct degree-pair profiles among 19320 nonisomorphic trees of that order. These are different objects, and the index cannot separate trees sharing a profile.

Fix: say “all 4069 degree-pair profiles of order-16 trees.” Search manuscript, supplement, and review reports for the same conflation.

### 8. Scientific/source limitations require decisions, not cosmetic closure

The current reviewer guide discloses seven octane entropies without matched primary sources, unresolved reference-state issues for tetramethylbutane vaporisation enthalpy, compilation-only acentric factors and most nonane vaporisation enthalpies, and unresolved redistribution terms for some sources. Those disclosures were read; primary literature and legal terms were not independently reassessed here.

For each unresolved measurement, retain a source-status label and show which claims depend on it. Use credible-source-only or exclusion sensitivities where already planned; label resulting analyses exploratory. Do not imply successful CSV reconstruction validates the original measurement. Do not rewrite historical preregistrations or substitute measurements to obtain a preferred result.

The paper should retain its cautious conclusion: no gain from gamma was demonstrated under the tested protocols; this is not equivalence or proof that gamma never helps. Computational reproducibility does not by itself establish novelty. Keep elementary inherited identities separate from new separation/collision findings.

## Fresh checks completed

1. Cloned repository and listed all six remote branch tips; identified `67e36ad` as the newest branch tip by commit timestamp.
2. Recounted all 100 included boiling-point provenance records: 57 direct AVG, one mean of two averages, 42 other.
3. Executed `python structural/count_dimension_check.py`: identities hold; centred ranks 7, 7, 8; 16 octane collision classes; within-class SSE 2.925 degC²; RMSE 0.403 degC. Exit 0.
4. Executed `python structural/exact_ties.py`: exact-reference comparisons reproduced through order 17, including first GA q-histogram merge at order 17 for unrestricted trees and none through 17 for maximum degree four. All numerical counts certified by the script. This is a rerun of repository code, not a new independent proof of the cited theorems.
5. Isolated checkpoint test reproduced false success with a missing output.
6. Empty-reference parser test returned empty dictionaries without rejection; comparison logic inspected for selective omission.

No full model-search replay, new Lean build, fresh PDF render, independent literature novelty search, or NIST-source download/reconstruction was performed in this continuation. The earlier paused audit's stronger execution claims remain unverified here. A minimum-dependency environment was used for the mathematical reruns, not the repository's locked Python 3.13 environment.

## Concrete instruction for Claude

Work on a separate correction branch from the current scientific revision. Fix items 1–7 and write an explicit decision/status for item 8. Preserve frozen protocols, datasets, experimental results and running processes. Regenerate notebooks and document copies from their authoritative sources. Add targeted adversarial checks for missing outputs, changed inputs, stale environments, clone failure and missing certificate rows. Run clean locked-environment verification of the exact candidate commit, explicitly distinguishing passed, failed and not-run stages; then build and inspect manuscript/supplement outputs and manifests. Report every changed file, test command, exit status, outstanding source issue and final SHA. Do not merge, force-push, rewrite history, tag or submit the paper as part of this review.

The useful next step is repair and verify these concrete defects; another large experiment campaign is not justified by these findings alone.
