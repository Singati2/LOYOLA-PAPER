import LoyolaFormal.Basic

/-!
# Pure-γ floor break at tree order 13 (L10)

Two distinct degree-pair profiles `P1 ≠ P2` (multisets of `ℕ × ℕ`, each pair written with
the smaller degree first) with the same multiset of rational imbalances `q`, hence
`LO(0,0,γ)` agrees for every real `γ`.  Both profiles are realised by explicit 13-vertex
trees given by parent arrays (vertex `i+1` is joined to `parent[i] ≤ i`).
-/

noncomputable section

open Real

namespace Loyola

/-- Profile `P1 = {(1,2)^1,(1,3)^2,(1,6)^5,(2,3)^2,(2,6)^1,(3,3)^1}`. -/
def P1 : Multiset (ℕ × ℕ) :=
  ([(1,2),(1,3),(1,3),(1,6),(1,6),(1,6),(1,6),(1,6),(2,3),(2,3),(2,6),(3,3)] : List (ℕ × ℕ))

/-- Profile `P2 = {(1,3)^3,(1,6)^5,(2,2)^1,(2,3)^2,(3,6)^1}`. -/
def P2 : Multiset (ℕ × ℕ) :=
  ([(1,3),(1,3),(1,3),(1,6),(1,6),(1,6),(1,6),(1,6),(2,2),(2,3),(2,3),(3,6)] : List (ℕ × ℕ))

/-- The multiplicities are as stated. -/
theorem P1_eq_replicates : P1 = Multiset.replicate 1 (1,2) + Multiset.replicate 2 (1,3) +
    Multiset.replicate 5 (1,6) + Multiset.replicate 2 (2,3) + Multiset.replicate 1 (2,6) +
    Multiset.replicate 1 (3,3) := by decide

theorem P2_eq_replicates : P2 = Multiset.replicate 3 (1,3) + Multiset.replicate 5 (1,6) +
    Multiset.replicate 1 (2,2) + Multiset.replicate 2 (2,3) + Multiset.replicate 1 (3,6) := by
  decide

theorem P1_ne_P2 : P1 ≠ P2 := by decide

theorem P1_card : Multiset.card P1 = 12 := by decide
theorem P2_card : Multiset.card P2 = 12 := by decide

/-- Rational imbalance `q(a,b) = |a-b|/(a+b)`, computed as `(max - min)/(a+b)`. -/
def qQ (p : ℕ × ℕ) : ℚ := ((max p.1 p.2 - min p.1 p.2 : ℕ) : ℚ) / ((p.1 + p.2 : ℕ) : ℚ)

/-- Reduced numerator/denominator of `q(a,b)` as a pair of naturals. -/
def qN (p : ℕ × ℕ) : ℕ × ℕ :=
  ((max p.1 p.2 - min p.1 p.2) / Nat.gcd (max p.1 p.2 - min p.1 p.2) (p.1 + p.2),
   (p.1 + p.2) / Nat.gcd (max p.1 p.2 - min p.1 p.2) (p.1 + p.2))

lemma div_gcd_div_gcd (m n : ℕ) :
    ((m / Nat.gcd m n : ℕ) : ℚ) / ((n / Nat.gcd m n : ℕ) : ℚ) = (m : ℚ) / n := by
  by_cases hg : Nat.gcd m n = 0
  · rw [Nat.gcd_eq_zero_iff] at hg
    obtain ⟨rfl, rfl⟩ := hg
    simp
  have hg' : ((Nat.gcd m n : ℕ) : ℚ) ≠ 0 := by exact_mod_cast hg
  rw [Nat.cast_div (Nat.gcd_dvd_left m n) hg', Nat.cast_div (Nat.gcd_dvd_right m n) hg',
    div_div_div_cancel_right₀ hg']

lemma qQ_eq_qN (p : ℕ × ℕ) : qQ p = ((qN p).1 : ℚ) / (qN p).2 := by
  unfold qQ qN
  rw [div_gcd_div_gcd]

/-- The reduced `q`-fractions of `P1` and `P2` agree as multisets (kernel-checked). -/
theorem P1_P2_same_qN : P1.map qN = P2.map qN := by decide

/-- **L10 (rational part)**: the multisets of `q`-values coincide. -/
theorem P1_P2_same_q : P1.map qQ = P2.map qQ := by
  have h : qQ = (fun r : ℕ × ℕ => (r.1 : ℚ) / r.2) ∘ qN := funext qQ_eq_qN
  rw [h, ← Multiset.map_map, ← Multiset.map_map, P1_P2_same_qN]

/-- The real `q` of a cast natural pair is the cast of the rational `qQ`. -/
lemma q_natCast (a b : ℕ) : q (a : ℝ) (b : ℝ) = ((qQ (a, b) : ℚ) : ℝ) := by
  unfold q qQ
  push_cast [Nat.cast_sub (min_le_max : min a b ≤ max a b)]
  congr 1
  rw [max_sub_min_eq_abs]
  try rw [abs_sub_comm]

/-- Loyola index of a multiset of natural degree pairs. -/
def LOn (α β γ : ℝ) (P : Multiset (ℕ × ℕ)) : ℝ :=
  LOm α β γ (P.map fun p => ((p.1 : ℝ), (p.2 : ℝ)))

lemma LOn_pure_gamma (γ : ℝ) (P : Multiset (ℕ × ℕ)) :
    LOn 0 0 γ P = ((P.map qQ).map fun r : ℚ => Real.exp (γ * r)).sum := by
  unfold LOn LOm
  rw [Multiset.map_map, Multiset.map_map]
  congr 1
  apply Multiset.map_congr rfl
  intro p _
  simp [psi, q_natCast]

/-- **L10 (real part)**: `LO(P1; 0,0,γ) = LO(P2; 0,0,γ)` for every real `γ`. -/
theorem P1_P2_same_pure_gamma (γ : ℝ) : LOn 0 0 γ P1 = LOn 0 0 γ P2 := by
  rw [LOn_pure_gamma, LOn_pure_gamma, P1_P2_same_q]

/-! ### Degree consistency from the profile alone -/

/-- Number of edge endpoints of degree `k` in a profile. -/
def endpoints (k : ℕ) (P : Multiset (ℕ × ℕ)) : ℕ :=
  (P.map fun e => (if e.1 = k then 1 else 0) + (if e.2 = k then 1 else 0)).sum

/-- **L10 (degree consistency, profile level)** for `P1`: every endpoint degree lies in
`{1,2,3,6}`; for each such `k`, `k ∣ endpoints k`; the implied vertex counts
`n_k = endpoints k / k` are `n₁=8, n₂=2, n₃=2, n₆=1`, summing to `13 = 12 + 1`. -/
theorem P1_degree_consistent :
    (∀ e ∈ P1, e.1 ∈ ({1,2,3,6} : Finset ℕ) ∧ e.2 ∈ ({1,2,3,6} : Finset ℕ)) ∧
    (∀ k ∈ ({1,2,3,6} : Finset ℕ), k ∣ endpoints k P1) ∧
    (endpoints 1 P1 / 1, endpoints 2 P1 / 2, endpoints 3 P1 / 3, endpoints 6 P1 / 6)
      = (8, 2, 2, 1) ∧
    ∑ k ∈ ({1,2,3,6} : Finset ℕ), endpoints k P1 / k = 13 ∧
    Multiset.card P1 + 1 = 13 := by decide

theorem P2_degree_consistent :
    (∀ e ∈ P2, e.1 ∈ ({1,2,3,6} : Finset ℕ) ∧ e.2 ∈ ({1,2,3,6} : Finset ℕ)) ∧
    (∀ k ∈ ({1,2,3,6} : Finset ℕ), k ∣ endpoints k P2) ∧
    (endpoints 1 P2 / 1, endpoints 2 P2 / 2, endpoints 3 P2 / 3, endpoints 6 P2 / 6)
      = (8, 2, 2, 1) ∧
    ∑ k ∈ ({1,2,3,6} : Finset ℕ), endpoints k P2 / k = 13 ∧
    Multiset.card P2 + 1 = 13 := by decide

/-! ### Realisation by explicit 13-vertex trees

A parent array `par` of length 12 with `par[i] ≤ i` defines the graph on `{0,…,12}` with edges
`{i+1, par[i]}`.  Such a graph is a tree (each non-root vertex has exactly one edge to a
strictly smaller vertex, so it is connected with `n - 1` edges).  The tree property itself is
the standard fact just quoted and is *not* re-proved here via `SimpleGraph.IsTree`; what is
machine-checked is the parent condition and the degree-pair profile. -/

def treeEdges (par : List ℕ) : List (ℕ × ℕ) :=
  (List.range par.length).map fun i => (i + 1, par.getD i 0)

def deg (E : List (ℕ × ℕ)) (v : ℕ) : ℕ := E.countP fun e => e.1 = v ∨ e.2 = v

def profile (E : List (ℕ × ℕ)) : Multiset (ℕ × ℕ) :=
  (E.map fun e => (min (deg E e.1) (deg E e.2), max (deg E e.1) (deg E e.2)) : List (ℕ × ℕ))

/-- Tree T1: hub 0 with leaves 1–5 and child 6; path 6–7–8–10–12; leaves 9 (on 7), 11 (on 8). -/
def par1 : List ℕ := [0, 0, 0, 0, 0, 0, 6, 7, 7, 8, 8, 10]

/-- Tree T2: hub 0 with leaves 1–5 and child 6; 6 has leaf 7 and child 8; 8–9–10;
10 has leaves 11, 12. -/
def par2 : List ℕ := [0, 0, 0, 0, 0, 0, 6, 6, 8, 9, 10, 10]

theorem par1_valid : par1.length = 12 ∧ ∀ i < 12, par1.getD i 0 ≤ i := by decide
theorem par2_valid : par2.length = 12 ∧ ∀ i < 12, par2.getD i 0 ≤ i := by decide

/-- **L10 (realisability)**: T1 has degree-pair profile `P1`. -/
theorem tree1_profile : profile (treeEdges par1) = P1 := by decide

/-- **L10 (realisability)**: T2 has degree-pair profile `P2`. -/
theorem tree2_profile : profile (treeEdges par2) = P2 := by decide

/-- Both trees have the same vertex degree sequence (on vertices `0..12`). -/
theorem trees_same_degree_sequence :
    (((List.range 13).map (deg (treeEdges par1))) : Multiset ℕ)
      = ((List.range 13).map (deg (treeEdges par2)) : Multiset ℕ) := by decide

end Loyola

#print axioms Loyola.P1_eq_replicates
#print axioms Loyola.P1_ne_P2
#print axioms Loyola.P1_card
#print axioms Loyola.P2_card
#print axioms Loyola.P1_P2_same_qN
#print axioms Loyola.P1_P2_same_q
#print axioms Loyola.P1_P2_same_pure_gamma
#print axioms Loyola.P1_degree_consistent
#print axioms Loyola.P2_degree_consistent
#print axioms Loyola.par1_valid
#print axioms Loyola.tree1_profile
#print axioms Loyola.tree2_profile
#print axioms Loyola.trees_same_degree_sequence
