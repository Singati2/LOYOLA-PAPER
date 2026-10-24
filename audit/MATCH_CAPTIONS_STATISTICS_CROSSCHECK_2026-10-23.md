# Captions and statistics cross-check, 2026-10-23

> **Status.** This is an independent re-verification of `3a5f061`. The reviewer's own scripts and outputs are in the session scratch directory (`valaudit/stats/`), not in the repository. The repository's `audit/independent_recompute_2026-10-23/` scripts were also run.
>
> **Follow-ups applied on the validation branch:**
> - `ss_indep.py` no longer crashes at IRLA. The placeholder `None` is now `(0,0,0,0)`. It reproduces 0.4565, 0.4579 and 0.2745, and gives IRLA 0.2343/0.5066/0.4625.
> - The Table 5 caption says "2000 candidates per model and seed".
>
> **Not changed:** the `tmb_dhvap_audit.csv` row labelled 10.263 lists |r| 0.3736, which is the value computed with the unrounded 10.26291; exact 10.263 gives 0.3735. The text's 0.374 is correct either way. Data files are frozen.

Worktree `wt-val` at 3a5f061, read only. Python `venv-locked2/bin/python -I`. Outputs and own scripts are in `valaudit/stats/` (own code in `valaudit/stats/own/`). Paths below are relative to the scratchpad. Nothing in any worktree was edited. verify.py and the repository's 50-seed pipeline were not run.

Worktree note: `audit/independent_recompute_2026-10-23/rada_ga_partition_check.py` showed up **untracked** at 21:08, after the commit and during this audit. Another process is writing to the worktree. The script is not part of 3a5f061. I ran it anyway (below).

## Input hashes (sha256, first 12)

bp_data.csv 95f48ce0a743 · bp_results_seeds.csv 1cf6e074195a · bp_results_summary.csv cc0ce8a5dc4d · bp_baselines.csv a696189805ff · DATA/octane_properties.csv 0a3c6a7847ca · tmb_dhvap_audit.csv b0b7c45dffe5 · lo_sensitivity_prediction_correlations.csv 131e9f8fb6c4 · lo_sensitivity_degeneracy_order10_trees.csv a4f00e401ded · external/v37_table_rows.tex fa46ffece786 · external/nonane_data.csv 527bf378fd79 · LOYOLA_paper.pdf 870d312a0eb5 · LOYOLA_supplement.pdf c7f4ee6bacf3 · fig_lo_degeneracy_order10_trees_v2.pdf 1a5adc671ca4 (the same file in figures/, both Overleaf trees and submission_candidate).

## 1. The repository's independent-recompute scripts

| Script | Command (S = valaudit/stats) | Output sha256 | Key numbers | Status |
|---|---|---|---|---|
| decane_indep.py | `py -I decane_indep.py external/bp/bp_data.csv S/decane_indep_out.csv` | 8d2554fc5b87… | n=34; medians GM12 0.51371, LOh 0.40587; median ΔQ² −0.071530; wins 15; CI [−0.15584, +0.00148] | VERIFIED: matches the summary CSV to 1e-10 |
| pooled_indep.py | `py -I pooled_indep.py …/bp_data.csv S/pooled_indep_out.csv` | 5b5498a740a8… | n=100; medians GM12 0.977133, LOh 0.976559; median ΔQ² −0.00011339; wins 25; CI [−0.0026358, +0.0019076]; per-seed Q² identical to the repository seeds CSV (max abs diff 0.0) | VERIFIED |
| bp_baselines_indep.py | `py -I bp_baselines_indep.py …/bp_data.csv` (stdout only) | (log) | decane: base −0.0615, IRLA 0.1669, LO1 0.1493, Class 0.1763, Ridge 0.8599; pooled: 0.9385, 0.9627, 0.9627, 0.9668, 0.9911 | VERIFIED: matches bp_baselines.csv |
| octane_indep.py | `py -I octane_indep.py DATA/octane_properties.csv` | (log) | Table 4: all 60 r values agree; 16 profiles and the 2 collision pairs; TMB orig 0.98384, excluded 0.97987, hypothetical 8.5636 gives 0.97607 / LO002 0.96958, sublimation 42.94/4.184 = 10.2629 gives 0.37357; order-10 trees: 106 trees, 79 profiles, degeneracy as in Fig. 1; 45 trees share an LO001 value | VERIFIED |
| ss_indep.py | `py -I ss_indep.py` | (log) | 75 trees; SS/Abr: M1 0.4238, HM 0.4017, R 0.4481, GA 0.4507, LO001 0.4565, LO002 0.4579 (Abr 0.2745). **Crashes at IRLA** (`TypeError: cannot unpack non-iterable NoneType`: the dict entry `"IRLA":None` is unpacked into `(a,b,g,c)`) | PARTLY: the script has a bug. A copy patched in S/own (`None` replaced by a dummy tuple, worktree untouched) gives IRLA 0.2343 / 0.5066 / 0.4625 |
| trees_indep.py | `py -I trees_indep.py` | (log) | orders 7–17: first q-histogram < profiles at order 13 (all trees: 570 vs 566) and order 16 (Δ≤4: 810 vs 809); order 10: 79 profiles, R/LO1/LO2/GA all 79; GA merges distinct q-histograms only at n=17 (all trees) | VERIFIED: consistent with the text and Table 2 |
| rada_ga_partition_check.py (untracked) | `py -I … ` (N=60) | — | partitions induced by GA, q and γq coincide for n=2..60 | VERIFIED; the file is not in the commit |

## 2. Own fresh checks (separate code)

| Claim | Source | Command | Result | Status |
|---|---|---|---|---|
| Test A: median ΔQ² −0.072, LO ahead in 15/50 | bp_results_seeds.csv | `own/own_seed_summary.py seeds.csv summary.csv` | −0.0715304490, 15 wins, 0 ties; the four per-model medians equal the summary CSV | VERIFIED |
| Test B: −0.0001, 25/50 | same | same | −0.0001133864, 25 wins, 0 ties | VERIFIED |
| Test A interval [−0.156, +0.001] reproduced with the repository's method | bp_tests.py `boot_ci`: 2000 molecule resamples, rng 20261005, statistic = median over seeds of Q²(LOh)−Q²(GM12) on the resample, conditional on the fixed outer predictions, percentile 2.5/97.5 | `own/own_decane.py bp_data.csv seeds.csv S/own_decane_out.csv`: brute-force double LOO with explicit delete-one refits (no leverage identity), own descriptor, same candidate streams (LO2 and GM2 draws consumed first) | per-seed Q² matches the repository seeds CSV to within 5e-11 for all 50 seeds; median −0.0715304490; 15 wins; CI [−0.15584287, +0.00148413]; output file byte-identical to decane_indep_out.csv (sha 8d2554fc…) | VERIFIED |
| Test B interval [−0.003, +0.002] | needs the outer predictions, which are not stored | pooled_indep.py (above); no second own implementation of pooled (cost) | [−0.0026358, +0.0019076] (pooled_indep, which reimplements boot_ci); matches the summary CSV | VERIFIED |
| Q² = 1 − PRESS/SS_tot about the full-sample mean | external/baselines.py `scores` (press, ss=((y−y.mean())²).sum()); bp_tests.py `q2` | read the code plus a numeric check | Test A "Base" (training-fold mean) Q² = −0.0615243 = 1 − (34/33)², which holds only when SS_tot is taken about the full-sample mean; octane/nonane Mean −0.1211 = 1−(18/17)², −0.0597 = 1−(35/34)² | VERIFIED |
| Ordinary vs nested labelling (Table 5) | bp_tests.py `baselines()` | read the code | Base, IRLA and LO1 are single-candidate (fold_select_ols/nested_size with one row = ordinary LOO); Class., Ridge (inner-LOO λ), GM12 and LOh are nested | VERIFIED |
| TMB 10.263 gives max \|r\| 0.37353 (text 0.374) | DATA/octane_properties.csv, own SMILES parser and LO sum | `own/own_tmb.py octane_properties.csv` | 10.263: LO001 0.37353, LO002 0.33167; excluded 0.97987 (LO002 0.97953); hypothetical 8.56358: 0.97607, LO002 0.96958 → 0.970; original 0.98384 | VERIFIED. Nit: tmb_dhvap_audit.csv labels the row 10.263 but lists 0.3736, which is the value for the unrounded 42.94/4.184 = 10.26291 (0.37357). The exact 10.263 gives 0.37353 → 0.3735. The text's 0.374 is right either way |

## 3. Tables and figure against their sources (`own/own_tables.py wt-val`)

| Item | Source | Result | Status |
|---|---|---|---|
| Table 1 (20 cells) | DATA/octane_properties.csv | 20/20 match | VERIFIED |
| Table 4 (60 cells, 5 bold) | lo_sensitivity_prediction_correlations.csv | 60/60 match; bold = argmax \|r\| per column (mM2, mM2, LO001, HM, M2); independently recomputed by octane_indep | VERIFIED |
| Table 5 (18 cells) | bp_baselines.csv, bp_results_summary.csv; also bp_table_rows.tex | 18/18 match; the rows are identical to bp_table_rows.tex | VERIFIED |
| Figure 1 | lo_sensitivity_degeneracy_order10_trees.csv; pdftotext of the figure PDF | bar labels 83.0, 67.0, 37.7, 47.2, 25.5, 27.4, 34.0, 36.8, 25.5×4 equal the CSV (83.02 … 25.47); distinct-value counts recomputed (18, 35, 66, 56, 79, 77, 70, 67, 79×4); floor 79/106 | VERIFIED |
| Table S7 (56 cells) | v37_table_rows.tex (identical, 7 rows); 42 cells checked directly against baselines_*.csv and v37_classical_fixed.csv; LO1 column recomputed (`own/own_lo1_q2.py`: 0.5915, 0.6393, 0.9572, 0.7852, 0.8227, 0.4088, 0.9031); LO>GM counts against expanded_robustness_summary_v35.csv and nonane_validation_summary.csv (53/64, 14/24, 100/100, 34/31, 26/28, 58/63, 95/98) | all match | VERIFIED |

140 table cells were compared programmatically, with 0 mismatches.

## 4. Caption edits in 3a5f061

| Edit | Check | Result | Status |
|---|---|---|---|
| Table 1: "differ in every tabulated property, including the measured boiling point" | both pairs, 5 columns | 3-/4-methylheptane: 118.9/117.7, −50.82/−50.69, 9.52/9.48, 111.26/109.32, 0.371/0.372; 3,4-dimethylhexane / 3-ethyl-2-methylpentane: 117.7/115.6, −50.91/−50.48, 9.32/9.21, 106.59/106.06, 0.340/0.330. All 10 comparisons differ | VERIFIED |
| Table 5: LO_h "registered Loyola model, … box of the hybrid control …: (α,β)∈(−12,12)², γ∈(−2,2), 2000 candidates per seed" | bp_tests.py `streams` (BUD=2000; hy = U(−12,12)², U(−2,2)); PREREG_v40.md l.26–29 ("2000 candidates per model", "LOh: Loyola hybrid, (alpha,beta) ~ U(−12,12)^2, gamma ~ U(−2,2)"); main §ablation l.1267 and box_sensitivity.py l.7–8 (the same hybrid box) | consistent. Nuance: "per seed" means per model per seed, which is how the prereg states it | VERIFIED |
| Table S7: "nested wherever an index, a point or a penalty is selected" | external/baselines.py `analyse` | Mean = fold_mean (ordinary); Class. = fold_select_ols over 10 classical (nested); IRLA = fold_ols (ordinary); Ridge = fold_ridge with inner-LOO λ (nested); LO1 = fit_predict, fixed (ordinary, make_v37_table.fixed_lo1_q2); GM/LO = fold_select_ols over the candidates (nested) | VERIFIED: the caption matches the code exactly |
| Table 5 caption (same phrase) | bp_tests.py | see §2 | VERIFIED |

## 5. S1/S2 edit: "0.745 for the best fixed index chosen within each fold"

The source is the supplement Table S2 caption (supplement.tex l.411) and text l.407, l.428. No CSV holds this number; verify_loyola_v35.py checks only the 0.764 (dec_LOO) and the non-nested LOO_fix 0.781. My own recomputation (`own/own_bestfixed_nested.py`): in each LOO fold the index with the largest training-fold \|r\| is picked from the 12 indices of RED, refitted by OLS and used to predict the held-out isomer, and \|r(pred, y)\| is reported. T_B: **0.7455** (mM2 picked in 17 folds, LO(0,0,1) in 1). S: 0.9498 (HM 14, M1 4). Non-nested mM2: 0.7805. So 0.745 is a fold-nested LOO *correlation*, not Q². The old wording "0.745 for mM2" was slightly wrong because one fold picks LO(0,0,1), and the new wording is accurate. **VERIFIED**.

## 6. PDFs (pdftotext; no compile)

| Check | Result | Status |
|---|---|---|
| Page counts | LOYOLA_paper.pdf 37 pp; LOYOLA_supplement.pdf 39 pp | VERIFIED |
| "??" anywhere | 0 occurrences in both | VERIFIED |
| Edited reference to Table S6 | The edit is in Section **S3** (Matched-budget comparison), not S6. It renders "(Section 6.2 of the main paper and Table S6)", and Table S6 is the search-box sensitivity table (tab:box), the correct target | VERIFIED; the task's "Section S6" is really S3 |
| PDFs contain the 3a5f061 edits | Table 1 caption ("…every tabulated property, including the measured boiling point"), Table 5 "2000 candidates per seed", "nested wherever" in Table 5 and Table S7, "best fixed index chosen within each fold", "10.263 kcal mol−1", "0.374 or below" all present | VERIFIED |
