v40.9 verification logs (2026-10-06), final v40.9 tree
verify_fast_path.log      python3 verify.py: core verifier, prose numbers, external regression tests, baseline tests, constancy check, provenance-CSV convention, manifest
selftest.log              python3 verify_loyola_v35.py --selftest (114 attacks) on the final verifier: after the figure-warning change, the restored CRLF convention of the provenance CSV (the v40.7/v40.8 self-test logs predate the LF rewrite that this fixes), the tuning-table parser hardening and its new attack
bp_rerun.log              external/bp/bp_tests.py with the explicit least-squares size_only: byte comparison of the three output CSVs with the committed ones
external_verify.log       python3 external/verify_external.py on the final tree (second replay, after the all-non-finite guards were added; the first replay with the new size_only also passed)
dataset_rebuild.log       nonane and boiling-point datasets rebuilt from the archived NIST pages in a temporary copy and compared byte-for-byte with the committed files; octane module = appendix table = provenance paper_value (90 values)
Documents unchanged since v40.8 (42 + 21 pages).
