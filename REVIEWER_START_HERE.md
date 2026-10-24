# Reviewer start here

This repository holds the paper "The Loyola Index Family and the Resolution Limit of Degree Imbalance"
(`main.tex`, `supplement.tex`, compiled as `LOYOLA_paper.pdf` and `LOYOLA_supplement.pdf`), its data,
code, tests, notebooks and Lean proofs. Everything stays in one repository.

**Pinned commit.** The code under review is commit `e3fc8810c066420354c96eb8c38a0b9190dfa663` on the branch
`review/match-final-four-fixes-2026-10-23`. Every notebook, in `notebooks/` and in `colab/`, runs exactly that
commit (its `PIN`). The notebooks are committed one step later, in `e90b5bfcb1a46937cb4f20a6b3420007b69caad1`, which changes nothing but
the notebooks; the Colab links below open them from that commit, so a link always runs the pinned code.
(A notebook opened from an older commit carries that commit's older pin.) On Colab the setup cell clones that branch and checks out the
pinned commit. In `colab/`, an existing checkout is moved to it if it is clean and rejected if it has
local changes; in `notebooks/`, an existing checkout of another commit stops with `REVISION MISMATCH`
(start a fresh runtime). The `notebooks/` setup installs the locked versions into Colab's own Python,
which is not 3.13; only the `colab/` setup builds a Python 3.13 environment. Locally, a checkout of another commit, or one with local changes, stops the notebook with
`REVISION MISMATCH` (`notebooks/`; set `LOYOLA_ALLOW_MISMATCH=1` to run anyway, with a printed
warning that the results are not tied to the pinned commit) or with an error naming both commits
(`colab/`). On every run the `colab/` setup installs the locked package versions, so a partly installed
or modified environment is repaired, rebuilds an environment with another Python, and stops unless
every locked package is at its locked version. The notebooks are regenerated, pinned to a commit, by `python notebooks/gen_notebooks.py
--pin <commit>` and `python colab/make_notebooks.py --pin <commit>`. A public tag is a separate,
later step and is not needed by the notebooks.

## Two-minute quick start

```bash
git clone https://github.com/Singati2/LOYOLA-PAPER.git && cd LOYOLA-PAPER
git checkout e3fc8810c066420354c96eb8c38a0b9190dfa663   # the pinned commit
python3 -m venv .venv && . .venv/bin/activate
python -m pip install -r requirements-lock.txt          # exact versions behind the committed outputs
python verify.py --offline                               # fast path, about 6 to 30 minutes
```

The 262 NIST WebBook pages that the data builds read are not redistributed (NIST SRD 69 is
copyrighted). Without them, run `python verify.py --offline`: the checks that read the pages are
reported as NOT RUN, everything else runs. To run those checks too, retrieve the pages first with
`python external/nist_pages.py --download` (about 5 minutes, one request per second); each page is
checked against the digest of the copy the data sets were built from. The last line is
`ALL PASS (fast path)`, `ALL PASS (fast path, offline: ...)`, `INCOMPLETE` or `FAILURES`. The scripts were run on Python 3.13; CI uses
Python 3.13 on Ubuntu.

## Notebooks

Each notebook prints every value of the paper next to its recomputed value. Its last cell fails if
any of them differ. Each step is labelled with one of three kinds:

- **recompute from source**: the value is derived again from the data or from first principles;
- **re-run an experiment**: a repository script is executed;
- **compare against stored output**: a committed result file is checked against the paper.

| Notebook | Covers | Runtime (laptop CPU) | Colab |
|---|---|---|---|
| `01_data.ipynb` | datasets, DATA/ copies, provenance counts (39 agreement, 8 cannot verify) | seconds | [open](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/e90b5bfcb1a46937cb4f20a6b3420007b69caad1/notebooks/01_data.ipynb) |
| `02_mathematics.ipynb` | Lemma 1, the colliding trees of orders 13 and 16, Example 2, certificates | under 1 min | [open](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/e90b5bfcb1a46937cb4f20a6b3420007b69caad1/notebooks/02_mathematics.ipynb) |
| `03_degeneracy.ipynb` | Table 2 and the degeneracy counts, by full tree enumeration | 1 to 5 min | [open](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/e90b5bfcb1a46937cb4f20a6b3420007b69caad1/notebooks/03_degeneracy.ipynb) |
| `04_octane_correlations.ipynb` | all 60 correlations of Table 4; tetramethylbutane audit | seconds | [open](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/e90b5bfcb1a46937cb4f20a6b3420007b69caad1/notebooks/04_octane_correlations.ipynb) |
| `05_boiling_points.ipynb` | Table 5 baselines and the 200-permutation check. `RUN_SLOW = True` regenerates the 50-seed medians (about 1 h) and the resampling (about 3.5 h) | about 5 min | [open](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/e90b5bfcb1a46937cb4f20a6b3420007b69caad1/notebooks/05_boiling_points.ipynb) |
| `06_verification_suite.ipynb` | `verify.py` fast path in a dedicated environment with the pinned versions | about 35 min | [open](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/e90b5bfcb1a46937cb4f20a6b3420007b69caad1/notebooks/06_verification_suite.ipynb) |

On Colab the setup cell clones the branch, checks out the pinned commit and installs
`requirements-lock.txt` and `requirements-extras-lock.txt`. Google Colab is a convenience, not a requirement. The notebooks are
regenerated by `notebooks/gen_notebooks.py`.

## Which script produces which table or figure

| Item | Produced by | Checked by |
|---|---|---|
| Table 1 `tab:collisions` | `redundancy_collisions.py` | `verify_loyola_v35.py` |
| Table 2 `tab:firstfail` | `structural/structural_checks.py` (S1) | `structural_checks.py` |
| Table 3 `tab:fgdss` | `fgd_structure_sensitivity.py` | `verify_loyola_v35.py` |
| Table 4 `tab:lo_octane` | `verify_loyola_v35.py` | `verify_loyola_v35.py` |
| Table 5 `tab:bp` | `external/bp/bp_tests.py`, `make_bp_table.py` | `external/verify_external.py` |
| Table S8 `tab:deviations` (Table 6 before 2026-10-23) | written by hand (protocol deviations) | `audit/check_labels.py` (labels only) |
| Figure 1 (main paper), Figure S1 | `generate_loyola_v35_figures.py` | `verify_loyola_v35.py` (canonical PDF content) |
| Tables S1 to S5 | `verify_loyola_v35.py`, `ablation_gm_vs_lo.py`, `expanded_robustness_v35.py`, `multi_order_degeneracy.py`, `octane_data.py` | `verify_loyola_v35.py` |
| Tables S6, S7 | `external/box_sensitivity.py`, `external/baselines.py`, `external/nonane_validation.py` | `external/verify_external.py` |
| Numbers in the running text | committed outputs | `prose_numbers_check.py` (758 checked, 22 cited values not checkable, at the pinned commit) |

`REPRODUCE.md` has the complete list, including every exploratory script.

## Levels of verification

| Command | What runs | Runtime | Notes |
|---|---|---|---|
| `python verify.py` | core verifier, prose numbers, regression and baseline tests, certificates, manifest | 6 to 35 min | this is the GitHub Actions job (`.github/workflows`); it is the only level CI runs |
| `python verify.py --full` | adds the external verifier, structural checks, 32-digit recount, verifier self-test, counter-attacks on the checkers, labels (needs `tectonic`) and Lean (needs `lake`) | about 1.5 to 2 h | if `tectonic` or `lake` is missing, the stage is printed as `[SKIP]` and the run ends `INCOMPLETE (full) ... SKIPPED: ...`, never `ALL PASS` |
| `python verify.py --everything` | adds `audit/run_all_scripts.py`, which reruns every script of its list in an isolated copy and compares every output; the two independent cross-checks it does not run are named in its output (`NOT_REPLAYED`) and have their own committed outputs | several hours | |
| `formal/verify.sh` | Lean 4 proofs: the 38 listed theorems, and an axiom check on all 52 declarations, axioms limited to propext, Classical.choice and Quot.sound | about 1 min after the first build | the first build downloads and builds Mathlib (several GB of disk) |

What was and was not run at the pinned commit is recorded in `audit/MATCH_FIGURE_2026-10-20.md` (earlier steps: `audit/REVIEW_2026-10-20_STATUS.md`, `audit/CORRECTIONS_2026-10-19_STATUS.md`). Older logs describe their own commits only.

## Data and licences

- **Code and text:** MIT (`LICENSE`).
- **Experimental values:** from the NIST Chemistry WebBook (NIST Standard Reference Database 69), subject to NIST's terms of use. Also from published compilations (NBS Circular 461, 1947; Wilhoit and Zwolinski 1971; Labauf et al. 1961, listed by NIST as Labbauf), and from KDB values as shown on Chemeo (acentric factors). Where a source page was archived, it is in the repository.
- **Redistribution terms of the KDB and Chemeo values have not been established** (see Known unresolved items).
- **Provenance:** every value has a record in `octane_property_provenance_v35.csv`, `external/nonane_provenance.csv` or `external/bp/bp_provenance.csv`. `audit/final/CLAIM_PROVENANCE_LEDGER.md` counts the independent primary determinations behind each value; compilations count as derivative.

## Known unresolved items

These are disclosed, not resolved:

- Seven octane gas-phase entropies match no primary source. The ΔH_vap of 2,2,3,3-tetramethylbutane has an unresolved reference state. Its acentric factor conflicts between compilations (0.247, 0.251, 0.255).
- All 18 acentric factors and 29 of the 34 nonane vaporisation enthalpies appear only in compilations, with no primary determination identified. 57 of the 100 boiling points are direct NIST/TRC averages and one is the mean of two agreeing NIST/TRC averages, 58 in all; the source pages of these averages are not archived.
- One citation's content is unverified: Konstantinova (1996), cited for the concept of degeneracy, is paywalled.
- The novelty statement (no earlier determination of the orders 13 and 16) is an absence claim. The search behind it is in `audit/final/NOVELTY_SEARCH_LOG.md`.
- `press_size` rejects a candidate when a leverage comes within 1e-6 of 1, even if the deleted fit is still defined. Such candidates have PRESS amplified by at least 10^6 and are never selected. The published outputs are byte-identical before and after this guard.
- The redistribution terms of the KDB and Chemeo values are not established.

## Reporting a discrepancy

Open a GitHub issue. Please give:

- the commit (`git rev-parse HEAD`);
- the command or notebook;
- the full output, including the `[PASS]`, `[FAIL]` and `[SKIP]` lines;
- your Python version and `pip freeze`.

For a number in the paper, also quote the sentence or table cell and the file the value should come from.
