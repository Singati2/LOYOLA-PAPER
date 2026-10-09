# Lean 4 verification of the mathematical statements

This file maps every numbered mathematical statement of the paper
*The Loyola Index Family and the Resolution Limit of Degree Imbalance*
(`main.tex`) to the Lean 4 theorems of `formal/` and says, for each one,
what is machine-checked and what is not. Build and check everything with

```
cd formal && ./verify.sh
```

which runs `lake build` (Lean `v4.34.1`, Mathlib `v4.34.1`), rejects any
`sorry`, `axiom` or `native_decide` in the sources, and confirms that every
theorem depends only on the standard axioms `propext`, `Classical.choice`
and `Quot.sound` (38 `#print axioms` checks: all 37 theorems of the development and the lemma `K13_degrees_in_range`). The modelling choices are in
`formal/README.md`: graphs enter as finite families or multisets of degree
pairs, degrees are positive reals, and `LO` is the sum of
`psi α β γ x y = (xy)^α (x+y)^β exp(γ |x-y|/(x+y))`.

## Statement by statement

| Paper | Statement | Lean | File | Status |
|---|---|---|---|---|
| Lemma 3.1 | affine independence of the imbalance direction (the augmented feature vectors span R^4 for Δ ≥ 3) | `det_W`, `det_W_ne_zero`, `witness_span`, `features_span` | `Independence.lean` | **partly formalised**: the spanning statement for every Δ ≥ 3; the identifiability consequence (θ = θ′, c = 1) and the Δ = 1, 2 dimension claims are not |
| Theorem 3.3 | global log-convexity of LO in (α, β, γ) | `logSumExp_convex` | `LogConvex.lean` | **partly formalised**: convexity of log LO; the gradient and Hessian formulas, the range of the slope and the strict-convexity criterion are not |
| Theorem 3.5 (ratio plane) | (i) on Π the index depends only on the q-histogram; (ii) pure-γ points separate exactly the q-histograms; (iii) colliding trees from order 13 (16 chemical) | order-13 profiles `P1`, `P2`: `P1_ne_P2`, `P1_P2_same_q`, `P1_P2_same_pure_gamma`, `P1_degree_consistent`, `P2_degree_consistent`, tree realisations | `Profiles.lean` | **partly formalised**: the order-13 collision (distinct profiles, equal q-histograms, equal pure-γ values, realised as trees) is checked; parts (i), (ii) (Lindemann–Weierstrass) and the pendant-path propagation are not; the minimality of orders 13 and 16 is computer-assisted, not a Lean proof: exhaustive enumeration of all trees of orders 2–16 in `structural/minimality_check.py` |
| Corollary 3.6 (degree-ratio indices) | every index of the form Σ f(min/max) depends only on the q-histogram | `one_sub_q_sq`, `q_only_direction` | `CauchySchwarz.lean` | identity `1 − q² = 4xy/(x+y)²` formalised; the corollary itself is a one-line consequence, not formalised |
| Proposition 3.8 | at rational exponents a nonzero algebraic γ never destroys a parent distinction | — | — | not formalised (Lindemann–Weierstrass is not in Mathlib) |
| Proposition 3.11 | γ-crossing bound by Laguerre's rule of signs | — | — | not formalised; the five-crossing witness is certified in 50-digit interval arithmetic by `structural/structural_checks.py` (block S3 of `structural_checks_out.txt`) and `audit/check_mathematics.py` |
| Proposition 3.13 | per-graph scale-invariant directions | `K13_gamma_absorbed` (illustration only: on K_{1,3} the γ term is absorbed into α) | `Counterexamples.lean` | not formalised as stated (exponential-family minimality); the Δ = 7 exception set is certified by `audit/check_mathematics.py` |
| Proposition 3.17 | limits along the γ axis | — | — | not formalised |
| Proposition 4.1 | degree-pair information ceiling on the octanes | — | — | not formalised (data statement); checked by `verify_loyola_v35.py` |
| Proposition 4.2 | generic discrimination of distinct profiles | — | — | not formalised (real-analytic zero sets) |
| Theorem 4.3 (imbalance restores weak discrimination), Example 4.4, Corollary 4.5 | at rational α, β with κ = 2α+β = p/r ∉ ℤ and algebraic γ ≠ 0, the edge weights are ℚ-independent iff Δ < 2^{r+1}; LO is then weakly discriminating | — | — | not formalised (Lindemann–Weierstrass and Besicovitch's theorem are not in Mathlib); Δ ≤ 4 exhaustively checked by `structural/weak_discrimination_check.py` |
| Proposition 5.1 | closed forms on standard graphs | — | — | not formalised; recomputed by `audit/check_mathematics.py` |
| Proposition 5.2 | path and star as extremal trees of the pure-γ points | — | — | not formalised; exhaustively checked for orders 4–12 by `structural/extremal_trees_check.py` |
| Proposition 5.4 (bracket bound) | m ψ_min ≤ LO ≤ m ψ_max | `ratio_bound`, `LO_ratio_bound` | `Bounds.lean` | **partly formalised**: the summation step is `ratio_bound` with h ≡ 1; the per-edge bounds ψ_min ≤ ψ_e ≤ ψ_max, and the extrema over the admissible pairs, enter as hypotheses |
| Corollary 5.5 (Cauchy–Schwarz interpolation) | LO at the midpoint of two parameter triples ≤ geometric mean | `psi_mul_psi_eq_sq`, `LO_le_sqrt_mul_sqrt`, `LO_le_sqrt_prod` | `CauchySchwarz.lean` | **formalised** (inequality) |
| Proposition 5.6 ((m, Δ) upper bound) | LO ≤ m Δ^{2α} (2Δ)^β e^{γ(Δ−1)/(Δ+1)} | `q_le_imbalance_max`, `psi_le_upper`, `LO_le_upper`, `LOm_le_upper` | `Bounds.lean` | **formalised** (inequality); equality case K_{1,Δ}: `K13_upper_attained`, `K13_degrees_in_range` for Δ = 3 |
| Proposition 5.7 ((m, δ) lower bound) | m δ^{2α} (2δ)^β ≤ LO | `lower_le_psi`, `lower_le_LO`, `lower_le_LOm` | `Bounds.lean` | **formalised** (inequality); `K2K3_lower_attained` shows the equality clause needs connectivity |
| Proposition 5.8 (ratio bound) and Corollary 5.9 | c_min Σh ≤ LO ≤ c_max Σh | `ratio_bound`, `LO_ratio_bound` | `Bounds.lean` | **formalised** |

Everything in Sections 4 and 6 (degeneracy counts, structure sensitivity,
the chemometric comparisons) is outside the Lean development and is
reproduced by the Python verifiers listed in `REPRODUCE.md`.

## Reading the Lean sources

* `Basic.lean`: definitions of `q`, `psi`, `LO`, `LOm`, `LOn`.
* `Bounds.lean`: the termwise bounds (Propositions 5.4 to 5.8).
* `CauchySchwarz.lean`: the interpolation inequality and the parent-family identity.
* `LogConvex.lean`: convexity of `log LO`.
* `Independence.lean`: the 4×4 determinant behind Lemma 1.
* `Profiles.lean`: the order-13 colliding tree pair of Theorem 3.5(iii).
* `Counterexamples.lean`: equality cases and the K_{1,3} absorption identity.
* `AxiomCheck.lean` and `expected_axiom_theorems.txt`: the list of theorems whose axioms are checked.
