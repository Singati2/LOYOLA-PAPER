# Feynman review: "The Loyola Index Family and the Resolution Limit of Degree Imbalance"

- Date: 2026-10-20
- Commit reviewed: `325bd05` (worktree `wt-fig`), `main.tex` (2149 lines) with `supplement.tex` and `LEAN_VERIFICATION.md` consulted
- Mode: read-only. Nothing in the repository was edited. The checks used two scratch scripts (`scratchpad/feyn_checks.py`, `scratchpad/feyn2.py`) that read `octane_data.py` and recompute numbers the paper prints.
- Method: for each claim I tried to explain it from first principles to a bright undergraduate. Each place where that explanation stalled, needed an unstated step, or turned out simpler than the paper's own route is listed as a gap.
- Labels: **[VERIFIED]** means I recomputed it or checked it against the source text or repository. **[JUDGEMENT]** is reviewer opinion. Line numbers refer to `main.tex` unless marked "Suppl.".

---

## 1. The paper in five plain sentences

1. Give each bond of a molecular graph a weight based on the degrees of its two end atoms. The Gutman–Milovanović weight is `(d_u d_v)^α (d_u+d_v)^β`; the paper multiplies it by `e^{γq}`, where `q = |d_u − d_v|/(d_u + d_v)` measures how lopsided the bond is. Summing over bonds gives `LO(G; α, β, γ)` (l. 250–258, 340–360).
2. Because each bond's weight depends only on its degree pair, the index is a weighted count of bond types, and γ adds no structural information. It only reweights the same ten counts (for Δ ≤ 4) differently (l. 259, 285–289, 980–985).
3. When the weight depends only on the degree *ratio* (the "ratio plane", β = −2α, which includes pure γ), the index sees only the histogram of q values. That histogram first fails to determine the bond-type counts of a tree at 13 vertices, or 16 for chemical trees. The minimality comes from computer enumeration; the propagation to larger orders comes from a pendant-path construction (l. 546–632, 1036–1063).
4. The other mathematics is short and mostly classical. log LO is a log-sum-exp, so it is convex. By Descartes' rule, two graphs swap order along γ at most (number of distinct q values − 1) times, which is 5 for Δ ≤ 4. The path and the star are the extremal trees. The termwise bounds are elementary (l. 456–511, 727–761, 1265–1296, 1298–1517).
5. Chemically, freeing γ gave no demonstrated predictive gain. The apparent gain on vaporisation enthalpy (ΔH_vap) disappears once the parent model may search a wide enough box, the two preregistered boiling-point tests were negative, and ridge regression on the raw bond-type counts outperformed every single index (l. 1604–1798).

---

## 2. Section by section

### 2.1 Definition and "every LO is a function of the degree-pair count vector" (l. 250–259, 321–373, 893–921, 976–985)

**What is claimed.** `LO = Σ_{i≤j} m_ij (ij)^α (i+j)^β e^{γ q_ij}` (Eq. 2, l. 357–360). The index therefore depends on G only through the counts m_ij, and graphs with equal counts can never be separated (Prop. "Degree-pair ceiling", l. 899–921).

**Simplest correct explanation.** Sort the bonds into bins labelled by (degree, degree). Every bond in a bin gets the same weight, so the index is the sum over bins of (bin count × bin weight). Two molecules with identical bin counts receive identical values whatever the weights are. For alkanes (Δ ≤ 4) there are ten bins, and after removing (1,1) and the handshake identity only about 7–8 free directions remain (Remark l. 930–940).

**Where my explanation got stuck.**
- I did not get stuck. The statement is a one-liner that the paper itself attributes to Rada [Rada2026LinearVDB] (l. 285–287, 917, 983).
- [JUDGEMENT] The terms "vertex-degree-based", "BID", "degree-pair profile", "count vector", "edge-type vector" and "M-polynomial" (l. 226, 285, 337–338, 599, 895, 917) all name one object, and none of them is defined formally. A student will reasonably wonder whether "vertex-degree-based index" includes non-additive functions of the degree sequence. The paper's argument covers only edge-additive ones; the claim also holds for any function of the degree sequence, since the profile determines the degree sequence of a graph without isolated vertices, but that step is unstated.

**New or repackaging?** Repackaging, and the paper says so (l. 983–985). A skeptic would call this whole section background.

**Severity.** Clarity.

**Suggested fix.** Define "BID / vertex-degree-based index = Σ_edges φ(d_u, d_v)" once in §2 and use only one name for m = (m_ij).

---

### 2.2 Lemma 1: affine independence of the imbalance direction (l. 389–437)

**What is claimed.** On the admissible pairs with Δ ≥ 3, q_ij is not an affine function of (ln ij, ln(i+j)). So no shift of (α, β) combined with a rescaling reproduces the effect of γ. For Δ = 2 it can be reproduced.

**Simplest correct explanation.** Use the identity 4ij/(i+j)² = 1 − q² (l. 519). The parent family already "knows" the imbalance, through `ln(ij) − 2 ln(i+j) = ln(1 − q²) − ln 4`. So the parent can weight bonds by (1 − q²)^α, which for small q behaves like e^{−αq²}. The γ factor weights bonds by e^{γq}. Lemma 1 therefore says, in plain words, that **q is not an affine function of ln(1 − q²) on the realised pairs.** That is true and almost obvious, since q and q² are different functions. The only work in the lemma is checking it on four integer pairs (3⁸ ≠ 2¹³).

**Where my explanation got stuck.**
- **The lemma is binary, but the chemistry depends on degree.** [VERIFIED] On the nine chemical pairs (Δ ≤ 4, excluding (1,1)), regressing q on (1, ln ij, ln(i+j)) gives R² = 0.888, with a largest residual of 0.11. On the six distinct chemical q values {0, 1/7, 1/5, 1/3, 1/2, 3/5}, corr(q, −ln(1 − q²)) = 0.951. The paper's own determinant ≈ −0.0150 (l. 410) is a hint of the same near-collinearity. The new direction exists, but in the chemical range it is a thin slice. This, more than "box truncation", predicts the null QSPR results of §6, and the paper never connects the two.
- The phrase "the imbalance direction is affinely independent ... once a vertex of degree at least 3 is admitted" (l. 297) sounds like a property of a graph. It is actually a property of the full admissible pair set; the paper notes this itself in the Remark (l. 439–451) and in Prop. identrank.

**New or repackaging?** [JUDGEMENT] It is elementary and correct. A skeptic would say: "You have shown that e^{γq} is not a power of (1 − q²). Nobody doubted it."

**Severity.** Major as an omission: the quantitative version is what a reader needs.

**Suggested fix.** After the proof, add one sentence and a number: "On the chemical pairs, q is explained by the parent coordinates with R² ≈ 0.89 (corr(q, ln(1 − q²)) ≈ 0.95 over the six chemical q values), so the new direction is real but narrow; Section 6 should be read in that light."

---

### 2.3 Theorem 1: log-convexity (l. 453–515) and the "partition function" wording (l. 280–283)

**What is claimed.** log LO is convex in θ = (α, β, γ). Its gradient is the edge-weighted mean of z = (ln ij, ln(i+j), q) and its Hessian is the covariance of z.

**Simplest correct explanation.** log Σ e^{linear} is convex, a standard fact about log-sum-exp. Its derivative in γ is the weighted average of q, which is non-negative, so LO increases in γ unless every bond is balanced.

**Where my explanation got stuck.**
- Nowhere mathematically.
- [JUDGEMENT] The sentence "LO is the partition function of an exponential family on the edges of G" (l. 282–283) is jargon that does no work. Nothing later uses statistical-mechanics content beyond convexity and the covariance rank. In a paper that then models *thermodynamic* properties, a chemist may read "partition function" physically, as if LO were related to Z of the molecule. It is not.

**New or repackaging?** Textbook (Boyd and Vandenberghe; Brown 1986, cited at l. 811).

**Severity.** Clarity, with a risk of misreading.

**Suggested fix.** Either delete "partition function" or add the sentence "(in the formal, statistical sense only; LO has no thermodynamic meaning)".

---

### 2.4 Theorem 2: the ratio plane (l. 517–668), the central result

**What is claimed.**
- (i) On Π (β = −2α), LO depends only on the q-histogram n_q.
- (ii) At every algebraic γ ≠ 0, LO(·; 0, 0, γ) separates exactly the q-histograms; this rests on Lindemann–Weierstrass via Rada 2019, Thm 3.4.
- (iii) Some trees have distinct profiles but equal histograms: for every n ≥ 13, and for every n ≥ 16 when Δ ≤ 4. The corollary is that every degree-ratio index (GA, AG, SDD, ISDD, DRSO, diminished Sombor) is blind to the same pairs.

**Simplest correct explanation.**
- (i) If the weight depends only on the ratio d_u/d_v, bonds with the same ratio look identical. A (1,2) bond and a (3,6) bond are the same to such an index, as are a (1,3) and a (2,6), and also (2,2), (3,3) and (4,4).
- (ii) The pure-γ index is `Σ_q n_q x^q` with x = e^γ. Every q is rational. If L is a common denominator and y = e^{γ/L}, then **LO(G) − LO(H) is a polynomial in y with integer coefficients**. Such a polynomial can vanish only if y is algebraic, which happens exactly when e^γ is algebraic. If γ is algebraic and nonzero, e^γ is transcendental by **Hermite–Lindemann**, the single-exponential case. Done: no linear-independence statement about many exponentials is needed.
- (iii) To fool the histogram you must swap bonds between ratio classes while keeping a valid tree. The order-13 pair (l. 603–614, 1057–1060) does exactly this: T1 has (1,2) + (2,6) + (3,3) where T2 has (3,6) + (1,3) + (2,2), one swap in each of the classes q = 1/3, 1/2 and 0. The five (1,6) bonds are shared padding, needed only because both swaps involve a degree-6 vertex (ratios 1:2 and 1:3 at once force a degree that is a multiple of both, the smallest being 6). For Δ ≤ 4 only the 1:2 class and the equal-degree class exist. The swap is then (1,2)² + (4,4)³ ↔ (2,2)³ + (2,4)², which needs degree-4 hubs and costs 16 vertices.

**Where my explanation got stuck, or found something simpler.**
1. **The transcendence step is heavier and narrower than necessary.** [VERIFIED by the argument above; the counterexample at l. 704–705, γ = ln 4 with e^γ = 4, is consistent with it.] The natural condition is "e^γ transcendental", not "γ algebraic". The simple argument gives a stronger global statement: *over all graphs at once, histogram collisions on the pure-γ line can occur only at the countably many γ for which e^γ is algebraic.* The paper states only the weaker "for any finite set, all but finitely many γ" (l. 557–558), and it covers γ = π only through the real-γ clause. Proposition offplane (l. 672–695) simplifies in the same way, because algebraic coefficients still give an algebraic-coefficient polynomial in y. Invoking Lindemann–Weierstrass is not wrong, but it hides the one-line mechanism. [JUDGEMENT] A referee who knows Rada 2019 will notice.
2. **Why 13 and why 16 is never explained.** Minimality is presented only as the output of exhaustive enumeration (l. 542–544, 632, 708–717; Limitations (i), l. 1807–1811). The mechanism above, which needs a degree-6 vertex for three simultaneous ratio-class swaps or Δ = 4 hubs for the 1:2 class, is a short heuristic that would let a reader believe the numbers without running code. It might even lead to a human proof of the Δ ≤ 4 case, where only two nontrivial classes exist. The paper names the classes (l. 632) but never draws this connection.
3. **"Resolution limit" in the title promises more than it delivers.** [JUDGEMENT] The limit that any function of the degree ratio sees only the ratio histogram is, as the paper concedes, Rada 2019 Prop. 2.5 (l. 650, 1871). Part (ii) is Rada 2019 Thm 3.4 applied as stated (l. 632). What is new is two numbers, 13 and 16, together with explicit witnesses (l. 650, "what is new are the explicit witnesses and the orders at which they first occur"). That admission sits in a Remark at l. 650. The contribution list (l. 298–304), the abstract (l. 201–207) and the title present it as a theorem.
4. **The parent attains the same separation** (l. 655–659). At γ = 0, varying α on Π separates histograms at all but finitely many α. So "pure-γ points attain the maximum on Π" is not something γ provides; the paper says "The limit thus belongs to the dependence on the degree ratio, not to γ" (l. 657–658). That sentence is the most honest summary of the section and should come first, not in the middle of a Remark.

[VERIFIED] I rechecked the order-13 and order-16 witnesses by hand from their verbal descriptions (l. 607–629). The vertex counts are 13 and 16, the edge counts are 12 and 15, and the profiles and q-histograms match the paper exactly, {0¹, (1/5)², (1/3)¹, (1/2)³, (5/7)⁵} and {0³, (1/3)⁴, (3/5)⁸}. The pendant-path increment −(1,d) + (2,d) + (L−1)(2,2) + (1,2) (l. 600) is correct.

**New or repackaging?** Mostly repackaging plus a computational fact. A skeptic would say: "Prop. 2.5 + Thm 3.4 of Rada 2019, plus a nauty run."

**Severity.** Major, for framing and for the missing mechanism. No blocker: the mathematics is correct.

**Suggested fix.** (a) Replace the Lindemann–Weierstrass paragraph with the integer-polynomial-in-e^{γ/L} argument and state the condition as "e^γ transcendental, e.g. any algebraic γ ≠ 0". (b) Add a three-sentence "why 13 / why 16" paragraph built on the ratio-class swaps and the degree-6 requirement. (c) Move "the limit belongs to the degree ratio, not to γ" into the theorem preamble and the abstract.

---

### 2.5 Proposition offplane: "parent distinctions survive" (l. 670–706)

**What is claimed.** At rational α, β and algebraic γ ≠ 0, LO separates every pair the parent separates, and it separates more pairs whenever some per-class sum c_q is nonzero.

**Simplest explanation.** The same polynomial-in-y argument with algebraic coefficients.

**Gap.** "Never destroys a distinction" (l. 682) is true at algebraic γ. But in practice one tunes γ over the reals, and at a fitted real γ the guarantee is "all but countably many". This is harmless but unstated in the Conclusion (l. 1876–1877).

**New?** It is a direct adaptation of Rada's argument.

**Severity.** Minor.

**Fix.** One clause: "(for real γ, at all but countably many values)".

---

### 2.6 Proposition laguerre: at most five order exchanges (l. 727–781)

**What is claimed.** Along γ, LO(G) − LO(H) has at most V ≤ r − 1 real zeros. For Δ ≤ 4 the q-values are {0, 1/7, 1/5, 1/3, 1/2, 3/5}, so the bound is 5. The bound is attained with Δ = 6; whether it is attained for Δ ≤ 4 is open.

**Simplest correct explanation.** Substitute x = e^γ. The difference becomes `Σ c_k x^{q_k}`, a "polynomial with fractional exponents". Descartes' rule of signs (Laguerre's version) says the number of positive roots is at most the number of sign changes in the coefficients. Six distinct exponents allow at most five sign changes.

**Where it got stuck.**
- "Exchange order" means a sign change of D. The proposition counts zeros *with multiplicity*. A tangential zero is a touch, not an exchange, so "exchange order at most five times" is correct but not identical to the statement proved. This is fine, but a student will ask.
- [VERIFIED] The Δ = 6 sharpness example (l. 764–771) checks out. With mpmath at 50 digits I find exactly five crossings, at γ ≈ −17.17, −11.96, −2.03, 2.73 and 31.13, matching the paper. All five lie at |γ| ≫ 2, outside the range used in any fit (γ ∈ (−2, 2), l. 1720), and three of them lie outside [−3, 3]. The chemical meaning of "five crossings" is therefore nil, and the paper does not say so.
- The bound uses only r, the number of distinct q values, and none of the tree structure. [JUDGEMENT] An exhaustive check over chemical trees up to order 16, which the authors already enumerate, would settle the open question (l. 776, 1812–1814) empirically within that range. Its absence is odd given the infrastructure.

**New?** An immediate corollary of a 19th-century rule. A skeptic would ask: "Why is this a Proposition and not a remark?"

**Severity.** Minor.

**Fix.** Call it a corollary of Descartes–Laguerre. Add "all crossings of the witness lie at |γ| > 2, outside the range used in Section 6". Report the maximum number of sign changes found among enumerated chemical trees.

---

### 2.7 Proposition identrank and Remark Δ = 7 (l. 783–859)

**What is claimed.** The rank of the Hessian equals the affine dimension A(G) of the realised z-points. Directions in the null space only rescale the index. For the octane data set A = 3, so the octane fits have no exact confounding.

**Simplest explanation.** If all of a graph's bond types lie on a plane in z-space, moving the parameters perpendicular to that plane multiplies every term by the same factor.

**Gap.** The useful chemical statement, "the octane union spans dimension 3, so γ is not exactly confounded" (l. 850–858), is again binary. As in 2.2, near-confounding is what matters for estimation, and the paper reports no condition number.

**New?** Standard exponential-family minimality (Brown 1986). The Δ = 7 exception is a curiosity.

**Severity.** Minor. Remark l. 827–841 could go to the supplement.

**Fix.** Report the smallest eigenvalue, or the condition number, of the Hessian at the fitted θ on the octanes.

---

### 2.8 Degeneracy floor 25.5% at order 10 (l. 1036–1125; Suppl. l. 685–720)

**What is claimed.** On the 106 trees of order 10, LO(0,0,1) and LO(0,0,2) have 79 distinct values, a degeneracy of 25.5%, equal to the floor because there are exactly 79 profiles. They tie with R, GA and AG, while M1 is at 83.0% and M2 at 67.0%.

**Simplest explanation.** [VERIFIED arithmetic] 100(1 − 79/106) = 25.47%. The 25.5% is a property of *the set of trees* (106 trees, 79 profiles), not of any index. Every index that separates all 79 profiles scores 25.5%, and Prop. generic (l. 945–972) shows that almost every θ does so.

**Where it got stuck.**
- **The number's meaning is unclear in the main text.** Under the paper's convention (excess structures over distinct values), 25.5% does *not* mean "25.5% of trees are confused". The supplement (Suppl. l. 694–699) states that 45 of the 106 trees (42.5%) share a value with another tree, but the main text never says this. A chemist will read 25.5% as the fraction of confusable molecules.
- "Attains the floor ... tied with R, GA and AG" (l. 1044–1046) reads like a merit. It is the generic behaviour. Only *leaving* the floor (M1, M2, χ) is informative. The supplement says this plainly (Suppl. l. 713–714, "does not distinguish ... from R"), but the main text and the Figure 1 caption are softer.

**New?** The counts are new numbers; the concept is not.

**Severity.** Major as a source of misunderstanding (see §3).

**Fix.** In the main text, state once: "25.5% is the profile floor; it means 79 classes among 106 trees, and 42.5% of trees share a value with another; any generic parameter point attains it."

---

### 2.9 Structure sensitivity (l. 1127–1188)

**What is claimed.** LO(0,0,2) has SS close to that of hyper-Zagreb and a lower Abr. Its SS/Abr ratio is about 0.458.

**Simplest explanation.** SS is the average *relative* change of the index under a one-edge move. [VERIFIED algebra] LO(0,0,γ) = m + (γ/2)·IRLA + O(γ²) (l. 1155–1156), and m = 9 is the same for every decane. The relative change is therefore roughly (γ/2)·ΔIRLA/m, which grows linearly in γ. The reported SS values 0.031, 0.062 and 0.126 at γ = 0.5, 1 and 2 (l. 1152–1153) are almost exactly proportional to γ.

**Gap.** The paper concedes that the match at γ = 2 "reflects the chosen value of γ" (l. 1159–1160), but it never says *why*: a relative-change measure depends on any constant offset, and the pure-γ index carries an offset of m. Under this reading, SS for pure-γ points is set by γ and is not a property of the structure.

**New?** No.

**Severity.** Minor.

**Fix.** One sentence: "SS is a relative-change measure; since LO(0,0,γ) ≈ m + (γ/2)·IRLA with m fixed within an isomer class, its SS scales roughly linearly with γ, so only the SS/Abr ratio is comparable across indices."

---

### 2.10 Closed forms, extremal trees and termwise bounds (l. 1190–1517)

**What is claimed.** Closed forms on K_n, C_n, P_n, S_n, K_{a,b}, Q_k, W_n and F_p. Among trees, the path minimises LO(·;0,0,γ) and the star maximises it (γ > 0). There are also bracket, (m, Δ), (m, δ), ratio and Cauchy–Schwarz bounds.

**Simplest explanation.** Each bond contributes e^{γq} ≥ 1, every leaf bond has q ≥ 1/3, a tree has at least two leaves, and the path has exactly two leaf bonds and all other bonds balanced. This gives the minimum. The star has every bond at the largest possible q = (n−2)/n, which gives the maximum. The bounds are "each term lies between its smallest and largest possible value, so sum".

**Gap.** None in correctness. [VERIFIED] I traced the proof at l. 1275–1289 line by line and it is complete. [JUDGEMENT] As the paper acknowledges (l. 1291), the extremal result follows from Cruz–Rada 2019 and from Gao–Gao 2024. The lower bound in Prop. lower_delta (l. 1432–1457) ignores γ entirely, since e^{γq} ≥ 1, so it is the γ = 0 bound restated. Readers may assume "machine-checked" (l. 1309–1313) adds weight here. It verifies the easy summation step, with the per-edge extrema taken as hypotheses (LEAN_VERIFICATION.md, rows for Props 11 and 14).

**New?** No. A skeptic would say: "Two pages of bookkeeping."

**Severity.** Minor (length).

**Fix.** Compress §5 to the closed forms and the extremal statement, and move the bounds to the supplement.

---

### 2.11 QSPR: octane correlations (l. 1519–1602)

**What is claimed.** Descriptive correlations with 18 octanes. LO(0,0,1) is best on ΔH_vap, with |r| = 0.984. Two collision pairs give an in-sample floor of 2.925 °C², an RMS of 0.403 °C.

**Simplest explanation.** [VERIFIED] The ΔH_vap of octane isomers drops as the molecule branches. Using the repository's own `octane_data.py`:

| Descriptor | r(ΔH_vap) | LOO Q² |
|---|---|---|
| Number of methyl groups (leaves) | −0.923 | 0.818 |
| Σ q (IRLA/2) | −0.980 | 0.948 |
| LO(0,0,1) | −0.984 | 0.957 |

LO(0,0,1) is, to first order, IRLA, a published parameter-free irregularity index. The Réti–Sharafdini et al. MATCH 2018 paper, cited at l. 276 only for the definition, already reports that irregularity indices predict octane properties other than T_B well (from its abstract; I did not check the per-index tables). [JUDGEMENT] The ΔH_vap "winner" is therefore a known branching effect in new clothing, and the paper never says so.

**Where it got stuck.**
- **What does the 0.403 °C floor mean?** [VERIFIED] The octane T_B standard deviation is 6.12 °C over a range of 99.2–125.6 °C. The collision floor caps in-sample R² at about 1 − 2.925/(17 · 6.12²) ≈ 0.995, while the actual nested Q² values are about 0.6–0.8. So the "nonzero irreducible in-sample error" (l. 909–910) is real but about 0.5% of the variance. It is not what limits these descriptors, and the paper never puts the floor next to the variance.
- [VERIFIED] The paper admits that the octane correlations were computed before the "fixed" γ = 1, 2 were documented (l. 1530–1532). Bold winners chosen from 12 correlated indices on 18 molecules (l. 1596–1597) are optimistic.

**Severity.** Major, for the missing IRLA / branching attribution. Minor for the rest, since the text is suitably hedged.

**Fix.** (a) Report the leaves-only and IRLA baselines in Table 3. (b) Say explicitly: "the pure-γ point's ΔH_vap performance is that of the published IRLA [RetiSharafdini2018IRLA]". (c) Give the collision floor as a fraction of property variance.

---

### 2.12 QSPR: matched-budget ablation, nonanes and preregistered boiling points (l. 1604–1798, Table 5 l. 1826–1860)

**What is claimed.**
- In box (−2, 2), freeing γ "improved" nested Q² for ΔH_vap, by about +0.07 on the octanes and +0.05 on the nonanes, "replicates" in the preregistered seed-count sense.
- In a wide box (half-width 12, chosen post hoc) the gain is about 0 (+0.004 and −0.002).
- The two preregistered boiling-point tests are negative: decanes ΔQ² = −0.072 with interval [−0.156, +0.001]; pooled C6–C10 −0.0001 with [−0.003, +0.002].
- Ridge regression on the counts reaches Q² = 0.860 on the decanes, against 0.149–0.514 for single indices.

**Simplest correct explanation.**
- LO contains GM (γ = 0), so with a perfect optimiser LO can never be worse in-sample.
- The narrow-box "gain" happened because the parent wanted to travel along the ratio plane to large α. [VERIFIED] The paper's own selected point M_{4.5,−9} has β = −2α exactly (l. 1653), which weights bonds by (1 − q²)^{4.5}, a decreasing function of imbalance, in other words an IRLA-like branching penalty. The box stopped the parent at about (1, −2) (l. 1623–1624). γ gave LO a shortcut to the same imbalance signal.
- Remove the box and both models reach the same place. The γ "effect" was a box artifact plus the near-collinearity of q and ln(1 − q²) (§2.2).
- On boiling points, no single scalar index can do well, because it compresses about 7 free count directions into one number. Ridge keeps them all, and Wiener's W (distance information) adds more (l. 1795, Q² = 0.904).

**Where it got stuck.**
1. **The design answers a different question from the one a reader asks.** "Does γ help?" is a question about model capacity. Random search with equal candidate counts in 2-D and 3-D mixes capacity with optimiser efficiency, and the paper concedes this twice (l. 1654–1656, 1780–1782). Seed counts measure optimiser variance on fixed data (l. 1673–1676, 1680–1683, 1764–1765). The intervals are "conditional on the fitted predictions" and omit selection (l. 1737, 1768–1770). The only selection-aware analysis is exploratory, and on the decanes it is uninformative: range [−0.510, +0.312] (l. 1774–1780). [JUDGEMENT] After all the caveats, the honest conclusion is "the experiment could not detect an effect of plausible size", which is weaker than "no demonstrated gain" sounds.
2. **"Preregistered" needs a definition.** [VERIFIED] The protocols are files committed to the authors' own repository (`external/PREREG_v37.md`, commit 964b127, dated 2026-10-03; `external/PREREG_v40.md`, commit a5cf378, dated 2026-10-05). Git dates are set by the author. Whether GitHub's server-side push record corroborates them is not stated in the paper, and no OSF or registry ID is given. The wide box used in the "preregistered" boiling-point tests had been chosen post hoc on the ΔH_vap curves (l. 1634–1636). That is disclosed, but a reader assumes "preregistered" means the design was fixed before outcome data of any kind were seen.
3. **Jargon density.** "Candidate stream", "hybrid control LO_h", "Edge", "seed-count criterion", "replicates (the protocol's name for ...)", "registered secondary question" and "deletion-rank guard" (l. 1638–1683, Table 5) are defined in passing or not at all. A chemist cannot follow §6.2–6.4 without the supplement.
4. **The ridge result is the real finding and is under-sold.** It is relegated to l. 316–318 and l. 1786–1797. The permutation p ≈ 0.005 (l. 1795) is the only properly selection-aware inference in the paper, and it concerns ridge, not γ.

**New?** [JUDGEMENT] The negative result is useful and honestly reported. Its lesson ("don't add a parameter to a degree-based index; use the counts") is known in chemometrics, and the paper cites Gutman's survey to that effect (l. 290–292).

**Severity.** Major. The section is correct but over-engineered for its conclusion, and it is easy to misread.

**Suggested fix.** Replace the random-search comparison with a deterministic nested optimisation (multi-start L-BFGS or a dense grid inside each fold) so that LO ⊇ GM holds by construction. Then report a single selection-aware interval for ΔQ². State the minimal detectable effect. Move the seed-count machinery to the supplement. Put the paragraph "q vs ln(1 − q²) are 0.95-correlated in the chemical range, so a large γ effect was not expected" at the start of §6.

---

### 2.13 Lean formalisation scope (l. 1309–1313, 1899–1906; `LEAN_VERIFICATION.md`)

**What is claimed.** Lean 4 / Mathlib checks the termwise inequalities (not their equality cases), log-sum-exp convexity, the spanning statement of Lemma 1, and the order-13 collision on the pure-γ line.

**Simplest explanation.** [VERIFIED from LEAN_VERIFICATION.md] Graphs enter Lean as multisets of degree pairs, not as graphs. The checked items are (a) Σ of per-edge inequalities, with the per-edge extrema as *hypotheses* for the bracket and ratio bounds, (b) a 4×4 determinant, (c) the arithmetic identity showing that two given multisets have equal q-sums, and (d) convexity of log-sum-exp. Treeness of the order-13 realisations is "the standard fact, not re-proved". Lindemann–Weierstrass, Laguerre, the enumeration-based minimality and the real-analytic zero sets are not formalised.

**Gap.** [JUDGEMENT] The formalised parts are the ones nobody would doubt. The parts a referee would actually want checked, minimality at 13 and 16 and the transcendence step, are not formalised. The paper's wording is accurate (l. 1899–1903), but "machine-checked" in §5 (l. 1309–1310) may suggest more than this.

**Severity.** Clarity.

**Fix.** Add one sentence: "The Lean development certifies routine algebra; the novel minimality claim is certified only by the enumeration script."

---

## 3. Five places a reader is most likely to misunderstand

1. **"Degeneracy 25.5%"** (l. 1043–1047). *Misread as:* a quarter of the trees are confused, and pure-γ is especially good. *Clarification:* "25.5% means 79 distinct values for 106 trees, the floor that almost every parameter point reaches; 42.5% of the trees share their value with another tree."
2. **"Separate exactly the q-histograms at algebraic γ ≠ 0"** (l. 202–203, 555–558). *Misread as:* algebraicity of γ matters chemically, or γ = 1 is special. *Clarification:* "The index is an integer polynomial in e^{γ/L}, so it separates histograms whenever e^γ is transcendental, which includes every algebraic γ ≠ 0 and almost every real γ."
3. **"γ can separate graphs that the parent merges"** (l. 259, 1108–1125). *Misread as:* γ adds structural information. *Clarification:* "γ never adds information beyond the bond-type counts; it only repairs coincidences of particular rational parent exponents, which generic parent exponents never suffer (Prop. generic)."
4. **"Replicates" and "preregistered"** (l. 1660–1676, 1701–1723). *Misread as:* an independently confirmed effect under a registry-backed protocol. *Clarification:* "'Replicates' is the name of a seed-count rule that measures optimiser variance, the interval included zero, and the protocols are time-stamped commits in the authors' own repository."
5. **"LO is the partition function of an exponential family"** (l. 282–283). *Misread (by chemists) as:* LO has thermodynamic meaning, which would make the ΔH_vap and S correlations look principled. *Clarification:* "'Partition function' is used in the formal statistical sense of a normaliser; LO has no thermodynamic interpretation."

Runner-up: "Every vertex-degree-based descriptor carries a nonzero irreducible error" (l. 909–910) sounds like a strong limitation, but the floor is RMS 0.40 °C against a property SD of 6.1 °C.

---

## 4. Jargon and notation to define earlier or simplify

| Term | Where | Issue | Proposal |
|---|---|---|---|
| BID / vertex-degree-based / degree-pair profile / count vector / edge-type vector / M-polynomial | l. 226, 285, 337, 599, 895, 917 | Six names, one object, no formal definition of "VDB index" | Define once in §2 and use "profile m" thereafter |
| q_uv, imb(x,y), q_ij, ρ_uv, ratio | l. 254, 354–355, 636 | Four notations for one quantity | Keep q; give ρ = (1−q)/(1+q) once |
| Π, κ = 2α+β, "pure-γ points", "ratio plane" | l. 525–535 | κ is introduced and then barely used | State in words: "Π = indices that depend only on degree ratios" |
| z_uv, augmented feature vector, A(G), R(G), r(G) | l. 379–387, 783–787 | Heavy apparatus for a rank statement | Move Prop. identrank and Remark Δ = 7 to the supplement |
| "floor", "ceiling" | l. 895–897 | The same quantity is called both | Choose one ("profile bound") |
| Degeneracy convention 100(1−k/N) | l. 1041 (defined only in Suppl. l. 690–699) | Non-obvious; differs from "share confused" | Define in the main text with the 42.5% companion number |
| Laguerre / generalised polynomial | l. 727–746 | Fine for mathematicians | Say "Descartes' rule of signs" first |
| Nested Q², candidate stream, Edge, LO_h, hybrid control, seed-count criterion, budget, half-width | l. 1607–1683, Table 5 | Undefined or defined in passing | Add a 6-line glossary box at the start of §6 |
| Lindemann–Weierstrass | l. 588–594 | Overkill (see 2.4) | Hermite–Lindemann plus the polynomial argument |
| "Partition function", "exponential family", "minimal representation" | l. 283, 811–813 | Decorative | Drop or footnote |

---

## 5. Is the chemistry connection convincing to a chemist?

[JUDGEMENT] No, and the paper partly concedes this.

- **No physical rationale for e^{γq}.** The paper says that positive γ "upweights degree-imbalanced edges" (l. 257). It never says what an imbalanced edge *is* chemically: a CH₃–C(quaternary) bond has q = 3/5, a CH₃–CH₂ bond has q = 1/3. It never says why the exponential, rather than linear or quadratic, should track any property. The data then show that linear is enough (IRLA, l. 1155–1159, 1689–1695) and that the quadratic-like parent does as well in a wide box.
- **The ΔH_vap story has a known chemical explanation that is never stated.** Branched alkanes are more compact, have less surface contact and weaker dispersion forces, and therefore lower ΔH_vap and T_B. [VERIFIED] The number of methyl groups alone gives r = −0.92 with octane ΔH_vap, and Σq gives −0.98. A chemist would want to read "LO(0,0,γ) is a smooth branching count" and the comparison to a methyl count.
- **The collision pairs are the most chemically instructive item, and they are under-used.** 3- vs 4-methylheptane, and 3,4-dimethylhexane vs 3-ethyl-2-methylpentane (Table 1, l. 1009–1034), differ only in *where* a branch sits. No degree-based index can see that, but distance-based ones can (W, l. 1795). That is the chemical take-home, and it appears only implicitly.
- **Scope.** All data are acyclic alkanes (l. 1797–1798, 1815–1816). With no heteroatoms, rings or unsaturation, the chemical audience of MATCH is served only as a methods caveat.
- **Data quality is handled carefully.** The 2,2,3,3-tetramethylbutane ΔH_vap reference-state problem is disclosed (l. 1546–1556) and NIST provenance is audited. This is a strength.

**Verdict on this point.** The chemistry is used as a test bed, not explained. That is acceptable for a negative methods result only if the paper says plainly that the predictive signal is a known branching effect.

---

## 6. Candid verdict: what the paper really teaches

[JUDGEMENT]

The paper is careful, honest and heavily hedged, and its mathematics is correct as far as I could check. I verified by hand or by recomputation:
- the order-13 and order-16 witnesses;
- the Lemma 1 determinants and the Δ = 2 identity;
- the five crossings of the Δ = 6 example;
- Example sumconn, with D(1) ≈ 0.2255 and D(10⁻⁶) ≈ 2.4 × 10⁻⁷;
- the collision floor of 2.925 °C² and RMS 0.403 °C;
- the K₄ / K₁,₃ collision at γ = ln 4;
- 25.5% = 100(1 − 79/106).

Once each claim is explained from first principles, though, most of them turn out to be either classical (log-sum-exp convexity, Descartes' rule, termwise bounds, path/star extremality via Cruz–Rada, Rada's degree-ratio observation and Lindemann argument) or simpler than presented. The transcendence step reduces to "an integer polynomial in e^{γ/L} has only algebraic roots".

The genuinely new mathematics is small. It consists of the orders 13 and 16 at which q-histograms first fail to determine tree profiles, with explicit witnesses; and the mechanism behind those numbers (ratio-class swaps needing a degree-6 vertex, or Δ = 4 hubs) is left unstated. The γ coordinate adds a functional direction that is real but nearly collinear with what the parent already reaches through (1 − q²)^α (R² ≈ 0.89 on the chemical pairs). The empirical sections confirm this. The narrow-box ΔH_vap gain came from truncating the parent, the boiling-point tests were null, the best "Loyola" point is essentially the published IRLA branching index, and ridge regression on the raw counts beats every single index.

What the paper really teaches is: **a ratio-only weighting of bonds is blind to swaps between equal-ratio bond types, which first become possible at 13 vertices (16 for alkanes), and adding an exponential imbalance parameter to the Gutman–Milovanović family neither adds information nor, on alkane data, demonstrably adds predictive power.** That is a legitimate, modest, negative-result paper. It would be stronger at half the length, framed around that sentence, with the q-vs-q² near-collinearity stated up front as the a-priori reason for the null.

---

## Five most important gaps (summary)

1. **Lemma 1 is binary; the near-collinearity that predicts the QSPR null is never quantified** (l. 389–437, 297, 1624–1627). Fix: report R² ≈ 0.89 (q on the parent coordinates over the chemical pairs) and corr(q, ln(1−q²)) ≈ 0.95, and open §6 with this.
2. **The transcendence step hides a one-line mechanism and states a narrower condition** (l. 555–558, 585–597, 672–695). Fix: argue via the integer polynomial in e^{γ/L}. The condition is "e^γ transcendental", and collisions over all graphs are confined to a countable set of γ.
3. **"Why 13 / why 16" is computational only** (l. 542–544, 632, 708–717, 1807–1811). Fix: add the ratio-class-swap explanation (a degree-6 vertex is needed for the 1:2 + 1:3 swap; Δ ≤ 4 allows only the 1:2 swap with degree-4 hubs) and attempt a human proof for Δ ≤ 4.
4. **The 25.5% degeneracy and "attains the floor" read as merits** (l. 1043–1052, Fig. 1 caption l. 1068). Fix: say in the main text that it is generic (Prop. generic) and give the 42.5% share of trees that collide.
5. **The predictive design conflates optimiser efficiency with model capacity, and "preregistered" / "replicates" overstate** (l. 1607–1683, 1701–1798; the protocols are self-hosted git commits 964b127 and a5cf378). The ΔH_vap winner is the published IRLA branching effect (l. 1155–1159, 1689–1695). Fix: use deterministic nested optimisation with a selection-aware interval, state the minimal detectable effect, define "preregistered", and credit IRLA / Réti et al. together with the methyl-count baseline (r = −0.92).

Web lookup used: search result for Réti, Sharafdini, Drégelyi-Kiss and Haghbin, "Graph irregularity indices used as molecular descriptors in QSPR studies" (PGU research page, https://research.pgu.ac.ir/_Pages/ResearchEN.aspx?ID=2434). Only the abstract was seen.


---
## Integration note (2026-10-20)

Applied: the main text now states that the 25.5% degeneracy is not the share of trees confused (45 of 106 trees, 42.5%, for LO(0,0,1)), with registered numbers; the Figure 1 caption explains the darker bars. Not applied (AUTHOR DECISION; would add analyses or restructure arguments): quantifying the q / (1-q^2) near-collinearity, replacing the Lindemann-Weierstrass paragraph by the e^gamma-transcendental argument, a structural explanation of orders 13 and 16, redesigned search protocol, IRLA / methyl-count baseline.
