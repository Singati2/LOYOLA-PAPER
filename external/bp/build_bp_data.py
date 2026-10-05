#!/usr/bin/env python3
"""Build the v40 boiling-point dataset (acyclic alkanes C6-C10) from the
archived NIST WebBook pages in nist_raw/, applying the rule fixed in
../PREREG_v40.md:
  1. NIST average (AVG) if given;
  2. else median of non-compilation determinations if their spread <= 3 K;
  3. else EXCLUDED (reason recorded).
Compilations excluded from rule 2: Weast & Grasselli 1989; Majer & Svoboda 1985.
Grouped records: when several NIST entries share one InChI skeleton, all
their pages are pooled before the rule is applied (policy added in v40.2
after an audit found a second page for 3-ethyl-4-methylhexane had been
skipped; the earlier single-page behaviour is recorded in the changelog).
Structures come from the NIST InChI skeleton (connection layer), parsed by a
strict alkane parser and checked by isomorphism against the enumerated trees
(each tree matched at most once, max degree <= 4).
Outputs: bp_data.csv (included molecules), bp_provenance.csv (every molecule,
every determination, rule applied or exclusion reason).
"""
import csv, html, os, re, statistics, sys
from collections import Counter
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
COMP = {"Weast and Grasselli, 1989", "Majer and Svoboda, 1985"}


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def inchi_tree(inchi, n_expected):
    """Carbon tree from the /c connection layer of an alkane InChI; strict."""
    m = re.search(r"/c([^/]+)", inchi)
    if not m:
        raise ValueError(f"no connection layer: {inchi}")
    layer = m.group(1)
    if not re.fullmatch(r"[0-9()\-,]+", layer):
        raise ValueError(f"unexpected characters in {layer}")
    G = nx.Graph(); stack = []; prev = None; i = 0
    while i < len(layer):
        ch = layer[i]
        if ch.isdigit():
            j = i
            while j < len(layer) and layer[j].isdigit():
                j += 1
            a = int(layer[i:j]); G.add_node(a)
            if prev is not None:
                G.add_edge(prev, a)
            prev = a; i = j; continue
        if ch == "(":
            stack.append(prev)
        elif ch == ",":
            prev = stack[-1]
        elif ch == ")":
            prev = stack.pop()
        i += 1
    if stack or G.number_of_nodes() != n_expected or not nx.is_tree(G) or max(d for _, d in G.degree()) > 4:
        raise ValueError(f"not a valid C{n_expected} alkane tree: {layer}")
    return G


def tboil(page):
    t = open(page, errors="replace").read()
    m = re.search(r'<table class="data" aria-label="One dimensional data">(.*?)</table>', t, re.S)
    if not m:
        return []
    rows = [[clean(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
            for r in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S)]
    return [r for r in rows if r and r[0] == "Tboil"]


def val(s):
    return float(s.split("±")[0].strip().rstrip("."))


def main():
    sk = [a for a in csv.DictReader(open(os.path.join(HERE, "nist_alkanes_skeletons_audit.csv")))
          if a["n"] in ("6", "7", "8", "9", "10")]
    trees = {n: [T for T in nx.nonisomorphic_trees(n) if max(d for _, d in T.degree()) <= 4] for n in range(6, 11)}
    used = Counter()
    data, prov = [], []
    for a in sk:
        n = int(a["n"])
        G = inchi_tree(a["skel"], n)
        idx = [k for k, T in enumerate(trees[n]) if nx.is_isomorphic(G, T)]
        if len(idx) != 1:
            raise SystemExit(f"structure match failed for {a['names']}")
        used[(n, idx[0])] += 1
        # Grouped-record policy (v40.2): a skeleton may have several NIST
        # entries with the same InChI (e.g. a racemic and an optically active
        # entry). ALL their pages are read and their boiling-point rows pooled
        # before the pre-registered rule is applied; every page is recorded.
        tb, cids = [], []
        for cid in a["ids"].split():
            p = os.path.join(HERE, "nist_raw", cid + ".html")
            if os.path.exists(p):
                rows_ = tboil(p)
                if rows_:
                    tb += [r + [cid] for r in rows_]; cids.append(cid)
        name = a["names"].split(";")[0].strip()
        pairs = sorted(tuple(sorted((G.degree(u), G.degree(v)))) for u, v in G.edges())
        pairs_s = " ".join(f"{i}-{j}" for i, j in pairs)
        if not tb:
            prov.append([n, name, a["ids"], "", "EXCLUDED", "no NIST boiling point", ""]); continue
        cid = " ".join(cids)
        dets = " ; ".join(f"{r[1]} K ({r[4]}; {r[3]}; {r[-1]})" for r in tb)
        avg = [r for r in tb if r[3] == "AVG"]
        prim = [val(r[1]) for r in tb if r[3] != "AVG" and r[4] not in COMP]
        if avg:
            av = [val(r[1]) for r in avg]
            if max(av) - min(av) > 3.0:
                prov.append([n, name, cid, "", "EXCLUDED", f"NIST averages on grouped pages differ by {max(av)-min(av):.2f} K > 3 K", dets]); continue
            T = statistics.mean(av); rule = "AVG" if len(av) == 1 else f"mean of {len(av)} NIST averages (agreeing within 3 K)"
        elif prim and max(prim) - min(prim) <= 3.0:
            T = statistics.median(prim); rule = f"median of {len(prim)} non-compilation determination(s), spread {max(prim)-min(prim):.2f} K"
        else:
            reason = "only compilation values" if not prim else f"spread {max(prim)-min(prim):.2f} K > 3 K"
            prov.append([n, name, cid, "", "EXCLUDED", reason, dets]); continue
        tbc = round(T - 273.15, 1)
        data.append([n, name, cid, f"{tbc:.1f}", pairs_s])
        prov.append([n, name, cid, f"{tbc:.1f}", "INCLUDED", rule, dets])
    if any(c > 1 for c in used.values()):
        raise SystemExit("a tree was matched by two NIST entries")
    with open(os.path.join(HERE, "bp_data.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n_C", "name", "nist_id", "T_B_C", "degree_pairs"]); w.writerows(data)
    with open(os.path.join(HERE, "bp_provenance.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n_C", "name", "nist_id", "T_B_C", "status", "rule_or_reason", "all_determinations"]); w.writerows(prov)
    c = Counter((r[0], r[4]) for r in prov)
    for n in range(6, 11):
        print(f"C{n}: trees {len(trees[n])}, NIST skeletons {sum(1 for a in sk if int(a['n'])==n)}, "
              f"included {c[(n,'INCLUDED')]}, excluded {c[(n,'EXCLUDED')]}")
    print("total included", len(data))


if __name__ == "__main__":
    main()
