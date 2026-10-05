# v40 boiling-point data (acyclic alkanes C6-C10)

- `nist_raw/`: NIST WebBook phase-change pages (Mask=4) for every C6-C10
  acyclic alkane, archived 2026-10-03 (154 pages).
- `nist_alkanes_skeletons_audit.csv`: the audit index (InChI skeleton, NIST ids).
- `build_bp_data.py`: applies the rule pre-registered in `../PREREG_v40.md`
  (NIST AVG; else median of non-compilation determinations if spread <= 3 K;
  else excluded) and derives each structure from its NIST InChI, checked by
  isomorphism against the enumerated trees.
- `bp_data.csv`: 100 included molecules (C6 5, C7 9, C8 18, C9 34, C10 34).
  Grouped-record policy (v40.2, Deviation D5 in ../PREREG_v40.md): all NIST
  pages sharing one InChI are pooled before the rule is applied; this excludes
  3-ethyl-4-methylhexane (two entries 6.40 K apart).
- `bp_provenance.csv`: all 142 molecules with every NIST determination and
  the rule applied or the exclusion reason (31 decanes have no NIST boiling
  point; 10 decanes and 1 nonane have determinations spreading > 3 K).
- `bp_tests.py`: the pre-registered Test A (decane) and Test B (pooled,
  size-adjusted) analyses.
