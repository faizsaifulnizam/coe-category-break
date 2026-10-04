"""Refresh entry point; only external HTTP and CLI/filesystem paths are substituted."""
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import download


class Refresh(unittest.TestCase):
    def run_refresh(self, data, raw):
        responses = [b'{}', b'{"data":{"url":"https://example.invalid/snapshot"}}', data]
        with patch.object(download, 'RAW', raw), patch.object(sys, 'argv', ['download.py', '--force']), patch.object(download, 'get', side_effect=responses):
            download.main()

    def test_unterminated_quote_preserves_snapshot(self):
        data = (download.RAW / download.FILE).read_bytes()
        # Quote only the final numeric cell, deliberately omitting its closing quote.
        prefix, premium = data.rstrip(b'\r\n').rsplit(b',', 1)
        malformed = prefix + b',"' + premium
        with self.assertRaises(csv.Error):
            download.validate(malformed)
        with tempfile.TemporaryDirectory() as td:
            raw = Path(td)
            previous = {download.FILE: b'previous raw', 'pull_manifest.json': b'previous manifest'}
            for name, value in previous.items():
                (raw / name).write_bytes(value)
            with self.assertRaises(csv.Error):
                self.run_refresh(malformed, raw)
            self.assertEqual(previous, {name: (raw / name).read_bytes() for name in previous})

    def test_bigint_overflow_preserves_snapshot(self):
        rows = list(csv.reader(io.StringIO((download.RAW / download.FILE).read_text())))
        for column in range(3, 7):
            with self.subTest(column=download.HEADER[column]), tempfile.TemporaryDirectory() as td:
                changed = [row[:] for row in rows]
                changed[-1][column] = '9223372036854775808'
                out = io.StringIO()
                csv.writer(out, lineterminator='\n').writerows(changed)
                data = out.getvalue().encode()
                with self.assertRaisesRegex(ValueError, 'BIGINT'):
                    download.validate(data)
                raw = Path(td)
                previous = {download.FILE: b'previous raw', 'pull_manifest.json': b'previous manifest'}
                for name, value in previous.items():
                    (raw / name).write_bytes(value)
                with self.assertRaisesRegex(ValueError, 'BIGINT'):
                    self.run_refresh(data, raw)
                self.assertEqual(previous, {name: (raw / name).read_bytes() for name in previous})

    def test_sql_nonnull_guard_covers_bids(self):
        import duckdb
        checks = (download.ROOT / 'sql/05_checks.sql').read_text()
        for column in ('bids_success', 'bids_received'):
            with self.subTest(column=column), duckdb.connect() as con:
                con.execute("CREATE TABLE staged (month DATE, round_no INTEGER, category VARCHAR, premium BIGINT, quota BIGINT, bids_success BIGINT, bids_received BIGINT)")
                con.execute("INSERT INTO staged VALUES ('2026-09-01', 2, 'Category E', 10000, 100, 100, 150)")
                con.execute(f'UPDATE staged SET {column} = NULL')
                con.execute('CREATE VIEW retained AS SELECT * FROM staged')
                result = dict(con.execute(checks).fetchall())
                self.assertFalse(result['parsed_nonnull'])

    def test_valid_imported_refresh_publishes_matching_manifest(self):
        data = (download.RAW / download.FILE).read_bytes()
        with tempfile.TemporaryDirectory() as td:
            raw = Path(td)
            (raw / download.FILE).write_bytes(b'previous raw')
            (raw / 'pull_manifest.json').write_bytes(b'previous manifest')
            self.run_refresh(data, raw)
            self.assertEqual((raw / download.FILE).read_bytes(), data)
            manifest = json.loads((raw / 'pull_manifest.json').read_text())
            self.assertEqual(manifest['files'][download.FILE], download.validate(data))
            self.assertEqual(manifest['dataset']['id'], download.DATASET_ID)
            self.assertFalse(any(p.name.startswith(('.stage-', '.rollback-')) for p in raw.iterdir()))


if __name__ == '__main__':
    unittest.main()
