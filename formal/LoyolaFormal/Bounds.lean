import LoyolaFormal.Basic

/-!
# Degree bounds (L1, L2, L3) and the ratio/bracket bound (L5)

Manuscript: `thm:upper_Delta`, `thm:lower_delta`, `thm:ratio_bound`.
-/

noncomputable section

open Real Finset

namespace Loyola

/-- **L1** (imbalance maximum). For `1 ≤ x, y ≤ Δ`, `q(x,y) ≤ (Δ-1)/(Δ+1)`. -/
theorem q_le_imbalance_max {x y Δ : ℝ} (hx1 : 1 ≤ x) (hy1 : 1 ≤ y)
    (hxΔ : x ≤ Δ) (hyΔ : y ≤ Δ) : q x y ≤ (Δ - 1) / (Δ + 1) := by
  unfold q
  have hxy : 0 < x + y := by linarith
  have hΔ : 0 < Δ + 1 := by linarith
  rw [div_le_div_iff₀ hxy hΔ]
  rcases le_total y x with h | h
  · rw [abs_of_nonneg (by linarith)]; nlinarith
  · rw [abs_of_nonpos (by linarith)]; nlinarith

/-- The constant on the right of `thm:upper_Delta`. -/
def upperConst (α β γ Δ : ℝ) : ℝ :=
  Δ ^ (2 * α) * (2 * Δ) ^ β * Real.exp (γ * ((Δ - 1) / (Δ + 1)))

/-- The constant on the right of `thm:lower_delta`. -/
def lowerConst (α β δ : ℝ) : ℝ := δ ^ (2 * α) * (2 * δ) ^ β

lemma rpow_two_mul_eq {t α : ℝ} (ht : 0 ≤ t) : t ^ (2 * α) = (t * t) ^ α := by
  rw [Real.rpow_mul ht, ← sq, Real.rpow_two]

/-- **L2, edge level** (`thm:upper_Delta`). -/
theorem psi_le_upper {α β γ x y Δ : ℝ} (hα : 0 ≤ α) (hβ : 0 ≤ β) (hγ : 0 ≤ γ)
    (hx1 : 1 ≤ x) (hy1 : 1 ≤ y) (hxΔ : x ≤ Δ) (hyΔ : y ≤ Δ) :
    psi α β γ x y ≤ upperConst α β γ Δ := by
  unfold psi upperConst
  have hΔ : 0 ≤ Δ := by linarith
  have h1 : (x * y) ^ α ≤ Δ ^ (2 * α) := by
    rw [rpow_two_mul_eq hΔ]
    exact Real.rpow_le_rpow (by positivity) (by nlinarith) hα
  have h2 : (x + y) ^ β ≤ (2 * Δ) ^ β :=
    Real.rpow_le_rpow (by linarith) (by linarith) hβ
  have h3 : Real.exp (γ * q x y) ≤ Real.exp (γ * ((Δ - 1) / (Δ + 1))) :=
    Real.exp_le_exp.2 (mul_le_mul_of_nonneg_left (q_le_imbalance_max hx1 hy1 hxΔ hyΔ) hγ)
  have hxy : 0 ≤ x * y := by positivity
  have hs : 0 ≤ x + y := by linarith
  gcongr

/-- **L2, summed** (`thm:upper_Delta`): `LO ≤ m · Δ^{2α} (2Δ)^β exp(γ(Δ-1)/(Δ+1))`
for any finite edge family of size `m = s.card` with all degrees in `[1, Δ]`. -/
theorem LO_le_upper {ι : Type*} {α β γ Δ : ℝ} (hα : 0 ≤ α) (hβ : 0 ≤ β) (hγ : 0 ≤ γ)
    (s : Finset ι) (d : ι → ℝ × ℝ)
    (h1 : ∀ e ∈ s, 1 ≤ (d e).1 ∧ 1 ≤ (d e).2)
    (hΔ : ∀ e ∈ s, (d e).1 ≤ Δ ∧ (d e).2 ≤ Δ) :
    LO α β γ s d ≤ s.card * upperConst α β γ Δ := by
  unfold LO
  calc ∑ e ∈ s, psi α β γ (d e).1 (d e).2 ≤ ∑ _e ∈ s, upperConst α β γ Δ :=
        sum_le_sum fun e he =>
          psi_le_upper hα hβ hγ (h1 e he).1 (h1 e he).2 (hΔ e he).1 (hΔ e he).2
    _ = s.card * upperConst α β γ Δ := by rw [sum_const, nsmul_eq_mul]

/-- **L2, summed, multiset version**. -/
theorem LOm_le_upper {α β γ Δ : ℝ} (hα : 0 ≤ α) (hβ : 0 ≤ β) (hγ : 0 ≤ γ)
    (E : Multiset (ℝ × ℝ))
    (hE : ∀ p ∈ E, 1 ≤ p.1 ∧ 1 ≤ p.2 ∧ p.1 ≤ Δ ∧ p.2 ≤ Δ) :
    LOm α β γ E ≤ Multiset.card E * upperConst α β γ Δ := by
  unfold LOm
  have := Multiset.sum_map_le_sum_map (s := E) (fun p => psi α β γ p.1 p.2)
    (fun _ => upperConst α β γ Δ) (fun p hp =>
      psi_le_upper hα hβ hγ (hE p hp).1 (hE p hp).2.1 (hE p hp).2.2.1 (hE p hp).2.2.2)
  simpa [Multiset.map_const', Multiset.sum_replicate, nsmul_eq_mul] using this

/-- **L3, edge level** (`thm:lower_delta`). -/
theorem lower_le_psi {α β γ x y δ : ℝ} (hα : 0 ≤ α) (hβ : 0 ≤ β) (hγ : 0 ≤ γ)
    (hδ : 0 < δ) (hx : δ ≤ x) (hy : δ ≤ y) :
    lowerConst α β δ ≤ psi α β γ x y := by
  unfold psi lowerConst
  have h1 : δ ^ (2 * α) ≤ (x * y) ^ α := by
    rw [rpow_two_mul_eq hδ.le]
    exact Real.rpow_le_rpow (by positivity) (by nlinarith) hα
  have h2 : (2 * δ) ^ β ≤ (x + y) ^ β :=
    Real.rpow_le_rpow (by linarith) (by linarith) hβ
  have h3 : 1 ≤ Real.exp (γ * q x y) :=
    Real.one_le_exp (mul_nonneg hγ (q_nonneg (by linarith) (by linarith)))
  calc δ ^ (2 * α) * (2 * δ) ^ β = δ ^ (2 * α) * (2 * δ) ^ β * 1 := by ring
    _ ≤ (x * y) ^ α * (x + y) ^ β * Real.exp (γ * q x y) := by
        have : 0 ≤ δ ^ (2 * α) := by positivity
        have : 0 ≤ (2 * δ) ^ β := by positivity
        have hx0 : 0 ≤ x * y := by nlinarith
        have hy0 : 0 ≤ x + y := by linarith
        have : 0 ≤ (x * y) ^ α := by positivity
        have : 0 ≤ (x + y) ^ β := by positivity
        gcongr

/-- **L3, summed** (`thm:lower_delta`): `m · δ^{2α} (2δ)^β ≤ LO`. -/
theorem lower_le_LO {ι : Type*} {α β γ δ : ℝ} (hα : 0 ≤ α) (hβ : 0 ≤ β) (hγ : 0 ≤ γ)
    (hδ : 0 < δ) (s : Finset ι) (d : ι → ℝ × ℝ)
    (h : ∀ e ∈ s, δ ≤ (d e).1 ∧ δ ≤ (d e).2) :
    s.card * lowerConst α β δ ≤ LO α β γ s d := by
  unfold LO
  calc (s.card : ℝ) * lowerConst α β δ = ∑ _e ∈ s, lowerConst α β δ := by
        rw [sum_const, nsmul_eq_mul]
    _ ≤ _ := sum_le_sum fun e he => lower_le_psi hα hβ hγ hδ (h e he).1 (h e he).2

/-- **L3, summed, multiset version**. -/
theorem lower_le_LOm {α β γ δ : ℝ} (hα : 0 ≤ α) (hβ : 0 ≤ β) (hγ : 0 ≤ γ)
    (hδ : 0 < δ) (E : Multiset (ℝ × ℝ)) (hE : ∀ p ∈ E, δ ≤ p.1 ∧ δ ≤ p.2) :
    Multiset.card E * lowerConst α β δ ≤ LOm α β γ E := by
  unfold LOm
  have := Multiset.sum_map_le_sum_map (s := E) (fun _ => lowerConst α β δ)
    (fun p => psi α β γ p.1 p.2) (fun p hp => lower_le_psi hα hβ hγ hδ (hE p hp).1 (hE p hp).2)
  simpa [Multiset.map_const', Multiset.sum_replicate, nsmul_eq_mul] using this

/-- **L5** (`thm:ratio_bound`, bracket form). If `c_min ≤ ψ_e / h_e ≤ c_max` with `h_e > 0`
on every edge, then `c_min · Σ h ≤ Σ ψ ≤ c_max · Σ h`.  Stated for arbitrary real edge
weights `ψ` (in particular `ψ_e = psi α β γ (d e).1 (d e).2`) and any BID weights `h`. -/
theorem ratio_bound {ι : Type*} (s : Finset ι) (ψ h : ι → ℝ) {cmin cmax : ℝ}
    (hpos : ∀ e ∈ s, 0 < h e)
    (hmin : ∀ e ∈ s, cmin ≤ ψ e / h e) (hmax : ∀ e ∈ s, ψ e / h e ≤ cmax) :
    cmin * ∑ e ∈ s, h e ≤ ∑ e ∈ s, ψ e ∧ ∑ e ∈ s, ψ e ≤ cmax * ∑ e ∈ s, h e := by
  rw [mul_sum, mul_sum]
  constructor
  · exact sum_le_sum fun e he => (le_div_iff₀ (hpos e he)).1 (hmin e he)
  · exact sum_le_sum fun e he => (div_le_iff₀ (hpos e he)).1 (hmax e he)

/-- **L5 specialised to the Loyola index** (`thm:ratio_bound`). -/
theorem LO_ratio_bound {ι : Type*} (α β γ : ℝ) (s : Finset ι) (d : ι → ℝ × ℝ) (h : ι → ℝ)
    {cmin cmax : ℝ} (hpos : ∀ e ∈ s, 0 < h e)
    (hmin : ∀ e ∈ s, cmin ≤ psi α β γ (d e).1 (d e).2 / h e)
    (hmax : ∀ e ∈ s, psi α β γ (d e).1 (d e).2 / h e ≤ cmax) :
    cmin * ∑ e ∈ s, h e ≤ LO α β γ s d ∧ LO α β γ s d ≤ cmax * ∑ e ∈ s, h e :=
  ratio_bound s (fun e => psi α β γ (d e).1 (d e).2) h hpos hmin hmax

end Loyola

#print axioms Loyola.q_le_imbalance_max
#print axioms Loyola.psi_le_upper
#print axioms Loyola.LO_le_upper
#print axioms Loyola.LOm_le_upper
#print axioms Loyola.lower_le_psi
#print axioms Loyola.lower_le_LO
#print axioms Loyola.lower_le_LOm
#print axioms Loyola.ratio_bound
#print axioms Loyola.LO_ratio_bound
