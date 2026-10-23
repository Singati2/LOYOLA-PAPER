# Preservation and test matrix, 2026-10-23

**Environment.**
- Python: `venv-locked2`, built from `requirements-lock.txt`.
- TeX: pdfTeX 1.40.22 (TeX Live 2022).
- Host: the MPCR lab machine.
- Every check was run in an isolated worktree. No other worktree was used, and `wt-mainrevert` was not touched.

## 1. Content crosswalk, 46 → 35 → 37 pages

| Version | Commit | Main | Supplement | Where |
|---|---|---|---|---|
| Full | `0877aa0` | 46 | 27 | `drafts/full_46pp_2026-10-23/` (verified byte-identical to `0877aa0` today) and the local branch `review/match-full-46pp-2026-10-23`, which is not on GitHub |
| Shortened | `e25d790` | 35 | 39 | public branch `review/match-editorial-clarity-2026-10-22` |
| Audit | this branch | 37 | 39 | local branch `review/match-final-scientific-audit-2026-10-23` |

**Material moved in the shortening:**
- **To S10:**
  - the proofs of Lemma 1 and Theorem 1;
  - per-graph identifiability, with the remark on Δ = 7 and the spider example;
  - the limits along γ;
  - the closed forms;
  - the termwise bounds.
- **To S11:**
  - the supporting parts of §6.2–6.4;
  - Table 6, now Table S8.

The audit branch moved the proof of Lemma 1 back to the main paper, verbatim. The full mapping of moves and numbers is in `audit/MATCH_SHORTENING_REPORT_2026-10-23.md`.

### Environments of the 46-page main paper

Checked with `preserve_check.py` (whitespace-normalised). Then each difference was inspected by hand.

**At `e25d790`: 72 of 74 are verbatim.**
- **Laguerre proof:** the dropped forward reference, intended.
- **Per-graph identifiability proof:** differs only in two cross-references, now hard-coded main-paper numbers. The script's normaliser misses these.

The report of the shortening said "73 verbatim". This is corrected here.

**On the audit branch: 63 verbatim.** The eleven that differ are:
- the two above;
- Definition (Loyola index family) and Eq. (1), for the terminal period;
- Definition (Ratio plane), Theorem 2 (part iii), the remark after the degree-ratio corollary, Remark (Sharpness) and Remark (Data sets): edits P1–P5 of the patch log;
- Table 5: caption and header;
- Table S8: column type only.

**Not removed:** no theorem-type statement, proof, table, figure, equation or display was removed, and no negative result or limitation was removed.

## 2. Checks and their status

| Check | Command | `e25d790` | Audit branch |
|---|---|---|---|
| Fast verifier | `venv-locked2/bin/python verify.py --offline` | **PASS** (rerun today, exit 0, 19 min). Core verifier FULL PASS covering all 8 numeric tables; prose numbers 756/0; external regression; baseline tests; constancy; interval certificates; style; extremal trees 4–12; collision minimality 13/16; sum-connectivity pair; count dimension and floor; DATA copies; manifest 428; CRLF convention. NIST stages **NOT RUN** | see section 4 |
| Prose numbers | `python prose_numbers_check.py` | PASS (inside verify) | **PASS** 756 checked, 0 failures, 22 uncheckable |
| Prose style | `python audit/check_style.py` | PASS | **PASS** |
| Labels, references, figure, tables, compile | `python audit/check_labels.py` | PASS (earlier today) | **PASS** |
| Test suites of 19 Oct, 20 Oct, 21 Oct | `python audit/test_corrections_2026_10_19.py`, `audit/test_review_2026_10_20.py`, `audit/test_replay_contract_2026_10_21.py` | exit 0 (earlier today) | **exit 0** (all three) |
| pdflatex ×3, both files | — | 35 + 39 pages, 0 undefined, 0 overfull | **37 + 39**, 0 undefined, 0 overfull |
| Clean-extraction build of `MATCH_OVERLEAF_CANDIDATE.zip` | `build_package.sh` (session scratch) | PASS; text identical (independent rebuild by the reproducibility review) | **PASS**; text identical to the shipped PDFs; no placeholders, no `??` |
| `SHA256SUMS.txt` | `sha256sum -c`, `python manifest.py` | PASS 428/428 (independent recompute) | see section 4 |
| Rendered-page inspection | pdftoppm and visual check | all table and figure pages | Table 5 and Table S8 pages re-inspected |
| `verify.py --full` (attack checks, 32-digit recount, tie certificates, verifier self-test, labels, Lean) | — | **NOT RUN**; PASS ON EARLIER COMMIT ONLY (`390728b`, code and manuscript of `c48bad0`, 25 stages, 180 min; `docs/match/11`) | **NOT RUN** |
| `verify.py --everything` | — | **NOT RUN** | **NOT RUN** |
| NIST-dependent stages | needs `external/nist_pages.py --download` | **BLOCKED**: pages not redistributed and not present | **BLOCKED** |
| Lean build | `formal/verify.sh` | **NOT RUN**; PASS ON EARLIER COMMIT ONLY (inside `--full` at `390728b`: 52 declarations, standard axioms; `formal/` unchanged since `91858a1`) | **NOT RUN** |
| Colab notebooks | — | **UNVERIFIED** (`COLAB_FOR_REVIEWERS.md`: "NOT TESTED IN REAL COLAB"); notebooks pin `c48bad05` | **UNVERIFIED** |
| 50-seed searches, bootstraps, permutation tests | — | **NOT RUN** (expensive; no value changed) | **NOT RUN** |

## 3. Proposed Colab smoke tests

These were not run.

1. In a fresh Colab, run `notebooks/01_data` with `LOYOLA_PIN` set to the final commit. Expect the printed commit and "0 mismatches".
2. Run `colab/12_enumeration_certificates` (about 1 min). Expect "ALL CERTIFICATES REPRODUCED".
3. Run `notebooks/06_verification_suite`. Expect "ALL PASS (fast path, offline…)".
4. Run `colab/10` at the final pin, then diff the `pdftotext` output against the committed PDFs.

## 4. Audit-branch verifier and manifest

`verify.py --offline` on the audit-branch working tree, after all source, PDF, zip and manifest changes and before the commit, gave **ALL PASS, exit 0, 15 min 36 s**:

- core verifier FULL PASS, covering all 8 numeric tables;
- prose numbers 756/0;
- external regression tests;
- baseline tests;
- constancy;
- interval certificates;
- style;
- extremal trees 4–12;
- collision minimality 13/16;
- sum-connectivity pair;
- count dimension and floor;
- DATA copies;
- manifest (434 files);
- CRLF convention.

The NIST stages were **NOT RUN**. The log is in the session scratch directory as `audit_runs/verify_offline_auditbranch.log`.

After that run only documentation changed: this section, `docs/match/11` and `SHA256SUMS.txt`. The manifest was then rewritten, and `python manifest.py` was rerun before the commit.

## 5. Packaging risk

- **Zip contents.** Each of the four zips holds the sources and the two figures. The bibliography is embedded, and no class file is needed.
- **Hashes.** The submission manifest rows were regenerated.
- **Template "Received" line.** It prints the compile date, which is the template's default.
- **Figure fonts.** The figures embed Type 3 fonts.
- **Reviewer pin.** The reviewer docs and notebooks still pin `c48bad05`. They must be repinned to the final approved commit before review. This is an author item.
