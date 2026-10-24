# Is the local audit (`3a5f061`) genuine? Claims and evidence, 2026-10-23

**Brief:** `docs/CLAUDE_VALIDATE_LOCAL_MATCH_AUDIT_AND_IMPLEMENT_2026-10-23.md`, pushed as `4f64671` by the repository owner's account. It is unsigned, like all commits in this repository.

**Provenance of the brief:**
- The push is recorded in GitHub's activity log as `Singati2`, `2491f0e → 4f64671`, at 2026-10-24 00:59 UTC.
- The commit adds only that file, built on `2491f0e`.
- It asks for nothing unsafe and repeats the no-push rule.

## 1. The commit exists and is complete

| Check | Result |
|---|---|
| Commit | `3a5f06168ddc1f9c066fb1f914ed65a1f7fff44b`, parent `3904e3896052ea92cca149477c7011f227330814`, author Ganesh Shiwakoti, no trailers |
| Branch | `review/match-literature-writing-audit-2026-10-23`, local only; `git ls-remote` returns nothing for it |
| Files changed | 35. Breakdown: manuscript sources and their 3 bundle copies plus the submission copies; 2 PDFs plus 2 copies; 4 zips; `README.md`; cover letter; `SHA256SUMS.txt`; submission manifest; `prose_claims_a.py`; `constancy_test_check.py`; 6 recompute scripts; the 2491f0e brief; 6 audit reports |
| The six named audit files | all present and read in full |
| Working tree | clean (0 changes) when this audit started |
| New worktree | `wt-val`, branch `review/match-audit-validation-2026-10-23`, from `3a5f061`. `3a5f061`, the public branch, `main`, the 46-page copy and `wt-mainrevert` were not modified |

Nothing was missing, so nothing was reconstructed.

## 2. Claim matrix

**Status:**
- **VERIFIED**: independently checked and correct.
- **PARTLY**: correct in substance, with a qualification.
- **FALSE**: wrong.

| # | Claim made by the earlier audit | Supporting diff or lines | Independent check | Status | Action |
|---|---|---|---|---|---|
| 1 | Credits to Rada, Cruz–Rada and Rada–Rodríguez–Sigarreta match the full texts at the cited locations | intro (i), Theorem 2 attribution, Proposition 7 | Rada 2019 Table 1, Def. 2.3, Prop. 2.5, Thm 3.4 and Cor. 3.5 re-read in the full text for this audit. The Cruz–Rada and RRS checks are recorded in the references report | VERIFIED (Rada re-read); the rest rest on the earlier full-text check | — |
| 2 | Rada 2019 Corollary 3.5 makes $e^{GA}$ separate exactly the q-histograms, for graphs of equal order | main.tex remark after the degree-ratio corollary (L3) | Proof that the GA partition of $K$ equals the $q$ partition, with an exact rational check for $n \le 60$; conditions (equal order, orientation, $(1,1)$, GA versus $e^{GA}$) examined | **VERIFIED** (`MATCH_RADA_Q_HISTOGRAM_PRIOR_ART_2026-10-23.md`) | keep L3; author sign-off |
| 3 | No earlier determination of orders 13 and 16 was found; the search statement was narrowed | L2 | Queries listed in the novelty matrix §0 and in `audit/final/NOVELTY_SEARCH_LOG.md`. A search that finds nothing does not prove novelty, and the text says "we found no" | VERIFIED as a search result, not as novelty | — |
| 4 | 56 main and 21 supplement entries match the records, in alphabetical order | bibliography | `grep -c \bibitem` gives 56 and 21. The record-matching rests on the earlier Crossref/OpenAlex/arXiv check. The two entries added (Ediz, Mondal et al.) were re-checked by arXiv ID and DOI | VERIFIED (counts and new entries); PARTLY (full re-match not repeated) | — |
| 5 | No unsupported citations and no copied passages | references report | Not repeated in full. Gao–Gao and Gutman–Buragohain–Nyauli remain unverifiable because they are paywalled | PARTLY | listed as a gap |
| 6 | Decane result −0.072, 15/50, [−0.156, +0.001] | Table 5 and text | Reproduced exactly by `decane_indep.py`. A second implementation with explicit refits matches the repository's per-seed $Q^2$ to $5\times10^{-11}$ | **VERIFIED** | — |
| 7 | Pooled result −0.0001, 25/50, [−0.003, +0.002] | Table 5 and text | `pooled_indep.py` gives −0.00011, 25, [−0.0026, +0.0019]; per-seed $Q^2$ identical to the repository | VERIFIED (one independent implementation) | — |
| 8 | $Q^2 = 1 - \mathrm{PRESS}/SS_{tot}$ about the full-sample mean; ordinary and nested LOO labelled correctly | Section 6, Table 5 and Table S7 captions | Code read. The base $Q^2 = 1-(34/33)^2$ identity holds only with the full-sample mean. Column-by-column check of which columns are nested | **VERIFIED** | — |
| 9 | Tetramethylbutane: 10.263 gives 0.37353; excluded 0.980; hypothetical liquid 0.976 against 0.970 | Section 6.1 | Recomputed: 0.37353, 0.97987, 0.97607 and 0.96958 | **VERIFIED**. Data-file note: the CSV row labelled 10.263 lists 0.3736 (unrounded input). Not changed | — |
| 10 | Tables 1–5, Figure 1 and S7 match their sources | tables | 140 cells compared by script, 0 mismatches; Figure 1 bar labels match | **VERIFIED** | — |
| 11 | Only wording, captions, attributions and documentation changed; no result, data or figure | full diff | The only number that changed is 10.26 → 10.263. No data, protocol, seed or figure file changed. Code changes are limited to the registry anchor and the guard's allowlist | **VERIFIED** | — |
| 12 | "Values cross" is correct | W1–W7 | Proposition 4 bounds the zeros of $LO(G)-LO(H)$ along γ | VERIFIED | keep; sign-off for W4–W5 |
| 13 | Chemical graph and chemical tree definitions are consistent | D1 | Δ ≤ 4, connected (Section 2), and enumeration as trees with Δ ≤ 4 | VERIFIED | sign-off |
| 14 | Octane data source cited | R1 | These are the two compilations the supplement uses (Section S1) | VERIFIED | — |
| 15 | Table 1, 5 and S7 captions | C1, C2, X2 | Both pairs differ in all 10 comparisons. The LO_h box, (−12,12)² × (−2,2), and the 2000 candidates match `bp_tests.py` and `PREREG_v40.md`. The S7 nesting matches the generator | VERIFIED; "per seed" means per model and seed | caption clarified |
| 16 | "0.745" relabelled as "the best fixed index chosen within each fold" | S1 | Recomputed: 0.7455. Within the folds ${}^mM_2$ is picked 17 times and $LO(0,0,1)$ once. It is a nested LOO correlation, which the sentence already says | VERIFIED | — |
| 17 | Supplement cross-reference corrected | X1 | It renders as "Table S6", which is the search-box table. The sentence is in Section S3; the earlier patch log said "S6" | VERIFIED; location misnamed in the log | noted here |
| 18 | README and cover letter aligned | README novelty paragraph, cover letter W1 | The README now matches the paper. The cover letter's "NIST WebBook source pages are not redistributed" is **false** for the cited URL | PARTLY | cover-letter sentence withheld |
| 19 | Availability sentence: "The release of the package cited here does not include the NIST WebBook pages" | E1 | No tag, release or DOI exists. The cited URL opens `main`, which serves 262 NIST pages, and the download script is not on `main` | **FALSE** today | sentence removed; author decision |
| 20 | 37/39 pages | PDFs | `pdfinfo` gives 37 and 39. The growth from 35 to 37 came in `3904e38` (Lemma 1 proof restored, referee caveats added) | VERIFIED | — |
| 21 | Lab name is "Machine Perception and Cognitive Robotics" | acknowledgment | The lab's own site (mpcrlab.com) uses that title; FAU news pages say "MPCR lab" | VERIFIED | unchanged |
| 22 | First fast verifier run failed at the guard; it passed after the allowlist change | guard | Log line reproduced. Negative controls T1–T3 fail as expected, T4 passes | **VERIFIED**; the relaxation is narrow (`MATCH_VERIFIER_GUARD_INDEPENDENCE`) | kept |
| 23 | `ss_indep.py` (shipped) reproduces Table 3 | recompute script | It crashed at IRLA because of a `None` placeholder | **FALSE** as shipped | fixed; output matches 0.4565, 0.4579, 0.2745 |
| 24 | Clean ZIP rebuild gives text identical to the PDFs | packaging | Rerun on this branch: True for both | VERIFIED | — |

**Summary:** 19 VERIFIED, 3 PARTLY (items 4, 5 and 18) and 2 FALSE (items 19 and 23). Both false items are fixed on this branch. Item 19 still needs the release decision before any NIST or availability wording can be restored.
