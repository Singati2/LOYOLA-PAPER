# Running the whole computation in Google Colab

This folder runs every script in the plan of `pipeline.py` again, from the source records to the final
tables (two independent cross-checks, `audit/permutation_pipeline_audit.py` and
`audit/v4030/uncertain_source_crosscheck.py`, are outside the plan; the final report names them, and their
committed outputs are separate evidence), and checks that each output matches the committed one. Run the notebooks in their
numbered order, each in its own Colab session. Only the order of the computation lives here: the
scripts stay where they are, so the paths used in the paper and in `REPRODUCE.md` stay valid.

| Notebook | What it runs | Lab time |
|---|---|---|
| `00_setup_and_plan.ipynb` | checks the setup, prints the full plan | 2 min |
| `01_build_datasets.ipynb` | nonane, boiling-point and calorimetric data sets from the NIST pages (downloaded, not redistributed); `DATA/` copies; source identities | 5 min |
| `02_mathematics_and_trees.ipynb` | tree enumeration, minimality, exact ties, certificates, Tables 1 and 2 (`structural_checks.py` is most of it) | 2.5 h |
| `03_octane_analyses.ipynb` | octane correlations, ablations, robustness, figures, Tables 3 and 4 (`verify_loyola_v35.py`) | 40 min |
| `04_nonane_vaporisation_enthalpies.ipynb` | baselines, the pre-registered nonane test, transfer, bootstrap, search boxes | 1.7 h |
| `05_boiling_points.ipynb` | pre-registered Tests A and B, coverage bias, Wiener baseline, Table 5, selection-aware resampling | 3.8 h |
| `06_independent_audits.ipynb` | claim provenance ledger, independent re-implementations, leakage probes | 1 h |
| `07_long_audits.ipynb` | the three longest audit scripts | 12 h |
| `08_consistency_checks.ipynb` | exploratory outputs, regression and baseline tests, every number in the prose | 10 min |
| `09_lean_proofs.ipynb` | optional: the Lean 4 proofs | 10-30 min |
| `10_compile_paper.ipynb` | optional: compile both documents with pdflatex; label and reference check | 10 min |
| `11_final_report.ipynb` | compares every rewritten output with the commit; writes `FINAL_REPORT.md` | 2 min |
| `12_enumeration_certificates.ipynb` | separate from the run above: the independent enumeration certificates of `audit/certificates/` (orders 13 and 16, first order by maximum degree, SDD and ISDD, witness trees); no NIST data, no Drive folder; any order | 1 min |

Notebook 12 runs on its own and needs no setup beyond a Colab session. Like every notebook here, it runs
the pinned commit (see below).

Lab times come from one run on the authors' machine with throttled CPU, three scripts at a time, so
they are upper estimates. Notebook 07 is long. If it does not fit in one session, open it again:
the run continues with the next unfinished script.

## Before the first notebook
1. Repository access. While the repository is private, do one of the following:
   * add a Colab secret named `GITHUB_TOKEN` (key icon in Colab's left bar) holding a GitHub token
     with read access to `Singati2/LOYOLA-PAPER`, and allow the notebook to use it. The token reaches
     git only through the environment of the clone or fetch command; it is not put into a URL, a
     command line, an error message, the notebook's variables or `.git/config`; or
   * make a bundle on your computer, `git bundle create LOYOLA-PAPER.bundle --all`, and upload it
     to the top folder of your Google Drive.

   Once the repository is public again, neither is needed.
2. Each notebook asks to mount Google Drive. Progress, logs and outputs are kept in
   `MyDrive/LOYOLA_colab_run`.

## How a run works
* Every notebook starts with the same setup cell. It clones the branch named in `REVISION` and
  checks out the exact commit named in `PIN`; every notebook of the folder names the same commit.
  An existing checkout is moved to that commit if it has no local changes and is rejected if it
  has. Run locally, the cell stops unless the checkout is that commit without local changes. The
  cell then installs, in a Python 3.13 environment, the exact package versions of
  `requirements-lock.txt` and `requirements-extras-lock.txt` (with their dependencies, which the
  lock files do not list): a missing package or one at another version is (re)installed, an
  environment with another Python is rebuilt, and the cell stops unless every locked package is at
  its locked version and `uv pip check` finds no broken dependency. The committed outputs were
  produced with these versions. The notebooks are regenerated with
  `python colab/make_notebooks.py --pin <commit>`.
* Notebook 01 has an explicit cell that retrieves the 262 NIST WebBook pages from the WebBook
  (one request per second, about 5 minutes). NIST SRD 69 is copyrighted, so the pages are not in the
  repository and no other cell downloads them. They are saved in a private Drive folder,
  `MyDrive/LOYOLA_nist_pages_private`, from which notebooks 04 and 08 copy them. Do not share or
  archive that folder. Each page is checked against the digest of the copy the committed data sets
  were built from; a changed page stops the run.
* `colab/pipeline.py` runs the scripts of a stage one after another, each from its own directory.
  Each script runs after every script whose output it reads. This order was checked against a
  trace of the files each script opens. After each script it saves the
  script's log, its exit status and every file it wrote to the state folder, with the SHA-256 of
  each file, the SHA-256 of every output of earlier scripts present when it ran, and a fingerprint
  of the commit, the script, its arguments, the Python version, the installed package versions and
  the lock files. The next notebook restores those files first, so each stage sees the outputs of
  the earlier ones.
* A finished script is skipped only if its fingerprint is unchanged, every output it wrote is
  present and unaltered, and no output of an earlier script has changed since it ran. Otherwise it
  runs again. The runner refuses to run on tracked files that differ from the commit (other than
  restored outputs). State files are written atomically.
* A state folder belongs to one commit. The runner refuses to continue a run with a different
  commit. To start again, delete or rename `MyDrive/LOYOLA_colab_run`.
* Notebook 11 lists every script as OK, PROBLEM, STALE (finished, but its record no longer
  validates: an output is missing or altered, or an input or the environment changed) or NOT RUN. It lists every output that differs
  from the committed file and does not hide floating-point differences. Four outputs already
  differed in their last digits between the authors' macOS run and a Linux run (see
  `verification_logs/lab_09ceba8/NOTE.md`). If they differ again, the report notes it next to the file.

The same runner works on any computer with Python 3.13:
`python colab/pipeline.py --list`, then `--stage 1` to `--stage 8`, then `--report`.

## Keeping the record of a run
Keep the state folder (`logs/`, `files/`, `run.json`, `FINAL_REPORT.md`, and `paper/` and
`lean_verify.log` from notebooks 09 and 10). It records which commit was run, with which Python, and
what each script printed. It can be archived next to the repository, for example on Zenodo. That
archive also contains the rebuilt data sets (extracted values with their sources, as in `DATA/`;
see `DATA/README.md`). It does not contain the NIST WebBook pages: every stage downloads them into
the Colab copy of the repository and they are never saved in the state folder.

To regenerate the notebooks after editing the stage list in `pipeline.py`, run
`python colab/make_notebooks.py`.
