# References, citation support, overlap and ethics: Loyola paper (MATCH)

> **Status (2026-10-23).** This report audits commit `3904e38`; line numbers refer to that commit. Items marked as applied are in `audit/MATCH_PATCH_LOG_2026-10-23.md`. Local full texts used for checking are private copies outside the repository and are not distributed. Discovery tools were used only to find sources; each claim was checked in the source itself.

Audited: worktree `wt-lit`, branch `review/match-literature-writing-audit-2026-10-23`, commit `3904e38`. Files: `main.tex` (1741 lines, 54 `\bibitem`), `supplement.tex` (1757 lines, 21 `\bibitem`). Read-only; nothing in any worktree was changed. Line numbers are for `3904e38`.

**Sources used.**
- Crossref (`api.crossref.org`, bibliographic query and DOI lookup) for all 75 entries.
- OpenAlex, zbMATH (Albertson; Bollobás–Erdős by OpenAlex) and the arXiv API (Ediz; Mondal).
- MATCH contents pages (`content{79n2,82n1,82n3,86n1,87n1,88n3,89n2,95n1,96n1,96n3,97n1,97n2}.htm`), fetched 2026-10-23.
- Local full texts, which are private and were not copied anywhere:
  - Rada 2019 (`match82n1_29-41.txt`)
  - Cruz–Rada 2019 (`match82n3_715-732.txt`)
  - Rada–Rodríguez–Sigarreta 2022 (`match87n1_97-108.txt`)
  - Gutman survey 2026 (`match96n3_819-837.txt`)
  - Rada 2026 (`rada2026.txt`, identical in content to `match96n3_841-863.txt`)
  - Nyauli–Buragohain 2027, Gutman et al. 2027, Kırgız 2027 (`match97n1_*`)
  - Ali et al. 2025 (`dl_ali/ali.txt`)
  - Jameson 2006, the author's copy (maths.lancs.ac.uk/jameson/zeros.pdf, saved in `litaudit/dl/`, outside the repo)
- Gao–Gao (ScienceDirect) and Gutman–Buragohain–Nyauli (Springer) returned 403 or an authentication redirect, and no abstract exists in Crossref, OpenAlex or Semantic Scholar. Both are NOT VERIFIABLE.
- Prior audits reused: `docs/match/13_REFERENCE_AUDIT.md` (commit `325bd05`, 56 entries) and `audit/MATCH_FORMAT_AND_REFERENCE_CHECK.md`. Where a verdict below rests only on the prior audit, the evidence column says "prior audit".

## 1. Bibliographic verification

### 1a. Integrity checks

| Check | main.tex | supplement.tex |
|---|---|---|
| `\bibitem` count | 54 | 21 |
| cited keys without a bibitem / bibitems never cited | 0 / 0 | 0 / 0 |
| duplicate keys | 0 | 0 |
| alphabetical order (MATCH: "listed in alphabetical order") | OK. Checked: Ali ×3 (shorter author list first), Cruz–Monsalve < Cruz–Rada, Das K. C. < Das P., Lin < Linstrom (key NISTWebBook), Movahedi < Natarajan (LoyolaRepo) < Nyauli, Rada < Rada–Rodríguez, Rakić < Randić, Reid < Réti < Rossini | OK. The prior S1 violations (KDB/Konstantinova, Rossini/Reid) are fixed: Konstantinova < Korea, Reid < Rossini |
| `\cite` lines in main body | 71 lines; 97+ key instances | — |

### 1b. Changes since 13_REFERENCE_AUDIT (`325bd05` → `3904e38`)

| Change | Status |
|---|---|
| `Brown1986` and `CarballosaQuintanaRodriguezSigarreta2023` moved from main to supplement (main 56 → 54) | correct. Main no longer cites them; supplement cites them at L1201 and L1345 |
| `LoyolaRepo` URL now wrapped in `\url{}` (prior fix B2) | done |
| Supplement now also lists GranadosJMC2025GM, MolinaSigarreta2025GM, PortillaJMC2025GM, LoyolaRepo and Wiener1947 (14 → 21); order fixed (prior S1) | done, in order |
| Prior fixes F1, F2, F3, F6, F7 and F8 | applied. F5 ("on trees"): the sentence was removed |
| Prior B1 (NIST retrieval date), KDB/Chéméo access dates, F4 (Konstantinova) | **still open** |

### 1c. Per-entry verification (main; the supplement shares 16 of these entries, with identical text)

All 54 main and 21 supplement entries exist. Authors, year, title, journal, bold volume and pages agree with the authoritative record. **No substantive mismatch was found.** Differences in the authoritative records that are not errors:
- Crossref gives online-first years, for example Das–Mondal 2023 (print 2024), Zhou–Trinajstić 2009 (print 2010), the MATCH 97 papers 2026 (volume year 2027), Song–Huang 2022 (2023), RRS 2021 (2022) and Barman–Das and Movahedi 2025 (2026).
- Crossref swaps issue and volume for MATCH 96 and 97 records.
- Crossref gives the first page of Shao–Jahanbani as "567". The MATCH contents page says 657–675, and the paper is right.
- Crossref's title for Gutman–Trinajstić reads "φ-electron", an OCR error. The paper's "π" is correct.
- Crossref spells Reid's review title "Wilhort", a Crossref typo.

| Key | Verified against | Notes |
|---|---|---|
| Albertson1997 | zbMATH: Ars Comb. 46, 219–225 (1997) | ✓ |
| AliGutmanFurtula2026BID | Crossref 10.1007/s00010-026-01306-5, vol. 100, art. 66 | ✓ |
| AliGutmanFurtulaAlbalahiHamza2025 | Crossref 10.3934/math.2025311; local PDF | ✓ |
| AliGutmanEtAl2027DRSO | Crossref 10.46793/match.97-2.10926 (7 authors); MATCH 97(2) contents pp. 639–656 | ✓ |
| Baker1975 | Crossref review 10.2307/3616894 (CUP 1975) | ✓. Rada 2019 cites the 1990 printing; either is fine |
| BarmanDas2026HSO | Crossref; MATCH 95(1) 63–94 | ✓ |
| Besicovitch1940 | Crossref 10.1112/jlms/s1-15.1.3 | ✓ ("s1-15" printed as 15, normal practice) |
| BollobasErdos1998 | OpenAlex: Ars Combin. 50, 225–233 | ✓ |
| CruzMonsalveRada2020 | Crossref 10.1016/j.dam.2020.03.009 | ✓ |
| CruzRada2019PathStar | local PDF header; MATCH 82(3) contents 715–732 | ✓ |
| DasMondal2024ExpGA | Crossref, 62(10) 2740–2760 | ✓ |
| DasMondalRazaPal2025ExpISDD | Crossref, 71 S1 537–561 | ✓ |
| DeutschKlavzar2015 | OpenAlex: IJMC 6(2) 93–102 | ✓ |
| FurtulaGutmanDehmer2013SS | Crossref 10.1016/j.amc.2013.03.072 | ✓ |
| GaoAMC2024 | Crossref 10.1016/j.amc.2024.128634 | ✓ (bibliographic data only) |
| GranadosJMC2025GM | Crossref 10.1007/s10910-024-01677-7, 63(2) 406–418 | ✓ |
| Gutman2021Sombor | MATCH 86(1) contents pp. 11–16 | ✓ |
| Gutman2026SomborSurvey | Crossref; local PDF | ✓ |
| GutmanBuragohainNyauli2026 | Crossref 10.1007/s10910-026-01799-0, 64(6) art. 39 | ✓ (bibliographic data only) |
| GutmanMilovanovic2020AKCE | Crossref 10.1016/j.akcej.2018.05.002 | ✓ |
| GutmanRedzepovicBuragohainNyauli2027 | Crossref; MATCH 97(1) 165–174; local PDF | ✓ |
| GutmanRedzepovicKizilirmakKulli2025EU | Crossref 10.30538/oms2025.0249 | ✓ |
| GutmanTrinajstic1972 | Crossref 10.1016/0009-2614(72)85099-1 | ✓ |
| HuMATCH2022 | Crossref; MATCH 88(3) 505–520 | ✓ |
| Jameson2006 | Crossref 10.1017/s0025557200179628, 90(518) | ✓ |
| Konstantinova1996Degeneracy | Crossref 10.1021/ci9502461 | ✓ |
| LabaufGreenshieldsRossini1961 | Crossref 10.1021/je60010a023 | ✓ |
| LinZhouWangMiao2022 | Crossref 10.3934/math.2022002 | ✓ |
| NISTWebBook | DOI 10.18434/T4D303 | ✓ The year "2025" has no retrieval date; see O2 |
| Mityagin2020 | Crossref 10.1134/s0001434620030189 | ✓ |
| MolinaSigarreta2025GM | Crossref 10.3934/math.2025094; authors Molina, Rodríguez-García, Sigarreta, Torralbas Fitz | ✓ |
| MovahediGutmanRedzepovicFurtula2026 | Crossref; MATCH 95(1) 141–162 | ✓ |
| LoyolaRepo | github.com/Singati2/LOYOLA-PAPER returns HTTP 200 | ✓ exists. Not pinned to a commit; see I2 and B1 |
| NyauliBuragohain2026CoRSO | Crossref; MATCH 96(1) 295–324 | ✓ |
| NyauliBuragohain2027DRSO | Crossref; MATCH 97(1) 135–164; local PDF | ✓ |
| PortillaJMC2025GM | Crossref 10.1007/s10910-025-01753-6 | ✓ |
| Rada2019ExpVDB | local PDF; MATCH 82(1) contents 29–41 | ✓ |
| Rada2026LinearVDB | Crossref; local PDF; MATCH 96(3) 841–863 | ✓ |
| RadaRodriguezSigarreta2022Weak | Crossref 10.46793/match.87-1.097r; local PDF | ✓ |
| RakicFurtula2019SS | Crossref 10.1002/cem.3138 | ✓ |
| Randic1975 | Crossref 10.1021/ja00856a001 | ✓ |
| Reid1972 | Crossref 10.1002/aic.690180637 (book review) | ✓ |
| RetiSharafdini2018IRLA | MATCH 79(2) contents pp. 509–524 | ✓ |
| APIProject44Circ461 | Crossref 10.6028/nbs.circ.461; the same 8 authors | ✓ |
| ShaoJahanbani2027 | MATCH 97(2) contents pp. 657–675 | ✓ |
| ShirdelRezapourSayadi2013HM | OpenAlex 10.22052/ijmc.2013.5294, 4(2) 213–220 | ✓ |
| Sigarreta2022ExpVDB | Crossref 10.3934/mbe.2022329 | ✓ |
| SongHuang2023EDV | Crossref; MATCH 89(2) 343–370 | ✓ |
| VukicevicFurtula2009GA | Crossref 10.1007/s10910-009-9520-x | ✓ |
| VukicevicGasperov2010 | OpenAlex: CCA 83(3) 243–260 | ✓ |
| Wiener1947 | Crossref 10.1021/ja01193a005 | ✓ |
| WilhoitZwolinski1971 | subject of the Reid review (Crossref) | ✓ |
| ZhouTrinajstic2009sumconn | Crossref 10.1007/s10910-008-9515-z | ✓ |
| ZhouTrinajstic2010 | Crossref 10.1007/s10910-009-9542-4 | ✓ |

Supplement-only entries:

| Key | Verified against | Notes |
|---|---|---|
| Brown1986 | Crossref 10.1214/lnms/1215466757 | ✓ |
| CarballosaQuintanaRodriguezSigarreta2023 | Crossref 10.1007/s10910-022-01446-4, 61(5) 933–949 | ✓ |
| Chemeo | web resource | no access date (O3) |
| Ediz2017Octane | arXiv 1701.02859: S. Ediz, title matches | ✓ |
| KDB | web database | no URL, no access date (O3) |
| MondalDePal2019QSPR | Crossref 10.1007/s40747-020-00262-0: Mondal, Dey, De, Pal, CIS 7(2) 977–996 (2021) | ✓. The entry correctly lists 4 authors; the arXiv version lists 3. The key name is cosmetic |

## 2. Citation-to-claim (main.tex)

Verdicts: S = supported, P = partial, NS = not supported, NV = not verifiable.

| Line(s) | Key(s) | Claim (short) | Verdict | Evidence |
|---|---|---|---|---|
| 225 | Rada2026 | graphs with equal counts are never separated by a VDB index | S | Rada 2026 §3.1, p. 849 |
| 225–228 | Rada2019, RRS2022, Rada2026 | for Δ≤4 every BID index is a linear functional of the ten counts; this representation is used in Rada 2019 and RRS 2022 and developed in Rada 2026 | S | Rada 2019 eqs. (1)–(2), p. 31. RRS eqs. (1)–(2), p. 99 (h=Δ(Δ+1)/2). Rada 2026 §2.1, p. 845 (h=Δ(Δ+1)/2=10) |
| 237–240 | Randic1975, GutmanTrinajstic1972, BollobasErdos1998, ZhouTrinajstic2010, Gutman2021 | classical indices | S (classical) | Rada 2019 Table 1 credits [10]=Gutman–Trinajstić for both Zagreb indices. M₂ is often credited to Gutman et al. 1975 (O5) |
| 240 | Gutman2026 | many Sombor variants, surveyed | S | survey, whole paper |
| 242 | AliGutmanFurtula2026BID | survey of extremal results on BID indices | S (title) | Crossref |
| 245–247 | GutmanMilovanovic2020; Granados, Molina, Portilla | GM family introduced; bounds and QSPR literature | S, except Portilla: NV beyond its title | prior audit (Molina p. 1999); Granados abstract. Portilla: title only |
| 251–259 | Molina, Shirdel, ZhouTrinajstic2009, VukicevicFurtula2009 | catalogue of special cases | S | prior audit (Molina p. 2000, 2008); not re-read |
| 263 | Ali 2025 | parameter-optimised versions fitted to octane properties | S | Ali 2025 abstract and p. 6790 ("13 properties of octane isomers … −3≤α≤3") |
| 277 | Rada2019 | LO is a subfamily of Rada's exponential VDB indices | S | Def. 3.1, p. 35 |
| 279–280 | CruzMonsalveRada, Sigarreta2022, GaoAMC2024; HuMATCH2022 | extremal theory of exponential indices; general edge weights | S (Gao: title only) | prior audit; Hu: general f |
| 282 | Das–Mondal; Das et al. | exponentiate a single classical generator | S | prior audit (abstracts) |
| 284–285 | Euler–Sombor; cosine-rule Sombor | imbalance weighted polynomially, not normalised | S | prior audit |
| 288 | Movahedi 2026 | functions of q appear in DSO | S | DSO weight √(d_u²+d_v²)/(d_u+d_v) = √((1+q²)/2) (algebra checked) |
| 289, 648 | NyauliBuragohain2027; **GutmanBuragohainNyauli2026** | degree-ratio indices | Nyauli: S (abstract p. 135, DRSO = Σ√((d_u/d_v)²+(d_v/d_u)²)). **GBN: NV** | GBN: no abstract obtainable; the title "Concealed relations…" does not show degree ratios |
| 291–292 | Albertson, Lin; Réti | normalised Albertson irregularity; IRLA = 2Σq | S | prior audit (Réti Prop. 2, p. 516) |
| 294 | Rada2019 | LO(0,0,γ) is the exponential index of γq | S | Def. 3.1 |
| 305 | Gutman2026 | new variants hardly ever improve on earlier ones in applications | S | survey §3 Concluding Remarks, p. 834: expectations of better applicative properties "are hardly ever matched by facts" |
| 323 | Rada2019 Thm 3.4, Prop. 2.5 | for graphs of equal order, separation of q-histograms at algebraic γ≠0 is Thm 3.4 applied to γq_ij; that no degree-ratio index separates more is Prop. 2.5 | S | Thm 3.4, p. 36: φ_ij algebraic ⇒ e^φ discriminates m̂_φ-classes on G_n, the graphs with n non-isolated vertices. Prop. 2.5, p. 34: m̂_φ equal ⇒ φ equal. The order restriction is stated correctly here |
| abstract 206–209 | (no \cite) | "By theorems of Rada, the points … separate exactly the histograms" | P (wording) | Thm 3.4 is on G_n only. The paper's own proof removes the restriction (L632); the abstract omits the qualifier. See O1 |
| 330, 1118 | CruzRada2019 | extremal trees follow from their criteria; f(i,j); f(1,2)=f(2,2)=2(E−1); Cor. 2.2 gives the lower bound and Cor. 3.2 the upper; the corollaries have no equality cases; uniqueness follows from the identities of Thms 2.1 and 3.1 | S | f and f(1,2)=f(2,2)=2(φ12−φ22), p. 718. Thm 2.1 identity, p. 718. Cor. 2.2 (part 2 = min ⇒ ≥ φ(P_n)), p. 719. Thm 3.1 identity (8) and Cor. 3.2 (part 1), pp. 725–726. Both corollaries are non-strict, as the text says. Strict f > f(1,2) in the identity gives uniqueness (checked) |
| 332, 599, 632 | Rada2026 §3.1 | degree-pair ceiling; pendant-path device for edge-type vectors | S | §3.1, p. 849: "By attaching the same pendent path to both trees…"; Fig. 1 |
| 399 | GM, Molina | LO(·,·,0) = M_{α,β} | S | definition |
| 536–539 | Rada2019, Rada2026; RRS2022, Rada2026 | equal profiles give equal values; sufficient linear criteria for separating profiles at fixed order | S | Prop. 2.5 / §3.1. RRS Thm 3.1; Rada 2026 Def. 1 and Thm 2, pp. 850–851 |
| 584, 869 | Mityagin2020 | zero set of a nonzero real-analytic function has measure zero | S | prior audit (Prop. 0, arXiv) |
| 589, 702 | Baker1975 | Lindemann–Weierstrass: e^{x_i} linearly independent over the algebraic numbers | S (via secondary source) | Rada 2019 Thm 3.3, p. 36, citing Baker; RRS Thm 3.7 |
| 632 | Rada2019, Rada2026, RRS Ex. 2.2 | Thm 3.4 for equal order; the proof does not need the order restriction; the pendant-path device; parallel to RRS Ex. 2.2 (classes of equal sum) | S | RRS Ex. 2.2, p. 102: φ(1,3)=φ(2,2) etc. for sum-only indices |
| 634 | SongHuang2023 | edge division vector; trees of order ≤10 determined | S | prior audit (pp. 343–345, 364–366). The (4,1,1) example was not rechecked |
| 634 | Rada2019 Ex. 2.6; RRS Ex. 2.1 | equal Randić index, different class counts; 29 vertices; infinite chemical family | S | Ex. 2.6, p. 35: T, T′ ∈ G_29, m̂_χ = (12,12,4) vs (10,2,16). RRS Ex. 2.1, p. 100: order 20p+9, m(S)≠m(T); m̂_χ also differs ((1,2): 8p+4 vs 6p+4) |
| 636 | LoyolaRepo | literature search recorded; enumeration code | S | `audit/final/NOVELTY_SEARCH_LOG.md` present at 3904e38 |
| 644–650 | Das–Mondal, Movahedi, Vukičević–Gašperov, Das et al., Nyauli, GBN, Gutman 2027, Ali 2027, Shao | these are degree-ratio indices | S, except GBN NV | the GA, SDD, ISDD and DSO weights are functions of d_u/d_v. Gutman 2027 p. 165 and Ali 2027 study DRSO |
| 654, 1437 | Rada2019 Prop. 2.5 | structure observation applied to weights depending only on the ratio | S | p. 34. For ratio-only φ, the q-classes refine the φ-classes |
| 676 | Rada2019 Thm 3.4 | the argument extends to algebraic coefficients | S | proof of Thm 3.4 uses integer coefficients and Thm 3.3 (independence over A), so algebraic coefficients work |
| 756 | Jameson2006 | Laguerre's extension: zeros (with multiplicity) ≤ sign changes V, same parity | S | Jameson Thm 3.1 (Z(F) ≤ S), Prop. 3.6 (S − Z even), zeros counted with order (§2). Recommend citing these numbers (O4) |
| 835 | Rada2026; DeutschKlavzar2015 | every VDB index is a function of the counts; equal counts mean equal M-polynomial | S | Rada 2026 §2.1; DK definition M(G;x,y)=Σ m_ij x^i y^j (prior audit) |
| 852 | CruzRada eqs. (3)–(4) | Σ(1/i+1/j) m_ij = n; Σ m_ij = n−1 | S | p. 718, eqs. (3) and (4) |
| 892 | RRS Thms 3.1 and 3.8; Rada2026 Thm 3, Cor. 2 | Z-independent weights, e.g. exponentials of distinct algebraic numbers, are weakly discriminating; support-restricted versions | S | RRS pp. 105–107; Rada 2026 pp. 852–853 |
| 894, 898 | RRS Ex. 2.2 | χ and M_{0,1/2} are not weakly discriminating on chemical trees; m(S)−m(T)=6(1,3)+4(2,3)+4(3,3)−4(1,4)−6(2,2)−4(2,4); order 17+t | S | p. 102: the √(x+y) and 1/√(x+y) rows; counts give the difference exactly; edges 16+p, so n=17+p |
| 939 | Konstantinova1996 | "Degeneracy measures the failure to discriminate non-isomorphic graphs" | P / NV | paywalled; abstract is about "discrimination ability". Prior F4 not applied (I5) |
| 977, 1023 | Besicovitch1940 | ℚ-independence of k-th roots of distinct k-th-power-free integers | S (via secondary source) | RRS Thm 3.3, p. 105, quoting Besicovitch |
| 1032–1039, 1062 | Furtula 2013; Rakić 2019; Barman–Das 2026 | SS/Abr protocol; fingerprint variant; published decane values | S | prior audit (Barman–Das pp. 84–86) |
| 1118 | Rada2026 §4.2 | the star condition holds; the path condition fails because e^{γ/3} > e^{γ/5} | S | p. 859: N_P(m(P_n)) requires γ12 ≤ γij for all other pairs; γ12=e^{γ/3} > γ23=e^{γ/5} |
| 1118 | **GaoAMC2024** | "general sufficient conditions for the path to be the unique minimal tree and the star the unique maximal tree of an exponential VDB index" | **NV** | ScienceDirect 403; no abstract in Crossref, OpenAlex or Semantic Scholar. The title is consistent. Authors must check against the paper (I4) |
| 1137 | Movahedi 2026 | octane benchmark of the DSO study | S | prior audit (§ chemical applicability, p. 155) |
| 1170–1171 | NISTWebBook; APIProject44 | octane property values audited against NIST and API-44 | S (relevance) | "the standard benchmark compilation" itself carries **no citation in main** (I1) |
| 1288 | NIST; Labauf; Reid; Wilhoit | 34 values, of which 29 are compiled: 4 under Labbauf et al., 25 under Reid | S (attribution) / counts NOT VERIFIED | prior audit confirmed the attribution on one NIST page. The counts were not re-counted here |
| 1326 | NIST | boiling points extracted from NIST | S (relevance) | — |
| 1421 | Wiener1947 | two-descriptor model: path number W and polarity number; on trees the polarity number is linear in the counts | S | prior audit (scanned paper: p = pairs three bonds apart). Linearity: p₃ = Σ_uv (d_u−1)(d_v−1) on trees (supplement L1618), correct |
| 1435–1437 | Rada2019 Thm 3.4, Prop. 2.5 | equal-order qualifier present | S | as at L323 |
| 1494 | LoyolaRepo | supplement, data, scripts and verifiers in the package | S for this branch; see B1 and I2 for the default branch | — |

Summary: 0 NOT SUPPORTED. NV: GBN (L289, L648) and Gao–Gao (L1118). PARTIAL: Konstantinova (L939) and the abstract qualifier (L206–209). Portilla is verified by title only.

## 3. Paraphrase and plagiarism screen

**Method.** main.tex and supplement.tex were compared with every local full text: Rada 2019, Cruz–Rada, RRS 2022, Gutman survey, Rada 2026, Kırgız, Nyauli–Buragohain 2027, Gutman et al. 2027, Ali 2025 and Jameson. The comparison used word shingles after stripping LaTeX, math and citations, at K=8 and, for main prose, K=6. No AI detector was used.

| Result | Detail |
|---|---|
| Runs of ≥8 identical words in **prose** | **none**, in main or supplement. Every K=8 hit is a bibliography entry (titles and journal names, L1515–1735) or a formula artefact (`uv e g d u d v …`) |
| Runs of 6–7 words in main prose | L54 "Communications in Mathematical and in Computer Chemistry" (template header); L254 "index, the sum-connectivity index, the harmonic index" (an index list, RRS p. 100); L538 "a class of graphs of fixed order" (technical phrase, Rada 2026 Def. 1); L744 "the number of sign changes in" (standard phrase). None is a risk |
| Close paraphrase of theorem statements | L589–592 restates Lindemann–Weierstrass in the standard form; Rada 2019 Thm 3.3 says "If α1,…,αn are distinct algebraic numbers then, e^α1,…,e^αn are linearly independent over A". Main: "for distinct algebraic numbers x_1,…,x_k the exponentials … are linearly independent over the field of algebraic numbers". This is a standard theorem statement, cited; no risk. L305 paraphrases Gutman p. 834 ("hardly ever matched by facts" → "hardly ever improve on earlier ones in applications"); a 2-word overlap, attributed, fine |

## 4. Ethics and policy

### 4a. What MATCH says (fetched 2026-10-23; raw HTML saved to `litaudit/work/`)

| Topic | prepare.html | ethics.htm |
|---|---|---|
| Authorship approval | — | "The corresponding author should ensure that all co-authors are included on the article, and that all co-authors have seen and approved the final version of the article and have agreed to its publication." |
| AI tools | **not mentioned** | **not mentioned** |
| Supplementary material | **not mentioned** | **not mentioned** |
| Data / data availability | **not mentioned** | **not mentioned** |
| Conflicts of interest / funding | **not mentioned** | **not mentioned** |
| Originality / plagiarism | "In addition to the usual requirements (originality, …)" | "The authors should ensure that they have written entirely original works, and if the authors have used the works of others, that this has been appropriately cited or quoted. If plagiarism is detected, the respective article will be retracted…" |
| Duplicate submission | — | "…the same or similar article has not been published previously and is not simultaneously considered for publication elsewhere." |
| Accuracy | — | "Fraudulent or knowingly inaccurate or knowingly incomplete statements are considered unethical and are unacceptable." |
| References | "The references must be prepared according to the examples given below and listed in alphabetical order." | — |
| Fees | No APC; 750 EUR for priority publication; 90 EUR per colour figure | — |
| Non-existent references | not on these pages. The prior audit reports a warning in the template (not re-checked) | — |

### 4b. What the manuscript contains

| Item | Location | Content / status |
|---|---|---|
| Corresponding author | main.tex:178 | footnote on M. Arockiaraj; e-mails at L185 |
| Acknowledgment | main.tex:1509 | thanks the MPCR Laboratory at FAU for computational resources. No individuals, no funding statement |
| Data availability | main.tex:1491–1498 | supplement `LOYOLA_supplement.pdf`, data, scripts and verifiers in `\cite{LoyolaRepo}`; protocols committed before fitting; "The NIST WebBook pages used are not redistributed; a script of the package downloads them…" |
| Machine-checked scope | main.tex:1500–1506 | Lean 4 scope stated; `LEAN_VERIFICATION.md` (present) |
| Protocol commit evidence | main.tex:1281–1282 (`964b127`), 1327 (`a5cf378`) | both commits are ancestors of HEAD (checked) |
| NIST data-use statement | main.tex:1497 | see B1 |
| KDB / Chéméo | supplement.tex:194 only | values used one by one, with citation. Neither entry has an access date (O3). `DATA/README.md:39–42` records Chéméo's terms (per 07_ETHICS) |
| Companion manuscript | not mentioned in main.tex or supplement.tex | consistent with "no citation of unpublished work". The overlap is analysed in `docs/match/16_COMPANION_OVERLAP.md`. The cover letter should mention it if it has been submitted anywhere (author decision) |
| AI-use, COI, funding statements | absent | not required by MATCH. Disclosure is the authors' decision |

## 5. Issues

| ID | Rating | file:line | Issue | Action |
|---|---|---|---|---|
| B1 | **BLOCKER** | main.tex:1496–1498; bibitem main.tex:1647–1649 | The data statement says "The NIST WebBook pages used are not redistributed". The cited repository resolves to the default branch `main` (`fa6c881`, 2026-10-21). That branch **tracks 262 raw NIST HTML pages** (`external/bp/nist_raw`, `external/nonane_raw_nist`, `external/bp/nist_hvap_pts`; `git ls-tree origin/main`), and they remain in the public history. This branch (3904e38) tracks 0. As things stand, the statement is inaccurate for what a reader opens | Authors: remediate the default branch or repository (`audit/NIST_HISTORY_REMEDIATION_PLAN.md`), or reword the statement, before submission |
| B2 | **BLOCKER** (process) | — (ethics.htm) | MATCH requires that all co-authors have approved the final version. `07_ETHICS…md:99–102` records no approval of this candidate | Obtain written approval from Natarajan, Shiwakoti and Arockiaraj |
| I1 | IMPORTANT | main.tex:1169–1171 | "The property values are the standard benchmark compilation" has no citation in the main paper. The compilations (Ediz 2017; Mondal et al.) are cited only in the supplement (supplement.tex:194, 918–933) | Cite the source compilation in main, e.g. `\cite{Ediz2017Octane}` or the IAMC octane benchmark (as used by Ali 2025), and add the bibitem in order |
| I2 | IMPORTANT | main.tex:1493, 1647–1649 | `LoyolaRepo` is cited without a commit, tag or DOI. The default branch (2026-10-21) predates this commit, so supplementary section numbers may differ from those cited | Cite a tag or commit, or a Zenodo DOI |
| I3 | IMPORTANT | main.tex:289, 648 | GutmanBuragohainNyauli2026 is cited as a source on degree-ratio indices; its content is NV (paywalled, no abstract) | Authors confirm from the full text, or drop it from both places |
| I4 | IMPORTANT | main.tex:1118 (Gao–Gao sentence) | The characterisation "general sufficient conditions for path unique minimal / star unique maximal" is NV | Authors check against the paper and cite the theorem number |
| I5 | IMPORTANT | main.tex:939 (also supplement.tex:687) | Konstantinova is cited for "degeneracy"; the paper concerns "discrimination ability" (prior F4, still open) | Reword as in the prior F4, or cite a page |
| I6 | IMPORTANT | main.tex:1288 | The counts 34 / 29 / 4 / 25 (NIST attributions) were not re-verified in this audit or the prior one | Recount from the provenance CSV |
| O1 | OPTIONAL | main.tex:206–209 (abstract) | "By theorems of Rada" carries no equal-order qualifier; Rada's Thm 3.4 is on G_n. The body (L323, 632, 1433) qualifies it correctly | e.g. "By theorems of Rada (for graphs of equal order; the restriction is removed here)", if space allows |
| O2 | OPTIONAL | main.tex:1630–1633; supplement same entry | NIST entry: year 2025, no retrieval date (NIST's recommended form includes "retrieved [date]") | Add the download dates |
| O3 | OPTIONAL | supplement KDB and Chemeo bibitems | no URL (KDB) and no access dates | Add `https://www.cheric.org/research/kdb/` and access dates |
| O4 | OPTIONAL | main.tex:756 | Jameson is cited without a location | `\cite[Theorem~3.1 and Proposition~3.6]{Jameson2006}` |
| O5 | OPTIONAL | main.tex:237 | GutmanTrinajstic1972 is credited for both Zagreb indices (M₂ usually Gutman et al. 1975) | optional extra citation |
| O6 | OPTIONAL | main.tex:247 | Portilla 2025 verified by title only | authors confirm that it is a bounds/QSPR paper |
| O7 | OPTIONAL | main.tex:253 | Shirdel et al. 2013 was corrected by Basavanagoud–Patil (IJMC 7, 2016). The paper cites it only for the HM name | none required |
