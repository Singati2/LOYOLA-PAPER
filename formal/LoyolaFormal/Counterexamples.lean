import LoyolaFormal.Bounds

/-!
# Counterexamples on small graphs (L7, L8, L9)

Graphs are given by their multisets of edge degree pairs.
-/

noncomputable section

open Real

namespace Loyola

/-- Degree-pair multiset of the star `S₄ = K_{1,3}`: three edges with degree pair `(1,3)`. -/
def K13 : Multiset (ℝ × ℝ) := Multiset.replicate 3 (1, 3)

lemma LOm_K13 (α β γ : ℝ) : LOm α β γ K13 = 3 * psi α β γ 1 3 := by
  simp [LOm, K13]; ring

lemma q_one_three : q 1 3 = 1 / 2 := by
  unfold q; norm_num [abs_of_neg]

/-- **L7** (γ is absorbed by α on `K_{1,3}`): for all `α β γ`,
`LO(K_{1,3}; α, β, γ) = LO(K_{1,3}; α + γ/(2 log 3), β, 0)`. -/
theorem K13_gamma_absorbed (α β γ : ℝ) :
    LOm α β γ K13 = LOm (α + γ / (2 * Real.log 3)) β 0 K13 := by
  rw [LOm_K13, LOm_K13]
  congr 1
  unfold psi
  have hl : Real.log 3 ≠ 0 := (Real.log_pos (by norm_num : (1:ℝ) < 3)).ne'
  have key : (3:ℝ) ^ (γ / (2 * Real.log 3)) = Real.exp (γ * (1 / 2)) := by
    rw [Real.rpow_def_of_pos (by norm_num)]
    congr 1
    field_simp
  rw [q_one_three, show (1:ℝ) * 3 = 3 by norm_num,
    Real.rpow_add (by norm_num : (0:ℝ) < 3), key]
  simp
  ring

/-- **L8** (the upper bound of `thm:upper_Delta` is attained): on `K_{1,3}` with `Δ = 3`,
`α = β = 0` and every `γ`, `LO = 3·exp(γ(3-1)/(3+1)) = m · upperConst`. -/
theorem K13_upper_attained (γ : ℝ) :
    LOm 0 0 γ K13 = 3 * Real.exp (γ * ((3 - 1) / (3 + 1))) ∧
    LOm 0 0 γ K13 = (Multiset.card K13 : ℝ) * upperConst 0 0 γ 3 := by
  have h1 : LOm 0 0 γ K13 = 3 * Real.exp (γ * ((3 - 1) / (3 + 1))) := by
    rw [LOm_K13]; unfold psi; rw [q_one_three]; norm_num
  refine ⟨h1, ?_⟩
  rw [h1]; simp [K13, upperConst]

/-- The hypotheses of `LOm_le_upper` hold for `K_{1,3}` with `Δ = 3`, so `K13_upper_attained`
is genuinely an equality case of `thm:upper_Delta`. -/
lemma K13_degrees_in_range : ∀ p ∈ K13, 1 ≤ p.1 ∧ 1 ≤ p.2 ∧ p.1 ≤ 3 ∧ p.2 ≤ 3 := by
  intro p hp
  simp only [K13, Multiset.mem_replicate] at hp
  rw [hp.2]; norm_num

/-- Degree-pair multiset of `K₂ ∪ K₃` (one edge `(1,1)`, three edges `(2,2)`). -/
def K2K3 : Multiset (ℝ × ℝ) := {(1, 1), (2, 2), (2, 2), (2, 2)}

/-- Vertex-degree multiset of `K₂ ∪ K₃`. -/
def K2K3_degrees : Multiset ℕ := {1, 1, 2, 2, 2}

/-- **L9** (`K₂ ∪ K₃` attains the lower bound of `thm:lower_delta` without being regular):
with `δ = 1`, `(α,β,γ) = (0,0,1)`: `LO = 4 = m · δ^0 (2δ)^0`, while the vertex degree
multiset `{1,1,2,2,2}` is not constant. -/
theorem K2K3_lower_attained :
    LOm 0 0 1 K2K3 = 4 ∧
    LOm 0 0 1 K2K3 = (Multiset.card K2K3 : ℝ) * lowerConst 0 0 1 ∧
    (∀ p ∈ K2K3, (1:ℝ) ≤ p.1 ∧ (1:ℝ) ≤ p.2) ∧
    ¬ ∃ c : ℕ, ∀ k ∈ K2K3_degrees, k = c := by
  have hq11 : q 1 1 = 0 := by simp [q]
  have hq22 : q 2 2 = 0 := by simp [q]
  have h4 : LOm 0 0 1 K2K3 = 4 := by
    simp [LOm, K2K3, psi, hq11, hq22]; norm_num
  refine ⟨h4, ?_, ?_, ?_⟩
  · rw [h4]; simp [K2K3, lowerConst]
  · intro p hp
    simp only [K2K3, Multiset.insert_eq_cons, Multiset.mem_cons,
      Multiset.mem_singleton] at hp
    rcases hp with h | h | h | h <;> subst h <;> norm_num
  · rintro ⟨c, hc⟩
    have h1 := hc 1 (by decide)
    have h2 := hc 2 (by decide)
    omega

end Loyola

#print axioms Loyola.K13_gamma_absorbed
#print axioms Loyola.K13_upper_attained
#print axioms Loyola.K13_degrees_in_range
#print axioms Loyola.K2K3_lower_attained
