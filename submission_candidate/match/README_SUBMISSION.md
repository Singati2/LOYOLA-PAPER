# MATCH submission candidate — NOT SUBMITTED

Candidate for **coauthor review** only. Nothing here has been sent to MATCH. Prepared 2026-10-20 on the
local branch `review/match-figure-2026-10-20`; the manuscript sources are those of commit
`b7f50c094c815e25cbce356f878de89814a0395a` (unchanged in the later documentation commits).

## Contents

| File | What it is |
|---|---|
| `main.tex` | the manuscript, MATCH template (A5, 10 pt), bibliography embedded (56 references, alphabetical) |
| `LOYOLA_paper.pdf` | compiled manuscript, 45 A5 pages, one figure (Figure 1, degeneracy on the trees of order 10) |
| `supplement.tex` | Supplementary Material, own bibliography (14 references, alphabetical) |
| `LOYOLA_supplement.pdf` | compiled supplement, 27 A5 pages, Figure S1 |
| `figures/fig_lo_degeneracy_order10_trees_v2.pdf` | Figure 1 (used by `main.tex`) |
| `figures/fig_lo_prediction_correlation_heatmap_v3.pdf` | Figure S1 (used by `supplement.tex`) |
| `MATCH_OVERLEAF_CANDIDATE.zip` | the two `.tex` files and the two figures, nothing else |
| `COVER_LETTER_DRAFT.md` | unsent draft with author placeholders |
| `CLEAN_SUBMISSION_MANIFEST.md` | sizes and SHA-256 of every file here |

## Compile

```
pdflatex main.tex       # three times
pdflatex supplement.tex # three times
```

Tested from a clean extraction of `MATCH_OVERLEAF_CANDIDATE.zip` with TeX Live (pdflatex): 44 and 27
pages, no undefined references or citations, no missing figure, and the extracted text identical to the
included PDFs. On Overleaf: upload the zip, compile with pdfLaTeX, select `main.tex` or `supplement.tex`.

## Relation between the documents

The supplement is cited from the paper as "Supplementary Section S...", "Table S..." and is self-contained
for compilation. MATCH's instructions do not say whether a supplement may be e-mailed with the manuscript;
confirm with the editorial office (author item).

## Not included, on purpose

Data, scripts, verifiers, notebooks, Lean sources, audit records, logs, earlier drafts (including the
24-page short draft), Overleaf folders of the repository, and any NIST WebBook page. These stay in the
research repository (https://github.com/Singati2/LOYOLA-PAPER), which the paper cites. The citation gives no
exact commit yet (author item; see `docs/match/07_ETHICS_LICENSE_AUTHOR_DECISIONS.md`).

## Before sending (author items)

All three authors approve the final version; title; acknowledgment text; status and citation of the
companion manuscript; exact repository commit or archive DOI in the citation; NIST history and KDB/Chemeo
licensing decisions; whether to send the supplement. See `docs/match/` in the repository.
