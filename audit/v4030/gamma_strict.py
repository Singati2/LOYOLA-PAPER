#!/usr/bin/env python3
"""The registered gamma comparison (Tests A and B of PREREG_v40, external/bp/bp_tests.run_test: GM in
the wide box vs LO hybrid, 50 seeds, seed-bootstrap interval of the median difference) rerun on the
strict provenance subset (tiers A and B) of the boiling-point data (v40.30 audit; exploratory).
The broad subset equals the full data for the boiling points (every value is A, A-AGG or B), so its
result is the registered one. The strict pooled subset holds only C9 and C10 compounds (all C6-C8
values are NIST averages), so it does not test the registered C6-C10 population.
Sign convention (as in bp_tests.run_test): dQ2 = Q2(LO hybrid) - Q2(GM wide box), higher Q2 is better;
"LOh better" counts seeds with dQ2 > 0. The 50 raw per-seed Q2 values are saved and the summary is
recounted from them.
  python3 audit/v4030/gamma_strict.py   -> gamma_strict_out.txt, gamma_strict_seeds.csv (no registered file is written)
"""
import csv, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [ROOT, os.path.join(ROOT, "external"), os.path.join(ROOT, "external", "bp")]
import bp_tests as T
tier = {r["molecule"]: r["tier"] for r in csv.DictReader(open(os.path.join(ROOT, "audit", "final", "scripts", "claim_provenance_ledger.csv"))) if r["dataset"] == "bp"}
rows, P, y, z = T.load()
_g = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()
out = [f"commit {_g('rev-parse', 'HEAD')}; modified tracked files: {len([l for l in _g('status', '--porcelain', '--untracked-files=no').splitlines() if l])}"]
strict = [i for i, r in enumerate(rows) if tier[r["name"]] in ("A", "B")]
dec = [i for i in strict if rows[i]["n_C"] == "10"]
allseeds = []
for label, idx, zz in (("A: decane T_B, strict", dec, None), ("B: pooled T_B (size-adjusted), strict (C9-C10 only)", strict, z)):
    seeds, sm = T.run_test(label, [P[i] for i in idx], y[idx], None if zz is None else zz[idx]); allseeds += seeds
    d = np.array([float(r[5]) - float(r[4]) for r in seeds])   # Q2_LOh - Q2_GM12 from the raw rows
    assert len(d) == 50 and int((d > 0).sum()) == sm[7] and abs(np.median(d) - float(sm[6])) < 1e-9, "recount differs from summary"
    out.append(f"{label}: recount from 50 raw seed rows: median dQ2 {np.median(d):+.4f}, dQ2 > 0 in {(d > 0).sum()}/50, "
               f"min {d.min():+.4f}, max {d.max():+.4f}")
    out.append(f"{label}: n={sm[1]}, median Q2 GM12 {float(sm[4]):.4f}, LOh {float(sm[5]):.4f}, median dQ2 {float(sm[6]):+.4f}, "
               f"LOh better in {sm[7]}/50 seeds, seed-bootstrap interval [{float(sm[8]):+.4f}, {float(sm[9]):+.4f}], rule: {sm[10]}")
    print(out[-1], flush=True)
with open(os.path.join(HERE, "gamma_strict_seeds.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["test", "seed", "Q2_GM2", "Q2_LO2", "Q2_GM12", "Q2_LOh"]); w.writerows(allseeds)
out.append(out[0].replace("commit", "end: commit"))
open(os.path.join(HERE, "gamma_strict_out.txt"), "w").write("\n".join(out) + "\n")
