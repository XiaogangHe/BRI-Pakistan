# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:46:58 2017

@author: wangy

Variable monthly flow method
(Paster et al. (2014) Accounting for environmental flow requirements in global water assessments)

Low flow months: MMF<=0.4*MAF
Low flow requirements: 0.6*MMF
Intermediate flow months: MMF>0.4*MAF & MMF<=0.8*MAF
Intermediate flow requirements: 0.45*MMF
High flow months: MMF>0.8*MAF
High flow requirements: 0.3*MMF
"""
import numpy as np

def vmf(streamflow, create, eflow_month):
    # Input: 
    # pandas dataframes - streamflow daily series and date labels
    # create: 
    #   True - create the monthly prescription of environmental flow
    #   False - apply eflow_month to get the daily environmental flow

    if create:
        q_mean = streamflow.groupby(streamflow.index.month).mean()

        eflow_month = q_mean.copy()

        highflow = q_mean['qrate'].values > 0.8*np.mean(q_mean['qrate'].values)
        lowflow = q_mean['qrate'].values <= 0.4*np.mean(q_mean['qrate'].values)
        midflow = ~(highflow | lowflow)

        if sum(highflow)>0:
            eflow_month.iloc[highflow] = 0.3*q_mean[highflow]
        if sum(midflow)>0:
            eflow_month.iloc[midflow] = 0.45*q_mean[midflow]
        if sum(lowflow)>0:
            eflow_month.iloc[lowflow] = 0.6*q_mean[lowflow]

        return eflow_month
    else:
        eflow = streamflow.copy()
        for month in range(1,13):
            eflow.iloc[eflow.index.month==month] \
                       = eflow_month.loc[month, 'qrate']

        return eflow