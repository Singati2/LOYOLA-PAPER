# LOYOLA_V35_REPAIR_LEDGER

Round-14 (v34→v35) findings→repairs are itemized in V34_TO_V35_SCIENTIFIC_CHANGELOG.md (all reproduced before repair). Historical v33→v34 ledger follows.


## §1 baseline inventory (requested v32→v33 change / claimed / present / verified / correct)
| Item | Claimed | Present | Independently verified this round | Correct? |
|---|---|---|---|---|
| GM reframe + novelty removal | yes | yes | re-read of intro/abstract/remark; 39/39 refs | YES |
| log-convexity theory | yes | yes | numeric Hessian PSD re-run; proof re-read | YES, tightened (Var(q)=0 case) |
| γ non-redundancy | yes | yes | rank recomputation Δ=2,3,4 | YES, identifiability remark added |
| GM-vs-LO nested ablation | yes | yes | code re-audited line-by-line (y-independent descriptors, all selection in outer-training); fresh recompute matches | Nested YES; **robustness gap found — repaired** |
| BID collisions | yes | yes | recomputed; names re-derived; [P] audit | YES |
| redundancy/PCA | yes | yes | recomputed (PC1–2 99.05%) | YES |
| structure sensitivity | yes | yes | **published control obtained** (see below) | YES — upgraded to verified-with-control |
| multi-order degeneracy | yes | yes | [N] fresh re-run | YES |
| uniform ratio bound | yes | yes | statement re-read; extrema over finite sets are sign-safe | YES |
| verifier expansion | yes | yes | 80-test selftest re-run | YES, extended to 83 |
| provenance | partial (10-value spot) | partial | **completed this round: full 90-value trace** | now complete |

## Findings → repairs
| # | Finding | Severity | Repair | Verified by |
|---|---|---|---|---|
| 1 | v33's "γ improves 2/5" is seed-dependent: 3-seed × 2-budget grid shows T_B ΔQ² flips sign ([−0.280,+0.136]); only ΔH_vap consistent ([+0.030,+0.076]); ΔH_f consistently negative | MATERIAL (statistical honesty) | Verdict sharpened in abstract, intro (v), §sec:ablation (new robustness paragraph), conclusion: "robust improvement on exactly one property, robust degradation on one, noise on the rest" | ablation_robustness.py/.csv (30 rows); [N2] checks canonical-config consistency + sign-consistency claims |
| 2 | FGD implementation lacked a published control (v33 caveat) | HIGH-risk area, resolved POSITIVELY | Open-access primary (Barman–Das MATCH 95 (2026) 63–94) read: protocol verbatim (p. 84) + Table 10 decane values; our 14 overlapping SS/Abr values: 10 exact at 4 dp, 4 within 1 unit of 4th dp | fgd_published_control.csv; [N2]; control sentence added to §sec:ss |
| 3 | thm:logconvex did not state exactly when ∂²_γ log LO = 0 | PRECISION | Added: Var_θ(q)=0 iff q constant over edges — includes (Δ,δ)-biregular graphs (nonzero constant imbalance, log LO affine and strictly increasing in γ) | statement re-derived; proof unchanged (criterion already implied) |
| 4 | prop:indep could be over-read as per-graph identifiability (GPT §3) | PRECISION | rem:ident added: weight-function independence ≠ per-graph identifiability; regular and degree-pair-poor graphs listed as exceptions | — |
| 5 | No generic-discrimination statement (GPT §7 asked for a careful one) | ADDITION | prop:generic: distinct count vectors separated for Lebesgue-a.e. θ; proof via z-injectivity (product+sum determine the pair) + linear independence of exponentials along a generic ray + real-analyticity | 151/151 distinct-profile octane pairs separated at sampled θ |
| 6 | Provenance incomplete (10-value spot check only) | LARGEST OPEN ITEM | Full 90-value trace (two agent campaigns); counts 6/63/13/7/1; §4.1 rewritten with the complete accounting incl. the tetramethylbutane sublimation and ω cases | octane_property_provenance_v35.csv; [N2] schema+count check; provenance doc |
| 7 | SMILES parser unaudited as a parser (GPT §16) | LOW | All 18 structures: 8 C / 7 edges / connected / tree / Δ≤4; 18/18 pairwise non-isomorphic (WL); parser documented as alkane-only | verifier section [P], runs every time |
| 8 | Selftest op harness missing new REQUIRED artifacts (own bug, found by selftest) | TOOLING | make_pkg extended | 83/83 |

## Not changed (audited and confirmed)
Table 2 / tuning / best-fixed values; GM attribution remark; collision and
multi-order tables; redundancy numbers; all v26–v33 statistical scoping.
No previously reported number changed in v35; the ablation table itself is
unchanged (its interpretation is sharpened).

## Reviewer passes (A–F, per GPT §22) — summary
A prior-art: novelty statement survives (scoped, search-documented).
B graph theory: boundary cases added (Δ≤2, regular, biregular, degree-pair-
poor graphs); no counterexample found to any stated result.
C statistics: leakage none found; unfairness addressed by robustness grid;
verdict weakened accordingly (the honest direction).
D chemical data: 90/90 traced; phases explicit; 2 marginal ω discrepancies +
1 sublimation case declared; no name/structure errors found.
E reproducibility: 83-attack selftest; all corruptions rejected.
F skeptical referee ("what if LO doesn't beat GM?"): the paper's claim IS
that it mostly doesn't — the contribution is the independence/convexity/
ceiling mathematics, the discrimination behaviour, the faithful SS result,
and the honest negative; nothing depends on a predictive win.
