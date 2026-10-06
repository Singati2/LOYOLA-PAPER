#!/usr/bin/env python3
"""Check every registered numeral in the running prose of main.tex and
supplement.tex against the canonical files it comes from.

The eight numeric tables are guarded by verify_loyola_v35.py and
external/verify_external.py; this script covers the numerals in running text
(abstract, sections, captions, footnotes, appendix), which earlier revisions
showed could go stale after a data change.  The registries hold one entry per
number: a regular expression anchored on the surrounding text with one named
group (?P<v>...) capturing the number as written, an expression that
recomputes the number from the committed CSV/output files (never from the
tex), and the tolerance implied by the displayed rounding.

  prose_claims_a.py  abstract, Section 6, Conclusion, Appendix A.1,
                     Supplementary S1/S3/S4   (417 entries)
  prose_claims_b.py  Sections 1-5, Reproducibility paragraph, Appendix A,
                     Supplementary S5/S6/S7   (318 entries)

Entries whose number has no machine source (cited published values, reference
temperatures, confidence levels) are listed as UNCHECKABLE and reported, not
tested.  Exit status 0 iff every pattern matches its file exactly once and
every captured value agrees with its recomputed value.  Runtime: seconds.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import prose_claims_a as A
import prose_claims_b as B


def main():
    bad = 0; checked = 0; unch = 0
    n, nc, nm, mism, patt = A.check(verbose=False)
    checked += nc; unch += n - nc; bad += len(mism) + len(patt)
    for pid, cnt in patt:
        print(f"[FAIL] A:{pid}: pattern matched {cnt} times")
    for pid, got, exp, note in mism:
        print(f"[FAIL] A:{pid}: tex says {got!r}, source gives {exp!r}; {note}")
    print(f"registry A: {n} entries, {nc} checkable, {nm} match, {len(mism)} mismatch, {len(patt)} pattern problems, {n - nc} uncheckable")
    res = B.evaluate()
    okb = sum(r["status"] == "OK" for r in res); unb = sum(r["status"] == "UNCHECKABLE" for r in res)
    badb = [r for r in res if r["status"] not in ("OK", "UNCHECKABLE")]
    for r in badb:
        print(f"[FAIL] B:{r['id']}: {r['status']} tex={r.get('tex')!r} expected={r.get('expected')!r} {r.get('error', '')}")
    checked += len(res) - unb; unch += unb; bad += len(badb)
    print(f"registry B: {len(res)} entries, {len(res) - unb} checkable, {okb} match, {len(badb)} problems, {unb} uncheckable")
    print(f"prose numbers: {checked} checked, {bad} failures, {unch} uncheckable (cited values; see UNCHECKABLE in the registries)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
