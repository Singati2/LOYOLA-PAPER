# Claim-by-claim novelty matrix: Loyola index family (MATCH submission)

> **Status (2026-10-23).** This report audits commit `3904e38`; line numbers refer to that commit. Items marked as applied are in `audit/MATCH_PATCH_LOG_2026-10-23.md`. Local full texts used for checking are private copies outside the repository and are not distributed. Discovery tools were used only to find sources; each claim was checked in the source itself.

Date: 2026-10-23. Manuscript: `main.tex` at commit 3904e38, identical to `submission_candidate/match/main.tex`. The audit was read-only: nothing in the repository was edited.
Line numbers are main.tex lines.

## 0. Sources and method

**Primary full texts examined.** These are local private copies under a private directory outside the repository. Their first lines were checked to confirm identity.

| Key | Bibliographic record (verified) | What was read |
|---|---|---|
| Rada2019 | J. Rada, *Exponential vertex–degree–based topological indices and discrimination*, MATCH 82 (2019) 29–41 | Full text: Table 1 (p.31) lists GA; Def. 2.1, Ex. 2.2, Def. 2.3, Ex. 2.4, **Prop. 2.5 (p.34)**, Ex. 2.6 (p.35, trees in G_29), Def. 3.1, Thm 3.3, **Thm 3.4 (p.36)**, **Cor. 3.5 (p.36)**, Ex. 3.6 |
| CruzRada2019 | R. Cruz, J. Rada, MATCH 82 (2019) 715–732 | Thm 2.1, Cor. 2.2, Thm 3.1, Cor. 3.2 located (text lines 145, 217, 636, 667); eqs. (3)–(4) |
| RRS2022 | J. Rada, J. M. Rodríguez, J. M. Sigarreta, MATCH 87 (2022) 97–108, doi 10.46793/match.87-1.097R | Ex. 2.1, **Ex. 2.2** (sum-classes; order 17+p), Thm 2.3 (Sombor weakly discriminating on CT_n), Thm 3.1, Thm 3.8 |
| Rada2026 | J. Rada, MATCH 96 (2026) 841–863, doi 10.46793/match.96-3.32925 | §3.1 (pendent-path device, l.335–336), Thm 3, Cor. 2, Ex. 3. Searched for "ratio": no degree-ratio or imbalance content |
| Gutman2026 survey | MATCH 96 (2026) 819–837 | Scanned: lists the degree-ratio Sombor and irregularity-Sombor indices. No discrimination-order results |
| Kırgız2027 | H. Kırgız, *On hyperbolic Sombor index and other topological indices*, MATCH 97 (2027) 121–134 | Definition: HSO = Σ√(d_u²+d_v²)/min(d_u,d_v) = Σ√(1+ρ⁻²), so HSO is **a degree-ratio index**. It also reports that Barman–Das computed HSO degeneracy on C8–C10 isomers |
| NyauliBuragohain2027 | MATCH 97 (2027) 135–164 | Scanned for discrimination and degeneracy content: none on collision orders |
| GutmanRBN2027 | MATCH 97 (2027) 165–174 | Read §4. Two decanes share DRSO and SO; I checked by hand that they share the **same profile** {(1,3)^6,(3,3)^3}. So this is not a ratio collision |
| AliGFAH2025 | AIMS Math. 10 (2025) 6788–6804 (`indep_lit/dl_ali`) | Abstract only |

**Bibliographic records verified this pass.** These were checked through Crossref, the MATCH contents pages and publisher abstracts.
- Jameson, Math. Gaz. 90 (2006) 223–234, doi 10.1017/S0025557200179628.
- Song–Huang, MATCH 89 (2023) 343–370, doi 10.46793/match.89-2.343s. The abstract confirms "trees of order no more than 10 completely determined".
- Das–Mondal EGA, J. Math. Chem. 62 (2024) 2740–2760, doi 10.1007/s10910-023-01542-z. The abstract states that "isomer discrimination potential" is assessed.
- Das–Mondal–Raza–Pal, J. Appl. Math. Comput. 71 (2025) 537–561.
- Gutman–Buragohain–Nyauli, J. Math. Chem. 64 (2026) #39.
- Gutman–Milovanović–Milovanović, AKCE 17 (2020) 74–85.
- Ali–Gutman–Furtula, Aequationes Math. 100 (2026) #66.
- Gao–Gao, AMC 472 (2024) 128634. The abstract confirms sufficient conditions for path-unique-min and star-unique-max of exponential VDB indices.
- Hu et al., MATCH 88 (2022) 505–520.
- Mityagin, Math. Notes 107 (2020) 529–530.
- MATCH contents pages: Barman–Das 95 (2026) 63–94; Movahedi et al. 95 (2026) 141–162; Nyauli–Buragohain CoRSO 96 (2026) 295–324; Ali et al. DRSO 97 (2027) 639–656; Shao–Jahanbani 97 (2027) 657–675.

**Not verified in this pass.** These are marked UNVERIFIED where used: Molina et al. AIMS Math 10 (2025) 1998–2020; Granados et al. JMC 63 (2025); Portilla et al. JMC 63 (2025); Réti et al. MATCH 79 (2018) 509–524 (the title was confirmed, but not the IRLA formula); Lin et al. AIMS Math 7 (2022) 25–38 (the title was confirmed); Baker 1975; Besicovitch 1940; Konstantinova 1996.

**Discovery queries run in this pass.** These add to the 20-query Consensus log in `audit/final/NOVELTY_SEARCH_LOG.md`, which was re-read.
- Consensus: "smallest trees with equal degree-based topological index different edge degree counts discrimination".
- Consensus: "degree-based topological indices that depend only on ratio of end-vertex degrees discrimination trees".
- Consensus: "exponential vertex-degree-based topological indices discrimination Rada".
- Consensus: "exponential irregularity index exp of degree difference edges topological index parameter".
- Consensus: "chemical trees with different edge-type vectors but equal geometric-arithmetic index or symmetric division deg index".
- WebSearch: "weakly discriminating degree-based index chemical trees smallest order Sombor geometric-arithmetic".
- WebSearch: "degeneracy of geometric-arithmetic index trees same GA non-isomorphic minimal order".
- WebSearch: "symmetric division deg index trees equal value different degree pairs discrimination".
- WebSearch: "topological index edge weight exp(|du−dv|/(du+dv)) imbalance parameter generalized index family".
- WebSearch: "non-isomorphic trees same M-polynomial smallest order degree-based indices equal".
- WebSearch: "general Albertson irregularity index OR sigma_t irregularity parameter imbalance degree-based family".
- WebSearch: "Descartes rule of signs Laguerre topological index parameter crossings ordering graphs general Randić".
- WebSearch: "degree-ratio topological index discrimination trees edge ratio distribution isomers degeneracy 2026".
- WebSearch: "Kulli (a,b)-KA index OR general sum-connectivity OR variable sum exdeg imbalance parameter exponential edge weight family".
- OpenAlex forward citations of RRS2022 (W3203569470). This returned 2 citing works, both on Euler–Sombor and both irrelevant. OpenAlex indexes Rada2019 with 0 citations, so citation chaining through OpenAlex failed for that paper.
- Semantic Scholar returned HTTP 429 (rate-limited), so no result came from it.

**Result of discovery.** No earlier determination of the first orders (13 for trees, 16 for Δ≤4) at which the degree-ratio (q-) histogram fails to determine the degree-pair profile was found in this search (queries above plus the repository log). This is an absence-of-evidence statement, not proof of novelty.

Closest analogues found:
- RRS2022 Ex. 2.2 gives chemical trees with distinct profiles and equal degree-*sum* class counts, at orders ≥18, with no minimality claim.
- Rada2019 Ex. 2.6 gives Randić product classes at order 29.
- Song–Huang 2023 completely determine trees of order ≤10 with equal edge-division vectors (a distance-type invariant).
- Minimal-order results for other indices exist: smallest JJ-equivalent trees at order 18 (Guo, Randić et al. 1999) and the smallest degenerate alkane pair for distance-information indices at 18 vertices (Ivanciuc et al. 1993). Both are listed in the repository log but are not cited in main.tex.

No prior family found in this search uses an exponential, normalised imbalance factor e^{γ|du−dv|/(du+dv)} coupled to M_{α,β}. The closest families are:
- general Albertson A_p (Lin et al. 2022);
- (a,b)-KA, general sum-connectivity and variable sum exdeg (vertex-based);
- variable Euler–Sombor and cosine-rule Sombor (already cited);
- exponential VDB indices generally (Rada2019; Gao–Gao 2024; Carballosa et al. JMC 2023, not cited in main.tex).

No use of Laguerre's rule of signs to bound order exchanges of a topological index along a parameter was found in this search.

## 1. Matrix

Classification key:
- **novel**: not found in the sources examined.
- **known**: stated in a cited source.
- **adapted**: a known result or method specialised or extended.
- **computational**: rests on finite enumeration.
- **exploratory**: empirical.

Confidence:
- **H**: primary source read at the cited location.
- **M**: primary source read only in part, or only the abstract.
- **L**: not read.

| # | Claim (section, line) | Closest published result (citation, location) | What prior authors established | What this manuscript adds | Class | Corrected wording / missing citation | Conf. / source examined |
|---|---|---|---|---|---|---|---|
| A1 | Abstract l.196–198: VDB indices cannot distinguish graphs with equal edge-degree-pair counts; ratio-only indices lose more | Rada2019 Ex. 2.2 (p.32), Prop. 2.5 (p.34); Rada2026 §3.1 | Equal m ⇒ equal value; equal class sums ⇒ equal value | Nothing new; framing only | known | none | H / full |
| A2 | Abstract l.203–206: "By theorems of Rada", LO(0,0,γ) at algebraic γ≠0 separates exactly the q-histograms, and no degree-ratio index separates more | Rada2019 Thm 3.4 + Prop. 2.5; **also Rada2019 Cor. 3.5 applied to GA** | Thm 3.4: e^φ with algebraic φ separates exactly the m̂_φ-classes on G_n. GA is in Table 1, and √(1−q²) is injective in q, so m̂_GA = q-histogram. **So e^{GA} already separates exactly the q-histograms (Cor. 3.5)** | Extends to graphs of unequal order (trivial); gives a one-parameter family of such separators | known (adapted) | Optional: "By an argument of Rada". **Missing credit:** the exponential GA index (and e^{ISDD}, e^{SDD}) already has this property by [Rada2019, Thm 3.4/Cor. 3.5]; see R4 | H / full |
| A3 | Abstract l.207–209; intro l.310–314: the histogram determines the profile of every tree up to order 12, and of every chemical tree up to order 15 | none found (queries §0) | — | Exhaustive enumeration of orders 2–17 in exact arithmetic (independent certificate in repo) | computational, novel (search-based) | Keep "by exhaustive enumeration"; keep the absence claim scoped to the search | M (absence claim) / n.a. |
| A4 | Abstract l.209–210: explicit counterexamples at every larger order | Rada2026 §3.1 (pendent-path device); RRS2022 Ex. 2.2 (sum-class analogue) | The device carries equal-m pairs to all larger orders. RRS gives sum-class witnesses | The ratio-class witnesses at 13 (Δ=6) and 16 (Δ=4); the device adapted to distinct-profile/equal-histogram pairs | novel witnesses + adapted device | none (credit present l.599, l.632) | H / full |
| A5 | Abstract l.210–211; intro l.315–316; concl. l.1442–1443: at fixed (α,β) two chemical graphs exchange order at most five times along γ | Laguerre's rule (Jameson 2006); no TI application found | Classical rule of signs for generalised polynomials | Count of 6 distinct imbalances for Δ≤4, giving ≤5; sharpness shown only at Δ=6 | adapted (routine application) | Already scoped. The "open for Δ≤4" caveat (l.785, l.1471) should stay | H (proof checked) / Jameson record verified, text not read |
| A6 | Abstract l.211–215; concl. l.1449–1460: no demonstrated γ gain on boiling points; the ΔH_vap gain shrank in an exploratory rerun | — | — | Pre-registered negative tests; exploratory wide-box rerun | exploratory | none | n.a. |
| I1 | Intro l.223–228: linear-functional representation on Δ≤4 | Rada2019 eqs. (1)–(2); RRS2022; Cruz–Rada eq. (1); Rada2026 §2.1 | The representation | none | known | Already credited | H |
| I2 | Intro l.274: γ reads no information beyond the counts but can separate graphs the parent merges at rational exponents | Rada2026 §2.1; RRS2022 Ex. 2.2 | Counts ceiling; sum-class failures of χ | Ex. 1 (l.896): LO(0,−½,1) separates the RRS pair | adapted / novel example | none | H |
| I3 | Intro l.276–280: LO is a subfamily of Rada's exponential VDB indices | Rada2019 Def. 3.1 | Every positive-weight index is formally exponential | — | known (trivial inclusion) | OPTIONAL: append "; Rada's discrimination theorem applies where the exponents are algebraic, in particular at the pure-γ points" | H |
| I4 | Intro l.281–299: novelty of the coordinate (linear in q in the exponent, coupled to GM; log-linear weights) | Das–Mondal 2024 (EGA); Das et al. 2025 (EISDD); Gutman et al. 2025 (variable Euler–Sombor); Nyauli–Buragohain 2026 (CoRSO); Movahedi et al. 2026 (DSO); Lin et al. 2022 (A_p); Réti et al. 2018 (IRLA) | Exponentials of single generators; polynomial and unnormalised imbalance weights; ratio functions | The 3-parameter log-linear form | novel definition (search-based) | Missing: the hyperbolic Sombor index (Barman–Das 2026, already in the bibliography) is a ratio function and could be named at l.287–289. Lin et al. and IRLA records: UNVERIFIED formula | M / abstracts + Kırgız full text |
| I5 | Intro l.310: "What is new here is where the known results bind for chemical graphs" | — | — | The order-13 result is for all trees, not chemical graphs | wording | OLD "where the known results bind for chemical graphs" → NEW "where the known results bind for trees and chemical trees" (OPTIONAL) | n.a. |
| I6 | Intro (i) l.320–333: Thm 2(ii) is Rada Thm 3.4 for equal order; corollary is Prop. 2.5; Prop. 3 is the same LW argument; extremal trees from Cruz–Rada; octane pairs realise the ceiling | Rada2019 Thm 3.4/Prop. 2.5; Cruz–Rada Cor. 2.2/3.2; Rada2026 §3.1 | As stated | — | known (correctly credited) | Add Cor. 3.5 / EGA (R4) | H |
| I7 | Intro (ii) l.334–344: witnesses at every order ≥13 / ≥16; Laguerre bound; identifiability (S10); Lemma 1; Thm 1 log-convexity | see rows L1, T1, T2(iii), P4, S10 | — | — | mixed | Thm 1 is a textbook log-sum-exp/exponential-family fact. OPTIONAL: cite Brown 1986 (already in the supplement) in main at l.511 | H |
| I8 | Intro (iii) l.345–347: minimality by enumeration; value counts for orders 7–17 | none found | — | Enumeration | computational | none | n.a. |
| I9 | Intro (iv) l.348–355: diagnostic QSPR | — | — | — | exploratory | none | n.a. |
| L1 | Lemma 1 (l.426–474): affine independence of (1, ln ij, ln(i+j), q_ij) for Δ≥3; fails for Δ≤2 | none found | — | Elementary determinant argument (3^8≠2^13) | novel (elementary) | none | H (proof checked) |
| T1 | Thm 1 (l.479–509): log-convexity; gradient = mean, Hessian = covariance | Standard log-sum-exp / exponential-family facts (Brown 1986, cited only in the supplement) | Convexity of log-partition functions | Specialisation, with the equality cases | known (applied) | Cite Brown1986 (or Boyd–Vandenberghe) in main; consider "Proposition" rather than "Theorem" (OPTIONAL) | H |
| D1 | Def. 3, eq. (5), l.517–533: ratio plane Π (κ=2α+β=0) | Rada2019 Prop. 2.5 gives the class-sum dependence; the identity 4ij/(i+j)²=1−q² is elementary | — | Identifying the plane of the family that is ratio-only | novel (elementary) | none | H |
| T2i | Thm 2(i) (l.549–554): on Π, LO depends only on n_q; graphs agree on Π iff the histograms agree; otherwise a.e. distinct | Rada2019 Prop. 2.5 | Equal class sums ⇒ equal values | iff + a.e. clause (exponential sum + real-analytic zero set) | adapted | none | H |
| T2ii | Thm 2(ii) (l.555–558): pure-γ at algebraic γ≠0 separates exactly n_q; all but finitely many real γ on finite sets | **Rada2019 Thm 3.4 (p.36)**; **Cor. 3.5 (e^{GA} is the same statement for one point)** | Exactly this for φ_ij=γq_ij on G_n | Removes the equal-order restriction; finite-set real-γ clause via Laguerre | known (special case) | Credited at l.632. **Add** at l.632: "For the single point e^{GA} this is already [Rada2019, Corollary 3.5], since the GA weight √(1−q²) is injective in q." | H / full |
| T2iii | Thm 2(iii) (l.559–568) + proof (l.598–630): propagation; witnesses at 13 (Δ=6) and 16 (Δ=4); existence at every n≥13 / n≥16 | Rada2026 §3.1 (device); RRS2022 Ex. 2.2 (sum-class construction) | Device and analogue | Ratio-class witnesses; profile-change vector | novel witnesses; adapted device | Credit present (l.599, l.632) | H |
| R1 | l.634 Song–Huang paragraph | Song–Huang MATCH 89 (2023) 343–370 | Complete determination of equal-EDV trees up to order 10 | Neither partition refines the other (checked in the repo) | known (credited) | none; record verified | M / abstract (full text read in an earlier audit) |
| R2 | l.636: "We found no earlier determination of the orders 13 and 16, **or of explicit colliding trees for degree-ratio indices**" | Single-index coincidences of ratio indices on isomers are plausibly visible in published degeneracy tables: Barman–Das 2026 HSO degeneracy on C8–C10; Das–Mondal EGA "isomer discrimination"; SDD on nonanes. The manuscript itself finds SDD merging distinct profiles at order 9 (l.668–673) | Degeneracy tables (not inspected for distinct-profile ties) | — | wording risk | **IMPORTANT.** OLD: "We found no earlier determination of the orders $13$ and $16$, or of explicit colliding trees for degree-ratio indices, in a literature search recorded in the repository~\cite{LoyolaRepo}." → NEW: "In a literature search recorded in the repository~\cite{LoyolaRepo} we found no earlier determination of the orders $13$ and $16$, and no earlier pair of trees with distinct degree-pair profiles and equal $q$-histograms, which collide for every degree-ratio index at once." | M |
| C1 | Corollary (l.638–651): every I_f(ρ) depends only on n_q; the witnesses defeat GA, AG, EGA, DSO, SDD, ISDD, EISDD, DRSO | Rada2019 Prop. 2.5 (credited l.655) | Class-sum dependence | Explicit witnesses; list of indices | adapted | Add the hyperbolic Sombor index~\cite{BarmanDas2026HSO} (HSO = Σ√(1+ρ^{-2}); verified in Kırgız 2027) to the list (OPTIONAL) | H |
| R3 | Remark l.654–674: within the class, pure-γ at algebraic γ≠0 "attain the most possible"; GA does not; SDD fails at 9 and ISDD at 10 | Rada2019 Cor. 3.5 (EGA); Thm 3.4 also gives e^{ISDD} and e^{SDD} (rational weights) | **EGA, EISDD and ESDD also attain the most possible** | Single-index vs class distinction (correct and valuable); SDD/ISDD witnesses (computational) | known in substance + computational | **IMPORTANT.** OLD (l.655–658): "Within the class it describes, the pure-$\gamma$ points at algebraic $\gamma \neq 0$ attain the most possible: by part~(ii) they separate every pair of graphs with distinct $q$-histograms." → NEW: "Within the class it describes, the pure-$\gamma$ points at algebraic $\gamma \neq 0$ attain the most possible: by part~(ii) they separate every pair of graphs with distinct $q$-histograms. So do the exponential $GA$, $SDD$ and $ISDD$ indices, by~\cite[Theorem~3.4 and Corollary~3.5]{Rada2019ExpVDB}, since their weights are algebraic and injective in $q$." | H |
| P3 | Prop. 3 (l.682–705): parent distinctions survive at rational (α,β), algebraic γ≠0 | Rada2019 Thm 3.3/3.4 method; LW independence over the algebraic numbers | Method | Statement with algebraic coefficients | adapted ("we do not claim it as a new theorem", l.680) | none | H |
| R5 | Remark l.707–716: K4 vs K_{1,3} at γ=ln 4 | — | — | Illustration | novel (trivial) | none | H |
| R6 | Remark floor l.718–735 + Table 2: floors 12/15; GA merges histograms first at 17 (Δ=5); R leaves the floor at 14 | none found | — | Enumeration; exact certification (Besicovitch) | computational | none | M |
| P4 | Prop. 4 (l.737–770): ≤V zeros with parity; ≤5 for Δ≤4 | Laguerre via Jameson 2006 | Rule of signs | Application; Δ≤4 count | adapted | none | H |
| R7 | Remark l.772–790: sharpness V=5 at Δ=6, order 12; Δ≤4 open | — | — | Numerical example (checked by an earlier reviewer) | computational | none | M |
| P5 | Prop. 5 (l.817–839): ceiling; 16 count vectors among 18 octanes; two collision pairs | Rada2019 Ex. 2.2; Rada2026 §3.1; Deutsch–Klavžar 2015 (M-polynomial); identical rows in the Barman–Das 2026 octane table (earlier audit) | Ceiling; octane ties implicit in published tables | Explicit pairs + SSE floor 2.925 °C² | known + computational | OPTIONAL: note that the pairs' equal values are visible in published octane tables (e.g.~\cite{BarmanDas2026HSO}) | H (Rada) / M (Barman–Das) |
| R8 | Remark l.848–858: Σm=n−1, Σ(1/i+1/j)m=n | Cruz–Rada eqs. (3)–(4) (credited) | Identities | Data ranks 7/8 | known + computational | none | H |
| P6 | Prop. 6 (l.863–890) + l.892: a.e. θ separates distinct counts; a.e. point is weakly discriminating on every class | RRS2022 Thm 3.1, 3.8; Rada2026 Thm 3, Cor. 2 | Point-wise sufficient criteria | a.e. version over the parameter space, inherited from the parent (stated) | adapted | none | H |
| E1 | Ex. 1 (l.896–908): LO(0,−½,1) separates the RRS Ex. 2.2 pair; D(1)≈0.2255 | RRS2022 Ex. 2.2 | Trees and difference vector | Separation | novel (small) | none | H |
| S4.2 | l.1010–1027: off-Π recovery at order 16 (3475/3476 → 4069) | — | — | Enumeration; not proved for larger n (stated) | computational | none | M |
| S4.3 | l.1029–1056 + Table 3: structure sensitivity on decanes; reproduces Barman–Das | Furtula–Gutman–Dehmer 2013; Barman–Das 2026 | Protocol and published values | New values for LO points | exploratory | none | M |
| P7 | Prop. 7 (l.1092–1123): P_n unique min, S_n unique max of LO(0,0,γ), γ>0 | Cruz–Rada Cor. 2.2/3.2 (bounds); Thm 2.1/3.1 (uniqueness); Gao–Gao 2024 (sufficient conditions, abstract); Rada2026 §4.2 (star half) | Bounds and conditions | Short direct proof; explicit bounds | known (credited) | none | H (Cruz–Rada) / M (Gao–Gao abstract) |
| Q1–Q4 | §6 (l.1125–1428): octane correlations, matched-budget ablation, nonane replication, boiling-point tests, ridge, Wiener | Ali et al. 2025 (parameter-optimised GM on octanes); Wiener 1947 | Fitted GM families on octanes | Pre-registered negative tests | exploratory | none (properly hedged) | n.a. |
| S10 | Supplement S10: per-graph identifiability (Prop. identrank), limits, closed forms, termwise bounds | Brown 1986 (rank); GM bounds literature (UNVERIFIED: Molina/Granados/Portilla); Carballosa et al. JMC 2023 (exponential-index inequalities, not cited in main) | Standard | Specialisations; Δ≤6 equality is computational | adapted / known | OPTIONAL: cite Carballosa et al. 2023 in S10 | L–M |

## 2. Cross-document consistency (novelty statements)

| Location | Statement | Agrees with main.tex? | Severity |
|---|---|---|---|
| Abstract l.203 vs intro l.322 / concl. l.1433 | Abstract: "By theorems of Rada", with no "equal order"; intro and conclusion say "for graphs of equal order" | Substantively yes (the proof removes the restriction) | OPTIONAL |
| Intro l.310 | "where the known results bind for chemical graphs", while the order-13 result concerns all trees | Minor mismatch | OPTIONAL |
| Remark l.655–656 | "pure-γ points ... attain the most possible", with EGA/EISDD (Rada Cor. 3.5) not mentioned | Incomplete credit | IMPORTANT |
| l.636 | "or of explicit colliding trees for degree-ratio indices" | Broader than the search supports; conflicts in spirit with l.666–673 (single-index failures at 9 and 10) | IMPORTANT |
| README l.107–109 | "a ratio-plane theorem stating exactly what the pure-γ line can discriminate ... with colliding trees at every order ≥ 13; a bound on γ-crossings; per-graph identifiability". No credit to Rada Thm 3.4/Prop. 2.5; omits order 16 for chemical trees; omits that minimality is computer-assisted | Over-claims relative to intro (i)/(ii) | IMPORTANT |
| README l.110–112 | "an apparent vaporization-enthalpy gain was an artefact of a search box that truncated the parent family" | Paper: gain "shrank to about zero in an exploratory rerun"; the wide-box analysis is not pre-registered (l.1482) | IMPORTANT |
| README l.113–114 | "ridge regression on the degree-pair counts is far stronger than any single index" | Paper: higher **point estimates**, not more accurate than Wiener's model on the decanes, small pooled margin, no interval (l.1423–1428) | IMPORTANT |
| README l.8, l.99–100 | Branch `review/match-figure-2026-10-20` @ c48bad0; "45 A5 pages", "Supplementary Material (27 pages)" | Stale (paper 37 pp, supplement 39 pp per the cover letter and commit message) | OPTIONAL (hygiene) |
| Cover letter l.17–41 | Main new results = where the ceiling binds (12/15, witnesses at 13/16, minimality computer-assisted, no ratio index separates all skeletons ≥16, ≤5 exchanges); Rada 2019 Thm 3.4/Prop. 2.5, Rada 2026 §3.1 and Cruz–Rada credited; Prop. 3 not claimed new | Agrees with abstract, intro and conclusion | — (add EGA/Cor. 3.5 credit if R3 is changed) |
| Conclusion l.1433–1447 | Matches intro (i)/(ii) | Agrees | — |
| REVIEWER_START_HERE l.106 | Absence claim pointed to the search log | Agrees | — |

## 3. Issues by severity

**BLOCKER.** None found. Every attribution to Rada, Cruz–Rada and RRS was checked against the primary text and matches the cited location. Credit is given at least once for each known theorem.

**IMPORTANT**
1. **Missing prior result (R3/T2ii).** Rada 2019 Cor. 3.5 already states that the exponential GA index has the discrimination property with respect to the m̂_GA-relation. Because the GA weight √(1−q²) is injective in q, that relation is exactly the equality of q-histograms. The same argument (Thm 3.4) covers e^{SDD} and e^{ISDD}, whose rational weights are injective in q. The manuscript cites EGA (l.644) and EISDD (l.647) only as indices that fail on the witnesses. It does not say that they also attain the q-histogram optimum. The fix is the replacements given in rows R3 and T2ii. A referee from the Rada school would notice this.
2. **Over-broad absence claim (R2, l.636).** Replace it with the narrowed wording given in row R2.
3. **README over-claims (§2).** README l.107–114 should be aligned with the paper:
   - OLD: "a ratio-plane theorem stating exactly what the pure-γ line can discriminate (edge-imbalance histograms), with colliding trees at every order ≥ 13" → NEW: "on the ratio plane the family sees only the histogram of edge imbalances; by Rada's theorem (MATCH 82 (2019), Thm 3.4) the pure-γ points separate exactly these histograms; by exhaustive enumeration the histogram determines the degree-pair counts of every tree up to order 12 (chemical trees: 15), with explicit colliding trees at every order ≥ 13 (≥ 16)".
   - OLD: "an apparent vaporization-enthalpy gain was an artefact of a search box that truncated the parent family" → NEW: "a vaporization-enthalpy gain that met a pre-registered seed-count rule shrank to about zero in an exploratory rerun with a search box that did not truncate the parent family".
   - OLD: "ridge regression on the degree-pair counts is far stronger than any single index" → NEW: "ridge regression on the degree-pair counts has higher point estimates than every single index evaluated (no interval reported), though not higher than Wiener's two-descriptor model on the decanes".

**OPTIONAL**
- Abstract l.203: "By theorems of Rada" → "By an argument of Rada".
- Intro l.310: "for chemical graphs" → "for trees and chemical trees".
- Add HSO~\cite{BarmanDas2026HSO} to the corollary list (l.644–650) and to the ratio-function list at l.287–289.
- Cite Brown 1986 at Theorem 1 (l.511); consider "Proposition" rather than "Theorem".
- Cite minimal-order precedents for other indices as context: Guo, Randić et al. 1999 (JJ-equivalent trees, order 18); Ivanciuc et al. 1993. Both are in the repository log and are UNVERIFIED in this pass.
- Mention Akbari et al., "Revisiting the diminished Sombor index", MATCH 96 (2026) 611–624, and Cheng et al., "On the degree-ratio Sombor index and graph energy", MATCH 97 (2027) 1251–1261. Both are verified on the MATCH contents pages, and both are degree-ratio-index papers not cited in the manuscript.
- Cite Carballosa et al., J. Math. Chem. 2023 (exponential-index inequalities) in S10.
- README hygiene: update the branch, commit and page counts.
- Intro l.276: Rada-inclusion clarification (earlier audit Fix 8).

## 4. Single index versus full histogram

The manuscript keeps these apart correctly. The 13/16 orders concern equality of the full q-histogram, which binds every degree-ratio index at once (Cor., Remark l.665–667). Single ratio indices can fail earlier through value coincidences: SDD at order 9 (both members are chemical trees), ISDD at 10, and GA merges distinct histograms at 17. The abstract and intro claims ("no degree-ratio index separates all skeletons of order 16 or more") are class-level and correct. The R2 rewording is needed so that the absence claim does not extend to single-index collisions, which the manuscript itself shows occur at order 9.
