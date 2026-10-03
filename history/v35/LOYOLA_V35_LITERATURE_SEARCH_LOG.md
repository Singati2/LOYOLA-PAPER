# LOYOLA_V33_LITERATURE_SEARCH_LOG — round-12 multi-agent campaign

Five parallel literature agents (deep-research workflow), each on primary
sources where obtainable; all verdicts re-checked in the main loop before any
manuscript change.

## A. Gutman–Milovanović definition (primary PDF read)
Molina, Rodríguez-García, Sigarreta, Torralbas Fitz, "On the
Gutman-Milovanović index and chemical applications," AIMS Mathematics
10(2):1998–2020 (2025), doi 10.3934/math.2025094. Verbatim: "If α, β are
arbitrary real numbers, the Gutman-Milovanović index is defined in [16] by
M_{α,β}(G) = ∑_{uv∈E(G)} (d_u d_v)^α (d_u + d_v)^β." — α on the product, β
on the sum, exactly our LO(·;α,β,0). Ref [16] = Gutman, E. Milovanović,
I. Milovanović, AKCE Int. J. Graphs Comb. 17 (2020) 74–85 ("the definition
in [16] is slightly different, but it is equivalent to this one").
Special-case catalogue quoted and matched to ours. QSPR: 6 properties × 22
PAHs, grid-optimized (α,β), R² 0.9406–0.9983.

## B. GM bounds overlap (theorem triage)
HIGH overlap at γ=0 for all our bound types except path/star tree
orderings: Δ/δ/m bounds + regular/biregular equality (Molina Thm 2.4,
Prop 2.1/2.6, Cor 2.8–2.11), Jensen/Hölder/Young/Radon (Granados JMC 2025
Thms 3/4/6; Molina Thms 3.3/3.6), Pólya–Szegő/Cauchy–Schwarz products
(Molina Thm 3.2), sandwich vs R/χ/H/M1/M2/GA/AG/ISI (Molina Cor 2.8–2.11),
independence-number extremal joins (Rao Li, Utilitas Math 125:83–91, 2025).
→ Remark rem:gmattr added; γ=0 specializations attributed, not claimed.

## C. γ-novelty adversarial search (kill-check)
No killing paper: no published index multiplies a degree-product/sum family
by an exponential of normalized degree imbalance; no multi-parameter linear
combination inside exponential-VDB weights found (Rada MATCH 82 2019 general
framework; Sigarreta MBE 2022 / Carballosa JMC 2023 single-generator
parametric exponentials; no "exponential Albertson"; Adriatic descriptors
difference-type only). Mandatory framing adopted: special case of Rada's
class; tree-extremal machinery attributed to Gao–Gao AMC 472 (2024) 128634
and Hu–Li–Li–Peng MATCH 88 (2022) 505–520; no extremal-ordering claims.
Residual risk declared: MATCH archives not read page-by-page; Kulli-style
low-visibility journals not fully excludable; mid-2026 preprints unindexed.

## D. Structure-sensitivity methodology
Furtula–Gutman–Dehmer, Appl. Math. Comput. 219 (2013) 8973–8978 (Crossref
verified; Elsevier full text paywalled — definitions taken from two citing
papers, one Gutman-coauthored, that state they follow the 2013 method):
similar-structure sets S(G) at graph edit distance 2 within the isomer
class; SS = mean, Abr = max of relative index differences; class-level
averages; desideratum SS large / Abr small; Abr ≥ SS. Variants: Rakić–
Furtula J. Chemometrics 33 (2019) e3138 (fingerprint similarity);
Redžepović–Furtula (2020/21) eigenvalue descriptors. Verdict: our σ/μ and
(max−min)/μ were NOT the published quantities → faithful GED-2
implementation added (fgd_structure_sensitivity.py); proxy renamed and
retired from the text.

## E. Provenance spot-check
See LOYOLA_V33_DATA_PROVENANCE.md (9/10 match; isooctane ω flagged).

## Verified-by-my-own-read this round (main loop)
AIMS 2025 GM paper (local PDF, definition + special cases + attribution);
Gao–Gao AMC 2024 authors/title (publisher listing); Hu et al. MATCH 88
authors/title; Portilla et al. JMC 2025 authors/volume/pages (publisher).
Carried forward from earlier rounds: Rada 2019 Theorem 3.4 verbatim;
Randić 1991; Sigarreta 2022.

## v34 note (round 13)
New primary read: Barman & Das, MATCH Commun. Math. Comput. Chem. 95 (2026)
63-94 (open access) — FGD protocol stated verbatim (p. 84, following Furtula-
Gutman-Dehmer 2013 [11]); Table 10 decane SS/Abr values used as the published
control for our implementation (14 overlapping values: 10 exact at 4 dp, 4
within one unit). No other new searches; the v33 novelty search (dated
2026-08-30) remains current.

## v35 note (round 14)
No new literature work required: all round-14 repairs are statistical-honesty,
provenance-taxonomy, tooling, or boundary-case corrections grounded in already-
read sources.
