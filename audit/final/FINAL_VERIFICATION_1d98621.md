# Final verification report: commit 1d98621

- **Code and text commit verified:** `1d98621a7d3e150cb66a2fd6e4e57abbda18e0a2` (v40.30). The logs are added in a later commit that touches only `verification_logs/` and the manifest.
- **Machine:** MacBook Pro, Apple Silicon (arm64), macOS (Darwin 24.6.0), 2026-10-12.
- **System Python:** 3.13.0.
- **Notebooks:** a fresh virtual environment built only from `requirements-lock.txt` and `requirements-extras-lock.txt` (numpy 2.4.4, scipy 1.17.1, networkx 3.6.1, mpmath 1.3.0, pandas 3.0.6).
- **Free disk:** about 5.6 GB. That rules out a Lean rebuild on this machine (see Lean).

Status words used below:
- **PASS:** executed on this commit and passed.
- **PASS (carried):** passed on an earlier commit, and every file it depends on is byte-identical at 1d98621.
- **NOT RUN:** not executed for this commit.
- **UNVERIFIED:** could not be checked.

## Matrix

| Area | Status | Evidence (command, commit, runtime) |
|---|---|---|
| Mathematics: collision orders 13 and 16 | PASS | `structural/minimality_check.py` in `verify.py` (fast path); notebook 02. Exhaustive over trees of orders 2 to 16, exact rationals. |
| Mathematics: Table 2 counts, orders 12 to 17 | PASS | notebook 03, recomputed by full enumeration (25 checks, 0 mismatches). |
| Mathematics: interval certificates, extremal trees, count dimension 7/7/8, error floor, Example 4.4 | PASS | `verify.py` fast path. |
| Mathematics: structural checks, 32-digit recount, verifier self-test, checker counter-attacks | PASS (carried) | `verify.py --full` at 3af7f67 ended ALL PASS (`verification_logs/v40.29/verify_full.log`). `structural/` and `formal/` are unchanged since. |
| Lean (38 theorems; axioms propext, Classical.choice, Quot.sound) | PASS (carried); NOT RUN at 1d98621 | passed at 3af7f67, and `formal/` is unchanged since. The local build cache was deleted to free disk. A rebuild needs about 7.6 GB, so it was not attempted with about 5.6 GB free. |
| Statistical code: press_size deletion-rank guard | PASS | `audit/final/scripts/counterattack_v4030.py`, T1; see "Defects" below. |
| Statistical code: constancy coverage | PASS | same script, T2. The checker's candidate set equals an independent reconstruction: 166,478 triples, and no test flags any of them. |
| Experiments: Test A/B, selection resampling, wide-box diagnostics | PASS | rerun with the patched press_size, on the working tree of 0e0a6d4. Every committed output is byte-identical. `external/bp/bp_tests.py` is identical at 1d98621. Runtimes: 58 min, 3 h 27 min and 21 s. |
| Experiments: core analyses (octane tables, ablations, sensitivities, figures) | PASS | core verifier in the `verify.py` fast path, which reruns them byte for byte. |
| Experiments: external verifier (nonane rebuild, all external re-runs) | PASS (carried) | at 3af7f67. Since then only the press_size guard has changed in `external/`, and the reruns above cover it. |
| Source provenance | PASS with UNVERIFIED items | `audit/final/scripts/claim_provenance.py` and `CLAIM_PROVENANCE_LEDGER.md`: 259 values, of which 39 independent, 97 NIST/TRC averages, 51 single primary, 11 single NIST, 52 compilation only, 9 unverified. Counter-attack T4 re-converts 78 octane values: 74 fall within tolerance, and the other 4 are exactly the rows labelled SOURCE VARIATION or CONFLICT. T3: the entropy lists are disjoint and total 6 + 7 = 13. |
| Citations | 2 VERIFIED, 1 UNVERIFIED | 1972 Zagreb citation (M1 and M2): Gutman and Das, MATCH 50 (2004) 84. IRLA: Réti et al., MATCH 79 (2018) 516, Proposition 2. Konstantinova (1996): content paywalled. |
| Prose numbers | PASS | 733 checked, 0 failures, 20 cited values not checkable. |
| Fast suite (`python3 verify.py`) | PASS | at 1d98621, clean tree: 16 steps, `ALL PASS (fast path)`, exit 0, manifest 499 files (`verification_logs/v40.30/verify_fast.log`). |
| LaTeX and figures | PASS | tectonic builds both documents (40 and 27 pages); `audit/check_labels.py` and `audit/check_style.py` pass; figures are regenerated and compared by the core verifier. |
| Notebooks, local fresh environment | PASS | all six executed at 1d98621, clean tree, in the lock-file environment: 01 (9 checks), 02 (20), 03 (25), 04 (69), 05 (27; `RUN_SLOW = False`, so the seed medians are compared against stored output), 06 (3; it ran the fast suite in its own pinned environment, ALL PASS). 153 checks, 0 mismatches. Executed copies are in `verification_logs/v40.30/notebooks/`. |
| Notebooks, Google Colab | NOT RUN | no Colab access from this machine. The Colab links resolve only after the tag `v40.30` exists. |
| GitHub Actions | NOT RUN for 1d98621 | the commit is not pushed. Last green run: 0c4a4db (fast path). CI runs only the fast path. |

## Defects confirmed in this round, with minimal reproductions

1. **press_size returned a finite PRESS for an undefined leave-one-out fit.** Fixed in 0e0a6d4.
   - Reproduction: `z = [1,2,3,4,5]`; `x = z` except `x[0] = 1.0001`; `y = [2,-1,3,4,0]`.
   - Deleting row 0 leaves 1, z and x linearly dependent (rank 2), so the deleted fit is undefined.
   - The old code returned 4.6301, because the leverage computed from the inverse of A'A came out as 1 − 5e-7 and passed |1 − h| > 1e-10. The new code returns inf.
   - Leave-one-out PRESS is undefined exactly when a deletion leaves the design rank deficient. For a full-rank design that is equivalent to h_ii = 1.
   - **Accepted limitation:** the new guard is conservative. It also rejects designs whose deletions are still defined but have 1 − h < 1e-6. In counter-attack T1(b) that happens at eps = 1e-4 and 1e-5, where 1 − h is 1.2e-8 and 1.2e-10. Such candidates have PRESS amplified by at least 10^6, so they are never selected; the reruns are byte-identical.
   - On 400 random well-posed designs nothing is rejected, and the result agrees with a 40-digit reference to 4.8e-16.
2. **The constancy checker did not cover the production candidate streams.**
   - It drew budget 500 after budget 200 from one random stream, omitted the LO-zero controls, and missed `ablation_robustness.py` (seeds 777 and 2024).
   - Fixed in 0e0a6d4 and 1d98621. The result is unchanged: no flag from any test, smallest relative range 2.43e-4 on the outer folds and 2.34e-4 including the inner folds.
3. **The supplement counted 13 entropies as "seven plus seven".** Fixed in 0e0a6d4.
4. **verify.py --full printed "ALL PASS" when the Lean or LaTeX stage was skipped.** Fixed in 1d98621; the run now ends "INCOMPLETE ... SKIPPED: ...".
5. **Notebook 05 failed on the four-decimal Test B cell (−0.0001)**, from v40.29 onwards. Fixed in 1d98621.

No defect changed a reported number, table, figure, theorem statement, data value or pre-registered conclusion.

## Files changed in this round (0c4a4db..1d98621)

**Code**
- `external/bp/bp_tests.py`: deletion-rank guard.
- `constancy_test_check.py`: production streams.
- `verify.py`: honest summary line.
- `notebooks/gen_notebooks.py`: pinning, labels, provenance checks, four-decimal parsing.
- `prose_claims_a.py`: two tolerances tightened to three decimals.

**Tests and audits**
- `external/test_regressions.py`: two tests.
- `audit/final/scripts/counterattack_v4030.py` and its output.
- `claim_provenance.py`, with its ledger CSV and output.
- `audit/run_all_scripts.py`: new scripts registered.

**Manuscript**
- `main.tex`:
  - decane range 0.149 to 0.514 (was 0.15 to 0.51; same quantity, more digits);
  - publisher of Wilhoit and Zwolinski;
  - novelty sentence points to the search log.
- `supplement.tex`:
  - entropy list of six;
  - publisher;
  - the independence sentence in S1.
- The Overleaf copies, zips and PDFs are rebuilt from these.

**Documentation**
- `REVIEWER_START_HERE.md`
- `REPRODUCE.md`
- `audit/final/CLAIM_PROVENANCE_LEDGER.md`
- `audit/final/NOVELTY_SEARCH_LOG.md`
- the changelog
- `source_sensitivity.py`: docstring only

## Unresolved items

1. Seven octane entropies and the tetramethylbutane ΔH_vap are unverified, and the tetramethylbutane acentric factor is a CONFLICT.
2. The acentric factors and 29 nonane ΔH_vap values exist only in compilations.
3. The content of the Konstantinova (1996) citation is UNVERIFIED.
4. The novelty statement is an absence claim, and it cannot be proved. Its search scope is documented.
5. The redistribution terms of the KDB and Chemeo values are not established.
6. Lean, the structural suite and the external verifier were not re-executed on 1d98621. They are carried over on the grounds of unchanged dependencies. Running `verify.py --full` on a machine with enough disk would close this.
7. The notebooks have not been run on Colab.

## Recommendation

**Ready to push for review** on a separate branch (for example `audit/provenance-final`), with a pull request. Supporting files:

- this matrix;
- `verification_logs/v40.30/`;
- `audit/final/scripts/counterattack_v4030_out.txt`.

**Not yet ready to freeze for submission.** The blockers are:

1. Run `python3 verify.py --full` (including Lean and labels) on the exact submission commit, on a machine with enough disk. The only evidence for those stages is carried over from 3af7f67.
2. Create the tag `v40.30`. The notebook pin and the Colab links depend on it.
3. Run the six notebooks once on Colab.
4. Author decisions:
   - the AI-use disclosure;
   - funding and conflict-of-interest lines;
   - coauthor approval;
   - the Zenodo DOI, minted only after the tag.

## Addendum: pull-request review of aa17932 (automated reviewer, three comments)

All three comments were reproduced and confirmed before any change.

1. **The ledger counted duplicate entries of one study as independent determinations.**
   - Affected rows: 2,2,5- and 2,3,5-trimethylhexane (both remaining entries are Osborne and Ginnings 1947), and 3,3-diethylpentane and 2,2,4,4-tetramethylpentane (Fuchs and co-workers).
   - Fix: the script now deduplicates by research group (first-author surname; the co-authors Fenske and Braun count as one group).
   - Result: four nonane ΔH_vap values move from tier A to tier B. **Corrected totals: A 35, A-AGG 97, B 55, B? 11, C 52, D 9** (was A 39, B 51). The boiling-point and nonane T_B tiers are unchanged.
2. **counterattack_v4030.py was not replayed by `audit/run_all_scripts.py`, and it needed git.**
   - It now reads the old press_size from a frozen copy (`audit/final/scripts/bp_tests_0c4a4db.py`, byte-identical to 0c4a4db apart from a two-line header) and is registered in the replay list.
   - Run in an isolated copy of the tracked tree without `.git`, it exits 0 and reproduces its committed output byte for byte.
3. **The notebooks ran unpinned when the tag could not be resolved.**
   - They now try to fetch the tag. If the revision still cannot be confirmed, they stop with REVISION MISMATCH unless `LOYOLA_ALLOW_MISMATCH=1` is set, in which case they print a warning that the results are not tied to the pinned revision.
   - Until the author creates the tag `v40.30`, every notebook run needs that variable.
   - Tested: without the variable, 01 stops; with it, 01 passes 9 checks.
