#!/usr/bin/env python3
"""Stability of the refit-subsampling intervals of sensitivity_followup.py (v40.30 audit).

Reruns the identical subsampling (same seed, same 200 subsets of 80% without replacement, whole nested
pipeline refitted, leave-one-out evaluation inside each subset), saves every replicate's difference
ridge - comparator, and reports for each comparator:
  - median and 2.5/97.5% quantiles from replicates 1-100, 101-200 and all 200;
  - a distribution-free 95% interval for the 2.5% and 97.5% quantiles themselves (binomial order statistics),
    which shows how precisely 200 replicates locate those tails;
  - the number of replicates with ridge ahead.
The all-200 quantiles must equal those printed by sensitivity_followup.py.
  python3 audit/v4030/refit_stability.py   -> refit_stability_out.txt, refit_subsample_raw.csv
"""
import csv, os, subprocess, sys
import numpy as np
from scipy.stats import binom
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, ROOT, os.path.join(ROOT, "external"), os.path.join(ROOT, "external", "bp")]
import importlib.util
spec = importlib.util.spec_from_file_location("fu", os.path.join(HERE, "sensitivity_followup.py"))
src = open(os.path.join(HERE, "sensitivity_followup.py")).read()
src = src[:src.index("# ---------------------------------------------------------------- 1. composition")]   # definitions only
fu = {"__file__": os.path.join(HERE, "sensitivity_followup.py"), "__name__": "fu"}; exec(compile(src, "sensitivity_followup_defs", "exec"), fu)
predict, q2, rows, y, tb, STRICT = fu["predict"], fu["q2"], fu["rows"], fu["y"], fu["tb"], fu["STRICT"]
_g = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()
STAMP = f"commit {_g('rev-parse', 'HEAD')}; modified tracked files: {len([l for l in _g('status', '--porcelain', '--untracked-files=no').splitlines() if l])}"
print(STAMP)  # freeze stamp: printed, not written, so the output file can be replayed on any commit
out = []
def oci(p, n=200, level=0.95):
    """Distribution-free interval (order statistics, 1-based) for the p-quantile from n draws."""
    lo = int(binom.ppf((1 - level) / 2, n, p)); hi = int(binom.ppf(1 - (1 - level) / 2, n, p)) + 1
    return max(lo, 1), min(hi, n)
raw = []
for tst, base, pooled in (("A decanes", [i for i in range(len(rows)) if rows[i]["n_C"] == "10"], False),
                          ("B pooled", list(range(len(rows))), True)):
    for sc in ("original", "strict"):
        idx0 = base if sc == "original" else [i for i in base if tb[i] in STRICT]
        m_sub = int(round(0.8 * len(idx0))); srng = np.random.default_rng(20261014); diffs = {}
        for r in range(200):
            idx = sorted(srng.choice(idx0, m_sub, replace=False)); assert len(set(idx)) == m_sub
            pr = predict(idx, pooled); yy = y[idx]
            for m in pr:
                if m != "ridge":
                    d = q2(pr["ridge"], yy) - q2(pr[m], yy); diffs.setdefault(m, []).append(d); raw.append([tst, sc, m, r, f"{d:+.6f}"])
        for m, d in diffs.items():
            d = np.array(d); s = np.sort(d)
            (a1, b1), (a2, b2) = oci(0.025), oci(0.975)
            q = lambda v: f"[{np.percentile(v, 2.5):+.3f}, {np.percentile(v, 97.5):+.3f}] med {np.median(v):+.3f}"
            out.append(f"{tst:9} {sc:8} vs {m:15}: 1-100 {q(d[:100])}; 101-200 {q(d[100:])}; all {q(d)}; "
                       f"95% range of the 2.5% quantile [{s[a1 - 1]:+.3f}, {s[b1 - 1]:+.3f}], of the 97.5% quantile "
                       f"[{s[a2 - 1]:+.3f}, {s[b2 - 1]:+.3f}]; ridge ahead {(d > 0).sum()}/200")
            print(out[-1], flush=True)
with open(os.path.join(HERE, "refit_subsample_raw.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["test", "scenario", "comparator", "replicate", "ridge_minus_comparator"]); w.writerows(raw)
print("end: " + STAMP)
open(os.path.join(HERE, "refit_stability_out.txt"), "w").write("\n".join(out) + "\n")
