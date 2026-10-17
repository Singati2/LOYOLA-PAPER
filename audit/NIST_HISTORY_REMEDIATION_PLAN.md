# NIST pages in the git history: remediation plan (for approval; nothing here has been carried out)

## Situation (2026-10-17)
* The 262 NIST Chemistry WebBook pages (NIST SRD 69) were removed from the tracked tree of
  `revision/v40.31-scientific` in the cleanup commit (see `NIST_REDISTRIBUTION_AUDIT.md`). They
  remain in the history: 72 of the 82 commits on all refs contain them, from `6f55119` (2026-10-03)
  onward.
* Every branch on GitHub still has the pages at its tip, except `revision/v40.31-scientific` after
  the cleanup: `main`, `audit/provenance-final`, `audit/v4030-adversarial`,
  `research/weak-discrimination` and `robustness-guards`.
* GitHub also keeps read-only pull-request refs (`refs/pull/1` to `refs/pull/5`, 8 refs). The owner
  cannot rewrite or delete them; only GitHub Support can.
* The repository is public, with 0 forks, no tags and no releases. No Zenodo archive exists. Anyone
  who cloned it before the rewrite keeps a copy, and nothing can recall such copies.

## Options, in increasing order of effect
1. **Make the repository private now** (`gh repo edit Singati2/LOYOLA-PAPER --visibility private
   --accept-visibility-change-consequences`). This stops further public access to every commit at
   once and is reversible. It breaks the public Colab links and the GitHub URL cited in `main.tex`
   until the repository is public again.
2. **Rewrite the history** with `git filter-repo --invert-paths --path external/bp/nist_raw --path
   external/bp/nist_hvap_pts --path external/nonane_raw_nist` on a fresh mirror clone, then
   force-push every branch.
   * Every commit SHA from `6f55119` onward changes.
   * The commits cited in the paper and the pre-registrations change too: `a5cf378` (the
     boiling-point rule) and the nonane protocol commit. The time-stamp evidence of
     pre-registration rests on those SHAs and their GitHub push times. A rewrite keeps the commit
     dates but not the SHAs. The paper and the PREREG files would then need a mapping table from
     old to new SHAs, and an external reader could no longer confirm the original SHAs on GitHub.
   * Open PRs #3 to #5 would have to be closed and reopened.
3. **Ask GitHub Support** to purge the cached views and the `refs/pull/*` refs. This is needed only
   after option 2, because those refs survive a force-push.

## Recommendation
Do option 1 now, and do not rewrite history. The pre-registration evidence (commit `a5cf378` and
the nonane protocol commit, with their GitHub push times) is part of the paper's scientific claim.
A rewrite would destroy it. Once the repository is private, the pages in the history are no longer
publicly distributed. Before the repository is made public again for submission, choose one of the
following:

* **(a) Publish a new public repository.** Start it from the cleaned tree of
  `revision/v40.31-scientific` as a single initial commit, or as a filtered copy. Keep the original
  repository private as the time-stamped record, and let the paper name the original SHAs as
  verifiable on request. This keeps the evidence intact, publishes no NIST pages, and needs no
  force-push.
* **(b) Rewrite the original repository (option 2),** and accept the loss of the SHA evidence
  described above.

Each of these steps needs your explicit authorization: changing the visibility, any force-push,
deleting a branch, opening a GitHub Support request, creating a new repository.
