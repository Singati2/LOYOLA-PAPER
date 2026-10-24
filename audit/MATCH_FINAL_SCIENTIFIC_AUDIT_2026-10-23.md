# MATCH final scientific audit, 2026-10-23

> **Correction (2026-10-23, `review/match-final-four-fixes-2026-10-23`).** This report cites the pair $K_4$, $K_{1,3}$ as evidence that the proof of Theorem 2(ii) does not need equal order. That is wrong: both graphs have four vertices. The manuscript sentence now reads "The proof above does not require the graphs to have equal order." The pair is kept only in its valid role, the non-algebraic $\gamma = \ln 4$ example. The text below is preserved as it was written.

- **Baseline audited:** `e25d790c51c6fa591d9b6c78b9dad20819d249d1`. On 2026-10-23 the remote tip of `review/match-editorial-clarity-2026-10-22` was fetched and confirmed equal to it, and `git status` was clean.
- **Archive check:** the archive `drafts/full_46pp_2026-10-23/` was compared with `0877aa0`. `main.tex`, `supplement.tex` and both PDFs are byte-identical.
- **Fixes:** made on the local branch `review/match-final-scientific-audit-2026-10-23` (see `MATCH_FINAL_PATCHLOG_2026-10-23.md`). Nothing was pushed or merged.

## How the audit was done

Five independent read-only reviews were run, each instructed to quote line numbers and not to invent problems:
- mathematics;
- statistics and QSPR;
- presentation, novelty and references;
- tables, figures and footnotes, with rendered pages inspected;
- reproducibility, packaging and the MATCH rules, read from the journal site.

Each finding used below was then re-checked against the source by the lead auditor. In particular:
- Rada (2019), Theorem 3.4: its class $\mathcal{G}_n$ was checked in the source text.
- Supplement S2, Table S2: the 0.764 and 0.745 values are leave-one-out correlations, not $Q^2$.
- `external/bp/wiener_baseline_out.txt`: $Q^2$ = 0.9038.
- `external/PREREG_v40.md`: the NIST download disclosure.
- The S11 seed counts.
- Whether the commits that hold NIST pages were already public: they are, on `main` and ten other remote branches.

## Executive verdict

**CONDITIONALLY READY: FIX LIST.**

The mathematics is correct. Two independent passes re-verified exactly:
- every enumeration up to order 17;
- both witness pairs;
- the five crossings of the sharpness example;
- both determinants, Example 1 and the equality cases;
- the cited theorems against their source texts.

Every number checked in the tables (all cells of Tables 1–5 and S8) and about 50 numbers in the prose agree with the CSVs. The negative results are reported honestly.

What stands in the way is:
1. a small set of over-claims, missing caveats and supplement-only facts that qualify main-text conclusions, now fixed on the audit branch;
2. author and editorial decisions that the audit cannot make (`MATCH_SUBMISSION_DECISIONS_2026-10-23.md`);
3. a strategic risk that no edit removes. By the paper's own account most of its theorems are known or elementary. The new content is the computer-established first orders 13 and 16 with explicit witnesses, plus a negative QSPR study. Three of the five reviewers independently judged the likely MATCH outcome to be **major revision**, mainly for contribution relative to length.

## Findings

### BLOCKER

None found in the sources.

The submission itself is blocked only by author decisions: coauthor approval, title, repository citation, AI disclosure and the supplement route.

### MAJOR

| # | Finding | Evidence | Status |
|---|---|---|---|
| M1 | **Over-claim:** "The parent attains it as well" (simultaneous separation of all $q$-histograms at $\gamma = 0$). The argument is pair by pair. GA, the parent at α = ½, merges histograms at order 17 | `main.tex` (e25d790) l. 626–631; Table 2, footnote d | Fixed (P3); coauthor sign-off |
| M2 | **Supplement-only fact reverses the reading of a main-text conclusion.** The main text concludes that ridge on the counts beats every single index, but Wiener's untuned W + p₃ reaches 0.904 on the decanes against ridge 0.860. Since p₃ is linear in the counts, W carries information beyond them | l. 1375–1383; S11; `external/bp/wiener_baseline_out.txt` | Fixed (Q14) |
| M3 | **"Do not indicate a gain from γ" overstates the negative.** On the pooled set the narrow-box LO beats the narrow-box GM in 40/50 seeds and the wide-box GM in 38/50 | l. 1341; S11 | Fixed: "inconclusive" (Q13) |
| M4 | **The only positive registered verdict (nonane $\Delta H_{\mathrm{vap}}$) rests on compiled values** that may be increment estimates, which would favour a degree-pair descriptor. The caveat was only in S4 | l. 1248–1253 | Fixed (Q6) |
| M5 | **The confirmatory boiling-point tests do not test the $\Delta H_{\mathrm{vap}}$ effect that motivated them.** γ had given mixed $T_B$ results, but the abstract and conclusion juxtapose the two | l. 1278, 1403–1408 | Fixed in body and conclusion (Q9). The abstract wording stays accurate as is |
| M6 | **Self-containment.** The proof of Lemma 1 (the only non-standard proof supporting "γ is a new direction") was in S10. Per-graph identifiability was listed as a main result but not stated. "Affine dimension" and "the termwise bound" were used undefined | l. 339, 441, 766, 1085 | Fixed (R1, A3, P5, A6) |
| M7 | **Contribution relative to length.** The known or elementary results are Theorem 2(i)(ii) and the corollary (Rada 2019), Proposition 3 (stated as not new), Proposition 7 (Cruz–Rada, Gao–Gao), Theorem 1 (log-sum-exp), Proposition 4 (Laguerre), Proposition 6 (inherited from the parent) and Lemma 1 (a rank check). The new results are the minimal orders 13/16 by enumeration, the witnesses and their propagation | Introduction (i)–(iii); l. 646, 857 | **Not fixed: author decision** (see the Proposals section below) |
| M8 | **Reviewer pin.** The reviewer docs and every Colab notebook pin `c48bad05`, 13 commits behind `e25d790`. A reviewer following them checks the 46-page version | `README.md:8`, `REVIEWER_START_HERE.md:7-8`, `COLAB_FOR_REVIEWERS.md:8-9`, `colab/*.ipynb` | **Not fixed.** The pin must name the final approved commit, which does not exist yet. Author item |
| M9 | **NIST pages in the public history.** 262 NIST WebBook HTML pages remain in commits `8793b06` and `dfcf7ee`. These were already public on `main` and ten other remote branches before today's push. The authors' own redistribution audit decided not to redistribute them | `audit/NIST_REDISTRIBUTION_AUDIT.md` | **Not fixed.** A history rewrite is excluded by the standing rules; author decision |
| M10 | **AI-use disclosure.** There is no AI-use, conflict or funding statement, and the MATCH site is silent on these. The public repository records extensive AI-assisted work | match.pmf.kg.ac.rs/prepare.html, /ethics.htm | **EDITORIAL-OFFICE CONFIRMATION REQUIRED**; author decision |
| M11 | **Companion manuscript.** It is disclosed in the cover-letter draft but not cited in the paper | `docs/match/16_COMPANION_OVERLAP.md`; cover letter | Author decision |

### MINOR (fixed unless marked)

| # | Finding | Fix |
|---|---|---|
| m1 | The "at most five times" quantifier lacked "at fixed (α,β)" in the abstract, introduction and cover letter | A1 |
| m2 | Rada's Theorem 3.4 is stated for graphs of equal order; the paper's own example compares $K_4$ and $K_{1,3}$ | A2 |
| m3 | Theorem 2(iii) was ambiguous about where the pendant path is attached | P2 |
| m4 | "The bound is attained" was ambiguous between Laguerre's V and the constant five | P4 |
| m5 | Definition of Π said it "contains GA and AG" | P1 |
| m6 | The local-tuning sentence presented LOO correlations as nested $Q^2$, called the comparator "best fixed point", and said "nested" for globally chosen pools | Q2 |
| m7 | "No parameter … tuned" conflicted with the next paragraph | Q1 |
| m8 | GM and BID were undefined; "therefore" was a non-sequitur | Q3, A4 |
| m9 | Octane losses were understated, including the $\Delta H_f$ interval that excludes zero against γ | Q4 |
| m10 | "Seed-count criterion" was used for 50 seeds, where it is undefined | Q5 |
| m11 | "Design error" was used for a component the boiling-point protocol still keeps | Q7 |
| m12 | The PREREG_v37 commitment to report a matching fixed index was honoured only in S11 | Q8 |
| m13 | The NIST pages were downloaded before the boiling-point rule was written. This was disclosed in PREREG_v40 but not in the paper | Q10 |
| m14 | The Table 5 caption said "nested" for ordinary-LOO columns; the column header "$>$" was cryptic; the text cited Table 5 for intervals it does not show | Q11, Q12 |
| m15 | Enumeration range given as 2–16 in one place, 2–17 elsewhere | A5 |
| m16 | Limitation (iii) should say 34 nonanes for $\Delta H_{\mathrm{vap}}$ | Q15 |
| m17 | Table S7 floated into S10; Table S8 had wide word gaps | L1, L2 |
| m18 | **Not fixed.** Table 2 sits alone on a float page with about 35% blank space. Abruptness is written "0.274" in the text against "0.2745" in the table; the value is correct. Table S5 and S6 captions rely on text for units and definitions. Figure PDFs embed Type 3 fonts. Notation clashes: E, c, V and D each have several meanings | Proposed; low risk |
| m19 | **Not fixed.** Two edits inside the supplement's "DO NOT MODIFY" template preamble (`10px` → `10pt`, removed commented blocks) | Harmless; revert if the editorial office objects |
| m20 | **Not fixed.** Personal home paths appear in `verification_logs/**`; a personal e-mail appears in `audit/push_lab_logs.sh`; a deliberate fake `ghp_` token sits in a redaction test | Author decision; no real secret found |
| m21 | **Not fixed.** "Pre-registered" rests on self-hosted git commits | Proposal: archive the tagged repository with a DOI (Zenodo) before submission |
| m22 | **Not fixed.** References GutmanBuragohainNyauli2026 (content not verified) and Konstantinova1996 (only partly supports "degeneracy") | Authors to confirm from the papers. Gutman, *Croat. Chem. Acta* 86 (2013) 351–361 is suggested for the linear-combination fact, after checking it |

### VERIFIED

Details are in the other audit files.

- **All mathematics.** Every proof, every enumeration (orders 2–17), the witnesses, the crossings, the determinants and the closed forms were re-verified. The attributions were checked against the source texts for:
  - Rada 2019: Theorem 3.4, Proposition 2.5, Example 2.6;
  - Cruz–Rada: Corollaries 2.2 and 3.2, Theorems 2.1 and 3.1;
  - Rada, Rodríguez and Sigarreta: Examples 2.1 and 2.2, Theorems 3.1 and 3.8;
  - Song–Huang.
- **Tables.** Every cell of Tables 1–5 and S8 matches its source, and the Figure 1 bars match their CSV. The figure files in the submission zip are byte-identical to `figures/`.
- **Statistics.** About 50 numbers in the text were checked:
  - Table 5;
  - the decane result: −0.072, 15/50, [−0.156, +0.001];
  - the 2,2,3,3-tetramethylbutane values: 0.980, 0.976, 0.970 and 0.374 (computed from 10.263 kcal/mol, max |r| = 0.37353);
  - the nonane verdicts;
  - the search-box diagnostics;
  - the permutation result (p = 1/201);
  - the ranks 7 and 8.
- **Statistical concepts.** The $Q^2$ definition and the ordinary-versus-nested LOO distinction are correct. The intervals are correctly called conditional on the fitted predictions. No text claims equivalence or "no effect".
- **Builds.** Clean-extraction builds give text identical to the shipped PDFs, and all 428 manifest hashes check.
- **Sensitive files.** The three new commits add no HTML, data or keys.

## Proposals that need coauthor decision (not applied)

1. **Contribution (M7).** Either:
   - **Option A:** add one genuine theorem. Candidates:
     - decide whether five crossings occur for Δ ≤ 4, by a search over trees for a six-class sign pattern with five real zeros;
     - settle the maximal chemical trees of the pure-imbalance points;
     - give a structural reason for 13/16.
   - **Option B:** cut Section 6 to about 3 pages and reframe the paper around the first-failure theorem.

   Recommendation: **Option B**. It needs no new mathematics and no new experiments, and it answers the referee objection the three reviewers raised independently. The title would change only with author approval.
2. **Theorem 1.** Demote it to a remark. It is the standard log-sum-exp computation, and no later result uses it.
3. **Lemma 1 statement.** State it for $P_\Delta \setminus \{(1,1)\}$, the case relevant to connected graphs other than $K_2$. The proof already contains the determinant.
4. **Reviewer pin and repository citation.** After approval, pin the docs and notebooks to the final commit, archive that commit with a DOI, and cite it in `\bibitem{LoyolaRepo}`.

## Journal-readiness recommendation

Do not submit before:
- (a) all three coauthors approve the fixes in the patch log, especially P1–P4;
- (b) the decisions in `MATCH_SUBMISSION_DECISIONS_2026-10-23.md` are made;
- (c) the editorial office confirms how a supplement may accompany the paper.

Proposal 1 is the most effective single change to lower the risk of major revision. It is a choice for the authors, not a correctness requirement.
