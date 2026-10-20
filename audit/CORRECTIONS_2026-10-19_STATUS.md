# Status of the corrections in `audit/LOYOLA_CORRECTIONS_2026-10-19.md` (2026-10-19)

Branch `review/corrections-impl-2026-10-19`, started from `review/short-version` (`aa993ed`), which descends
from `revision/v40.31-scientific` (`67e36ad`), the commit the report reviewed, and already carries the
earlier attribution and statistics corrections. Nothing was merged, tagged, pushed or submitted. No
frozen protocol, pre-registered hypothesis, data set, seed or registered result was changed.

## Items 1 to 7

| # | Item | State | Changed files | Check |
|---|---|---|---|---|
| 1 | Checkpoint reuse does not validate inputs or outputs | **Fixed.** A finished script is reused only if its fingerprint (commit, script file, arguments, Python, installed package versions, lock files) is unchanged, every output it wrote is present with its recorded SHA-256, and no output of an earlier script has changed since it ran. Tracked files that differ from the commit (other than restored outputs) stop the run. State files are written atomically. The report lists scripts whose record no longer validates as STALE and requires every script to validate for COMPLETE. An old-format state folder (no digests) is not trusted. | `colab/pipeline.py`, `colab/README.md` | `audit/test_corrections_2026_10_19.py` 1a to 1k |
| 2 | Notebook setup can expose a GitHub token | **Fixed.** The token reaches git only through the environment of that one git process (an HTTP header via `GIT_CONFIG_*`), never in a URL or command line; error messages are redacted; the token variable is cleared in a `finally` block. Notebooks regenerated. | `colab/make_notebooks.py`, `colab/*.ipynb`, `colab/README.md` | 2a to 2e (dummy marker secret, forced clone failure) |
| 3 | No immutable, self-validating entry point | **Fixed.** Every notebook in `colab/` and `notebooks/` runs one exact commit (`PIN`), given to the generators with `--pin`. A clean existing checkout is moved to it, one with local changes is rejected, a stale clone fetches it. The Colab environment is synchronised to the lock files on every run (`uv pip sync`: partial installs repaired, unlocked packages removed) and rebuilt if its Python is not 3.13. The reviewer guide documents this single workflow; the links point to the commit, not to the tag `v40.30`, which does not exist. Creating a public tag stays a separate step. | `colab/make_notebooks.py`, `notebooks/gen_notebooks.py`, `colab/*.ipynb`, `notebooks/*.ipynb`, `REVIEWER_START_HERE.md`, `colab/README.md` | 3a to 3h. Not run: a session in an empty Colab runtime (no Colab access from this machine) |
| 4 | 57 direct averages against 58 aggregate-derived values | **Fixed.** Recount of `external/bp/bp_provenance.csv`: 100 included, 57 `AVG`, 1 `mean of 2 NIST averages (agreeing within 3 K)` (3-methylhexane), 42 medians of non-compilation determinations. The supplement (all copies) now says "57 of the 100 values ... and 1 further value is the mean of two NIST averages that agree within 3 K"; the reviewer guide and the provenance ledger say the same. Both numbers are checked against the CSV by the prose registry (`v4029_avg57`, new `corr_meanavg`). No data set changed. | `supplement.tex` and its copies, `drafts/short/supplement_short.tex`, `REVIEWER_START_HERE.md`, `audit/final/CLAIM_PROVENANCE_LEDGER.md`, `prose_claims_a.py` | `prose_numbers_check.py`: 757 checked, 0 failures |
| 5 | Unsupported "several-fold" uncertainty comparison | **Already fixed** on `review/short-version` before this report: no "several-fold" remains in any manuscript, supplement or guide (`grep`), and the Table 5 caption states that the registered intervals are conditional on the fitted predictions. | none | `grep -rn several-fold` returns nothing |
| 6 | Exact-reference comparison needs coverage checks | **Fixed.** `structural/exact_ties.py` requires every expected reference row (32-digit counts n = 7 to 17 for all trees and maximum degree 4; chi n = 7 to 12; fractional points n = 12 to 16, 9 points, γ = 0 and 1), exactly once and parsable, and stops with exit 2 otherwise. It reports the comparisons completed (`32-digit 22/22, chi 6/6, fractional 90/90`) and fails if any is incomplete. Rerun: all counts certified, output unchanged apart from the coverage line. | `structural/exact_ties.py`, `structural/exact_ties_out.txt` | 6: missing row in each file, truncated file, empty file, broken row, duplicated row each exit nonzero; unmodified files pass |
| 7 | "Trees" against "profiles" | **Fixed.** The revision report now says 4069 degree-pair profiles of the 19320 trees of order 16. The manuscript, supplement and short version already said "($4069$ profiles)"; the following "separate all $4069$" and "of $4069$" now also say "profiles". The three registry patterns that read these sentences were updated (values unchanged). | `audit/V4031_REVISION_REPORT.md`, `main.tex`, `supplement.tex`, short versions and Overleaf copies, `prose_claims_b.py` | prose registry 0 failures |

## Item 8: source limitations (decision and status, no new experiments)

Decision: the disclosures stay as they are, each unresolved measurement keeps its source label, and no value
is replaced or removed to change a result. The analyses that restrict to better-documented sources already
exist, are labelled exploratory, and are listed below. No new experiment is justified by the report.

| Unresolved source | Claims that depend on it | Existing sensitivity (exploratory) | Status |
|---|---|---|---|
| Seven octane gas-phase entropies with no matched primary source | Octane correlation ranking for S (Table 4, Figure S1) | `source_sensitivity.py` (four entropies replaced); `audit/v4030/uncertain_source_sensitivity.py`: S broad n = 5, strict n = 2, NOT ESTIMABLE | Disclosed; no claim rests on S alone |
| ΔH_vap of 2,2,3,3-tetramethylbutane (reference state) | Vaporisation-enthalpy comparison of GM and LO | `tmb_exclusion_sensitivity.py` (TMB excluded, same seeds and budgets) | Disclosed; the exclusion result is reported in the main text and the supplement (trace in `TMB_DHVAP_AUDIT.md`) |
| Acentric factors (all 18 from compilations; TMB 0.247, 0.251, 0.255) | Octane correlation ranking for ω | `source_sensitivity.py` (KDB values); strict and broad subsets have n = 0 (NOT ESTIMABLE) | Disclosed; the ω ranking is not separable from compilation quality |
| 29 of 34 nonane vaporisation enthalpies from compilations | Nonane pre-registered test and the exploratory ΔH_vap result in the abstract | strict subset n = 4, NOT ESTIMABLE | Disclosed; the abstract already calls the gain exploratory and shrinking to about zero |
| 57 direct NIST averages and 1 mean of two averages among the 100 boiling points (pages not archived) | Tests A and B (Table 5) | `bp_duplicate_sensitivity.py` (averages quoting more than 3 K dropped: decane ridge 0.863); `uncertain_source_sensitivity.py` strict tier: decanes n = 28, pooled n = 42, ridge still ahead | Disclosed (wording corrected under item 4) |
| Redistribution terms of KDB and Chemeo values | Repository contents, not results | none needed | Open; a licensing decision for the authors, together with the NIST history (approval item c) |

The paper keeps its conclusion: no gain from γ was demonstrated under the tested protocols. This is not
equivalence and not proof that γ never helps. Reproducible computation does not establish novelty or the
quality of a source measurement.

## Verification of the candidate commit

Recorded in the commit message that follows this file and in the final report to the authors: every command,
its exit status, and the stages that passed, failed or were not run.
