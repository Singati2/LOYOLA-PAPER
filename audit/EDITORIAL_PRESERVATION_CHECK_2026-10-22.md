# Editorial preservation check, 2026-10-22

- **Starting branch:** `review/match-final-adjustments-2026-10-21`. Work began at `31e61ec`.
- **Base:** fast-forwarded before committing to `723a2d0`, which adds only `docs/CLAUDE_EDITORIAL_EXECUTION_GO_2026-10-22.md`. `main.tex` is the same at `31e61ec` and `723a2d0`.
- **Branch:** `review/match-editorial-clarity-2026-10-22`, a separate worktree, committed locally only.
- **Briefs:**
  - `docs/CLAUDE_MANUSCRIPT_STYLE_REVISION_PROMPT_2026-10-22.md`
  - `docs/CLAUDE_EDITORIAL_EXECUTION_GO_2026-10-22.md`
- **Other worktrees:** none touched; `wt-mainrevert` was not modified.

## Changed files

| File | Change |
|---|---|
| `main.tex` | prose only; see `audit/EDITORIAL_STYLE_CHANGELOG_2026-10-22.md` |
| `LOYOLA_MAIN_OVERLEAF/main.tex`, `LOYOLA_FINAL_PAPER_OVERLEAF/main.tex`, `submission_candidate/match/main.tex` | copied from `main.tex`; they were byte-identical copies before and are again |
| `LOYOLA_paper.pdf`, `submission_candidate/match/LOYOLA_paper.pdf` | rebuilt (pdflatex x3) |
| `LOYOLA_MAIN_OVERLEAF.zip`, `LOYOLA_FINAL_PAPER_OVERLEAF.zip`, `submission_candidate/match/MATCH_OVERLEAF_CANDIDATE.zip` | rebuilt from the bundle folders |
| `submission_candidate/match/CLEAN_SUBMISSION_MANIFEST.md`, `submission_candidate/match/README_SUBMISSION.md` | hash rows, page count (46) and Figure 1 page (21) |
| `docs/match/01_JOURNAL_REQUIREMENTS_AND_GAPS.md`, `docs/match/11_VERIFICATION_AND_RELEASE_MATRIX.md` | page count; verification rows |
| `audit/EDITORIAL_STYLE_CHANGELOG_2026-10-22.md`, this file | new |
| `SHA256SUMS.txt` | regenerated (`manifest.py --write`) |

**Not changed:** `supplement.tex`, figures, data, CSV outputs, scripts, notebooks, registries, `formal/` (Lean), protocols, seeds and locks. `git diff 723a2d0 -- supplement.tex figures/ '*.csv' '*.py' formal/` is empty.

## Preservation of the mathematics and metadata

These results come from a script in the session scratchpad (`preserve.py`). It compares the environments, whitespace-normalised, of `git show 723a2d0:main.tex` and the edited `main.tex`.

| Item | Result |
|---|---|
| Preamble (title, authors, affiliations, e-mails, macros) | identical |
| 2 theorems, 1 lemma, 12 propositions, 3 corollaries, 4 definitions, 16 proofs, 8 remarks, 2 examples | identical |
| 9 `equation` environments, all display math `\[...\]` | identical |
| 6 tables (all cells and captions), 1 figure and its caption | identical |
| Bibliography | identical |
| `\label`s | none added or removed |
| `\cite`s | one `\cite{LoyolaRepo}` merged away in the Data availability paragraph (the repository is still cited there); one `\cite{Rada2026LinearVDB}` added to the new first sentence of the introduction, which states the degree-pair ceiling that the paper already attributes to this reference |
| `\ref`s | only additions (cross-references in the regrouped contribution list and the new discussion paragraph) |
| Inline math in prose | added `$13$` and `$16$`, in the discussion paragraph, restating Theorem `thm:ratioplane`(iii) and Remark `rem:floor`. Removed: `$IRLA$` from the conclusion, `$GA$`/`$AG$` from the contribution list (still named in the introduction), and one `$\Pi$` |

## Checks

| Check | Command | Result |
|---|---|---|
| Prose numbers (every registered numeral, anchored on its sentence) | `python prose_numbers_check.py` | **PASS**: 764 checked, 0 failures, 22 uncheckable; no registry pattern was edited |
| Prose style | `python audit/check_style.py` | **PASS** (longest sentence 45 words; no dashes or stock phrases) |
| Labels, references, figure, tables, Overleaf bundles; compile | `python audit/check_labels.py` | **PASS** |
| Tests of 19 Oct, 20 Oct and the replay contract | `python audit/test_corrections_2026_10_19.py`, `audit/test_review_2026_10_20.py`, `audit/test_replay_contract_2026_10_21.py` | **PASS** (all three exit 0) |
| Manifest | `python manifest.py` | **PASS**: 420 files, all match |
| Fast verification | `python verify.py`, edited tree before the fast-forward | all stages **PASS** (core verifier including the drift guard on all 8 numeric tables, prose numbers, baseline tests, certificates, collision minimality 13/16, extremal trees, style), except: **FAIL manifest**, as expected before regeneration and **PASS** after it (row above); **SKIP** for the NIST stages (pages not present in this worktree) |
| PDF build | pdflatex x3 | **PASS**: 46 pages (base 45), 0 undefined, 0 overfull, 18 underfull notices (base 19), Figure 1 on p. 21 |
| Clean-extraction build of `MATCH_OVERLEAF_CANDIDATE.zip` | `build_package.sh` | **PASS**: 46 + 27 pages; paper text identical to `LOYOLA_paper.pdf`; supplement text identical except the `\today` "Received" date |
| Attack-suite anchors used by `audit/attack_checks.py` | grep | present once each |
| `verify.py --full` / `--everything`, Lean build, Colab | — | **NOT RUN**: the science is unchanged and the brief excludes expensive runs |

## Not pushed

The branch is committed locally and has not been pushed. Nothing was merged, force-pushed or rewritten.
