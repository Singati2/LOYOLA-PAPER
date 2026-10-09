# Source audit: the vaporisation enthalpy of 2,2,3,3-tetramethylbutane

The octane benchmark used in Table 4 of the paper gives
ΔH_vap = 8.410 kcal/mol for 2,2,3,3-tetramethylbutane (TMB, CAS 594-82-1).
NIST lists ΔvapH° = 42.94 and 42.91 kJ/mol (10.26 kcal/mol). This file traces
both values and records what each one measures. The benchmark value is kept
unchanged in the paper; the alternatives are sensitivity analyses only.

## 1. Phase behaviour

* NIST WebBook (archived copy: `external/bp/nist_raw/C594821.html`): triple point
  373.97 K (Scott, Douslin et al. 1952), T_boil 379.6 K, T_fus 374 K.
  TMB is therefore crystalline at 298 K. A liquid at 298 K exists only as a
  hypothetical supercooled state.

## 2. Values on record

| Quantity | Value | Temperature | Process | Source |
|---|---|---|---|---|
| Benchmark "DHVAP" | 8.410 kcal/mol (35.19 kJ/mol) | stated as 25 °C | not stated | Milano octane set, www.moleculardescriptors.eu, reproduced in Ediz 2017 (arXiv:1701.02859, Table 1) |
| Circular 461, Table 3m, "at 25 °C" | 10.24 kcal/mol | 298 K | **sublimation**, solid → gas (footnote b) | Rossini et al., NBS Circ. 461 (1947), p. 134, table dated March 31, 1944 |
| Circular 461, Table 3m, "at normal boiling point" | 7.56 kcal/mol | 379.45 K | liquid → gas | same table |
| NIST ΔvapH° | 42.94 kJ/mol (10.26 kcal/mol) | 298 K | listed as vaporisation | Majer and Svoboda 1985 |
| NIST ΔvapH° | 42.91 kJ/mol | 298 K | listed as vaporisation; the same paper is listed as ΔsubH 42.9 ± 0.9 | Osborne and Ginnings 1947 |
| NIST ΔsubH° | 43.37 ± 0.21 kJ/mol | 273–338 K data | sublimation | Scott, Douslin et al. 1952 |
| NIST ΔvapH | 33.3 kJ/mol (7.96 kcal/mol) | 383 K (data 377–390 K) | liquid → gas | Stephenson and Malanowski 1987 |
| NIST ΔfusH | 7.54 kJ/mol | 373.9 K | fusion | Scott, Douslin et al. 1952 |

## 3. Findings

1. **The benchmark column follows Circular 461 at 25 °C for the other 17 isomers**
   (for example n-octane 9.915, 2-methylheptane 9.483, 2,2,4-trimethylpentane
   8.396 in Circular 461 against 9.915, 9.484, 8.402 in the benchmark). For TMB
   Circular 461 gives 10.24 kcal/mol at 25 °C, explicitly a heat of sublimation.
   The benchmark's 8.410 does not appear in Circular 461.
2. **The NIST 298 K "ΔvapH°" values describe the crystal.** The compound is solid at
   298 K, and NIST lists the Osborne–Ginnings measurement both as ΔvapH° (42.91)
   and as ΔsubH° (42.9). These values agree with Circular 461's 10.24 kcal/mol
   sublimation enthalpy, not with a liquid → gas process. They are therefore not
   interchangeable with the vaporisation enthalpies of the other 17 isomers.
3. **8.410 is consistent with a hypothetical supercooled liquid at 298 K**, but this is
   not established. ΔsubH(298 K) − ΔfusH(373.9 K) = 43.37 − 7.54 = 35.83 kJ/mol
   = 8.56 kcal/mol; with Circular 461's 10.24 kcal/mol the same estimate is
   8.44 kcal/mol. A heat-capacity correction of ΔfusH from 373.9 K to 298 K is not
   applied. The earliest identifiable carrier of 8.410 is the Milano octane
   dataset; its original source is not stated there and was not located.
4. The liquid value at the normal boiling point (7.56 kcal/mol) refers to a
   different temperature from the other 17 entries and is not used as a variant.

## 4. Sensitivity (`tmb_dhvap_audit.py`, output `tmb_dhvap_audit.csv`)

| Variant | TMB value (kcal/mol) | Top index | top \|r\| | LO(0,0,1) \|r\| | lowest \|r\| |
|---|---|---|---|---|---|
| original benchmark | 8.410 | LO(0,0,1) | 0.984 | 0.984 | 0.383 |
| isomer excluded | — | LO(0,0,1) | 0.980 | 0.980 | 0.279 |
| hypothetical-liquid estimate | 8.564 | LO(0,0,1) | 0.976 | 0.976 | 0.368 |
| NIST 298 K, solid → gas | 10.263 | LO(0,0,1) | 0.374 | 0.374 | 0.018 |

The column leader is the same in every variant. The magnitudes survive every
liquid-phase variant and collapse only when a sublimation enthalpy is put in the
place of a vaporisation enthalpy, which mixes two processes in one column.

## 5. What depends on this value

Only the ΔH_vap column of Table 4 and the exploratory matched-budget comparison of
Section 6.2 (whose TMB-excluded repetition is in `dhvap_tmb_exclusion_summary_v36.csv`).
No theorem, no proposition and no pre-registered test uses it.
