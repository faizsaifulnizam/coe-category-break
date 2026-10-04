"""Visual producer CLI: figures/banner hashes repeat in the same environment."""
from pathlib import Path
import hashlib
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]

class Figures(unittest.TestCase):
    def test_figures_cli_repeat_bytes(self):
        self.assertTrue((ROOT/'src/figures.py').exists(),'figure CLI missing')
        paths=[ROOT/f'reports/figures/{stem}{suffix}.png' for stem in ('f1_levels','f2_gap') for suffix in ('','-dark')]+[ROOT/f'assets/banner{suffix}.svg' for suffix in ('','-dark')]
        subprocess.run([sys.executable,str(ROOT/'src/figures.py')],check=True,cwd=ROOT)
        first={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        subprocess.run([sys.executable,str(ROOT/'src/figures.py')],check=True,cwd=ROOT)
        self.assertEqual(first,{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
        self.assertTrue(all(p.stat().st_size>(10000 if p.suffix=='.png' else 500) for p in paths))

if __name__=='__main__':unittest.main()
