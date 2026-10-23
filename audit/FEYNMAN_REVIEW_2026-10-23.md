# Independent review of the manuscript, 2026-10-23

Scope: `main.tex` at `745bc08` (branch `review/match-editorial-clarity-2026-10-22`). Every number below was recomputed with code written for this review. It was not taken from the repository's own verifiers. Scripts:

| Checks | Scripts |
|---|---|
| Mathematics | session scratchpad `mathcheck/` (`tree_enum.py`, `analyze*.py`, `delta7.py`, `songhuang.py`, `chi4.py`) |
| Statistics | `statcheck/` |
| Citations | `citecheck/`, private copies of the cited MATCH papers, not committed |
| Journal form | `matchcheck/`: the MATCH template, `prepare.html` and six papers from 2026–2027 |

## 1. Verdict

1. **No mathematical or numerical error was found.**
   - Every proof was read line by line.
   - Every counterexample was rebuilt.
   - Every enumeration count was reproduced exactly.
   - Every table cell that can be recomputed from the repository data was recomputed and agrees at the printed precision.
2. **One cross-reference defect was found and fixed.** It had been introduced by the editorial pass.
3. **Two attribution or wording inaccuracies remain** for the authors to correct.
4. **Several presentation issues** matter for MATCH.

## 2. Defects

| # | Where | Defect | Status |
|---|---|---|---|
| D1 | Contribution (i), l. 339 | `Corollary~\ref{cor:ratioclass}` printed "Corollary 3.1". The template's corollaries are unnumbered (`\newtheorem*`), so `\ref` returned the subsection number. Introduced in `745bc08`; `check_labels.py` does not catch it. | **Fixed**: now "the corollary on degree-ratio indices in Section 3". No other `\ref` points at an unnumbered environment. |
| D2 | l. 1352 | "Theorem 2.1 and Corollary 2.2 of [Cruz–Rada] then give the lower bound with equality only for $P_n$, and their Theorem 3.1 and Corollary 3.2 give the upper bound with equality only for $S_n$". The corollaries state only $\varphi(T)\ge\varphi(P_n)$ and $\varphi(T)\le\varphi(S_n)$ (checked in the source, MATCH 82, pp. 719, 728). Uniqueness comes from the direct proof given in the paper. | **Open (authors).** Suggested: "... give the lower bound $LO(T)\ge LO(P_n)$ ... and the upper bound $LO(T)\le LO(S_n)$; uniqueness follows from the direct proof above." |
| D3 | l. 1620–1622 | "level at three decimals with $LO(0,0,2)$" holds when the isomer is excluded (0.97987 against 0.97953). It does not hold with the 8.56 estimate (0.9763 against 0.9700), and the sentence reads as covering both cases. The sublimation case gives a largest $\lvert r\rvert$ of 0.37474, which rounds to 0.375, so "0.374 or below" is true only if truncated. | **Open (authors).** Write "with the isomer excluded, level at three decimals with $LO(0,0,2)$ ($0.980$); with the hypothetical-liquid estimate first at $0.976$"; and "$0.375$ or below". The second change needs a prose-registry update. |
| D4 | l. 313–315, 343 | [Rada 2026, §3.1] says pendant paths give examples "with arbitrarily many vertices". "Every larger order" follows, because a path of length $L$ adds $L$ vertices, but that inference is the paper's own, not Rada's. | Minor. Optional: "of every larger order (pendant paths of any length)". |

## 3. Mathematics: what was checked and how

| Claim | Independent check | Result |
|---|---|---|
| All trees of orders 2–17 | networkx generator; counts 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159, 7741, 19320, 48629 (OEIS A000055) | ✓ |
| Theorem 2(iii) minimality: the $q$-histogram equals the profile up to order 12 (all trees) and 15 ($\Delta\le4$) | exact rational histograms | ✓; first failures at 13 (566/570) and 16 (809/810) |
| Order-13 witnesses $T_1$, $T_2$ (proof and §4.2) | built from the verbal description, then profiles and histograms recomputed; both occur among the 1301 trees | ✓. There are 4 colliding pairs at order 13; the paper shows one |
| Order-16 witnesses | same check | ✓; the unique colliding pair among chemical trees of order 16 |
| Pendant-path propagation | profile change $-(1,d)+(2,d)+(L-1)(2,2)+(1,2)$ checked by hand, including $d=2$ | ✓ |
| Table 2 (first failures) | exact radical arithmetic (Besicovitch keys) | ✓ every cell: $R$ 14 (1095/1100) and 17 (1191/1194, $\Delta\le4$); $GA$ merge at 17; none for $\Delta\le4$ up to 17 |
| $GA$ order-17 witness | realised; equal $GA$; different histograms | ✓ |
| Remark on the floor: $R$ beats every point of $\Pi$ at 13–17 | 570/566, 1095/1090, 2100/2093, 4007/3996, 7604/7582 | ✓ |
| Off-plane counts at order 16 | exact keys | ✓ 3475, 3476 → 4069; 3940 → 4067; 4007 → 4068; $GA$ 3996 both; $LO(0.3,0.2,0)$ 4069 (50-digit) |
| Order-10 degeneracy and Figure 1 | floats at 11 s.d. | ✓ every bar; 45 trees share a value |
| $\chi$ leaves the floor at order 10 (all trees and $\Delta\le4$) | exact | ✓ 77/79 and 47/49 |
| SDD merge at order 9; ISDD first at order 10 | exact rationals; both SDD profiles realised; value $58/3$ | ✓ (both are first occurrences) |
| Remark on sharpness | both order-12 trees realised; 8 imbalances; $V=5$; zeros at −17.17, −11.96, −2.03, 2.73, 31.13 | ✓ |
| Example 2 (sum-connectivity) | difference vector matches the source (RRS 2022, Ex. 2.2); $\chi$ difference $0$; $D(1)=0.225538$, $D(10^{-6})=2.401\times10^{-7}$ | ✓ |
| Lemma 1 | $3\times3$ determinant $=\ln2\ln\frac98=0.08164$; $4\times4$ determinant $=-0.015003$; ranks 1, 3, 4, 4 for $\Delta=1..4$; the $\Delta=2$ formula for $q$; the algebra $3^8\ne2^{13}$ | ✓ |
| Remark on $\Delta=7$ | all subsets of at most 4 pairs | ✓ none for $\Delta\le6$; exactly $\{(1,7),(2,6),(3,5),(4,4)\}$ at 7; the reduction to 4-subsets is sound |
| Song–Huang comparison | the 7-vertex pair with EDV (4,1,1) has different profiles and histograms; the octane pairs have EDV (3,2,1,1)/(3,2,2,0) and (4,2,0,1)/(4,2,1,0), $W$ 76/75 and 68/67 | ✓ |
| Theorem 1, Propositions (offplane, laguerre, identrank, limits, collision, generic, closed forms, extremal, bounds) | proofs read; closed forms and equality cases rederived by hand | ✓ no gaps found |

**Proof-level notes.** None is an error.

- **Theorem 2(ii) (Rada's Theorem 3.4).** Rada states it on $\mathcal G_n$, graphs of one order. The Lindemann–Weierstrass argument does not use this, so applying it to graphs of different orders is valid. A short remark that the argument does not use the fixed order would pre-empt a referee.
- **Proposition (Parent distinctions survive).** This is Lindemann–Weierstrass with algebraic coefficients in one line. Calling it "proved here" is accurate but generous (author decision 1 of the editorial changelog).
- **Remark on $\Delta=7$.** It says "It fails from $\Delta=7$", but that concerns sets of admissible pairs. No connected graph realises the violating sets: at $\Delta=8$ there are three such sets, all with constant degree sum. The heading could say "admissible sets" to avoid the reading that graphs with $\Delta\ge7$ fail.

## 4. Statistics

| Item | Result |
|---|---|
| Table 4 (60 correlations, bold entries, margins 0.001–0.032, the $-0.0002$ entry) | ✓ |
| Leave-one-isomer-out shift ≤ 0.027; 14 pairs with $\lvert r\rvert\ge0.99$; PC1+PC2 = 99.05% (standardised PCA); 0.982 and 0.993 | ✓ |
| Table 1 values; 16 distinct count vectors; floor 2.925 °C², RMS 0.403 °C | ✓ |
| Ranks 7 / 7 / 8 of the centred count matrices | ✓ |
| Octane union of 9 pairs with affine dimension 3 | ✓ |
| $\mathrm{corr}(LO(0,0,1),IRLA)=0.996$; expansion $m+\tfrac{\gamma}{2}IRLA$ | ✓ |
| Leave-one-out $Q^2$ 0.957 / 0.948 / 0.949 and 0.903 / 0.897 | ✓ (full-sample-mean convention) |
| Table 3 (all 36 cells), $IRLA$ row, SS along $\gamma$, ratio 0.427 | ✓ independent FGD implementation |
| Table 5 Base / Class. / $IRLA$ / LO$_1$ / Ridge | ✓ independently re-run with nesting |
| Table 5 GM / LO$_h$ / $\Delta Q^2$ / wins / intervals; narrow-box and resampling numbers | ✓ against the repository outputs; the 50-seed searches were not re-run |

**Not checked:**
- the uncorrected 101-molecule cohort, whose data are not in the repository;
- the 50-seed searches, bootstraps and permutation test, which were not re-run because they are expensive.

**Methodological points a referee is likely to raise:**

1. **$Q^2$ is never defined in the main text.** Its first use is l. 1686. Define it as $Q^2 = 1-\mathrm{PRESS}/\sum(y_i-\bar y)^2$ with the full-sample mean. With the training-fold mean the values change by about 0.005 (0.957 → 0.962).
2. **Unlike comparisons sit side by side.** A plain leave-one-out $Q^2$ of a post-selected fixed point (l. 1728, 1770, 1782) is placed next to nested $Q^2$ of tuned models. The caveats are present, but a table note or one sentence should say these numbers are not comparable.
3. **The decane result points the other way.** The decane interval $[-0.156,+0.001]$ and the median $-0.072$ (15 of 50 wins) suggest the hybrid Loyola model was, if anything, worse there. The text says only "no gain was demonstrated". Saying the direction plainly is more informative and costs one clause.
4. **Ridge against single indices is not a like-for-like comparison of capacity.** Ridge has up to 7–8 effective count dimensions. Reporting the effective degrees of freedom at the selected penalty would make "ridge leads" self-explanatory.
5. **Interval rule.** "Excluding zero" was read as "lower end above zero" (l. 1808). The deviations table calls this "read as one-sided", but these are the same rule. Use one wording in both places.
6. **No equivalence margin or power analysis.** This is stated in the text, but the abstract and conclusion should say that the negative verdicts are not evidence of equivalence. The conclusion half-says it.

A suggestion from the statistics check was rejected after verification: that the ±12 box was chosen after the boiling-point registration. `external/PREREG_v40.md` (commit `a5cf378`, before any fitting) registers $U(-12,12)^2$ for GM12 and LO$_h$. The post-outcome choice concerns the nonane test only, and Table 6 already lists it.

## 5. Abstract, introduction and conclusion

The three agree with the body and with each other on:
- the orders 12/13 and 15/16;
- at most five exchanges for chemical graphs;
- the attribution to Rada and to Cruz–Rada;
- the non-truncating box;
- the negative boiling-point verdicts.

Points to improve:
- **Abstract, first sentence:** "can distinguish fewer graphs still" is loose. Suggested: "separates still fewer pairs of graphs".
- **Abstract length:** about 239 words, longer than all six sampled MATCH abstracts (77–220).
- **Conclusion:** it does not say that the negative verdicts are not equivalence, while the abstract leaves the decane direction out. The two should match.
- **Introduction:** "What is new here" mentions only the chemical orders (15/16), while the abstract leads with all trees (12/13). Mentioning both would keep them parallel.

## 6. Tables and figure

- **Figure 1:** the bars match the recomputation and the caption is accurate. The clause "it carries no information beyond the profile" is true of every vertex-degree-based index, not only of those on the floor. Moving it to the general sentence would avoid that reading.
- **Table 2:** the caption holds a proof sketch (Besicovitch, exact certification), which MATCH captions don't carry. Move it to the text. The footnotes a–d are correct.
- **Table 5:** the caption is overloaded, and the column header "$>$" is cryptic ("wins of 50").
- **Notation:** $q$-histograms written as $\{0^{1},\tfrac15^{2},\dots\}$ (l. 1121, proof of Theorem 2) look like powers of fractions in the PDF. Write multiplicities as $\tfrac15\,(\times2)$ or as a small table.
- **Table 1:** uses kcal and cal units, matching the octane benchmark literature. That is acceptable, but the supplement should state the conversion.

## 7. MATCH form (verified against the template, `prepare.html` and six 2026–2027 MATCH papers)

**Matches:**
- the template preamble;
- the title and author block;
- no keywords or MSC (the template forbids them);
- theorem numbering;
- table caption above and figure caption below;
- alphabetical references in MATCH format, including `#` article numbers;
- black-and-white figures.

All 16 MATCH bibliography entries were checked against the first pages of the papers, with no discrepancy.

**Differs from usual practice (no rule is violated):**
1. **Length:** 46 pp against a median of 20 in vols 95–97. The longest was 58 pp, and nine papers ran to 40 pp or more.
2. **Discussion section:** none of the sampled papers has a "Discussion and limitations" section. "Concluding remarks" is usual.
3. **Pre-registration apparatus:** nested leave-one-out, bootstraps, pre-registration and a deviations table appear in no sampled paper. The sampled papers report octane $r$, degeneracy and structure sensitivity, which this paper also has.
4. **Supplement:** there are 21 pointers to a supplement. MATCH states no mechanism for supplementary files.
5. **Data availability:** no sampled paper has a Data availability paragraph.

## 8. Feynman summary: what the paper really shows

If an index looks at each bond only through the ratio of its end degrees, it sees only how many bonds have each ratio. For trees, that ratio count first loses information at 13 vertices, and at 16 for molecules. Below those sizes, nothing has been lost relative to the full degree-pair counts. The $\gamma$ knob adds no new information about the molecule. It re-weights counts the index already had, which can undo accidental ties at special exponents. Whether that re-weighting predicts properties better was tested honestly and not demonstrated. A plain regression on the counts did better than any single index.

The mathematics is correct and mostly a careful application of known tools: Lindemann–Weierstrass, Descartes–Laguerre, log-sum-exp convexity and the pendant-path device. The new facts are the two orders and their witnesses, and those orders rest on enumeration. A MATCH referee is likely to accept the mathematics and ask for a much shorter QSPR section.

**Recommendation:**
- fix D2 and D3;
- define $Q^2$;
- cut the main text toward about 30 pp by moving the nested-search, box and deviation material (§6.2–6.4, Table 6) to the supplement, leaving the verdicts and one paragraph of method;
- rename the "Discussion and limitations" section "Concluding remarks".
