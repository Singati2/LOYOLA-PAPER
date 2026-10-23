# MATCH final patch log, 2026-10-23

- **Baseline:** `e25d790` (public branch `review/match-editorial-clarity-2026-10-22`; the remote tip was verified equal to `e25d790` before work began).
- **Branch:** `review/match-final-scientific-audit-2026-10-23`, local only, in a separate worktree.
- **Brief:** `CLAUDE_MATCH_FINAL_SCIENTIFIC_AUDIT_2026-10-23.md`, supplied by the author.

Every edit corrects a demonstrated error, a quantifier, an attribution, a missing caveat or a layout defect found in the audit (`audit/MATCH_FINAL_SCIENTIFIC_AUDIT_2026-10-23.md`).

Nothing was changed in:
- numerical results, tables (other than captions or headers), figures or figure sources;
- data, CSVs, protocols, seeds, cohorts or thresholds;
- Lean files, authorship or acknowledgment.

Line numbers below refer to `git show e25d790:main.tex` (M) and `git show e25d790:supplement.tex` (S).

## Edits that touch a statement, definition or remark

These need **coauthor sign-off**. Each is a narrowing or a clarification; no result is strengthened.

| # | Where | Before → after (excerpt) | Justification |
|---|---|---|---|
| P1 | M 498–500, Definition (Ratio plane) | "It contains the pure-γ points (0,0,γ), $GA = 2LO(\tfrac12,-1,0)$ and $AG = …$" → "… and the points $(\tfrac12,-1,0)$ and $(-\tfrac12,1,0)$, at which $GA = …$ and $AG = …$" | Π is a set of parameter points, not of indices |
| P2 | M 529, Theorem 2(iii) | "Attaching a pendant path of length $L \ge 1$ at such a leaf in each produces" → "…, so that the leaf becomes a vertex of degree 2, produces" | Removes the ambiguity flagged by the mathematics referee (path at the leaf, not at its neighbour). The proof's difference vector $-(1,d)+(2,d)+(L-1)(2,2)+(1,2)$ already assumed this reading |
| P3 | M 626–631, remark after the corollary on degree-ratio indices | "The parent attains it as well: … separates two distinct histograms at all but finitely many α" → "The parent comes close: … separates any two given distinct histograms at all but finitely many α, hence all pairs at once for α outside a countable set. It fails at α = ½, the point of GA" | **Over-claim corrected.** The pair-by-pair argument does not give simultaneous separation at a given α. GA, which is the parent at α = ½, merges histograms at order 17 (Table 2, footnote d) |
| P4 | M 739, 746, Remark (Sharpness) | "The bound is attained." → "The bound $V$ is attained." plus "Here $V = 5 < r - 1 = 7$." | The example has Δ = 6 and attains Laguerre's V, not the constant five for Δ ≤ 4, which stays open (already stated) |
| P5 | M 766–767, Remark (Data sets) | "its affine dimension is 3" now preceded by a one-sentence definition of affine dimension | The term was defined only in S10 |
| P6 | M 384, Eq. (1) | terminal period added | Typography |

## Attribution and quantifier edits (prose)

| # | Where | Change | Justification |
|---|---|---|---|
| A1 | M 210–211, abstract; M 315–316, introduction; cover letter | "Two chemical graphs exchange order at most five times along γ" → "At fixed (α,β), two chemical graphs exchange order at most five times as γ varies" | Proposition 4 holds at fixed (α,β); along other lines the count is unbounded by five (Remark (Sharpness), last sentence) |
| A2 | M 322, M 600, M 1387–1389 (conclusion), cover letter | Rada's Theorem 3.4 credited "for graphs of equal order"; M 600 adds that the paper's proof needs no order restriction (pair $K_4$, $K_{1,3}$) | Rada (MATCH 82 (2019) 29–41) states Theorem 3.4 on $\mathcal{G}_n$, the graphs with $n$ non-isolated vertices (source text checked) |
| A3 | M 338–339, contribution (ii) | Laguerre bound described as "an application of Laguerre's rule of signs"; per-graph identifiability "stated and proved in Supplementary Section S10" | The main text listed identifiability as a result proved here but did not state it |
| A4 | M 225, 241, 301 | "BID" spelled out at first use; "therefore" removed where it did not follow | Undefined acronym; non-sequitur |
| A5 | M 604 | "orders 2 to 16" → "orders 2 to 17" | Agrees with Table 2 and the remark on the floor; the enumeration covers order 17 (verified by the mathematics referee) |
| A6 | M 1085 | "the termwise bound (Supplementary Section S10) gives" → "every edge has $q \le \tfrac35$, which gives" | One-line justification inline instead of a supplement pointer |

## Restored proof

| # | Where | Change | Justification |
|---|---|---|---|
| R1 | M 441–442 ← S 1130–1162 | Proof of Lemma 1 restored to the main paper **verbatim**, apart from its optional title; removed from S10.1. S10.1 renamed "Proof of Theorem 1 of the main paper", and the S10 intro adjusted | Lemma 1 is the only justification in the paper that γ is a direction the parent cannot reproduce. Its proof (the 3⁸ ≠ 2¹³ rank argument, and the (1,1)-free determinant that makes it apply to connected graphs other than $K_2$) is non-standard and short. Theorem 1's proof is the textbook log-sum-exp computation and stays in S10 |

## Statistical reporting edits

All values come from the existing supplement or protocol files; no number was recomputed or changed.

| # | Where | Change | Evidence |
|---|---|---|---|
| Q1 | M 1107–1108 | "No parameter … is tuned" → "… is optimised …, although the choice of γ = 1, 2 cannot be shown to precede the octane data (below)" | The two adjacent statements conflicted |
| Q2 | M 1125 | "exceeded the best fixed point only by a 0.001 in-sample margin and, under nested leave-one-out, on octane $T_B$ (0.764 against 0.745)" → "exceeded the best fixed index …, in a leave-one-out correlation nested within globally chosen candidate pools, on octane $T_B$ (0.764 against 0.745 for ${}^{m}M_2$)" | S2, Table S2: these are LOO correlations, not $Q^2$; the pools were chosen on all 18 isomers; the comparator is the index ${}^{m}M_2$ |
| Q3 | M 1201 | "LO" and "GM" defined at first use | GM was never defined in the main text |
| Q4 | M 1210–1211 | "usually degraded $\Delta H_f$ and was mixed elsewhere" → "usually degraded $\Delta H_f$, $S$ and $\omega$, and was mixed on $T_B$; on $\Delta H_f$ the … interval … excludes zero against γ" | Table S3(b): S 34/31, ω 26/28 of 100; S4: $[-0.281,-0.044]$ |
| Q5 | M 1234 | "reaches the seed-count criterion" → "reaches 40 of 50 seeds" | The v37 criterion (80/100 at two budgets) is undefined for 50 seeds at one budget |
| Q6 | M 1251 | Increment-estimate caveat added for the compiled nonane $\Delta H_{\mathrm{vap}}$ | S4: "A degree-pair-based predictor may also be favoured if the compiled values were themselves derived from structural increments". This bears on the only positive registered verdict |
| Q7 | M 1270–1271 | "design error" now qualified as "used on its own", and the boiling-point protocol's use of a seed count with an interval is stated | PREREG_v40 keeps a 40/50 seed count joined to an interval |
| Q8 | M 1274 | Sentence added: the untuned $LO(0,0,1)$ matches the tuned Loyola model on nonane $\Delta H_{\mathrm{vap}}$ in point estimate | PREREG_v37 requires saying so when a fixed index matches; S11: 0.903 against median 0.900 |
| Q9 | M 1278, 1282–1284; conclusion M 1408 | The boiling-point tests are stated not to test the $\Delta H_{\mathrm{vap}}$ gain directly; γ had given mixed $T_B$ results | Prevents reading the negative boiling-point verdicts as a confirmatory refutation of the $\Delta H_{\mathrm{vap}}$ effect |
| Q10 | M 1284 | Disclosure added: the boiling-point rule was written after all C4–C16 NIST pages had been downloaded to count available values; no C6, C7 or C10 boiling point had entered a model | PREREG_v40 lines 3–7 |
| Q11 | M 1300 | "(Table 5)" → "(results in Table 5 and below)" | Table 5 shows no intervals |
| Q12 | M 1304, 1314–1315, 1321, Table 5 | Caption "nested leave-one-out $Q^2$" → "leave-one-out $Q^2$, nested wherever an index, a point or a penalty is selected"; column header "$>$" → "wins" | The $IRLA$ and $LO_1$ columns are ordinary LOO of fixed descriptors |
| Q13 | M 1341; S 1640–1641 | "do not indicate a gain from γ" → "inconclusive" (main); "neither establish nor exclude a gain" (S11) | On the pooled set the narrow-box LO beats the narrow-box GM in 40/50 seeds and the wide-box GM in 38/50 (S11). "Do not indicate a gain" overstated the negative |
| Q14 | M 1375, 1378; conclusion M 1412 | Wiener's two-descriptor model is stated to give a higher point estimate than ridge on the decanes; the ridge sentence adds "though not more accurately than Wiener's model on the decanes" | S11 and `external/bp/wiener_baseline_out.txt`: W + p₃ gives $Q^2$ = 0.9038 against ridge 0.860. Omitting this let readers take the degree-pair counts as the ceiling |
| Q15 | M 1426, limitation (iii) | "35 nonanes" → "35 nonanes (34 for $\Delta H_{\mathrm{vap}}$)" | Section 6.3 |

## Layout

| # | Where | Change |
|---|---|---|
| L1 | S preamble (allowed package slot), S before `\section{Further results…}` | `\usepackage{placeins}` and `\FloatBarrier`, so Table S7 no longer floats into S10 |
| L2 | S 1662, Table S8 | Column type `p{}` → `>{\raggedright\arraybackslash}p{}`, removing the wide word gaps. Cell text unchanged |

## Other files

- **Copies:** `LOYOLA_MAIN_OVERLEAF/main.tex`, `LOYOLA_FINAL_PAPER_OVERLEAF/{main,supplement}.tex`, `LOYOLA_SUPPLEMENT_OVERLEAF/main.tex` and `submission_candidate/match/{main,supplement}.tex` were recopied from the sources. All four zips were rebuilt.
- **PDFs:** both PDFs were rebuilt with pdflatex ×3.
- **Registry (`prose_claims_a.py`):** the anchors of `s6_tuning_margin` and `v4029_nfix_tb_main` follow the reworded sentence (Q2). Their expressions and tolerances are unchanged.
- **Page counts and wording:** `README_SUBMISSION.md`, `docs/match/01`, `LOYOLA_FINAL_PAPER_OVERLEAF/README.txt` and `COVER_LETTER_DRAFT.md` now give 37 pages. The cover letter also adopts A1, A2, A5 and Q9.
- **Hashes:** the hash rows of `CLEAN_SUBMISSION_MANIFEST.md` and `SHA256SUMS.txt` were regenerated.

## Before and after

| | `e25d790` | this branch |
|---|---|---|
| Main pages | 35 | 37 |
| Supplement pages | 39 | 39 |
| Figure 1 | p. 19 | p. 18 |
| References begin | p. 31 | p. 33 |
| Undefined refs / overfull | 0 / 0 | 0 / 0 |
| Prose numbers | 756 checked, 0 failures | 756 checked, 0 failures |
| Style | PASS | PASS (after splitting five sentences over 45 words) |
| Labels | PASS | PASS |
| Three test suites | exit 0 | exit 0 |
| `verify.py --offline` | ALL PASS (rerun today on `e25d790`, 19 min) | see `MATCH_PRESERVATION_AND_TEST_MATRIX_2026-10-23.md` |

### Preservation of the 74 environments of the 46-page version

Run with `preserve_check.py` (whitespace-normalised).

**At `e25d790`: 72 verbatim.** The other two differ as follows:
- **Laguerre proof:** the dropped forward reference.
- **Per-graph identifiability proof:** cross-references only, Theorem 1 and Eq. (4) written as hard numbers. The script's normaliser misses this case.

This corrects the earlier report of 73 verbatim.

**On this branch:** the eleven environments that differ are:
- the two above;
- P1–P6;
- Table 5 (Q12) and Table S8 (L2).

The definition (Loyola index family) and Eq. (1) count separately because of the period (P6). No other environment changed.
