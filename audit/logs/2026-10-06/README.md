# Audit validation logs

`*-original.log` refers to v40.8 snapshot ab9e1df. The original core and external checks pass; its selftest fails four provenance-mutation harness cases. Other logs record the subsequent fixes and independent checks described in the comprehensive audit.

`high-precision.log` records a fresh run of structural/hp_counts.py. `structural-auxiliary.log` runs S2, S4, S5, S6 and S7, without repeating the expensive original floating-point S3 search. The crossing logs check the reported witness directly; interval-checks.log comes from audit/check_mathematics.py. The full original S3 search is not claimed. The original formal log records a successful fresh build followed by the locale-dependent name comparison failure; the fixed formal log records all 36 reports passing after that script fix. The optional process-path adapter is documented in audit/runtime.

The fixed selftest exercises all 113 cases. The fixed regression log covers ten focused tests. The auxiliary-output log rebuilds fractional-point, chi-floor and calorimetric availability outputs in an isolated copy. These logs are evidence for the stated checks, not authentication of every experimental source value or formal verification of all manuscript mathematics.

The final pooled-results log checks all 50 seeds, the bootstrap summary and all pooled baselines against published outputs. The existing full-design candidate eligibility filter is retained; only deletion-induced rank loss among otherwise eligible candidates uses explicit refitting. The decane one-predictor code path is unchanged and passed the original full external reproduction.
