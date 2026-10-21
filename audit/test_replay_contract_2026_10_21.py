#!/usr/bin/env python3
"""Adversarial checks of the replay contract of colab/pipeline.py and audit/run_all_scripts.py (2026-10-21).

  python3 audit/test_replay_contract_2026_10_21.py      (about 20 seconds; small synthetic git repositories only,
                                                          no NIST data, no computation of the paper)

The runner must not record a script as OK, or the run as COMPLETE, unless every file that
colab/expected_outputs.py lists for the script was rewritten (present, not empty) and no other tracked file
was. Each attack below must fail (PROBLEM, STALE, rerun or refusal); the legitimate runs must succeed.
These are mock runs: they test the bookkeeping, not a real or Colab replay of the paper.
Each check prints PASS or FAIL; the exit status is the number of failures.
"""
import contextlib, importlib.util, io, json, os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def sh(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def quiet(f, *a):
    """(return value or 'EXIT: message', printed text)."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        try:
            r = f(*a)
        except SystemExit as e:
            r = f"EXIT: {e.code}"
    return r, out.getvalue()


# a.py writes out_a.txt (read by b.py); b.py writes out_b.txt; c.py is check-only. MODE selects an attack.
A = """import os
m = os.environ.get('MODE', '')
open(os.environ['RUNLOG'], 'a').write('a\\n')
if m == 'skip':            pass                                              # exit 0, required output not written
elif m == 'empty':         open('out_a.txt', 'w').close()
elif m == 'scratch':       open('scratch.tmp', 'w').write('x\\n')            # writes only an untracked scratch file
elif m == 'extra':         open('out_a.txt', 'w').write('a 1\\n'); open('src.py', 'w').write(open('src.py').read())
else:                      open('out_a.txt', 'w').write('a ' + os.environ.get('VAL', '1') + '\\n')
"""
B = """import os
open(os.environ['RUNLOG'], 'a').write('b\\n')
open('out_b.txt', 'w').write('b from ' + open('out_a.txt').read())
"""
C = """import os
open(os.environ['RUNLOG'], 'a').write('c\\n')
if os.environ.get('MODE') == 'checkwrite':
    open('out_b.txt', 'w').write(open('out_b.txt').read())                    # a check-only script rewriting a tracked file
"""


class Fixture:
    def __init__(self, tmp, name):
        self.repo, self.state, self.runlog = (os.path.join(tmp, name, x) for x in ("repo", "state", "runs.txt"))
        os.makedirs(os.path.join(self.repo, "external"))
        sh("git", "init", "--quiet", "-b", "main", cwd=self.repo)
        sh("git", "config", "user.email", "test@example.invalid", cwd=self.repo)
        sh("git", "config", "user.name", "test", cwd=self.repo)
        for f, src in (("a.py", A), ("b.py", B), ("c.py", C), ("src.py", "x = 1\n"),
                       ("out_a.txt", "a 1\n"), ("out_b.txt", "b from a 1\n")):
            open(os.path.join(self.repo, "external", f), "w").write(src)
        for f in ("requirements-lock.txt", "requirements-extras-lock.txt"):
            open(os.path.join(self.repo, f), "w").write("numpy==2.0\n")
        sh("git", "add", "-A", cwd=self.repo); sh("git", "commit", "--quiet", "-m", "fixture", cwd=self.repo)
        os.environ.update(LOYOLA_STATE=self.state, RUNLOG=self.runlog, VAL="1", MODE="")
        spec = importlib.util.spec_from_file_location(f"pipeline_{name}", os.path.join(ROOT, "colab", "pipeline.py"))
        P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
        P.REPO = self.repo
        P.STAGES = [(1, "s", "fixture", [("external/a.py", 1), ("external/b.py", 1), ("external/c.py", 1)])]
        P.ORDER = {"external/a.py": 0, "external/b.py": 1, "external/c.py": 2}
        P.EXPECTED = {"external/a.py": ["external/out_a.txt"], "external/b.py": ["external/out_b.txt"], "external/c.py": []}
        P.INCIDENTAL, P.CHECK_ONLY, P.NEEDS_NIST = {}, {"external/c.py"}, set()
        self.P = P
        self.head = sh("git", "rev-parse", "HEAD", cwd=self.repo)

    def runs(self):
        r = open(self.runlog).read().split() if os.path.exists(self.runlog) else []
        open(self.runlog, "w").close()
        return r

    def stage(self, mode=""):
        os.environ["MODE"] = mode
        try:
            return quiet(self.P.run_stage, 1, False)
        finally:
            os.environ["MODE"] = ""

    def report(self):
        return quiet(self.P.report)

    def rec(self, script):
        return json.load(open(self.P.marker(self.state, script)))

    def path(self, *p):
        return os.path.join(self.repo, *p)


def main():
    tmp = tempfile.mkdtemp(prefix="loyola_contract_")
    try:
        run(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{len(FAILS)} FAILED" if FAILS else "\nALL PASS")
    return len(FAILS)


def run(tmp):
    # ---- the legitimate run
    F = Fixture(tmp, "good")
    r, _ = F.stage()
    check("C1 a clean synthetic run that meets the contract has no PROBLEM", r == 0 and F.runs() == ["a", "b", "c"])
    rep, out = F.report()
    check("C2 its report is COMPLETE (replay plan only) and names the cross-checks outside the plan",
          rep == 0 and "COMPLETE (replay plan only)" in out and "## Not replayed by this pipeline" in out
          and "not a replay of every script" in out, out[-400:])
    check("C3 a check-only script that writes no tracked file is OK", F.P.validate(F.state, "external/c.py", F.head)[0])
    check("C4 regenerated tracked outputs are accepted as outputs (resume runs nothing)", F.stage()[0] == 0 and F.runs() == [])

    # ---- exit 0 but the required output was never generated
    F = Fixture(tmp, "skip")
    F.stage("skip"); rec = F.rec("external/a.py")
    check("A1 exit 0 without writing the required output is a PROBLEM",
          rec["exit"] == 0 and rec["ok"] is False and rec.get("missing") == ["external/out_a.txt"], rec)
    rep, out = F.report()
    check("A1' the report is not COMPLETE and names the missing output",
          rep == 1 and "COMPLETE" not in out.split("**Result:")[-1] and "missing external/out_a.txt" in out, out[-500:])

    # ---- an empty output
    F = Fixture(tmp, "empty")
    F.stage("empty"); rec = F.rec("external/a.py")
    check("A2 an empty required output is a PROBLEM", rec["ok"] is False and rec.get("missing") == ["external/out_a.txt"], rec)

    # ---- writes only an unexpected scratch file
    F = Fixture(tmp, "scratch")
    F.stage("scratch"); rec = F.rec("external/a.py")
    check("A3 exit 0 writing only an untracked scratch file is a PROBLEM",
          rec["ok"] is False and rec.get("scratch") == ["external/scratch.tmp"] and rec.get("missing") == ["external/out_a.txt"], rec)
    check("A3' a scratch file is never saved as an output",
          not os.path.exists(os.path.join(F.state, "files", "external", "scratch.tmp")))

    # ---- rewrites a tracked file that is not listed
    F = Fixture(tmp, "extra")
    F.stage("extra"); rec = F.rec("external/a.py")
    check("A4 rewriting an unlisted tracked file is a PROBLEM", rec["ok"] is False and rec.get("unexpected") == ["external/src.py"], rec)
    F = Fixture(tmp, "checkwrite")
    F.stage("checkwrite"); rec = F.rec("external/c.py")
    check("A5 a check-only script that rewrites a tracked file is a PROBLEM",
          rec["ok"] is False and rec.get("unexpected") == ["external/out_b.txt"], rec)

    # ---- cached outputs: deleted, truncated, replaced
    F = Fixture(tmp, "cache"); F.stage(); F.runs()
    saved = os.path.join(F.state, "files", "external", "out_a.txt")
    open(saved, "w").close(); F.stage()
    check("A6 a truncated cached output makes its script run again", "a" in F.runs())
    open(saved, "w").write("forged\n"); F.stage()
    check("A7 a replaced cached output makes its script run again", "a" in F.runs())
    os.remove(saved); F.stage()
    check("A8 a deleted cached output makes its script run again", "a" in F.runs())
    os.remove(F.path("external", "out_b.txt"))
    check("A9 a deleted tracked output in the repository is restored or rerun, never accepted silently",
          F.stage()[0] == 0 and os.path.exists(F.path("external", "out_b.txt")))
    F.runs()

    # ---- forged index entries
    F = Fixture(tmp, "forge"); F.stage(); F.runs()
    open(F.path("external", "src.py"), "w").write("x = 2  # tampered source\n")
    idx = json.load(open(os.path.join(F.state, "files.json")))
    idx["external/src.py"] = {"sha": F.P.sha256(F.path("external", "src.py")), "by": "external/a.py"}
    json.dump(idx, open(os.path.join(F.state, "files.json"), "w"))
    r, _ = F.stage()
    check("A10 a forged files.json entry whitelisting a modified tracked source stops the runner",
          isinstance(r, str) and r.startswith("EXIT") and "not an expected output" in r and F.runs() == [], r)
    rep, _ = F.report()
    check("A10' and the report refuses too", isinstance(rep, str) and rep.startswith("EXIT"), rep)
    sh("git", "add", "external/src.py", cwd=F.repo)                          # the same forgery with the edit staged
    r, _ = F.stage()
    check("A10b the forgery is refused when the source edit is staged as well",
          isinstance(r, str) and r.startswith("EXIT") and F.runs() == [], r)
    idx.pop("external/src.py"); json.dump(idx, open(os.path.join(F.state, "files.json"), "w"))
    r, _ = F.stage()
    check("A10c a staged source edit without an index entry is refused, with its full path",
          isinstance(r, str) and ": external/src.py" in r, r)

    F = Fixture(tmp, "forge2"); F.stage(); F.runs()
    open(F.path("external", "out_b.txt"), "w").write("b forged\n")
    idx = json.load(open(os.path.join(F.state, "files.json")))
    idx["external/out_b.txt"]["sha"] = F.P.sha256(F.path("external", "out_b.txt"))
    json.dump(idx, open(os.path.join(F.state, "files.json"), "w"))
    os.remove(os.path.join(F.state, "files", "external", "out_b.txt"))      # restore() cannot overwrite it
    r, _ = F.stage()
    check("A11 a forged digest for an expected output (record not matching) is refused as an uncommitted change",
          isinstance(r, str) and "not saved outputs of this run" in r and "external/out_b.txt" in r, r)

    F = Fixture(tmp, "traversal"); F.stage(); F.runs()
    idx = json.load(open(os.path.join(F.state, "files.json")))
    idx["../evil.txt"] = {"sha": "0" * 64, "by": "external/a.py"}
    json.dump(idx, open(os.path.join(F.state, "files.json"), "w"))
    r, _ = F.stage()
    check("A12 a path outside the repository in the index stops the runner",
          isinstance(r, str) and "unsafe path" in r and not os.path.exists(os.path.join(F.repo, "..", "evil.txt")), r)

    F = Fixture(tmp, "badjson"); F.stage(); F.runs()
    open(os.path.join(F.state, "files.json"), "w").write("{not json")
    r, _ = F.stage()
    check("A13 a corrupted files.json stops the runner", isinstance(r, str) and "cannot be trusted" in r, r)

    # ---- records: missing, tampered, corrupted, other commit
    F = Fixture(tmp, "records"); F.stage(); F.runs()
    os.remove(F.P.marker(F.state, "external/b.py"))
    rep, out = F.report()
    check("A14 a missing stage record is NOT RUN and the report is not COMPLETE", rep == 1 and "NOT RUN" in out)
    F.stage(); F.runs()
    rec = F.rec("external/a.py"); rec["fingerprint"]["commit"] = "0" * 40
    json.dump(rec, open(F.P.marker(F.state, "external/a.py"), "w"))
    ok, why = F.P.validate(F.state, "external/a.py", F.head)
    check("A15 a tampered fingerprint (other commit) is STALE", not ok and "changed" in why, why)
    F.stage(); F.runs()
    rec = F.rec("external/a.py"); rec["fingerprint"]["inventory"] = "0" * 64
    json.dump(rec, open(F.P.marker(F.state, "external/a.py"), "w"))
    check("A16 a record made under another output inventory is STALE", not F.P.validate(F.state, "external/a.py", F.head)[0])
    F.stage(); F.runs()
    rec = F.rec("external/a.py"); rec["outputs"] = {}
    json.dump(rec, open(F.P.marker(F.state, "external/a.py"), "w"))
    check("A17 a record whose outputs omit an expected file is STALE",
          F.P.validate(F.state, "external/a.py", F.head) == (False, "recorded outputs do not match the expected-output inventory"))
    F.stage(); F.runs()
    open(F.P.marker(F.state, "external/b.py"), "w").write("{corrupt")
    rep, out = F.report()
    check("A18 a corrupted record is STALE and the report is not COMPLETE", rep == 1 and "STALE (record unreadable" in out, out[-500:])
    F.stage(); r = F.runs()
    check("A18' and the script runs again", r == ["b"], r)
    os.environ["VAL"] = "2"; quiet(F.P.run_script, F.state, "external/a.py", F.head); F.runs(); os.environ["VAL"] = "1"
    ok, why = F.P.validate(F.state, "external/b.py", F.head)
    check("A19 a modified upstream input makes the dependent record STALE", not ok and "earlier script" in why, why)
    F.stage(); F.runs()
    run_json = os.path.join(F.state, "run.json"); good = open(run_json).read()
    json.dump({"commit": "f" * 40}, open(run_json, "w"))
    r, _ = F.stage()
    check("A20 a state folder of another commit is refused", isinstance(r, str) and "belongs to commit" in r, r)
    open(run_json, "w").write("[1,")
    r, _ = F.stage()
    check("A21 a corrupted run.json is refused", isinstance(r, str) and "unreadable or corrupted" in r, r)
    open(run_json, "w").write(good)

    # ---- source changes: deleted and renamed tracked files
    F = Fixture(tmp, "git"); F.stage(); F.runs()
    os.remove(F.path("external", "src.py"))
    r, _ = F.stage()
    check("A22 a deleted tracked source file is refused", isinstance(r, str) and "external/src.py" in r, r)
    sh("git", "checkout", "--", "external/src.py", cwd=F.repo)
    sh("git", "mv", "external/src.py", "external/src2.py", cwd=F.repo)
    r, _ = F.stage()
    check("A23 a renamed tracked source file is refused (both paths named)",
          isinstance(r, str) and "external/src.py" in r and "external/src2.py" in r, r)
    sh("git", "reset", "--quiet", "--hard", cwd=F.repo)

    # ---- a different output changes the comparison with the commit
    F = Fixture(tmp, "differ"); os.environ["VAL"] = "3"; F.stage(); os.environ["VAL"] = "1"
    rep, out = F.report()
    check("A24 outputs that differ from the commit prevent COMPLETE", rep == 1 and "DIFFERS `external/out_a.txt`" in out, out[-400:])

    # ---- the real inventory
    spec = importlib.util.spec_from_file_location("pipeline_real", os.path.join(ROOT, "colab", "pipeline.py"))
    P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
    tracked = set(sh("git", "ls-files", cwd=ROOT).split("\n"))
    listed = [f for v in P.EXPECTED.values() for f in v]
    check("R1 the inventory covers exactly the scripts of the plan", set(P.EXPECTED) == set(P.ORDER))
    check("R2 every listed output is a tracked file and not a NIST page",
          all(f in tracked and P.safe_rel(f) for f in listed), [f for f in listed if f not in tracked])
    check("R3 no output is listed for two scripts", len(listed) == len(set(listed)))
    check("R4 the check-only scripts are exactly those with no listed output",
          {s for s, v in P.EXPECTED.items() if not v} == P.CHECK_ONLY)
    check("R5 the cross-checks outside the plan are not in the inventory", not set(P.NOT_REPLAYED) & set(P.EXPECTED))
    RA = importlib.util.spec_from_file_location("run_all_real", os.path.join(ROOT, "audit", "run_all_scripts.py"))
    ra = importlib.util.module_from_spec(RA); RA.loader.exec_module(ra)
    scripts = [s for s, _ in ra.SCRIPTS]
    check("R6 run_all_scripts.py checks every script it runs against the inventory (or lists it as check-only)",
          all(s in ra.EXPECTED or s in ra.CHECK_ONLY for s in scripts) and set(scripts) - {"manifest.py"} == set(P.EXPECTED))
    ok = ra.judge({"script": "external/bp/bp_tests.py", "exit": 0, "changed": [], "touched_files": ["external/bp/bp_tests.py.log"]})
    check("R7 run_all_scripts.py: exit 0 without the expected outputs is a PROBLEM", ok[0] is False and "missing" in ok[1], ok)
    ok = ra.judge({"script": "external/bp/make_bp_table.py", "exit": 0, "changed": [],
                   "touched_files": ["external/bp/bp_table_rows.tex", "main.tex"]})
    check("R8 run_all_scripts.py: an unlisted tracked rewrite is a PROBLEM", ok[0] is False and "main.tex" in ok[1], ok)
    ok = ra.judge({"script": "external/bp/make_bp_table.py", "exit": 0, "changed": [], "touched_files": ["external/bp/bp_table_rows.tex"]})
    check("R9 run_all_scripts.py: the expected output, identical, is OK", ok[0] is True, ok)
    ok = ra.judge({"script": "prose_numbers_check.py", "exit": 0, "changed": [], "touched_files": []})
    check("R10 run_all_scripts.py: a check-only script writing nothing is OK", ok[0] is True, ok)


if __name__ == "__main__":
    sys.exit(main())
