# Reference audit: Loyola index paper (MATCH submission)

Date: 2026-10-20. Commit audited: `325bd05` (`main.tex`, `supplement.tex`; `LOYOLA_paper.pdf`, `LOYOLA_supplement.pdf`).
Read-only audit. Nothing in the repository was changed.

**Line-number caveat.** The worktree `wt-fig` has *uncommitted* edits to `main.tex` (abstract, around line 716, 1040, 1068, 1157, 1291 and 1705). The line numbers below are for the committed file (`git show 325bd05:main.tex`). After about line 1040, working-tree line numbers can be up to +3 higher.

**Method.**
- Reference numbers come from `pdftotext LOYOLA_paper.pdf`: [1]–[56], in the same order as the `\bibitem`s.
- Bibliographic data was checked against Crossref (`api.crossref.org`), arXiv, Semantic Scholar and OpenAlex.
- Content was checked against full texts wherever they could be obtained. Sixteen open-access MATCH PDFs were downloaded from `match.pmf.kg.ac.rs/electronic_versions/...` and read: Rada 2019, Rada 2026, Rada–Rodríguez–Sigarreta 2022, Cruz–Rada 2019, Song–Huang 2023, Réti et al. 2018, Hu et al. 2022, Gutman 2021, the Gutman 2026 survey, Barman–Das 2026, Movahedi et al. 2026, Nyauli–Buragohain 2026 and 2027, Gutman et al. 2027, Ali et al. 2027 and Shao–Jahanbani 2027. The other full texts read were AIMS Math (Molina 2025, Ali 2025), arXiv (Mityagin, Ediz, Mondal), the Euler–Sombor PDF and one NIST WebBook page.
- Springer, Elsevier, ACS and Wiley full texts were blocked. Where only a title or abstract could be seen, the verdict says so.
- "Secondary" means the claim was confirmed through a source I read that quotes the cited work, not through the cited work itself.

## Summary

| | count |
|---|---|
| Citation instances (key × line), main paper | 97 |
| SUPPORTED | 84 |
| PARTIALLY SUPPORTED | 7 |
| NOT SUPPORTED | 0 |
| NOT VERIFIABLE (content paywalled or unavailable) | 6 |
| Bibliography entries cited / uncited / missing / duplicates | 56 / 0 / 0 / 0 |
| Alphabetical-order violations, main | 0 |
| Substantive bibliographic errors, main | 0 (2 cosmetic items: NIST retrieval date, repository URL markup) |
| Supplement: entries / uncited / missing | 14 / 0 / 0 |
| Supplement: alphabetical-order violations | 2 ([5] KDB before [6] Konstantinova; [12] Rossini before [13] Reid) |

All 56 main entries exist and match the authoritative records: authors, title, journal, bold volume, year and pages.

Crossref differences that are **not** errors:
- online-first years, for example Das–Mondal 2023 online and 2024 in print;
- MATCH issue numbers placed in the volume field;
- the first page of Shao–Jahanbani given as 567 (the PDF prints 657–675);
- Crossref has no records for the older MATCH issues (79, 82); their PDFs confirm the citations.

## Main paper: per-reference table

Verdict codes: S = supported, P = partially supported, NS = not supported, NV = not verifiable.

| [n] | key | entry correct? | cited at (lines, 325bd05) | claim attributed | verdict | evidence / source | fix needed |
|---|---|---|---|---|---|---|---|
| 1 | Albertson1997 | yes (Ars Combin. **46** (1997) 219–225; DBLP) | 275 | Albertson irregularity, of which q is a normalised form | S (classical; secondary: cited for the irregularity index in the Euler–Sombor paper and in Nyauli–Buragohain 2027, ref. [2]) | pisrt.org Euler–Sombor PDF | none |
| 2 | AliGutmanFurtula2026BID | yes; Crossref 10.1007/s00010-026-01306-5, vol 100, art. 66 | 227 | survey of extremal results on BID indices | S (title) | Crossref | none |
| 3 | AliGutmanFurtulaAlbalahiHamza2025 | yes; 10.3934/math.2025311, 10 (2025) 6788–6804 | 248 | parameter-optimised GM versions fitted to octane properties | S: abstract says 13 octane properties; text says optimal (α,β) in [−3,3] | aimspress PDF math-10-03-311 | none |
| 4 | AliGutmanEtAl2027DRSO | yes; MATCH **97** (2027) 639–656, doi 10.46793/match.97-2.10926 | 646 | studies the degree-ratio Sombor index | S | MATCH PDF, abstract | none |
| 5 | Baker1975 | yes (CUP 1975, first edition) | 589, 692 | Lindemann–Weierstrass: e^{x_i} linearly independent over the algebraic numbers for distinct algebraic x_i | S (secondary: Rada 2019 states it as Theorem 3.3 and cites Baker [1]; standard result; the book itself was not viewed) | MATCH 82 p. 35 | none |
| 6 | BarmanDas2026HSO | yes; MATCH **95** (2026) 63–94, doi 10.46793/match95-1.03425 | 1137 | published decane-class SS/Abr values; implements the FGD protocol | S: Section "Smoothness"; Table 10 gives SS/Abr for octanes, nonanes and decanes | MATCH 95 pp. 84–86 | none |
| 7 | Besicovitch1940 | yes; J. London Math. Soc. **s1-15** (1940) 3–6, doi 10.1112/jlms/s1-15.1.3 | 1075, 1121 | Q-linear independence of k-th roots of distinct k-th-power-free integers | S (secondary: Rada–Rodríguez–Sigarreta 2022, Theorem 3.3, quotes Besicovitch as the independence of n-th roots of p1^m1…pk^mk with 0≤m_i<n, which is the same statement; original paywalled) | MATCH 87 p. 105 | none |
| 8 | BollobasErdos1998 | yes (Ars Combin. **50** (1998) 225–233; zbMATH 1602780 per prior check) | 224 | general Randić index | S (classical attribution) | zbMATH (prior check) | none |
| 9 | Brown1986 | yes; doi 10.1214/lnms/1215466757 | 811 | exponential-family language: minimal representation | NV (book not inspected; standard terminology) | Crossref | none |
| 10 | CarballosaQuintana…2023 | yes; JMC 61(5) 933–949, doi 10.1007/s10910-022-01446-4 | 1304 | inequalities between exponential indices | S (title; repository summary) | Crossref; e-archivo.uc3m.es | none |
| 11 | CruzMonsalveRada2020 | yes; DAM 283 (2020) 634–643, doi 10.1016/j.dam.2020.03.009 | 264 | extremal theory of exponential VDB indices | S: abstract says e^χ is maximised by the path among trees | Semantic Scholar abstract | none |
| 12 | CruzRada2019PathStar | yes; MATCH **82** (2019) 715–732 | 312, 1291 | extremal trees of the pure-γ points follow from their criteria; f(i,j)=ij/(i+j)(φ_ij+2φ12−3φ22); Theorem 2.1 gives the path bound, Theorem 3.1 the star bound | S: f and f(1,2)=f(2,2)=2(φ12−φ22) are on p. 717. Theorems 2.1 and 3.1 are the path and star *identities*; the bounds themselves are Corollaries 2.2 and 3.2 (non-strict). With strict f>f(1,2) the identities give uniqueness, as the text says | MATCH 82 pp. 717–727 | optional: "Theorem 2.1 (with Corollary 2.2)" and "Theorem 3.1 (Corollary 3.2)" |
| 13 | DasMondal2024ExpGA | yes; JMC 62(10) 2740–2760, doi 10.1007/s10910-023-01542-z | 266; 640 | 266: "published *one-parameter* exponential indices … place their parameter on a single classical generator"; 640: e^GA is a degree-ratio index | 266: P; 640: S | The abstract (SKKU repository) describes EGA as the exponential variant of GA, i.e. Σe^{GA weight}, with no tunable parameter. The GA weight depends only on the degree ratio, so 640 holds | reword 266 (Fix F1) |
| 14 | DasMondalRazaPal2025ExpISDD | yes; J. Appl. Math. Comput. 71 (Suppl. 1) 537–561, doi 10.1007/s12190-025-02461-9 | 266; 643 | as in [13]; ISDD and its exponential are ratio indices | 266: P; 643: S (title; ISDD weight ij/(i²+j²) is a ratio function) | Crossref | Fix F1 |
| 15 | DeutschKlavzar2015 | yes; Iran. J. Math. Chem. **6** (2015) 93–102, doi 10.22052/ijmc.2015.10106 | 917 | graphs with equal counts share the M-polynomial | S: abstract defines M(G;x,y)=Σ m_ij x^i y^j | Semantic Scholar abstract | none |
| 16 | FurtulaGutmanDehmer2013SS | yes; AMC 219 (2013) 8973–8978, doi 10.1016/j.amc.2013.03.072 | 1130, 1166 | SS/Abr criterion; similar structures by single-edge relocation (graph edit distance 2) | S (secondary: Barman–Das give FGD's algorithm with S(G)={Φ: GED(Φ,G)=2} and the SS/Abr formulas) | MATCH 95 pp. 84–85 | none |
| 17 | GaoAMC2024 | yes; AMC 472 (2024) #128634 | 264; 1291 | 264: extremal theory of exponential VDB indices; 1291: "general sufficient conditions for the path to be the unique minimal tree and the star the unique maximal tree" | 264: S (title); 1291: NV (abstract not accessible; ScienceDirect returns 403) | Crossref | check against the paper before submission |
| 18 | GranadosJMC2025GM | yes; JMC 63(2) 406–418 | 232, 1304 | GM bounds and QSPR literature; bounds at γ=0 known | S: abstract gives upper and lower bounds for GM and models polyaromatic hydrocarbons | Semantic Scholar abstract | none |
| 19 | Gutman2021Sombor | yes; MATCH **86** (2021) 11–16 | 225 | Sombor index | S | MATCH PDF | none |
| 20 | Gutman2026SomborSurvey | yes; MATCH **96** (2026) 819–837 | 225, 290 | survey of variants; "new variants hardly ever improve on earlier ones in applications" | S: Concluding remarks say better applicative properties are "hardly ever matched by facts" | MATCH 96 p. 834 | none |
| 21 | GutmanBuragohainNyauli2026 | yes; JMC 64(6) #39, doi 10.1007/s10910-026-01799-0 | 273, 644 | q (or the degree ratio) appears in degree-ratio indices; it is a degree-ratio index | NV (no abstract retrievable; title "Concealed relations between vertex-degree-based topological indices" does not show degree ratios) | Crossref | confirm the content (Fix F3) |
| 22 | GutmanMilovanovic2020AKCE | yes; AKCE 17(1) 74–85, doi 10.1016/j.akcej.2018.05.002 | 230, 362 | introduced M_{α,β} | S (secondary: Molina 2025 says "the Gutman–Milovanović index is defined in [16]", with [16] being this paper) | AIMS math-10-02-094 p. 1999 | none |
| 23 | GutmanRedzepovicBuragohainNyauli2027 | yes; MATCH **97** (2027) 165–174 | 646 | studies DRSO | S | MATCH PDF | none |
| 24 | GutmanRedzepovicKizilirmakKulli2025EU | yes; Open J. Math. Sci. 9 (2025) 141–148 | 268 | variable Euler–Sombor index weights the imbalance polynomially, without normalisation | S: d²+d²+λdd=(d_u−d_v)²+(λ+2)d_ud_v (Proposition 2 proof) | pisrt.org PDF | none |
| 25 | GutmanTrinajstic1972 | yes; CPL 17 (1972) 535–538 | 222 | Zagreb indices | S (classical; Rada 2019 Table 1 cites it for both Zagreb indices). Note: M2 is usually credited to Gutman et al. 1975 | — | optional |
| 26 | HuMATCH2022 | yes; MATCH **88** (2022) 505–520 | 264 | the extremal theory of Rada's *exponential* VDB indices is developed here | P: the paper treats a general edge-weight function f under monotonicity and convexity conditions, for graphs of given order and size. "Exponential" occurs only once, in a description of Cruz–Rada's earlier work | MATCH 88 pp. 505–507 | Fix F2 |
| 27 | Jameson2006 | yes; Math. Gaz. 90(518) 223–234 | 746 | Laguerre's extension of Descartes' rule to generalised polynomials | S (title and abstract; the detailed real-exponent statement was not viewed) | Crossref and OpenAlex abstract | none |
| 28 | Konstantinova1996Degeneracy | yes; JCICS 36 (1996) 54–57 | 1039 | "Degeneracy measures the failure to discriminate non-isomorphic graphs" | P: the abstract concerns the "discrimination ability" of distance and information indices on unbranched hexagonal systems. The term "degeneracy" and any formula could not be seen. The 100(1−k/N) convention is correctly presented as the authors' own | OpenAlex abstract | Fix F4 (optional) |
| 29 | LabaufGreenshieldsRossini1961 | yes; JCED 6(2) 261–263, doi 10.1021/je60010a023; Crossref byline "Abbas Labauf" | 1667 | NIST lists values "under Labbauf et al." (printed as Labauf) | S: NIST page for 2-methyloctane shows ΔvapH° 44.9 kJ/mol, "Reid, 1972", with "See also Labbauf, Greenshields, et al., 1961"; spelling handled correctly | webbook.nist.gov C3221612 | none (the counts 4 and 25 were not re-counted) |
| 30 | LinZhouWangMiao2022 | yes; AIMS Math 7 (2022) 25–38 | 275 | generalisation of Albertson irregularity | S (abstract) | Semantic Scholar | none |
| 31 | NISTWebBook | essentially yes; DOI 10.18434/T4D303 | 1545, 1667, 1707 | data source | S | NIST | cosmetic: NIST's recommended form has a retrieval date (Fix B1) |
| 32 | Mityagin2020 | yes; Math. Notes 107 (2020) 529–530 | 584, 951 | zero set of a nonzero real-analytic function has measure zero | S: Proposition 0 | arXiv 1512.07276 | none |
| 33 | MolinaSigarreta2025GM | yes; AIMS Math 10(2) 1998–2020 | 232, 236, 362, 1304 | GM bounds and QSPR literature; catalogue of special cases; GM family; γ=0 bounds | S: p. 2000 lists M_{0,1}, M_{1,0}, M_{−1/2,0}, 2M_{1/2,−1}, ½M_{−1/2,1}, M_{0,−1/2}, 2M_{0,−1}; p. 2008 ISI=M_{1,−1}; ^mM_2 via M_{α,0}. HM is not listed explicitly but is cited separately to [48] | AIMS PDF | none |
| 34 | MovahediGutmanRedzepovicFurtula2026 | yes; MATCH **95** (2026) 141–162 | 272; 640; 1524 | 272: "the ratio q_uv itself appears in the diminished Sombor index"; 640: DSO is a ratio index; 1524: octane benchmark | 272: P (DSO=Σ√(d_u²+d_v²)/(d_u+d_v)=Σ√((1+q²)/2); q appears only in their bounds, as \|d_u−d_v\|/(√2(d_u+d_v)), Theorems 3–4); 640: S; 1524: S (octane dataset, Section on chemical applicability) | MATCH 95 pp. 141, 146–147, 155 | Fix F3 |
| 35 | LoyolaRepo | yes (URL returns HTTP 200; it is the origin remote) | 632, 1830, 1891, 1893 | literature-search log; code; protocols; supplement | S (`audit/final/NOVELTY_SEARCH_LOG.md` and `LOYOLA_supplement.pdf` are present) | github.com/Singati2/LOYOLA-PAPER | cosmetic: wrap the URL in `\url{}` (Fix B2) |
| 36 | NyauliBuragohain2026CoRSO | yes; MATCH **96** (2026) 295–324 | 269 | cosine-rule Sombor indices weight the imbalance polynomially, without normalisation | S: √(d²+d²−2dd cosθ) | MATCH PDF abstract | none |
| 37 | NyauliBuragohain2027DRSO | yes; MATCH **97** (2027) 135–164 | 273; 644 | 273: q itself appears in degree-ratio indices; 644: degree-ratio indices | 273: P (DRSO uses d(u)/d(v), which is a function of q, not q itself); 644: S | MATCH 97 p. 135 | Fix F3 |
| 38 | PortillaJMC2025GM | yes; JMC 63(10) 2068–2087 | 232, 1304 | GM bounds and QSPR; γ=0 bounds known | NV (title only) | Crossref | confirm |
| 39 | Rada2019ExpVDB | yes; MATCH **82** (2019) 29–41 | 262, 278, 301, 632, 650, 1037, 1869, 1871 | exponential VDB indices (Definition 3.1); LW argument and Theorem 3.4; Example 2.6 (two trees on 29 vertices with different m̂_χ and equal Randić index); Proposition 2.5; "introduced … for their discriminating power **on trees**" | 262, 278, 301, 632, 650, 1871: S; 1869: S (wording: "Rada's Lindemann–Weierstrass theorem" can be read as attributing LW to Rada); 1037: P (Rada works over G_n, all graphs with n non-isolated vertices, not trees) | MATCH 82 pp. 33–37: Prop. 2.5 p. 34, Ex. 2.6 p. 35, Thm 3.4 p. 36 | Fixes F5, F6 |
| 40 | Rada2026LinearVDB | yes; MATCH **96** (2026) 841–863 | 228, 286, 537, 599, 632, 917, 983, 1291 | linear framework; every VDB index a linear functional on S_Δ (h=10 for Δ=4); no VDB index separates equal profiles and sufficient criteria for weak discrimination; pendant-path device; star condition (Section 4.2) holds, path condition fails | all S: Sections 2.1, 3.1 (pendant path, Fig. 1), Theorems 2–3, Corollary 2, Section 4.2 normal cones of S_n and P_n | MATCH 96 pp. 844–859 | none |
| 41 | RadaRodriguezSigarreta2022Weak | yes; MATCH **87** (2022) 97–108 | 632, 974, 992, 997 | definition of weak discrimination; several indices fail on chemical trees while SO succeeds; Example 2.2 (sum classes; χ and √(x+y) fail); m(S)−m(T)=6(1,3)+4(2,3)+4(3,3)−4(1,4)−6(2,2)−4(2,4), order 17+t | all S: recomputed from Example 2.2 (p. 101), which gives the difference and n=17+p exactly; Theorem 2.3 covers SO | MATCH 87 pp. 97–103 | none |
| 42 | RakicFurtula2019SS | yes; J. Chemom. 33 (2019) e3138 | 1131 | fingerprint-based variant | S (abstract) | Semantic Scholar | none |
| 43 | Randic1975 | yes; JACS 97 (1975) 6609–6615 | 222 | Randić index | S (classical) | Crossref | none |
| 44 | Reid1972 | yes; AIChE J. 18(6) 1278 (a book review; Crossref title "Handbook on vapor pressure … R. C. Wilhort [sic] and B. J. Zwolinski") | 1667 | NIST lists 25 values under Reid; it is a review of the handbook | S (nature of the item confirmed by Crossref; NIST attribution confirmed on one page) | Crossref 10.1002/aic.690180637; NIST | optional: add DOI |
| 45 | RetiSharafdini2018IRLA | yes; MATCH **79** (2018) 509–524 | 276 | IRLA(G)=2Σ\|d_u−d_v\|/(d_u+d_v) | S (Proposition 2, p. 516, rendered page viewed) | MATCH 79 p. 516 | none |
| 46 | APIProject44Circ461 | yes (NBS Circ. C461, 1947, per prior Open Library check) | 1546 | property audit source | S (relevance); data not checked | — | none |
| 47 | ShaoJahanbani2027 | yes; MATCH **97** (2027) 657–675 (Crossref's "567" is wrong) | 646 | studies DRSO | S (DRSO=Σ√(d_u⁴+d_v⁴)/(d_ud_v), a ratio function) | MATCH PDF p. 658 | none |
| 48 | ShirdelRezapourSayadi2013HM | yes; Iran. J. Math. Chem. 4 (2013) 213–220 | 238 | hyper-Zagreb HM=Σ(d_u+d_v)² | S (abstract) | Crossref/OpenAlex | none |
| 49 | Sigarreta2022ExpVDB | yes; MBE 19 (2022) 6985–6995 | 264 | extremal problems for exponential indices | S (abstract) | Semantic Scholar | none |
| 50 | SongHuang2023EDV | yes; MATCH **89** (2023) 343–370 | 632 | edge division vector; edge-additive eccentric indices (Wiener, Gutman) agree on EDV-equivalent trees; all such trees of order ≤10 determined | S (Definition 6.1, Theorem 6.1, Section 5, abstract) | MATCH 89 pp. 343–345, 364–366 | none (the authors' own (4,1,1) example was not rechecked) |
| 51 | VukicevicFurtula2009GA | yes; JMC 46 (2009) 1369–1376 | 244 | GA index | S (classical; Rada 2019 Table 1 cites it for GA) | — | none |
| 52 | VukicevicGasperov2010 | yes (Croat. Chem. Acta **83** (2010) 243–260; Hrčak per prior check) | 641 | SDD index | S (secondary: Adriatic indices source, as cited in Molina 2025 [40,41]) | — | none |
| 53 | Wiener1947 | yes; JACS 69 (1947) 17–20 | 1795 | two-descriptor model with path number W and p₃ = pairs three bonds apart | S: the scanned paper defines the path number w and the polarity number p as "the number of pairs of carbon atoms separated by three carbon–carbon bonds" | people.iup.edu scan of ja01193a005 | optional: say "path number w and polarity number p (our p₃)" |
| 54 | WilhoitZwolinski1971 | yes (TRC, Texas A&M Research Foundation, 1971; consistent with the Reid review title) | 1667 | the handbook reviewed by Reid | S | Crossref (Reid record) | none |
| 55 | ZhouTrinajstic2009sumconn | yes; JMC 46 (2009) 1252–1270 | 241 | sum-connectivity index | S (classical) | Crossref | none |
| 56 | ZhouTrinajstic2010 | yes; JMC 47 (2010) 210–218 | 224 | general sum-connectivity | S (classical) | Crossref | none |

### Theorem attributions flagged in the brief

| Attribution | Result |
|---|---|
| "Theorem 3.4 of Rada 2019", L632 | Correct. The LW-based discrimination is with respect to the m̂_φ relation for algebraic φ_ij. Applying it with φ_ij=γq_ij gives classes = q-classes for γ≠0. Small caveat: Rada states the theorem over G_n (fixed number of non-isolated vertices). The argument is order-free |
| Proposition 2.5 of Rada 2019, L650 and L1871 | Correct as an application. Prop. 2.5 is the general "m̂_φ equal ⇒ φ equal". For weights depending only on the ratio, the classes are unions of q-classes |
| Example 2.6 of Rada 2019, L632 | Correct: T, T′ ∈ G_29; m̂_χ(T)=(12,12,4) vs (10,2,16) on (1,2),(1,4)/(2,2),(2,4)/(4,4); χ equal |
| Besicovitch 1940 | Correct statement (seen via the RRS 2022 quote) |
| Lindemann–Weierstrass, Baker | Correct statement (Rada 2019, Theorem 3.3, cites Baker) |
| Gutman–Milovanović index | Correctly credited (Molina 2025 credits [16] = Gutman–Milovanović–Milovanović 2020) |
| Degree-ratio Sombor index | Correct: Nyauli–Buragohain 2027 introduce it; Gutman et al. 2027, Ali et al. 2027 and Shao–Jahanbani 2027 study it |
| Song & Huang | Correct |
| Konstantinova 1996 degeneracy | Weakly supported: P, see Fix F4 |
| Rada 2019 exponential VDB indices | Correct, except "on trees" (L1037) |
| Cruz–Monsalve–Rada | Correct |
| Wiener 1947, W and p₃ | Correct |
| NIST WebBook citation | Correct; add a retrieval date |
| Labauf/Labbauf naming | Correct: Crossref and the ACS byline "Abbas Labauf"; NIST "Labbauf"; the text keeps both |

## Supplement references (14; numbered as printed in LOYOLA_supplement.pdf)

| [n] | key | entry correct? | cited at (supplement.tex lines) | claim | verdict | evidence | fix |
|---|---|---|---|---|---|---|---|
| 1 | BarmanDas2026HSO | yes | 810 | decane control values for the seven common indices | S | MATCH 95 Table 10 | none |
| 2 | Chemeo | web resource, no access date | 188 | KDB values consulted through Chéméo | S (relevance) | — | add access date |
| 3 | Ediz2017Octane | yes; arXiv:1701.02859, S. Ediz, 2017 | 188, 225, 913, 917, 927, 946 | octane set: TMB acentric factor 0.255; 2,3,3-TMP S=102.10; n-octane 111.70 | S: Ediz Table rows give TMB AcenFac 0.25529, 2,3,3-TMP 102.10, n-octane 111.70 | arXiv PDF | none |
| 4 | FurtulaGutmanDehmer2013SS | yes | 792, 818 | SS/Abr criterion; SS large and Abr small are desirable | S (secondary, Barman–Das p. 85) | — | none |
| 5 | KDB | no URL, no access date | 188 | acentric factors | S (relevance) | — | add URL (cheric.org/research/kdb) and access date; **out of alphabetical order** (Fix S1) |
| 6 | Konstantinova1996Degeneracy | yes | 687 | as main L1039 | P | as main | Fix F4 |
| 7 | LabaufGreenshieldsRossini1961 | yes | 584 | short paper covering all 35 nonanes and 75 decanes | S (title) | Crossref | none |
| 8 | NISTWebBook | as main | 186, 568 | data source | S | — | Fix B1 |
| 9 | MondalDePal2019QSPR | yes (Mondal, Dey, De, Pal, Complex Intell. Syst. 7 (2021) 977–996, doi 10.1007/s40747-020-00262-0; arXiv 1906.06660 lists Mondal, De, Pal) | 912 | 2,3,3-trimethylpentane S=102.06 in their octane dataset | S (arXiv table row) | arXiv PDF | key name only (cosmetic) |
| 10 | MovahediGutmanRedzepovicFurtula2026 | yes | 190 | same five octane properties as benchmark | S (they use T_B, ΔH_f, ΔH_vap, …) | MATCH 95 p. 155 | none |
| 11 | RakicFurtula2019SS | yes | 793 | fingerprint variant | S | abstract | none |
| 12 | APIProject44Circ461 | yes | 903, 928 | gas-phase entropies; Ediz's ΔH_vap column follows the 1947 tables | S (relevance; not checked against the tables) | — | **order** (Fix S1) |
| 13 | Reid1972 | yes | 585 | review of the handbook; NIST lists 25 values as Reid | S | NIST | — |
| 14 | WilhoitZwolinski1971 | yes | 585 | handbook | S | — | none |

## Fixes needed

Citation and support fixes. Line numbers are for `325bd05`.

**F1 (L266), "one-parameter" exponential indices.**
- Current: `Published one-parameter exponential indices~\cite{DasMondal2024ExpGA, DasMondalRazaPal2025ExpISDD} place their parameter on a single classical generator.`
- Proposed: `Published exponential indices~\cite{DasMondal2024ExpGA, DasMondalRazaPal2025ExpISDD} exponentiate the edge weight of a single classical index and carry no free parameter.`
- If the authors have checked that these papers do contain a scaling parameter, keep the original wording and cite the equation number.

**F2 (L262–264), Hu et al. is not an exponential-index paper.**
- Current: `whose extremal theory is developed in~\cite{CruzMonsalveRada2020, Sigarreta2022ExpVDB, GaoAMC2024, HuMATCH2022}.`
- Proposed: `whose extremal theory is developed in~\cite{CruzMonsalveRada2020, Sigarreta2022ExpVDB, GaoAMC2024}; extremal graphs for indices with a general degree-based edge-weight function are studied in~\cite{HuMATCH2022}.`

**F3 (L271–273), "q itself appears".**
- Current: `The ratio $q_{uv}$ itself appears in the diminished Sombor index~\cite{MovahediGutmanRedzepovicFurtula2026}, in degree-ratio indices~\cite{NyauliBuragohain2027DRSO, GutmanBuragohainNyauli2026}, and, as a normalised form …`
- Proposed: `Functions of $q_{uv}$ appear in the diminished Sombor index, whose edge weight is $\sqrt{(1+q_{uv}^2)/2}$ and whose bounds involve $|d_u-d_v|/(d_u+d_v)$~\cite{MovahediGutmanRedzepovicFurtula2026}, in the degree-ratio indices~\cite{NyauliBuragohain2027DRSO, GutmanBuragohainNyauli2026}, which depend on $d_u/d_v$, and, as a normalised form …`
- GutmanBuragohainNyauli2026 could not be checked. Confirm that it concerns degree-ratio indices; if it does not, drop it from L273 and L644.

**F4 (L1039; supplement L687), Konstantinova "degeneracy" (optional, low risk).**
- Current: `Degeneracy~\cite{Konstantinova1996Degeneracy} measures the failure to discriminate non-isomorphic graphs`
- Proposed: `Degeneracy, the failure of an index to discriminate non-isomorphic graphs (the converse of the discrimination ability studied in~\cite{Konstantinova1996Degeneracy}), is quantified here …`
- Alternatively, cite the page where Konstantinova defines her measure.

**F5 (L1037), "on trees".**
- Current: `Exponential indices of this type were introduced by Rada~\cite{Rada2019ExpVDB} for their discriminating power on trees.`
- Proposed: `Exponential indices of this type were introduced by Rada~\cite{Rada2019ExpVDB} for their discriminating power on graphs with a given number of non-isolated vertices.`

**F6 (L1869), wording.**
- Current: `by Rada's Lindemann--Weierstrass theorem~\cite[Theorem~3.4]{Rada2019ExpVDB}`
- Proposed: `by Rada's theorem based on the Lindemann--Weierstrass theorem~\cite[Theorem~3.4]{Rada2019ExpVDB}`
- Line 301 ("Rada's Lindemann–Weierstrass argument") is fine.

**F7 (L1291, optional precision).**
- Current: `Theorem~2.1 of~\cite{CruzRada2019PathStar} then gives the lower bound … and their Theorem~3.1 gives the upper bound`
- Proposed: `Theorem~2.1 of~\cite{CruzRada2019PathStar} (cf. their Corollary~2.2) then gives … and their Theorem~3.1 (cf. Corollary~3.2) gives …`
- Before submission, check the Gao–Gao characterisation in the same paragraph against the paper (NV).

**F8 (L1795, optional).**
- Current: `with the path number $W$ and the number $p_3$ of carbon pairs three bonds apart`
- Proposed: `with the path number $W$ and the polarity number $p_3$ (Wiener's $p$), the number of carbon pairs three bonds apart`

Bibliographic fixes:

**B1 (NIST, main [31] and supplement [8]).**
- Current: `… National Institute of Standards and Technology, Gaithersburg, 2025, \url{https://doi.org/10.18434/T4D303}.`
- Proposed: `… National Institute of Standards and Technology, Gaithersburg, \url{https://doi.org/10.18434/T4D303} (retrieved <date range of downloads>).`

**B2 (LoyolaRepo [35]).**
- Current: `https://github.com/Singati2/LOYOLA-PAPER (2026).`
- Proposed: `\url{https://github.com/Singati2/LOYOLA-PAPER} (2026).`

**S1 (supplement order).**
- Move `KDB` ("Korea …") after `Konstantinova1996Degeneracy`.
- Move `APIProject44Circ461` (Rossini) after `Reid1972`.
- Resulting order: Barman, Chéméo, Ediz, Furtula, Konstantinova, Korea KDB, Labauf, Linstrom, Mondal, Movahedi, Rakić, Reid, Rossini, Wilhoit.

**S2 (supplement KDB/Chéméo).** Add a URL and access date to KDB, and an access date to Chéméo.

Not errors (no action needed): the Crossref differences listed in the summary, and "Labauf" in the bibliography with "Labbauf" in the NIST quote.


---
## Integration note (2026-10-20)

Applied: Hu et al. 2022 cited for general edge weights; exponential indices of Das-Mondal described as exponentiating one classical generator (no parameter claim); "Functions of the ratio q" for the diminished Sombor and degree-ratio indices; Rada 2019 "who studied their discriminating power" (not "on trees"); "Rada's theorem based on the Lindemann-Weierstrass theorem"; Cruz-Rada Theorems and Corollaries 2.1/2.2 and 3.1/3.2; Wiener's polarity number named; repository URL in \url{}; supplement bibliography reordered (Konstantinova before KDB, Reid before Rossini). Not changed: NIST year (retrieval date unknown; AUTHOR to supply), Konstantinova "degeneracy" (paywalled, NOT VERIFIABLE), the four NOT VERIFIABLE items (author to confirm from the full texts), KDB/Chemeo access dates (author).
