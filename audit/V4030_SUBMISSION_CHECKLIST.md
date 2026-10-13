# v40.30 submission checklist

Status as of the adversarial audit. The code repairs are frozen at `01ad6c6` (branch `audit/v4030-adversarial`), and the manuscript edits and audit evidence are on `audit/v4030-edits`. PR #3 is at `716cd37` and `main` at `0c4a4db`; nothing has been pushed beyond PR #3.

Owner key:
- **A** = author decision;
- **R** = run on a machine with enough resources;
- **C** = code or documentation, already done or done by the maintainer.

## Must pass before the release tag `v40.30` is created

| # | Task | Owner | Status |
|---|---|---|---|
| 1 | Merge the audit fixes into the submission line. Merge `audit/v4030-adversarial` into PR #3, or review it as its own PR. | A | pending author approval |
| 2 | Run `python3 verify.py --everything` on the exact commit to be tagged, **with Lean**. It needs `lake` on PATH and about 8 GB of free disk for the Mathlib build; this machine had about 5.6 GB. The run must end `ALL PASS (everything)` with exit 0. `INCOMPLETE` (exit 3) does not count. | R | Without Lean, on 01ad6c6: every executed stage PASS, including the replay of all 53 scripts; ended INCOMPLETE, exit 3 (`verification_logs/v40.30/everything_01ad6c6.log`). With Lean: NOT RUN. |
| 3 | Run `cd formal && bash verify.sh`. It must report 38 theorems with axioms limited to propext, Classical.choice and Quot.sound. | R | NOT RUN at 01ad6c6. Last pass at 3af7f67; `formal/` is unchanged since. |
| 4 | Run the six notebooks on the final commit in a fresh environment. Before the tag exists they need `LOYOLA_ALLOW_MISMATCH=1`; after tagging, run them without it. | R | done at 1d98621 (153 checks, 0 mismatches); rerun on the final commit after tagging |
| 5 | GitHub Actions green on the final commit. This covers the fast path only. | C | green on 716cd37 |
| 6 | Compile both documents with tectonic. Run `audit/check_labels.py` and `audit/check_style.py`. | C | PASS at 1d98621 (40 and 27 pages) |

## Owner decisions before submission

| # | Decision | Owner |
|---|---|---|
| 7 | AI-use disclosure, as MATCH and the authors' institutions require | A |
| 8 | Funding and conflict-of-interest lines; replace the generic acknowledgment | A |
| 9 | Approval of the final text by all coauthors | A |
| 10 | Create and push the tag `v40.30`. Then mint the Zenodo DOI from the tag and cite it in place of the repository URL. | A |
| 11 | Whether to keep the sentence "the untuned pure-imbalance point ... matched the tuned models" in the conclusion. It rests on point estimates, with no equivalence test. A neutral alternative is "came within 0.004 of the tuned models". | A |
| 12 | Redistribution of the KDB and Chemeo acentric-factor values: confirm the terms, or replace them with values from a source that permits redistribution | A |
| 13 | Manuscript length. The main text is 40 pages and the supplement 27. MATCH sets no hard limit known to us, but moving Section 6 detail to the supplement would focus the paper on the collision-order and resolution-limit results | A |
| 14 | The Konstantinova (1996) citation, whose content is unverified (paywalled): check it in a library copy, or cite a source that defines degeneracy explicitly | A |

## Disclosed limitations that stay as limitations

These do not block submission, but must not be described as resolved:

- Seven octane gas-phase entropies match no primary source.
- The tetramethylbutane ΔH_vap has an unresolved reference state, and its ω is a CONFLICT.
- All 18 acentric factors and 29 of the 34 nonane ΔH_vap values exist only in compilations.
- 57 of the 100 boiling points are NIST/TRC averages whose source pages are not archived.
- The novelty statement is an absence claim; its search scope is in `audit/final/NOVELTY_SEARCH_LOG.md`.
- The `press_size` guard rejects defined fits with 1 − h ≤ 1e-6. Such fits are never selected, and the published outputs are byte-identical with and without the guard.
- The predictive conclusions are negative or exploratory. Keep "no demonstrated gain"; do not write "no gain exists" or "equivalent".

## Do not

- merge to `main`, create the tag or mint a DOI without the author's explicit approval;
- change a registered value or a pre-registered endpoint to make a check pass;
- describe an `INCOMPLETE` verification as a full verification.
