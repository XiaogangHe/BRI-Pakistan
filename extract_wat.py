# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 15:25:11 2017

@author: wangy

Extract water temperature, and streamflow data at the grid overlying each 
power plant, and subset to date_range
"""
import csv
import numpy as np
import xarray as xr
import os

def extract_wat(qrateList, wtempList, lat, lon, ids, date_range \
                , path, prefix, verbose = False): 

    # rate of streamflow(m^3/s)
    qrate = {}
    for pp in range(len(lat)):
        qrate[ids[pp]] = [] # ensure every power plant is initialized
    for qq in qrateList:
        if verbose:
            print(qq)
        with xr.open_dataset(qq) as qfile:
            for pp in range(len(lat)):
                if verbose:
                    print('     ' + ids[pp])
                if ((lon[pp] <= max(qfile.lon.values)) \
                    & (lon[pp] >= min(qfile.lon.values)) \
                    & (lat[pp] <= max(qfile.lat.values)) \
                    & (lat[pp] >= min(qfile.lat.values))):
                    dummy = qfile.discharge.sel(lat = lat[pp] \
                         , lon = lon[pp], method = 'Nearest').values
                    list_of_dates = qfile.time.to_dataframe()
                    qrate[ids[pp]] = dummy[ np.where((list_of_dates \
                         >= date_range[0]).values & (list_of_dates \
                         <= date_range[-1]).values)[0] ].tolist()
    # -- to time series files
    for pp in range(len(lat)):
        with open(os.path.join(path, 'qrate', prefix + ids[pp] + '.csv') \
                  , 'w') as a_series:
            wr = csv.writer(a_series, lineterminator='\n')
            for val in qrate[ids[pp]]:
                wr.writerow([val])

    # water temperature (oC)
    wtemp = {}
    for pp in range(len(lat)):
        wtemp[ids[pp]] = [] # ensure every power plant is initialized
    for tt in wtempList:
        with xr.open_dataset(tt) as tfile:
            for pp in range(len(lat)):
                if verbose:
                    print(ids[pp] + ' at ' + str(pp) + ' ' + tt)
                if ((lon[pp] <= max(tfile.lon.values)) \
                    & (lon[pp] >= min(tfile.lon.values)) \
                    & (lat[pp] <= max(tfile.lat.values)) \
                    & (lat[pp] >= min(tfile.lat.values))):
                    dummy = tfile.waterTemp.sel(lat = lat[pp] \
                         , lon = lon[pp], method = 'Nearest').values - 273.15
                    list_of_dates = tfile.time.to_dataframe()
                    wtemp[ids[pp]] = dummy[ np.where((list_of_dates \
                         >= date_range[0]).values & (list_of_dates \
                         <= date_range[-1]).values)[0] ].tolist()
    # -- to time series files
    for pp in range(len(lat)):
        with open(os.path.join(path, 'wtemp', prefix + ids[pp] + '.csv') \
                  , 'w') as a_series:
            wr = csv.writer(a_series, lineterminator='\n')
            for val in wtemp[ids[pp]]:
                wr.writerow([val])

    return 1