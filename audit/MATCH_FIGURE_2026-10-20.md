# Degeneracy figure moved into the main paper (2026-10-20)

Branch `review/match-figure-2026-10-20`, from `9212441` (`review/corrections-impl-2026-10-19`). Review candidate
for the coauthors; not pushed, merged, tagged or submitted. No data set, registered result, proof, protocol or
seed was changed.

## Decision

The order-10 degeneracy bar chart (formerly Figure S2) becomes Figure 1 of the main paper, in Section 4.2
"Degeneracy across tree orders". The heatmap stays in the supplement as Figure S1.

Reasons:

* The figure shows the paper's central object, the degree-pair-profile floor: on the 106 trees of order 10 no
  vertex-degree-based index can have fewer than 25.5% degenerate trees, because the trees realise only 79
  profiles. The main text already rested its sentence on the most degenerate indices on this figure, which
  lived in the supplement; the main paper had no figure.
* The figure makes the limit of the result visible as well: the pure-gamma points share the floor with R, GA and
  AG. The caption now states that an index on the floor separates the trees with distinct profiles at this order
  and carries no information beyond the profile, so the figure cannot be read as a performance claim.
* MATCH's instructions (match.pmf.kg.ac.rs/prepare.html, read 2026-10-20) set no page limit and no figure
  rules; they require camera-ready LaTeX in the MATCH template (A5) and state no article processing charge.
  The cost is one page (43 to 44); the supplement drops from 28 to 27 pages.

## Accuracy of the figure

Independently recounted (script outside the repository, networkx enumeration): 106 trees, 79 distinct
edge-degree-pair profiles, floor 100(1 - 79/106) = 25.47%; distinct values M1 18, M2 35, HM 66, mM2 56, R 79,
chi 77, H/2 70, ISI 67, GA 79, AG 79, LO(0,0,1) 79, LO(0,0,2) 79, equal to
`lo_sensitivity_degeneracy_order10_trees.csv` and to the bars. Every index plotted is a function of the profile,
so none can exceed 79 values.

## Changes

| File | Change |
|---|---|
| `generate_loyola_v35_figures.py` | the bar chart is drawn at 4.4 x 2.9 in instead of 6.5 x 3.6 in, without a title (the caption carries it), y-axis to 92 %; printed text is 7-8 pt in the A5 text block instead of 4-5 pt. Data, colours and floor computation unchanged. The heatmap code is unchanged and its committed file is kept byte for byte |
| `figures/fig_lo_degeneracy_order10_trees_v2.pdf` | regenerated; a fresh regeneration matches it in the verifier's canonical form, and all three CSVs of the generator are identical |
| `main.tex` | Figure 1 (`fig:degeneracy`) placed in Section 4.2, referenced as `Figure~\ref{fig:degeneracy}` instead of "Supplementary Figure~S2"; caption: the former one plus the interpretation sentence; data-availability sentence no longer mentions supplementary figures (none is cited) |
| `supplement.tex` | the figure removed; its sentence cites "Figure~1 of the main paper" |
| `prose_claims_b.py` | the seven caption entries read `main.tex`; two body entries anchored so they match once (the caption repeats their wording) |
| `audit/check_labels.py` | new: main-paper figures are numbered from the source and must appear in the compiled paper; every "Figure~N of the main paper" in the supplement must exist and, near "degeneracy", must cite a degeneracy figure |
| Overleaf bundles | main and supplement copies; `LOYOLA_MAIN_OVERLEAF/figures/` added with the figure; the unused copy removed from the supplement bundle; READMEs and page counts updated; zips rebuilt |
| `README.md`, `REPRODUCE.md`, `REVIEWER_START_HERE.md` | figure listings and page count |
| `LOYOLA_paper.pdf`, `LOYOLA_supplement.pdf` | rebuilt: 44 and 27 A5 pages |

The short draft (`drafts/short/`) was not changed. Its supplement is generated from `supplement.tex` and still
holds the figure as Figure S2; it is out of step with this branch until it is regenerated.

## Checks on this branch

Figure regeneration compared with the committed files (canonical form) and CSVs: identical. Labels and
references: PASS, and a supplement citing "Figure~2 of the main paper" fails. Prose numbers: 758 checked,
0 failures, and a caption changed from 79 to 78 fails. Prose style: PASS. Builds: no undefined references, no
overfull boxes, no "??"; the main Overleaf bundle compiles on its own with the figure. Tests of 19 and 20
October: all pass. `verify.py` (fast or full) was not run on this branch; the full run on `9212441` was in
progress and was not touched.
