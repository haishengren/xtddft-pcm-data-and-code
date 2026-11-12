"""Figures 7–8: fixed-geometry gas-to-solution comparisons from CSV tables."""
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

d = {'benzyl': read_table('Benzyl_solvent_shifts.csv'), 'BlatterO': read_table('BlatterO_solvent_shifts.csv')}

blatter_energies = {(r['method'], r['treatment'], r['root']): r['E'] for r in read_states('BlatterO_gas_LR_energies.csv')}

U='#0072B2';X='#D55E00';G='#009E73'
plt.rcParams.update({'font.family':'Arial','font.size':8,'axes.labelsize':9,
 'axes.linewidth':.7,'xtick.direction':'in','ytick.direction':'in',
 'xtick.top':True,'ytick.right':True,'legend.frameon':False,'legend.fontsize':7.5,
 'lines.linewidth':1.2,'svg.fonttype':'none','savefig.facecolor':'white'})
def save(fig,name):
 fig.savefig(OUT/(name+'.png'),dpi=600,bbox_inches='tight')
 fig.savefig(OUT/(name+'.svg'),bbox_inches='tight')
 plt.close(fig)
def tag(ax,t):ax.text(-.12,1.04,t,transform=ax.transAxes,fontweight='bold',fontsize=10)
b={r['state_in_solution']:r for r in d['benzyl']}
fig,axs=plt.subplots(1,3,figsize=(7.1,2.55),gridspec_kw={'width_ratios':[1,1.05,1.2]})
fig.subplots_adjust(wspace=.52,bottom=.23,top=.82)
ax=axs[0];tag(ax,'(a)')
for state,color,ls,mark in [('U4',U,'--','o'),('X6',X,'-','s'),('U5',U,'--','o'),('X4',X,'-','s')]:
 r=b[state];ax.plot([0,1],[r['gas_Rsolv'],r['LR']],ls,marker=mark,color=color,markersize=3.4,zorder=3 if state.startswith('X') else 2)
 y=r['LR']+(0.055 if state=='X4' else -.06 if state=='U5' else 0)
 ax.text(1.08,y,state,va='center',fontsize=7.5,color=color)
ax.set(xlim=(-.2,1.65),ylim=(4.12,5.6),xticks=[0,1],xticklabels=['Gas','LR / CHX'],ylabel='Excitation energy / eV')
ax.legend(handles=[Line2D([],[],color=U,ls='--',label='U'),Line2D([],[],color=X,ls='-',label='X')],loc='upper left',ncol=2,bbox_to_anchor=(0,1.24))
ax=axs[1];tag(ax,'(b)');xx=np.arange(3)
for state,col,ls,mk in [('U5',U,'--','o'),('X4',X,'-','s')]:
 r=b[state];vals=[r['reference_shift'],r['LR_kernel_shift'],r['total_LR']]
 ax.plot(xx,vals,color=col,ls=ls,marker=mk,markersize=4,zorder=3 if state[0]=='X' else 2,label=state)
ax.axhline(0,color='.6',lw=.6);ax.set(xticks=xx,xticklabels=['fr − gas','LR − fr','LR − gas'],ylabel='Energy shift / eV',ylim=(-.16,.025))
ax.tick_params(axis='x',labelrotation=25);ax.legend(loc='upper right')
ax=axs[2];tag(ax,'(c)');xx=np.arange(5)
for state,col,ls,mk in [('U5',U,'--','o'),('X4',X,'-','s')]:
 r=b[state];vals=[1239.841984/r[k] for k in ['gas_Rsolv','fr','LR','cLR','ptSS_CE']]
 ax.plot(xx,vals,color=col,ls=ls,marker=mk,markersize=4,zorder=3 if state[0]=='X' else 2,label=state)
ax.axhline(258,color='.25',ls=':',lw=1,label='Experiment')
ax.set(xticks=xx,xticklabels=['Gas','fr','LR','cLR','ptSS+CE'],ylabel='Wavelength / nm',ylim=(254,267))
ax.tick_params(axis='x',labelrotation=35);ax.legend(loc='lower left',bbox_to_anchor=(-.07,1.02),ncol=3,fontsize=6.8,columnspacing=.5,handlelength=1.1)
save(fig,'Figure7_Benzyl_gas_solution')
fig,axs=plt.subplots(1,2,figsize=(6.8,2.65),gridspec_kw={'width_ratios':[1.6,1]})
fig.subplots_adjust(wspace=.4,bottom=.2,top=.8)
ax=axs[0];tag(ax,'(a)');rows=d['BlatterO'];xx=np.arange(len(rows));w=.24
ax.bar(xx-w,[r['reference_shift'] for r in rows],w,color='#9DADBA',label='fr − gas')
ax.bar(xx,[r['LR_kernel_shift'] for r in rows],w,color=G,label='LR − fr')
ax.bar(xx+w,[r['total_LR'] for r in rows],w,color=X,label='LR − gas')
ax.axhline(0,color='.25',lw=.65);ax.set(xticks=xx,xticklabels=[r['state_in_solution'] for r in rows],ylabel='Energy shift / eV',ylim=(-.05,.13))
ax.legend(ncol=3,loc='lower left',bbox_to_anchor=(-.03,1.015),columnspacing=.9,handlelength=1.1)
ax=axs[1];tag(ax,'(b)')
for method,col,ls,mk in [('U',U,'--','o'),('X',X,'-','s')]:
 gas=blatter_energies[(method,'gas',2)]
 lr=blatter_energies[(method,'LR',2)]
 ax.plot([0,1],[1239.841984/gas,1239.841984/lr],color=col,ls=ls,marker=mk,markersize=4,label=method,zorder=3 if method=='X' else 2)
ax.axhline(616,color='.25',ls=':',lw=1,label='Experiment')
ax.set(xticks=[0,1],xticklabels=['Gas','LR / DCM'],xlim=(-.2,1.2),ylim=(584,624),ylabel='Wavelength / nm')
ax.legend(ncol=3,loc='lower left',bbox_to_anchor=(-.08,1.015),columnspacing=.7,handlelength=1.3)
save(fig,'Figure8_Blatter_solvent_shifts')
