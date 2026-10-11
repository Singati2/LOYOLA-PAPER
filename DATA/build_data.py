#!/usr/bin/env python3
"""Build the DATA/ folder: one place with every dataset the paper uses.

The analysis scripts keep reading the original files (octane_data.py,
external/..., octane_property_provenance_v35.csv). This script copies them here
byte for byte, and writes octane_properties.csv from octane_data.OCTANES, so
the copies can never drift from what the analyses use.

  python3 DATA/build_data.py           rebuild DATA/
  python3 DATA/build_data.py --check   exit 1 if any file in DATA/ differs from its source
"""
import csv, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

COPIES = [  # (file in DATA/, source relative to the repository root)
    ("octane_provenance.csv", "octane_property_provenance_v35.csv"),
    ("nonane_properties.csv", "external/nonane_data.csv"),
    ("nonane_provenance.csv", "external/nonane_provenance.csv"),
    ("boiling_points_C6_C10.csv", "external/bp/bp_data.csv"),
    ("boiling_points_provenance.csv", "external/bp/bp_provenance.csv"),
    ("calorimetric_dHvap298_alkanes.csv", "external/bp/calorimetric_dHvap298_alkanes.csv"),
]


def octane_csv():
    import octane_data as od
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["name", "smiles", "T_B_C", "dHf_kcal_per_mol", "dHvap_kcal_per_mol", "S_cal_per_mol_K", "omega"])
    for name, row in zip(od.NAMES, od.OCTANES):
        w.writerow([name, *row])
    return buf.getvalue().encode()


def inchi_degree_pairs(inchi):
    """Unordered degree pairs of the carbon skeleton from the /c connection layer of an alkane InChI."""
    import re as _re
    layer = inchi.split("/c", 1)[1].split("/", 1)[0]
    edges, stack, prev = set(), [], None
    for tok in _re.findall(r"\d+|[-(),]", layer):
        if tok.isdigit():
            a = int(tok)
            if prev is not None:
                edges.add(frozenset((prev, a)))
            prev = a
        elif tok == "(":
            stack.append(prev)
        elif tok == ")":
            prev = stack.pop()
        elif tok == ",":
            prev = stack[-1]
    deg = {}
    for e in edges:
        for v in e:
            deg[v] = deg.get(v, 0) + 1
    return sorted(tuple(sorted(deg[v] for v in e)) for e in edges)


def bp_structures_csv():
    """Structure table for the 100 boiling-point molecules (v40.28): NIST identifiers and the skeleton
    InChI from the archived NIST audit, with the degree pairs re-derived from the InChI and required
    to equal those used by the analyses."""
    audit = list(csv.DictReader(open(os.path.join(ROOT, "external", "bp", "nist_alkanes_skeletons_audit.csv"))))
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["n_C", "name", "nist_id", "inchi_skeleton", "degree_pairs"])
    for r in csv.DictReader(open(os.path.join(ROOT, "external", "bp", "bp_data.csv"))):
        ids = set(r["nist_id"].split())
        hits = [a for a in audit if ids & set(a["ids"].split())]
        if len(hits) != 1:
            sys.exit(f"structure table: {len(hits)} audit rows for {r['nist_id']}")
        inchi = hits[0]["skel"]
        got = " ".join(f"{i}-{j}" for i, j in inchi_degree_pairs(inchi))
        want = " ".join(sorted(r["degree_pairs"].split(), key=lambda t: tuple(map(int, t.split("-")))))
        if got != want or f"C{r['n_C']}H" not in inchi:
            sys.exit(f"structure table: InChI {inchi} gives {got}, data have {want}")
        w.writerow([r["n_C"], r["name"], r["nist_id"], inchi, r["degree_pairs"]])
    return buf.getvalue().encode()


def expected():
    out = {"octane_properties.csv": octane_csv(), "boiling_points_structures.csv": bp_structures_csv()}
    for dst, src in COPIES:
        with open(os.path.join(ROOT, src), "rb") as f:
            out[dst] = f.read()
    return out


def main():
    want = expected()
    if "--check" in sys.argv:
        bad = []
        for name, data in want.items():
            p = os.path.join(HERE, name)
            if not os.path.exists(p) or open(p, "rb").read() != data:
                bad.append(name)
        print("DATA/ check:", "every file matches its source" if not bad else "DIFFERS: " + ", ".join(bad))
        sys.exit(1 if bad else 0)
    for name, data in want.items():
        with open(os.path.join(HERE, name), "wb") as f:
            f.write(data)
    print(f"wrote {len(want)} files to DATA/")


if __name__ == "__main__":
    main()
