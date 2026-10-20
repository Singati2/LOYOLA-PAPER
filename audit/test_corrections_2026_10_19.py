#!/usr/bin/env python3
"""Adversarial checks for the corrections of audit/LOYOLA_CORRECTIONS_2026-10-19.md (items 1, 2, 3, 6).

  python3 audit/test_corrections_2026_10_19.py        (about 30 seconds; no network, no NIST data)

Item 1  colab/pipeline.py reuses a finished script only when nothing it depends on changed: a deleted or
        altered saved output, an uncommitted source change, a changed environment and a changed upstream
        output must each prevent reuse; an unchanged finished run must resume without running anything.
Item 2  the notebook git helper must not show a token after a failed clone (dummy marker secret).
Item 3  every generated notebook runs one pinned commit; a clean stale checkout is moved to it, a checkout
        with local changes is rejected.
Item 6  structural/exact_ties.py must stop (exit 2) when a reference row is missing, duplicated or broken,
        or a reference file is truncated; the unmodified files must pass.
Each check prints PASS or FAIL; the exit status is the number of failures.
"""
import ast, base64, glob, importlib.util, json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def sh(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def git_repo(path):
    os.makedirs(path, exist_ok=True)
    sh("git", "init", "--quiet", "-b", "main", cwd=path)
    sh("git", "config", "user.email", "test@example.invalid", cwd=path)
    sh("git", "config", "user.name", "test", cwd=path)


# ---------------------------------------------------------------- item 1: checkpoint reuse
def item1(tmp):
    repo, state, runlog = os.path.join(tmp, "repo"), os.path.join(tmp, "state"), os.path.join(tmp, "runs.txt")
    git_repo(repo)
    os.makedirs(os.path.join(repo, "external"))
    open(os.path.join(repo, "external", "a.py"), "w").write(
        "import os\nopen(os.environ['RUNLOG'], 'a').write('a\\n')\n"
        "open('out_a.txt', 'w').write('a ' + os.environ.get('VAL', '1') + '\\n')\n")
    open(os.path.join(repo, "external", "b.py"), "w").write(
        "import os\nopen(os.environ['RUNLOG'], 'a').write('b\\n')\n"
        "open('out_b.txt', 'w').write('b from ' + open('out_a.txt').read())\n")
    for f in ("requirements-lock.txt", "requirements-extras-lock.txt"):
        open(os.path.join(repo, f), "w").write("numpy==2.0\n")
    sh("git", "add", "-A", cwd=repo); sh("git", "commit", "--quiet", "-m", "fixture", cwd=repo)

    os.environ.update(LOYOLA_STATE=state, RUNLOG=runlog, VAL="1")
    P = load(os.path.join(ROOT, "colab", "pipeline.py"), "pipeline_under_test")
    P.REPO = repo
    P.STAGES = [(1, "s", "fixture", [("external/a.py", 1), ("external/b.py", 1)])]
    P.ORDER = {"external/a.py": 0, "external/b.py": 1}
    P.CHECK_ONLY, P.NEEDS_NIST = set(), set()
    head = sh("git", "rev-parse", "HEAD", cwd=repo)

    def runs():
        r = open(runlog).read().split() if os.path.exists(runlog) else []
        open(runlog, "w").close()
        return r

    def stage():
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            return P.run_stage(1, False)

    check("1a first run executes both scripts", stage() == 0 and runs() == ["a", "b"])
    check("1b unchanged finished run resumes without running anything", stage() == 0 and runs() == [])

    os.remove(os.path.join(state, "files", "external", "out_a.txt"))
    stage(); r = runs()
    check("1c deleted saved output invalidates its script", "a" in r, r)

    with open(os.path.join(state, "files", "external", "out_b.txt"), "a") as f:
        f.write("tampered\n")
    stage(); r = runs()
    check("1d altered saved output invalidates its script", r == ["b"], r)

    os.environ["VAL"] = "2"                     # the upstream script now produces a different output
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        P.run_script(state, "external/a.py", head)
    runs(); os.environ["VAL"] = "1"
    stage(); r = runs()
    check("1e changed upstream output invalidates the dependent script", r == ["b"], r)
    check("1e' the dependent output reflects the new upstream output",
          open(os.path.join(repo, "external", "out_b.txt")).read() == "b from a 2\n")

    with open(os.path.join(repo, "external", "a.py"), "a") as f:
        f.write("# local edit\n")
    try:
        stage(); refused = False
    except SystemExit:
        refused = True
    check("1f uncommitted source change is refused", refused and runs() == [])
    sh("git", "checkout", "--", "external/a.py", cwd=repo)

    real = P.env_fingerprint
    P.env_fingerprint = lambda: dict(real(), packages="different")
    stage(); r = runs()
    check("1g changed environment invalidates every script", r == ["a", "b"], r)
    P.env_fingerprint = real
    stage(); runs()

    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        complete = P.report()
    check("1h report is COMPLETE for a validated run", complete == 0)
    os.remove(os.path.join(state, "files", "external", "out_b.txt"))
    with contextlib.redirect_stdout(io.StringIO()) as out:
        incomplete = P.report()
    check("1i report flags a missing expected output", incomplete == 1 and "STALE" in out.getvalue())

    json.dump(["external/out_a.txt"], open(os.path.join(state, "files.json"), "w"))   # old index: no digests
    stage(); r = runs()
    check("1j an index without digests is not trusted", r == ["a", "b"], r)
    leftovers = [f for f in glob.glob(os.path.join(state, "**", ".tmp-*"), recursive=True)]
    check("1k state files are written atomically (no temporary files left)", not leftovers, leftovers)


# ---------------------------------------------------------------- items 2 and 3: notebook setup
def helpers():
    src = open(os.path.join(ROOT, "colab", "make_notebooks.py")).read()
    tree = ast.parse(src)
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "GIT_HELPERS")
    ns = {}
    exec(ast.literal_eval(node.value), ns)
    return ns


def item2(tmp):
    ns = helpers()
    marker = "ghp_DUMMYMARKER0123456789abcdefXYZ"
    auth = base64.b64encode(("x-access-token:" + marker).encode()).decode()
    dest = os.path.join(tmp, "clone")
    try:
        ns["git_net"](["clone", "--quiet", "https://127.0.0.1:9/none.git", dest], marker); err = ""
    except RuntimeError as e:
        err = str(e)
    check("2a failed clone raises", bool(err))
    check("2b the error message does not contain the token", marker not in err and auth not in err, err[:200])
    try:                                   # a git message that echoes the secret is redacted too
        ns["git_net"](["clone", "--quiet", f"https://127.0.0.1:9/{marker}.git", dest + "2"], marker); err2 = ""
    except RuntimeError as e:
        err2 = str(e)
    check("2c an echoed token is redacted", marker not in err2 and "***" in err2, err2[:200])
    cfg = subprocess.run(["git", "config", "--global", "--list"], capture_output=True, text=True).stdout
    check("2d the token is not written to git configuration", marker not in cfg and auth not in cfg)
    nbs = sorted(glob.glob(os.path.join(ROOT, "colab", "*.ipynb")))
    bad = [os.path.basename(f) for f in nbs if "x-access-token:\" + token" in open(f).read()
           or re.search(r"clone.*url.*check=True", open(f).read())]
    check("2e no notebook puts the token into a clone URL", not bad, bad)


def item3(tmp):
    nbs = sorted(glob.glob(os.path.join(ROOT, "colab", "*.ipynb")))
    pins = {}
    for f in nbs:
        m = re.search(r'PIN = os\.environ\.get\(\\"LOYOLA_PIN\\", \\"([0-9a-f]{40})\\"\)', open(f).read())
        pins[os.path.basename(f)] = m and m[1]
    check("3a every notebook is pinned to a full commit SHA", all(pins.values()), [k for k, v in pins.items() if not v])
    check("3b all notebooks are pinned to the same commit", len(set(pins.values())) == 1, set(pins.values()))
    pin = next(iter(pins.values()))
    check("3c the pinned commit exists in this repository",
          subprocess.run(["git", "-C", ROOT, "cat-file", "-e", f"{pin}^{{commit}}"]).returncode == 0)

    ns = helpers()
    origin = os.path.join(tmp, "origin"); git_repo(origin)
    open(os.path.join(origin, "f.txt"), "w").write("1\n"); sh("git", "add", "-A", cwd=origin); sh("git", "commit", "--quiet", "-m", "1", cwd=origin)
    c1 = sh("git", "rev-parse", "HEAD", cwd=origin)
    work = os.path.join(tmp, "work"); sh("git", "clone", "--quiet", "--branch", "main", origin, work)
    open(os.path.join(origin, "f.txt"), "w").write("2\n"); sh("git", "commit", "--quiet", "-am", "2", cwd=origin)
    c2 = sh("git", "rev-parse", "HEAD", cwd=origin)
    try:
        h = ns["at_pin"](work, c2, [origin, "main"]); ok = h == c2
    except RuntimeError as e:
        ok = False
    check("3d a stale checkout without the pinned commit is fetched and moved to it", ok)
    check("3e an existing checkout at a newer commit is moved back to the pin", ns["at_pin"](work, c1, [origin, "main"]) == c1)
    open(os.path.join(work, "f.txt"), "w").write("local\n")
    try:
        ns["at_pin"](work, c2, [origin, "main"]); rejected = False
    except RuntimeError:
        rejected = True
    check("3f a checkout with local changes is rejected", rejected)
    setup = json.load(open(os.path.join(ROOT, "colab", "01_build_datasets.ipynb")))["cells"][1]["source"]
    setup = "".join(setup)
    check("3g the environment is synchronised to the lock files on every run (partial installs repaired)",
          '"pip", "sync"' in setup and "requirements-lock.txt" in setup)
    check("3h an environment with another Python is rebuilt", "sys.version_info[:2] != (3, 13)" in setup and "shutil.rmtree(ENV)" in setup)


# ---------------------------------------------------------------- item 6: exact reference coverage
def item6(tmp):
    src = os.path.join(ROOT, "structural")
    files = ("hp_counts_out.txt", "chi_floor_out.txt", "fractional_points_out.txt")

    def run_with(mutate):
        d = tempfile.mkdtemp(dir=tmp)
        shutil.copy(os.path.join(src, "exact_ties.py"), d)
        for f in files:
            shutil.copy(os.path.join(src, f), d)
        mutate(d)
        return subprocess.run([sys.executable, "exact_ties.py"], cwd=d, capture_output=True, text=True, timeout=120)

    def edit(name, fn):
        def m(d):
            p = os.path.join(d, name)
            new = fn(open(p).read())               # read before opening for writing (which truncates)
            assert new != open(p).read() or name == "", "mutation changed nothing"
            open(p, "w").write(new)
        return m

    drop_hp = edit("hp_counts_out.txt", lambda t: re.sub(r"(?m)^n=13 mol .*\n", "", t, count=1))
    drop_chi = edit("chi_floor_out.txt", lambda t: re.sub(r"(?m)^n=9 profiles.*\n", "", t, count=1))
    drop_frac = edit("fractional_points_out.txt", lambda t: re.sub(r" \(0\.5,0,1\):\d+", "", t, count=1))
    truncate = edit("hp_counts_out.txt", lambda t: t[: len(t) // 3])
    empty = edit("chi_floor_out.txt", lambda t: "")
    broken = edit("hp_counts_out.txt", lambda t: re.sub(r"(?m)^(n=12 all) N=", r"\1 N:", t, count=1))
    dup = edit("chi_floor_out.txt", lambda t: t + re.search(r"(?m)^n=10 profiles.*\n", t)[0])
    for name, m in [("missing 32-digit row", drop_hp), ("missing chi row", drop_chi), ("missing fractional entry", drop_frac),
                    ("truncated file", truncate), ("empty file", empty), ("broken row format", broken), ("duplicated row", dup)]:
        r = run_with(m)
        check(f"6 {name} -> nonzero exit", r.returncode != 0 and "REFERENCE ERROR" in r.stdout, (r.returncode, r.stdout[-200:]))
    E = load(os.path.join(src, "exact_ties.py"), "exact_ties_under_test")
    try:
        E.committed(); ok = True
    except Exception as e:
        ok = False
    check("6 unmodified reference files pass the coverage check", ok)
    out = open(os.path.join(src, "exact_ties_out.txt")).read()
    check("6 committed output reports complete comparison coverage",
          "reference comparisons completed: 32-digit 22/22, chi 6/6, fractional 90/90" in out)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        for f in (item1, item2, item3, item6):
            d = os.path.join(tmp, f.__name__); os.makedirs(d)
            try:
                f(d)
            except Exception as e:                                  # an unexpected error is a failure, not a pass
                check(f"{f.__name__} ran to the end", False, repr(e))
    print(f"\n{'ALL CHECKS PASSED' if not FAILS else str(len(FAILS)) + ' FAILED: ' + ', '.join(FAILS)}")
    return len(FAILS)


if __name__ == "__main__":
    sys.exit(main())
