#!/usr/bin/env python3
"""The NIST Chemistry WebBook pages that the data builds read: offline check, and an explicit download.

The WebBook is NIST Standard Reference Database 69. NIST states that its Standard Reference Data are
copyrighted by the U.S. Secretary of Commerce and may not be reproduced, stored in a retrieval system
or transmitted without prior permission (https://www.nist.gov/srd/public-law, Standard Reference Data
Act, 15 U.S.C. 290e). The pages are therefore not redistributed with this repository, and nothing in
it downloads them automatically: verify.py and CI run offline. Whoever wants to rebuild the data sets
from their sources retrieves the pages from the WebBook with --download, for their own use.

nist_pages.csv lists, for each of the 262 pages, the local path, the WebBook URL, the date the page was
first committed to the repository (2026-10-03 to 2026-10-06) and the SHA-256 of that copy, the version
from which the committed data sets were built. On 2026-10-17 all 262 live pages matched it.

The digest is taken over a canonical form of the page: the web host (Cloudflare) rewrites an
e-mail-protection token and a challenge script at the end of every response, so the token is blanked
and everything from the first `<script data-cfasync` on is dropped. All WebBook content lies before it.

  python3 external/nist_pages.py                     offline: are the pages present and unchanged?
  python3 external/nist_pages.py --download          retrieve the missing pages, one request per second
                                 [--delay S]         seconds between requests (at least 1)
                                 [--cache DIR]       also copy pages from / save them to a private DIR
  python3 external/nist_pages.py --cache DIR         offline: copy the pages from DIR, then check
  python3 external/nist_pages.py --accept-changed    install pages that NIST changed since they were archived

Exit status: 0 all 262 pages present and identical; 1 a page differs from its archived version (it is
saved as `<path>.changed` and not used unless --accept-changed); 2 pages missing (not downloaded).
A changed page is never accepted silently: the committed data sets refer to the archived versions.
"""
import csv, hashlib, os, re, shutil, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIST = os.path.join(HERE, "nist_pages.csv")
TERMS = ("NIST Chemistry WebBook (NIST SRD 69), (c) U.S. Secretary of Commerce; see https://www.nist.gov/srd/public-law.\n"
         "The pages are retrieved for your own use and are not to be redistributed.")


def canonical(data):
    data = re.sub(rb"email-protection#[0-9a-f]+", b"email-protection#", data)
    return data.split(b"<script data-cfasync")[0]


def digest(data):
    return hashlib.sha256(canonical(data)).hexdigest()


def pages():
    with open(LIST, newline="") as f:
        return list(csv.DictReader(f))


def local_paths():
    """Repository-relative paths of the pages present on disk (for scripts that copy the tree)."""
    return [p["path"] for p in pages() if os.path.exists(os.path.join(ROOT, p["path"]))]


def status():
    """(identical, changed, missing) lists of repository-relative paths; no network."""
    same, changed, missing = [], [], []
    for p in pages():
        path = os.path.join(ROOT, p["path"])
        if not os.path.exists(path):
            missing.append(p["path"])
        elif digest(open(path, "rb").read()) == p["sha256_canonical"]:
            same.append(p["path"])
        else:
            changed.append(p["path"])
    return same, changed, missing


def available():
    same, changed, missing = status()
    return not changed and not missing


def fetch(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "LOYOLA-PAPER reproducibility (python urllib)"})
            return urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:
            if k == tries - 1:
                raise RuntimeError(f"could not download {url}: {e}")
            time.sleep(10 * (k + 1))


def arg(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def main():
    download, accept = "--download" in sys.argv, "--accept-changed" in sys.argv
    cache = arg("--cache")
    delay = max(1.0, float(arg("--delay") or 1.0))
    rows = pages()
    copied = got = 0
    if cache or download:
        todo = [p for p in rows if not os.path.exists(os.path.join(ROOT, p["path"]))]
        if download and todo:
            print(TERMS)
        for p in todo:
            path = os.path.join(ROOT, p["path"])
            cached = os.path.join(cache, p["path"]) if cache else None
            data = None
            if cached and os.path.exists(cached):
                data = open(cached, "rb").read(); copied += 1
            elif download:
                if got:
                    time.sleep(delay)                       # rate limit: sequential, at least one second apart
                data = fetch(p["url"]); got += 1
                if got % 50 == 0:
                    print(f"  {got} pages retrieved", flush=True)
                if cached:
                    os.makedirs(os.path.dirname(cached), exist_ok=True); open(cached, "wb").write(data)
            if data is None:
                continue
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if digest(data) != p["sha256_canonical"] and not accept:
                open(path + ".changed", "wb").write(data)
                continue
            open(path, "wb").write(data)
    same, changed, missing = status()
    changed += [p["path"] for p in rows if os.path.exists(os.path.join(ROOT, p["path"]) + ".changed")
                and p["path"] in missing]
    missing = [m for m in missing if m not in changed]
    print(f"{len(rows)} NIST WebBook pages: {len(same)} present and identical to the archived version"
          + (f" ({got} retrieved from the WebBook)" if got else "") + (f" ({copied} copied from {cache})" if copied else "")
          + (f"; {len(missing)} NOT DOWNLOADED (python3 external/nist_pages.py --download)" if missing else "")
          + (f"; {len(changed)} CHANGED since archived: {', '.join(changed[:5])}{' ...' if len(changed) > 5 else ''}" if changed else ""))
    if changed and accept:
        print("--accept-changed: the changed pages are used; outputs built from them may differ from the committed ones")
        return 2 if missing else 0
    return 1 if changed else 2 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
