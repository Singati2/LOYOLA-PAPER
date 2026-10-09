# The Loyola Index Family: What a Degree-Imbalance Coordinate Can and Cannot Resolve

Advik Natarajan, Ganesh Shiwakoti, Michael Arockiaraj — manuscript, supplement,
data, code and machine-checked proofs.

**v40.23 (2026-10-07):** co-authors' review applied: Section 3 framed in plain words, attribution remark removed, QSPR data detail cut further, LEAN_VERIFICATION.md added (statement-by-statement map to the Lean theorems); collision minimality certified by exhaustive enumeration (structural/minimality_check.py); Rada 2026 overlap stated before Theorem 2; new Theorem 4.3: imbalance restores weak discrimination on molecular graphs at rational exponents with 2a+b non-integer; restructured in MATCH statement-driven form (section-based numbering, numbered contributions, Discussion and limitations); v40.22 added the novelty audit, Proposition 3, the order-17 certification and the experiment fixes; see V35_TO_V36_SCIENTIFIC_CHANGELOG.md.

## Lean verification

`LEAN_VERIFICATION.md` maps every numbered statement of the paper to the Lean 4 theorems of `formal/` and states what is machine-checked; `cd formal && ./verify.sh` rebuilds and checks the development.

## Current documents
| File | Content |
|---|---|
| `main.tex`, `LOYOLA_paper.pdf` | the paper (38 A5 pages, MATCH template) |
| `supplement.tex`, `LOYOLA_supplement.pdf` | Supplementary Material (23 pages) |
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
`V35_TO_V36_SCIENTIFIC_CHANGELOG.md` records every revision; earlier
version notes and logs are kept only in the git history.

License: MIT (see `LICENSE`).
