# Publication readiness decision: v40.30 (branch `audit/v4030-adversarial`)

Date: 2026-10-16. Manuscript as of `2732099` (unchanged through `36ab0d5`). Target: MATCH Commun. Math.
Comput. Chem. Sources: the lab run in `verification_logs/lab_09ceba8/`, three independent read-only
reviews written for this report (mathematics, statistics, novelty and journal fit), and spot checks of
their key claims against the files. Earlier positive verdicts (`audit/V4030_SUBMISSION_READINESS.md`,
`audit/final/`) were re-examined, not copied.

## Decision

**Not ready to submit as it stands; ready after the mandatory items in the last section.** No
mathematical error and no error that changes a registered result was found. What blocks submission
is author-side front matter and release items, one missing citation in the same journal, and
wording that claims more than the evidence or the Lean development supports. All mandatory fixes are
edits to text or release steps; none needs a new experiment.

## 1. Verification status (lab run at 09ceba8, mpcrlab12, Linux)

| Check | Status | Evidence |
|---|---|---|
| Lean 4 build, 38 listed theorems + all 52 declarations, axioms only propext/Classical.choice/Quot.sound, no sorry/admit | PASS | `lean_verify.log` |
| Notebooks 01-06 (153 checks) | PASS (05 and 06 on rerun after a thermal-throttling timeout) | `notebooks/`, `notebooks_rerun.log` |
| `verify.py --everything`, all stages except the two below | PASS | `verify_everything.log` |
| Labels and references (`audit/check_labels.py`) | PASS | `check_labels.log` (run separately; needs PyMuPDF, which no requirements file declares) |
| Every-script replay, 60 scripts | **56 exact, 4 numerical discrepancies** (none exact; assessed in Section 2) | `run_all_scripts_rerun.log`, `run_all_scripts_remaining38.log` |
| Manifest at HEAD | PASS after `36ab0d5`; it **failed** at `b607b5f` and `ec4d306` (lab logs pushed without manifest entries; CI on PR #4 failed) | `SHA256SUMS.txt`, PR #4 checks |
| GitHub Actions fast path on `36ab0d5` | PASS (run 38915720868); FAIL on `b607b5f` and `ec4d306` (manifest) | PR #4 checks |
| Colab notebooks at tag `v40.30` | NOT RUN (tag does not exist) | |

The replay's last 38 scripts ran through a wrapper that removed only the 7200 s per-script timeout
(the replay aborts the whole stage on one timeout; `selection_resampling.py` needs more than 2 h on
this machine). This is the one way in which the lab run departs from the scripts as committed.

## 2. The four numerical discrepancies

None of the changed values appears in `main.tex` or `supplement.tex` (searched). All committed
outputs were produced on macOS; these are Linux reruns of byte-identical scripts and inputs.

| Script | What differs | Scientific effect | Status |
|---|---|---|---|
| `external/transfer_exploratory.py` | 3 of 800 cells of `Q2_transfer_frozen`, 14th significant digit (-4226.5717015756 vs ...754; -1468.9151952190 vs ...189) | none: `transfer_exploratory_summary.csv` identical; exploratory script | DISCREPANCY, last-digit rounding; diff retained (`transfer_exploratory_diff.txt`) |
| `external/wide_box_diagnostics.py` | reported maximum relative solver errors (2.24e-14 vs 1.93e-14; 1.40e-14 vs 1.29e-14; 1.17e-15 vs 1.14e-15) | none: rejections 0/3000 and argmin agreement 10/10 identical; all D3 Q2 lines identical | DISCREPANCY, error magnitudes only; diff retained |
| `audit/final/scripts/counterattack_v4030.py` | T1a old-code value at delta=1e-4 (4.6301 vs 4.60937); T1b old/new relative errors (e.g. 1.5e-12 vs 9.6e-13; 3.5e-7 vs 5.6e-7); T1c max error 4.8e-16 vs 3.3e-16 | none: in every case the same outcome holds on both platforms (old code returns a finite wrong value where the fit is undefined, new code returns inf; at eps 1e-4 and 1e-5 the new code rejects; 0 of 400 well-posed designs rejected or changed). T2-T4 identical. | DISCREPANCY, precision only; diff retained. The macOS-specific values are quoted in `audit/V4030_COUNTEREXAMPLES.md` and `audit/final/FINAL_VERIFICATION_1d98621.md`. |
| `audit/final/scripts/press_size_probe.py` | its output file differs; the replay deleted its copy, so the differing line is not known | none, by the script's own exit code: it exits non-zero unless both published outputs are reproduced (`bp_results_summary.csv`, `bp_baselines.csv`), rejections at 1e-6 and 1e-10 are 0, the selected candidate never differs from the QR argmin, leverage-1 rejections are 0, all values are finite and max relative PRESS-vs-QR difference is <= 1e-8. The replay logged `exit 0` (14724 s). The remaining free lines are the two floating-point magnitudes (smallest singular-value ratio, max PRESS-vs-QR difference). | DISCREPANCY, bounded: no decision, rejection count, selection or published result changes; exact differing line UNRESOLVED (a 4 h rerun would settle it) |

## 3. Mathematical correctness

Independent re-derivation of every numbered statement in Sections 2-5 (hand checks, 40-digit
recomputation) found **no error**. Constructions of Theorem 3.5(iii) (orders 13 and 16), the GA merge at
order 17, the five crossings at Delta = 6, the Delta = 7 identifiability exception, the octane collision
vectors and error floor, and Example 4.4 were reproduced. "Every order >= 13" is proved by the pendant-path
construction, not by enumeration. Confidence about 90%; the enumeration code and the cited theorems were
not audited line by line.

Issues to fix (wording or certification, not correctness):
- **Lean coverage is narrower than the framing.** Lean checks the elementary inequalities, one
  determinant (Lemma 3.1 spanning), log-sum-exp convexity, the identity 1 - q^2 = 4xy/(x+y)^2 and the
  order-13 pair on the pure-gamma line only. Nothing using Lindemann-Weierstrass, Laguerre, analyticity,
  the extremal-tree argument or the pendant-path propagation is machine-checked, and the graph-to-degree-pair
  link is not formalised. `LEAN_VERIFICATION.md` and main.tex:1820-1825 say so; **main.tex:1266-1268 does
  not**: for Propositions 5.4 and 5.8 the per-edge extrema are hypotheses of the Lean theorem
  (`formal/LoyolaFormal/Bounds.lean:121-148`). "38 theorems, standard axioms" must not be read as "the
  main results are machine-checked".
- main.tex:519-521 attributes the *first* orders to Theorem 3.5(iii); (iii) proves existence from 13 on,
  minimality comes from enumeration.
- main.tex:281 "characterises exactly what the pure-gamma points discriminate" needs "for algebraic gamma != 0"
  (gamma = ln 4 merges K4 and K1,3, Remark 3.9).
- Table 2: the R entries rest on numerical ties that the caption itself calls uncertified, yet the text
  states them as fact (main.tex:1018, 1037). Exact certification is cheap (group by the squarefree part of ij).
- "GA merges first at 17" needs orders 2-6, which `hp_counts.py` (orders 7-17) does not cover; the
  enumeration range is given as 2-16 (main.tex:609) and 2-17 (main.tex:677).
- Remark 3.9 omits the rationality of alpha, beta it needs; notation clashes (V, c, m, Delta).

**Verdict: PASS for correctness; Lean scope overstated in one sentence.**

## 4. Statistical validity

Pre-registration order is confirmed by GitHub push times (PREREG_v40 13:58:37Z, data and
`bp_tests.py` 14:01:18Z, results 16:19Z on 2026-10-05); the registered text was never edited, only
appended to. D5 and D6 could not have flipped a verdict. No leakage (standardisation and penalty
chosen inside each outer fold). The negative verdicts stand: every flaw found is anti-conservative,
so it could only have produced a false positive.

Challenges to the earlier positive audit:
- **The registered prereg ordering is weak protection.** The full dataset arrived 2 min 41 s after
  the prereg and NIST pages had been archived two days earlier (disclosed). Git cannot show that no one
  looked at decane boiling points. The data rule is mechanical, which limits the risk.
- **Test A had essentially no power** (selection-aware range of dQ2 [-0.51, +0.31]); no smallest effect
  of interest or equivalence margin was registered. The paper correctly says "not demonstrated", but it
  should say explicitly that Test A could not have detected a plausible effect.
- **The registered contrast handicaps gamma by design**: LOh searches 3 dimensions and GM12 2 with
  the same 2000 draws. The -0.072 mostly reflects search density. Section 6.2 acknowledges this;
  Section 6.4 and the abstract do not.
- **The registered interval is not valid inference on the procedure** (bootstrap conditional on
  selection, about 5 times too narrow in Test B; the seed-count arm measures optimiser variance). The
  caption says so.
- **Under-reported result** (recomputed from `external/bp/bp_results_seeds.csv`): on the pooled set
  the narrow-box LO2 beats GM12 in **38/50** seeds (median +0.0033) and GM2 in 40/50; the text reports
  only "marginally ahead (0.980 against 0.976)". Not a registered contrast, but readers need it:
  "no gain from gamma" holds for the LOh-vs-GM12 contrast, not for gamma in general.
- **Overclaims**: "replicates"/"replicated" for nonane dHvap (main.tex:1622, 1806) is a seed-count rule
  that PREREG_v37 calls non-inferential, with a bootstrap interval [-0.006, +0.113] including 0 and 29/34
  values compiled. "The gain disappears" (main.tex:1627, 1769) should be "shrinks to about zero under
  matched search" (best-vs-best on octanes is still +0.015). The Wiener sentence (main.tex:1725) rests on
  one point estimate without an interval.
- Minor: PREREG_v40.md D6 says it lists "every post hoc change"; ten later commits changed
  `bp_tests.py` (all listed in Table 6, outputs unchanged at 4 dp).

**Verdict: PASS for the negative conclusions as worded with hedges; FAIL on two wordings
("replicated", "disappears") and one omission (38/50) until fixed.**

## 5. Novelty and fit

The index itself is a member of Rada's exponential class, and most of the "family" mathematics is
classical (linearity in degree-pair counts, log-sum-exp convexity, exponential-family identifiability,
Rada 2019's Lindemann-Weierstrass argument); the paper concedes this (main.tex:272). New, but modest:
the minimal orders 13 (all trees) and 16 (Delta <= 4) at which distinct degree-pair profiles share a
degree-ratio histogram, which through Corollary 3.6 defeats GA, AG, SDD, ISDD, the diminished Sombor and the
degree-ratio Sombor indices; the Laguerre bound on gamma-crossings with a sharp example; Proposition 3.8.

**Verdict: incremental to moderate; publishable in MATCH if pitched as the degree-ratio collision
result, not as a new index.** The paper argues against its own index (no generic resolution gain, no
predictive gain shown), so a referee may ask why it is introduced.

- **Missing citation (mandatory):** Song et al., MATCH 89 (2023) 343-370 (non-isomorphic trees with equal
  edge-division vectors; infinite classes; complete for order <= 10) is the closest collision paper, in the
  same journal. The repository's own search log marks it "novelty-relevant"
  (`audit/final/NOVELTY_SEARCH_LOG.md:8,29`), but `main.tex` does not cite it.
- The title still says "Degree Imbalance" although Remark 3.7 shows the limit belongs to the degree ratio
  and the parent family reaches it; the earlier referee's retitling was not adopted. main.tex:262-265
  still phrases the coordinate as a novelty claim; contribution (ii) does not credit Rada 2019.
- Length: 40 A5 pages plus a 27-page supplement, long for MATCH; Section 6 is the obvious cut.
- Worth adding: Gutman 2013 (Croat. Chem. Acta, the m_ij survey), Rada et al. 2021 and Das et al. 2021
  (DAM); check whether the tangent Sombor index is ratio-only (Corollary 3.6).

## 6. Remaining limitations (disclosed in the repository, still open)

Seven octane entropies match no primary source; the tetramethylbutane dHvap reference state is
unresolved and its acentric factor conflicts between compilations; all 18 acentric factors and 29 of 34
nonane dHvap values are compilation-only; 57 of 100 boiling points are NIST/TRC averages without
archived source pages; the Konstantinova (1996) citation is unverified; the novelty statement is an
absence claim; the redistribution terms of the KDB and Chemeo values are not established.

## 7. What must happen before submission

Mandatory:
1. Cite and distinguish Song et al., MATCH 89 (2023).
2. Correct the wording: main.tex:1266-1268 (Lean scope of Props 5.4/5.8), 519-521 (minimality from
   enumeration), 281 (algebraic gamma), 1622/1806 ("replicated" -> met its seed-count criterion),
   1627/1769 ("disappears" -> shrinks to about zero under matched search); report the 38/50 narrow-box
   pooled result; state that Test A was not powered.
3. Front matter: replace the placeholder acknowledgment (main.tex:1827); add funding and
   conflict-of-interest lines; replace `\date{\today}` (main.tex:166); AI-use statement; coauthor approval.
4. Data and release: settle the KDB/Chemeo redistribution terms, or remove or re-source those values;
   create tag `v40.30` and an archive DOI (Zenodo) and cite it in the data-availability statement; run
   the notebooks on Colab at the tag.
5. Fix the replay so a timeout is recorded as a PROBLEM and the stage continues, and declare PyMuPDF in
   the requirements (or the labels stage cannot run from the lock files).

Recommended: retitle toward degree-ratio indices and lead the cover letter with the order-13/16
obstruction; certify the Table 2 R ties exactly; shorten Section 6; add the three survey citations;
settle the press_size_probe line with a 4 h rerun; note in the two audit documents that their quoted
counterattack values are macOS-specific.

Acceptance at MATCH cannot be assured by any audit. With items 1-4 done, the scientific content is in
a state to submit.
