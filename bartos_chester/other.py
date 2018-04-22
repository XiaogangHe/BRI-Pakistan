# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 11:40:50 2017

@author: wangy

Non-cooling water use intensities
"""
from constants import rho_w

def other(net_eff, country):    
    # Water use intensity of wet flue-gas desulfurization
    fgd = 0.37 # m3/MWh

    # Water use intensity of ash handling
    # ---- gross heat rate (kcal MWh-1)
    ghr = 8.5e5/net_eff/1.08
    # ---- net calorific value and ash content
    if country=='China':
        ncv = 5500. # (kcal kg-1)
        A = 0.217
    elif country=='India':
        ncv = 4500.
        A = 0.36
    else:
        ncv = 5000.
        A = 0.28
    # ---- water to ash ratio (kg/kg)
    lam = 2.6

    ashw = (ghr/ncv)*A*lam/rho_w # m3/MWh
    
    # Water use of CCS shift steam
    ccs = 0.32 # m3/MWh

    return (fgd, ashw, ccs)