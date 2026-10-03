import LoyolaFormal.Basic

/-!
# Exponent additivity and the Cauchy–Schwarz bound (L4); the q-only direction (L6)

Manuscript: `thm:cs`; the parent-family identity `1 - q² = 4xy/(x+y)²`.
-/

noncomputable section

open Real Finset

namespace Loyola

/-- **L4, edge identity** (`thm:cs`): exponent additivity
`ψ(α₁,β₁,γ₁) ψ(α₂,β₂,γ₂) = ψ(α,β,γ)²` when the exponents average to `(α,β,γ)`. -/
theorem psi_mul_psi_eq_sq {α β γ α₁ β₁ γ₁ α₂ β₂ γ₂ x y : ℝ} (hx : 0 < x) (hy : 0 < y)
    (hα : α₁ + α₂ = 2 * α) (hβ : β₁ + β₂ = 2 * β) (hγ : γ₁ + γ₂ = 2 * γ) :
    psi α₁ β₁ γ₁ x y * psi α₂ β₂ γ₂ x y = psi α β γ x y ^ 2 := by
  unfold psi
  have hxy : 0 < x * y := mul_pos hx hy
  have hs : 0 < x + y := by linarith
  have e1 : (x * y) ^ α₁ * (x * y) ^ α₂ = (x * y) ^ α * (x * y) ^ α := by
    rw [← Real.rpow_add hxy, ← Real.rpow_add hxy, hα, two_mul]
  have e2 : (x + y) ^ β₁ * (x + y) ^ β₂ = (x + y) ^ β * (x + y) ^ β := by
    rw [← Real.rpow_add hs, ← Real.rpow_add hs, hβ, two_mul]
  have e3 : Real.exp (γ₁ * q x y) * Real.exp (γ₂ * q x y)
      = Real.exp (γ * q x y) * Real.exp (γ * q x y) := by
    rw [← Real.exp_add, ← Real.exp_add, ← add_mul, hγ, two_mul, add_mul]
  calc (x * y) ^ α₁ * (x + y) ^ β₁ * Real.exp (γ₁ * q x y) *
        ((x * y) ^ α₂ * (x + y) ^ β₂ * Real.exp (γ₂ * q x y))
      = ((x * y) ^ α₁ * (x * y) ^ α₂) * ((x + y) ^ β₁ * (x + y) ^ β₂) *
        (Real.exp (γ₁ * q x y) * Real.exp (γ₂ * q x y)) := by ring
    _ = _ := by rw [e1, e2, e3]; ring

/-- **L4, summed** (`thm:cs`): for any finite edge family with positive degrees,
`LO(α,β,γ) ≤ √LO(α₁,β₁,γ₁) · √LO(α₂,β₂,γ₂)`. Uses Mathlib's
`Real.sum_mul_le_sqrt_mul_sqrt` (Cauchy–Schwarz for finite sums). -/
theorem LO_le_sqrt_mul_sqrt {ι : Type*} {α β γ α₁ β₁ γ₁ α₂ β₂ γ₂ : ℝ}
    (hα : α₁ + α₂ = 2 * α) (hβ : β₁ + β₂ = 2 * β) (hγ : γ₁ + γ₂ = 2 * γ)
    (s : Finset ι) (d : ι → ℝ × ℝ) (hd : ∀ e ∈ s, 0 < (d e).1 ∧ 0 < (d e).2) :
    LO α β γ s d ≤ √(LO α₁ β₁ γ₁ s d) * √(LO α₂ β₂ γ₂ s d) := by
  unfold LO
  set f : ι → ℝ := fun e => √(psi α₁ β₁ γ₁ (d e).1 (d e).2)
  set g : ι → ℝ := fun e => √(psi α₂ β₂ γ₂ (d e).1 (d e).2)
  have hedge : ∀ e ∈ s, psi α β γ (d e).1 (d e).2 = f e * g e := by
    intro e he
    obtain ⟨h1, h2⟩ := hd e he
    simp only [f, g]
    rw [← Real.sqrt_mul (psi_nonneg h1 h2), psi_mul_psi_eq_sq h1 h2 hα hβ hγ,
      Real.sqrt_sq (psi_nonneg h1 h2)]
  have hf : ∑ e ∈ s, f e ^ 2 = ∑ e ∈ s, psi α₁ β₁ γ₁ (d e).1 (d e).2 :=
    sum_congr rfl fun e he => Real.sq_sqrt (psi_nonneg (hd e he).1 (hd e he).2)
  have hg : ∑ e ∈ s, g e ^ 2 = ∑ e ∈ s, psi α₂ β₂ γ₂ (d e).1 (d e).2 :=
    sum_congr rfl fun e he => Real.sq_sqrt (psi_nonneg (hd e he).1 (hd e he).2)
  rw [sum_congr rfl hedge, ← hf, ← hg]
  exact Real.sum_mul_le_sqrt_mul_sqrt s f g

/-- **L4, summed, product form**: `LO(α,β,γ) ≤ √(LO(α₁,β₁,γ₁) · LO(α₂,β₂,γ₂))`. -/
theorem LO_le_sqrt_prod {ι : Type*} {α β γ α₁ β₁ γ₁ α₂ β₂ γ₂ : ℝ}
    (hα : α₁ + α₂ = 2 * α) (hβ : β₁ + β₂ = 2 * β) (hγ : γ₁ + γ₂ = 2 * γ)
    (s : Finset ι) (d : ι → ℝ × ℝ) (hd : ∀ e ∈ s, 0 < (d e).1 ∧ 0 < (d e).2) :
    LO α β γ s d ≤ √(LO α₁ β₁ γ₁ s d * LO α₂ β₂ γ₂ s d) := by
  have h0 : 0 ≤ LO α₁ β₁ γ₁ s d :=
    sum_nonneg fun e he => psi_nonneg (hd e he).1 (hd e he).2
  rw [Real.sqrt_mul h0]
  exact LO_le_sqrt_mul_sqrt hα hβ hγ s d hd

/-- `1 - q(x,y)² = 4xy/(x+y)²`. -/
theorem one_sub_q_sq {x y : ℝ} (hx : 0 < x) (hy : 0 < y) :
    1 - q x y ^ 2 = 4 * (x * y) / (x + y) ^ 2 := by
  unfold q
  have hs : (x + y) ≠ 0 := by linarith
  rw [div_pow, sq_abs]
  field_simp
  ring

/-- **L6** (the parent family contains a q-only direction):
`(xy)^α (x+y)^(-2α) = 4^(-α) (1 - q²)^α`. -/
theorem q_only_direction {x y : ℝ} (hx : 0 < x) (hy : 0 < y) (α : ℝ) :
    (x * y) ^ α * (x + y) ^ (-2 * α) = (4 : ℝ) ^ (-α) * (1 - q x y ^ 2) ^ α := by
  have hs : 0 < x + y := by linarith
  have hxy : 0 < x * y := mul_pos hx hy
  have e1 : ((x + y) ^ 2) ^ α = (x + y) ^ (2 * α) := by
    rw [Real.rpow_mul hs.le, Real.rpow_two]
  rw [one_sub_q_sq hx hy, Real.div_rpow (by positivity) (by positivity),
    Real.mul_rpow (by norm_num) hxy.le, e1, Real.rpow_neg (by norm_num : (0:ℝ) ≤ 4),
    show -2 * α = -(2 * α) by ring, Real.rpow_neg hs.le]
  have h4 : (0:ℝ) < 4 ^ α := by positivity
  have h5 : (0:ℝ) < (x + y) ^ (2 * α) := by positivity
  field_simp

end Loyola

#print axioms Loyola.psi_mul_psi_eq_sq
#print axioms Loyola.LO_le_sqrt_mul_sqrt
#print axioms Loyola.LO_le_sqrt_prod
#print axioms Loyola.one_sub_q_sq
#print axioms Loyola.q_only_direction
