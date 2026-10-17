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
to mix results of different commits.

Stages 1, 4 and 8 read the NIST WebBook pages, which are not redistributed. The runner never
downloads them: notebook 01 has an explicit download cell (external/nist_pages.py --download, one
request per second) that saves them to a private cache folder (LOYOLA_NIST_CACHE, else
LOYOLA_nist_pages_private in Google Drive, else .nist_cache/ in the repository), and those stages
copy them from there. The pages are never copied into the state folder.
"""
import argparse, datetime, hashlib, json, os, platform, shutil, subprocess, sys, time

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
        json.dump({"commit": head, "started": datetime.datetime.now().isoformat(timespec="seconds"),
                   "python": platform.python_version(), "machine": platform.platform()}, open(meta, "w"), indent=1)
    if git("status", "--porcelain", "--untracked-files=no") and not os.path.exists(os.path.join(st, "files.json")):
        print("WARNING: the repository has local changes before the first stage; they are not part of the commit.")
    return head


def restore(st):
    """Copy the outputs of earlier finished scripts back into this copy of the repository."""
    idx = os.path.join(st, "files.json")
    if not os.path.exists(idx):
        return 0
    n = 0
    for rel in json.load(open(idx)):
        src = os.path.join(st, "files", rel)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(os.path.join(REPO, rel)) or REPO, exist_ok=True)
            shutil.copy2(src, os.path.join(REPO, rel)); n += 1
    return n


def save(st, rels):
    idx = os.path.join(st, "files.json")
    known = set(json.load(open(idx))) if os.path.exists(idx) else set()
    for rel in rels:
        dst = os.path.join(st, "files", rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(REPO, rel), dst); known.add(rel)
    json.dump(sorted(known), open(idx, "w"), indent=0)


def marker(st, script):
    return os.path.join(st, "logs", script.replace("/", "__").replace(" ", "_") + ".json")


def run_script(st, script):
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
    save(st, written)
    ok = code == 0 and (written or script in CHECK_ONLY)
    rec = dict(script=script, exit=code, seconds=round(dt), files_written=written, ok=bool(ok),
               finished=datetime.datetime.now().isoformat(timespec="seconds"), last_lines=last)
    json.dump(rec, open(marker(st, script), "w"), indent=1)
    print(f"--- {script}: exit {code}, {dt/60:.1f} min, {len(written)} files written"
          + ("" if ok else "  <-- PROBLEM (see " + log + ")"), flush=True)
    for l in last:
        print("    " + l)
    return ok


def run_stage(n, redo):
    st = state_dir(); check_commit(st)
    print(f"state folder: {st}; restored {restore(st)} output files of earlier scripts")
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
        if not redo and os.path.exists(marker(st, script)) and json.load(open(marker(st, script)))["ok"]:
            print(f"skip (already finished): {script}"); continue
        bad += not run_script(st, script)
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
    st = state_dir(); head = check_commit(st); restore(st)
    lines = [f"# LOYOLA full run: final report", "",
             f"Commit {head}; Python {platform.python_version()} on {platform.platform()}; "
             f"report written {datetime.datetime.now():%Y-%m-%d %H:%M}.", "", "## Scripts", "",
             "| Stage | Script | Result | Minutes |", "|---|---|---|---|"]
    counts = {"OK": 0, "PROBLEM": 0, "NOT RUN": 0}
    for n, _, _, scripts in STAGES:
        for script, _ in scripts:
            m = marker(st, script)
            if os.path.exists(m):
                r = json.load(open(m)); res = "OK" if r["ok"] else "PROBLEM"
                shown = res if r["ok"] else f"{res} (exit {r['exit']})"
                lines.append(f"| {n} | `{script}` | {shown} | {r['seconds']/60:.1f} |")
            else:
                res = "NOT RUN"; lines.append(f"| {n} | `{script}` | NOT RUN | |")
            counts[res] += 1
    same, differ = 0, []
    idx = os.path.join(st, "files.json")
    for rel in (json.load(open(idx)) if os.path.exists(idx) else []):
        if subprocess.run(["git", "cat-file", "-e", f"HEAD:{rel}"], cwd=REPO, capture_output=True).returncode != 0:
            continue                                              # a scratch file the script created, not a committed output
        committed = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=REPO, capture_output=True).stdout
        if digest(os.path.join(REPO, rel), rel) == digest(committed, rel):
            same += 1
        else:
            differ.append(rel)
    lines += ["", "## Committed outputs rewritten by the run", "",
              f"{same} identical to the commit (PDFs by canonical form); {len(differ)} differ.", ""]
    for rel in differ:
        lines.append(f"* DIFFERS `{rel}`" + (f": {SEEN_BEFORE[rel]}" if rel in SEEN_BEFORE else ""))
    verdict = ("COMPLETE: every script ran and exited 0, and every rewritten output is identical"
               if counts["PROBLEM"] == counts["NOT RUN"] == 0 and not differ else
               f"{counts['OK']} scripts OK, {counts['PROBLEM']} PROBLEM, {counts['NOT RUN']} NOT RUN; {len(differ)} outputs differ")
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
