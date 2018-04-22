# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 18:48:39 2017

@author: wangy

Invert capacity factor from the heat load to condenser (J/s) for a generic 
thermoelectric generator
"""
import numpy as np

def cf(wi, non_cool, capacity, wavail):
    # Input:
    # wi - water withdrawal intensity of the cooling system (m3/MWh)
    # non_cool - non-cooling water use intensity (FGD, ash handling, or 
    #                                              shift steam for CCS)
    # capacity - nameplate capacity of the power plant (MW)
    # wavail - available streamflow (m3/s)

    # Output:
    # cavail - available capacity (MW)
    # cf - the capacity factor
    
    sec_in_hour = 3600.

    cavail = wavail*sec_in_hour/(wi+non_cool)
    cf = np.minimum(cavail/capacity, 1.)

    return (cavail, cf)