# v40.30 adversarial review: claim-by-claim assessment

**Audited revisions**
- `716cd37`: the PR #3 head, the starting point.
- `01ad6c6`: code repairs, frozen for verification.
- `2732099`: manuscript edits, prepared in a separate worktree from `01ad6c6`.

**Companion files**
- `V4030_COUNTEREXAMPLES.md`: reproductions.
- `V4030_SUBMISSION_CHECKLIST.md`: remaining tasks.
- `v4030/SENSITIVITY_SUMMARY.md`: source-quality sensitivity.

The file names omit the tool name requested in the brief, because the repository keeps tool names out of its files.

**Verdict scale**
- **PASS:** independently reproduced or verified with adequate precision.
- **LIMITED:** supported, with a stated restriction.
- **UNRESOLVED:** these data cannot decide it.
- **FAIL:** refuted.

**Evidence classes**
- (M) mathematical proof;
- (C) computational reproduction;
- (E) exploratory empirical result;
- (N) not estimable.

## Executive verdict

- **No mathematical result was refuted.** Every theorem, proposition, example and table count tested was reproduced by code written for this audit.
- **Five verification-infrastructure defects were confirmed and repaired**, each with a test that fails on the old code. The `press_size` fix was made in the prior round; the other four in this one. None changed a reported number.
- **The empirical claims are narrower than "robust".**
  - "No demonstrated gain from γ" survives every restriction.
  - "Ridge on degree-pair counts beats every single index" survives on the decanes under strict provenance and under refitting.
  - On the strict pooled set it does not survive refitting variability.
  - The octane column rankings are not resolved by these data.
  - Several source-restricted analyses are not estimable.

## Claims

| # | Claim (location) | Class | Verdict | Evidence |
|---|---|---|---|---|
| 1 | First collision orders 13 (all trees) and 16 (Δ ≤ 4) for q-histograms (Thm 3.5(iii), abstract) | M+C | **PASS** | Independent enumeration of orders 2–17, complete against OEIS A000055 and A000602. The witnesses equal the paper's. No collision at orders ≤ 12 or ≤ 15 (`v4030/math_independent_out.txt`). |
| 2 | Ratio-plane theorem (i), (ii); pendant-path propagation (iii) | M | **PASS** | The proofs were read in full. The change vector −(1,d)+(2,d)+(L−1)(2,2)+(1,2) was checked, and all four witness trees were realised by hand and by code. |
| 3 | Lemma 3.1 (affine independence) and its Δ = 1, 2 cases | M+C | **PASS** | Determinants ln 2·ln(9/8) and −(1/6)ln(3/2)ln(2^13/3^8) match to 12 digits; the Δ = 2 identity holds on all three pairs. |
| 4 | Log-convexity theorem; Cauchy–Schwarz corollary | M | **PASS** | The proofs were read in full. The equality and strictness criteria are correct. |
| 5 | Order exchanges ≤ V ≤ r − 1; five crossings for Δ ≤ 4; attainment at Δ = 6 (Prop 3.8, Rem 3.9) | M+C | **PASS** | V = 5 and five sign changes at γ ≈ −17.17, −11.96, −2.03, 2.73, 31.13. The six imbalances for Δ ≤ 4 were checked. Attainment for Δ ≤ 4 is stated as open, which is correct. |
| 6 | Identifiability bound, equality for Δ ≤ 6, the unique Δ = 7 exception (Prop 3.10, Rem 3.11) | M+C | **PASS** | No violation among subsets of ≤ 4 pairs for Δ ≤ 6; for Δ = 7 only {(1,7),(2,6),(3,5),(4,4)}. The reduction argument was checked. |
| 7 | Degree-pair ceiling; 16 count vectors on the octanes; error floor 2.925 °C² | M+C | **PASS** | 16 vectors, the two stated pairs, SSE 2.925 = 117/40. Stated as in-sample, which is correct. |
| 8 | Count ranks 7, 7, 8 | C | **PASS** | Centred ranks 7, 7, 8; the identity Σ(1/i+1/j)m_ij = n holds for every molecule. |
| 9 | Generic discrimination; Example 4.4 | M+C | **PASS** | D(1) = 0.225538, D(1e-6) = 2.401e-7; the profile difference was checked term by term. |
| 10 | Closed forms (9 families) | M+C | **PASS** | Maximum error 1.7e-39 at a random parameter point. |
| 11 | Extremal trees of the pure-γ points | M+C | **PASS** | Proof read, including γ < 0. Exhaustive check for n = 4–14 at γ ∈ {1, −1, 0.3}. |
| 12 | Termwise, bracket and ratio bounds, with equality cases (Section 5) | M | **PASS** | Proofs read. The equality cases for Δ = 1, γ = 0 and γ > 0 were checked. |
| 13 | Table 2 and footnotes a–d | C | **PASS** | Independent recount of all 12 cells and the GA merge order (`v4030/table2_independent_out.txt`). |
| 14 | Supplementary Table S4 (84 cells) | C | **PASS** | Independent recount, 0 mismatches. |
| 15 | Table 1 values | C | **PASS** | All 20 cells equal the dataset. |
| 16 | Tables 4, 5, S1–S3, S5–S7 | C | **PASS** | Exact display strings checked by the verifiers; notebooks 04 and 05 recompute 69 + 27 values with 0 mismatches. |
| 17 | Figures S1, S2 | C | **PASS** | Regenerated and compared byte for byte by the core verifier. The bold leaders and the 25.5% floor match the data. The −0.000 display is annotated (edit E2). |
| 18 | Lean scope statements (supplement S7, conclusion) | M | **PASS (source)**; build **NOT RUN** | No sorry, axiom or native_decide. The paper claims no more than is formalised. The build passed at 3af7f67, and `formal/` is unchanged since. |
| 19 | No demonstrated gain from γ (pre-registered Tests A and B) | E | **PASS** (as a negative claim) | Registered verdict reproduced from the raw seeds (15/50, 25/50; sign convention verified). Strict subsets: 12/50 and 10/50, also "no evidence". **Not** evidence of equivalence: no margin was pre-specified, and the Test A interval spans −0.51 to +0.31. |
| 20 | Ridge on degree-pair counts outperforms every single index (Section 6.4, conclusion) | E | **LIMITED** | **Decanes:** +0.684, CI [+0.46, +1.11]. Strict n = 28: +0.856. 200/200 refitted subsets for every comparator. Independent scikit-learn rebuild identical. **Pooled:** +0.024, CI [+0.014, +0.041], 200/200, under the registered set. **Strict pooled:** C9–C10 only; the jump to +0.28 is a cohort effect (refit effect ≈ 0), and only 181/200 subsets have ridge ahead, so **UNRESOLVED** there. **Stability** (`v4030/refit_stability_out.txt`): replicates 1–100 and 101–200 agree, and the 95% order-statistic range of the strict-pooled 2.5% quantile is [−0.55, −0.42], so the negative tail is not Monte Carlo noise. These are exploratory dataset-composition sensitivity intervals, not confidence intervals. **Restriction:** the claim concerns single-index models; Wiener's two-descriptor model reaches 0.904. |
| 21 | Octane column leaders of Table 4 | E | **UNRESOLVED** | Every leader-minus-runner-up interval includes 0, even on the full data. The paper already calls them descriptive. |
| 22 | Nonane ΔH_vap replication (pre-registered) | E | **LIMITED** | Reported as obtained. 29 of 34 values are compilation-only, and the strict subset (n = 4) is **N**. The gain disappears in the wide box (exploratory). |
| 23 | Octane S, ω and T_B under strict provenance | N | **NOT ESTIMABLE** | S n = 2 and ω n = 0 (strict); T_B strict n = 0. No robustness claim. |
| 24 | Data provenance labels (39 agreement, 8 cannot verify; ledger 35/97/55/11/52/9) | C | **PASS** | Data rebuilt byte for byte from archived pages. Units and phase re-converted (74/78 within tolerance; the other 4 are labelled). Studies deduplicated by research group. No duplicate compounds (100 distinct skeletons). |
| 25 | Novelty (orders 13 and 16, explicit colliding trees) | — | **UNRESOLVED (by nature)** | An absence claim, worded "we found no". The search is documented (Consensus 20 queries; zbMATH and arXiv queries) and found no predecessor. |

## Confirmed defects (all repaired; none changes a reported number)

| ID | Severity | Defect | Test |
|---|---|---|---|
| D1 | P1 | `verify.py --full/--everything` exited 0 with skipped stages | `test_verify_incomplete_exit_status` |
| D2 | P1 | `press_size` returned a finite PRESS for an undefined deleted fit (repaired in 0e0a6d4) | `test_press_size_deletion_rank_loss` |
| D3 | P2 | The constancy check stayed clean when a generator stream was dropped or a new one added | mutation tests: exit 1 |
| D4 | P2 | The notebook pin passed on a modified tree | six-case pin test |
| D5 | P2 | The provenance ledger counted duplicate entries of one study as independent (A 39 → 35) | regenerated ledger |

**Verified non-defects:**
- the duplicate-`run_test` concern (one call only);
- leakage through the target (held-out prediction change exactly 0 in every fold: 4 decane models × 34 folds and 5 pooled models × 100 folds);
- leakage through features (chosen model unchanged in every fold; this is evidence, not proof);
- chemical duplicates (none);
- the provenance join (no unmatched or duplicate records).

## Manuscript edits made (branch `audit/v4030-edits`, commit `2732099`)

| # | Edit |
|---|---|
| E1 | Table 6: row for the stricter rank threshold and the deletion-rank guard, with "No output changes". |
| E2 | Table 4 and Figure S1 captions: the −0.000 entry is −0.0002. |
| E3 | Conclusion: "matched the tuned models" becomes "as accurate in point estimate … no equivalence test was made". |
| E4 | Supplement S8: an exploratory source-quality paragraph, with each number registered in the prose checker (742 checked, 0 failures). |

No abstract, theorem, table value, dataset or pre-registered endpoint was changed.

## Placement recommendation for MATCH

**Main text**
- The ratio-plane theorem and collision orders (claims 1–2).
- The crossing bound and its Δ = 6 attainment (5).
- The identifiability results (6).
- The ceiling and error floor (7).
- The extremal trees (11).
- The bounds (12).
- Tables 1–2.
- The pre-registered negative γ result (19).
- The ridge-versus-single-index finding with its restriction (20).

**Supplement**
- Table 4 rankings (21), labelled descriptive.
- The nonane replication and box sensitivity (22).
- The source-quality sensitivity (E4; claims 20 strict, 23).
- Tuning, ablation and structure-sensitivity tables.
- The Lean scope.
- The provenance detail.

**Optional shortening** (an author decision): move the octane correlation discussion and Table 4 to the supplement, keeping one sentence and Table 1 in Section 6.

## Reproducibility matrix (01ad6c6)

| Stage | Status |
|---|---|
| `verify.py` fast path | **PASS** (all 16 steps, inside the `--everything` run) |
| `verify.py --full` stages: external verifier, structural checks, 32-digit recount, self-test, 13 counter-attacks, labels | **PASS** |
| `verify.py --everything` (replay of every script) | see the run result below |
| Lean (`formal/verify.sh`) | **NOT RUN** on this commit (about 5.6 GB free; the Mathlib build needs about 7.6 GB). Passed at 3af7f67, and `formal/` is unchanged since. |
| Notebooks (fresh environment) | **PASS** at 1d98621 (153 checks); the pin logic was re-tested at 01ad6c6 |
| Google Colab | **NOT RUN** |
| GitHub Actions | green on 716cd37 (fast path only); not run on 01ad6c6 or 2732099 (not pushed) |

**Run result:** RUN_RESULT_PLACEHOLDER

## Submission blockers (see the checklist)

1. A complete `verify.py --everything` with Lean, on the commit to be tagged, on a machine with enough disk.
2. Author decisions:
   - the AI-use statement;
   - funding and conflict-of-interest lines;
   - coauthor approval;
   - the KDB and Chemeo redistribution terms;
   - the Konstantinova citation.
3. Create the tag `v40.30` and mint the Zenodo DOI, after approval; then run the notebooks on Colab.

**On acceptance.** No audit can guarantee acceptance at MATCH. These results show that the mathematical content survived an adversarial reproduction, and that the empirical claims are stated no more strongly than the data support.
