"""Small shared byte publication seam: staged files, atomic per-file replacement."""
import csv
import io
import os
from pathlib import Path
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def publish(files):
    """Single writer only; ordinary exceptions roll back, not power-loss/crash atomic."""
    staged={}
    old={}
    changed=[]
    try:
        for path,data in files.items():
            path=Path(path)
            path.parent.mkdir(parents=True,exist_ok=True)
            old[path]=path.read_bytes() if path.exists() else None
            fd,name=tempfile.mkstemp(prefix='.stage-',dir=path.parent)
            staged[path]=Path(name)
            with os.fdopen(fd,'wb') as f:
                f.write(data)
        for path,tmp in staged.items():
            tmp.replace(path)
            changed.append(path)
    except Exception:
        for path in reversed(changed):
            if old[path] is None:
                path.unlink(missing_ok=True)
            else:
                fd,name=tempfile.mkstemp(prefix='.rollback-',dir=path.parent)
                with os.fdopen(fd,'wb') as f:
                    f.write(old[path])
                Path(name).replace(path)
        raise
    finally:
        for tmp in staged.values():
            tmp.unlink(missing_ok=True)


def csv_bytes(columns,rows):
    out=io.StringIO()
    writer=csv.writer(out,lineterminator='\n')
    writer.writerow(columns)
    writer.writerows(rows)
    return out.getvalue().encode('utf-8')
