"""Visual producer CLI: figures/banner hashes repeat in the same environment."""
from pathlib import Path
import hashlib
import subprocess
import sys
import unittest
import tempfile
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
ROOT=Path(__file__).resolve().parents[1]

class Figures(unittest.TestCase):
    def test_gap_title_and_theme_window_contrast(self):
        from src import figures
        original=figures.qa
        seen=[]
        def inspect(fig,title,footer,subtitle):
            ax=fig.axes[0]
            if ax.get_ylabel()=='B−A gap (S$ thousands)':
                self.assertIn('year before May 2022',title.get_text())
                self.assertIn('2026 Jan–Sep median gap is S$2,750',title.get_text())
                dark=fig.get_facecolor()[0]<.5
                self.assertEqual([p.get_alpha() for p in ax.patches],[.34 if dark else .16]*2)
                seen.append(dark)
            original(fig,title,footer,subtitle)
        try:
            with patch.object(figures,'qa',inspect):figures.main()
            self.assertEqual(seen,[False,True])
        finally:
            figures.plt.close('all')

    def test_figures_cli_repeat_bytes(self):
        self.assertTrue((ROOT/'src/figures.py').exists(),'figure CLI missing')
        paths=[ROOT/f'reports/figures/{stem}{suffix}.png' for stem in ('f1_levels','f2_gap') for suffix in ('','-dark')]+[ROOT/f'assets/banner{suffix}.svg' for suffix in ('','-dark')]
        subprocess.run([sys.executable,str(ROOT/'src/figures.py')],check=True,cwd=ROOT)
        first={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        subprocess.run([sys.executable,str(ROOT/'src/figures.py')],check=True,cwd=ROOT)
        self.assertEqual(first,{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
        self.assertTrue(all(p.stat().st_size>(10000 if p.suffix=='.png' else 500) for p in paths))
        for path in paths:
            self.assertEqual(path.read_bytes(),(ROOT/'docs/img'/path.name).read_bytes())

    def test_late_pages_replace_rolls_back_entire_figure_batch(self):
        from src import figures,common
        with tempfile.TemporaryDirectory() as td:
            def fail_late(files):
                mapped={Path(td)/p.relative_to(ROOT):data for p,data in files.items()}
                self.assertEqual(len(mapped),12)
                target=list(mapped)[-1]
                self.assertTrue(target.is_relative_to(Path(td)/'docs/img'))
                before={p:('old '+str(p.relative_to(td))).encode() for p in mapped}
                for p,data in before.items():
                    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
                original=Path.replace
                def fail(source,dest):
                    if source.name.startswith('.stage-') and Path(dest)==target:
                        raise OSError('injected final Pages replacement failure')
                    return original(source,dest)
                with patch.object(Path,'replace',fail):
                    with self.assertRaisesRegex(OSError,'injected final Pages'):
                        common.publish(mapped)
                self.assertEqual(before,{p:p.read_bytes() for p in before})
                self.assertFalse(any(p.name.startswith(('.stage-','.rollback-')) for p in Path(td).rglob('*')))
            with patch.object(figures,'publish',fail_late):figures.main()

if __name__=='__main__':unittest.main()
