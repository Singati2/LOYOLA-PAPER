"""Prop. 5(ii) equality A(R) = min(|R|-1, r(R), 3): exhaustive over ALL subsets of P_6 (2^21),
and over subsets of P_7 with at most 6 pairs. Batched SVD, tol 1e-9; margins reported."""
import itertools, math, json, sys
import numpy as np
from fractions import Fraction as F

def pairs(D):
    return [(i, j) for i in range(1, D + 1) for j in range(i, D + 1)]

def z(i, j):
    return [math.log(i * j), math.log(i + j), abs(i - j) / (i + j)]

def check(D, maxsize=None, tol=1e-9):
    Pd = pairs(D)
    Z = np.array([z(*p) for p in Pd])
    Q = [F(abs(i - j), i + j) for i, j in Pd]
    viol = []
    min_ok_sv = np.inf; max_zero_sv = 0.0
    nsub = 0
    top = len(Pd) if maxsize is None else maxsize
    for k in range(1, top + 1):
        combs = np.array(list(itertools.combinations(range(len(Pd)), k)), dtype=np.int16)
        nsub += len(combs)
        if k == 1:
            continue
        # chunk to bound memory
        for s in range(0, len(combs), 200000):
            C = combs[s:s + 200000]
            pts = Z[C]                        # (b,k,3)
            Dm = pts[:, 1:, :] - pts[:, :1, :]  # (b,k-1,3)
            sv = np.linalg.svd(Dm, compute_uv=False)  # (b, min(k-1,3))
            A = (sv > tol).sum(1)
            nz = sv[sv > tol]
            if nz.size: min_ok_sv = min(min_ok_sv, nz.min())
            zz = sv[sv <= tol]
            if zz.size: max_zero_sv = max(max_zero_sv, zz.max())
            for row, a in zip(C, A):
                r = len(set(Q[t] for t in row))
                bound = min(k - 1, r, 3)
                if a < bound:
                    viol.append(([Pd[t] for t in row], int(a), bound))
    return nsub, viol, float(min_ok_sv), float(max_zero_sv)

out = {}
for D in range(1, 7):
    nsub, viol, mok, mz = check(D)
    out[f"Delta{D}_all_subsets"] = {"subsets": nsub, "violations": len(viol), "min_nonzero_sv": mok, "max_zero_sv": mz}
    print(D, out[f"Delta{D}_all_subsets"], flush=True)
nsub, viol, mok, mz = check(7, maxsize=6)
v4 = [v for v in viol if len(v[0]) <= 4]
out["Delta7_subsets_le6"] = {"subsets": nsub, "violations_total": len(viol), "violations_le4": [str(v) for v in v4],
                             "all_violations_contain_the_sum8_set": all({(1, 7), (2, 6), (3, 5), (4, 4)} <= set(v[0]) for v in viol),
                             "min_nonzero_sv": mok, "max_zero_sv": mz}
print(out["Delta7_subsets_le6"])
json.dump(out, open("identrank_out.json", "w"), indent=1)
