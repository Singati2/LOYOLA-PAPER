**LOYOLA-PAPER: code, data, mathematics, and experiment review**

Review date: 20 October 2026 (UTC)  
Repository: [Singati2/LOYOLA-PAPER](https://github.com/Singati2/LOYOLA-PAPER)  
Primary reviewed revision: [67e36adb434cdad25f8e19e42349a1f550bc11b6](https://github.com/Singati2/LOYOLA-PAPER/commit/67e36adb434cdad25f8e19e42349a1f550bc11b6), branch `revision/v40.31-scientific`.

The central numerical results survived the checks performed here. The newest revision also corrects several substantive overstatements present in earlier drafts. I would nevertheless fix the reproducibility defects and reporting inconsistencies below before freezing a submission. This review found no demonstrated change to a registered scientific verdict; it did find ways for the new reproduction workflow to report success without validating the current source or complete checkpoint contents.

Scope: the linked repository, its six published branches, recent changes, mathematical arguments, principal computation paths, data builders and provenance, experiment design, notebooks, verification machinery, and compiled documents. Branches were mapped and compared; they were not each subjected to a separate full experiment replay. This is not an audit of the other repositories on the Singati2 account, nor a claim that every line has been independently proved correct. No changes were pushed.

The latest work is not on `main`. A reviewer following the default GitHub page can therefore read an older scientific and computational package.

| Branch | Head | Last commit date |
|---|---|---|
| revision/v40.31-scientific | 67e36adb | 17 Oct 2026 |
| audit/v4030-adversarial | f109127b | 16 Oct 2026 |
| audit/provenance-final | 716cd371 | 12 Oct 2026 |
| main | 0c4a4db0 | 12 Oct 2026 |
| robustness-guards | 01bfaf55 | 10 Oct 2026 |
| research/weak-discrimination | 41db8c10 | 9 Oct 2026 |

PRs #3, #4, and #5 form a stack; #5 explicitly says “review only, do not merge.” The repository API returned no tags during this review. The latest successful [GitHub Actions run](https://github.com/Singati2/LOYOLA-PAPER/actions/runs/39066288218) runs the fast offline suite. It does not establish that every experiment, source retrieval, notebook, or Lean proof was freshly rerun at the latest head.

**Corrections, ordered by practical importance**

P1 means fix before relying on the affected workflow or distributing it to reviewers. P2 means a concrete correctness or reporting correction before release. P3 means useful maintenance. These priorities concern the affected behavior, not an allegation that the whole paper is invalid.

| ID | Priority | Finding | Required change |
|---|---|---|---|
| R1 | P1 | Colab checkpoints can produce a false `COMPLETE` report after source changes or missing cached outputs | Bind checkpoints to source, inputs, environment, and output hashes; invalidate stale stages and reject incomplete state |
| R2 | P1 | A failed token-authenticated Colab clone can expose the token in its exception | Keep credentials out of command arguments and sanitize failure output |
| R3 | P2 | Exact tie checker accepts empty reference-count files | Require complete, unique reference coverage before comparing |
| R4 | P2 | “57 of 100” does not describe all aggregate-derived boiling points | State 57 direct AVG rows plus one mean of two AVG records: 58 aggregate-derived values |
| R5 | P2 | Strict-subset output calls a molecule bootstrap a seed bootstrap | Correct the label, regenerate its output, and identify the resampling unit |
| R6 | P2 | Table 5 says uncertainty is understated “several-fold,” without a comparable calibrated interval | Remove the numerical multiplier and retain the conditional-interval limitation |
| R7 | P2 | Reviewer links, release identity, and coverage descriptions disagree | Publish one exact revision entry point and an explicit verification/coverage inventory |
| R8 | P2 release decision | Raw-page removal is complete only in the newest branch tree | Resolve the already-documented distribution/history decision while preserving preregistration evidence |
| R9 | P3 | Numerical implementation and document maintenance can be simplified | Reuse SVD quantities for PRESS; generate status counts; keep paper claims separate from audit history |

1. **R1 — Colab completion does not authenticate the computation it reports.**  
   Source: [colab/pipeline.py, commit/state checks](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/colab/pipeline.py#L118), [skip logic](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/colab/pipeline.py#L198), and [report](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/colab/pipeline.py#L229).

   The runner records HEAD, but a successful marker is reused solely because its `ok` field is true. It does not verify the source or input files used by that script. The report compares only outputs listed in `files.json`; it does not verify all tracked source files. Missing cached artifacts are silently skipped during restoration.

   Reproduction: use the actual pipeline module with a temporary git repository and one output-producing stage. Run successfully, replace its tracked script with `raise SystemExit(17)` without committing, and rerun. The stage is skipped and the report still returns zero with `COMPLETE`; directly running the current script exits 17. Delete its cached output and the report also returns zero, falling back to the output already present in the working checkout. Neither fixture modifies the reviewed repository.

   Correct the state model: record a source/input/environment digest per stage, an explicit expected-output inventory, and each output digest. Validate markers and cached files before reuse; invalidate downstream stages when an input changes. A dirty source tree must either be rejected or have its exact content identified as a separate run. Comparing only files detected by modification time is insufficient to prove that every required output was regenerated.

   Acceptance checks: edited source cannot silently reuse an old success; missing or corrupt cached output fails; upstream input changes invalidate dependent stages; a clean interrupted run resumes successfully; the final report distinguishes cached verified results from scripts executed in the current session.

2. **R2 — Token-containing clone commands are printable on failure.**  
   Source: [colab/make_notebooks.py](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/colab/make_notebooks.py#L28), replicated into the 12 numbered Colab notebooks.

   The setup inserts `GITHUB_TOKEN` into the HTTPS clone URL and passes that URL to `subprocess.run(..., check=True)`. Python's `CalledProcessError` includes the command arguments in its displayed exception. The remote URL is cleaned only after a successful clone.

   A test with a deliberately fake token confirmed it appears in the exception string. No real credential was used or observed. This affects the optional authenticated access path, not ordinary public cloning.

   Use a clean repository URL with a credential helper or `GIT_ASKPASS` mechanism; keep the secret out of argv and notebook output. Handle errors without printing credential-bearing commands, clean up temporary credentials in a `finally` block, and regenerate all notebooks. Test a forced clone failure with a fake secret and assert that neither logs nor exceptions contain it.

3. **R3 — Exact comparison coverage is optional when it should be mandatory.**  
   Source: [structural/exact_ties.py, reference parser and comparisons](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/structural/exact_ties.py#L74).

   `committed()` permits empty dictionaries; the comparison branches use `if ref` and `n in chi_ref`. Running the actual checker in a temporary folder with empty `hp_counts_out.txt` and `chi_floor_out.txt`, while retaining the normal fractional-point reference, exits zero and prints “all numerical counts certified exactly.” The independent exact enumeration still happens, but the intended R/GA/q-histogram and chi reference comparisons disappear silently.

   Assert the exact expected key sets for each input file, including uniqueness and valid parsing, before enumeration. Report how many reference records were compared. Add missing, empty, truncated, duplicate, and malformed-reference tests. The repository manifest is a separate protection against accidental changes; it does not replace a self-contained coverage assertion in this checker.

4. **R4 — Distinguish direct averages from all aggregate-derived values.**  
   Sources: [supplement.tex](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/supplement.tex#L1037), [prose_claims_a.py](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/prose_claims_a.py#L309), and `REVIEWER_START_HERE.md:93`.

   The provenance has 57 included rows whose rule is directly `AVG`, plus one included molecule whose rule is “mean of 2 NIST averages (agreeing within 3 K).” That molecule is 3-methylhexane, grouped from records C589344 and C6131244. Thus 58 of the 100 values depend on averages. The quality ledger already classifies 58 as A-AGG; the strict subset contains the other 42.

   The current prose-number helper uses `.startswith("AVG")`, so it verifies the narrower count and misses the grouped-average case. Clarify the prose as “57 values use a NIST average directly, and one is the mean of two NIST averages; 58 are aggregate-derived.” Generate this count from the same classification used by the quality ledger. This is a category/wording correction, not a reason to alter the registered numerical dataset.

5. **R5 — The strict-subset interval label names the wrong sampling unit.**  
   Sources: [audit/v4030/gamma_strict.py](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/audit/v4030/gamma_strict.py#L2) and [external/bp/bp_tests.py, boot_ci](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/external/bp/bp_tests.py#L157).

   The script and saved output say “seed-bootstrap interval.” They call `run_test`, whose `boot_ci` resamples molecule indices and takes the median contrast across the fixed set of seed predictions. It does not resample seeds.

   Replace the label with “95% molecule-bootstrap interval, conditional on fitted outer predictions.” Regenerate `gamma_strict_out.txt` and check any downstream quotations. Keep the results identified as exploratory strict-subset analyses. The existing results are decanes: median difference −0.1294, 12/50 wins, interval [−0.1858, −0.0292]; strict pooled C9–C10: −0.0397, 10/50, [−0.0907, −0.0053]. This correction changes their description, not their numerical values or the registered verdict.

6. **R6 — Remove the unsupported uncertainty multiplier.**  
   Source: [main.tex, Table 5 caption](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/main.tex#L1720), versus the explanation beginning around line 1750.

   The caption still says the registered intervals “understate the uncertainty several-fold.” The nearby text correctly explains that the refitted 80% subsample ranges differ in training size and seed averaging, are not directly comparable, and are not confidence intervals for the full-sample contrast. Their width ratio therefore does not estimate a calibrated uncertainty multiplier.

   Suggested replacement: “The registered intervals are conditional on the fitted outer predictions and omit refitting and model-selection uncertainty; exploratory refitted subsample ranges are reported below.” Keep the current warning that no gain was demonstrated under these protocols and that equivalence was not established.

7. **R7 — Make the reviewer entry point and coverage claims accurate.**  
   Sources: [REVIEWER_START_HERE.md](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/REVIEWER_START_HERE.md), [README.md](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/README.md), `REPRODUCE.md`, `colab/make_notebooks.py`, and `.github/workflows/verify.yml`.

   The reviewer guide targets a future `v40.30` tag that does not exist. The README still leads with v40.29 and links the older `main` notebooks. The new Colab notebooks use a mutable revision branch; when their work directory already exists, setup does not ensure that its HEAD matches the requested revision. An existing environment is likewise reused based on the Python executable's presence, without validating its dependency fingerprint.

   Use one exact commit for the present review package and one deliberate release tag after corrections. Verify both the checked-out revision and environment on setup. Distinguish the older lightweight notebooks from the new staged replay. Update the 733/20 prose counts to the observed 756 checked/22 uncheckable entries; describe the Lean checker as 38 explicitly listed checks plus all 52 declarations where applicable. The older 38-theorem wording alone is incomplete.

   Coverage also needs precision. The new pipeline lists 60 commands and `audit/run_all_scripts.py` lists 61. Both omit `audit/permutation_pipeline_audit.py` and `audit/v4030/uncertain_source_crosscheck.py`. The permutation audit explicitly documents itself as a separate run, so its omission is not hidden; nevertheless “every script” is too broad. Add a clearly named optional audit stage or list these exclusions and require their separate evidence before claiming complete coverage. Lean, notebook execution, and document compilation also need separately recorded status.

   Run and archive the full release validation at the final frozen source revision. Older logs remain useful evidence about their own commits, but must not be relabeled as current-head full validation. The green current CI result is correctly limited to fast offline checks.

8. **R8 — Finish the repository's existing raw-source distribution decision.**  
   Source: [audit/NIST_HISTORY_REMEDIATION_PLAN.md](https://github.com/Singati2/LOYOLA-PAPER/blob/67e36adb434cdad25f8e19e42349a1f550bc11b6/audit/NIST_HISTORY_REMEDIATION_PLAN.md).

   The newest tree removes 262 raw WebBook pages and adds explicit retrieval with digest checks. Those pages remain in older branch tips, including `main`, and in history. Therefore removing them from the latest branch is not a repository-wide removal.

   Resolve the author decision already documented in the repository about permission, public distribution, and preservation of the original preregistration commits. Retain original evidence and document any old-to-new revision mapping if history is ever changed. This review confirms repository state; it does not make an independent legal determination or recommend silently rewriting history. No visibility or history change was performed.

9. **R9 — Optional hardening and editorial maintenance.**  
   The pooled PRESS implementation already computes an SVD for rank and leverage guards but still uses the inverse of the normal equations for its residuals and reported leverages. Reusing the orthonormal factor would simplify the numerical path and avoid squaring the condition number. This is a maintenance recommendation, not a reproduced current-data error: an independent SVD calculation for three pooled outer folds, 2,000 LOh candidates each, agreed in selected candidate and differed in PRESS by at most about 1.9 × 10⁻¹⁴.

   Generate version/count/status text from one metadata source where practical. Keep historical audit files intact but label superseded conclusions prominently. The compiled paper is 42 A5 pages and the supplement 28; spot-checked pages are legible, with no detected out-of-page text. Table 5 is dense. A tighter distinction between the main mathematical contribution and the extensive audit history would improve readability; this is editorial advice, not a journal length-rule violation.

**Data corrections and limitations that still matter**

These are largely already disclosed in the newest manuscript. They must not be presented as newly discovered errors, silently “fixed” by changing preregistered outcomes, or erased from the limitations.

| Data issue | What the current evidence establishes | Correct treatment |
|---|---|---|
| Seven octane entropy values and the tetramethylbutane enthalpy | Primary-source agreement remains unresolved for these benchmark entries | Obtain original determinations where possible; retain explicit unresolved labels and sensitivity variants |
| Tetramethylbutane ΔH_vap = 8.41 kcal/mol | Reference-state/source problems remain; a crystal sublimation enthalpy is not automatically a liquid vaporization enthalpy | Preserve the phase distinction and exclusion/alternative-value sensitivities; do not substitute a crystal value into a liquid column |
| Eighteen octane acentric factors | The benchmark values are compiled; a matching primary determination for the entire column was not established | Keep source-quality qualification; document alternative TMB values rather than claiming primary validation |
| Nonane vaporization enthalpies | 29/34 are compilation entries, four are direct primary determinations, and one is an aggregate | Treat this as a limited external benchmark; four strict primary cases cannot support a broad high-precision replication claim |
| 3-ethyl-4-methylhexane boiling point | 413.55 K versus 407.15 K for an enantiomer entry; source discrepancy remains | Keep the conflict and sensitivity analysis; retain its exclusion from the pooled set under the registered spread rule |
| 2,2,6-trimethylheptane duplicate determination | Counting the duplicated row once changes 148.20 °C to 148.35 °C, stored as 148.4 °C; recorded ridge Q² changes 0.8599 to 0.8591 | Preserve registered values and show a clearly versioned deduplicated sensitivity |
| AVG entries bypass the ordinary 3 K screen | This follows the registered extraction rule, even for quoted uncertainty above 3 K | Describe the exemption honestly; any stricter filtering is a sensitivity analysis |
| Strict pooled dataset | 42 molecules, comprising 14 C9 and 28 C10; no C6–C8 | Call it a C9–C10 sensitivity cohort, not a strict replication across C6–C10 |

The archived-source reconstruction was strong: all 262 old raw pages matched the newest canonical digest manifest, and the latest builders reproduced six dataset/provenance/identity/census CSVs byte-for-byte. This verifies transformation of the available archived records. It does not establish primary measurement quality, completeness of NIST, or agreement of today's live pages. No live WebBook re-download was performed.

**Mathematical and experimental assessment**

The useful central distinction is between information in the degree-pair count vector and how a low-dimensional scalar model uses it. Every member of the index family is a function of those counts. A new parameter can change a restricted prediction model or its search behavior without adding graph information beyond that vector.

The newest version appropriately narrows pure-gamma discrimination to the stated algebraic-parameter conditions, treats minimality as enumeration-assisted, distinguishes degree-pair information from the edge-division vector literature, and limits the Lean claims. Keep those qualifications. The withdrawn weak-discrimination theorem on the research branch should remain clearly separated from the submission.

| Claim/check | Review result |
|---|---|
| Affine dimension of count vectors | Independently reconstructed ranks: octanes 7, measured decanes 7, pooled set 8 |
| Octane count-based error floor | Independently obtained SSE = 117/40 = 2.925 °C², MSE = 0.1625 °C², RMSE = 0.4031128874 °C |
| Interpretation of that floor | A fixed-function indistinguishability bound; not a universal floor on cross-validation predictions fitted separately in different folds |
| First distinct profiles sharing a q-histogram | Reproduced at order 13 for all trees, order 16 for maximum degree at most 4 |
| Exact radical/tie enumeration | Reproduced through order 17; n=17 all-tree profiles 7,778, q-histograms 7,582, R values 7,604, chi values 6,434, GA values 7,581 |
| GA merges | First all-tree merge of distinct q-histograms at order 17; none through order 17 for maximum degree at most 4 |
| Chemical crossing bound | The stated five-crossing bound and the distinction from unrestricted sharpness are appropriate; a degree-6 example does not establish attainability among chemical trees |
| Generic discrimination | Must not be sold as new information uniquely introduced by gamma when the parent family already generically distinguishes the same count profiles |
| 50 search seeds | Describe optimizer variation on fixed molecules; do not treat them as 50 independent experimental samples |
| Equal search budgets in 2D and 3D | A fair declared computational protocol, but not proof that the extra parameter can never help; the 3D search may be disadvantaged |
| “No demonstrated gamma gain” | Supported as a protocol-specific conclusion; does not establish equivalence or a universal absence of useful effects |
| Pooled Q² near 0.99 | Carbon-number variation contributes strongly; preserve the size-adjusted and fixed-carbon comparisons |
| Wiener W + p3 comparison | Independent LOO Q² = 0.9038067173 on 34 decanes; descriptive comparison, without turning a historically selected model into an untouched new confirmation set |

After the request to continue, I extended the checks in three directions. An independently written SVD implementation reran the observed nested ridge fit and all 200 registered response permutations, selecting the penalty separately for each response inside each training fold. It reproduced observed Q² = 0.8598706416; permuted median −0.0881800489, 95th percentile −0.0087071759, and maximum 0.1952448321. None met the observed result, giving the plus-one permutation p-value 1/201 = 0.0049751244. This supports the registered within-decane association test; it does not resolve measurement provenance or prove performance on a new external population.

An independent graph-atlas search checked 30,845 bound instances on all 995 connected simple graphs of orders 2–7, across the stated parameter grids. The upper/lower equality cases, bracket bounds, positive-reference ratio bounds, and Cauchy–Schwarz interpolation all passed. This finite search supplements the proof review; it is not a proof for arbitrary graphs or parameters.

The repository's longer independent mathematics audit also reproduced its committed output exactly, including all-tree enumeration through order 17, the five-crossing witness, the degree-7 rank exception, and path/star extrema through order 14. The adversarial numerical probe again showed that the new leverage guard rejects the old undefined-fit example, and all 400 well-posed random designs agreed with the high-precision reference. Some printed error magnitudes differed across environments, as the repository already anticipates; those differences are retained in the evidence. The same probe reconverted 78 parsable octane source values, with 74 inside its tolerance and the four remaining differences already classified as source variation/conflict. Several formatted source fields were unparsed, so this is not a blanket validation of all measurements.

I found no reason in these checks to reverse the paper's principal registered conclusion. The strongest remaining scientific qualification is source quality and the limited inferential scope, rather than a demonstrated arithmetic failure.

**What was actually executed**

The audit used Python 3.12.14 with the repository's pinned core dependency versions, including NumPy 2.4.4, SciPy 1.17.1, NetworkX 3.6.1, SymPy 1.14.0, and mpmath 1.3.0. The repository's designated Python/CI version is 3.13, so this was an additional environment check, not an exact interpreter reproduction.

| Execution | Result | Evidence file |
|---|---|---|
| main: `python verify.py` with its archived pages | ALL PASS, including source/auxiliary checks | verify-fast.log |
| newest revision: `python verify.py --offline` | ALL PASS for the offline fast path; source/auxiliary stages explicitly NOT RUN, one regression test skipped | latest-fast.log |
| newest exact tie enumeration | Exact counts reproduced through n=17 | exact-ties.log |
| Independent rank, exact floor, graph-distance, and nested ridge computations | Reproduced the stated ranks/floor and baseline results | independent-review.log; independent_review.py |
| Latest builders with the historical archived pages, in a temporary copy | Six CSVs byte-identical; all 262 canonical hashes matched | independent-review.log |
| Registered Tests A and B, seeds 0 and 49, all four model streams | 16 Q² results match committed values within 5.0 × 10⁻¹¹ | targeted-replay.log; targeted_replay.py |
| Independent SVD PRESS comparison, pooled seed-0 LOh candidates, outer folds 0/49/99 | Same selected candidates, maximum absolute difference about 1.9 × 10⁻¹⁴ | targeted-replay.log |
| Independent SVD nested-ridge replay of all 200 registered permutations | All four reported summary values reproduced; p = 1/201 | independent-permutations.log; independent_permutations.py |
| Independent finite-graph bound/equality search | 30,845 checks on 995 connected graphs; no counterexample | independent-bounds.log; independent_bounds.py |
| Longer repository independent mathematics audit | Exact committed text reproduced | extended-math.log |
| Repository adversarial solver, constancy, and source-conversion probes | Behavioral conclusions reproduced; floating-point error-print differences retained | extended-counterattack.log; extended-replay-differences.txt |
| Pipeline dirty-source and missing-cache probes | Reproduced R1 | independent-review.log |
| Fake-token exception probe | Reproduced the disclosure mechanism in R2 | independent-review.log |
| Empty reference-file probe | Reproduced R3 with exit zero | exact-certificate-missing-reference.log |
| Label/citation/bundle check | Passed | labels.log |
| PDF inspection | Selected pages visually checked; no out-of-page text detected in page-coordinate scan | Inspection described here |

Independent nested ridge results, with penalty selection and scaling confined to training partitions:

| Cohort | n | Q² | RMSE (°C) |
|---|---:|---:|---:|
| Decanes | 34 | 0.8598706416 | 2.9360254379 |
| Pooled C6–C10 | 100 | 0.9910686922 | 2.6609199580 |
| Strict decanes | 28 | 0.8514698353 | 2.9838318233 |
| Strict pooled C9–C10 | 42 | 0.9508951252 | 2.5394419327 |

Not freshly rerun here: the entire 50-seed experimental ensemble, all selection-aware resampling runs, the repository's separate scikit-learn permutation script, every notebook in Colab, a new Lean build, or an end-to-end `verify.py --everything` at the latest commit. The full 200-permutation calculation was independently rerun using the SVD implementation described above. Existing repository logs were examined as historical evidence, not relabeled as executions of this review. Prior-art novelty was not exhaustively established by this audit.

**Recommended completion order**

Fix R1 and R2 first, with small failure-case tests that prove the fixes. Correct R3–R6 and regenerate only their affected outputs and document bundles. Consolidate release identity and coverage under R7, and resolve the existing distribution decision under R8. Then run full validation once against the chosen final source revision, archive its environment and explicit pass/fail/not-run inventory, and freeze the submission. Retain registered data/results and put data changes in versioned sensitivities.

The accompanying evidence archive contains the independent audit scripts, execution logs, repository state snapshot, and this report. It excludes raw third-party source pages and the repository itself.

