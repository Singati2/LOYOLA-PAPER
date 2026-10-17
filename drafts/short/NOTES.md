# Short version of the paper: draft notes (2026-10-17)

**Superseded in part by `SHORT_VS_FULL_CHANGELOG.md`, which gives the current maps. This file keeps the
revision history of the draft.** Revision 3: new title; abstract states what is known and what is new;
SDD/ISDD early-failure caveat; Cruz–Rada corollary with a complete check; γ-choice disclosure;
`supplement_short.tex` built by `build_supplement.py`.

`main_short.tex` → `main_short.pdf`: 24 A5 pages (full paper: 43). `python3 build.py` assembles it
from `body.tex`, the preamble and title block of `main.tex` (byte-identical) and the bibliography
entries it cites. Then run `pdflatex main_short.tex` three times. The full paper and the Supplement
are unchanged.

## Framing
The draft opens with the resolution limit of degree-ratio indices: every such index depends only on
the q-histogram, which loses degree-pair information from tree order 13 (16 for chemical trees).
The Loyola family is the vehicle for the study, not a proposed better predictor.

## Rules followed
* No new number. Every numeric token of `body.tex` occurs verbatim in `main.tex` or `supplement.tex`
  (checked by script).
* No claim strengthened. After an independent comparison against `main.tex`, all qualifiers of the
  full paper's QSPR section were restored (see "Revision 2").

## Revision 2 (after independent review)
* The ridge claim now has the full paper's scope. On measured boiling points ridge leads every
  single index. On the octanes it is below the best single index for 4 of 5 properties
  (Supplement Table S7). The first draft said "on alkanes", which was wrong.
* "Off Pi, gamma never destroys any distinction" now carries its hypotheses: rational exponents,
  algebraic gamma. Without them it is false (K4 against K_{1,3} at gamma = ln 4).
* Restored:
  * the narrow-box medians that the pre-registration requires;
  * the 2-D against 3-D budget handicap;
  * "does not show that gamma never helps", the absence of a registered equivalence margin, and
    "ranges are not confidence intervals";
  * the compiled nonane enthalpies (29 of 34);
  * the "conditional" bootstrap;
  * the not-pre-registered status of the wide-box repeat, and that the box was chosen from both
    the octane and the nonane curves;
  * the degraded Delta H_f and the S win-count dependence;
  * the decane cohort (34 of 75) and its representativeness caveat;
  * the qualifiers on Wiener's model, the Test B secondary result, all octane-correlation caveats,
    and the definitions of degeneracy and IRLA.
* Statistics review:
  * The table caption no longer says the registered intervals "understate the uncertainty
    several-fold". Each resampling replicate uses one candidate stream, and on the pooled set the
    seed-to-seed spread on the full data is as wide as the resampling range. This was checked from
    `bp_results_seeds.csv`: [-0.014, +0.008] against [-0.015, +0.008].
  * The full paper's caption has the same sentence and needs the same fix.
  * Ridge claims are now point estimates; the nonane LO-minus-ridge interval that includes zero is
    stated.
  * Wiener: on trees p3 = sum (d_u-1)(d_v-1) is a function of the degree-pair counts, so W carries
    the distance information.
  * Also added: the Test B secondary result marked as point estimates with no registered interval,
    "medians over seeds", "post hoc" on the nonane bootstrap, and the ridge inputs in the table
    caption.
* Restored the completeness of the shortened proofs: independence lemma (consequence and the
  Delta <= 2 case), strict convexity "only if", the c_k of the Laguerre bound, identifiability
  (ii), extremal trees, and the existence of v in generic discrimination.
* Attributions, each checked against the original paper:
  * Theorem 3(ii) is Theorem 3.4 of Rada 2019 applied to the weights gamma q_ij.
  * The degree-ratio corollary is Rada 2019, Proposition 2.5, for ratio-only weights.
  * The colliding construction parallels Rada–Rodríguez–Sigarreta 2022, Example 2.2 (degree-sum
    classes).
  * Both inequalities of the extremal-tree proposition follow from Cruz–Rada 2019, Corollaries 2.2
    and 3.2; the direct proof adds uniqueness.
  * Cruz–Rada check. Their Corollary 2.2 needs f(1,2) = f(2,2) = min f on their set L, where
    f(i,j) = ij/(i+j) (phi_ij + 2 phi_12 - 3 phi_22). For phi = exp(gamma q), f(1,2) = f(2,2) =
    2(e^{gamma/3} - 1).
    * Checked numerically: for n < 60 and gamma in {0.001, ..., 30}, every other pair of L is at
      least 21% higher.
    * Analytic sketch from the novelty review: ij/(i+j) > 1 when i, j >= 2, and (1,j) for j >= 3
      gives at least (9/4)(e^{gamma/3} - 1).
    * The star needs phi(1,n-1) to be the unique maximum, which holds because q is largest there.
    * Status: PARTIALLY VERIFIED (numeric check plus a sketch, not a written proof). The corollaries
      give the inequalities only; uniqueness comes from the direct proof.
  * Also restored: Song–Huang, the exponential-VDB extremal literature, Ali et al. 2025, and the
    Euler–Sombor and cosine-rule Sombor indices.
  * The full paper should take the same attribution fixes. Its sentence contrasting part (ii) with
    Rada 2026 Example 3 overstates the step, and its Cruz–Rada sentence understates what that paper
    covers.

## Cut from the main text (the authors must decide: drop, or move to the Supplement)
* Section 5.1, closed forms on standard graphs (Proposition 9).
* Section 5.3, termwise bounds: bracket bound, Cauchy-Schwarz interpolation, upper and lower bounds,
  ratio bound and its uniform corollary. Some of these are Lean-checked.
* Section 4.3, structure sensitivity and Table 3.
* Limits along the gamma axis (Proposition 6).
* Remarks: independence versus identifiability, the case Delta = 7, the dimension of the counts.
* The dense-grid Q2 values, the M_{4.5,-9} comparison, the narrow-box seed-matched counts (38/50,
  40/50), and the uncorrected 101-molecule cohort (still listed in the deviations table).

## Two facts the draft uses that main.tex and the Supplement do not yet state
* p3 = sum_{uv} (d_u - 1)(d_v - 1) on trees: a path of length 3 is fixed by its middle edge. This
  is elementary but new to the text.
* "Each resampling replicate uses a single candidate stream" (`external/bp/selection_resampling.py`).
  The pooled seed-to-seed spread that shows this was left out of the draft, because it is in
  neither text.

Both should go into the Supplement before submission.

## Before it could replace the full version
* The Supplement refers to main-paper numbers that change:
  * "Section 6" and 6.1–6.4 become Section 5 (there is no 6.4);
  * "Table 4" (octane correlations) becomes Table 3;
  * "Table 5" becomes Table 4;
  * "Table 3" (structure sensitivity) is cut;
  * "Theorem 2" becomes Theorem 3;
  * "Proposition 7" becomes Proposition 1.

  The Supplement needs renumbering. If cut material moves there, its own sections change too.
* `prose_numbers_check.py`, the claim registries, `LEAN_VERIFICATION.md` and Supplement S7 are keyed
  to `main.tex` and do not check this draft.
* Title: the novelty review suggests "... Resolution Limit of Degree-Ratio Indices", since the limit
  belongs to the ratio, not to gamma. This is the authors' choice and is not changed here.
* Coauthor approval of the reframing.
