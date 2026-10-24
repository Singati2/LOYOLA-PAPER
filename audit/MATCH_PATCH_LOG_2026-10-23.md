# Patch log: literature and writing audit, 2026-10-23

- **Branch:** `review/match-literature-writing-audit-2026-10-23`, local only.
- **Base:** `3904e38`, the scientific audit, which itself builds on `e25d790`.
- **Brief:** `docs/CLAUDE_MATCH_LITERATURE_WRITING_AUDIT_PROMPT_2026-10-23.md`, pushed as `2491f0e`. It is copied unchanged onto this branch.
- **Why each change was made:** the reasons are in the four audit reports of the same date.

## What did not change

- No theorem hypothesis, proof, result, data value, protocol, seed, interval, selection rule or negative conclusion was changed. No figure was changed.
- Every number in the text is unchanged except one: the NIST value 10.26 is now given as 10.263 kcal/mol (S4). That is the value already used in the computation.

**Edits that need sign-off by all three authors** (they change the wording of a statement or add an attribution):
- W4–W5: the title and wording of the Proposition.
- D1: the new definition.
- L3: the new credit to Rada's Corollary 3.5.
- E1: the availability wording. It is true only once the repository citation is pinned.

## main.tex

| ID | Location | Old → new | Reason |
|---|---|---|---|
| L1 | Abstract | "By theorems of Rada" → "By an argument of Rada" | Rada's Theorem 3.4 covers graphs of equal order; the paper's proof drops that restriction. The intro and conclusion give the precise credit |
| W1 | Abstract | "two chemical graphs exchange order at most five times" → "the values of two chemical graphs cross at most five times" | Everywhere else "order" means number of vertices |
| W2 | Introduction | "the order of two chemical graphs changes at most five times" → "the values of two chemical graphs cross at most five times" | as W1 |
| W3 | Contribution (ii) | "order exchanges along γ" → "crossings along γ" | as W1 |
| W4 | Proposition title | "Order exchanges along γ" → "Crossings along γ" | as W1. **Sign-off** |
| W5 | Proposition statement | "two such graphs exchange order at most five times" → "the values of two such graphs cross at most five times" | as W1. Wording only; the mathematics is the same. **Sign-off** |
| W6 | Conclusion | as W1 | as W1 |
| W7 | Limitation (ii) | "can exchange order five times" → "can cross five times" | as W1 |
| D1 | Section 2, notation | New: "Graphs with Δ ≤ 4 are called chemical graphs, and trees with Δ ≤ 4 chemical trees; the chemical trees of order n are the carbon skeletons of the acyclic alkanes CₙH₂ₙ₊₂." | The paper used these terms without defining them. **Sign-off** |
| L2 | After Theorem 2 | The search statement is narrowed to orders 13 and 16 and to "no earlier pair of trees with distinct degree-pair profiles and equal q-histograms, which collide for every degree-ratio index at once" | The old claim, "explicit colliding trees for degree-ratio indices", was broader than the search supports. The paper itself shows single-index collisions at order 9 |
| L3 | Remark after the degree-ratio corollary | New: "For graphs of equal order the exponential GA index does the same, by [Rada 2019, Corollary 3.5], since its weight √(1−q²) is algebraic and injective in q. GA itself does not…" | Missing credit, checked in the full text: GA is in Rada's Table 1, and his Corollary 3.5 applies to it. **Sign-off** |
| S1 | Section 6, local tuning | "0.745 for ${}^{m}M_2$" → "0.745 for the best fixed index chosen within each fold" | 0.745 is the fixed choice nested within the folds (supplement Table S2 caption) |
| S2 | Section 6.3 | New: "The design refits every model on the nonanes, so it tests whether the procedure replicates, not whether a model fitted on the octanes transfers." | Says what "replication" covers |
| S3 | Section 6.3 | "tuning γ adds nothing there" → "in point estimate tuning γ shows no gain there" | It is a point estimate, not a demonstrated null |
| R1 | Section 6.1 | "the standard benchmark compilation" → "the octane benchmark compilation used in earlier QSPR studies [Ediz 2017; Mondal et al. 2021]" | The main text had no citation for the data source |
| B1–B2 | Bibliography | Ediz 2017 and Mondal et al. 2021 added to main, in alphabetical order. Main now has 56 entries | Moved from the supplement's bibliography. Neither entry is new; both were checked against arXiv and Crossref |
| S4 | Section 6.1 | "The NIST value of 10.26" → "The NIST value of 10.263 kcal/mol" | Same value as the audit CSV; the unit is added |
| C1 | Table 5 caption | LO_h is described as "the registered Loyola model, searched in the box of the hybrid control of Section 6.2: (α,β) ∈ (−12,12)², γ ∈ (−2,2), 2000 candidates per seed" | The caption read as if LO_h were a control rather than the registered model |
| C2 | Table 1 caption | "differ in the measured properties" → "differ in every tabulated property, including the measured boiling point" | S and ω are partly compiled values, not measurements |
| E1 | Data availability | "The NIST WebBook pages used are not redistributed" → "The release of the package cited here does not include the NIST WebBook pages used" | The default branch `main` still tracks 262 NIST pages, so the old sentence is false for the unpinned link. The new wording becomes true once decision D1 pins the cited release. **Sign-off** |

## supplement.tex

| ID | Location | Change | Reason |
|---|---|---|---|
| X1 | S6, box comparison | "(Table 5 and Section 6.2 of the main paper)" → "(Section 6.2 of the main paper and Table S6)" | Main Table 5 is the boiling-point table, so the reference was wrong |
| X2 | Table S7 caption | "Nested leave-one-out Q²" → "Leave-one-out Q² (nested wherever an index, a point or a penalty is selected)" | Same correction as the earlier fix to Table 5 |

## Other files

- **`README.md`:**
  - The novelty paragraph is aligned with the paper: Rada credit for equal order, order 16, computer-assisted minimality, the vaporisation-enthalpy result as an exploratory rerun, and ridge as point estimates.
  - The page counts are now 37 and 39.
  - The reviewer pin to `c48bad05` (line 8) is **not** changed. Repinning waits for decision D1.
- **`submission_candidate/match/COVER_LETTER_DRAFT.md`:** W1 wording.
- **`prose_claims_a.py`:** the anchor `tmb_nist_main` follows S4. The value and tolerance are unchanged.
- **Copies:** the bundle copies, both PDFs and the four zips were regenerated, and `SHA256SUMS.txt` and `CLEAN_SUBMISSION_MANIFEST.md` were updated.
- **`audit/independent_recompute_2026-10-23/`:** the reviewer's independent recomputation scripts. They read repository data only.
- **`constancy_test_check.py`:** `decane_indep.py` and `pooled_indep.py` were added to `NOT_SELECTION`. They draw candidate triples only to re-derive published results and select nothing for the paper. The check's logic is unchanged.

## Proposed, not applied

These need an author decision or a citation that was not verified:
- Add the hyperbolic Sombor index (Barman–Das 2026, already in the bibliography) to the corollary list. It is a degree-ratio index, by Kırgız 2027.
- Theorem 1: call it a Proposition and cite Brown 1986 in the main text. A rename would also change five references in the supplement.
- Cite precedents for minimal-order results: Guo, Randić et al. 1999 and Ivanciuc et al. 1993. Both are **unverified**.
- Name the tree generator and the OEIS count checks for the enumeration. A citation for the generator still has to be verified.
- Caption completeness for Tables 3, 4, S1, S3, S5 and S6; the details are in the caption audit.
- Introduction: "where the known results bind for chemical graphs" → "for trees and chemical trees".
- References: the Konstantinova "degeneracy" wording, the NIST retrieval date, and KDB/Chéméo access dates.

## Checks run after the edits

| Check | Result |
|---|---|
| `prose_numbers_check.py` | 756 checked, 0 failures |
| `audit/check_style.py` | PASS (longest sentence 45 words) |
| `audit/check_labels.py` | PASS |
| Test suites of 19, 20 and 21 Oct | exit 0, all three |
| pdflatex ×3 | main 37 pp, supplement 39 pp; 0 undefined references or citations; 0 overfull boxes |
| Clean-extraction build of `MATCH_OVERLEAF_CANDIDATE.zip` | 37 + 39 pp; text identical to the shipped PDFs; no placeholders and no `??` |
| Independent decane recomputation (`decane_indep.py`) | −0.0715, 15/50, [−0.156, +0.001] |
| Rendered-page inspection | Table 5 (p. 29) |
| `verify.py --offline` | ALL PASS, exit 0, on the second run; the NIST stages were NOT RUN (details in the decision file) |
