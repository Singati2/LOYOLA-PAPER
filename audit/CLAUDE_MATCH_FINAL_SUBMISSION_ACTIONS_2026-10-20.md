# LOYOLA-PAPER — Claude final MATCH submission adjustments

**Date:** 2026-10-20  
**Status:** Instructions for Claude; not a certification of a new run, submission approval, or permission to modify frozen results.  
**Repository:** https://github.com/Singati2/LOYOLA-PAPER  
**Review branch:** `review/match-figure-2026-10-20`  
**Scientific-code reference:** `c48bad05f8e95805d4f0f700f5324d1071b903cd` (as identified in the review guide; check the remote again).  
**Recorded full verification:** `390728b`: `verify.py --full`, 25/25 PASS, 0 FAIL, 0 SKIP, per the repository's verification matrix. This is *recorded evidence*, not an independent rerun by ChatGPT.

## Goal and scope

Prepare the current LOYOLA manuscript and reproducibility release for a defensible submission to *MATCH Communications in Mathematical and in Computer Chemistry*. The scientific centerpiece is the resolution limit of degree-pair / degree-imbalance representations, with certified minimum collision orders 13 (general trees) and 16 (chemical trees), explicit witnesses, carefully attributed ratio-plane discrimination, and the crossing bound. Do **not** present predictive improvement from gamma as the central contribution; the negative and inconclusive predictive findings should remain transparently reported.

**Start by fetching this exact file and reading the referenced repository files. Confirm whether each item is still open on the current remote branch before editing.** This is a targeted change request, not an invitation to redesign the paper.

### Non-negotiable preservation rules

- Do not modify registered datasets, pre-registrations, hypotheses, parameters, seeds, numerical outcomes, frozen analyses, exact mathematical statements, or Lean certificates just to improve the presentation.
- Do not invent additional results, new novelty claims, or experimental confirmations.
- Do not interrupt running jobs or independently launch `verify.py --everything`, the long Colab stage 07, or expensive experiments without explicit approval.
- Preserve manuscript and supplement copies, existing audit logs, the shorter draft, and provenance. Work in a separate review worktree/branch where possible.
- Never force-push, rewrite Git history, merge into `main`, erase historical evidence, make the repository private, redistribute archived NIST pages, or submit the paper without express author authorization.
- Do not put tokens in Git URLs, argv, error messages, notebook outputs, committed logs, or shell history. Keep NIST caches private.
- Separate **confirmed defect**, **stale documentation**, **not yet tested**, and **requires author/legal decision** in every report.

## P1 — Fix false-positive replay completion and source/output trust

**Inspect:** `colab/pipeline.py`, `audit/run_all_scripts.py`, `colab/README.md`, and the relevant existing tests. The code at the inspected commit uses `run_script()` to discover written files dynamically and uses `validate()` / `report()` to check recorded outputs. A script's status currently depends on exit 0 plus detected writes (or inclusion in `CHECK_ONLY`); validating only self-reported output files is not the same as independently verifying the expected outputs.

**Required changes:**
1. Define an authoritative **expected-output inventory per script**, with explicit handling of scripts that are check-only, generate no persistent output, produce optional artifacts, or have genuinely dynamic names. Keep it reviewable and version-controlled; avoid deriving the expectation solely from the same observed write list that is being checked.
2. Make a successful script record require its expected files to exist and be authenticated (path, hash and provenance), and reject missing, altered, unlisted or inappropriately empty output sets. Consider intermediate scripts that rewrite tracked files and the intentional exclusions for private NIST source pages.
3. Validate input fingerprints and prior-stage dependencies, and make reusing cached results fail closed when the output inventory, source fingerprint, run record, or saved artifact is absent or corrupted.
4. Harden `check_clean()`: a tracked source modification must never be accepted merely because the path appears in a state index. Distinguish an authorised, hash-validated generated output from a source file even if an adversary adds a forged index entry. Handle deleted and renamed tracked files as well as modified files.
5. Make `--report` emit `COMPLETE` only if **all planned scripts**, authoritative expected outputs, input provenance, fingerprints and status records are valid, the output comparisons satisfy the documented policy, and unexecuted cross-checks are explicitly distinguished. Do not call it a complete replay of *all* paper scripts when two independent checks remain outside the plan.
6. Fail safely on malformed state files, forged/corrupted markers, unknown paths and unsafe path traversal. Do not allow a cached record to turn a failed/incomplete run into PASS.

**Required adversarial regression tests (small synthetic fixtures; no expensive computation):**
- Exit code 0, but one required output was never generated: FAIL.
- Empty, truncated, deleted or replaced cached output: FAIL / rerun as appropriate.
- Forge `files.json` to whitelist a modified tracked source: FAIL.
- Script returns 0 and writes only an unexpected scratch file: FAIL when its required output is missing.
- Missing stage record, tampered fingerprint, modified upstream input, corrupted JSON, or mismatched commit: FAIL / STALE.
- Legitimately regenerated tracked outputs and independent check-only scripts remain supported.
- A clean, fully mocked/synthetic pipeline meeting the contract reports COMPLETE.

Document the before/after attacks and exact commands/results. Do not claim real Colab or full replay execution from mock tests.

## P1 — Correct cover-letter novelty without changing theorems

**Inspect:** `submission_candidate/match/COVER_LETTER_DRAFT.md`, `main.tex`, `audit/final/NOVELTY_SEARCH_LOG.md`, and `docs/match/07_ETHICS_LICENSE_AUTHOR_DECISIONS.md`.

- The cover-letter draft currently presents path/star extremality in its list of 'new content'. Check its literature attribution in the manuscript; **remove it from the novelty list** if already established. It may be included as a contextual result with an accurate citation, not marketed as a new theorem.
- Credit Rada appropriately for the degree-pair linearity/span fact and any inherited separation theorem. Do not call the existing linearity result a new discovery.
- Put the **minimal collision orders (13 and 16), explicit witnesses, scope of exact certification, and the crossing bound** first; describe the ratio-plane finding precisely, distinguishing a result proved here from a consequence of prior work. Preserve any algebraic-gamma qualification.
- Retain the experimentally negative/non-equivalence caveats. A failure to show gamma's gain is *not* proof of equivalence or proof it can never help.
- Review the companion-paper disclosure and bracketed author confirmations without asserting unverified publication/submission status or changing author names/order.

**Acceptance:** Cover letter matches the claims and attribution in the actual candidate manuscript, contains no unsupported originality claim, and retains placeholders for items only coauthors can authorise.

## P2 — Synchronise submission release, page counts and verification provenance

**Inspect:**
- `README.md`, `REVIEWER_START_HERE.md`, `REPRODUCE.md`;
- `docs/match/11_VERIFICATION_AND_RELEASE_MATRIX.md`;
- `docs/match/10_COLAB_REPRODUCIBILITY_TEST.md`;
- `submission_candidate/match/README_SUBMISSION.md`;
- `submission_candidate/match/CLEAN_SUBMISSION_MANIFEST.md`;
- actual `submission_candidate/match/` PDFs, `.tex` files, and `MATCH_OVERLEAF_CANDIDATE.zip`.

**Known discrepancy at inspection:** The submission README says **45 main-paper pages**, while the matrix's logged clean-extraction build says **44**. Determine which is correct **from the actual final PDF(s) and fresh clean-extraction build**, not from historical notes. Also verify 27 supplement pages and the location/number of the main degeneracy figure. If a mismatch exists, rebuild only the submission artifacts required for consistency; do not alter datasets or numerical scientific content.

- Cross-check all displayed page/figure counts, filenames, bibliography state, clean build, and SHA-256 hashes; regenerate the manifest when content actually changes.
- Add a **final release row** in the verification matrix naming the exact scientific-code commit, notebook commit(s), documentation/submission commit(s), commands run, environment, outcome and limitations. Distinguish a run's tested commit from descendant documentation-only commits; do not misrepresent them as having been directly rerun.
- Confirm the final reviewer links work from a browser without authentication if the repository is public, and that each notebook's embedded PIN matches the intended code. A GitHub branch tip is not itself a stable, reproducible pin.
- Fix stale 'not pushed' instructions if the branch is already remotely present. Conversely, do not claim any future unpublished update is public until confirmed.
- Ensure the citations in the manuscript/cover letter use an **exact commit or approved archival DOI**, not just a moving repository root.
- Synchronise the short manuscript only if it is intentionally part of the proposed submission; otherwise clearly label it as a separate draft, not a release artifact.

**Acceptance:** A reader can identify exactly what source, notebook, submission zip and PDF belong together, which checks were run against which commits, and how to reproduce the documented results.

## P2 — Real Google Colab smoke test (do not fabricate)

The existing matrix records locally simulated Colab-style runs of the essential notebooks, but **no actual hosted Google Colab test**. An AI operating without access to a real Colab runtime must leave the status as NOT TESTED and give the user exact manual steps.

When the user can run Colab:
1. Run fresh, clean runtimes for essential `notebooks/01`–`06` (with fast settings and only as resources permit), plus `colab/12_enumeration_certificates.ipynb`.
2. At minimum, test `colab/00_setup_and_plan.ipynb` for Python 3.13 provisioning, pinned commit, dependency lock consistency, Drive setup where appropriate, and clean checkout handling.
3. Capture notebook URL, commit PIN, Python/package versions, final assertion summary, failure logs, and whether any cell was skipped.
4. Record actual PASS/FAIL/NOT TESTED per notebook, not an aggregate blanket claim. Leave the full staged replay and unrun independent cross-checks explicitly unverified.

**Do not** start the 12-hour stage or `--everything` simply to make the release look stronger. Request author approval first.

## P2 — Transparent data and publication disclosure (author decisions)

Review `docs/match/07_ETHICS_LICENSE_AUTHOR_DECISIONS.md`, `DATA/README.md`, the provenance ledger, and manuscript limitations. Preserve the registered numbers:

- **58 aggregate-derived boiling-point values** = 57 direct averages + 1 mean of two averages.
- Clearly disclose derivative/compilation-only values, conflicting sources, unresolved reference states, and checks that were not freshly repeated.
- Do not silently remove, alter, resample, or 'correct' data to improve predictive performance.
- Public NIST WebBook pages in `main`/history and KDB/Chemeo redistribution terms require an **author/legal decision**; do not unilaterally rewrite history, delete prior pre-registration commits or redistribute the pages. Keep the clean submission package free of restricted source pages.
- Obtain actual approval from every coauthor; confirm author order, spelling, affiliations, corresponding author, acknowledgments, final title, and companion-manuscript disclosure. These cannot be auto-certified by a code audit.
- Verify MATCH's current author/submission instructions before asserting publication rules; do not mark the paper SUBMITTED.

## Deliverable and safe workflow

1. Fetch the remote review branch and inspect the latest commits; do **not** work from old `main` by accident. Record your starting SHA and any existing uncommitted changes. Leave other worktrees and running processes alone.
2. Create a distinct local review worktree and incremental branch for proposed implementation; never force-push or silently merge. Preserve exact before/after diffs and tests. Do not update pinned notebooks until the final *scientific/code commit* is settled.
3. Implement only confirmed P1/P2 technical and editorial corrections. Put author/legal choices in a separate unresolved-decision table instead of guessing.
4. Run cheap unit, adversarial and document consistency tests first. Run appropriate existing fast verification only if warranted by modified code and resources; use `--full` only when its coverage is needed. Do not launch expensive tests or real Colab on the author's behalf without an available, explicitly authorised environment.
5. Prepare `audit/CLAUDE_FINAL_MATCH_CHANGE_REPORT.md` summarising: starting and ending SHAs; changed files; each issue and disposition (FIXED / UNCHANGED-WITH-JUSTIFICATION / AUTHOR DECISION / NOT TESTED); tests with actual exit codes; preserved datasets/outcomes; remaining limitations; and suggested release artifacts.
6. **Before pushing any implementation changes**, show a concise diff summary and test evidence for author review. Do not merge, tag, archive or submit without approval.

### Final checklist

- [ ] Replay cannot report COMPLETE with missing expected outputs or tampered source/state.
- [ ] Adversarial false-positive tests fail as intended; valid synthetic replay succeeds.
- [ ] Cover-letter originality and earlier-work attribution corrected.
- [ ] Final PDF, TeX build, zip, page counts, figure references and SHA-256 manifest agree.
- [ ] Release matrix records exact commits, commands and limited verification scope.
- [ ] Reviewer notebook links and pinned code are valid.
- [ ] Real Colab status accurately recorded, including NOT TESTED where appropriate.
- [ ] Data/provenance caveats and 58 aggregate-derived values preserved.
- [ ] Companion, licensing and coauthor approvals marked pending until genuinely resolved.
- [ ] No protocol or registered result changed; no force-push/history rewrite; no submission performed.

**Definition of done:** A small, verifiable correction set suitable for all authors to review, with release-level evidence and no inflated mathematical novelty, experimental certainty, or reproducibility claim. The publication decision belongs to the authors and MATCH's editors.
