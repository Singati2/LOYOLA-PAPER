# V34 → V35 scientific changelog (round-14 GPT audit → repair)

Every round-14 finding was REPRODUCED before repair, per the prompt's rule.

## 1. Predictive-robustness conclusion corrected (the material repair)
- GPT's counterexample reproduced EXACTLY: seed 2, budget 200, ΔH_vap:
  Q²_GM = 0.8707455, Q²_LO = 0.8611587, ΔQ² = −0.0095868 (all 7 decimals).
- Expanded analysis run: seeds 0–99 × budgets {200, 500} (1000 nested
  configurations; expanded_robustness_v35.csv + summary). GPT's counts
  reproduced exactly: ΔH_vap improved 91/100 (budget 200) and 93/100 (500);
  ΔH_f degraded 86/100 and 76/100.
- Same-(α,β) paired control added (LO candidates vs the same candidates with
  γ zeroed): ΔH_vap 93/100 better at both budgets — the tendency is γ's,
  not an artifact of independent candidate streams; but it is NOT
  sign-invariant.
- All "robustly/exactly one/consistently" formulations replaced (abstract,
  intro, §ablation, conclusion) with the descriptive-tendency language
  ("usually improved … usually degraded …, neither direction sign-invariant;
  descriptive tendencies, not inferential evidence"). Primary seed-12345
  table retained, labeled as the primary configuration.

## 2. Acentric-factor sensitivity statement corrected (v34 statement was false)
- Reproduced GPT's numbers exactly: substituting ω = 0.303 (isooctane) and
  0.251 (tetramethylbutane) moves M₂/ω from −0.987602 to −0.985664
  (displayed −0.988 → −0.986); 8 of 12 ω correlations change at the third
  decimal; the property-wise winner (M₂) does not change.
- Manuscript sentence replaced accordingly; omega_source_sensitivity_v35.csv
  added and live-recomputed by the verifier. Benchmark values preserved as
  supplied (not silently replaced).

## 3. Provenance reclassified under a strict explicit taxonomy
- "VERIFIED EXACT" now means exact at reported precision without conversion;
  a new class AGREEMENT WITHIN TOLERANCE holds values that agree within the
  audit tolerances/source uncertainty but not at reported precision.
- Value-aware audit of all 90 rows (32 rows downgraded, none upgraded; the
  two GPT-flagged rows — isooctane ω and 3-ethylhexane ω — moved out of
  EXACT). New counts: **3 exact / 34 unit-conversion / 32 within-tolerance /
  13 source-variation / 7 cannot-verify / 1 conflict.** Manuscript §4.1,
  provenance CSV (renamed _v35), docs and verifier all updated; the verifier
  now re-derives the classification from the row values (value-aware), not
  just the label counts.

## 4. Mathematical boundary corrected
- prop:indep: "for Δ≤2 the span has dimension 3" was FALSE at Δ=1 (single
  pair (1,1), augmented vector (1,0,ln2,0), rank 1). Statement and proof now
  give rank 1 / 3 / 4 for Δ = 1 / 2 / ≥3; verifier enforces all three ranks.
  The principal Δ≥3 result is unchanged.

## 5. Retired proxy figure removed
- fig_lo_structure_sensitivity_decanes_v3.pdf (σ/μ proxy labeled "structure
  sensitivity") removed from figures/, generator, and manifest; generator
  docstring corrected (stale v29 text; now "two manuscript figures"); the
  proxy CSV is retained, documented as a legacy normalized-dispersion
  artifact; verifier rejects any manuscript reference to the retired figure.
- FGD table values and the published control (10/14 exact, 4 within 1 unit)
  unchanged.

## 6. Consistency cleanup
- Appendix data table "3-methyl-3-ethylpentane" → "3-ethyl-3-methylpentane".
- Collision text now notes the alphabetized IUPAC form 3-ethyl-2-
  methylpentane (SMILES/structures/collision classes unchanged).
- Changelog test-count corrected (83, now 87 after the new attacks).
- Stale v29/v32 references in script docstrings fixed.
- Barman–Das bibliography entry checked: no duplicated fragment found in
  this copy (duplicate-line scan clean); reported as not-reproduced.

## Verification
verify_loyola_v35.py FULL PASS exit 0 (adds: Δ-rank checks, value-aware
provenance rules, expanded-robustness and ω-sensitivity CSV checks incl. the
seed-2 counterexample row, retired-proxy guard); selftest **87 tests** all
rejected for the intended reason, exit 0.
