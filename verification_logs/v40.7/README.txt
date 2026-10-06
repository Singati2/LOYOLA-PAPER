v40.7 verification logs (2026-10-05), all on the final v40.7 tree
core_verify.log          python3 verify_loyola_v35.py: FULL PASS, 0 failures
selftest.log             python3 verify_loyola_v35.py --selftest: 113/113 attacks rejected (after the constancy-guard change)
external_verify.log      python3 external/verify_external.py (allowlist comparator from pull request #1): see last line
structural.log           python3 structural/structural_checks.py (with s3_certify): exit 0; output committed as structural_checks_out.txt
hp_counts.log            python3 structural/hp_counts.py: all counts reproduced at 32 significant digits (Table 2, Section 5, Table S4)
regen_core_scripts.log   byte-identity of the regenerated CSVs of expanded_robustness_v35.py, tmb_exclusion_sensitivity.py and external/nonane_validation.py after the constancy-test / D4-parser changes
constancy_test_check.log python3 constancy_test_check.py: neither constancy definition flags any candidate
test_regressions.log     python3 external/test_regressions.py: 6 tests OK
Documents: main.tex 42 A5 pages, supplement.tex 21 pages; 0 undefined references, 0 overfull boxes (tectonic).
Lean sources unchanged since v40.5 (verification_logs/v40.5/lean.log remains valid).
