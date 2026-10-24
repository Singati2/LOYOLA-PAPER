# Claude execution brief — Verify the unpublished MATCH audit, then implement only supported fixes

**Created:** 2026-10-23  
**Repository:** https://github.com/Singati2/LOYOLA-PAPER  
**Published instruction branch:** review/match-editorial-clarity-2026-10-22 (previous tip 2491f0e)  
**Unpublished work to inspect on the lab machine:** review/match-literature-writing-audit-2026-10-23, commit 3a5f061  
**Submission target:** MATCH Communications in Mathematical and in Computer Chemistry

> **Source/evidence boundary:** The following audit findings and results were REPORTED by Claude in the author's pasted local-session transcript. They are not automatically verified facts. The local commit 3a5f061 was NOT on GitHub when this brief was prepared. The purpose of this file is to let Claude inspect that actual local commit, establish which claims are genuine, make only evidenced fixes, and report what can safely be published. Do NOT try to reconstruct the missing local commit from this summary or claim the manuscript changes were pushed.

## 1. Begin with the actual local audit, not the public documentation branch

On the lab machine where the local audit was performed:

1. Locate the correct repository and worktree. Run git status, git worktree list, git log --oneline --decorate -15, git show --stat 3a5f061, and compare the audit commit against its actual parent. Confirm the SHA and full changed-file list.
2. Read these six local files in full:
   - audit/MATCH_LITERATURE_NOVELTY_MATRIX_2026-10-23.md
   - audit/MATCH_TABLE_FIGURE_CAPTION_AUDIT_2026-10-23.md
   - audit/MATCH_SECTION_CONSISTENCY_AUDIT_2026-10-23.md
   - audit/MATCH_REFERENCES_ETHICS_AUDIT_2026-10-23.md
   - audit/MATCH_FINAL_SUBMISSION_DECISION_2026-10-23.md
   - audit/MATCH_PATCH_LOG_2026-10-23.md
3. Inspect the modified main.tex, supplement.tex, bibliography, README, cover-letter draft, number/citation registries, audit scripts, verifier guard/allowlist, and any modified build scripts.
4. If 3a5f061 or any of its audit files is missing, STOP the implementation; identify the missing material. Do not replace it with guessed changes.
5. Create a NEW local review worktree from the real 3a5f061, leaving that original commit, public editorial branch, main, preserved 46-page manuscript, and wt-mainrevert unchanged.

## 2. Evaluate the exact claims reported in the previous audit

Prepare a table with **claim | supporting local diff/lines | independently checked source/test | VERIFIED / PARTLY VERIFIED / UNSUPPORTED / FALSE / BLOCKED | action**.

### 2A. Literature claims

Reported by the earlier audit:
- Credits to Rada, Cruz–Rada, and Rada–Rodríguez–Sigarreta were checked against full texts.
- **Previously missing:** Rada 2019, Corollary 3.5, allegedly implies that the exponential geometric–arithmetic (GA) index separates exactly the same q-histogram classes for equal-order graphs.
- No earlier determination of collision orders 13 and 16 was found; the original search claim was narrowed.
- All **56 main** and **21 supplementary** bibliography entries were said to match publisher records and be alphabetical; no unsupported citations or copied passages were identified.

**Do not accept these statements merely because the prior audit says they were checked.** Inspect original Rada 2019 Theorem 3.4, Corollary 3.5, and the index/function definitions. Establish mathematically whether Rada's index-induced equivalence is EXACTLY the manuscript's q-histogram equivalence, or only a related/conditional relation. Distinguish equal order, degree-pair orientation, symmetry, graph assumptions, and degeneracies. Record a proof or counterexample. Only then decide the correct credit and novelty wording.

For the other named papers, cross-check the exact theorem/corollary, equality and uniqueness conditions, and supported in-text claim. Verify an appropriately bounded prior-art search for orders 13 and 16, including search terms and sources; a negative search is not a proof of novelty. Do not invent new claims of first discovery.

### 2B. Numerical claims

Reported as independently reproduced:
- Decane comparison: median delta-Q-squared **−0.072**, LO family ahead **15 of 50 seeds**, interval **[−0.156, +0.001]**.
- Pooled test, Q-squared definition and implementation, tetramethylbutane results, Tables 1–5, and Figure 1.

Reproduce these from fixed data and recorded methods where feasible. Identify input files, commands, output hashes, verification level, and any access issues. In particular:
- The decane interval includes zero; the point estimate favours the parent, but neither a gain nor a loss is established by that interval alone.
- Check ordinary fixed-feature leave-one-out versus nested selection and whether Q-squared equals one minus PRESS divided by full-sample-mean SS-total.
- Use the actual tetramethylbutane input **10.263 kcal/mol**, not its rounded 10.26 value; recheck |r| about 0.37353 and the hypothetical-liquid 0.970 comparison.
- Compare each table entry, figure axis/legend, caption, footnote, denominator, sample size, uncertainty convention, and surrounding interpretation with original outputs. Never recalculate a new result and silently substitute it for the frozen result.

### 2C. Claimed wording/caption edits

The audit says that ONLY language, captions, attribution, and documentation were edited; no result/data/figure changed. Confirm this from the FULL diff, including any new audit recomputation scripts or guard modifications. Audit these exact edits individually:

1. "exchange order" to "values cross" — verify it correctly describes the plotted mathematical behavior and does not confuse vertex order.
2. Definitions of **chemical graphs** and **chemical trees** — ensure consistency with degree bounds, connectedness and actual enumeration protocols.
3. Citation for original **octane data source** in main text — ensure real dataset provenance and units.
4. Clarified captions for **Table 1**, **Table 5**, and **Supplementary Table S7** — independently check values, population, model, units and footnotes.
5. Tightened language for local tuning, replication, point estimates, negative or inconclusive results, and post-selection evaluation — don't turn exploratory findings into confirmatory claims.
6. Corrected supplement cross-reference — check both compiled PDFs and numbering.
7. README and cover letter aligned with contribution, statistical and release claims — confirm exact consistency with manuscript.
8. Two manuscripts are reported: **37 pages main / 39 pages supplement**, versus the earlier **35 / 39**. Explain why the extra two pages appeared; do not optimize page count at the expense of science.

### 2D. Author-controlled edits

The earlier audit explicitly reserved author approval for these FOUR items. Provide exact BEFORE and AFTER text, rationale, source and a checkbox-style signoff record for each. Do not classify them as author-approved:
- Proposition title and wording.
- New definition of chemical graph/chemical tree.
- Credit to Rada 2019.
- Availability sentence referring to "the release of the package cited here".

The lab acknowledgment was reportedly already correct as **Machine Perception and Cognitive Robotics** (mpcrlab.com); verify the official lab name and do not alter an already correct acknowledgment merely to match inaccurate brief wording.

## 3. Address two genuine-looking but UNRESOLVED release/security problems

### A. Public NIST material

The prior audit says public main still exposes **262 NIST pages**. Inspect public tracked files, archives, binary assets, publication branches, and relevant Git history to find exactly what is exposed. Determine redistribution permissions from authoritative sources rather than guessing. Do not copy copyrighted pages into a new branch or release; merely deleting them from the tip does NOT erase exposure in old commits. Provide remediation options and their risks. Never force-push or rewrite public history without explicit author approval.

### B. Claim about an immutable package release

The revised data-availability wording ("the release of the package cited here") is conditional: verify whether a real, immutable **specific commit/tag/DOI and release artifact** exists. If not, do not publish an untrue release statement. Either cite an existing exact commit with a truthful availability description or prepare a proposed Zenodo/tag plan and mark it BLOCKED pending release creation and author approval. Do NOT create a tag, DOI, deposit or public release without authorization.

## 4. Independently audit the fast verifier change

Earlier audit report:
- First offline verifier run FAILED at one stage when new audit-only recomputation scripts were caught by a guard.
- Claude expanded the audit-only script allowlist and the next fast offline verifier run returned ALL PASS.
- Clean rebuilding the ZIP reportedly yielded text identical to included PDFs.
- **NOT RUN** on the 3a5f061 tree: full verifier, Lean, Colab, NIST-page-dependent stages.

Do not accept green status at face value. Show the exact failing log, original and revised allowlist, each added script and the guard's documented purpose. Confirm new audit scripts are genuinely read-only/isolated. Add an adversarial negative-control test: intentionally introduce a prohibited change in an isolated worktree and demonstrate the guard STILL fails, then restore everything. If the allowed scripts bypass substantive protections, revert the guard relaxation and leave the audit as failing/blocked. Separately rerun the final safe test suite, caption/cross-reference tests, manifest checks and source-to-ZIP PDF text equivalence; report every actual command, tree SHA, exit code and not-run requirement.

## 5. Decide what to implement — not all reported fixes are automatic

**Implement now in the NEW local worktree when independently supported:**
- Precise attribution, no overstated novelty.
- Minimal correct definitions and data provenance citation.
- Verified wording ("values cross" if applicable), table/figure captions, footnotes and cross-references.
- Cautious nested-vs-ordinary validation descriptions, negative-result interpretation and non-overclaiming replication language.
- README and cover-letter alignment with the true state of the manuscript.

**Do not implement without author decision:**
- Material alteration of theorem/proposition content, definition scope or mathematics.
- Any unverified Rada-to-q-histogram equivalence.
- A data-availability sentence that assumes an unpublished release exists.
- A public NIST history rewrite, DOI/tag/Zenodo publication or companion-paper disclosures that need consent.
- Any experimental/data/code change, rerun that could disrupt running jobs, removal of necessary proof material, or weakening of verification guards.

Preserve **all existing results, numeric tables, original computations, frozen protocols, seeds, figures, 46-page historical copy, full mathematical claims unless disproved**, and the negative/inconclusive chemistry results. No generic AI rewriting and no changes intended to defeat AI detectors. Prefer scientifically necessary corrections over a specific page limit.

## 6. Required deliverables on the new local branch

Write/update these reports, with exact file paths, original-source pages and commands:

- audit/MATCH_LOCAL_AUDIT_GENUINENESS_2026-10-23.md — independent claims/evidence matrix.
- audit/MATCH_RADA_Q_HISTOGRAM_PRIOR_ART_2026-10-23.md — formal mapping, proof/counterexample, and corrected novelty language.
- audit/MATCH_FINAL_TEXT_PATCHES_2026-10-23.md — line-by-line before/after corrections and review status.
- audit/MATCH_CAPTIONS_STATISTICS_CROSSCHECK_2026-10-23.md — all tables/figures, footnotes, Q-squared, negative results and provenance.
- audit/MATCH_VERIFIER_GUARD_INDEPENDENCE_2026-10-23.md — first failure, allowlist change, negative tests and final pass/fail.
- audit/MATCH_NIST_RELEASE_RIGHTS_2026-10-23.md — exact exposure, permissions status, accurate availability text and remediation/release options.
- audit/MATCH_FINAL_COAUTHOR_GATE_2026-10-23.md — four signoffs, NIST/license actions, archived citation, supplement routing, reproducibility gaps, MATCH readiness.

Final response must give: genuine vs unsupported audit findings; changed file list and new LOCAL commit; exact full/fast checks actually run; page counts and main/supplement comparison; immutable citation status; NIST concern; author decisions; and READY / CONDITIONALLY READY / NOT READY with no ambiguity.

## 7. GitHub publication rule

This Markdown instruction file is being placed on the **existing PUBLIC editorial review branch** so you can read it remotely. It is NOT a push of the unpublished audit work or manuscript corrections.

**Keep 3a5f061 intact and local for inspection.** Do NOT push the local audit branch, the new implementation branch, a manuscript ZIP, NIST material or altered main automatically. First present the complete evidence/verification report and obtain explicit author permission to publish the reviewed manuscript branch. When permission is given, push a NEW branch with normal fast-forward history only, verify the remote SHA, and do not merge main or open a PR unless requested.

**Success criterion:** defensible novelty/attribution, preserved mathematics and statistics, independently checked guard and citations, transparent unresolved legal/release/author decisions, and a coherent MATCH manuscript—not merely a green test badge.
