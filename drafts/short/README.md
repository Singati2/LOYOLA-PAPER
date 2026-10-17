# Short version of the manuscript (review draft, not for submission yet)

This folder holds a shorter version of `main.tex`. The full paper (`main.tex`, `LOYOLA_paper.pdf`) and
the Supplement (`supplement.tex`, `LOYOLA_supplement.pdf`) are unchanged.

| File | Content |
|---|---|
| `body.tex` | text of the short version (abstract to acknowledgment) |
| `build.py` | assembles `main_short.tex`: the MATCH preamble and title block of `../../main.tex` (only the `\title` line differs), then `body.tex`, then the bibliography entries of `../../main.tex` that `body.tex` cites |
| `build_supplement.py` | derives `supplement_short.tex` from `../../supplement.tex`: renumbered references into the main paper, the structure-sensitivity table in S6, closed forms and termwise bounds in a new S10 |
| `supplement_short.tex`, `supplement_short.pdf` | Supplementary Material of the short version (generated) |
| `SHORT_VS_FULL_CHANGELOG.md` | section, statement, supplement and claim map between the two versions |
| `main_short.tex` | assembled source (generated; kept so it compiles on its own, e.g. on Overleaf) |
| `main_short.pdf` | compiled draft |
| `NOTES.md` | what was cut, what was restored after review, and what must change before it could replace the full paper |

The short main text uses no figures; the short supplement reads the two figures from `../../figures/`. No data files are used. Every value in it appears in `main.tex` or
`supplement.tex`, which the repository's verifiers check against the computations.

## Build
```bash
cd drafts/short
python3 build.py && python3 build_supplement.py   # regenerate both .tex files
for f in main_short supplement_short; do for i in 1 2 3; do pdflatex -interaction=nonstopmode $f.tex; done; done
```

## Checks
* Every numeric token of `body.tex` occurs in `main.tex` or `supplement.tex`:
  ```bash
  python3 -c "import re;b=open('body.tex').read();f=open('../../main.tex').read()+open('../../supplement.tex').read();print(sorted(n for n in set(re.findall(r'(?<![\w.])[-+]?\d+(?:\.\d+)?(?![\w])',b)) if n not in f))"
  ```
  This prints `[]`.
* The repository's own checks (`verify.py`, `prose_numbers_check.py`, `LEAN_VERIFICATION.md`) are keyed
  to `main.tex` and do not cover this draft.
