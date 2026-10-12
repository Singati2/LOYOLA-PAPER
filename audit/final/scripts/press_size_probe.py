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
its own output. It exits non-zero unless verdict() holds: both reproductions, no rejection at
either threshold, no selection change, no leverage-1 rejection, every rank-accepted PRESS and every
QR value finite, and accepted PRESS within QR_REL_TOL of QR. QR_REL_TOL = 1e-8 is about 100 times
the observed maximum (7.3e-11) and far below the 1e-4 worst case the threshold allows.

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
     "argmin_changes_if_1e10": 0, "rank_reject_leverage": 0, "nonfinite_qr": 0}
QR_REL_TOL = 1e-8


def verdict(S, repro_summary, repro_baselines):
    """List of failed conditions (empty iff the probe passes)."""
    fails = []
    if not (repro_summary and repro_baselines): fails.append("published outputs not reproduced")
    for k in ("rej_1e6", "rej_1e10", "band", "argmin_changes", "argmin_changes_if_1e10", "rank_reject_leverage", "nonfinite_qr"):
        if S[k] != 0: fails.append(f"{k} = {S[k]}")
    if not (S["calls"] > 0 and S["candidates"] > 0): fails.append("no press_size call observed")
    if not (np.isfinite(S["max_rel_vs_qr"]) and S["max_rel_vs_qr"] <= QR_REL_TOL): fails.append(f"max_rel_vs_qr = {S['max_rel_vs_qr']}")
    if not np.isfinite(S["max_abs_vs_qr"]): fails.append("max_abs_vs_qr not finite")
    return fails


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
    S["nonfinite_qr"] += int((fin & ~np.isfinite(q)).sum())
    if fin.any():
        S["min_ratio_accepted"] = min(S["min_ratio_accepted"], float(ratio[fin].min()))
        d = np.abs(r[fin] - q[fin])
        S["max_abs_vs_qr"] = max(S["max_abs_vs_qr"], float(d.max())); S["max_rel_vs_qr"] = max(S["max_rel_vs_qr"], float((d / q[fin]).max()))
        if int(np.argmin(r)) != int(np.argmin(np.where(fin, q, np.inf))): S["argmin_changes"] += 1
        q10 = np.where(ok10 & np.all(np.abs(1 - h) > 1e-10, axis=1), q, np.inf)
        if int(np.argmin(r)) != int(np.argmin(q10)): S["argmin_changes_if_1e10"] += 1
    return r


def same(path, got):
    ref = list(csv.reader(open(os.path.join(BPDIR, path))))[1:]
    return [[str(v) for v in r] for r in got] == ref


def main():
    BP.press_size = wrapped
    # bp_tests.main() without its file writes
    rows, P, y, z = BP.load()
    dec = [i for i, r in enumerate(rows) if r["n_C"] == "10"]
    summ, base = [], []
    for label, args in (("A: decane T_B", ([P[i] for i in dec], y[dec], None)), ("B: pooled C6-C10 T_B (size-adjusted)", (P, y, z))):
        _, sm = BP.run_test(label, *args); summ.append(sm); base += BP.baselines(label, *args)

    rs, rb = same("bp_results_summary.csv", summ), same("bp_baselines.csv", base)
    lines = ["press_size threshold probe over the published Tests A and B (external/bp/bp_tests.py)",
             "reproduces bp_results_summary.csv: " + str(rs),
             "reproduces bp_baselines.csv: " + str(rb),
             f"calls {S['calls']}, candidates {S['candidates']}",
             f"rejected at 1e-6: {S['rej_1e6']}; at 1e-10: {S['rej_1e10']}; in [1e-10, 1e-6): {S['band']}",
             f"smallest sv_min/sv_max: all {S['min_ratio_all']:.3e}, accepted {S['min_ratio_accepted']:.3e}",
             f"accepted PRESS vs QR: max relative difference {S['max_rel_vs_qr']:.2e}, max absolute {S['max_abs_vs_qr']:.2e}",
             f"selected candidate differs from QR argmin: {S['argmin_changes']} calls (at 1e-10: {S['argmin_changes_if_1e10']})",
             f"leverage-1 rejections among rank-accepted candidates: {S['rank_reject_leverage']}"]
    out = "\n".join(lines) + "\n"
    print(out, end="")
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "press_size_probe_out.txt"), "w").write(out)
    fails = verdict(S, rs, rb)
    for f in fails: print("FAIL:", f, file=sys.stderr)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
