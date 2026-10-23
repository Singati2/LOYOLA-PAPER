# 01 — MATCH requirements and gaps

Candidate: branch `review/match-figure-2026-10-20` (pushed to GitHub on 2026-10-20, not merged; this note was first written before the push). Sources read on 2026-10-20.

| Source | URL | Accessed |
|---|---|---|
| Instructions for authors | https://match.pmf.kg.ac.rs/prepare.html | 2026-10-20 |
| Publication ethics | https://match.pmf.kg.ac.rs/ethics.htm | 2026-10-20 |
| Journal home page | https://match.pmf.kg.ac.rs/ | 2026-10-20 |
| Template (Overleaf, by the MATCH editors, CC BY 4.0) | https://www.overleaf.com/latex/templates/match-communications-in-mathematical-and-in-computer-chemistry/hbcbmwdkqpcm | 2026-10-20 |

The pages were read through a fetch tool that summarises. Quotations below are the tool's quoted phrases;
wording should be rechecked by an author on the live page before sending.

## Rules found in the official instructions

| # | Rule (quoted or paraphrased) | Where in the candidate | State | Action |
|---|---|---|---|---|
| 1 | Written in English | `main.tex`, `supplement.tex` | COMPLIANT | none |
| 2 | Submit by e-mail to match@pmf.kg.ac.rs | not a source item | AUTHOR ACTION | corresponding author sends; nothing is sent from here |
| 3 | "Papers must be composed in the LaTeX typesetting system" and "the MATCH template must be used" | `main.tex:1-110` keeps the template preamble and title macro | COMPLIANT in structure (A5, 10 pt, the template's title macro and journal header kept). The page geometry `margin=1.5cm,a5paper,twoside,inner=2cm` was not compared line by line with the live template source | AUTHOR CHECK: diff the preamble against the downloaded template once |
| 4 | "Manuscripts should be in camera-ready form ... not in appropriate camera-ready form will not be considered" | `LOYOLA_paper.pdf` (37 A5 pages after the audit corrections of 2026-10-23, see `audit/MATCH_FINAL_PATCHLOG_2026-10-23.md`; 35 after the shortening of the same day, see `audit/MATCH_SHORTENING_REPORT_2026-10-23.md`; 46 after the editorial pass of 2026-10-22; 45 before) | COMPLIANT on build checks (no undefined references, no overfull boxes, no `??`); see `06_LAYOUT_AND_FIGURE_REVIEW.md` | none |
| 5 | References "prepared according to the examples" and "listed in alphabetical order" | `main.tex` bibliography, 54 entries (56 before 2026-10-23; the two entries cited only by text moved to the supplement are now in its bibliography) | COMPLIANT on order (checked by first-author surname, 0 inversions); entry format and content: see `13_REFERENCE_AUDIT.md` | fixes listed there, if any |
| 6 | Non-trivial mathematics or non-routine computer-based procedures, and a clear connection to chemistry | Sections 3-5 (theorems, exact enumeration), Section 6 (octane, nonane, boiling points) | PLAUSIBLY MET; judged in `04_REFEREE_RISK_MATRIX.md` | referee judgement |
| 7 | "All papers are refereed" | — | information | none |
| 8 | No article processing charge; priority publication on request costs 750 EUR | — | information | AUTHOR DECISION only if priority publication is wanted |

## Colour figures (rechecked 2026-10-21)

The live `prepare.html` holds, inside an HTML comment (so not displayed), a "Color figures fee" paragraph:
"Colored figures cannot be published free of charge. Therefore, please re-arrange your figures to be
black-and-white ... If, however, you prefer to keep the colored figures, then you are requested to pay 90 Euro
per colored figure". The template says nothing about colour. Eleven published MATCH papers checked as page
images (vols 82, 87, 88, 96, 97, including Gutman et al., MATCH 97 (2027) 165-174 with four figures) have no
coloured page. Figure 1 of the main paper (moved there on 2026-10-20) was in two shades of blue; it is now
black and white (light grey bars, dark grey bars on the floor, black outlines and dashed line), with the
same data and caption. The supplement's colour heatmap is unchanged: the supplement is not part of the
journal's pages.

## Ethics page (https://match.pmf.kg.ac.rs/ethics.htm)

| Rule | State | Action |
|---|---|---|
| Accurate account of the work; no knowingly inaccurate or incomplete statements | supported by the claim checks (prose registry, labels, verifiers); see `11_VERIFICATION_AND_RELEASE_MATRIX.md` | none beyond open items |
| "Entirely original works"; others' work cited or quoted | see `13_REFERENCE_AUDIT.md` and the companion-manuscript item below | AUTHOR DECISION |
| Not published before and not under consideration elsewhere at the same time | the same authors have a related manuscript in preparation (`Singati2/topological-index-orthogonality`, "Ten Edge-Degree Counts Are All a Degree-Based Topological Index Can See", v2.1) that covers the degree-pair span and evaluates 400 Loyola points; it is not cited in `main.tex` | AUTHOR DECISION: confirm it is not submitted; disclose and cite it, or confine it; see `07_ETHICS_LICENSE_AUTHOR_DECISIONS.md` |
| Corresponding author includes all co-authors and confirms they approved the final version and agreed to publication | no record of approval of this candidate | BLOCKER until all three authors approve |
| Significant errors after publication must be reported | information | none |

## Template items (Overleaf template by the MATCH editors)

| Template item | Candidate | State |
|---|---|---|
| A5, 10 pt, `article` | `\documentclass[a5paper, 10pt]{article}` (`main.tex:1`) | COMPLIANT |
| Title block with journal name, ISSN 0340-6253, DOI line from `\vol`, `\num`, `\id`, `\pubyear` | kept, placeholders `00`, `00`, `xxxxx`, `0000` (`main.tex:93-96`) | COMPLIANT: placeholders are the editors' to fill; no publication metadata or DOI invented. The placeholder renders a link to `doi.org/10.46793/match.00-00.xxxxx`, which does not resolve; this is the template's behaviour |
| Received date from `\today` | `\date{\today}` (`main.tex:187`) | as in the template; an earlier audit (`audit/PUBLICATION_READINESS_DECISION.md:158`) suggested replacing it; the template itself uses `\today`. AUTHOR/EDITOR choice |
| No keywords and no MSC in the template | none in the candidate | COMPLIANT |
| Corresponding-author footnote | on Michael Arockiaraj (`main.tex:178`) | AUTHOR CONFIRMATION |
| E-mail line | three addresses in author order (`main.tex:185`) | AUTHOR CONFIRMATION |
| `\acknowledgment{}` | "The authors thank colleagues for helpful discussions." (`main.tex:1908`) | AUTHOR DECISION: generic text; name the people or remove it; nothing is invented here |

## NOT SPECIFIED IN CURRENT OFFICIAL INSTRUCTIONS

Page or word limit; number or format of figures and tables; supplementary material and how to send it;
keywords; MSC codes; AI-use disclosure; data or code deposit; conflict-of-interest or funding statements;
cover letter. Where this candidate includes such items (supplement, data-availability paragraph, figure), they
are the authors' choices, not journal requirements. Whether a separate supplement PDF may be e-mailed with the
manuscript is an item to confirm with the editorial office (AUTHOR/EDITOR CONFIRMATION).

## Gaps that need an author

1. Approval of the final version by all three authors (ethics page).
2. Status and disclosure of the companion manuscript (ethics page: overlapping submission).
3. Acknowledgment text.
4. Whether to send the supplement as a separate PDF.
5. The repository citation `LoyolaRepo` (`main.tex:2055`) gives a URL without a commit, tag or archive DOI;
   a reader cannot tell which version supports the paper. Cite an exact commit or an archive DOI once one
   exists (none is invented here).
