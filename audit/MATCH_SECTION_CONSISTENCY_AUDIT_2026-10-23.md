# Section consistency audit (draft)

> **Status (2026-10-23).** This report audits commit `3904e38`; line numbers refer to that commit. Items marked as applied are in `audit/MATCH_PATCH_LOG_2026-10-23.md`. Local full texts used for checking are private copies outside the repository and are not distributed. Discovery tools were used only to find sources; each claim was checked in the source itself.

- **Scope:** `main.tex` (M) and `supplement.tex` (S) at `3904e38`, read only. PDF pages are those of the shipped PDFs.
- **Ratings:** BLOCKER / IMPORTANT / OPTIONAL. No BLOCKER was found: every substantive claim I checked agrees with its table or source, and the numerical checks are listed in `captions_draft.md` §A.
- **Proposals:** each keeps the authors' sentence structure and gives the exact old → new text.

## 1. Does each section's prose interpretation match its table or figure?

| Section | Object | Prose (quoted) | Matches? | Note |
|---|---|---|---|---|
| 4.1, M 822–828, 1226–1229 | Table 1 | "differ by $1.2\,^{\circ}$C and $2.1\,^{\circ}$C in $T_B$" | Yes (118.9−117.7; 117.7−115.6) | "differ in measured properties" (M 826) overstates the S and ω columns. IMPORTANT; proposal in `captions_draft.md`, Table 1 row |
| 4.2, M 942–965 | Fig. 1, Table 2, Table S4 | "$45$ of the $106$ trees ($42.5\%$)"; "$\chi$ leaves it from order $10$, with $77$ values against $79$ profiles"; "$R$ still attains the floor at order $13$ ($570$ values) … the pure-$\gamma$ points give $1090$" | Yes (own enumeration) | — |
| 4.2, M 1010–1027 | order-16 counts | "$3475$ and $3476$ … separate all $4069$ … $3940$ to $4067$ … $4007$ to $4068$ … ($3996$ in both cases)" | Yes (own enumeration) | — |
| 4.3, M 1044–1056 | Table 3 | "$0.1257$ against $0.1256$ … ($0.274$ against $0.313$) … ($0.4579$ and $0.4565$) … ($0.448$--$0.451$)" | Yes | The table prints 0.2745/0.3126; OPTIONAL to quote those |
| 6.1, M 1211–1224 | Table 4 | "Fourteen pairs have $|r| \ge 0.99$ … $99.05\%$ … $0.982$ … $0.993$" | Yes (own code) | — |
| 6.1, M 1174–1184 | TMB | "($|r| = 0.980$) … ($|r| = 0.976$), where $LO(0,0,2)$ follows at $0.970$ … $0.374$ or below" | Yes for the 10.263 input | The text says "The NIST value of $10.26$". IMPORTANT; see `captions_draft.md` M-T4b |
| 6.1, M 1158–1162 | Table S2 | "on octane $T_B$ ($0.764$ against $0.745$ for ${}^{m}\!M_2$)" | **No, mislabelled.** 0.745 is the best fixed index re-chosen in every fold: ${}^{m}\!M_2$ in 17/18 folds and $LO(0,0,1)$ in one (own recomputation, which reproduces 0.7455). S2 itself words it correctly ("With the fixed choice nested in the folds", S 411) | **M-S1, IMPORTANT.** M 1162: "on octane $T_B$ ($0.764$ against $0.745$ for ${}^{m}\!M_2$)" → "on octane $T_B$ ($0.764$ against $0.745$ for the best fixed index chosen within each fold, ${}^{m}\!M_2$ in $17$ of $18$ folds)" |
| 6.2, M 1242–1272 | Tables S3, S6 | "$100/100$ … $+0.069$ and $+0.068$ … $93/100$ and $96/100$ … $(1.021, -1.993)$ … $16$ of the $18$ … $+0.004$ ($28$ of $50$) … $-0.002$ ($24$ of $50$) … $-0.010$ and $-0.016$ … $0.887 \to 0.942$ … $0.957 \to 0.946$ … $11$ to $38$" | Yes (all CSV values) | — |
| 6.3, M 1294–1315 | Table S7, S4 | "$95/100$ and $98/100$ … $+0.048$ and $+0.053$ … ($58/100$ and $63/100$) … $[-0.006, +0.113]$" | Yes | "so tuning $\gamma$ adds nothing there over $\gamma = 1$" (M 1315) is a null claim from two point estimates (0.903 against 0.900) with no interval. This conflicts with the paper's own stance at M 1405–1407 and 1478–1480. **M-S2, IMPORTANT.** "so tuning $\gamma$ adds nothing there over $\gamma = 1$" → "so in point estimate tuning $\gamma$ adds nothing there over $\gamma = 1$" |
| 6.4, M 1375–1428 | Table 5 | "median $\Delta Q^2 = -0.072$, LO is ahead in $15$ of $50$ seeds … $[-0.156, +0.001]$ … $-0.0001$, $25$ of $50$ … $[-0.003, +0.002]$ … ($0.469$ and $0.465$) … ($0.980$ against $0.976$) … $-0.110$ … $[-0.510, +0.312]$ … $0.860$ … between $0.149$ and $0.514$ … $0.991$ … ($0.963$ against $0.967$) … ($0.977$ …) … $1/201$" | Yes: decane contrast and all baselines recomputed with my own code; the rest from CSVs and outputs | "LO is ahead" (M 1376) names the model "LO", while Table 5 calls it LO$_h$. OPTIONAL: "LO is ahead in $15$ of $50$ seeds" → "LO$_h$ is ahead in $15$ of $50$ seeds" |
| S3, S 505–507 | — | "Once the parent is searched over a wide box, freeing $\gamma$ gives no consistent gain (Table~5 and Section~6.2 of the main paper)" | Wrong table: Table 5 holds the boiling points; the ΔH$_{vap}$ wide-box result is Table S6 | IMPORTANT. "(Table~5 and Section~6.2 of the main paper)" → "(Section~6.2 of the main paper and Table~\ref{tab:box})" |

## 2. Are exploratory or post-selection fits ever called independent, generalisation or validation?

I searched both sources for independent*, validat*, generali[sz]*, replicat*, external*, confirm*, out-of-sample and transfer*. **No exploratory or post-selection fit is called independent validation or generalisation.** The supplement is careful:
- S 335: "descriptive rather than independent replications";
- S 594: "rather than independent experimental validation";
- S 656–658: "it tests whether the \emph{procedure} replicates rather than whether an octane-trained model transfers";
- M 1339–1340: "a pooled size-adjusted analysis rather than a fresh external test".

**Residual risk: the word "replication" in the main paper.**
- **Where it appears:** the section title "Replication on the nonane isomers" (M 1279), "use the $35$ nonane isomers as a replication set" (M 1138) and "\emph{replicates}" (M 1295–1297).
- **The gap:** the main text never says what S 656–658 says, namely that it is the procedure that replicates, not a fitted model.
- **Why it matters:** a reader of the main paper alone can take "replicates" as an out-of-sample confirmation of the octane model.
- **Rating:** **M-S3, IMPORTANT.**
- **Fix:** after M 1300 ("…and not an inferential test."), insert "The design refits every model on the nonanes, so it tests whether the procedure replicates, not whether a model fitted on the octanes transfers."

**Smaller point:** `external/PREREG_v37.md` is titled "external validation". The paper rightly does not adopt that wording. No change is needed.

## 3. Do the abstract, introduction contributions, section claims and conclusion agree?

| Claim | Abstract | Introduction | Body | Conclusion | Verdict |
|---|---|---|---|---|---|
| Pure-γ points at algebraic γ ≠ 0 separate exactly the q-histograms | "By theorems of Rada, the points $LO(G;0,0,\gamma)$ at algebraic $\gamma \neq 0$ separate exactly the histograms" (M 203–205) | "is, for graphs of equal order, Theorem~3.4 of~\cite{Rada2019ExpVDB}" (M 322–323) | M 632: "The proof above does not need the order restriction" | "For graphs of equal order, … is Rada's theorem" (M 1433–1436) | Consistent in substance. The abstract alone omits the equal-order qualifier. OPTIONAL: "By theorems of Rada, the points" → "By theorems of Rada, extended here to graphs of different orders, the points" |
| No degree-ratio index separates more | M 205–206 | M 323–325 | Corollary and Remark, M 638–674 | M 1436–1437 | Consistent |
| Histogram determines counts up to order 12 (all trees) and 15 (chemical trees) | "every tree up to order twelve and of every chemical tree, the carbon skeleton of an alkane, up to order fifteen" (M 207–209) | "up to order $15$ and not beyond" (M 311–314) | Remark (floor), Table 2 | "up to order twelve and loses it at order thirteen, and for chemical trees at sixteen" (M 1438–1441) | Consistent and verified. **Term "chemical tree" is not defined in the body** (see §5) |
| Counterexamples at every larger order | M 209–210 | (ii), M 334–337 | Theorem 2(iii) | M 1441 | Consistent |
| At most five crossings at fixed (α,β) | "two chemical graphs exchange order at most five times as $\gamma$ varies" (M 210–211) | "the order of two chemical graphs changes at most five times along $\gamma$" (M 315–316) | Proposition 4, M 748–750 | "Along the imbalance axis two chemical graphs exchange order at most five times" (M 1442–1443) | Consistent in content. **"Order" clashes with order = \|V\|** (see §5, M-T1) |
| Boiling-point tests negative | "did not demonstrate a predictive gain from $\gamma$" (M 211–212) | (iv), M 348–355 | 6.4 | M 1453–1458 | Consistent |
| ΔH$_{vap}$ gain met a seed-count rule and shrank in a wide box | M 212–215 | (iv): "Freeing $\gamma$ gives no demonstrated gain once the parent's search box does not truncate it" | 6.2–6.3 | M 1450–1453 | Consistent. The abstract does not say the nonane values are compilations, which the body flags (M 1288–1292). Acceptable for an abstract |
| Ridge on counts leads single indices | — | "ridge regression on the degree-pair counts leads every single index evaluated in point estimate" (M 353–355) | M 1423–1428 | "a linear model on the degree-pair counts had higher point estimates than every single index, and Wiener's two-descriptor model higher still" (M 1458–1460) | Consistent. The conclusion renames ridge as "a linear model". OPTIONAL: "There a linear model on the degree-pair counts" → "There ridge regression on the degree-pair counts" |
| Results of Sections 3–5 "exact" | — | (iii) separates computer-assisted results | 4.3 is a numerical structure-sensitivity summary | "The results of Sections~\ref{sec:geometry}--\ref{sec:bounds} are exact." (M 1462) | Imprecise: Section 4.3 is not a theorem, and 4.2 counts rest on enumeration. OPTIONAL: → "The results of Sections~\ref{sec:geometry}--\ref{sec:bounds} are proved or rest on exhaustive enumeration, apart from the structure-sensitivity summaries of Section~\ref{sec:ss}." |
| Nonane protocol timing | — | — | M 1281–1283: "committed … before the nonane data were committed and before any model was fitted to them" | S 568–570: "recorded in a git commit … before any nonane value was collected" | Different strengths. The protocol text itself says "Written 2026-10-03, before any nonane property value was collected" (`external/PREREG_v37.md:3`), and git can show only the commit order. OPTIONAL: align S 568–570 to "recorded in a git commit of the reproducibility package before the nonane data were committed (the protocol states that it was written before any nonane value was collected)". |

## 4. Are definitions and theorem dependencies locatable?

### Notation defined before first use

Most notation is defined before use:
- $q_{uv}$ (M 269, 391); $m_{ij}$ and profile (M 372–375);
- $q$-histogram (Def. 2, M 403); $P_\Delta$ (Lemma 1, M 428); $\Pi$ (Def. 3, M 527);
- affine dimension (M 800, before its use at M 853);
- degeneracy (M 939–941); $SS$, $Abr$ (M 1036–1038);
- $Q^2$, ordinary and nested LOO (M 1146–1156); GM, LO (M 1237–1238); $n_C$ (M 1338); BID (M 225); IRLA (M 292).

Exceptions:

| Item | First use | Definition | Rating | Proposal |
|---|---|---|---|---|
| "chemical tree" / "chemical graph" | abstract M 208; body M 310, 315, 632, 669, 894, 1120, 1440, 1443, 1488 | never defined in the body; the abstract's apposition "the carbon skeleton of an alkane" is the only gloss. Prop. 4 states the five-crossing bound for "graphs with $\Delta \le 4$", which the abstract calls "chemical graphs" | **IMPORTANT** | M 365–367: "The chemometric sections use hydrogen-suppressed molecular graphs of alkane carbon skeletons, for which $\Delta \le 4$, while the mathematical results do not assume this bound unless stated." → "Graphs with $\Delta \le 4$ are called \emph{chemical graphs}, and trees with $\Delta \le 4$ \emph{chemical trees}; the chemical trees of order $n$ are the hydrogen-suppressed carbon skeletons of the acyclic alkanes $\mathrm{C}_n\mathrm{H}_{2n+2}$. The chemometric sections use these graphs, while the mathematical results do not assume $\Delta \le 4$ unless stated." |
| $T_B$, $\Delta H_f$, $\Delta H_{vap}$, $S$, ω | Table 1 (cited M 827, p. 15) | M 1165–1168 (p. 24) | IMPORTANT | caption fix in `captions_draft.md` (Table 1) |
| LO$_h$ | M 1402 (text), Table 5 caption | Table 5 caption | OPTIONAL | M 1264: "A hybrid control widens only $(\alpha,\beta)$" → "A hybrid control, LO$_h$, widens only $(\alpha,\beta)$" |
| $TI$ | Prop. 5, M 822 | none | OPTIONAL | "for every vertex-degree-based index $TI$" → "for every vertex-degree-based topological index $TI$" |
| $LO_G(\theta)$ against $LO(G;\theta)$ | M 418 against M 820 | implicit | OPTIONAL | M 418: add after the equation "(we write $LO_G(\theta)$ for $LO(G;\theta)$)" |

### Notation clashes (OPTIONAL; the prior audit noted E, c, V and D)

The clearest clashes:
1. $m$ is the size $|E|$ (M 362) and also a count vector in Prop. 6. Fix: "let $m \neq m'$ be two distinct edge-degree-pair count vectors" (M 864) → "let $\mathbf{m} \neq \mathbf{m}'$ be …", with $m_{ij} - m'_{ij}$ → $\mathbf{m}_{ij} - \mathbf{m}'_{ij}$ in the display.
2. $V$ is the vertex set (M 361) and the number of sign changes in Prop. 4 (M 744). Fix: rename the latter $\sigma$ in Prop. 4, its proof and Remark (Sharpness).
3. $R$ is the Randić index and $R(G)$ the set of realised pairs in S10.2 (S 1173). Fix: rename the latter $\mathcal{R}(G)$.
4. $S$ is entropy, the star $S_n$, the tree $S$ of Example 1 and $S(G)$ in S6. Left as is; context disambiguates.

### Proof dependencies

All proofs cite only earlier material or standard facts, except:

| Dependency | Where | Rating | Proposal |
|---|---|---|---|
| Theorem 2(ii) proof uses Prop. 4, stated later | M 595–596: "has at most $k - 1$ real zeros (Proposition~\ref{prop:laguerre} below)" | OPTIONAL (not circular: Prop. 4 does not use Theorem 2) | → "has at most $k - 1$ real zeros (Laguerre's rule~\cite{Jameson2006}; see Proposition~\ref{prop:laguerre} below)" |
| Theorem 2(iii) proof refers to the profiles "listed in Section~\ref{sec:degeneracy}" | M 603–604 | OPTIONAL | Self-sufficient already: the proof lists the edge multisets. Delete "listed in Section~\ref{sec:degeneracy}" or keep |
| Remark (floor) uses Table 2, Section 4.1 and Prop. 6, all later | M 718–735 | OPTIONAL | Acceptable forward references; the remark interprets rather than proves |
| Prop. 5 proof | Rada 2026 and M-polynomial | — | fine |
| Lemma 1, Prop. 3, Prop. 4, Prop. 6, Prop. 7 | self-contained | — | verified (Lemma 1 determinants recomputed) |

### Is Theorem 1's proof (S10.1) needed in the main paper?

**No.**
- **Main paper:** Theorem 1 is cited once in the main text, in the contribution list (M 344, "\log LO is a log-sum-exp and hence convex (Theorem~\ref{thm:logconvex})"). No main-text proof, remark or numerical claim uses its gradient or Hessian formulas or its strictness criterion. I grepped every `\ref`: `thm:logconvex` occurs once.
- **Remark (Data sets), M 796–806:** this is the only main-text passage close to the strictness criterion. It defines affine dimension itself and rests on the rescaling-direction notion of Prop. S1, not on Theorem 1.
- **Supplement:** the dependants are all inside the supplement:
  - Prop. S1(i) ("as in the proof of Theorem~1", S 1195);
  - the Cauchy–Schwarz corollary ("midpoint log-convexity …, Theorem~1", S 1432–1433);
  - the Lean section (S 867–869).
- **Status mismatch:**
  - The main paper labels the result a "Theorem", calls it one of "Two elementary facts" (M 340–344) and says its proof "is the standard computation" (M 511).
  - In MATCH, "Theorem 1" in a paper whose contribution is the 13/16 thresholds draws a referee's attention to the weakest result.
  - **Fix:** change `\begin{theorem}[Log-convexity]` → `\begin{proposition}[Log-convexity]`.
  - **Numbering:** Proposition shares the theorem counter (M 31), so the number stays 1 and nothing in the main text renumbers.
  - **Supplement:** the hard-coded "Theorem~1 of the main paper" becomes "Proposition~1 of the main paper" at S 1126, 1130, 1132, 1195, 1433.
- **Comprehension:**
  - The one non-obvious clause a reader cannot see at once is the strictness criterion.
  - **Fix:** after M 511, add one sentence and drop the pointer-only line: "The proof is the standard computation of the gradient and Hessian of a log-sum-exp function and is given in Supplementary Section~S10." → "Differentiating $\log \sum_{uv} e^{\theta^{\top} z_{uv}}$ gives the stated gradient and Hessian, and $\operatorname{Cov}_{\theta}(z)$ is singular in a direction $v$ exactly when $v^{\top} z_{uv}$ is constant over the edges, because $w(\theta)$ charges every edge; the details are in Supplementary Section~S10.1."
- **Overall rating:** OPTIONAL. Restoring the full proof is not justified by any dependency.
- **Lemma 1, for contrast:** its proof is correctly in the main paper (restored by R1). It is the only justification that γ is a new direction, and the main text uses it at M 342 and M 892.

## 5. IMRaD as a diagnostic: where each element is found

| Element | Location | Finding |
|---|---|---|
| Motivation | M 223–233 (information loss of degree-based and degree-ratio indices); M 235–263 (place of the GM family); M 301–308 (QSPR use, Gutman's caution) | Findable. Chemical relevance comes late: the first paragraph is purely graph-theoretic, and the QSPR relevance appears in ¶5 (M 305–308) and contribution (iv). OPTIONAL: no change needed for MATCH |
| Gap | M 230–233 ("This paper asks at which tree orders that second loss begins…"); M 310–316 ("What is new here is where the known results bind for chemical graphs") | Clear. The novelty search is recorded at M 636 |
| Methods: mathematics | Definitions in §2 (M 358–410); standing notation in §3 (M 415–424) | Clear |
| Methods: enumeration | M 636: "exhaustive enumeration of all trees of orders $2$ to $17$ in exact rational arithmetic, reproducible with the code of the repository"; counting precision and certification in the Table 2 caption (M 977–985) | **The generation algorithm and the count check are not stated in the main paper.** The scripts use NetworkX's WROM generator and assert the counts against OEIS A000055 and A000602 (`structural/minimality_check.py:10-21`, `structural/exact_ties.py:26-27, 141-142`). I reproduced 48 629 trees of order 17 (24 894 with Δ ≤ 4). **IMPORTANT** for a computer-assisted minimality claim. Proposal at M 636, after "in exact rational arithmetic,": insert "the trees being generated by the algorithm of Wright, Richmond, Odlyzko and McKay as implemented in NetworkX and their numbers checked against the known counts ($48\,629$ trees of order $17$, of which $24\,894$ have $\Delta \le 4$; OEIS A000055 and A000602)," and keep "reproducible with the code of the repository~\cite{LoyolaRepo}". The authors should add the citation: R. A. Wright, B. Richmond, A. Odlyzko, B. D. McKay, Constant time generation of free trees, SIAM J. Comput. 15 (1986) 540–548. I did not check these bibliographic details against the source; verify before use |
| Methods: QSPR | M 1135–1156 (sets, comparison set, $Q^2$, ordinary/nested); M 1236–1240 (matched budget); M 1258 (wide box); M 1281–1292 (nonane protocol); M 1319–1346 (bp rule, Tests A/B, criterion) | Findable. Candidate rounding (3 decimals) and the inner-LOO-RMSE selection rule appear only in S3 (S 446–452). Acceptable |
| Results | §§3–5 (theorems, enumeration, extremal), §6.1–6.4 | Findable |
| Interpretation | Remarks after Thm 2 (M 632–674), Rem. floor (M 718–735), M 892–894, M 1222–1224, M 1274–1277, M 1398–1407, M 1423–1428 | Present and appropriately hedged |
| Limitations | Conclusion (i)–(iv), M 1462–1484; also M 1332–1334, 1398–1407 | Present. The four kinds match the body |

## 6. Grammar, terminology and consistency

Spelling is British throughout the body. I found no -ize/-yze, "behavior", "neighbor" or "vapor" in running text of either file; American forms occur only in bibliography titles, where they must stay. Hyphenation of "pre-registered", "leave-one-out", "half-width" and "edge-degree-pair" is consistent.

| # | Location | Issue | Old → new | Rating |
|---|---|---|---|---|
| M-T1 | M 210–211; 315–316; 337–338; 737; 749–750; 1443; 1471 | "Order" means $|V|$ throughout the paper ("trees of order 13"), but "exchange order" / "the order … changes" means ranking. In the abstract the two senses sit two sentences apart | M 210–211: "two chemical graphs exchange order at most five times as $\gamma$ varies" → "the values of two chemical graphs cross at most five times as $\gamma$ varies". M 315–316: "the order of two chemical graphs changes at most five times along $\gamma$" → "the values of two chemical graphs cross at most five times along $\gamma$". M 337–338: "A bound on the number of order exchanges along $\gamma$" → "A bound on the number of crossings along $\gamma$". M 737: `[Order exchanges along $\gamma$]` → `[Crossings along $\gamma$]`. M 749–750: "two such graphs exchange order at most five times as $\gamma$ ranges over $\mathbb{R}$" → "the values of two such graphs cross at most five times as $\gamma$ ranges over $\mathbb{R}$". M 1442–1443: "two chemical graphs exchange order at most five times" → "the values of two chemical graphs cross at most five times". M 1471–1472: "can exchange order five times along $\gamma$" → "can cross five times along $\gamma$". (Remark (Sharpness) already says "cross") | IMPORTANT |
| M-T2 | M 365–367 | "chemical tree/graph" undefined (§4) | see §4 | IMPORTANT |
| M-T3 | S 719, 735, 746–747, 755–765, 1219 | "molecular subset", "molecular trees", "mol.", "molecular graphs" against "chemical trees" in the main paper | "molecular subsets with $\Delta \le 4$" → "chemical trees ($\Delta \le 4$)"; "Among molecular trees ($\Delta \le 4$)" → "Among chemical trees ($\Delta \le 4$)"; "hence for all molecular graphs" → "hence for all chemical graphs"; Table S4 "mol." → "chem." | OPTIONAL |
| M-T4 | M 1086, 1433, 1488 | "pure-imbalance points" alongside 19 uses of "pure-$\gamma$ points" | Section title "Extremal trees for the pure-imbalance points" → "Extremal trees for the pure-$\gamma$ points"; M 1433 "the pure-imbalance points" → "the pure-$\gamma$ points"; M 1488 likewise | OPTIONAL |
| M-T5 | M 1321–1322; S 667 | $C_8$, $C_9$ in math italics against upright "C4--C16", "C6--C10" elsewhere | "outside $C_8$ and $C_9$" → "outside C8 and C9"; S 667 "from $C_8$ to $C_9$" → "from C8 to C9" | OPTIONAL |
| M-T6 | S 232, 405, 923–925 | "vs", "vs." against "against" elsewhere | "($0.305$ vs.\ compiled $0.303$)" → "($0.305$ against the compiled $0.303$)"; "($0.985$ vs $0.984$)" → "($0.985$ against $0.984$)"; in S8 (iii) "vs" → "against" | OPTIONAL |
| M-T7 | S 202, 248, 253, 788, 906, 911, 912, 918, 922, 932, 983, 995 against S 549 and the main paper | "dataset" (supplement) against "data set" (main paper and S 549) | → "data set" throughout the supplement | OPTIONAL |
| M-T8 | S 253 | "the $2,3,3$-trimethylpentane value" (math mode) | → "the 2,3,3-trimethylpentane value" | OPTIONAL |
| M-T9 | M 892 (last sentence) | The construction "adds no graph information …, only the different weighting" is awkward | "The parameter $\gamma$ adds no graph information beyond the counts, of which every vertex-degree-based index is a functional~\cite{Rada2026LinearVDB}, only the different weighting of Lemma~\ref{prop:indep}." → "The parameter $\gamma$ adds no graph information beyond the counts, of which every vertex-degree-based index is a functional~\cite{Rada2026LinearVDB}; what it adds is the different weighting of Lemma~\ref{prop:indep}." | OPTIONAL |
| M-T10 | M 1421 | The Wiener comparison is stated without its numbers | "Without tuning it gives a higher point estimate than ridge on the decanes (Supplementary Section~S11)" → "Without tuning it gives a higher point estimate than ridge on the decanes ($Q^2 = 0.904$ against $0.860$; Supplementary Section~S11)" (0.9038 verified in `wiener_baseline_out.txt`) | OPTIONAL |
| M-T11 | S 1125–1128; S 1563–1565 | Editorial history left in a submission file: "material moved from the main paper to shorten it … Statements and proofs are unchanged apart from cross-references"; "the parts … that were moved here to shorten it … The text is unchanged apart from cross-references" | S 1125–1128 → "This section holds the proof of Theorem~1 of the main paper, per-graph identifiability, the limits along the $\gamma$ axis, closed forms on standard graphs and termwise bounds." S 1563–1565 → "This section holds supporting analyses for Sections~6.2--6.4 of the main paper and the list of changes made to the pre-registered protocols after outcomes had been seen (Table~\ref{tab:deviations})." | OPTIONAL |
| M-T12 | M 1376 | "LO is ahead" against Table 5's "LO$_h$" | see §1 | OPTIONAL |
| M-T13 | M 1458 | "a linear model on the degree-pair counts" against "ridge regression" elsewhere | see §3 | OPTIONAL |

## Summary of ratings

- **BLOCKER:** none.
- **IMPORTANT (8 here):**
  1. M-T1: the "exchange order" ambiguity;
  2. M-T2: "chemical tree" undefined;
  3. M-S1: "0.745 for ${}^{m}\!M_2$";
  4. M-S2: "adds nothing" without "in point estimate";
  5. M-S3: the meaning of "replicates";
  6. enumeration algorithm and count check not named;
  7. S 507 points to Table 5 instead of Table S6;
  8. the Table 1 symbols, and "measured properties" (cross-listed in the captions draft).
- **OPTIONAL:** everything else above, including Theorem 1 → Proposition 1 with a one-sentence proof sketch.
