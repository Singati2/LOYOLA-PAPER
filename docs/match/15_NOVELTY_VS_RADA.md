# 15 — Novelty of the manuscript against the work of J. Rada

Date: 2026-10-20
Manuscript: `wt-fig/main.tex`, branch `review/match-figure-2026-10-20`, commit `e19f506` (read-only; nothing edited).

## 0. Sources actually read

All four PDFs were downloaded with curl from `match.pmf.kg.ac.rs/electronic_versions/...` into `match_drafts/rada/` and read in full with `pdftotext -layout`. MD5 checksums match the copies used in the reference audit (`13_REFERENCE_AUDIT.md`).

| Key | Paper | File | Read |
|---|---|---|---|
| Rada2026LinearVDB | J. Rada, A finite-dimensional linear framework for VDB topological indices, MATCH 96 (2026) 841–863 | `match96n3_841-863.pdf` | whole paper; Figure 1 checked as an image (p. 849) |
| Rada2019ExpVDB | J. Rada, Exponential VDB topological indices and discrimination, MATCH 82 (2019) 29–41 | `match82n1_29-41.pdf` | whole paper |
| RadaRodriguezSigarreta2022Weak | Rada, Rodríguez, Sigarreta, Weakly discriminating VDB topological indices, MATCH 87 (2022) 97–108 | `match87n1_97-108.pdf` | whole paper |
| CruzRada2019PathStar | Cruz, Rada, The path and the star as extremal values of VDB indices among trees, MATCH 82 (2019) 715–732 | `match82n3_715-732.pdf` | Sections 1–3 (pp. 715–727) |

Also used for one row only: Barman–Das, MATCH 95 (2026) 63–94 (`BarmanDas2026HSO`), octane index table (`tmp_refs/dl/match95n1_63-94.txt`, p. 79 as extracted).
**Not read for this report:** Gao–Gao 2024, Cruz–Monsalve–Rada 2020, Molina–Sigarreta 2025, Granados 2025, Portilla 2025, Carballosa et al. 2023, Brown 1986, Jameson 2006. Rows that depend on them are marked as such.

### What the Rada papers contain (only what was read)

**Rada 2026 (MATCH 96).**
- §2.1, p. 845: the edge-type vector m(G) on S_Δ with h = Δ(Δ+1)/2, and I_f(G) = ⟨γ_f, m(G)⟩. Every VDB index is a linear functional on R^h.
- §2.2–2.3, pp. 845–848: Theorem 1 and Corollary 1, polynomial interpolation of any weight system; Example 1 does this for Sombor on S_4.
- §3.1, pp. 848–849: strong discrimination fails because equal m(G) gives equal values for every VDB index. Figure 1 shows two chemical trees S, T with identical edge-type vectors (T as drawn has 11 vertices). The paper says: "By attaching the same pendent path to both trees, one obtains such counterexamples with arbitrarily many vertices."
- §3.2, pp. 849–851: Definition 1 (weak discrimination, citing Rada 2019) and the difference space W(C). Theorem 2: W(C) ∩ ker⟨γ,·⟩ = {0} is sufficient. Example 2 shows it is not necessary.
- §3.3–3.4, pp. 851–855: Theorem 3 (support restriction plus Q-linear independence) and Corollary 2 (forbidden edge types). Example 3 covers exponential indices with distinct algebraic λ_ij via Lindemann–Weierstrass. Example 4 covers catacondensed hexagonal systems and Example 5 a class of chemical trees.
- §4.1–4.2, pp. 855–859: the feasible polytope and its normal cones. Star: the cone is γ_{1,n−1} ≥ γ_ij for all (i,j), and strict inequalities make S_n the unique maximiser (p. 858). Path: γ_12 ≤ γ_ij and γ_22 ≤ γ_ij for (i,j) ∉ {(1,2),(2,2)}, which makes P_n the unique minimiser (pp. 858–859). Examples: Sombor, M_1, Randić with α < 0.
- §4.3, pp. 859–861: examples on T_4 and {C_4, P_4, S_4}.
- **Absent from the paper:** degree-ratio or imbalance weights; q-histograms; collision orders; parameter families; order-exchange counts; identifiability.

**Rada 2019 (MATCH 82, 29–41).**
- Eqs. (1)–(2), pp. 30–31: ϕ(G) = m(G)·ϕ on G_n. This representation is attributed there to Rada–Bermudo.
- Definition 2.1, p. 31: discrimination with respect to an equivalence relation.
- Example 2.2, p. 32: equal m implies equal ϕ for every ϕ.
- Definition 2.3 and eqs. (3)–(6), pp. 32–33: the m̂_ϕ-structure, i.e. class sums over pairs with equal weight.
- **Proposition 2.5, p. 34:** if m̂_ϕ(G) = m̂_ϕ(G′) then ϕ(G) = ϕ(G′).
- **Example 2.6, p. 35:** trees T, T′ in G_29 with m̂_χ(T) = (12, 12, 4) and m̂_χ(T′) = (10, 2, 16) on the classes listed there, and χ(T) = χ(T′).
- **Definition 3.1, p. 35:** exponential index e^ϕ.
- Theorem 3.3, p. 35: Lindemann–Weierstrass, cited from Baker.
- **Theorem 3.4, p. 36:** if every ϕ_ij is algebraic, then e^ϕ discriminates exactly the m̂_ϕ-classes on G_n.
- Corollary 3.5 covers the indices of Table 1. Section 4 shows that the extremal graphs of e^χ over G_n are S_n (minimum) and K_n (maximum).

**Rada–Rodríguez–Sigarreta 2022 (MATCH 87).**
- Weak discrimination: φ(H) = φ(H′) ⇔ m(H) = m(H′) (abstract; p. 99).
- **Example 2.1, pp. 100–101:** chemical trees of order 20p+9 with equal Randić index and different m.
- **Example 2.2, pp. 101–102:** M_1, HM, sum-connectivity, reciprocal sum-connectivity and harmonic all satisfy φ(1,3)=φ(2,2), φ(1,4)=φ(2,3), φ(2,4)=φ(3,3), so they fail on chemical trees. The trees in that example have order 17+p.
- Eq. (8), p. 102: the handshake relations.
- Theorem 2.3: Sombor is weakly discriminating on CT_n.
- **Theorem 3.1, p. 105:** Z-linearly independent weights give weak discrimination on any class.
- Theorem 3.3 (Besicovitch) and the prime index.
- **Theorem 3.8, p. 106:** if the φ_ij are distinct algebraic numbers, then e^φ is weakly discriminating on any class.

**Cruz–Rada 2019 (MATCH 82, 715–732).**
- Eq. (1), p. 716: the linear representation, noted there as "bond incident degree indices".
- Eqs. (3)–(4), p. 718: Σ(1/i+1/j)m_ij = n and Σ m_ij = n−1 on trees.
- f(i,j) = ij/(i+j)(ϕ_ij+2ϕ_12−3ϕ_22) with f(1,2) = f(2,2), p. 717.
- Theorem 2.1 (path identity) and Corollary 2.2 (path bounds), pp. 718–719.
- Theorem 3.1 (star identity, g = ϕ) and Corollary 3.2 (star bounds), pp. 725–726.
- Table 2: extremal trees of exponential versions of classical indices. Imbalance weights do not appear.

### Check on the manuscript's "no earlier ratio collisions" claim (L634)

I computed the q-histograms of every explicit colliding pair in the Rada papers:
- **Rada 2019 Ex. 2.6:** n_{1/3} is 24 against 26. Not a ratio collision.
- **RRS 2022 Ex. 2.1:** n_{1/3} is 16p+8 against 18p+8. Not a ratio collision.
- **RRS 2022 Ex. 2.2:** S has n_{1/2} = 6 and n_{1/5} = 4; T has n_{3/5} = 4 and n_{1/3} = 6. Not a ratio collision.
- **Rada 2026 Fig. 1:** the two trees have equal m, so their profiles are not distinct.

None of these is a pair with distinct profiles and equal q-histograms. This agrees with the manuscript's statement for the works read here.

## 1. Classification table

Statuses:
- **KNOWN**: the result itself is stated in the source cited.
- **KNOWN IN SUBSTANCE**: a direct specialisation or routine consequence of a cited result.
- **NEW**: not found in the works read. This does not claim global novelty.
- **UNCLEAR**: depends on cited non-Rada work that was not read.

Line numbers refer to `main.tex` at e19f506.

### 1a. Formal statements

| # | Statement (label, line) | Content | Status | Evidence |
|---|---|---|---|---|
| 1 | Lemma `prop:indep`, L391 | For Δ ≥ 3 the vectors (1, ln ij, ln(i+j), q_ij) span R⁴, so a shift of (α,β) plus a scale cannot reproduce γ ≠ 0. This fails for Δ ≤ 2. | NEW | No parameter family, and no independence of the imbalance direction, appears in Rada 2019, 2026, RRS 2022 or Cruz–Rada 2019. Elementary determinant argument. |
| 2 | Theorem `thm:logconvex`, L458 | log LO is convex, with gradient E[z] and Hessian Cov(z); it is monotone in γ; strictness criterion. | NEW (elementary) | Not in the Rada papers. This is the standard log-sum-exp fact; the manuscript calls it elementary (L299). |
| 3 | Theorem `thm:ratioplane`(i), L551 | On Π = {β = −2α}, LO depends only on the q-histogram. Graphs agree on all of Π iff their histograms are equal; otherwise they differ almost everywhere on Π. | KNOWN IN SUBSTANCE (the dependence); the identification of Π is NEW | The dependence is Rada 2019 Prop. 2.5 (p. 34) for weights that are constant on q-classes, plus the identity 4ij/(i+j)² = 1−q². The "iff/a.e." clause is a routine exponential-sum and real-analytic argument. Π itself does not appear in the works read. |
| 4 | Theorem `thm:ratioplane`(ii), L557 | For algebraic γ ≠ 0, LO(·;0,0,γ) is equal iff the q-histograms are equal; the same holds for all but finitely many real γ on a finite set. | KNOWN IN SUBSTANCE | Direct specialisation of **Rada 2019 Thm 3.4 (p. 36)** to ϕ_ij = γq_ij, whose m̂_ϕ-classes are the q-classes. The manuscript says so at L634. Rada states it over G_n, but the argument does not depend on the order. The real-γ clause is routine. |
| 5 | Theorem `thm:ratioplane`(iii), propagation device, L561–566 | Attaching a pendant path of length L at a leaf next to a degree-d vertex changes both profiles by −(1,d)+(2,d)+(L−1)(2,2)+(1,2). | KNOWN (device) | **Rada 2026 §3.1, p. 849**: "By attaching the same pendent path to both trees, one obtains such counterexamples with arbitrarily many vertices." Credited at L601 and L634. Keeping *distinct* profiles with *equal* histograms is a one-line adaptation. The change vector is correct (checked). |
| 6 | Theorem `thm:ratioplane`(iii), existence plus witnesses, L567–569 and proof L605–631 | Explicit trees at order 13 (all trees) and order 16 (Δ ≤ 4) with distinct profiles and equal q-histograms, and hence such pairs at every n ≥ 13 (n ≥ 16 for Δ ≤ 4). | NEW | No ratio-class collision in any of the four papers (see §0). The Rada examples concern product or sum classes, or equal m. |
| 7 | Corollary `cor:ratioclass`, L636 | Every I_f(G) = Σ f(ρ_uv) depends only on the q-histogram, so the trees of #6 collide for GA, AG, SDD, ISDD, the diminished Sombor index, DRSO, and others. | KNOWN IN SUBSTANCE (dependence); the witnesses come from #6 | Rada 2019 **Prop. 2.5** for weights that depend only on the ratio. The manuscript says so in Remark `rem:ratioclass` (L652). It is the ratio analogue of the sum-class argument in RRS 2022 Ex. 2.2. |
| 8 | Proposition `prop:offplane`, L674 | For rational α, β and algebraic γ ≠ 0: LO(G) = LO(H) iff every q-class sum c_q vanishes. A nonzero algebraic γ never merges graphs that the parent separates. | NEW | Not stated in the works read. The method is that of Rada 2019 Thms 3.3–3.4 (independence over the algebraic numbers, so algebraic coefficients are allowed). It is not a direct specialisation of Thm 3.4, because the LO weights are not e^{algebraic} when α, β ≠ 0. |
| 9 | Proposition `prop:laguerre`, L729 | A difference along γ has at most V ≤ r−1 real zeros, with V's parity. For Δ ≤ 4 there are 6 imbalances, so at most five order exchanges. | NEW (routine application of a classical rule) | Not in the Rada papers. It is Laguerre's extension of Descartes' rule of signs (Jameson 2006, not read here). |
| 10 | Proposition `prop:identrank`, L791 | A(G) equals the Hessian rank and there are 3−A(G) rescaling directions; A(G) ≤ min(\|R\|−1, r, 3); explicit direction when r = 2. | NEW | Not in the Rada papers. Standard exponential-family rank reasoning (Brown 1986, not read). |
| 11 | Example `ex:spider`, L845 | Spider with four legs of length 3: γ is confounded with (α,β). | NEW (illustration) | — |
| 12 | Proposition `prop:gamma_eq_0_or_inf`, L863 | Limits of LO / e^{γ·imb_max} and of LO / e^{γ·imb_min}. | NEW (elementary) | — |
| 13 | Proposition `prop:collision`, L901, first sentence | Equal count vectors give equal values for every VDB index. | KNOWN | **Rada 2026 §3.1, pp. 848–849**; Rada 2019 Ex. 2.2, p. 32; RRS 2022 eq. (2) and p. 99. |
| 14 | Proposition `prop:collision`, octane part, L906–912 | 16 count vectors among the 18 octanes; the pairs {3-, 4-methylheptane} and {3,4-dimethylhexane, 3-ethyl-2-methylpentane}. | KNOWN IN SUBSTANCE | In the octane index table of **Barman–Das 2026** (cited as `BarmanDas2026HSO`; p. 79 as extracted) both pairs have identical rows for all tabulated degree-based indices. The manuscript itself says "known degree-pair ceiling" (L310). The irreducible-SSE floor 2.925 °C² (L928) is a NEW computation. |
| 15 | Proposition `prop:generic`, L947 | For almost every θ ∈ R³, LO separates any two distinct count vectors. With countably many pairs, almost every θ is weakly discriminating on every class (L976). | NEW | Not stated in the works read. It is close in spirit to the point-wise sufficient criteria of **RRS 2022 Thm 3.1 (p. 105) and Thm 3.8 (p. 106)** and **Rada 2026 Thm 3, Cor. 2 and Ex. 3 (pp. 852–854)**, which give specific weakly discriminating indices through Z/Q-linear independence. Prop. `generic` is the almost-everywhere version over a parameter space. The manuscript notes that it is inherited from the parent (L981). |
| 16 | Example `ex:sumconn`, L997 | The RRS 2022 Ex. 2.2 trees (order 17+t) are separated by LO(0,−½,1), with D(1) ≈ 0.2255. | Trees KNOWN; separation NEW | The trees and their difference vector are in RRS 2022 Ex. 2.2, pp. 101–102 (difference and order rechecked). D(γ) recomputed: D(1) = 0.2255. |
| 17 | Proposition `prop:closedforms`, L1205 | LO on K_n, C_n, P_n, S_n, K_{a,b}, Q_k, W_n, F_p and r-regular graphs. | NEW (routine) | Not in the Rada papers, except that Rada 2019 p. 37 gives e^χ(S_n) for exponential Randić. The γ = 0 cases are presumably in the GM literature, which was not checked. |
| 18 | Proposition `prop:extremal`, L1269 | For γ > 0, P_n is the unique minimiser and S_n the unique maximiser of LO(·;0,0,γ) on trees, with explicit bounds; the roles reverse for γ < 0. | KNOWN IN SUBSTANCE | **Cruz–Rada 2019 Thm 2.1 / Cor. 2.2 (pp. 718–719)** for the path and **Thm 3.1 / Cor. 3.2 (pp. 725–726)** for the star, once one checks f > f(1,2) (the manuscript does this, L1295). The star half is also **Rada 2026 §4.2, p. 858** (strict γ_{1,n−1} > γ_ij holds, since q is uniquely maximal at (1,n−1) among pairs with i+j ≤ n). The path half does **not** follow from Rada 2026 p. 858 (e^{γ/3} > e^{γ/5}), as the manuscript says correctly. Gao–Gao 2024 was not read. |
| 19 | Proposition `thm:bracket`, L1331 | m·ψ_min ≤ LO ≤ m·ψ_max, with equality cases. | KNOWN IN SUBSTANCE | Immediate from the linear representation (Rada 2026 §2.1): a sum of m terms that each lie in [min, max]. |
| 20 | Corollary `thm:cs`, L1363 | Cauchy–Schwarz interpolation. | KNOWN IN SUBSTANCE | Cauchy–Schwarz; midpoint case of #2. Carballosa et al. 2023 was not read. |
| 21 | Proposition `thm:upper_Delta`, L1399 | Upper bound in m and Δ for α, β, γ ≥ 0, with equality cases. | UNCLEAR | Not in the Rada papers. The manuscript says the γ = 0 versions are known (Molina, Granados, Portilla; not read). The γ > 0 extension and its equality cases look routine. |
| 22 | Proposition `thm:lower_delta`, L1436 | Lower bound in m and δ, with equality cases. | UNCLEAR | Same as #21. |
| 23 | Proposition `thm:ratio_bound`, L1468 | c_min·I_h ≤ LO ≤ c_max·I_h. | KNOWN IN SUBSTANCE | Termwise argument, as in #19. |
| 24 | Corollary `cor:ratio_uniform`, L1508 | Uniform version over P_Δ. | KNOWN IN SUBSTANCE | Same argument as #23. |

**Counts for the formal statements (24 rows):**

| Status | Count | Rows |
|---|---|---|
| KNOWN | 2 | #5, #13 |
| KNOWN IN SUBSTANCE | 9 | #3, #4, #7, #14, #18, #19, #20, #23, #24 |
| NEW | 11 | #1, #2, #6, #8, #9, #10, #11, #12, #15, #16, #17 |
| UNCLEAR | 2 | #21, #22 |

- Rows #3, #14 and #16 also contain a NEW sub-part (Π; the SSE floor; the separation at γ = 1).
- Of the 11 NEW rows, #2, #9, #11, #12 and #17 are elementary or routine.
- The substantive new mathematics is #1, #6, #8, #10 and #15.

### 1b. Computational and remark-level claims

| Claim (line) | Status | Evidence |
|---|---|---|
| Minimality of the orders 13 (all trees) and 16 (Δ ≤ 4): q-histograms determine profiles up to orders 12 and 15 (Remark `rem:floor`, L710; Table `tab:firstfail`, L1076; L634) | NEW (computer-assisted) | Not in the works read. |
| Degeneracy floor: the number of distinct profiles bounds the number of distinct values of any VDB index (L897–899, L1049–1051) | KNOWN IN SUBSTANCE | Rada 2026 §3.1, pp. 848–849. The counts (79/106, 566/570, 809/810, 1095/1100, 1191/1194) are NEW computations. |
| SDD merges profiles at order 9, ISDD at order 10 (L663–669) | NEW (computational) | — |
| GA merges two different q-histograms at order 17 (L721–726) | NEW (computational) | — |
| Sharpness of five crossings at Δ = 6, order 12 (Remark `rem:crossings`, L765) | NEW | Open for Δ ≤ 4 (stated in the manuscript). |
| Δ = 7 is the first failure of equality in identrank (ii) (Remark `rem:delta7`, L829) | NEW | — |
| K_4 against K_{1,3} at γ = ln 4 (L706–707) | NEW (illustration) | — |
| Remark `rem:countdim` (L932): m_11 = 0, Σm = n−1, Σ(1/i+1/j)m_ij = n | Identities KNOWN; data ranks NEW | **Cruz–Rada 2019 eqs. (3)–(4), p. 718**; RRS 2022 eq. (8), p. 102 (the n_i form). These identities are not cited at L932. |
| Off-Π recovery at order 16 (L1112–1129): 3475/3476 → 4069 at γ = 1, and related counts | NEW (computational) | — |

## 2. Chemical relevance of each NEW item

Each sentence is grounded in the manuscript (Δ ≤ 4 means hydrogen-suppressed alkane skeletons, L330–332).

- **#1 Lemma `indep`.** For any set of alkane skeletons that contains a branching carbon (Δ ≥ 3), no retuning of the Gutman–Milovanović exponents reproduces the imbalance factor. γ is therefore a different weighting of the same degree-pair information (L986–987), not a new kind of information.
- **#2 Log-convexity.** For every molecule, log LO is convex and non-decreasing in γ, and strictly increasing unless all bonds join carbons of equal degree. On regular skeletons such as cycloalkane rings γ has no effect (L259, L472–474).
- **#6 Ratio collisions.** Up to order 15, two alkane skeletons with different degree-pair counts are always told apart by their bond-imbalance histogram. From order 16 on there are skeletons with different counts that every degree-ratio descriptor (GA, AG, the diminished Sombor and degree-ratio Sombor indices, SDD) assigns the same value (Cor. `cor:ratioclass`; Remark `rem:floor`).
- **#8 Parent distinctions survive.** At the rational exponents of the classical indices (Randić, sum-connectivity, Zagreb), a nonzero algebraic γ never merges two molecules that the classical index separates. It can split ties, as for the sum-connectivity pair of Example `ex:sumconn` and the order-16 trees of Section `sec:degeneracy`.
- **#9 Crossing bound.** Two alkane skeletons can change their order at most five times as γ varies, whatever (α,β) is. Tuning γ cannot reorder a pair of molecules arbitrarily often (L739–742).
- **#10 Identifiability.** If the bonds of a molecule realise only two imbalance values, γ is exactly confounded with (α,β), as on the spider of Example `ex:spider`. On the octane set the union of realised pairs has affine dimension 3, so fitted γ values there are free of exact confounding of this kind (Remark `rem:dataset`).
- **#11 Spider example.** This gives one concrete chemical tree (Δ = 4) on which γ cannot be identified from that molecule's values alone.
- **#12 γ-limits.** For large |γ| the index is dominated by the most imbalanced bonds (γ → +∞) or the least imbalanced bonds (γ → −∞). Extreme values of γ therefore reduce the descriptor to a weighted count of one bond type.
- **#15 Generic discrimination.** Almost every parameter point separates all alkane skeletons with different degree-pair counts. The octane collisions of Table `tab:collisions` (equal counts) are the only collisions common to every parameter value, and the property is inherited from the parent (L981).
- **#16 Sum-connectivity pair.** The imbalance factor separates the chemical trees of order 17+t that the sum-connectivity index merges, though only by a small amount for small γ (L1007–1008).
- **#17 Closed forms.** On regular molecular graphs, such as cycloalkane rings, LO reduces to the parent value for every γ.
- **Minimal orders 13/16 (computer-assisted).** For chemical-tree descriptors this marks the size, order 16 with Δ ≤ 4, at which degree-ratio indices first lose degree-pair information. Below that size these indices are as discriminating as any vertex-degree-based index (Remark `rem:floor`).
- **SDD/ISDD and GA merges.** Individual degree-ratio indices can fail earlier than the histogram does: SDD fails on chemical trees of order 9 and ISDD at order 10, through coincidences among their values (L663–669).

## 3. Proposed introduction paragraph and credit fixes

### 3a. Proposed insertion (place immediately before "Our contributions are as follows.", L297)

```latex
Several facts used below are known. Every vertex-degree-based index is a
linear function of the edge-degree-pair counts $m_{ij}$
\cite{Rada2019ExpVDB, RadaRodriguezSigarreta2022Weak, Rada2026LinearVDB},
so graphs with equal counts receive equal values of every such index, and
attaching the same pendant path to two such graphs gives examples of every
larger order~\cite[Section~3.1]{Rada2026LinearVDB}. An index whose edge
weights coincide on a class of degree pairs depends on a graph only through
the class sums of its counts~\cite[Proposition~2.5]{Rada2019ExpVDB}, and the
exponential of an index with algebraic edge weights separates exactly these
class sums~\cite[Theorem~3.4]{Rada2019ExpVDB}. Applied to the weights
$\gamma q_{ij}$, these two results give Theorem~\ref{thm:ratioplane}(ii) and
the dependence on the $q$-histogram in Corollary~\ref{cor:ratioclass}. The
path and the star are the extremal trees of the pure-$\gamma$ points by the
criteria of Cruz and Rada~\cite{CruzRada2019PathStar}. New here are the ratio
plane $\Pi$, on which every point of the family depends on a graph only
through its $q$-histogram; explicit trees with distinct profiles and equal
$q$-histograms at order $13$, and at order $16$ with $\Delta \le 4$, together
with the computer-assisted result that no smaller trees have this property;
the fact that at rational $(\alpha,\beta)$ a nonzero algebraic $\gamma$ never
merges two graphs that the parent separates; the bound of five order exchanges
along $\gamma$ for $\Delta \le 4$; and per-graph identifiability. For alkane
carbon skeletons, the $q$-histogram, and with it every degree-ratio index such
as $GA$, $AG$ or the diminished Sombor index, carries the full degree-pair
information up to order $15$ and not beyond. At the rational exponents of the
classical indices the imbalance factor never merges two molecules that the
parent separates, and the order of two such molecules changes at most five
times as $\gamma$ varies.
```

It introduces no new numbers. Every number in it (13, 15, 16, Δ ≤ 4, five) already appears in the manuscript.

### 3b. Over- and under-credit (line, current text, problem, fix)

1. **L287–288**
   - *Current:* "On graphs with $\Delta \le 4$ every BID index is a linear functional of the ten edge-degree-pair counts~\cite{Rada2026LinearVDB}"
   - *Problem:* Under-credits the earlier work. The representation φ(G) = m(G)·φ is eq. (1)–(2) of Rada 2019 (pp. 30–31, attributed there to Rada–Bermudo) and of RRS 2022 (p. 98), and eq. (1) of Cruz–Rada 2019 (p. 716). Rada 2026 develops it systematically (p. 845), so the citation itself is correct.
   - *Fix:* "... of the ten edge-degree-pair counts, a representation used in~\cite{Rada2019ExpVDB, RadaRodriguezSigarreta2022Weak} and developed systematically in~\cite{Rada2026LinearVDB}, so ..."

2. **L300–306, contribution (ii)**
   - *Current:* "The ratio-plane theorem (Theorem~\ref{thm:ratioplane}) characterises exactly what the pure-$\gamma$ points at algebraic $\gamma \neq 0$ discriminate, by Rada's Lindemann--Weierstrass argument~\cite{Rada2019ExpVDB}, with tree collisions ... Its corollary extends the collisions to every degree-ratio index ..."
   - *Problem:* The item lists as a contribution a characterisation that is a direct specialisation of Rada 2019 Thm 3.4. It also does not say that the corollary's dependence statement is Rada 2019 Prop. 2.5, which the body states at L652 but the list does not. This overstates our part and under-credits Rada.
   - *Fix:* replace the item with:
     ```latex
     \item[(ii)] The ratio plane $\Pi$ (Theorem~\ref{thm:ratioplane}), on
     which the family depends on a graph only through its $q$-histogram.
     That the pure-$\gamma$ points at algebraic $\gamma \neq 0$ separate
     exactly the $q$-histograms is Theorem~3.4 of~\cite{Rada2019ExpVDB}
     applied to the weights $\gamma q_{ij}$, and that no degree-ratio index
     separates more is Proposition~2.5 there. New are explicit trees with
     distinct profiles and equal $q$-histograms at every order from $13$, and
     from $16$ for $\Delta \le 4$, and the computer-assisted result that these
     orders are the first. The corollary carries the collisions to every
     degree-ratio index, such as $GA$, $AG$ and the diminished Sombor index.
     ```

3. **L310, contribution (iv)**
   - *Current:* "Two octane collision pairs realising the known degree-pair ceiling (Proposition~\ref{prop:collision})"
   - *Problem:* "Known" has no citation. The two octane pairs are also already visible as identical rows in the octane index table of Barman–Das 2026 (cited elsewhere as `BarmanDas2026HSO`). Listing them as a contribution under-credits that work.
   - *Fix:* "The degree-pair ceiling~\cite[Section~3.1]{Rada2026LinearVDB} on the octanes, where two isomer pairs share their counts (their tabulated degree-based index values already coincide in~\cite{BarmanDas2026HSO}) (Proposition~\ref{prop:collision}), value counts ..."

4. **L539–541**
   - *Current:* "Rada~\cite{Rada2026LinearVDB} shows that no vertex-degree-based index separates trees with equal profiles, and gives sufficient linear criteria for an index to separate all distinct profiles."
   - *Problem:* Two small issues:
     - The observation is older (Rada 2019 Ex. 2.2, p. 32).
     - Rada 2026's criteria (Thm 2, Thm 3, Cor. 2) are for a class of graphs of fixed order. The first point-wise criterion of this kind is RRS 2022 Thm 3.1.
   - *Fix:* "Graphs with equal profiles receive equal values of every vertex-degree-based index~\cite{Rada2019ExpVDB, Rada2026LinearVDB}, and sufficient linear criteria for an index to separate all distinct profiles within a class of graphs of fixed order are given in~\cite{RadaRodriguezSigarreta2022Weak, Rada2026LinearVDB}."

5. **L634**
   - *Current:* "Explicit trees of this kind for a single index were given by Rada~\cite[Example~2.6]{Rada2019ExpVDB}, who exhibits two trees on $29$ vertices that have different class counts and equal Randi\'c index."
   - *Problem:* The sentence is accurate (p. 35) but leaves out RRS 2022 Ex. 2.1, which gives an infinite family of chemical trees with equal Randić index and different counts.
   - *Fix:* append ", and Rada, Rodr\'{\i}guez and Sigarreta~\cite[Example~2.1]{RadaRodriguezSigarreta2022Weak} give an infinite family of chemical trees with equal Randi\'c index and different counts."
   - The sentence that follows, "We found no earlier determination of the orders 13 and 16, or of explicit colliding trees for degree-ratio indices", is consistent with all four papers read; see the q-histogram check in §0.

6. **L932–937, Remark `rem:countdim`**
   - *Current:* "... since a vertex of degree $d$ lies on $d$ edges, $\sum_{i \le j} (1/i + 1/j)\,m_{ij} = n$."
   - *Problem:* Under-credit: these identities are eqs. (3)–(4) of Cruz–Rada 2019 (p. 718); compare RRS 2022 eq. (8).
   - *Fix:* append "(see~\cite[eqs.~(3)--(4)]{CruzRada2019PathStar})".

7. **L976**
   - *Current:* "In the terminology of Rada, Rodr\'{\i}guez and Sigarreta~\cite{RadaRodriguezSigarreta2022Weak}, an index is weakly discriminating ... As there are countably many pairs of count vectors, Proposition~\ref{prop:generic} gives that almost every point of the family is weakly discriminating over every class at once."
   - *Problem:* Under-credit: the point-wise sufficient conditions are not mentioned, even though the almost-everywhere statement is their parameter-space counterpart. Those conditions are:
     - Z-linear independence of the weights (RRS 2022 Thm 3.1);
     - exponentials of distinct algebraic weights (RRS 2022 Thm 3.8; Rada 2026 Example 3);
     - support restrictions (Rada 2026 Thm 3, Cor. 2).
   - *Fix:* insert before "As there are": "They also showed that weights linearly independent over $\mathbb{Z}$, for instance exponentials of distinct algebraic numbers, give weakly discriminating indices~\cite[Theorems~3.1 and~3.8]{RadaRodriguezSigarreta2022Weak}, and support restrictions of this criterion are given in~\cite[Theorem~3, Corollary~2]{Rada2026LinearVDB}."

8. **L262–266 (optional clarification, not a credit error)**
   - *Current:* "The family is a three-parameter subfamily of the exponential vertex-degree-based indices of Rada~\cite{Rada2019ExpVDB}"
   - *Problem:* Every index with positive weights is formally an exponential index, so the inclusion carries no content of its own. Rada's discrimination theorem applies only where the exponent weights are algebraic, which here means the pure-γ points. A reader may take Rada's theorem to cover LO in general.
   - *Fix:* append "; Rada's discrimination theorem~\cite[Theorem~3.4]{Rada2019ExpVDB} applies to it where the exponents $\alpha\ln(ij) + \beta\ln(i+j) + \gamma q_{ij}$ are algebraic, in particular at the pure-$\gamma$ points."

**Checked and correct as written (no change needed):**

| Line | Text | Source |
|---|---|---|
| L201 | abstract, "By theorems of Rada" | Thm 3.4 and Prop. 2.5. "Results" would be slightly more exact. |
| L228–229 | — | Rada 2026 |
| L280 | — | Rada 2019 Def. 3.1 |
| L601 and L634 | the pendant-path device | Rada 2026 p. 849 |
| L634 | Part (ii) = Thm 3.4 | Rada 2019 |
| L652 | Prop. 2.5 | Rada 2019 |
| L919 | — | Rada 2026 |
| L983–985 | — | Rada 2026 |
| L994 | Ex. 2.2 | RRS 2022: χ and √(x+y) are in its list |
| L999–1000 | difference vector and order 17+t | RRS 2022 Ex. 2.2, rechecked |
| L1039 | — | Rada 2019 |
| L1295 | Cruz–Rada Thm 2.1/Cor. 2.2 and Thm 3.1/Cor. 3.2; Rada 2026 §4.2 star half holds and path half fails | both correct |
| L1872–1875 | — | Rada 2019 Thm 3.4 and Prop. 2.5 |

**No over-credit to Rada was found.** Every attribution to Rada in the manuscript matches what the papers state.


---
## Integration note (2026-10-20)

Applied after checking the cited passages in the downloaded texts (Rada 2019 Example 2.2 and Proposition 2.5 / Theorem 3.4; Rada-Rodriguez-Sigarreta 2022 Example 2.1, Theorems 3.1 and 3.8; Rada 2026 Section 3.1, Theorem 3, Corollary 2; Cruz-Rada eqs. (3)-(4)): a "known / new" paragraph before the contributions list (its chemical-relevance sentences were narrowed: no degree-ratio index separates all alkane skeletons of order 16 or more; a nonzero algebraic gamma never merges molecules the parent separates, at rational (alpha, beta); at most five order exchanges for chemical graphs), contribution (ii) rewritten to credit Rada 2019, credit fixes 1, 4, 5, 6, 7. Fix 3 applied without the Barman-Das parenthetical (only one table row was checked). Fix 8 (optional) not applied. No number or result changed.
