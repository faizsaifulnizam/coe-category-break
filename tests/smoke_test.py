"""Snapshot locks: update explicitly after a reviewed re-pull."""
import csv
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def main():
    raw=ROOT/'data/raw/coe-bidding-results.csv'
    manifest=json.loads((raw.parent/'pull_manifest.json').read_text())
    assert hashlib.sha256(raw.read_bytes()).hexdigest()==manifest['files'][raw.name]['sha256']
    with (ROOT/'outputs/gap_summary.csv').open() as f:rows=list(csv.DictReader(f))
    assert len(rows)==12
    all_rows={(r['window'],r['period']):r for r in rows if r['variant']=='all'}
    for key,n,gap in [(('structural','pre'),98,6190.5),(('structural','post'),106,18198.5),(('tight','pre'),24,21745.5),(('tight','post'),24,24081.5)]:
        assert int(all_rows[key]['n_exercises'])==n
        assert float(all_rows[key]['median_gap'])==gap
    for stem in ('f1_levels','f2_gap'):
        for suffix in ('','-dark'):assert (ROOT/f'reports/figures/{stem}{suffix}.png').stat().st_size>10000
    for suffix in ('','-dark'):assert (ROOT/f'assets/banner{suffix}.svg').stat().st_size>500
    assert 'not a causal estimate' in (ROOT/'README.md').read_text(encoding='utf-8').lower()
    print('PASS: raw byte SHA, 12 summary rows, four headline locks, four figures, two banners, causal refusal')

if __name__=='__main__':main()
