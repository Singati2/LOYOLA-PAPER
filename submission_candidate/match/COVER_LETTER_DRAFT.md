# Cover letter — DRAFT, NOT SENT

> Draft for the authors. Items in [square brackets] need an author decision. Nothing has been sent to
> MATCH. MATCH's instructions do not require a cover letter; this text can also serve as the e-mail body.

To: Prof. Ivan Gutman, Editor-in-Chief, and Prof. Boris Furtula, Managing Editor,
MATCH Communications in Mathematical and in Computer Chemistry (match@pmf.kg.ac.rs)

Dear Editors,

We submit the manuscript "[The Loyola Index Family and the Resolution Limit of Degree Imbalance —
final title to be confirmed by the authors]" by Advik Natarajan, Ganesh Shiwakoti and Michael Arockiaraj
for consideration in MATCH Communications in Mathematical and in Computer Chemistry. The manuscript (37 A5 pages) is
prepared with the MATCH LaTeX template; [a Supplementary Material PDF is attached / is available on
request — confirm with the editorial office whether a separate supplement may be sent].

**What the paper does.** The Loyola family multiplies each edge term of the Gutman–Milovanović index by
$e^{\gamma q_{uv}}$, where $q_{uv}$ is the normalised degree imbalance of the edge. The main new results
concern where the known degree-ratio ceiling binds for trees and chemical trees:

* the histogram of edge imbalances determines the degree-pair counts of a tree up to order 12, and of a
  tree of maximum degree at most 4 up to order 15; explicit trees with distinct degree-pair counts and
  equal histograms are given at order 13 (16 for maximum degree at most 4) and at every larger order;
* these orders are the first. The minimality is computer-assisted, by an exhaustive enumeration of all
  trees of orders 2 to 17 in exact rational arithmetic, with exact (radical and transcendence-based)
  certification of the ties; it is not a pen-and-paper proof;
* as a consequence, no degree-ratio index (for example $GA$, $AG$ or the diminished Sombor index)
  separates all alkane carbon skeletons of order 16 or more;
* at fixed $(\alpha,\beta)$, two chemical graphs exchange order at most five times as $\gamma$ varies.

**Relation to earlier work.** Several facts the paper uses are known, and the text credits them. That every
vertex-degree-based index depends on a graph only through its edge-degree-pair counts, and the pendant-path
construction that carries equal counts to every larger order, are standard; the paper cites them from
Rada (MATCH 96 (2026), Section 3.1). That the pure-imbalance points at algebraic $\gamma \neq 0$ separate exactly the imbalance
histograms, and that no degree-ratio index separates more, is, for graphs of equal order, Theorem 3.4 and
Proposition 2.5 of Rada (2019) applied to this family. The same Lindemann--Weierstrass argument, with algebraic coefficients,
shows that at rational $(\alpha,\beta)$ a nonzero algebraic $\gamma$ never merges two molecules that the
parent index separates; the paper states this as a direct consequence, not as a new theorem. That the path and the star are the extremal trees of the pure-imbalance
points follows from the criteria of Cruz and Rada (MATCH 82 (2019)): their Corollaries 2.2 and 3.2 give
the bounds, and the paper's short direct proof gives the uniqueness; the result is not claimed as new. The affine independence of the imbalance direction and the
log-convexity of the family are stated in the paper as elementary facts.

**Related work by the same authors.** The three authors are also preparing a separate manuscript, "Ten
Edge-Degree Counts Are All a Bond-Incident-Degree Index Can See: An Exact Redundancy Certificate and What It
Leaves for New Molecular Descriptors" (G. Shiwakoti, A. Natarajan, M. Arockiaraj) [confirm the title: the
companion's README, LaTeX source and CITATION.cff give three different wordings]. It is [not submitted to
any journal and not posted on a preprint server — authors to confirm, including for the June 2026
journal-format version]; a draft and its code are public at
https://github.com/Singati2/topological-index-orthogonality. That manuscript is a chemoinformatics study:
it turns the known fact that every bond-incident-degree index is a linear combination of the
edge-degree-pair counts (Rada, MATCH 96 (2026)) into a rank test on MoleculeNet data sets, and it includes
the Loyola family among the indices it screens. It contains none of the theorems, enumerations, bounds or
boiling-point and octane analyses of the present submission, and the two manuscripts share no text, data,
figures or tables. Earlier drafts of the present paper, under the working name "Wuzi index", are visible in
the public history of that repository and of https://github.com/Singati2/LOYOLA-PAPER; [authors to confirm:
they have not been published or submitted elsewhere]. [If the companion manuscript is submitted while this one is under review,
we will inform the editor and cite it.]

**Chemistry.** We test the family on octane properties, a pre-registered replication on nonanes and
pre-registered tests on measured boiling points of acyclic alkanes. The results are negative or modest and
are reported as such: the boiling-point tests, on a property where $\gamma$ had given mixed results, did not demonstrate a
predictive gain from $\gamma$ (on the decanes the point estimate favoured the parent, with an interval that included zero), and a gain
on vaporisation enthalpies that met a pre-registered seed-count rule shrinks to about zero in an
exploratory comparison with a wider search box. These results do not show that $\gamma$ can never help,
nor that the family is equivalent to its parent; the family is not proposed as a better predictor. Source limitations of the experimental values are stated
in the paper and the supplement.

**Reproducibility.** Data, scripts, verifiers and Lean proofs of the stated scope are in
https://github.com/Singati2/LOYOLA-PAPER [cite the exact commit or archive DOI once fixed; the manuscript's
reference currently gives only the repository address]. The NIST
WebBook source pages are not redistributed.

This manuscript is original, has not been published, and is not under consideration elsewhere. All
authors have approved the final version and agree to its submission. [Corresponding author to confirm
both statements before sending.]

Sincerely,
[Michael Arockiaraj, corresponding author — confirm]
Department of Mathematics, Loyola College, Chennai, India
[e-mail]
