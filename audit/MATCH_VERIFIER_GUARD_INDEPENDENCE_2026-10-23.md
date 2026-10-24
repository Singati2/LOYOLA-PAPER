# Verifier guard independence, 2026-10-23

Under test: the change to `constancy_test_check.py` in `3a5f061`. That commit added two audit scripts to the guard's allowlist, after which `verify.py --offline` passed.

## 1. What the guard protects

`constancy_test_check.py` (lines 40–59) walks the whole tree and collects every `.py` file whose text matches `uniform(-2, 2` or `candidate_triples(`, that is, every script that draws Loyola candidate triples. Each such file must appear in one of three sets:
- `SAMPLING`, whose generator lines are checked literally;
- `RUNTIME_GUARDED`, scripts that select through `external/baselines.fold_select_ols` and so carry the resolution guard at run time;
- `NOT_SELECTION`, defined in the source as "audit copies and checkers do not select for the paper".

The stated purpose is that "a new or forgotten generator cannot leave this check clean". After this assertion, the script reruns the constancy comparison on the paper's inputs.

## 2. First failure (verifier log, branch working tree before `3a5f061`)

```
[FAIL] constancy test check (0 s): AssertionError: candidate generators not covered by this check:
['audit/independent_recompute_2026-10-23/decane_indep.py', 'audit/independen…
```

The other 14 stages passed, and the NIST stages were NOT RUN.

## 3. The change

Before (`3904e38`):
```python
NOT_SELECTION = {"constancy_test_check.py", "audit/final/scripts/baselines_old.py", "audit/final/scripts/bp_tests_0c4a4db.py",
                 "audit/final/scripts/counterattack_v4030.py", "audit/final/scripts/nonane_calc.py"}
```
After (`3a5f061`):
```python
NOT_SELECTION = {"constancy_test_check.py", "audit/final/scripts/baselines_old.py", "audit/final/scripts/bp_tests_0c4a4db.py",
                 "audit/final/scripts/counterattack_v4030.py", "audit/final/scripts/nonane_calc.py",
                 # 2026-10-23 literature audit: independent re-computations, not used for selection
                 "audit/independent_recompute_2026-10-23/pooled_indep.py", "audit/independent_recompute_2026-10-23/decane_indep.py"}
```

Two exact paths were added. There is no wildcard and no directory exemption, and the guard logic is unchanged.

## 4. Are the added scripts really outside the paper's pipeline?

| Script | Imports | Writes | Referenced by |
|---|---|---|---|
| `decane_indep.py` | csv, sys, numpy | one file, at the path given as `argv[2]` | nothing except the guard list |
| `pooled_indep.py` | csv, sys, numpy | one file, at the path given as `argv[2]` | nothing except the guard list |

- Neither script imports a repository module.
- `grep -rn independent_recompute --include=*.py --include=*.sh --include=*.yml` outside their own directory finds only the guard line.
- `verify.py`, the table builders and the manuscript build never run them.
- They re-derive published decane and pooled contrasts from `external/bp/bp_data.csv` with their own code, and they select nothing that enters the paper.

They are therefore what the guard's `NOT_SELECTION` category describes.

## 5. Negative-control tests

The tests ran in a throwaway worktree (`wt-guardtest`, detached at `3a5f061`), which was restored and left clean (0 changes). Command: `python constancy_test_check.py`. Log: session scratch `valaudit/guard_tests.log`.

| Test | Manipulation | Expected | Exit |
|---|---|---|---|
| T1 | New file `rogue_select.py` at the repository root that calls `rng.uniform(-2, 2, (10, 3))` | fail | **1** |
| T2 | The same file placed inside the exempted directory as `rogue_indep.py` | fail (the exemption is per path) | **1** |
| T3 | Guard restored to the `3904e38` version, with the two scripts present | fail (reproduces the first failure) | **1** |
| T4 | Unmodified `3a5f061` tree | pass | **0** |

T1 and T2 show the guard still catches a new generator anywhere, including next to the exempted files.

**Residual risk.** Someone could later edit one of the two exempted files into a selector without the guard noticing. This is the same exposure as the four `audit/final/scripts/*` entries already in `NOT_SELECTION`. It is limited because nothing imports or runs these files.

## 6. Verdict

The relaxation is narrow and matches the guard's documented purpose, and it does not bypass a substantive protection. It is **kept**.

## 7. Final checks on the validation branch

See `MATCH_FINAL_COAUTHOR_GATE_2026-10-23.md`, section "Checks run", for the commands, tree and exit codes after this branch's edits.
