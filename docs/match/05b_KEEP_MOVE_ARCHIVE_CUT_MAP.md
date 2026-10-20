# Section map of `main.tex` and `supplement.tex`: what to keep, move, archive or cut (verdict A)

Date: 2026-10-20. Commit `325bd05`.

Line numbers refer to `wt-fig/main.tex` (2149 lines) and `wt-fig/supplement.tex` (1182 lines). Pages are compiled A5 pages:

* `LOYOLA_paper.pdf`: 44 pages, accurate to about ±1 page after p. 33.
* `LOYOLA_supplement.pdf`: 27 pages.

Actions:

* **KEEP:** stays where it is.
* **CONDENSE:** stays, shortened; no claim or caveat is removed.
* **MOVE:** goes to the supplement, which exists only in the repository because MATCH publishes the paper only.
* **ARCHIVE:** goes to repository Markdown or scripts only, in neither PDF.
* **CUT:** deleted (only redundant prose; never a caveat, limitation or deviation).
* **RECEIVE:** the supplement section takes in moved material.

## `main.tex`

| Lines | Pages | Unit | Action | Note |
|---|---|---|---|---|
| 1–190 | — | Preamble, MATCH template, title block | KEEP | The title may change to "…of Degree-Ratio Indices on Trees" if the coauthors agree. |
| 195–213 | 1 | Abstract | CONDENSE | Port the short draft's class-first sentence (Rada 2019 Proposition 2.5) and the SDD early-failure caveat, within the word budget. |
| 217–228 | 2 | Introduction: index landscape | KEEP | |
| 230–248 | 2 | Gutman–Milovanovič family and its special cases | KEEP | |
| 250–259 | 2–3 | Definition of LO in the introduction; "what γ adds" | KEEP | |
| 261–283 | 3 | Related work (Rada 2019; exponential indices; Euler–Sombor; cosine-rule Sombor; diminished Sombor; degree-ratio indices; IRLA) | KEEP | Novelty and citation distinctions. |
| 285–293 | 3 | Linear-framework framing; "not proposed as a better predictor" | KEEP | |
| 295–319 | 3–4 | Contributions (i)–(vi) | CONDENSE | Item (iv): drop "structure sensitivity". Item (v): keep the extremal trees and say the closed forms and bounds are in S10. Item (vi): add "on the octanes ridge does not lead". |
| 321–338 | 4 | Preliminaries: notation and profile | KEEP | |
| 340–373 | 4–5 | Definitions 1–2, Eq. (2) | KEEP | |
| 376–387 | 5 | §3 set-up, Eq. (3) | KEEP | Eq. (3) is cited by S7. |
| 389–403 | 5–6 | Lemma 1 statement | CONDENSE | Move the Δ = 2 formula sentence (402) into the proof. |
| 405–437 | 6–7 | Lemma 1 proof | KEEP | |
| 439–451 | 7 | Remark (independence vs identifiability) | CONDENSE | To 2 sentences. |
| 453–511 | 7–8 | Theorem 1 and proof | CONDENSE | Trim the semiregular-bipartite sentence (472–480) to a clause. |
| 513–515 | 8 | Pointer: CS corollary as the midpoint case | CUT | It moves with §5.3 to S10, where the CS proof already says this. |
| 517–527 | 8 | §3.1 factorisation, Eq. (4) | KEEP | |
| 529–544 | 8 | Definition 3 and lead-in | KEEP | |
| 546–630 | 8–11 | Theorem 2 and proof with the order-13/16 witnesses | KEEP | Core result. |
| 632 | 11 | Attribution and novelty paragraph | CONDENSE | Drop the Song–Huang seven-vertex/Wiener detail. Keep all attribution sentences and the computer-assisted minimality statement. |
| 634–647 | 11 | Corollary (degree-ratio indices) | KEEP | |
| 649–668 | 11–12 | Remark (Rada 2019 Proposition 2.5; what is new; SDD/ISDD early failure) | KEEP, CONDENSE | Merge the GA sentence with 719–724. |
| 670–695 | 12 | Proposition 3 and proof | KEEP | |
| 697–706 | 12 | Remark (order-16 recovery; K₄ vs K₁,₃ at γ = ln 4) | KEEP | The counterexample is a hypothesis caveat. |
| 708–725 | 12–13 | Remark (floor on Π); GA merge at 17 | KEEP | |
| 727–741 | 13 | Proposition 4 (Laguerre) | KEEP | |
| 743–754 | 13 | Proof: Laguerre's rule | KEEP | |
| 755–760 | 13 | Proof: "independent check" of parity via Proposition 6 | CUT | Redundant; removes the forward reference to the moved Proposition 6. |
| 763–781 | 13–14 | Remark (sharpness at Δ = 6; Δ ≤ 4 open) | KEEP | Open problem; limitation (ii). |
| 783–826 | 14 | Proposition 5 and proof | KEEP | |
| 827–841 | 15 | Remark (the case Δ = 7) | MOVE to S10 | Leave one sentence: equality for Δ ≤ 6 by enumeration, fails from Δ = 7. |
| 843–859 | 15 | Example 1 (spider); Remark (data sets) | KEEP | Needed for the QSPR confounding statement. |
| 861–888 | 15–16 | Proposition 6 (limits along γ) and proof | MOVE to S10 | Not used after the cut at 755–760. Renumbers Propositions 7 → 6, 8 → 7, 10 → 8. |
| 890–928 | 16 | §4.1: Proposition 7 (ceiling) and proof; SSE floor 2.925/0.403 | KEEP | Worked chemical example; the SSE-floor caveat. |
| 930–940 | 17 | Remark (dimension of counts; ranks 7/8) | MOVE to S10 | |
| 942–972 | 17 | Proposition 8 (generic) and proof | KEEP | |
| 974–993 | 17–18 | RRS weak discrimination; inherited from parent; χ not weakly discriminating | KEEP | Known/new distinction. |
| 995–1007 | 18 | Example 2 (RRS trees, D(γ)) | KEEP | Worked example; small-γ caveat. |
| 1009–1034 | 18–19 | Table 1 (octane collision pairs) | KEEP | |
| 1036–1037 | 19 | Orphan sentence (Rada introduced exponential indices) | CONDENSE | Merge into the next paragraph. |
| 1039–1063 | 19–20 | Degeneracy narrative (25.5 % floor; orders 7–12; χ at 10; order-13 profiles; R at 14) | CONDENSE | Keep the 25.5 %/79 floor sentence, the order-13 profiles and the pointers. The order-by-order R/χ details stay in S5 (already there). |
| 1065–1070 | 21 | Figure 1 (order-10 degeneracy chart) | KEEP | Added in `5d5d16a`. |
| 1072–1106 | 20–21 | Table 2 (first failures) | KEEP | Caption: the "Recounts at 50 to 60 digits agree" clause goes to ARCHIVE. |
| 1108–1125 | 21–22 | Off-plane recovery at order 16 | CONDENSE | Keep 4069 vs 3475/3476, the exactness basis, "not proved for larger orders", "no predictive gain" and "sign depends on property". The other counts are in S5 already. |
| 1127–1160 | 22–23 | §4.3 structure sensitivity prose | MOVE to S6 (already near-verbatim there) | Leave 3 summary sentences with the caveats (no ranking at the third decimal; SS not fixed; IRLA ratio higher). |
| 1162–1188 | 23 | Table 3 (SS/Abr) | MOVE to S6 | Renumbers Tables 4/5/6 → 3/4/5. |
| 1190–1199 | 23 | §5 heading; graph families | MOVE (with 5.1) | Retitle §5 "Extremal trees and bounds". |
| 1201–1261 | 23–24 | Proposition 9 (closed forms) and proof | MOVE to S10 | Routine; all nine forms re-derived as correct. |
| 1263–1290 | 24–25 | Proposition 10 (extremal trees) and proof | KEEP | Claimed in the abstract. |
| 1291–1295 | 25–26 | Cruz–Rada derivation; Gao–Gao; Rada 2026 §4.2; general (α, β); chemical-tree bound; maximal chemical trees open | KEEP | Attribution and an open problem. |
| 1295–1296 | 26 | "orders 4 to 12 also checked by enumeration" | ARCHIVE | |
| 1298–1313 | 26 | §5.3 lead-in (known γ = 0 cases; Lean status) | CONDENSE into the §5 summary | 5–6 lines: what S10 contains, that the γ = 0 cases are known (with citations) and that the inequalities, not the equality cases, are Lean-checked. |
| 1315–1517 | 26–30 | Definition 4; Propositions 11–14; CS and uniform-ratio corollaries; proofs | MOVE to S10 | About 3.6 pages saved. |
| 1519–1536 | 30 | §6 lead-in: γ-choice disclosure; exploratory local tuning | KEEP | Disclosures. |
| 1538–1557 | 30–31 | §6.1 data provenance; TMB reference state; S-column caveat | KEEP | Caveats. |
| 1559–1582 | 31 | Table 4 (octane correlations) | KEEP | |
| 1584–1602 | 31–32 | Split best correlation; collinearity; collision pairs realised | KEEP | |
| 1607–1626 | 32 | §6.2 design; narrow-box result; boundary selection | KEEP | |
| 1627–1634 | 32–33 | Dense-grid Q² values and boundary-fold counts | MOVE to a new table in S9 | Not in any supplement today. Keep one sentence: "chosen after inspecting both curves, the smallest examined in which the selections are interior". |
| 1634–1636 | 33 | "Box does not favour the parent uniformly" (T_B 0.665 → 0.606; 0.576 → 0.524) | KEEP | |
| 1638–1652 | 33 | Wide-box repeat (not pre-registered); hybrid control; S moving from 11 to 38 wins | KEEP | |
| 1652–1653 | 33 | M₄.₅,₋₉ fixed-point comparison (post-selection) | MOVE to S3 | Keep "untuned LO(0,0,1) and IRLA match the wide-box parent" if desired. |
| 1653–1656 | 33 | No demonstrated advantage; 2-D vs 3-D handicap | KEEP | |
| 1658–1683 | 34 | §6.3 registered nonane verdict as obtained; compiled enthalpies; design error; primary evidence switched | KEEP | Pre-registration status and deviation. |
| 1685–1699 | 34–35 | LO(0,0,1) and IRLA; ridge on the nonanes; conditional bootstrap | KEEP, plus additions | Add: LO-minus-ridge interval [−0.101, +0.032] includes zero; on the octanes ridge is below the best index for 4 of 5 properties, level on ΔH_vap (0.954 vs 0.957; Table S7). |
| 1701–1723 | 35 | §6.4 cohort, extraction rule, decane representativeness, Tests A/B, criterion | KEEP | |
| 1725–1750 | 35–36 | Table 5 (boiling points) | KEEP | |
| 1752–1798 | 35–37 | Verdicts; narrow-box medians; seed-matched counts; uncorrected 101 cohort; resampling; no equivalence margin; 2-D/3-D; non-comparability; ridge; permutation; Wiener p₃; scope | KEEP; restructure into 3 paragraphs | Every sentence is a pre-registration requirement or a caveat. The deviations table refers to the uncorrected cohort. |
| 1800–1824 | 37–38 | §7 limitations (i)–(iv) | KEEP | |
| 1826–1860 | 38 | Table 6 (deviations) | KEEP; CONDENSE layout only | Optionally merge the three code-level Test B rows (1851–1854) into one row that names all three. No deviation is removed. |
| 1862–1886 | 38–39 | Conclusion; open problems | KEEP | |
| 1888–1906 | 39–40 | Data availability (supplement file; NIST not redistributed; Lean coverage) | CONDENSE slightly | Point to S7/S10 for the Lean-checked bounds. |
| 1908–2146 | 40–44 | Acknowledgment; 56 references | KEEP | Drop entries cited only by moved material, after checking (e.g. CarballosaQuintanaRodriguezSigarreta2023 if uncited). |

## `supplement.tex`

| Lines | Pages | Unit | Action | Note |
|---|---|---|---|---|
| 1–176 | 1 | Preamble; S-prefix numbering; opening note | KEEP | Update the title line if the main title changes. |
| 178–299 | 1–5 | S1 octane provenance; correlation details; redundancy; Figure S1 heatmap | KEEP | Backs the main-text open items. Update "Table 4" → 3. |
| 300–428 | 5–9 | S2 local tuning; Tables S1–S2 | KEEP | Source of the 0.764/0.745 disclosure. Update table references. |
| 429–558 | 9–12 | S3 matched-budget comparison; Table S3 | KEEP; RECEIVE the M₄.₅,₋₉ sentence | |
| 559–684 | 12–15 | S4 nonane replication (protocol; D1/D4; compiled-enthalpy caveat; frozen-parameter exploration; post hoc bootstrap) | KEEP | Exploratory analyses stay, to avoid selective reporting. Update "Table 5", "Proposition 7" → 6. |
| 685–733 | 15–16 | S5 degeneracy narrative | KEEP; RECEIVE main 1039–1063 and 1108–1125 details not already present (most are) | Already references Figure 1 of the main paper. |
| 735–764 | 17 | Table S4 (orders 7–12) | KEEP | |
| 766–786 | 17 | S5 fixed fractional exponents | KEEP | Holds 3940/4067, 4007/4068, 3996. |
| 788–839 | 18–19 | S6 structure-sensitivity protocol | KEEP; RECEIVE main Table 3 (as Table S·) and any main 4.3 sentence missing here | Replace "Table 3 of the main paper" with the local table. |
| 840–888 | 19–20 | S7 Lean formalisation | KEEP | Re-point the bounds to S10. `LEAN_VERIFICATION.md` stays the statement-by-statement map. |
| 889–1021 | 20–24 | S8 open provenance items; Table S5 octane data | KEEP | The data table and the open items are needed for the main-text caveats. |
| 1022–1062 | 24–25 | S9 reporting conventions; extraction rule; decane representativeness | KEEP | |
| 1064–1110 | 25–26 | Tables S6 (box) and S7 (within-fold baselines) | KEEP; RECEIVE a new dense-grid table (main 1627–1634) | |
| new | — | **S10 Further results on the family** | RECEIVE: closed forms (main 1193–1261); limits along γ (861–888); Δ = 7 identifiability set (827–841); dimension of counts (930–940); termwise bounds with proofs (1298–1517); Lean status per bound; bibliography entries Carballosa et al. 2023, Molina–Sigarreta 2025, Granados 2025, Portilla 2025 | `drafts/short/build_supplement.py` shows the S10 assembly. Do not rerun it on the current files: it targets the old numbering and now yields a dangling "Figure 1 of the main paper". |
| 1112–1182 | 26–27 | Bibliography | KEEP; extend for S10 | |

No supplement section is marked ARCHIVE or CUT. The supplement already lives only in the repository, and the exploratory analyses in S2–S4 must stay visible to avoid selective reporting.
