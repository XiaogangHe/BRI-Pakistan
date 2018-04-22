# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:42:16 2017

@author: wangy

Q90_Q50 method for environmental flow
(Pastor et al. (2014) Accounting for environmental flow requirements in global water assessments)

For months that have mean monthly flow <= mean annual flow, use Q90 as the 
low-flow requirement; For months that have mean monthly flow > mean annual 
flow, use Q50 as the high-flow requirement. 
"""
import numpy as np

def q90_q50(streamflow, create, eflow_month):
    # Input: 
    # pandas dataframes - streamflow daily series and date labels
    # create: 
    #   True - create the monthly prescription of environmental flow
    #   False - apply eflow_month to get the daily environmental flow

    if create:
        q_mean = streamflow.groupby(streamflow.index.month).mean()        
        q50 = streamflow.quantile(q=0.5)
        q90 = streamflow.quantile(q=0.1)

        eflow_month = q_mean.copy()

        highflow = q_mean['qrate'].values > np.mean(q_mean['qrate'].values)
        eflow_month.iloc[highflow] = q50[0].copy()
        eflow_month.iloc[~highflow] = q90[0].copy()
        
        return eflow_month
    else:
        eflow = streamflow.copy()
        for month in range(1,13):
            eflow.iloc[eflow.index.month==month] \
                       = eflow_month.loc[month, 'qrate']

        return eflow