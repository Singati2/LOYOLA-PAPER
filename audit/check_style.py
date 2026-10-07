#!/usr/bin/env python3
"""Plain-prose check of main.tex and supplement.tex.

The journal's register is short declarative sentences without rhetorical
flourish.  This script strips LaTeX (preamble, math, tables, figures, the
bibliography, commands) from the document bodies and then fails on

  1. dashes used as punctuation in prose (an em dash ``---'' anywhere, or a
     spaced en dash `` -- ''; en dashes inside compounds such as
     geometric--arithmetic or page ranges are not punctuation);
  2. sentences longer than MAX_WORDS words;
  3. stock phrases of machine-written prose (list TELLS below);
  4. the contrast pattern ``X, not Y'' and ``not X but Y'' used as a punchline.

It also prints sentence-length statistics (mean, standard deviation, share of
sentences over 30 words) for both documents and, when the two reference
MATCH papers are present as text, for those, so the registers can be compared.

  python3 audit/check_style.py            check main.tex and supplement.tex
  python3 audit/check_style.py --stats    statistics only, never fails
Exit 0 iff no finding.  Runtime: under a second.
"""
import glob, os, re, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_WORDS = 45
TELLS = [
    r"\bcrucial(ly)?\b", r"\bnotabl[ey]\b", r"\bimportantly\b", r"\bit is worth noting\b", r"\bworth noting\b",
    r"\bwe (emphasi[sz]e|stress) that\b", r"\bin what follows\b", r"\bwe now turn\b", r"\bthis section collects\b",
    r"\bdelve\b", r"\bleverag(e|es|ing)\b", r"\brobustly\b", r"\bnuanced\b", r"\bunderscor(e|es|ing)\b",
    r"\bhighlight(s|ing)? the\b", r"\bas much [a-z ]+ as\b", r"\bthe content here is\b", r"\bit should be noted\b",
    r"\bserves? as a\b", r"\bplays? a (central|key|crucial) role\b", r"\bin this paper, we\b",
    r"\bremarkabl[ey]\b", r"\bstrikingly\b", r"\bsubstantially\b", r"\bseamless(ly)?\b", r"\bholistic\b",
    r"\bmultifaceted\b", r"\bshed(s)? light\b", r"\bpav(e|es|ing) the way\b", r"\bin a nutshell\b",
]
CONTRAST = [r",\s+not\s+(a|an|the)?\s*[a-z-]+(\s+[a-z-]+){0,3}[.;:]", r"\bnot\s+[a-z-]+(\s+[a-z-]+){0,4}\s+but\s+(rather\s+)?[a-z]"]


def body(tex):
    t = tex[tex.find(r"\begin{document}"):]
    t = t[:t.find(r"\begin{thebibliography}")] if r"\begin{thebibliography}" in t else t
    t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\begin\{cases\}.*?\\end\{cases\}", "", t, flags=re.S)       # may hold $ inside \text{}
    t = re.sub(r"\\(?:text|mbox|textrm)\{[^{}]*\}", " ", t)
    t = re.sub(r"\\(?:texttt|url)\{[^{}]*\}", "CODE", t)
    for env in ("table", "figure", "equation\\*?", "align\\*?", "gather\\*?", "multline\\*?", "tabular", "thebibliography"):
        t = re.sub(r"\\begin\{%s\}.*?\\end\{%s\}" % (env, env), ". ", t, flags=re.S)
    t = re.sub(r"\\\[.*?\\\]", " MATH ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " MATH ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", "MATH", t)
    t = re.sub(r"\\(section|subsection|paragraph|caption)\*?(\[[^\]]*\])?\{[^{}]*\}", ". ", t)
    t = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^\]]*\])?", ". ", t)
    t = re.sub(r"\\item(\[[^\]]*\])?", ". ", t)
    t = re.sub(r"\\(proof|qed|par|noindent|smallskip|medskip|bigskip)\b", ". ", t)
    t = re.sub(r"\\(cite|ref|eqref|label|textbf|textit|emph|url|href)\*?(\[[^\]]*\])?\{[^{}]*\}", "REF", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    t = re.sub(r"[{}]", "", t)
    return t


def sentences(txt):
    txt = re.sub(r"\s+", " ", txt)
    txt = re.sub(r"(\.\s*)+\.", ".", txt)
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z(])", txt)
    return [p.strip() for p in parts if len(re.findall(r"[A-Za-z]{2,}", p)) >= 4]


def dash_findings(txt):
    out = []
    for m in re.finditer(r"---", txt):
        out.append(("em dash", txt[max(0, m.start() - 50):m.end() + 50]))
    for m in re.finditer(r"(?<!-)\s--\s(?!-)", txt):
        out.append(("spaced en dash", txt[max(0, m.start() - 50):m.end() + 50]))
    return out


def stats(sents):
    L = [len(s.split()) for s in sents]
    return dict(n=len(L), mean=statistics.mean(L), sd=statistics.pstdev(L), over30=sum(x > 30 for x in L) / len(L), max=max(L))


def check(name):
    raw = open(os.path.join(ROOT, name)).read()
    txt = body(raw)
    findings = [(name, kind, ctx.replace("\n", " ")) for kind, ctx in dash_findings(txt)]
    sents = sentences(txt)
    for s in sents:
        n = len(s.split())
        if n > MAX_WORDS:
            findings.append((name, f"{n} words", s[:140]))
        for pat in TELLS:
            if re.search(pat, s, re.I):
                findings.append((name, "tell " + pat, s[:140]))
        for pat in CONTRAST:
            if re.search(pat, s):
                findings.append((name, "contrast", s[:140]))
    return findings, stats(sents)


def main():
    only_stats = "--stats" in sys.argv
    allf = []
    for name in ("main.tex", "supplement.tex"):
        f, st = check(name)
        allf += f
        print(f"{name}: {st['n']} sentences, mean {st['mean']:.1f} words, sd {st['sd']:.1f}, {100*st['over30']:.0f}% over 30 words, longest {st['max']}")
    scratch = os.environ.get("MATCH_REF_DIR", "")
    for p in sorted(glob.glob(os.path.join(scratch, "match*.txt"))) if scratch else []:
        t = open(p).read(); t = t[t.find("Introduction"):t.find("References")]
        t = re.sub(r"\n\d+\n", " ", t); t = t.replace("\n", " ")
        st = stats(sentences(t))
        print(f"{os.path.basename(p)}: {st['n']} sentences, mean {st['mean']:.1f} words, sd {st['sd']:.1f}, {100*st['over30']:.0f}% over 30 words, longest {st['max']}")
    if only_stats:
        return
    for name, kind, ctx in allf:
        print(f"[FAIL] {name}: {kind}: ...{ctx}...")
    print("prose style check:", "PASS" if not allf else f"{len(allf)} FINDINGS")
    sys.exit(1 if allf else 0)


if __name__ == "__main__":
    main()
