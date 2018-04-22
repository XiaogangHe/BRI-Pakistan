import pylab
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
sys.path.append('~/PythonModules')   
from util import day2month                                                
from scipy import stats
from netCDF4 import Dataset

params = {'backend': 'ps',
          'axes.labelsize': 20,
          'grid.linewidth': 0.2,
          'font.size': 20,
          'legend.fontsize': 16,
          'legend.frameon': False,
          'xtick.labelsize': 16,
          'xtick.direction': 'in',
          'ytick.labelsize': 16,
          'ytick.direction': 'out',
          'savefig.bbox': 'tight',
          'text.usetex': False}
pylab.rcParams.update(params)

### Functions

def linear_fit(syear, eyear, y):
    x = np.arange(syear, eyear+1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    y_fit = intercept + slope*x

    return slope, intercept, p_value, y_fit

dir_wsi = '~/Research/PECS/Data/Pakistan/WSI'
dir_fig = '~/Research/PECS/Figures'

models = ['gfdl-esm2m', 'hadgem2-es', 'ipsl-cm5a-lr', 'miroc-esm-chem', 'noresm1-m']

### Historical
wsi_hist_gfdl = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[0])).variables['wsi'][:]
wsi_hist_ipsl = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[1])).variables['wsi'][:]
wsi_hist_miro = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[2])).variables['wsi'][:]
wsi_hist_nore = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[3])).variables['wsi'][:]
wsi_hist_hadg = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[4])).variables['wsi'][:]

### SSP2
wsi_ssp2_gfdl = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[0])).variables['wsi'][:]
wsi_ssp2_ipsl = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[1])).variables['wsi'][:]
wsi_ssp2_miro = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[2])).variables['wsi'][:]
wsi_ssp2_nore = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[3])).variables['wsi'][:]
wsi_ssp2_hadg = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[4])).variables['wsi'][:]

### Append historical and future data to get the time series (1971 to 2055)
wsi_gfdl = np.append(wsi_hist_gfdl.mean(-1).mean(-1), wsi_ssp2_gfdl.mean(-1).mean(-1))
wsi_ipsl = np.append(wsi_hist_ipsl.mean(-1).mean(-1), wsi_ssp2_ipsl.mean(-1).mean(-1))
wsi_miro = np.append(wsi_hist_miro.mean(-1).mean(-1), wsi_ssp2_miro.mean(-1).mean(-1))
wsi_nore = np.append(wsi_hist_nore.mean(-1).mean(-1), wsi_ssp2_nore.mean(-1).mean(-1))
wsi_hadg = np.append(wsi_hist_hadg.mean(-1).mean(-1), wsi_ssp2_hadg.mean(-1).mean(-1))

wsi = np.array([wsi_gfdl, wsi_ipsl, wsi_miro, wsi_nore, wsi_hadg])

### Figures with 5 panels
fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(15, 10))

colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']
color_vline = '#ABABAD'

for i in range(5):

    ### Linear regression
    slp_hist, int_hist, pva_hist, wsi_fit_hist = linear_fit(1971, 2004, wsi[i][:34])
    slp_ssp2, int_ssp2, pva_ssp2, wsi_fit_ssp2 = linear_fit(2005, 2055, wsi[i][34:])

    axes[i].plot(wsi_gfdl, color='grey', alpha=0.6)
    axes[i].plot(wsi_ipsl, color='grey', alpha=0.6)
    axes[i].plot(wsi_miro, color='grey', alpha=0.6)
    axes[i].plot(wsi_nore, color='grey', alpha=0.6)
    axes[i].plot(wsi_hadg, color='grey', alpha=0.6)
    axes[i].plot(np.arange(0, 35), wsi[i][:35], linewidth=3, color=colors[i], alpha=0.6)
    axes[i].plot(np.arange(34,85), wsi[i][34:], linewidth=3, color=colors[i], alpha=1.0)
    axes[i].spines['top'].set_visible(False)
    axes[i].spines['bottom'].set_visible(False)
    axes[i].spines['right'].set_visible(False)
    axes[i].spines['left'].set_linewidth(2)
    axes[i].xaxis.tick_bottom()
    axes[i].yaxis.tick_left()
    axes[i].set_xticks([])
    axes[i].set_xticklabels([])
    axes[i].xaxis.set_ticks_position('none')
    axes[i].axvline(x=4, c=color_vline)
    axes[i].axvline(x=14, c=color_vline)
    axes[i].axvline(x=24, c=color_vline)
    axes[i].axvline(x=34, c=color_vline)
    axes[i].axvline(x=44, c=color_vline)
    axes[i].axvline(x=54, c=color_vline)
    axes[i].axvline(x=64, c=color_vline)
    axes[i].axvline(x=74, c=color_vline)
    axes[i].axvline(x=84, c=color_vline)
    axes[i].set_xlim([-1, 84]) 
    axes[i].set_ylim([0.15, 0.55])       
    axes[i].set_yticks([0.25, 0.45]) 
    axes[i].set_yticklabels([0.25, 0.45]) 
    axes[i].axvspan(0, 34, facecolor='#D6D5D5', alpha=0.2)
    axes[i].axvspan(34, 85, facecolor='#D6D5D5', alpha=0.6)
    axes[i].text(0.01, 0.9, models[i].upper(), fontsize=12.5, color=colors[i], horizontalalignment='left', verticalalignment='center', transform=axes[i].transAxes)
    axes[i].text(0.160, 0.9, "trend=%4.3f/year, $p=%4.3f$" % (slp_hist, pva_hist), fontsize=12.5, ha='left', va='center', transform=axes[i].transAxes, alpha=0.8)
    axes[i].text(0.555, 0.9, "trend=%4.3f/year, $p=%4.3f$" % (slp_ssp2, pva_ssp2), fontsize=12.5, ha='left', va='center', transform=axes[i].transAxes, alpha=0.8)
    axes[i].plot(np.arange(0, 34), wsi_fit_hist, ls='--', linewidth=3, color=colors[i], alpha=0.6)
    axes[i].plot(np.arange(34, 85), wsi_fit_ssp2, ls='--', linewidth=3, color=colors[i], alpha=1.0)

axes[2].set_ylabel('Water stress index [-]')
axes[4].set_xticks(np.arange(4, 85, 10))
axes[4].set_xticklabels(np.arange(1975, 2056, 10))

plt.subplots_adjust(hspace=0.1)

plt.savefig('%s/wsi_average_ts_1971_2055.pdf' % (dir_fig))

plt.show()

