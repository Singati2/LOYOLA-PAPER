#!/usr/bin/env python3
"""Write or check SHA256SUMS.txt: exactly one SHA-256 per git-tracked file
(the manifest itself excluded).

  python3 manifest.py --write   regenerate from `git ls-files`
  python3 manifest.py           check; exit 1 on any of: duplicate path,
                                tracked file missing from the manifest,
                                manifest path not tracked / missing on disk,
                                hash mismatch
"""
import hashlib, os, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); MAN = os.path.join(ROOT, "SHA256SUMS.txt")
def sha(p):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, p), "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
tracked = sorted(set(subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True,
                                    check=True).stdout.splitlines()) - {"SHA256SUMS.txt"})
if "--write" in sys.argv:
    with open(MAN, "w") as f:
        for p in tracked: f.write(f"{sha(p)}  {p}\n")
    print(f"wrote {len(tracked)} entries"); sys.exit(0)
errs, seen = [], {}
for ln, line in enumerate(open(MAN), 1):
    if not line.strip(): continue
    h, _, p = line.rstrip("\n").partition("  ")
    if p in seen: errs.append(f"duplicate path {p} (lines {seen[p]} and {ln})"); continue
    seen[p] = ln
    if p not in tracked: errs.append(f"{p}: in manifest but not git-tracked")
    elif not os.path.exists(os.path.join(ROOT, p)): errs.append(f"{p}: missing on disk")
    elif sha(p) != h: errs.append(f"{p}: hash mismatch")
for p in tracked:
    if p not in seen: errs.append(f"{p}: tracked but not in manifest")
print("\n".join(errs) if errs else f"manifest OK: {len(seen)} files, one hash per path, all match")
sys.exit(1 if errs else 0)
