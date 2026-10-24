# Final release gate, 2026-10-23

- **Last tested source:** `e3fc8810c066420354c96eb8c38a0b9190dfa663` (SOURCE_COMMIT).
- **Notebooks:** `e90b5bfcb1a46937cb4f20a6b3420007b69caad1`.
- **Branch:** `review/match-final-four-fixes-2026-10-23`, local and not pushed. Its baseline, `0492b80`, was confirmed on GitHub.

## Verdict: CONDITIONALLY READY

All four findings of the brief were confirmed and fixed. Two more mis-anchored checks were found and fixed. The mathematics, data, results, seeds, protocols and figures are unchanged.

Submission is blocked only by author actions:

| # | Blocker | Status | Owner |
|---|---|---|---|
| G1 | **Immutable citation.** `\bibitem{LoyolaRepo}` is the bare repository URL, which opens `main` (`fa6c881`); that commit predates the current supplement numbering. No tag, release or DOI exists. The reviewer docs now pin `e3fc881`/`e90b5bf`, but the manuscript cannot cite its own commit. | BLOCKED pending a release decision. Proposal: tag `e3fc881`, or a later approved commit, deposit it at Zenodo without the three NIST page directories, and cite "version X, doi:…" plus that commit | Authors |
| G2 | **NIST exposure.** 262 WebBook pages are on `main` and 4 other branch tips, in all branch histories and in `refs/pull/1–4`. Two provenance CSVs carry verbatim NIST rows. No permission to redistribute was found, and NIST will not be contacted (authors' decision). | NOT RESOLVED. The availability sentence about NIST was removed from the paper and withheld in the cover letter. Recommended first step: a normal commit on `main` removing the three directories, which already happens on the review branches as `67e36ad`. A history rewrite needs separate authorization | Authors |
| G3 | **All-author approval.** MATCH's ethics page requires it. Pending sign-offs: Proposition 4 title and wording, the chemical-graph definition, the Rada Corollary 3.5 credit, and the removed availability sentence (`MATCH_FINAL_COAUTHOR_GATE_2026-10-23.md`); also the earlier P1–P4. | NOT RECORDED | All three authors |
| G4 | **Supplement route.** MATCH's pages are silent on supplementary files. | Ask the editorial office (unsent draft in `MATCH_SUBMISSION_DECISIONS_2026-10-23.md`) | Corresponding author |

## Preserved

- The witnesses at orders 13 and 16, and their minimality (collision-minimality stage: 13 for all trees, 16 for Δ ≤ 4).
- Credit to Rada for equal order; the GA/q correspondence is proved in `MATCH_RADA_Q_HISTOGRAM_PRIOR_ART`.
- The search statement is limited to what the search covered, and makes no claim of first discovery.
- The negative QSPR results and all limitations.
- 50 optimiser seeds are not presented as independent scientific samples; the text describes the seed-count rule as a summary of optimiser variance.
- The conditional bootstrap does not refit or retune, and the text says it neither establishes equivalence nor excludes gains of practical size.

## Test matrix (source commit, unless stated)

| Check | Command | Result |
|---|---|---|
| Fast verifier | `python verify.py --offline` | **ALL PASS**, exit 0. 14 stages: core verifier FULL PASS on all 8 numeric tables; prose numbers 757/0/22; external regression (1 skip); baseline tests; constancy; interval certificates; style; extremal trees 4–12; collision minimality 13/16; sum-connectivity pair; count dimension and floor; DATA copies; manifest 458; CRLF. NIST stages NOT RUN |
| Prose numbers | `python prose_numbers_check.py` | 757 checked, 0 failures, 22 uncheckable |
| Registry anchor sweep | `python audit/independent_recompute_2026-10-23/registry_anchor_sweep.py` | 779 entries; 2 flags, both correct |
| Registry mutation tests | log in `audit/independent_recompute_2026-10-23/` | 10 of 10 behave as required |
| Style, labels | `audit/check_style.py`, `audit/check_labels.py` | PASS, PASS |
| Test suites | `audit/test_corrections_2026_10_19.py`, `audit/test_review_2026_10_20.py`, `audit/test_replay_contract_2026_10_21.py` | 0, 0, 0; the replay test was also rerun on the notebook commit: 0 |
| PDFs | pdflatex ×3 | main 37 pp, supplement 39 pp; 0 undefined; 0 overfull. S8 and references inspected visually |
| Clean ZIP build | `build_package.sh` | 37 + 39 pp; text identical: True, True |
| Notebooks (fresh clone) | `nbconvert --execute` on 01_data and 02_mathematics | 9/0 and 20/0 (checks/mismatches); negative control refused |
| `verify.py --full` / `--everything`, Lean | — | **NOT RUN** on this branch; the last pass was at `390728b`. `formal/` is unchanged |
| Real Google Colab | — | **NOT RUN** |
| NIST-dependent stages | — | **BLOCKED**: the pages are not in this tree |
| Public link resolution | — | **NOT POSSIBLE** until the branch is pushed |

## Scan of the package

**Checked:**
- No NIST HTML is in this branch's tree.
- No new binary files except the paper's PDFs and zips.
- No real tokens. The only token-like string is the dummy redaction-test marker.

**Not changed (decision G2):** the verbatim NIST rows already in the provenance CSVs, and the personal home paths in `verification_logs/**` (listed earlier).

## Publication

Nothing from this branch has been pushed. Pushing it as a new branch needs explicit author permission. Once pushed, verify the remote SHAs and the Colab links (`MATCH_REVIEWER_PINS_AND_REPLAY_2026-10-23.md`).
