# Comprehensive audit of LOYOLA-PAPER

Audit date: 6 October 2026. Reviewed snapshot: [`ab9e1df209d3f570c8795b508a54c28a852dae2a`](https://github.com/Singati2/LOYOLA-PAPER/tree/ab9e1df209d3f570c8795b508a54c28a852dae2a), v40.8. Findings describe that snapshot; accompanying changes fix the software defects identified below. This is a scientific and software review, not a guarantee that every possible bug or mathematical error has been excluded.

## Assessment

The main algebraic framework is coherent, and the core numerical results reproduced. Independent interval checks support the finite rank claim and the five-crossing witness. The results support the scoped conclusion that these protocols have not demonstrated an incremental predictive benefit from gamma. They do not prove that gamma never helps, that optimization has reached global optima, or that all experimental property values have been verified against their definitive primary determinations.

The strongest actionable problems were in reproducibility and verification. One missing source archive silently changes cohort membership; four advertised adversarial tests were not executed correctly; structural checks could report failure without failing the run; and the size-adjusted PRESS implementation mishandled deletion-induced rank loss. A mathematical wording problem about fitted-model identifiability also needs clarification.

## Confirmed defects and corrections

### 1. Missing archived source silently changes the boiling-point cohort — high priority

Location: [`external/bp/build_bp_data.py`](https://github.com/Singati2/LOYOLA-PAPER/blob/ab9e1df209d3f570c8795b508a54c28a852dae2a/external/bp/build_bp_data.py), grouped-record page loop.

The builder reads a listed NIST page only when it exists, silently ignoring missing files. In an isolated copy, deleting `nist_raw/C500006531.html` caused exit status 0 and changed the included cohort from **100 to 101**, admitting 3-ethyl-4-methylhexane at 140.4 degrees C. This restores the very grouped-page omission that the v40.2 policy was intended to prevent.

Correction: require every listed archived page to exist before applying the pooling rule. Added a regression test that removes this specific second page and requires failure. The full external verifier compares regenerated outputs against committed files and would detect this cohort change; the defect is the individual builder's failure to diagnose its missing input. This finding does not allege that the complete committed 100-molecule cohort is wrong.

### 2. Four adversarial tests fail in their own CSV harness — medium priority

Location: [`verify_loyola_v35.py`](https://github.com/Singati2/LOYOLA-PAPER/blob/ab9e1df209d3f570c8795b508a54c28a852dae2a/verify_loyola_v35.py), `run_selftest` / `prov_line`.

A fresh locked-environment run reported 113 tests with **four misbehaving tests**. All four raised `csv.Error` about newlines in an unquoted field. The helper splits only CRLF while ordinary text reads normalize newlines to LF. Thus the four intended provenance corruptions never reach the verifier. These are harness failures, not evidence that the verifier accepts those corruptions.

Correction: split text using `splitlines()` so both LF and CRLF input work. Validation results are recorded below.

### 3. Structural checks are partly fail-open — medium priority

Location: [`structural/structural_checks.py`](https://github.com/Singati2/LOYOLA-PAPER/blob/ab9e1df209d3f570c8795b508a54c28a852dae2a/structural/structural_checks.py).

`S3_certify()` returns normally with no witnesses. A failed nonempty certificate prints `NOT certified` without raising. S2 logs an alleged exact GA collision without enforcing it, and S4 logs rank exceptions without enforcing the claimed exception set.

Correction: reject an empty witness set and failed crossing certificates; assert the exact GA collision and the expected degree-6/degree-7 rank outcomes. The underlying reported witness passed an independent check; this defect concerns what the checker would do if a result changed.

### 4. Size-adjusted PRESS is unreliable when a deletion changes rank — medium priority

Location: [`external/bp/bp_tests.py`](https://github.com/Singati2/LOYOLA-PAPER/blob/ab9e1df209d3f570c8795b508a54c28a852dae2a/external/bp/bp_tests.py), `press_size`, `_standardize`, `fit_pred_size`.

The shortcut residual/(1-h) requires the deleted design to preserve rank. With `z = [6,7,8,9,10,11]`, `x = [0,0,0,0,0,1]`, and `y = [0,1,2,4,3,9]`, the shortcut gives RMSE **12.56439573**, while explicit leave-one-out refits using the repository's own prediction convention give **2.05060137**. The existing implementation intentionally filters full-design singular or ill-conditioned candidates by assigning infinity. That eligibility policy is distinct from the deletion-rank defect and is preserved. Scaling an ordinary descriptor by 1e200 or 1e-200 incorrectly produces infinity.

Correction: rescale extreme inputs before standardizing; use explicit refits for deletion-induced rank loss or leverage-one cases among eligible full-design candidates; retain the fast shortcut and the existing full-design eligibility filter. Allowing previously filtered full-design candidates would change per-seed results and the experimental selection policy, so that broader change is not included. Added deletion-rank and extreme-scale tests. A separate check of selected candidates in all four families, seed 0 and budget 100 on the pooled cohort, agreed with explicit refitting within **1.7e-13** before these changes. The adversarial defect therefore does not by itself establish an error in a published cell.

### 5. Checksum manifest omits eight tracked files — medium priority

`python manifest.py` failed at the reviewed commit. Missing entries:

- `entropy_api44_sensitivity_v41.csv`
- `prose_claims_a.py`
- `prose_claims_b.py`
- `prose_numbers_check.py`
- `verification_logs/v40.8/README.txt`
- `verification_logs/v40.8/core_verify.log`
- `verification_logs/v40.8/prose_numbers_check.log`
- `verification_logs/v40.8/source_sensitivity.log`

Correction: regenerate the manifest after staging all new audit files and final edits, then require `python manifest.py` to pass. Existing checksum entries were not reported as mismatches in the initial snapshot check.

### 6. Edge-feature rank is not, by itself, fitted-QSPR identifiability — mathematical wording

Location: [`main.tex`](https://github.com/Singati2/LOYOLA-PAPER/blob/ab9e1df209d3f570c8795b508a54c28a852dae2a/main.tex), paragraph following the per-graph identifiability result, around lines 879–883.

The statement that only common rescaling leaves correlations unchanged is false: Pearson correlation is also unchanged by adding a constant to every descriptor value, and its absolute value is unchanged by any nonzero affine rescaling. OLS with an intercept is likewise invariant to descriptor translation and nonzero scaling.

Full affine rank of the union of edge features rules out the stated uniform edge-weight rescaling direction. It does not automatically establish identifiability of the molecule-level sums after fitting an intercept and slope. Those are different maps. Suggested replacement:

> The union of the octane edge features has affine dimension three, so no nonzero direction produces a common multiplicative rescaling of every edge contribution. This edge-level statement does not alone establish identifiability of the fitted QSPR model, which is invariant under affine transformations of its descriptor.

No theorem or manuscript text was silently rewritten in the accompanying software fixes. Further model-level identifiability claims need their own proof or explicitly scoped numerical Jacobian check.

Minor documentation issue: the reviewed README's leading version paragraph still says v40.5 although the snapshot is v40.8. The accompanying fixes update it.

### 7. Fractional-point exploratory output is stale — medium priority

Location: `structural/fractional_points_out.txt`. A fresh run of the committed script and current data changes both the octane entropy and pooled-cohort rows. For example, entropy Q2 at (alpha,beta,gamma)=(0,0.5,0) changes from the committed 0.915 to 0.907; the corresponding gamma=1 value changes from 0.844 to 0.837. Some pooled cells change by one unit in the displayed third decimal. The concluding win count remains **52 of 81**.

Correction: regenerated the output and added `audit/check_exploratory_outputs.py`, which rebuilds it, the chi-floor output and calorimetric availability CSV in an isolated copy and compares exact bytes. This exposes a coverage gap in the old verification map: committing an auxiliary output was not equivalent to checking it against current inputs.

### 8. Calorimetric availability script depends on current working directory — low priority

`python external/bp/build_calorimetric_set.py` from the repository root fails with `FileNotFoundError` for `nist_alkanes_skeletons_audit.csv`. Relative input/output paths are tied to the invocation directory instead of the script directory.

Correction: anchor the input CSV, archived individual-point pages and output path to the script location. The resulting committed availability CSV is unchanged. The isolated auxiliary-output check invokes the script from an unrelated directory.

### 9. Formal verifier compares theorem names in a locale-dependent order — low priority

The pinned Lean build completed successfully and printed all 36 expected axiom reports, but the original `formal/verify.sh` returned failure because it sorts reported names using the ambient locale while comparing against the literal order of the committed expected file. The two sets contain the same names. Case/underscore collation changes their order.

Correction: sort both lists using `LC_ALL=C` before comparison, retaining count, duplicate and unexpected-axiom checks. The patched verifier passes all 36 reports. This was a false rejection by the script, not a theorem failure.

## Mathematics reviewed

The closed-form reductions, augmented-feature determinant argument, log-sum-exp mean/covariance identities and convexity, gamma monotonicity, size/imbalance factorization, ratio-plane histogram argument, pendant-path extension, generalized Descartes/Laguerre crossing bound, per-graph affine-rank interpretation, Cauchy–Schwarz inequality, connected-graph bounds, asymptotic finite-sum reasoning, and generic discrimination argument were examined. I found no contradiction in these central arguments under their stated assumptions.

Independent checks in `audit/check_mathematics.py` go beyond reproducing decimal output:

- At 50-digit interval precision, every one of the **7,525** subsets of two to four degree pairs for maximum degree 6 has a minor excluding zero at the claimed rank.
- For maximum degree 7, among **24,129** subsets, the only exception is `((1,7),(2,6),(3,5),(4,4))`; its common degree sum gives the stated affine-rank obstruction.
- Both reported crossing profiles are realized by enumerated 12-vertex trees. Exact rational coefficients have five sign variations. Interval evaluation proves opposite nonzero endpoint signs in five disjoint brackets: [-17.18,-17.16], [-11.97,-11.95], [-2.04,-2.02], [2.72,2.74], [31.12,31.14]. Continuity gives at least five crossings; the stated Laguerre bound gives at most five.

The high-precision recount reproduced all committed structural counts at 32 significant digits, including Table S4. Such recounting is strong numerical evidence; it should not be conflated with a symbolic equality proof for every algebraic index value. Logarithmic or ratio statements require at least one edge; adding an explicit nonempty-edge condition where relevant would make domain conventions clearer.

The Lean source has a limited, disclosed scope: 36 selected theorems on degree-pair objects, bounds, convexity, independence and explicit profile certificates. It does not formalize every graph-theoretic realization, strictness condition, transcendence argument, crossing bound or statistical conclusion. After resolving a process-path startup problem in this audit environment, the official pinned Lean 4.34.1 toolchain built the project successfully. The original name-order check exposed finding 9; the patched verifier passes with 36 fresh axiom reports, no `sorry`, no explicit extra axiom declarations or `native_decide`, and dependencies restricted to `propext`, `Classical.choice` and `Quot.sound`. The optional environment adapter in `audit/runtime` redirects only Lean's own executable-path lookup; no Lean sources or kernel were changed. See the original and fixed formal logs.

## Experiments and statistical interpretation

The nested outer/inner leave-one-out design is appropriate for assessing the stated search procedures. Training-fold preprocessing and ridge selection were inspected. The full degree-pair count baseline is a useful comparison because every index in the family is a weighted sum of those counts.

The following limitations matter when interpreting the otherwise reproducible outputs:

1. **Small datasets and post-selection comparisons.** The 18-octane descriptive correlations and globally chosen anchor pools are exploratory. Local tuning inside a previously selected anchor pool is not independent confirmation of the whole selection process. The current supplement substantially acknowledges this.
2. **Seeds are optimizer repetitions.** A 95/100 or 40/50 seed win count is not that many independent molecular datasets, experimental replications or hypothesis tests. The preregistered rule defines a decision protocol, not a conventional population-level significance test.
3. **Conditional bootstrap intervals.** The molecule bootstrap resamples already fitted out-of-fold predictions without refitting or rerunning search. It conditions on those predictions and does not include full model-selection uncertainty. Overlapping cross-validation training sets also complicate an independent-errors interpretation. Intervals containing zero do not establish equivalence or prove absence of useful effects.
4. **Search budgets and boxes.** Equal numbers of random candidates do not give equal coverage of two- and three-dimensional spaces. Lower gamma-model Q2 can reflect selection, estimation or search behavior; it is not proof that gamma intrinsically has no information. Conversely, a narrow-box advantage does not establish superiority over a sufficiently searched parent family. The manuscript now limits these claims reasonably.
5. **External-validation scope.** Refitting/calibrating on nonanes or decanes under LOO evaluates those cohort-specific procedures, rather than a completely frozen octane-trained predictor. The pooled C6–C10 cohort includes previously studied molecules and substantial size variation, so its high Q2 is not a wholly new independent replication. Size-only comparisons and within-carbon-number diagnostics are important context.
6. **Coverage bias.** A nonsignificant included-versus-excluded comparison is not proof of unbiased data availability, especially with small groups. It can only constrain the particular detectable differences examined.

These limitations support the phrasing **“no demonstrated benefit under the stated protocols”**, not **“gamma can never improve prediction.”** Nested selection is discussed in the primary methodological reference [Cawley and Talbot (2010)](https://jmlr.csail.mit.edu/papers/v11/cawley10a.html).

Bibliographic spot checks confirmed the publisher records for [Rada's 2026 finite-dimensional framework](https://match.pmf.kg.ac.rs/issues/m96n3/m96n3_32925.html), [Rada's 2019 exponential-index paper](https://match.pmf.kg.ac.rs/content82n1.htm), and [Molina et al.'s 2025 parent-family paper](https://www.aimspress.com/article/doi/10.3934/math.2025094). These support retaining the manuscript's explicit acknowledgment of prior linear frameworks, exponential transformations and parent-family reductions. They do not establish uniqueness of the new combination or settle all novelty claims.

Repository history supports the intended preregistration order: nonane protocol commit `964b127` (3 October, 15:54 -04:00) precedes the first result commit `9925655` (16:20); boiling-point protocol commit `a5cf378` (5 October, 09:58 -04:00) precedes the first result commit `05baef8` (12:19). Their ancestry was checked. These are repository records, not independently registered timestamps. Subsequent deviations and the grouped-page correction are disclosed; the final cohort is an amended implementation rather than an untouched initial protocol.

## Property sources and physical comparability

Dataset rebuilds test agreement with archived sources and parsing policies, not the truth of every experimental determination. NIST WebBook is an authoritative collection but includes both primary measurements and compilations. The nonane enthalpy endpoint is dominated by compiled values: only four of 34 are calorimetric, with one additional averaged entry. It is therefore weaker evidence for experimental validation than the boiling-point endpoints.

I downloaded and visually checked [NBS Circular 461](https://nvlpubs.nist.gov/nistpubs/Legacy/circ/nbscircular461.pdf), Table 3p, printed page 159 / PDF page 177. Its gas-phase entropy column at 25 degrees C gives the six historical values used by the v40.8 sensitivity script: 108.35, 103.06, 104.38, 105.43, 103.48, and 103.14 cal/(degree mole), with the ethyl/methyl names in the table written in the alternative order. These values verify the historical sensitivity input; they do not authenticate the different later values used in the main octane dataset.

Re-running source sensitivity reproduced the omega maximum correlation shift 0.0032, the compiled-entropy alternative shift 0.0431, and the 1947-entropy alternative shift 0.0180. The latter changes the best absolute-correlation index from HM to M1. Remaining primary-source gaps and the tetramethylbutane reference-state issue should remain disclosed; they cannot be resolved by simply relabeling provenance rows as verified.

## Fresh validation record

The Python requirements were installed from `requirements-lock.txt`: Python 3.12.14, NumPy 2.4.4, SciPy 1.17.1, NetworkX 3.6.1, mpmath 1.3.0. Earlier starts before dependency installation were discarded from the validation record.

| Check | Result |
|---|---|
| Core verifier: calculations, eight guarded numeric tables, canonical figures and analysis artifacts | PASS, zero failures |
| Overleaf bundles and document artifacts | Canonical TeX/figure entries match all three ZIPs; PDFs have 42 and 21 pages; v40.8 entropy-source paragraph present in paper PDF; no fresh TeX build claimed |
| Prose-number checker | PASS: 719 checked; 16 explicitly uncheckable cited values |
| Original quick regression suite | PASS: 6 tests |
| Original adversarial selftest | FAIL: 4 harness failures out of 113; 109 passed |
| High-precision structural recount | PASS: all counts and Table S4 reproduced |
| Independent interval rank and crossing checks | PASS; patched 50-digit reported-witness certificate also PASS |
| Constancy-test comparison | PASS: 140,262 triples; no old/new disagreement on tested folds |
| Source-sensitivity rerun and original NBS table inspection | PASS within the scope described above |
| Patched quick regression suite | PASS: 10 tests |
| Auxiliary fractional-point, chi-floor and calorimetric availability outputs | PASS after stale fractional-point output was regenerated |
| Full external reproduction | PASS: source rebuilds, baseline tests, analyses and guarded tables |
| Patched adversarial selftest | PASS: all 113 tests |
| Final patched pooled boiling-point reproduction | PASS: all 50 seed results, bootstrap summary and pooled baselines match published outputs; decane one-predictor path unchanged |
| Original formal checker after successful build | FAIL: locale-dependent name ordering; 36 reports present |
| Patched formal verifier | PASS: successful build and all 36 fresh expected axiom reports |
| Archived boiling-point page identities | PASS: 154 molecular formulas and carbon skeletons match records |

The exhaustive original order-12 floating-point crossing search was not repeated; the reported witness was checked directly with intervals. I have not independently reproduced every exploratory solver diagnostic, conducted a complete novelty search, or located definitive primary determinations for all unresolved property entries. Those limitations are distinct from the confirmed defects above.

The final fixes preserve the published boiling-point seed results, summaries and baselines. The regenerated auxiliary fractional-point file changes the stale entropy/pooled display cells described in finding 7, while its 52-of-81 headline remains unchanged.

## Next scientific priorities

Resolve the later entropy and enthalpy reference-state provenance; clarify edge-level versus fitted-model identifiability; retain the negative conclusion's protocol-specific scope; and seek genuinely new measured cohorts if stronger predictive claims are intended. Report optimization and source sensitivities alongside any headline improvement. Software checks should exit unsuccessfully when a claimed certificate is missing or false, and source archives should be treated as required inputs.
