#!/usr/bin/env python3
"""Write the numbered Colab notebooks of this folder (run after editing STAGES in pipeline.py).

  python colab/make_notebooks.py
"""
import os, sys
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pipeline import STAGES  # noqa: E402

REVISION = "revision/v40.31-scientific"
REPO_URL = "https://github.com/Singati2/LOYOLA-PAPER.git"

SETUP = f'''# Setup (the same cell in every notebook of colab/; about 2 minutes the first time in a session)
REVISION = "{REVISION}"   # the branch or tag to run; every notebook of one run must use the same commit
REPO_URL = "{REPO_URL}"
import os, sys, shutil, subprocess
IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")             # progress and outputs are kept in MyDrive/LOYOLA_colab_run
    WORK = "/content/LOYOLA-PAPER"
    if not os.path.exists(WORK):
        token = None
        try:
            from google.colab import userdata
            token = userdata.get("GITHUB_TOKEN")  # Colab secret (key icon on the left), needed while the repository is private
        except Exception:
            pass
        bundle = "/content/drive/MyDrive/LOYOLA-PAPER.bundle"
        if token:
            url = REPO_URL.replace("https://", "https://x-access-token:" + token + "@")
            subprocess.run(["git", "clone", "--quiet", "--branch", REVISION, url, WORK], check=True)
            subprocess.run(["git", "-C", WORK, "remote", "set-url", "origin", REPO_URL], check=True)   # token not kept on disk
        elif os.path.exists(bundle):
            subprocess.run(["git", "clone", "--quiet", "--branch", REVISION, bundle, WORK], check=True)
        else:
            subprocess.run(["git", "clone", "--quiet", "--branch", REVISION, REPO_URL, WORK], check=True)
    os.chdir(WORK)
    ENV = "/content/loyola-env"
else:                                         # run locally from inside the repository
    while not os.path.exists("verify.py") and os.getcwd() != "/":
        os.chdir("..")
    ENV = os.path.join(os.getcwd(), ".venv-colab")
PY = os.path.join(ENV, "bin", "python")
if not os.path.exists(PY):                    # Python 3.13 and the pinned versions that produced the committed outputs
    if shutil.which("uv") is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "uv"], check=True)
    UV = ["uv"] if shutil.which("uv") else [sys.executable, "-m", "uv"]
    subprocess.run(UV + ["venv", "--quiet", "--python", "3.13", ENV], check=True)
    subprocess.run(UV + ["pip", "install", "--quiet", "--python", PY, "-r", "requirements-lock.txt",
                         "-r", "requirements-extras-lock.txt"], check=True)
print(subprocess.run([PY, "-c", "import sys, numpy, scipy; print('python', sys.version.split()[0], '| numpy', "
                      "numpy.__version__, '| scipy', scipy.__version__)"], capture_output=True, text=True).stdout.strip())
print("commit", subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
STATE = os.environ.get("LOYOLA_STATE") or ("/content/drive/MyDrive/LOYOLA_colab_run" if IN_COLAB
                                           else os.path.join(os.getcwd(), "colab_run"))   # as in pipeline.py


def pipeline(*args):
    """Run colab/pipeline.py with the pinned Python, show its output as it comes, stop on failure."""
    p = subprocess.Popen([PY, "-u", "colab/pipeline.py", *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in p.stdout:
        print(line, end="")
    if p.wait() != 0:
        raise RuntimeError("pipeline.py " + " ".join(args) + " reported a problem (see the output above)")
'''

NIST_MD = ("## Retrieve the NIST WebBook pages (explicit step)\n\n"
           "The data sets of this stage are rebuilt from 262 pages of the NIST Chemistry WebBook (NIST Standard "
           "Reference Database 69). NIST states that its Standard Reference Data are copyrighted and may not be "
           "reproduced or redistributed without permission (https://www.nist.gov/srd/public-law), so the pages are "
           "not part of the repository and no other cell or notebook downloads them. The next cell retrieves them "
           "from the WebBook for your own use, one request per second (about 5 minutes), and checks each against "
           "the digest of the copy the committed data sets were built from; a changed page stops the run. The pages "
           "are kept in a private Drive folder, `MyDrive/LOYOLA_nist_pages_private`, so that notebooks 04 and 08 "
           "can reuse them without downloading again. That folder is not part of the run record: do not share or "
           "archive it.")
NIST_CELL = '''# explicit, rate-limited retrieval of the NIST WebBook pages (skips pages already in the private folder)
sys.path.insert(0, "colab")
from pipeline import nist_cache
r = subprocess.run([PY, "external/nist_pages.py", "--download", "--cache", nist_cache()])
if r.returncode != 0:
    raise RuntimeError("NIST pages missing or changed since they were archived (see the output above)")'''

RESUME = ("If the session disconnects, open this notebook again and run all cells: finished scripts are "
          "skipped and the run continues with the next one. Keep the browser tab open while it runs.")


def write(name, cells):
    nb = new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["colab"] = {"provenance": []}
    path = os.path.join(HERE, name)
    nbformat.write(nb, path)
    print("wrote", os.path.relpath(path, os.path.dirname(HERE)))


def badge(name, revision=REVISION):
    return (f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
            f"(https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/{revision}/colab/{name})")


# Notebook 12 runs the independent enumeration certificates of audit/certificates/. They exist only on the
# review branch so far; set CERT_REVISION to REVISION once that branch is merged.
CERT_REVISION = "review/short-version"
CERT_SETUP = f'''# Setup: fetch the revision and install networkx at the version that produced the committed outputs
REVISION = "{CERT_REVISION}"   # a branch or tag that contains audit/certificates/
import os, sys, subprocess
if not os.path.exists("minimal.py"):
    while not os.path.exists("verify.py") and os.getcwd() != "/":   # inside a local checkout: go to its top folder
        os.chdir("..")
    if not os.path.exists("verify.py"):                             # on Colab: clone the revision
        os.chdir("/content" if os.path.isdir("/content") else os.path.expanduser("~"))
        if not os.path.exists("LOYOLA-PAPER"):
            subprocess.run(["git", "clone", "--quiet", "--depth", "1", "--branch", REVISION,
                            "{REPO_URL}"], check=True)
        os.chdir("LOYOLA-PAPER")
    os.chdir("audit/certificates")
if "google.colab" in sys.modules:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "networkx==3.6.1"], check=True)
import networkx
print("python", sys.version.split()[0], "| networkx", networkx.__version__)
print("commit", subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())'''
CERT_RUN = '''def run(*args):
    """Run one certificate script, print its last line, return its full output."""
    out = subprocess.run([sys.executable, *args], capture_output=True, text=True, check=True).stdout
    print(args[0], "->", out.strip().splitlines()[-1])
    return out

a = run("minimal.py", "17")
assert a.strip().splitlines()[-1] == "{'all': 13, 'chem': 16}"
b = run("by_delta.py", "18")
assert "'4': 16, '5': 16" in b and "'None': 13" in b and "'3'" not in b.splitlines()[-1]
c = run("ratio_indices.py")
assert "('SDD', 'chem'): 9" in c and "('ISDD', 'chem'): 10" in c
d = run("witnesses.py")
assert d.count("OK for every order") == 2
print("ALL CERTIFICATES REPRODUCED")'''


def main():
    total = sum(m for s in STAGES for _, m in s[3])
    write("00_setup_and_plan.ipynb", [
        new_markdown_cell(f"# 0. Setup and plan of the full run\n\n{badge('00_setup_and_plan.ipynb')}\n\n"
                          "Run the notebooks of this folder in their numbered order, each in its own Colab session. "
                          "This one checks the setup and prints the plan. Notebooks 01 to 08 run every script of the "
                          f"paper (about {total // 60} hours on the lab machine, most of it in notebooks 02, 04, 05 and 07), "
                          "09 and 10 are optional (Lean proofs, compiled PDFs), and 11 compares every output with the commit.\n\n"
                          "While the repository is private, either add a Colab secret `GITHUB_TOKEN` (a GitHub token with "
                          "read access to the repository) or put `LOYOLA-PAPER.bundle` (made with "
                          "`git bundle create LOYOLA-PAPER.bundle --all`) in the top folder of your Google Drive."),
        new_code_cell(SETUP),
        new_code_cell('pipeline("--list")'),
    ])
    for n, name, title, scripts in STAGES:
        mins = sum(m for _, m in scripts)
        listing = "\n".join(f"{i}. `{s}` (lab: {m} min)" for i, (s, m) in enumerate(scripts, 1))
        nist = [new_markdown_cell(NIST_MD), new_code_cell(NIST_CELL)] if n == 1 else []
        write(f"{n:02d}_{name}.ipynb", [
            new_markdown_cell(f"# {n}. {title}\n\n{badge(f'{n:02d}_{name}.ipynb')}\n\n"
                              f"Runs these scripts in this order (about {mins} minutes on the lab machine):\n\n{listing}\n\n"
                              f"Each script rewrites its committed output files; notebook 11 compares them with the commit. "
                              f"{RESUME}"),
            new_code_cell(SETUP),
            *nist,
            new_code_cell(f'pipeline("--stage", "{n}")'),
        ])
    write("09_lean_proofs.ipynb", [
        new_markdown_cell(f"# 9. Lean proofs (optional)\n\n{badge('09_lean_proofs.ipynb')}\n\n"
                          "Installs the Lean toolchain named in `formal/lean-toolchain`, builds the formalisation and checks "
                          "that every listed theorem uses only the standard axioms (`formal/verify.sh`). The first build "
                          "downloads Mathlib (about 5 GB) and takes 10 to 30 minutes."),
        new_code_cell(SETUP),
        new_code_cell('''subprocess.run("curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh"
               " | sh -s -- -y --default-toolchain none", shell=True, check=True)
r = subprocess.run(["bash", "formal/verify.sh"], capture_output=True, text=True)
print(r.stdout[-6000:], r.stderr[-3000:])
state = STATE
os.makedirs(state, exist_ok=True)
open(os.path.join(state, "lean_verify.log"), "w").write(r.stdout + r.stderr)
if r.returncode != 0:
    raise RuntimeError("formal/verify.sh failed")'''),
    ])
    write("10_compile_paper.ipynb", [
        new_markdown_cell(f"# 10. Compile the paper and the supplement (optional)\n\n{badge('10_compile_paper.ipynb')}\n\n"
                          "Installs TeX Live (about 5 minutes), compiles both documents with pdflatex, the engine the MATCH "
                          "template names, and runs the label and cross-reference check. The PDFs are copied to the state "
                          "folder. Their bytes depend on the TeX installation, so they are not compared with the committed PDFs."),
        new_code_cell(SETUP),
        new_code_cell('''subprocess.run("apt-get -qq update && apt-get -qq install -y texlive-latex-recommended texlive-latex-extra "
               "texlive-fonts-recommended lmodern > /dev/null", shell=True, check=True)
import tempfile
build = tempfile.mkdtemp()
for f in ("main.tex", "supplement.tex"):
    shutil.copy(f, build)
shutil.copytree("figures", os.path.join(build, "figures"))
for doc in ("main", "supplement"):
    for _ in range(3):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", doc + ".tex"], cwd=build,
                           capture_output=True, text=True, errors="replace")   # TeX logs are not UTF-8
    print(doc, "exit", r.returncode, "|", r.stdout.strip().splitlines()[-1])
    if r.returncode != 0:
        raise RuntimeError(doc + ".tex did not compile")
state = STATE
os.makedirs(os.path.join(state, "paper"), exist_ok=True)
for doc, out in (("main", "LOYOLA_paper.pdf"), ("supplement", "LOYOLA_supplement.pdf")):
    shutil.copy(os.path.join(build, doc + ".pdf"), os.path.join(state, "paper", out))
r = subprocess.run([PY, "audit/check_labels.py"], capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-1500:])
if r.returncode != 0:
    raise RuntimeError("label and reference check failed")'''),
    ])
    write("12_enumeration_certificates.ipynb", [
        new_markdown_cell(f"# 12. Enumeration certificates (independent, about 2 minutes)\n\n"
                          f"{badge('12_enumeration_certificates.ipynb', CERT_REVISION)}\n\n"
                          "Re-runs the four scripts of `audit/certificates/`, written independently of the repository's "
                          "verifiers: the minimal orders 13 (all trees) and 16 (maximum degree at most 4) at which distinct "
                          "degree-pair profiles share a degree-ratio histogram, the first order for each bound on the maximum "
                          "degree, the first orders at which SDD and ISDD merge distinct profiles (9 and 10), and the witness "
                          "trees with the pendant-path construction. Exact rational arithmetic; only `networkx` is needed. "
                          "No NIST data are used, and no Drive folder or state folder is involved, so this notebook can be "
                          "run on its own, in any order."),
        new_code_cell(CERT_SETUP),
        new_code_cell(CERT_RUN),
    ])
    write("11_final_report.ipynb", [
        new_markdown_cell(f"# 11. Final report\n\n{badge('11_final_report.ipynb')}\n\n"
                          "Restores every output of notebooks 01 to 08 from the state folder and compares each with the "
                          "committed file (PDFs by canonical form). Lists every script as OK, PROBLEM or NOT RUN, and every "
                          "output that differs. The report is saved as `FINAL_REPORT.md` in the state folder."),
        new_code_cell(SETUP),
        new_code_cell('''try:
    pipeline("--report")
finally:
    from IPython.display import Markdown, display
    state = STATE
    if os.path.exists(os.path.join(state, "FINAL_REPORT.md")):
        display(Markdown(open(os.path.join(state, "FINAL_REPORT.md")).read()))'''),
    ])


if __name__ == "__main__":
    main()
