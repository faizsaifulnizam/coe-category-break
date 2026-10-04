"""Generate full-precision CSVs only after all SQL comparisons validate."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.build_dataset import connect
from src.common import ROOT, csv_bytes, publish


def main():
    con=connect()
    files={}
    for table,name in [('exercise','exercise_series'),('gap_summary','gap_summary'),('sensitivity','sensitivity')]:
        query=con.execute(f'SELECT * FROM {table} ORDER BY ALL')
        columns=[d[0] for d in query.description]
        rows=query.fetchall()
        if not rows or any(r is None for r in rows):
            raise ValueError(f'empty {table}')
        files[ROOT/f'outputs/{name}.csv']=csv_bytes(columns,rows)
    assert con.sql('SELECT count(*) FROM sensitivity').fetchone()[0]==6
    publish(files)
    print('summary (S$; post minus pre medians, not causal effects):')
    for r in con.sql('SELECT * FROM sensitivity ORDER BY ALL').fetchall():print(r)
    con.close()

if __name__=='__main__':main()
