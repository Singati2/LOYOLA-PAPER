# Reproduction map

Environment: `python3 -m pip install -r requirements-lock.txt` (numpy, scipy,
networkx, matplotlib, sympy, mpmath). Lean: `formal/verify.sh` (elan/lake).

## Checks to run
| Command | What it verifies | Runtime |
|---|---|---|
| `python3 verify_loyola_v35.py` | octane data, closed forms, bounds, all 8 core tables (exact display strings), figures (canonical PDF content), every core analysis re-run byte-for-byte | ~5 min |
| `python3 verify_loyola_v35.py --selftest` | 113 adversarial attacks on the verifier itself | ~10 min |
| `python3 external/verify_external.py` | nonane data rebuilt from archived NIST pages; boiling-point data rebuilt; every external analysis re-run byte-for-byte; Tables tab:external, tab:box, tab:bp row by row | ~25 min |
| `python3 structural/structural_checks.py` | tree orders 7-17, GA and crossing witnesses, identifiability (Delta<=6), structure sensitivity of IRLA and the gamma sweep, auxiliary Q2 values, ridge permutation check; Table tab:firstfail entry by entry | ~20 min |
| `formal/verify.sh` | Lean 4 proofs (36 theorems; no sorry/axioms) | ~1 min after first build |
| `python3 manifest.py` | SHA-256 of every tracked file, one hash per path | seconds |

## Every table and figure
| Item | Document | Produced by | Checked by |
|---|---|---|---|
| Table 1 tab:collisions | main | redundancy_collisions.py | verify_loyola_v35.py |
| Table 2 tab:firstfail | main | structural/structural_checks.py (S1) | structural_checks.py (check_tab_firstfail) |
| Table 3 tab:fgdss | main | fgd_structure_sensitivity.py | verify_loyola_v35.py (first-principles recomputation) |
| Table 4 tab:lo_octane | main | verify_loyola_v35.py | verify_loyola_v35.py |
| Table 5 tab:box | main | external/box_sensitivity.py, make_box_table.py | verify_external.py |
| Table 6 tab:external | main | external/baselines.py, nonane_validation.py, make_v37_table.py | verify_external.py |
| Table 7 tab:bp | main | external/bp/bp_tests.py, make_bp_table.py | verify_external.py |
| Table 8 tab:octane-data | main | octane_data.py | verify_loyola_v35.py |
| Figure S1 fig:octanes | supplement | generate_loyola_v35_figures.py | verify_loyola_v35.py (regeneration, decompressed-content compare) |
| Figure S2 fig:degeneracy | supplement | generate_loyola_v35_figures.py | verify_loyola_v35.py |
| Tables S1-S2 tab:lo_tuning(_bestfixed) | supplement | verify_loyola_v35.py | verify_loyola_v35.py |
| Table S3 tab:ablation | supplement | ablation_gm_vs_lo.py, expanded_robustness_v35.py | verify_loyola_v35.py |
| Table S4 tab:multiorder | supplement | multi_order_degeneracy.py | verify_loyola_v35.py |

## Experiments quoted in the text without their own table
| Experiment | Script | Checked by |
|---|---|---|
| 100-seed robustness, paired control | expanded_robustness_v35.py | verify_loyola_v35.py |
| tetramethylbutane exclusion sweep | tmb_exclusion_sensitivity.py | verify_loyola_v35.py |
| omega- and entropy-source sensitivity | source_sensitivity.py | verify_loyola_v35.py |
| exploratory transfer (octane -> nonane) | external/transfer_exploratory.py | verify_external.py |
| molecule bootstrap intervals | external/uncertainty_exploratory.py | verify_external.py |
| pre-registered nonane test | external/nonane_validation.py (PREREG_v37.md) | verify_external.py |
| pre-registered boiling-point tests | external/bp/bp_tests.py (PREREG_v40.md) | verify_external.py |
| structural counts and witnesses | structural/structural_checks.py | itself (output committed) |
| fixed fractional exponents, gamma=0 vs 1 (exploratory) | structural/fractional_points.py | output committed (fractional_points_out.txt) |

## Datasets
| Dataset | Source | Rebuilt / checked by |
|---|---|---|
| 18 octanes (octane_data.py) | NIST WebBook / KDB; per-value provenance in octane_property_provenance_v35.csv | verify_loyola_v35.py (values = appendix = provenance; class rules) |
| 35 nonanes (external/nonane_data.csv) | archived NIST pages external/nonane_raw_nist/ | external/build_nonane_data.py via verify_external.py |
| 101 alkanes C6-C10 boiling points (external/bp/bp_data.csv) | archived NIST pages external/bp/nist_raw/ | external/bp/build_bp_data.py via verify_external.py |
