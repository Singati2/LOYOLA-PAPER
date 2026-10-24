"""Flag registry entries whose captured value lies in a bibliography, URL/DOI/arXiv fragment,
label/ref, or inside a degree-pair tuple. Run from the repository root."""
import re, sys
sys.path.insert(0, '.')
import prose_claims_a as A, prose_claims_b as B
files = {"main": open("main.tex").read(), "supp": open("supplement.tex").read()}
entries = [e for mod in (A, B) for e in getattr(mod, [n for n in dir(mod) if n.isupper() and isinstance(getattr(mod, n), list) and getattr(mod, n) and isinstance(getattr(mod, n)[0], dict) and "pattern" in getattr(mod, n)[0]][0])]
print("entries", len(entries))
flags = []
for e in entries:
    if e["file"] not in files: continue
    t = files[e["file"]]; ms = list(re.finditer(e["pattern"], t))
    if len(ms) != 1: flags.append((e["id"], "match count %d" % len(ms))); continue
    m = ms[0]
    if "v" not in m.re.groupindex: continue
    s, en = m.span("v")
    bib = t.find("\\begin{thebibliography}")
    ctx = t[max(0, s - 60): en + 30]
    reasons = []
    if bib != -1 and s > bib: reasons.append("in bibliography")
    if re.search(r"(doi\.org/|arXiv:|\\url\{|https?://)[^\s}]*$", t[max(0, s - 80):s]): reasons.append("in URL/DOI")
    if re.search(r"\\(label|ref|cite)\{[^}]*$", t[max(0, s - 40):s]): reasons.append("in label/ref/cite")
    if re.search(r"\(\d+,$", t[max(0, s - 6):s]) or re.match(r",\d+\)", t[en:en + 6]): reasons.append("inside degree pair")
    if reasons: flags.append((e["id"], "; ".join(reasons) + " | " + ctx.replace("\n", " ")))
for f in flags: print(f)
print("flagged", len(flags))
