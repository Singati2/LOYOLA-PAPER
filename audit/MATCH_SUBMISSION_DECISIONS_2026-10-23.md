# MATCH submission decisions, 2026-10-23

Nothing here has been decided or sent. Each item names who should act.

## MATCH rules: what the site says and what it does not

Sources read on 2026-10-23:
- https://match.pmf.kg.ac.rs/prepare.html
- https://match.pmf.kg.ac.rs/ethics.htm
- https://match.pmf.kg.ac.rs/template/match_template.zip

**Stated:**
- Submission is by e-mail to match@pmf.kg.ac.rs, in camera-ready form.
- The MATCH LaTeX template must be used.
- References are in alphabetical order.
- Manuscripts with non-existent references are rejected.
- No keywords and no MSC codes (template comments).
- The corresponding author ensures that all co-authors are included and have approved the final version.
- No duplicate or simultaneous submission.

**Not stated (EDITORIAL-OFFICE CONFIRMATION REQUIRED):**
- a page limit;
- supplementary material, including whether a separate 39-page PDF may be sent;
- PDF versus TeX submission;
- AI-use disclosure;
- conflict-of-interest, funding and data-availability statements;
- copyright and licence.

## Decisions

| # | Decision | Current state | Responsible | Next action |
|---|---|---|---|---|
| 1 | Approve the audit fixes, especially the statement/remark edits P1–P4 | On the local branch, not pushed | All three authors | Read `MATCH_FINAL_PATCHLOG_2026-10-23.md` |
| 2 | Contribution and length: Option A (new theorem) or B (cut Section 6 to about 3 pages, reframe around 13/16) | 37 + 39 pages | All authors | Decide; the audit recommends B |
| 3 | Final title | "The Loyola Index Family and the Resolution Limit of Degree Imbalance" | All authors | Confirm or change (two reviewers suggest moving the index name out of the title) |
| 4 | Names, order, affiliations, e-mails, corresponding author | Consistent across paper, supplement, `README.md`, `LoyolaRepo` and cover letter: Advik Natarajan (Oregon State), Ganesh Shiwakoti (FAU), Michael Arockiaraj (Loyola College Chennai, corresponding). Consistency does not prove accuracy | Each author for own entry | Written confirmation from each author |
| 5 | Acknowledgment | Uses the text supplied on 2026-10-23: "…the Machine Perception and Cognitive Robotics (MPCR) Laboratory at Florida Atlantic University (FAU)…". The audit brief names the lab "Machine Perception and Robotics Cognitive Lab". The two wordings differ. The text implies resources only, not funding or affiliation | G. Shiwakoti | Confirm the lab's official name; the paper is unchanged until then |
| 6 | Repository citation | `\bibitem{LoyolaRepo}` gives the URL only. Reviewer docs and notebooks pin `c48bad05` (old) | Authors | After approval: tag the final commit, archive it with a DOI (e.g. Zenodo), cite the DOI, and repin the docs and Colab notebooks |
| 7 | Companion manuscript ("Ten Edge-Degree Counts …") | Disclosed in the cover-letter draft; not cited in the paper; status unconfirmed | Authors | Confirm status; decide whether to cite it as in preparation |
| 8 | Redistribution: NIST, KDB, Chemeo | NIST pages are absent from the tree but present in public history (262 pages, commits `8793b06` and `dfcf7ee`, on `main` and ten other branches). Verbatim NIST rows are in provenance CSVs (rated "uncertain" by the authors' own audit). KDB/Chemeo-derived octane values have unestablished terms | Authors | Decide whether to keep, remove or rewrite. A history rewrite is a destructive, public action that needs explicit authorization |
| 9 | AI-use disclosure | None in the paper; the site is silent; the public repository documents AI-assisted editing and auditing | Authors | Decide on wording; ask the editorial office (draft below) |
| 10 | Supplement route | 39-page supplement in the repository; the paper cites S1–S11 | Corresponding author | Ask the editorial office (draft below) |
| 11 | Personal data in the public tree | Home paths in `verification_logs/**`; a personal e-mail in `audit/push_lab_logs.sh` (also the public commit e-mail) | G. Shiwakoti | Decide whether to remove them in a normal commit |
| 12 | Approval of the final version by all three authors | Not recorded | Corresponding author | Required by the ethics page before submission |
| 13 | Open problems removed from the conclusion on 2026-10-22 | One open problem kept | Authors | Decide whether to restore the others |

## Unsent e-mail draft to the editorial office (do not send without approval)

> To: match@pmf.kg.ac.rs
> Subject: Enquiry before submission: supplementary material and disclosures
>
> Dear Editors,
>
> We are preparing a manuscript for MATCH Communications in Mathematical and in Computer Chemistry, about
> 37 pages in the MATCH template. It is accompanied by a supplementary document of about 39 pages
> containing further proofs, data tables and the details of the computational tests. Before submitting
> we would be grateful for guidance on three points:
>
> 1. May a separate supplementary PDF be sent with the manuscript, or should such material be deposited
>    in a public archive and cited instead?
> 2. Does MATCH require a statement on the use of AI-based tools in preparing a manuscript, and if so,
>    in what form and where?
> 3. Are conflict-of-interest or data-availability statements expected?
>
> With kind regards,
> [corresponding author: name, affiliation, e-mail]
