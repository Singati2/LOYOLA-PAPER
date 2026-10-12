#!/usr/bin/env python3
"""Adequacy of the press_size rank threshold (v40.29) on the boiling-point tests.

Runs Tests A and B of external/bp/bp_tests.py exactly as published (same seeds, same calls), with
press_size wrapped so that every call is also evaluated by an independent QR solve. It records:
the number of calls and candidates; the counts rejected at the current threshold (1e-6) and at the
former one (1e-10); the count in [1e-10, 1e-6); the smallest singular-value ratio; the largest
absolute and relative difference between accepted PRESS values and QR; how often the selected
candidate (argmin) differs from the QR argmin, under each threshold; and leverage-1 rejections.
It then checks that the wrapped run reproduces the committed bp_results_summary.csv and
bp_baselines.csv, so the probe covers the published run. It writes no file of the package except
its own output.

  cd audit/final/scripts && python3 press_size_probe.py      -> press_size_probe_out.txt
"""
import csv, json, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BPDIR = os.path.join(ROOT, "external", "bp")
sys.path.insert(0, BPDIR)
import bp_tests as BP

orig = BP.press_size
S = {"calls": 0, "candidates": 0, "rej_1e6": 0, "rej_1e10": 0, "band": 0, "min_ratio_all": np.inf,
     "min_ratio_accepted": np.inf, "max_rel_vs_qr": 0.0, "max_abs_vs_qr": 0.0, "argmin_changes": 0,
     "argmin_changes_if_1e10": 0, "rank_reject_leverage": 0}


def press_qr(A, yt):
    Q, _ = np.linalg.qr(A)
    h = (Q ** 2).sum(axis=2); res = yt - np.einsum("cni,cmi,m->cn", Q, Q, yt)
    return np.sqrt(((res / (1 - h)) ** 2).mean(axis=1)), h


def wrapped(Xt, zt, yt):
    r = orig(Xt, zt, yt)
    X = BP._standardize(np.asarray(Xt, float)); C, n = X.shape
    zs = np.asarray(zt, float); zs = (zs - zs.mean()) / (zs.std() if zs.std() > 0 else 1.0)
    A = np.stack([np.ones((C, n)), np.broadcast_to(zs, (C, n)), X], axis=2)
    sv = np.linalg.svd(A, compute_uv=False); ratio = sv[:, -1] / sv[:, 0]
    q, h = press_qr(A, yt)
    ok6, ok10 = ratio > 1e-6, ratio > 1e-10
    S["calls"] += 1; S["candidates"] += C
    S["rej_1e6"] += int((~ok6).sum()); S["rej_1e10"] += int((~ok10).sum()); S["band"] += int((ok10 & ~ok6).sum())
    S["min_ratio_all"] = min(S["min_ratio_all"], float(ratio.min()))
    fin = np.isfinite(r)
    S["rank_reject_leverage"] += int((ok6 & ~fin).sum())
    if fin.any():
        S["min_ratio_accepted"] = min(S["min_ratio_accepted"], float(ratio[fin].min()))
        d = np.abs(r[fin] - q[fin])
        S["max_abs_vs_qr"] = max(S["max_abs_vs_qr"], float(d.max())); S["max_rel_vs_qr"] = max(S["max_rel_vs_qr"], float((d / q[fin]).max()))
        if int(np.argmin(r)) != int(np.argmin(np.where(fin, q, np.inf))): S["argmin_changes"] += 1
        q10 = np.where(ok10 & np.all(np.abs(1 - h) > 1e-10, axis=1), q, np.inf)
        if int(np.argmin(r)) != int(np.argmin(q10)): S["argmin_changes_if_1e10"] += 1
    return r


BP.press_size = wrapped
# bp_tests.main() without its file writes
rows, P, y, z = BP.load()
dec = [i for i, r in enumerate(rows) if r["n_C"] == "10"]
summ, base = [], []
for label, args in (("A: decane T_B", ([P[i] for i in dec], y[dec], None)), ("B: pooled C6-C10 T_B (size-adjusted)", (P, y, z))):
    _, sm = BP.run_test(label, *args); summ.append(sm); base += BP.baselines(label, *args)

def same(path, got):
    ref = list(csv.reader(open(os.path.join(BPDIR, path))))[1:]
    return [[str(v) for v in r] for r in got] == ref

lines = ["press_size threshold probe over the published Tests A and B (external/bp/bp_tests.py)",
         "reproduces bp_results_summary.csv: " + str(same("bp_results_summary.csv", summ)),
         "reproduces bp_baselines.csv: " + str(same("bp_baselines.csv", base)),
         f"calls {S['calls']}, candidates {S['candidates']}",
         f"rejected at 1e-6: {S['rej_1e6']}; at 1e-10: {S['rej_1e10']}; in [1e-10, 1e-6): {S['band']}",
         f"smallest sv_min/sv_max: all {S['min_ratio_all']:.3e}, accepted {S['min_ratio_accepted']:.3e}",
         f"accepted PRESS vs QR: max relative difference {S['max_rel_vs_qr']:.2e}, max absolute {S['max_abs_vs_qr']:.2e}",
         f"selected candidate differs from QR argmin: {S['argmin_changes']} calls (at 1e-10: {S['argmin_changes_if_1e10']})",
         f"leverage-1 rejections among rank-accepted candidates: {S['rank_reject_leverage']}"]
out = "\n".join(lines) + "\n"
print(out, end="")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "press_size_probe_out.txt"), "w").write(out)
ok = "False" not in out and S["rej_1e6"] == 0 and S["argmin_changes"] == 0
sys.exit(0 if ok else 1)
