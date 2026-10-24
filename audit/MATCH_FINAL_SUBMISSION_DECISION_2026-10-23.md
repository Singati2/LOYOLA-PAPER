# Final submission decision: literature and writing audit, 2026-10-23

## Verdict: CONDITIONALLY READY

The mathematics, the attributions and the numbers hold up:
- **Attributions.** Every one was checked against the primary full text, at the location cited.
- **Bibliography.** All 56 main entries and 21 supplement entries agree with Crossref, OpenAlex, arXiv or the MATCH contents pages.
- **Citations.** No citation is unsupported.
- **Copying.** No prose run of 8 or more words is shared with any local full text.
- **Numbers.** The decane, pooled, Q², tetramethylbutane, table and figure values reproduce, by independent code where noted.

Two blockers remain. Both are author actions and cannot be fixed by editing the text.

| # | Blocker | Evidence | Owner |
|---|---|---|---|
| B1 | **The repository citation is unpinned, and the default branch redistributes NIST pages.** `\bibitem{LoyolaRepo}` gives only the URL. That URL opens `main` (`fa6c881`, 21 Oct), which tracks 262 NIST WebBook HTML pages and predates the current supplement numbering. The data-availability sentence is now worded for "the release of the package cited here" (E1); it is true only once a release is pinned. | `git ls-tree origin/main`; main.tex, Data availability | Authors: tag and archive the approved commit (for example with a Zenodo DOI) and cite it; decide what to do with `main` |
| B2 | **No record of all-author approval.** MATCH's ethics page requires that all co-authors have seen and approved the final version. | `docs/match/07_ETHICS_LICENSE_AUTHOR_DECISIONS.md` | Corresponding author |

## Three priorities

1. **Resolve B1.** Pin and archive the cited release, then repin `README.md`, `REVIEWER_START_HERE.md` and the Colab notebooks, which still point to `c48bad05`. Then decide how `main` should stop serving the NIST pages. A normal commit removes them from the tip; removing them from history would be a destructive public action needing separate authorization.
2. **Approve the patches.** All three authors should approve this branch's edits (patch log, especially W4–W5, D1, L3 and E1) and the earlier P1–P4. Record the approval (B2).
3. **Answer the contribution objection.** The literature matrix confirms that the theory is mostly known or adapted, all of it credited. What is new is the 13/16 witnesses, their computer-assisted minimality, Lemma 1, the Laguerre application and Example 1. The earlier audit's Option B is still recommended: cut Section 6 to about 3 pages and lead with 13/16.

## Known verification gaps

| Check | Status |
|---|---|
| `verify.py --offline` | **ALL PASS**, exit 0 (see the last section) |
| `verify.py --full` and `--everything`, Lean | NOT RUN on this branch; passed only at `390728b`. `formal/` is unchanged |
| NIST-dependent stages | BLOCKED: the pages are not in this tree, and NIST is not to be contacted |
| Colab notebooks | UNVERIFIED |
| 50-seed searches, bootstraps, permutation tests | NOT RUN; no input changed. The decane contrast was re-implemented independently and reproduces (−0.0715, 15/50, [−0.156, +0.001]) |
| Exact radical certification behind Table 2 | NOT RERUN on this branch; covered by the "collision minimality" verifier stage |
| Gao–Gao 2024, Gutman–Buragohain–Nyauli 2026 | NOT VERIFIABLE: paywalled, no abstract reachable; bibliographic records only |
| Besicovitch, Lindemann–Weierstrass, Wiener 1947 | Supported through secondary sources only |
| Semantic Scholar discovery | Rate-limited; discovery used Consensus, web search, OpenAlex and the repository's 20-query log |

**Novelty.** No earlier determination of the orders 13 and 16 was found. The queries are in the novelty matrix. This is an absence of evidence, not a proof of novelty, and the manuscript words it that way (L2).

## Author-approval checklist

- [ ] Patch log of this branch read; W4–W5 (Proposition title and wording), D1 (chemical-tree definition), L3 (Rada Corollary 3.5 credit) and E1 (availability wording) approved
- [ ] Earlier audit edits P1–P4 (`MATCH_FINAL_PATCHLOG_2026-10-23.md`) approved
- [ ] Repository release pinned and archived; `\bibitem{LoyolaRepo}` updated; reviewer docs and notebooks repinned
- [ ] Decision recorded on the NIST pages on `main` and in history
- [ ] Contribution framing chosen (Option A or B)
- [ ] Title confirmed
- [ ] Names, order, affiliations and e-mails confirmed by each author
- [ ] Acknowledgment confirmed. The lab's own site gives the name used in the paper, "Machine Perception and Cognitive Robotics" (mpcrlab.com). The two audit briefs use a different wording, which is not the official name
- [ ] Companion-manuscript status and citation decided
- [ ] AI-use disclosure decided. MATCH's prepare and ethics pages, read 2026-10-23, say nothing on AI tools, supplements, data or conflicts
- [ ] Supplement route confirmed with the editorial office (unsent draft in `MATCH_SUBMISSION_DECISIONS_2026-10-23.md`)
- [ ] Optional items in the patch log accepted or declined
- [ ] All three authors approve the final PDF (MATCH ethics page)

## Lemma 1, Theorem 1 and the supplement

- **Lemma 1.** Its proof is restored in the main text. Its proof is the only argument for the paper's claim that γ is a new direction.
- **Theorem 1.** Nothing in the main text depends on its proof, which is cited once, in the contribution list. It stays in Supplement S10. Optionally rename it a Proposition and cite Brown 1986 (patch log, not applied).
- **Supplement.** MATCH's pages do not say whether a separate 39-page supplement may be submitted. This needs confirmation from the editorial office.

## Scientific results left unchanged

- Theorem 2 (i)–(iii), Propositions 3–7, Lemma 1, Theorem 1, Example 1 and the remarks: same mathematics; only W4–W5 wording and the L3 credit changed.
- The first-failure orders 13 (trees) and 16 (chemical trees); the floors 12 and 15; Table 2.
- The octane correlations (Table 4), the collision pairs (Table 1), structure sensitivity (Table 3) and Figure 1.
- The matched-budget ablation, the wide-box rerun and the hybrid control (−0.002, 24/50).
- The nonane protocol verdicts (95/100, 98/100; mixed for T_B) and the bootstrap interval [−0.006, +0.113].
- The boiling-point tests, both negative: decanes −0.072, 15/50, [−0.156, +0.001]; pooled −0.0001, 25/50, [−0.003, +0.002].
- Ridge and Wiener comparisons; tetramethylbutane sensitivity (0.980, 0.976 against 0.970, ≤ 0.374).
- All limitations and the single open problem.

## Verification on this branch

See the end of the patch log for the checks run after the edits.

`verify.py --offline` was run on the branch working tree after all edits:
- **First run:** failed one stage. The constancy guard flagged the two new recompute scripts as unlisted candidate generators.
- **Fix:** they were added to the guard's `NOT_SELECTION` list, which is the list meant for audit-only checkers.
- **Second run:** **ALL PASS**, exit 0, about 20 minutes:
  - core verifier FULL PASS, covering all 8 numeric tables;
  - prose numbers 756/0;
  - external regression tests;
  - baseline tests;
  - constancy;
  - interval certificates;
  - style;
  - extremal trees 4–12;
  - collision minimality 13/16;
  - sum-connectivity pair;
  - count dimension and floor;
  - DATA copies;
  - manifest (447 files);
  - CRLF convention.

The NIST stages were **NOT RUN**. Only this report, the patch log and `SHA256SUMS.txt` changed after the run; the manifest was rewritten and rechecked before the commit.
