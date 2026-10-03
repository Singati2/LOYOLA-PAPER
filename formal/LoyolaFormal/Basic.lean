import Mathlib

/-!
# Loyola index family: basic definitions

A graph is modelled abstractly by its edges together with the (real) degrees of
their endpoints:

* `LO α β γ s d = ∑ e ∈ s, ψ(d e)` for a finite index set `s : Finset ι` of edges and a
  degree map `d : ι → ℝ × ℝ` (e.g. `ι = Sym2 V`, `s = G.edgeFinset`,
  `d e = (deg u, deg v)`);
* `LOm α β γ E` for a multiset `E : Multiset (ℝ × ℝ)` of degree pairs.
-/

noncomputable section

open Real

namespace Loyola

/-- Degree imbalance `q(x,y) = |x - y| / (x + y)`. -/
def q (x y : ℝ) : ℝ := |x - y| / (x + y)

/-- Edge weight `ψ(x,y;α,β,γ) = (xy)^α (x+y)^β exp(γ q(x,y))` (real powers). -/
def psi (α β γ x y : ℝ) : ℝ := (x * y) ^ α * (x + y) ^ β * Real.exp (γ * q x y)

/-- Loyola index of a finite edge family with degree map `d`. -/
def LO {ι : Type*} (α β γ : ℝ) (s : Finset ι) (d : ι → ℝ × ℝ) : ℝ :=
  ∑ e ∈ s, psi α β γ (d e).1 (d e).2

/-- Loyola index of a multiset of degree pairs. -/
def LOm (α β γ : ℝ) (E : Multiset (ℝ × ℝ)) : ℝ :=
  (E.map fun p => psi α β γ p.1 p.2).sum

lemma q_nonneg {x y : ℝ} (hx : 0 < x) (hy : 0 < y) : 0 ≤ q x y :=
  div_nonneg (abs_nonneg _) (by linarith)

lemma psi_pos {α β γ x y : ℝ} (hx : 0 < x) (hy : 0 < y) : 0 < psi α β γ x y := by
  unfold psi
  have h1 : 0 < x * y := mul_pos hx hy
  have h2 : 0 < x + y := by linarith
  positivity

lemma psi_nonneg {α β γ x y : ℝ} (hx : 0 < x) (hy : 0 < y) : 0 ≤ psi α β γ x y :=
  (psi_pos hx hy).le

lemma psi_symm (α β γ x y : ℝ) : psi α β γ x y = psi α β γ y x := by
  unfold psi q
  rw [mul_comm x y, add_comm x y, abs_sub_comm]

end Loyola
