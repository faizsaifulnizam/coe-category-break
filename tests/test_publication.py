"""Publishing seam uses real temporary files; tests ordinary replacement rollback."""
import importlib
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
common=importlib.import_module('src.common') if importlib.util.find_spec('src.common') else None

class Publication(unittest.TestCase):
    def test_validated_batch_replaces_both_files(self):
        self.assertTrue(callable(getattr(common,'publish',None)),'batch publication missing')
        with tempfile.TemporaryDirectory() as td:
            a,b=Path(td)/'reports/figures/f1.png',Path(td)/'docs/img/f1.png'
            a.parent.mkdir(parents=True)
            a.write_bytes(b'old')
            common.publish({a:b'new',b:b'two'})
            self.assertEqual(a.read_bytes(),b'new')
            self.assertEqual(b.read_bytes(),b'two')

    def test_ordinary_second_replace_failure_restores_first(self):
        with tempfile.TemporaryDirectory() as td:
            a,b=Path(td)/'reports/figures/f1.png',Path(td)/'docs/img/f1.png'
            a.parent.mkdir(parents=True);b.parent.mkdir(parents=True)
            a.write_bytes(b'one');b.write_bytes(b'two')
            original=Path.replace
            def fail_second(source,target):
                if source.name.startswith('.stage-') and Path(target)==b:
                    raise OSError('injected ordinary replace failure')
                return original(source,target)
            with patch.object(Path,'replace',fail_second):
                with self.assertRaisesRegex(OSError,'injected'):
                    common.publish({a:b'new one',b:b'new two'})
            self.assertEqual(a.read_bytes(),b'one')
            self.assertEqual(b.read_bytes(),b'two')
            self.assertFalse(any(p.name.startswith(('.stage-','.rollback-')) for p in Path(td).rglob('*')))

if __name__=='__main__':unittest.main()
