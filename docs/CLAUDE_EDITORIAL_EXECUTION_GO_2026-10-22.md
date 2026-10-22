# Claude — GO: execute LOYOLA-PAPER editorial revision

**Date:** 2026-10-22  
**Repository:** https://github.com/Singati2/LOYOLA-PAPER  
**Instruction status:** Author-approved **start of editorial work**, not approval to publish or merge the rewritten manuscript.  
**Base:** Latest verified commit on `review/match-final-adjustments-2026-10-21`.  
**Required detailed brief:** `docs/CLAUDE_MANUSCRIPT_STYLE_REVISION_PROMPT_2026-10-22.md`

## Go ahead

Read and execute the detailed brief above. This file explicitly authorizes starting the **prose-only editorial revision**. Do not await another "go" instruction. Keep the work isolated from other active projects and worktrees.

1. Check the repository's current status, branch heads, active worktrees, and in-progress tasks. Record the exact baseline commit SHA. If the intended base changed, inspect those changes and use the latest *verified* baseline. Never discard, stash, or overwrite someone else's uncommitted work.
2. Create a **separate worktree** and new branch named `review/match-editorial-clarity-2026-10-22`. If that branch already exists, inspect its history and status before reusing it; do not reset or overwrite it.
3. Improve the manuscript's abstract, introduction, transitions around mathematical exposition, QSPR analysis, limitations, and conclusion. Make the prose concise, clear, natural, and appropriate for *MATCH Communications in Mathematical and in Computer Chemistry*. Remove generic stage-setting, redundant claims, overly dense sentences, and audit-report-style repetition while keeping the authors' intellectual voice.
4. **Do not change the scientific content:** preserve theorems, proof logic, assumptions, quantified statements, notation, formulas, tables, figures, labels, citations, authorship metadata, verified numerical findings, protocols, and data provenance. Do not invent results or strengthen the novelty, inference, or practical predictive claims.
5. Clearly distinguish new contributions from work already known from Rada, Cruz–Rada, and other cited sources. Preserve the ratio-plane distinctions, algebraic/rational parameter restrictions, first collision orders (13 general trees, 16 chemical trees), enumeration limits, five-exchange upper bound and sharpness uncertainty.
6. Retain the negative QSPR conclusions, uncertainty intervals, the distinction between pre-registered and exploratory analyses, the parent-search-box limitation, and the limits of Lean verification. Do not remove or hide post hoc disclosures or convert point-estimate comparisons into general superiority claims.
7. Prepare two Markdown reports:
   - `audit/EDITORIAL_STYLE_CHANGELOG_2026-10-22.md` — the locations, rationale, and representative before/after text for each substantive prose edit.
   - `audit/EDITORIAL_PRESERVATION_CHECK_2026-10-22.md` — base SHA, modified files, diff verification, and a truthful PASS/FAIL/NOT RUN table for build/reference/label checks.
8. Build the LaTeX manuscript and run relevant inexpensive consistency checks if available. Avoid numerical recomputation, frozen-protocol changes, and expensive verification runs. If LaTeX cannot be built, disclose that clearly.
9. Review the full diff to ensure there are no accidental changes to math, proof statements, citations, metadata, figures, tables, or statistical conclusions. Flag ambiguities for the authors instead of silently resolving them.
10. Commit the editorial revision **locally only** on the new branch. **Do not push the edited manuscript, merge to `main`, force-push, or rewrite history** until the authors review the diff and reports.

## Separate main-branch cleanup — do not touch

The worktree `wt-mainrevert` contains a staged revert related to seven `Created using Colab` commits on `main`. This is a **different task** and is **not authorized by this instruction**. Do not run its pending commands, commit its staged changes, push its branch, reset it, or disturb its contents. If it interferes with the editorial task, stop and report the conflict.

## Required completion report

Provide the base commit, editorial branch and local commit hash; sections and files edited; three or more specific before/after examples; precise status of LaTeX and lightweight checks; unresolved concerns; and confirmation that **no manuscript push or merge occurred**.

**Quality criterion:** Improve mathematical clarity, accurate attribution, readable academic prose, and submission readiness. This is not a task to evade AI detectors or make unverifiable claims about who wrote the paper.
