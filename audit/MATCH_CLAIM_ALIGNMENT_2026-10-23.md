# Claim alignment: abstract, introduction and conclusion (audit branch, 2026-10-23)

**Status labels:**
- **K:** known result, credited.
- **N:** proved here.
- **C:** computer-assisted (finite enumeration).
- **E:** empirical.

"Fixed" refers to `MATCH_FINAL_PATCHLOG_2026-10-23.md`.

| Abstract claim | Status | Evidence | Introduction | Conclusion | Verdict |
|---|---|---|---|---|---|
| Vertex-degree-based indices cannot distinguish graphs with equal edge-degree-pair counts | K | Proposition 5; Rada 2026 | first paragraph, cited | — | consistent |
| Degree-ratio indices lose further information | K | Corollary on degree-ratio indices; Rada 2019, Proposition 2.5 | first paragraph; (i) | first paragraph | consistent |
| Pure-γ points at algebraic γ ≠ 0 separate exactly the $q$-histograms ("by theorems of Rada") | K (equal order), N (any order) | Theorem 2(ii) and its proof; Rada 2019, Theorem 3.4 is on $\mathcal{G}_n$ | (i), now says "for graphs of equal order" | now says "for graphs of equal order" | fixed (A2). The abstract's "by theorems of Rada" is acceptable, since the order restriction is removed by the same argument given in the paper |
| No degree-ratio index separates more | K | Corollary; Rada 2019, Proposition 2.5 | (i) | first paragraph | consistent. The claim is about the class, not about one arbitrary index; a single index can do worse (SDD at order 9, GA at 17), as the remark says |
| The histogram determines the counts up to order 12 (all trees) and 15 (chemical trees) | C | Remark (floor on Π), Table 2; `collision minimality` stage, rerun today | "What is new"; (iii) | "minimality … rests on exhaustive enumeration" | consistent. "Order" means vertices throughout; the witness trees have 13 and 16 vertices (12 and 15 edges), checked |
| Explicit counterexamples at every larger order | N | Theorem 2(iii): witnesses plus pendant-path propagation | (ii) | first paragraph | consistent |
| At fixed (α,β), two chemical graphs exchange order at most five times as γ varies | N (application of Laguerre) | Proposition 4 | now "At fixed (α,β)" | now "Along the imbalance axis" with fixed (α,β) from context; whether five is attained for Δ ≤ 4 is open (limitation ii) | fixed (A1) |
| Pre-registered tests on measured boiling points did not demonstrate a gain from γ | E | Table 5; decanes −0.072, 15/50, [−0.156, +0.001]; pooled −0.0001, 25/50, [−0.003, +0.002] | (iv) | second paragraph | consistent. The body and conclusion now add that these tests do not test the $\Delta H_{\mathrm{vap}}$ effect (Q9). No text claims equivalence |
| A $\Delta H_{\mathrm{vap}}$ gain met a pre-registered seed-count rule and shrank to about zero in an exploratory wide-box rerun | E | Section 6.3; Table S6; hybrid control −0.002 (24/50) | (iv) | second paragraph | consistent. The body now adds the increment-estimate caveat (Q6) |
| (body/conclusion) Ridge on the counts has higher point estimates than every single index | E | Table 5 | (iv) | second paragraph | fixed (Q14): Wiener's W + p₃ is higher still on the decanes (0.904 against 0.860) |

## Novelty checks

| Claim | Finding |
|---|---|
| `prop:offplane` | Presented as Rada's argument with algebraic coefficients, "we do not claim it as a new theorem". The introduction (i) and the cover letter agree |
| Extremal trees | Bounds credited to Cruz–Rada, Corollaries 2.2 and 3.2 (source checked: no equality cases). Uniqueness comes from the direct proof, also from their Theorems 2.1 and 3.1 with strict inequalities. Gao–Gao also credited. Introduction (i) and cover letter agree |
| Orders 13/16 | "We found no earlier determination … in a literature search recorded in the repository." This is a search record, not a proof of novelty. The wording is appropriate and does not use "not found" as proof |
| Generic discrimination | Stated as inherited from the parent, not conferred by γ |
| Lemma 1, Theorem 1 | Listed as "elementary facts" |

## Limitations

The concluding remarks keep four kinds of limitation:
- enumeration scope;
- theoretical scope (five crossings for Δ ≤ 4 open);
- data quality, with 34 nonanes for $\Delta H_{\mathrm{vap}}$ now stated;
- inferential scope: no equivalence margin, and the post-outcome changes are listed in Table S8.

The single open problem (extremal graphs for general triples, starting with maximal chemical trees) matches the open question left in Section 5. None of these was removed by the edits.
