"""End-to-end CSV receipt with independent stdlib calculations."""
import csv
from pathlib import Path
import statistics
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]

class Analysis(unittest.TestCase):
    def test_analysis_cli_and_all_window_numbers(self):
        self.assertTrue((ROOT/'src/analysis.py').exists(),'analysis CLI missing')
        subprocess.run([sys.executable,str(ROOT/'src/analysis.py')],check=True,cwd=ROOT)
        with (ROOT/'data/raw/coe-bidding-results.csv').open(encoding='utf-8-sig') as f:raw=list(csv.DictReader(f))
        paired={}
        for r in raw:
            if r['month']<'2018-01' or r['month'] in ('2020-04','2020-05','2020-06') or r['vehicle_class'] not in ('Category A','Category B'):continue
            paired.setdefault((r['month'],int(r['bidding_no'])),{})[r['vehicle_class']]=int(r['premium'].replace(',',''))
        with (ROOT/'outputs/gap_summary.csv').open() as f:summary=list(csv.DictReader(f))
        for s in summary:
            values=[]
            for (m,rnd),ab in paired.items():
                if (m<'2022-05')!=(s['period']=='pre'):continue
                if s['window']=='tight' and not '2021-05'<=m<='2023-04':continue
                if s['variant']=='round1' and rnd!=1:continue
                if s['variant']=='exclude_transition' and m in ('2022-04','2022-05'):continue
                values.append((ab['Category A'],ab['Category B'],ab['Category B']-ab['Category A']))
            self.assertEqual(int(s['n_exercises']),len(values))
            for i,key in enumerate(('a','b','gap')):
                v=[x[i] for x in values]
                for metric,op in [('median',statistics.median),('min',min),('max',max)]:
                    self.assertEqual(float(s[f'{metric}_{key}']),op(v))

if __name__=='__main__':unittest.main()
