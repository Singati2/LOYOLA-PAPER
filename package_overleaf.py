#!/usr/bin/env python3
"""Synchronize Overleaf sources and ZIPs with the canonical manuscript files."""
from pathlib import Path
import argparse
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
PROJECTS = {
    "LOYOLA_FINAL_PAPER_OVERLEAF": {"main.tex": "main.tex", "supplement.tex": "supplement.tex"},
    "LOYOLA_MAIN_OVERLEAF": {"main.tex": "main.tex"},
    "LOYOLA_SUPPLEMENT_OVERLEAF": {"main.tex": "supplement.tex"},
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check without writing")
    args = parser.parse_args()
    if args.check:
        errors = []
        for name, sources in PROJECTS.items():
            folder = ROOT / name
            expected = dict(sources)
            if name != "LOYOLA_MAIN_OVERLEAF":
                expected.update({str(p.relative_to(ROOT)): str(p.relative_to(ROOT))
                                 for p in (ROOT / "figures").glob("*.pdf")})
            for target, source in expected.items():
                if not (folder / target).exists() or (folder / target).read_bytes() != (ROOT / source).read_bytes():
                    errors.append(f"{name}/{target}: differs from {source}")
            try:
                with zipfile.ZipFile(ROOT / (name + ".zip")) as z:
                    files = {str(p.relative_to(folder)): p for p in folder.rglob("*") if p.is_file()}
                    if sorted(z.namelist()) != sorted(files):
                        errors.append(f"{name}.zip: file list differs from folder")
                    for target, p in files.items():
                        if target not in z.namelist() or z.read(target) != p.read_bytes():
                            errors.append(f"{name}.zip: {target} differs from folder")
            except (OSError, zipfile.BadZipFile) as exc:
                errors.append(f"{name}.zip: {exc}")
        if errors:
            parser.exit(1, "\n".join(errors) + "\n")
        print("Overleaf packages match canonical sources and figures")
        return
    for name, sources in PROJECTS.items():
        folder = ROOT / name
        for target, source in sources.items():
            shutil.copyfile(ROOT / source, folder / target)
        if name != "LOYOLA_MAIN_OVERLEAF":
            for source in sorted((ROOT / "figures").glob("*.pdf")):
                shutil.copyfile(source, folder / "figures" / source.name)
        with zipfile.ZipFile(ROOT / (name + ".zip"), "w", zipfile.ZIP_DEFLATED) as z:
            for source in sorted(folder.rglob("*")):
                if source.is_file():
                    z.write(source, source.relative_to(folder))
        print(f"synchronized {name}")


if __name__ == "__main__":
    main()
