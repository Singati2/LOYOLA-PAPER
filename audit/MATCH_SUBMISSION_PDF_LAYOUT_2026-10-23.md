# Submission PDF layout, 2026-10-23

## Supplement: Table S8 and the bibliography

**Before (`f720a16`).** The References heading, entries [1]–[2], Table S8, and then [3] onwards fell on these pages:

| Page | Content (`pdftotext`) |
|---|---|
| 36 | References heading, [1], [2], and Table S8 (start) |
| 37 | Table S8 |
| 38 | [3] … |

**Cause.** At `supplement.tex` line 1660, `\begin{thebibliography}` followed `\end{table}` of `tab:deviations` with no float flush. The `\FloatBarrier` added on 23 October sat before S10 only.

**Fix.** `\FloatBarrier` was inserted immediately before `\singlespacing\n\begin{thebibliography}{00}`; `placeins` was already loaded.

**After (source commit `e3fc881`):**

| Page | Content |
|---|---|
| 37 | Table S8, complete: the deviation table, 10 rows |
| 38 | "References", [1]–[11] |
| 39 | [12]–[21] |

Pages 37 and 38 were rendered with `pdftoppm` at 60 dpi and inspected visually. Table S8 is complete on p. 37, the References heading starts p. 38, and the entries are contiguous through [21]. No table interrupts them.

**Unchanged:**
- 39 pages;
- Table S1–S8, Section S1–S11 and equation numbering, with all labels resolved;
- 0 undefined references or citations;
- 0 overfull boxes.

## Main paper

The only text change is the order sentence after the proof of Theorem 2. The paper is still 37 pages, with 0 undefined references and 0 overfull boxes, and float placement is unchanged.

## Copies and hashes

The SHA-256 prefixes match at the source commit:

| File | Root | `submission_candidate/match/` |
|---|---|---|
| `LOYOLA_paper.pdf` | `5a6d4ece7da04159…` | `5a6d4ece7da04159…` |
| `LOYOLA_supplement.pdf` | `ac6585c6a0d29729…` | `ac6585c6a0d29729…` |

**Zips and manifests:**
- `MATCH_OVERLEAF_CANDIDATE.zip` (`14bd2a9a1f61d557…`) was rebuilt from the committed sources.
- Clean extraction gives 37 + 39 pages, 0 undefined, no placeholders and no `??`. The `pdftotext` output of the clean build equals the shipped PDFs for both documents: True, True.
- The three Overleaf zips (`LOYOLA_FINAL_PAPER_OVERLEAF`, `LOYOLA_MAIN_OVERLEAF`, `LOYOLA_SUPPLEMENT_OVERLEAF`) were rebuilt from the synced bundle folders.
- `CLEAN_SUBMISSION_MANIFEST.md` rows were regenerated, 5 of them changed, and `SHA256SUMS.txt` was rewritten. `manifest.py` reports all files matching.

**Not changed:** the captions of Tables 2 and 5 (the optional simplification in the brief) were left as they are, because their content is correct.
