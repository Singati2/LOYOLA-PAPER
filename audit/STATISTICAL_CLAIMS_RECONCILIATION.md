# Statistical claims reconciliation (2026-10-17)

Every claim below traces to committed outputs. "Independent check" means a recomputation, or a reading of
the code, done in this review. Nothing frozen was rerun: no protocol, cohort, seed, estimand or
threshold was changed. The corrected sentences are in `main.tex`, `supplement.tex` and
`drafts/short/body.tex` on branch `review/short-version`.

## Design facts checked

| Item | Evidence | Status |
|---|---|---|
| Ridge baselines are fully nested | λ is taken from a fixed log-grid by inner LOO inside each outer fold; standardisation uses training statistics; the intercept is not penalised (`external/baselines.py`, `external/bp/bp_tests.py`; statistics reviewer) | VERIFIED (code reading) |
| Permutation test | p = (b+1)/(B+1) = 1/201 with b = 0 and B = 200; λ is re-chosen in every permutation; an independent sklearn re-implementation is in `audit/permutation_pipeline_audit_out.txt`. It tests association, not ridge against the indices | VERIFIED |
| Registered molecule bootstrap | Resamples molecules over fixed outer predictions, takes the median over 50 seeds, omits refitting and selection. The paper says so | VERIFIED |
| Nonane bootstrap is post hoc | `external/PREREG_v37.md` contains no bootstrap | VERIFIED (grep) |
| Selection-aware resampling | One fresh candidate stream per replicate: `bp_tests.streams(r)` in `external/bp/selection_resampling.py` | VERIFIED (code) |
| The resampling range on the pooled set is mostly optimiser noise | Seed-to-seed spread of LO_h − GM12 on the full data, from `external/bp/bp_results_seeds.csv`: pooled 2.5–97.5 % [−0.0139, +0.0080], sd 0.006; decanes [−0.364, +0.083], sd 0.136. Resampling ranges: pooled [−0.015, +0.008]; decanes [−0.510, +0.312] | VERIFIED (recomputed) |
| On trees, p₃ = Σ_uv (d_u−1)(d_v−1) | A path of length 3 is fixed by its middle edge | VERIFIED (proof) |
| Octane ridge is weaker than the best single index | Supplement Table S7: T_B 0.344 against 0.662 (GM); ΔH_f 0.654 against 0.831; S 0.721 against 0.905; ω 0.851 against 0.979; ΔH_vap 0.954 against 0.957 (level) | VERIFIED (table) |
| LO − ridge intervals on the nonanes | `external/uncertainty_exploratory.csv`: ΔH_vap [−0.101, +0.032]; T_B [−0.398, +0.325]. Both include 0 | VERIFIED (CSV) |
| Data reuse | The half-width-12 box was chosen from the octane **and** nonane curves; LO(0,0,1) was singled out on the octanes; M_{4.5,−9} was read off the selections; Test B reuses the octane and nonane boiling points. All are disclosed in both versions | VERIFIED (text) |
| γ ∈ {1, 2} fixed before the octane data were seen | Cannot be documented: the history begins at v35 with the octane results present | **NOT VERIFIABLE**; disclose in the text (open item) |

## Claims: before and after

| # | Claim (before) | Problem | Corrected sentence (now in the text) | Status |
|---|---|---|---|---|
| 1 | Table caption: "The registered intervals … understate the uncertainty several-fold" | It compares a median-over-50-seeds interval with single-stream resampling ranges, which the text itself calls not comparable. On the pooled set the range is seed noise | "…conditional on the fitted predictions and omit refitting and selection uncertainty (see below)", plus "Each replicate uses a single candidate stream, so the ranges also contain optimiser variance" | FIXED (main and short) |
| 2 | "ridge regression on the degree-pair counts leads/outperformed every single index" (contribution (vi), Section 6.4, conclusion) | No interval for ridge against the indices in the paper. The claim is limited to boiling points (it is false on the octanes) | Scoped to measured boiling points and stated "in point estimate". "The margin is large on the decanes and small on the pooled set, where size alone gives Q² = 0.938, and no interval for these differences is reported here." | FIXED |
| 3 | Supplement S4: "Ridge … predicts the nonanes better than every index model" | Its own conditional intervals include 0 | "has the highest point estimate … the conditional intervals for LO minus ridge include zero for both" | FIXED |
| 4 | "A term linear in the imbalance is what matters for this property" (main 6.3; supplement S4) | The wide-box parent, which has no linear-q term, reaches 0.942 and 0.892 | "suffices … in point estimate, but it is not necessary" | FIXED |
| 5 | Wiener: "distance information beyond the degree pairs carries much of the remaining signal" | p₃ is a function of the degree-pair counts; only W adds distance information; W+p₃ against ridge is unresolved | Identity stated; "W may add to the degree-pair information; its difference from ridge is not resolved here" | FIXED |
| 6 | Test B secondary: "both tuned models do (0.977)" | No interval and no registered decision rule | "have higher point estimates (0.977; no interval was registered for this secondary question)" | FIXED |
| 7 | "matches or beats the tuned Loyola model" | Point estimates | "…in point estimate" | FIXED |
| 8 | Local tuning on octane T_B (0.764 against 0.745) | A nested-LOO point difference with no interval. The ±0.161 bootstrap half-width of Supplement Table S2 refers to the in-sample gain, so it cannot be compared with this difference (the reviewer's first suggested wording made that comparison and was not adopted) | "a small point-estimate difference without an interval; no superiority is claimed" | FIXED (main) |
| 9 | "every single index stays between 0.149 and 0.514" | Medians for the tuned models | "(medians over seeds for the tuned models)" | FIXED |
| 10 | Table caption "n_C in every model" | Ridge uses the counts only (their sum is n_C − 1) | Caption corrected | FIXED |
| 11 | Supplement: "no γ effect remains to be established" | Ambiguous | "no γ effect is established" | FIXED |
| 12 | Nonane bootstrap not marked post hoc | Not registered | "A post hoc molecule bootstrap…" | FIXED |

Unchanged, because they are correctly worded:
* the pre-registered verdicts (decanes −0.072, 15/50, [−0.156, +0.001]; pooled −0.0001, 25/50,
  [−0.003, +0.002]);
* the nonane "replicates" verdict, reported as obtained with its seed-count caveat;
* "no gain demonstrated … not equivalence … do not show that γ never helps";
* the absence of a registered equivalence margin;
* the 2-D against 3-D budget handicap.

## Outstanding

* Ridge against single-index intervals. The statistics reviewer's conditional bootstrap, not reproduced
  here, gives ridge minus best classical on the decanes [+0.47, +1.10] and on the pooled set
  (size + classical) [+0.014, +0.042]. Prior-audit item B2 gives ridge minus median GM12 of +0.346
  [+0.160, +0.747] on the decanes and +0.014 [+0.008, +0.024] pooled. Adding them would support the
  boiling-point claim with intervals; this needs a registry entry and is **not done**. It is exploratory.
* Multiplicity: the 12 × 5 octane correlations are described as descriptive with unadjusted intervals,
  which is acceptable. No inferential claim rests on them.
* Does the QSPR part support the resolution-limit story? Only indirectly. The boiling-point result
  (counts ≫ any single index, including every degree-ratio index) agrees with the ceiling/floor picture.
  The collisions at order ≥ 13 or 16 never occur in the data sets (n ≤ 10), so the experiments do
  **not** test the minimal-order theorem. Say so explicitly if the QSPR section is kept.
