# 16. Overlap between the LOYOLA manuscript and the companion manuscript

Date: 2026-10-20. Read-only check. Nothing was edited, committed, pushed or opened in either repository.

- **Manuscript A** (for MATCH): "The Loyola Index Family and the Resolution Limit of Degree Imbalance", A. Natarajan, G. Shiwakoti, M. Arockiaraj. Sources: `wt-fig/main.tex`, `wt-fig/supplement.tex` (worktree of `Singati2/LOYOLA-PAPER`, HEAD `e19f506`).
- **Manuscript B** (companion): "Ten Edge-Degree Counts Are All a Bond-Incident-Degree Index Can See: An Exact Redundancy Certificate and What It Leaves for New Molecular Descriptors", G. Shiwakoti, A. Natarajan, M. Arockiaraj. Source: `Singati2/topological-index-orthogonality`, `docs/paper2_orthogonality_screening.tex` ("Draft v2.3", last commit `dfdfecc`, 2026-10-08) and `docs/supplement_body.tex`, `docs/tables_v2/*.tex`. Downloaded copies are in `match_drafts/companion/` (`docs/`, `hist/` for historical versions, `loyola/` for the public LOYOLA files).

Title wording differs across B's files: the README says "...a Degree-Based Topological Index Can See" (v2.1), the `.tex` and the committed PDF say "...a Bond-Incident-Degree Index Can See", and `CITATION.cff` uses a third title. The committed PDF is v2.1 (dated 7 Oct 2026, 22 pp.). The `.tex` is v2.3.

## 1. Is the "Wuzi" first paper an earlier version of A?

Yes. The repository description still reads "Two-paper package: Wuzi parametric topological-index family (graph theory) + reproducible orthogonality-screening pipeline". That describes the state before 2026-10-05. The history shows:

- 2026-05-19 to 2026-06-01: "Paper 1" (Wuzi) lived in this repo as `docs/paper1_wuzi.tex` and `docs/paper1_wuzi_match.tex` (MATCH template, internal versions "MATCH v2" to "MATCH v10"; title at `06a985b`: "The Wuzi Index Family and the Ten-Dimensional Ceiling of Molecular BID Descriptors"). Commit `65c5651` (2026-05-20) split the original single project into Paper 1 and Paper 2 "per advisor direction, no work duplicated".
- 2026-10-03: `Singati2/LOYOLA-PAPER` was created. Wuzi was renamed Loyola (`LO`). Manuscript A still defines `\Wuzi` as a macro for `LO(G;α,β,γ)` and uses the label `def:wuzi`.
- 2026-10-05, commit `a663abd`: "Remove Paper 1 material ... Paper 1 (Loyola index family) now lives in Singati2/LOYOLA-PAPER". The current tree holds Paper 2 only, as the README "History" section says. The old Paper 1 files can still be reached through the public commit history. The tag `v1.4-paper2-orthogonality` named in that commit message is not in the current tag list (only `v2.0-paper2` to `v2.3-paper2`).

Text check (8-word shingles, LaTeX stripped, inline math removed). A against the June Paper 1 (`06a985b`) shares 156 shingles. They cover 8.0% of the old Paper 1's words and 2.0% of A's. The longest shared runs are 21 to 25 words, in the bound statements (the "bracket bound" and the bound through a BID index with positive edge contribution). A is a heavily rewritten descendant of that draft and the same project. The old draft was never a journal publication.

## 2. Submission and posting status (what is visible)

| Item | Evidence | Status |
|---|---|---|
| B on arXiv / ChemRxiv / journal | README: "(v2.1, in preparation)"; `.tex`: "Draft v2.3"; no arXiv, ChemRxiv or DOI in the repo. arXiv API (title, "Loyola index", "Wuzi", author queries) and Crossref title queries: no hit | None found |
| B, June 2026 "journal submission files" | Commit `e4a96f2` (2026-06-01) "Add journal submission files, SI, ..." added `paper2_molinf_main.tex` / `paper2_molinf_wiley.tex` (Molecular Informatics / Wiley formats, title "Orthogonality Screening of Topological Indices for QSPR Modeling: A Structural and Empirical Redundancy Analysis", "Draft of \today", four authors incl. P. Chalise). The June README lists Molecular Informatics, J. Cheminformatics and JCIM as targets and says "Paper 2 submission gated on Paper 1 arXiv ID: scheduled". No later commit records an actual submission, a manuscript number or a decision. The files were deleted in `a663abd` | Prepared, submission not recorded. **AUTHOR CONFIRMATION NEEDED**: was the v1 (Molecular Informatics) version ever submitted, and if so, is it withdrawn or rejected? |
| Paper 1 (Wuzi) in 2026 | Commit messages "Paper 1 MATCH v2 ... v10" (2026-05-26/27) are internal revision rounds (advisor/co-author items). No submission record | Not submitted as far as visible |
| A | LOYOLA commits `3af7f67` ("final adversarial review before submission"), `410e579` ("clean submission package (not submitted)"). Open PRs #3 to #5 are internal review branches | Not submitted |
| Neither on arXiv | as above | Neither posted |

Only the public GitHub repositories are visible for either manuscript. Both carry full drafts. A's compiled PDF is in LOYOLA-PAPER. B's v2.1 PDF is in `docs/`.

## 3. Cross-citation

- **A does not cite B.** v40.5 (`64355b8`, 2026-10-05) added a paragraph and a bibitem ("Ten edge-degree counts are all a degree-based topological index can see ... in preparation (2026)") saying the companion turns the degree-pair observation into a span certificate and that "the present paper is the case study of that statement". v40.10 (`8ecf31f`, "no citation of unpublished work") removed both. A now cites only its own repository (`LoyolaRepo`).
- **B does not cite A formally.** No bibitem. Its introduction says: "One of the parametric families screened below, the three-parameter Loyola family ..., is studied mathematically in separate work by a subset of the present authors." This is inaccurate: the author sets are identical (order differs). B's README links to `Singati2/LOYOLA-PAPER` as "the companion mathematical paper". B commit `cbe8b0b` records "no citation of unpublished work, matching LOYOLA v40.10".
- Both repositories therefore point at each other publicly (B's README, A's commit history), but neither manuscript cites the other.

## 4. Overlap list and classification

| # | Overlap | In A | In B | Class |
|---|---|---|---|---|
| 1 | **The Loyola family itself.** B defines `LO(G;α,β,γ)=Σ(d_ud_v)^α(d_u+d_v)^β exp(γ\|d_u−d_v\|/(d_u+d_v))`, notes that it reduces to Gutman–Milovanović at γ=0, evaluates a 100-point grid on ESOL, FreeSolv, Lipophilicity and BBBP (400 evaluations), and finds every point exactly in the span of the 18-index baseline (relative residual ≤ 2×10⁻¹²). Partial correlation is exactly 0. The pairwise screen passes one point (FreeSolv, (−1,−1,1), max\|r\|=0.943). B also reports an earlier draft's erroneous partial correlations 0.028/0.036/0.009 for the Loyola grid. | Definition 2.1 (same formula, same name, same notation); main subject | Sections 1, 4 (census), 5 (pitfall), Table "cert"; scripts `02_wuzi_grid_search.py`, `src/wuzi_index.py`, `results/*/wuzi_grid.csv` | **MUST DISCLOSE.** The same authors evaluate the index family that A introduces in a second manuscript, with a negative verdict on its added linear information. An editor or referee who finds B (it is public and names the family) would see an undisclosed related manuscript. |
| 2 | **Every BID index is a linear functional of the ten edge-degree-pair counts on Δ≤4; the family lies in a fixed 10-dimensional space.** | Introduction l. 287–289 and Section 3 remark l. 984, credited to Rada 2026 (MATCH 96) only. A adds its own affine-dimension facts (≤7 at fixed order, 8 across orders) | Central premise; credited to Gutman 2013, Rada–Cruz 2014, Cruz–Espinal–Rada 2024, Rada 2026. B's own contribution is the statistical rank certificate built on it (Prop. "cert", Cor. "datafree") | **SHOULD CITE.** The fact is classical and both papers credit third parties, so this is not duplicate publication. But it is the premise of B's whole paper, and the earlier A draft described A as "the case study of that statement". Cite B where A uses it, or disclose it in the cover letter at minimum. |
| 3 | **"Ceiling"/"floor" language.** A: degree-pair ceiling (Prop. "collision": equal m_ij ⇒ equal value for every vertex-degree-based index); two octane collision pairs; 25.5% degeneracy floor on 106 order-10 trees. B: "information ceiling" from hydrogen-suppressed graph collisions (different molecules, same graph) and a "graph-oracle floor" on MoleculeNet | Section 3.4–3.5, Table "collisions", Fig. degeneracy | Section "ceiling", Fig. 2 | **INCIDENTAL.** The words are shared but the results are different. A's collisions are different graphs with equal degree-pair counts. B's are identical graphs from different molecules. No shared result, number or data. |
| 4 | **Conclusion about predictive value.** A: "the family is not proposed as a better predictor"; freeing γ gives no demonstrated gain; ridge regression on the degree-pair counts leads every single index on boiling points. B: no BID index (Loyola included) adds linear information beyond the baseline; the counts alone do as well in tree ensembles | Abstract, contributions (vi), Section 6 | Abstract, Sections 4, 8 | **SHOULD CITE** (it comes with #1 and #2). The conclusions point the same way on disjoint data, so citing B strengthens A. |
| 5 | **Datasets.** A: 18 octanes (5 properties), 35 nonanes, 101 C6–C10 boiling points, decanes, calorimetric ΔH_vap, all trees of orders 2–17. B: ESOL, FreeSolv, Lipophilicity, BBBP plus 13 MoleculeNet sets (318,648 molecules). B mentions octanes only in prose about other authors' practice | — | — | **INCIDENTAL.** The datasets are disjoint. No MoleculeNet data in A, no octane, nonane or boiling-point data in B. |
| 6 | **Identical numbers** | none found | none found | **INCIDENTAL.** No shared numerical result. B's grid ({−1,−½,0,½,1}²×{0,½,1,2}) is not used in A. |
| 7 | **Figures and tables** | `fig_lo_degeneracy_order10_trees_v2`, `fig_lo_prediction_correlation_heatmap_v3`; tables of collisions, degeneracy, octane correlations, boiling-point tests | `fig1_certificate_and_screen`, `fig2_information_ceiling`; tables bench, census, cert, chem, data, general, nonbid, phi | **INCIDENTAL.** No shared figure or table. In B's repo history (removed 2026-10-05) were earlier Paper 1 figures, `fig6_degeneracy_bars` and `fig4_octane_heatmap`, ancestors of A's degeneracy and octane figures. They are not in B's current manuscript. |
| 8 | **Code lineage.** B's repo still ships `src/wuzi_index.py`, `tests/test_wuzi_identities.py` and `02_wuzi_grid_search.py`, the original Wuzi implementation | own implementation in LOYOLA-PAPER | yes | **INCIDENTAL** (software; no disclosure needed beyond #1) |
| 9 | **Earlier public drafts of A** (Paper 1 Wuzi, May–June 2026) in B's commit history | — | history only | **INCIDENTAL** for duplicate publication: they are unpublished drafts on GitHub, not a journal or preprint server. One clause in the cover letter covers them (see wording). |
| 10 | **Shared bibliography** (Rada 2026, Gutman–Milovanović 2020, Gutman 2021 Sombor, Vukičević–Furtula GA, Nyauli–Buragohain, Movahedi et al., Barman–Das, Konstantinova, ...) | — | — | **INCIDENTAL** |
| 11 | **Author metadata.** A: Natarajan at Oregon State University. B (`.tex`, `CITATION.cff`): Natarajan at Loyola College, Chennai. Author order differs (A: Natarajan, Shiwakoti, Arockiaraj; B: Shiwakoti, Natarajan, Arockiaraj). B says "a subset of the present authors", but the sets are identical | — | — | **INCIDENTAL** for MATCH. **AUTHOR DECISION** to make B consistent before it goes anywhere. |

## 5. Verbatim and near-verbatim text overlap

Method: both LaTeX sources were stripped (preamble, comments, `\cite`/`\ref`/`\label`/`\url`, inline and display math, environment names, bibliography). Word shingles were then compared, and the longest common word runs were found with `difflib`. Script: `scratchpad/overlap_scripts/ngram.py`. A = `main.tex`+`supplement.tex` (17,592 words). B = paper `.tex`+`supplement_body.tex`+`tables_v2` (7,908 words).

| Shingle length | Shared shingles | Jaccard | A covered | B covered |
|---|---|---|---|---|
| 5 words | 12 | 0.05% | 0.41% | 0.67% |
| 8 words | 0 | 0 | 0 | 0 |
| 12 words | 0 | 0 | 0 | 0 |

No common run reaches 8 words. The 12 shared 5-grams are stock phrases ("be the number of edges", "carries no information beyond the", "let ... be a simple connected", "of maximum degree at most", "the Gutman–Milovanović family", "on graphs without isolated vertices").

Cross-check on the compiled PDFs (A paper+supplement 25,735 words vs B v2.1 PDF 12,458 words, references included): 8-gram coverage is 1.25% of A and 2.0% of B. All the longest shared runs (8 to 25 words) are bibliography entries (Konstantinova; Vukičević–Furtula GA; Barman–Das hyperbolic Sombor; Nyauli; Klavžar M-polynomial) and the FAU affiliation line.

For comparison, B against its own June v1 shows 0.3% 8-gram coverage (a full rewrite). A against the June Wuzi Paper 1 shows 2.0% / 8.0% (see §1).

**Verdict: no text recycling between A and B.**

## 6. Recommendation

The overlap is in topic and object, not in text or results: B screens the family that A introduces, and both rest on the same classical span fact. Under MATCH's rules (no simultaneous consideration, cite one's own work), the risk is non-disclosure. Duplication is not the issue. Disclose B in the cover letter and confirm its status. Citing B in A is the stronger option but is an author decision, because A's authors deliberately removed the citation in v40.10.

**Proposed cover-letter paragraph** (edit the bracketed items after confirming facts):

> Related work by the same authors. The three authors are also preparing a separate manuscript, "Ten Edge-Degree Counts Are All a Bond-Incident-Degree Index Can See: An Exact Redundancy Certificate and What It Leaves for New Molecular Descriptors" (G. Shiwakoti, A. Natarajan, M. Arockiaraj). It is [not submitted to any journal and not posted on a preprint server]; a draft and its code are public at https://github.com/Singati2/topological-index-orthogonality. That manuscript is a chemoinformatics study. It turns the known fact that every bond-incident-degree index is a linear combination of the edge-degree-pair counts (Rada, MATCH 96 (2026)) into a statistical rank test on MoleculeNet datasets, and it includes the Loyola family among the indices it screens. It contains none of the theorems, enumerations, closed forms, bounds or boiling-point and octane analyses of the present submission. The two manuscripts share no text, data, figures or tables. Earlier drafts of the present paper, under the working name "Wuzi index", are visible in that repository's public commit history and in https://github.com/Singati2/LOYOLA-PAPER; they have not been published or submitted elsewhere. [If the companion manuscript is submitted while this one is under review, we will inform the editor and cite it.]

Facts to confirm before sending: (a) B, including the June 2026 Molecular Informatics–format v1, has never been submitted, or else its current status; (b) B will not be submitted to MATCH, or will be disclosed if it is; (c) the bracketed clause.

**Optional citation sentence for A** (AUTHOR DECISION; for Section 3 after "of which every vertex-degree-based index is a functional~\cite{Rada2026LinearVDB}", or for the Introduction after the "ten-dimensional space" sentence):

> In a separate study~\cite{ShiwakotiNatarajanArockiaraj2026Span} we use this fact as a rank test on molecular data sets, under which every bond-incident-degree index, the Loyola family included, is an exact linear combination of a baseline of classical indices.

> `\bibitem{ShiwakotiNatarajanArockiaraj2026Span} G. Shiwakoti, A. Natarajan, M. Arockiaraj, Ten edge-degree counts are all a bond-incident-degree index can see: an exact redundancy certificate and what it leaves for new molecular descriptors, manuscript in preparation (2026); \url{https://github.com/Singati2/topological-index-orthogonality}.`

MATCH-style reference lists accept "in preparation" or "manuscript" items, but some editors dislike them. If the authors keep the v40.10 policy (no citation of unpublished work), the cover-letter paragraph alone discharges the disclosure duty.

**Housekeeping for the companion (AUTHOR DECISION, not done):** update the stale repository description ("Two-paper package: Wuzi ..."); fix "a subset of the present authors"; reconcile Natarajan's affiliation and the three title variants; regenerate the v2.1 PDF to v2.3.
