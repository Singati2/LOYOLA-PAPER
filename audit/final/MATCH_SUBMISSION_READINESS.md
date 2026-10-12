# MATCH submission readiness (v40.29)

Manuscript: "The Loyola Index Family and the Resolution Limit of Degree Imbalance"
(main.tex, 40 A5 pages; supplement.tex, 27 pages). Review base: commit 0817f35 (v40.28); all
dispositions below are applied in v40.29 unless marked otherwise.

Companion reports in this folder: `FINAL_DATA_PROVENANCE_AUDIT.md`,
`FINAL_MATHEMATICAL_REFEREE_REPORT.md` (Section 10 is the novelty assessment),
`FINAL_CODE_STATISTICS_AUDIT.md`. Independent scripts are in `scripts/`.

## 1. How the review was done

1. Four independent audits of 0817f35: data provenance, mathematics, code and statistics, novelty.
   Each auditor wrote its own check code and did not import the repository's checkers.
2. A leakage audit of every experiment (preprocessing, selection, boxes, duplicates, transfer,
   seeds, data construction, permutation test).
3. A review panel: four referees with distinct briefs (graph theorist, QSPR statistician, handling
   editor, adversarial referee), an anonymous peer ranking of the four reports, an authors'
   counter-attack issue by issue, and a chair ruling on each issue.
4. Three findings from an outside audit log (a conditioning defect in `press_size`, the scope of the
   calorimetric count, a repeated NIST row), and a later independent audit of 0817f35 with nine
   findings (Section 3, items marked A).

The reviews were not independent in the way separate human referees are, so agreement between them
was treated as a lead and not as evidence. Every finding listed as confirmed below was re-checked directly, by reading the
source, by an independent computation or against the primary source.

## 2. Verdict

No mathematical error was found. Every exact statement tested reproduced exactly: collision orders
13 and 16 (exhaustive enumeration to order 17), all counts of Table 2 (recounted at 50 to 60 digits),
the five crossings (interval arithmetic), the ranks 7, 7 and 8, the octane floor SSE = 117/40, the
extremal trees and the Lean build (38 theorems on the standard axioms). No registered value and no
pre-registered verdict changes in v40.29.

The predicted editorial outcome is major revision on significance and length, not on correctness.
The paper itself states that gamma adds no graph information beyond the degree-pair counts, that no
predictive gain was demonstrated, and that GA ties the pure-gamma points below order 17. The
strongest defensible contribution is the explicit colliding trees at orders 13 and 16, which bind
every degree-ratio index (including the degree-ratio Sombor index of four MATCH 97 papers), together
with the five-crossing bound, Proposition 3.8 and the registered negative evidence.

Recommendation: freeze the manuscript after v40.29. The remaining items are author decisions
(Section 5), not defects.

## 3. Issues by severity

Status: FIXED (changed in v40.29), DOCUMENTED (kept, with the limitation stated), AUTHOR (decision
for the authors), OPEN (unresolved question).

### Submission-critical (all fixed)
| # | Issue | Evidence | Status |
|---|---|---|---|
| C1 | Supplement said acentric factors "were taken from KDB-derived compilations"; 15 of 18 do not match KDB exactly and TMB matches neither KDB (0.251) nor Ediz 2017 Table 1 (0.25529) | supplement.tex, Section S1 and item (v) of S8; Ediz 2017 Table 1 read directly | FIXED: described as compiled values of unidentified origin, within 0.005 of both compilations except TMB |
| C2 | Supplementary Table S8 caption: "Tuning does not exceed the best fixed index under LOO on any property" is false once the fixed choice is nested (T_B: fixed 0.745, tuned 0.764) | verify_loyola_v35.py:1112 selects on all 18; nested recomputation | FIXED: caption and two text passages state the nested values |

### Should fix (all fixed unless marked)
| # | Issue | Status |
|---|---|---|
| S1 | Selection guard of `external/baselines.py` rejected well-resolved candidates after a translation (expected failure since v40.26) | FIXED: resolution guard; 12 callers byte-identical; 16 to 17 regression tests pass, none expected to fail |
| S2 | `press_size` accepted designs nearly collinear with n_C and returned a PRESS wrong by several percent | FIXED: threshold 1e-6; smallest ratio on data 4.6e-4; 20,300 calls, max deviation from QR 7e-11, no selection changes (audit/final/scripts/press_size_probe.py and _out) |
| S3 | "The colliding families ... are new" overclaimed the pendant-path propagation, which is Rada 2026's device | FIXED (main.tex, comment after Theorem 3.5) |
| S4 | Contribution list presented elementary facts and a known ceiling as contributions | FIXED (items (i) and (iv)) |
| S5 | Abstract and conclusion stated the minimal orders as fact although they rest on enumeration | FIXED ("by exhaustive enumeration") |
| S6 | Lean coverage of the termwise bounds overstated | FIXED (edgewise extrema of bracket and ratio bounds are hypotheses) |
| S7 | Stale theorem numbers after Remark 4.2 was added | FIXED (LEAN_VERIFICATION.md, README.md, REPRODUCE.md, notebook 02) |
| S8 | TMB excluded: "LO(0,0,1) stays first" ranks a 0.0004 margin the paper elsewhere declines to rank | FIXED (level at three decimals, 0.9799 against 0.9795) |
| S9 | TMB 8.41 "consistent with" a supercooled liquid; it lies 0.15 below the estimate | FIXED ("lies just below") |
| S10 | 3-ethyl-4-methylhexane second T_B unexplained | FIXED: it is the d-enantiomer entry, TRC 2 K against 0.5 K (NIST pages in external/bp/nist_raw) |
| S11 | Nonane enthalpy sources: NIST lists 25 values as Reid 1972 | FIXED (Reid 1972 cited, doi 10.1002/aic.690180637, verified) |
| S12 | Calorimetric count "only 25" not scoped (the audit covered C4 to C16) | FIXED |
| S13 | Wide-box disappearance and permutation test wording ("thus") | FIXED (exploratory label; "thus" removed) |
| S14 | Octane S 11 to 38 wins attributed to optimiser variance; it reflects the protocol change | FIXED |
| S15 | Nonane ridge "predicts better" is a point estimate | FIXED |
| S16 | Missing classical boiling-point baseline: Wiener W + p3 gives Q2 = 0.904 on the decanes, above ridge (0.860) | FIXED: added with script `external/bp/wiener_baseline.py`; Wiener 1947 cited (doi 10.1021/ja01193a005) |
| S17 | Interval reading ("one-sided") undefined; registered intervals understate uncertainty | FIXED (lower end of the two-sided 95% interval; caption note) |
| S18 | Test B dQ2 printed as -0.000 | FIXED (-0.0001, and 101-cohort value from the changelog) |
| S19 | Wide box lowers the parent on T_B, so it is not uniformly favourable to the parent | FIXED (one sentence) |
| S20 | LO(0,0,1) and M_{4.5,-9} singled out on the octanes; Q2 0.949 is post-selection (nested 0.938 to 0.942) | FIXED |
| S21 | Remark 3.10: subset step unproved | FIXED (argument added and checked) |
| S22 | Bibliography abbreviations (Discrete Appl. Math., Iran. J. Math. Chem., Ars Combin.); Table 2 footnote letters skipped c | FIXED |
| S23 | M-polynomial and exponential-index inequality literature uncited | FIXED (Deutsch and Klavzar 2015; Carballosa et al. 2023, both verified) |

### From the independent audit of 0817f35 (items A)
| # | Issue | Status |
|---|---|---|
| A1 | Repeated NIST row, 2,2,6-trimethylheptane | MITIGATED; SOURCE UNRESOLVED (see O1): registered value kept, sensitivity reported |
| A2 | NIST averages (57 of 100 values) bypass the 3 K screen; quoted uncertainties up to 6 K | MITIGATED; SOURCE UNRESOLVED: disclosed in Supplement S9 with an exploratory variant (decane ridge 0.863 without the two averages quoting more than 3 K). Excluding those two does not validate the other 55 averages |
| A3 | Calorimetric count broader than the C4-C16 search | FIXED (S12) |
| A4 | Calorimetric census not rebuildable from raw pages | MITIGATED; SOURCE UNRESOLVED: DATA/README.md and REPRODUCE.md call it a census of a curated index |
| A5 | `press_size` inverts A'A; nearly collinear designs crash or err | FIXED (S2); the audit's reproducer is now rejected cleanly and an accepted case matches QR |
| A6 | Selection guard translation defect; final size refit used raw n_C (a shift of 1e8 changed the prediction) | FIXED: both; regression tests added; outputs unchanged |
| A7 | 2,3-dimethylhexane entropy labelled agreement but matched only to a secondary compilation; the 1947 API value differs by 1.91 | CLASSIFICATION FIXED; SOURCE UNRESOLVED: reclassified CANNOT VERIFY (1947 entry: NBS Circular 461 Table 3p, printed p. 159, ideal gas at 25 C, 106.11 cal/(deg mole), against 108.02 used, difference +1.91; the value used is not verified against any primary source); seven entropies now, API-44 sensitivity rerun with seven (max shift 0.016, M1 ahead of HM by 0.005); classification labels documented as numerical agreement, not source authority |
| A8 | InChI parser accepted repeated atoms and bonds | FIXED: occurrence and repeated-bond checks; rebuild reproduces all 100 molecules; regression test added |
| A9 | Standing hypothesis admitted K1; Lean map pointed to the wrong script for closed forms | FIXED |

### Finding-to-change map (independent audit of 0817f35)
Every row was re-checked after the change. "Byte-identical" means the rerun output files equal the committed ones.

| Finding | Changed files | Regression test or check | Numerical impact | Remaining limitation |
|---|---|---|---|---|
| A1 repeated NIST row, 2,2,6-trimethylheptane | DATA/README.md; audit/final/scripts/bp_duplicate_sensitivity.py (+ _out) | sensitivity script in audit/run_all_scripts.py | none on registered results; exploratory 148.2 to 148.4 degC moves decane ridge Q2 0.8599 to 0.8591, pooled 0.9911 unchanged | registered median rule kept; the original Marschner and Carmody (1951) paper was not consulted, so whether the two 421.15 K rows are separate samples is unresolved |
| A2 NIST averages bypass the 3 K screen | supplement.tex (S9); same sensitivity script; prose_claims_a.py (v4029_avg57, v4029_avg6K, v4029_qual863) | prose-number registry (733 checked, 0 failures) | none on registered results; exploratory decane ridge 0.863 without the two averages quoting more than 3 K (pooled 0.9909) | individual-point pages behind the 57 averages are not archived; uncertainty is not a machine-readable field |
| A3 calorimetric count broader than the search | main.tex (Section 6.4 sentence); prose_claims_a.py (bp_cal25 re-anchored) | prose-number registry | none (count unchanged, scope stated as C4 to C16) | no search beyond C16 (the audit's C17 heptadecane example is outside scope) |
| A4 calorimetric census not rebuildable from raw pages | DATA/README.md; REPRODUCE.md | documentation only | none | phase-change pages outside C6 to C10 are not archived; the census is reproducible from the curated index only |
| A5 press_size inverts A'A | external/bp/bp_tests.py (threshold 1e-10 to 1e-6) | external/test_regressions.py: test_press_size_near_collinear (60-digit reference); audit/final/scripts/press_size_probe.py (every published call compared with QR) | byte-identical Test B outputs; 20,300 calls, smallest ratio 4.6e-4, max deviation from QR 7e-11, no selection change | normal equations are still used inside the accepted range (condition number of A'A at most 1e12); a QR rewrite was not adopted because it would perturb last digits of committed outputs |
| A6a selection guard not translation invariant | external/baselines.py (resolution guard) | test_selection_translation_invariance (formerly expected failure), test_rounding_noise_rejected, test_small_relative_range_accepted; audit/final/scripts/adversarial.py | byte-identical outputs in all 12 callers; old and new masks never differed on 395,987 guard calls | exact translation invariance is impossible for any noise-rejecting guard; translations that leave fewer than 1024 resolvable steps are rejected by design |
| A6b final size refit used raw n_C | external/bp/bp_tests.py (fit_pred_size standardises n_C) | test_size_refit_translation | byte-identical bp_tests and selection_resampling outputs | none known |
| A7 2,3-dimethylhexane entropy labelled agreement | octane_property_provenance_v35.csv and DATA copy; source_sensitivity.py; entropy_api44_sensitivity_v41.csv; main.tex; supplement.tex; DATA/README.md; verify_loyola_v35.py (expected counts 39/8) | core verifier provenance-count check; prose-number registry | counts 40/7 to 39/8; seven entropies unverified; API-44 sensitivity recomputed with seven substitutions, a numerical change: max shift 0.016 (was 0.018), M1 ahead of HM by 0.005 (was 0.004); no registered test uses entropy | the count check confirms consistency with the CSV, not the source; the 1947 value 106.11 was read from NBS Circular 461 Table 3p, and no later primary determination was located |
| A8 InChI parser accepted repeats | external/bp/build_bp_data.py | test_inchi_parser_rejects_repeats; full rebuild | rebuild reproduces all 100 molecules and every committed bp file | none known |
| A9 K1 standing hypothesis; Lean pointer | main.tex; LEAN_VERIFICATION.md | label and build checks | none | none |

### Optional or documented
| # | Issue | Status |
|---|---|---|
| O1 | 2,2,6-trimethylheptane: NIST repeats one row; the registered median rule gives 148.2 degC, counting it once gives 148.4 (decane ridge 0.8599 to 0.8591, pooled unchanged) | DOCUMENTED (DATA/README.md; script in scripts/) |
| O2 | Seven octane entropies cannot be matched to a primary source; API-44 values differ by 0.07 to 2.2 | DOCUMENTED (sensitivity exists; S ordering not interpreted). A check of Scott 1974 is optional |
| O3 | Compiled-only nonane dHvap analysis would read "mixed" | DOCUMENTED in FINAL_DATA_PROVENANCE_AUDIT.md (verdict already discounted in the paper) |
| O4 | Wide-box comparison uses random search; equal budgets are not equally thorough in 2 and 3 dimensions | DOCUMENTED (stated in Section 6.2; conclusion now says "under random search at matched budgets"). A gamma-grid control is optional |
| O5 | Grouped CV by count vector not reported | DOCUMENTED here: Q2 moves by at most 0.01 |
| O6 | One PDF-bookmark warning from math in a section title | harmless |
| O7 | The open question of five crossings for Delta <= 4 | OPEN (stated in the paper) |

## 4. Verification record (v40.29)
Recorded in `verification_logs/v40.29/` after the full run: commands, environment versions,
outputs, skipped tests and expected failures (none remain), commit SHA.

## 5. Author decisions (cannot be fixed by editing)
1. Structural cuts (about 15 to 25 pages, deleting Section 6 or Section 5 material, renaming the
   family): declined. Every referee on the panel raised length; a MATCH referee may still ask.
2. AI-use disclosure: the manuscript has none, and the repository rule excludes tool mentions. Check
   the current MATCH instructions and decide.
3. Acknowledgment ("The authors thank colleagues for helpful discussions") is a placeholder; add
   funding and conflict-of-interest lines if required.
4. Archive DOI: mint a Zenodo DOI for the tagged release and add it with the commit hash to the
   data-availability statement and to the LoyolaRepo reference.
5. Cover letter: lead with the corollary on degree-ratio indices, which binds the MATCH 97
   degree-ratio Sombor papers, and present the registered negative evidence as part of the result.
6. Coauthor approval of v40.29.
7. The MATCH template prints "(Received <compile date>)" through \date{\today}; follow the
   journal's template instruction.
