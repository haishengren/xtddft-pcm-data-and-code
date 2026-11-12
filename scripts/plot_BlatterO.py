"""Blatter-O Figure 9; experimental digitization: DOI 10.1002/anie.201605612."""
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
parser.add_argument('--output', type=Path, default=Path('figures'))
parser.add_argument('--experimental-data', type=Path, default=None,
                    help='Optional digitized spectrum CSV with columns wavelength_nm,log10_extinction')
args = parser.parse_args()
OUT = args.output
OUT.mkdir(parents=True,exist_ok=True)

U='#0072B2';X='#D55E00';GRAY='#9B9B9B';INK='#222222'
COL={'U':U,'X':X};LS={'U':'--','X':'-'};ZORDER={'U':2,'X':3};MC={'LR':U,'cLR':'#009E73','ptSS':'#8064A2','ptSS+CE':X}
HC=1239.841984
plt.rcParams.update({
    'font.family':'sans-serif','font.sans-serif':['Arial','DejaVu Sans'],
    'font.size':8.5,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,
    'legend.fontsize':8,'mathtext.fontset':'custom','mathtext.rm':'Arial',
    'mathtext.it':'Arial:italic','mathtext.bf':'Arial:bold','mathtext.fallback':'stixsans',
    'axes.linewidth':.7,'axes.edgecolor':INK,'axes.labelcolor':INK,
    'xtick.direction':'in','ytick.direction':'in','xtick.top':True,'ytick.right':True,
    'xtick.major.size':3,'ytick.major.size':3,'xtick.minor.size':1.7,'ytick.minor.size':1.7,
    'xtick.major.width':.65,'ytick.major.width':.65,'xtick.minor.width':.5,'ytick.minor.width':.5,
    'legend.frameon':False,'legend.handlelength':2,'legend.borderaxespad':.4,
    'lines.linewidth':1.15,'lines.markersize':4,'svg.fonttype':'none',
    'savefig.facecolor':'white','figure.facecolor':'white','axes.unicode_minus':True,
})
AUDIT={}

spectrum_rows = read_states('BlatterO_LR_spectrum.csv')
APP = {'BlatterO_'+m: {'states': [r for r in spectrum_rows if r['method']==m]} for m in ['U','X']}

EXPERIMENTAL = None
if args.experimental_data is not None:
    if not args.experimental_data.is_file():
        parser.error(f'Experimental data file not found: {args.experimental_data}')
    with args.experimental_data.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    required = {'wavelength_nm', 'log10_extinction'}
    if not rows or not required.issubset(rows[0]):
        parser.error('Experimental CSV must contain wavelength_nm and log10_extinction columns')
    EXPERIMENTAL = np.array([[float(r['wavelength_nm']), float(r['log10_extinction'])]
                             for r in rows])

def panel(ax,letter):
    box=ax.get_position()
    ax.figure.text(max(.02,box.x0-.05),box.y1+.012,'('+letter+')',weight='bold',fontsize=9.5,va='bottom')

def finish(fig,stem):
    fig.savefig(OUT/(stem+'.svg'))
    fig.savefig(OUT/(stem+'.png'),dpi=600)
    plt.close(fig)

def spectrum(states,wavelength,fwhm):
    sig=fwhm/math.sqrt(8*math.log(2));ee=HC/wavelength
    return sum(s['f']*np.exp(-.5*((ee-s['E'])/sig)**2) for s in states)/(sig*math.sqrt(2*math.pi))

def figure8():
    lam=np.linspace(260,730,1881)
    if EXPERIMENTAL is not None:
        raw=np.array(EXPERIMENTAL);raw=raw[raw[:,0]<=730];raw=raw[np.argsort(raw[:,0])]
        exp=10**np.interp(lam,raw[:,0],raw[:,1]);exp/=exp.max()
    fig,axs=plt.subplots(2,2,figsize=(6.69,4.85));fig.subplots_adjust(left=.10,right=.98,bottom=.11,top=.94,wspace=.30,hspace=.43)
    for j,w in enumerate([.15,.30]):
        ax=axs[0,j];panel(ax,'ab'[j]);ax.axvspan(HC/4.05,HC/3.25,color='#EFEFEF',zorder=0)
        if EXPERIMENTAL is not None:
            ax.plot(lam,exp,color=INK,lw=1,label='Exp.')
        else:
            ax.text(.03,.94,'Experimental spectrum not bundled',ha='left',va='top',
                    transform=ax.transAxes,fontsize=7,color=GRAY)
        curves={m:spectrum(APP['BlatterO_'+m]['states'],lam,w) for m in ['U','X']};norm=max(a.max() for a in curves.values())
        for m in ['U','X']:ax.plot(lam,curves[m]/norm,color=COL[m],lw=1.05,ls=LS[m],zorder=ZORDER[m],label=m+'-TDDFT')
        ax.set(xlim=(260,730),ylim=(0,1.12),xlabel=r'$\lambda$ / nm',ylabel='Relative absorption')
        ax.set_xticks([300,400,500,600,700]);ax.set_yticks([0,.5,1]);ax.xaxis.set_minor_locator(MultipleLocator(50))
        ax.text(.97,.94,f'FWHM {w:.2f} eV',ha='right',va='top',transform=ax.transAxes,fontsize=8)
        if j==0:ax.legend(loc='upper right',bbox_to_anchor=(1,.84),fontsize=7.5,labelspacing=.25,handlelength=1.65)
    windows={}
    for j,m in enumerate(['U','X']):
        ax=axs[1,j];panel(ax,'cd'[j]);ax.axvspan(3.25,4.05,color='#EFEFEF',zorder=0)
        states=[s for s in APP['BlatterO_'+m]['states'] if 3.25<=s['E']<=4.5]
        for s in states:
            ax.vlines(s['E'],0,s['f'],color=COL[m],lw=1.25)
            if (m=='U' and s['root'] in [16,20]) or (m=='X' and s['root'] in [14,17]):
                ax.annotate(m+str(s['root']),(s['E'],s['f']),xytext=(-2,4),textcoords='offset points',ha='right',va='bottom',fontsize=8,color=COL[m])
        ax.set(xlim=(3.2,4.55),ylim=(0,.40),xlabel=r'$\omega^{\mathrm{LR}}$ / eV',ylabel=r'$f_I$')
        ax.set_xticks([3.25,3.5,3.75,4,4.25,4.5]);ax.set_xticklabels(['3.25','3.50','3.75','4.00','4.25','4.50']);ax.set_yticks([0,.1,.2,.3]);ax.xaxis.set_minor_locator(MultipleLocator(.125))
        ax.text(.04,.94,m+'-TDDFT',ha='left',va='top',transform=ax.transAxes,fontsize=8,color=COL[m])
        windows[m]={}
        for hi in [4.05,4.5]:
            ss=[s for s in states if s['E']<=hi];total=sum(s['f'] for s in ss);center=sum(s['E']*s['f'] for s in ss)/total
            windows[m][str(hi)]={'roots':[s['root'] for s in ss],'sum_f':total,'weighted_center':center}
    assert abs(windows['U']['4.05']['sum_f']-.5574)<1e-8 and abs(windows['X']['4.5']['sum_f']-1.1034)<1e-8
    AUDIT['figure8']={'window_statistics':windows,'fwhm_eV':[.15,.30],
                     'wavelength_range_nm':[260,730],
                     'experimental_processing':('interpolate log10(extinction), exponentiate, normalize; '
                         'U/X share one maximum at each FWHM' if EXPERIMENTAL is not None
                         else 'experimental spectrum omitted; see data/THIRD_PARTY_DATA.md')}
    finish(fig,'Figure9_BlatterO_absorption')

if __name__=='__main__':
    figure8()
