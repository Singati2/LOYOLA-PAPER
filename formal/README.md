# Lean 4 formalization of key results of the Loyola-index paper

Lean `leanprover/lean4:v4.34.1`, Mathlib tag `v4.34.1` (prebuilt oleans via `lake exe cache get`).
Build and check: `./verify.sh` (runs `lake build`, greps the sources for `sorry`/`axiom`/
`native_decide`, and checks that every `#print axioms` line lists only
`propext`, `Classical.choice`, `Quot.sound`). Current status: builds cleanly, no `sorry`, no
warnings, 36 `#print axioms` checks all clean.

## Modelling choices (read this first)

* `q x y = |x - y| / (x + y)`, `psi α β γ x y = (x*y)^α * (x+y)^β * exp (γ * q x y)` with
  `Real.rpow` (`LoyolaFormal/Basic.lean`).
* **Graphs are abstracted to degree data.** No `SimpleGraph` is used. An edge set is either
  - a `Finset ι` of edges with a degree map `d : ι → ℝ × ℝ` (`LO α β γ s d = Σ_{e∈s} ψ(d e)`);
    a graph instantiates this with `ι = Sym2 V`, `s = G.edgeFinset`, `d uv = (deg u, deg v)`, or
  - a `Multiset (ℝ × ℝ)` of degree pairs (`LOm`), or a `Multiset (ℕ × ℕ)` cast to `ℝ` (`LOn`).
  Hypotheses such as "max degree Δ" or "min degree δ" are therefore stated as bounds on the
  degree pairs; the combinatorial link "these numbers are the vertex degrees of a graph" is
  not formalized (except the explicit tree realisations in L10, see below).
* Degrees are arbitrary positive reals in the analytic results (more general than integers).

## Theorem map

| Item | Lean name (file) | Manuscript |
|---|---|---|
| L1 | `Loyola.q_le_imbalance_max` (Bounds) | imbalance maximum used in `thm:upper_Delta` |
| L2 | `psi_le_upper`, `LO_le_upper`, `LOm_le_upper` (Bounds); constant `upperConst` | `thm:upper_Delta` (inequality) |
| L3 | `lower_le_psi`, `lower_le_LO`, `lower_le_LOm` (Bounds); constant `lowerConst` | `thm:lower_delta` (inequality) |
| L4 | `psi_mul_psi_eq_sq`, `LO_le_sqrt_mul_sqrt`, `LO_le_sqrt_prod` (CauchySchwarz) | `thm:cs` (inequality) |
| L5 | `ratio_bound`, `LO_ratio_bound` (Bounds) | `thm:ratio_bound` (inequality; also the bracket form of `thm:bracket` with `h ≡ 1`) |
| L6 | `one_sub_q_sq`, `q_only_direction` (CauchySchwarz) | parent-family identity `1 - q² = 4xy/(x+y)²`, `(xy)^α (x+y)^(-2α) = 4^(-α)(1-q²)^α` |
| L7 | `K13_gamma_absorbed` (Counterexamples) | counterexample: on `K_{1,3}`, `LO(α,β,γ) = LO(α+γ/(2 log 3), β, 0)` |
| L8 | `K13_upper_attained`, `K13_degrees_in_range` (Counterexamples) | counterexample: `thm:upper_Delta` is attained (`K_{1,3}`, Δ=3, α=β=0, all γ) |
| L9 | `K2K3_lower_attained` (Counterexamples) | counterexample to the equality clause of `thm:lower_delta` (see caveat) |
| L10 | `P1_ne_P2`, `P1_card`, `P2_card`, `P1_eq_replicates`, `P2_eq_replicates`, `P1_P2_same_qN`, `P1_P2_same_q`, `P1_P2_same_pure_gamma`, `P1_degree_consistent`, `P2_degree_consistent`, `par1_valid`, `par2_valid`, `tree1_profile`, `tree2_profile`, `trees_same_degree_sequence` (Profiles) | pure-γ floor break at tree order 13 |
| L11 | `logSumExp_convex` (LogConvex) | `thm:logconvex` (convexity of `log LO` in θ) |
| L12 | `det_W`, `det_W_ne_zero`, `witness_span`, `features_span` (Independence) | `prop:indep` (spanning statement, every Δ ≥ 3) |

### Precise statements of the less obvious items

* **L2/L3 summed**: `LO_le_upper : LO α β γ s d ≤ s.card * upperConst α β γ Δ` assuming
  `α,β,γ ≥ 0` and `1 ≤ d_e.1, d_e.2 ≤ Δ` on `s`; `lower_le_LO : s.card * lowerConst α β δ ≤ LO`
  assuming `δ > 0` and `δ ≤ d_e.1, d_e.2`.
* **L4**: `α₁+α₂ = 2α, β₁+β₂ = 2β, γ₁+γ₂ = 2γ` and positive degrees on `s` give
  `LO α β γ s d ≤ √(LO α₁ β₁ γ₁ s d) * √(LO α₂ β₂ γ₂ s d)` (via `Real.sum_mul_le_sqrt_mul_sqrt`).
* **L5**: for any real weights `ψ`, positive `h`, and `cmin ≤ ψ_e/h_e ≤ cmax` on `s`:
  `cmin·Σh ≤ Σψ ∧ Σψ ≤ cmax·Σh`.
* **L8**: `LOm 0 0 γ K13 = 3·exp(γ·((3-1)/(3+1)))` and `= card K13 · upperConst 0 0 γ 3`;
  `K13_degrees_in_range` shows the hypotheses of `LOm_le_upper` hold with Δ = 3, so this is an
  equality case of L2.
* **L9**: for `{(1,1),(2,2),(2,2),(2,2)}`: `LOm 0 0 1 = 4 = card · lowerConst 0 0 1`, all
  degrees ≥ 1, and the vertex-degree multiset `{1,1,2,2,2}` is not constant.
  **Caveat:** `K₂ ∪ K₃` is *disconnected*. `thm:lower_delta` is stated for connected graphs,
  and for connected graphs "every edge has equal endpoint degrees" does force regularity, so
  this example refutes the equality clause only if connectivity is dropped (as in the
  manuscript's degree-pair-only reading). Whether the clause fails for some *connected* graph
  is not addressed here.
* **L10**: `P1`, `P2 : Multiset (ℕ × ℕ)` (pairs written smaller-degree-first).
  Proved: `P1 ≠ P2`; both have card 12; the multisets of reduced fractions `q = num/den`
  coincide (`P1_P2_same_qN`, kernel `decide`), hence the multisets of rational `q` values
  coincide (`P1_P2_same_q`), hence `LOn 0 0 γ P1 = LOn 0 0 γ P2` for every real γ.
  *Degree consistency (profile only)*: with `endpoints k P` = number of edge endpoints of
  degree `k`, every endpoint degree lies in `{1,2,3,6}`, `k ∣ endpoints k P` for each such `k`,
  `(n₁,n₂,n₃,n₆) = (8,2,2,1)` for both profiles, `Σ n_k = 13`, and `card P + 1 = 13`
  (edge count of a 13-vertex tree).
  *Realisability*: explicit parent arrays `par1`, `par2` (vertex `i+1` joined to
  `par[i] ≤ i`, vertices `0..12`) whose degree-pair profiles are exactly `P1` and `P2`
  (`tree1_profile`, `tree2_profile`), with the same vertex degree sequence. That a parent
  array with `par[i] ≤ i` defines a tree is the standard fact (connected, `n-1` edges); it is
  not re-derived via `SimpleGraph.IsTree`.
* **L11**: for `s.Nonempty` and any `z : ι → Fin n → ℝ`,
  `ConvexOn ℝ univ (fun θ => log (Σ_{e∈s} exp (θ ⬝ᵥ z e)))`, proved from Hölder
  (`Real.inner_le_Lp_mul_Lq_of_nonneg`). Holds for every `n`, in particular `n = 3`.
* **L12**: `W` is the 4×4 matrix of `feat i j = (1, log(ij), log(i+j), q i j)` for
  `(1,1),(2,2),(1,2),(1,3)`; `det W = log 2 · (8 log 3 − 13 log 2)/6` and it is nonzero since
  `3^8 = 6561 < 8192 = 2^13` (no decimal bounds on logs needed). Hence for every `Δ ≥ 3`,
  `span ℝ (feat '' {(i,j) | 1 ≤ i ≤ j ≤ Δ}) = ⊤` in `Fin 4 → ℝ`.

## Not formalized

* All **equality characterizations** ("equality iff ...") in `thm:upper_Delta`,
  `thm:lower_delta`, `thm:cs`, `thm:ratio_bound`, `thm:bracket`. Only the inequalities are
  proved; L8/L9 are explicit equality instances.
* The gradient/Hessian formulas and the strict-monotonicity / zero-variance statements in
  `thm:logconvex` (only convexity is proved).
* In `prop:indep`: the identifiability corollary (`θ = θ'`, `c = 1`) and the Δ = 1, 2
  dimension claims (only the Δ ≥ 3 spanning statement is proved).
* The graph layer: no `SimpleGraph`, connectivity, or degree-sum combinatorics; graphs enter
  only through their degree-pair multisets (plus the explicit tree certificates of L10).
* The other results of the paper (closed forms, `thm:m1_bound`, `thm:R_chi`, `thm:sombor`,
  `prop:collision`, `prop:generic`, the empirical sections).
