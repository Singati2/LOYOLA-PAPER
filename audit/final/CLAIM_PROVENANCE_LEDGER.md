# Claim provenance ledger (v40.30)

**Scope.** This ledger covers every factual claim of the paper that rests on an outside source:

- the 259 experimental values (octane, nonane and boiling-point sets);
- the attributions and literature claims attached to the 54 cited works of main.tex and the 12 of supplement.tex;
- the statements of novelty.

Theorems are excluded. They rest on their proofs, the enumeration code and the Lean files, not on sources.

**Question asked.** For each claim, the ledger asks what its earliest identifiable source is. It also asks whether any agreeing source is an *independent* confirmation, or a *repeat* of that source. This is not the same question as the provenance labels ask. A label such as "AGREEMENT WITHIN TOLERANCE" records numerical agreement only.

**Reproduction.** Run `cd audit/final/scripts && python3 claim_provenance.py`. It writes `claim_provenance_ledger.csv` (one row per value) and `claim_provenance_out.txt`.

## 1. Rule for independence

Agreement with any of the following works counts as **derivative**. Each reproduces earlier measurements, so it never counts as a second confirmation:

- NBS Circular 461 (API Research Project 44, 1947)
- Reid (1972), a review of Wilhoit and Zwolinski (1971)
- Majer and Svoboda (1985)
- Stephenson and Malanowski (1987)
- Daubert (1996)
- KDB, including the values shown on Chemeo
- the compiled 18-octane datasets: the Milano set reproduced by Ediz (2017), and the set reproduced by Mondal et al. (2019)

Several of these compilations reproduce one another, so agreement *between* them is not independent either.

| Tier | Meaning |
|---|---|
| A | Two or more primary determinations from different research groups stand behind the value. Entries of one study (two methods, two temperatures) and papers of one first author count once, and the co-authors Fenske and Braun count as one group. |
| A-AGG | A NIST/TRC average of two or more listed determinations. The constituent papers are not archived in the package, so their mutual independence is not checked. |
| B | One identifiable primary determination. Every other agreeing source is derivative. |
| B? | One NIST value whose primary reference was not recorded when the value was traced. |
| C | Derivative only: the value appears only in compilations, and its earliest determination is not identified. |
| D | Not verified: CANNOT VERIFY, CONFLICT, or an unresolved reference state. |

## 2. Experimental values (259)

| Set | Property | n | A | A-AGG | B | B? | C | D |
|---|---|---|---|---|---|---|---|---|
| Octanes | T_B | 18 | – | 15 | – | 3 | – | – |
| Octanes | ΔH_f | 18 | 1 | – | 15 | 2 | – | – |
| Octanes | ΔH_vap | 18 | – | 3 | 11 | 3 | – | 1 |
| Octanes | S | 18 | – | – | 2 | 3 | 6 | 7 |
| Octanes | ω | 18 | – | – | – | – | 17 | 1 |
| Nonanes | T_B | 35 | 10 | 20 | 5 | – | – | – |
| Nonanes | ΔH_vap | 34 | – | 1 | 4 | – | 29 | – |
| Boiling-point sets | T_B | 100 | 24 | 58 | 18 | – | – | – |
| **All** | | **259** | **35** | **97** | **55** | **11** | **52** | **9** |

### Derivative chains

These are cases where agreement looks like confirmation but is a repeat of one source.

1. **Octane ΔH_f.**
   - 15 of 18 values rest on a single combustion-calorimetry study: Prosen and Rossini (1945), as attributed by NIST.
   - The 1947 API-44 tables list the same values, but they are a compilation that includes that study, so they confirm nothing.
   - Only 2,2,3,3-tetramethylbutane has a second, later determination (Good 1972). It is the only octane ΔH_f in tier A.
2. **Octane ΔH_vap.**
   - 11 values rest on one calorimetric study, Osborne and Ginnings (1947).
   - Majer and Svoboda (1985), Reid (1972), Stephenson and Malanowski (1987) and the API-44 tables are reviews or handbooks that reproduce it.
3. **Octane ω.** All 18 acentric factors come from compilations (KDB, and the dataset reproduced by Ediz 2017). No original determination is identified for any of them. The paper already says that their original source is unidentified.
4. **Octane S.** Six values agree only with the 1947 API-44 tables or a compiled octane dataset. Seven match no source (tier D). Only two rest on a named primary study: Messerly (1971) and Pitzer (1941).
5. **Nonane ΔH_vap.**
   - 29 of 34 values are a single NIST entry from a compilation: 25 listed under Reid (1972), which reviews the 1971 handbook, and 4 under Labbauf, Greenshields and Rossini (1961).
   - The earliest identifiable source of the 25 is the 1971 handbook, whose own sources NIST does not list.
   - The paper discloses both groups (Section 6 and Supplementary Section S8). This ledger adds that **none of the 29 has an independent confirmation**.
6. **The ΔH_vap benchmark 8.41 kcal/mol (2,2,3,3-tetramethylbutane).**
   - The chain runs: the Milano octane dataset, reproduced by Ediz (2017), and then the value used here.
   - For the other 17 octanes, that dataset's ΔH_vap column follows the 1947 API-44 tables. For this isomer the earliest source is not identified.
   - The compound is crystalline at 298 K. The reference state is therefore unresolved (tier D), and the paper says so.
7. **Entropy 102.06 for 2,3,3-trimethylpentane.** The value used comes from a reproduction of a reproduction: the compiled dataset as reproduced by Mondal et al. (2019). Its earliest source is not identified (tier D).
8. **Boiling-point averages.**
   - 57 of the 100 included values are direct NIST/TRC averages and one is the mean of two agreeing NIST/TRC averages (3-methylhexane), all tier A-AGG. The averages do list their constituent determinations, but the source pages behind those determinations are not archived.
   - The 1 "mean of two NIST averages" is also A-AGG.
   - Of the 42 medians of non-compilation determinations, 24 draw on two or more distinct first authors (tier A) and 18 on a single determination (tier B).

### Values that cannot be independently verified (tier D, and C where no primary source exists)

- **Seven octane gas-phase entropies:** 4-methylheptane, 2,2-dimethylhexane, 2,3-dimethylhexane, 3,4-dimethylhexane, 3-ethyl-2-methylpentane, 3-ethyl-3-methylpentane and 2,3,3-trimethylpentane.
- **ΔH_vap of 2,2,3,3-tetramethylbutane** (reference state unresolved).
- **ω of 2,2,3,3-tetramethylbutane** (CONFLICT: 0.247 against 0.251 in KDB and 0.255 in Ediz).
- **The other 17 acentric factors and 29 nonane vaporisation enthalpies.** They agree with their compilation, but no primary determination is identified, so the agreement cannot be checked against a measurement.

## 3. Literature claims

The "Earliest source" column names the original work where the cited work is secondary. "Check" records what this ledger established:

- **verified (computation):** the claim is reproduced by code in the package.
- **verified (metadata):** the bibliographic record was confirmed against Crossref, the publisher or arXiv during the v40.29 audit.
- **content not re-verified:** the claim describes the content of a paper and was not re-read for this ledger.
- **to verify:** the attribution may not be the earliest one; checking it needs a literature lookup that could not be run in this session.

| Claim (location) | Cited | Earliest source | Independent confirmation | Check |
|---|---|---|---|---|
| Randić index; Zagreb indices (main §1) | Randic1975; GutmanTrinajstic1972 | Randić 1975 (original); Gutman and Trinajstić 1972 (original for both M1 and M2) | Gutman and Das, MATCH 50 (2004) 83–92, p. 84: "in the approximate expressions for total π-electron energy two terms occur", namely M1 and M2; the names came later (Gutman, Ruščić, Trinajstić, Wilcox, J. Chem. Phys. 62 (1975) 3399–3405, DOI 10.1063/1.430994) | **VERIFIED** (secondary account by an author of the original, read from the scanned page) |
| General Randić; general sum-connectivity (main §1) | BollobasErdos1998; ZhouTrinajstic2010 | the cited works are the originals | – | content not re-verified |
| Sombor index (main §1) | Gutman2021Sombor | original | – | content not re-verified |
| GA, HM, sum-connectivity as special cases (main §2) | VukicevicFurtula2009GA; ShirdelRezapourSayadi2013HM; ZhouTrinajstic2009sumconn | originals | the special-case identities follow by substituting the parameters into the definition; the tables compute these indices as LO at the stated points | verified (by definition); attribution content not re-verified |
| Gutman–Milovanović family (main §2) | GutmanMilovanovic2020AKCE | original | – | content not re-verified |
| Exponential VDB indices (main §2) | Rada2019ExpVDB | original | – | content not re-verified |
| The ratio q appears in irregularity and degree-ratio indices (main §2) | Albertson1997; LinZhouWangMiao2022; RetiSharafdini2018IRLA; others | IRLA is defined in Réti, Sharafdini, Drégelyi-Kiss, Haghbin, MATCH 79 (2018) 509–524, p. 516, Proposition 2: IRLA(G) = 2 Σ \|d_v − d_u\| / (d_v + d_u), a lower bound for the IRL index of Vukičević and Gašperov (2010); no earlier source is named there | identical to the manuscript's 2 Σ q_uv | **VERIFIED** (read from the published PDF) |
| On Δ ≤ 4 every BID index is a linear functional of the ten counts (main §2) | Rada2026LinearVDB | immediate from the definition. The count vector already appears in the M-polynomial (Deutsch and Klavžar 2015) | follows from the definition | verified (by definition) |
| Rada (2026) shows that no VDB index separates trees with equal profiles; its Example 3 assumes distinct exponents; the pendant-path device (main §3) | Rada2026LinearVDB | the cited work (MATCH 96, 2026) | exhaustive enumeration (`structural/structural_checks.py`, S1) finds collisions at every order 13 to 17, consistent with the propagation, but does not test the device itself | verified (metadata); content not re-verified for this ledger |
| Lindemann–Weierstrass theorem (main §3) | Baker1975 | Lindemann 1882; Weierstrass 1885. Baker (1975) is a textbook treatment | standard | secondary citation, acceptable |
| Zero set of a nonzero real-analytic function has measure zero (main §3, §4) | Mityagin2020 | folklore. Mityagin (2020) gives a short proof | standard | secondary citation, acceptable |
| Laguerre's extension of Descartes' rule (main §5) | Jameson2006 | Laguerre 1883. Jameson (2006) is expository | the five-crossing certificate is checked in interval arithmetic | secondary citation, acceptable |
| Weak discrimination; Example 2.2 trees with equal sum-connectivity (main §4) | RadaRodriguezSigarreta2022Weak | original | the equal sum-connectivity value is recomputed (`structural/sumconn_pair_check.py`, D(1e-6) = 2.4e-7) | verified (computation) for the value; that the trees are exactly those of the cited example is content not re-verified |
| Degeneracy (main §5, supp. S2) | Konstantinova1996Degeneracy | bibliographic record confirmed (J. Chem. Inf. Comput. Sci. 36 (1996) 54–57, DOI 10.1021/ci9502461); the abstract and full text are behind the publisher's paywall | – | **UNVERIFIED (content)**: whether the paper uses "degeneracy" in the sense cited could not be checked; the manuscript cites it for the concept, not as its origin |
| Structure sensitivity; fingerprint variant (main §5, supp. S6) | FurtulaGutmanDehmer2013SS; RakicFurtula2019SS | originals | the implementation reproduces 11 of 14 published SS/Abr values of Barman and Das (2026) | verified (computation, against a third-party table) |
| Path and star criteria (main §5) | CruzRada2019PathStar | original | the proposition is proved directly and checked for orders 4 to 12 | verified (computation) |
| Gutman's survey: new variants hardly ever improve on earlier ones (main §1) | Gutman2026SomborSurvey | the survey | – | content not re-verified (opinion attributed to a source) |
| Parameter-optimised indices fitted to octane properties (main §2) | AliGutmanFurtulaAlbalahiHamza2025 | original | – | content not re-verified |
| Wiener's model with W and p3 (main §6) | Wiener1947 | original | Q² = 0.904 is recomputed (`external/bp/wiener_baseline.py`) | verified (metadata, computation) |
| Octane benchmark of the diminished Sombor study (main §6, supp. S1) | MovahediGutmanRedzepovicFurtula2026 | the benchmark compilation itself (see §2 above) | – | content not re-verified |
| Data sources: NIST WebBook, API-44, Labbauf 1961, Wilhoit–Zwolinski 1971, Reid 1972, Ediz 2017, Mondal 2019 | as listed | see §2 | see §2 | verified (metadata, archived pages) |

## 4. Statements of novelty (absence claims)

These state that something was *not* found. No search can establish them, so they **cannot be independently verified**.

- **"We found no earlier determination of the orders 13 and 16, or of explicit colliding trees for degree-ratio indices"** (main §1).
  - The support is a literature search of 20 Consensus searches (99 unique papers), plus full-text reading of the closest candidates.
  - Song and Huang (MATCH 89, 2023) study a different, distance-type invariant. Two trees with the same edge-division vector have M1 = 26 and 28.
  - Novikov and Shapiro do not decide whether five crossings can be attained.
  - The claim is worded as "we found no", which matches what the evidence supports.
- **Open problems in the conclusion** (whether five crossings can be attained for Δ ≤ 4, and others). These are stated as open, which is correct.

## 5. What this changes

- **No numerical result changes.** Every value keeps its registered number, and no conclusion depends on the tier of an individual value. The QSPR verdicts are robust to the documented substitutions (Supplementary Sections S1 and S8).
- **Disclosure gap closed.** See the supplement clarification above. It names no new citations; citing Prosen and Rossini (1945) and Osborne and Ginnings (1947) directly would need their bibliographic records verified first.
- **Attributions.** The 1972 Zagreb citation (M1 and M2) and the IRLA citation are verified (§3). The content of the Konstantinova (1996) citation remains UNVERIFIED because the paper is paywalled.
- **Supplement clarification added (v40.30).** Section S1 now states that agreement with a secondary compilation is not independent confirmation when both derive from the same measurement, and points to this ledger.
