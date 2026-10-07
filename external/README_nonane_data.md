# Nonane (C9H20) property dataset — sources and rules

Built 2026-10-03 under `PREREG_v37.md` (data rules binding). Every value was read
from a NIST Chemistry WebBook page fetched with curl on 2026-10-03; raw HTML is
archived in `nonane_raw_nist/` and `build_nonane_data.py` regenerates the CSVs from
it byte-for-byte (no hand-typed values). No value was estimated, imputed or recalled.

## Files
- `nonane_data.csv` — name, cas, smiles, T_B_C, dHvap_kcal (blank = MISSING).
- `nonane_provenance.csv` — one row per value (69 rows): original value/units,
  conversion, all NIST determinations with references, selection rule, URL,
  retrieval date, verbatim NIST table row.
- `nonane_identity.csv` — NIST name, IUPAC InChI, CAS, URLs per isomer.
- `check_nonane_structures.py` — enumerates the 35 trees (n=9, max deg <= 4), parses
  every SMILES with `octane_data.alkane_adj`, checks a 1:1 match to the trees, and
  checks each SMILES graph is isomorphic to the carbon skeleton in NIST's InChI for
  that CAS. Passes (exit 0). The 35 NIST InChI graphs are pairwise non-isomorphic.
- `nonane_crosscheck_secondary.csv` — secondary comparison (not used in data).
- `build_nonane_data.py`, `nonane_raw_nist/` — reproducibility.

## Sources
Identity: NIST name search `cbook.cgi?Name=<name>&Units=SI&Mask=4` (CAS, InChI).
Values: `cbook.cgi?ID=C<CAS>&Mask=4` phase-change table; for NIST AVG entries the
"Individual data points" pages (`&Type=TBOIL`, `&Type=HVAP`) are recorded in
`all_determinations`.

## Rules applied
- T_B degC = K - 273.15, half-up to 0.1. dHvap kcal/mol = kJ/4.184, half-up to 0.01.
- dHvap = NIST "ΔvapH° (enthalpy of vaporization at standard conditions)" rows only;
  temperature-dependent ΔvapH(T) rows ignored.
- Selection: NIST AVG if given; else most recent calorimetric (method C) entry.

## Counts
- T_B: 35/35. Rule: NIST AVG 20; single NIST determination 5; no AVG and several
  determinations 10 (see deviation D1).
- dHvap: 34/35. Rule: NIST AVG 1 (n-nonane); most recent calorimetric 4
  (2,2,5-TMHx, 2,3,5-TMHx [Osborne & Ginnings 1947]; 3,3-diethylpentane [Fuchs &
  Peacock 1979]; 2,2,4,4-TMP [Fuchs, Peacock et al. 1982]); sole non-calorimetric
  NIST entry 29 (see D2).

## MISSING
- dHvap, 3-ethyl-4-methylhexane (CAS 3074-77-9): the NIST page has no ΔvapH° entry
  (only Tboil). Not imputed. (A secondary table lists 43.95 kJ/mol; not used.)

## Flags / deviations requiring author decision (prereg gaps)
- **D1 (T_B, 10 isomers without NIST AVG and >1 determination):** the prereg fallback
  "most recent calorimetric determination" does not apply to a boiling point. Applied
  the analogue "most recent primary experimental determination" (excluding the CRC
  Handbook compilation, Weast & Grasselli 1989). All determinations are listed so the
  authors can ratify or change this and record it as a deviation. Largest spreads:
  2,2,3-trimethylhexane (404.85–407.4 K; used Maretina & Petrov 1961, 407.4 K,
  TRC unc. 1.5 K), 4-ethylheptane (411.65–414.55 K), 4,4-dimethylheptane
  (407.5–408.4 K; used Levina et al. 1952, 407.5 K).
- **D2 (dHvap, 29 isomers):** the only NIST ΔvapH° entry is non-calorimetric
  (method N/A): Reid 1972 (25; a handbook compilation, NIST notes "See also
  Labbauf, Greenshields, et al., 1961") or Labbauf, Greenshields & Rossini 1961,
  J. Chem. Eng. Data 6, 261 (4). Neither prereg rule (AVG / calorimetric) is met;
  values used as the sole available NIST value and flagged. Strictly these are not
  primary measurements.
- **D3 (T_B precision):** NIST AVG values are rounded to the uncertainty digit; 13 of
  20 are integer-K (e.g. "404. ± 2."), so T_B_C carries only ~1 K precision there
  despite the 0.1 degC format.
- **D4 (T_B outlier inside a NIST AVG):** 2,3,3,4-tetramethylpentane AVG = "413. ± 6."
  K (139.9 degC); 7 of its 8 individual points are 414.35–414.7 K, one (Cline 1939)
  is 405 K. Used as the prereg rule dictates; authors should be aware. 2,4-dimethyl-
  heptane's point list contains a 352.0 K entry that NIST's AVG (406. ± 1.) excludes.
- Same-study duplicates (Osborne & Ginnings 1947 listed as 41.4 and 41.42; 40.2 and
  40.17 kJ/mol): the more precisely reported entry was used.

## Secondary cross-check (dHvap only; not used in data)
Table 1 of arXiv:2605.00044 ("Resolving Open Problems on the Hyper-Zagreb Index...",
values in kJ/mol, citing Mondal, Huh & Das 2024) lists 35 values keyed C9:1–C9:35 with
hyper-Zagreb index HM but no names. Isomers were matched only where HM is unique
(17 comparable with a primary value). |diff| > 0.05 kcal/mol: 2-methyloctane 0.06,
2,6-dimethylheptane 0.12, 2,4,4-trimethylhexane 0.06, 3,3-diethylpentane 0.18,
2,2,4,4-tetramethylpentane 0.09. No accessible secondary compilation of all-35 T_B
was found (Wiley QSPR paper 10.1155/jom/9300802: HTTP 403; Wikipedia rate-limited
and is tertiary), so T_B was not cross-checked.

## Source label mapping
NIST WebBook labels 25 of the nonane dHvap entries "Reid, 1972". That entry is
R. C. Reid's review (AIChE J. 18 (1972) 1278) of the handbook by R. C. Wilhoit
and B. J. Zwolinski, *Handbook of Vapor Pressures and Heats of Vaporization of
Hydrocarbons and Related Compounds* (Texas A&M Research Foundation, 1971); the
manuscript cites the handbook (WilhoitZwolinski1971). The other 4 compilation
entries are Labbauf (the journal record spells it "Labauf"), Greenshields & Rossini, J. Chem. Eng.
Data 6 (1961) 261-263.
