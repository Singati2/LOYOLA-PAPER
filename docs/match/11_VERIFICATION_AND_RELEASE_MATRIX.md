# 11 — Verification and release matrix

Platform for every local run: Linux (Ubuntu, `mpcrlab12`), Python 3.13.16 in a uv environment built from
`requirements-lock.txt` and `requirements-extras-lock.txt` (resolving install, then an exact-version
check), pdflatex from TeX Live. NIST pages: the private local copies, all 262 identical to the archived
digests; nothing downloaded.

## Checks on the candidate

The candidate's code and manuscript are commit `b7f50c0`; `6f8ac71` adds only notebooks, `672a5b3` only
documentation. The runs below were made on `672a5b3` (which contains `b7f50c0` unchanged).

| Check | Command | Commit | Status | Runtime / log |
|---|---|---|---|---|
| Fast verification, clean detached worktree, NIST pages present | `python verify.py` | `672a5b3` | **PASS** (ALL PASS, exit 0; 17 stages; tree clean afterwards) | 17 min 15 s; `scratchpad/verify_672a5b3.log` |
| — of which prose numbers | `prose_numbers_check.py` | `672a5b3` | PASS: 764 checked, 0 failures, 22 uncheckable | 19 s |
| — of which manifest | `manifest.py` | `672a5b3` | PASS: 400 files | — |
| Labels, references, figures, tables, Overleaf bundles | `python audit/check_labels.py` | `672a5b3` | **PASS**, exit 0 | `labels_672a5b3.log` |
| Corrections tests (19 Oct) | `python audit/test_corrections_2026_10_19.py` | `672a5b3` | **PASS** (all checks), exit 0 | — |
| Review tests (20 Oct), incl. every Colab link -> notebook PIN = guide commit | `python audit/test_review_2026_10_20.py` | `672a5b3` | **PASS**, exit 0 | — |
| Figure regeneration vs committed figures and CSVs (canonical PDF form) | generator into a temp dir + `_pdf_canonical` | `5d5d16a` (figure code unchanged since) | PASS | — |
| Mutation tests of new registry entries (45, 42.5, four, figure caption 79) and of the figure cross-reference | edit, run checker, restore | working tree before `b7f50c0` | PASS (each mutation fails the checker) | — |
| PDF builds (superseded by the 2026-10-21 row below) | pdflatex x3 | `b7f50c0` sources | PASS: main 44 pp, supplement 27 pp; 0 undefined, 0 overfull, 0 `??`; 19 / 4 underfull notices (unchanged from before the edits) | — |
| Clean-extraction build of `MATCH_OVERLEAF_CANDIDATE.zip` (superseded by the 2026-10-21 row below) | unzip + pdflatex x3 | `b7f50c0` sources | PASS: 44 / 27 pp; text identical to the included PDFs | `scratchpad/build_package.sh` |
| Independent counterexample verification (41 claims) | `audit/independent_counterexamples_2026-10-20/*.py` | `325bd05` text (claims unchanged since) | 38 CONFIRMED, 0 REFUTED, 3 NOT CHECKABLE | about 8 min, one core |
| Reference audit (56 + 14 references) | manual + Crossref | `325bd05` | 84 supported, 7 partial (wording fixed in `b7f50c0`), 0 unsupported, 6 not verifiable | `13_REFERENCE_AUDIT.md` |
| `verify.py --full`, clean detached worktree, NIST pages present, Lean cache | `python verify.py --full` | `390728b` (code and manuscript of `c48bad0`; later commits change only docs and this log) | **PASS**: ALL PASS (full), exit 0; 25 stages PASS, 0 FAIL, 0 SKIP, incl. external verifier (5216 s), structural checks (3286 s), 32-digit recount, exact tie certificate, self-test, 13/13 counter-attacks rejected, labels, Lean (52 declarations, standard axioms only) | 180 min; `scratchpad/verify_full_390728b.log`. The only file rewritten is the counter-attack log `audit/attack_checks_out.txt` (its committed copy quoted 756 checked; refreshed to 764; it also contains a random temporary-folder name, so it differs on every run) |
| `verify.py --everything` / Colab stage 7 | — | candidate | **NOT RUN** | many hours; author approval |
| Lean build | `formal/verify.sh` | candidate | **NOT RUN** (`formal/` unchanged since the last recorded pass at `3af7f67`) | — |
| Any Google Colab session | — | any | **NOT TESTED IN REAL COLAB** | see `10_COLAB_REPRODUCIBILITY_TEST.md` |
| Simulated clean Colab-style runtime (Python 3.12, clone from GitHub, fake `google.colab`), notebooks 01-06 and colab/12 | nbclient | pin `0477cdf` (same setup code as `c48bad0`) | PASS: 01 9/0, 02 20/0, 03 25/0, 04 69/0, 05 27/0, 06 ALL PASS on Python 3.13.16 (6/0), colab/12 ALL CERTIFICATES REPRODUCED | about 40 min; `10_COLAB_REPRODUCIBILITY_TEST.md` |
| Cross-checks outside the replay plan | `audit/permutation_pipeline_audit.py`, `audit/v4030/uncertain_source_crosscheck.py` | candidate | NOT RUN (committed outputs from older commits) | — |

## Additions of 2026-10-21 (branch `review/match-final-adjustments-2026-10-21`)

These follow `audit/CLAUDE_MATCH_FINAL_SUBMISSION_ACTIONS_2026-10-20.md`. The manuscript sources (`main.tex`,
`supplement.tex`), data, figures and notebooks are unchanged from `c48bad0`; the replay harness changed (code
commit `69b9538`), so `390728b`'s full pass does not cover the harness change itself.

| Check | Command | Commit | Status | Runtime / log |
|---|---|---|---|---|
| Replay-contract attacks on synthetic repositories (missing, empty, scratch-only and unlisted outputs; truncated, replaced, deleted cached outputs; forged index entries incl. a staged source edit; path traversal; corrupted index, record and run.json; other commit; tampered fingerprint; changed upstream input; deleted and renamed sources; differing outputs; a clean run reports COMPLETE) | `python audit/test_replay_contract_2026_10_21.py` | `69b9538` | **PASS**: 44/44, exit 0 | about 20 s |
| Same attacks against the previous runner (before) | same test copied into a worktree of `5a96fc5` | `5a96fc5` | as expected FAILS: A1, A1', A2, A3, A3', A4, A5 (exit 0 accepted without its output, or with a scratch file, an empty file or an unlisted rewrite), A10b (a staged source edit hidden by a forged index entry is accepted), A11, A12; the corrupted-index case ends in an unhandled `JSONDecodeError`. A10 was refused only through a path-parsing slip (first path read as `xternal/src.py`) | `scratchpad/inv/before.txt` |
| Mutation tests of the new checks | remove each check in turn, rerun the test | working tree | PASS: each mutation makes its attack test fail (A1-A3, A10, A11, A17) | — |
| Earlier pipeline tests | `python audit/test_corrections_2026_10_19.py`, `python audit/test_review_2026_10_20.py` | `69b9538` | **PASS** (fixture of item 1 now commits its two outputs and lists them, as the new contract requires) | — |
| Expected-output inventory vs actual writes | 45 scripts of at most 6 lab minutes run in order in a throwaway clone with the private NIST pages; tracked files rewritten per script recorded | `5a96fc5` scripts | **PASS**: 45/45 exit 0; each rewrote exactly its listed tracked files, no untracked file; 15 longer scripts not run | `scratchpad/inv/trace.json` |
| Expected-output inventory, long scripts | write calls read by hand; counts compared with the lab replay of `09ceba8` | — | consistent with every lab count (`verification_logs/lab_09ceba8`); NOT RUN here | — |
| Clean-extraction build of `MATCH_OVERLEAF_CANDIDATE.zip` | unzip into an empty folder + pdflatex x3 | `c48bad0` sources | **PASS**: main 45 pp (Figure 1 on p. 22), supplement 27 pp; 0 undefined, 0 overfull; text identical to the included PDFs except the `\today` "Received" date | — |
| Reviewer links | raw.githubusercontent.com for every Colab link in README, REVIEWER_START_HERE, COLAB_FOR_REVIEWERS, docs/match/08 | `afafe6c`, `23bfd45` | **PASS**: 14/14 real links 200 without signing in (2 further matches are `<NB_COMMIT>` placeholders) | — |
| Fast verification of the code commit, clean detached worktree, NIST pages present | `python verify.py` | `69b9538` | **PASS**: ALL PASS (fast path), exit 0, 17 stages, 764 prose numbers checked (0 failures), manifest 416 files; tree clean afterwards. `verify.py` does not run the replay harness, so this is a regression check of everything else | 17 min; `scratchpad/verify_69b9538.log` |
| Labels, figures, tables, bundles | `python audit/check_labels.py` | `69b9538` | **PASS**, exit 0 | — |
| New runner on real scripts: `run_all_scripts.py --fast` | `python audit/run_all_scripts.py --fast`, clean detached worktree, NIST pages present | `69b9538` | 41 scripts: 40 OK (8 check-only, every other script rewrote exactly its listed outputs, identical), 1 PROBLEM: `counterattack_v4030.py`, whose output differs in the same lines as on the lab replay of `09ceba8` (deliberately near-singular designs; `SEEN_BEFORE`). No false PROBLEM from the new rule | about 40 min; `scratchpad/inv/runall_fast.log` |
| New runner on real scripts: pipeline stages 1 and 8, then `--report` | `colab/pipeline.py --stage 1`, `--stage 8`, `--report` (state folder in scratch, private NIST cache) | `69b9538` | 10/10 scripts OK, 14 outputs identical to the commit; report correctly not COMPLETE ("10 scripts OK, 0 PROBLEM, 0 STALE, 50 NOT RUN; 0 outputs differ"); stages 2-7 NOT RUN | about 5 min; `scratchpad/inv/report.log` |
| Real Google Colab | — | any | **NOT TESTED** | — |
| Figure 1 in black and white (MATCH colour-figure fee): fresh regeneration vs committed figure and CSVs | generator into a temp dir + `_pdf_canonical` | this commit | **PASS**: both figures equal in canonical form, 3 CSVs identical; rendered bar chart has 0 chromatic pixels; the heatmap is unchanged byte for byte | — |
| Rebuild of `LOYOLA_paper.pdf` and clean-extraction build of the zip after the figure change | pdflatex x3; `scratchpad/build_package.sh` | this commit (sources of `c48bad0`) | **PASS**: 45 + 27 pp, 0 undefined, 0 overfull; text of the paper identical to the previous PDF except the `\today` date (now October 21, 2026); supplement PDF not rebuilt (it does not use Figure 1) | — |
| Editorial prose pass (branch `review/match-editorial-clarity-2026-10-22`, base `723a2d0`): fast verification | `python verify.py` | edited working tree on `31e61ec` (before the docs-only fast-forward to `723a2d0`) | all stages **PASS** except manifest (expected: new docs files and edited `main.tex` not yet in `SHA256SUMS.txt`, regenerated in the editorial commit); NIST stages SKIP (pages not present in that worktree) | about 17 min; `scratchpad/verify_edit.log` |
| Editorial pass: prose numbers, style, labels/compile, tests of 19 and 20 Oct, manifest | `prose_numbers_check.py`, `audit/check_style.py`, `audit/check_labels.py`, `audit/test_*`, `manifest.py` | editorial commit | see `audit/EDITORIAL_PRESERVATION_CHECK_2026-10-22.md` | — |
| Editorial pass: rebuild and clean-extraction build | pdflatex x3; `scratchpad/build_package.sh` | editorial commit | **PASS**: 46 + 27 pp, 0 undefined, 0 overfull, Figure 1 on p. 21; text of the clean build identical to `LOYOLA_paper.pdf`; supplement text identical except the `\today` date | — |
| Shortening to 35 pp (2026-10-23): fast verifier, offline | `python verify.py --offline` | shortening commit (working tree before commit) | **ALL PASS** (exit 0): core verifier (all 8 numeric tables), prose numbers 756/0, baseline tests, constancy, interval certificates, style, extremal trees 4-12, collision minimality 13/16, sum-connectivity pair, count dimension, DATA copies, manifest 428 files; NIST-page stages NOT RUN (pages not present) |
| Shortening: labels, tests, builds | `audit/check_labels.py`, three `audit/test_*` suites, pdflatex x3, `build_package.sh` | shortening commit | **PASS**: labels; tests exit 0; main 35 pp, supplement 39 pp, 0 undefined, 0 overfull; clean-extraction text identical. NOT RUN: `--full` (incl. attack checks), `--everything`, Lean, Colab |
| Tests after the figure change | `test_review_2026_10_20`, `test_corrections_2026_10_19`, `test_replay_contract_2026_10_21`, `check_labels`, `check_style` | this commit | **PASS**, all exit 0 | — |

### Release set (what belongs together)

| Item | Commit or file |
|---|---|
| Manuscript and supplement sources | `c48bad05f8e95805d4f0f700f5324d1071b903cd` (unchanged since) |
| Notebooks and their PIN | notebooks at `afafe6c44bd66e0d90e7b5e723010e41e1236ec2`, pinned to `c48bad0`; not re-pinned (the checklist says to re-pin only once the final code commit is settled) |
| Last full verification | `390728b` (code and manuscript of `c48bad0`); ALL PASS (full), 25/25 |
| Replay harness with the expected-output contract | `69b9538` (descendant of `390728b`; not covered by its full run; covered by the contract tests and the fast run above) |
| Submission package | `submission_candidate/match/` at the head of `review/match-final-adjustments-2026-10-21`; Figure 1, `LOYOLA_paper.pdf` and the zip regenerated after Figure 1 was made black and white; the supplement PDF is unchanged from `c48bad0` (SHA-256 in `CLEAN_SUBMISSION_MANIFEST.md`). The notebooks are pinned to `c48bad0` and so still regenerate the blue version of Figure 1 until they are re-pinned |

## Earlier evidence (certifies only its own commit)

| Run | Commit | Status |
|---|---|---|
| `verify.py --full`, clean worktree, NIST pages present | `9212441` (pushed head of `review/corrections-impl-2026-10-19`) | **PASS**: ALL PASS (full), exit 0, all stages incl. Lean; 190 min; first complete full pass of the project. It certifies `9212441` only |
| `verify.py` fast | `9212441`, `f6bbb49` | PASS (earlier reports) |
| `verify.py --full` | `67e36ad` | FAILED, two harness/environment causes, both since fixed (see `audit/VERIFICATION_AND_NIST_STATUS.md`) |

## Which result-level checks the candidate's edits could affect

The edits are wording, a figure's drawing size, registry patterns and a checker. Computations, data sets
and committed outputs are unchanged (the manifest of `672a5b3` matches, and the core verifier regenerated the
outputs it covers and found them identical, including both figures). The long suites of `--full` (external
verifier, structural checks, 32-digit recount, self-test, counter-attacks, Lean) do not read the edited text
except through the checks already run above, so their outcome on `9212441`, once finished, is relevant
evidence for the computations but not a certification of this commit.

## Release blockers

| # | Blocker | Owner |
|---|---|---|
| 1 | Approval of the final version by all three authors (MATCH ethics) | authors |
| 2 | Companion manuscript: status, citation or disclosure | authors |
| 3 | NIST pages in public history and the default branch; KDB/Chemeo redistribution | authors / legal |
| 4 | Repository citation without an exact commit or DOI | authors |
| 5 | ~~Push of `review/match-figure-2026-10-20`~~ done 2026-10-20 (normal push, not merged); links return 200 | — |
| 6 | ~~Full verification of the final commit~~ done: PASS at `390728b` | — |
| 7 | One real Colab session of the essential reviewer path | user |
| 8 | Acknowledgment text; title confirmation; optional condensation | authors |

Status of the candidate: **full verification PASS** at `390728b`; replay-harness contract tests PASS at `69b9538`; essential notebooks PASS in a simulated Colab-style runtime; **NOT TESTED IN REAL COLAB**.
