# Reproduction map

Environment: `python3 -m pip install -r requirements-lock.txt` (numpy, scipy,
networkx, matplotlib, sympy, mpmath). Lean: `formal/verify.sh` (elan/lake).

## Checks to run
| Command | What it verifies | Runtime |
|---|---|---|
| `python3 verify.py` (`--full` for everything below) | single entry point: runs the core verifier, the prose-number check, the external regression and baseline tests, the constancy check and the manifest, and exits non-zero on any failure; `--full` adds the external verifier, the structural suite, the 32-digit recount, the self-test and (if a Lean toolchain is present) the Lean proofs | ~6 min / ~1 h |
| `python3 verify_loyola_v35.py` | octane data, closed forms, bounds, all 8 core tables (exact display strings), figures (canonical PDF content), every core analysis re-run byte-for-byte | ~5 min |
| `python3 verify_loyola_v35.py --selftest` | 114 adversarial attacks on the verifier itself | ~10 min |
| `python3 external/verify_external.py` | nonane data rebuilt from archived NIST pages; boiling-point data rebuilt; every external analysis re-run byte-for-byte; Tables tab:external, tab:box, tab:bp row by row | ~25 min |
| `python3 structural/structural_checks.py` | tree orders 7-17, GA and crossing witnesses, identifiability (Delta<=6), structure sensitivity of IRLA and the gamma sweep, auxiliary Q2 values, ridge permutation check; Table tab:firstfail entry by entry | ~20 min |
| `formal/verify.sh` | Lean 4 proofs (36 theorems; no sorry/axioms) | ~1 min after first build |
| `python3 manifest.py` | SHA-256 of every tracked file, one hash per path | seconds |
| `python3 external/test_regressions.py` | unit checks of the shared regression core (extreme descriptor scales, large-offset constancy) and of the fail-closed CSV comparator, without running the external suite | seconds |
| `python3 prose_numbers_check.py` | every registered numeral of the running prose of both documents (735 entries in prose_claims_a.py and prose_claims_b.py; 16 cited values listed as uncheckable) recomputed from the canonical files | seconds |
| `python3 constancy_test_check.py` | shows that the constancy test is inert: no candidate descriptor of the octane analyses is flagged under the old or the new definition | ~1 min |

`verify_loyola_v35.py` establishes agreement between the manuscript tables, the canonical CSVs and a fresh recomputation from `octane_data.py`; it does not re-derive the octane values from primary sources (those are checked against `octane_property_provenance_v35.csv` by class rules), and a few checks assert previously observed outcomes (sign patterns of dQ2, provenance agreement counts) as regression guards.

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
| omega- and entropy-source sensitivity (compiled alternatives; 1947 API-44 edition for the six unverified entropies, entropy_api44_sensitivity_v41.csv) | source_sensitivity.py | verify_loyola_v35.py (the two original outputs); the 1947-edition output by re-running the script |
| exploratory transfer (octane -> nonane) | external/transfer_exploratory.py | verify_external.py |
| molecule bootstrap intervals | external/uncertainty_exploratory.py | verify_external.py |
| pre-registered nonane test | external/nonane_validation.py (PREREG_v37.md) | verify_external.py |
| pre-registered boiling-point tests | external/bp/bp_tests.py (PREREG_v40.md) | verify_external.py |
| decane coverage-bias check (included vs excluded) | external/bp/coverage_bias.py | verify_external.py |
| calorimetric dHvap availability (25 outside C8/C9; 1 decane) | external/bp/build_calorimetric_set.py | output committed (calorimetric_dHvap298_alkanes.csv) |
| wide-box solver/selection/dense-grid diagnostics | external/wide_box_diagnostics.py | output committed (wide_box_diagnostics_out.txt) |
| structural counts and witnesses | structural/structural_checks.py | itself (output committed) |
| 32-digit recount of the distinct-value counts (orders 7-17); pure-gamma counts = q-histogram counts | structural/hp_counts.py | itself (hp_counts_out.txt committed) |
| fixed fractional exponents, gamma=0 vs 1 (exploratory) | structural/fractional_points.py | output committed (fractional_points_out.txt) |
| chi floor (orders 7-12) | structural/chi_floor.py | output committed (chi_floor_out.txt) |

## Datasets
| Dataset | Source | Rebuilt / checked by |
|---|---|---|
| 18 octanes (octane_data.py) | NIST WebBook / KDB; per-value provenance in octane_property_provenance_v35.csv | verify_loyola_v35.py (values = appendix = provenance; class rules) |
| 35 nonanes (external/nonane_data.csv) | archived NIST pages external/nonane_raw_nist/ | external/build_nonane_data.py via verify_external.py |
| 100 alkanes C6-C10 boiling points (external/bp/bp_data.csv) | archived NIST pages external/bp/nist_raw/ | external/bp/build_bp_data.py via verify_external.py |
