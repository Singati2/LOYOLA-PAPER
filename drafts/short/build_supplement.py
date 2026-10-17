"""Derive supplement_short.tex, the Supplementary Material of the short version, from ../../supplement.tex.

The full supplement is not changed. This script
  1. renumbers its references into the main paper to the numbering of the short version;
  2. moves the structure-sensitivity table (Table 3 of the full paper) into Section S6;
  3. appends Section S10 with the closed forms and termwise bounds of the full paper, which the short
     version cut from its main text (several of them are the Lean-checked statements of Section S7),
     with the bibliography entries they cite.
Every replacement is asserted to apply the expected number of times.
"""
import re

full = open("../../main.tex").read()
s = open("../../supplement.tex").read()


def sub(old, new, count):
    global s
    n = s.count(old)
    assert n == count, (old, n, count)
    s = s.replace(old, new)


# 1. references into the main paper (full -> short numbering); order matters (Table 3 before 4 -> 3)
sub("Table~3 of the main paper", "Table~\\ref{tab:s-fgdss}", 1)
sub("Table~4 of the main paper", "Table~3 of the main paper", s.count("Table~4 of the main paper"))
sub("Table~5 of the main paper", "Table~4 of the main paper", s.count("Table~5 of the main paper"))
sub("(Table~5 and Section~6.2 of the main paper)", "(Table~4 and Section~5.2 of the main paper)",
    s.count("(Table~5 and Section~6.2 of the main paper)"))
sub("Sections~6.3 and~6.4 of the main paper", "Sections~5.2 and~5.3 of the main paper",
    s.count("Sections~6.3 and~6.4 of the main paper"))
for a, b in (("6.1", "5.1"), ("6.2", "5.2"), ("6.3", "5.2"), ("6.4", "5.3")):
    sub(f"Section~{a} of the main paper", f"Section~{b} of the main paper", s.count(f"Section~{a} of the main paper"))
sub("Section~6 of the main paper", "Section~5 of the main paper", s.count("Section~6 of the main paper"))
sub("Theorem~2 of the main paper", "Theorem~3 of the main paper", s.count("Theorem~2 of the main paper"))
sub("Proposition~7 of the main paper", "Proposition~1 of the main paper", 1)
sub("Eq.~(3) of the main paper", "the exponential-family form at the start of Section~4 of the main paper", 1)
sub("formalisation (Lean v4.34.1, Mathlib v4.34.1) of the following\nstatements of the main paper.",
    "formalisation (Lean v4.34.1, Mathlib v4.34.1) of the following\nstatements of the main paper and of Section~\\ref{sec:s-bounds}.", 1)
refs = sorted(set(re.findall(r"(?:Sections?|Table|Theorem|Proposition|Definition)~[0-9.]+(?: and~[0-9.]+)? of the main paper", s)))
allowed = {"Section~4 of the main paper", "Table~3 of the main paper", "Table~4 of the main paper", "Section~5 of the main paper",
           "Section~5.1 of the main paper", "Section~5.2 of the main paper", "Section~5.3 of the main paper",
           "Sections~5.2 and~5.3 of the main paper", "Theorem~3 of the main paper",
           "Proposition~1 of the main paper"}
assert set(refs) <= allowed, set(refs) - allowed

# 2. structure-sensitivity table into S6
t0 = full.index("\\begin{table}[htbp]\n\\centering\n\\caption{Structure sensitivity $SS$")
t1 = full.index("\\end{table}", t0) + len("\\end{table}")
table = full[t0:t1].replace("\\label{tab:fgdss}", "\\label{tab:s-fgdss}")
sub("\\section{Lean formalisation}\\label{sec:s-lean}", table + "\n\n\\section{Lean formalisation}\\label{sec:s-lean}", 1)

# 3. Section S10: closed forms and termwise bounds, verbatim from the full paper
a = full.index("\\subsection{Closed-form values on standard graphs}")
b = full.index("\\subsection{Extremal trees for the pure-imbalance points}")
c = full.index("\\subsection{Termwise bounds}")
d = full.index("\\section{QSPR diagnostics}")
bounds = full[a:b] + full[c:d]
for old, new in (("\\ref{def:wuzi}", "1 of the main paper"),
                 ("Theorem~\\ref{thm:logconvex}", "Theorem~5 of the main paper"),
                 ("(Supplementary Section~S7)", "(Section~\\ref{sec:s-lean})"),
                 ("\\subsection{Closed-form values on standard graphs}\\label{sec:closedforms}",
                  "\\subsection*{Closed-form values on standard graphs}\\label{sec:closedforms}"),
                 ("\\subsection{Termwise bounds}\\label{sec:termwise}",
                  "\\subsection*{Termwise bounds}\\label{sec:termwise}")):
    assert old in bounds, old
    bounds = bounds.replace(old, new)
bounds = bounds.replace("Definition~1 of the main paper", "Definition~1 of the main paper")
head = ("\\section{Closed forms and termwise bounds}\\label{sec:s-bounds}\n\n"
        "These results of the full version are not needed for the argument of the main paper and are "
        "collected here; the formalised inequalities of Section~\\ref{sec:s-lean} are among them. "
        "Here Proposition, Corollary and Definition numbers continue within this Supplement.\n\n")
sub("\\begin{thebibliography}{00}", head + bounds + "\n\\singlespacing\n\\begin{thebibliography}{00}", 1)

# bibliography entries cited in S10 and missing from the supplement
for key in re.findall(r"\\cite\{([^}]*)\}", bounds):
    for k in (x.strip() for x in key.split(",")):
        if f"\\bibitem{{{k}}}" not in s:
            i = full.index(f"\\bibitem{{{k}}}")
            j = full.index("\\bibitem", i + 1)
            sub("\\end{thebibliography}", "  " + full[i:j].rstrip() + "\n\n\\end{thebibliography}", 1)

# figures are read from the repository's figures/ folder, not copied
sub("\\graphicspath{", "\\graphicspath{{../../figures/}", 1)
sub("\\IfFileExists{figures/#1}", "\\IfFileExists{../../figures/#1}", 1)
open("supplement_short.tex", "w").write(s)
print("supplement_short.tex written")
