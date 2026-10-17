# Submission decision checklist (2026-10-17)

## Blocking (must be closed before submission)

| # | Item | Owner | State |
|---|---|---|---|
| B1 | Coauthor approval of the short version, its new title and its framing | all authors | open |
| B2 | Decide whether the full version is retired as a submission (recommended) or kept as a technical report in the repository | authors | open |
| B3 | Public code and data location without the NIST history. Options: a new public repository from the cleaned tree (recommended); make the original private; or rewrite history (not recommended). See `VERIFICATION_AND_NIST_STATUS.md` | owner of `Singati2/LOYOLA-PAPER` | open; **needs separate explicit approval** |
| B4 | Provenance CSVs and the C4–C16 skeleton census: keep, regenerate locally, or withdraw | authors | open |
| B5 | Review and approve the manuscript corrections on `review/short-version` (attribution and statistics), then decide whether they also go onto `revision/v40.31-scientific` | authors | open |
| B6 | Run `verify.py --full` on the commit to be submitted, and create the immutable tag the notebooks pin (`notebooks/gen_notebooks.py` expects a tag) | maintainer | `--full` on `67e36ad` RUNNING; tag not created |
| B7 | The data-availability sentence must name the final repository and commit or tag | authors | open |

## Non-blocking (would strengthen the paper)

| # | Item |
|---|---|
| N1 | Add the Δ ≤ 3 theorem (proof in `NOVELTY_AND_PROOF_MATRIX.md`) and the per-Δ first-order table (`certificates/by_delta.py`) |
| N2 | Add the conditional intervals for ridge against single indices on the boiling points (exploratory; new registry entries) |
| N3 | Cite Öz–Gutman 2025 (angle parametrisation of SDD, ISDD and SO₂) and Kırgız 2027 (hyperbolic Sombor, a ratio index), and Balaban–Quintas (smallest degenerate trees for J) as a genre precedent |
| N4 | Say explicitly that the QSPR data sets (n ≤ 10) lie below the collision orders, so the experiments do not test the theorem |
| N5 | Re-key `LEAN_VERIFICATION.md` and the prose registries to the short version if it becomes the submission |
| N6 | Remove the C4/C5/C11–C16 census dependency if B4 withdraws it, and update Section S9 |

## Decisions that are only the authors'

* Title of the short version (proposed: "The Loyola Index Family and the Resolution Limit of
  Degree-Ratio Indices on Trees").
* Whether to keep the QSPR section at its current length or cut it to a page with the boiling-point
  result.
* Journal order: MATCH first, Journal of Mathematical Chemistry as fallback (`FINAL_PUBLICATION_READINESS_2026-10-17.md`).

## Approvals requested (separate; approval of one is not approval of another)

1. Push `revision/v40.31-scientific` (`a609843`, audit fix) and `review/short-version` (review commits)
   to GitHub, without force.
2. Any merge into `main` or change to `main`.
3. Any NIST history or visibility action (B3).
