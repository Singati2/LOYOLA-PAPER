import Mathlib

/-!
# Global log-convexity (L11, manuscript `thm:logconvex`, convexity part)

For a nonempty finite edge set with feature vectors `z_e ∈ ℝⁿ` (the paper uses `n = 3`,
`z_e = (log(d_u d_v), log(d_u+d_v), q_uv)`), `θ ↦ log Σ_e exp(⟨θ, z_e⟩)` is convex on all of
`ℝⁿ`.  Proof via Hölder's inequality (`Real.inner_le_Lp_mul_Lq_of_nonneg`).
-/

noncomputable section

open Real Finset

namespace Loyola

/-- **L11** (`thm:logconvex`, convexity statement). -/
theorem logSumExp_convex {ι : Type*} {n : ℕ} (s : Finset ι) (hs : s.Nonempty)
    (z : ι → Fin n → ℝ) :
    ConvexOn ℝ Set.univ (fun θ : Fin n → ℝ => Real.log (∑ e ∈ s, Real.exp (θ ⬝ᵥ z e))) := by
  refine ⟨convex_univ, ?_⟩
  intro θ₁ _ θ₂ _ a b ha hb hab
  simp only [smul_eq_mul]
  set S₁ := ∑ e ∈ s, Real.exp (θ₁ ⬝ᵥ z e)
  set S₂ := ∑ e ∈ s, Real.exp (θ₂ ⬝ᵥ z e)
  have hS₁ : 0 < S₁ := sum_pos (fun e _ => Real.exp_pos _) hs
  have hS₂ : 0 < S₂ := sum_pos (fun e _ => Real.exp_pos _) hs
  rcases ha.eq_or_lt with rfl | ha'
  · have hb1 : b = 1 := by linarith
    subst hb1; simp [S₂]
  rcases hb.eq_or_lt with rfl | hb'
  · have ha1 : a = 1 := by linarith
    subst ha1; simp [S₁]
  -- rewrite each summand as a product of powers
  have hsum : ∑ e ∈ s, Real.exp ((a • θ₁ + b • θ₂) ⬝ᵥ z e)
      = ∑ e ∈ s, Real.exp (θ₁ ⬝ᵥ z e) ^ a * Real.exp (θ₂ ⬝ᵥ z e) ^ b := by
    refine sum_congr rfl fun e _ => ?_
    rw [add_dotProduct, smul_dotProduct, smul_dotProduct, smul_eq_mul, smul_eq_mul,
      Real.exp_add, ← Real.exp_mul, ← Real.exp_mul, mul_comm a, mul_comm b]
  have hH := Real.inner_le_Lp_mul_Lq_of_nonneg s (Real.holderConjugate_one_div ha' hb' hab)
    (f := fun e => Real.exp (θ₁ ⬝ᵥ z e) ^ a) (g := fun e => Real.exp (θ₂ ⬝ᵥ z e) ^ b)
    (fun e _ => by positivity) (fun e _ => by positivity)
  have hp1 : ∀ e, (Real.exp (θ₁ ⬝ᵥ z e) ^ a) ^ (1 / a) = Real.exp (θ₁ ⬝ᵥ z e) := by
    intro e
    rw [← Real.rpow_mul (Real.exp_pos _).le, mul_one_div_cancel ha'.ne', Real.rpow_one]
  have hp2 : ∀ e, (Real.exp (θ₂ ⬝ᵥ z e) ^ b) ^ (1 / b) = Real.exp (θ₂ ⬝ᵥ z e) := by
    intro e
    rw [← Real.rpow_mul (Real.exp_pos _).le, mul_one_div_cancel hb'.ne', Real.rpow_one]
  simp only [hp1, hp2, one_div_one_div] at hH
  rw [hsum]
  have hpos : 0 < ∑ e ∈ s, Real.exp (θ₁ ⬝ᵥ z e) ^ a * Real.exp (θ₂ ⬝ᵥ z e) ^ b :=
    sum_pos (fun e _ => by positivity) hs
  calc Real.log (∑ e ∈ s, Real.exp (θ₁ ⬝ᵥ z e) ^ a * Real.exp (θ₂ ⬝ᵥ z e) ^ b)
      ≤ Real.log (S₁ ^ a * S₂ ^ b) := Real.log_le_log hpos hH
    _ = a * Real.log S₁ + b * Real.log S₂ := by
        rw [Real.log_mul (by positivity) (by positivity), Real.log_rpow hS₁, Real.log_rpow hS₂]

end Loyola

#print axioms Loyola.logSumExp_convex
