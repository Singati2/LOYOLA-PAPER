# LOYOLA DATA PROVENANCE — full 90-value trace (v35, revised in v36)

Machine-readable trace: `octane_property_provenance_v35.csv` (90 rows =
18 molecules × 5 properties; per-row source value, unit, conversion, phase,
URL, CAS confirmation, retrieval note dated 2026-08-30). Schema and class
counts are enforced by the verifier ([N2]).

## v36 revisions (supersede the v35 statements below where they conflict)
- **Four ΔH_vap values corrected** to the NIST WebBook (identical to the
  standard octane dataset, arXiv:1701.02859 Table 1, at 2 dp):
  3,3-dimethylhexane 9.04→8.97; 3-ethyl-3-methylpentane 9.21→9.08;
  2,2,3-trimethylpentane 8.88→8.83; 2,3,3-trimethylpentane 9.02→8.90.
  All four rows are now VERIFIED AFTER UNIT CONVERSION ("corrected in v36"
  in the CSV note). The data live only in `octane_data.py`.
- **Reclassified** (recorded value does not match at reported precision):
  2,3,4-trimethylpentane S (102.39 vs 427.2/4.184 = 102.10), 3,4-dimethylhexane
  ω (0.340 vs 0.338), 2,5-dimethylhexane ΔH_f (−53.21 vs −53.20) and
  2,3,4-trimethylpentane ΔH_f (−51.97 vs −51.96): VERIFIED → AGREEMENT WITHIN
  TOLERANCE. 2,2-dimethylhexane ΔH_vap (8.92 inside the recorded 8.913–8.930
  span) AGREEMENT → VERIFIED (v35 mis-parsed "8.913-8.930" as containing a
  negative number). The verifier's parser now removes parenthetical working
  before reading numbers (v35 treated e.g. "(427.2/4.184)" as a range), checks
  that every paper_value equals the dataset, and uses PROV_TOL(ΔH_vap) = 0.04.
- **Recount:** 3 / 34 / 32 / 13 / 7 / 1 — the totals are unchanged, but the
  composition is different (4 rows left the verified classes, 4 entered, and
  the 2,2,3-trimethylpentane ΔH_vap row stays verified only after correction).
- **Name:** 2-methyl-3-ethylpentane is now listed under its IUPAC name
  3-ethyl-2-methylpentane (same compound, SMILES CCC(CC)C(C)C).
- **ω statement corrected:** the ω discrepancies DO alter reported
  correlations at displayed precision: substituting the compiled values
  (0.303, 0.251) changes 8 of the 12 ω correlations at the third decimal
  (e.g. M₂ −0.988 → −0.986; `omega_source_sensitivity_v35.csv`); the
  winning descriptor (M₂) is unchanged.
- **Entropy sensitivity (disclosure only; data not changed):** four S values
  cannot be matched to a primary source and differ from the standard octane
  dataset (octane 111.55 vs 111.70; 2,2-dimethylhexane 103.13 vs 103.40;
  2,2,4-trimethylpentane 101.81 vs 104.10; 2,3,3-trimethylpentane 101.31 vs
  102.10). Substituting them changes all 12 S correlations at the third
  decimal (max |Δr| = 0.034); the winner (HM) is unchanged
  (`entropy_source_sensitivity_v36.csv`, `source_sensitivity.py`).
  **Flag for the authors:** the 2,3,3-trimethylpentane S value 101.31 is
  identical to the 2,2,3-trimethylpentane value — a possible copy error in
  the compiled table that should be checked against the original source.

## Final classification counts (claimed identically in manuscript §5.1)
| Class | Count |
|---|---|
| VERIFIED EXACT (exact at reported precision, no conversion) | 3 |
| VERIFIED AFTER UNIT CONVERSION (exact at reported precision after K/kJ/J conversion) | 34 |
| AGREEMENT WITHIN TOLERANCE (within audit tolerance / source uncertainty, not exact at reported precision) | 32 |
| SOURCE VARIATION / EXPLAINED | 13 |
| CANNOT VERIFY | 7 |
| CONFLICT | 1 |
| **Total** | **90** |

**Round-14 reclassification (strict taxonomy; external audit finding):** the v34
CSV used "VERIFIED" for tolerance-level matches. All 90 rows were re-audited
value-aware; 32 rows were downgraded to the new AGREEMENT WITHIN TOLERANCE
class (none upgraded), including the two audit-flagged rows (isooctane omega
0.305 vs 0.303; 3-ethylhexane omega 0.362 vs 0.361). The verifier now
re-derives each row's class from its numeric fields. Matched at reported
precision: 37/90; agreeing within tolerance or explained variation: 82/90. Phase discipline: all formation enthalpies verified
against the explicitly GAS-phase NIST values (liquid values, ~10 kcal/mol
lower, were present on the same pages and correctly not used); entropies
matched to gas-phase 298.15 K, 1 bar; boiling points converted K→°C;
enthalpies kJ→kcal at 4.184.

## The 8 non-verified values, explicitly
- **6 × gas-phase entropy S** (4-methylheptane, 2,2-dimethylhexane,
  3,4-dimethylhexane, 3-ethyl-2-methylpentane, 3-ethyl-3-methylpentane,
  2,3,3-trimethylpentane): the NIST WebBook gas-thermochemistry pages for
  these isomers list no S°(gas); no authoritative alternative was reachable
  within the agents' fetch budgets. CANNOT VERIFY, not contradicted.
- **ΔH_vap(298 K) of 2,2,3,3-tetramethylbutane**: the compound is a solid at
  room temperature (m.p. ≈ 100 °C); NIST tabulates a sublimation enthalpy
  (~42.9 kJ/mol), not a 298 K liquid-vaporization value. CANNOT VERIFY as a
  vaporization datum; flagged in-text.
- **ω of 2,2,3,3-tetramethylbutane**: paper 0.247 vs KDB 0.251 (diff 0.004,
  marginally outside the 0.003 tolerance). CONFLICT (marginal); flagged
  in-text together with the isooctane ω variance (0.305 vs 0.303, classified
  AGREEMENT WITHIN TOLERANCE). [v36 correction: these discrepancies DO change
  8 of 12 ω correlations at the third decimal (see the v36 section above);
  the winning descriptor is unchanged.]

## Method
Two multi-agent campaigns (6 agents × 3 molecules; 3 stalled groups retried
as 9 single-molecule agents with a strict 4-fetch budget). Sources: NIST
WebBook phase-change (Mask=4) and gas-phase thermochemistry (Mask=1) pages
under the CAS-confirmed compound entries; Chemeo (KDB compilation) for
acentric factors, which NIST does not list. Every CAS→name mapping was
confirmed from the fetched page title. In v35 no value was altered; in v36
exactly four ΔH_vap values were corrected to NIST (see the v36 section);
all other values are preserved as supplied for comparability, with
conflicts declared rather than silently repaired.

## Identity fields
Names ↔ SMILES: all 18 independently re-derived from the SMILES (v33 round,
[P] parser audit re-checks structure validity and pairwise distinctness on
every verifier run). CAS numbers: confirmed via the fetched NIST page names
(recorded per-row in the CSV). InChIKeys: NOT generated (no RDKit in this
environment) — declared.

## Bibliography and remaining CANNOT VERIFY
Unchanged from v33 (39/39 verified references; AKCE 2020 original
formulation and Portilla JMC 2025 full text remain paywalled; LaTeX compile
remains the author's Overleaf step).
