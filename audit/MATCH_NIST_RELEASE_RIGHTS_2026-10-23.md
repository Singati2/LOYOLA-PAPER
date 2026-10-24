# NIST WebBook exposure, rights and release plan, 2026-10-23

> **Status.** This is a read-only audit. Nothing was changed on GitHub, at Zenodo or at NIST, and NIST was not contacted. **The authors have decided not to contact NIST and not to redistribute NIST pages.** Read the "ask NIST" options below with that in mind: the remediation that respects the decision is to stop serving the pages, not to seek permission.
>
> **Applied on the validation branch:**
> - The data-availability sentence about NIST pages was removed from `main.tex`. No release exists, and the cited URL opens `main`, which still serves all 262 pages, so the sentence was false.
> - The matching sentence in the cover-letter draft is withheld pending the authors' decision.

This was a read-only audit. Nothing in the repo, on GitHub, at Zenodo or at NIST was changed or contacted. I did not copy any NIST page content.

## 1. Exposure inventory

Repo: public, not a fork, 0 forks, 0 stars. Default branch is `main`. GitHub `pushed_at` is 2026-10-24T00:59Z (UTC).

### Tracked NIST WebBook HTML at each remote branch tip
I identified the pages by path (`*.htm[l]`) and checked each one by content signature: `webbook.nist.gov` or "NIST Chemistry WebBook" in the first 2 KB. All 262 HTML files matched. There are no other HTML files.

| Branch | Tip | Date | NIST HTML |
|---|---|---|---|
| main (=HEAD) | fa6c881 | 2026-10-21 | **262** |
| audit/provenance-final (PR #3, open) | 716cd37 | 2026-10-12 | 262 |
| audit/v4030-adversarial (PR #4, open) | f109127 | 2026-10-16 | 262 |
| research/weak-discrimination | 41db8c1 | 2026-10-09 | 262 |
| robustness-guards | 01bfaf5 | 2026-10-10 | 262 |
| revision/v40.31-scientific (PR #5, open) | 67e36ad | 2026-10-17 | 0 |
| review/corrections-2026-10-19 | 31e8de9 | 2026-10-20 | 0 |
| review/corrections-impl-2026-10-19 | 9212441 | 2026-10-20 | 0 |
| review/match-figure-2026-10-20 | 5a96fc5 | 2026-10-20 | 0 |
| review/match-final-adjustments-2026-10-21 | 723a2d0 | 2026-10-22 | 0 |
| review/match-editorial-clarity-2026-10-22 | 4f64671 | 2026-10-23 | 0 |

Where the 262 pages sit on `main`: `external/nonane_raw_nist/` (91), `external/bp/nist_raw/` (154) and `external/bp/nist_hvap_pts/` (17).

GitHub also holds pull-request refs that the branch owner cannot delete. I counted HTML in each through the API:
- refs/pull/1/head 0d8b5ef (closed PR): 245 pages
- refs/pull/2/head 71d1757 (closed PR): 256 pages
- refs/pull/3/head and /merge: 262 pages each
- refs/pull/4/head and /merge: 262 pages each
- refs/pull/5/head and /merge: 0 pages

### Commits that added or removed the pages (author: Ganesh Shiwakoti)
| Commit | Date | Effect |
|---|---|---|
| 6f55119 | 2026-10-03 | +91 (`external/nonane_raw_nist/`) |
| d3d832e | 2026-10-05 | +154 (`external/bp/nist_raw/`) |
| 8793b06 | 2026-10-05 | +11 (`external/bp/nist_hvap_pts/`) |
| dfcf7ee | 2026-10-06 | +6 (`external/bp/nist_hvap_pts/`) |
| 67e36ad | 2026-10-17 | −262, "Stop redistributing the NIST WebBook pages" |

Every remote branch contains all four adding commits, so every branch's history includes the pages. Commit 67e36ad is only on `revision/v40.31-scientific` and the five `review/*` branches. **It has never been merged into `main`.** The `main` tip (fa6c881, "Created using Colab", 2026-10-21) still serves all 262 pages.

The removal branches carry `external/nist_pages.py` and `external/nist_pages.csv`, which download the pages and verify them against the original copies.

### Archives
I enumerated every historical blob of each tracked archive: LOYOLA_MAIN/FINAL_PAPER/SUPPLEMENT_OVERLEAF.zip and submission_candidate/match/MATCH_OVERLEAF_CANDIDATE.zip, 157 distinct blobs in all.
- No archive has an HTML entry or a file name containing "nist".
- None contains the string `webbook.nist.gov` after decompression.
- No tar or gz files are tracked.

### Releases, tags and assets
- GitHub releases: 0.
- Tags: 0, both through the API and through `git ls-remote`.
- There are therefore no release assets.

### CSVs on main that contain NIST-derived text (described here, not copied)
- `DATA/nonane_provenance.csv`, duplicated as `external/nonane_provenance.csv`: 69 rows (T_B and ΔHvap for nonane isomers), and every `url` points to webbook.nist.gov.
  - `verbatim_snippet` (up to about 100 characters) is a transcribed WebBook summary-table row: quantity, value ± uncertainty, units, method code and comment.
  - `all_determinations` (up to about 4.3k characters) lists every WebBook determination. Each entry has its value, the literature reference (author, year), and NIST/TRC annotations such as assigned uncertainty and method codes.
  - Neither column contains HTML markup. Even so, these are verbatim excerpts of the WebBook compilation, not just values.
- `DATA/boiling_points_provenance.csv` (143 rows) has NIST IDs, the selected values and an `all_determinations` list in the same style.
- These files have NIST URLs and values but no long verbatim text:
  - `DATA/octane_provenance.csv` and `octane_property_provenance_v35.csv`
  - `DATA/calorimetric_dHvap298_alkanes.csv` and `external/bp/calorimetric_dHvap298_alkanes.csv`
  - `external/bp/nist_alkanes_skeletons_audit.csv`
- I did not check whether the removal branches change these CSVs. That is worth confirming.

## 2. Rights: what NIST says

- **WebBook home page** (https://webbook.nist.gov/chemistry/)
  - Copyright in NIST Standard Reference Data falls under the Standard Reference Data Act.
  - The footer shows "All rights reserved" and links to NIST's copyright page.
  - The page says the site "is covered by copyright".
  - NIST also reserves the right to charge for access in the future.
  - The database DOI for citation is 10.18434/T4D303.
- **SRD public-law page** (https://www.nist.gov/srd/public-law, Public Law 90-396, Standard Reference Data Act of 1968, amended by PL 114-329)
  - SRD is copyrighted by the Secretary of Commerce on behalf of the United States, and all rights are reserved.
  - Reproducing, storing or transmitting SRD is restricted "without prior permission".
  - The Act lets the Secretary authorize others to reproduce and publish.
  - The page I fetched did not show the 15 U.S.C. 290 codification itself.
- **NIST copyright page** (https://www.nist.gov/oism/copyrights)
  - General site content is "considered public information".
  - SRD is excepted and handled in a separate statement.
- **SRD copyright, fair use and licensing statement** (https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications)
  - The Secretary may secure copyright in SRD, in the US and in Universal Copyright Convention countries.
  - For licensed SRD it says "licensing information is available at" the SRD site.
  - It gives a recommended citation format.
  - It gives no general fair-use or redistribution grant for SRD.
- **SRD portal** (https://www.nist.gov/srd)
  - Lists the WebBook as a free SRD portal.
  - States no SRD-69 licence terms.
- **WebBook copyright URL**: https://webbook.nist.gov/chemistry/copyright/ returned 404, so it is not a usable source.

**What is established:**
- The WebBook is SRD, it is copyright-asserted, and all rights are reserved.
- NIST's SRD statement requires prior permission to reproduce, store or transmit.
- I found no public licence or permission that covers redistributing archived WebBook pages.

**What is not established:**
- Whether this repo or its authors have any written NIST permission. None is recorded in the repo.
- Whether and how far copyright covers the individual numeric values (facts), as opposed to the compiled pages and annotations.
- Whether the transcribed table rows in the provenance CSVs (values, reference strings, TRC comments) would be acceptable to NIST or fall under fair use.

This is not legal advice. Only NIST, through its SRD office, can authoritatively answer the permission question.

## 3. Immutable release status

- **Tags, releases and DOIs:** none on GitHub.
- **Zenodo:** `q=Singati2` returned 0 hits, and `q="Singati2/LOYOLA-PAPER"` returned 0 hits. `q=LOYOLA-PAPER` returned unrelated "Loyola" records only.
- **How the manuscript cites the repo:** `\bibitem{LoyolaRepo}` in main.tex (line 1664) is "A. Natarajan, G. Shiwakoti, M. Arockiaraj, The Loyola index family: data, scripts and verifiers, \url{https://github.com/Singati2/LOYOLA-PAPER} (2026)". It is a bare, mutable repo URL with no commit, tag or DOI. The origin/main copy is the same.
- **Data-availability text** (wt-val main.tex line 1498): it points to `LOYOLA_supplement.pdf` in the package and says "The release of the package cited here does not include the NIST WebBook pages used; a script ... downloads them and checks each against the copy ...". **This is false today.**
  - No release exists.
  - The cited URL resolves to `main`, which serves all 262 pages.
  - The download script exists only on unmerged branches.
- The origin/main version of the paragraph does not mention NIST at all.

## 4. Remediation options (none were carried out)

| Option | Fixes | Does not fix | Risk | Reversible? | Who approves |
|---|---|---|---|---|---|
| (a) Normal commit that deletes the pages from `main` (for example, merge 67e36ad / PR #5) | `main` tip and default view stop serving the pages, and the availability sentence can become true for `main`/the release | Pages stay in history (4 commits), on 4 other branches, in refs/pull/1–4, and in existing clones and caches | Low; the download script replaces the offline copies | Yes (revert) | All three authors; repo owner Singati2 |
| (b) `git filter-repo` removal of the 3 directories on all branches, then force-push; also delete stale branches | Pages disappear from reachable branch history, and every SHA changes | refs/pull/* (including closed PRs #1 and #2) keep the old commits until GitHub Support purges them; cached commit/blob views also need GitHub Support; forks (none now), local clones, Colab copies and Software Heritage archives may keep copies; any SHA cited anywhere (audit notes, preregistration anchors such as "committed before fitting") breaks | High: it rewrites the provenance timestamps the paper relies on, so the preregistration evidence would need re-anchoring or an archived mapping of old to new SHAs | Practically no (only if a pre-rewrite mirror is kept, which would itself still contain the pages) | All authors; strongly advisable to wait for NIST's answer; repo owner; GitHub Support request |
| (c) Make the repo private | Stops public access at once, including history and PR refs | Copies already made; the paper cites a public URL that reviewers could no longer open | Breaks reproducibility for reviewers unless access is granted | Yes | Repo owner and all authors |
| (d) Leave as is | Nothing | Ongoing public redistribution of copyright-asserted SRD with no recorded permission, and the false manuscript sentence | Rights complaint; credibility with reviewers | n/a | n/a |

**Recommended order:** first (a), done now by merging the removal into `main`. Then ask NIST's SRD office for permission or guidance (the authors decide whether to). Do (b) only if NIST asks for it, coordinating with GitHub Support for refs/pull and caches.

### Release plan proposal
1. The authors approve one commit on `main` after the removal. In that commit, `git ls-tree -r` shows 0 NIST HTML files, and the archives contain no HTML (confirmed above for all existing zip versions).
2. Exclude from the release:
   - `external/nonane_raw_nist/`, `external/bp/nist_raw/` and `external/bp/nist_hvap_pts/`.
   - Any downloaded page cache, which should be gitignored.
   - Pending the authors' or NIST's decision, the long `verbatim_snippet` and `all_determinations` columns, which could be swapped for values plus a WebBook URL and the literature reference.
   - The private or audit notes the authors do not want archived.
3. Keep in the release:
   - `external/nist_pages.py` and `nist_pages.csv` (URLs, retrieval dates, SHA-256), so others can re-download and verify.
   - Citation of the WebBook as Linstrom & Mallard (eds.), NIST SRD 69, doi:10.18434/T4D303.
4. Create an annotated tag (for example `v1.0-match-submission`) and a GitHub release on that commit. Enable the Zenodo GitHub integration first so that it mints a version DOI plus a concept DOI. Check that the Zenodo zip contains no HTML before the DOI is cited.
5. Update `\bibitem{LoyolaRepo}` to give the DOI and tag, and keep the GitHub URL as a secondary pointer.

## 5. Data-availability wording

**True today (no release, no DOI; the pages are still on `main`).** Use this only once the removal is merged into `main`. Until then, the second sentence must be dropped, because it would be false.

> The supplementary sections and tables cited here are in the file `LOYOLA_supplement.pdf` of the reproducibility repository~\cite{LoyolaRepo}, which also holds the data, the scripts and verifiers that recompute every tabulated value, and the nonane and boiling-point protocols, committed before the corresponding models were fitted. The repository does not redistribute the NIST Chemistry WebBook (NIST SRD 69) pages from which the data sets were built; a script in the repository downloads them and checks each against SHA-256 checksums of the copies used.

**If nothing is merged before submission:** keep the first sentence only, and do not mention NIST pages being excluded.

**Once a DOI exists:**

> ... are in the reproducibility package~\cite{LoyolaRepo} (release vX.Y, doi:10.5281/zenodo.NNNNNNN; also at https://github.com/Singati2/LOYOLA-PAPER). The archived release does not include the NIST Chemistry WebBook (NIST SRD 69, doi:10.18434/T4D303) pages; a script in the package downloads them and checks each against SHA-256 checksums of the copies from which the data sets were built.

with `\bibitem{LoyolaRepo}` reading "A. Natarajan, G. Shiwakoti, M. Arockiaraj, The Loyola index family: data, scripts and verifiers, version X.Y, Zenodo (2026), doi:10.5281/zenodo.NNNNNNN."
