#!/usr/bin/env python3
"""Checks for external/baselines.py (run: python3 external/test_baselines.py).

1. GM/LO reproduce the package exactly: seed 12345 / budget 200 (ablation
   values) and every one of the 1000 rows of expanded_robustness_v35.csv
   (Q2_GM, Q2_LO to 1e-9), hence the 100-seed summary counts/medians in
   expanded_robustness_summary_v35.csv.
2. Descriptor sanity: fixed indices on n-octane / known closed forms.
3. Leakage: for every method, property and outer fold, replacing the held-out
   y by a shuffled / wild value changes neither the selection nor the
   held-out prediction.
"""
import csv, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import baselines as B  # noqa: E402

FAIL = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


def main():
    t0 = time.time()
    ds = B.load_octane()
    rows, _ = B.analyse(ds, verbose=False)
    get = {(r["property"], r["method"]): r for r in rows}

    print("[1] reproduction of package values")
    ref = {"T_B": (0.612757, 0.748334), "dHvap": (0.884398, 0.970845)}
    for p, (qg, ql) in ref.items():
        g = get[(p, "GM_s12345_b200")]["Q2"]; l = get[(p, "LO_s12345_b200")]["Q2"]
        check(round(g, 6) == qg and round(l, 6) == ql,
              f"{p} seed12345/b200 Q2_GM {g:.6f} (want {qg}), Q2_LO {l:.6f} (want {ql})")
    for r in csv.DictReader(open(os.path.join(ROOT, "ablation_robustness.csv"))):
        if r["seed"] == "12345" and r["budget"] == "200":
            p = r["property"]
            g = get[(p, "GM_s12345_b200")]["Q2"]; l = get[(p, "LO_s12345_b200")]["Q2"]
            check(abs(g - float(r["Q2_GM"])) < 1e-9 and abs(l - float(r["Q2_LO"])) < 1e-9,
                  f"{p} seed12345/b200 vs ablation_robustness.csv (1e-9)")
    per = {p: (get[(p, "GM_s12345_b200")]["_per_seed"], get[(p, "LO_s12345_b200")]["_per_seed"])
           for p in ds["props"]}
    nrow, maxdev = 0, 0.0
    for r in csv.DictReader(open(os.path.join(ROOT, "expanded_robustness_v35.csv"))):
        sb = (int(r["seed"]), int(r["budget"])); gm, lo = per[r["property"]]
        maxdev = max(maxdev, abs(gm[sb][0] - float(r["Q2_GM"])), abs(lo[sb][0] - float(r["Q2_LO"])))
        nrow += 1
    check(nrow == 1000 and maxdev < 1e-9,
          f"expanded_robustness_v35.csv: {nrow} rows, max |dQ2| deviation {maxdev:.2e}")
    for r in csv.DictReader(open(os.path.join(ROOT, "expanded_robustness_summary_v35.csv"))):
        b, p = int(r["budget"]), r["property"]; gm, lo = per[p]
        d = np.array([lo[(s, b)][0] - gm[(s, b)][0] for s in B.SEEDS])
        okc = (int((d > 0).sum()) == int(r["LO_better"]) and int((d < 0).sum()) == int(r["LO_worse"])
               and abs(np.median(d) - float(r["dQ2_median"])) < 1e-9
               and abs(d.min() - float(r["dQ2_min"])) < 1e-9 and abs(d.max() - float(r["dQ2_max"])) < 1e-9)
        check(okc, f"summary b{b} {p}: LO_better {int((d > 0).sum())}/{r['LO_better']}, "
                   f"median dQ2 {np.median(d):+.10f}/{r['dQ2_median']}")

    print("[2] descriptor sanity")
    P = B.alkane_pairs("CCCCCCCC")  # path P8: 2 (1,2) edges, 5 (2,2) edges
    X = B.descriptor_matrix([P], [t for _, t in B.FIXED_INDICES])[:, 0]
    want = {"M1": 26, "M2": 24, "HM": 98, "mM2": 2 / 2 + 5 / 4, "R": 2 / 2**0.5 + 5 / 2,
            "chi": 2 / 3**0.5 + 5 / 2, "H/2": 2 / 3 + 5 / 4, "ISI": 2 * 2 / 3 + 5,
            "GA": 2 * 2**0.5 / 3 + 5 / 2, "AG": 2 * 3 / 2**0.5 + 5 * 2,
            "LO(0,0,1)": 2 * np.exp(1 / 3) + 5, "LO(0,0,2)": 2 * np.exp(2 / 3) + 5}
    for k, (name, _) in enumerate(B.FIXED_INDICES):
        check(abs(X[k] - want[name]) < 1e-12, f"{name}(P8) = {X[k]:.6f}")
    check(abs(B.irla(P) - 4 / 3) < 1e-12, "IRLA(P8) = 4/3")
    c = B.count_vector(B.alkane_pairs("CC(C)(C)C(C)(C)C"))
    check(c[B.DEG_PAIRS.index((1, 4))] == 6 and c[B.DEG_PAIRS.index((4, 4))] == 1 and c.sum() == 7,
          "count vector of 2,2,3,3-tetramethylbutane")
    # ridge: lambda -> 0 equals OLS on standardized (full-rank) subset
    rng = np.random.default_rng(0)
    F = rng.normal(size=(20, 3)); yy = F @ [1, -2, 0.5] + rng.normal(size=20)
    Xd = np.column_stack([np.ones(20), F]); beta = np.linalg.lstsq(Xd, yy, rcond=None)[0]
    check(np.allclose(B.ridge_fit_predict(F, yy, F[:2], 1e-12), Xd[:2] @ beta, atol=1e-8),
          "ridge(lambda->0) == OLS with intercept")

    print("[3] leakage: perturbing the held-out y changes nothing")
    pairs = [B.alkane_pairs(s) for s in ds["smiles"]]
    gm_t, lo_t = B.candidate_triples(0, 200)
    feats = {
        "mean": (B.fold_mean, None),
        "fixed_best": (B.fold_select_ols, B.descriptor_matrix(pairs, [t for _, t in B.FIXED_INDICES])),
        "IRLA": (B.fold_ols, np.array([B.irla(P) for P in pairs])),
        "ridge_counts": (B.fold_ridge, np.array([B.count_vector(P) for P in pairs])),
        "GM(seed0,b200)": (B.fold_select_ols, B.descriptor_matrix(pairs, gm_t)),
        "LO(seed0,b200)": (B.fold_select_ols, B.descriptor_matrix(pairs, lo_t)),
    }
    lrng = np.random.default_rng(2026)
    for mname, (fn, Fm) in feats.items():
        bad = 0; tot = 0
        for p in ds["props"]:
            y = ds["Y"][p]
            perm = lrng.permutation(len(y))
            for i in range(len(y)):
                p0, s0 = fn(Fm, y, i)
                for newval in (y[perm[i]], y[i] + 1e3 * y.std(), -y[i]):
                    y2 = y.copy(); y2[i] = newval
                    p1, s1 = fn(Fm, y2, i)
                    tot += 1
                    bad += not (p0 == p1 and s0 == s1)
        check(bad == 0, f"{mname}: {tot} perturbed folds, {bad} changed")
    print(f"\n{len(FAIL)} failures; {time.time() - t0:.1f}s")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
