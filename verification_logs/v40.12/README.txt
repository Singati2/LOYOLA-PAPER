v40.12 verification logs (2026-10-06), final v40.12 tree
verify_fast_path.log      python3 verify.py (core verifier, prose numbers, regression tests, baseline tests, constancy check with the corrected 17-molecule fold set, auxiliary outputs, source identities, interval certificates, CSV convention, manifest)
external_verify.log       python3 external/verify_external.py after the coverage_bias.py lookup and build_nonane_data.py message changes: PASS; every regenerated output byte-identical
Affected outputs re-run and compared before the replay: coverage_bias.csv, nonane_data.csv, nonane_provenance.csv, calorimetric_dHvap298_alkanes.csv all IDENTICAL; constancy_test_check_out.txt regenerated (35 folds).
attack_checks.log         python3 audit/attack_checks.py: 13 attacks, 13 rejected (output committed as audit/attack_checks_out.txt)
run_all_scripts.log       python3 audit/run_all_scripts.py: every script replayed in isolation (output committed as audit/run_all_scripts_out.txt)
Verifier, structural scripts, Lean sources and manuscripts unchanged since v40.11 (their v40.11 logs remain valid).
