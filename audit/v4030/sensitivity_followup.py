#!/usr/bin/env python3
"""Follow-up to uncertain_source_sensitivity.py (v40.30 audit; exploratory, not pre-registered).

1. COHORT COMPOSITION of the strict boiling-point subsets against the excluded compounds: carbon
   number, boiling-point distribution and descriptor distributions.
2. DECOMPOSITION of the ridge advantage against each PREDEFINED comparator (no comparator is chosen
   on the evaluation data): full data -> matched (the original out-of-fold predictions on the
   retained compounds: the cohort-selection effect) -> refit on the retained compounds (the refitting
   effect).
     decanes: classical (the within-fold best of the classical indices, selected inside each fold),
              IRLA, LO(0,0,1)
     pooled:  size+classical, size+IRLA, size+LO(0,0,1) (each with n_C), and size only
   The claim tested is "ridge on degree-pair counts outperforms every single-index model".
3. UNCERTAINTY, two kinds, labelled by what they estimate:
   (a) fixed-prediction paired bootstrap over compounds (2000 resamples): uncertainty of the
       evaluation of these fitted predictions on this sample; Q2 denominator recomputed per replicate;
       simultaneous over the three single-index comparators (Bonferroni, 98.33% percentile intervals).
   (b) refit subsampling: 200 random subsets of 80% of the compounds without replacement, each with
       the whole nested pipeline refitted (penalty and within-fold selection included); the spread of
       the out-of-sample difference across subsets estimates the variability of the procedure under
       resampling of compounds. It is not a confidence interval for a population parameter.
  python3 audit/v4030/sensitivity_followup.py   -> sensitivity_followup_out.txt, sensitivity_decomposition.csv,
                                                   sensitivity_composition.csv
"""
import csv, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [ROOT, os.path.join(ROOT, "external"), os.path.join(ROOT, "external", "bp")]
import baselines as BL
import bp_tests as T

tier = {r["molecule"]: r["tier"] for r in csv.DictReader(open(os.path.join(ROOT, "audit", "final", "scripts", "claim_provenance_ledger.csv"))) if r["dataset"] == "bp"}
rows, Pall, y, z = T.load()
tb = np.array([tier[r["name"]] for r in rows]); STRICT = {"A", "B"}
OUT = []
def say(s): print(s, flush=True); OUT.append(s)
_g = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()
stamp = lambda: f"commit {_g('rev-parse', 'HEAD')}; modified tracked files: {len([l for l in _g('status', '--porcelain', '--untracked-files=no').splitlines() if l])}"
say(stamp())
def q2(p, yy): return 1 - ((yy - p) ** 2).sum() / ((yy - yy.mean()) ** 2).sum()

def predict(idx, pooled):
    Pk, yk = [Pall[i] for i in idx], y[idx]
    F = np.array([BL.count_vector(p) for p in Pk], float)
    ir = np.array([BL.irla(p) for p in Pk])[None, :]; lo1 = BL.descriptor_matrix(Pk, [(0, 0, 1)]); Xc = BL.descriptor_matrix(Pk, T.CLASSICAL)
    out = {"ridge": BL.outer_loo(BL.fold_ridge, F, yk)[0]}
    if pooled:
        zk = z[idx]
        out.update({"size+classical": T.nested_size(Xc, zk, yk), "size+IRLA": T.nested_size(ir, zk, yk),
                    "size+LO(0,0,1)": T.nested_size(lo1, zk, yk), "size only": T.size_only(zk, yk)})
    else:
        out.update({"classical": BL.outer_loo(BL.fold_select_ols, Xc, yk)[0], "IRLA": BL.outer_loo(BL.fold_select_ols, ir, yk)[0],
                    "LO(0,0,1)": BL.outer_loo(BL.fold_select_ols, lo1, yk)[0]})
    return out

# ---------------------------------------------------------------- 1. composition
COMP = []
say("1. COMPOSITION (strict = tiers A and B; excluded = NIST/TRC averages)")
for lab, mask in (("strict retained", np.isin(tb, list(STRICT))), ("excluded", ~np.isin(tb, list(STRICT))), ("all", np.ones(len(rows), bool))):
    idx = np.flatnonzero(mask); Pk = [Pall[i] for i in idx]
    irv = np.array([BL.irla(p) for p in Pk]); lov = BL.descriptor_matrix(Pk, [(0, 0, 1)])[0]
    ncs = {c: int((z[idx] == c).sum()) for c in range(6, 11)}
    say(f"  {lab:16} n={len(idx):3} n_C {ncs} | T_B mean {y[idx].mean():.1f} sd {y[idx].std():.1f} | IRLA mean {irv.mean():.2f} sd {irv.std():.2f} "
        f"| LO(0,0,1) mean {lov.mean():.2f} sd {lov.std():.2f}")
    COMP.append([lab, len(idx), *ncs.values(), f"{y[idx].mean():.2f}", f"{y[idx].std():.2f}", f"{irv.mean():.3f}", f"{irv.std():.3f}", f"{lov.mean():.3f}", f"{lov.std():.3f}"])
for c in (9, 10):
    a = [y[i] for i in range(len(rows)) if z[i] == c and tb[i] in STRICT]; b = [y[i] for i in range(len(rows)) if z[i] == c and tb[i] not in STRICT]
    if a and b: say(f"  C{c}: T_B retained mean {np.mean(a):.1f} sd {np.std(a):.1f} (n={len(a)}) vs excluded {np.mean(b):.1f} sd {np.std(b):.1f} (n={len(b)})")
with open(os.path.join(HERE, "sensitivity_composition.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["group", "n", "nC6", "nC7", "nC8", "nC9", "nC10", "TB_mean", "TB_sd", "IRLA_mean", "IRLA_sd", "LO001_mean", "LO001_sd"]); w.writerows(COMP)

# ---------------------------------------------------------------- 2-3. decomposition and uncertainty
DEC = []; rng = np.random.default_rng(20261013)
say("2-3. DECOMPOSITION and UNCERTAINTY of ridge minus each predefined comparator")
for tst, base, pooled in (("A decanes", [i for i in range(len(rows)) if rows[i]["n_C"] == "10"], False),
                          ("B pooled", list(range(len(rows))), True)):
    full = predict(base, pooled); yb = y[base]
    comps = [m for m in full if m != "ridge"]; singles = [m for m in comps if m != "size only"]
    pos = [j for j, i in enumerate(base) if tb[i] in STRICT]; sidx = [base[j] for j in pos]; ys = y[sidx]
    refit = predict(sidx, pooled)
    for m in comps:
        f_d = q2(full["ridge"], yb) - q2(full[m], yb)
        m_d = q2(full["ridge"][pos], ys) - q2(full[m][pos], ys)
        r_d = q2(refit["ridge"], ys) - q2(refit[m], ys)
        bs = []
        for _ in range(2000):
            b = rng.integers(0, len(ys), len(ys))
            if np.ptp(ys[b]) == 0: continue
            bs.append(q2(refit["ridge"][b], ys[b]) - q2(refit[m][b], ys[b]))
        lvl = 100 * (1 - 0.05 / len(singles)) if m in singles else 95.0
        lo, hi = np.percentile(bs, [(100 - lvl) / 2, 100 - (100 - lvl) / 2])
        DEC.append([tst, m, len(base), len(sidx), f"{f_d:+.4f}", f"{m_d:+.4f}", f"{r_d:+.4f}", f"{m_d - f_d:+.4f}", f"{r_d - m_d:+.4f}",
                    f"{lvl:.2f}", f"{lo:+.4f}", f"{hi:+.4f}"])
        say(f"  {tst:9} vs {m:15}: full {f_d:+.3f} (n={len(base)}) -> matched {m_d:+.3f} -> refit {r_d:+.3f} (n={len(sidx)}); "
            f"cohort effect {m_d - f_d:+.3f}, refit effect {r_d - m_d:+.3f}; fixed-prediction {lvl:.2f}% interval [{lo:+.3f}, {hi:+.3f}]")
say(stamp())
# refit subsampling
SUB = []
say("3b. REFIT SUBSAMPLING (200 subsets of 80% without replacement, whole nested pipeline refitted)")
for tst, base, pooled in (("A decanes", [i for i in range(len(rows)) if rows[i]["n_C"] == "10"], False),
                          ("B pooled", list(range(len(rows))), True)):
    for sc in ("original", "strict"):
        idx0 = base if sc == "original" else [i for i in base if tb[i] in STRICT]
        m_sub = int(round(0.8 * len(idx0))); diffs = {}
        srng = np.random.default_rng(20261014)
        for r in range(200):
            idx = sorted(srng.choice(idx0, m_sub, replace=False)); pr = predict(idx, pooled); yy = y[idx]
            for m in pr:
                if m != "ridge": diffs.setdefault(m, []).append(q2(pr["ridge"], yy) - q2(pr[m], yy))
        for m, d in diffs.items():
            d = np.array(d)
            SUB.append([tst, sc, m, len(idx0), m_sub, f"{np.median(d):+.4f}", f"{np.percentile(d, 2.5):+.4f}", f"{np.percentile(d, 97.5):+.4f}", int((d > 0).sum())])
            say(f"  {tst:9} {sc:8} vs {m:15}: n={len(idx0)} subsets of {m_sub}: median {np.median(d):+.3f}, 2.5-97.5% "
                f"[{np.percentile(d, 2.5):+.3f}, {np.percentile(d, 97.5):+.3f}], ridge ahead in {(d > 0).sum()}/200")
with open(os.path.join(HERE, "sensitivity_decomposition.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["test", "comparator", "n_full", "n_strict", "diff_full", "diff_matched", "diff_refit", "cohort_effect", "refit_effect",
                "fixed_pred_interval_level", "fixed_pred_lo", "fixed_pred_hi"]); w.writerows(DEC)
    w.writerow([]); w.writerow(["test", "scenario", "comparator", "n", "subset_size", "subsample_median", "subsample_p2.5", "subsample_p97.5", "ridge_ahead_of_200"]); w.writerows(SUB)
say(stamp())
open(os.path.join(HERE, "sensitivity_followup_out.txt"), "w").write("\n".join(OUT) + "\n")
