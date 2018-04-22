# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 00:34:48 2017

@author: wangy
"""
import numpy as np
import pandas as pd
import os
from ismember import ismember
import collections

def read_pp_raptis():
    countries = {'BGD': 'Bangladesh', 'KHM': 'Cambodia', 'CHN': 'China' \
                 , 'IND': 'India', 'IDN': 'Indonesia', 'JPN': 'Japan' \
                 , 'MYS': 'Malaysia', 'MNG': 'Mongolia', 'MMR': 'Myanmar' \
                 , 'PAK': 'Pakistan', 'PHL': 'Philippines' \
                 , 'KOR': 'South Korea', 'TWN': 'Taiwan' \
                 , 'THA': 'Thailand', 'VNM': 'Vietnam'}

    # Read the power plants
    df = pd.read_excel(os.path.join(os.path.realpath('..') \
                               , 'IIASAPP_AISA_COAL.xlsx'), 'Sheet1', 0)

    # Subset to operating coal-fired power plants in the above Asian countries, 
    # (removed: built after 2010 to reflect the up-to-date technology)
    subset = np.asarray(ismember(df.ISO, countries.keys())) \
             & np.asarray(ismember(df.msg_combo, ['coal_st', 'coal_cc'])) \
             & (df.STATUS.values.astype(unicode) == 'OPR')

    # Note: Tech2 has the information whether it is ST or coal-CC; Tech only 
    # tells whether the turbine is sub-, super-, or ultrasuper-critical
    # Fills the missing values in the country column with the de-coded ISO code
    # and in this process replaces Hongkong (China) by China
    df1 = pd.DataFrame(data = collections.OrderedDict( \
                          {'Unit': df['UNIT'][subset].astype(unicode) \
                           , 'Plant': df['PLANT'][subset].astype(unicode) \
                           , 'Country': [countries[x] for x in df['ISO'][subset].astype(unicode)] \
                           , 'Capacity': pd.to_numeric(df['MW_x'][subset], errors = coerce) \
                           , 'Year': pd.to_numeric(df['YEAR'][subset].astype(unicode), errors = coerce) \
                           , 'Tech': df['STYPE'][subset].astype(unicode) \
                           , 'Tech2': df['msg_combo'][subset].astype(unicode) \
                           , 'Cooling': df['cool_group_msg'][subset].astype(unicode)
                           , 'Latitude': pd.to_numeric(df['latC'][subset], errors = coerce) \
                           , 'Longitude': pd.to_numeric(df['lonC'][subset], errors = coerce) \
                           , 'Net_Eff': pd.to_numeric(df['mean_annual_cycle_efficiency'][subset], errors = coerce) \
                           }))

    # Drop the unknown lat & lon's
    df1 = df1.dropna(subset=('Latitude','Longitude')).reset_index(drop=True)


    return df1