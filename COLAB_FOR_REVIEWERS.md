# Checking the paper in Google Colab

**Status: NOT TESTED IN REAL COLAB.** The steps below follow the notebook code and local runs; no run in
Google Colab has been recorded for this commit. Times are estimates. Full detail:
`docs/match/08_COLAB_START_HERE.md` (click-by-click), `docs/match/09_COLAB_RUN_MATRIX.md` (what each
notebook checks), `docs/match/10_COLAB_REPRODUCIBILITY_TEST.md` (what was and was not tested).

Pinned code commit: `c48bad05f8e95805d4f0f700f5324d1071b903cd` (branch `review/match-figure-2026-10-20`).
The links open the notebooks of commit `afafe6c44bd66e0d90e7b5e723010e41e1236ec2`, whose `PIN` is that code
commit. **The links work only once that branch is on GitHub.** Open each notebook in a fresh runtime
(a new tab), choose Runtime > Run all, and check the last line.

## Google Drive

* The essential notebooks (below) need no Drive. At the end of each run they offer to save the result table
  (CSV and a JSON record with commit, Python and package versions, checks and mismatches) to
  `MyDrive/LOYOLA_colab_checks/<commit>/`. Colab shows "Permit this notebook to access your Google Drive
  files?": click **Connect to Google Drive**, choose the account, **Allow**. Declining only skips the save.
  To switch it off, run `import os; os.environ["LOYOLA_SAVE_TO_DRIVE"] = "0"` first.
* The full-reproduction notebooks (`colab/`) require Drive: progress in `MyDrive/LOYOLA_colab_run`, the
  private NIST page cache in `MyDrive/LOYOLA_nist_pages_private` (never share this folder).
* Access lasts for the runtime session only; Colab asks again in each new session.

## RUN THESE FIRST: essential reviewer verification (about 1 to 1.5 h in total; no NIST pages, no Drive)

| # | Notebook | Checks | Pass when the last line reads |
|---|---|---|---|
| 1 | [notebooks/01_data](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/afafe6c44bd66e0d90e7b5e723010e41e1236ec2/notebooks/01_data.ipynb) | datasets, `DATA/` copies, provenance counts | `... checks, 0 mismatches` |
| 2 | [notebooks/02_mathematics](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/afafe6c44bd66e0d90e7b5e723010e41e1236ec2/notebooks/02_mathematics.ipynb) | Lemma 1, the order-13 and order-16 collision trees, Example 2, certificates | `... checks, 0 mismatches` |
| 3 | [notebooks/03_degeneracy](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/afafe6c44bd66e0d90e7b5e723010e41e1236ec2/notebooks/03_degeneracy.ipynb) | Table 2, Figure 1 values, degeneracy counts by full tree enumeration | `... checks, 0 mismatches` |
| 4 | [notebooks/04_octane_correlations](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/afafe6c44bd66e0d90e7b5e723010e41e1236ec2/notebooks/04_octane_correlations.ipynb) | all 60 correlations of Table 4, tetramethylbutane audit | `... checks, 0 mismatches` |
| 5 | [notebooks/05_boiling_points](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/afafe6c44bd66e0d90e7b5e723010e41e1236ec2/notebooks/05_boiling_points.ipynb) — keep `RUN_SLOW = False` | Table 5 baselines, 200-permutation check | `... checks, 0 mismatches` (the permutation cell can take up to about 50 min) |
| 6 | [notebooks/06_verification_suite](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/afafe6c44bd66e0d90e7b5e723010e41e1236ec2/notebooks/06_verification_suite.ipynb) | the repository's fast verifier, offline | `ALL PASS (fast path, offline: ...)` then `... checks, 0 mismatches` |
| 7 | [colab/12_enumeration_certificates](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/afafe6c44bd66e0d90e7b5e723010e41e1236ec2/colab/12_enumeration_certificates.ipynb) | minimal orders 13 and 16 with code independent of the repository's verifiers | `ALL CERTIFICATES REPRODUCED` |

Stop and report if a notebook prints `REVISION MISMATCH`, `MISMATCH`, `FAILURES`, `INCOMPLETE` or raises an
error. First cell of each notebook: record the printed Python version and commit. Known risks to watch
(untested): the `notebooks/` setup installs the locked package versions into Colab's own Python (not 3.13);
if notebook 6 fails to build its environment (`ensurepip`), use the offline-verifier cells of
`docs/match/08_COLAB_START_HERE.md`, step 6b, which build a Python 3.13 environment with `uv`.

What these steps establish: every value they check is recomputed from the committed data or re-executed
from the scripts at the pinned commit and compared with the paper. They do not rebuild the data sets from
the NIST source pages and do not rerun the long experiments.

## RUN THESE ONLY IF YOU WANT FULL REPRODUCTION (authors; hours; needs Google Drive and the NIST pages)

1. `colab/00_setup_and_plan` — prints the plan and builds the Python 3.13 environment.
2. `colab/01_build_datasets` — downloads the 262 NIST WebBook pages once, one request per second, into a
   **private** Drive folder, checks each against its recorded digest, and rebuilds the data sets. A changed
   page is reported as source drift, not accepted.
3. `colab/02` (about 2.5 h), `03` (40 min), `04` (1.7 h, reads the private NIST cache), `05` (3.8 h),
   `06` (1 h), `08` (10 min, reads the cache) — in this order; each resumes from Drive after a disconnect.
4. Optional: `colab/09` (Lean, downloads several GB), `colab/10` (compiles the PDFs).
5. `colab/11_final_report` — validates every recorded stage; it says COMPLETE only if every script of the
   plan ran at this commit and every output matches. Without stage 7 it lists those scripts as NOT RUN and
   ends with an error: that is expected, not a failure of the checks that ran.
6. Optional, very long: `colab/07_long_audits` (about 12 h of lab time; not suitable for a free Colab session).
7. Separately (outside the plan, after notebook 11): `audit/permutation_pipeline_audit.py` (about 30 to 60 min)
   and `audit/v4030/uncertain_source_crosscheck.py`; both need only `requirements-extras-lock.txt`.

Never put the NIST pages in a public notebook output, a shared folder or the repository.
