# Claude Prompt — LOYOLA-PAPER Literature, Writing, and MATCH Submission Audit

**Date:** October 23, 2026
**Repository:** Singati2/LOYOLA-PAPER
**Baseline:** review/match-editorial-clarity-2026-10-22 at e25d790
**Journal:** MATCH Communications in Mathematical and in Computer Chemistry

## Objective
Incorporate the handwritten research-writing advice thoughtfully into a rigorous final editorial and scientific audit of the LOYOLA paper: organize research logically (IMRaD as a diagnostic, not compulsory section headings), include clear analysis and interpretation of results and graphs, strengthen literature review, use paper-discovery tools responsibly, maintain references, polish English, and check citations and publication ethics. Do not rewrite the paper merely to satisfy an AI detector or reach an arbitrary page count.

## Mandatory safeguards
1. Fetch and verify the remote baseline. Work only in a NEW local branch/worktree; do not edit the public review branch, main, or wt-mainrevert.
2. Do not push, merge, force-push, open a PR, or submit the paper. Commit any reviewed work locally only, pending author authorization.
3. Preserve the 46-page archive, existing 35-page paper and 39-page supplement as recoverable reference versions.
4. Do not change theorem statements, hypotheses, proofs, registered results, experiments, data, code, protocols, selection rules, seeds, statistical intervals, or negative conclusions without independently demonstrating an error and recording proposed changes for author approval.
5. Do not copy copyrighted NIST/KDB/Chemeo pages, paywalled articles, tokens, private data or other restricted materials into the public repository.
6. Do not fabricate references, results, web searches or verification passes. AI/similarity detectors do not establish authorship or plagiarism. Check the target journal's current policies rather than guessing.

## A. Establish evidence and baseline
Read main.tex, supplement.tex, audit/MATCH_SHORTENING_REPORT_2026-10-23.md, audit/FEYNMAN_REVIEW_2026-10-23.md, REPRODUCE.md, REVIEWER_START_HERE.md, the relevant bibliography, figures, result artifacts and cover-letter draft. Compare against the preserved 46-page version. Verify actual author count, author order, affiliations and corresponding author using the manuscript and author confirmation; do not rely on conflicting historical descriptions. Preserve the status distinction between checks passed on e25d790 and checks passed only on earlier commits.

## B. Literature and novelty audit — highest priority
Use a claim-by-claim prior-literature comparison. Focus on degree-based topological indices; edge-degree pair counts and linearity; degree-imbalance descriptors; Rada's relevant results and other MATCH literature; Cruz–Rada bounds and equality cases; ratio-plane statements, algebraic parameters and Lindemann–Weierstrass reasoning; graph and chemical-tree collision/minimality claims; and statistical QSPR evidence in small alkane cohorts.

Produce a matrix with:
- Manuscript claim and exact section
- Closest published result, verifiable citation and source location
- What prior authors established
- What this manuscript demonstrably adds
- Novel / known / adapted / computational / exploratory classification
- Corrected wording or missing citation
- Confidence and whether full primary source was examined

Use Semantic Scholar, Elicit, Consensus, ResearchRabbit, Connected Papers, SciSpace, and citation chaining as discovery tools if available, but verify source details and claims in the original articles. Mark inaccessible papers as unverified. Avoid asserting the off-plane argument is a new theorem if derived from prior work. Carefully distinguish what an individual index can discriminate from what equality of the full degree-imbalance histogram implies. Ensure abstract, introduction, contribution paragraph, conclusion, README and cover letter agree on novelty.

## C. Scientific narrative: adapt IMRaD without forcing it
Review the abstract and introduction for motivation, chemical relevance, actual research gap, proper citation and clear contributions. Make mathematical definitions, theorem/proof dependencies and algorithmic methods locatable. Separate established theorems, computational enumerations and exploratory QSPR outcomes. Ensure discussion and conclusion interpret limitations and genuinely negative or inconclusive results.

Specifically evaluate whether moving the proofs of Lemma 1 and Theorem 1 to Supplement S10 makes the main paper insufficiently self-contained for MATCH reviewers. Recommend their restoration only if justified by dependency or comprehension needs; avoid restoring material just to increase length. Assess whether the separate 39-page supplement can be submitted under MATCH rules, and flag editorial confirmation if not explicit.

## D. Graphs, tables, footnotes and statistics
Audit every figure and table in main and supplement (including Figure 1, Tables 1–5 and Supplementary Table S8):
- Compare all displayed values and counts against source artifacts, checked code or certified output, documenting missing sources.
- Verify each caption and footnote defines population/cohort, units, model, sample size, intervals, uncertainty metric, abbreviations, fixed versus selected hyperparameters, controls, exceptions and limitations as appropriate.
- Check numbering and cross-references after the shortening, especially S10–S11.
- Check every surrounding prose interpretation; avoid calling exploratory or post-selection fits independent generalization.
- Present a ledger: Object | Location | Source | Verified? | Caption/footnote concern | Proposed correction.

Independently check the reported decane median ΔQ² = −0.072, Loyola ahead in 15/50 seeds, interval [−0.156, +0.001], and what can and cannot be concluded. Confirm Q² uses the documented PRESS/SS_tot definition around the full-sample mean and clearly distinguish ordinary from nested leave-one-out. Check the tetramethylbutane use of 10.263 kcal/mol, maximum |r| approximately 0.37353, and hypothetical-liquid comparison 0.970. Do not substitute the erroneous rounded-input 0.375 claim.

## E. Literature-review tooling, references, prose and ethics
Treat Elicit, Consensus, Semantic Scholar and citation-network tools as discovery aids, not authorities. A lightweight literature mind map or thematic reading map may be useful; prioritize directly related original articles over decorative diagrams. Check bibliography authors, publication year, title, journal, DOI, pages, ordering, duplicates, and citation-to-claim correctness. Identify unsupported references, near-verbatim paraphrases or plagiarism risks by reviewing the actual passages, not relying on detector scores. Explain any source access gaps.

Polish grammar, terminology, consistency, transitions and scientific precision while retaining the author's voice and all qualifications. Do not add generic filler. Verify and preserve the authors' approved acknowledgement credit to the Machine Perception and Robotics/Cognitive Lab at Florida Atlantic University for computing setup; confirm exact official lab naming before editing. Check overlapping companion-manuscript disclosures, data rights, repository citation pin/DOI and AI-use policy. Do not make author/affiliation changes without author consent.

## F. Validation and outputs
Perform proportionate, safe local checks and report exactly what ran. For changed text, rerun style, labels/cross-references, prose-number checks and both PDF builds; confirm captions/footnotes visually where feasible. Run or request permission for full mathematical/Lean, NIST-dependent, Colab and expensive statistical suites only when necessary; never imply these passed on e25d790 if they were not rerun. Keep code, running jobs and frozen protocols unchanged.

Write:
1. audit/MATCH_LITERATURE_NOVELTY_MATRIX_2026-10-23.md
2. audit/MATCH_TABLE_FIGURE_CAPTION_AUDIT_2026-10-23.md
3. audit/MATCH_SECTION_CONSISTENCY_AUDIT_2026-10-23.md
4. audit/MATCH_REFERENCES_ETHICS_AUDIT_2026-10-23.md
5. audit/MATCH_FINAL_SUBMISSION_DECISION_2026-10-23.md
6. audit/MATCH_PATCH_LOG_2026-10-23.md, if edits are made.

All findings must cite exact file paths/lines and source evidence. Rate issues BLOCKER, IMPORTANT or OPTIONAL. The final verdict must be READY, CONDITIONALLY READY, or NOT READY, include a concise three-item priority list, the known verification gaps, a precise author-approval checklist and a list of unchanged scientific results. Keep recommendations distinct from implemented changes.

**STOP:** After local review and local commits, report results and obtain approval. Do not push this audit or manuscript changes to GitHub.