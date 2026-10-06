# Pre-registration: external validation and baselines (v37)

Written 2026-10-03, before any nonane property value was collected or any
new analysis was run. Committed to git before results exist; later changes
to this plan must be recorded as deviations, not silent edits.

## Questions
- **Q1 (external replication).** On the 35 constitutional nonane isomers, does
  freeing gamma improve nested out-of-sample prediction of the properties
  available with primary-source data, relative to the optimized parent
  M_{alpha,beta}, under the identical protocol used for the octanes?
- **Q2 (baselines).** On octanes (and nonanes where data allow), how do GM and
  LO compare with: (a) a training-fold mean predictor; (b) each fixed
  established index in the paper's comparison set (one-descriptor OLS, the
  index chosen inside the training fold by inner LOO); (c) a simple imbalance
  aggregate IRLA(G) = 2 sum q_uv (one-descriptor OLS); (d) ridge regression
  on the full edge-degree-pair count vector, ridge penalty chosen by inner
  LOO inside each outer fold.

## Data rules (nonanes)
- Graphs: all 35 trees on 9 vertices with maximum degree <= 4, each matched to
  its IUPAC name and CAS number; identity checked by graph isomorphism.
- Properties: boiling point T_B (all 35 expected) and standard enthalpy of
  vaporization at 298.15 K (as available). Other properties only if a
  primary source covers at least 25 isomers.
- Every value must come from a fetched primary page (NIST WebBook preferred),
  recorded with URL, retrieval date, original value, units, conditions and
  conversion. A value that cannot be sourced is MISSING, never imputed or
  estimated. A property is analysed only if at least 25 isomers have values.
- Unit/precision policy fixed in advance: T_B in degC to 0.1; dHvap in
  kcal/mol (kJ/4.184) to 0.01; where several determinations exist, use the
  NIST-selected/average value if given, else the most recent calorimetric
  determination, recorded explicitly.

## Analysis (identical to the octane protocol; fixed now)
- Nested LOO: outer fold holds out one molecule; inside, candidates scored by
  inner-LOO RMSE of one-descriptor OLS; best candidate refit on the training
  fold; held-out molecule predicted. Q^2 = 1 - PRESS/SS_tot, RMSE.
- Candidate streams: seeds 0..99, budgets 200 and 500, LO triples U(-2,2)^3
  rounded to 3 dp drawn first, then GM pairs; paired control = LO candidates
  with gamma = 0.
- Primary outcome for Q1: number of seeds (of 100, per budget) with
  dQ^2 = Q^2_LO - Q^2_GM > 0, and median dQ^2, per property.

## Decision rules (fixed now)
- "Replicates" for a property: LO better in >= 80/100 seeds at both budgets
  AND median dQ^2 > 0 at both budgets. "Does not replicate": LO better in
  <= 50/100 at either budget. Otherwise "mixed".
- The manuscript will report the outcome for every analysed property,
  whatever it is, including a null or negative result for dHvap. No property,
  seed range, budget or protocol detail will be changed after results are seen.
- Baselines are reported in full; if ridge on degree-pair counts or a fixed
  index beats both GM and LO, the manuscript says so.
- All counts are optimizer-variance summaries on fixed datasets, not
  inferential tests; the manuscript keeps that wording.

## Deviations / clarifications (recorded 2026-10-03 after data collection, BEFORE any nonane analysis was run)
Data collection raised four situations the plan did not cover. Decisions
are fixed here before any nonane model was fitted:
- **D1 (T_B, 10 isomers without a NIST average):** the "most recent
  calorimetric" fallback does not apply to boiling points. Rule adopted: the
  most recent primary measurement listed by NIST, excluding handbook
  compilations (Weast & Grasselli 1989). All listed values are preserved in
  nonane_provenance.csv.
- **D2 (dHvap, 29 of 34 values):** the only NIST entry is from a compilation
  (Reid 1972: 25; Labbauf, Greenshields & Rossini 1961: 4), not a calorimetric
  determination. The dHvap analysis is run as pre-registered on the
  NIST-listed values, and the manuscript states that 29 of 34 values are
  compilation-grade. No sub-analysis is added.
- **D3 (precision):** 13 NIST T_B averages are quoted to whole kelvins; values
  are used as given and the reduced precision is stated.
- **D4 (2,3,3,4-tetramethylpentane T_B):** primary analysis uses the NIST
  average (413 +/- 6 K) as pre-registered; one sensitivity run replaces it by
  the median of the individual NIST points. Both are reported.
- dHvap is missing for 3-ethyl-4-methylhexane (no NIST entry): n = 34 for dHvap.
