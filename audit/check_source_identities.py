#!/usr/bin/env python3
"""Check archived C6-C10 NIST page formulas and carbon skeletons against records."""
import csv
import html
from pathlib import Path
import re
import sys
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'external/bp'))
import build_bp_data as B


def main():
    checked = 0
    with open(ROOT / 'external/bp/nist_alkanes_skeletons_audit.csv', newline='') as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        n = int(row['n'])
        if n not in range(6, 11):
            continue
        expected = B.inchi_tree(row['skel'], n)
        for cid in row['ids'].split():
            page = (ROOT / 'external/bp/nist_raw' / f'{cid}.html').read_text(errors='replace')
            match = re.search(r'<span class="inchi-text">(.*?)</span>', page, re.S)
            if not match:
                raise AssertionError(f'{cid}: missing archived InChI')
            inchi = html.unescape(match.group(1)).strip()
            if not inchi.startswith(f'InChI=1S/C{n}H{2*n+2}/'):
                raise AssertionError(f'{cid}: unexpected molecular formula: {inchi}')
            if not nx.is_isomorphic(expected, B.inchi_tree(inchi, n)):
                raise AssertionError(f'{cid}: carbon skeleton differs from dataset record')
            checked += 1
    if checked != 154:
        raise AssertionError(f'expected 154 archived pages, checked {checked}')
    print(f'Archived source formula/skeleton checks PASS: {checked} pages')


if __name__ == '__main__':
    main()
