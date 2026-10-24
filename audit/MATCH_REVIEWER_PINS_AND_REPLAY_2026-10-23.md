# Reviewer pins and replay, 2026-10-23

## Pins

| | SHA | What it contains |
|---|---|---|
| **SOURCE_COMMIT** | `e3fc8810c066420354c96eb8c38a0b9190dfa663` | All manuscript, registry and layout fixes of this branch, with rebuilt PDFs, zips and manifests. Its ancestry includes the replay-harness hardening `69b9538` ("fail closed on missing, empty or unlisted outputs and on forged or corrupted state") |
| **NOTEBOOK_COMMIT** | `e90b5bfcb1a46937cb4f20a6b3420007b69caad1` | Only `colab/*.ipynb` (13), `notebooks/*.ipynb` (6) and `SHA256SUMS.txt`. They were regenerated with `python colab/make_notebooks.py --pin <SOURCE> --revision review/match-final-four-fixes-2026-10-23` and `python notebooks/gen_notebooks.py notebooks --pin <SOURCE> --revision review/match-final-four-fixes-2026-10-23`. The diff touches only `PIN`, `REVISION` and badge lines |
| Docs commit | branch head | `README.md`, `REVIEWER_START_HERE.md`, `COLAB_FOR_REVIEWERS.md`, `colab/README.md`, the dated notes in `docs/match/08–10`, and the reports |

The two pins are separate commits because a commit cannot contain its own SHA.

**Where the pins appear:**
- Docs name source `e3fc881` for checkout, and open the notebooks at `e90b5bf`: 6 links each in `README.md` and `REVIEWER_START_HERE.md`, 7 in `COLAB_FOR_REVIEWERS.md`.
- No `c48bad0` or `afafe6c` remains in these four files or in any notebook.
- Historical audit logs that name old commits were left unchanged.

## Safeguards in the setup cells

These were read from the generators and are unchanged:

| Safeguard | Behaviour |
|---|---|
| Stale or wrong checkout | `notebooks/`: if HEAD ≠ PIN or the tracked files are dirty, raise `REVISION MISMATCH` unless `LOYOLA_ALLOW_MISMATCH=1`, which prints a warning. `colab/`: `at_pin()` checks an existing checkout and moves it to PIN only if it is clean |
| Dependencies | On Colab, pip installs from `requirements-lock.txt` (plus pandas from the extras lock). Version mismatches, and modules already imported at other versions, raise errors |
| Replay state (`colab/pipeline.py`, from `69b9538`) | Fails closed on missing, empty or unlisted outputs and on forged or corrupted state |
| Token | Optional Colab secret `GITHUB_TOKEN`, passed as an `http.extraHeader` through the environment and never placed in the URL. `git_net` redacts the token and the Basic-auth string from errors. No real token is in any tracked file; the only token-like string is the dummy test marker `ghp_DUMMYMARKER…` in `audit/test_corrections_2026_10_19.py`, which checks the redaction |

## Tests run

| Test | Command | Result |
|---|---|---|
| Fresh clone at SOURCE | `git clone --no-local <branch> clone && git checkout --detach e3fc881`; the tree was clean | OK |
| Notebook 01 | `jupyter nbconvert --execute` of the `e90b5bf` copy of `notebooks/01_data.ipynb`, run from `clone/nbtest/` with the locked venv first on `PATH` | exit 0; "commit e3fc881…; pinned commit e3fc881…"; **9 checks, 0 mismatches** |
| Notebook 02 | same, `notebooks/02_mathematics.ipynb` | exit 0; "Mathematics interval checks PASS"; **20 checks, 0 mismatches** |
| Negative control | the same notebook with the clone checked out at `e90b5bf` (HEAD ≠ PIN) | exit 1, `REVISION MISMATCH` |
| Replay contract | `python audit/test_replay_contract_2026_10_21.py` on the notebook commit's tree | exit 0 |

**Environment note.** The first notebook attempt failed one check with exit 127. The notebook calls `python DATA/build_data.py`, and the test shell had no `python` on `PATH`. With the venv on `PATH` it passed. Colab provides `python`, so this was a property of the test harness, not of the notebook.

## Not run

- **Real Google Colab: NOT RUN.** A local `nbconvert` execution does not equal a real Colab run.
- **Public link check: NOT POSSIBLE YET.** The branch is local, so the `blob/e90b5bf…` and `--branch review/match-final-four-fixes-2026-10-23` links resolve only after an authorized push.
- Notebooks 03–06 and colab/00–12 were not executed. Notebook 06 runs `verify.py --offline`, which was run directly on the source commit (ALL PASS).
- No tag, GitHub release, Zenodo deposit or DOI was created or cited.

## Before review

1. Push the branch, with author approval.
2. Open each link in `COLAB_FOR_REVIEWERS.md` to confirm it resolves to `e90b5bf`.
3. Run at least `notebooks/01_data` and `colab/12_enumeration_certificates` in real Colab.
4. Once a release or DOI exists, regenerate the pins against it.
