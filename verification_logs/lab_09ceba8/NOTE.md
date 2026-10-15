# Lab run at 09ceba8 (mpcrlab12, Ubuntu 22.04, i9-9900K, Python 3.13.16)

Read this before SUMMARY.txt, which lists every attempt in order.

## Result
| Stage | Result |
|---|---|
| Lean (formal/verify.sh) | PASS: 38/38 listed theorems and all 52 declarations use only propext, Classical.choice, Quot.sound; no sorry |
| Notebooks 01-04 | PASS (123 checks, 0 mismatches) |
| Notebooks 05, 06 | PASS on rerun (05: 27 checks, 06: 3 checks, 0 mismatches); the first run of each timed out (outputs kept as `*_first_run_timeout.ipynb`) |
| verify.py --everything | every stage PASS except: labels SKIP (no tectonic), every-script replay FAIL (below) |
| Every-script replay | INCOMPLETE: crashed on a timeout; 20 OK, 2 rounding-level differences, the remaining scripts were not replayed |

verify.py --everything stages that passed: core verifier, prose numbers (742 checked, 0 failures), external regression tests, baseline tests, constancy check, auxiliary outputs, archived-source identities, interval certificates, prose style, extremal trees, collision minimality, sum-connectivity pair, count dimension, DATA copies, manifest, external verifier, structural checks, 32-digit recount, verifier self-test, counter-attacks (13 attacks, 13 rejected, 0 false negatives), Lean proofs, provenance CSV convention.

## Every-script replay (audit/run_all_scripts.py)
Run twice (inside verify.py --everything, and directly with full stderr in `run_all_scripts_rerun.log`). Both runs stopped with
`subprocess.TimeoutExpired: ... selection_resampling.py timed out after 7200 seconds`.
That script took 1724 s on the author's machine. A per-script timeout raises out of the thread pool and ends the whole stage, so the scripts listed after it were not replayed here. Suggested fix: record a timeout as a PROBLEM and continue.

The two scripts reported as PROBLEM differ only in floating-point last digits (committed outputs come from macOS):
- `external/transfer_exploratory.py`: 3 cells of the frozen-Q2 column differ in the 14th significant digit (e.g. -4226.5717015756 vs -4226.5717015754); all other cells identical.
- `external/wide_box_diagnostics.py`: the reported maximum relative solver errors differ (2.24e-14 vs 1.93e-14; 1.40e-14 vs 1.29e-14; 1.17e-15 vs 1.14e-15); rejections (0 of 3000) and argmin agreement (10/10) identical.

## Environment notes
- The notebooks call bare `python`; run without the venv on PATH they fail with exit 127. The first attempt here did, and was discarded.
- Running `verify.py --everything` before the notebooks rewrites `audit/attack_checks_out.txt` and makes the manifest check in notebook 06 fail; here the notebooks ran first. Files rewritten by --everything are kept under `rewritten_by_everything/`.
- The first runs were slowed by a concurrent job that held the CPU at 800 MHz (thermal throttling); that job was paused for the reruns.
- Notebooks ran with LOYOLA_ALLOW_MISMATCH=1 (tag v40.30 not yet created): results are tied to 09ceba8.
