# The Loyola Index Family: What a Degree-Imbalance Coordinate Can and Cannot Resolve

Advik Natarajan, Ganesh Shiwakoti, Michael Arockiaraj — manuscript, supplement,
data, code and machine-checked proofs.

**v40.11 (2026-10-06):** fail-closed data build and structural checks, scoped identifiability wording, single verification entry point with continuous integration; no citation of unpublished work. See `V35_TO_V36_SCIENTIFIC_CHANGELOG.md`.

## Current documents
| File | Content |
|---|---|
| `main.tex`, `LOYOLA_paper.pdf` | the paper (43 A5 pages, MATCH template) |
| `supplement.tex`, `LOYOLA_supplement.pdf` | Supplementary Material (21 pages) |
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
`V35_TO_V36_SCIENTIFIC_CHANGELOG.md` records every revision; `history/` keeps
earlier version notes and the v35 provenance audit.

License: MIT (see `LICENSE`).
