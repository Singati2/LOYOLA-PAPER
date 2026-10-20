# 07 — Ethics, licensing and author decisions

Nothing in this file has been acted on. Every item is for the authors (and, for licensing, legal advice);
no repository visibility, history, branch, licence or authorship change was made, nobody was contacted, and
nothing was submitted.

## 1. NIST Chemistry WebBook pages (SRD 69)

Verified state (2026-10-20, `git ls-tree` per remote ref):

| Ref | Tip | Raw NIST HTML pages tracked |
|---|---|---|
| `origin/main` (default branch) | `0c4a4db` | 262 |
| `origin/audit/v4030-adversarial` | `f109127` | 262 |
| `origin/audit/provenance-final` | `716cd37` | 262 |
| `origin/robustness-guards` | `01bfaf5` | 262 |
| `origin/research/weak-discrimination` | `41db8c1` | 262 |
| `origin/revision/v40.31-scientific` | `67e36ad` | 0 |
| `origin/review/corrections-impl-2026-10-19` and this candidate | — | 0 |

The repository is public. The pages remain in history (from `6f55119` onward) and in GitHub's read-only
pull-request refs. Each 262 = 154 (`external/bp/nist_raw`) + 91 (`external/nonane_raw_nist`) + 17
(`external/bp/nist_hvap_pts`).

Separate questions:

1. **Legal:** whether the past and present public distribution of the pages is permitted under NIST's
   terms. Needs legal advice; not decided here. The authors' instruction stands: NIST is not contacted and
   the pages are not redistributed.
2. **Distribution risk:** the default branch `main` (v40.29) still tracks all pages, and it is what the
   paper's repository citation opens (`main.tex`, `LoyolaRepo`: bare URL). Options with their consequences
   are in `audit/NIST_HISTORY_REMEDIATION_PLAN.md` (private repository now; new clean public repository; or
   history rewrite). Each needs explicit author authorisation.
3. **Pre-registration evidence:** the paper cites commits `964b127` (nonane protocol) and `a5cf378`
   (boiling-point rule) as time-stamped evidence. Both are in the page-bearing history. A history rewrite
   changes these SHAs and breaks that evidence; the remediation plan recommends against it.

## 2. KDB / Chemeo values

`DATA/README.md:39-42`: Chemeo's terms (consulted 2026-10-16) permit value-by-value use with citation and
forbid bulk download or redistribution of the database as-is; the KDB terms could not be retrieved. The
acentric factors (18 values) and their alternatives are in `octane_property_provenance_v35.csv` and
`DATA/octane_provenance.csv`. Removing HTML pages does not settle this. AUTHOR/LEGAL DECISION: whether the
curated values may stay in a public repository with attribution. The submission package
(`submission_candidate/match/`) contains no data files.

## 3. Overlapping work by the same authors

`github.com/Singati2/topological-index-orthogonality` (public; README read 2026-10-20) describes the manuscript
"Ten Edge-Degree Counts Are All a Degree-Based Topological Index Can See: An Exact Redundancy Certificate
and What It Leaves for New Molecular Descriptors" (G. Shiwakoti, A. Natarajan, M. Arockiaraj, v2.1, "in
preparation"). It states the degree-pair span of bond-incident-degree indices (crediting Rada, MATCH 96
(2026)) and reports a census including "400 points of the Loyola family". The LOYOLA manuscript does not
cite or mention it. The TopoQSPR project of the same group (`Singati2/TopoQSPR`) also relies on the
edge-type-count span and names this companion manuscript as its main overlap risk.

MATCH ethics page: a submission must not be under consideration elsewhere at the same time, and others'
work (including one's own) must be cited. AUTHOR DECISION:

* confirm that neither related manuscript is submitted anywhere while this one is under consideration;
* cite the companion manuscript (as "in preparation" or its repository) where the LOYOLA paper uses the
  degree-pair ceiling, or state the relation in the cover letter;
* ensure no text is reused between the manuscripts without attribution.

## 4. Authors, affiliations, correspondence

As in `main.tex:178-185` and `supplement.tex:150-157` (identical; the short draft also identical):
Advik Natarajan (a, Department of Mathematics, Oregon State University), Ganesh Shiwakoti (b, Department
of Mathematics and Statistics, Florida Atlantic University), Michael Arockiaraj (c, Department of
Mathematics, Loyola College, Chennai; corresponding author). E-mails in author order. The companion
manuscript lists the authors in a different order (Shiwakoti, Natarajan, Arockiaraj); that is normal for a
different paper but worth a deliberate confirmation. `audit/MATCH_FORMAT_AND_REFERENCE_CHECK.md:79`
records that the affiliations were set on the authors' instruction on 2026-10-19. AUTHOR CONFIRMATION:
order, spellings, affiliations, corresponding author, e-mail addresses. Nothing was changed.

## 5. Declarations

The MATCH instructions do not ask for funding, conflict-of-interest, data-availability or AI-use statements
(NOT SPECIFIED IN CURRENT OFFICIAL INSTRUCTIONS). The manuscript has a data-availability paragraph and
an acknowledgment ("The authors thank colleagues for helpful discussions."). AUTHOR DECISIONS:

* acknowledgment: name the people, or remove it (nothing is invented here);
* funding and conflicts: state them if any exist (none are invented here);
* AI assistance: the journal states no policy; whether to disclose the use of AI tools in preparing code,
  audits or text is the authors' decision;
* persistent archive: no Zenodo or other DOI exists; cite an exact commit (or a DOI once created).

## 6. Approval

MATCH requires that the corresponding author confirm that all co-authors approved the final version.
No approval of this candidate is recorded. BLOCKER until obtained.
