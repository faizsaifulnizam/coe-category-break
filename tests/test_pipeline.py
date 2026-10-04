"""Real byte-validation seam, no network doubles."""
import csv
import io
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import importlib.util
spec = importlib.util.find_spec('src.download')
download = importlib.import_module('src.download') if spec else None

HEADER = ['month','bidding_no','vehicle_class','quota','bids_success','bids_received','premium']
def sample():
    rows=[]
    for year in range(2010,2027):
        for month in range(1,13):
            for rnd in (1,2):
                for cat in 'ABCDE':
                    pause = year == 2020 and month in (4,5,6)
                    rows.append([f'{year}-{month:02}',str(rnd),f'Category {cat}',0 if pause else 100,0 if pause else 100,0 if pause else 150,0 if pause else 10000])
    return rows

def encoded(rows):
    s=io.StringIO(); w=csv.writer(s,lineterminator='\n');w.writerow(HEADER);w.writerows(rows);return s.getvalue().encode()

class RawValidation(unittest.TestCase):
    def test_official_shape_with_suspension(self):
        self.assertTrue(callable(getattr(download, 'validate', None)), 'byte validator missing')
        info=download.validate(encoded(sample()))
        self.assertEqual(info['rows'],2040)
        self.assertEqual(info['suspended_exercises'],6)
        self.assertEqual(info['month_max'],'2026-12')

class FailureBoundaries(unittest.TestCase):
    def test_missing_category_rejected_even_in_latest(self):
        for key in [('2022-05','1','Category A'),('2026-12','2','Category B')]:
            with self.subTest(key=key), self.assertRaisesRegex(ValueError,'unpaired'):
                download.validate(encoded([r for r in sample() if tuple(r[:3])!=key]))

    def test_duplicate_rejected(self):
        rows=sample()
        with self.assertRaisesRegex(ValueError,'duplicate'):
            download.validate(encoded(rows+[rows[0]]))

    def test_missing_full_exercise_rejected(self):
        with self.assertRaisesRegex(ValueError,'missing scheduled'):
            download.validate(encoded([r for r in sample() if r[:2]!=['2022-06','1']]))

    def test_latest_round1_is_complete_exercise_not_complete_month(self):
        info=download.validate(encoded([r for r in sample() if r[:2]!=['2026-12','2']]))
        self.assertEqual(info['latest_round'],1)

    def test_missing_suspension_rows_are_not_imputed(self):
        rows=[r for r in sample() if r[3]!=0]
        info=download.validate(encoded(rows))
        self.assertEqual(info['suspension_rows'],0)
        self.assertEqual(info['complete_auction_exercises'],402)

    def test_invalid_network_schema_preserves_existing_snapshot(self):
        import tempfile
        from unittest.mock import patch
        # get() is the external HTTP boundary. Execute real CLI logic, not a fake downloader.
        with tempfile.TemporaryDirectory() as td:
            raw=Path(td);out=raw/download.FILE;out.write_bytes(b'previous')
            manifest=raw/'pull_manifest.json';manifest.write_bytes(b'old manifest')
            responses=[b'{}',b'{"data":{"url":"https://example.invalid/snapshot"}}',b'bad,schema\\n1,2\\n']
            with patch.object(download,'RAW',raw), patch.object(sys,'argv',['download.py','--force']), patch.object(download,'get',side_effect=responses):
                with self.assertRaisesRegex(ValueError,'schema'):download.main()
            self.assertEqual(out.read_bytes(),b'previous')
            self.assertEqual(manifest.read_bytes(),b'old manifest')

    def test_stage_rejects_valid_but_manifest_mismatched_bytes(self):
        import json
        import shutil
        import tempfile
        from unittest.mock import patch
        from src import build_dataset
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);raw=root/'data/raw';raw.mkdir(parents=True)
            shutil.copytree(build_dataset.ROOT/'sql',root/'sql')
            data=encoded(sample());info=download.validate(data)
            (raw/'pull_manifest.json').write_text(json.dumps({'files':{download.FILE:info}}))
            rows=sample();rows[-1][6]+=1
            (raw/download.FILE).write_bytes(encoded(rows))
            with patch.object(build_dataset,'ROOT',root):
                with self.assertRaisesRegex(ValueError,'manifest'):
                    build_dataset.connect()

if __name__=='__main__': unittest.main()
