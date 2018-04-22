# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 19:45:55 2017

@author: wangy

Get the ambient atmospheric conditions for a recirculating power plant
"""

from constants import B
import numpy as np
import pandas as pd
import os

def met(pid, GCM, RCP, met_path): 
    # Inputs: 
    # pplant - ID of the power plant
    # GCM, RCP - name of the GCM and scenario
    twb = {}
    w_in = {}
    w_out = {}
    h_ain = {}
    h_aout = {}

    for ii in range(len(pid)):
        # Read from .csv files the temeprature (oC), ambient pressure (Pa),
        # relative humidity, and wet-bulb temperature
        t_air = pd.read_csv(os.path.join(met_path, 'tas', GCM + '_' + RCP \
                                         + '_' + pid[ii] + '.csv') \
                            , squeeze = True, header = None).values
        ps_air = pd.read_csv(os.path.join(met_path, 'ps', GCM + '_' + RCP \
                                          + '_' + pid[ii] + '.csv') \
                            , squeeze = True, header = None).values
        rh_air = pd.read_csv(os.path.join(met_path, 'hurs', GCM + '_' + RCP \
                                          + '_' + pid[ii] + '.csv') \
                            , squeeze = True, header = None).values
        twb[pid[ii]] = pd.read_csv(os.path.join(met_path, 'twb', GCM + '_' + RCP \
                                       + '_' + pid[ii] + '.csv') \
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

        w_in[pid[ii]] = B * p_vapor / (ps_air - p_vapor) /1000. # (kg/kg)
        w_out[pid[ii]] = B * p_vapor_sat / (ps_air - p_vapor_sat) / 1000. # (kg/kg)
    
        h_ain[pid[ii]] = (t_air*(1.01+0.00189*w_in[pid[ii]]*1000.) \
                         + 2.5*w_in[pid[ii]]*1000.)*1000. # (J/kg)
        h_aout[pid[ii]] = (t_air*(1.01+0.00189*w_out[pid[ii]]*1000.) \
                          + 2.5*w_out[pid[ii]]*1000.)*1000. # (J/kg)
        
    twb = pd.DataFrame(twb)
    w_in = pd.DataFrame(w_in)
    w_out = pd.DataFrame(w_out)
    h_ain = pd.DataFrame(h_ain)
    h_aout = pd.DataFrame(h_aout)

    return (twb, w_in, w_out, h_ain, h_aout)