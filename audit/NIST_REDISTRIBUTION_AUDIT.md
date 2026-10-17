# NIST WebBook redistribution cleanup and audit (2026-10-17)

Decision of the authors: NIST is not contacted, and neither archived NIST Chemistry WebBook pages
nor an unlicensed copy of its data set are redistributed.

## Access terms reviewed
* https://www.nist.gov/srd/public-law (consulted 2026-10-17): "Standard Reference Data (SRD) are
  copyrighted by the U.S. Secretary of Commerce on behalf of the United States of America. All
  rights reserved. None of our SRD may be reproduced, stored in a retrieval system or transmitted,
  in any form or by any means, electronic, mechanical, photocopying, recording or otherwise, without
  prior permission." Legal basis: the Standard Reference Data Act (P.L. 90-396, 15 U.S.C. 290e),
  as amended by P.L. 114-329. The page names no permitted uses.
* https://webbook.nist.gov/chemistry/ (consulted 2026-10-17): "© 2026 by the U.S. Secretary of
  Commerce … All rights reserved", with a pointer to the SRD Act.
* The WebBook is free to consult on the web. Using and citing individual values from it is ordinary
  scientific practice. Copying its pages, or a substantial structured extract of its content, is
  what the notice reserves.

## What was changed
1. **Removed from the tracked tree: all 262 HTML pages** (154 `external/bp/nist_raw/*.html`, 17
   `external/bp/nist_hvap_pts/*.html`, 91 `external/nonane_raw_nist/*.html`).
   * The three folders are now in `.gitignore`.
   * The local copies are kept and untouched. They are byte-identical to the committed archive
     (git blob hashes checked).
   * `SHA256SUMS.txt` no longer lists them.
2. **`external/nist_pages.py` and `external/nist_pages.csv` (new).**
   * For each page, the CSV lists the path, the WebBook URL, the date it was first committed and the
     SHA-256 of the archived copy (in canonical form: Cloudflare's per-response token and trailing
     script removed; all WebBook content lies before them).
   * By default the script only checks offline.
   * `--download` is the only path that contacts NIST. It must be started by the user. It sends one
     request at a time, at least one second apart, and fetches only missing pages.
   * A page whose content differs from the archived copy is saved as `.changed` and is not used.
     The run then exits 1. `--accept-changed` exists for exploration only, and outputs built that
     way are not the registered ones.
   * On 2026-10-17 all 262 live pages matched their archived digests.
3. **No automatic download anywhere.**
   * `verify.py` never downloads. The new `--offline` mode reports the checks that read the pages
     as NOT RUN. Without `--offline`, missing pages make the run INCOMPLETE (exit 3).
   * CI runs `verify.py --offline`. The reviewer notebook 06 runs the same command.
   * In the Colab sequence, notebook 01 has one explicit download cell. It saves the pages to a
     private Drive folder outside the run record. Stages 1, 4 and 8 copy the pages from that folder and
     never download them.
   * `test_regressions.py` skips its one page-dependent test when the pages are absent.
   * `attack_checks.py` and `run_all_scripts.py` copy the downloaded pages into their isolated trees.
4. **Wording.**
   * The Data availability paragraph of `main.tex` now states that the WebBook pages are not
     redistributed and that a script retrieves and checks them.
   * `supplement.tex` S6: "traced to its archived source page" became "traced to its WebBook source
     page (retrieved on 3 October 2026)".
   * READMEs, `REPRODUCE.md`, `REVIEWER_START_HERE.md`, `DATA/README.md` and `colab/README.md` were
     updated to match.

## Audit of the remaining repository content
| Content | Where | NIST content | Assessment |
|---|---|---|---|
| Values used in the analyses, each with its WebBook URL | `external/bp/bp_data.csv` (100 T_B), `external/nonane_data.csv` (35 T_B, 34 ΔH_vap), octane values in `octane_data.py`, the paper's tables | individual values | Citation of individual scientific values. Kept. |
| Provenance of each value used: every NIST determination for the molecule, with NIST's reference attribution | `external/bp/bp_provenance.csv` and `DATA/boiling_points_provenance.csv` (142 molecules, 549 determinations); `external/nonane_provenance.csv` and `DATA/nonane_provenance.csv` (69 rows; `all_determinations` plus a `verbatim_snippet` of the NIST table row) | WebBook table rows for 177 molecules, partly verbatim | **Uncertain.** These are facts with citations, needed to audit the selection rules. They also reproduce NIST's curated rows, including AVG values and TRC uncertainties, for whole molecules. Not removed: they are inputs and outputs of the registered analyses and checks. |
| Identity extracts | `external/nonane_identity.csv` (35 rows: NIST name, InChI, CAS, verbatim snippet) | identifiers | Low concern. InChI is an open identifier. Kept. |
| Calorimetric ΔH_vap census | `external/bp/calorimetric_dHvap298_alkanes.csv` and the `DATA/` copy (48 rows of determinations with references) | WebBook values with attribution | **Uncertain**, same reasoning as the provenance rows. |
| Curated census of NIST acyclic-alkane entries C4 to C16 | `external/bp/nist_alkanes_skeletons_audit.csv` (475 entries: NIST names and ids, availability flags, 156 T_B values, 155 ΔH_vap reference lists, URLs) | systematic extract over a whole compound class, including values the paper does not use (C4, C5, C11 to C16) | **Highest concern.** It is the closest thing in the repository to a copy of part of the database. It is an input of `build_bp_data.py`, `build_calorimetric_set.py` and `check_source_identities.py`. Its C4, C5 and C11 to C16 rows cannot be regenerated, because those pages were never archived. |
| Claim ledger | `audit/final/scripts/claim_provenance_ledger.csv` (259 rows) | source labels and tiers, no NIST table text | Kept. |
| Overleaf zips | `LOYOLA_*_OVERLEAF.zip` | `.tex` and figures only (3, 6 and 7 files) | No pages. |
| Notebooks | `notebooks/`, `colab/`, `verification_logs/*/notebooks` | path names only | No page content. |
| GitHub Actions | `.github/workflows/verify.yml` | no `upload-artifact` step; `gh api …/actions/artifacts` returns 0 | No artifacts. |
| Colab run record | `MyDrive/LOYOLA_colab_run` | rebuilt CSVs (same as the rows above); pages are excluded by `pipeline.py` | Same status as the CSVs. |
| Git history | 72 of 82 commits, all remote branches except this one, PR refs | the 262 pages | See `NIST_HISTORY_REMEDIATION_PLAN.md`. Not changed. |

Removing the HTML pages does not settle the uncertain rows above. Without permission from NIST,
the conservative option is to stop publishing them as committed files.
* The provenance files are already regenerated byte for byte from the downloaded pages by
  `build_nonane_data.py`, `build_bp_data.py` and `build_calorimetric_set.py`. They could be built
  locally after `--download` and checked against committed SHA-256 digests, instead of being
  committed.
* The C6 to C10 part of the census could be rebuilt from the pages in the same way. The C4, C5 and
  C11 to C16 rows support only the data-availability sentence of Section 6.4 and Supplementary S9.
  They would have to be withdrawn, or replaced by a count with URLs.

This changes committed data files and the checks that read them, so it needs the authors' decision.
It was not done in this cleanup.

## Verification of this cleanup
Run on 2026-10-17 in a fresh clone of `2158b72` with this change applied, and in the working copy.
Reference for "identical": the files of commit `2158b72`, the last commit with the pages.

| Check | Command | Result |
|---|---|---|
| Offline fast path, no network (`unshare -rn`), no pages | `python verify.py --offline` | every step PASS except the core verifier, which failed after 1,334 s while another job held the machine's load average near 20 (the stage summary shows 0 math failures); overall FAILURES, exit 1. Run alone the same way (no network, no pages), the core verifier gave FULL PASS, exit 0, in 21 min. Pages-dependent steps reported NOT RUN |
| Missing pages without `--offline` | `python verify.py` (steps stubbed out) | INCOMPLETE, exit 3, as designed |
| Explicit download | `python3 external/nist_pages.py --download` | 262 retrieved, 262 identical to the archived digests, exit 0; offline re-check exit 0 |
| Data sets rebuilt from the downloaded pages | the three builders and `DATA/build_data.py`, SHA-256 against `2158b72` | 14 identical, 0 differ |
| Fast path with the pages | `python verify.py` | ALL PASS (fast path), exit 0; every step PASS, including archived-source identities (154 pages) |
| Colab runner without pages | `colab/pipeline.py --stage 1` and `--stage 4`, empty cache, no network | both stop with the download instruction, exit 1; nothing downloaded |
| Colab runner from the private cache | `colab/pipeline.py --stage 1`, cache filled, no network | every script exit 0; outputs identical to `2158b72`; no page in the state folder |
| Notebooks | `nbformat.validate` on `colab/*.ipynb` and `notebooks/06` | valid |
| PDFs | `pdflatex` x3 (`main.tex`), `tectonic` (`supplement.tex`) | all exit 0; no undefined references; 42 and 28 pages; text identical to the committed PDFs |
| Tracked pages | `git ls-files` on the three folders | 0 tracked; 262 local copies kept, all ignored |
| Clean clone of commit `67e36ad`, no network, no pages, low machine load | `python verify.py --offline` | ALL PASS (fast path, offline), exit 0, 19 min 51 s; NOT RUN: auxiliary outputs, archived-source identities, one page-dependent regression test |
| GitHub Actions on `67e36ad` (PR #5) | `verify.py --offline` | success (run 39066288218) |
| Tracked tree and artifacts of `67e36ad` | `git ls-tree`, `git grep` for WebBook markup, `unzip -Z1` on the three zips, release and Actions artifact lists | 0 HTML files, no WebBook page markup, zips hold `.tex`, figures and READMEs only, 0 releases, 0 artifacts |

Files changed relative to `2158b72`, other than the 262 removed pages: code and documentation listed
above, the two wording edits of `main.tex` and `supplement.tex` (and their Overleaf copies), and the
rebuilt PDFs and zips. No data set, output CSV, table, figure, Lean file or registered result changed.

SHA-256 of the artifacts of this commit:
* `LOYOLA_paper.pdf` eff09ca431609b2236f5067e36805aa6b67997854ec269b0a8780e5c095b264e
* `LOYOLA_supplement.pdf` acd56ba8d4e6e502abf636b9062d832c603674ef1c03e441091331b5247051ed
* `LOYOLA_FINAL_PAPER_OVERLEAF.zip` 44e37ac31a15209a9e2e766021ace2823f8f219e666920a4091534b3b6f95bb0
* `LOYOLA_MAIN_OVERLEAF.zip` efd976d570136c79bf38e6b5dc23194b590d5ecd12829428910777f635abdd18
* `LOYOLA_SUPPLEMENT_OVERLEAF.zip` 9638dda06139ae254579ac1d5e139fd02cc0efcd378beb991f9ef8e343668c6e
* `external/nist_pages.csv` 896079c6fc7b34bb2d9e911640ecbe3da1f9fc34eeb4b9b522415f06ea4b6392

Not run for this commit: `verify.py --full` and `--everything` (several hours).
