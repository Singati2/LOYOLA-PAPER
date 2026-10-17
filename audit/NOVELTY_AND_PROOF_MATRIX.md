# Novelty and proof matrix (2026-10-17)

Status labels: **VERIFIED** means checked here by an independent proof, independent code, or a reading of
the primary source. **PARTIALLY VERIFIED** means some evidence, but not complete. **NOT TESTED** means not
checked. "Not found in a literature search" is never treated as proof of novelty.

Primary sources read in full or at the cited statements (PDFs from match.pmf.kg.ac.rs):

| Short name | Reference |
|---|---|
| Rada 2019 | J. Rada, MATCH 82 (2019) 29–41: Definition 2.3, Proposition 2.5, Theorem 3.4 |
| Cruz–Rada 2019 | R. Cruz, J. Rada, MATCH 82 (2019) 715–732: the set L, Theorem 2.1, Corollary 2.2, Theorem 3.1, Corollary 3.2 |
| RRS 2022 | J. Rada, J. M. Rodríguez, J. M. Sigarreta, MATCH 87 (2022) 97–108: Examples 2.1 and 2.2, Section 3 |
| Rada 2026 | J. Rada, MATCH 96 (2026) 841–863, read by the literature reviewer: Theorem 2, Example 3, Section 4.2 |

## 1. Objects

* **Graphs.** A graph is finite, simple and connected, with at least one edge. A *tree* is unlabeled
  (isomorphism classes). A *chemical tree* has maximum degree Δ ≤ 4.
* **Degree-pair profile.** The profile m(G) = (m_ij)_{i≤j} counts edges by their unordered end-degree
  pair. (1,1) occurs only in K_2, so for trees of order n ≥ 3, m_11 = 0.
* **q-histogram.** q_ij = (j−i)/(i+j), and n_q(G) = Σ_{q_ij = q} m_ij. The ratio min/max = (1−q)/(1+q),
  so the q-histogram equals the multiset of edge degree ratios.
* **Collision at order n.** Two trees of order n (in the class) with *distinct* profiles and *equal*
  q-histograms. Counts are of distinct profiles realised by trees, not of trees.
* **First collision order.** The least n with a collision in the class.
* **Degree-ratio index.** I_f(G) = Σ_{uv} f(min(d_u,d_v)/max(d_u,d_v)), for any f on (0,1]. This
  includes:
  * GA = Σ 2√(ij)/(i+j);
  * AG;
  * SDD = Σ (i/j + j/i);
  * ISDD = Σ ij/(i²+j²);
  * the exponential GA and ISDD;
  * the diminished Sombor index;
  * DRSO and the related ratio indices;
  * the hyperbolic Sombor index (Kırgız, MATCH 97 (2027)), which is also of this form but is not yet
    cited.

## 2. Results, verification, and the known/new boundary

| # | Statement | Proof or verification | Prior art (primary source) | Known / new | Status |
|---|---|---|---|---|---|
| 1 | A degree-ratio index depends on G only through its q-histogram | One line: ρ = (1−q)/(1+q) | Rada 2019, Proposition 2.5 (equal m̂_φ-structure ⇒ equal φ), specialised to ratio-only weights. Öz–Gutman (tangent Sombor, HJMS 2025) puts SDD, ISDD and SO₂ on one per-edge angle | **Known in substance** | VERIFIED (proof; Rada 2019 read) |
| 2 | Pure-γ points at algebraic γ ≠ 0 separate exactly the q-histograms (Theorem 2(ii) full / 3(ii) short) | Lindemann–Weierstrass | **Rada 2019, Theorem 3.4**, applied to φ_ij = γ q_ij (algebraic), whose classes of equal weight are the q-classes | **Known (special case)** | VERIFIED (Theorem 3.4 read) |
| 3 | On Π, values depend only on the q-histogram; differing histograms differ off a null set (part (i)) | Factorisation, plus real-analytic zero sets (Mityagin) | Standard | Elementary | VERIFIED (proof checked by two reviews) |
| 4 | **First collision order 13 (all trees), 16 (Δ ≤ 4)** | Exhaustive enumeration of all unlabeled trees, orders 2–17. Independent code: `certificates/minimal.py`; `minimal_out.txt` gives 570 profiles / 566 histograms at n = 13 and 810/809 at n = 16 for Δ ≤ 4, with no collision below | **Not found** in a search of RRS 2022 and its OpenAlex forward citations, Rada 2026, the DRSO papers (MATCH 97), the GA survey, the HSO paper, OpenAlex and arXiv. Google Scholar "cited by" was not reachable | **Apparently new, computational** | Enumeration VERIFIED (independent code, plus the repository's own exact verifier). Novelty PARTIALLY VERIFIED |
| 5 | Explicit witnesses at 13 and 16, and collisions at every larger order with the same maximum degree (part (iii)) | Pendant-path attachment changes both profiles by the same vector −(1,d)+(2,d)+(L−1)(2,2)+(1,2). `certificates/witnesses.py` builds all four trees from the prose descriptions and checks orders 13–40 and 16–43 | The device is from Rada 2026 §3.1. The construction parallels **RRS 2022, Example 2.2** (degree-*sum* classes (1,3)~(2,2), (1,4)~(2,3), (2,4)~(3,3) in chemical trees). Here the classes are degree-*ratio* classes: {(1,2),(2,4)} and {(2,2),(3,3),(4,4)} for Δ ≤ 4 | **Known technique; new witnesses** | VERIFIED (algebraic proof plus executable check) |
| 6 | Orders 13/16 are the first at which **all** degree-ratio indices fail **simultaneously** | Follows from 1 and 4 | — | New residual of 4 | VERIFIED |
| 6a | A **single** ratio index can fail earlier: SDD merges distinct profiles at order 9 (also among chemical trees); ISDD at order 10; GA first falls below the profile floor at order 13 | `certificates/ratio_indices.py` (exact rationals). SDD witness {(1,2),(1,3)²,(2,2)⁴,(2,3)} against {(1,2)³,(1,3),(2,3)³,(3,3)}, both 58/3 | Found by the literature reviewer, re-derived here | **Caveat**: the 13/16 statement must not be read as "SDD first fails at 13". Added to both manuscripts | VERIFIED |
| 7 | Ceiling: equal profiles give equal values of every VDB index; the octane collision pairs | Definition | Rada 2026; Deutsch–Klavžar 2015 (M-polynomial); folklore in octane tables | **Known** | VERIFIED |
| 8 | Generic discrimination (almost every θ separates distinct profiles) | Real-analytic zero set | Standard; compare Rada 2026 Theorem 3 / RRS 2022 §3 (Z-independence) | **Known method** | VERIFIED |
| 9 | Parent distinctions survive at rational (α,β) and algebraic γ ≠ 0 | Lindemann–Weierstrass with algebraic coefficients | Same method as Rada 2019 Theorem 3.4 | Small new statement (known method) | VERIFIED (proof checked) |
| 10 | Order exchanges along γ: at most V ≤ r−1, so at most 5 for Δ ≤ 4; attained at Δ = 6 (order 12) | Laguerre's rule (Jameson 2006) | Classical tool; no prior use found for this family | **Incremental** | Proof VERIFIED. Sharpness example VERIFIED numerically by the comparison reviewer (V = 5; crossings at −17.18, −11.97, −2.03, 2.73, 31.13). Δ ≤ 4 sharpness open |
| 11 | Log-convexity; per-graph identifiability (rank = A(G)); equality in A ≤ min(\|R\|−1, r, 3) for Δ ≤ 6, failing at Δ = 7 | Exponential-family facts (Brown 1986); the Δ ≤ 6 equality is by enumeration | Textbook | **Known** (the Δ = 7 set is a small new fact) | Proofs VERIFIED (after the short-draft repairs); Δ ≤ 6 enumeration NOT re-run independently |
| 12 | Extremal trees of LO(·;0,0,γ): path is the unique minimiser and star the unique maximiser for γ > 0, reversed for γ < 0 | The paper's direct proof is VERIFIED. A **complete derivation from Cruz–Rada** is written below | **Cruz–Rada 2019, Theorems 2.1 and 3.1** (both identities give uniqueness) | **Known (corollary)**. The full paper's old sentence "the path half does not follow…" referred only to Rada 2026 §4.2 and understated Cruz–Rada | VERIFIED (proof below; Cruz–Rada read) |
| 13 | Closed forms; bracket, Cauchy–Schwarz, (Δ,δ) and ratio bounds | Direct | γ = 0 cases: Molina–Sigarreta 2025, Granados 2025, Portilla 2025; exponential-index inequalities: Carballosa et al. 2023 | **Routine extensions** | Lean-checked (inequalities only); not re-checked here |
| 14 | **Δ ≤ 3: the q-histogram determines the profile at every order** (candidate addition, not in either manuscript) | Proof below. Enumeration: `certificates/by_delta.py` finds no collision up to order 18 | Not found | New but elementary | VERIFIED (proof plus enumeration) |
| 15 | First collision order by maximum degree: none for Δ ≤ 3; 16 for Δ ≤ 4 and Δ ≤ 5; 13 for Δ ≥ 6 (up to order 18) (candidate addition) | `certificates/by_delta.py`, `first_collisions_upto18.json` lists every colliding class | Not found | New, computational | VERIFIED (enumeration up to order 18) |

### Proof of 12 from Cruz–Rada 2019

Their setting: n ≥ 3, and L = {(i,j) : 1 ≤ i ≤ j, i + j ≤ n, (i,j) ≠ (1,1)}. Theorem 2.1 is the identity
φ(T) = φ(P_n) + Σ_{(i,j)∈L} [f(i,j) − f(1,2)] (i+j)/(ij) · m_ij(T), with
f(i,j) = ij/(i+j) (φ_ij + 2φ_12 − 3φ_22). Theorem 3.1 is the identity
φ(T) = φ(S_n) + Σ_L [φ_ij − φ_{1,n−1}] m_ij(T).

Take φ_ij = e^{γ q_ij}, γ > 0, and E = e^{γ/3} > 1. Then f(1,2) = f(2,2) = 2(E−1) > 0. For every other
pair of L, f(i,j) > 2(E−1):

* **i, j ≥ 2, (i,j) ≠ (2,2).** φ_ij ≥ 1, so the bracket is at least 2(E−1) > 0. Also ij/(i+j) > 1,
  because ij − i − j = (i−1)(j−1) − 1 ≥ 1.
* **(1,j), j ≥ 3.** j/(j+1) ≥ 3/4 and φ_1j ≥ e^{γ/2}, so f ≥ (3/4)(e^{γ/2} + 2E − 3). This exceeds
  2(E−1) if and only if 3e^{γ/2} > 2E + 1. With x = e^{γ/6} > 1 that reads
  3x³ − 2x² − 1 = (x−1)(3x²+x+1) > 0.

Hence every term of Theorem 2.1 is ≥ 0, and it is > 0 unless m_ij = 0 for all pairs other than (1,2) and
(2,2), that is T = P_n. Similarly φ_{1,n−1} = e^{γ(n−2)/n} is the strict maximum of φ on L, since q is
largest exactly at (1,n−1). So Theorem 3.1 gives φ(T) ≤ φ(S_n), with equality only for S_n.

For γ < 0 the same steps reverse:
* E < 1, and every bracket is ≤ 2(E−1) < 0.
* Multiplying by a factor > 1, or by one ≥ 3/4, moves a negative bracket further below 2(E−1). The
  polynomial inequality reverses because x < 1.

∎ This is now written into `main.tex` and the short draft as an attribution, not as a new result.

### Proof of 14 (Δ ≤ 3)

* For a tree of order n ≥ 3 with Δ ≤ 3 the admissible pairs are (1,2), (1,3), (2,2), (2,3), (3,3), with
  q = 1/3, 1/2, 0, 1/5, 0.
* The q-histogram therefore fixes m_12, m_13, m_23 and s = m_22 + m_33, and its total fixes n − 1.
* Counting each vertex once over its incident edges gives Σ_{i≤j} (1/i + 1/j) m_ij = n. So
  m_22 + (2/3) m_33 = n − (3/2) m_12 − (4/3) m_13 − (5/6) m_23.
* Together with m_22 + m_33 = s this determines m_22 and m_33.

∎ For n ≤ 2 the class is {K_1, K_2}. The same argument fails for Δ ≥ 4, because the class {(1,2),(2,4)}
has two pairs with different vertex weights and the system has a free direction. The order-16 witness
uses exactly that direction: Δm_12 = −2, Δm_24 = +2, Δm_22 = +3, Δm_44 = −3.

## 3. Honest assessment of the surviving mathematics

* **Genuinely new, not found anywhere, but computational:**
  * the exact first orders 13 and 16;
  * the per-Δ table: none for Δ ≤ 3, 16 for Δ ≤ 5, 13 for Δ ≥ 6;
  * the explicit witnesses.

  The all-order extension is a known device, and the class-wide indistinguishability is a one-line
  consequence of Rada 2019.
* **Not new:**
  * the q-histogram dependence;
  * algebraic-γ separation;
  * generic discrimination;
  * the extremal trees;
  * convexity and identifiability;
  * the closed forms and termwise bounds.

  These are known results or routine specialisations, and both manuscripts now credit them as such.
* **Small incremental items:**
  * the Laguerre crossing bound with its Δ = 6 sharp example;
  * the parent-distinctions statement;
  * the Δ = 7 identifiability set.
* **Referee objections to expect:**
  1. "A finite search for the smallest tree realising a known kernel vector". The minimal orders have no
     structural proof; the Δ ≤ 3 proof above is the only non-computational threshold statement.
  2. Chemical relevance at n ≥ 13 or 16 is weak, since real isomer degeneracy there is dominated by
     equal-profile isomers.
  3. Individual indices (SDD, ISDD) fail earlier, so the 13/16 statement concerns the class, not
     particular indices.
* **Two additions that would strengthen the paper without inflating it.** Both are proposals and are
  not yet in either manuscript.
  1. The Δ ≤ 3 theorem (full proof) with the per-Δ first-order table, which turns the single threshold
     into a short classification.
  2. A lattice description of the collision directions. For each Δ, the kernel of the map
     "profile → (q-histogram, vertex identity, integrality of n_k)" explains why Δ = 4, 5 need order 16
     while Δ ≥ 6 needs only 13. This is not done.
