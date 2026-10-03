# LOYOLA_v35 — round-14 GPT-audit repairs (statistical honesty + provenance taxonomy)

Authoritative manuscript: `main.tex`. v35 repairs the five defects of GPT's
round-14 independent audit of v34 — every one REPRODUCED before repair:

1. **Robustness conclusion corrected**: GPT's seed-2 counterexample
   (ΔH_vap Q²_GM 0.8707455 vs Q²_LO 0.8611587) reproduced to 7 decimals;
   expanded to seeds 0–99 × budgets {200,500} (+ paired same-(α,β) control):
   ΔH_vap better in 91–93/100 seeds, ΔH_f worse in 76–86/100, neither
   sign-invariant. Manuscript now uses descriptive-tendency language only.
2. **ω-sensitivity statement corrected** (v34's was false): substituting the
   compiled acentric factors moves 8/12 ω correlations at the 3rd decimal
   (M₂: −0.988 → −0.986); winner unchanged (omega_source_sensitivity_v35.csv).
3. **Provenance reclassified** under a strict taxonomy (EXACT = exact at
   reported precision): 3 / 34 / 32 / 13 / 7 / 1
   (exact / unit-conv / within-tolerance / variation / cannot-verify /
   conflict); the verifier now re-derives classes from row values.
4. **prop:indep boundary fixed**: Δ=1 rank is 1 (not 3); ranks 1/3/4 for
   Δ=1/2/≥3 now stated and machine-enforced.
5. **Retired σ/μ proxy figure removed** from figures/, generator, manifest;
   verifier rejects its reintroduction. FGD table + published control
   (10/14 exact, 4 within 1 unit of 4th decimal) unchanged.

## Verification
```bash
python3 -m pip install -r requirements-lock.txt
python3 verify_loyola_v35.py            # FULL PASS exit 0 (~3-4 min)
python3 verify_loyola_v35.py --selftest # 87 attacks, all rejected, exit 0 (~9 min)
python3 expanded_robustness_v35.py      # regenerates the 1000-row sweep (~3 min)
shasum -a 256 -c SHA256SUMS.txt
```

## Standing CANNOT VERIFY (unchanged)
Overleaf compile/rendered PDF; 6 NIST-absent gas entropies; the
tetramethylbutane sublimation case; paywalled AKCE 2020 / Portilla JMC full
texts; InChIKeys. **Gating steps: coauthor sign-off on the reframe, then the
author's Overleaf compile.**
