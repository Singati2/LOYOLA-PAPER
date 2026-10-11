# Observation-level provenance audit of the disputed chemical data

Disposition of every finding in v40.29: see `MATCH_SUBMISSION_READINESS.md` in this folder.

Repository: ~/LOYOLA-PAPER, commit 0817f35 ("v40.28: fixes from four independent reviews").
Paper: "The Loyola Index Family and the Resolution Limit of Degree Imbalance" (MATCH Commun. Math. Comput. Chem.).
Audit date: 2026-10-11. The calculation scripts and their outputs are in `audit/final/scripts/` (`audit_calc.py`, `nonane_calc.py` and their `_out` files). The source PDFs consulted (NBS Circular 461, doi:10.6028/NBS.CIRC.461, and Ediz 2017, arXiv:1701.02859) are public and not redistributed here. All new calculations below are exploratory and are not proposed as replacements for registered values.

## 1. Summary

The registered data are honestly described in almost every respect, and none of the five disputed items changes a conclusion the paper draws. The existing sensitivity analyses reproduce exactly from the repository code. Three findings are new.

1. **Acentric factor of 2,2,3,3-tetramethylbutane (TMB).** The paper's own stated benchmark (the Milano octane set, reproduced in Ediz 2017, arXiv:1701.02859, Table 1) gives 0.25529, not 0.251 (KDB) and not 0.247 (value used). The repository compares 0.247 only with KDB. The source of 0.247 was not located. Five of the 18 acentric factors used match neither the Milano set nor KDB at the third decimal. The supplement's statement that the acentric factors "were taken from KDB-derived compilations" (supplement.tex:188) is therefore not supported value by value. Substituting the Milano TMB value moves the omega correlations by at most 0.007 and leaves M2 first. The conclusion is unchanged, but the source sentence should be corrected.
2. **Second boiling point of 3-ethyl-4-methylhexane.** The 407.15 K entry (NIST C500006531) belongs to the record named "d-3-ethyl-4-methylhexane". It is a single enantiomer from an organic degradation study (Lukes and Langthaler, Chem. Listy 51 (1957) 1869), and TRC assigns it an uncertainty of 2 K. The registered 413.55 K (Fenske et al. 1947) carries 0.5 K. Enantiomers share one normal boiling point, so the 6.4 K gap is a measurement discrepancy and not a stereochemical difference. This supports keeping the registered value, with the existing exclusion and replacement scenarios as sensitivity analyses. The repository does not record this point anywhere.
3. **8.41 kcal/mol for TMB.** Two independent routes give the hypothetical supercooled liquid at 298 K a value of 8.56 kcal/mol (sublimation minus fusion, with no heat-capacity correction) and 8.65 kcal/mol (the normal-boiling-point liquid value of Circular 461, 7.56 kcal/mol, scaled by the 25 °C to T_b ratio of the other 17 isomers; ±2 SD range 8.51 to 8.79). The value 8.41 lies 0.15 to 0.24 kcal/mol below both estimates. A positive liquid-minus-crystal heat-capacity correction would raise the first estimate further. "Consistent with a hypothetical supercooled liquid" is close but slightly generous. The best classification is unverified, most plausibly an estimated or extrapolated hypothetical-liquid value. LO(0,0,1) stays first in every liquid-phase variant (|r| = 0.984, 0.980, 0.976, 0.968).

Also confirmed directly from the scanned NBS Circular 461 (doi:10.6028/NBS.CIRC.461): all six Table 3p entropies used in `entropy_api44_sensitivity_v41.csv`, and the Table 3m TMB entries (10.24 kcal/mol, footnote b, sublimation; 7.56 kcal/mol at the normal boiling point). One manuscript claim overstates its evidence. The "later revisions" against which the 1947 entropies are compared were matched only in secondary QSPR datasets, never in a TRC or other primary table (supplement.tex:916 to 917). One numerical description is too strong. With TMB excluded, LO(0,0,1) leads LO(0,0,2) by 0.0004 (0.9799 against 0.9795), a tie at the displayed precision (main.tex:1520 to 1521).

For the nonane vaporisation enthalpies, the 29 compiled values are correctly disclosed. In an exploratory split, the counts-ridge baseline fits the compiled values about twice as closely as the five measured ones (mean absolute leave-one-out residual 0.059 against 0.120 kcal/mol). The registered "replicates" verdict becomes "mixed" on the 29 compiled values alone (77/100 and 75/100 seeds). It stays "replicates" with the four Labbauf rows removed (88/100 and 94/100). The paper already withdraws inferential weight from this verdict (wide box, seed-count criterion), so no conclusion changes.

## 2. Sources verified in this audit

Each DOI below was resolved through doi.org content negotiation or Crossref on 2026-10-11, and the metadata shown were returned by the resolver. Page and table numbers are given only where read from the document itself.

| Source | Identifier (verified) | What was checked |
|---|---|---|
| Rossini, Pitzer, Taylor, Ebert, Kilpatrick et al., *Selected Values of Properties of Hydrocarbons*, NBS Circular 461 (1947), API Research Project 44 | doi:10.6028/NBS.CIRC.461; PDF at nvlpubs.nist.gov | Table 3p, "Paraffins, C8, heat of formation, entropy, and free energy of formation at 25 °C", dated April 30, 1944 and April 30, 1945, printed p. 159 (PDF p. 177): gas entropies of all 18 octanes read. Table 3m, "Heat and entropy of vaporization, at 25 °C and the normal boiling point", dated March 31, 1944, printed p. 134 (PDF p. 152): TMB 10.24 kcal/mol at 25 °C with footnote b ("Heat of sublimation, for the process ... (solid) = ... (gas)") and 7.56 kcal/mol at the normal boiling point (106.30 °C). Table 1p footnote d, printed p. 157 (PDF p. 175): "S° represents the entropy (exclusive of nuclear spin) ... in its appropriate standard reference state". |
| Osborne, Ginnings, J. Res. NBS 39 (1947) 453 | doi:10.6028/jres.039.031 | Metadata only. Cited by NIST for TMB ΔvapH° 42.91 kJ/mol (method C) and ΔsubH° 42.9 ± 0.9 kJ/mol, and for the 2,2,5- and 2,3,5-trimethylhexane calorimetric values. |
| Scott, Douslin, Gross, Oliver et al., J. Am. Chem. Soc. 74 (1952) 883 to 887, "2,2,3,3-Tetramethylbutane: heat capacity, heats of transition, fusion and sublimation, vapor pressure, entropy and thermodynamic functions" | doi:10.1021/ja01124a007 | Metadata only. NIST attributes to it T_triple 373.97 K, ΔsubH° 43.37 ± 0.21 kJ/mol (273 to 338 K data), crystal I to liquid ΔH 7.540 kJ/mol at 373.9 K, and gas S° 389.3 J/(mol K). |
| Scott, J. Chem. Phys. 60 (1974) 3144 to 3165, "Correlation of the chemical thermodynamic properties of alkane hydrocarbons" | doi:10.1063/1.1681500 | Abstract: entropies at 298.15 K "tabulated for all alkanes C3 to C10" from a correlation fitted to 41 experimental entropies. NIST cites it as the source of the n-octane gas S° (467.06 J/(mol K)). Its tabulated values for the six disputed isomers were **not** seen (paywalled). The companion U.S. Bureau of Mines Bulletin 666 (1974) is cited by NIST; no DOI verified. |
| Needham, Wei, Seybold, J. Am. Chem. Soc. 110 (1988) 4186 to 4194 | doi:10.1021/ja00221a015 | Metadata only. The repository calls it the probable lineage of the octane QSPR dataset. That its tables contain the values used was **not verified**. |
| Ediz, arXiv:1701.02859 (2017) | arXiv record and PDF retrieved | Table 1 read in full: Entropy, AcenFac, HVAP, DHVAP of the 18 octanes, "from www.moleculardescriptors.eu". TMB DHVAP 8.410, TMB AcenFac 0.25529. |
| Mondal, De, Pal, arXiv:1906.06660 (2019) | arXiv record retrieved | Title and authors only. Table 2 not re-read. |
| Labbauf (Crossref: "Labauf"), Greenshields, Rossini, J. Chem. Eng. Data 6 (1961) 261 to 263 | doi:10.1021/je60010a023 | Metadata only (publisher page HTTP 403, no abstract in Crossref). Method of the vaporisation enthalpies **not verified**. |
| Somayajulu et al., J. Chem. Eng. Data 22 (1977) 229 to 234, "Enthalpies of formation, combustion, and vaporization of the 35 nonanes and 75 decanes" | doi:10.1021/je60073a021 | Metadata only. A later tabulation of the same 110 compounds, not mentioned in the repository. Values not seen. |
| Reid, AIChE J. 18 (1972) 1278 (review of the Wilhoit and Zwolinski handbook) | doi:10.1002/aic.690180637 | Metadata confirms that NIST's "Reid, 1972" label is a one-page book review. The repository's mapping to WilhoitZwolinski1971 is correct. |
| Fenske, Braun, Wiegand, Quiggle, McCormick, Rank, Anal. Chem. 19 (1947) 700 to 765, "Raman spectra of hydrocarbons" | doi:10.1021/ac60010a002 | Metadata only. Cited by NIST for 3-ethyl-4-methylhexane T_boil 413.55 K (TRC uncertainty 0.5 K). |
| Lukes, Langthaler, Chem. Listy 51 (1957) 1869, "Degradation of branched optically active tertiary bases" | DOI not verified | Title and citation as listed on the archived NIST page `external/bp/nist_raw/C500006531.html`. |
| Majer, Svoboda, *Enthalpies of Vaporization of Organic Compounds* (Blackwell, 1985) | book, no DOI | Not consulted directly. Cited through NIST only. |
| NIST Chemistry WebBook | live pages and archived HTML in the repository | Gas-phase pages (Mask=1) of the six isomers in item 1, re-fetched 2026-10-11: no S° entry on any of them. TMB phase-change page (archived): values in item 2. |
| Chemeo (KDB) TMB page | chemeo.com/cid/54-292-8 | ω 0.2510, T_c 567.80 K, P_c 2870 kPa, all labelled "KDB". |

## 3. Observation-level table

Units are as registered. "Dataset value" is the value in `DATA/octane_properties.csv` or `external/nonane_data.csv`. Classification labels: measured, calculated, extrapolated, compiled, conflicted, unverified (several may apply). Recommendation labels: retain, flag, exclude in a source-qualified sensitivity analysis (SQSA), correct.

### 3a. Items 1 to 3 and 5

| # | Molecule | CAS | Property, unit | T, reference state | Dataset value | Competing value(s) | Original publication of the dataset value | Classification | Recommendation |
|---|---|---|---|---|---|---|---|---|---|
| E1 | 4-methylheptane | 589-53-7 | S°, cal/(mol K) | 298.15 K, ideal gas, 1 bar (1947 tables: 1 atm; offset R ln 1.01325 = 0.026, negligible) | 109.32 | 108.35, Circular 461 Table 3p p. 159 (verified). 109.30, Milano set (Ediz Table 1, verified) | Not located. Agrees with the secondary octane QSPR datasets. NIST WebBook has no gas S°. Possibly Scott 1974 or the TRC tables (not verified) | compiled; conflicted (+0.97 against 1947); unverified | retain; flag; 1947 value in SQSA (exists) |
| E2 | 2,2-dimethylhexane | 590-73-8 | S°, cal/(mol K) | as E1 | 103.13 | 103.06, Table 3p (verified). 103.40, Milano set (verified) | Not located | compiled; unverified (within 0.07 of 1947; 0.27 from Milano) | retain; flag; SQSA (exists, both alternatives) |
| E3 | 3,4-dimethylhexane | 583-48-2 | S°, cal/(mol K) | as E1 | 106.59 | 104.38, Table 3p (verified). 106.60, Milano (verified) | Not located | compiled; conflicted (+2.21 against 1947, the largest gap); unverified | retain; flag; SQSA (exists) |
| E4 | 3-ethyl-2-methylpentane | 609-26-7 | S°, cal/(mol K) | as E1 | 106.06 | 105.43, Table 3p (listed as "2-Methyl-3-ethylpentane"; verified). 106.10, Milano (verified) | Not located | compiled; conflicted (+0.63); unverified | retain; flag; SQSA (exists) |
| E5 | 3-ethyl-3-methylpentane | 1067-08-9 | S°, cal/(mol K) | as E1 | 101.48 | 103.48, Table 3p ("3-Methyl-3-ethylpentane"; verified). 101.50, Milano (verified) | Not located | compiled; conflicted (exactly −2.00 against 1947); unverified | retain; flag; SQSA (exists). Check Scott 1974 for this isomer first (see note) |
| E6 | 2,3,3-trimethylpentane | 560-21-4 | S°, cal/(mol K) | as E1 | 102.06 (corrected in v40.5 from a duplicated 101.31) | 103.14, Table 3p (verified). 102.10, Milano (verified) | Mondal et al. 2019, arXiv:1906.06660, Table 2, as recorded in the repository (table not re-read here) | compiled; conflicted (−1.08); unverified | retain; flag; SQSA (exists) |
| T1 | 2,2,3,3-tetramethylbutane | 594-82-1 | ΔH_vap, kcal/mol | stated as 298 K, liquid to gas. The compound is a crystal at 298 K (T_triple 373.97 K), so a liquid at 298 K is hypothetical | 8.41 | 10.24, sublimation at 25 °C (Table 3m, p. 134, footnote b; verified). 7.56, liquid at T_b 379.45 K (Table 3m; verified). NIST ΔvapH° 42.94 kJ/mol = 10.26 (Majer and Svoboda 1985) and 42.91 (Osborne and Ginnings 1947, doi:10.6028/jres.039.031), both describing the crystal. ΔsubH° 43.37 ± 0.21 kJ/mol (Scott et al. 1952, doi:10.1021/ja01124a007). Estimates for the hypothetical liquid: 8.56 (ΔsubH − ΔfusH, no ΔCp correction) and 8.65 (Table 3m ratio extrapolation, this audit) | Milano octane set ("DHVAP 8.410", Ediz 2017 Table 1, verified). Original source not stated there and not located | unverified; most plausibly estimated or extrapolated for a hypothetical supercooled liquid; not a calorimetric liquid value | retain as registered; flag; exclusion and liquid-estimate variants in SQSA (exist); never substitute the 298 K NIST value (process mismatch) |
| W1 | 2,2,3,3-tetramethylbutane | 594-82-1 | acentric factor ω, dimensionless | defined from vapour pressure at T_r = 0.7 (about 397 K, real liquid) and P_c | 0.247 | 0.25529, Milano set (Ediz Table 1, verified; **not recorded in the repository**). 0.2510, KDB via Chemeo (verified). Exploratory estimate from KDB T_c and P_c, NIST T_b 379.6 K and ΔvapH 33.3 kJ/mol near T_b: 0.246, range 0.217 to 0.275 over T_c ± 2 K, P_c ± 0.5 bar, ΔvapH ± 1 kJ/mol | Not located | calculated quantity; compiled; conflicted between compilations (0.247 / 0.251 / 0.255, a spread of 0.008, well inside the propagated input uncertainty); source unverified | retain; correct the source description; add the Milano value to the SQSA |
| B1 | 3-ethyl-4-methylhexane | 3074-77-9 | normal boiling point, °C (registered 140.4) | 1 atm, liquid to vapour | 413.55 K | 407.15 K, NIST C500006531 ("d-3-ethyl-4-methylhexane"; same skeleton InChI; TRC uncertainty 2 K) from Lukes and Langthaler, Chem. Listy 51 (1957) 1869 (DOI not verified) | Fenske et al., Anal. Chem. 19 (1947) 700 to 765, doi:10.1021/ac60010a002 (TRC uncertainty 0.5 K). Page and table within the article not verified | measured; conflicted (two measurements 6.4 K apart). The competing value is a single enantiomer from a synthetic-chemistry paper with four times the TRC uncertainty | retain the registered value; flag; excluded and replaced scenarios in SQSA (exist); keep the exclusion from the pooled Test B as pre-registered (PREREG_v40 D5) |

### 3b. Item 4: nonane standard vaporisation enthalpies from compilations

Common fields for every row: property ΔvapH°, kJ/mol as listed by NIST and converted to kcal/mol (÷ 4.184); temperature 298.15 K; reference state liquid to gas at standard conditions (NIST "ΔvapH°"); NIST method "N/A"; classification **compiled** (the derivation of individual entries in the original compilations was not verified: measured, Clapeyron-derived from vapour-pressure equations, or increment-estimated); recommendation **retain; flag (already flagged as deviation D2); report the compiled-only and source-split analyses as exploratory**. "Competing value" is the secondary QSPR table of arXiv:2605.00044 as recorded in `external/nonane_crosscheck_secondary.csv`. That table was not re-verified here and is itself a compilation, so it is not independent. No calorimetric value exists on NIST for any of these 29 isomers.

| # | Molecule | CAS | NIST value (kJ/mol) | Dataset (kcal/mol) | Competing value | Compilation |
|---|---|---|---|---|---|---|
| N1 | 2-methyloctane | 3221-61-2 | 44.9 | 10.73 | 44.65 kJ/mol (diff 0.06 kcal/mol) | Wilhoit and Zwolinski 1971 (NIST label "Reid, 1972") |
| N2 | 3-methyloctane | 2216-33-3 | 44.9 | 10.73 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N3 | 4-methyloctane | 2216-34-4 | 44.5 | 10.64 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N4 | 3-ethylheptane | 15869-80-4 | 44.5 | 10.64 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N5 | 4-ethylheptane | 2216-32-2 | 44.1 | 10.54 | none matched uniquely | Labbauf et al. 1961 (doi:10.1021/je60010a023) |
| N6 | 2,2-dimethylheptane | 1071-26-7 | 42.3 | 10.11 | 42.28 (0.00) | Wilhoit and Zwolinski 1971 |
| N7 | 2,3-dimethylheptane | 3074-71-3 | 43.6 | 10.42 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N8 | 2,4-dimethylheptane | 2213-23-2 | 42.9 | 10.25 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N9 | 2,5-dimethylheptane | 2216-30-0 | 43.3 | 10.35 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N10 | 2,6-dimethylheptane | 1072-05-5 | 43.3 | 10.35 | 42.82 (0.12) | Wilhoit and Zwolinski 1971 |
| N11 | 3,3-dimethylheptane | 4032-86-4 | 42.6 | 10.18 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N12 | 3,4-dimethylheptane | 922-28-1 | 43.6 | 10.42 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N13 | 3,5-dimethylheptane | 926-82-9 | 43.3 | 10.35 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N14 | 4,4-dimethylheptane | 1068-19-5 | 42.2 | 10.09 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N15 | 3-ethyl-2-methylhexane | 16789-46-1 | 43.2 | 10.33 | none matched uniquely | Labbauf et al. 1961 |
| N16 | 3-ethyl-3-methylhexane | 3074-76-8 | 42.9 | 10.25 | 43.04 (0.04) | Labbauf et al. 1961 |
| N17 | 4-ethyl-2-methylhexane | 3074-75-7 | 42.9 | 10.25 | none matched uniquely | Labbauf et al. 1961 |
| N18 | 2,2,3-trimethylhexane | 16747-25-4 | 41.7 | 9.97 | 41.91 (0.05) | Wilhoit and Zwolinski 1971 |
| N19 | 2,2,4-trimethylhexane | 16747-26-5 | 40.7 | 9.73 | 40.57 (0.03) | Wilhoit and Zwolinski 1971 |
| N20 | 2,3,3-trimethylhexane | 16747-28-7 | 42.1 | 10.06 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N21 | 2,3,4-trimethylhexane | 921-47-1 | 42.7 | 10.21 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N22 | 2,4,4-trimethylhexane | 16747-30-1 | 41.1 | 9.82 | 40.84 (0.06) | Wilhoit and Zwolinski 1971 |
| N23 | 3,3,4-trimethylhexane | 16747-31-2 | 42.2 | 10.09 | 42.28 (0.02) | Wilhoit and Zwolinski 1971 |
| N24 | 3-ethyl-2,2-dimethylpentane | 16747-32-3 | 41.7 | 9.97 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N25 | 3-ethyl-2,3-dimethylpentane | 16747-33-4 | 42.7 | 10.21 | 42.55 (0.04) | Wilhoit and Zwolinski 1971 |
| N26 | 3-ethyl-2,4-dimethylpentane | 1068-87-7 | 42.3 | 10.11 | none matched uniquely | Wilhoit and Zwolinski 1971 |
| N27 | 2,2,3,3-tetramethylpentane | 7154-79-2 | 41.2 | 9.85 | 41 (0.05) | Wilhoit and Zwolinski 1971 |
| N28 | 2,2,3,4-tetramethylpentane | 1186-53-4 | 40.8 | 9.75 | 41 (0.05) | Wilhoit and Zwolinski 1971 |
| N29 | 2,3,3,4-tetramethylpentane | 16747-38-9 | 41.8 | 9.99 | 41.75 (0.01) | Wilhoit and Zwolinski 1971 |

For contrast, the five non-compiled nonane values are measured: n-nonane (NIST average of calorimetric determinations, 46.5 ± 0.2 kJ/mol); 2,2,5- and 2,3,5-trimethylhexane (Osborne and Ginnings 1947, calorimetric, doi:10.6028/jres.039.031); 3,3-diethylpentane (Fuchs and Peacock 1979) and 2,2,4,4-tetramethylpentane (Fuchs, Peacock et al. 1982), both calorimetric per NIST, DOIs not verified. 3-ethyl-4-methylhexane has no ΔvapH° on NIST and is correctly left missing.

## 4. Per-item notes

### Item 1. Six octane gas entropies (E1 to E6)

*What the sources show.* Table 3p of Circular 461 (printed p. 159) gives the gas entropies at 25 °C. I read all 18 from the PDF text layer and they match the repository's `S_API44` dictionary for the six isomers exactly. The same page shows that the 1947 edition is systematically superseded wherever a later primary or NIST value exists: n-octane 110.82 (1947) against 111.63 (NIST, from Scott 1974); 2,3,4-trimethylpentane 102.99 against 102.10 (NIST, Pitzer 1941); TMB 94.34 against 93.05 (NIST, Scott et al. 1952 calorimetry). Disagreeing with the 1947 table is therefore no evidence of error. All six values used agree with the Milano compilation (Ediz Table 1, one decimal) within 0.04, except 2,2-dimethylhexane (103.13 against 103.40). The Milano and Mondal datasets very probably share one lineage, so this agreement is corroboration between compilations and not primary verification. The NIST WebBook gas pages of all six were re-fetched and carry no S°.

*Most promising primary route, not completed.* Scott 1974 (doi:10.1063/1.1681500) states that it tabulates S°(298.15 K) "for all alkanes C3 to C10". It is the likely origin of the post-1947 values, but its tables were not accessible here. E5 (3-ethyl-3-methylpentane, 101.48 against 1947's 103.48, a difference of exactly 2.00) and E3 (3,4-dimethylhexane, +2.21) are the two entries to check first. The exact 2.00 offset fits either a genuine revision (for example a changed symmetry number or a different treatment of mixing entropy) or a units-digit transcription in the compiled dataset. This audit cannot tell which.

*Classification.* Compiled, unverified against a primary source; E1, E3, E4, E5 and E6 conflict with the 1947 edition by more than the 0.3 tolerance. These values are statistical-mechanical or correlation results in every edition, never direct measurements (only about 41 alkane entropies were experimental by 1974, according to Scott's abstract).

*Existing sensitivity analyses.* `entropy_api44_sensitivity_v41.csv` covers exactly this item and reproduces from the code: max |Δ|r|| = 0.018 (HM), with M1 ahead of HM by 0.004 (0.957 against 0.953). `entropy_source_sensitivity_v36.csv` covers the Milano alternatives for four entropies: max |Δ|r|| = 0.043 (ISI), with HM ahead of M1 by 0.007. Two further scenarios were added here, both exploratory. With the six excluded (n = 12), M1 0.978 leads HM 0.976, and |r| rises for most indices by up to 0.102 (ISI −0.593 to −0.695; ^mM2 0.863 to 0.943). With the full 1947 column for all 18 isomers, M1 0.964 leads χ 0.959, and HM 0.956 is third.

*Effect on conclusions.* None. main.tex:1524 to 1526 already declines to interpret the S ordering. The winner of the S column depends on the source in every scenario, which the manuscript states. Note that the `winner_changes` column of the v41 CSV is a column-level flag repeated on each row, not a per-index property.

*Recommendation.* Retain the registered values, keep the flag, and keep the 1947 substitution as the source-qualified sensitivity analysis. Optionally add the n = 12 exclusion line. Correct the wording at supplement.tex:916 to 917 (Section 7, R3).

### Item 2. TMB vaporisation enthalpy 8.41 kcal/mol (T1)

*Reference state.* The candidates were tested one at a time:
(a) Solid to gas at 298 K: 10.24 (1947, explicitly sublimation) and 10.26 (NIST "ΔvapH°", which equals ΔsubH° for the same Osborne and Ginnings measurement). Ruled out.
(b) Real liquid at or near T_b: 7.56 at 379.45 K (1947) and 7.96 at 383 K (NIST, Stephenson and Malanowski 1987). Ruled out.
(c) Hypothetical supercooled liquid at 298 K: ΔsubH°(298) − ΔfusH(373.9 K) = 43.37 − 7.54 = 35.83 kJ/mol = 8.56 kcal/mol. The ΔfusH attribution to Scott et al. 1952 is correct; NIST lists 7.540 kJ/mol for crystal I to liquid under that reference. A ΔCp(l − s) > 0 correction from 373.9 to 298 K lowers ΔfusH(298) and so raises this estimate. TMB phase I is a plastic crystal, so the correction is probably small, but it was not quantified. A second route: in Table 3m, ΔH(25 °C)/ΔH(T_b) for the other 17 isomers ranges from 1.133 to 1.186 and is close to linear in (T_b − 25 °C) (residual SD 0.009). Applied to 7.56 at T_b = 106.30 °C, it gives 8.65 kcal/mol (±2 SD: 8.51 to 8.79).
(d) A group-additivity estimate: possible, but no source located.

Conclusion: 8.41 is of the right magnitude for a hypothetical liquid but sits 0.15 to 0.24 kcal/mol (2 to 3 percent) below both reproducible estimates. Its origin is unknown. The value also equals, to within 0.01, the adjacent 2,2,4-trimethylpentane entry (8.40 in the dataset, 8.402 in the Milano set). A row-transfer error in the original compilation can be neither excluded nor confirmed, and this is mentioned only as an open possibility.

*Classification.* Unverified; most plausibly estimated or extrapolated (hypothetical liquid); not measured.

*Existing sensitivity analyses.* `tmb_dhvap_audit.csv` (correlations) and `dhvap_tmb_exclusion_summary_v36.csv` (matched-budget comparison: 93/100 and 96/100, medians +0.046 and +0.051) both reproduce. The extra variant added here (8.65) gives LO(0,0,1) |r| = 0.968 with LO(0,0,2) second at 0.959. The 10.26 substitution collapses every |r| to 0.374 or below, as the manuscript says, but it mixes two processes in one column and is not a valid alternative.

*Effect on conclusions.* None in the paper's framing: main.tex:1523 to 1524 already makes the ΔH_vap correlations conditional on a liquid-phase value, and no pre-registered test uses the value. One precision issue: with TMB excluded, LO(0,0,1) 0.9799 and LO(0,0,2) 0.9795 tie at three decimals, so "stays first" (main.tex:1520) and "the column leader is LO(0,0,1) in all four" (supplement.tex:954) claim a ranking that the manuscript's own rule (main.tex:1565) declines to make.

*Recommendation.* Retain 8.41 as the registered benchmark value; flag it; keep the exclusion and the hypothetical-liquid variants in the SQSA; do not substitute 10.26. Wording changes R2 and R4 below.

### Item 3. TMB acentric factor (W1)

*What the sources show.* KDB (via Chemeo) gives 0.2510, with T_c 567.80 K and P_c 2870 kPa. The Milano set, which the manuscript presents as the benchmark compilation, gives 0.25529. The value used, 0.247, was found in neither. Its source was not located. A rough check from KDB critical constants and NIST liquid data gives 0.246, but plausible input uncertainty spans 0.217 to 0.275, so the three compiled values cannot be told apart by calculation. ω is a derived quantity in every case.

*Wider observation.* Compared with the Milano column, five of the 18 ω values used differ at the third decimal: 3-ethyl-2-methylpentane 0.330 against 0.33243; 3-ethyl-3-methylpentane 0.302 against 0.30690; 2,2,3-trimethylpentane 0.300 against 0.30082; 2,3,3-trimethylpentane 0.291 against 0.29318; TMB 0.247 against 0.25529. Against KDB, only three of 18 match exactly (the repository's own classification). The ω column therefore matches neither cited compilation, and its source is unidentified.

*Existing sensitivity analyses.* `omega_source_sensitivity_v35.csv` (TMB 0.251, 2,2,4-trimethylpentane 0.303) reproduces: max shift 0.0032, M2 stays first. The Milano TMB value is not covered. Added here: TMB 0.2553 gives max shift 0.007, M2 0.986 first, HM 0.979 second. The full Milano ω column gives max shift 0.008, M2 0.986 first. TMB excluded: M2 0.981 first.

*Effect on conclusions.* None. The bolded ω entry (M2) is stable under every scenario.

*Recommendation.* Retain 0.247 as registered; correct the source description (R1); add the Milano value as a second alternative in the existing sensitivity analysis; describe the item as variation between compilations and not as a single "conflict".

### Item 4. Nonane vaporisation enthalpies from compilations (N1 to N29)

*What the sources show.* NIST lists, for each of these 29 isomers, a single ΔvapH° with method "N/A": 25 from the Wilhoit and Zwolinski handbook (shown as "Reid, 1972", which Crossref confirms is a one-page review, doi:10.1002/aic.690180637) and 4 from Labbauf et al. 1961 (doi:10.1021/je60010a023). A 1977 tabulation of the same 35 nonanes and 75 decanes exists (Somayajulu et al., doi:10.1021/je60073a021) and is not mentioned in the repository; its values were not seen. How the individual entries were derived could not be checked, because the 1961 and 1977 papers are paywalled. The supplement's statement that the 1961 tabulation "is not a set of individual calorimetric measurements" (supplement.tex:591 to 592) is plausible, since 110 compounds were treated in one three-page paper, but this audit did not verify it.

*Existing sensitivity analyses.* None. PREREG_v37 D2 states "No sub-analysis is added."

*Exploratory checks (this audit, no inferential weight).* (i) Counts-ridge leave-one-out residuals, reproducing the repository's Q² = 0.927: mean |residual| is 0.059 kcal/mol for the 29 compiled values and 0.120 kcal/mol for the 5 measured values. Four of the five measured residuals are negative. This fits the manuscript's caveat that compiled values may be smoother in structural increments, though n = 5 is very small. (ii) The registered GM against LO comparison on subsets:

| Subset | n | LO better (B = 200 / 500) | median ΔQ² | rule outcome |
|---|---|---|---|---|
| as registered (reproduced) | 34 | 95 / 98 | +0.048 / +0.053 | replicates |
| compiled values only | 29 | 77 / 75 | +0.021 / +0.019 | mixed |
| Labbauf rows removed | 30 | 88 / 94 | +0.038 / +0.045 | replicates |
| Wilhoit and Zwolinski rows only | 25 | 55 / 51 | +0.005 / +0.004 | mixed |

*Effect on conclusions.* None for the paper as written. The verdict is already qualified as compilation-grade (main.tex:1640 to 1645), shown to vanish in the wide box, and discounted as optimiser variance (main.tex:1651 to 1656). The table does show that the "replicates" label is not robust to provenance subsetting, which supports the authors' decision to treat it as non-primary.

*Recommendation.* Retain; keep the D2 flag; optionally report the compiled-only result as an exploratory sentence (R6); hedge or verify the "not a set of individual calorimetric measurements" sentence (R5).

### Item 5. Nonane boiling point of 3-ethyl-4-methylhexane (B1)

*What the sources show.* The archived NIST pages show two records with the same standard InChI (no stereo layer): C3074779 "Hexane, 3-ethyl-4-methyl-" with T_boil 413.55 K (Fenske et al. 1947, TRC uncertainty 0.5 K), and C500006531 "d-3-ethyl-4-methylhexane" with T_boil 407.15 K (Lukes and Langthaler 1957, TRC uncertainty 2 K). The second study concerns the degradation of optically active tertiary bases, so its sample was a single enantiomer of a compound with one stereocentre (C4). Enantiomers have identical normal boiling points, and any difference between racemate and pure enantiomer for a liquid alkane is far smaller than 6.4 K. The disagreement is therefore between two measurements of unequal quality. Taken alone, the TRC uncertainties favour the registered value.

*Classification.* Measured; conflicted.

*Existing sensitivity analyses.* `external/nonane_tb_conflict_out.txt` covers all three scenarios and its numbers match the supplement (supplement.tex:580 to 587): registered 58/63, ridge 0.682; excluded 55/60, ridge 0.679; 134.0 °C 61/66, ridge 0.647; verdict mixed in all three. PREREG_v40 D5 records the exclusion from the pooled Test B. The three-kelvin spread rule there correctly excludes the molecule regardless of which value is better.

*Effect on conclusions.* None. The verdict is mixed in every scenario, and the deviations table of the main paper (tab:deviations, main.tex:1805 to 1806) reports this.

*Recommendation.* Retain 413.55 K in the registered nonane data; keep the exclusion from Test B as pre-registered; keep both scenarios as the SQSA; add the stereochemical and uncertainty facts to the record (R7).

## 5. What the manuscript and README currently say

| Item | Location | Current content (paraphrase unless quoted) | Audit assessment |
|---|---|---|---|
| all octane items | main.tex:1510 to 1515 | Benchmark audited against NIST and API-44; "The open items are six entropies, the compiled acentric factors and the vaporisation enthalpy of 2,2,3,3-tetramethylbutane, which is crystalline at 298 K." | accurate |
| 2 | main.tex:1515 to 1524 | 8.41 "has no stated source and is consistent with a hypothetical supercooled liquid, for which sublimation minus fusion enthalpy gives about 8.56"; NIST 10.26 describes sublimation; LO(0,0,1) "stays first" excluded (0.980) and hypothetical (0.976); sublimation lowers every \|r\| to 0.374 or below; correlations conditional on a liquid value | numbers verified. "consistent with" slightly generous (8.41 is 2 to 3 percent below two estimates); "stays first" is a three-decimal tie in the excluded case. Units missing on 8.41, 8.56, 10.26 |
| 1 | main.tex:1524 to 1526 | entropies can move the 0.001 HM to M1 margin; S ordering not interpreted | accurate |
| 2 | main.tex:1588 to 1592 | 93/100 and 96/100 with TMB excluded | verified |
| 4 | main.tex:1640 to 1645 | 29 of 34 from Labbauf et al. and Wilhoit and Zwolinski; agreement "measures consistency with compiled values" | accurate |
| 1, 2, 3 | main.tex:1772 to 1775 | six entropies and compiled ω rest on secondary sources; TMB ΔH_vap reference state unresolved | accurate |
| 5 | main.tex:1805 to 1806 | second NIST T_B 6.4 K lower, still mixed | accurate |
| 3 | supplement.tex:186 to 188 | "Acentric factors, which NIST does not list, are the exception and were taken from KDB-derived compilations." | **not supported**: 15 of 18 do not match KDB exactly, 5 do not match the Milano set, and TMB matches neither |
| 1, 2, 3 | supplement.tex:209 to 230 | classification counts 3/29/40/10/7/1; six entropies differ from API-44 by 0.07 to 2.2; TMB "marginal conflict" 0.247 against 0.251; substitution moves M2 −0.988 to −0.986 | counts match the CSV; numbers verified; omits the Milano 0.255 |
| 1 | supplement.tex:244 to 255 | four entropies differ from a QSPR compilation by 0.04 to 2.29; up to 0.043; winner HM unchanged | verified |
| 2 | supplement.tex:549 to 563 | TMB exclusion 93/96, paired 95/96, medians +0.046 and +0.051, range −0.048 to +0.098 | verified against `dhvap_tmb_exclusion_summary_v36.csv` |
| 5 | supplement.tex:578 to 587 | Lukes and Langthaler 407.15 K, 6.4 K below; excluded 55/60, ridge 0.679; 134.0 °C 61/66, 0.647; mixed | verified; does not note the enantiomer or the TRC uncertainties |
| 4 | supplement.tex:587 to 596 | 4 of 34 calorimetric, one average, 29 from two compilations; 1961 tabulation "is not a set of individual calorimetric measurements"; "may rest partly on structural-increment estimates" | first claim verified from NIST; the "is not" sentence is unverified (paywalled) |
| 1 | supplement.tex:904 to 920 | thirteen entropies have no NIST S°; six unmatched; 1947 values differ by 0.07 to 2.2 "as that edition does for isomers whose later revisions we could confirm"; substitution: at most 0.018, M1 ahead by 0.004 | numbers verified; "later revisions we could confirm" overstates (matched only in secondary datasets) |
| 2 | supplement.tex:936 to 958 | full TMB trace; four variants; "The column leader is LO(0,0,1) in all four" | verified except the tie in the excluded variant |
| 3 | supplement.tex:959 to 963 | ω of 2,2,4-trimethylpentane and TMB differ from "an alternative compilation" by 0.002 to 0.004 | true for KDB; TMB differs from the Milano set by 0.008 |
| all | supplement.tex:964 to 971 | no item moves a correlation by more than 0.043 except the sublimation substitution | still true with the Milano ω (0.007) and the full 1947 S column (0.033) |
| all | DATA/README.md:24 to 34 | seven CANNOT VERIFY, one CONFLICT "(0.247 against a compiled 0.251)"; 3-ethyl-4-methylhexane note | accurate but incomplete (Milano ω; enantiomer) |
| 2 | TMB_DHVAP_AUDIT.md:41 to 47, 59 | "consistent with a hypothetical supercooled liquid"; "column leader is the same in every variant" | as for the manuscript |
| 4 | external/README_nonane_data.md (D2, Source label mapping) | Reid 1972 is a review of the Wilhoit and Zwolinski handbook | confirmed by Crossref |

## 6. Recommended manuscript and README changes

No registered benchmark value should be replaced. Every new analysis below is to be labelled exploratory and reported apart from the registered results.

### Submission-critical

**R1. Acentric-factor source statement (supplement.tex:186 to 188, with 225 to 226 and 959 to 963).** The current sentence names a source that 15 of the 18 values do not match exactly.
Replace "Acentric factors, which NIST does not list, are the exception and were taken from KDB-derived compilations." with:
> Acentric factors, which NIST does not list, are the exception. They are compiled values whose original source we could not identify. They agree with the KDB values (via Chemeo) and with the Milano octane set reproduced by Ediz~\cite{Ediz2017Octane} to within $0.005$, except for 2,2,3,3-tetramethylbutane, whose value ($0.247$) differs from both ($0.251$ in KDB, $0.255$ in the Milano set).

At supplement.tex:225 to 226, replace "One value is a marginal conflict, the acentric factor of 2,2,3,3-tetramethylbutane ($0.247$ vs.\ compiled $0.251$)" with "One value varies between compilations by more than the audit tolerance, the acentric factor of 2,2,3,3-tetramethylbutane ($0.247$ against $0.251$ in KDB and $0.255$ in the Milano set)".
At supplement.tex:959 to 963, append: "With the Milano value $0.255$ for 2,2,3,3-tetramethylbutane, no $\omega$ correlation moves by more than $0.007$ and $M_2$ remains first."
In DATA/README.md:27 to 28, replace "(0.247 against a compiled 0.251)" with "(0.247 against 0.251 in KDB and 0.25529 in the Milano octane set; source of 0.247 not located)". Add the Milano TMB value as a second alternative in `source_sensitivity.py` and record it in `octane_property_provenance_v35.csv`, noting that the result was max shift 0.007, M2 first.

### Should fix

**R2. Tie in the TMB-excluded ΔH_vap column (main.tex:1520 to 1521; supplement.tex:954; TMB_DHVAP_AUDIT.md:59).**
main.tex: replace "$LO(0,0,1)$ stays first with the isomer excluded ($|r| = 0.980$)" with "$LO(0,0,1)$ stays first or level with $LO(0,0,2)$ with the isomer excluded ($|r| = 0.980$ for both)".
supplement.tex:954: replace "The column leader is $LO(0,0,1)$ in all four." with "$LO(0,0,1)$ has the largest $|r|$ in all four, although with the isomer excluded it is level with $LO(0,0,2)$ at three decimals ($0.9799$ against $0.9795$)."

**R3. "Later revisions we could confirm" (supplement.tex:916 to 917; same phrase in the six `note` fields of `octane_property_provenance_v35.csv`).**
Replace "as that edition does for isomers whose later revisions we could confirm" with "as that edition does for isomers whose later values we could match in compiled octane datasets or in the NIST WebBook (for example $n$-octane $110.82$ against $111.63$, and 2,2,3,3-tetramethylbutane $94.34$ against $93.05$)". The n-octane and TMB figures were read from Table 3p and from NIST in this audit.

**R4. Strength of "consistent with a hypothetical supercooled liquid" and missing units (main.tex:1516 to 1519; supplement.tex:947 to 949; TMB_DHVAP_AUDIT.md:41 to 47).**
main.tex: replace "The benchmark value $8.41$ has no stated source and is consistent with a hypothetical supercooled liquid, for which sublimation minus fusion enthalpy gives about $8.56$. The NIST value of $10.26$ at $298$~K describes sublimation" with "The benchmark value $8.41$~kcal\,mol$^{-1}$ has no stated source. It is close to, but $2$ to $3$ percent below, two estimates for a hypothetical supercooled liquid at $298$~K ($8.56$ from sublimation minus fusion enthalpy and $8.65$ from the 1947 liquid value at the normal boiling point scaled as for the other isomers). The NIST value of $10.26$~kcal\,mol$^{-1}$ at $298$~K describes sublimation".
If the 8.65 estimate is adopted, add it to `tmb_dhvap_audit.py` as a fifth variant (result: LO(0,0,1) |r| = 0.968, LO(0,0,2) second at 0.959).

**R5. Unverified method claim for the 1961 compilation (supplement.tex:590 to 592).**
Replace "which covers all $35$ nonanes and $75$ decanes and is not a set of individual calorimetric measurements" with "which covers all $35$ nonanes and $75$ decanes in a single short paper and, as far as we could determine, does not report individual calorimetric measurements". Alternatively keep the sentence only after the authors have checked the 1961 paper's methods section. Optionally add: "A later tabulation of the same compounds exists (Somayajulu et al., J. Chem. Eng. Data 22 (1977) 229)."

**R7. Nature of the second 3-ethyl-4-methylhexane boiling point (supplement.tex:580 to 583; DATA/README.md:31 to 33).**
supplement.tex: after "(Lukes and Langthaler, 1957) under a separate entry," insert "for the dextrorotatory enantiomer prepared in a study of optically active amines, with a TRC-assigned uncertainty of $2$\,K against $0.5$\,K for the registered value; enantiomers share one normal boiling point, so the difference is a measurement discrepancy,".
DATA/README.md: append to the 3-ethyl-4-methylhexane note: "The second entry (C500006531) is for d-3-ethyl-4-methylhexane (Lukes and Langthaler 1957, TRC uncertainty 2 K; registered value TRC uncertainty 0.5 K)." Do not edit PREREG_v40.md, which is a frozen record. Put the note in the README or a change log.

### Optional

**R6. Compiled-only nonane ΔH_vap analysis (supplement, Section S4, after the sentence ending "rather than independent experimental validation").**
> In an exploratory analysis not covered by the protocol, the $\gamma$ comparison on the $29$ compiled values alone gave LO better in $77/100$ and $75/100$ seeds (median $\Delta Q^2 = +0.021$ and $+0.019$), which the registered rule would call mixed, and the count-based ridge baseline fitted the compiled values about twice as closely as the five measured ones (mean absolute residual $0.059$ against $0.120$~kcal\,mol$^{-1}$).

The script is `audit/final/scripts/nonane_calc.py`.

**R8. Entropy exclusion scenario (supplement.tex:919 to 920).** Append: "Excluding the six entropies instead ($n = 12$) puts $M_1$ ahead of $HM$ by $0.002$ ($0.978$ against $0.976$)."

**R9. Primary-source follow-up for E1 to E6.** Before or after submission, check the S°(298.15 K) table of Scott 1974 (doi:10.1063/1.1681500) or U.S. Bureau of Mines Bulletin 666 for the six isomers, starting with 3-ethyl-3-methylpentane (101.48 against 1947's 103.48) and 3,4-dimethylhexane (106.59 against 104.38). If they match, the classification can move from CANNOT VERIFY to verified against a correlation-based primary compilation. Values should change only if a primary source shows a transcription error.

**R10. Wording in the provenance CSV.** For TMB ω, change the classification label "CONFLICT" to "SOURCE VARIATION (compilations 0.247 / 0.251 / 0.255; source of value used not located)", or keep CONFLICT and add the Milano value to the note. Either is defensible, provided the README and the supplement use the same term.

## 7. Coverage matrix

| Item | Existing repo analysis | Reproduced | Covers the item fully? | Changes any paper conclusion? |
|---|---|---|---|---|
| 1 Six entropies | entropy_api44_sensitivity_v41.csv; entropy_source_sensitivity_v36.csv | yes (0.018; M1 +0.004 / 0.043; HM +0.007) | yes for substitution; exclusion not run (here: M1 +0.002) | no (S ordering not interpreted) |
| 2 TMB 8.41 | tmb_dhvap_audit.csv; dhvap_tmb_exclusion*_v36.csv | yes | yes; the 8.65 variant added here does not change the leader | no (correlations stated as conditional; no test uses it) |
| 3 TMB ω | omega_source_sensitivity_v35.csv | yes (max 0.003) | no: Milano 0.255 missing (here: max 0.007, M2 first) | no |
| 4 Nonane ΔH_vap compiled | none (PREREG_v37 D2: "No sub-analysis is added") | n/a | no (here: compiled-only verdict mixed) | no (verdict already discounted) |
| 5 3-ethyl-4-methylhexane T_B | nonane_tb_conflict_out.txt; PREREG_v40 D5 | numbers match the supplement | yes | no (mixed in all three scenarios) |
