#!/usr/bin/env python3
"""Rebuild auxiliary outputs in an isolated copy and compare exact bytes."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = (
    ('structural/fractional_points.py', 'structural/fractional_points_out.txt'),
    ('structural/chi_floor.py', 'structural/chi_floor_out.txt'),
    ('external/bp/build_calorimetric_set.py', 'external/bp/calorimetric_dHvap298_alkanes.csv'),
)


def main():
    with tempfile.TemporaryDirectory() as td:
        target = Path(td) / 'repo'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('.git', '.lake', '__pycache__'))
        for script, output in OUTPUTS:
            produced = target / output
            produced.unlink()
            subprocess.run([sys.executable, str(target / script)], cwd=td, check=True,
                           stdout=subprocess.DEVNULL)
            if produced.read_bytes() != (ROOT / output).read_bytes():
                raise AssertionError(f'fresh output differs: {output}')
            print(f'PASS: {output}', flush=True)
    print('Auxiliary output reproduction PASS')


if __name__ == '__main__':
    main()
