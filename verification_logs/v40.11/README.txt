v40.11 verification logs (2026-10-06), final v40.11 tree
verify_fast_path.log      python3 verify.py: core verifier, prose numbers, external regression tests (10), baseline tests, constancy check, auxiliary outputs, archived-source identities, interval certificates, provenance-CSV convention, manifest
selftest.log              python3 verify_loyola_v35.py --selftest: 114 attacks, after the terminator-agnostic provenance splitter
structural.log            python3 structural/structural_checks.py with the fail-closed assertions (S2 exact collision, S3 witnesses certified, S4 exception set): exit 0; output committed
lean.log                  formal/verify.sh with locale-independent name comparison: 36 theorem reports
external_verify.log       python3 external/verify_external.py on the final tree (fail-closed data build; hardened press_size): PASS
fractional_points regenerated (was stale since v40.5); audit/check_exploratory_outputs.py now guards it.
Documents: main.tex 42 A5 pages (identifiability clause scoped; no citation of unpublished work), supplement.tex 21 pages.
