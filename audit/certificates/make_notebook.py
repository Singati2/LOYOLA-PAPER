"""Write collision_orders_colab.ipynb: runs the four certificates of this folder on Google Colab or locally."""
import nbformat as nbf
nb = nbf.v4.new_notebook()
nb.cells = [
 nbf.v4.new_markdown_cell(
  "# Minimal collision orders of degree-ratio histograms: certificates\n\n"
  "Re-runs, in about two minutes on one CPU and well under 1 GB of memory, the exhaustive enumerations behind the "
  "minimal orders 13 (all trees) and 16 (maximum degree at most 4), the table of first orders by maximum degree, "
  "the early collisions of SDD and ISDD, and the witness trees with the all-order construction. "
  "Only `networkx` is needed (pinned to the version in `requirements-lock.txt`). No NIST data and nothing licensed is used. "
  "Set `REVISION` to the branch or tag to check."),
 nbf.v4.new_code_cell(
  "import os, subprocess, sys\n"
  "REVISION = os.environ.get('LOYOLA_REVISION', 'review/short-version')\n"
  "if not os.path.exists('minimal.py'):\n"
  "    if not os.path.exists('LOYOLA-PAPER'):\n"
  "        subprocess.run(['git', 'clone', '--quiet', '--depth', '1', '--branch', REVISION,\n"
  "                        'https://github.com/Singati2/LOYOLA-PAPER.git'], check=True)\n"
  "    os.chdir('LOYOLA-PAPER/audit/certificates')\n"
  "if 'google.colab' in sys.modules:\n"
  "    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'networkx==3.6.1'], check=True)\n"
  "import networkx; print('python', sys.version.split()[0], 'networkx', networkx.__version__)"),
 nbf.v4.new_code_cell(
  "def run(*args):\n"
  "    out = subprocess.run([sys.executable, *args], capture_output=True, text=True, check=True).stdout\n"
  "    print(out.strip().splitlines()[-1]); return out\n"
  "a = run('minimal.py', '17')\n"
  "assert a.strip().splitlines()[-1] == \"{'all': 13, 'chem': 16}\"\n"
  "b = run('by_delta.py', '18')\n"
  "assert \"'4': 16, '5': 16\" in b and \"'None': 13\" in b and \"'3'\" not in b.splitlines()[-1]\n"
  "c = run('ratio_indices.py')\n"
  "assert \"('SDD', 'chem'): 9\" in c and \"('ISDD', 'chem'): 10\" in c\n"
  "d = run('witnesses.py')\n"
  "assert d.count('OK for every order') == 2\n"
  "print('ALL CERTIFICATES REPRODUCED')"),
]
nbf.write(nb, "collision_orders_colab.ipynb")
