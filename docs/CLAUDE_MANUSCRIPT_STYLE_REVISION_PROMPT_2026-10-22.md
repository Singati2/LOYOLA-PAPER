# Claude editing prompt: LOYOLA manuscript — precise, natural mathematical writing

**Date:** 22 October 2026  
**Repository:** https://github.com/Singati2/LOYOLA-PAPER  
**Starting branch:** review/match-final-adjustments-2026-10-21  
**Main manuscript:** main.tex  
**Intended outlet:** MATCH Communications in Mathematical and in Computer Chemistry  
**Task type:** Evidence-preserving editorial revision, not new research.

## Mission

Act as a careful mathematical-sciences journal editor and reproducibility-aware coauthor. Revise the LOYOLA paper so its language is **direct, specific, proportionate, and recognisably appropriate to a mathematical research article**, rather than resembling a generic literature survey, a project-management summary, or a running audit report.

The objective is **better scientific communication**, not defeating AI detectors or disguising the use of writing tools. Textual style cannot establish who wrote a manuscript. Do not make statements about human or AI authorship that are not documented. Preserve all truthful acknowledgments and follow the eventual journal's AI-assistance disclosure rules if applicable.

**Do the editing, not just a critique.** Make controlled prose-only improvements, with a traceable change log, on a fresh editorial review branch. Do not change mathematical results to make the paper sound more impressive.

## Source-of-truth and safety rules

1. Inspect the repository, branches, clean/dirty Git status, and the current main.tex before touching files. Start from review/match-final-adjustments-2026-10-21, **unless a newer author-approved manuscript branch exists**, in which case document the choice and exact commit hash before proceeding.
2. Work on a **new branch**, suggested name review/match-editorial-clarity-2026-10-22. Never directly modify main or rewrite another review branch.
3. Do not force-push, merge, squash, rebase an in-progress branch, delete data, overwrite uncommitted work, alter Git history, or interrupt any running tests.
4. Treat the existing verified mathematics and numerical outputs as frozen. Do **not** rerun expensive computations or change code, datasets, preregistered plans, random seeds, candidate grids, tables, figures, certificates, Lean proofs, or dependency locks for an editorial task.
5. Do not modify a theorem statement, lemma, hypothesis, quantifier, proof, symbol, equation, displayed formula, domain restriction, reference number, numerical value, or mathematical implication as part of a stylistic simplification. Preserve LaTeX labels, cross-references, and bibliography keys.
6. If a sentence is conceptually wrong, ambiguous, internally inconsistent, unsupported, or incompatible with its citation, **flag it for author review** rather than silently changing its scientific meaning.
7. Never invent citations, experimental checks, preregistration, significance, effect sizes, physical interpretations, or stronger novelty claims.
8. Avoid absolute claims of methodological superiority, statistical equivalence, or validation when evidence establishes only a point estimate, a conditional interval, or failure to demonstrate improvement.
9. Keep the paper's exact disclosures of post hoc decisions and deviations. Reorganising them is acceptable only if their substance, prominence, and traceability are retained.
10. Do not expand the mathematics. This is a prose and organisation pass.

## Key scientific distinctions that must survive verbatim in meaning

- The Loyola family extends the Gutman–Milovanović family through a normalised degree-imbalance exponential factor. At gamma = 0 it equals the parent family.
- The ratio-plane/pure-gamma discrimination statements rely on established results of **Rada**. Clearly distinguish inherited theorems and consequences from the paper's new enumerative collision thresholds, examples, and other specific contributions.
- At nonzero **algebraic** gamma, pure-gamma points distinguish imbalance histograms; do **not** claim that every individual degree-ratio index separates all different histograms. Every degree-ratio index is limited by the histogram; some can collide earlier.
- The exhaustive collision thresholds are order **13** for general trees and **16** for chemical trees. The corresponding positive information-recovery ranges end at orders **12** and **15**, respectively. Retain the qualification that minimality relies on exhaustive enumeration.
- The bound on order exchanges along gamma is at most **five** for the stated chemical graph class; do not assert sharpness if it remains unresolved.
- Parent-distinction preservation has restrictions on the parent exponents and gamma; do not drop the rational/algebraic hypotheses.
- Extremal pure-gamma tree results and their relationship to previous criteria by **Cruz and Rada** require correct attribution.
- The empirical result is **no demonstrated predictive gain** from freeing gamma under the stated comparisons, not proof that gamma can never help.
- The apparent vaporisation-enthalpy gain under the narrow search was affected by a truncated parent parameter box; the wide-box reanalysis was exploratory. Do not present it as independently preregistered.
- A seed-count rule primarily tracked optimiser variation; it is not a molecule-level significance test. Preserve bootstrap uncertainty and the distinction between in-sample, nested out-of-sample, and post-selection quantities.
- Regression on degree-pair counts performed better than individual indices **in reported point estimates under the tested conditions**. Do not turn this into an unqualified universal conclusion.
- Lean checks only the specifically formalised statements, not the full paper. Preserve the explicit boundary between formal, computational, and unverified arguments.

## Concrete editorial targets

### A. Abstract (near main.tex lines 194–216 on the starting branch)

Create a compact abstract with this logical order:
1. Scientific problem: what information a degree-imbalance-based index can distinguish.
2. Exact relationship to the established parent index and earlier theory, described briefly.
3. Main **new** outcome: the explicit collision thresholds and any essential derived bound, each with its qualification.
4. One restrained sentence on the pre-registered predictive tests and the exploratory wide-box diagnostic.

Avoid stacking every theorem and auxiliary result into one paragraph. Do not imply that the Rada theory is newly proved here. Keep the mathematically essential parameter restrictions. Avoid artificial buzzwords and over-claiming.

### B. Introduction (approximately lines 221–345)

**Current problem:** The opening starts with a broad textbook-style survey, catalogs many indices, and introduces the specific research problem relatively late. The six-item contribution list also puts routine facts, established results, proofs, numerical enumeration, and QSPR on roughly equal footing.

**Edit:** Begin with the discrimination/resolution-limit problem in chemical graphs, then introduce the parent and the Loyola extension, then situate the precise question in the literature. Compress the catalog of classic indices without deleting necessary attributions or technical context. Prefer grouped citations linked to clear claims rather than sequential summaries of every neighboring index.

Distinguish explicitly:
- known foundation from Rada and related work;
- what is genuinely new in the present paper;
- what is computer-assisted or numerical;
- what is only a diagnostic application.

Reduce the contributions passage to a short, logically ordered narrative or a compact list if it genuinely improves clarity. Preserve all reference labels and citations used elsewhere.

### C. Mathematical sections (approximately lines 347–1548)

Keep proofs and mathematical assertions stable. Edit *only* surrounding exposition that is genuinely repetitive, overly ceremonious, or detached from the mathematical step it introduces.

- Prefer “Here we determine ...” or a direct theorem lead-in over formulaic stage-setting.
- Explain why each result matters before or after the formal statement **without adding claims**.
- Distinguish limitations of the family, of the ratio-plane subfamily, and of a particular index.
- Keep all literature-credit statements and precise proof limitations.
- Do not shorten a proof merely to save pages. Leave all equations and proof logic untouched.
- Never convert computer-assisted enumeration into a claimed purely analytical proof.

### D. QSPR diagnostics (approximately lines 1549–1829)

**Current problem:** Dense paragraphs carry design details, seed counts, effect estimates, caveats, and post hoc analysis in uninterrupted succession. The same methodological warnings recur in multiple sections.

**Edit:** Make each subsection follow **question → design → observed result → interpretation → necessary caveat**. Break overlong prose into shorter paragraphs where helpful. Keep exact numerical outcomes, cohorts, confidence/uncertainty statements, selection details, registration status, and restrictions.

Keep these contrasts unmistakable:
- octane descriptive correlations versus predictive tests;
- narrow parent search box versus wide-box reanalysis;
- pre-registered result versus later exploratory sensitivity analysis;
- optimiser-seed counts versus molecule-bootstrap uncertainty;
- single-index comparisons versus ridge and Wiener reference models;
- point-estimate improvement versus uncertainty-supported inference.

An editor must be able to reconstruct which analyses were decided before data inspection and which were decided afterwards. Do not move essential caveats into an obscure supplement merely to shorten the paper.

### E. Discussion and limitations (approximately lines 1830–1890)

**Current problem:** This reads partly like an internal auditing checklist.

**Edit:** Start with the substantive interpretation: what the mathematics establishes, where the structural ceiling occurs, and what the empirical results do or do not support. Organise limitations around **theoretical scope, enumeration scope, data quality, and inferential scope** rather than generic review language.

Retain the protocol-deviation table and every substantive admission. It may be placed and introduced more naturally, but do not suppress it or soften negative findings.

### F. Conclusion (approximately lines 1892–1916)

**Current problem:** Repeats the abstract and lists many theorems and qualifications sequentially.

**Edit:** Conclude in two or three concise paragraphs:
1. New structural contribution, distinguished from prior theoretical tools.
2. Practical conclusion from the limited QSPR experiments, including uncertainty and the negative finding.
3. One focused direction for future work, rather than a long catalogue.

Do not restate every result, table, or proof. The reader should leave with a clear statement of the paper's actual advance.

### G. Data availability and verification disclosures (approximately lines 1918–1936)

Maintain the exact distinction among available code/data, privately retrieved NIST source pages, downloaded data checks, and the limited scope of Lean verification. Improve readability only. Do not imply all original NIST material is redistributed or all arguments are machine-checked.

## Style requirements

- Write like an experienced mathematical author: **specific nouns and verbs, measured claims, concise explanations, and correctly scoped assertions**.
- Remove generic phrases that do not convey information, repetitive “we also show” sequences, inflated novelty framing, and stock transitions.
- Vary sentence construction *for clarity*, not cosmetic randomness. Some long mathematical sentences are necessary.
- Prefer concrete subjects (“The enumeration shows ...”; “On the tested decanes ...”) over vague “It is worth noting ...”.
- Consolidate duplicated background; do not repeat the same limitation in full in abstract, introduction, results, discussion, and conclusion.
- Preserve discipline-specific terminology when it is the clearest formulation. Do not replace technical language with casual language.
- Do **not** add marketing language, claims of “unprecedented,” “groundbreaking,” “robust,” or “comprehensive” unless the evidence supports it.
- Do not substitute a generic AI rewrite for the authors' argument. Preserve the paper's intellectual voice and careful negative conclusions.
- Do not introduce new formulas, new mathematical sections, extra results, or speculative physical interpretations.
- There is **no arbitrary page cap**. Prioritise accuracy over word-count reduction. A modest reduction in repetitive prose is desirable, but never at the cost of mathematical specificity or disclosure.

## Execution and verification workflow

1. **Inventory and baseline:** Record the starting branch, exact commit SHA, manuscript path(s), and Git working-tree status. Identify duplicate rendered or Overleaf sources; determine whether they are generated copies before editing. Do not independently edit multiple divergent copies.
2. **Editorial map:** Identify paragraphs that are generic, repetitive, excessively dense, or audit-like. Record the original location and the precise editorial reason for changing each.
3. **New worktree/branch:** If other verification is running, use a separate worktree. Make only the minimum main.tex prose changes needed to improve the six target areas.
4. **Diff review:** Inspect a word-level diff. Explicitly check that no theorems, hypotheses, constants, values, mathematical equations, algorithms, labels, citation keys, table cells, proofs, bibliography records, author names, affiliations, or outcome claims changed unintentionally.
5. **Build:** If a LaTeX build environment is available, compile and check for errors, undefined references, missing figures, or layout regressions. State honestly if it is unavailable. Do not install large new stacks just for an editorial pass.
6. **Targeted textual verification:** Run any cheap existing prose/figure/reference consistency checks that are relevant. Do not trigger a multi-hour numerical/full verification suite; the science is unchanged. If scientific files must change unexpectedly, STOP and flag them.
7. **Editorial deliverables:** Save:
   - audit/EDITORIAL_STYLE_CHANGELOG_2026-10-22.md — before/after excerpts, section and line references, reasons for changes, and any unresolved author decisions;
   - audit/EDITORIAL_PRESERVATION_CHECK_2026-10-22.md — starting commit, changed-file list, exact checks run, PASS/FAIL/NOT RUN results, and confirmation of which mathematics/results/citations were untouched.
8. **Git hygiene:** Commit locally to the new branch with a descriptive message. Do **not** merge to main or push manuscript edits until the authors have reviewed the word diff and verification record. Do not force-push at any stage.

## Definition of done

The edited manuscript should:
- open with the actual structural-discrimination question rather than a generic survey;
- state the original contribution without taking credit for Rada/Cruz–Rada results;
- retain the correct order-13/order-16 collision boundary and all hypotheses;
- read as a coherent mathematical research article rather than an assembled audit;
- preserve honest negative QSPR results, post hoc labels, uncertainty, and the preregistration record;
- contain no invented references, silent changes to science, or LaTeX breakage;
- have a readable, line-specific changelog and explicit verification status;
- leave running jobs, frozen computations, and repository history intact.

## Required final response

Report:
1. The exact base commit and editorial branch.
2. Sections edited and a concise summary of substantive prose improvements.
3. Specific examples of before/after wording.
4. Whether any scientific ambiguities require the authors' decision.
5. Compilation and consistency checks, distinguishing **PASS**, **FAIL**, and **NOT RUN**.
6. Changed files, local commit hash, and confirmation that no push/merge/force action occurred.
7. A short editor-facing assessment of remaining readability problems.

**Important:** This is an editorial pass for correctness, clarity, attribution, and publication readiness. It must never be framed as proof of human authorship or as a promise to evade automated AI-writing detectors.
