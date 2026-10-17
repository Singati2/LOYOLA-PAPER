# Final publication readiness: Loyola paper (2026-10-17)

## Verdict

| Version | Verdict |
|---|---|
| Full (`main.tex`, 43 pages, plus a 28-page supplement) | **NO-GO as a submission.** Most of its theory is known mathematics, its length is out of proportion to its new content, and it reads as a new-index paper |
| Short (`drafts/short`, 24 pages, plus a 33-page supplement) | **REVISE, then a conditional GO for MATCH as a short paper.** The surviving new mathematics is real but narrow and computational. The blocking items in the checklist must be closed first |

Passing verification scripts is not the basis of this verdict. The scripts show the numbers are
reproducible. They do not show that the contribution is new or significant. The judgement below rests
on primary-source comparison and independent proofs and enumerations.

## The single most defensible new theorem

For unlabeled trees, the edge degree-ratio histogram (equivalently the multiset of q_uv) determines the
degree-pair profile up to order 12, and for trees with maximum degree at most 4 up to order 15. At
orders 13 and 16 there are explicit trees with distinct profiles and equal histograms. A pendant-path
attachment extends them to every larger order with the same maximum degree. Consequently every
degree-ratio index (GA, AG, SDD, ISDD, exponential GA and ISDD, diminished Sombor, DRSO, hyperbolic
Sombor) fails simultaneously from those orders on; individual indices can fail earlier (SDD at order 9,
ISDD at 10).

| Aspect | Status |
|---|---|
| Minimal orders | **VERIFIED** by independent enumeration (`audit/certificates/`) and by the repository's own exact verifier |
| Witnesses and all-order construction | **VERIFIED** by proof and executable check |
| Novelty | **PARTIALLY VERIFIED**: not found in Rada 2019, Rada 2026, RRS 2022 and its forward citations, the DRSO papers, the GA survey, OpenAlex or arXiv. Google Scholar "cited by" was not checked. The method is RRS 2022 Example 2.2 transferred from degree-sum classes to degree-ratio classes, and the class-wide consequence is a one-line corollary of Rada 2019 Proposition 2.5 |

## Known against new (details: `audit/NOVELTY_AND_PROOF_MATRIX.md`)

* **Known, and now credited in both versions:**
  * q-histogram dependence: Rada 2019, Proposition 2.5;
  * algebraic-γ separation: Rada 2019, Theorem 3.4;
  * generic discrimination;
  * the ceiling;
  * log-convexity and identifiability;
  * the extremal trees, a corollary of Cruz–Rada 2019 Theorems 2.1 and 3.1, with a complete check
    written out;
  * closed forms and termwise bounds (routine).
* **New but computational:** the minimal orders 13 and 16, the witnesses, and (not yet in the
  manuscripts) the per-Δ table: none for Δ ≤ 3, 16 for Δ ≤ 4 and Δ ≤ 5, 13 for Δ ≥ 6.
* **New and proved by hand, small:** Δ ≤ 3 trees never collide; parent distinctions survive at rational
  exponents; the Laguerre crossing bound with a sharp example at Δ = 6.

## Key strengths

1. A precise, checkable combinatorial statement, with certificates that run in about a minute and a
   Colab notebook (`audit/certificates/collision_orders_colab.ipynb`).
2. Honest negative QSPR results under pre-registered protocols, with the post-hoc changes tabulated.
3. A reproducibility package with offline CI, exact verifiers and a Lean formalisation of the
   elementary inequalities.

## Top five weaknesses

| # | Weakness | Type |
|---|---|---|
| 1 | **Incremental novelty.** The theorem is a finite search for the smallest trees realising known kernel directions; there is no structural explanation of why 13 and 16 | **Blocker for the full version.** For the short version a referee risk, partly answered by the Δ ≤ 3 theorem and per-Δ table (proposed addition) |
| 2 | **Weak chemical relevance of the threshold.** The data sets have n ≤ 10, where the collisions do not occur, so the QSPR part does not test the theorem. Real degeneracy at n ≥ 13 is dominated by equal-profile isomers | Improvement: say it explicitly. MATCH requires "a clear connection to chemistry" |
| 3 | **Attribution errors in the committed full paper.** It contrasts part (ii) with Rada 2026 Example 3 instead of crediting Rada 2019 Theorem 3.4, understates Cruz–Rada, and omits RRS 2022 Example 2.2 as the template | **Fixed on the review branch**; it was a blocker |
| 4 | **Statistical overstatements in the committed full paper and supplement:** "understate several-fold", unscoped ridge superiority, "linear term is what matters", the Wiener reading, a nonane ridge claim contradicted by its own intervals | **Fixed on the review branch**; it was a blocker. The intervals for ridge against the indices are still absent (improvement) |
| 5 | **Data licensing and history.** The NIST pages are in 72 of 82 public commits. The provenance CSVs and skeleton census are unresolved. The paper cites a public URL whose history contains them | **Blocker** before a public repository link goes into a submitted paper (decision needed; see `audit/VERIFICATION_AND_NIST_STATUS.md`) |

Further open questions:
* Whether the choice γ ∈ {1, 2} predates the octane data. It cannot be documented, and both texts now
  disclose this.
* No equivalence margin was registered, so no equivalence claim is possible. The texts say so.
* The Lean map (`LEAN_VERIFICATION.md`) is keyed to the full paper.

## Journal recommendation

* **MATCH (first choice).** Its stated test is: "A paper acceptable for publication must contain
  non-trivial mathematics or communicate non-routine computer-based procedures AND have a clear
  connection to chemistry" (match.pmf.kg.ac.rs, checked 2026-10-17).
  * The minimal-order result fits "non-routine computer-based procedures", and MATCH has published
    the closest prior work: Rada 2019, RRS 2022, and Balaban–Quintas on the smallest degenerate trees
    for J.
  * No APC. LaTeX with the MATCH template is mandatory and is already used. No length limit is
    stated.
  * The degree-ratio indices (DRSO, GA, SDD) are actively studied there, so the result is relevant to
    its readers.
  * No MATCH editorial restricting new-index papers could be found. The often-quoted Gutman view is a
    personal communication reported in a 2018 paper and must not be cited as policy.
* **Journal of Mathematical Chemistry (fallback).** Broader scope; mandatory data-availability
  statement; preprint-friendly; median 12 days to first decision (journal homepage). It does not
  mention topological indices, so the fit for this topic is weaker.
* No acceptance probability is given; none can be substantiated.

## Recommended submission strategy

1. Authors decide:
   * the short version as the submission, with its title;
   * whether to add the Δ ≤ 3 theorem and per-Δ table (recommended; about one page, already
     certified);
   * the NIST and repository route.
2. Close the blocking checklist items: coauthor approval; public repository without the NIST history
   (new repository from the cleaned tree is recommended); provenance-CSV decision; tag for the notebook
   revision; a data-availability sentence matching the chosen repository.
3. Optionally add the ridge-against-index conditional intervals (exploratory, registry entry
   required).
4. Submit the short version to MATCH by e-mail. Do not post a preprint without checking with the
   editors, because MATCH requires that "the same or similar article has not been published
   previously".
