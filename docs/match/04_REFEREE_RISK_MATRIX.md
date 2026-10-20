# Referee risk matrix: simulated MATCH panel

- **Manuscript:** "The Loyola Index Family and the Resolution Limit of Degree Imbalance". The source is `main.tex` (2149 lines, compiled to 44 A5 pages as `LOYOLA_paper.pdf`) and `supplement.tex` (27 A5 pages).
- **Worktree:** `wt-fig`, branch `review/match-figure-2026-10-20`, commit **325bd05**.
- **Date:** 2026-10-20.
- **Line numbers** refer to `main.tex` at 325bd05.

> **These are SIMULATED referee perspectives, not real reviewers.** They do not predict what the MATCH editor or actual referees will say. There are four perspectives:
> - (G) mathematical graph theory;
> - (C) mathematical chemistry;
> - (R) computational reproducibility;
> - (S) statistical/QSPR methodology.
>
> The review was read-only on the repository. No file there was edited and no expensive computation was rerun. The light checks were:
> - re-deriving the witness trees, closed forms and several identities by hand;
> - counting the Lean declarations;
> - reading committed outputs;
> - two web searches.
>
> No novelty claim below rests on search results being absent.

Classification used throughout:
- **VERIFIED FACT:** checked directly against the source, a committed output or a hand calculation.
- **PLAUSIBLE REFEREE CONCERN:** a judgement a competent referee could reasonably make.
- **EDITORIAL PREFERENCE:** style or emphasis only.
- **AUTHOR DECISION:** the authors must choose. It is not a defect.

Severity levels: blocker, major, minor, editorial.

---

## 0. Top risks in priority order

| # | Risk | Perspective | Severity | Class |
|---|---|---|---|---|
| 1 | The mathematical novelty is thin relative to the paper's size. The separation theorem is Rada 2019 Thm 3.4 / Prop 2.5 specialised. γ adds no generic discrimination. The new content is an enumeration result: minimal orders 13 and 16, explicit witnesses, the Δ = 6 five-crossing example and the Δ = 7 exception. | G, C | major | PLAUSIBLE REFEREE CONCERN |
| 2 | Length and balance. The paper is 44 + 27 pages. Section 6 and Table 6 carry audit-trail detail (solver rescaling, rank guards) that is unusual for MATCH. The QSPR result is negative. | C, S | major (editorial) | PLAUSIBLE REFEREE CONCERN |
| 3 | The minimality of 13 and 16 is computer-assisted only. There is no structural explanation and no certificate (list of colliding classes) in the paper. | G | major-to-minor | PLAUSIBLE REFEREE CONCERN |
| 4 | The search protocol may handicap γ: random search with equal budgets in 2D and 3D. The strict-cohort γ intervals lie entirely below zero and the supplement does not report them. The negative verdict is protocol-specific. | S | major (if raised) | VERIFIED FACT (unreported intervals) + PLAUSIBLE CONCERN |
| 5 | Wording on the most-read surfaces. The abstract calls the vaporisation-enthalpy gain "exploratory" although it met a pre-registered criterion. Discussion (iv) says "reverses". Section 4.3 says "shows" about a third-decimal difference. | S | minor | VERIFIED FACT |
| 6 | Data provenance. 7 octane entropies, the compiled ω values and the TMB ΔH_vap are unresolved. 29/34 nonane ΔH_vap values are compiled. 58/100 boiling points derive from NIST averages that bypass the 3 K screen, and the main text does not say so. The strict cohort is only 42 molecules (C9–C10). | C, S | minor-to-major | VERIFIED FACT |
| 7 | Immutable version. `\cite{LoyolaRepo}` gives no commit, tag or DOI. The repository default branch `main` holds an older package. NIST raw pages remain in history. | R | major for a reproducibility referee | VERIFIED FACT |
| 8 | The title attaches the "resolution limit" to degree imbalance. The paper's own Remark (lines 655–659) says the limit belongs to the degree ratio, not to γ. | G | editorial | AUTHOR DECISION |

---

## 1. Main contribution and novelty (perspectives G and C)

### 1.1 What the paper actually claims (VERIFIED FACT, read from the source)

| Item | Exact statement and hypotheses | Lines | Proof status |
|---|---|---|---|
| Lemma 1 (affine independence) | For Δ ≥ 3 the vectors (1, ln ij, ln(i+j), q_ij) span ℝ⁴. The statement fails for Δ ≤ 2, with an explicit formula for Δ = 2. | 389–437 | Proved; I re-derived 3⁸ ≠ 2¹³. The determinant and the Δ = 2 formula check. |
| Theorem 1 (log-convexity) | Covers m ≥ 1, the gradient and Hessian, and the strictness criterion. | 456–511 | Proved; textbook log-sum-exp. |
| Theorem 2(i) | On Π = {β = −2α} the value depends only on n_q, and differs for different histograms off a null set. | 549–554, 571–584 | Proved via the factorisation in Eq. 7 and the real-analytic null-set result (Mityagin). |
| Theorem 2(ii) | For every **nonzero algebraic γ** (negative included), equality holds iff the histograms are equal. On a finite set of graphs it holds for all but finitely many real γ. | 555–558, 585–597 | Proved by Lindemann–Weierstrass; credited to Rada 2019 Thm 3.4 at line 632. |
| Theorem 2(iii) | Trees with distinct profiles and equal histograms, each with a leaf next to a vertex of the same degree d ≥ 2, propagate by a pendant path. Pairs exist at every n ≥ 13, and at every n ≥ 16 when Δ ≤ 4. | 559–568, 597–630 | Existence is proved. **Minimality is by enumeration only** (lines 541–544, 632, 708–713). |
| Proposition 3 (off-plane) | With **α, β ∈ ℚ** and **algebraic γ ≠ 0**, a parent distinction is never destroyed. | 672–695 | Proved. The counterexample at transcendental γ = ln 4 (K₄ vs K₁,₃) holds: 6 = 3e^{ln4/2}. |
| Proposition 4 (Laguerre) | D has at most V ≤ r − 1 real zeros, with parity. For Δ ≤ 4 there are 6 imbalances, so at most 5 exchanges for every fixed (α, β). | 727–761 | Classical tool (Jameson 2006). The six imbalances {0, 1/7, 1/5, 1/3, 1/2, 3/5} check. |
| Five-crossing remark | Attained by order-12 trees with Δ = 6. Whether it is attained for Δ ≤ 4 is **open**. | 763–781 | Certified numerically (interval arithmetic in a prior audit). Edge counts (11 each) and the 8 distinct imbalances check. |
| Prop 7 (ceiling) and the error floor | Equal profiles give equal values of every VDB index. The octane SSE floor is 2.925 °C², stated for a fixed function only (lines 926–928). | 899–928 | Elementary (M-polynomial; Deutsch–Klavžar is cited). SSE = 18/25 + 441/200 = 117/40 checks. |
| Prop 8 (generic) | Almost every θ separates distinct profiles. Stated as **inherited from the parent** (lines 976–985). | 945–985 | Elementary. |
| Prop 10 (extremal) | For n ≥ 4 and γ > 0, P_n is the unique minimiser and S_n the unique maximiser. γ < 0 swaps them. Credited to Cruz–Rada 2019 and Gao–Gao 2024. | 1265–1296 | Proved. The (x−1)(3x²+x+1) step checks. |
| Lean scope | Covers the termwise inequalities (Prop 12, Prop 13, Cauchy–Schwarz corollary), only the summation step for Props 11 and 14, log-sum-exp convexity, the spanning in Lemma 1, and the order-13 collision on the pure-γ line. Transcendence, Laguerre and enumeration are **not** formalised. | 1306–1313, 1899–1906 | VERIFIED: `formal/` holds 37 `theorem` + 15 `lemma` = **52** declarations. `expected_axiom_theorems.txt` lists **38** (37 theorems + `K13_degrees_in_range`). `verify.sh` checks both sets. |
| Exact tie certification | Table 2 counts are certified exactly. Pure-γ counts come from the q-histograms (Thm 2(ii)). R and GA counts, including the GA merge at order 17, come from radicals plus Besicovitch 1940. | 1075–1082, 1120–1121 | VERIFIED by hand: the GA order-17 witness gives 10√5/3 + 4 on both sides. Edge counts are 16 and handshake sums are 17. |

### 1.2 Hand checks of the witnesses (VERIFIED FACT)

| Witness | Checks performed |
|---|---|
| Order-13 trees T₁, T₂ (lines 607–615) | Built from the verbal descriptions. Both have 13 vertices and 12 edges. Their edge lists match the stated profiles, and both give the histogram {0¹, ⅕², ⅓¹, ½³, (5/7)⁵}. |
| Order-16 chemical pair (lines 615–629) | Both have 16 vertices and 15 edges. Both give the histogram {0³, ⅓⁴, (3/5)⁸}. Both have a leaf adjacent to a degree-4 vertex. |
| SDD order-9 pair (lines 662–665) | Both give 58/3. Handshake sums are 9 = n. |
| Example 2 (lines 995–1007) | The D(γ) formula re-derived from the count difference. D(1) ≈ 0.2255. D′(0) ≈ 0.240 gives D(10⁻⁶) ≈ 2.4 × 10⁻⁷. |
| Proposition 9 | All nine closed forms re-derived, including the W_n spoke imbalance (n−4)/(n+2) and the F_p imbalance (p−1)/(p+1). |
| Diminished Sombor index | It equals √(d_u² + d_v²)/(d_u + d_v) = √((1+q²)/2), a ratio function. This supports its inclusion in the Corollary (lines 640, 271–272). Definition checked against arXiv:2508.06532. |

### 1.3 Concerns

**N1. The separation theorem is a specialisation of known results** (Thm 2(ii); lines 202–204, 298–304, 632, 650, 1866–1871)
- **Prior art:**
  - Rada 2019, *MATCH* 82, Thm 3.4 (Lindemann–Weierstrass on classes of equal edge weight) and Prop 2.5 (indices whose weight depends on a class function).
  - Rada 2026, *MATCH* 96, for the linear framework and the pendant-path device.
  - The paper credits all of these (lines 201, 299–301, 599, 632, 650, 1869–1871). Attribution is honest.
- **Severity:** major for significance, none for correctness. Class: PLAUSIBLE REFEREE CONCERN.
- **Expected referee reading:**
  - "Thm 2(i) is the identity 4ij/(i+j)² = 1 − q²."
  - "Thm 2(ii) is Rada's theorem with φ = γq."
  - "The Corollary is one line."
  - "Contribution (i) is textbook."
  - "The new content is a computer search."
- **Necessary revision:** none to the mathematics. Lead the abstract and introduction with the combinatorial result: minimal orders 13 and 16 with explicit witnesses, binding GA, AG, SDD, ISDD, the exponential GA/ISDD, diminished Sombor and degree-ratio Sombor at once. Present Thm 2(i)–(ii) as the framing lemma.
- **Verification method:** compare the abstract (lines 196–212) and contributions (lines 295–319) against the novelty classification in `audit/final/FINAL_MATHEMATICAL_REFEREE_REPORT.md` §10.
- **Residual uncertainty:** the exact numbering of Rada 2019 Prop 2.5 and Cruz–Rada Thm 2.1/3.1 was not re-read here. A prior audit read Rada 2019 Thm 3.4 in full.

**N2. Generic discrimination and the ceiling are elementary** (Props 7 and 8; lines 899–985)
- **Prior art:**
  - Deutsch–Klavžar 2015 (M-polynomial) and Rada 2026 for the ceiling.
  - The real-analytic null-set fact for Prop 8.
  - The paper says Prop 8 is "inherited from the parent rather than conferred by γ" (lines 976–985). It calls the ceiling "known" in contribution (iv) (line 308).
- **Severity:** minor. Class: PLAUSIBLE REFEREE CONCERN, already pre-empted.
- **Necessary revision:**
  - Optionally demote Prop 7 to a remark.
  - Drop "irreducible" at line 910. "Nonzero in-sample error" suffices.
- **Verification method:** read lines 908–910 and 923–928 together.
- **Residual uncertainty:** low.

**N3. Linearity in counts and the ten-dimensional space** (lines 285–289, 980–985, 259)
- The paper states plainly that γ "adds no graph information beyond the edge-degree-pair counts" (lines 259, 980–983). Nothing is oversold. Class: VERIFIED FACT, no action needed.

**N4. Minimality of 13 and 16 rests on enumeration** (lines 302–303, 541–544, 632, 708–713; Discussion (i) at lines 1807–1811)
- **Evidence:**
  - The paper states the computer assistance in four places.
  - Profiles and q-histograms are exact rationals.
  - Prior independent audits reproduced the counts: 570/566 at n = 13, and 810/809 at n = 16 for Δ ≤ 4.
  - The text gives no structural reason why 13 is the threshold.
- **Severity:** minor-to-major, depending on the referee. Class: PLAUSIBLE REFEREE CONCERN.
- **Necessary revision:**
  - Give all colliding histogram classes at the first orders in the supplement: 4 classes at n = 13 and 1 class at n = 16 for Δ ≤ 4.
  - Name the enumeration method (non-isomorphic tree generator) and the count check against OEIS A000055/A000602, so a referee can audit it without running code.
  - Optionally add a two-line heuristic for why a collision needs a degree ≥ 5 vertex below n = 16 (both n = 13 witnesses have a degree-6 vertex).
- **Verification method:** check `structural/minimality_check.py` and `structural/exact_ties_out.txt` for the class listing, and check the supplement for S5 content.
- **Residual uncertainty:** whether a MATCH referee accepts a computer-assisted minimality claim without a certificate in the paper. MATCH routinely publishes computer-assisted counts.

**N5. Missing context for minimal-order degeneracy results**
- **Prior art:** precedents for "smallest non-isomorphic trees with equal index" exist and are not cited:
  - Ivanciuc et al. 1993, J. Math. Chem. (smallest degenerate alkane pair, 18 vertices);
  - Guo, Randić et al. 1999 (smallest JJ-equivalent trees, order 18);
  - Randić et al. 2013 (smallest trees with equal Balaban J, n = 12);
  - Dehmer et al. 2012, PLoS ONE.

  All are listed in `audit/final/NOVELTY_SEARCH_LOG.md` (P41, P42, P74, P76). Only Konstantinova 1996 is cited (line 1039).
- **Severity:** minor. Class: PLAUSIBLE REFEREE CONCERN.
- **Necessary revision:** add one sentence and two or three verified citations placing "first collision order" in this tradition. This strengthens the novelty claim, because those results concern single indices while this one concerns a whole class.
- **Verification method:** confirm the bibliographic data of each citation before adding it (MATCH rejects non-existent references).
- **Residual uncertainty:** the bibliographic details of P41 and P76 were only Consensus-level in the log.

**N6. Song & Huang 2023 is described within scope** (line 632)
- **Evidence:**
  - The text limits their result to the edge division vector and edge-additive eccentric indices Σ f(μ(e)). Wiener and Gutman indices qualify on trees, since Gut = 4W − (2n−1)(n−1).
  - It says "Neither partition of trees refines the other".
  - The octane Wiener values 76/75 and 68/67 are the standard values.
- **Severity:** none. Class: VERIFIED FACT.
- **Residual uncertainty:** the full text of Song–Huang was not re-read here. `audit/V4031_REVISION_REPORT.md` §1 records a full reading.

**N7. Exponential and extremal literature not cited**
- Liu, You, Chen, Huang, *MATCH* 92 (2024), "Unified extremal results for (exponential) BID indices of trees", is not cited. A referee may ask why Prop 10 is not derived from it.
- The prior audit concluded it does not apply, because e^{γq} is not monotone in each degree.
- **Severity:** minor. Class: PLAUSIBLE REFEREE CONCERN.
- **Necessary revision:** one sentence after line 1291 saying why that result does not cover Prop 10, after verifying the reference.
- **Residual uncertainty:** the claim that it does not apply rests on the prior audit, not a re-read.

**N8. The withdrawn weak-discrimination theorem does not leak**
- Branch `origin/research/weak-discrimination` (41db8c1) contains "Theorem (Imbalance restores weak discrimination)" and a corollary for M_{0,1/2}.
- Current main.tex contains:
  - only the generic statement (line 974, a consequence of Prop 8);
  - the single Rada–Rodríguez–Sigarreta χ pair (lines 987–1007, Example 2);
  - finite-order counts explicitly "not proved for larger orders" (lines 1120–1122).
- There is no `thm:weakdisc` and no claim that γ restores weak discrimination at rational exponents. Class: VERIFIED FACT, no action needed.

### 1.4 Hypotheses and edge cases (G)

| Case | Where | Status |
|---|---|---|
| γ < 0 | Thm 2(ii) "nonzero algebraic"; Prop 10 swap; Props 12/13 restricted to γ ≥ 0 (lines 1305–1307) | Correct (VERIFIED) |
| γ = 0 | Excluded from Thm 2(ii): all graphs of equal size agree. The parent at γ = 0 on Π separates histograms at all but finitely many α (lines 654–657), stated per pair. | Correct |
| Transcendental γ | Counterexample at γ = ln 4 (line 704) | Correct |
| Irrational α, β in Prop 3 | Hypothesis α, β ∈ ℚ stated (line 673), and repeated in the remark (line 698) | Correct |
| Trees vs profiles | Line 717: "separate more trees" should read "take more distinct values / separate more profiles". Lines 1112–1114 use "profiles" correctly. | Editorial |
| Degree cap | Lemma 1 needs Δ ≥ 3. Prop 4's "five" holds for Δ ≤ 4. Five crossings are attained only at Δ = 6, and Δ ≤ 4 is open (lines 776, 1812–1814). | Correct |
| Thm 2(iii) with d = 2 or L = 1 | The vector −(1,d) + (2,d) + (L−1)(2,2) + (1,2) is fine; the maximum degree is preserved because it is ≥ 2. | Correct |
| Pendant-path attachment needs a common d | Stated as a hypothesis. Both witnesses satisfy it (d = 3 and d = 4). | Correct |
| Lines 1291 (i, j ≥ 2 ⇒ ij/(i+j) > 1) | Fails at (2,2), which the sentence's "every other pair" implicitly excludes. | Editorial: write "i, j ≥ 2, (i,j) ≠ (2,2)" |

---

## 2. Chemistry and statistics (perspectives C and S)

**S1. "50 optimizer seeds are not 50 samples"** (lines 1673–1676, 1680–1682, 1764–1765; PREREG_v37 decision rules)
- Disclosed: the seed counts are called a "summary of optimiser variance", the text says "we regard [this] as a design error", and measured boiling points became primary.
- **Severity:** none remaining. Class: VERIFIED FACT.
- **Residual risk:** a referee may still object that "replicates" appears as a verdict word at all (line 1670). Keep the scare-quote explanation.

**S2. Equal budgets in 2D vs 3D, and random search** (lines 1654–1656, 1780–1782, 1879)
- **Evidence:** the paper discloses that the design "may handicap" the three-parameter model.
- **New observation (VERIFIED FACT):** `audit/v4030/gamma_strict_out.txt` gives these registered-test results on the source-strict cohorts:

  | Cohort | n | Median ΔQ² | 95% molecule-bootstrap interval |
  |---|---|---|---|
  | Strict decanes | 28 | −0.129 | [−0.186, −0.029] |
  | Strict C9–C10 pooled | 42 | −0.040 | [−0.091, −0.005] |

  Both intervals **exclude zero on the negative side**. The supplement (lines 970–971) reports only "LO ahead in 12 and 10 of 50 seeds".
- A referee who sees the intervals may read them as evidence that the 3D random search is less efficient. The ablation also shows a 0.957 → 0.946 hybrid loss in the wide box (line 1651). Taken together, this suggests the negative verdict partly measures the optimiser, not γ.
- **Severity:** major if raised. Class: PLAUSIBLE REFEREE CONCERN; the unreported intervals are a VERIFIED FACT.
- **Necessary revision:** report the two strict-cohort intervals in S8, with the caveat that they are conditional and exploratory.
- **Optional (expensive, not run here):** an exploratory control giving both models a deterministic optimiser, e.g. a dense grid or multistart local optimisation inside each fold. It would separate "γ is useless" from "the search is starved".
- **Verification method:** rerun `audit/v4030/gamma_strict.py` (about 25 min).
- **Residual uncertainty:** whether better optimisation changes any verdict is unknown.

**S3. Nested LOO and selection** (lines 1609–1615; Tables 5 and S7)
- The design is fully nested and the ridge penalty is chosen inside folds. The permutation check reruns the full nested ridge (lines 1792–1795): p = 1/201, independently reproduced.
- The permutation tests ridge's association, not γ. The text does not claim otherwise.
- **Severity:** none. Class: VERIFIED FACT.

**S4. Conditional molecule bootstrap** (lines 1697–1699, 1737, 1769–1771, 1776–1786)
- Disclosed as conditional on fitted predictions and as omitting refitting and selection. The "several-fold" multiplier is **gone** from the Table 5 caption: grep finds no hits.
- **Severity:** none. Class: VERIFIED FACT.

**S5. 58 aggregate-derived boiling points (57 + 1) and the 42-molecule strict cohort**
- **Evidence (VERIFIED):** supplement line 1036 now says "57 of the 100 … and 1 further value … so 58 values rest on NIST averages". Supplement lines 964–971 say the restricted pooled set keeps only 42 boiling points, all nonanes and decanes, "because every C6–C8 value is a NIST average".
- **main.tex** mentions neither. Section 6.4 (lines 1707–1713) describes the extraction rule without saying that averages bypass the 3 K screen or that 58% of values are aggregates.
- **Severity:** minor. Class: PLAUSIBLE REFEREE CONCERN.
- **Necessary revision:** one sentence in Section 6.4: "58 of the 100 values rest on NIST averages, which the rule admits without the 3 K screen. Restricted to primary determinations only 42 values remain, all C9–C10 (Supplementary Section S8)."
- **Verification method:** `prose_claims_a.py` entry `corr_agg58`, and `external/bp/bp_provenance.csv`.
- **Residual uncertainty:** none on the counts. The quality of the 57 averages is not established.

**S6. Octane entropies, TMB ΔH_vap, acentric factors and nonane ΔH_vap provenance** (lines 1544–1557, 1665–1669, 1815–1819)
- Disclosed:
  - seven entropies unresolved;
  - ω compiled, of unidentified origin;
  - TMB 8.41 with no source, crystalline at 298 K;
  - 29/34 nonane ΔH_vap values are compilation entries.
- The Discussion (iii) says "Seven octane entropies and the compiled acentric factors rest on secondary sources". The audit found the ω source unidentified (`FINAL_DATA_PROVENANCE_AUDIT` W1).
- On the 29 compiled nonane values alone, the pre-registered ΔH_vap verdict would read "mixed" (77/100 and 75/100; provenance audit §1). This is not in the paper.
- **Severity:** minor. Class: VERIFIED FACT (disclosure present) + PLAUSIBLE REFEREE CONCERN (compiled-only sensitivity absent).
- **Necessary revision:** optionally add the compiled-only nonane split to S4 as exploratory.
- **Residual uncertainty:** primary sources for the entropies (Scott 1974) were not consulted.

**S7. Scope of the error floor** (lines 923–928)
- Correctly stated as a bound for a single fixed predictor, not for cross-validated errors. Class: VERIFIED FACT, no action.

**S8. Pooled Q² confounded by carbon number** (lines 1715–1717, 1747, 1796–1798)
- "Size alone gives Q² = 0.938" is stated, and Test B is called a "pooled size-adjusted analysis rather than a fresh external test". LOO is not grouped by n_C, and the text does not say so.
- **Severity:** minor. Class: PLAUSIBLE REFEREE CONCERN.
- **Necessary revision:** add "(leave-one-molecule-out, not grouped by carbon number)".

**S9. Wiener W + p₃ benchmark** (lines 1795, 317–318)
- **Evidence:** W + p₃ gives Q² = 0.904 on the decanes, above ridge (0.860). This was independently reproduced (0.9038). The text gives it honestly in Section 6.4.
- Contribution (vi) (lines 316–318) says ridge "leads every single index evaluated in point estimate". That is literally true, since Wiener's model has two descriptors. However, a chemistry referee will note that the paper's best decane predictor is a 1947 two-descriptor model containing distance information.
- **Severity:** minor. Class: PLAUSIBLE REFEREE CONCERN.
- **Necessary revision:** add to contribution (vi): "…while Wiener's two-descriptor model, which adds the Wiener index, has the highest decane point estimate."

**S10. Abstract, captions and conclusion versus outputs**

| Location | Text | Finding |
|---|---|---|
| Abstract, lines 210–212 | "an exploratory gain on vaporisation enthalpies shrinks to about zero" | **Mislabelled.** The nonane gain met a pre-registered seed-count criterion (lines 1669–1672). The wide-box comparison is what was exploratory (lines 1638, 1823). See text error E1. |
| Line 1822–1823 | "the wide-box analysis that reverses the nonane conclusion" | Inconsistent with "shrinks to about zero" (lines 1643, 1679, 1840–1841) and with the median −0.002. See E2. |
| Lines 1157–1159 | "shows that the favourable sensitivity–abruptness balance is a property of linear imbalance weighting" | Rests on 0.4625 vs 0.4579, a third-decimal difference. Lines 1149–1150 say such differences "do not rank the indices". See E3. |
| Table 5 caption | "several-fold" | Removed. VERIFIED. |
| "dominance", "strongest baseline", "superior" | — | No overclaiming hits. "strongest" appears once (line 1585) for a column correlation, with caveats at 1595–1597. VERIFIED. |
| Conclusion, lines 1879–1882 | — | Accurate ("met the seed-count criterion … interval that included zero"; "no equivalence test"). |

---

## 3. Computational reproducibility (perspective R)

**R1. No immutable version is cited** (line 2055–2057; Data availability, lines 1889–1906)
- **Evidence (VERIFIED):**
  - `LoyolaRepo` gives `https://github.com/Singati2/LOYOLA-PAPER (2026)` with no commit, tag or DOI, and no `\url`.
  - `git branch -a` shows `origin/main` is older than the review branches, so a referee following the link sees an older package (also LOYOLA_REVIEW R7).
  - No Zenodo DOI exists (MATCH_SUBMISSION_READINESS §5 item 4).
- **Severity:** major for an R referee. Class: VERIFIED FACT.
- **Necessary revision:** before submission, merge or tag the frozen commit, mint an archive DOI, and cite the DOI and commit in the bibliography and Data availability.
- **Verification method:** resolve the DOI, then check that the tag's tree builds both PDFs and passes `verify.py`.
- **Residual uncertainty:** none on the facts.

**R2. NIST raw pages in history and third-party data rights**
- 262 WebBook pages remain in older branches and history. KDB/Cheméo terms are unresolved (V4031 §6, LOYOLA_REVIEW R8).
- **Severity:** minor for referees, a release blocker for archiving. Class: AUTHOR DECISION.

**R3. Coverage statements**
- The Lean count is consistent: 38 listed plus all 52 declarations.
- `LEAN_VERIFICATION.md` mentions only the 38 checks and not the 52-declaration pass that `verify.sh` also performs. **Editorial.**
- Lean was NOT re-run at the recent heads (V4031 §8). `formal/` is unchanged since a PASS at 09ceba8. Class: VERIFIED FACT.
- **Necessary revision:** run `formal/verify.sh` once at the frozen commit and archive the log.

**R4. A prose-number check passes for the wrong reason** (new; VERIFIED FACT)
- `prose_claims_a.py` line 951, entry `bp_3K_a`, anchors the "3 K" spread threshold to the regex `\\headsep\s+=\s+(?P<v>\d+)pt\s+\\renewcommand\*\{\\thefootnote\}…`. That regex matches `main.tex` lines 117–119 (`\headsep = 3pt`), a page-layout parameter.
- main.tex contains no "3 K" claim at all; grep finds none.
- The check reports success independent of the data.
- **Severity:** minor (tooling integrity, no effect on the paper). Class: VERIFIED FACT.
- **Necessary revision:** point the entry at supplement text that states the 3 K rule, or retire it.
- **Verification method:** grep `bp_3K_a` and confirm the match location.

**R5. Exact-tie checker coverage, Colab state model and token exposure** (LOYOLA_REVIEW R1–R3)
- Recorded as fixed on the 19 October correction branch (`audit/REVIEW_2026-10-20_STATUS.md`, `audit/CORRECTIONS_2026-10-19_STATUS.md`). Not re-tested here.
- **Residual uncertainty:** whether those fixes are in 325bd05's ancestry was not traced line by line.

---

## 4. Title (AUTHOR DECISION)

| Option | Fits | Misfits |
|---|---|---|
| Current: "The Loyola Index Family and the Resolution Limit of Degree Imbalance" (line 177) | q is the normalised degree imbalance and is in bijection with the degree ratio, so the phrase is technically accurate. Thm 2(i)–(ii) holds for all graphs, not only trees. | It reads as if γ (the imbalance parameter) has a resolution limit. The paper's Remark (lines 655–659) says "The limit thus belongs to the dependence on the degree ratio, not to γ", and the parent reaches the same limit. A referee may see a mismatch between the title and the body. |
| Short draft: "The Loyola Index Family and the Resolution Limit of Degree-Ratio Indices on Trees" (`drafts/short/main_short.tex:177`) | Names the class that is actually bound (GA, AG, SDD, ISDD, DSO, degree-ratio Sombor) and the setting of the new combinatorial result (orders 13 and 16 are tree results). It matches the strongest defensible contribution identified by every prior audit. | "on Trees" undersells Thm 2(i)–(ii), which holds for all graphs. The phrase "resolution limit" for a class of indices is new terminology. |

**Panel view (simulated, non-binding).** The short-draft title describes what is new more precisely. The authors could also drop "on Trees" if they want the general-graph statement covered. The revision report (V4031 §5) records that the authors kept the current title deliberately. This is an author choice, not a correction. If the title is kept, one sentence in the introduction saying that "degree imbalance" means the degree ratio, not the parameter γ, would remove the misreading.

---

## 5. Concrete text errors in main.tex (only evidenced ones)

| ID | Line | Current text | Problem | Proposed fix |
|---|---|---|---|---|
| E1 | 210–212 | "and an exploratory gain on vaporisation enthalpies shrinks to about zero once the parent is searched over a box that does not truncate it." | The nonane ΔH_vap gain met the **pre-registered** seed-count criterion ("replicates", lines 1669–1672). What is exploratory is the wide-box comparison (lines 1638–1639, 1822–1823, Table 6). The abstract mislabels which part is exploratory. | "and a gain on vaporisation enthalpies that met a pre-registered seed-count criterion shrinks to about zero, in an exploratory comparison, once the parent is searched over a box that does not truncate it." |
| E2 | 1822–1823 | "but the wide-box analysis that reverses the nonane conclusion is itself not pre-registered." | "Reverses" overstates. Everywhere else the gain "shrinks to about zero" (lines 1643, 1679–1680, 1840–1841). The hybrid median is −0.002 and the 3D median −0.016 (line 1648). | "but the wide-box analysis, in which the nonane gain shrinks to about zero, is itself not pre-registered." |
| E3 | 1157–1159 | "The higher ratio of this first-order aggregate shows that the favourable sensitivity--abruptness balance is a property of linear imbalance weighting rather than of the exponential form." | The ratios differ only in the third decimal: 0.4625 for IRLA vs 0.4579 and 0.4565 for the pure-γ points. Lines 1149–1150 say "these third-decimal differences do not rank the indices". "Shows" contradicts that. | "The comparable ratio of this first-order aggregate suggests that the sensitivity--abruptness balance does not depend on the exponential form." |
| E4 | 717–719 | "generic points off $\Pi$ … and the Randi\'c index separate more trees than any point of $\Pi$." | Trees/profiles conflation, as flagged in LOYOLA_CORRECTIONS item 7. No vertex-degree-based index separates trees with equal profiles. The comparison is of distinct values (570 vs 566 at n = 13, and so on). | "…take more distinct values on the trees than any point of $\Pi$." |
| E5 | 1291 | "if $i, j \ge 2$ then … and $ij/(i+j) > 1$" | False at (2,2), where ij/(i+j) = 1. The sentence means "every other pair" but the quantifier includes (2,2). | "if $i, j \ge 2$ and $(i,j) \ne (2,2)$ then …" |
| E6 (editorial) | 1704–1706 | "NIST lists only $25$ skeletons outside $C_8$ and $C_9$, and one of the $75$ decanes, with at least one calorimetric…" | Ambiguous. `prose_claims_a.py` (`bp_cal25`: rows with n ∉ {8,9}) shows the one decane is **among** the 25, but the sentence reads as 25 + 1. | "NIST lists only $25$ skeletons outside $C_8$ and $C_9$, among them one of the $75$ decanes, with at least one calorimetric…" |

No numerical error was found in main.tex. Every number spot-checked (SSE, witnesses, closed forms, Example 2, GA merge, SDD 58/3, structure-sensitivity ratios, Table 4 margins, Lean counts, supplement table cross-references S3–S7) agrees.

---

## 6. Separation by class

**VERIFIED FACT**
- Thm 2 hypotheses are stated correctly (algebraic γ ≠ 0, with γ < 0 allowed). Prop 3 needs α, β ∈ ℚ, and it states this.
- The witnesses at orders 13 and 16 and the GA order-17 witness are correct by hand.
- Lean: 38 listed, 52 declarations, and the textual scope at lines 1306–1313 and 1899–1906 is accurate.
- The "several-fold" claim is removed. There is no "dominance" or "strongest baseline" overclaim.
- The withdrawn weak-discrimination theorem is absent.
- The 58/42 counts are in the supplement only.
- The strict-cohort γ intervals exclude zero on the negative side and are unreported.
- `bp_3K_a` is mis-anchored.
- `LoyolaRepo` has no immutable identifier, and `main` is stale.
- Text errors E1–E5.

**PLAUSIBLE REFEREE CONCERN**
- Novelty thin relative to size (N1, N2).
- Minimality without a certificate (N4).
- Missing minimal-order degeneracy citations (N5) and Liu et al. 2024 (N7).
- Optimiser handicap (S2).
- Main-text disclosure of the aggregate boiling points (S5).
- Compiled-only nonane split (S6).
- Grouping by n_C (S8).
- The Wiener model in contribution (vi) (S9).
- Length and audit-trail density (risk 2).

**EDITORIAL PREFERENCE**
- Demote Prop 7 to a remark.
- Drop "irreducible" (line 910).
- E6.
- Shorten Table 6, e.g. merge the three solver-guard rows into "numerical-hygiene changes; no output changed".
- Add the five-crossing question to the conclusion's list of open problems.
- Mention the 52-declaration check in `LEAN_VERIFICATION.md`.

**AUTHOR DECISION**
- Title (Section 4).
- Archive DOI and merging to `main`.
- NIST and KDB distribution.
- AI-use disclosure (MATCH states no policy).
- Acknowledgment placeholder (line 1908).
- Whether to cut Section 6 or the supplement.
- Whether to run an optimiser-fairness control.

---

## 7. Anticipated editor and referee outcome scenarios (no probabilities)

1. **Major revision on significance and length.** Referees accept correctness and ask the authors to:
   - refocus on the degree-ratio obstruction;
   - shorten Section 6 and Table 6;
   - add a certificate for the enumeration;
   - add context citations.

   This matches the prior internal readiness assessment.
2. **Minor revision.** A graph-theory referee values the explicit witnesses binding four recent MATCH degree-ratio Sombor papers, plus the honest negative QSPR. Requested changes are wording (E1–E5) and the reference version (R1).
3. **Reject: insufficient novelty.** A referee views the paper as a known theorem (Rada 2019) plus a computer search plus a negative QSPR study. The objection would be that the family adds nothing (the paper itself shows γ adds no generic discrimination and no demonstrated predictive gain), so introducing a new named index is unjustified.
4. **Split request.** The editor suggests a short mathematical note on degree-ratio indices (essentially the short draft), with the QSPR study moved elsewhere or dropped.
5. **Reproducibility hold.** A referee follows the repository link to the stale `main`, finds an inconsistent package, and asks for an archived release before review continues.

---

## 8. Factual author rebuttal outline

1. **Attribution, not overclaiming.** Thm 2(ii) is credited to Rada 2019 Thm 3.4 (line 632), the Corollary to Rada 2019 Prop 2.5 (line 650), and the pendant-path device to Rada 2026 (line 599). The claimed novelty is limited to the first orders 13 and 16 and their explicit witnesses (line 650: "what is new are the explicit witnesses and the orders at which they first occur").
2. **Why it matters for MATCH.** One explicit pair of order-13 trees, and one of order-16 chemical trees, defeats GA, AG, SDD, ISDD, exponential GA/ISDD, the diminished Sombor index and the degree-ratio Sombor index studied in MATCH 97 (Corollary, lines 634–647). No paper introducing those indices records this. The literature search is documented, and its limits are stated in `audit/final/NOVELTY_SEARCH_LOG.md`.
3. **Minimality is computer-assisted and stated as such** (lines 302–303, 541–544, 632, 1807–1811):
   - exact rational arithmetic;
   - tree counts checked against OEIS A000055/A000602;
   - independently reproduced;
   - [if added] the colliding classes are listed in the supplement.
4. **Exactness of the counts.** Ties are certified by Lindemann–Weierstrass and Besicovitch, not by floating point (Table 2 caption, lines 1075–1082).
5. **γ is not sold as better.** The paper says so explicitly (lines 259, 290–293, 976–985), and the pre-registered tests are negative and reported as such, with every post-hoc change listed in Table 6.
6. **On the optimiser critique.** Equal budgets and random search are pre-registered (PREREG_v40). The text states the possible handicap (lines 1654–1656, 1780–1782) and limits the conclusion to "no gain demonstrated under these protocols" (lines 1783–1786). [If run] An exploratory deterministic-optimiser control gives …
7. **Data quality.** Every unresolved value is listed with a sensitivity analysis (Supplement S1, S8). No unresolved octane value enters a pre-registered test (lines 1556–1557).
8. **Reproducibility.** [After R1] The archived release <DOI> at commit <hash> rebuilds both PDFs and passes the verifier. The Lean scope is stated precisely, and the transcendence, Laguerre and enumeration arguments are declared not formalised (lines 1902–1903).

---

*Sources consulted for this matrix:*
- `main.tex` and `supplement.tex` at 325bd05;
- the audit files listed in the brief;
- `formal/verify.sh` and `formal/expected_axiom_theorems.txt`;
- `prose_claims_a.py` lines 948–954;
- `audit/v4030/gamma_strict_out.txt`;
- `drafts/short/main_short.tex`;
- the web: arXiv:2508.06532 (definition of the diminished Sombor index) and MATCH 87 (2022) 97–108 (Rada, Rodríguez, Sigarreta).


---
## Integration note (2026-10-20)

Applied in the candidate after checking each against main.tex: E1 (abstract labels the registered seed-count result and the exploratory wide-box comparison exactly), E2 ("reverses" -> "shrinks to about zero"), E3 ("shows" -> "suggests", third-decimal gap), E4 (trees -> distinct values), E5 ((i,j) != (2,2)), E6 ("among them one of the 75 decanes"). Registry entry bp_3K_a removed (it matched the preamble line \headsep = 3pt; main.tex states no 3 K threshold). Not applied (AUTHOR DECISION): title, length reduction, new analyses (search protocol, strict-cohort intervals in the main text, compiled-only nonane verdict), citation of a fixed repository version.
