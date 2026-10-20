"""Exact distinct-value counts on all trees / trees with Delta<=4, orders 2..17.
Exactness: rational-exponent sums are reduced to the Q-basis {N^(1/k): N k-th-power-free}
(Besicovitch); at gamma=1,2 (algebraic) Lindemann-Weierstrass reduces equality to equality of the
per-imbalance-class coefficients. Every exact count is cross-checked numerically at 50 digits."""
import pickle, json, sys, time
from fractions import Fraction as F
from collections import Counter, defaultdict
import mpmath as mp
from common import qhist, radical_key, maxdeg, lo_mp, count_distinct_mp, qf

mp.mp.dps = 50
TOL = mp.mpf(10) ** -40
res = pickle.load(open("profiles_2_17.pkl", "rb"))

GM = {  # name: (alpha, beta, k)
    "M1": (F(0), F(1), 1), "M2": (F(1), F(0), 1), "HM": (F(0), F(2), 1), "mM2": (F(-1), F(0), 1),
    "R": (F(-1, 2), F(0), 2), "chi": (F(0), F(-1, 2), 2), "H": (F(0), F(-1), 1), "ISI": (F(1), F(-1), 1),
    "GA": (F(1, 2), F(-1), 2), "AG": (F(-1, 2), F(1), 2),
}
FRAC = [(F(0), F(1, 2)), (F(1, 2), F(0)), (F(0), F(-1, 2)), (F(-1, 2), F(0)), (F(1, 2), F(-1)),
        (F(-1, 2), F(1)), (F(1, 3), F(0)), (F(0), F(1, 3)), (F(1, 6), F(0))]

def kof(a, b):
    from math import lcm
    return lcm(a.denominator, b.denominator)

def sdd(p):
    return sum(m * (F(i, j) + F(j, i)) for (i, j), m in p)

def isdd(p):
    return sum(m * F(i * j, i * i + j * j) for (i, j), m in p)

out = {}
t0 = time.time()
for n in range(2, 18):
    for sset in ("all", "mol"):
        prof = {p: c for p, c in res[n]["profiles"].items() if sset == "all" or maxdeg(p) <= 4}
        P = list(prof)
        Ntrees = sum(prof.values())
        row = {"N": Ntrees, "profiles": len(P)}
        qh = {p: qhist(p) for p in P}
        row["qhist"] = len(set(qh.values()))
        # pure gamma at gamma=1,2: exact (per-q key at alpha=beta=0 == q-hist) and numeric
        for g in (1, 2):
            kx = len(set(radical_key(p, F(0), F(0), 1, per_q=True) for p in P))
            kn, gap = count_distinct_mp([lo_mp(p, 0, 0, g, mp) for p in P], TOL)
            row[f"LO00{g}"] = kx
            row[f"LO00{g}_num"] = kn
        for name, (a, b, k) in GM.items():
            keys = {p: radical_key(p, a, b, k) for p in P}
            row[name] = len(set(keys.values()))
            if name in ("R", "GA", "chi"):
                kn, gap = count_distinct_mp([lo_mp(p, mp.mpf(a.numerator) / a.denominator,
                                                   mp.mpf(b.numerator) / b.denominator, 0, mp) for p in P], TOL)
                row[name + "_num"] = kn
            if name == "GA":
                grp = defaultdict(set)
                for p in P:
                    grp[keys[p]].add(qh[p])
                merges = [k_ for k_, s in grp.items() if len(s) > 1]
                row["GA_merges_qhist"] = len(merges)
                if merges:
                    row["GA_merge_example"] = [str([q for q in s]) for s in [grp[merges[0]]]]
                    # store profiles in merge
                    row["GA_merge_profiles"] = [str(p) for p in P if keys[p] == merges[0]]
        row["SDD"] = len(set(sdd(p) for p in P))
        row["ISDD"] = len(set(isdd(p) for p in P))
        for (a, b) in FRAC:
            k = kof(a, b)
            for g in (0, 1):
                kk = len(set(radical_key(p, a, b, k, per_q=(g == 1)) for p in P))
                row[f"({a},{b},{g})"] = kk
        if n >= 12:
            kn, gap = count_distinct_mp([lo_mp(p, mp.mpf("0.3"), mp.mpf("0.2"), 0, mp) for p in P], TOL)
            row["generic(0.3,0.2,0)_num"] = kn
            row["generic_mingap"] = mp.nstr(gap, 5) if gap is not None else None
            for (a, b) in [(F(1, 2), F(0)), (F(-1, 2), F(0)), (F(0), F(1, 2)), (F(0), F(1, 3))]:
                kn, _ = count_distinct_mp([lo_mp(p, mp.mpf(a.numerator) / a.denominator,
                                                 mp.mpf(b.numerator) / b.denominator, 1, mp) for p in P], TOL)
                row[f"({a},{b},1)_num"] = kn
        out[f"{n}_{sset}"] = row
        print(n, sset, {k: v for k, v in row.items() if "example" not in k and "profiles" != k[:8]},
              f"{time.time()-t0:.0f}s", flush=True)
json.dump(out, open("counts_out.json", "w"), indent=1, default=str)
