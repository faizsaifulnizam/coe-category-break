"""Independent official acquisition; validate bytes before replacing the snapshot."""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
FILE = 'coe-bidding-results.csv'
DATASET_ID = 'd_69b3380ad7e51aff3a7dcc84eba52b8a'
HEADER = ['month','bidding_no','vehicle_class','quota','bids_success','bids_received','premium']
CATEGORIES = {f'Category {c}' for c in 'ABCDE'}
PAUSE = {('2020-'+m, str(r)) for m in ('04','05','06') for r in (1,2)}
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0.0.0 Safari/537.36'


def validate(data):
    rows = list(csv.reader(io.StringIO(data.decode('utf-8-sig'))))
    if not rows or rows[0] != HEADER:
        raise ValueError('invalid download schema')
    keys = Counter()
    groups = defaultdict(list)
    for r in rows[1:]:
        if len(r) != 7:
            raise ValueError('wrong field count')
        month, rnd, cat = r[:3]
        if not re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', month) or rnd not in {'1','2'} or cat not in CATEGORIES:
            raise ValueError('invalid month/round/category')
        if any(not re.fullmatch(r'(\d+|\d{1,3}(,\d{3})+)', x) for x in r[3:]):
            raise ValueError('invalid integer cell')
        vals = [int(x.replace(',','')) for x in r[3:]]
        if (month,rnd) in PAUSE:
            if any(vals):
                raise ValueError('suspended exercise contains nonzero observations')
        elif vals[0] <= 0 or vals[3] <= 0:
            raise ValueError('nonpositive auction quota/premium outside suspension')
        keys[(month,rnd,cat)] += 1
        groups[(month,rnd)].append(cat)
    if any(v != 1 for v in keys.values()):
        raise ValueError('duplicate exercise/category')
    if any(set(v) != CATEGORIES for v in groups.values()):
        raise ValueError('unpaired/incomplete exercise (including latest)')
    if not groups:
        raise ValueError('empty dataset')
    first, last = min(groups), max(groups)
    if first != ('2010-01','1') or last < ('2025-06','2'):
        raise ValueError('coverage below historical/freshness floor')
    expected = set()
    y,m = 2010,1
    while f'{y:04}-{m:02}' <= last[0]:
        for rnd in ('1','2'):
            key=(f'{y:04}-{m:02}',rnd)
            if key <= last and key not in PAUSE:
                expected.add(key)
        y,m = (y+1,1) if m==12 else (y,m+1)
    if set(groups)-PAUSE != expected:
        raise ValueError('missing scheduled exercise outside known suspension')
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'rows':len(rows)-1,
            'month_min':first[0],'month_max':last[0],'latest_round':int(last[1]),
            'published_exercises':len(groups),'complete_auction_exercises':len(set(groups)-PAUSE),
            'suspended_exercises':6,'suspension_rows':sum(len(groups[k]) for k in PAUSE),
            'categories':sorted(CATEGORIES)}


def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Referer':'https://data.gov.sg/'})
    with urllib.request.urlopen(req,timeout=180) as response:
        return response.read()


def fetch():
    base=f'https://api-open.data.gov.sg/v1/public/api/datasets/{DATASET_ID}'
    get(base+'/initiate-download')
    for _ in range(15):
        response=json.loads(get(base+'/poll-download'))
        url=(response.get('data') or {}).get('url')
        if url:
            return get(url)
        time.sleep(2)
    raise RuntimeError('no signed download URL after 15 polls')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--force',action='store_true',help='refresh explicitly; prose/locks require renewed review')
    args=parser.parse_args()
    path=RAW/FILE
    if path.exists() and not args.force:
        info=validate(path.read_bytes())
        manifest=json.loads((RAW/'pull_manifest.json').read_text())
        if info != manifest['files'][FILE]:
            raise ValueError('cached snapshot does not match manifest; refusing to bless changed bytes')
        print('validated vendored snapshot:',info)
        return
    data=fetch()
    info=validate(data)
    manifest={'dataset':{'id':DATASET_ID,'url':f'https://data.gov.sg/datasets/{DATASET_ID}/view'},
              'retrieved_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),
              'source':'LTA via data.gov.sg public v1 initiate/poll signed download',
              'files':{FILE:info}}
    # Import here to keep the validator usable independently.
    from common import publish
    publish({path:data, RAW/'pull_manifest.json':(json.dumps(manifest,indent=2)+'\n').encode()})
    print('downloaded and validated:',info)

if __name__=='__main__': main()
