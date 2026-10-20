# Colab start here (draft, 2026-10-20)

Status of this draft: written from a static audit only. No step below has been run in Google Colab by
the author of this draft. Expected outputs come from the notebook code and from local lab runs at older
commits (listed in `09_COLAB_RUN_MATRIX.md`). Treat every runtime as an estimate.

## 0. Which commit do the links run?

There are two pin chains. Use the one whose branch is on GitHub.

| Chain | Code commit (PIN) | Notebook commit (links) | Branch | On public GitHub now? |
|---|---|---|---|---|
| A, figure moved into the main paper (current) | `5d5d16abe45e0cccd182209b2b7c9048eccbb289` | `0a36902e5b6ed7a56b0534641cb12431616c2066` | `review/match-figure-2026-10-20` | **No.** Local only. All links 404 until the branch is pushed |
| B, previous review state | `95c840c857d00413e6a3bf7b83989216d5c79b14` | `23bfd45baecc1335f2bc075c02743ab2905b60cf` | `review/corrections-impl-2026-10-19` (head `9212441`) | Yes. Every link checked returns HTTP 200 |

In the links below, `<NB_COMMIT>` stands for the notebook commit. For chain A it is
`0a36902e5b6ed7a56b0534641cb12431616c2066`, and the links work only after
`review/match-figure-2026-10-20` is pushed. For chain B it is `23bfd45baecc1335f2bc075c02743ab2905b60cf`,
which works now but runs the code from before the figure move.

Link pattern (open in a browser that is signed in to Google):

```
https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/<NB_COMMIT>/notebooks/01_data.ipynb
https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/<NB_COMMIT>/colab/00_setup_and_plan.ipynb
```

Chain B links that work today (checked with `curl` on raw.githubusercontent.com, HTTP 200):

- https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/23bfd45baecc1335f2bc075c02743ab2905b60cf/notebooks/01_data.ipynb
- https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/23bfd45baecc1335f2bc075c02743ab2905b60cf/notebooks/02_mathematics.ipynb
- https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/23bfd45baecc1335f2bc075c02743ab2905b60cf/notebooks/03_degeneracy.ipynb
- https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/23bfd45baecc1335f2bc075c02743ab2905b60cf/notebooks/04_octane_correlations.ipynb
- https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/23bfd45baecc1335f2bc075c02743ab2905b60cf/notebooks/05_boiling_points.ipynb
- https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/23bfd45baecc1335f2bc075c02743ab2905b60cf/notebooks/06_verification_suite.ipynb
- https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/23bfd45baecc1335f2bc075c02743ab2905b60cf/colab/12_enumeration_certificates.ipynb
- `colab/00` to `colab/11`: same pattern, `.../blob/23bfd45baecc1335f2bc075c02743ab2905b60cf/colab/<name>.ipynb`
  (all 13 return 200).

The Colab badge inside each notebook opens the branch copy (`blob/<branch>/...`), not the commit. For
chain A those badges also 404 until the branch is pushed. The branch names contain `/`. Whether Colab's
GitHub loader resolves such branch URLs was not tested. The commit-SHA links above avoid the question.

What actually runs is decided by `PIN` inside the notebook, not by the link. Every notebook at
`0a36902` has `PIN = 5d5d16a…`, and every notebook at `23bfd45` has `PIN = 95c840c…` (checked with
`git show`).

## 1. Before you start (all tiers)

1. Use a Google account with Colab access and a desktop browser. Keep the tab open while a notebook runs.
   Free Colab disconnects idle sessions and caps session length.
2. Is the repository public? Open https://github.com/Singati2/LOYOLA-PAPER in a private window. It
   returned HTTP 200 on 2026-10-20.
   - If it is public, no token is needed.
   - If it is private, see section 5 first.
3. Python version. Colab's default Python is whatever the current runtime image ships (3.12 as of 2025,
   to this draft's knowledge; not checked today). The repository was run on Python 3.13. How each
   notebook family deals with that:
   - `colab/00`–`11`: the setup cell installs `uv` and creates `/content/loyola-env` with
     `uv venv --python 3.13`. uv downloads a standalone CPython 3.13 if none is present. Every script runs
     with that 3.13 interpreter, with the exact locked versions. The cell stops if a locked package is at
     another version, or if `uv pip check` fails. The notebook kernel itself stays on Colab's Python.
   - `colab/12`: runs on Colab's own Python and installs only `networkx==3.6.1`. Exact rational
     arithmetic makes this safe.
   - `notebooks/01`–`06`: **no Python 3.13 provisioning.** The setup cell runs
     `pip install -r requirements-lock.txt -r requirements-extras-lock.txt` into Colab's own Python.
     That replaces Colab's numpy, pandas, ipykernel and jupyter_client. Notebook 06 then builds
     `.venv-verify` with `venv.create(..., with_pip=True)` from that same Colab Python. The first cell
     prints the Python version that is actually used. Record it.

## 2. Tier 1: reviewer smoke test (about 1 to 1.5 h of wall time in total; estimate)

Goal: every number checked by the fast notebooks matches the paper, and the independent certificates
reproduce. No NIST download, no Drive.

Order. Open each notebook in its own tab, so that each gets a fresh runtime.

| Step | Open | Do | Expected last lines | Stop if |
|---|---|---|---|---|
| 1 | `notebooks/01_data.ipynb` | Runtime > Run all | first cell: `commit <PIN>; pinned commit <PIN>`, then `python 3.x.y \| numpy 2.4.4 \| scipy 1.17.1 \| networkx 3.6.1 \| mpmath 1.3.0`. Then `OK ...` lines, and finally `9 checks, 0 mismatches` (count seen at the lab run of 09ceba8) | `REVISION MISMATCH`, any `MISMATCH` line, or a numpy/scipy version other than the locked one (restart the runtime and Run all again once) |
| 2 | `notebooks/02_mathematics.ipynb` | Run all | `20 checks, 0 mismatches` (lab, 09ceba8) | any `MISMATCH` |
| 3 | `notebooks/03_degeneracy.ipynb` | Run all (a few minutes: enumerates every tree up to order 17) | `25 checks, 0 mismatches` (lab) | any `MISMATCH` |
| 4 | `notebooks/04_octane_correlations.ipynb` | Run all | `69 checks, 0 mismatches` (lab) | any `MISMATCH` |
| 5 | `notebooks/05_boiling_points.ipynb` | keep `RUN_SLOW = False`, Run all | `27 checks, 0 mismatches` (lab). The 200-permutation cell is the slow part. Docs say "about 5 min", but the lab run took 2855 s on a throttled CPU | any `MISMATCH`; the permutation cell running for more than 90 min |
| 6a | `notebooks/06_verification_suite.ipynb` | Run all | a cell that prints `ALL PASS (fast path, offline: the checks that read the NIST WebBook pages were NOT RUN)`, then `3 checks, 0 mismatches` | the venv cell fails with an `ensurepip` error (see 6b); `FAILURES` or `INCOMPLETE` |
| 6b | alternative to 6a: in a fresh Colab tab, run the offline verifier by hand (cells below) | | same `ALL PASS (fast path, offline: ...)` line | any `[FAIL]` line |
| 7 | `colab/12_enumeration_certificates.ipynb` | Run all (about 1 to 2 min plus install) | `minimal.py -> {'all': 13, 'chem': 16}`, `by_delta.py -> ...`, `ratio_indices.py -> ...`, `witnesses.py -> ...`, then `ALL CERTIFICATES REPRODUCED` | an `AssertionError` |

Step 6b, the offline verifier without notebook 06. Paste each block into its own cell of a new notebook.
Replace `<PIN>` and `<BRANCH>` with the chain's code commit and branch.

```python
!git clone --quiet --branch <BRANCH> https://github.com/Singati2/LOYOLA-PAPER.git /content/LP
%cd /content/LP
!git checkout --quiet --detach <PIN> && git rev-parse HEAD && git status --porcelain --untracked-files=no
```
```python
!pip install --quiet uv && uv venv --quiet --python 3.13 /content/v313
!uv pip install --quiet --python /content/v313/bin/python -r requirements-lock.txt
!/content/v313/bin/python verify.py --offline 2>&1 | tail -40
```

This uses Python 3.13 and only the core lock, as CI does. Expected last line:
`ALL PASS (fast path, offline: the checks that read the NIST WebBook pages were NOT RUN)`. Lab and clean-clone
runs took 20 to 35 min.

Tier 1 passes when steps 1–5, 6a or 6b, and 7 all end as above.

## 3. Tier 2: author reproduction (staged replay; about 9.8 h of lab-measured script time without notebook 07, plus setup and download; estimate)

Goal: rerun every script of the `colab/pipeline.py` plan from the NIST source pages, and compare every
rewritten output with the commit. Each notebook runs in its own Colab session. Progress lives in
`MyDrive/LOYOLA_colab_run`, so a disconnect loses at most the script that was running.

Each `colab/` notebook has the same setup cell. It mounts Drive (approve the pop-up), clones the branch,
checks out `PIN`, builds the Python 3.13 environment and prints:

```
python 3.13.x | numpy 2.4.4 | scipy 1.17.1
commit <PIN> | lock files <12 hex>
```

If it raises `... has local changes to tracked files; delete that folder and run this cell again`, run
`!rm -rf /content/LOYOLA-PAPER` and rerun the cell. The state on Drive is not affected. This happens when
a second notebook is run in the same runtime after an earlier stage rewrote an output with different bytes.

Order. The stages read each other's outputs, so this order is required:

| # | Notebook | Cells | Needs NIST pages | Lab time (estimate) | Expected end |
|---|---|---|---|---|---|
| 1 | `colab/00_setup_and_plan.ipynb` | Run all | no | 2 min | the stage list, total about 1334 lab minutes |
| 2 | `colab/01_build_datasets.ipynb` | Run all. The NIST cell retrieves 262 pages, one per second, into `MyDrive/LOYOLA_nist_pages_private` | **yes, downloads them** | 5 min + about 5 min download | `262 NIST WebBook pages: 262 present and identical ...`, then `Stage 1 finished: every script exited 0` |
| 3 | `colab/02_mathematics_and_trees.ipynb` | Run all | no | 2.5 h (`structural_checks.py` 128 min) | `Stage 2 finished: every script exited 0` |
| 4 | `colab/03_octane_analyses.ipynb` | Run all | no | 40 min | `Stage 3 finished: ...` |
| 5 | `colab/04_nonane_vaporisation_enthalpies.ipynb` | Run all | **yes, copied from the private cache** | 1.7 h | `Stage 4 finished: ...` |
| 6 | `colab/05_boiling_points.ipynb` | Run all | no | 3.8 h (`selection_resampling.py` 145 min, `bp_tests.py` 78 min) | `Stage 5 finished: ...` |
| 7 | `colab/06_independent_audits.ipynb` | Run all | no | 1 h | `Stage 6 finished: ...` |
| 8 | `colab/08_consistency_checks.ipynb` | Run all | **yes, copied from the cache** | 10 min | `Stage 8 finished: ...` |
| 9 | `colab/09_lean_proofs.ipynb` (optional) | Run all | no | 10–30 min (downloads Mathlib, several GB) | `formal/verify.sh` output ending without `FAIL`; log saved as `lean_verify.log` in the state folder |
| 10 | `colab/10_compile_paper.ipynb` (optional) | Run all | no | about 10 min (TeX Live install) | `main exit 0 \| ...`, `supplement exit 0 \| ...`, label check passes. The PDFs are not compared by bytes |
| 11 | `colab/11_final_report.ipynb` | Run all | no | 2 min | see below |
| 12 | `colab/12_enumeration_certificates.ipynb` | Run all | no | 1–2 min | `ALL CERTIFICATES REPRODUCED` |

If a stage's NIST check fails, the runner prints
`This stage reads the NIST WebBook pages. Run the download cell of notebook 01 first ...`.
Rerun notebook 01's NIST cell, then the stage.

**What notebook 11 will say in Tier 2.** Notebook 07 is skipped in this tier, so its three scripts are
`NOT RUN`. The verdict line is then
`**Result: 57 scripts OK, 0 PROBLEM, 0 STALE, 3 NOT RUN; k outputs differ.**`, and the cell ends with
`RuntimeError: pipeline.py --report reported a problem`. That error is expected in Tier 2. The report is
still displayed and saved. A Tier 2 pass is:

- 57 OK, 0 PROBLEM, 0 STALE, and NOT RUN only for the 3 stage-7 scripts;
- every `DIFFERS` line names a file that is flagged in the report as having differed on the lab replay
  (`external/transfer_exploratory_out.txt`, `external/wide_box_diagnostics_out.txt`,
  `audit/final/scripts/counterattack_v4030_out.txt`). Any other `DIFFERS` file is a real discrepancy. Diff
  it against the commit: the state folder's `files/` keeps the copy.

Running a stage out of order is not blocked. It shows up in the report as `STALE` for the later scripts.
Fix it by rerunning those stages in order. `--redo` is not needed; reopening the notebook is enough.

### The two cross-checks outside the plan (run separately)

Neither replay runs them (`NOT_REPLAYED` in `colab/pipeline.py` and `audit/run_all_scripts.py`). Both need
`requirements-extras-lock.txt` (scikit-learn, pandas), which the `colab/` environment already has. Neither
needs the NIST pages or any stage output: they read committed files (`external/bp/bp_data.csv`,
`structural/structural_checks_out.txt`, `audit/final/scripts/claim_provenance_ledger.csv`). Both rewrite
their committed `*_out.txt` in place, so run them **after** notebook 11, in a fresh runtime. Add these
cells after the setup cell of any `colab/` notebook, for example a copy of `11_final_report.ipynb`:

```python
r = subprocess.run([PY, "audit/permutation_pipeline_audit.py"], capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-1500:], "exit", r.returncode)
print(subprocess.run(["git", "diff", "--stat", "--", "audit/permutation_pipeline_audit_out.txt"], capture_output=True, text=True).stdout or "output identical to the commit")
```
```python
r = subprocess.run([PY, "audit/v4030/uncertain_source_crosscheck.py"], capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-1500:], "exit", r.returncode)
print(subprocess.run(["git", "diff", "--", "audit/v4030/uncertain_source_crosscheck_out.txt"], capture_output=True, text=True).stdout or "output identical to the commit")
```

Expected:
- permutation audit: exit 0, last line `RESULT: independent re-implementation reproduces the paper pipeline`,
  with `Q2 0.8599, median -0.0882, 95th pct -0.0087, max 0.1952`. It takes 30–60 min on a lab machine
  (`n_jobs=-1`), longer on 2 free-Colab vCPUs (estimate).
- uncertain-source cross-check: exit 0. The only expected diff is the `commit ...` line, because the
  committed file records commit `01ad6c6`. Every Q2 line must be unchanged.

Save both outputs in the state folder, for example by copying them to `STATE`.

## 4. Tier 3: optional exhaustive (only with the authors' approval)

- `colab/07_long_audits.ipynb`: three scripts of about 4 h each on the lab machine (`press_size_probe.py`
  245 min, `refit_stability.py` 245, `sensitivity_followup.py` 255; 12.4 h in total). Each script has to
  finish inside one session. That is unreliable on free Colab: use Colab Pro or a local machine. After it,
  rerun notebook 11. COMPLETE is reached only if nothing differs. `press_size_probe_out.txt` and the files
  above already differed on the lab Linux replay, so a COMPLETE verdict on Linux is not expected.
- `python verify.py --everything`: not a Colab job (about 10 h at the lab, needs `tectonic` and `lake`).
  Run it locally, never at the same time as another long job.

## 5. If the repository is private

- `colab/00`–`11`: add a Colab secret `GITHUB_TOKEN` (key icon in the left bar; a fine-grained token with
  read-only Contents access to `Singati2/LOYOLA-PAPER`), and turn on notebook access. Alternatively, put
  `LOYOLA-PAPER.bundle` (`git bundle create LOYOLA-PAPER.bundle --all`) at the top of MyDrive. The token
  is passed to git as an HTTP header, through the environment of that one git process, and its value is
  removed from error messages.
- To open a notebook from a private repository, Colab itself needs GitHub authorisation (File > Open
  notebook > GitHub > "Include private repos").
- `colab/12` and `notebooks/01`–`06` **have no token or bundle support**: their clone fails while the
  repository is private. Workaround: before Run all, insert this cell at the top, run it, then run the
  rest:

```python
import base64, os, subprocess
from google.colab import userdata
tok = userdata.get("GITHUB_TOKEN")
env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="http.extraHeader",
           GIT_CONFIG_VALUE_0="Authorization: Basic " + base64.b64encode(("x-access-token:" + tok).encode()).decode())
r = subprocess.run(["git", "clone", "--quiet", "--branch", "<BRANCH>", "https://github.com/Singati2/LOYOLA-PAPER.git",
                    "/content/LOYOLA-PAPER"], env=env, capture_output=True, text=True)
print("clone exit", r.returncode); del tok, env
subprocess.run(["git", "-C", "/content/LOYOLA-PAPER", "checkout", "--quiet", "--detach", "<PIN>"], check=True)
```

  The `notebooks/` setup cell then finds `LOYOLA-PAPER` and checks the PIN. For `colab/12`, `cd` into
  `/content` first. Do not print `r.stderr` unredacted.

## 6. Decision tree

```
Is the chain's branch on GitHub (link returns a notebook, not 404)?
 ├─ no  → chain A not pushed: push review/match-figure-2026-10-20 first, or use chain B (runs 95c840c)
 └─ yes → Is the repository public?
          ├─ no  → section 5, then continue
          └─ yes → Tier 1, steps 1-7
                   ├─ setup error "REVISION MISMATCH" → Runtime > Disconnect and delete runtime; reopen the link
                   ├─ numpy/scipy version not locked in the first cell → Runtime > Restart session; Run all again
                   ├─ notebook 06 venv/ensurepip error → step 6b
                   ├─ any MISMATCH / FAILURES / AssertionError → stop; save the notebook (File > Download .ipynb);
                   │    report the commit, the cell and the full output (section "Reporting" of REVIEWER_START_HERE.md)
                   └─ all pass → Tier 1 done.  Author reproduction needed?
                                 ├─ no  → stop
                                 └─ yes → Tier 2 (00, 01 with NIST, 02-06, 08, [09, 10], 11, 12; then the two cross-checks)
                                          ├─ PROBLEM in a stage → open its log in MyDrive/LOYOLA_colab_run/logs/, fix, rerun that notebook
                                          ├─ 11 shows DIFFERS outside the three known files → diff files/<path> against the commit
                                          └─ 57 OK + 3 NOT RUN (stage 7) → Tier 2 done; Tier 3 only with approval
```


---
## Integration note (2026-10-20)

Fixed in the candidate after this audit: README notebook-output statement, colab/README NIST download statement, reviewer-guide description of an existing checkout and of the Python used by notebooks/. Still open (test in real Colab before changing code): notebooks/ installs the locked versions into Colab's own Python; notebook 06 venv with ensurepip. Links: the candidate's notebook commit is re-pinned at the end of this review; see 11_VERIFICATION_AND_RELEASE_MATRIX.md for the final commits.
