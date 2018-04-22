# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 07:26:22 2017

@author: wangy

Calculate the water use intensity of the eight Pakistan power plants for
He Xiaogang.
"""
from extract_met3 import extract_met
from extract_wat import extract_wat
import eflow as ef
import glob2
import os
import numpy as np
import pandas as pd
import itertools as it
import bartos_chester as bc
from read_pp import read_pp2
from cooling_params import *

gcms = ['gfdl-esm2m', 'hadgem2-es', 'ipsl-cm5a-lr', 'miroc-esm-chem', 'noresm1-m']
scn = ['hist','rcp6p0']
out_path = os.path.join(os.path.realpath('.'), 'output', 'hexiaogang')
dates = {'hist': pd.date_range('1951-01-01', '2004-12-31') \
         , 'rcp6p0': pd.date_range('2006-01-01', '2099-12-31')}
mask = ['Mask13', 'Mask16', 'Mask17']
path_to_wat = os.path.join(os.path.realpath('..' + os.sep + '..' + os.sep \
                                            + '..'), 'watxene' \
                           , 'Wat-Data', 'wattemp', 'waterTemp_real')
gcms_fl = {'gfdl-esm2m': 'GFDL-ESM2M', 'hadgem2-es': 'HadGEM2-ES', \
           'ipsl-cm5a-lr' : 'IPSL-CM5A-LR', 'miroc-esm-chem': \
           'MIROC-ESM-CHEM', 'noresm1-m': 'NorESM1-M'}
discharge_name = {'hist': 'discharge_dailyTot_output_hist.nc' \
                  , 'rcp6p0': 'discharge_dailyTot_output.nc'}
wtemp_name = {'hist': 'waterTemp_dailyTot_hist.nc' \
              , 'rcp6p0': 'waterTemp_dailyTot.nc'}

stations = [['A','Supercritical', 1320, 24.7854, 67.3695, \
             0.30+4.3e-5*np.log(1320 + 2475.0)], 
            ['B','Subcritical', 660, 24.4338, 70.1736, \
             0.24+2.6e-2*np.log(660 + 5.4)], \
            ['C','Subcritical', 330, 24.8408, 70.3151, \
             0.24+2.6e-2*np.log(330 + 5.4)], \
            ['D','Subcritical', 330, 24.8408, 70.3151, \
             0.24+2.6e-2*np.log(330 + 5.4)], \
            ['E','Supercritical', 1320, 30.7196, 73.2359, \
             0.30+4.3e-5*np.log(1320 + 2475.0)], \
            ['F','Supercritical', 300, 25.1080, 62.3466, \
             0.30+4.3e-5*np.log(300 + 2475.0)], \
            ['G','Subcritical',1320, 24.6970, 70.1790, \
             0.24+2.6e-2*np.log(1320 + 5.4)], \
            ['H','Supercritical',1320, 24.9057, 66.6944, \
             0.30+4.3e-5*np.log(1320 + 2475.0)]]

for GCM,RCP in it.product(gcms, scn):
    ###########################################################################
    # Obtain the meteorological data
    ###########################################################################
    tasList = sorted(glob2.glob(os.path.join(os.path.realpath('pp_series'), \
                                'temp', 'EastAsia_tas_bced_1960_1999_' + \
                                GCM + '_' + RCP + '_*.nc')))
    psList = sorted(glob2.glob(os.path.join(os.path.realpath('pp_series'), \
                               'temp', 'EastAsia_ps_bced_1960_1999_' + GCM + \
                               '_' + RCP + '_*.nc')))
    hursList = sorted(glob2.glob(os.path.join(os.path.realpath('pp_series'), \
                                             'temp', 'EastAsia_hurs_' + \
                                             GCM + '_' + RCP + '_*.nc')))
    twbList = sorted(glob2.glob(os.path.join(os.path.realpath('pp_series'), \
                                             'temp', 'EastAsia_twb_' + \
                                             gcms_fl[GCM] + '_' + RCP + \
                                             '_*.nc')))
    prefix = GCM + '_' + RCP + '_'
    for s in stations:
        success_met = extract_met(tasList, psList, hursList, twbList, \
                                  [s[3]], [s[4]], \
                                  [s[0]], out_path, prefix, False)
 
    ###########################################################################
    # Obtain the streamflow data
    ###########################################################################
    qrateList = []
    wtempList = []
    for m in mask:
        qrateList.append(os.path.join(path_to_wat, gcms_fl[GCM], m \
                         , discharge_name[RCP]))
        wtempList.append(os.path.join(path_to_wat, gcms_fl[GCM], m \
                         , wtemp_name[RCP]))

    # Loop through the flow rate and water temperature files to write
    prefix = GCM + '_' + RCP + '_'
    for s in stations:
        success_wat = extract_wat(qrateList, wtempList, \
                                  [s[3]], [s[4]], [s[0]], dates[RCP], \
                                  out_path, prefix, False)


#==============================================================================
# ###############################################################################
# # Calculate the available streamflow
# ###############################################################################
# for GCM in gcms:
#     for s in stations:
#         # Read the historical streamflow
#         temp = pd.read_csv(os.path.join(out_path, 'qrate', \
#                                         GCM+'_hist_'+s[0]+'.csv') \
#                            , header=None).values.flatten()
#         qrate_hist = pd.DataFrame(data=temp, index=dates['hist'], columns=['qrate'])
# 
#         # Read the future streamflow
#         temp = pd.read_csv(os.path.join(out_path, 'qrate', \
#                                         GCM+'_rcp6p0_'+s[0]+'.csv') \
#                            , header=None).values.flatten()
#         qrate_future = pd.DataFrame(data=temp, index=dates['rcp6p0'], columns=['qrate'])
# 
#         # Historical reference period (1961-1990)
#         baseline = qrate_hist.iloc[(dates['hist'].year>=1961) \
#                                    & (dates['hist'].year<=1990)]
# 
#         # Monthly constant e-flow based on the shifted FDC method
#         param_3 = ef.shiftfdc(baseline, True, [], [])
# 
#         ## Historical
#         # Calculate the environmental flow using eflow methods
#         # Save the difference between incoming streamflow and environmental 
#         # flow to binary format file
#         # ---- Environmental Management Class C (Table 3, Smakhitin (2006) An
#         # assessment of environmental flow requirements of Indian River basins)
#         wavail_3 = qrate_hist - ef.shiftfdc(qrate_hist, False, param_3, 3)
#         wavail_3[wavail_3<0.] = 0.
#         wavail_3.qrate.values.tofile(os.path.join(out_path, 'shiftfdc_' \
#                                      + GCM + '_hist_' + s[0] + '_emc3.bin'))
# 
#         ## Future
#         wavail_3 = qrate_future - ef.shiftfdc(qrate_future, False, param_3, 3)
#         wavail_3[wavail_3<0.] = 0.
#         wavail_3.qrate.values.tofile(os.path.join(path_to_out, 'shiftfdc_' + \
#                                                   GCM+'_rcp6p0_'+s[0]+'_emc3.bin'))
#==============================================================================

for GCM,RCP in it.product(gcms, scn):
    ###########################################################################
    # Calculate the water use factor
    ###########################################################################
    if (RCP=='hist'):
        dates = pd.date_range(start='1951-01-01', end='2004-12-31')
    else:
        dates = pd.date_range(start='2006-01-01', end='2099-12-31')

    ko = 1
    nc = 1
    ap = 1
    dT = 1
    ##ef = 4
    non_cool = 0.

    rho_w = 1000.
    c_pw = 4.184 * 10**3
    h_fg = 2.45
    k = 0.000662
    B = 621.9907
    j_per_mwh = 3.6e+09

    # Loop through the individual power plants is good because there is no need
    # to consider water allocation within the same grid
    for s in stations:
        #######################################################################
        # Get the meteorological, streamflow, and water temperature
        #######################################################################
        # relative humidity, and wet-bulb temperature
        t_air = pd.read_csv(os.path.join(out_path, 'tas', GCM + '_' + RCP \
                                         + '_' + s[0] + '.csv') \
                            , squeeze = True, header = None).values
        ps_air = pd.read_csv(os.path.join(out_path, 'ps', GCM + '_' + RCP \
                                          + '_' + s[0] + '.csv') \
                            , squeeze = True, header = None).values
        rh_air = pd.read_csv(os.path.join(out_path, 'hurs', GCM + '_' + RCP \
                                          + '_' + s[0] + '.csv') \
                            , squeeze = True, header = None).values
        t_wb = pd.read_csv(os.path.join(out_path, 'twb', GCM + '_' + RCP \
                                       + '_' + s[0] + '.csv') \
                          , squeeze = True, header = None).values

        # Calculate from the above preliminary variables
        # - w_out: humidity ratio of outgoing air (g/kg)
        # - w_in: humidity ratio of incoming air (g/kg)
        # - h_aout: enthalpy of the outgoing air (kJ/kg)
        # - h_ain: enthalpy of the incoming air (kJ/kg)
        # water vapor saturation pressure (Pa)
        # http://www.vaisala.com/Vaisala%20Documents/Application%20notes/Humidity_Conversion_Formulas_B210973EN-F.pdf
        tc = 647.096 # (K)
        pc = 22064000. # (Pa)
        theta = 1 - (t_air + 273.15) / tc
        p_vapor_sat = pc * np.exp(tc / (t_air+273.15) * (-7.85951783*theta \
                               + 1.84408259*(theta**1.5) - 11.7866497*(theta**3) \
                               + 22.6807411*(theta**3.5) - 15.9618719*(theta**4) \
                               + 1.80122502*(theta**7.5))) # (Pa)
        p_vapor = p_vapor_sat * rh_air / 100.
        w_in = B * p_vapor / (ps_air - p_vapor) /1000. # (kg/kg)
        w_out = B * p_vapor_sat / (ps_air - p_vapor_sat) / 1000. # (kg/kg)
        h_ain = (t_air*(1.01+0.00189*w_in*1000.) \
                        + 2.5*w_in*1000.)*1000. # (J/kg)
        h_aout = (t_air*(1.01+0.00189*w_out*1000.) \
                         + 2.5*w_out*1000.)*1000. # (J/kg)

        # Read the water temperature
        wtemp = pd.read_csv(os.path.join(out_path, 'wtemp' \
                     , GCM+'_'+RCP+'_'+s[0]+'.csv') \
                     , squeeze=True, header=None)

        # Calculate cooling water intensity
        net_eff = s[5]
        wi = bc.tower(net_eff, k_os[ko], n_cc[nc], t_wb \
                      , approach[ap], wtemp, w_out, w_in, h_aout, h_ain)

        # Write the capacity and capacity factors to binary file
        # <Water Use Intensity (m3/MWh)>
        (wi+non_cool).to_records(index=False).tofile(os.path.join(out_path \
                     , 'wi_'+RCP+'_'+GCM+'_'+s[0]+'.bin'))
