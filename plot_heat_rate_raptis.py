# -*- coding: utf-8 -*-
"""
Created on Fri Aug 04 14:28:44 2017

@author: wangy
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from uniformstyle import uniformstyle
from read_pp_raptis import read_pp_raptis
from ismember import ismember


def straightline(x, x0, b, a):
     y = a + b*(x+x0)
     return y

def logcurve(x, x0, b, a):
     y = a + b*np.log(x+x0)
     return y

def sigmoid(x, x0, k, c):
     y = c / (1 + np.exp(k*(x+x0)))
     return y

coal_plants = read_pp_raptis()
# coal_plants = coal_plants.iloc[coal_plants.YEAR.values >= 2007]

##The power plants in countries do not differ systematically in thermal eff.
##groups = coal_plants.groupby('ISO') 
# Group by combustion and cooling technology
groups = coal_plants.groupby(['Tech','Cooling'])
groups2 = coal_plants.groupby('Tech')

techName = {'SUPERC': 'Supercritical', 'SUBCR': 'Subcritical' \
            , 'ULTRSC': 'Ultra-super', 'nan': 'Unknown'}
techList = ['SUBCR', 'SUPERC']
cooName = {'ot_saline': 'OT Saline', 'cl_fresh': 'CT Fresh' \
           , 'ot_fresh': 'OT Fresh', 'air': 'Air', 'CHP': 'CHP'}
##cooList = coal_plants.Cooling.unique()
cooList = ['cl_fresh','ot_fresh','air']

# Fit curves for the different combustion types
# ---- do not separate between cooling system types because the differences 
#      are not clear, but limit to ot_fresh, cl_fresh, and air
params = []
for tt in range(len(techList)):
    subset = ismember(techList, ['ot_fresh','cl_fresh','air'])
    #try:
    group = groups2.get_group(techList[tt])
    #except KeyError:
    #    continue
    no_nans = ~(np.isnan(group['Net_Eff'].values) \
              | np.isnan(group['Capacity'].values))

    xdata = pd.to_numeric(group.Capacity[no_nans])
    ydata = pd.to_numeric(group.Net_Eff[no_nans])
    # Log/Sigmoid/Linear fits
    if techList[tt]=='SUBCR':
        prms, pcovs = curve_fit(logcurve, xdata, ydata)
    else: 
        prms, pcovs = curve_fit(straightline, xdata, ydata)
    params.append(tuple(prms))

# Plot the relationship between size of the power plant and mean annual 
# cycle efficiency
# ---- draw the plot with fitted curves: limit to ct_fresh
clist = ['#05bc0e','#e83704','#000cff']

plt.style.use('classic')
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['axes.labelsize'] = 12
mpl.rcParams['legend.fontsize'] = 12
mpl.rcParams['figure.figsize'] = 8, 3.3 # change some settings from ggplot
fig, axes = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
count = 0
for tt in range(len(techList)):
    if (tt==1):
        locs = []
    ax = axes[tt-1]
    for cc in range(len(cooList)):
        if (cooList[cc]=='ot_fresh') | (cooList[cc]=='cl_fresh') \
           | (cooList[cc]=='air'):
            try:
                group = groups.get_group((techList[tt], cooList[cc]))
            except KeyError:
                continue
            temp = ax.scatter(group['Capacity'].values \
                              , group['Net_Eff'].values \
                              , edgecolor=clist[cc] \
                              , color='none' \
                              , linewidth=1.)
            if (tt==1):
                locs.append(temp)
            ax.set_xlim(left=-10, right=1100)
            ax.set_ylim(bottom=0.15, top=0.5)
            #ax.set_xscale('log', base=1.5)
            count = count+1
    xdummy = np.linspace(0, 1200, 50)
    if techList[tt]=='SUBCR':
        ax.plot(xdummy, logcurve(xdummy, *(params[tt])) \
                , linestyle = '-', color='k')
        ax.text(50., 0.2, "y=%1.2f%+2.1e*log(x%+2.1f)" \
                % (params[tt][2], params[tt][1], params[tt][0]) \
                   , fontsize=12, color='k')
    else:
        ax.plot(xdummy, straightline(xdummy, *(params[tt])) \
                , linestyle = '-', color='k')
        ax.text(50., 0.2, "y=%1.2f%+2.1e*(x%+2.1f)" \
                % (params[tt][2], params[tt][1], params[tt][0]) \
                   , fontsize=12, color='k')
    ax.set_xlabel('Nameplate Capacity (MW)')
    ax.set_title(techName[techList[tt]], size=12)
axes[0].set_ylabel('Net Efficiency')
lgd = ax.legend(locs,['Tower Freshwater','Once-through Freshwater','Air'] \
                , ncol=3, numpoints=1, loc='lower center', bbox_to_anchor=(1.,-.35) \
                , frameon=False)
fig.subplots_adjust(hspace=.2, wspace=.1)
plt.savefig('pp_MWx_efficiency_with_curves.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.close(fig)