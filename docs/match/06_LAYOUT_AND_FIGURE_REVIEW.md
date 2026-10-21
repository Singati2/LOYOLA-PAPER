# 06 — Layout and figure review

Candidate branch `review/match-figure-2026-10-20`; PDFs built with pdflatex (TeX Live on this machine), three
passes, from the committed sources. Inspected as rendered page images (all 44 + 27 pages as contact sheets at
40 dpi, the figure pages at 110 dpi) and programmatically (`pdftotext`, `pdffonts`, the LaTeX logs).

## Figure recommendation

The order-10 degeneracy chart (formerly Figure S2) is **Figure 1 of the main paper** (Section 4.2,
"Degeneracy across tree orders"); the octane heatmap stays in the supplement as **Figure S1**. Reasons, the
independent recount of every bar (106 trees, 79 profiles, floor 25.47 %, all twelve index counts equal to
`lo_sensitivity_degeneracy_order10_trees.csv`) and the file changes are in `audit/MATCH_FIGURE_2026-10-20.md`.
This is an AUTHOR DECISION to confirm.

The caption states the measure as $100(1 - 79/106)$, the number of distinct values against the number of
trees, which the main text defines ("distinct-value convention $100(1-k/N)$", Section 4.2). The supplement
(Section S5) adds that this is not the share of trees lacking a unique value (42.5 % for $LO(0,0,1)$). That
distinction is kept in the supplement and is referenced from the main text ("Supplementary Section~S5").

The chart was redrawn at 4.4 x 2.9 in (previously 6.5 x 3.6 in) so that, at 0.97 of the 11.3 cm A5 text
width, its text prints at about 7-8 pt (previously 4-5 pt). Data and colours are unchanged; a fresh
regeneration matches the committed file in the verifier's canonical form.

Update 2026-10-21: the chart is now black and white (light grey bars, dark grey bars on the floor, black
outlines and dashed line) because of MATCH's colour-figure fee; see `01_JOURNAL_REQUIREMENTS_AND_GAPS.md`.
Data, size and caption are unchanged.

## Cross-references changed

| Where | Before | After |
|---|---|---|
| `main.tex`, Section 4.2 | "(Supplementary Figure~S2)" | "(Figure~\ref{fig:degeneracy})" |
| `main.tex`, data availability | "supplementary sections, figures and tables cited here" | "supplementary sections and tables cited here" (the main text cites no supplementary figure) |
| `supplement.tex`, Section S5 | "(Figure~\ref{fig:degeneracy})" and the figure itself | "(Figure~1 of the main paper)"; figure removed (no duplicate) |
| `audit/check_labels.py` | no figure cross-check | main-paper figures numbered and checked; a wrong figure number from the supplement fails |

No bibliography entry was changed in this step. Reference-level findings are in `13_REFERENCE_AUDIT.md`.

## Page counts

| Document | Before (`9212441`) | Candidate |
|---|---|---|
| Main paper `LOYOLA_paper.pdf` | 43 | 44 |
| Supplement `LOYOLA_supplement.pdf` | 28 | 27 |
| Short draft `drafts/short/main_short.pdf` (archive, unchanged) | 24 | 24 |

## Build checks

| Check | Main | Supplement |
|---|---|---|
| Undefined references or citations (log) | 0 | 0 |
| `??` in the text | 0 | 0 |
| Overfull boxes (log) | 0 | 0 |
| Fonts embedded | all | all |
| Type 3 fonts | DejaVu Sans in Figure 1 (matplotlib default) | DejaVu Sans in Figure S1 |
| Label/reference/figure/table checker (`audit/check_labels.py`) | PASS | PASS |

Type 3 fonts are embedded and render correctly; MATCH states no font rule. Setting matplotlib's
`pdf.fonttype` to 42 would give TrueType fonts but changes both committed figure files; left as an optional
production choice.

## Page-by-page findings (main paper)

* p1: title block from the template; DOI line shows the template placeholders (correct for an unpublished
  paper). Abstract fits on the first page.
* p2-18: running text, theorem environments and proofs; no overfull lines; displayed equations within the
  text block.
* p19: Table 1 (octane collision pairs) at the top, then Section 4.2.
* p20: Figure 1 at the top, directly after its first citation (p19). p21: Table 2 on a float page with about 40 % white space. Alternatives were tried (figure earlier in the
  source): the figure then lands above its own subsection, and Table 2 still stands alone. Kept as is;
  minor. A production editor may reflow it.
* p23: Table 3 (structure sensitivity), small type as in the other tables.
* p31 (Table 4) and p35 (Table 5): dense (smallest type in the paper) but legible at 100 %; Table 5 is the densest
  object, as the 20 October review also noted.
* p38: Table 6 (protocol deviations).
* p40-44: acknowledgment and 56 references, alphabetical; p44 holds the last eight references.

## Supplement

Figure S1 (heatmap) on p5 at full width; the remaining pages are text and tables; Table S5 (octane data)
p23. No layout defects seen.

## Remaining warnings

1. Table 2 float page with white space (minor).
2. Tables 4 and 5 are dense; legible, but a referee may ask for splitting (editorial).
3. Type 3 figure fonts (optional change).
4. Front-matter items for the authors: acknowledgment text, corresponding author, e-mail line (see `01_...`).
