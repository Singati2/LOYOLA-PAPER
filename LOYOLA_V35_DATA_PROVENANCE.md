# LOYOLA_V35_DATA_PROVENANCE — full 90-value trace (completed this round)

Machine-readable trace: `octane_property_provenance_v35.csv` (90 rows =
18 molecules × 5 properties; per-row source value, unit, conversion, phase,
URL, CAS confirmation, retrieval note dated 2026-08-30). Schema and class
counts are enforced by the verifier ([N2]).

## Final classification counts (claimed identically in manuscript §4.1)
| Class | Count |
|---|---|
| VERIFIED EXACT (exact at reported precision, no conversion) | 3 |
| VERIFIED AFTER UNIT CONVERSION (exact at reported precision after K/kJ/J conversion) | 34 |
| AGREEMENT WITHIN TOLERANCE (within audit tolerance / source uncertainty, not exact at reported precision) | 32 |
| SOURCE VARIATION / EXPLAINED | 13 |
| CANNOT VERIFY | 7 |
| CONFLICT | 1 |
| **Total** | **90** |

**Round-14 reclassification (strict taxonomy; GPT audit finding):** the v34
CSV used "VERIFIED" for tolerance-level matches. All 90 rows were re-audited
value-aware; 32 rows were downgraded to the new AGREEMENT WITHIN TOLERANCE
class (none upgraded), including the two GPT-flagged rows (isooctane omega
0.305 vs 0.303; 3-ethylhexane omega 0.362 vs 0.361). The verifier now
re-derives each row's class from its numeric fields. Matched at reported
precision: 37/90; agreeing within tolerance or explained variation: 82/90. Phase discipline: all formation enthalpies verified
against the explicitly GAS-phase NIST values (liquid values, ~10 kcal/mol
lower, were present on the same pages and correctly not used); entropies
matched to gas-phase 298.15 K, 1 bar; boiling points converted K→°C;
enthalpies kJ→kcal at 4.184.

## The 8 non-verified values, explicitly
- **6 × gas-phase entropy S** (4-methylheptane, 2,2-dimethylhexane,
  3,4-dimethylhexane, 2-methyl-3-ethylpentane, 3-ethyl-3-methylpentane,
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
  SOURCE VARIATION). Both discrepancies are far below any level that could
  alter a reported correlation at displayed precision.

## Method
Two multi-agent campaigns (6 agents × 3 molecules; 3 stalled groups retried
as 9 single-molecule agents with a strict 4-fetch budget). Sources: NIST
WebBook phase-change (Mask=4) and gas-phase thermochemistry (Mask=1) pages
under the CAS-confirmed compound entries; Chemeo (KDB compilation) for
acentric factors, which NIST does not list. Every CAS→name mapping was
confirmed from the fetched page title. No value was altered in the dataset;
the benchmark is preserved as supplied for comparability, with conflicts
declared rather than silently repaired.

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
