"""Assemble main_short.tex from the MATCH preamble of main.tex, body.tex and the cited bibliography entries."""
import re
src=open("../../main.tex").read()
k=src.index("\\begin{document}"); k=src.index("\\maketitle",k); pre=src[:k+len("\\maketitle")]+"\n"
bib=src[src.index("\\singlespacing\n\n \\begin{thebibliography}"):]
body=open("body.tex").read()
cited=set(k.strip() for m in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]*)\}", body) for k in m.split(","))
pos=[m.start() for m in re.finditer(r"\\bibitem\{", bib)]; end=bib.index("\\end{thebibliography}")
items=[bib[a:b] for a,b in zip(pos,pos[1:]+[end])]
keys=[re.match(r"\\bibitem\{([^}]*)\}",it).group(1) for it in items]
assert not cited-set(keys), cited-set(keys)
keep=[it.rstrip()+"\n\n" for it,k in zip(items,keys) if k in cited]
open("main_short.tex","w").write(pre+body+bib[:pos[0]]+"  "+"  ".join(keep)+bib[end:])
print(f"{len(cited)} cited, {len(keep)} bibliography entries")
