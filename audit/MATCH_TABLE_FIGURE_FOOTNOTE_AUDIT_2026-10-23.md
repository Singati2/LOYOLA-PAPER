# Table, figure and footnote audit, 2026-10-23

- **Audited:** `e25d790` (main 35 pp, supplement 39 pp), read only.
- **Rendered pages:** PNG pages were inspected for every table and figure.
- **Re-checked:** the pages changed on the audit branch were re-rendered (main 37 pp).
- **Page numbers below:** those of `e25d790`. Audit-branch pages are given where they differ.

## Inventory

| ID | Page (e25d790 → branch) | Content | Source of numbers | Cited in |
|---|---|---|---|---|
| Table 1 `tab:collisions` | 16 | The 2 octane collision pairs; units in the caption | `DATA/octane_properties.csv`, `bid_collision_table.csv` | main §3.1, §6.1 |
| Table 2 `tab:firstfail` | 18 | First order at which discrimination is lost; footnotes a–d | `structural/structural_checks_out.txt`, `exact_ties_out.txt` | main §3.2 |
| Figure 1 `fig:degeneracy` | 19 → 18 | Degeneracy of 12 indices on the 106 trees of order 10 | `lo_sensitivity_degeneracy_order10_trees.csv`, `generate_loyola_v35_figures.py` | main §3.2; supplement S5 |
| Table 3 `tab:fgdss` | 20 | SS, Abr and SS/Abr on the 75 decanes | `fgd_structure_sensitivity_decanes.csv` | main §3.3; S6 |
| Table 4 `tab:lo_octane` | 24 | Pearson r, 12 indices × 5 properties | `lo_sensitivity_prediction_correlations.csv` | main §6.1; the supplement 12 times |
| Table 5 `tab:bp` | 27 → 29 | Boiling-point Tests A and B | `external/bp/bp_baselines.csv`, `bp_results_summary.csv` | main §6.4; S11 |
| Fig. S1 `fig:octanes` | S p. 5 | Heatmap of Table 4 | as Table 4 | S1 |
| Tables S1–S7 | S pp. 7–26 | Tuning, best fixed index, ablation, multi-order, octane data, box, within-fold baselines | `verify_loyola_v35_results.csv` §E/F, `ablation_summary.csv`, `expanded_robustness_summary_v35.csv`, `multi_order_degeneracy.csv`, `DATA/octane_properties.csv`, `external/box_sensitivity_summary.csv`, `external/make_v37_table.py` | main and supplement |
| Table S8 `tab:deviations` | S p. 37 | Post-outcome protocol changes (was main Table 6) | text | main limitation (iv); S11 |

## Checks

| Check | Result |
|---|---|
| Table 1 values (20) and the 1.2 and 2.1 °C gaps | VERIFIED |
| Table 2, all entries (orders 13–17), against structural outputs; also re-derived independently by the mathematics review | VERIFIED |
| Table 2 footnotes a–d: attached, all used, none lost against the 46-page version | VERIFIED |
| Table 3 (36 values) and the ratios 0.4579, 0.4565 and 0.448–0.451 in the text | VERIFIED |
| Table 4 (60 cells, 5 bold), the "−0.000 = −0.0002" note, the 0.001–0.032 margins, 14 pairs with \|r\| ≥ 0.99, 99.05%, 0.982 and 0.993 | VERIFIED |
| Table 5 (18 cells), the intervals in the text, the narrow-box medians and the permutation summary | VERIFIED |
| Figure 1 bars: 83.0, 67.0, 37.7, 47.2, 25.5, 27.4, 34.0, 36.8, and 25.5 for GA, AG and both LO points; floor 25.5% = 79/106 | VERIFIED against the CSV and the text |
| Figure 1 file in `MATCH_OVERLEAF_CANDIDATE.zip` | same SHA-256 as `figures/` (`1a5adc67…`); no `\safefig` placeholder in any PDF |
| Fig. S1 (60 values = Table 4); Tables S3, S4, S5 (90 values), S6, S7 | VERIFIED. Table S2's 0.745 and 0.950 have no CSV; recomputed independently as 0.7455 and 0.9498 |
| Table S8: cells against the 46-page Table 6 | identical except three cross-references, now hard-coded main-paper numbers |
| Float environments, 46-page version against `e25d790` | byte-identical except S8 (cross-references) |
| Cross-references, both directions | all correct against `main.aux` and `supplement.aux`; no stale "Table 6"; Proposition 7 → 5 handled |
| S1–S11, Tables S1–S8 and Fig. S1 numbering | contiguous |
| Standalone builds of both files | PASS (0 undefined, 0 overfull) |

## Findings

**Fixed on the audit branch:**
- Table 5:
  - The caption said "nested" for ordinary-LOO columns. Now: "nested wherever an index, a point or a penalty is selected".
  - The column header "$>$" is now "wins".
  - The text cited Table 5 for intervals it does not show. Now: "results in Table 5 and below".
- Table S7 floated past the S10 heading. A `\FloatBarrier` was added; S7 is now on p. 25 and S10 starts on p. 26.
- Table S8 had wide word gaps and a hyphenated cross-reference. The columns are now ragged-right; re-rendered and checked.

**Proposed, not applied:**
- Table 2 sits alone on a float page with about 35% blank space. Use `[t]`, or move the certification sentences from the caption to the text.
- Abruptness of $LO(0,0,2)$ is "0.274" in the text and "0.2745" in Table 3. The value is 0.27447, so both are correct, but "0.2745 against 0.3126" would avoid a reader's rounding doubt. This needs a registry anchor change.
- Table S5 lacks units in its caption, and Table S6 relies on the text for "Edge", ">" and LO$_h$. Self-contained captions are preferred.
- Table 5 uses `\scriptsize` with `tabcolsep` 1.5pt. The cell labels of Fig. S1 are about 5 pt.
- Both figure PDFs embed Type 3 fonts. Re-export with `pdf.fonttype = 42` if production objects. This changes figure files, so it needs approval.
- Table S8 says "interval rule read as one-sided", while the main text says "lower end of the two-sided 95% interval exceeds zero". The substance agrees; aligning the wording is optional.
