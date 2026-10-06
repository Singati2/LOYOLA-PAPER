#!/usr/bin/env python3
"""Pre-registered external validation on the 35 nonane isomers (PREREG_v37.md).

Q1: for each property with >= 25 NIST-sourced values (T_B, dHvap), the matched-
budget nested LOO comparison of the optimized parent GM (gamma = 0) and the
optimized Loyola family (gamma free), seeds 0..99, budgets 200 and 500, with the
paired control (LO candidates with gamma zeroed). Identical protocol and
candidate stream to the octane analysis (via external/baselines.py, which
reproduces the octane package values exactly).

Decision rule (fixed in PREREG before data): replicates if LO better in
>= 80/100 seeds at both budgets AND median dQ2 > 0 at both; does not replicate
if LO better in <= 50/100 at either budget; otherwise mixed.

Sensitivity (deviation D4): T_B with 2,3,3,4-tetramethylpentane replaced by the
median of its individual NIST boiling points.

Outputs: nonane_validation_seeds.csv, nonane_validation_summary.csv
"""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import baselines as B
from octane_data import alkane_pairs

SEEDS, BUDGETS = range(100), (200, 500)


def load():
    rows = list(csv.DictReader(open(os.path.join(HERE, "nonane_data.csv"))))
    return rows


def d4_median():
    """Median of the individual NIST T_B points for 2,3,3,4-tetramethylpentane (K).

    The points are read from the archived NIST data-points page
    (nonane_raw_nist/pts_C16747389_TBOIL.html) with the same table parser as
    the boiling-point dataset build, and cross-checked against the values
    quoted in nonane_provenance.csv; a mismatch stops the run."""
    import html as _html, re
    page = os.path.join(HERE, "nonane_raw_nist", "pts_C16747389_TBOIL.html")
    t = open(page, errors="replace").read()
    m = re.search(r'<table class="data"[^>]*>(.*?)</table>', t, re.S)
    if not m:
        raise SystemExit("D4: no data table in the archived NIST points page")
    clean = lambda x: re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", x))).strip()
    rows = [[clean(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            for r in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S)]
    vals = [float(r[0].rstrip(".")) for r in rows if len(r) >= 2 and re.fullmatch(r"\d{3}\.\d*", r[0])]
    quoted = []
    for r in csv.DictReader(open(os.path.join(HERE, "nonane_provenance.csv"))):
        if r["name"].endswith("2,3,3,4-tetramethylpentane") and r["property"] == "T_B":
            quoted = [float(x.rstrip(".")) for x in re.findall(r"(\d{3}\.\d*) K \(", r["all_determinations"])]
    if not vals or sorted(vals) != sorted(quoted):
        raise SystemExit(f"D4: archived page points {vals} do not match provenance {quoted}")
    return float(np.median(vals)), vals


def q2(preds, y):
    return 1 - ((preds - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def run(P, y):
    out = []
    for seed in SEEDS:
        for b in BUDGETS:
            gm_t, lo_t = B.candidate_triples(seed, b)
            lz_t = np.column_stack([lo_t[:, :2], np.zeros(b)])
            res = []
            for T in (gm_t, lo_t, lz_t):
                X = B.descriptor_matrix(P, T)
                preds, _ = B.outer_loo(B.fold_select_ols, X, y)
                res.append(q2(preds, y))
            out.append((seed, b, *res))
    return out


def classify(rows):
    verdict = {}
    for b in BUDGETS:
        d = np.array([r[3] - r[2] for r in rows if r[1] == b])
        verdict[b] = (int((d > 0).sum()), float(np.median(d)))
    better = [verdict[b][0] for b in BUDGETS]; med = [verdict[b][1] for b in BUDGETS]
    if min(better) >= 80 and min(med) > 0:
        v = "REPLICATES"
    elif min(better) <= 50:
        v = "DOES NOT REPLICATE"
    else:
        v = "MIXED"
    return v, verdict


def main():
    rows = load()
    analyses = []
    for prop, col in (("T_B", "T_B_C"), ("dHvap", "dHvap_kcal")):
        keep = [r for r in rows if r[col].strip()]
        P = [alkane_pairs(r["smiles"]) for r in keep]
        y = np.array([float(r[col]) for r in keep])
        analyses.append((prop, "primary", P, y))
        if prop == "T_B":
            med, pts = d4_median()
            y2 = y.copy()
            idx = [i for i, r in enumerate(keep) if r["name"].endswith("2,3,3,4-tetramethylpentane")][0]
            y2[idx] = round(med - 273.15, 1)
            analyses.append((prop, f"D4 sensitivity (TMP T_B = median {med:.2f} K of {len(pts)} points)", P, y2))
    seeds_out, summ = [], []
    for prop, label, P, y in analyses:
        res = run(P, y)
        v, verdict = classify(res)
        for r in res:
            seeds_out.append([prop, label, r[0], r[1]] + [f"{x:+.10f}" for x in (r[2], r[3], r[3] - r[2], r[4], r[3] - r[4])])
        for b in BUDGETS:
            d = np.array([r[3] - r[2] for r in res if r[1] == b])
            dp = np.array([r[3] - r[4] for r in res if r[1] == b])
            qg = np.array([r[2] for r in res if r[1] == b]); ql = np.array([r[3] for r in res if r[1] == b])
            summ.append([prop, label, len(y), b, int((d > 0).sum()), int((dp > 0).sum()),
                         f"{np.median(qg):+.4f}", f"{np.median(ql):+.4f}",
                         f"{np.median(d):+.4f}", f"{d.min():+.4f}", f"{d.max():+.4f}", v])
        print(f"{prop:6s} {label[:40]:40s} n={len(y)}  verdict: {v}  "
              + "  ".join(f"B={b}: LO better {verdict[b][0]}/100, median dQ2 {verdict[b][1]:+.4f}" for b in BUDGETS))
    with open(os.path.join(HERE, "nonane_validation_seeds.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["property", "analysis", "seed", "budget", "Q2_GM", "Q2_LO", "dQ2", "Q2_LOzero", "dQ2_paired"])
        w.writerows(seeds_out)
    with open(os.path.join(HERE, "nonane_validation_summary.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["property", "analysis", "n", "budget", "LO_better", "paired_better",
                                       "median_Q2_GM", "median_Q2_LO", "median_dQ2", "dQ2_min", "dQ2_max", "prereg_verdict"])
        w.writerows(summ)


if __name__ == "__main__":
    main()
