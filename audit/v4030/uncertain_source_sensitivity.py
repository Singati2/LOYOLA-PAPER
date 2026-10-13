#!/usr/bin/env python3
"""Source-quality sensitivity of the reported comparisons (v40.30 audit; exploratory, not pre-registered).

SCENARIOS (tiers from audit/final/scripts/claim_provenance_ledger.csv)
  original : every value (the registered analysis).
  broad    : tiers A, B, A-AGG, B?. A-AGG is a NIST/TRC average whose constituent determinations are
             not audited, so it does NOT establish independent groups; B? is a single NIST value whose
             primary reference is not recorded, so it is NOT a verified primary determination.
  strict   : tiers A and B only (two or more research groups, or one identified primary study).

ESTIMABILITY (fixed before the restricted results were read; every n is printed so another rule can
be applied): a correlation ranking needs n >= 10, a non-constant property and non-constant
descriptors (below 10 molecules a leader chosen among 12 candidates is not interpretable). A
leave-one-out regression needs n >= 10 and a centred count matrix of rank >= 2; the size-adjusted
pooled models also need a non-constant n_C. Otherwise the analysis is reported NOT ESTIMABLE and no
statistic is quoted.

COMPARISONS
  matched : the original full-data leave-one-out predictions evaluated on the retained molecules only
            (no refit) next to the refit on the retained molecules.
  paired bootstrap : 2000 resamples of molecules (seed 20261013); both models are evaluated on the same
            resample, so the interval is for their difference. Fold predictions are held fixed, so the
            interval is conditional on the fitted models (it does not refit).
  READING : an interval that excludes 0 supports a difference in that direction; one that includes 0
            means the difference is NOT RESOLVED by these data. Neither establishes equivalence, which
            would need a pre-specified margin.
MACHINE-READABLE OUTPUT (next to this script)
  sensitivity_filters.csv   per dataset and property: values per tier, retained per scenario, missing provenance
  sensitivity_octane.csv    per property and scenario: n, excluded identifiers, estimable, |r| of the original
                            leader and runner-up, difference, 95% CI, reading, subset leader
  sensitivity_bp.csv        per test and scenario: n, excluded identifiers, estimable, count rank, full-data Q2,
                            matched (original predictions on retained molecules), refit Q2, difference, 95% CI
The commit and the number of modified tracked files are stamped at the start of the text output.
  python3 audit/v4030/uncertain_source_sensitivity.py   -> uncertain_source_sensitivity_out.txt and the CSVs
"""
import subprocess
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [ROOT, os.path.join(ROOT, "external"), os.path.join(ROOT, "external", "bp")]
from octane_data import OCTANES, NAMES, PROPS, alkane_pairs, lo_pairs
import baselines as BL
import bp_tests as T

MIN_N, NBOOT = 10, 2000
tier = {(r["dataset"], r["molecule"], r["property"]): r["tier"]
        for r in csv.DictReader(open(os.path.join(ROOT, "audit", "final", "scripts", "claim_provenance_ledger.csv")))}
SCEN = [("original", None), ("broad", {"A", "B", "A-AGG", "B?"}), ("strict", {"A", "B"})]
OUT = []
def say(s): print(s, flush=True); OUT.append(s)
def ci(v): return f"[{np.percentile(v, 2.5):+.3f}, {np.percentile(v, 97.5):+.3f}]"
def reading(v):
    lo, hi = np.percentile(v, 2.5), np.percentile(v, 97.5)
    return "difference supported" if lo > 0 or hi < 0 else "NOT RESOLVED (interval includes 0; not equivalence)"
def q2(p, y): return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()
rng = np.random.default_rng(20261013)
_g = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()
say(f"commit {_g('rev-parse', 'HEAD') or 'unknown'}; modified tracked files: {len([l for l in _g('status', '--porcelain', '--untracked-files=no').splitlines() if l])}")
OCT_ROWS, BP_ROWS, FILT_ROWS = [], [], []
def write(fn, header, rows):
    with open(os.path.join(HERE, fn), "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
# filter verification against the ledger: every molecule must have a tier
for ds, props, names in (("octane", PROPS, NAMES), ("bp", ["T_B"], None), ("nonane", ["T_B", "dHvap"], None)):
    for prop in props:
        led_rows = [(m, t) for (d, m, pr), t in tier.items() if d == ds and pr == prop]
        missing = [nm for nm in (names or []) if (ds, nm, prop) not in tier]
        cnt = {t: sum(1 for _, x in led_rows if x == t) for t in ("A", "A-AGG", "B", "B?", "C", "D")}
        FILT_ROWS.append([ds, prop, len(led_rows), *cnt.values(), sum(cnt[t] for t in ("A", "B", "A-AGG", "B?")),
                          cnt["A"] + cnt["B"], len(missing)])
write("sensitivity_filters.csv", ["dataset", "property", "n_ledger", "A", "A-AGG", "B", "B?", "C", "D", "retained_broad",
                                  "retained_strict", "missing_provenance"], FILT_ROWS)

# ---------------------------------------------------------------- octane correlations (Table 4)
IDX = {"M1": (0, 1, 0), "M2": (1, 0, 0), "HM": (0, 2, 0), "mM2": (-1, 0, 0), "R": (-0.5, 0, 0), "chi": (0, -0.5, 0),
       "H/2": (0, -1, 0), "ISI": (1, -1, 0), "GA": (0.5, -1, 0), "AG": (-0.5, 1, 0), "LO(0,0,1)": (0, 0, 1), "LO(0,0,2)": (0, 0, 2)}
P = [alkane_pairs(r[0]) for r in OCTANES]
X = {k: np.array([lo_pairs(p, *t) for p in P]) for k, t in IDX.items()}
say("OCTANE TABLE 4: the original column leader and runner-up, |r| on each subset, paired bootstrap of |r|(leader) - |r|(runner-up)")
for k, prop in enumerate(PROPS):
    y = np.array([r[1 + k] for r in OCTANES]); t = [tier.get(("octane", nm, prop), "?") for nm in NAMES]
    r0 = {i: abs(np.corrcoef(X[i], y)[0, 1]) for i in IDX}; lead, run = sorted(r0, key=r0.get, reverse=True)[:2]
    for sc, allowed in SCEN:
        keep = np.array([allowed is None or x in allowed for x in t]); n = int(keep.sum())
        excl = [nm for nm, kp in zip(NAMES, keep) if not kp]
        ok = n >= MIN_N and np.ptp(y[keep]) > 0 and all(np.ptp(X[i][keep]) > 0 for i in IDX)
        head = f"  {prop:6} {sc:8} n={n:2} excluded={18 - n:2}"
        if not ok:
            say(f"{head}: NOT ESTIMABLE"); OCT_ROWS.append([prop, sc, n, ";".join(excl), "no", lead, run, "", "", "", "", "", "", ""]); continue
        r = {i: abs(np.corrcoef(X[i][keep], y[keep])[0, 1]) for i in IDX}
        lead_s = max(r, key=r.get)
        idx = np.flatnonzero(keep); d = []
        for _ in range(NBOOT):
            b = rng.choice(idx, len(idx))
            if np.ptp(y[b]) == 0 or np.ptp(X[lead][b]) == 0 or np.ptp(X[run][b]) == 0: continue
            d.append(abs(np.corrcoef(X[lead][b], y[b])[0, 1]) - abs(np.corrcoef(X[run][b], y[b])[0, 1]))
        say(f"{head}: {lead} {r[lead]:.3f} vs {run} {r[run]:.3f}, difference {r[lead] - r[run]:+.3f}, 95% CI {ci(d)}; "
            f"{reading(d)}; subset leader {lead_s}" + (f"; excluded: {', '.join(excl)}" if 0 < len(excl) <= 8 else ""))
        OCT_ROWS.append([prop, sc, n, ";".join(excl), "yes", lead, run, f"{r[lead]:.4f}", f"{r[run]:.4f}", f"{r[lead] - r[run]:+.4f}",
                         f"{np.percentile(d, 2.5):+.4f}", f"{np.percentile(d, 97.5):+.4f}", reading(d), lead_s])

# ---------------------------------------------------------------- boiling points
rows, Pall, y, z = T.load()
tb = np.array([tier.get(("bp", r["name"], "T_B"), "?") for r in rows])
def preds(idx, pooled):
    Pk, yk = [Pall[i] for i in idx], y[idx]
    F = np.array([BL.count_vector(p) for p in Pk], float)
    out = {"ridge": BL.outer_loo(BL.fold_ridge, F, yk)[0]}
    ir = np.array([BL.irla(p) for p in Pk])[None, :]; lo1 = BL.descriptor_matrix(Pk, [(0, 0, 1)]); Xc = BL.descriptor_matrix(Pk, T.CLASSICAL)
    if pooled:
        zk = z[idx]
        out.update({"size only": T.size_only(zk, yk), "size+classical": T.nested_size(Xc, zk, yk),
                    "size+IRLA": T.nested_size(ir, zk, yk), "size+LO(0,0,1)": T.nested_size(lo1, zk, yk)})
    else:
        out.update({"classical": BL.outer_loo(BL.fold_select_ols, Xc, yk)[0], "IRLA": BL.outer_loo(BL.fold_select_ols, ir, yk)[0],
                    "LO(0,0,1)": BL.outer_loo(BL.fold_select_ols, lo1, yk)[0]})
    return out, F
say("BOILING POINTS: leave-one-out Q2; ridge on degree-pair counts minus the best single-index model, paired bootstrap")
for tst, base_idx, pooled in (("A decanes", [i for i in range(len(rows)) if rows[i]["n_C"] == "10"], False),
                              ("B pooled ", list(range(len(rows))), True)):
    full, _ = preds(base_idx, pooled); yfull = y[base_idx]
    singles = [m for m in full if m not in ("ridge", "size only")]
    for sc, allowed in SCEN:
        pos = [j for j, i in enumerate(base_idx) if allowed is None or tb[i] in allowed]
        idx = [base_idx[j] for j in pos]; n = len(idx)
        head = f"  {tst} {sc:8} n={n:3} excluded={len(base_idx) - n:2}"
        excl = ";".join(rows[base_idx[j]]["name"] for j in range(len(base_idx)) if j not in set(pos))
        if n < MIN_N:
            say(f"{head}: NOT ESTIMABLE"); BP_ROWS.append([tst.strip(), sc, n, excl, "no"] + [""] * 10); continue
        pr, F = preds(idx, pooled); yk = y[idx]
        rank = int(np.linalg.matrix_rank(F - F.mean(0)))
        if rank < 2 or (pooled and np.ptp(z[idx]) == 0):
            say(f"{head}: NOT ESTIMABLE (count rank {rank})"); continue
        q = {m: q2(p, yk) for m, p in pr.items()}; best = max(singles, key=q.get)
        matched = {m: q2(full[m][pos], yk) for m in ("ridge", best)}
        d = []
        for _ in range(NBOOT):
            b = rng.integers(0, n, n)
            if np.ptp(yk[b]) == 0: continue
            d.append(q2(pr["ridge"][b], yk[b]) - q2(pr[best][b], yk[b]))
        say(f"{head} (count rank {rank}): refit ridge {q['ridge']:.3f}, best single {best} {q[best]:.3f}, difference "
            f"{q['ridge'] - q[best]:+.3f}, 95% CI {ci(d)}, {reading(d)}; matched original fit on these molecules: ridge "
            f"{matched['ridge']:.3f}, {best} {matched[best]:.3f}; all: " + ", ".join(f"{m} {v:.3f}" for m, v in q.items()))
        fullq = {m: q2(full[m], yfull) for m in ("ridge", best)}
        BP_ROWS.append([tst.strip(), sc, n, excl, "yes", rank, best, f"{fullq['ridge']:.4f}", f"{fullq[best]:.4f}", f"{matched['ridge']:.4f}",
                        f"{matched[best]:.4f}", f"{q['ridge']:.4f}", f"{q[best]:.4f}",
                        f"{q['ridge'] - q[best]:+.4f} [{np.percentile(d, 2.5):+.4f}, {np.percentile(d, 97.5):+.4f}]", reading(d)])
say("NOT RUN: the registered gamma test (GM vs LO over 50 seeds) on the restricted subsets (about one hour each; not pre-registered).")
say("NOT ESTIMABLE by construction: nonane dHvap strict (n = 4); octane S strict and broad (n = 2, 5); octane omega (n = 0); octane T_B strict (n = 0).")
write("sensitivity_octane.csv", ["property", "scenario", "n", "excluded", "estimable", "original_leader", "original_runner_up",
                                 "abs_r_leader", "abs_r_runner_up", "difference", "ci95_lo", "ci95_hi", "reading", "subset_leader"], OCT_ROWS)
write("sensitivity_bp.csv", ["test", "scenario", "n", "excluded", "estimable", "count_rank", "best_single", "full_Q2_ridge",
                             "full_Q2_best_single", "matched_Q2_ridge", "matched_Q2_best_single", "refit_Q2_ridge",
                             "refit_Q2_best_single", "refit_difference_ci95", "reading"], BP_ROWS)
say(f"end: commit {_g('rev-parse', 'HEAD') or 'unknown'}; modified tracked files: {len([l for l in _g('status', '--porcelain', '--untracked-files=no').splitlines() if l])}")
open(os.path.join(HERE, "uncertain_source_sensitivity_out.txt"), "w").write("\n".join(OUT) + "\n")
