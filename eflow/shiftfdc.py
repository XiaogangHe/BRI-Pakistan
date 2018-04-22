# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:43:55 2017

@author: wangy

Shifted FDC method (Smakhtin & Anputhas (2006) An assessment of environmental 
flow requirements of Indian River Basins)
"""
import numpy as np

def shiftfdc(streamflow, create, hist_fdc, emc):
    # Input: 
    # streamflow daily series and date labels
    # create: 
    #   True - create hist_fdc (historical flow-duration-curve)
    #   False - map streamflow to environmental flow based on new_fdc and 
    #           the environmental management class (emc: 1-7; Table 3 of 
    #           Smakhtin & Anputhas 2006)
    
    if create:
        # probabilities of exceedance
        qts = np.array([.01, .1, 1., 5., 10., 20., 30., 40., 50., 60. \
                        , 70., 80., 90., 95., 99., 99.9, 99.99]) / 100.
        # 
        hist_fdc = streamflow.quantile(q=1.-qts)
        hist_fdc.index = qts

        return hist_fdc
    else:
        # shift the FDC by some environmental class
        new_fdc = hist_fdc.copy()
        new_fdc.iloc[:(len(hist_fdc)-emc)] = hist_fdc.iloc[emc:].values.copy()
        # append the missing probabilities of exceedance by linear 
        # interpolation
        for f in range((len(hist_fdc)-emc), len(hist_fdc)):
            new_fdc.iloc[f] = new_fdc.iloc[f-1] - new_fdc.iloc[f-2]
            
        new_fdc.iloc[new_fdc['qrate'].values<0.] = 0.

        # apply the shifted FDC to streamflow to get the environmental flow
        afunc = _wrapper(hist_fdc, new_fdc)
        eflow = streamflow.applymap(afunc)

        return eflow

def _wrapper(a_fdc, b_fdc):
    def flow_to_eflow(x):
        # Convert x to the corresponding probability of exceedance (index) on a_fdc
        above = sum((a_fdc.qrate.values - x) > 0.)

        # Convert the probability of exceedance (index) to the corresponding value
        # on b_fdc
        if (above==0):
            eflow = b_fdc.iloc[above,0].copy()
        elif (above<len(a_fdc)):
            p = ((above-1)*(x-a_fdc.iloc[above,0]) \
                 + above*(a_fdc.iloc[above-1,0]-x)) \
                 /(a_fdc.iloc[above-1,0]-a_fdc.iloc[above,0])
            eflow = b_fdc.iloc[above-1,0]*(above-p) \
                    + b_fdc.iloc[above,0]*(p-above+1)
        else:
            eflow = b_fdc.iloc[above-1,0].copy()

        return eflow
    return flow_to_eflow