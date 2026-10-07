v40.19 verification record.
- verify_fast_path.log: python3 verify.py on the v40.19 tree (ALL PASS), recorded before the final manifest write.
- verify_everything.log: python3 verify.py --everything on the same tree (commit ed8aa92): core verifier, prose
  numbers, regression and baseline tests, constancy check, auxiliary outputs, archived-source identities, interval
  certificates, prose style, manifest, external verifier, structural checks, 32-digit recount, verifier self-test,
  13 counter-attacks, labels and references, Lean proofs (36 theorems): all PASS.  The last step (every script
  replayed in isolation) reported one problem: audit/attack_checks_out.txt, which the counter-attack step of the
  same run had just rewritten with new runtimes and the current registry size, no longer matched its committed hash
  inside the replay snapshot.  The record is now written without runtimes (audit/attack_checks.py) and the replay
  was re-run alone afterwards: audit/run_all_scripts_out.txt, "every script exits 0 and reproduces its committed
  outputs" (38 scripts).
