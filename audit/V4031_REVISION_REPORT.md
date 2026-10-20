# v40.31 scientific revision: change report

Branch `revision/v40.31-scientific`, from `audit/v4030-adversarial` at `f109127`. Not merged into
`main`. No tag, no Zenodo archive. No registered outcome, protocol file, dataset, committed analysis
output or frozen experimental setting was changed. Every manuscript change is a correction of
wording, scope or citation, or the exact certification of a number already in the paper.

Read with `audit/PUBLICATION_READINESS_DECISION.md`; Section 7 below corrects four of its points.

## 1. Mathematical novelty: Song and Huang (MATCH 89, 2023)

**Source.** R. Song, Q. Huang, A relation on trees and the topological indices based on subgraph,
MATCH Commun. Math. Comput. Chem. 89 (2023) 343-370, doi:10.46793/match.89-2.343S. Read in full
(open access PDF of the MATCH site); bibliographic data checked against the issue index, the article
page and the PDF header.

**What it establishes.** For an edge e of a tree T of order n, mu(e) = min{n_u(e), n_v(e)} is the order
of the smaller component of T - e; the edge division vector counts edges by mu. The paper orders trees
by this vector, constructs non-isomorphic trees with equal vectors (branch exchanges, Lemma 3.1,
Theorem 5.5, infinitely many pairs), classifies trees determined by their vector (starlike trees, double
stars, power stars; Section 4), and determines all coincidences up to order 10 (one pair at order 7, three
at order 8, eleven classes at order 9; Remark 5.1 for order 10). Theorem 6.1: equal vectors give equal
values of every edge-additive eccentric index sum_e f(mu(e)) (Wiener, Gutman, Wiener-Hosoya, degree
distance and others in its Table 1). No degree-based index is treated.

**Relation to this paper.** The invariant is distance-type and does not control degrees. Independently
re-derived here: the two trees of order 7 with vector (4,1,1) have degree-pair profiles
{(1,4)^3,(1,2),(2,2),(2,4)} and {(1,3)^3,(1,2),(2,3),(3,3)} and different q-histograms; all three order-8
pairs also differ in profile and q-histogram; the two octane collision pairs of Table 1 have different
vectors ((3,2,1,1) vs (3,2,2,0); (4,2,0,1) vs (4,2,1,0)) and different Wiener indices (76/75, 68/67).
Neither partition refines the other. The paper states this as "Neither partition of trees refines the
other, so their collisions and ours are of different kinds"; an earlier draft of this revision said the
collisions "concern disjoint classes of indices", which was false, because a constant edge function f
gives an index in both classes. None of Lemma 3.1, Theorem 3.5, Corollary 3.6, the minimal orders
13 and 16, Proposition 3.11, Proposition 3.13 or Section 4 is implied or anticipated by Song and Huang.
The shared element is the type of question (whole classes of indices that cannot separate certain
trees, with complete small-order counts) and a branch-moving construction similar in spirit to the
pendant-path propagation.

**Change.** main.tex, after the proof of Theorem 3.5: a paragraph that cites and distinguishes Song and
Huang, with the order-7 example and the sentence "Neither partition of trees refines the other, so
their collisions and ours are of different kinds" (replacing "disjoint classes of indices", see above);
bibitem `SongHuang2023EDV` (alphabetical, after Sigarreta).
`audit/final/NOVELTY_SEARCH_LOG.md`: "Song et al. 2022" corrected to "Song, Huang 2023"; entry P03 year
2021 corrected to 2022 (MATCH 87 appeared in 2022, as main.tex already states).

## 2. Mathematical correctness and scope

| Location (v40.30) | Problem | Change |
|---|---|---|
| main.tex:281, contribution (ii) | "characterises exactly what the pure-gamma points discriminate" holds only for algebraic gamma != 0 (gamma = ln 4 merges K4 and K1,3, Remark 3.9) | "at algebraic gamma != 0", credits Rada's Lindemann-Weierstrass argument, states that minimality is established by enumeration |
| main.tex:519-521 | attributed the *first* orders to Theorem 3.5(iii), which proves existence from order 13 on | existence by part (iii); minimality "computer-assisted (Remark 3.10)" |
| main.tex:666, Remark 3.9 | "only if" needs rational alpha, beta (Lindemann-Weierstrass needs algebraic coefficients) | "At rational alpha, beta" |
| main.tex:1266-1268 | "Their inequalities ... are machine-checked" covered Props 5.4 and 5.8, for which Lean takes the per-edge extrema as hypotheses (`formal/LoyolaFormal/Bounds.lean:121-148`) | inequalities of Corollary 5.5 and Props 5.6/5.7 machine-checked (not their equality cases); for 5.4/5.8 only the summation step (an earlier draft of this revision omitted Corollary 5.5, whose inequality is formalised in `formal/LoyolaFormal/CauchySchwarz.lean`) |
| main.tex:1820-1825 (data availability) | order-13 collision listed as machine-checked without scope | "on the pure-gamma line"; "The transcendence, Laguerre and enumeration arguments are not machine-checked" |
| Table 2 caption, main.tex:1018, 1037, 1076-1080 | ties off the ratio plane stated as facts but "numerical and not certified"; orders 2-6 not covered for the GA statement | **certified exactly** (below); caption, Remark 3.10 and the order-16 paragraph say so; "Orders 2 to 17 were examined". The caption says the pure-gamma counts follow from the q-histograms (Theorem 3.5(ii)) and the R and GA counts, including GA's merge at order 17, from exact arithmetic in the radicals (Besicovitch). An earlier draft split the certification "on Pi" / "off Pi", which was wrong because GA lies on Pi but needs the radical argument |

**Exact tie certificate** (`structural/exact_ties.py`, new; output `structural/exact_ties_out.txt`; 18 s).
Every value is a sum of edge weights (ij)^a (i+j)^b e^(g q) with rational a, b and g in {0, 1}. Each
weight is written exactly as r N^(1/k) e^(g q), N k-th-power-free. Two values are equal iff their
coefficient maps (q, N) -> r agree: for g = 0 by Besicovitch's theorem (k-th roots of distinct
k-th-power-free positive integers are linearly independent over Q; J. London Math. Soc. 15 (1940) 3-6,
added to the bibliography), for g = 1 additionally by Lindemann-Weierstrass (Proposition 3.8). Result
for all trees and trees with Delta <= 4 of orders 2-17 (tree counts asserted against OEIS A000055,
A000602): every count of R, chi and GA in `hp_counts_out.txt` and `chi_floor_out.txt`, the 18
fractional-point counts of orders 12-16 in `fractional_points_out.txt` (exponents 1/3, 1/6 taken
exactly), and LO(3/10,1/5,0) separating all 4069 degree-pair profiles of the 19320 trees of order 16, agree exactly with the numerical
counts. The pure-gamma counts follow from the q-histograms alone (Theorem 3.5(ii)); the R and GA counts
need the radical argument, because GA is a function of the q-histogram but can merge distinct ones. GA
merges two distinct q-histograms first at order 17 (`n=17 all ... qhist=7582 ... GA=7581 GA_qmerges=1`;
none for Delta <= 4 up to 17), now with orders 2-6 covered. Added to `verify.py --full` and to the replay list.

Preserved: every theorem, proof, construction and number of Sections 2-5.

## 3. Statistical interpretation (no registered outcome changed)

- **Narrow-box result now reported for both cohorts** (Section 6.4): the narrow-box Loyola model beats
  the wide-box parent GM12 in 38 of 50 seeds on the pooled set (median seed-matched difference +0.0033)
  but in only 22 of 50 on the decanes (median -0.037); against the narrow-box parent the counts are 40
  and 25 of 50 (recomputed from `external/bp/bp_results_seeds.csv`; registered in `prose_claims_a.py`).
  The text says these were not registered, carry no interval and are descriptive counts of optimiser
  variance on fixed data, so they do not indicate a gain from gamma. "Seed-matched" replaces "paired",
  since the candidate streams are drawn sequentially. An earlier draft reported the pooled set only and
  said the counts show that the negative verdict concerns the registered contrast "not every use of
  gamma"; that framing was withdrawn.
- **Power and design** (Section 6.4): the selection-aware decane range is so wide that it neither
  supports nor excludes gains of practical size, the registered interval omits refitting and selection,
  and no smallest effect of interest or equivalence margin was registered. The registered contrast gives
  the three-parameter model three dimensions against two at the same candidate budget, which "may
  handicap" it. The negative verdicts "do not establish equivalence, and they do not show that gamma
  never helps"; the conclusion says the same, and its "the decane test had little power" became "the
  decane intervals were wide".
- **"Replicates"** is kept as the registered verdict label of PREREG_v37, and the text now says it is
  the name of a seed-count rule that the protocol itself calls non-inferential, whose molecule-bootstrap
  interval includes 0. Conclusion: "met the seed-count criterion ..., with a bootstrap interval that
  included zero" instead of "replicated".
- **"Disappears"** (abstract, Section 6.3, Table 6, conclusion, supplement Section S4) -> "shrinks to about zero" (the nonane
  hybrid median is -0.002; octane best-versus-best still differs by about +0.015).
- **Wiener sentence**: now presented as a single point estimate without an interval, for descriptors
  historically chosen on alkane boiling points.
- **Pre-registration timing** (Section 6.3): "before any nonane value was collected" -> "before the
  nonane data were committed and before any model was fitted to them", which is what git shows
  (964b127 at 15:54, data 6f55119 at 16:05 on 2026-10-03). Collection time is not verifiable from git.

Registered outcomes unchanged: Test A -0.072, 15/50, [-0.156, +0.001]; Test B -0.0001, 25/50,
[-0.003, +0.002]; nonane dHvap "replicates" (95/100, 98/100), T_B "mixed". No numeric table cell changed; the only table edits are the wording of the Table 6 effect
cell ("disappears" -> "shrinks to about zero") and the Table 2 (tab:firstfail) caption (orders examined,
certification scope).

## 4. Reproducibility and tooling

- **Replay timeouts** (`audit/run_all_scripts.py`): a script exceeding `LOYOLA_SCRIPT_TIMEOUT` seconds
  (default 7200, unchanged) is reported as a PROBLEM with its own status text ("TIMED OUT, outputs not
  compared") and the replay continues. Changed outputs are copied to a `loyola_changed_*` directory that
  is created only when the first changed file is found; the RESULT line names it only if it exists and
  holds files (otherwise "no changed outputs to keep"), so a discrepancy can be diffed afterwards (the
  `press_size_probe.py` diff was lost for this reason). Tested on a clean clone with a 2 s limit before
  the lazy directory and the TIMED OUT text were added: 19 scripts reported "timeout after 2 s", the
  replay finished, no traceback. That test was not repeated after those two changes.
- **PyMuPDF declared**: `pymupdf==1.25.1` in `requirements-extras-lock.txt` (used by `audit/check_labels.py`;
  1.24.10 has no Python 3.13 wheel).
- **Two mis-anchored prose registry entries fixed**: `ext_cal4` matched "Delta <= 4. Its" in the
  introduction instead of "NIST lists 4 under Labbauf". It was re-anchored in v40.31 but still computed
  the count of calorimetric selection rules (method C), which is also 4, so the coincidence persisted.
  It now counts the nonane provenance rows whose NIST source is Labbauf et al. (4), and an entry
  `ext_reid25` checks the 25 under Reid. `bp_cov34` matched an unrelated nonane fold count; v40.31 said
  the coverage sentence had left main.tex, which was wrong (Section 6.4 still says "with $34$ and $41$
  molecules"). The fold-count entry is renamed `bp_non_dhvap_bd`, and new entries `bp_cov34_main` and
  `bp_cov41_main` check the coverage sentence against `coverage_bias.csv`.
  Registry changes in v40.31: five entries re-anchored to reworded sentences (`ext_tb63`, `bp_gm2_976`,
  `rp_enum_to17`, `off_orders12`, `off_orders16`), one repurposed (`ff_cap_below7`), eight added (six
  checkable, two cited values of Song and Huang marked UNCHECKABLE); prose check then 748 checked, 0
  failures, 22 uncheckable. Further changes after review: `ext_cal4` recomputed as above; `bp_cov34`
  renamed `bp_non_dhvap_bd`; `bp_nb_med`, `bp_nb_40` and `bp_nb_50b` re-anchored to the two-cohort
  narrow-box sentence; eight entries added, all checkable (`ext_reid25`, `bp_cov34_main`,
  `bp_cov41_main`, `bp_nb_dec22`, `bp_nb_dec50`, `bp_nb_dec_med`, `bp_nb_dec25`, `ff_cap_ga17`). Prose
  check (`prose_numbers_check.py`): registry A 455 entries, 438 checkable, 438 match; registry B 323
  entries, 318 checkable, 318 match; 756 checked, 0 failures, 22 uncheckable.
- **Replay discrepancies of the lab run (unchanged status)**: 56 of 60 scripts exact; 4 differ only in
  floating-point digits or error magnitudes (`transfer_exploratory.py`, `wide_box_diagnostics.py`,
  `counterattack_v4030.py`, `press_size_probe.py`). The `press_size_probe.py` difference is bounded by
  its exit-0 verdict (published outputs reproduced, all rejection and selection-change counts 0) but the
  differing line is **not identified**; it is not an exact match.

## 5. Journal readiness (MATCH)

Checked against https://match.pmf.kg.ac.rs/prepare.html and the current template (`match_template.zip`,
downloaded 2026-10-16):
- **Date**: the template itself uses `\date{\today}` ("Received ..."); kept. The earlier advice to
  replace it was wrong.
- **AI assistance**: MATCH states no policy (prepare.html, ethics.htm). No statement was invented; the
  authors must decide on a disclosure (COPE's position is that tool use should be disclosed and tools
  cannot be authors; its page could not be retrieved verbatim here).
- **Template deviations (author decision, not changed)**: main.tex changes the protected theorem block
  (numbered corollaries and remarks with shared counters and `[section]` numbering; the template has
  unnumbered `\newtheorem*` corollaries and remarks) and `\baselineskip` 10px -> 10pt, although the
  template says not to modify that code. Reverting renumbers every statement; it needs the authors'
  decision. `\email` lists only the corresponding author; the template lists every author.
- **Title**: kept. The earlier recommendation to retitle toward "degree-ratio indices" was not adopted:
  q = |d_u - d_v|/(d_u + d_v) is the normalised degree imbalance and a bijective function of the degree
  ratio, so "resolution limit of degree imbalance" is accurate; Remark 3.7 already says the limit is not
  specific to gamma. A retitle is an authorial choice, not a correction.
- **Length**: 42 + 28 A5 pages (40 + 28 before). MATCH states no limit; Section 6 remains the natural
  place to shorten if the editor asks.
- **References**: alphabetical order kept; two verified additions (Besicovitch 1940, Song and Huang 2023);
  MATCH rejects papers with non-existent references, so nothing unverified was added.
- **Cover-letter argument** (for the authors): lead with the order-13 and order-16 obstruction for every
  degree-ratio index (GA, AG, SDD, ISDD, diminished Sombor, degree-ratio Sombor; Corollary 3.6), with
  explicit witnesses and an exact certificate; then the crossing bound and identifiability; then the
  pre-registered negative QSPR result as a calibration of what gamma does not add.

## 6. Data rights

The KDB/Cheméo-derived values are the 18 octane acentric factors and comparison values in
`DATA/octane_provenance.csv` (and its root copy `octane_property_provenance_v35.csv`, identical byte for byte), two
hard-coded values in `source_sensitivity.py`, the KDB critical constants of 2,2,3,3-tetramethylbutane
(Tc 567.8 K, Pc 28.7 bar) in `audit/final/scripts/audit_calc.py`, and three comparison numbers in
supplement.tex. The manuscript tables do not use KDB values.
- The repository also holds 262 complete NIST Chemistry WebBook pages (SRD 69): 154 under
  `external/bp/nist_raw`, 17 under `external/bp/nist_hvap_pts` and 91 under `external/nonane_raw_nist`
  (`git ls-files`). Their terms of use were not reviewed for this revision.
- Cheméo (https://www.chemeo.com/about, /tos, consulted 2026-10-16): value-by-value use is allowed with
  the citation "Cheméo, chemical and physical properties (https://www.chemeo.com)"; bulk download and
  inclusion of the database as-is are not; the content is claimed under copyright and the sui generis
  database right. The citation was missing; it is now in the supplement, with KDB named as the original
  source.
- KDB/CHERIC terms could not be retrieved: on 2026-10-16 the CHERIC domain served unrelated content.
  The redistribution terms of the KDB values remain **unresolved**.
- `DATA/README.md` now states that the MIT licence covers code and text, not third-party values, lists
  the KDB/Cheméo footprint above, describes the 262 NIST pages and says their SRD terms were not
  reviewed, and says that no archive should be made until the KDB/Cheméo and NIST terms are settled. No archive was created.
- Options for the authors: (a) keep only the cited comparison numbers in the supplement and replace the
  copied KDB strings in the public CSVs by the Cheméo page URL and a status flag; (b) ask Cheméo for
  permission; (c) keep as is with attribution, relying on value-by-value use. (a) removes the question.

## 7. Corrections to the earlier readiness decision (f109127)

1. Song and Huang were called "the closest collision paper" and their citation "mandatory" for novelty.
   That came from the abstract-level search; the full text shows a distance-type invariant that does not
   anticipate any result here. The citation is still appropriate (same journal, same kind of question)
   but it is not a novelty threat.
2. "Replace `\date{\today}`" was wrong: it is the MATCH template's own setting.
3. Retitling was listed as recommended; it is not needed (Section 5).
4. The decision called the Table 2 R entries uncertified; they are now certified exactly.

## 8. Verification at the head of this branch

Certified commit: `c9fbac2` (fresh clone; Linux, Python 3.13.16). The commit that adds this section
changes only this report and `SHA256SUMS.txt`; the GitHub Actions fast path runs on it after the push.

| Check | Status | Evidence |
|---|---|---|
| `verify.py` fast path, 16 stages (core verifier, prose numbers, regression and baseline tests, constancy, auxiliary outputs, source identities, interval certificates, style, extremal trees, minimality, sum-connectivity pair, count dimension, DATA copies, manifest, CSV convention) | PASS (ALL PASS, 13.5 min) | lab log |
| Prose numbers | PASS: 756 checked, 0 failures, 22 uncheckable | |
| Labels and references (`audit/check_labels.py`, tectonic 0.15.0, PyMuPDF 1.25.1) | PASS | |
| Exact tie certificate (`structural/exact_ties.py`) | PASS: all numerical counts certified exactly | |
| Counter-attacks on the checkers (`audit/attack_checks.py`) | PASS: 13 attacks, 13 rejected, 0 false negatives | |
| Replay, fast scripts (41), with one committed output deliberately corrupted | behaves as designed: 37 OK; the corrupted output is detected three ways (exact_ties CHANGED, prose numbers, manifest); `counterattack_v4030.py` differs exactly as recorded on 2026-10-16 (macOS vs Linux precision); both changed outputs retained for diffing | |
| Replay timeout path (`LOYOLA_SCRIPT_TIMEOUT=2`) | PASS: 20 scripts reported TIMED OUT, replay completed, no traceback, "no changed outputs to keep" | |
| Lean 4 build | NOT RUN at this head; `formal/` is unchanged since the PASS at 09ceba8 (2026-10-15) | `git diff f109127 -- formal` is empty |
| Full replay of all 60 scripts and `verify.py --full` | NOT RUN at this head (several hours); last full results at 09ceba8: 56 exact, 4 floating-point discrepancies | lab_09ceba8 |
| PDFs | rebuilt with tectonic 0.15.0: 42 + 28 A5 pages | |
| Data added or changed by this branch | none (no CSV, HTML or data file in `git diff f109127`) | |


## 9. MATCH template restored verbatim (after section 8)

The preamble of `main.tex` above the template's line "DO NOT MODIFY THE EXISTING CODE ABOVE THIS LINE" is now
identical, line for line, to `match_template.tex` from https://match.pmf.kg.ac.rs/template/match_template.zip
(downloaded 2026-10-16). The only additions are the paper's packages, placed where the template says "PLACE ADDITIONAL
PACKAGES HERE". The earlier preamble had changed the protected theorem declarations (one counter shared by all
statements and reset at every section, numbered corollaries and remarks, equations numbered within sections) and
`\baselineskip=10px` (to `10pt`).

Consequences:

* Numbering follows the template: theorems and propositions share one counter; lemmas, definitions, examples
  and equations have their own; corollaries and remarks are unnumbered. Section, table and page numbers are
  unchanged (42 A5 pages, even, as MATCH prefers).
* The five in-text references to a corollary or remark now name it ("the Cauchy--Schwarz interpolation corollary
  of Section 5.3", "the remark on the floor on Π", "the remark on sharpness in Section 3.1").
* The template's `10px` is a pdfTeX unit, so the main paper is now built with pdflatex, the engine the template
  names. `audit/check_labels.py` uses pdflatex and simulates the counters from the `\newtheorem` declarations
  instead of assuming section-reset numbering (tectonic remains a fallback, given `10pt` in its temporary copy only).
* MATCH states no maximum length; its only page rule is that the number of pages should, if possible, be even.
  The paper has no colour pages, so the colour-figure fee (90 EUR per figure) does not apply.

| Old | New | Old | New |
|---|---|---|---|
| Definition 2.1, 2.2, 3.4, 5.3 | Definition 1, 2, 3, 4 | Proposition 4.1, 4.3 | Proposition 7, 8 |
| Lemma 3.1 | Lemma 1 | Example 4.4 | Example 2 |
| Theorem 3.3 | Theorem 1 | Proposition 5.1, 5.2 | Proposition 9, 10 |
| Theorem 3.5 | Theorem 2 | Proposition 5.4 | Proposition 11 |
| Corollary 3.6, 5.5, 5.9 | unnumbered | Proposition 5.6, 5.7, 5.8 | Proposition 12, 13, 14 |
| Proposition 3.8, 3.11, 3.13, 3.17 | Proposition 3, 4, 5, 6 | Remarks | unnumbered |
| Example 3.15 | Example 1 | Equations (2.1)-(5.5) | (1)-(9) |

The supplement, `LEAN_VERIFICATION.md`, `README.md`, `REPRODUCE.md`, `REVIEWER_START_HERE.md`, notebook 02 and its
generator, and two script docstrings use the new numbers. Earlier audit reports, change logs, verification logs and
the v40.30 audit scripts keep the numbering of the version they describe; sections 1-8 above use the old numbering.

Verification after this change (lab, 2026-10-16): `verify.py` fast path ALL PASS (16 stages); labels and references
PASS with pdflatex (a planted stale "Theorem~3.5 of the main paper" in the supplement is rejected); counter-attacks
13 of 13 rejected; prose numbers 756 checked, 0 failures. Lean, the full replay and `--full` were NOT RUN for this
change; `formal/` is unchanged.
