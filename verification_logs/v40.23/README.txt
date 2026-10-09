v40.23 verification record (all outputs and exit statuses checked).

1. verify_everything_run1.log: python3 verify.py --everything on the frozen tree. 20 of 21 stages PASS
   (21 PASS lines including the CSV convention line); the isolated replay flagged two bookkeeping problems:
   external/bp/selection_resampling.py defaults (200/100 replicates) differed from the run reported in the
   paper (500/200), and the counter-attack record (which stores the registry size, 697 -> 717) had been
   rewritten by the run. Process exit=1.
2. Fix: defaults set to 500/200; new counter-attack record committed; manifest refreshed. No reported number
   changed.
3. verify_fast_path.log: python3 verify.py on the fixed tree. ALL PASS, exit=0.
4. run_all_scripts.log: python3 audit/run_all_scripts.py on the fixed tree. Every script (44) exits 0 and
   reproduces its committed outputs, exit=0. The other --full stages (external verifier, structural checks,
   32-digit recount, self-test, 13 counter-attacks, labels, Lean with 38 axiom checks) passed in run 1 on a tree
   that differs only in the two files above.
The SHA-256 manifest was rewritten after these logs and this file were final.
