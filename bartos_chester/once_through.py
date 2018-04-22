# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 14:00:05 2017

@author: wangy

Calculate the water withdrawal intensity of once-through cooling systems
(m3/MWh)
"""

from constants import rho_w, c_pw, j_per_mwh
import numpy as np
import pandas as pd

def once_through(net_eff, k_os, wtemp, T_max_out, dT_max):
    # Input: 
    # net_eff - net thermal efficiency of the power plant (-)
    # k_os - fraction of heat loss via flue gas (-)
    # wtemp - intake water temperature (oC)
    # T_max_out - maximum allowable discharge temeprature (oC)
    # dT_max - maximum allowable temperature rise in the condenser

    # Allowed temperature rise in the condenser (oC)
    # (Use a smaller number instead of zero to generate large heat load instead
    #  of NaN's)
    dT_cond = np.maximum(np.minimum(T_max_out-wtemp.values, dT_max), 0.)

    wi = (1-net_eff-k_os)/net_eff/rho_w/c_pw/dT_cond*j_per_mwh

    if not isinstance(dT_cond, int):
        wi[dT_cond==0.] = float('inf') # in python, 1./float('inf')=0.0

    if not type(wi) is pd.core.frame.DataFrame:
        wi = pd.DataFrame({'x':wi})

    return wi