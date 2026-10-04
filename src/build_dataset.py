"""Validated staging and first-class SQL. Each stage validates before publication."""
from pathlib import Path
import sys
import tempfile
import duckdb
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.common import ROOT, publish
from src.download import validate


def connect(raw_path=None):
    path=Path(raw_path) if raw_path else ROOT/'data/raw/coe-bidding-results.csv'
    info=validate(path.read_bytes())
    if raw_path is None:
        import json
        manifest=json.loads((path.parent/'pull_manifest.json').read_text())
        if manifest['files'][path.name]!=info:
            raise ValueError('raw bytes do not match pull manifest')
    con=duckdb.connect()
    con.execute('SET threads=1')
    con.execute('CREATE TABLE raw AS SELECT * FROM read_csv(?, all_varchar=true)',[str(path)])
    con.execute((ROOT/'sql/01_staging.sql').read_text())
    checks=con.execute((ROOT/'sql/05_checks.sql').read_text()).fetchall()
    if not all(passed for _,passed in checks):
        con.close()
        raise ValueError(f'SQL checks failed: {checks}')
    con.execute((ROOT/'sql/02_metrics.sql').read_text())
    if con.sql('SELECT count(*) FROM gap_summary').fetchone()[0]!=12:
        con.close()
        raise ValueError('empty/incomplete comparison windows')
    return con


def main():
    con=connect()
    # Temporary directory inside destination filesystem, never a hardcoded /tmp.
    folder=ROOT/'data/processed';folder.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=folder) as td:
        path=Path(td)/'exercise.parquet'
        con.execute('COPY (SELECT * FROM exercise ORDER BY month,round_no) TO ? (FORMAT PARQUET)',[str(path)])
        assert con.execute('SELECT count(*) FROM read_parquet(?)',[str(path)]).fetchone()[0]==con.sql('SELECT count(*) FROM exercise').fetchone()[0]
        publish({folder/'exercise.parquet':path.read_bytes()})
    print('SQL checks 5/5; paired analysis exercises:',con.sql('SELECT count(*) FROM exercise').fetchone()[0])
    con.close()

if __name__=='__main__':main()
