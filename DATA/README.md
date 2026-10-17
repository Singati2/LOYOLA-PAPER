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
| `calorimetric_dHvap298_alkanes.csv` | | alkanes with calorimetric ΔH_vap(298 K) on the NIST WebBook (data-availability check for a future test). Built from the curated index `../external/bp/nist_alkanes_skeletons_audit.csv` (C4 to C16, retrieved 2026-10-03); phase-change pages outside C6 to C10 are not archived, so this census is reproducible from the curated index, not end to end from raw pages | Supplementary Section S9 |

Third-party values and licence

* The MIT licence of the repository covers its code and text. It does not cover the property values
  taken from third-party sources, which remain under the terms of those sources and are used here,
  with attribution, for verification of the paper: the NIST Chemistry WebBook (NIST Standard
  Reference Database 69), the published compilations cited in the paper, and the Korea
  Thermophysical Properties Data Bank (KDB) as shown on Cheméo (https://www.chemeo.com).
* Complete NIST Chemistry WebBook pages (NIST Standard Reference Database 69) are not redistributed.
  NIST states that its Standard Reference Data are copyrighted by the U.S. Secretary of Commerce and
  may not be reproduced, stored in a retrieval system or transmitted without prior permission
  (https://www.nist.gov/srd/public-law, consulted 2026-10-17). The data builds read 262 pages (154
  under `../external/bp/nist_raw`, 17 under `../external/bp/nist_hvap_pts`, 91 under
  `../external/nonane_raw_nist`). Nothing downloads them automatically; `verify.py --offline` and CI
  run without them. `python3 ../external/nist_pages.py --download` retrieves them from the WebBook
  for the user's own use (one request per second) and checks each against the SHA-256 of the copy
  from which the committed data sets were built (`../external/nist_pages.csv` lists URL, archive date
  and digest). The repository keeps the values extracted from those pages, each with its WebBook URL;
  see `../audit/NIST_REDISTRIBUTION_AUDIT.md` for what they contain and what remains open. The pages
  were tracked in commits up to v40.31 (`2158b72`) and removed from the tracked tree after it; the
  history was not rewritten, so the earlier commits still contain them.
* Cheméo's terms (https://www.chemeo.com/tos, consulted 2026-10-16) permit value-by-value use with
  the citation "Cheméo, chemical and physical properties (https://www.chemeo.com)" and forbid bulk
  download or inclusion of the database as-is. The KDB terms could not be retrieved (the CHERIC site
  did not serve them on 2026-10-16). The KDB/Cheméo footprint of the repository is:
  - `octane_provenance.csv` and its byte-identical copy `../octane_property_provenance_v35.csv`:
    the 18 octane acentric-factor rows (source column: KDB via Cheméo) and 25 further rows
    (T_B 9, ΔH_f 3, ΔH_vap 4, S 9) that cite KDB or Cheméo as a comparison value or as a source
    consulted that lacks the value;
  - `../source_sensitivity.py`: two hard-coded KDB acentric factors (0.303 for
    2,2,4-trimethylpentane, 0.251 for 2,2,3,3-tetramethylbutane);
  - `../audit/final/scripts/audit_calc.py`: the KDB critical constants of 2,2,3,3-tetramethylbutane
    (Tc 567.8 K, Pc 28.7 bar);
  - `../supplement.tex` (and its copies under `../LOYOLA_SUPPLEMENT_OVERLEAF` and
    `../LOYOLA_FINAL_PAPER_OVERLEAF`): three KDB comparison numbers (0.251, stated twice, and 0.303),
    plus the differences from KDB (0.002 to 0.004) derived from them and the statement that the
    remaining acentric factors agree with KDB to within 0.005.
* Redistribution terms for the KDB/Cheméo values and the NIST pages are not yet settled, so no
  archive (Zenodo or other) should be made from this repository until they are.

Notes

* 2,2,3,3-tetramethylbutane: the benchmark ΔH_vap = 8.41 kcal/mol has no stated source
  and the compound is crystalline at 298 K. See `../TMB_DHVAP_AUDIT.md` for the trace and
  the separately reported sensitivity analyses. The value is kept unchanged.
* Quality flags: the `classification` column of `octane_provenance.csv` marks every octane
  value (VERIFIED EXACT, VERIFIED AFTER UNIT CONVERSION, AGREEMENT WITHIN TOLERANCE,
  SOURCE VARIATION / EXPLAINED, CANNOT VERIFY, CONFLICT). The eight CANNOT VERIFY values are seven
  gas-phase entropies (2,3-dimethylhexane was reclassified in v40.29: its only match is a secondary
  compilation, and the 1947 API Project 44 value differs by 1.91) and the tetramethylbutane ΔH_vap; the one CONFLICT is the tetramethylbutane
  acentric factor (0.247 against 0.251 in KDB and 0.25529 in the octane set of Ediz 2017,
  Table 1; the source of 0.247 was not located, and no compilation reproduces the ω column exactly). These values are kept as the historical
  benchmark and their sensitivity is reported (Supplementary Sections S1, S3, S8). The label records
  numerical agreement, not source authority: AGREEMENT WITHIN TOLERANCE can mean agreement with a
  compiled dataset, and the `source` column says which; only rows citing NIST or NBS Circular 461 rest on
  a primary source that was inspected.
* 3-ethyl-4-methylhexane: the nonane T_B (413.55 K) has a second NIST entry 6.4 K lower; the
  molecule is excluded from the pooled boiling-point cohort and its effect on the nonane test is in
  `../external/nonane_tb_conflict_out.txt` (Supplementary Section S4). The second entry (NIST C500006531,
  Lukes and Langthaler 1957, TRC uncertainty 2 K) is for d-3-ethyl-4-methylhexane; the registered value
  (Fenske et al. 1947) carries a TRC uncertainty of 0.5 K, so the registered value is kept.
* 2,2,6-trimethylheptane (decanes): NIST lists 421.15 K from Marschner and Carmody (1951) twice. The
  registered rule takes the median of every listed determination (148.2 degC); counting that row
  once gives 148.4 degC and moves the decane ridge Q2 from 0.8599 to 0.8591 (pooled 0.9911 either
  way). The registered value is kept; see `../audit/final/scripts/bp_duplicate_sensitivity.py`.
* Pre-registration records: `../external/PREREG_v37.md` (nonanes), `../external/PREREG_v40.md`
  (boiling points), including every change made after outcomes were seen.
