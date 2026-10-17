# Verification and NIST status (2026-10-17)

Labels: VERIFIED, PARTIALLY VERIFIED, FAILED, NOT TESTED, RUNNING.

## Commits (linear history, checked with `git cat-file -p`)

| Commit | Parent | Branch | Content | Pushed |
|---|---|---|---|---|
| `2158b72` | `eb8c25c` | `revision/v40.31-scientific` | Colab notebooks; last commit that tracks the 262 NIST pages | yes |
| `67e36ad` | `2158b72` | `revision/v40.31-scientific` | Removes the 262 pages from tracking; offline verification; explicit download script; two wording edits to the manuscript | **yes** (fast-forward, remote = local verified) |
| `a609843` | `67e36ad` | `revision/v40.31-scientific` | Corrects `audit/NIST_REDISTRIBUTION_AUDIT.md`; `SHA256SUMS.txt` | **no** (local, 1 ahead) |
| `9face2a` | `a609843` | `review/short-version` | Adds `drafts/short/` only (0 files outside it) | no |
| later commits on `review/short-version` | | | see the final report | no |

`main` is `0c4a4db`, untouched.

## Verification runs (exact exit codes)

| Run | Commit | Environment | Exit | Status |
|---|---|---|---|---|
| `verify.py --offline`, fresh clone, `unshare -rn`, machine load ≈ 20 | `67e36ad` tree, before commit | Python 3.13.16, `.venv-verify` (requirements-lock) | **1** | FAILED: the core verifier failed after 1,334 s (summary: 0 math failures). Re-run alone the same way: FULL PASS, exit 0 (21 min). Diagnosis: timeout under load, not science |
| `verify.py` with no pages, without `--offline` (stages stubbed) | same | same | **3** | VERIFIED: reported INCOMPLETE, as designed |
| `nist_pages.py --download` and offline check | same | same | 0, 0 | VERIFIED: 262/262 identical to the archived digests |
| Data sets rebuilt from the downloaded pages, compared with `2158b72` | same | same | — | VERIFIED: 14 identical, 0 differ |
| `verify.py` with pages (fast path) | same | same | **0** | VERIFIED: all stages pass, including archived-source identities (154 pages) |
| Clean clone of `67e36ad`, `verify.py --offline`, no network, low load | `67e36ad` | same | **0** | VERIFIED. NOT RUN by design: auxiliary outputs, archived-source identities, one page-dependent regression test |
| GitHub Actions run 39066288218 (PR #5) | `67e36ad` | ubuntu-latest, Python 3.13, `requirements-lock` | success | VERIFIED. Covers `verify.py --offline` only, so no page-dependent checks, no `--full`, no Lean |
| Local checks: manifest, DATA copies, prose style | `a609843` | `.venv-verify` | 0, 0, 0 | VERIFIED. **No CI**: not pushed. The CI status of `67e36ad` does **not** carry over |
| `verify.py --full`, clean clone plus pages copied locally (no download) | `67e36ad` | `.venv-verify`; `lake` and `pdflatex` present | — | **RUNNING** since 16:26. Fast stages all PASS; at 17:08 it was in the "external verifier" stage. The final exit code will be reported when it ends |
| Colab runner without pages (stages 1 and 4) | `67e36ad` tree | same | 1, 1 | VERIFIED: stops with the download instruction; nothing downloaded |
| Colab runner from the private cache (stage 1) | same | same | 0 | VERIFIED: outputs identical to `2158b72`; no page in the state folder |
| Review-branch checks (manuscript corrections) | `review/short-version` | `.venv-verify` | see the final report | see the final report |

## The audit document `audit/NIST_REDISTRIBUTION_AUDIT.md`

* Table syntax: 13 rows × 4 columns and 15 rows × 3 columns, consistent; no truncated cell.
* Three factual gaps were fixed in `a609843`:
  * the first offline run's overall exit 1 was not stated;
  * "Stages 4 and 8" became "Stages 1, 4 and 8" (`colab/pipeline.py` copies pages for every stage
    containing a NEEDS_NIST script);
  * the clean-clone run, CI and the artifact check were added.
* It distinguishes the offline fast path (CI), the fast path with pages, and the page-dependent checks.
  It states that `--full` was not run for that commit. That is still true until the RUNNING job ends.

## Current exposure (VERIFIED, non-destructive checks on `67e36ad`)

* `git ls-tree` gives 0 HTML files. `git grep` finds no WebBook page markup (`NIST Chemistry WebBook</title>`
  or `cdn-cgi/l/email-protection`).
* The three Overleaf zips hold only `.tex` files, figures and READMEs. The PDFs are built from `.tex` only.
* GitHub releases: 0. Actions artifacts: 0.
* The 262 local copies are kept, ignored by `.gitignore`, and byte-identical to the committed blobs.
  A backup tar is in the session scratchpad.

## Historical exposure (VERIFIED, unchanged)

* The pages are in 72 of 82 commits, from `6f55119` (2026-10-03).
* They are at the tip of every remote branch except `revision/v40.31-scientific`.
* They are in 8 read-only `refs/pull/*`.
* The repository is **public**, with 0 forks.

## Licensing uncertainties (unresolved; the authors must decide)

* **Provenance CSVs** (`external/bp/bp_provenance.csv`, `DATA/boiling_points_provenance.csv`,
  `external/nonane_provenance.csv` and its `DATA/` copy). They reproduce NIST table rows, some verbatim,
  for 177 molecules.
* **Calorimetric census** (48 rows).
* **C4–C16 skeleton census** (`external/bp/nist_alkanes_skeletons_audit.csv`, 475 entries). This is the
  highest concern. Its C4, C5 and C11–C16 rows cannot be regenerated, because those pages were never
  archived.
* Individual values cited with URLs are ordinary citation, but the term "SRD may not be reproduced …
  without prior permission" (nist.gov/srd/public-law) makes whole-molecule row extracts uncertain.

## Remediation options: each needs separate approval; none was executed

1. **Make the repository private** (reversible). It stops public access to the history. It breaks the
   public Colab links and the URL cited in the paper until the repository is public again.
2. **For submission, publish a new public repository** from the cleaned tree, keeping the original
   private as the time-stamped record. This keeps the pre-registration SHA evidence (`a5cf378`,
   `964b127`) without a force-push.
3. **Rewrite history** (`git filter-repo` plus force-push) and ask GitHub Support to purge the
   `refs/pull` refs. This destroys the SHA evidence of the pre-registrations. Not recommended.
4. **Provenance CSVs and census.** Stop committing them, regenerate them locally after `--download`
   and check them against committed digests. Withdraw the C4/C5/C11–C16 census rows or replace them by
   counts and URLs. This changes committed data and checks and needs the authors' decision.

Detailed plan: `audit/NIST_HISTORY_REMEDIATION_PLAN.md`.
