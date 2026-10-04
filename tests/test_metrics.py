"""SQL producer seam exercised on independent calendar fixtures."""
import importlib
import importlib.util
import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from test_pipeline import sample, encoded
build=importlib.import_module('src.build_dataset') if importlib.util.find_spec('src.build_dataset') else None

class Metrics(unittest.TestCase):
    def test_calendar_windows_and_full_exercise_median(self):
        self.assertTrue(callable(getattr(build,'connect',None)),'staging/metrics seam missing')
        rows=sample()
        for r in rows:
            if r[3] and r[2]=='Category B':r[6]+=100 if r[0]<'2022-05' else 300
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'raw.csv';p.write_bytes(encoded(rows))
            con=build.connect(p)
            summary=con.sql('''SELECT "window",period,n_exercises,median_gap FROM gap_summary WHERE variant='all' ORDER BY "window",period''').fetchall()
            self.assertEqual(summary,[('structural','post',112,300.0),('structural','pre',98,100.0),('tight','post',24,300.0),('tight','pre',24,100.0)])
            seq=con.sql("SELECT rolling_gap FROM exercise WHERE month='2020-07-01' ORDER BY round_no").fetchall()
            self.assertEqual(seq,[(None,),(None,)])
            self.assertEqual(con.sql("SELECT rolling_gap FROM exercise WHERE month='2020-08-01' AND round_no=1").fetchone()[0],100.0)
            con.close()

    def test_transition_selection_is_two_each_side_before_round_filter(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'raw.csv';p.write_bytes(encoded(sample()))
            con=build.connect(p)
            self.assertEqual(con.sql('SELECT strftime(month,\'%Y-%m\'),round_no FROM exercise WHERE transition ORDER BY month,round_no').fetchall(),[('2022-04',1),('2022-04',2),('2022-05',1),('2022-05',2)])
            counts=con.sql('''SELECT variant,period,n_exercises FROM gap_summary WHERE "window"='tight' ORDER BY variant,period''').fetchall()
            self.assertEqual(counts,[('all','post',24),('all','pre',24),('exclude_transition','post',22),('exclude_transition','pre',22),('round1','post',12),('round1','pre',12)])
            con.close()

    def test_future_growth_changes_only_structural_post(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'raw.csv';rows=sample();p.write_bytes(encoded(rows))
            con=build.connect(p)
            before=con.sql('SELECT * FROM gap_summary ORDER BY ALL').fetchall();con.close()
            extra=[['2027-01','1',f'Category {c}',100,100,150,10000] for c in 'ABCDE']
            p.write_bytes(encoded(rows+extra))
            con=build.connect(p)
            after=con.sql('SELECT * FROM gap_summary ORDER BY ALL').fetchall()
            self.assertEqual([r for r in before if r[0]=='tight' or r[2]=='pre'],[r for r in after if r[0]=='tight' or r[2]=='pre'])
            self.assertEqual(con.sql('''SELECT n_exercises,end_round FROM gap_summary WHERE "window"='structural' AND variant='all' AND period='post' ''').fetchone(),(113,1))
            con.close()

if __name__=='__main__':unittest.main()
