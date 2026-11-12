"""SI Figure S1 and broadened-window integrals from the 40-root CSV spectrum."""
from pathlib import Path
from read_data import read_table, read_states
import math, argparse, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, LogLocator, NullFormatter, ScalarFormatter
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path('figures'))
OUT=parser.parse_args().output
OUT.mkdir(parents=True,exist_ok=True)

spectrum_rows = read_states('BlatterO_LR_spectrum.csv')
states = {m: [r for r in spectrum_rows if r['method']==m] for m in ['U','X']}

Phi=lambda z:.5*math.erfc(-z/math.sqrt(2))
phi=lambda z:math.exp(-.5*z*z)/math.sqrt(2*math.pi)
def integral(m,a,b,width,n=40):
 sigma=width/math.sqrt(8*math.log(2));area=moment=0.
 for s in states[m][:n]:
  x=(a-s['E'])/sigma;y=(b-s['E'])/sigma;weight=Phi(y)-Phi(x)
  area+=s['f']*weight
  moment+=s['f']*(s['E']*weight+sigma*(phi(x)-phi(y)))
 return {'area':area,'centroid':moment/area}
def compare(a,b,width,n=40):
 u=integral('U',a,b,width,n);x=integral('X',a,b,width,n)
 return {'lower':a,'upper':b,'fwhm':width,'U':u,'X':x,'change_percent':100*(x['area']/u['area']-1),'centroid_shift_eV':x['centroid']-u['centroid']}
windows=[(3.25,4.05),(3.25,4.50)]
fixed=[];sliding=[];ranges=[]
for a,b in windows:
 for width in [.15,.30]:
  fixed.append(compare(a,b,width))
  points=[]
  for delta in np.linspace(-.1,.1,201):
   v=compare(a+delta,b+delta,width);v['delta']=float(delta);v['base_window']=[a,b];sliding.append(v);points.append(v)
  ranges.append({'base_window':[a,b],'fwhm':width,'min_percent':min(v['change_percent'] for v in points),'max_percent':max(v['change_percent'] for v in points),'max_30_to_40_relative_area_change':max(abs(integral(m,a+d,b+d,width,40)['area']/integral(m,a+d,b+d,width,30)['area']-1) for d in np.linspace(-.1,.1,201) for m in ['U','X'])})
with (OUT/'sliding_window_integrals.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['base_lower_eV','base_upper_eV','FWHM_eV','shift_eV','lower_eV','upper_eV','area_U','area_X','relative_change_percent','centroid_shift_eV'])
 for s in sliding:w.writerow(s['base_window']+[s['fwhm'],s['delta'],s['lower'],s['upper'],s['U']['area'],s['X']['area'],s['change_percent'],s['centroid_shift_eV']])
# Check exact CDF integrals against dense-grid numerical integration at delta=0.
for s in fixed:
 for m in ['U','X']:
  E=np.linspace(s['lower'],s['upper'],20001);sigma=s['fwhm']/math.sqrt(8*math.log(2))
  y=sum(t['f']*np.exp(-.5*((E-t['E'])/sigma)**2)/(sigma*math.sqrt(2*math.pi)) for t in states[m])
  assert abs(np.trapezoid(y,E)-s[m]['area'])<1e-7
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','DejaVu Sans'],'font.size':9,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,'axes.linewidth':.7,'xtick.direction':'in','ytick.direction':'in','xtick.top':True,'ytick.right':True,'legend.frameon':False,'svg.fonttype':'none'})
fig,axs=plt.subplots(1,2,figsize=(6.5,2.7),sharey=True);fig.subplots_adjust(left=.10,right=.98,bottom=.22,top=.86,wspace=.15)
for ax,(a,b),letter in zip(axs,windows,'ab'):
 for width,color in [(.15,'#0072B2'),(.30,'#D55E00')]:
  pts=[s for s in sliding if s['base_window']==[a,b] and s['fwhm']==width]
  ax.plot([s['delta'] for s in pts],[s['change_percent'] for s in pts],color=color,lw=1.35,label=f'{width:.2f} eV')
 ax.axhline(0,color='#777777',lw=.6);ax.axvline(0,color='#999999',lw=.6,ls=':')
 ax.set(xlim=(-.10,.10),xticks=[-.1,-.05,0,.05,.1],xlabel=r'Window shift $\delta$ / eV',ylim=(-9,4),title=f'({letter})  {a:.2f}–{b:.2f} eV')
 ax.tick_params(length=3);ax.legend(title='FWHM',loc='lower left',fontsize=8,title_fontsize=8)
axs[0].set_ylabel(r'$(A_X-A_U)/A_U$ / %')
fig.savefig(OUT/'Figure_S1_sliding_windows.svg');fig.savefig(OUT/'Figure_S1_sliding_windows.png',dpi=500);plt.close(fig)
for row in fixed: print(row)
for row in ranges: print(row)
