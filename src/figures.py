"""Code-generated theme pairs; pixel QA runs before the batch is published."""
import csv
from datetime import date,datetime,timedelta,timezone
import io
import json
from pathlib import Path
import sys
from xml.sax.saxutils import escape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
from PIL import ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.common import ROOT,publish
from src.build_dataset import connect

FONTS=ROOT/'assets/fonts'


def qa(fig,title,footer,subtitle):
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    w,h=fig.canvas.get_width_height()
    boxes=[]
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text().strip():continue
        b=t.get_window_extent(renderer)
        assert b.x0>=2 and b.y0>=2 and b.x1<=w-2 and b.y1<=h-2, f'clipped text: {t.get_text()}'
    for t in (title,footer,subtitle):
        b=t.get_window_extent(renderer)
        margin=min(b.x0,w-b.x1)
        assert margin>=40,f'title/footer margin {margin}'
        boxes.append(b)
        print(f'text margin {margin:.1f}px: {t.get_text().splitlines()[0]}')
    assert not any(a.overlaps(b) for i,a in enumerate(boxes) for b in boxes[i+1:]),'figure text overlap'
    for ax in fig.axes:
        texts=[t.get_window_extent(renderer) for t in ax.texts if t.get_visible() and t.get_text()]
        assert not any(a.overlaps(b) for i,a in enumerate(texts) for b in texts[i+1:]),'annotations overlap'
        legend=ax.get_legend()
        if legend:
            box=legend.get_window_extent(renderer)
            for line in ax.lines:
                vertices=line.get_transform().transform(line.get_path().vertices)
                assert not any(box.contains(x,y) for x,y in vertices),'legend covers plotted observation'
    print('QA PASS: in-bounds, annotation/figure-text overlap, legend observation clearance')


def banner(dark):
    bg,ink,muted=('#14293D','#E7E3DC','#A9B6C1') if dark else ('#FBFBF9','#14293D','#5C6B79')
    accent='#D4B87A' if dark else '#B9975B'
    texts=[(64,108,'coe-category-break',54,'SourceSerif4-Regular.ttf'),
           (64,182,'Did the B–A premium gap move after May 2022?',24,'Inter-Regular.ttf'),
           (64,220,'A descriptive before/after read — not a causal estimate.',21,'Inter-Regular.ttf'),
           (1216,264,"A six-repo series on Singapore's public data · 5 of 6",18,'Inter-Regular.ttf')]
    elements=[]
    for x,y,s,size,font in texts:
        bounds=ImageFont.truetype(str(FONTS/font),size).getbbox(s)
        left=x-bounds[2] if size==18 else x+bounds[0]
        right=x if size==18 else x+bounds[2]
        assert left>=40 and right<=1240 and y-size>=40 and y+8<=280
        family='Source Serif 4, Georgia, serif' if font.startswith('Source') else 'Inter, Arial, sans-serif'
        anchor='end' if size==18 else 'start'
        elements.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" font-size="{size}" fill="{ink if size==54 else muted}">{escape(s)}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="320" viewBox="0 0 1280 320" role="img" aria-label="COE category break: descriptive, not causal"><title>coe-category-break</title><rect width="1280" height="320" fill="{bg}"/><rect x="64" y="134" width="480" height="4" fill="{accent}"/>'+''.join(elements)+'</svg>\n').encode()


def main():
    con=connect()
    rows=con.sql('SELECT month,round_no,premium_a,premium_b,gap,rolling_gap FROM exercise ORDER BY month,round_no').fetchall()
    con.close()
    values={(r[0],r[1]):r[2:] for r in rows}
    xs=[];series=[[],[],[],[]]
    y,m=2018,1
    while date(y,m,1)<=rows[-1][0]:
        for rnd in (1,2):
            if (date(y,m,1),rnd)>(rows[-1][0],rows[-1][1]):continue
            xs.append(date(y,m,1)+timedelta(days=14*(rnd-1)))
            v=values.get((date(y,m,1),rnd),(None,)*4)
            for i in range(4):series[i].append(float('nan') if v[i] is None else v[i]/1000)
        y,m=(y+1,1) if m==12 else (y,m+1)
    manifest=json.loads((ROOT/'data/raw/pull_manifest.json').read_text())
    pulled=datetime.fromisoformat(manifest['retrieved_at']).astimezone(timezone(timedelta(hours=8))).date()
    files={}
    for font in FONTS.glob('*.ttf'):font_manager.fontManager.addfont(str(font))
    for dark in (False,True):
        plt.style.use(ROOT/f"assets/style{'-dark' if dark else ''}.mplstyle")
        ink,muted,petrol,burnt,brass=('#E7E3DC','#A9B6C1','#4C93B5','#D97E4F','#D4B87A') if dark else ('#14293D','#5C6B79','#22607B','#C0552B','#B9975B')
        for gap in (False,True):
            fig,ax=plt.subplots(figsize=(8,4.5),dpi=200)
            fig.subplots_adjust(left=.105,right=.96,bottom=.23,top=.77)
            title=fig.text(.04,.945,'Already wide in the year before May 2022;\n2026 median gap is about S$2,750' if gap else 'Both categories rose; the gap followed its own path',fontsize=13,ha='left',va='top',fontfamily='Source Serif 4',color=ink)
            subtitle=fig.text(.04,.80 if gap else .84,f"2018–{rows[-1][0].year} · EV Cat A limit → 110kW: May 2022 R1 · descriptive, not causal",fontsize=9,color=muted)
            ax.axvline(date(2022,5,1),color=ink,ls=':',lw=1.2)
            if gap:
                ax.axvspan(date(2021,5,1),date(2022,5,1),color=petrol,alpha=(.34 if dark else .16),hatch='///' if dark else None,label='tight pre (12 months)')
                ax.axvspan(date(2022,5,1),date(2023,5,1),color=brass,alpha=(.34 if dark else .16),hatch='...' if dark else None,label='tight post (12 months)')
                ax.plot(xs,series[2],color=muted,lw=.9,label='B−A per exercise')
                ax.plot(xs,series[3],color=brass,lw=1.9,label='3-exercise median (full only)')
                ax.axhline(0,color=ink,lw=.6)
                ax.set_ylabel('B−A gap (S$ thousands)')
            else:
                ax.plot(xs,series[0],color=petrol,lw=1.7,label='Category A')
                ax.plot(xs,series[1],color=burnt,ls='--',lw=1.7,label='Category B')
                ax.set_ylabel('Quota premium (S$ thousands)')
            ax.set_xticks([date(year,1,1) for year in range(2018,rows[-1][0].year+1,2)])
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            ax.set_xlim(date(2018,1,1),xs[-1]+timedelta(days=20))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:,.0f}'))
            ax.legend(loc='best',fontsize=8)
            footer=fig.text(.04,.035,f'No auctions Apr–Jun 2020; no smoothing across the pause. Source: LTA/data.gov.sg, pulled {pulled}.\nR1/R2 = first/second exercise; plotted at month-start/+14 days, not actual closing dates. See exercise CSV.',fontsize=7.2,color=muted,va='bottom')
            qa(fig,title,footer,subtitle)
            out=io.BytesIO();fig.savefig(out,format='png',dpi=200);plt.close(fig)
            suffix='-dark' if dark else ''
            files[ROOT/f"reports/figures/f{2 if gap else 1}_{'gap' if gap else 'levels'}{suffix}.png"]=out.getvalue()
        files[ROOT/f"assets/banner{'-dark' if dark else ''}.svg"]=banner(dark)
    # Keep Pages copies in the same validated batch, including ordinary-exception rollback.
    for path,data in list(files.items()):
        files[ROOT/'docs/img'/path.name]=data
    publish(files)
    print('published four figures + two banners and matching Pages copies; QA passed before writes')

if __name__=='__main__':main()
