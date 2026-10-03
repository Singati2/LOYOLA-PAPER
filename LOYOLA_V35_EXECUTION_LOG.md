# LOYOLA_V35_EXECUTION_LOG — round-14 (v34 → v35)

## Environment
Python 3.13.0 · NumPy 2.4.4 · SciPy 1.17.1 · networkx 3.6.1 · matplotlib
3.10.8 · Darwin 24.6.0 · no TeX engine. Pins: requirements-lock.txt.

## Reproductions (BEFORE any edit)
| GPT claim | Reproduced? |
|---|---|
| seed 2 / budget 200 / dHvap: Q2_GM=0.8707455, Q2_LO=0.8611587, dQ2=-0.0095868 | YES — identical to all 7 decimals |
| 100-seed counts: dHvap 91/100 (b200), 93/100 (b500) better; dHf 86/100, 76/100 worse | YES — identical counts |
| omega substitution: M2 -0.987602 -> -0.985664 (displayed -0.988 -> -0.986) | YES — identical to 6 decimals; 8/12 correlations shift at 3rd decimal; winner unchanged |
| isooctane & 3-ethylhexane omega rows labeled VERIFIED EXACT despite 0.002/0.001 gaps | YES — confirmed in v34 CSV; 32 rows total reclassified under strict rules (all downgrades) |
| prop:indep Delta=1 rank = 1, not 3 | YES — single augmented vector (1,0,ln2,0) |
| Proxy figure still generated/labeled as structure sensitivity | YES — removed |
| Duplicated fragment after Barman–Das bibitem | NOT REPRODUCED in this copy (duplicate-line scan clean) — reported, no edit made |
| "82 self-tests" stale count | YES (v33→v34 changelog) — corrected (now 87) |

## Executions and exit codes
| Command | Result | Exit |
|---|---|---|
| expanded_robustness_v35.py (1000 nested configs + paired control) | CSV + summary written; counts above | 0 |
| omega sensitivity recompute | omega_source_sensitivity_v35.csv | 0 |
| provenance value-aware reclassification (all 90 rows) | 3/34/32/13/7/1; no upgrades | 0 |
| clean-room generator run (empty dir) | 2 manuscript PDFs + 3 CSVs, CSVs byte-identical | 0 |
| verify_loyola_v35.py (positive control) | TOTAL failures: 0, FULL PASS | 0 |
| verify_loyola_v35.py --selftest | 87 tests (50 tex, 29 csv, 6 op, 2 positive): ALL REJECTED FOR THE INTENDED REASON | 0 |
| static integrity | 39/39 refs; 0 orphans/undefined/unresolved; envs balanced; 0 stale "robust/exactly one/consistently" phrases; 0 proxy references | — |
| bundle acceptance (second clean extraction) | recorded at packaging | 0 |

## What FAILED to reproduce
Only the Barman–Das duplicated-fragment claim (see table); everything else
reproduced exactly.

## Production pass (round 15 sign-off, 2026-08-31)
TeX engine obtained (Tectonic 0.17.0/XeTeX): manuscript COMPILES, exit 0 — the
15-round CANNOT VERIFY is CLOSED. Production fixes (no scientific content
changed; drift guard + 87-test selftest re-pass): baselineskip 10px->10pt
(XeTeX portability); 16 raw accented chars -> accent macros (glyphs were
dropped by XeTeX fonts); 5 overfull displays fixed (113/72/42/28/13 pt:
abstract equation split, SS/Abr display stacked, Thm-7 proof multline,
Prop-13 specialisation displayed, degeneracy-convention spacing); remaining
overfulls 11.4/8.2/2.1/1.2 pt (<=4 mm, immaterial). Visual inspection: all 36
pages read — 8 tables in-margin, 2 figures clean, references complete with
correct diacritics. Compiled PDF bundled as LOYOLA_v35_compiled.pdf.
