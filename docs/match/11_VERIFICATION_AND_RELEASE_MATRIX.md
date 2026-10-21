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
| PDF builds | pdflatex x3 | `b7f50c0` sources | PASS: main 44 pp, supplement 27 pp; 0 undefined, 0 overfull, 0 `??`; 19 / 4 underfull notices (unchanged from before the edits) | — |
| Clean-extraction build of `MATCH_OVERLEAF_CANDIDATE.zip` | unzip + pdflatex x3 | `b7f50c0` sources | PASS: 44 / 27 pp; text identical to the included PDFs | `scratchpad/build_package.sh` |
| Independent counterexample verification (41 claims) | `audit/independent_counterexamples_2026-10-20/*.py` | `325bd05` text (claims unchanged since) | 38 CONFIRMED, 0 REFUTED, 3 NOT CHECKABLE | about 8 min, one core |
| Reference audit (56 + 14 references) | manual + Crossref | `325bd05` | 84 supported, 7 partial (wording fixed in `b7f50c0`), 0 unsupported, 6 not verifiable | `13_REFERENCE_AUDIT.md` |
| `verify.py --full`, clean detached worktree, NIST pages present, Lean cache | `python verify.py --full` | `390728b` (code and manuscript of `c48bad0`; later commits change only docs and this log) | **PASS**: ALL PASS (full), exit 0; 25 stages PASS, 0 FAIL, 0 SKIP, incl. external verifier (5216 s), structural checks (3286 s), 32-digit recount, exact tie certificate, self-test, 13/13 counter-attacks rejected, labels, Lean (52 declarations, standard axioms only) | 180 min; `scratchpad/verify_full_390728b.log`. The only file rewritten is the counter-attack log `audit/attack_checks_out.txt` (its committed copy quoted 756 checked; refreshed to 764; it also contains a random temporary-folder name, so it differs on every run) |
| `verify.py --everything` / Colab stage 7 | — | candidate | **NOT RUN** | many hours; author approval |
| Lean build | `formal/verify.sh` | candidate | **NOT RUN** (`formal/` unchanged since the last recorded pass at `3af7f67`) | — |
| Any Google Colab session | — | any | **NOT TESTED IN REAL COLAB** | see `10_COLAB_REPRODUCIBILITY_TEST.md` |
| Simulated clean Colab-style runtime (Python 3.12, clone from GitHub, fake `google.colab`), notebooks 01-06 and colab/12 | nbclient | pin `0477cdf` (same setup code as `c48bad0`) | PASS: 01 9/0, 02 20/0, 03 25/0, 04 69/0, 05 27/0, 06 ALL PASS on Python 3.13.16 (6/0), colab/12 ALL CERTIFICATES REPRODUCED | about 40 min; `10_COLAB_REPRODUCIBILITY_TEST.md` |
| Cross-checks outside the replay plan | `audit/permutation_pipeline_audit.py`, `audit/v4030/uncertain_source_crosscheck.py` | candidate | NOT RUN (committed outputs from older commits) | — |

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
| 5 | Push of `review/match-figure-2026-10-20` (Colab links 404 until then) | user |
| 6 | ~~Full verification of the final commit~~ done: PASS at `390728b` | — |
| 7 | One real Colab session of the essential reviewer path | user |
| 8 | Acknowledgment text; title confirmation; optional condensation | authors |

Status of the candidate: **full verification PASS** at `390728b`; essential notebooks PASS in a simulated Colab-style runtime; **NOT TESTED IN REAL COLAB**.
