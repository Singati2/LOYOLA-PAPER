# 03 — Change ledger

Branch `review/match-figure-2026-10-20` (local), from `9212441` (pushed head of
`review/corrections-impl-2026-10-19`). Every change below is in git; nothing was deleted from history,
no data set, registered result, proof, protocol or seed was changed, and nothing was pushed.

## Commits

| Commit | Content |
|---|---|
| `5d5d16a` | Degeneracy chart moved into the main paper (Figure 1); chart redrawn for A5 legibility; supplement figure removed; registry and label checker updated (`audit/MATCH_FIGURE_2026-10-20.md`) |
| `0a36902`, `325bd05` | notebooks pinned to `5d5d16a`; guide links (superseded by the chain below) |
| `b7f50c0` | verified text and citation fixes, records (`docs/match/`), independent counterexample scripts |
| `6f8ac71` | notebooks pinned to `b7f50c0` |
| final docs commit(s) | reviewer guide and README links to `6f8ac71`; this ledger, the verification matrix, the submission package |

## Changes in the manuscript (`main.tex`, `supplement.tex`)

| # | Location | Change | Why necessary | Unchanged | Verified by |
|---|---|---|---|---|---|
| M1 | Sec. 4.2, Fig. 1 | degeneracy chart in the main paper; caption adds that floor attainment carries no information beyond the profile and explains the darker bars | central concept of the paper had no figure; supplementary figure was the main text's evidence | data, colours, values | independent recount of all 12 bars; regeneration identical in canonical form; label check |
| M2 | Sec. 4.2 | sentence: 25.5 % is not the share of trees sharing a value (45 of 106, 42.5 %) | prevents misreading the figure (Feynman review) | definition of degeneracy | registry `main_45share`, `main_425` (mutation-tested) |
| M3 | abstract | "an exploratory gain" -> "a gain ... that met a pre-registered seed-count rule shrinks to about zero, in an exploratory comparison" | label registered and exploratory analyses exactly (referee E1) | the conclusion (shrinks to about zero) | prose check; text at lines 1669-1683 |
| M4 | Sec. 7 (iv) | "reverses the nonane conclusion" -> "the nonane gain shrinks to about zero" | overstatement of a change from +0.048 to -0.002 (E2) | — | consistent with lines 1643, 1683, Table 6 |
| M5 | Sec. 4.3 | "shows that ... is a property of linear imbalance weighting" -> "suggests that ... does not depend on the exponential form" | a third-decimal gap the paper itself says cannot rank indices (E3) | numbers | — |
| M6 | Sec. 3.1, after Theorem 2 | "separate more trees" -> "take more distinct values on these trees" | trees vs profiles (E4) | — | — |
| M7 | proof after Prop. extremal | "if $i,j \ge 2$" -> "if $i,j\ge2$ and $(i,j)\ne(2,2)$" | the strict inequality fails at (2,2), which the sentence means to exclude (E5) | the result | hand check; counterexample report (path/star extremal orders 4-17 confirmed) |
| M8 | Sec. 6.4 | "and one of the 75 decanes" -> "among them one of the 75 decanes" | the decane is among the 25 (E6) | numbers | registry `bp_cal25`, `bp_cal_one` |
| M9 | Sec. 6.3 | ridge caveats: LO minus ridge interval [-0.101, +0.032] includes zero; ridge below the best index model on four of five octane properties, level on ΔH_vap (0.954 vs 0.957) | the long text implied ridge dominance; caveat existed only in the short draft and the supplement | — | registry `main_ci_ridge_*`, `main_oct_ridge_*` (mutation-tested) |
| M10 | Sec. 1, 4.2, 8, proof | citation wording: Hu 2022 for general weights; Das-Mondal indices "exponentiate a classical generator"; "functions of the ratio q"; Rada 2019 "who studied their discriminating power"; "Rada's theorem based on the Lindemann-Weierstrass theorem"; Cruz-Rada theorems and corollaries; Wiener's polarity number | citations claimed slightly more than the sources show (`13_REFERENCE_AUDIT.md`) | cited works and numbering | reference audit; label check |
| M11 | bibliography | repository URL in `\url{}`; supplement entries reordered (Konstantinova before KDB, Reid before Rossini) | MATCH requires alphabetical order | entries | label check; build |
| M12 | data availability | "sections, figures and tables" -> "sections and tables" | the main text cites no supplementary figure now | — | — |

## Changes outside the manuscript

| Item | Change | Why |
|---|---|---|
| `generate_loyola_v35_figures.py` | chart size 4.4 x 2.9 in, no title | print legibility (4-5 pt -> 7-8 pt) |
| `prose_claims_a.py`, `prose_claims_b.py` | entries for every new number; caption entries read main.tex; two patterns anchored; `bp_3K_a` removed (matched the preamble `\headsep = 3pt`, not a claim) | keep every number checked |
| `audit/check_labels.py` | main-paper figure numbering and supplement cross-references | a wrong figure reference previously passed |
| `README.md`, `REVIEWER_START_HERE.md`, `REPRODUCE.md`, `colab/README.md` | figure listing, page counts, CI trigger, notebook outputs, changelog coverage, NIST cache wording, existing-checkout and Python behaviour of `notebooks/`, links | stale or wrong statements (inventory, Colab audit) |
| `COLAB_FOR_REVIEWERS.md` | new: essential vs optional Colab checklist | user request |
| `audit/independent_counterexamples_2026-10-20/` | new: independent scripts and outputs (41 claims) | user request |
| `docs/match/` | new: review records 01-14 | master assignment |
| Overleaf folders and zips | synchronised; main bundle has `figures/`; unused figure removed from the supplement bundle | bundles must compile |
| `submission_candidate/match/` | new: clean package | master assignment |

## Proposed, not done (AUTHOR DECISION)

| Proposal | Source | Reason not done |
|---|---|---|
| Condense the main paper by about 8 pages (closed forms and termwise bounds, Proposition 6 and two remarks, Sec. 4.3 and Table 3, repetition in Sec. 4.2 to the supplement) | `05_LONG_VS_SHORT_DECISION.md`, `05b_...` | structural; renumbers propositions and tables, the Lean map and registries; needs coauthor approval |
| Title | `04_...` | author decision |
| New analyses (q / q^2 collinearity, deterministic nested search, selection-aware interval, compiled-only nonane verdict, IRLA / methyl-count baseline, structural explanation of 13 and 16) | `04_...`, `12_...` | would be new experiments or arguments |
| Cite the companion manuscript; acknowledgment; funding; AI use; exact repository commit or DOI | `07_...` | author decisions |
| Repository: label superseded verdict files, `main.log`, privacy items in `verification_logs/lab_09ceba8/` and `audit/push_lab_logs.sh` | `02_FILE_INVENTORY.md` | archive files; no deletion or rewrite without consent; none is in the package |
| NIST history and repository visibility; KDB/Chemeo redistribution | `07_...` | legal / author decisions |
| Optional: TrueType fonts in the figures | `06_...` | changes both committed figure files |
| Test, then possibly change, the `notebooks/` setup (Colab Python) | `10_...` | must be tested in real Colab first |
