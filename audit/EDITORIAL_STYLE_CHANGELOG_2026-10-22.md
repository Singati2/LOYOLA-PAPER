# Editorial style changelog, 2026-10-22

This pass carries out `docs/CLAUDE_MANUSCRIPT_STYLE_REVISION_PROMPT_2026-10-22.md` and changes prose only.

- **Base:** `31e61ec` (`review/match-final-adjustments-2026-10-21`), fast-forwarded before committing to `723a2d0`, which adds only the GO file. `main.tex` is the same in both. No newer author-approved manuscript branch exists.
- **Branch:** `review/match-editorial-clarity-2026-10-22`, in a separate worktree.
- **Edited source:** `main.tex`. The three byte-identical copies were then overwritten from it:
  - `LOYOLA_MAIN_OVERLEAF/main.tex`
  - `LOYOLA_FINAL_PAPER_OVERLEAF/main.tex`
  - `submission_candidate/match/main.tex`
- **Unchanged:** `supplement.tex`.

Line numbers refer to the base file (`git show 31e61ec:main.tex`).

## Changes

| # | Where (base lines) | Before (excerpt) | After (excerpt) | Reason |
|---|---|---|---|---|
| 1 | Abstract, 195-213 | opens with "For a graph $G$, the Gutman--Milovanović index ..." | opens with the problem: "Vertex-degree-based indices cannot distinguish graphs with equal edge-degree-pair counts, and an index that depends on each edge only through its degree ratio can distinguish fewer graphs still. We determine where this second loss begins for trees ..." | Brief A: the abstract now states the problem before the definitions |
| 2 | Abstract, 207-209 | "We also show that two chemical graphs exchange order at most five times along $\gamma$, and that the path and the star are the extremal trees" | "Two chemical graphs exchange order at most five times along $\gamma$, and by criteria of Cruz and Rada the path and the star are the extremal trees" | Attribution. The abstract no longer claims the extremal-tree result as the authors' own (same point as change-report item `main.tex:208`) |
| 3 | Abstract, 205-207 | "..., with explicit counterexamples at every larger order." | "..., and explicit counterexamples exist at every larger order." | Wording only |
| 4 | Introduction, before 221 | survey of degree-based indices first | new first paragraph: the degree-pair ceiling, then the further loss through degree-ratio weights, then the question of the paper | Brief B: the introduction opens with the resolution-limit problem. The BID linear-functional sentence and its citations moved here from base 287-291 unchanged, and `\cite{Rada2026LinearVDB}` was added to the first sentence |
| 5 | Introduction, 287-293 | "On graphs with $\Delta \le 4$ every BID index is a linear functional ... so the whole family lies in a fixed ten-dimensional space." | "For $\Delta \le 4$ the whole family therefore lies in the fixed ten-dimensional space of linear functionals of the counts." | Removes a duplicate of the sentence moved in change 4 |
| 6 | Introduction, 308-315 | "What is new here is where these facts bind ... up to order $15$ and not beyond" | its own paragraph, beginning "What is new here ... By exhaustive enumeration, the $q$-histogram carries ..." | Separates known results from new ones. Adds the qualifier the brief requires: minimality rests on enumeration |
| 7 | Contributions, 317-345 | six items (i)-(vi), with known, new, computer-assisted and applied results mixed | four items by status: (i) known theorems applied to the family (Rada Thm 3.4 / Prop. 2.5, Cruz–Rada, degree-pair ceiling); (ii) results proved here; (iii) computer-assisted results; (iv) the diagnostic application | Brief B. Every reference and cross-reference is kept. Proposition `prop:offplane` was not in the old list and is now listed under (ii) as an application of the same transcendence argument (see author decision 1) |
| 8 | After the ratio-plane proof, 660 | one paragraph of about 400 words | four paragraphs: attribution; comparison with Song–Huang; earlier explicit examples; literature search and computer-assisted minimality | Readability. No sentence changed |
| 9 | Section 6 opening, 1552-1566 | design, provenance caveat and evidential status in one paragraph | three paragraphs: (a) the question of the section and the status of the evidence ("the octane correlations are descriptive ... primary predictive evidence"), (b) design, (c) provenance caveat and the tuning check | Brief D: question → design → caveat. One new opening sentence states the question. The other sentences are verbatim |
| 10 | 6.1, 1577 | data provenance and the 2,2,3,3-tetramethylbutane discussion in one paragraph | split before "The open items are ..." | Readability |
| 11 | 6.2, 1647-1686 | two dense paragraphs | five: narrow-box result; boundary diagnosis; dense grid and choice of box; wide-box rerun; fixed points; conclusion | Brief D. Sentences verbatim |
| 12 | 6.3, 1699-1729 | the verdict pointed to "the molecule-bootstrap interval reported at the end of this subsection"; the interval came four sentences later | the bootstrap interval sentence now follows the verdict directly, ending "and this interval includes $0$"; the subsection is split into design, verdict, interpretation, fixed point, reference models | Brief D: the result and its uncertainty sit together. The values and wording of the interval sentence are unchanged |
| 13 | 6.4, 1733-1828 | one paragraph of about 45 lines after the table | split into: verdicts; unregistered narrow-box comparisons; cohort correction; selection-aware resampling; interpretation; ridge reference; permutation check; Wiener model; conclusion. "The two summaries differ ... Nor are the ranges confidence intervals ..." moved from after the interpretation to directly after the resampling ranges it qualifies | Brief D. One sentence moved; no wording changed |
| 14 | Discussion, 1833-1835 | "The results of Sections ... are exact. Their limits ... are as follows." | new opening paragraph on what the mathematics establishes (counts ceiling, coarser $q$-histogram, orders 13/16, $\gamma$ reweights the same counts) and what the experiments did not show; then "... are of four kinds." | Brief E: substantive interpretation first. Each statement restates a result of Sections 3-6 (Theorem `thm:ratioplane`, Section `sec:degeneracy`, Section `sec:bp`) |
| 15 | Discussion list, 1836-1854 | items (i)-(iv) without headings | headed *Enumeration scope*, *Theoretical scope*, *Data quality*, *Inferential scope*; (iv) gains two sentences: "The negative verdicts mean that no gain was demonstrated. They do not show that $\gamma$ never helps, and no equivalence margin was registered" | Brief E. Restates Section 6.4. The protocol-deviation table is unchanged |
| 16 | Conclusion, 1895-1916 | two paragraphs restating most results, ending with three open problems | three paragraphs: (1) Rada's theorems as the tool and the location of the limit (orders 12/13, 16) as the contribution, with "The minimality of these orders rests on exhaustive enumeration"; (2) the QSPR outcome; (3) one open problem (extremal graphs for general triples, starting with the maximal chemical trees of the pure-imbalance points) | Brief F. Removed from the conclusion: path/star extremality, the remark about the untuned point and *IRLA*, and the open problems on ABC/Sombor bounds and other compound classes (see author decision 3) |
| 17 | Data availability, 1919-1929 | two sentences both citing the repository; one long Lean sentence | the repository contents in one sentence; the Lean scope in its own paragraph, opening "Only part of the mathematics is machine-checked." | Brief G. Readability; the scope of the Lean check is unchanged |

## Not changed

- **Sections 2-5:** apart from change 8, these were left as they are. Their exposition is already tied to the statements, and the brief forbids shortening proofs.
- **Tables, figure and captions:** unchanged.
- **Acknowledgment:** "The authors thank colleagues for helpful discussions" is unchanged. It is a placeholder, and the authors must supply the real text.

## Decisions for the authors

1. **Proposition `prop:offplane`:** contribution (ii) now lists it as a result proved here. Its proof applies Lindemann–Weierstrass in the way of Rada's Theorem 3.4. Decide whether to call it new or a consequence of Rada's argument.
2. **Abstract opening:** the abstract now opens with "an index that depends on each edge only through its degree ratio can distinguish fewer graphs still". Check that you are happy with this framing.
3. **Open problems:** the conclusion now names one. The other two (sharp two-sided bounds in ABC/Sombor; other compound classes) were removed from the paper. Restore them if you want them stated.
4. **Page count:** the paper grew from 45 to 46 pages, because the paragraph breaks add white space. There is no page cap.
5. **Acknowledgment:** the text still has to be written.
