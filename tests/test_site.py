"""Stdlib checks for the publication surface; no browser dependency in CI."""
import csv
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
import re
import struct
import unittest
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[1]
REPO='https://github.com/faizsaifulnizam/coe-category-break'
PAGES='https://faizsaifulnizam.github.io/coe-category-break/'
SERIES=('hdb-resale-mart','card-book-quality','coe-quota-premium','retail-sales-split','coe-category-break','hdb-lease-slope')
class Tags(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

class Site(unittest.TestCase):
    def test_site_assets_metadata_claims_and_series(self):
        html=(ROOT/'docs/index.html').read_text(encoding='utf-8')
        card=(ROOT/'docs/social-card.html').read_text(encoding='utf-8')
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertTrue((ROOT/'docs/.nojekyll').exists())
        tags=Tags(html).tags
        meta={a.get('property',a.get('name')):a.get('content') for t,a in tags if t=='meta'}
        self.assertEqual(meta['og:image'],PAGES+'img/social-card.png')
        self.assertEqual((meta['og:image:width'],meta['og:image:height']),('1280','640'))
        self.assertEqual(meta['twitter:card'],'summary_large_image')
        self.assertEqual(meta['twitter:image'],meta['og:image'])
        self.assertIn(('link',{'rel':'canonical','href':PAGES}),tags)
        for tag,attrs in tags:
            for key in ('src','srcset','href'):
                value=attrs.get(key)
                if not value:continue
                url=urlsplit(value)
                if not url.scheme and url.path:
                    target=(ROOT/'docs'/unquote(url.path)).resolve()
                    self.assertTrue(target.is_relative_to(ROOT/'docs'),value)
                    self.assertTrue(target.is_file(),value)
                elif value.startswith(REPO+'/blob/main/'):
                    self.assertTrue((ROOT/value.removeprefix(REPO+'/blob/main/')).is_file(),value)
        for text in (html,card):
            for font in re.findall(r"url\('([^']+)'\)",text):
                self.assertTrue((ROOT/'docs'/font).is_file(),font)
        for name in SERIES:
            self.assertIn('https://github.com/faizsaifulnizam/'+name,html)
            self.assertIn('https://github.com/faizsaifulnizam/'+name,readme)
        for number in ('6,190.50','18,198.50','12,008','21,745.50','24,081.50','2,336'):
            self.assertIn(number,html)
            self.assertIn(number,readme)
        for text in (html,readme):
            self.assertIn('not causal',text)
            self.assertIn('if_i_ran_the_test.md',text)
        self.assertIn('not a causal estimate',card)
        with (ROOT/'outputs/gap_summary.csv').open(encoding='utf-8',newline='') as f:
            rows=list(csv.DictReader(f))
        for window,pre,post,delta,counts in [('structural','6190.5','18198.5','12008',(98,106)),('tight','21745.5','24081.5','2336',(24,24))]:
            chosen={r['period']:r for r in rows if r['window']==window and r['variant']=='all'}
            self.assertEqual((Decimal(chosen['pre']['median_gap']),Decimal(chosen['post']['median_gap'])),(Decimal(pre),Decimal(post)))
            self.assertEqual(Decimal(post)-Decimal(pre),Decimal(delta))
            self.assertEqual(tuple(int(chosen[p]['n_exercises']) for p in ('pre','post')),counts)
        for theme in ('','-dark'):
            data=(ROOT/f'docs/img/social-card{theme}.png').read_bytes()
            self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II',data[16:24]),(1280,640))
        self.assertEqual(readme.count('<picture>'),3)
        self.assertNotIn('<a href="reports/figures/',readme)

if __name__=='__main__':unittest.main()
