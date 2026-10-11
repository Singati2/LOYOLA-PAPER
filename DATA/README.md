# DATA

Every dataset used in the paper, in one place. The analysis scripts read the
original files; `build_data.py` copies them here byte for byte (and writes
`octane_properties.csv` from `octane_data.py`), and `python3 DATA/build_data.py --check`,
part of `python3 verify.py`, fails if any copy differs from its source.

| File | Rows | Content | Used in |
|---|---|---|---|
| `octane_properties.csv` | 18 | octane isomers: SMILES, T_B (°C), ΔH_f and ΔH_vap (kcal/mol, 298 K), S (cal/(mol K), gas, 298 K), acentric factor ω | Section 6.1, Table 4, Supplementary Table S5 |
| `octane_provenance.csv` | 90 | value-by-value source record for the octane data (NIST WebBook, 1947 API Project 44 tables), with classification | Supplementary Sections S1, S8 |
| `nonane_properties.csv` | 35 | nonane isomers: CAS, SMILES, T_B (°C), ΔH_vap (kcal/mol, 34 values) from the NIST WebBook | Section 6.3 |
| `nonane_provenance.csv` | | determinations, selection rule and verbatim source snippet for every nonane value | Supplementary Section S4 |
| `boiling_points_C6_C10.csv` | 100 | measured boiling points (°C) of the C6–C10 alkanes admitted by the pre-registered rule, with degree pairs | Section 6.4, Table 5 |
| `boiling_points_structures.csv` | 100 | the same molecules with NIST identifiers and the skeleton InChI from the archived NIST audit; `build_data.py` re-derives the degree pairs from the InChI connection layer and fails on any mismatch | Section 6.4 |
| `boiling_points_provenance.csv` | | included and excluded molecules with the rule and all NIST determinations | Section 6.4 |
| `calorimetric_dHvap298_alkanes.csv` | | alkanes with calorimetric ΔH_vap(298 K) on the NIST WebBook (data-availability check for a future test) | Supplementary Section S9 |

Notes

* 2,2,3,3-tetramethylbutane: the benchmark ΔH_vap = 8.41 kcal/mol has no stated source
  and the compound is crystalline at 298 K. See `../TMB_DHVAP_AUDIT.md` for the trace and
  the separately reported sensitivity analyses. The value is kept unchanged.
* Quality flags: the `classification` column of `octane_provenance.csv` marks every octane
  value (VERIFIED EXACT, VERIFIED AFTER UNIT CONVERSION, AGREEMENT WITHIN TOLERANCE,
  SOURCE VARIATION / EXPLAINED, CANNOT VERIFY, CONFLICT). The seven CANNOT VERIFY values are six
  gas-phase entropies and the tetramethylbutane ΔH_vap; the one CONFLICT is the tetramethylbutane
  acentric factor (0.247 against a compiled 0.251). These values are kept as the historical
  benchmark and their sensitivity is reported (Supplementary Sections S1, S3, S8).
* 3-ethyl-4-methylhexane: the nonane T_B (413.55 K) has a second NIST entry 6.4 K lower; the
  molecule is excluded from the pooled boiling-point cohort and its effect on the nonane test is in
  `../external/nonane_tb_conflict_out.txt` (Supplementary Section S4).
* Pre-registration records: `../external/PREREG_v37.md` (nonanes), `../external/PREREG_v40.md`
  (boiling points), including every change made after outcomes were seen.
