# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 12:19:06 2018

@author: wang.3866
"""
import pandas as pd
import os

gcms = ['gfdl-esm2m', 'hadgem2-es', 'ipsl-cm5a-lr', 'miroc-esm-chem', 'noresm1-m']
plants = ['A','B','C','D','E','F','G','H']

time = pd.date_range(start='2006-01-01', end='2099-12-31')


streamflow = pd.DataFrame(data=0., index=time, columns=plants)
for pp in plants:
    for gg in gcms:
        temp = pd.read_csv(os.path.join(os.path.realpath('output'), \
                                        'hexiaogang', 'qrate', \
                                        gg+'_rcp6p0_'+pp+'.csv'), \
                           header=None)
        streamflow.loc[:, pp] += temp.values[:,0]
streamflow = streamflow / len(gcms)

# Average by year
streamflow = streamflow.loc[(streamflow.index.year >= 2046) & \
                            (streamflow.index.year <= 2055), :]

# Convert from m^3/s to million m^3/year
streamflow_2050s = streamflow.mean() * 3600 * 24 * 365 / 1e6

#
print('Total water demand = %5.3f million m^3 per year' % streamflow_2050s.sum())
