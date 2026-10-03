import LoyolaFormal.Basic

/-!
# Affine independence of the imbalance direction (L12, manuscript `prop:indep`)

The augmented feature vectors `(1, log(ij), log(i+j), q_ij)` of the pairs
`(1,1), (2,2), (1,2), (1,3)` form a matrix with determinant `log 2 · (8 log 3 - 13 log 2)/6`,
which is nonzero because `2^13 = 8192 > 6561 = 3^8`.  Hence for every `Δ ≥ 3` the features of
all admissible pairs `1 ≤ i ≤ j ≤ Δ` span `ℝ⁴`.
-/

noncomputable section

open Real

namespace Loyola

/-- Augmented feature vector `(1, log(ij), log(i+j), q_ij)`. -/
def feat (i j : ℕ) : Fin 4 → ℝ :=
  ![1, Real.log ((i : ℝ) * j), Real.log ((i : ℝ) + j), q i j]

/-- The four witness rows. -/
def W : Matrix (Fin 4) (Fin 4) ℝ := Matrix.of ![feat 1 1, feat 2 2, feat 1 2, feat 1 3]

lemma log_four : Real.log 4 = 2 * Real.log 2 := by
  rw [show (4:ℝ) = 2 ^ 2 by norm_num, Real.log_pow]; norm_num

lemma W_explicit : W = !![1, 0, Real.log 2, 0;
    1, 2 * Real.log 2, 2 * Real.log 2, 0;
    1, Real.log 2, Real.log 3, 1/3;
    1, Real.log 3, 2 * Real.log 2, 1/2] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [W, feat, q, log_four, abs_of_neg, abs_of_nonneg]

theorem det_W : W.det = Real.log 2 * (8 * Real.log 3 - 13 * Real.log 2) / 6 := by
  rw [W_explicit, Matrix.det_succ_row_zero]
  simp [Fin.sum_univ_succ, Matrix.det_fin_three, Matrix.submatrix, Fin.succAbove]
  ring

lemma thirteen_log_two_gt : 8 * Real.log 3 < 13 * Real.log 2 := by
  have h1 : Real.log ((3:ℝ) ^ 8) < Real.log ((2:ℝ) ^ 13) :=
    Real.log_lt_log (by norm_num) (by norm_num)
  rw [Real.log_pow, Real.log_pow] at h1
  exact_mod_cast h1

theorem det_W_ne_zero : W.det ≠ 0 := by
  rw [det_W]
  have h2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have h3 := thirteen_log_two_gt
  have : Real.log 2 * (8 * Real.log 3 - 13 * Real.log 2) < 0 := by nlinarith
  intro h; linarith

/-- The four witness feature vectors span `ℝ⁴`. -/
theorem witness_span : Submodule.span ℝ (Set.range fun k : Fin 4 => W k) = ⊤ := by
  have hli : LinearIndependent ℝ (fun k : Fin 4 => W k) :=
    Matrix.linearIndependent_rows_of_det_ne_zero det_W_ne_zero
  exact hli.span_eq_top_of_card_eq_finrank (by simp)

/-- **L12** (`prop:indep`, spanning statement): for every `Δ ≥ 3`, the augmented feature
vectors of the admissible pairs `{(i,j) : 1 ≤ i ≤ j ≤ Δ}` span `ℝ⁴`. -/
theorem features_span (Δ : ℕ) (hΔ : 3 ≤ Δ) :
    Submodule.span ℝ ((fun p : ℕ × ℕ => feat p.1 p.2) ''
      {p | 1 ≤ p.1 ∧ p.1 ≤ p.2 ∧ p.2 ≤ Δ}) = ⊤ := by
  refine eq_top_iff.2 (witness_span ▸ Submodule.span_mono ?_)
  rintro _ ⟨k, rfl⟩
  fin_cases k
  · exact ⟨(1, 1), ⟨le_rfl, le_rfl, by omega⟩, rfl⟩
  · exact ⟨(2, 2), ⟨by norm_num, le_rfl, by omega⟩, rfl⟩
  · exact ⟨(1, 2), ⟨le_rfl, by norm_num, by omega⟩, rfl⟩
  · exact ⟨(1, 3), ⟨le_rfl, by norm_num, by omega⟩, rfl⟩

end Loyola

#print axioms Loyola.det_W
#print axioms Loyola.det_W_ne_zero
#print axioms Loyola.witness_span
#print axioms Loyola.features_span
