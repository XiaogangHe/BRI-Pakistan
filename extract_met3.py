# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:14:50 2017

@author: wangy

Extract the meteorological conditions at the grid overlying each power plant
from the list of lat & lon
"""
import csv
import xarray as xr
import os

def extract_met(tasList, psList, hursList, twbList, lat, lon, ids \
                , path, prefix, verbose = False):
    # surface temperature (oC)
    tas = {}
    for pp in range(len(lat)):
        tas[ids[pp]] = []
    for at in tasList:
        tast = xr.open_dataset(at) # with xr.open_dataset(at) as tast:
        for pp in range(len(lat)):
            if verbose:
                print(ids[pp] + ' at ' + str(pp) + ' ' + at)
            tas[ids[pp]].extend(( \
                   tast.tasAdjust.sel(lat = lat[pp], lon = lon[pp] \
                   , method = 'Nearest').values - 273.15).tolist())
        tast.close()
    # -- to time series files
    for pp in range(len(lat)):
        with open(os.path.join(path, 'tas', prefix + ids[pp] + '.csv') \
                  , 'w') as a_series:
            wr = csv.writer(a_series, lineterminator='\n')
            for val in tas[ids[pp]]:
                wr.writerow([val])

    # surface pressure (Pa)
    ps = {}
    for pp in range(len(lat)):
        ps[ids[pp]] = []
    for at in psList:
        pst = xr.open_dataset(at)
        for pp in range(len(lat)):
            if verbose:
                print(ids[pp] + ' at ' + str(pp) + ' ' + at)
            ps[ids[pp]].extend( \
                   pst.psAdjust.sel(lat = lat[pp], lon = lon[pp] \
                   , method = 'Nearest').values.tolist())
        pst.close()
    # -- to time series files
    for pp in range(len(lat)):
        with open(os.path.join(path, 'ps', prefix + ids[pp] + '.csv') \
                  , 'w') as a_series:
            wr = csv.writer(a_series, lineterminator='\n')
            for val in ps[ids[pp]]:
                wr.writerow([val])

    # relative humidity (%)
    hurs = {}
    for pp in range(len(lat)): # len(lat)
        hurs[ids[pp]] = []
    for at in hursList:
        hurt = xr.open_dataset(at)
        for pp in range(len(lat)): # len(lat)
            if verbose:
                print(ids[pp] + ' at ' + str(pp) + ' ' + at)
            hurs[ids[pp]].extend( \
                    hurt.hurs.sel(lat = lat[pp], lon = lon[pp] \
                    , method = 'Nearest').values.tolist())
        hurt.close()
    # -- to time series files
    for pp in range(len(lat)): # 
        with open(os.path.join(path, 'hurs', prefix + ids[pp] + '.csv') \
                  , 'w') as a_series:
            wr = csv.writer(a_series, lineterminator='\n')
            for val in hurs[ids[pp]]:
                wr.writerow([val])

    # wet-bulb temperature (oC)
    twb = {}
    for pp in range(len(lat)):
        twb[ids[pp]] = []
    for at in twbList:
        twbt = xr.open_dataset(at)
        for pp in range(len(lat)):
            if verbose:
                print(ids[pp] + ' at ' + str(pp) + ' ' + at)
            twb[ids[pp]].extend( \
                   twbt.twb.sel(lat = lat[pp], lon = lon[pp] \
                   , method = 'Nearest').values.tolist())
        twbt.close()
    # -- to time series files
    for pp in range(len(lat)): # len(lat)
        with open(os.path.join(path, 'twb', prefix + ids[pp] + '.csv') \
                  , 'w') as a_series:
            wr = csv.writer(a_series, lineterminator='\n')
            for val in twb[ids[pp]]:
                wr.writerow([val])

    return 1