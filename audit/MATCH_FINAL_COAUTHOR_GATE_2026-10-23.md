# Final coauthor gate, 2026-10-23

**Branch:** `review/match-audit-validation-2026-10-23` (local), built on `3a5f061`.

## Readiness: CONDITIONALLY READY

The science is ready and independently checked. Submission is blocked by three author actions, listed below. Do not submit until all three are done.

**What was verified:**
- The mathematics, attributions, tables, figure and statistics.
- The Rada mapping was proved, and the decane and pooled tests were reproduced independently.
- The wording edits change no result.

**What blocks submission:**

| # | Blocker | Why | Owner |
|---|---|---|---|
| G1 | **No immutable citation of the repository** | `\bibitem{LoyolaRepo}` is a bare URL that opens `main` (`fa6c881`, 21 Oct). That version predates the current supplement numbering and still serves 262 NIST pages. No tag, GitHub release, Zenodo record or DOI exists. The NIST sentence was therefore removed from the availability paragraph. | Authors: approve a commit, tag it, archive it with a DOI that excludes the NIST pages, then update `\bibitem{LoyolaRepo}` and repin `README.md`, `REVIEWER_START_HERE.md` and the notebooks (still `c48bad05`). Nothing has been created; creating these requires your authorization |
| G2 | **NIST pages are public** | 262 pages sit at the tip of `main` and four other branches, in all branch histories, and in GitHub's `refs/pull/1–4`. Verbatim NIST rows are in two provenance CSVs. No permission to redistribute was found, and per the authors' decision NIST will not be contacted. | Authors. Recommended: a normal commit on `main` that removes the three page directories (the removal already exists as `67e36ad` on the review branches). A history rewrite, or a GitHub Support purge of the PR refs, is a separate decision and needs explicit authorization. See `MATCH_NIST_RELEASE_RIGHTS_2026-10-23.md` |
| G3 | **No recorded approval by all authors** | The MATCH ethics page requires that all co-authors approve the final version | Corresponding author |

## Sign-offs (none approved yet)

| Item | Before → after | Rationale and source | Sign-off |
|---|---|---|---|
| S-1 Proposition title and statement (W4–W5) | "Order exchanges along γ" / "two such graphs exchange order at most five times" → "Crossings along γ" / "the values of two such graphs cross at most five times" | "Order" means number of vertices elsewhere in the paper. The mathematics is unchanged (zeros of $LO(G)-LO(H)$) | [ ] A. Natarajan [ ] G. Shiwakoti [ ] M. Arockiaraj |
| S-2 Definition (D1) | — → "Graphs with Δ ≤ 4 are called chemical graphs, and trees with Δ ≤ 4 chemical trees; the chemical trees of order n are the carbon skeletons of the acyclic alkanes CₙH₂ₙ₊₂." | The terms were used without definition; consistent with Section 2 and with the enumeration | [ ] [ ] [ ] |
| S-3 Rada credit (L3) | — → "For graphs of equal order the exponential GA index does the same, by [Rada 2019, Corollary 3.5], since its weight √(1−q²) is algebraic and injective in q." | Proved in `MATCH_RADA_Q_HISTOGRAM_PRIOR_ART_2026-10-23.md`, from Rada's Table 1, eq. (3), Theorem 3.4 and Corollary 3.5 | [ ] [ ] [ ] |
| S-4 Availability sentence (E1) | "The NIST WebBook pages used are not redistributed; a script…" (`e25d790`) → "The release of the package cited here does not include…" (`3a5f061`) → **removed** (this branch) | Both earlier versions are false for the cited URL. Once G1 and G2 are resolved, restore one of the two versions drafted in the NIST report (§5) | [ ] [ ] [ ] |
| Earlier P1–P4 | `MATCH_FINAL_PATCHLOG_2026-10-23.md` | — | [ ] [ ] [ ] |

The acknowledgment is unchanged and correct. The lab's site (mpcrlab.com) gives the name used in the paper, "Machine Perception and Cognitive Robotics".

## Other author decisions

- **Supplement route.** MATCH's pages do not mention supplementary files. Ask the editorial office first; the draft e-mail is in `MATCH_SUBMISSION_DECISIONS_2026-10-23.md` and is unsent.
- **AI-use disclosure, companion manuscript, title.** MATCH's pages do not mention AI use. The companion manuscript and the title remain open.
- **Contribution framing.** The theory is mostly known or adapted, all of it credited. The new results are the 13 and 16 witnesses, their computer-assisted minimality, Lemma 1, the Laguerre application and Example 1. Option B is recommended: cut Section 6 to about 3 pages and lead with 13 and 16.
- **Optional edits:** see the "Proposed, not applied" list in `MATCH_PATCH_LOG_2026-10-23.md`.

## Reproducibility gaps

| Item | Status |
|---|---|
| `verify.py --offline` | ALL PASS on this branch |
| `verify.py --full` and `--everything`, Lean | NOT RUN on this branch. They last passed at `390728b`; `formal/` is unchanged |
| NIST-dependent stages | BLOCKED: the pages are not in this tree, and NIST will not be contacted |
| Colab notebooks | UNVERIFIED; they are pinned to `c48bad05` |
| Pooled bootstrap interval | One independent implementation only (`pooled_indep.py`) |
| Gao–Gao 2024, Gutman–Buragohain–Nyauli 2026 | Not verifiable (paywalled) |

## Checks run

All checks ran in the validation worktree after this branch's edits.

| Command | Exit / result |
|---|---|
| `python prose_numbers_check.py` | 756 checked, 0 failures |
| `python audit/check_style.py` | PASS |
| `python audit/check_labels.py` | PASS |
| `python audit/test_corrections_2026_10_19.py`, `audit/test_review_2026_10_20.py`, `audit/test_replay_contract_2026_10_21.py` | 0, 0, 0 |
| pdflatex ×3, both files | main 37 pp, supplement 39 pp; 0 undefined; 0 overfull |
| `build_package.sh` (clean extraction of `MATCH_OVERLEAF_CANDIDATE.zip`) | 37 and 39 pp; text identical to the shipped PDFs: True, True |
| `python constancy_test_check.py`, negative controls T1–T4 | 1, 1, 1, 0 (as expected) |
| `python -I audit/independent_recompute_2026-10-23/rada_ga_partition_check.py 60` | partitions coincide for n = 2..60 |
| `python -I audit/independent_recompute_2026-10-23/ss_indep.py` | reproduces 0.4565, 0.4579 and 0.2745 |
| `python -I audit/independent_recompute_2026-10-23/decane_indep.py external/bp/bp_data.csv <out>` | −0.0715, 15, [−0.1558, +0.0015] |
| `python manifest.py` | 456 files, all match |
| `python verify.py --offline` | **ALL PASS**, exit 0 (all 14 offline stages; NIST stages NOT RUN) |

## Publication rule

Nothing has been pushed:
- `3a5f061` and this branch are local only.
- The public branch is unchanged at `4f64671`.
- No tag, release, DOI, pull request or merge was created.

Publishing needs explicit author permission. When it is given, push a new branch by fast-forward only and verify the remote SHA.
