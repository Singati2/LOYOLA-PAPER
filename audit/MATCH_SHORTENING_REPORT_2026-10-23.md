# MATCH-oriented shortening and corrections, 2026-10-23

- **Branch:** `review/match-editorial-clarity-2026-10-22`, a separate worktree. The work started from `0877aa0`, was committed locally and was not pushed.
- **Result:**
  - main paper: 46 → **35** A5 pages
  - supplement: 27 → **39** pages
- **Preserved 46-page version:**
  - local branch `review/match-full-46pp-2026-10-23` at `0877aa0`;
  - `drafts/full_46pp_2026-10-23/`, which holds `main.tex`, `supplement.tex` and both PDFs, byte-identical to `0877aa0`.
- **`wt-mainrevert`:** not touched.

## 1. Required corrections

| # | Request | What changed in `main.tex` | Notes |
|---|---|---|---|
| 1 | Cruz–Rada attribution | Section 5: "Corollary 2.2 of [Cruz–Rada] then gives the lower bound $LO(T)\ge LO(P_n)$, and their Corollary 3.2 gives the upper bound … These corollaries state the bounds without equality cases. Uniqueness is given by the direct proof above, and also by the identities of their Theorems 2.1 and 3.1, since the inequalities just shown are strict away from …" | Checked against the private copy of MATCH 82 (pp. 718–728). Theorems 2.1 and 3.1 are identities; the corollaries are non-strict. The earlier review overstated this point (see `audit/FEYNMAN_REVIEW_2026-10-23.md` §9). |
| 2 | Tetramethylbutane comparison and "0.374 → 0.375" | The "level at three decimals" clause now applies only to the excluded-isomer case. The hypothetical-liquid case reads "where $LO(0,0,2)$ follows at $0.970$". "0.374 or below" is **unchanged**. | An independent recomputation gives 0.37353 with NIST's 10.263 kcal/mol, which is the value used by the paper and by `tmb_dhvap_audit.csv`. The 0.37474 of the earlier review came from the rounded 10.26. Changing the text to 0.375 would have been an error. A new registry entry, `tmb_hyp_r2_main`, checks the 0.970. |
| 3 | Define $Q^2$; separate ordinary from nested leave-one-out | New paragraph at the first use (Section 6 opening). It defines $Q^2 = 1-\sum(y_i-\hat y_{(i)})^2/\sum(y_i-\bar y)^2$ with $\bar y$ the full-sample mean, and states ordinary leave-one-out (fixed descriptor; only the regression is refit) against nested (the selection of a parameter point, index or ridge penalty is repeated inside each fold). It also states that an ordinary leave-one-out $Q^2$ of a point chosen on the same data is optimistic. | The definition matches `q2()` in `external/bp/bp_tests.py` and `external/nonane_validation.py`. `external/baselines.py::fold_ridge` confirms the ridge penalty is chosen inside each fold. |
| 4 | Novelty of `prop:offplane` | Introduced as "the argument behind [Rada 2019, Thm 3.4] applies unchanged when the coefficients are algebraic … a direct consequence of the Lindemann–Weierstrass theorem … we do not claim it as a new theorem". It was moved from contribution (ii), "proved here", to (i), "known theorems applied", and dropped from the "What is new" paragraph. | Statement and proof are unchanged. The cover-letter draft was updated to match. |
| 5 | Decane negative result explicit | Section 6.4, after the registered numbers (−0.072, 15/50, [−0.156, +0.001]), now reads: "On the decanes the point estimate therefore favours the parent, and the Loyola model is behind in most seeds, but the interval includes zero, so the test establishes neither a gain nor a loss from γ." The concluding remarks say the same without numbers. | The interpretation does not go beyond the registered interval. |

Additional fixes:
- The acknowledgment is now the text supplied by the authors; it contains no placeholder.
- Ridge capacity: ridge fits one coefficient per count, and the centred count matrix has rank 7 on the decanes and 8 on the pooled set (from the existing remark on the dimension of the counts). This is now stated next to the ridge verdict.

## 2. Retained, shortened, moved

| Part (46-page section) | Pages before → after | Disposition |
|---|---|---|
| Abstract | about 239 → 182 words | **Shortened.** Keeps the problem, the family, Rada's theorems, the orders 12/15 with explicit counterexamples, the five-crossing bound, and the negative chemistry results with the exploratory qualifier. Drops the extremal-tree clause (a known result) and the Zagreb/Randić list. Fixes "fewer graphs still". |
| 1 Introduction | 2–5 → 2–5 | **Shortened.** The paragraph "Several facts used below are known" duplicated contribution item (i) and was removed; it carried the D4 wording. The statuses of the contributions were corrected (item 4 above). |
| 2 Preliminaries | **retained** | |
| 3 Parameter geometry | 6–17 → 6–14 | **Retained:** Lemma 1 and Theorem 1 (statements), Theorem 2 and its full proof with the order-13 and order-16 witnesses, the corollary and remark on degree-ratio indices, Proposition 3, the remarks on off-plane behaviour and the floor on Π, Proposition 4 with its sharpness remark, and the remark on data sets. **Moved to S10:** the proofs of Lemma 1 and Theorem 1, the remark on independence against identifiability, per-graph identifiability (old Prop. 5, with the Δ = 7 remark and the spider example) and the limits along γ (old Prop. 6). **Condensed:** the Song–Huang and earlier-examples paragraphs. |
| 4 Discrimination | 17–24 → 14–20 | **Retained:** Propositions 5 (ceiling) and 6 (generic), Example 1 (formerly 2), Tables 1–3, Figure 1, all counts. **Condensed:** the weak-discrimination discussion, and the γ-trend and *IRLA* sentences of 4.3, which Supplementary S6 already states and the `sup_ss` registry entries check. |
| 5 Closed forms, bounds, extremal trees | 24–31 → 20–22 | **Retained:** the extremal-tree proposition (now Proposition 7) and its proof. **Moved to S10:** closed forms (old 5.1, Prop. 9) and termwise bounds (old 5.3: Definition 4, Props 11–14, the Cauchy–Schwarz and uniform-ratio corollaries). Section renamed "Extremal trees for the pure-imbalance points". |
| 6.1 Octanes | **retained** (with the TMB fix) | |
| 6.2 Freeing γ, search box | about 2.5 → 1.5 pp | **Retained:** design, narrow-box result, boundary diagnosis, how the box of half-width 12 was chosen (after inspecting the curves), the wide-box result with the hybrid control, and the conclusion. **Moved to S11:** dense-grid values, the effect of the box on $T_B$, and the post-selection fixed parent point $M_{4.5,-9}$. |
| 6.3 Nonanes | **retained:** protocol, provenance, verdict, interval and design-error statement | **Moved to S11:** the untuned point, *IRLA* and ridge details. A one-sentence summary stays, including that the ridge interval includes zero. |
| 6.4 Boiling points | **retained:** cohort rule, design, Table 5, both verdicts with all numbers, the narrow-box levels, the resampling ranges, the interpretation (no equivalence margin, three against two dimensions), ridge, the permutation check and the final verdict | **Moved to S11:** seed-by-seed cross-box comparisons, the numbers for the uncorrected cohort, and the Wiener model. A one-sentence pointer stays for each. |
| 7 Discussion and limitations, 8 Conclusion | 39–41 → 29–31 | **Merged** into "7 Concluding remarks": the results and their attribution, the chemistry outcome (decane direction now stated), limitations (i)–(iv) and the open problem. **Moved:** Table 6 (protocol deviations), now Supplementary Table S8, unchanged. |
| Data availability, Lean scope | **condensed** | Same scope statements. |
| References | 56 → 54 | Brown 1986 and Carballosa et al. 2023 are cited only by the moved text, so they now appear in the supplement's bibliography, together with five other entries the moved text cites. |

**Negative results and limitations:** none was removed. Every verdict, interval and seed count of Sections 6.2–6.4 that was in the main text is either still there or in S11 verbatim. The changes made after outcomes had been seen are listed in Table S8 and referenced from limitation (iv).

## 3. Numbering changes (main paper)

| Item | Before | After |
|---|---|---|
| Degree-pair ceiling | Proposition 7 | Proposition 5 (Supplement S3 updated) |
| Generic discrimination | Proposition 8 | Proposition 6 |
| Extremal trees | Proposition 10 | Proposition 7 |
| Per-graph identifiability | Proposition 5 | Supplementary Proposition S1 |
| Limits along γ | Proposition 6 | Supplementary Proposition S2 |
| Closed forms | Proposition 9 | Supplementary Proposition S3 |
| Bracket, upper, lower and ratio bounds | Propositions 11–14 | Supplementary Propositions S4–S7 |
| Sum-connectivity example | Example 2 | Example 1 |
| Protocol deviations | Table 6 | Supplementary Table S8 |
| Discussion and Conclusion | Sections 7, 8 | Section 7 |

Unchanged:
- Lemma 1, Theorems 1–2, Propositions 3–4, Definitions 1–3, Tables 1–5, Figure 1, Equations (1)–(4), and Sections 1–6 with their subsection numbers 6.1–6.4.
- Every "Section 6.x / Table 4 / Theorem 2 of the main paper" in the supplement therefore still holds; `audit/check_labels.py` verifies them.

The supplement now prefixes theorem-type numbers with S, like its sections, tables and equations. `LEAN_VERIFICATION.md`, `REPRODUCE.md`, `REVIEWER_START_HERE.md` and the Overleaf READMEs were updated to the new numbers.

## 4. Preservation checks

- **Statements and proofs:**
  - All 74 theorem-type, proof, table, figure and display-math environments of the 46-page `main.tex` were compared, whitespace-normalised, with the new `main.tex` + `supplement.tex`. Cross-references were normalised; the script is `restructure/preserve_check.py` in the session scratchpad.
  - 73 are verbatim. The one change is in the proof of Proposition 4: "As in the proof of Proposition 6 below, only $c_k$ survives" became "Only $c_k$ survives", because Proposition 6 moved.
- **Data, numbers, scripts and protocols:**
  - No data file, CSV output, script, protocol, seed or Lean file changed.
  - No number in any table changed. The 0.970 is new text, taken from `tmb_dhvap_audit.csv` and registered.
- **Prose registry:**
  - 63 entries whose sentences moved verbatim were re-pointed from `main` to `supp`, with only the file field changed. `restructure/retarget_registry.py` accepts an entry only if its pattern matches `main.tex` 0 times and `supplement.tex` exactly once.
  - 7 further moved entries were re-pointed and given more surrounding context in the anchor:
    - six because the moved Section 6.3 text repeats sentences already in S4;
    - one because "Supplementary Table S7" became "Table S7" in the supplement.
  - 10 entries kept their file but gained context:
    - eight S4/S1 anchors, so that they match only their original sentence;
    - two Section 6.4 anchors, whose following words changed ("In" became "On the decanes", "Seed by seed" became "Seed-by-seed comparisons").
  - In all 17, the captured number, expression and tolerance are unchanged.
  - Nine Section 4.3 entries for `main` were dropped. Their numbers are no longer in the main text and are still checked in S6.
  - One entry was added (0.970).
  - Result: 756 checked, 0 failures. Before: 764 checked, 0 failures.

## 5. Verification

| Check | Result |
|---|---|
| `python prose_numbers_check.py` | **PASS**: 756 checked, 0 failures, 22 uncheckable (cited values) |
| `python audit/check_style.py` | **PASS** (longest sentence 45 words) |
| `python audit/check_labels.py` (compiles `main.tex`, cross-document numbering) | **PASS** |
| The three test suites (`test_corrections_2026_10_19`, `test_review_2026_10_20`, `test_replay_contract_2026_10_21`) | **PASS** (exit 0) |
| pdflatex ×3, both documents | main 35 pp, supplement 39 pp; 0 undefined references, 0 overfull boxes; Figure 1 on p. 19 |
| Clean extraction of `MATCH_OVERLEAF_CANDIDATE.zip` (`build_package.sh`) | 35 + 39 pages; text identical to the included PDFs |
| `python verify.py --offline` (fast path, run on the final working tree before the commit) | **ALL PASS**, exit 0: core verifier (all 8 numeric tables, 588 s), prose numbers, baseline tests, constancy, interval certificates, style, extremal trees 4–12, collision minimality 13/16, sum-connectivity pair, count dimension, DATA copies, manifest. NIST-page stages NOT RUN (pages not in this worktree) |
| `manifest.py --write` | regenerated after the last edit; `manifest.py`: OK |

**Not run** (expensive, and no computation changed):
- `verify.py --full`, including `audit/attack_checks.py`;
- `--everything`;
- the Lean build;
- the NIST-page stages;
- the Colab notebooks;
- the 50-seed searches, bootstraps and permutation test.

The two anchors that `audit/attack_checks.py` mutates in `main.tex` are still present, each exactly once. Earlier passes of these checks apply to earlier commits and are not claimed for this one.

## 6. MATCH readiness

**Form**
- Template, references, captions, theorem numbering and black-and-white figure are unchanged and compliant.
- 35 pages is still above the median of the recent MATCH papers sampled (20), but within their range (up to 58).
- The abstract (182 words) is now within the sampled range (77–220).
- MATCH states no route for supplementary files, so whether S1–S11 may accompany the submission must be confirmed with the editorial office.

**Open author items**
- Approval by all three authors.
- Final title.
- Exact commit or DOI for the repository citation.
- Status of the companion manuscript.
- NIST/KDB/Chemeo redistribution.
- AI-use disclosure.
- Whether to keep the "Concluding remarks" name.
- Whether to restore the two removed open problems.
