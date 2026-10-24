# Numeric registry anchor audit, 2026-10-23

**Scope.** This audit covers the prose-number registries `prose_claims_a.py` and `prose_claims_b.py`, as checked by `prose_numbers_check.py`. Each entry pairs a regular expression, whose capture group `v` must match exactly once in the stated file, with the value recomputed from data.

**The problem.** A pass means only that the captured token equals the recomputed value. If the expression lands on the wrong token, the claim in the prose goes unchecked even though the entry passes.

## 1. Wrong matches found

| Entry | Intended claim | Was matching | Now matching | Expected value (source) |
|---|---|---|---|---|
| `ext_tb_avg20` | 20 nonane boiling points are NIST averages | the `020` inside DOI `10.1007/s40747-020-00262-0` in the supplement bibliography | supplement S4: "…differ in evidential status. **Twenty** of the $35$ boiling points are NIST averages" | `word(non_tb_rule('NIST average'), True)` = "Twenty"; `nonane_provenance.csv`, T_B rows with rule "NIST average…": 20 |
| `ext_tb_single5` | 5 are single NIST determinations | the `5` in $(3,5)$ of the degree-sum example | "(13 quoted only to 1 K). **Five** are single NIST determinations" | `word(non_tb_rule('single NIST'), True)` = "Five"; 5 |
| `ext_tb_recent10` (new) | 10 are the most recent primary determination | — | "…determinations and **ten** are the most recent primary determination" | `word(non_tb_rule('no NIST AVG'))` = "ten"; 10 |
| `oct_90values` | 90 octane property values were traced | the volume number **90** of Jameson, *Math. Gaz.* **90** (2006) | supplement S1: "attributed to the NIST WebBook. All **$90$**" | `len(PROV)` = 90 (`octane_property_provenance_v35.csv`) |
| `rp_proof_d4` | the order-16 pair has a leaf adjacent to a vertex of degree 4 | the `4` of $(2,4)$ in the unrelated spider example of Supplementary Section S10 | main, proof of Theorem 2(iii): "$(4,4)$ have $q = 0$. Both also have a leaf adjacent to a vertex of degree $d = $ **4**" | `common_leaf_degree(*mol16_pair())` = 4 |

The 20, 5 and 10 were confirmed from `external/nonane_provenance.csv`: of 35 T_B rows, 20 are "NIST average (AVG) value", 5 are "single NIST Tboil determination" and 10 are "no NIST AVG; most recent primary experimental". `word()` gained the entry 20 → "twenty".

**History.** The two nonane anchors date from `ab9e1df` (v40.8, 2026-10-05). They already pointed at the DOI and the degree pair at `0877aa0` and `e25d790`.

## 2. Sweep of all entries

`audit/independent_recompute_2026-10-23/registry_anchor_sweep.py` imports both registries and reads 779 entries. For every entry that matches exactly once, it flags any capture that lies:
- in the bibliography;
- in a URL, DOI or arXiv fragment;
- in a `\label`, `\ref` or `\cite` argument;
- directly inside a degree pair `(i,j)`.

| Run | Flags |
|---|---|
| Before the fixes | 4: `oct_90values` (bibliography), `rp_proof_d4` (degree pair), `cr_alpha`, `sup_frac_16` |
| After the fixes | 2: `cr_alpha` and `sup_frac_16`, both inspected and correct. Each captures the parameter value itself: $(\alpha,\beta) = (-1,0)$ and the point $(\tfrac16, 0)$ |

**Limitation.** The sweep is heuristic. It finds anchors in the wrong kind of context. It cannot find an anchor that lands on the right kind of token in the wrong sentence. Only the flagged entries and the five above were inspected by hand; the other entries were not individually re-read.

## 3. Mutation tests

The tests ran in a throwaway worktree, since removed. Log: `audit/independent_recompute_2026-10-23/registry_mutation_tests_2026-10-23.log`.

| Test | Mutation | Required | Result |
|---|---|---|---|
| M1 | "Twenty" → "Nineteen" | fail | FAIL `ext_tb_avg20` (pattern matched 0 times) |
| M2 | "Five" → "Four" | fail | FAIL `ext_tb_single5` (pattern matched 0 times) |
| M3 | DOI `020` → `021` (supplement) | no false failure | 0 failures |
| M3b | same DOI in main | no false failure | 0 failures |
| M4 | $(3,5)$ → $(3,6)$ | no false provenance failure | only `id_fail_set` fails. That entry legitimately checks this example; no `ext_tb_*` failure |
| M5 | delete "Five … determinations and" | fail closed | FAIL `ext_tb_single5` and `ext_tb_recent10` |
| M6′ | duplicate the anchored "Twenty" sentence | fail closed | FAIL `ext_tb_avg20` (matched 2 times) |
| M7 | *Math. Gaz.* 90 → 91 | no false failure | 0 failures |
| M8 | "All $90$" → "All $89$" | fail | FAIL `oct_90values` and `s1_90` |
| M9 | order-16 $d = 4$ → $d = 5$ | fail | FAIL `rp_proof_d4` (tex 5, expected 4) |

**Notes:**
- An earlier attempt at M6 was a faulty test: the duplicate did not reproduce the anchored phrase, so it produced no second match. The corrected test M6′ is the one recorded.
- M1 and M2 fail as pattern errors rather than value mismatches, because the count words are written literally in the patterns. Both fail closed.
- `s1_90` already checked the same "All $90$", so `oct_90values` is now redundant with it, but correct.

## 4. Counts

| | Before (`f720a16`) | After (source commit `e3fc881`) |
|---|---|---|
| Registry A entries | 462 | 463 (+ `ext_tb_recent10`) |
| Registry B entries | 316 | 316 |
| `prose_numbers_check.py` | "756 checked, 0 failures, 22 uncheckable". At least 4 of these "matched" the wrong token | "757 checked, 0 failures, 22 uncheckable"; the 5 entries above re-anchored |

"757 checked" means 757 entries matched and agreed. It does not certify that every anchor sits on its intended sentence beyond the sweep and the hand-checked entries listed here.
