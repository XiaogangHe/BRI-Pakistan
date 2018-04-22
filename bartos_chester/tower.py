# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 16:00:20 2017

@author: wangy

Calculate the water withdrawal intensity of once-through cooling systems
(m3/MWh), ignoring drift losses.
"""

from constants import rho_w, c_pw, j_per_mwh
import numpy as np
import pandas as pd

def tower(net_eff, k_os, n_cc, t_wb, approach, wtemp, w_out, 
          w_in, h_aout, h_ain):
    # Input: 
    # net_eff - net thermal efficiency of the power plant (-)
    # k_os - fraction of heat loss via flue gas (-)
    # n_cc - cycles of concentration
    # approach - cooling tower approach (oC)
    # wtemp: the temperature of makeup water (oC), assumed equal to the
    #            temperature of the inlet source
    # - meteorological conditions
    #   -- t_wb: wet-bulb temperature (oC)
    #   -- w_out: humidity ratio of outgoing air (kg/kg)
    #   -- w_in: humidity ratio of incoming air (kg/kg)
    #   -- h_aout: enthalpy of the outgoing air (J/kg)
    #   -- h_ain: enthalpy of the incoming air (J/kg)

    wi = (1-net_eff-k_os)/net_eff*(w_out-w_in)/rho_w/ \
         ((h_aout-h_ain)*(1-1/n_cc) \
           + ((t_wb+approach)/n_cc-wtemp)*c_pw*(w_out-w_in))*j_per_mwh

    wi[np.isclose(w_out, w_in)] = float('inf')
    
    wi = pd.DataFrame({'x':wi.values})

    return wi