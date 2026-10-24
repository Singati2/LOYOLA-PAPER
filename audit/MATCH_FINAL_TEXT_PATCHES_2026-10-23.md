# Final text patches: review status of every edit, 2026-10-23

This report covers:
- every manuscript edit in `3a5f061` (diff against `3904e38`), each re-reviewed;
- the edits made on `review/match-audit-validation-2026-10-23`.

**Status labels:**
- **KEPT**: verified and unchanged.
- **REVISED**: changed on this branch.
- **SIGN-OFF**: needs approval by all three authors; not approved.

**Numbers.** The full diff changes one number, 10.26 → 10.263 (S4). Every other added number is in a bibliography entry, a caption box or a subscript of the definition.

## main.tex

| ID | Before | After | Evidence | Status |
|---|---|---|---|---|
| L1 | Abstract: "By theorems of Rada" | "By an argument of Rada" | Rada's Theorem 3.4 is stated for graphs of equal order; the paper's proof covers any order | KEPT |
| W1–W3, W6–W7 | "exchange order" / "order … changes" | "the values … cross" / "crossings" | Proposition 4 bounds the real zeros of $D(\gamma)=LO(G)-LO(H)$, that is, where the two values coincide. "Order" elsewhere means number of vertices. A zero of even multiplicity is a touch, not a crossing, but it is counted in the bound, so "at most five" stays true | KEPT |
| W4 | Proposition title "Order exchanges along γ" | "Crossings along γ" | as W1 | KEPT · **SIGN-OFF** |
| W5 | "two such graphs exchange order at most five times" | "the values of two such graphs cross at most five times" | as W1; the mathematics is unchanged | KEPT · **SIGN-OFF** |
| D1 | — | "Graphs with Δ ≤ 4 are called chemical graphs, and trees with Δ ≤ 4 chemical trees; the chemical trees of order n are the carbon skeletons of the acyclic alkanes CₙH₂ₙ₊₂." | Consistent with Section 2 (finite simple connected graphs), the Δ ≤ 4 restriction of Theorem 2(iii) and Table 2, and the enumeration of chemical trees as trees with Δ ≤ 4 (the collision-minimality stage). The correspondence with alkane skeletons is up to isomorphism, which is standard | KEPT · **SIGN-OFF** |
| L2 | "We found no earlier determination of the orders 13 and 16, or of explicit colliding trees for degree-ratio indices, in a literature search…" | "In a literature search recorded in the repository we found no earlier determination of the orders 13 and 16, and no earlier pair of trees with distinct degree-pair profiles and equal q-histograms, which collide for every degree-ratio index at once." | Narrower, and still a search result rather than a proof of novelty. The queries are in `MATCH_LITERATURE_NOVELTY_MATRIX` §0 and `audit/final/NOVELTY_SEARCH_LOG.md` | KEPT |
| L3 | "…distinct q-histograms. GA does not" | "…distinct q-histograms. For graphs of equal order the exponential GA index does the same, by [Rada 2019, Corollary 3.5], since its weight √(1−q²) is algebraic and injective in q. GA itself does not" | Proved, and checked exactly for n ≤ 60, in `MATCH_RADA_Q_HISTOGRAM_PRIOR_ART_2026-10-23.md` | KEPT · **SIGN-OFF** |
| S1 | "(0.764 against 0.745 for ${}^{m}M_2$)" | "(0.764 against 0.745 for the best fixed index chosen within each fold)" | Supplement Table S2 caption: "With the fixed choice nested in the folds it becomes 0.745 for $T_B$"; see the captions and statistics cross-check | KEPT |
| S2 | — | "The design refits every model on the nonanes, so it tests whether the procedure replicates, not whether a model fitted on the octanes transfers." | Section 6.3: "the nested design was applied to the 35 constitutional nonane isomers" | KEPT |
| S3 | "so tuning γ adds nothing there over γ = 1" | "so in point estimate tuning γ shows no gain there over γ = 1" | There is no interval, so it is not a demonstrated null | KEPT |
| R1 + B1–B2 | "the standard benchmark compilation" (no citation) | "the octane benchmark compilation used in earlier QSPR studies [Ediz 2017; Mondal et al. 2021]"; both entries copied from the supplement's bibliography | These are the two compilations the supplement already uses for the octane values (Section S1). Records checked: arXiv 1701.02859, and doi 10.1007/s40747-020-00262-0. Units are in the Table 1 caption | KEPT |
| S4 | "The NIST value of 10.26" | "The NIST value of 10.263 kcal/mol" | Same value as `tmb_dhvap_audit.csv`; the 0.374 bound uses 10.263 (max \|r\| 0.37353) | KEPT |
| C1 | Table 5: "LO$_h$ being the hybrid control with (α,β) in the wide box and γ ∈ (−2,2)." | "LO$_h$ being the registered Loyola model, searched in the box of the hybrid control of Section 6.2: (α,β) ∈ (−12,12)² and γ ∈ (−2,2), 2000 candidates per seed." | Section 6.4 text and `external/bp/bp_tests.py`; see the captions and statistics cross-check | KEPT |
| C2 | Table 1: "The two members differ in the measured properties." | "The two members differ in every tabulated property, including the measured boiling point." | Both pairs differ in all five columns; S and ω are partly compiled values | KEPT |
| E1 | "The NIST WebBook pages used are not redistributed; a script of the package downloads them…" → in `3a5f061`: "The release of the package cited here does not include the NIST WebBook pages used; …" | **Sentence removed.** The paragraph ends "…committed before the corresponding models were fitted." | No tag, release or DOI exists. `\bibitem{LoyolaRepo}` is the bare URL, which opens `main`, and `main` tracks all 262 NIST pages. The download script `external/nist_pages.py` is not on `main`. Both versions of the sentence are false today (`MATCH_NIST_RELEASE_RIGHTS_2026-10-23.md`). The remaining sentence is also only fully accurate once the citation is pinned, because `main` predates the current supplement numbering. That is blocker B1 | **REVISED** · **SIGN-OFF**; replacement text depends on the release decision |

## supplement.tex

| ID | Before | After | Evidence | Status |
|---|---|---|---|---|
| X1 | "(Table 5 and Section 6.2 of the main paper)" | "(Section 6.2 of the main paper and Table S6)" | Main Table 5 is the boiling-point table; the box comparison is Table S6 (`tab:box`). It renders as "Table S6" | KEPT |
| X2 | Table S7: "Nested leave-one-out $Q^2$" | "Leave-one-out $Q^2$ (nested wherever an index, a point or a penalty is selected)" | Columns as generated; see the captions and statistics cross-check | KEPT |

## Other files

| File | Change | Status |
|---|---|---|
| `README.md` | Novelty paragraph aligned with the paper; page counts 37/39 | KEPT. Line 8 still pins `c48bad05` for reviewers; repinning waits for the release decision |
| `COVER_LETTER_DRAFT.md` | W1 wording (`3a5f061`). On this branch, "The NIST WebBook source pages are not redistributed." is replaced by a bracketed author note withholding the sentence | **REVISED** |
| `prose_claims_a.py` | Anchor `tmb_nist_main` follows S4; value and tolerance unchanged | KEPT |
| `constancy_test_check.py` | Two exact paths added to `NOT_SELECTION` | KEPT; see `MATCH_VERIFIER_GUARD_INDEPENDENCE_2026-10-23.md` |

## Why the paper is 37 pages, not 35

The page count grew in `3904e38`, not in `3a5f061`.
- **`3904e38`:** restored the proof of Lemma 1 to the main text. Lemma 1 is the only non-standard support for the claim that γ is a new direction. It also added caveats a referee would ask for: the order restriction on Rada's theorem, the fixed-(α,β) quantifier, the Wiener comparison, the increment-estimate warning, the boiling-point scope, a definition of affine dimension, and the GM and LO definitions at first use.
- **`3a5f061`:** kept 37 pages.

No page target was applied. The page count was not optimised at the expense of content.
