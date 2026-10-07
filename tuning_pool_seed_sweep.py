#!/usr/bin/env python3
"""Seed sweep behind the Supplementary S2 sentence on the nested gain of local
tuning near M2 on omega: the 50-triple pool of Table S2 is re-drawn with
default_rng(seed) for seed = 0..99 (same recipe as verify_loyola_v35.py
section [E]: perturbations U(-0.3, 0.3) rounded to two decimals, pools drawn
in the order M2, HM, mM2, LO(0,0,1), LO(0,0,2)), and the nested leave-one-out
gain LOO_50 - LOO_0 (|r| of the leave-one-out predictions with the in-fold
best pool member minus |r| with the anchor) is recorded for M2 on omega.
Output: tuning_pool_seed_sweep_out.txt (committed).  Runtime: seconds."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from octane_data import OCTANES, PROPS, alkane_pairs, lo_pairs

OP = [alkane_pairs(r[0]) for r in OCTANES]; n = len(OP)
Y = {p: np.array([r[1 + i] for r in OCTANES], float) for i, p in enumerate(PROPS)}
ANCH = [("M2", (1., 0., 0.)), ("HM", (0., 2., 0.)), ("mM2", (-1., 0., 0.)), ("LO(0,0,1)", (0., 0., 1.)), ("LO(0,0,2)", (0., 0., 2.))]


def col(t):
    return np.array([lo_pairs(P, *t) for P in OP])


def absr(x, y):
    xc = x - x.mean(); yc = y - y.mean()
    return abs(float(xc @ yc / (np.linalg.norm(xc) * np.linalg.norm(yc))))


def loo_pred(x, y):
    pred = np.empty(n)
    for i in range(n):
        m = np.ones(n, bool); m[i] = False; xt, yt = x[m], y[m]
        if xt.var() == 0:
            pred[i] = yt.mean()
        else:
            b = ((xt - xt.mean()) * (yt - yt.mean())).sum() / ((xt - xt.mean()) ** 2).sum()
            pred[i] = (yt.mean() - b * xt.mean()) + b * x[i]
    return pred


def nested_gain(seed, anchor, prop):
    rng = np.random.default_rng(seed); pools = {}
    for anm, (a0, b0, g0) in ANCH:
        perts = []
        for _ in range(50):
            da, db, dg = (round(float(rng.uniform(-0.3, 0.3)), 2) for _ in range(3))
            perts.append((round(a0 + da, 2), round(b0 + db, 2), round(g0 + dg, 2)))
        pools[anm] = perts
    y = Y[prop]; a0 = dict(ANCH)[anchor]
    pc = [col(t) for t in pools[anchor]]; xb = col(a0)
    l0 = absr(loo_pred(xb, y), y)
    pred = np.empty(n)
    for i in range(n):
        m = np.ones(n, bool); m[i] = False; yt = y[m]
        bk, bt = -1, -1.0
        for kk, c in enumerate(pc):
            rr = absr(c[m], yt)
            if rr > bt:
                bt, bk = rr, kk
        x = pc[bk]; xt = x[m]
        if xt.var() == 0:
            pred[i] = yt.mean()
        else:
            b = ((xt - xt.mean()) * (yt - yt.mean())).sum() / ((xt - xt.mean()) ** 2).sum()
            pred[i] = (yt.mean() - b * xt.mean()) + b * x[i]
    return absr(pred, y) - l0


def main():
    gains = np.array([nested_gain(s, "M2", "omega") for s in range(100)])
    g42 = nested_gain(42, "M2", "omega")
    lines = [f"seed-42 pool (Table S2): nested gain M2/omega = {g42:+.4f}",
             f"seeds 0-99: median nested gain M2/omega = {np.median(gains):+.4f}, positive in {int((gains > 0).sum())} of 100 seeds, "
             f"min {gains.min():+.4f}, max {gains.max():+.4f}"]
    print("\n".join(lines)); open(os.path.join(HERE, "tuning_pool_seed_sweep_out.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
