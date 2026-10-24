# Claude execution prompt — Adversarial independent referee audit of LOYOLA-PAPER and MATCH fit

**Date:** 2026-10-24  
**Repository:** https://github.com/Singati2/LOYOLA-PAPER  
**Current review branch:** `review/match-final-four-fixes-2026-10-23`  
**Last reviewed source commit:** `e3fc8810c066420354c96eb8c38a0b9190dfa663`  
**Notebooks pinned to source:** `e90b5bfcb1a46937cb4f20a6b3420007b69caad1`  
**Documentation branch tip before this prompt:** `31726f36a00a4a27769c8fcd7cd9d2ac9b0c4ee8`  
**Target:** *MATCH Communications in Mathematical and in Computer Chemistry*  

## Your mission: try to falsify the paper, not to confirm your earlier audit

The authors do **not** consider this paper scientifically cleared. Multiple prior "ALL PASS" reports were too readily interpreted as submission-readiness. **Perform a genuine, adversarial, independent mathematical, computational, statistical, bibliographic, figure/table, data-provenance and journal-fit audit.** Detect substantive mistakes and misleading inferences, propose fixes backed by evidence, and execute only the corrections that do not change frozen claims or data without explicit author review.

The ChatGPT independent referee report dated 2026-10-24 made a **partial** independent check of `e3fc881`. Its positive results are useful cross-check targets, **not trusted evidence or a substitute for your own computations**. That review had not run the repository's full Lean/Colab pipelines, all nested statistics, checked every original source, or visually inspected the actual distributed PDFs. Do not claim that an unattached external audit ZIP exists in your local worktree.

### Rules for evidence and language

Classify every meaningful claim as:
- **INDEPENDENTLY VERIFIED** — own re-derivation or independently coded experiment, exact input/commit, command/log and clear assumptions.
- **REPRODUCED FROM COMMITTED DATA** — agreement with the repository's saved data, *not* independent verification of source measurements.
- **REVIEWED / MATHEMATICALLY ARGUED** — primary-source proof audited step by step; state limits.
- **NOT VERIFIED** — incomplete, unavailable, too costly, or results inherited from older commits.
- **INCORRECT / COUNTEREXAMPLE FOUND** — show the exact contradiction and smallest reproducer.
- **SUBMISSION BLOCKER** — unresolved ethical, legal, data, author, journal, or reproducibility prerequisite.

Never label a theorem "proved" because 10,000 examples passed. Never label a bibliography "verified" just because its `\cite` keys resolve. Never call the manuscript "MATCH-ready" just because its template resembles a published paper. Do **not** accept the authors' or your own verification tools as independent arbiters.

## 0. Preservation and isolation — before doing anything

1. Confirm the exact Git commit graph, branch, ancestry, clean/dirty status, all active worktrees, and any ongoing experimental processes. Confirm `e3fc881` is the tested science source and `e90b5bf` contains the notebook pins. If remote/local refs differ, record it before proceeding.
2. Create a **new local worktree/branch** for this audit, e.g. `review/match-adversarial-referee-2026-10-24`. Do not edit `main`, old branches, any running task, historical full manuscript, or `wt-mainrevert`.
3. Use scratch-only directories for independent scripts, files and environments; ideally a second fresh checkout. Identify Python, RDKit, NumPy, NetworkX, SciPy, mpmath, TeX, Lean and other versions. Pin all dependencies, seeds and input hashes. Estimate compute requirements before costly jobs.
4. Do not rerun expensive processes unnecessarily or interrupt existing research jobs. If resources are insufficient, run bounded falsification tests first and explicitly mark the rest NOT RUN. Prefer new methods over copying any repository "independent" script.
5. No force pushes, merges, releases, tag creation, Zenodo publication, source-data edits, Git history rewrite, citation removal, manuscript submission or public upload of restricted material without author authorization. This task is an AUDIT. The new branch stays local pending review.
6. Preserve all existing mathematics, negative QSPR outcomes, candidate streams, tables, raw data, frozen preregistrations, existing manifests, historical commit SHAs and manuscript versions. If an actual error demands a substantive change, create a minimal proposed patch and a precise impact analysis for author signoff; don't silently change certified results.
7. No fabricated numerical output, DOI, paper availability, mathematical novelty, journal instruction, source rights, or passing test. Store logs and checksums, not merely "PASS" summaries.

## 1. Mathematics: independently attack every substantive claim

Build a theorem/lemma/corollary/proposition/remark ledger for both `main.tex` and `supplement.tex`. For **every** numbered or advertised result, give: exact statement/hypotheses, upstream dependencies, published predecessor (if any), proof steps checked, independent test, possible counterexample, novelty status, and VERIFIED / NOT VERIFIED / WRONG verdict.

### A. Ratio-plane theorem and degree-ratio information loss
- Confirm algebraically and by a fresh implementation that on `β = −2α`, the LO family factors through the complete multiset of `q = |d_u−d_v|/(d_u+d_v)`.
- Carefully distinguish: equal degree-pair count vectors; equal `q`-histograms; equal values for *one* fixed index; equality for all parameter points; graph isomorphism. Test each implication and non-implication with explicit graph pairs.
- Independently check the pure-`γ` statement for **nonzero algebraic γ**, Rada's fixed-order hypothesis, the manuscript's argument outside fixed order, the exceptional real γ set, and the claimed almost-everywhere statements. Check that the old `K_4` vs `K_{1,3}` **equal-order** example is no longer incorrectly used as evidence about different orders.
- Independently verify Rada (2019) Theorem 3.4, Corollary 3.5, Proposition 2.5 and the exact equivalence of the GA-weight partition and the `q` partition, using `GA_{ij}=sqrt(1-q_{ij}²)`; distinguish **ordinary GA** from **exponential GA**. Identify what is known, directly adapted, and genuinely new.

### B. First collision orders 13 and 16 — prove the computation's scope
- Enumerate **all nonisomorphic trees at least through order 17** and all chemical trees (`Δ ≤ 4`) with an independent implementation of edge-degree-pair profiles and *exact rational* q-histograms. Compare total trees, distinct profile vectors, histogram vectors and individual collisions with the paper's Table 2, certificates and textual assertions.
- The 2026-10-24 partial independent review used `networkx.nonisomorphic_trees`, which is **not independent** if the authors also rely on that generator. Where possible cross-check completeness with a second generator (e.g. nauty/geng or a separately implemented canonical-tree enumerator), OEIS unlabeled-tree totals, and a graph-isomorphism check. Do not claim independent enumeration if both methods share the same generator.
- Earlier partial check targets: `n=13` unrestricted **570 profiles / 566 histograms**; `n=16` unrestricted **4069 / 3996**; chemical `n=16` **810 / 809**; `n=10` unrestricted **79 / 79**, with **106** trees. These are cross-check numbers, not axioms.
- Construct and save actual adjacency lists/SMILES (if applicable) for the order-13 and order-16 witness pairs. Verify graphical realization, vertex counts, maximum degree, distinct profiles, equal q-histograms, and claimed pendant-leaf conditions. Independently check the pendant-path propagation lemma, including exactly how profile vectors change, degree caps, and extension to **every greater order**.
- Distinguish the first *class-wide loss* from earlier accidental ties of **individual** GA, SDD, ISDD or other index values. Check exact algebraic ties; do not use 11-digit float grouping as proof of exact equality. Clarify "4069 degree-pair profiles" versus numbers of trees.

### C. All other mathematics
- Check affine independence of `(1, ln(ij), ln(i+j), q_ij)`: exact proof for `Δ ≥ 3`, rank drops at `Δ = 1,2`, all quantifiers, scale-identifiability and isolated-vertex/domain edge cases. Numerical rank alone is inadequate.
- Audit parent-point survival, algebraicity/rationality, Lindemann–Weierstrass/Besicovitch arguments, countable exceptional sets, equality cases and negative exponent cases. Try to falsify every bound with small connected/nonconnected graphs and adversarial parameters.
- Audit crossing Proposition 4: use generalized Descartes/Laguerre's correct hypotheses, sign changes, **zeros counted with multiplicity** versus true sign-changing crossings (tangencies), zero function exception, and `Δ≤4` imbalance count. Independently reproduce the claimed five roots approximately **−17.170899, −11.960559, −2.026012, 2.734463, 31.133294** for the specified **Δ=6**, `α=-1,β=0` witness; confirm those profiles are realized by actual trees. Do not conflate this with five attainable crossings for `Δ≤4` (open).
- Audit log-convexity, extremal path/star, closed forms, termwise bounds, Cauchy–Schwarz, `m,δ,Δ` hypotheses, `K_2`, regular graphs, empty-edge cases, chemical-tree definitions and the supplement's identifiability/rank results. Look for missing hypotheses or stronger equality/uniqueness claims than proved.
- Check Lean scopes **statement by statement** against the natural-language theorem; only cite a specific Lean declaration if it actually formalizes that assertion. If possible run a fresh Lean build; if not, mark NOT RUN and distinguish historical passes.

## 2. Every table, figure, example and numeral — no cherry-picking

Create an exhaustive inventory with IDs, pages, source path, regeneration command, data hash, rounding/units, caption, citation, denominator, output file, independent result and verdict.

**Main:** Tables **1–5**, **Figure 1**, every numerical remark and main-text example.  
**Supplement:** Tables **S1–S8**, Figure **S1**, numerical examples, footnotes, reference numbers and all associated panel/caption text.

Requirements:
- Recompute the **18 octane structures** from supplied SMILES with a fresh RDKit parser; independently obtain degree-pair vectors, 16 distinct vectors, two collision pairs, Table 1 values and the precise information-theoretic SSE floor `2.925 °C²` / RMSE `0.4031128874 °C` **under the stated in-sample fixed-structure formulation**. Do not generalize this floor to unrelated cross-validation procedures.
- Recompute **all 60 Table 4 signed Pearson correlations** from the committed 18×5 octane benchmark, exact Loyola index formula, and appropriate statistical definitions. Independently check displayed 3-decimal rounding and highlighting, signed near-zero ISI term, tied ranks and uncertainties. The earlier partial review matched all 60 *against the committed CSV*, not original measurements.
- Recompute Figure 1 on **all 106 trees at order 10**, every compared index, distinct-value counts, legend, labels, decimal percentages and reference floor. Cross-check exact radicals vs high-precision grouping for equality. Earlier independent count targets: `18,35,66,56,79,77,70,67,79,79,79,79`. Verify the actual image, grayscale legibility, Type 3/Type 42 fonts, physical sizing, placement and caption.
- Recompute Table 2 order thresholds and all footnotes, Table 3 SS/Abr calculations, and Table 5 full statistical rows from the **primary source files** rather than merely copying `*_summary.csv`.
- Independently regenerate Tables S1–S8 and Figure S1, including seed/interval provenance, nested/non-nested methods, font sizes, unit declarations, readability and float placement. Check S8 truly ends before the supplement bibliography.
- For **every** captured prose number, test its semantic anchor; prior false matches included '020' from a DOI and '5' from degree pair `(3,5)`. Re-run mutation tests against intended sentences; ensure a similar accidental match in a footnote/citation/bibliography cannot satisfy a scientific check. Don't mistake "757/0" for 757 independently grounded facts.
- Download/extract the **actual** committed main/supplement PDFs and MATCH/Overleaf ZIPs. Build fresh from source and compare checksums or meaningful rendered/text equality. **Visually inspect all pages with tables, figures, supplement bibliography and first-page metadata**. A LaTeX exit code and text equality alone are insufficient. Where a PDF is analyzed, inspect page screenshots and report page numbers.

## 3. Statistics and chemistry: independently rerun the complete inference

Do not simply re-read `bp_results_summary.csv`. Build an independent pipeline from the properly defined **raw cohort rows** and independently chosen folds while honoring the frozen registered protocol.

1. Audit each source row, units, structures, isomer naming, duplicates, missing values, group leakage and chemical interpretation for C6–C10 pooled, 34 decanes, 35 nonanes and 18 octanes. Distinguish **primary measurements**, secondary compilations, averages, post hoc corrections and questionable phase states. Determine the actual status of **57 direct AVG + 1 grouped AVG**, not by asserting the old audit.
2. Reproduce ordinary leave-one-out and **fully nested** descriptor/model/ridge-penalty search correctly. Confirm which Table 5/Table S7 columns select a feature, parameter point or penalty *inside each training fold*; validate exact `Q² = 1−PRESS/SS_total` with the **full-sample** mean denominator and negative-score behavior.
3. Independently reproduce all **50-seed** narrow- and wide-box registered/exploratory contrasts, actual candidate distributions/streams, equal or unequal search budgets, dimensionality effects, fixed-`γ` controls, classical indices, ridge on degree-pair counts, `n_C` size-adjusted models, and Wiener `W+p3`. Publish full per-fold/per-seed predictions and input/seed hashes in audit-only private scratch; preserve frozen original results.
4. Check paired statistic `median_seed(Q²_LO − Q²_GM)` versus `median(Q²_LO) − median(Q²_GM)`; these are different functionals. In the committed decane summary the former is approximately **−0.071530449** and the latter approximately **−0.10784319**. Verify both and ensure Table 5 cannot mislead readers.
5. Reproduce conditional molecule-bootstrap intervals with the **same resampling unit**. Independently assess the implications of intervals that do not re-fit or re-select. Contrast, rather than conflate, fully selection-aware retraining resamples, permuted-label controls, seed variation and prospective external validation. Do not treat 50 optimizer seeds as 50 independent molecules.
6. Recheck pooled results (`ΔQ²≈−0.00011339`, 25/50), decane (`ΔQ²≈−0.07153045`, 15/50), ridge (`0.85987064` decanes; `0.99106869` pooled), strict-source sensitivity, possible dominance by carbon number, and Wiener baseline (`0.90380672` decanes). These are **targets to challenge**, not granted truths.
7. Recheck octane property sensitivities, seven entropy provenance questions, compiled acentric factors, `2,2,3,3`-tetramethylbutane crystalline versus hypothetical-liquid/subsimation state, `10.263` versus rounded `10.26` kcal/mol, ties and uncertainty effects. Report which numerical conclusions depend materially on these inputs.
8. Verify every preregistration timestamp/source SHA, outcomes observed before protocol changes, registered versus exploratory tests, post hoc family changes, multiplicity, conditional intervals, benchmark strengths, and which effect sizes could be practically meaningful. **Negative findings do not establish equivalence or global inferiority.**
9. For every numerical disagreement specify whether it is a real bug, cohort/protocol mismatch, rounding issue, source ambiguity, or irreproducible artifact. Use paired, unit-aware uncertainty only when supportable.

## 4. Full bibliography and plagiarism / claim-support audit

The source TeX has **56 main** and **21 supplement** cited-and-defined keys, but syntax completeness is not source correctness.

- Verify **every one of the 77 entries** from a publisher, journal, DOI/Crossref, archived official PDF, or authoritative primary text: title, author order, year, volume, issue, pages/article number, DOI, bibliographic formatting, journal abbreviation and whether it actually exists as of the audit date.
- For every in-text citation, audit the *surrounding claim* against the primary source theorem, experiment, assumptions or limitation. Record exact original page/theorem/equation; do not trust reference titles, search snippets, secondary summaries or a previous "all supported" audit.
- Focus especially on Rada **2019** and **2026**, Cruz–Rada, Rada–Rodríguez–Sigarreta, Song–Huang, weak discrimination, original Gutman–Milovanović index, degree-ratio Sombor works, thermochemical primary sources, and the QSPR/baseline literature. Distinguish **ordinary vs exponential GA** and different order vs same order.
- For 2027 citations, check what is genuinely published **online as of 2026-10-24**, not merely a claimed future year/volume; distinguish "in progress", online first, formally released and inferred pages. Correct inaccuracies only after evidence.
- Verify alphabetical order **by actual author names**, not BibTeX citation keys. Check duplicate sources/cross-document inconsistencies, unsupported first/novel/optimal/stronger claims, quoted/copied language, copyright and permissions. A similarity checker result is not a substitute for source comparison.
- Produce a **complete citation-to-claim ledger** and a focused prior-art novelty matrix. A literature search that found no earlier threshold result is NOT a proof of priority.

## 5. Compare with real recent MATCH articles, not merely instructions

Consult MATCH's **official current instructions** at https://match.pmf.kg.ac.rs/prepare.html and its **actual 2026–2027 volumes** and primary PDFs. Include the status of each volume at the time of review, including any in-progress online 2027 volume/issue.

At minimum examine representative comparable papers:
- Juan Rada, *A Finite-Dimensional Linear Framework for Vertex-Degree-Based Topological Indices* — MATCH Vol. 96 (2026).
- Nyauli–Buragohain, degree-ratio Sombor paper — MATCH Vol. 97 (2027), if already available online.
- The Gutman/Redžepović/Buragohain/Nyauli degree-ratio comparison — MATCH Vol. 97 (2027), if accessible.
- A recent article on topological-index discrimination / geometric construction in MATCH Vol. 98 (2027), **only if actually available**.
- A substantial computation-and-proof paper from a recent volume, as a contrast in reproducibility and methods reporting.

For each compare **primary mathematical novelty**, precise theorems/counterexamples, chemical motivation/application, assumptions, proof length, numerical rigor, source availability, figure/caption discipline, limitations, citation conventions and overall focus. Calculate the actual main-paper page counts from PDFs. Avoid claiming a hard MATCH page cap without a journal source.

Inspect the real LOYOLA first page against the **official blank/template instructions**: placeholder `\vol{00}`, `\num{00}`, `\pubyear{0000}`, `\id{xxxxx}`, `\date{\today}`/Received date, copyright/licence hook, corresponding author, affiliations, metadata, fonts, grayscale figures, and typesetting. **Do not invent an assigned journal volume, DOI, received date or licence.**

Verify whether MATCH accepts a **37-page main paper plus 39-page supplement** and how it should be supplied. If official instructions are silent, prepare a short question for the editorial office; mark the answer PENDING rather than guessing.

## 6. Reproducibility and integrity: attack the full system

- Verify the exact **SOURCE_COMMIT** `e3fc881`, **NOTEBOOK_COMMIT** `e90b5bf`, docs tip and all internal references. The manuscript's bare repository citation may still open an older, mutable `main`. Treat this as a critical reviewer reproducibility gap.
- Check full notebook setup and pipeline from a fresh clone, pinned dependencies, credential redaction, immutable data hashes, correct cached-state rejection, missing/changed output detection and read/write contracts.
- Run meaningful **negative controls** that intentionally corrupt outputs, registry anchors, hashes, certificates, input structures, URLs or environment versions. The verifier must FAIL when it should. Confirm a whitelist addition cannot silently exempt production logic.
- Where practical, run `verify.py --offline`, full verifier/Lean, a fresh PDF build and real Google Colab execution (particularly `notebooks/01_data.ipynb` and `colab/12_enumeration_certificates.ipynb`) **on the same source revision**. If unable, say NOT RUN with exact blocker. Historical passes never cover a later commit automatically.
- Audit NIST WebBook redistribution: old `main` reportedly publicly exposed **262 archived HTML pages** and long verbatim source excerpts in provenance CSVs. Examine existing public exposure and applicable rights; stop further redistribution. A normal tip deletion does not erase Git history or PR refs. **Do not rewrite history, force push or publicize source pages without the owners' authorization.**
- Create a truthful plan for an immutable release/tag/DOI; never cite an uncreated release or assume one exists. Obtain all coauthor approvals before submission.

## 7. Specific output files and acceptance gates

Create the following **new local audit** reports, with evidence, small reproducible scripts, exact SHA and command logs; keep private data out of commits:
1. `audit/MATCH_ADVERSARIAL_EXECUTIVE_VERDICT_2026-10-24.md` — ranked fatal/major/minor issues; what is independently verified vs not; recommendation.
2. `audit/MATCH_EVERY_THEOREM_PROOF_MATRIX_2026-10-24.md` — proof-by-proof dependencies, counterexamples, novelty and exact scope of Lean.
3. `audit/MATCH_INDEPENDENT_ENUMERATION_CERTIFICATES_2026-10-24.md` — generator independence, profile/count tables, exact witness graphs, orders 13/16, and path propagation.
4. `audit/MATCH_ALL_TABLES_FIGURES_NUMBERS_2026-10-24.md` — complete main + supplement table/figure/numeral inventory, regenerated values, rounding, PDF screenshots/page inspection and differences.
5. `audit/MATCH_NESTED_QSPR_REANALYSIS_2026-10-24.md` — independently rerun folds/seeds, per-seed values, uncertainty, cohorts, leakage/preregistration and honest negative conclusions.
6. `audit/MATCH_ALL_77_REFERENCES_AND_CLAIMS_2026-10-24.md` — publisher proof and exact per-citation claim support; unresolved paywalled sources clearly flagged.
7. `audit/MATCH_RECENT_VOLUME_COMPARISON_2026-10-24.md` — real accepted comparable articles with full-text evidence, current author instructions and gap analysis.
8. `audit/MATCH_PROVENANCE_REPRO_RELEASE_GATE_2026-10-24.md` — NIST rights, data lineage, exact pinned commits, verifier attacks, Colab/Lean/full-run status, archival options, coauthor and supplement decisions.
9. `audit/MATCH_CHANGE_REQUESTS_BEFORE_SUBMISSION_2026-10-24.md` — minimal proposed diffs for **each** real defect with severity, affected figures/tables and precise verification test.

**Final response to authors:**
- Begin with **REFUTED / VERIFIED / UNVERIFIED** headline findings; list real mathematical or statistical mistakes before stylistic issues.
- Report actual fresh experiments and divergences, every unrun test, affected table/figure, complete reproducibility source and relevant comparison articles.
- State the most serious novel contribution *remaining after prior-art subtraction*.
- Give a defensible **MATCH suitability** analysis, separate from formatting, acceptance probability and submission readiness.
- End with a firm **SUBMIT / DO NOT SUBMIT / CANNOT ASSESS** and blockers.
- **Do not push these audit outputs or manuscript edits automatically.** Present evidence and proposed changes for authors to review first. Protect all prior branches and running processes.

**Scientific standard:** A hostile referee should be able to locate each proof, independently run each decisive experiment, trace each figure/table cell to its source, check each reference against the original publication, and reproduce the stated limits without relying on the paper's own PASS badge.
