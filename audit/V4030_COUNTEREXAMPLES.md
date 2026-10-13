# v40.30 adversarial audit: counterexamples and reproductions

**Audited commits.** Audit branch `audit/v4030-adversarial`, starting from `716cd37` (the PR #3 head). The repairs are in `01ad6c6`. Each item gives the command, the old behaviour, the new behaviour and the regression or mutation test. All outputs below were produced in this audit.

**Naming.** The file names omit the tool name requested in the brief, because the repository keeps tool names out of its files.

## C1. `verify.py --full` / `--everything` exited 0 when a required stage was skipped (P1)

**Reproduction.** Tectonic and lake are removed from PATH, and the slow steps are stubbed so that the summary logic runs in seconds:

```bash
mkdir -p /tmp/fakebin && ln -sf "$(which python3)" /tmp/fakebin/python3
PATH=/tmp/fakebin:/usr/bin:/bin python3 -c '
import shutil, sys, verify as V
V.FAST = V.FULL = V.EVERYTHING = []; V.check_csv_conventions = lambda: True
for a in (["verify.py","--full"], ["verify.py","--everything"], ["verify.py"]):
    sys.argv = a; print(a[1:], "-> exit", V.main())'
```

**Old (716cd37):**

```
[SKIP] labels and references: no tectonic on PATH
[SKIP] Lean proofs: no Lean toolchain (lake) on PATH
INCOMPLETE (full): executed steps passed, SKIPPED: labels and references, Lean proofs
['--full'] -> exit 0
INCOMPLETE (everything): ... -> exit 0
```

**New (01ad6c6):**
- A run with skipped stages exits **3**.
- `--allow-skip` gives exit 0 and still prints INCOMPLETE.
- A complete run and the fast path exit 0.

**Test.** `external/test_regressions.py::test_verify_incomplete_exit_status` fails on the old `verify.py` (`FAILED (failures=1)`) and passes on the new one.

**Impact.** None on any result. It affects only what an exit status certifies. CI runs the fast path, which is unaffected.

## C2. The constancy check stayed clean when a production stream was dropped (P2)

**Mutation.** In an isolated copy of the tracked tree, the `ablation_robustness.py` streams were removed from `constancy_test_check.py`.

- **Old (716cd37):** `distinct candidate triples: 163288 ... RESULT: the two constancy tests never disagree ...`, exit 0. The omission is invisible.
- **New (01ad6c6):** `AssertionError: candidate set has 163288 triples, expected 166478: a stream was added or dropped`, exit 1.

**Second mutation.** A new script `new_generator.py` drawing `rng.uniform(-2, 2, ...)` was added.

- **New:** `AssertionError: candidate generators not covered by this check: ['new_generator.py']`, exit 1.
- **Old:** no such check existed.

**Coverage.** The count 166,478 equals the independent reconstruction in `audit/final/scripts/counterattack_v4030.py` (T2). That reconstruction rebuilds the streams from each generator's own recipe, recomputes the degree pairs with its own SMILES parser, and covers outer and inner folds. It finds a smallest relative range of 2.344e-4 and no exact-zero spread.

**Impact.** None on any result. No candidate in any stream is flagged.

## C3. The notebook pin passed on a modified working tree (P2)

**Test.** The setup-cell logic was run in throwaway clones of 716cd37 (script in the audit log):

| Case | 716cd37 behaviour (from its code; not executed) | 01ad6c6 behaviour (executed) |
|---|---|---|
| (a) tag at HEAD, clean | runs | runs (exit 0) |
| (b) tag at HEAD, tracked file modified | **runs**, printing only "(uncommitted changes)" | stops: REVISION MISMATCH ... with uncommitted changes (exit 1) |
| (c) no tag | stops | stops (exit 1) |
| (d) tag on another commit | stops | stops (exit 1) |
| (e) no tag, `LOYOLA_ALLOW_MISMATCH=1` | runs with a warning | runs with a warning (exit 0) |
| (f) source archive without `.git` | stops | stops (exit 1) |

**Impact.** Only on what a notebook run certifies.

## C4. Duplicate determinations counted as independent (P2; found by the PR #3 reviewer, reproduced here)

**Old (aa17932).** These four nonane ΔH_vap values were in tier A:

| Compound | What the "independent" entries actually were |
|---|---|
| 2,2,5-trimethylhexane | both Osborne and Ginnings 1947 |
| 2,3,5-trimethylhexane | both Osborne and Ginnings 1947 |
| 3,3-diethylpentane | Fuchs and Peacock 1979, under two methods |
| 2,2,4,4-tetramethylpentane | Fuchs and co-workers |

**Fixed (716cd37).** Deduplication by research group. **Totals: A 35 (was 39), B 55 (was 51).**

**01ad6c6 additionally:**
- boiling-point groups are matched by first surname;
- Anonymous entries are ignored;
- the National Bureau of Standards co-authors (Howard, Mears, Pomerantz) are merged.

The totals are unchanged by these additions.

**Impact.** The ledger's count of independently confirmed values was overstated by four. No value in the paper is affected.

## C5. press_size returned a finite PRESS for an undefined fit (P1; fixed in 0e0a6d4, re-verified here)

**Reproduction.** `cd audit/final/scripts && python3 counterattack_v4030.py` gives:

```
T1a delta=0.0001: deleted rank 2; old 4.6301; new inf; reference None
T1b eps=0.001: min(1-h) 1.20e-06; reference 1414.02; old rel.err 1.3e-09; new rel.err 1.3e-09
T1b eps=0.0001: min(1-h) 1.20e-08; reference 14159.6; old rel.err 3.5e-07; new rel.err rejected
T1c 400 random well-posed designs: rejected or old != new in 0; max rel. error vs 40-digit reference 4.8e-16
```

**Exact condition.** Leave-one-out PRESS for y ~ 1 + z + x is undefined exactly when deleting some row leaves a rank-deficient design. For a full-rank design that is equivalent to h_ii = 1.

**Guard behaviour.** The guard is conservative by design. It also rejects defined fits with 1 − h ≤ 1e-6, which have PRESS amplified by at least 10^6 and are never selected.

**Replays with the guard:** `bp_tests.py`, `selection_resampling.py` and `wide_box_diagnostics.py` reproduce every committed output byte for byte.

## C6. The replay detects a corrupted counter-attack output (verification, no defect)

`run_all_scripts.run_one` was run on `counterattack_v4030.py` twice:
- with the committed reference: `changed: []`;
- with the reference hash of `counterattack_v4030_out.txt` replaced: `changed: ['audit/final/scripts/counterattack_v4030_out.txt']`, which the replay reports as a problem.

The script reads the old press_size from a frozen copy. Run in an isolated copy without `.git`, it exits 0 and reproduces its output byte for byte.

## No counterexample found

`audit/v4030/math_independent.py` was written for this audit. Its output is in `math_independent_out.txt`.

| Claim | Independent result |
|---|---|
| First collision orders | 13 (all trees) and 16 (Δ ≤ 4). Enumeration of orders 2 to 17 is complete against OEIS A000055 and A000602, with no duplicate canonical forms. The witnesses equal the paper's profiles, and both pairs are realised by trees. |
| No collision at lower orders | none at orders ≤ 12 (all trees) or ≤ 15 (Δ ≤ 4) |
| GA | first merges two distinct histograms at order 17. The paper's example has an exact GA difference of 0 and different histograms. |
| Five crossings | V = 5, with 5 sign changes at γ ≈ −17.17, −11.96, −2.03, 2.73, 31.13 |
| Lemma 3.1 | determinants ln 2 · ln(9/8) and −(1/6) ln(3/2) ln(2^13/3^8) match to 12 digits; the Δ = 2 identity holds |
| Identifiability bound | no violation among subsets of ≤ 4 pairs for Δ ≤ 6; for Δ = 7 only {(1,7),(2,6),(3,5),(4,4)} |
| Counts | 16 distinct octane count vectors with the two stated collision pairs; centred ranks 7, 7, 8; error floor SSE 2.925 (RMSE 0.4031) |
| Extremal trees | path and star are the unique extremisers for n = 4 to 14 at γ ∈ {1, −1, 0.3} |
| Closed forms | max error 1.7e-39 |
| Example 4.4 | D(1) = 0.225538, D(1e-6) = 2.401e-7 |
| Raw data rebuild | `build_bp_data.py` and `build_nonane_data.py`, run from the archived NIST pages, reproduce `bp_data.csv`, `bp_provenance.csv` and `nonane_data.csv` byte for byte |
| Unit re-conversion | 78 octane values (T4): 74 within tolerance; the other 4 are exactly the rows labelled SOURCE VARIATION or CONFLICT |
