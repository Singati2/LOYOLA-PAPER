# Colab reproducibility test (draft, 2026-10-20)

**Nothing here was tested in real Google Colab.** This machine has no Colab access. Everything below is
static reading of the code plus cheap local checks on the worktree `wt-fig` (branch
`review/match-figure-2026-10-20`, HEAD `325bd05`, local only), with no edits to it. Two local
assumptions should be kept in mind when reading the results: the local environment is Python 3.13 with
the locked versions, and Colab's Python is assumed to differ.

## 1. What was executed (static and cheap checks)

| # | Check | Command (abridged) | Result |
|---|---|---|---|
| 1 | PIN, REVISION and badge in every committed notebook, for both chains | `git show <c>:<path>` for c = `6f8ac71` and `23bfd45`, then a regex for `LOYOLA_PIN`, `REVISION`, `blob/` and output counts (`scratchpad/match_audit_pins.py`) | 19/19 notebooks at `6f8ac71`: PIN `b7f50c0be45e…`, REVISION `review/match-figure-2026-10-20`. 19/19 at `23bfd45`: PIN `95c840c857d0…`, REVISION `review/corrections-impl-2026-10-19`. 0 stored outputs in every notebook. No `/home`, `mpcrlab` or `FAU` string |
| 2 | Pin chain scope | `git diff --stat b7f50c0 6f8ac71`; `git diff --stat 6f8ac71 325bd05`; `git merge-base --is-ancestor b7f50c0 6f8ac71` | `6f8ac71` changes 19 notebooks plus `SHA256SUMS.txt` only. `325bd05` changes README, guide and `SHA256SUMS.txt` only. The pin is an ancestor of the notebook commit |
| 3 | The generators reproduce the committed notebooks | scratch clone (`git clone` of the worktree into `scratchpad/regen_clone`), then `colab/make_notebooks.py --pin b7f50c0 --revision review/match-figure-2026-10-20` and the same for `notebooks/gen_notebooks.py` | 19 files changed, and the only changed lines are the random nbformat cell `id`s. Content is identical |
| 4 | Notebook validity | `nbformat.validate` plus `ast.parse` of every code cell | 19/19 valid, 0 syntax errors |
| 5 | Plan consistency | import `colab/pipeline.py`; compare `ORDER` with `audit/run_all_scripts.py` `SCRIPTS` | 60 scripts in both, no duplicates, every file exists; `run_all` adds only `manifest.py`. Stage minutes: 6/147/40/101/226/60/745/9, total 1334 |
| 6 | `pipeline.py --list` runs | `python colab/pipeline.py --list` in the scratch clone | OK |
| 7 | Reviewer links | `grep` of the colab URLs in `REVIEWER_START_HERE.md` and `README.md` at `325bd05` and `9212441`; `curl -s -o /dev/null -w '%{http_code}'` on the raw.githubusercontent.com equivalent | `325bd05`: 12 links (6 per document), all to `blob/6f8ac71…/notebooks/0N_*.ipynb`, all **404** (unpushed). `9212441`: 6 distinct links to `blob/23bfd45…/notebooks/…`, all **200**. All 13 `colab/*.ipynb` at `23bfd45`: 200. Commit `95c840c` page: 200. `b7f50c0` and branch `review/match-figure-2026-10-20`: 404. Repository root: 200 (public). `git ls-remote`: `review/corrections-impl-2026-10-19` = `9212441` |
| 8 | Notebook 12 assertions against the committed certificate outputs | `grep` of `audit/certificates/*_out.txt` | consistent: `{'all': 13, 'chem': 16}`, by-Δ dictionary, SDD/ISDD 9/10, two "OK for every order" |
| 9 | Hard-coded local paths | `grep -rnE '/home/|mpcrlab|FAU|/Users/' notebooks/ colab/ audit/run_all_scripts.py …` | none in notebooks, generators, pipeline or docs. Present only in the committed lab logs (`verification_logs/lab_09ceba8/notebooks/*.ipynb`, `run_all_scripts_rerun.log`: `/home/mpcrlab/LOYOLA-PAPER`, uv Python path). No token-like string |
| 10 | Cross-check evidence age | `git log eed7d03..b7f50c0 -- <inputs>` | the permutation audit output (eed7d03) predates a change to `external/baselines.py` (3af7f67), which it imports. The cross-check output records commit 01ad6c6 |
| 11 | Observed runtimes | `grep` of the per-script times in `verification_logs/lab_09ceba8/*` | match the `pipeline.py` lab minutes. Notebook 05 permutation cell took 2855 s; notebook 06 verifier took 1222 s |

Not run: any notebook, any pipeline stage, `verify.py`, the NIST download, the two cross-checks, Lean, TeX.

## 2. Findings

### Defects (documentation or code)

1. **`notebooks/` setup does not provide Python 3.13 on Colab** (`notebooks/gen_notebooks.py:41-42`). It
   pip-installs both lock files into the kernel's own Python, whatever Colab ships. That replaces Colab's
   numpy, pandas, `ipykernel==7.4.0` and `jupyter_client==8.10.0` inside the running kernel. Packages
   imported before the install can stay at the old version until a restart, and google-colab's own pins
   may conflict. The `colab/` setup handles this correctly: `uv venv --python 3.13`, an exact-version
   check, then `uv pip check` (`colab/make_notebooks.py:128-136`). The guide's "scripts were run on Python
   3.13" holds for `colab/` only. NOT TESTED in Colab.
2. **Notebook 06 builds its verifier venv with `venv.create(env, with_pip=True)` from Colab's Python**
   (`notebooks/gen_notebooks.py:346-351`). This depends on `ensurepip` being available in the Colab image,
   which this audit did not establish. Older Colab images lacked it. The venv is not Python 3.13 either.
   If it fails, use the uv cell of `08_COLAB_START_HERE.md` step 6b.
3. **README.md:89 is false.** It says "The notebooks are committed with their outputs from a local run".
   All 19 notebooks at `6f8ac71` (and at `23bfd45`) have 0 outputs. The executed lab copies are
   under `verification_logs/lab_09ceba8/notebooks/` and belong to commit 09ceba8.
4. **colab/README.md:92-93 contradicts the runner.** It says "every stage downloads them into the Colab copy
   of the repository". The runner never downloads (`colab/pipeline.py` docstring and `run_stage`). Only
   notebook 01's explicit cell downloads, into the private cache, and stages 1, 4 and 8 copy from there.
5. **No private-repository access in `colab/12` and in `notebooks/01-06`.** `colab/make_notebooks.py:203`
   clones without a token or bundle, and `notebooks/gen_notebooks.py:38` likewise. Yet colab/README.md:26
   says notebook 12 "needs no setup beyond a Colab session". This does not matter while the repository
   is public. It breaks if remediation option 1 (make the repository private,
   `audit/VERIFICATION_AND_NIST_STATUS.md`) is taken.
6. **REVIEWER_START_HERE.md:11-13 overstates `notebooks/` setup behaviour.** "An existing checkout is moved
   to it if it is clean" is true only for `colab/` (`at_pin`). The `notebooks/` setup clones and checks out
   only when `LOYOLA-PAPER` is absent. Otherwise it stops with `REVISION MISMATCH`. That is safe, but not
   what the guide says.
7. **Runtime statements disagree** (all of them are estimates):
   - `notebooks/06`: about 35 min (REVIEWER_START_HERE.md:56), about 7 min (README.md:87), 6+1 min (notebook text). Observed: 1222 s.
   - `notebooks/05`: about 5 min (both docs). Observed permutation cell: 2855 s, throttled.
   - `notebooks/05` `RUN_SLOW`: about 1 h (README.md:86) against 1 h + 3.5 h (guide:55, notebook).
   - `notebooks/03`: under a minute (README.md:84), 1–5 min (guide:53).
   - `colab/12`: about 2 min (make_notebooks.py:316), 1 min (colab/README.md:24), about a minute (README.md:71).
   - `selection_resampling.py`: about 30 min (REPRODUCE.md:39), 145 lab min (pipeline), 3.5 h (notebook 05), 1724 s "on the author's machine" (NOTE.md).
   - Full replay: about 25 h (REPRODUCE.md:36) against a 1334-minute (22.2 h) plan sum.
8. **The cross-check evidence is not at the pin.** `audit/permutation_pipeline_audit_out.txt` was last
   written at eed7d03, before `external/baselines.py` changed in 3af7f67. The crosscheck output records
   01ad6c6. Neither has been rerun at `b7f50c0` or `95c840c`. The `NOT_REPLAYED` notes in the docs are
   accurate about this ("must be rerun on their own before claiming that they reproduce").

### Consistency and security observations (no defect)

- Token handling in `colab/` (`colab/make_notebooks.py:25-62, 93-121`): the token travels only in
  `GIT_CONFIG_VALUE_0` in a per-process environment, as an HTTP extraHeader. It is redacted (raw and base64)
  from error text, and the variables are cleared in `finally`. It is not written to `.git/config`, the URL or
  argv. The notebooks contain no stored outputs, so no secret can leak through committed notebooks.
  Residual risk: a user who prints `os.environ` or runs `!env` in that session will not see it, because
  it is never put in `os.environ`. OK.
- NIST pages: downloaded only by the explicit notebook-01 cell, at most one request per second
  (`external/nist_pages.py`), into `MyDrive/LOYOLA_nist_pages_private`. The repository copies are
  git-ignored. `run_script` excludes `NIST_DIRS` from the saved outputs, so the pages never reach the state
  folder or `FINAL_REPORT.md`. Changed pages are written as `*.changed` and stop the run. OK. The
  user must not share the private Drive folder.
- `notebooks/` never touches NIST pages. Notebook 06 runs `--offline`, so the NIST checks print NOT RUN by design.
- Resumability: per-script records with fingerprints. A stage run out of order shows up as STALE, not as a
  false OK. Pipeline order is not enforced, only detected.
- Notebook 11 can only say COMPLETE if notebook 07 is run and no output differs. Four outputs already
  differed on a Linux lab replay (`SEEN_BEFORE`), so on Colab (Linux) expect `k outputs differ` with k ≤ 4, and
  a RuntimeError from the cell. That is accurately documented but easy to misread as a failure.
- Running two `colab/` notebooks in one runtime can trip `at_pin` ("has local changes to tracked files")
  when an earlier stage rewrote an output with different bytes. The message tells the user to delete the
  folder, which is safe. Advise one runtime per notebook.
- Branch-name badges (`blob/review/...`): whether Colab resolves branch names containing `/` was not
  tested. The commit-SHA links in the docs avoid this.

## 3. Failure actions

| Symptom | Action |
|---|---|
| Link opens "Notebook not found" / 404 | chain A is not pushed. Push the branch, or use the chain B links |
| `REVISION MISMATCH` (`notebooks/`) | Runtime > Disconnect and delete runtime, then reopen the link. Never set `LOYOLA_ALLOW_MISMATCH=1` for evidence |
| `cannot check out the pinned commit` / clone failed | the branch does not contain the PIN, or the repository is private: see 08 §5 |
| `the environment does not match the lock files: …` (`colab/`) | rerun the setup cell once. If it repeats, save the message: it names the package and version |
| first cell prints numpy ≠ 2.4.4 (`notebooks/`) | Runtime > Restart session, then Run all. Record the Python version |
| notebook 06 venv / ensurepip error | use the uv cell (08 §2, step 6b) |
| `This stage reads the NIST WebBook pages…` | run notebook 01's NIST cell, then the stage again |
| NIST `CHANGED since archived` | stop. Do not use `--accept-changed`. Report the page names |
| `PROBLEM (see …log)` in a stage | open `MyDrive/LOYOLA_colab_run/logs/<script>.log`. After fixing the cause, reopen the notebook (finished scripts are skipped) |
| notebook 11 `DIFFERS` outside the known files | `git diff --no-index` the committed file against `files/<path>` in the state folder |
| session dies in notebook 07 | reopen. The unfinished script restarts from its beginning (about 4 h): use Colab Pro or a local machine |

## 4. What the user should execute manually next in Colab (short list)

1. Push `review/match-figure-2026-10-20` (it holds `b7f50c0`, `6f8ac71` and `325bd05`). Then confirm in a
   private window that
   `https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/6f8ac717209fc414b6fa1747d9f3b5d165ecd4eb/notebooks/01_data.ipynb`
   opens. Until then, test with the `23bfd45` links (they run `95c840c`).
2. In a fresh Colab runtime run `!python --version`, and record it.
3. Tier 1: `notebooks/01`–`05` (Run all, default `RUN_SLOW=False`). Record the first-cell version line
   and the final `N checks, 0 mismatches` of each.
4. `notebooks/06`. If the venv cell fails, run the uv-based offline verifier (08 §2, step 6b) and record
   the `ALL PASS (fast path, offline: …)` line and the elapsed time.
5. `colab/12_enumeration_certificates.ipynb` → `ALL CERTIFICATES REPRODUCED`.
6. `colab/00_setup_and_plan.ipynb` only: confirm that the setup cell prints `python 3.13.x | numpy 2.4.4 |
   scipy 1.17.1` and the pinned commit. This is the single test of uv's Python 3.13 provisioning on Colab.
7. Optional, author reproduction: `colab/01` (NIST cell) → `02` … `06` → `08` → `11`, then the two cross-checks
   (08 §3). Download `FINAL_REPORT.md` and the two cross-check outputs, then record the commit and wall
   times in a new status file. Do not start `colab/07` or `verify.py --everything` without approval.


---
## Integration note (2026-10-20)

Fixed in the candidate after this audit: README notebook-output statement, colab/README NIST download statement, reviewer-guide description of an existing checkout and of the Python used by notebooks/. Still open (test in real Colab before changing code): notebooks/ installs the locked versions into Colab's own Python; notebook 06 venv with ensurepip. Links: the candidate's notebook commit is re-pinned at the end of this review; see 11_VERIFICATION_AND_RELEASE_MATRIX.md for the final commits.
