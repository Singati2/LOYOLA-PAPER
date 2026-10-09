#!/usr/bin/env python3
"""Label, reference, figure and table consistency of main.tex and supplement.tex.

Checks (each must hold):
  1. every \\ref/\\eqref in a document resolves to a \\label in the same document,
     and every \\label is unique;
  2. every table/figure environment has exactly one \\caption and one \\label,
     and every table/figure label is referenced at least once in its document;
  3. every \\cite key has a \\bibitem in the same document, and every \\bibitem
     is cited;
  4. the supplement's cross-document references ("Table~N of the main paper",
     "Theorem~N/Proposition~N/Lemma~N of the main paper", "Section~N.M of the
     main paper") point at numbers the compiled main paper actually assigns
     (read from the PDF produced by tectonic in a temporary copy), and each
     "Table~N of the main paper" is checked against the caption keyword the
     supplement's sentence names, when it names one (TABLE_WORDS below);
  5. figure files referenced by \\includegraphics / \\safefig exist under
     figures/ in every Overleaf bundle.
Exit 0 iff all checks pass.  Runtime: about one minute (one compile).
"""
import os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad = 0
# words a supplement sentence uses near "Table~N of the main paper" -> a word its caption must contain
TABLE_WORDS = {"correlation": "correlation", "search box": "search box", "structure sensitivity": "structure sensitivity"}


def fail(msg):
    global bad
    bad += 1; print("[FAIL]", msg)


def strip_comments(t):
    return re.sub(r"(?<!\\)%.*", "", t)


def doc_checks(name):
    t = strip_comments(open(os.path.join(ROOT, name)).read())
    labels = re.findall(r"\\label\{([^}]*)\}", t)
    dup = {l for l in labels if labels.count(l) > 1}
    for l in sorted(dup):
        fail(f"{name}: duplicate label {l}")
    refs = re.findall(r"\\(?:eq)?ref\{([^}]*)\}", t)
    for r in sorted(set(refs)):
        if r not in labels:
            fail(f"{name}: \\ref{{{r}}} has no label")
    for env in ("table", "figure"):
        for m in re.finditer(r"\\begin\{%s\}(.*?)\\end\{%s\}" % (env, env), t, re.S):
            body = m.group(1); caps = len(re.findall(r"\\caption", body)); labs = re.findall(r"\\label\{([^}]*)\}", body)
            if caps != 1 or len(labs) != 1:
                fail(f"{name}: a {env} environment has {caps} caption(s) and {len(labs)} label(s)")
            elif labs[0] not in refs:
                fail(f"{name}: {env} {labs[0]} is never referenced")
    cites = {k.strip() for c in re.findall(r"\\cite\{([^}]*)\}", t) for k in c.split(",")}
    bibs = re.findall(r"\\bibitem\{([^}]*)\}", t)
    for k in sorted(cites - set(bibs)):
        fail(f"{name}: \\cite{{{k}}} has no bibitem")
    for k in sorted(set(bibs) - cites):
        fail(f"{name}: bibitem {k} is never cited")
    figs = [f for f in re.findall(r"\\(?:includegraphics|safefig)(?:\[[^\]]*\])?\{([^}]*)\}", t) if "#" not in f]
    return figs


def compiled_numbers():
    tmp = tempfile.mkdtemp(prefix="loyola_labels_")
    shutil.copy(os.path.join(ROOT, "main.tex"), tmp); shutil.copytree(os.path.join(ROOT, "figures"), os.path.join(tmp, "figures"))
    r = subprocess.run(["tectonic", "-k", "main.tex"], cwd=tmp, capture_output=True, text=True)
    if r.returncode != 0:
        fail("main.tex does not compile"); return {}, {}
    import fitz
    txt = "".join(p.get_text() for p in fitz.open(os.path.join(tmp, "main.pdf")))
    # theorem-type numbering follows source order (shared counter for theorem/proposition/corollary when the
    # corollary environment is numbered; lemma has its own counter), so it is read from main.tex, not harvested
    # from the PDF text, where in-text references such as "Theorem 2(ii)" would be mistaken for headings
    src = strip_comments(open(os.path.join(ROOT, "main.tex")).read()); body_src = src[src.find(r"\begin{document}"):]
    # v40.23: one counter shared by every \newtheorem{...}[theorem] environment, reset at each \section
    # (\newtheorem{theorem}{Theorem}[section]), so numbers read "3.4"
    shared = set(re.findall(r"\\newtheorem\{(\w+)\}\[theorem\]", src)) | {"theorem"}
    results = {}; sec = 0; k = 0
    for m_ in re.finditer(r"\\section\{|\\begin\{(\w+)\}(?:\[([^\]]*)\])?", body_src):
        if m_.group(0).startswith("\\section"):
            sec += 1; k = 0; continue
        env, title = m_.group(1), (m_.group(2) or "").strip()
        if env not in shared:
            continue
        k += 1
        results[(env.capitalize(), f"{sec}.{k}")] = title or "(untitled)"
    pdf_heads = set(re.findall(r"\n(Theorem|Proposition|Lemma)\s+(\d+\.\d+)\s*[.(]", txt))   # PyMuPDF may break a justified line at every word
    for (kind, n), title in results.items():
        if kind in ("Theorem", "Proposition", "Lemma") and (kind, n) not in pdf_heads:
            fail(f"{kind} {n} ({title[:30]}) numbered in the source but not found as a heading in the compiled paper")
    shutil.rmtree(tmp, ignore_errors=True)
    # table and section numbers follow source order, so they are read from main.tex itself
    src = strip_comments(open(os.path.join(ROOT, "main.tex")).read())
    tables = {i + 1: re.search(r"\\caption\{(.{0,80})", body).group(1)
              for i, body in enumerate(re.findall(r"\\begin\{table\}(.*?)\\end\{table\}", src, re.S))}
    sections, n_sec, n_sub = set(), 0, 0
    for kind in re.findall(r"\\(section|subsection)\{", src[src.find(r"\begin{document}"):]):
        if kind == "section":
            n_sec, n_sub = n_sec + 1, 0; sections.add(str(n_sec))
        else:
            n_sub += 1; sections.add(f"{n_sec}.{n_sub}")
    pdf_tables = {int(n) for n in re.findall(r"\nTable (\d+)\. ", txt)}
    if set(tables) - pdf_tables:
        fail(f"tables numbered in the source but absent from the compiled paper: {sorted(set(tables) - pdf_tables)}")
    return results, tables, sections


def main():
    figs_main = doc_checks("main.tex"); figs_supp = doc_checks("supplement.tex")
    results, tables, sections = compiled_numbers()
    su = re.sub(r"\s+", " ", strip_comments(open(os.path.join(ROOT, "supplement.tex")).read()))
    for m in re.finditer(r"Sections?~(\d(?:\.\d)?)(?:(?:,| and)~(\d(?:\.\d)?))*(?: and Table~\d+)? of the main paper", su):
      for n in re.findall(r"\d(?:\.\d)?", m.group(0)):
        if n not in sections:
            fail(f"supplement cites Section~{n} of the main paper, which the compiled main paper does not number so")
    for m in re.finditer(r"Table~(\d+) of the main paper|main paper, Table~(\d+)", su):
        num = m.group(1) or m.group(2); ctx = su[max(0, m.start() - 100):m.start()].lower()
        found = [(ctx.rfind(word), word) for word in TABLE_WORDS if word in ctx]
        for _, word in sorted(found)[-1:]:                      # the keyword nearest the citation decides
            cap_word = TABLE_WORDS[word]
            if int(num) in tables and cap_word not in tables[int(num)].lower():
                fail(f"supplement cites Table~{num} of the main paper for '{word}' but that table's caption is '{tables[int(num)][:40]}'")
    for kind, n in re.findall(r"(Theorem|Proposition|Lemma|Corollary|Remark)~(\d+(?:\.\d+)?) of the main paper", su):
        if (kind, n) not in results:
            fail(f"supplement cites {kind}~{n} of the main paper, which the compiled main paper does not number so")
    for n in [x or y for x, y in re.findall(r"Table~(\d+) of the main paper|main paper, Table~(\d+)", su)]:
        if int(n) not in tables:
            fail(f"supplement cites Table~{n} of the main paper, not present")
    print("compiled main-paper numbering:", {f"{k[0]} {k[1]}": v[:30] for k, v in sorted(results.items())})
    print("tables:", {k: v[:40] for k, v in sorted(tables.items())}); print("sections:", sorted(sections))
    for bundle, figs in (("LOYOLA_MAIN_OVERLEAF", figs_main), ("LOYOLA_SUPPLEMENT_OVERLEAF", figs_supp), ("LOYOLA_FINAL_PAPER_OVERLEAF", figs_main + figs_supp)):
        for f in figs:
            cands = [f, f + ".pdf"] if not f.endswith(".pdf") else [f]
            if not any(os.path.exists(os.path.join(ROOT, bundle, c)) or os.path.exists(os.path.join(ROOT, bundle, "figures", os.path.basename(c))) for c in cands):
                fail(f"{bundle}: figure {f} missing")
    print("label/reference/figure/table checks:", "PASS" if bad == 0 else f"{bad} FAILURES")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
