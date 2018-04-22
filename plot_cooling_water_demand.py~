import pylab
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
sys.path.append('~/PythonModules')   
from util import day2month                                                
from scipy import stats

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
def get_CWD_annual_total(scenario, model_name, plant_ID, syear, capacity, capacity_factor):
    '''
    scenario: 'hist' | 'ssp2_rcp6p0' | 'ssp3_rcp6p0' 
    model_name: 'gfdl-esm2m' | 'ipsl-cm5a-lr' | 'miroc-esm-chem' | 'noresm1-m' | 'hadgem2-es'
    plant_ID: 'A' | 'B'
    capacity: Unit: [MW]
    capacity_factor: [-]
    '''
    cwd_day = np.fromfile('%s/wi_%s_%s_%s.bin' % (dir_cwd, scenario, model_name, plant_ID))    ### Unit: m3/MWH/day
    cwd_mon_day = np.array(day2month(cwd_day, datetime.datetime(syear, 1, 1)))
    cwd_mon_sum = np.array([mon.sum() for mon in cwd_mon_day]) 
    cwd_yea_sum = cwd_mon_sum.reshape(-1, 12).sum(-1)
    cwd_yea_sum = cwd_yea_sum*24*capacity*capacity_factor                                      ### Unit: m3/year
    
    return cwd_yea_sum

def get_CWD_annual_total_allPlant(scenario, model_name, plant_ID, syear, capacity, capacity_factor):
    '''
    scenario: 'hist' | 'ssp2_rcp6p0' | 'ssp3_rcp6p0' 
    model_name: 'gfdl-esm2m' | 'ipsl-cm5a-lr' | 'miroc-esm-chem' | 'noresm1-m' | 'hadgem2-es'
    plant_ID: array
    capacity: array (Unit: [MW])
    capacity_factor: [-]
    '''
    nPlant = np.shape(plant_ID)[0]
    cwd_yea_sum_allPlant = np.array([get_CWD_annual_total(scenario, model_name, plant_ID[i], syear, capacity[i], capacity_factor) for i in range(nPlant)])
    
    return cwd_yea_sum_allPlant

def linear_fit(syear, eyear, y):
    x = np.arange(syear, eyear+1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    y_fit = intercept + slope*x

    return slope, intercept, p_value, y_fit

dir_cwd = '/home/wind/hexg/Research/PECS/Data/Pakistan/streamflow_and_water_withdrawal'
dir_fig = '/home/wind/hexg/Research/PECS/Figures'

models = ['gfdl-esm2m', 'hadgem2-es', 'ipsl-cm5a-lr', 'miroc-esm-chem', 'noresm1-m']
plant_ID = ['A', 'B', 'C', 'D', 'E', 'G', 'H']
plant_capacity = [1320, 660, 330, 330, 1320, 1320, 1320] 

### Interpolate the capacity factor
cap_year = np.array([1970, 1980, 1990, 2000, 2005, 2010, 2013])
cap_fac = np.array([0.385, 0.393, 0.490, 0.423, 0.525, 0.552, 0.459])
cap_fac_avg = cap_fac.mean()

### Historical
cwd_hist_gfdl = get_CWD_annual_total_allPlant('hist', models[0], plant_ID, 1951, plant_capacity, cap_fac_avg).sum(0)
cwd_hist_ipsl = get_CWD_annual_total_allPlant('hist', models[1], plant_ID, 1951, plant_capacity, cap_fac_avg).sum(0)
cwd_hist_miro = get_CWD_annual_total_allPlant('hist', models[2], plant_ID, 1951, plant_capacity, cap_fac_avg).sum(0)
cwd_hist_nore = get_CWD_annual_total_allPlant('hist', models[3], plant_ID, 1951, plant_capacity, cap_fac_avg).sum(0)
cwd_hist_hadg = get_CWD_annual_total_allPlant('hist', models[4], plant_ID, 1951, plant_capacity, cap_fac_avg).sum(0)

### SSP2
cwd_ssp2_gfdl = get_CWD_annual_total_allPlant('rcp6p0', models[0], plant_ID, 2005, plant_capacity, cap_fac_avg).sum(0)
cwd_ssp2_ipsl = get_CWD_annual_total_allPlant('rcp6p0', models[1], plant_ID, 2005, plant_capacity, cap_fac_avg).sum(0)
cwd_ssp2_miro = get_CWD_annual_total_allPlant('rcp6p0', models[2], plant_ID, 2005, plant_capacity, cap_fac_avg).sum(0)
cwd_ssp2_nore = get_CWD_annual_total_allPlant('rcp6p0', models[3], plant_ID, 2005, plant_capacity, cap_fac_avg).sum(0)
cwd_ssp2_hadg = get_CWD_annual_total_allPlant('rcp6p0', models[4], plant_ID, 2005, plant_capacity, cap_fac_avg).sum(0)

### Append historical and future data (1971 to 2055)
cwd_gfdl = np.append(cwd_hist_gfdl[20:], cwd_ssp2_gfdl[:51])
cwd_ipsl = np.append(cwd_hist_ipsl[20:], cwd_ssp2_ipsl[:51])
cwd_miro = np.append(cwd_hist_miro[20:], cwd_ssp2_miro[:51])
cwd_nore = np.append(cwd_hist_nore[20:], cwd_ssp2_nore[:51])
cwd_hadg = np.append(cwd_hist_hadg[20:], cwd_ssp2_hadg[:51])

cwd = np.array([cwd_gfdl, cwd_ipsl, cwd_miro, cwd_nore, cwd_hadg])

### Figures with 5 panels
fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(15, 10))

colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']
color_vline = '#ABABAD'

for i in range(5):

    ### Linear regression
    slp_hist, int_hist, pva_hist, cwd_fit_hist = linear_fit(1971, 2004, cwd[i][:34])
    slp_ssp2, int_ssp2, pva_ssp2, cwd_fit_ssp2 = linear_fit(2005, 2055, cwd[i][34:])

    axes[i].plot(cwd_gfdl, color='grey', alpha=0.6)
    axes[i].plot(cwd_ipsl, color='grey', alpha=0.6)
    axes[i].plot(cwd_miro, color='grey', alpha=0.6)
    axes[i].plot(cwd_nore, color='grey', alpha=0.6)
    axes[i].plot(cwd_hadg, color='grey', alpha=0.6)
    axes[i].plot(np.arange(0, 35), cwd[i][:35], linewidth=3, color=colors[i], alpha=0.6)
    axes[i].plot(np.arange(34,85), cwd[i][34:], linewidth=3, color=colors[i], alpha=1.0)
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
    axes[i].set_ylim([79000000, 80000000])                           ### For all plants
    axes[i].set_yticks([79200000, 79500000, 79800000])               ### For all plants 
    axes[i].set_yticklabels([79.2, 79.5, 79.8])                      ### For all plants
    axes[i].axvspan(0, 34, facecolor='#D6D5D5', alpha=0.2)
    axes[i].axvspan(34, 85, facecolor='#D6D5D5', alpha=0.6)
    axes[i].text(0.01, 0.9, models[i].upper(), fontsize=12.5, color=colors[i], horizontalalignment='left', verticalalignment='center', transform=axes[i].transAxes)
    axes[i].text(0.120, 0.06, "trend=%4.3f m$^3$/year, $p=%4.3f$" % (slp_hist, pva_hist), fontsize=12.5, ha='left', va='center', transform=axes[i].transAxes, alpha=0.8)
    axes[i].text(0.555, 0.06, "trend=%4.3f m$^3$/year, $p=%4.3f$" % (slp_ssp2, pva_ssp2), fontsize=12.5, ha='left', va='center', transform=axes[i].transAxes, alpha=0.8)
    axes[i].plot(np.arange(0, 34), cwd_fit_hist, ls='--', linewidth=3, color=colors[i], alpha=0.6)
    axes[i].plot(np.arange(34, 85), cwd_fit_ssp2, ls='--', linewidth=3, color=colors[i], alpha=1.0)

axes[2].set_ylabel('Cooling water demand [$10^6$ m$^3$]')
axes[4].set_xticks(np.arange(4, 85, 10))
axes[4].set_xticklabels(np.arange(1975, 2056, 10))

plt.subplots_adjust(hspace=0.1)

plt.savefig('%s/cooling_water_demand_allPlant_ts_1971_2055.pdf' % (dir_fig))

plt.show()
