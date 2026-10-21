# Change report for `audit/CLAUDE_MATCH_FINAL_SUBMISSION_ACTIONS_2026-10-20.md`

Date: 2026-10-21. Branch `review/match-final-adjustments-2026-10-21`, made from
`origin/review/match-figure-2026-10-20` at `5a96fc5` (no uncommitted changes at the start). Separate
worktree; no other worktree or running process was touched. Nothing was merged, tagged, force-pushed or
submitted. Datasets, pre-registrations, seeds, numerical outcomes, theorems, Lean files, manuscript
sources, figures and notebooks are unchanged.

Commits: code `69b9538`; documentation and package: the next commit on the branch (it changes no code).

## Dispositions

Kinds: **confirmed defect**, **stale documentation**, **not yet tested**, **author/legal decision**.

| # | Item | Kind | Disposition |
|---|---|---|---|
| P1.1 | No authoritative per-script output list; status was exit 0 plus any detected write | confirmed defect | **FIXED**: `colab/expected_outputs.py` lists the outputs of all 60 scripts of the plan (7 check-only). It was reviewed by hand from each script's write calls, checked against every rewrite count of the lab replay of `09ceba8`, and checked by a trace of the 45 shorter scripts (see below). It is not derived from observed writes. |
| P1.2 | A script could pass with its required output missing, empty, or replaced by a scratch file, or after rewriting another tracked file | confirmed defect (before-test A1-A5 fail) | **FIXED** in `colab/pipeline.py` (`run_script`, `validate`) and `audit/run_all_scripts.py` (`judge`). Only listed outputs are saved to the state folder. A record must list exactly the expected outputs. |
| P1.3 | Input fingerprints, prior-stage dependencies, fail-closed reuse | partly present before (fingerprint, upstream digests) | **FIXED** for the gaps: the fingerprint now also covers the runner and the output list. An unreadable record is STALE and is rerun. A record of another script, or one whose outputs differ from the list, is STALE. A corrupted `files.json` or `run.json` stops the runner with a message instead of a traceback. |
| P1.4 | `check_clean()` | confirmed defect (before-test A10b fails) | **FIXED**. Before: a staged source edit plus a forged index entry was accepted. The porcelain parser also dropped the first character of the first path, which is the only reason the unstaged case was refused. Now `git diff --no-renames --name-only -z HEAD` covers modified, deleted and renamed files (both paths), staged or not. A changed file is accepted only if it is a listed output of the script named in the index, and both the index and that script's record hold its current digest. |
| P1.5 | `--report` wording and COMPLETE criterion | confirmed (wording claimed "every expected output" without a list) | **FIXED**: COMPLETE now requires all 60 records valid against the list and no output differing from the commit. The verdict reads "COMPLETE (replay plan only)" and says that the two independent cross-checks were not run and that the run is not a replay of every script of the repository. |
| P1.6 | Malformed state, forged markers, unknown paths, traversal | confirmed defect (before: no path check; traceback on bad JSON) | **FIXED**: index paths must be plain relative paths inside the repository, not in `.git`, not NIST pages, and listed outputs of the named script; otherwise the runner stops. |
| P1 tests | adversarial regression tests | — | `audit/test_replay_contract_2026_10_21.py`: 44 checks, all PASS, exit 0, about 20 s. Against the old runner the same file fails A1, A1', A2, A3, A3', A4, A5, A10b, A11 and A12, then stops with an unhandled `JSONDecodeError` at A13. Mutations that remove each new check make the corresponding test fail. These are mock runs, not a real or Colab replay. |
| P1 cover letter | path/star extremality marketed as new; attribution | confirmed defect | **FIXED** in `COVER_LETTER_DRAFT.md`. The new results come first: orders 13/16, witnesses, the computer-assisted scope of minimality, the corollary for degree-ratio indices, the crossing bound and the algebraic-γ statement. The letter credits Rada 2026 §3.1, Rada 2019 Thm 3.4 / Prop. 2.5 and Cruz–Rada 2019, and states that the predictive results do not show equivalence or that γ can never help. Placeholders added for the companion title (three wordings in its repository) and for the statement that earlier drafts were never submitted. Author names and order are unchanged. |
| P2 page counts | 44 vs 45 | stale documentation | **FIXED**: a fresh clean-extraction build gives 45 + 27 pages, Figure 1 on p. 22, 0 undefined, 0 overfull, and text identical to the included PDFs except the `\today` date. `README_SUBMISSION.md` corrected; the old matrix rows are marked superseded. PDFs and zip are unchanged, so their hashes stand. |
| P2 manifest | `CLEAN_SUBMISSION_MANIFEST.md` | stale after the edits | **FIXED**: regenerated for the changed cover letter and README; the other hashes were re-checked and are unchanged. |
| P2 release row | matrix | — | **ADDED** to `docs/match/11`: tests per commit, the release set, and which commits a run covers. |
| P2 links and pins | "not pushed / 404" notes | stale documentation | **FIXED** in `docs/match/01`, `08`, `10`, `11`. All 14 real reviewer links return 200 without authentication. Notebook PINs are unchanged (`c48bad0`), as checked by `audit/test_review_2026_10_20.py`. **Not re-pinned**: the checklist says to wait for the final code commit. The staged Colab notebooks therefore still run the old runner until the authors settle the code and the pins are regenerated. |
| P2 repository citation | `\bibitem{LoyolaRepo}` gives only the URL | author decision | **UNCHANGED**: a commit or DOI can only be cited once the authors fix the final commit. Placeholder in the cover letter. |
| P2 short manuscript | the 24-page draft | — | **UNCHANGED**: already labelled as not part of the package (`README_SUBMISSION.md`, "Not included"). |
| P2 real Colab | — | not yet tested | **NOT TESTED**. Manual steps are in `docs/match/08_COLAB_START_HERE.md` and `COLAB_FOR_REVIEWERS.md`. Stage 7 and `--everything` were not started. |
| MATCH colour-figure fee | Figure 1 (moved into the main paper on 2026-10-20) was in colour; the fee paragraph of `prepare.html` (90 EUR per coloured figure, or redraw in black and white) is in an HTML comment, and published MATCH papers checked have no colour | found 2026-10-21 | **FIXED** on the authors' instruction: `generate_loyola_v35_figures.py` draws the bars in greys with black outlines and a black dashed line; data, caption and size unchanged; figure copies, `LOYOLA_paper.pdf`, zip and manifests regenerated. Notebooks still pinned to `c48bad0` (blue version) until re-pinned |
| P2 data disclosure | 58 aggregate-derived boiling points | — | **UNCHANGED**, already disclosed: `supplement.tex:1036` (57 direct averages + 1 mean of two). |
| P2 NIST/KDB/Chemeo, approvals, title, acknowledgment, companion status | — | author/legal decision | **UNCHANGED**; see the table below. |

## Still open (authors / legal)

| Decision | Where |
|---|---|
| Approval of the final version by all three authors; author order, spelling, affiliations, corresponding author | `docs/match/07` §4, §6 |
| Final title | cover letter placeholder |
| Companion manuscript: status (including the June version with a fourth author), title, citation or disclosure | `docs/match/07` §3, `16_COMPANION_OVERLAP.md` |
| NIST pages in public history and on `main`; KDB/Chemeo redistribution | `docs/match/07` §1-2, `audit/NIST_HISTORY_REMEDIATION_PLAN.md` |
| Exact commit or DOI for the repository citation; then re-pin the notebooks to that commit | `main.tex` `LoyolaRepo`; three-commit pin chain |
| Acknowledgment text; AI-use disclosure | `docs/match/07` §5 |
| Abstract wording "We also show … that the path and the star are the extremal trees": the body credits Cruz–Rada, but the abstract does not say the result follows from known criteria. Suggested: "… and, from known criteria, that the path and the star …". Not changed, because it is manuscript text. | `main.tex:208` |

## Tests run (exit codes)

| Test | Commit | Exit | Result |
|---|---|---|---|
| `python audit/test_replay_contract_2026_10_21.py` | `69b9538` | 0 | 44/44 PASS |
| same test against the previous runner | `5a96fc5` | 1 | fails A1, A1', A2, A3, A3', A4, A5, A10b, A11, A12; crashes at A13 (unhandled `JSONDecodeError`) |
| mutations removing each new check | working tree | — | each makes its attack test fail |
| `python audit/test_corrections_2026_10_19.py` | `69b9538` | 0 | ALL CHECKS PASSED |
| `python audit/test_review_2026_10_20.py` | `69b9538` | 0 | ALL CHECKS PASSED |
| trace of the 45 shorter scripts vs `colab/expected_outputs.py` | `5a96fc5` scripts | 0 | 45/45 match exactly, no untracked writes |
| `python verify.py` (fast), clean worktree, NIST pages present | `69b9538` | 0 | ALL PASS (17 stages), tree clean |
| `python audit/run_all_scripts.py --fast` (new runner, real scripts) | `69b9538` | 1 | 40/41 OK; the 1 PROBLEM is the known near-singular difference of `counterattack_v4030.py` (same lines as the lab replay of `09ceba8`) |
| `colab/pipeline.py --stage 1`, `--stage 8`, `--report` | `69b9538` | 0, 0, 1 | 10/10 OK, 14 outputs identical; report "50 NOT RUN", correctly not COMPLETE |
| `python audit/check_labels.py`, `audit/check_style.py` | working tree | 0, 0 | PASS |
| clean-extraction build of the Overleaf zip | `c48bad0` sources | 0 | 45 + 27 pages; text identical except the date |

Not run: `verify.py --full` or `--everything` at `69b9538`, pipeline stages 2-7, real Google Colab.
