"""NH2 Figures 4–6 and vacuum-limit fits, using CSV data in data/."""
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

excitation_rows = read_states('NH2_excitation_energies.csv')
NH = {'vacuum': read_table('NH2_vacuum_limit.csv'), 'main': {
    method+'_'+mode: [r for r in excitation_rows if r['method']==method and r['treatment']==mode]
    for method in ['U','X'] for mode in ['fr','LR']}}

GAS = {m: {str(r['root']): r for r in excitation_rows
                  if r['method']==m and r['treatment']=='gas'} for m in ['U','X']}

transition_dipoles = {r['state']: r for r in read_table('NH2_transition_dipoles.csv')}

difference_dipoles = {r['state']: r for r in read_table('NH2_difference_dipoles.csv') if r['density_reference']=='fr'}

SS = {r['state']: r for r in read_table('NH2_state_specific.csv')}

def state(name,mode='LR'):
    return next(s for s in NH['main'][name[0]+'_'+mode] if s['root']==int(name[1:]))

def panel(ax,letter):
    box=ax.get_position()
    ax.figure.text(max(.02,box.x0-.05),box.y1+.012,'('+letter+')',weight='bold',fontsize=9.5,va='bottom')

def zero(ax):ax.axhline(0,color='#777777',lw=.65,zorder=0)

def finish(fig,stem):
    fig.savefig(OUT/(stem+'.svg'))
    fig.savefig(OUT/(stem+'.png'),dpi=600)
    plt.close(fig)

def figure4():
    fig,ax=plt.subplots(figsize=(3.55,2.8))
    fig.subplots_adjust(left=.19,right=.97,bottom=.20,top=.97)
    rows=sorted(NH['vacuum'],key=lambda r:r['epsilon'])
    xx=np.array([r['epsilon']-1 for r in rows])
    for m,col,mark,ls,ms in [('U',U,'o',LS['U'],5.2),('X',X,'^',LS['X'],3.8)]:
        yy=np.array([r[m] for r in rows])
        ax.loglog(xx,yy,color=col,marker=mark,ls=ls,ms=ms,mfc='white',mew=.85,label=m+'-TDDFT',zorder=ZORDER[m])
    ax.loglog(xx,.045*xx,':',color='#777777',lw=.85,label='Slope 1',zorder=0)
    ax.set(xlabel=r'$\varepsilon-1$',ylabel=r'$d_{\max}$ / eV',xlim=(6e-7,.16),ylim=(2.8e-8,.045))
    ax.legend(loc='upper left',fontsize=7.7)
    ax.xaxis.set_major_locator(LogLocator(base=10,numticks=8));ax.yaxis.set_major_locator(LogLocator(base=10,numticks=8))
    ax.xaxis.set_minor_locator(LogLocator(base=10,subs=[2,5]));ax.yaxis.set_minor_locator(LogLocator(base=10,subs=[2,5]))
    ax.xaxis.set_minor_formatter(NullFormatter());ax.yaxis.set_minor_formatter(NullFormatter())
    AUDIT['figure4']={'epsilon_minus_one':xx.tolist(),'U':[r['U'] for r in rows],'X':[r['X'] for r in rows],'axes':'log-log; no zero data point added'}
    finish(fig,'Figure4_NH2_vacuum_limit')

def figure5():
    fig=plt.figure(figsize=(6.69,5.12));gs=fig.add_gridspec(2,2,height_ratios=[1,1.12],left=.10,right=.98,bottom=.16,top=.95,wspace=.34,hspace=.50)
    ax=fig.add_subplot(gs[0,0]);panel(ax,'a')
    for j,(m,roots) in enumerate([('U',[3,5]),('X',[4,7])]):
        for root in roots:
            name=m+str(root);s=state(name)
            ax.hlines(s['E'],j-.24,j+.24,color=COL[m],lw=1.5)
            ax.text(j,s['E']+.06,name,ha='center',va='bottom',color=COL[m],fontsize=8)
    ax.set(xlim=(-.65,1.65),ylim=(6.9,9.1),xticks=[0,1],xticklabels=['U-TDDFT','X-TDDFT'],ylabel=r'$\omega^{\mathrm{LR}}$ / eV')
    ax.tick_params(axis='x',length=0,top=False,pad=5);ax.yaxis.set_major_locator(MultipleLocator(.5));ax.yaxis.set_minor_locator(MultipleLocator(.1))
    ax=fig.add_subplot(gs[0,1]);panel(ax,'b')
    names=['U3','X4','U5','X7'];xpos=[0,.8,2.1,2.9]
    for name,x in zip(names,xpos):ax.bar(x,state(name)['f']/state(name)['E'],width=.52,color=COL[name[0]],edgecolor=COL[name[0]],lw=.5)
    ax.set(xticks=xpos,xticklabels=names,xlim=(-.6,3.5),ylim=(0,.0133),ylabel=r'$f_I/\omega_I$ / eV$^{-1}$')
    ax.set_yticks([0,.004,.008,.012]);ax.tick_params(axis='x',length=0,top=False)
    for x,label in [(.4,'Lower'),(2.5,'Upper')]:ax.text(x,-.19,label,transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=8)
    ax=fig.add_subplot(gs[1,:]);panel(ax,'c')
    names=['U1','X1','U4','X3','U7','X6','U3','U5','X4','X7']
    xs=np.array([0,.75,2,2.75,4,4.75,6,6.75,7.5,8.25])
    frgas=[state(n,'fr')['E']-GAS[n[0]][n[1:]]['E'] for n in names]
    lrfr=[state(n)['E']-state(n,'fr')['E'] for n in names]
    # Gas-to-frozen changes are already tabulated. Here resolve the smaller kernel shifts.
    ax.bar(xs,lrfr,width=.48,color=[COL[n[0]] for n in names],zorder=2)
    zero(ax);ax.set(xticks=xs,xticklabels=names,ylabel=r'$\Delta_{\mathrm{corr}}^{\mathrm{LR}}$ / eV',xlim=(-.55,8.8),ylim=(-.048,.003))
    ax.set_yticks([-.04,-.03,-.02,-.01,0]);ax.yaxis.set_minor_locator(MultipleLocator(.005));ax.tick_params(axis='x',length=0,top=False)
    for xc,lab in [(.375,r'CO $4\to5$'),(2.375,r'OV $5\to6$'),(4.375,r'OV $5\to7$'),(7.125,r'CV $4\to6$')]:
        ax.text(xc,-.21,lab,transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=8)
    AUDIT['figure5']={'states':names,'fr_minus_gas':frgas,'LR_minus_fr':lrfr,
        'CV_LR':{n:{'energy':state(n)['E'],'f':state(n)['f'],'f_over_energy':state(n)['f']/state(n)['E']} for n in ['U3','U5','X4','X7']}}
    finish(fig,'Figure5_NH2_spin_and_response')

def figure6():
    names=['U1','X1','U7','X6','X7'];x=np.array([0,.8,2.1,2.9,4.2]);dip=transition_dipoles
    fig=plt.figure(figsize=(6.69,4.72));gs=fig.add_gridspec(2,2,height_ratios=[1,1.15],left=.10,right=.98,bottom=.11,top=.95,wspace=.34,hspace=.45)
    ax=fig.add_subplot(gs[0,0]);panel(ax,'a')
    ax.bar(x,[2.541746473*dip[n]['transition_norm_au'] for n in names],width=.48,color=[COL[n[0]] for n in names])
    ax.set(xticks=x,xticklabels=names,xlim=(-.55,4.75),ylim=(0,.92),ylabel=r'$|\boldsymbol{\mu}_{0I}|$ / D')
    ax.set_yticks([0,.3,.6,.9]);ax.tick_params(axis='x',length=0,top=False)
    ax=fig.add_subplot(gs[0,1]);panel(ax,'b')
    mu=[difference_dipoles[n]['delta_mu_rel_D_z'] for n in names]
    ax.bar(x,mu,width=.48,color=[COL[n[0]] for n in names]);zero(ax)
    ax.set(xticks=x,xticklabels=names,xlim=(-.55,4.75),ylim=(-4.05,.15),ylabel=r'$\Delta\mu_{I,z}^{\mathrm{fr}}$ / D')
    ax.set_yticks([-4,-3,-2,-1,0]);ax.tick_params(axis='x',length=0,top=False)
    ax=fig.add_subplot(gs[1,:]);panel(ax,'c')
    corrections={m:[SS[n]['delta_'+k] for n in names] for m,k in [('LR','LR'),('cLR','cLR'),('ptSS','ptSS'),('ptSS+CE','ptSS_CE')]}
    xx=np.arange(len(names))
    for j,(m,values) in enumerate(corrections.items()):ax.bar(xx+(j-1.5)*.18,values,width=.17,color=MC[m],label=m)
    zero(ax);ax.set(xticks=xx,xticklabels=names,ylim=(-.425,.055),xlim=(-.55,4.55),ylabel=r'$\Delta_{\mathrm{corr}}^{m}$ / eV')
    ax.set_yticks([-.4,-.3,-.2,-.1,0]);ax.yaxis.set_minor_locator(MultipleLocator(.05));ax.tick_params(axis='x',length=0,top=False)
    ax.legend(loc='upper right',ncol=4,handlelength=1.15,columnspacing=1.25,fontsize=8)
    AUDIT['figure6']={'states':names,'transition_norm_au':[dip[n]['transition_norm_au'] for n in names],'delta_mu_fr_z_D':mu,'corrections_from_fr_eV':corrections}
    finish(fig,'Figure6_NH2_density_response')

if __name__=='__main__':
    figure4();figure5();figure6()
    for m in ['U','X']:
        x=np.array([r['epsilon']-1 for r in NH['vacuum']])
        y=np.array([r[m] for r in NH['vacuum']])
        for mask,label in [(np.ones(len(x),dtype=bool),'all five points'),(x<.00101,'three near-vacuum points')]:
            slope,intercept=np.polyfit(x[mask],y[mask],1)
            print(m,label,'slope =',slope,'intercept / eV =',intercept)
