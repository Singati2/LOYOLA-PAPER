# The Loyola Index Family and the Resolution Limit of Degree Imbalance

Advik Natarajan, Ganesh Shiwakoti, Michael Arockiaraj: manuscript, supplement,
data, code, machine-checked proofs and runnable notebooks.

## Revision under review

The revision under review is on the branch `review/match-figure-2026-10-20`, at commit `5d5d16abe45e0cccd182209b2b7c9048eccbb289`,
not on `main`. Start with `REVIEWER_START_HERE.md`. The change notes below stop at v40.29; later changes
are recorded in `audit/V4031_REVISION_REPORT.md`, `audit/CORRECTIONS_2026-10-19_STATUS.md`,
`audit/REVIEW_2026-10-20_STATUS.md` and `audit/MATCH_FIGURE_2026-10-20.md`.

**v40.29 (2026-10-11):** final adversarial review before submission. Reports in `audit/final/`:
data provenance, mathematical referee report (with the novelty assessment), code and statistics audit,
and `MATCH_SUBMISSION_READINESS.md`; independent check scripts in `audit/final/scripts/`. No
mathematical error and no change to any registered result. Code: the selection guard of
`external/baselines.py` now counts resolvable steps instead of a relative-range floor, which repairs
the translation defect deferred in v40.26 (no output changes; the expected failure is now a passing
test), and the rank threshold of `press_size` is 1e-6, which rejects nearly collinear designs whose
closed-form PRESS was inaccurate (smallest ratio on the data 4.6e-4, no output changes). New
exploratory baselines: Wiener's W + p3 model on the decanes (`external/bp/wiener_baseline.py`,
Q2 = 0.904) and the 2,2,6-trimethylheptane duplicate-row sensitivity. Wording: acentric-factor
sources, the TMB enthalpy and its tied ranking, the 3-ethyl-4-methylhexane enantiomer entry, nonane
enthalpy sources (Reid 1972), the nested best-fixed comparison of Supplementary Table S8, post-selection
status of LO(0,0,1) and M_{4.5,-9}, interval reading, Lean scope, novelty statements (Rada 2026 device,
M-polynomial, exponential-index inequalities), enumeration-based minimality, Remark 3.10 proof step.
An independent audit of v40.28 was also addressed: NIST averages and the 3 K screen, the calorimetric
census scope, the size refit and InChI parser, and a seventh unverified octane entropy
(2,3-dimethylhexane; API-44 sensitivity rerun).

**v40.28 (2026-10-10):** fixes from four independent reviews (two mathematical, one data/code, one
referee). No mathematical error was found. New: the affine dimension of the degree-pair counts (at most 7
at fixed order, 8 across orders, attained by the data sets) and the octane boiling-point error floor
(`structural/count_dimension_check.py`); the nonane 3-ethyl-4-methylhexane boiling-point conflict and
its sensitivity (`external/nonane_tb_conflict.py`, verdict still mixed); the registered secondary
question of Test B. The rank test in `press_size` is now scale invariant (no displayed value
changes). Wording: Theorem 3.3 (Delta > delta), Remark 3.7 (the parent's ratio line reaches the same
limit), Remark 3.10 (all trees), relation to Rada 2026 Example 3, K_{a,b}, Section 5 preamble and
Corollary 5.9, Lean scope in the conclusion, Supplement S7 and LEAN_VERIFICATION.md.

**v40.27 (2026-10-10):** Propositions 5.6-5.8 state a nonempty edge set; the remark after
Proposition 5.8 no longer calls the comparison sharp (its constants are the best edgewise ones,
and a bound is attained only when every edge attains the extremum).

**v40.26 (2026-10-10):** review fixes: predictive claims in Section 6.4 limited to the models, boxes
and budgets evaluated; the exploratory resampling range no longer compared with the conditional
interval; the one-sided gain rule in `external/bp/bp_tests.py` now requires a positive lower endpoint
(verdicts unchanged); m >= 1 in Proposition 3.17; countable-union step for generic discrimination;
true interval check of the Lemma 3.1 witness; reproduction map and `requirements-extras-lock.txt`.
The relative-range guard of `fold_select_ols` was not translation invariant; it was recorded as an
expected failure here and repaired in v40.29 (no output changes in any caller). The rank guard of the
boiling-point tests was fixed in v40.28.

**v40.25 (2026-10-09):** MATCH-style pass: abstract leads with the mathematical results; Section 6
and the conclusion condensed (no number or verdict changed); reference list strictly
alphabetical; three 2027 MATCH papers on the degree-ratio Sombor index cited under Corollary 3.6.

**v40.24 (2026-10-09):** the weak-discrimination theorem (former Theorem 4.3) is withdrawn from
the submission and kept on the branch `research/weak-discrimination`; Example 4.3 is now
checked directly from the trees (`structural/sumconn_pair_check.py`).

**v40.23 (2026-10-09):** restructured in MATCH statement-driven form; collision minimality certified over all tree orders 2–16;
tetramethylbutane ΔH_vap source audit; exploratory selection-aware resampling; independent
permutation audit. Full history in `V35_TO_V36_SCIENTIFIC_CHANGELOG.md`.

## Run the whole computation again (Google Colab)

`colab/` holds numbered notebooks, `00_setup_and_plan.ipynb` to `11_final_report.ipynb`, that re-run every
script in the plan of `colab/pipeline.py` in dependency order (the two independent cross-checks outside the plan are named in its report), from the source records to the tables. They keep their
progress in Google Drive, so a long run can continue after a disconnect. The last notebook compares every
output with the commit. `12_enumeration_certificates.ipynb` runs on its own in about a minute and reproduces the
minimal collision orders 13 and 16 with code independent of the repository's verifiers. See `colab/README.md`.

## Run the checks yourself (Jupyter or Google Colab)

These are lightweight checks of single parts of the paper, separate from the staged replay above. Each notebook recomputes one part of the paper from the data in `DATA/` and prints the
value in the paper next to the recomputed value; the last cell fails if any differ. On
Colab the notebook clones this repository and installs the requirements itself.

| Notebook | What it checks | Time | Open |
|---|---|---|---|
| `notebooks/01_data.ipynb` | the datasets in `DATA/` and their provenance | seconds | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/0a36902e5b6ed7a56b0534641cb12431616c2066/notebooks/01_data.ipynb) |
| `notebooks/02_mathematics.ipynb` | Lemma 1, the colliding profiles of Theorem 2, Example 2, certificates | under a minute | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/0a36902e5b6ed7a56b0534641cb12431616c2066/notebooks/02_mathematics.ipynb) |
| `notebooks/03_degeneracy.ipynb` | Table 2 and the order-10 and order-16 counts, by enumerating every tree | under a minute | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/0a36902e5b6ed7a56b0534641cb12431616c2066/notebooks/03_degeneracy.ipynb) |
| `notebooks/04_octane_correlations.ipynb` | all 60 correlations of Table 4 and the tetramethylbutane audit | seconds | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/0a36902e5b6ed7a56b0534641cb12431616c2066/notebooks/04_octane_correlations.ipynb) |
| `notebooks/05_boiling_points.ipynb` | Table 5 baselines, the 200-permutation check, the resampling summary | about 5 minutes (`RUN_SLOW = True`: about 1 hour) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/0a36902e5b6ed7a56b0534641cb12431616c2066/notebooks/05_boiling_points.ipynb) |
| `notebooks/06_verification_suite.ipynb` | the repository's own fast verification suite, in an environment with the pinned versions | about 7 minutes | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/0a36902e5b6ed7a56b0534641cb12431616c2066/notebooks/06_verification_suite.ipynb) |

The notebooks are committed with their outputs from a local run. `notebooks/gen_notebooks.py`
regenerates them. The Lean proofs need a Lean toolchain and are not run in a notebook.

## Lean verification

`LEAN_VERIFICATION.md` maps every numbered statement of the paper to the Lean 4 theorems of `formal/` and states what is machine-checked; `cd formal && ./verify.sh` rebuilds and checks the development.

## Current documents
| File | Content |
|---|---|
| `main.tex`, `LOYOLA_paper.pdf` | the paper (44 A5 pages, MATCH template; one figure) |
| `supplement.tex`, `LOYOLA_supplement.pdf` | Supplementary Material (28 pages) |
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
                                        # without the NIST WebBook pages (not redistributed) use --offline, as CI does;
                                        # python3 external/nist_pages.py --download retrieves them (explicit, rate-limited)
python3 verify_loyola_v35.py            # core tables, figures, analyses
python3 external/verify_external.py     # nonane and boiling-point tests, rebuilt from the downloaded NIST pages
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
