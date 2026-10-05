# LOYOLA v36 — data correction, full-precision rounding, verifier hardening

Authoritative manuscript: `main.tex`. Compiled copy: `LOYOLA_paper.pdf`.
v36 repairs the defects listed below; each was reproduced before repair and
every regenerated table cell was cross-checked with an independent
re-implementation (no package code imported). Script filenames keep their
historical `_v35` suffixes.

## Repairs
1. **Data error (ΔH_vap, kcal/mol, 298 K).** Four values corrected to the
   NIST WebBook (identical to the standard octane dataset, arXiv:1701.02859
   Table 1, at 2 dp): 3,3-dimethylhexane 9.04→8.97; 3-ethyl-3-methylpentane
   9.21→9.08; 2,2,3-trimethylpentane 8.88→8.83; 2,3,3-trimethylpentane
   9.02→8.90. The data now live in ONE module, `octane_data.py` (OCTANES,
   NAMES, parser); every script imports it, so no other file holds a copy.
   Every dependent analysis, table, figure and prose number was regenerated.
   Main consequences: the ΔH_vap column winner is now LO(0,0,1) (|r| 0.984;
   LO(0,0,2) 0.981); in the 100-seed sweep γ improved ΔH_vap in 100/100
   seeds at both budgets and in the paired control (previously 91–93/100).
   The text keeps this explicitly descriptive (optimizer variance over
   candidate streams on one fixed 18-molecule dataset).
2. **Double rounding.** All canonical CSVs are written at full precision
   (10 decimals / 12 significant digits); every displayed number is the single
   rounding of a full-precision value (tab:ablation T_B ΔQ² +0.136, ω Q²_LO
   +0.956, ω RMSE_LO 0.008; FGD published control now classified from the
   rounded full-precision values: 11/14 exact, 3/14 within one unit).
3. **Verifier.** Exact display-string comparison for every numeric cell of all
   eight numeric tables (lo_octane, lo_tuning, lo_tuning_bestfixed, ablation
   (both panels), multiorder, fgdss, collisions, octane-data); tab:ablation,
   tab:fgdss and tab:multiorder recomputed from first principles inside the
   verifier (hat-matrix PRESS selection; AHU canonical forms); provenance
   parser fixed, paper values must equal the dataset, PROV_TOL(ΔH_vap) = 0.04;
   the [N] re-run now covers seven scripts (including the 100-seed sweep and
   the source-sensitivity script). `--selftest`: 112 tests (incl. a stale-figure attack), all rejected for
   the intended reason.
4. **Tuning pools.** tab:lo_tuning_bestfixed reuses the tab:lo_tuning pools
   (one `default_rng(42)` stream: M2, HM, mM2, LO(0,0,1), then LO(0,0,2)); the
   T_B best-of-pool value is now 0.835 in both tables.
5. **Text.** max selected |γ| 0.48; seed-specific "column-winner gain is zero"
   claim reworded (median +0.003, positive in 96% of pool seeds for M2/ω);
   seeds and rounding conventions stated; tab:ablation split into a single
   illustrative seed (a) and the 100-seed median [min, max] and sign counts
   (b); "2-methyl-3-ethylpentane" → "3-ethyl-2-methylpentane"; Figure 2
   dashed line explained.
6. **Provenance.** Misclassified rows corrected (see
   `LOYOLA_V35_DATA_PROVENANCE.md`, v36 section); recount 3/34/32/13/7/1 (v36.1 strict rule: 3/29/37/13/7/1)
   (same totals, different composition); "one marginal conflict" sentence
   fixed; the false ω "cannot alter a correlation" claim corrected.
7. **Entropy-source sensitivity** (disclosure only, data unchanged):
   `entropy_source_sensitivity_v36.csv` — all 12 S correlations change at the
   third decimal (max 0.034), winner HM unchanged. The 2,3,3-trimethylpentane
   S value (101.31) duplicates the 2,2,3-trimethylpentane value: possible copy
   error, flagged for the authors.

## Verification
```bash
python3 -m pip install -r requirements-lock.txt
python3 verify_loyola_v35.py            # FULL PASS, exit 0 (~3 min)
python3 verify_loyola_v35.py --selftest # all attacks rejected, exit 0 (~5 min)
shasum -a 256 -c SHA256SUMS.txt
```
Regeneration (each writes next to itself): `ablation_gm_vs_lo.py`,
`ablation_robustness.py`, `expanded_robustness_v35.py`,
`redundancy_collisions.py`, `fgd_structure_sensitivity.py`,
`multi_order_degeneracy.py`, `source_sensitivity.py`,
`generate_loyola_v35_figures.py`.

## Standing CANNOT VERIFY
6 NIST-absent gas entropies; the tetramethylbutane 298 K vaporization case;
paywalled AKCE 2020 / Portilla JMC full texts; InChIKeys. Coauthor sign-off
and the authors' own Overleaf compile remain the gating steps.

## Integrity manifest
`python3 manifest.py --write` regenerates SHA256SUMS.txt (one SHA-256 per
git-tracked file); `python3 manifest.py` checks it and fails on duplicate
paths, untracked/missing files or hash mismatches.

## External test (v37)
`python3 external/verify_external.py` regenerates the nonane data, the
pre-registered analysis, baselines, the exploratory transfer and
molecule-bootstrap analyses, and Table 6, and checks them against the
committed files. See external/PREREG_v37.md (and the template for a future
measured-data test, external/PREREG_TEMPLATE_measured_dHvap.md).
