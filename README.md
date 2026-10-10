# The Loyola Index Family and the Resolution Limit of Degree Imbalance

Advik Natarajan, Ganesh Shiwakoti, Michael Arockiaraj: manuscript, supplement,
data, code, machine-checked proofs and runnable notebooks.

**v40.27 (2026-10-10):** Propositions 5.6-5.8 state a nonempty edge set; the remark after
Proposition 5.8 no longer calls the comparison sharp (its constants are the best edgewise ones,
and a bound is attained only when every edge attains the extremum).

**v40.26 (2026-10-10):** review fixes: predictive claims in Section 6.4 limited to the models, boxes
and budgets evaluated; the exploratory resampling range no longer compared with the conditional
interval; the one-sided gain rule in `external/bp/bp_tests.py` now requires a positive lower endpoint
(verdicts unchanged); m >= 1 in Proposition 3.17; countable-union step for generic discrimination;
true interval check of the Lemma 3.1 witness; reproduction map and `requirements-extras-lock.txt`.
Known issue, deferred: the relative-range guard of `fold_select_ols` (`external/baselines.py`) is not
translation invariant (a candidate x + 1e13 is rejected). It is recorded as an expected failure in
`external/test_regressions.py`; on the package data correcting it changes no selected fold, and the
rank-guard audit of the boiling-point tests is on the branch `robustness-guards`.

**v40.25 (2026-10-09):** MATCH-style pass: abstract leads with the mathematical results; Section 6
and the conclusion condensed (no number or verdict changed); reference list strictly
alphabetical; three 2027 MATCH papers on the degree-ratio Sombor index cited under Corollary 3.6.

**v40.24 (2026-10-09):** the weak-discrimination theorem (former Theorem 4.3) is withdrawn from
the submission and kept on the branch `research/weak-discrimination`; Example 4.3 is now
checked directly from the trees (`structural/sumconn_pair_check.py`).

**v40.23 (2026-10-09):** restructured in MATCH statement-driven form; collision minimality certified over all tree orders 2–16;
tetramethylbutane ΔH_vap source audit; exploratory selection-aware resampling; independent
permutation audit. Full history in `V35_TO_V36_SCIENTIFIC_CHANGELOG.md`.

## Run the checks yourself (Jupyter or Google Colab)

Each notebook recomputes one part of the paper from the data in `DATA/` and prints the
value in the paper next to the recomputed value; the last cell fails if any differ. On
Colab the notebook clones this repository and installs the requirements itself.

| Notebook | What it checks | Time | Open |
|---|---|---|---|
| `notebooks/01_data.ipynb` | the datasets in `DATA/` and their provenance | seconds | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/main/notebooks/01_data.ipynb) |
| `notebooks/02_mathematics.ipynb` | Lemma 3.1, the colliding profiles of Theorem 3.5, Example 4.3, certificates | under a minute | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/main/notebooks/02_mathematics.ipynb) |
| `notebooks/03_degeneracy.ipynb` | Table 2 and the order-10 and order-16 counts, by enumerating every tree | under a minute | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/main/notebooks/03_degeneracy.ipynb) |
| `notebooks/04_octane_correlations.ipynb` | all 60 correlations of Table 4 and the tetramethylbutane audit | seconds | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/main/notebooks/04_octane_correlations.ipynb) |
| `notebooks/05_boiling_points.ipynb` | Table 5 baselines, the 200-permutation check, the resampling summary | about 5 minutes (`RUN_SLOW = True`: about 1 hour) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/main/notebooks/05_boiling_points.ipynb) |
| `notebooks/06_verification_suite.ipynb` | the repository's own fast verification suite, in an environment with the pinned versions | about 7 minutes | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/main/notebooks/06_verification_suite.ipynb) |

The notebooks are committed with their outputs from a local run. `notebooks/gen_notebooks.py`
regenerates them. The Lean proofs need a Lean toolchain and are not run in a notebook.

## Lean verification

`LEAN_VERIFICATION.md` maps every numbered statement of the paper to the Lean 4 theorems of `formal/` and states what is machine-checked; `cd formal && ./verify.sh` rebuilds and checks the development.

## Current documents
| File | Content |
|---|---|
| `main.tex`, `LOYOLA_paper.pdf` | the paper (38 A5 pages, MATCH template) |
| `supplement.tex`, `LOYOLA_supplement.pdf` | Supplementary Material (26 pages) |
| `DATA/` | every dataset, byte-identical copies, with a README |
| `LOYOLA_FINAL_PAPER_OVERLEAF.zip` | Overleaf upload (both documents + figures) |

## What the paper shows
The Loyola index LO(G; α, β, γ) = Σ_uv (d_u d_v)^α (d_u + d_v)^β exp(γ |d_u − d_v|/(d_u + d_v))
extends the Gutman–Milovanović family (γ = 0).
- **Structure:** a size–shape factorisation; a ratio-plane theorem stating exactly what
  the pure-γ line can discriminate (edge-imbalance histograms), with colliding trees at
  every order ≥ 13; a bound on γ-crossings; per-graph identifiability.
- **Prediction (negative, under the stated protocols):** an apparent vaporization-enthalpy
  gain was an artefact of a search box that truncated the parent family; pre-registered
  tests on measured boiling points (34 decanes; 100 alkanes C6–C10) show no demonstrated
  benefit from γ; ridge regression on the degree-pair counts is far stronger than any
  single index.

## Reproducing everything
See **[REPRODUCE.md](REPRODUCE.md)**: every table, figure, experiment and dataset is
mapped to the script that produces it and the check that verifies it.
Quick start:
```bash
python3 -m pip install -r requirements-lock.txt
# optional, for the scikit-learn audit and the notebooks: -r requirements-extras-lock.txt
python3 verify.py                       # single entry point: all fast checks (--full for the long suites); run by CI on every push
python3 verify_loyola_v35.py            # core tables, figures, analyses
python3 external/verify_external.py     # nonane and boiling-point tests, rebuilt from raw NIST pages
python3 structural/structural_checks.py # structural counts and witnesses
(cd formal && ./verify.sh)              # Lean 4 proofs
python3 manifest.py                     # checksums
```

## Pre-registrations
`external/PREREG_v37.md` (nonane test) and `external/PREREG_v40.md` (boiling-point
tests), each committed before the corresponding models were fitted.

## History
`V35_TO_V36_SCIENTIFIC_CHANGELOG.md` records every revision; earlier
version notes and logs are kept only in the git history.

License: MIT (see `LICENSE`).
