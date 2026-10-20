#!/usr/bin/env python3
"""Run the whole LOYOLA computation from the beginning to the end, one numbered stage at a time.

Every script of the paper is listed below exactly once, in an order in which each script runs
after every script whose output it reads. Each script runs from its own directory, exactly as
audit/run_all_scripts.py runs it, and rewrites its committed output files in place. The last
stage compares every tracked file with the committed version (PDFs by canonical form).

  python colab/pipeline.py --list            the stages, their scripts and lab running times
  python colab/pipeline.py --stage 3         run stage 3 (finished scripts are skipped)
  python colab/pipeline.py --stage 3 --redo  run stage 3 again from its first script
  python colab/pipeline.py --report          compare every file with the commit; write FINAL_REPORT.md

Progress is kept in a state folder, so a run can stop at any point (a Colab disconnect, a closed
notebook) and continue in a new session: the outputs of finished scripts are copied there after
each script and restored into a fresh copy of the repository before the next stage runs. The
state folder is LOYOLA_STATE if set, else LOYOLA_colab_run in Google Drive when Drive is mounted,
else colab_run/ inside the repository. A state folder belongs to one commit; the runner refuses
to mix results of different commits, and refuses to run on tracked files changed from that commit.

A finished script is skipped only if nothing it depends on has changed. Its record holds a fingerprint
(commit, script file, script arguments, Python and installed package versions, lock files) and the
SHA-256 of every output it wrote and of every output of earlier scripts present when it ran. If the
fingerprint differs, if a saved output is missing or altered, or if an earlier script's output has
changed since (for example after --redo), the script runs again. State files are written atomically.

Stages 1, 4 and 8 read the NIST WebBook pages, which are not redistributed. The runner never
downloads them: notebook 01 has an explicit download cell (external/nist_pages.py --download, one
request per second) that saves them to a private cache folder (LOYOLA_NIST_CACHE, else
LOYOLA_nist_pages_private in Google Drive, else .nist_cache/ in the repository), and those stages
copy them from there. The pages are never copied into the state folder.
"""
import argparse, datetime, hashlib, json, os, platform, shutil, subprocess, sys, tempfile, time
from importlib import metadata

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NIST_DIRS = ("external/bp/nist_raw/", "external/bp/nist_hvap_pts/", "external/nonane_raw_nist/")
# scripts that read the NIST WebBook pages (traced 2026-10-17)
NEEDS_NIST = {"external/build_nonane_data.py", "external/bp/build_bp_data.py", "external/bp/build_calorimetric_set.py",
              "audit/check_source_identities.py", "external/nonane_validation.py", "external/test_regressions.py"}

# (stage number, folder-style name, title, [(script with arguments, lab minutes)])
# The order was checked against a trace of the files each script opens (2026-10-17): every script
# runs after every script whose output it reads.
# Lab minutes: one run on the authors' lab machine (i9-9900K held near 800 MHz by thermal limits,
# three scripts at a time), so most are upper estimates; a Colab CPU is usually faster per core.
STAGES = [
    (1, "build_datasets", "Build the data sets from the NIST source pages", [
        ("external/build_nonane_data.py", 1), ("external/check_nonane_structures.py", 1),
        ("external/bp/build_bp_data.py", 1), ("external/bp/build_calorimetric_set.py", 1),
        ("DATA/build_data.py", 1), ("audit/check_source_identities.py", 1)]),
    (2, "mathematics_and_trees", "Mathematics: tree enumeration, certificates, Tables 1 and 2", [
        ("structural/minimality_check.py", 1), ("structural/extremal_trees_check.py", 1),
        ("structural/sumconn_pair_check.py", 1), ("structural/count_dimension_check.py", 1),
        ("structural/fractional_points.py", 1), ("structural/chi_floor.py", 1),
        ("multi_order_degeneracy.py", 1), ("redundancy_collisions.py", 1), ("audit/check_mathematics.py", 1),
        ("structural/structural_checks.py", 128), ("structural/hp_counts.py", 9),   # hp_counts reads structural_checks_out.txt
        ("structural/exact_ties.py", 1)]),                                          # exact_ties reads hp_counts_out.txt
    (3, "octane_analyses", "Octanes: correlations, ablations, robustness, figures, Tables 3 and 4", [
        ("ablation_gm_vs_lo.py", 1), ("source_sensitivity.py", 1), ("fgd_structure_sensitivity.py", 1),
        ("tmb_dhvap_audit.py", 1), ("tuning_pool_seed_sweep.py", 1), ("generate_loyola_v35_figures.py", 1),
        ("tmb_exclusion_sensitivity.py", 2), ("expanded_robustness_v35.py", 2), ("constancy_test_check.py", 3),
        ("ablation_robustness.py", 13), ("verify_loyola_v35.py", 14)]),
    (4, "nonane_vaporisation_enthalpies", "Nonanes and vaporisation enthalpies: pre-registered test, search boxes", [
        ("external/baselines.py", 5), ("external/baselines.py --dataset nonane", 5),
        ("external/nonane_validation.py", 14), ("external/transfer_exploratory.py", 2),
        ("external/uncertainty_exploratory.py", 14), ("external/wide_box_diagnostics.py", 3),
        ("external/box_sensitivity.py", 45), ("external/nonane_tb_conflict.py", 11),
        ("external/make_box_table.py", 1), ("external/make_v37_table.py", 1)]),
    (5, "boiling_points", "Measured boiling points: pre-registered Tests A and B, Table 5", [
        ("external/bp/coverage_bias.py", 1), ("external/bp/wiener_baseline.py", 1),
        ("external/bp/bp_tests.py", 78), ("external/bp/make_bp_table.py", 1),
        ("external/bp/selection_resampling.py", 145)]),
    (6, "independent_audits", "Independent audit scripts (re-implementations and probes)", [
        ("audit/final/scripts/claim_provenance.py", 1),   # its ledger is read by the v4030 audits below and in stage 7
        ("audit/v4030/math_independent.py", 3), ("audit/v4030/table2_independent.py", 1),
        ("audit/v4030/leakage_probe.py", 4), ("audit/v4030/feature_leakage_probe.py", 4),
        ("audit/v4030/uncertain_source_sensitivity.py", 6), ("audit/final/scripts/counterattack_v4030.py", 5),
        ("audit/final/scripts/bp_duplicate_sensitivity.py", 11), ("audit/v4030/gamma_strict.py", 25)]),
    (7, "long_audits", "The three longest audit scripts (several hours each on the lab machine)", [
        ("audit/final/scripts/press_size_probe.py", 245), ("audit/v4030/refit_stability.py", 245),
        ("audit/v4030/sensitivity_followup.py", 255)]),
    (8, "consistency_checks", "Consistency checks over all outputs: provenance, prose numbers, tests", [
        ("audit/check_exploratory_outputs.py", 1),
        ("external/test_regressions.py", 1), ("external/test_baselines.py", 6),
        ("prose_numbers_check.py", 1)]),
]
# scripts whose exit status is their whole result (they write no tracked file)
CHECK_ONLY = {"external/check_nonane_structures.py", "audit/check_exploratory_outputs.py", "audit/check_source_identities.py",
              "audit/check_mathematics.py", "prose_numbers_check.py", "external/test_regressions.py", "external/test_baselines.py"}
# outputs that already differed in the last digits on the lab replay of 09ceba8 (Linux) from the committed
# outputs (macOS); see verification_logs/lab_09ceba8/NOTE.md. They are still reported as DIFFERS.
SEEN_BEFORE = {
    "external/transfer_exploratory_out.txt": "3 cells differed in the 14th significant digit on the lab replay",
    "external/wide_box_diagnostics_out.txt": "solver-error magnitudes (about 1e-14) differed on the lab replay",
    "audit/final/scripts/counterattack_v4030_out.txt": "error magnitudes of deliberately near-singular designs differed on the lab replay",
    "audit/final/scripts/press_size_probe_out.txt": "differed on the lab replay; the differing line was not identified",
}


def git(*a):
    return subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True).stdout.strip()


def state_dir():
    if os.environ.get("LOYOLA_STATE"):
        d = os.environ["LOYOLA_STATE"]
    elif os.path.isdir("/content/drive/MyDrive"):
        d = "/content/drive/MyDrive/LOYOLA_colab_run"
    else:
        d = os.path.join(REPO, "colab_run")
    os.makedirs(os.path.join(d, "logs"), exist_ok=True); os.makedirs(os.path.join(d, "files"), exist_ok=True)
    return d


def nist_cache():
    """Private folder for the NIST pages retrieved by the user (kept outside the state folder, never archived)."""
    if os.environ.get("LOYOLA_NIST_CACHE"):
        return os.environ["LOYOLA_NIST_CACHE"]
    if os.path.isdir("/content/drive/MyDrive"):
        return "/content/drive/MyDrive/LOYOLA_nist_pages_private"
    return os.path.join(REPO, ".nist_cache")


ORDER = {script: i for i, script in enumerate(s for _, _, _, scripts in STAGES for s, _ in scripts)}
LOCKS = ("requirements-lock.txt", "requirements-extras-lock.txt")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, obj):
    """Write a state file atomically: a crash leaves either the old or the new file, never a partial one."""
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".tmp-")
    with os.fdopen(fd, "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, path)


def copy_atomic(src, dst):
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(dst) or ".", prefix=".tmp-"); os.close(fd)
    shutil.copy2(src, tmp); os.replace(tmp, dst)


def env_fingerprint():
    """Interpreter, platform, every installed package version and the lock files."""
    pkgs = sorted(f"{d.metadata['Name']}=={d.version}".lower() for d in metadata.distributions() if d.metadata["Name"])
    locks = {f: (sha256(os.path.join(REPO, f)) if os.path.exists(os.path.join(REPO, f)) else None) for f in LOCKS}
    return dict(python=platform.python_version(), implementation=platform.python_implementation(),
                machine=platform.machine(), system=platform.system(),
                packages=hashlib.sha256("\n".join(pkgs).encode()).hexdigest(), locks=locks)


def fingerprint(head, script):
    path = os.path.join(REPO, script.split()[0])
    return dict(commit=head, script=script, script_sha=sha256(path) if os.path.exists(path) else None, env=env_fingerprint())


def load_index(st):
    """{relative path: {"sha": SHA-256 of the saved copy, "by": script that wrote it}}. An index in the old
    format (a plain list, no digests) cannot validate reuse, so it is treated as empty."""
    idx = os.path.join(st, "files.json")
    if not os.path.exists(idx):
        return {}
    data = json.load(open(idx))
    return data if isinstance(data, dict) else {}


def check_commit(st):
    head = git("rev-parse", "HEAD")
    if not head:
        sys.exit("No git metadata: clone the repository (or a git bundle of it) instead of unpacking an archive.")
    meta = os.path.join(st, "run.json")
    if os.path.exists(meta):
        rec = json.load(open(meta))
        if rec["commit"] != head:
            sys.exit(f"The state folder {st} belongs to commit {rec['commit'][:9]}, but this copy is {head[:9]}. "
                     "Use the same commit, or point LOYOLA_STATE at a new folder.")
    else:
        write_json(meta, {"commit": head, "started": datetime.datetime.now().isoformat(timespec="seconds"),
                          "python": platform.python_version(), "machine": platform.platform()})
    return head


def check_clean(st):
    """Refuse to run if a tracked file differs from the commit, other than the saved outputs of finished
    scripts (restored from the state folder). Uncommitted source changes do not change HEAD, so without
    this check they would be run, and reported, as the commit."""
    index = load_index(st)
    changed = [l[3:].split(" -> ")[-1] for l in git("status", "--porcelain", "--untracked-files=no").split("\n") if l]
    dirty = sorted(rel for rel in changed if rel not in index
                   or not os.path.exists(os.path.join(REPO, rel)) or sha256(os.path.join(REPO, rel)) != index[rel]["sha"])
    if dirty:
        sys.exit("Tracked files differ from the commit and are not saved outputs of this run: " + ", ".join(dirty[:10])
                 + (" ..." if len(dirty) > 10 else "") + ". Commit them, or restore them with git checkout, then run again.")


def restore(st):
    """Copy the saved outputs of earlier scripts back into this copy of the repository. A saved output that is
    missing or altered is not restored; the record of the script that wrote it then fails validation."""
    index = load_index(st); n, bad = 0, []
    for rel, info in index.items():
        src = os.path.join(st, "files", rel)
        if not os.path.exists(src) or sha256(src) != info["sha"]:
            bad.append(rel); continue
        copy_atomic(src, os.path.join(REPO, rel)); n += 1
    if bad:
        print(f"WARNING: {len(bad)} saved outputs are missing or altered; the scripts that wrote them will run again: "
              + ", ".join(sorted(bad)[:10]))
    return n


def save(st, script, rels):
    index = load_index(st)
    for rel in rels:
        dst = os.path.join(st, "files", rel)
        copy_atomic(os.path.join(REPO, rel), dst)
        index[rel] = {"sha": sha256(dst), "by": script}
    write_json(os.path.join(st, "files.json"), index)
    return {rel: index[rel]["sha"] for rel in rels}


def upstream(index, script):
    """Saved outputs of the scripts that come before this one in the run order."""
    pos = ORDER.get(script, -1)
    return {rel: info["sha"] for rel, info in index.items() if ORDER.get(info["by"], 1 << 30) < pos}


def marker(st, script):
    return os.path.join(st, "logs", script.replace("/", "__").replace(" ", "_") + ".json")


def validate(st, script, head, index=None):
    """(True, "") if the script's record may be reused, else (False, reason)."""
    m = marker(st, script)
    if not os.path.exists(m):
        return False, "not run"
    rec = json.load(open(m))
    if not rec.get("ok"):
        return False, f"exit {rec.get('exit')}"
    if "fingerprint" not in rec or rec["fingerprint"] != fingerprint(head, script):
        return False, "commit, script, arguments or environment changed"
    index = load_index(st) if index is None else index
    for rel, h in rec.get("outputs", {}).items():
        src = os.path.join(st, "files", rel)
        if index.get(rel, {}).get("sha") != h or not os.path.exists(src) or sha256(src) != h:
            return False, f"saved output missing or altered: {rel}"
        if not os.path.exists(os.path.join(REPO, rel)) or sha256(os.path.join(REPO, rel)) != h:
            return False, f"output in the repository missing or altered: {rel}"
    if rec.get("inputs") != upstream(index, script):
        return False, "an output of an earlier script changed"
    return True, ""


def run_script(st, script, head):
    inputs = upstream(load_index(st), script)
    parts = script.split(); cwd = os.path.join(REPO, os.path.dirname(parts[0]))
    env = {k: v for k, v in os.environ.items() if k != "MPLBACKEND"}   # a notebook's inline backend must not leak in
    log = marker(st, script)[:-5] + ".log"
    t0 = time.time()
    print(f"\n=== {script}  (started {datetime.datetime.now():%H:%M:%S})", flush=True)
    with open(log, "w") as f:
        p = subprocess.Popen([sys.executable, os.path.basename(parts[0])] + parts[1:], cwd=cwd, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        last = []
        for line in p.stdout:
            f.write(line); last = (last + [line.rstrip()])[-3:]
        code = p.wait()
    dt = time.time() - t0
    tracked = set(git("ls-files").split("\n"))
    written = []
    for dp, dns, fns in os.walk(REPO):
        dns[:] = [d for d in dns if not d.startswith(".") and d not in ("__pycache__", "colab_run")
                  and not (d == "formal" and dp == REPO)]   # Lean build trees are large and written by no script
        written += [os.path.relpath(os.path.join(dp, fn), REPO) for fn in fns if os.path.getmtime(os.path.join(dp, fn)) > t0]
    written.sort()
    written = [w for w in written if w in tracked or w.startswith(("external/", "audit/", "structural/", "DATA/"))]
    written = [w for w in written if not w.startswith(NIST_DIRS)]   # NIST pages are downloaded, never kept in the state folder
    outputs = save(st, script, written)
    ok = code == 0 and (written or script in CHECK_ONLY)
    rec = dict(script=script, exit=code, seconds=round(dt), files_written=written, ok=bool(ok),
               finished=datetime.datetime.now().isoformat(timespec="seconds"), last_lines=last,
               fingerprint=fingerprint(head, script), outputs=outputs, inputs=inputs)
    write_json(marker(st, script), rec)
    print(f"--- {script}: exit {code}, {dt/60:.1f} min, {len(written)} files written"
          + ("" if ok else "  <-- PROBLEM (see " + log + ")"), flush=True)
    for l in last:
        print("    " + l)
    return ok


def run_stage(n, redo):
    st = state_dir(); head = check_commit(st)
    print(f"state folder: {st}; restored {restore(st)} output files of earlier scripts")
    check_clean(st)
    stage = next(s for s in STAGES if s[0] == n)
    if any(s.split()[0] in NEEDS_NIST for s, _ in stage[3]):
        # the NIST WebBook pages are not redistributed and this runner never downloads them: it copies them
        # from the private cache filled by the explicit download cell of notebook 01, then checks them
        nist = os.path.join(REPO, "external", "nist_pages.py")
        code = subprocess.run([sys.executable, nist, "--cache", nist_cache()]).returncode
        if code != 0:
            sys.exit("This stage reads the NIST WebBook pages. Run the download cell of notebook 01 first "
                     f"(python3 external/nist_pages.py --download --cache {nist_cache()}), then this stage again.")
    print(f"Stage {n}: {stage[2]}  ({len(stage[3])} scripts, about {sum(m for _, m in stage[3])} lab minutes)")
    bad = 0
    for script, _ in stage[3]:
        if not redo:
            ok, why = validate(st, script, head)
            if ok:
                print(f"skip (already finished, outputs and inputs unchanged): {script}"); continue
            if why != "not run":
                print(f"run again ({why}): {script}")
        bad += not run_script(st, script, head)
    print(f"\nStage {n} {'finished: every script exited 0' if bad == 0 else f'finished with {bad} PROBLEM(S)'}")
    return bad


def digest(path_or_bytes, name):
    data = path_or_bytes if isinstance(path_or_bytes, bytes) else open(path_or_bytes, "rb").read()
    if name.endswith(".pdf"):
        sys.path.insert(0, REPO)
        from verify_loyola_v35 import _pdf_canonical
        return hashlib.sha256(repr(_pdf_canonical(data)).encode()).hexdigest()
    return hashlib.sha256(data).hexdigest()


def report():
    st = state_dir(); head = check_commit(st); restore(st); check_clean(st)
    index = load_index(st)
    lines = [f"# LOYOLA full run: final report", "",
             f"Commit {head}; Python {platform.python_version()} on {platform.platform()}; "
             f"report written {datetime.datetime.now():%Y-%m-%d %H:%M}.", "", "## Scripts", "",
             "| Stage | Script | Result | Minutes |", "|---|---|---|---|"]
    counts = {"OK": 0, "PROBLEM": 0, "STALE": 0, "NOT RUN": 0}
    for n, _, _, scripts in STAGES:
        for script, _ in scripts:
            m = marker(st, script)
            if not os.path.exists(m):
                res = "NOT RUN"; lines.append(f"| {n} | `{script}` | NOT RUN | |")
            else:
                r = json.load(open(m)); ok, why = validate(st, script, head, index)
                if ok:
                    res, shown = "OK", "OK"
                elif not r["ok"]:
                    res, shown = "PROBLEM", f"PROBLEM (exit {r['exit']})"
                else:
                    res, shown = "STALE", f"STALE ({why})"
                lines.append(f"| {n} | `{script}` | {shown} | {r['seconds']/60:.1f} |")
            counts[res] += 1
    same, differ = 0, []
    for rel in sorted(index):
        if subprocess.run(["git", "cat-file", "-e", f"HEAD:{rel}"], cwd=REPO, capture_output=True).returncode != 0:
            continue                                              # a scratch file the script created, not a committed output
        committed = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=REPO, capture_output=True).stdout
        if not os.path.exists(os.path.join(REPO, rel)):
            differ.append(rel); continue
        if digest(os.path.join(REPO, rel), rel) == digest(committed, rel):
            same += 1
        else:
            differ.append(rel)
    lines += ["", "## Committed outputs rewritten by the run", "",
              f"{same} identical to the commit (PDFs by canonical form); {len(differ)} differ.", ""]
    for rel in differ:
        lines.append(f"* DIFFERS `{rel}`" + (f": {SEEN_BEFORE[rel]}" if rel in SEEN_BEFORE else ""))
    verdict = ("COMPLETE: every script ran and exited 0, every expected output is present and unchanged, "
               "and every rewritten output is identical"
               if counts["OK"] == len(ORDER) and not differ else
               f"{counts['OK']} scripts OK, {counts['PROBLEM']} PROBLEM, {counts['STALE']} STALE, "
               f"{counts['NOT RUN']} NOT RUN; {len(differ)} outputs differ")
    lines += ["", f"**Result: {verdict}.**", "",
              "Outputs that differ are kept in the state folder (`files/`); compare them with `git diff --no-index`."]
    open(os.path.join(st, "FINAL_REPORT.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); print(f"\nwritten to {os.path.join(st, 'FINAL_REPORT.md')}")
    return 0 if verdict.startswith("COMPLETE") else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--stage", type=int); ap.add_argument("--redo", action="store_true")
    ap.add_argument("--list", action="store_true"); ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.list:
        for n, name, title, scripts in STAGES:
            print(f"Stage {n} ({name}): {title}; about {sum(m for _, m in scripts)} lab minutes")
            for s, m in scripts:
                print(f"   {m:4d} min  {s}")
        return 0
    if a.report:
        return report()
    if a.stage is None:
        ap.error("give --stage N, --list or --report")
    return 1 if run_stage(a.stage, a.redo) else 0


if __name__ == "__main__":
    sys.exit(main())
