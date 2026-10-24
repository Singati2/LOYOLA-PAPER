# Claude Instructions — Four Verified MATCH Corrections and Final Reviewer-Package Audit

**Date:** 2026-10-23 (America/New_York)  
**Repository:** `Singati2/LOYOLA-PAPER`  
**Reviewed baseline:** `review/match-audit-validation-2026-10-23` at `f720a16c4742749bcc464f1659028e56ce28863a`  
**Paper:** *The Loyola Index Family and the Resolution Limit of Degree Imbalance*  
**Journal:** *MATCH Communications in Mathematical and in Computer Chemistry*  
**Status:** Reviewer instructions only. This file does **not** implement manuscript fixes or certify submission readiness.

## Why this brief exists

An independent review of the pushed `f720a16` candidate identified four targeted corrections. These findings have been compared with the actual GitHub source, except that the PDF page-placement finding comes from the independent review's visual inspection and must be re-checked from a rebuilt PDF. The review reports strong reproducibility evidence for the paper's main mathematical results and statistical conclusions. **Do not restart the whole paper or change frozen experiments because of these editorial/reviewer-package defects.**

The independent review reported:
- First distinct degree-pair profiles with equal q-histograms at tree order **13** (general) and **16** (chemical, maximum degree four).
- Decanes: median paired `ΔQ² = −0.0715304490`, Loyola wins **15/50** seeds, conditional interval approximately **[−0.15584287, +0.00148413]**.
- Pooled set: median `ΔQ² = −0.0001133864`, Loyola wins **25/50**, conditional interval approximately **[−0.00263582, +0.00190755]**.
- Nested ridge `Q² ≈ 0.8598706416` for decanes, `0.9910686922` pooled; decane Wiener `W+p3` `Q² ≈ 0.9038067173`.
- All 60 octane correlation cells, Figure 1's 106 trees and 79 degree-pair profiles, and relevant table values were reproduced.
- The exponential GA versus q-class correspondence and Rada attribution were reviewed positively.
- Fast `verify.py --offline`, replay/correction tests and PDF ZIP rebuild were reported PASS at the reviewed revision; **full verification, a new Lean build, real Colab execution and some source-dependent checks were NOT RUN**.

Treat these as **review evidence to preserve and independently verify where affected**, not carte-blanche certification of every mathematical or experimental claim.

## Non-negotiable Git rules

1. Begin with `git fetch origin`, `git status`, `git worktree list`, and `git rev-parse origin/review/match-audit-validation-2026-10-23`. Confirm baseline SHA. If it moved, compare and report the difference before editing.
2. Create a **new local branch/worktree**, e.g. `review/match-final-four-fixes-2026-10-23`, from the verified baseline. Preserve `main`, the audit branch, other review branches, the archived 46-page version, and `wt-mainrevert`.
3. Do **not** push, force-push, merge, rewrite history, open a PR, create a release or DOI, or submit to MATCH without a separate instruction from the authors. This Markdown file alone may be public.
4. Keep all frozen datasets, numerical results, registered protocols, experiment seeds, figures, proofs and formal results intact. Changes must be minimal and supported by a diff and an audit entry.
5. Do not redistribute NIST WebBook pages, verbatim copyrighted extracts, proprietary source documents, private files, credentials, or tokens in a proposed public package. Do not rewrite public Git history as an incidental cleanup.
6. Never claim a test passed if you did not run it on the stated exact source commit.

## P1 — Reproducibility: retire outdated reviewer pins

**Confirmed:** `README.md` around line 8 and `REVIEWER_START_HERE.md` around line 7 still identify `c48bad05f8e95805d4f0f700f5324d1071b903cd` as the reviewed code. `notebooks/` and `colab/` currently use old `PIN` defaults; some links fetch notebook files at `afafe6c`. The replay-output safeguards were introduced later (including `69b9538`). Consequently the current advertised Colab route does not execute the exact newest source.

**Implement:**
- Choose one finalized source commit **after** P2–P4 are corrected and tested. Create and record a source SHA (`SOURCE_COMMIT`); choose the notebook commit separately (`NOTEBOOK_COMMIT`) to avoid a self-referential commit pin.
- Update/rebuild notebook generators, actual notebooks, setup cells, and Colab URLs so the notebook revision `NOTEBOOK_COMMIT` checks out and verifies exactly `SOURCE_COMMIT`, not `c48bad0`.
- Update `README.md`, `REVIEWER_START_HERE.md`, `COLAB_FOR_REVIEWERS` if present, `docs/match/*` relevant release matrices, manuscript data-availability claims and all linked notebook docs so that they agree on these two distinct immutable SHAs.
- Ensure every setup cell rejects a stale or dirty checkout, performs locked dependency checks, detects missing or changed outputs, rejects stale replay/cache state, and explains what is and is not verified. Do not put GitHub personal access tokens in clone commands or errors.
- Validate links publicly, test a fresh clone, run the existing replay contract tests, and—if practical—execute at least one real Google Colab notebook end-to-end. **A simulated Colab run does not equal a real one.**
- Do **not** create or cite a nonexistent tag, GitHub release, Zenodo DOI, or stable package. If authors have not approved a release, use a truthful commit-pinned citation/proposal and flag the release as pending.
- Preserve historical audit logs as historical: add an accurately dated latest status rather than silently rewriting old commit-specific evidence.

**Acceptance criteria:** From a fresh reviewer route, every advertised link resolves to `NOTEBOOK_COMMIT`; every notebook checks out precisely `SOURCE_COMMIT`; the source includes the replay safety fixes; fast/replay tests pass on the actual tested source; all README and cover-letter references agree; no unavailable DOI is claimed.

## P2 — Mathematical explanation: the graph-order example is wrong

**Confirmed in `main.tex` near line 636:** the manuscript claims that its proof does not require equal order, “as the pair `K_4`, `K_{1,3}` ... illustrates.” In fact **both graphs have four vertices**.

**Implement the minimal recommended fix:**
- Replace that explanation with: **“The proof above does not require the graphs to have equal order.”** Do not use `K_4` versus `K_{1,3}` as evidence about different orders.
- If an example materially improves the exposition and the authors prefer one, `K_4` (four vertices, six edges, all q=0) and `C_6` (six vertices, six edges, all q=0) are an elementary **different-order same-histogram** example; verify exact graph and index facts before using it.
- **Keep** the existing `K_4` versus `K_{1,3}` illustration where it really concerns **nonalgebraic γ**, including the specific `γ=ln 4` statement, after independently confirming the equation and original logical role.
- Search and correct the same mistaken explanation in `audit/MATCH_RADA_Q_HISTOGRAM_PRIOR_ART_2026-10-23.md`, the final patch/audit reports, supplementary discussion and any cover letter. Label superseded historical reports appropriately rather than deleting evidence.
- Re-check the proof's domain, q-histogram definition, any fixed-order restriction in Rada's theorem and the manuscript's own argument. Do **not** weaken or change the theorem itself unless a real mathematical problem is established.

**Acceptance criteria:** No current explanatory text claims `K_4` and `K_{1,3}` have different numbers of vertices; the original nonalgebraic γ example is retained in its valid role; mathematics is unchanged; TeX and references compile.

## P2 — Prose checker: two falsely anchored assertions

**Confirmed in `prose_claims_a.py`, around lines 908–909:**
- `ext_tb_avg20`, allegedly checking **20** nonane boiling-point records selected as NIST averages, currently matches the text `020` inside DOI `10.1007/s40747-020-00262-0`.
- `ext_tb_single5`, allegedly checking **5** selected single NIST determinations, currently matches the `5` in degree pair `(3,5)` in a mathematical example.

The values **20** and **5** are reportedly correct counts, but these two patterns **do not verify those scientific prose claims**. Therefore “756 checked, zero failures” must not be interpreted as 756 correctly anchored assertions.

**Implement:**
1. Find where each scientific count is actually asserted (main TeX, supplement, README or a cited provenance table). Confirm each count independently from the appropriate provenance CSV and its selection rules.
2. If the count is expressed in a current manuscript/document, anchor the registry to that precise sentence and correct source-file designation. Require a unique match with sufficient surrounding semantics.
3. If the count was removed from the manuscript and is only data provenance, **retire the two stale prose entries** and add direct named provenance-count assertions in an appropriate test file instead. Do not artificially preserve “756” as the registry count.
4. Run **mutation tests**:
   - Changing the intended 20/5 claim must cause a failure.
   - Changing the DOI “020” or unrelated degree pair must not create a false provenance-count failure.
   - Missing/duplicated target sentence must fail closed if the registry declares it covered.
5. Review similar registry patterns for collisions against footnotes, citations, DOI fragments, bibliography and mathematical examples; list how many were sampled and any further bad anchors.

**Acceptance criteria:** Every retained numeric claim is matched to its intended sentence/data source, and final checked/uncheckable/removed counts are accurately documented with test logs.

## P3 — Supplement PDF: Table S8 interrupts references

**Independently reported from visual inspection; re-check in a fresh PDF build.** In the `f720a16` supplement, the References heading and entries [1]–[2] appeared on page 36, Table S8 on page 37, then more references afterward. Source near `supplement.tex` line 1660 starts `thebibliography` after an unflushed table environment.

**Implement:**
- Flush pending floats immediately before the bibliography, using the already available `\FloatBarrier`/float handling where appropriate, or a justified `\clearpage`.
- Rebuild the supplement **and every distributed copy**, including the submission ZIP/PDF; confirm numbering and contents did not change.
- Visually inspect the final bibliography pages and S8 placement, not merely “zero overfull boxes”. Confirm S8 completes before the References heading/first entry.
- Optionally simplify captions of Table 2 or Table 5 *only* if readability improves without altering statistical definitions or source distinctions; avoid a broad layout rewrite.

**Acceptance criteria:** The references form a contiguous section after the tables; no table interrupts them; both PDFs compile with no missing references; all distributed copies and clean-extraction builds agree.

## P4 — Freeze a coherent MATCH reviewer package

After the four targeted fixes:
- Preserve the **order-13/order-16 collision witnesses**, their minimality evidence and correct attribution to Rada and other predecessors. Do not claim a negative literature search proves worldwide novelty.
- Preserve negative QSPR results and limitations; 50 optimizer seeds are not 50 independent scientific samples; a conditional bootstrap that does not refit/retune cannot establish model equivalence.
- Run targeted math and proof integrity checks, affected table/caption checks, style/labels, `prose_numbers_check.py`, the three correction/review/replay-contract test programs, `constancy_test_check.py`, and `verify.py --offline`. Record full code paths, commands, exit codes, SHA, counts and skips.
- Run the full suite/Lean/Colab/source-dependent stages only when feasible and authorized; otherwise label them clearly **NOT RUN**, never inherited PASS.
- Rebuild `main.tex` and `supplement.tex` with pdflatex, all three Overleaf ZIP variants, the MATCH submission ZIP, PDFs, and `SHA256SUMS.txt`. Check for no missing files, placeholders, broken links, inconsistent PDF text or NIST materials.
- Distinguish a correct **current pinned citation** from a possible future DOI. The public `main` has been reported to expose 262 NIST pages and some long verbatim NIST-derived provenance fields: do not say this is resolved without verifying and obtaining the authors' release/rights decision.
- Obtain approval from all three authors for the manuscript and the previously flagged proposition terminology, chemical-graph definition, Rada credit and data-availability statement. Confirm the official supplement submission route with MATCH if still undocumented.

## Output reports (new local review branch)

Write:
- `audit/MATCH_FOUR_FINDINGS_RESOLUTION_2026-10-23.md` — exact source evidence, before/after text, acceptance tests, and status for each P1–P3 issue.
- `audit/MATCH_NUMERIC_REGISTRY_ANCHOR_AUDIT_2026-10-23.md` — wrong matches, corrected semantics, mutation-test logs, coverage counts.
- `audit/MATCH_REVIEWER_PINS_AND_REPLAY_2026-10-23.md` — source SHA, notebook SHA, links, clean clone/Colab tests and replay contract verification.
- `audit/MATCH_SUBMISSION_PDF_LAYOUT_2026-10-23.md` — screenshot/page check of final S8 and bibliography, PDF/ZIP hash agreement.
- `audit/MATCH_FINAL_RELEASE_GATE_2026-10-23.md` — last tested SHA, test matrix, NIST/rights/release/coauthor/supplement blockers, and `READY` / `CONDITIONALLY READY` / `NOT READY`.

## Final report back to authors

Give the verified baseline and new **local** commit(s); exact file modifications; corrected mathematical sentence; corrected numeric-checker mapping and coverage counts; fresh PDF page-placement outcome; reviewer-source and notebook commit pins; commands actually run and statuses; unresolved NIST/history/data-rights and author approval; and the final conditional publication verdict.

**Do not automatically publish or merge manuscript modifications.** This Markdown instruction itself was shared on GitHub so the authors can pull it. Author approval is required before pushing the repaired scientific candidate.

**Guiding principle:** fix genuine defects without changing the supported mathematics, freezing an out-of-date reviewer pathway, or claiming a reproducibility/release milestone that has not occurred.
