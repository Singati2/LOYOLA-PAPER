# v40.30 submission readiness

**Repository state**
- Code repairs frozen at `01ad6c6`.
- Manuscript edits and audit evidence up to `53bb763`.
- This report and the stricter Lean check in the following commit.
- All local, on branch `audit/v4030-adversarial`.
- GitHub: `main` at `0c4a4db`, PR #3 at `716cd37`.
- Nothing beyond PR #3 has been pushed. No tag. No merge.

**Status words.** PASS (executed and passed), FAIL, NOT RUN. A green fast GitHub Action is not taken as evidence for any stage it does not run.

## Required verification steps

| # | Step | Status | Evidence |
|---|---|---|---|
| 1 | Fast suite, `python3 verify.py` | **PASS** | at 01ad6c6, inside the run in step 3; at 53bb763 standalone: ALL PASS (fast path), exit 0, 742 prose numbers, manifest 541 files |
| 2 | Full-suite stages (external verifier, structural checks, 32-digit recount, self-test, 13 counter-attacks, labels) | **PASS** | `verification_logs/v40.30/everything_01ad6c6.log` |
| 3 | Replay of every script, `verify.py --everything` | **PASS** | 53 scripts, all exit 0 and reproduce their committed outputs (6,097 s). The run as a whole is INCOMPLETE, exit 3, because Lean was skipped. |
| 4 | Lean 4 proofs, `formal/verify.sh` | **NOT RUN** at 01ad6c6 or later | Not enough disk on the audit machine; the owner chose not to delete files. Passed at 3af7f67, and `formal/LoyolaFormal/` is unchanged since. Steps: `audit/V4030_LEAN_EXTERNAL_RUN.md`. |
| 5 | Stricter Lean check (all 52 declarations, `admit` scan; added in this audit) | **NOT RUN** (untested) | `bash -n` passes, and the generated input was inspected. It must run as part of step 4. |
| 6 | Both documents compile (tectonic) | **PASS** | 40 and 28 pages at 2732099 |
| 7 | Six notebooks, fresh lock-file environment | **PASS** at 1d98621 (153 checks); **NOT RUN** at 53bb763 | The pin logic was re-tested at 01ad6c6 in six cases. Rerun after tagging. |
| 8 | Notebooks on Google Colab | **NOT RUN** | No access. The links resolve only after the tag exists. |
| 9 | GitHub Actions | **PASS** on 716cd37 (fast path only); **NOT RUN** on 01ad6c6 and later | not pushed |
| 10 | Independent mathematics recomputation | **PASS** | `audit/v4030/math_independent_out.txt`, `table2_independent_out.txt`; the S4 recount |
| 11 | Independent ridge pipeline (scikit-learn) | **PASS** | per-compound difference ≤ 5.7e-13 °C and the same penalty in every fold, on 4 sets (`sensitivity_ridge_crosscheck.csv`) |
| 12 | Leakage probes | **PASS** (evidence, not proof) | target probe: prediction change exactly 0 in every fold of 9 models; feature probe: chosen model unchanged in every fold. They cover the leakage paths they exercise only. |
| 13 | Data rebuild from archived pages | **PASS** | bp and nonane data byte-identical; 100 distinct carbon skeletons |

## Claims by evidence type

**Formally proved (Lean; build pending step 4):**
- the termwise bounds and Cauchy–Schwarz interpolation;
- log-sum-exp convexity;
- the Lemma 3.1 spanning statement;
- the identity 1 − q² = 4xy/(x+y)²;
- the order-13 colliding profile pair.

**Proved on paper and independently reproduced numerically:**
- the ratio-plane theorem and the collision orders 13 and 16 (exhaustive enumeration checked against OEIS);
- the crossing bound and five crossings at Δ = 6;
- identifiability and the Δ = 7 exception;
- the ceiling, count ranks and error floor;
- the extremal trees, closed forms and Example 4.4;
- Tables 1, 2 and S4, and every other table through the verifiers.

**Empirical results:**

| Result | Verdict |
|---|---|
| No demonstrated gain from γ | **PASS** as a negative claim. Registered 15/50 and 25/50 seeds; strict 12/50 and 10/50. Not equivalence. |
| Ridge on counts beats every single index | **LIMITED**. Holds on the decanes (strict and refit, 200/200) and on the registered pooled set (200/200). **Not resolved on the restricted pooled C9–C10 set** (181/200, lower tail [−0.55, −0.42]); this is stated in Supplementary Section S8. |
| Octane column leaders | **UNRESOLVED** (every interval includes 0); described as descriptive in the paper. |
| Nonane ΔH_vap replication | **LIMITED** (29/34 values compilation-only); the wide-box result is exploratory. |
| Strict octane S, ω, T_B and nonane ΔH_vap | **NOT ESTIMABLE**. |

## Open items before submission

| Item | Owner | Status |
|---|---|---|
| Lean, step 4 (with step 5), on the commit to be tagged | run on a machine with enough disk | NOT RUN |
| AI-use statement; funding and conflict-of-interest lines; coauthor approval | author | open |
| KDB and Chemeo redistribution terms for the acentric factors | author | open |
| Konstantinova (1996) citation, content unverified (paywalled) | author | open |
| Tag `v40.30`, Zenodo DOI, Colab run (steps 7 and 8) | author approval | open |
| Review pull request for `audit/v4030-adversarial`, kept separate from `main` | author approval | not pushed |

**Verdict.** The mathematics and computation are ready. Submission readiness depends on the Lean run and the author items above. Acceptance at MATCH cannot be assured by any audit.
