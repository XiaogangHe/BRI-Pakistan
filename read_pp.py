# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:08:25 2017

@author: wangy

Read the power plants data into pandas data structure
"""
import pandas as pd
import collections
import numpy as np

def read_pp():
    # Read the planned power plants from the Global Coal Power Plant Tracker

    df = pd.read_excel('../Global Coal Plant Tracker July 2017a_myversion.xlsx', 
                       'Projects', 0)
    planned = ((df['Status'] == 'Construction') \
                | (df['Status'] == 'Permitted') \
                | (df['Status'] == 'Pre-permit')) \
             & ((df['Region'] == 'East Asia') \
                | (df['Region'] == 'SE Asia') \
                | (df['Region'] == 'South Asia'))

    df1 = pd.DataFrame(data = collections.OrderedDict( \
                          {'ID': df['Tracker ID'][planned].astype(unicode) \
                           , 'Latitude': pd.to_numeric(df['Latitude'][planned], errors = coerce) \
                           , 'Longitude': pd.to_numeric(df['Longitude'][planned], errors = coerce) \
                           , 'Year': pd.to_numeric(df['Year'][planned], errors = coerce) \
                           , 'Capacity': pd.to_numeric(df['Capacity (MW)'][planned], errors = coerce) \
                           , 'Heat_Rate': pd.to_numeric(df['Heat rate'][planned], errors = coerce) \
                           , 'Tech': df['Combustion technology'][planned].astype(unicode) \
                           , 'Region': df['Region'][planned].astype(unicode) \
                           , 'Country': df['Country'][planned].astype(unicode) \
                           , 'Province': df['Subnational unit'][planned].astype(unicode) \
                           , 'Location': df['Location'][planned].astype(unicode) \
                           , 'Status': df['Status'][planned].astype(unicode) \
                           , 'Chinese': df['Chinese name'][planned].astype(unicode)}))

    df1.drop_duplicates(subset=['ID'], keep='first', inplace=True)

    # the Burma power plant has a typo in latitude; used 
    # http://www.sourcewatch.org/index.php/Myeik_Than_Phyo_Thu_power_station
    # http://www.gps-coordinates.org/
    # to ascertain the correct latitude
    #df2 = df2.set_value(df2['ID'] == 'G107147', 'Latitude', 13.)
    df1.loc[df1['ID'] == 'G107147', 'Latitude'] =  13.

    # The Central Java power plant's locationis ascertained by internet search
    # http://www.sourcewatch.org/index.php/Jawa-8_through_Jawa-13_power_stations
    # http://www.sourcewatch.org/index.php/Cilacap_Sumber_power_station
    df1.loc[df1['ID'] == 'G111930', 'Latitude'] = -7.6832417
    df1.loc[df1['ID'] == 'G111930', 'Longitude'] = 109.096384

    # two Indian power plants have switched latitude and longitude; used
    # http://www.sourcewatch.org/index.php/Paguthan_power_station
    # to ascertain this mistake
    df1.loc[df1['ID'] == 'G107725', 'Latitude'] = 21.78
    df1.loc[df1['ID'] == 'G107726', 'Latitude'] = 21.78
    df1.loc[df1['ID'] == 'G107725', 'Longitude'] = 72.979
    df1.loc[df1['ID'] == 'G107726', 'Longitude'] = 72.979

    # drop the other five operationg power plants  without latitude and 
    # longitude (two 55MW, two 50MW, one 35MW)
    df2 = df1.dropna(subset = ['ID', 'Latitude', 'Longitude'] \
                     ).reset_index(drop = True)
    return df2


def read_pp2(add_planned):
    # Read the planned power plants from the Global Coal Power Plant Tracker
    # Cooling system information will be referenced from Catherine Raptis
    # dataset from get_mixed_cooling()

    df = pd.read_excel('../Global Coal Plant Tracker July 2017a_myversion.xlsx', 
                       'Projects', 0)

    if add_planned:
        planned = ((df['Status'] == 'Operating') \
                    | (df['Status'] == 'Construction') \
                    | (df['Status'] == 'Permitted') \
                    | (df['Status'] == 'Pre-permit')) \
                 & ((df['Region'] == 'East Asia') \
                    | (df['Region'] == 'SE Asia') \
                    | (df['Region'] == 'South Asia'))
    else:
        planned = ((df['Status'] == 'Operating')) \
                 & ((df['Region'] == 'East Asia') \
                    | (df['Region'] == 'SE Asia') \
                    | (df['Region'] == 'South Asia'))

    df1 = pd.DataFrame(data = collections.OrderedDict( \
                          {'ID': df['Tracker ID'][planned].astype(unicode) \
                           , 'Latitude': pd.to_numeric(df['Latitude'][planned], errors = coerce) \
                           , 'Longitude': pd.to_numeric(df['Longitude'][planned], errors = coerce) \
                           , 'Year': pd.to_numeric(df['Year'][planned], errors = coerce) \
                           , 'Capacity': pd.to_numeric(df['Capacity (MW)'][planned], errors = coerce) \
                           , 'Heat_Rate': pd.to_numeric(df['Heat rate'][planned], errors = coerce) \
                           , 'Tech': df['Combustion technology'][planned].astype(unicode) \
                           , 'Region': df['Region'][planned].astype(unicode) \
                           , 'Country': df['Country'][planned].astype(unicode) \
                           , 'Province': df['Subnational unit'][planned].astype(unicode) \
                           , 'Location': df['Location'][planned].astype(unicode) \
                           , 'Status': df['Status'][planned].astype(unicode) \
                           , 'Chinese': df['Chinese name'][planned].astype(unicode)}))

    # Four of the power plants have duplicated IDs
##            Status  Capacity  Country      Region   Longitude         Tech  \
##275     Pre-permit       300    China   East Asia  107.642000  Subcritical   
##276     Pre-permit       300    China   East Asia  107.642000  Subcritical   
##2326     Operating        30    China   East Asia  113.058302  Subcritical   
##2327     Operating        30    China   East Asia  113.047455  Subcritical   
##3416     Permitted       256    India  South Asia   85.259024      Unknown   
##3417     Permitted       185    India  South Asia   85.259024  Subcritical   
##4018  Construction       600  Vietnam     SE Asia  106.528090      Unknown   
##4019  Construction       600  Vietnam     SE Asia  106.528090      Unknown   
##
##           Location   Latitude       ID  Province  Heat_Rate    Year  
##275             nan  35.709000  G104553     Gansu     8702.0  2021.0  
##276             nan  35.709000  G104553     Gansu     8702.0  2021.0  
##2326  Wangqiao Town  36.402869  G111100    Shanxi     8863.0     NaN  
##2327  Wangqiao Town  36.489669  G111100    Shanxi     8863.0     NaN  
##3416    Meramandali  20.808214  G106866    Odisha     8605.0  2019.0  
##3417    Meramandali  20.808214  G106866    Odisha     8702.0  2019.0  
##4018            nan   9.585170  G102532  Tra Vinh     8714.0  2021.0  
##4019            nan   9.585170  G102532  Tra Vinh     8714.0  2021.0  
    df1.drop_duplicates(subset=['ID'], keep='first', inplace=True)

    # the Burma power plant has a typo in latitude; used 
    # http://www.sourcewatch.org/index.php/Myeik_Than_Phyo_Thu_power_station
    # http://www.gps-coordinates.org/
    # to ascertain the correct latitude
    #df2 = df2.set_value(df2['ID'] == 'G107147', 'Latitude', 13.)
    df1.loc[df1['ID'] == 'G107147', 'Latitude'] =  13.
           
    # The Central Java power plant's locationis ascertained by internet search
    # http://www.sourcewatch.org/index.php/Jawa-8_through_Jawa-13_power_stations
    # http://www.sourcewatch.org/index.php/Cilacap_Sumber_power_station
    df1.loc[df1['ID'] == 'G111930', 'Latitude'] = -7.6832417
    df1.loc[df1['ID'] == 'G111930', 'Longitude'] = 109.096384

    # two Indian power plants have switched latitude and longitude; used
    # http://www.sourcewatch.org/index.php/Paguthan_power_station
    # to ascertain this mistake
    df1.loc[df1['ID'] == 'G107725', 'Latitude'] = 21.78
    df1.loc[df1['ID'] == 'G107726', 'Latitude'] = 21.78
    df1.loc[df1['ID'] == 'G107725', 'Longitude'] = 72.979
    df1.loc[df1['ID'] == 'G107726', 'Longitude'] = 72.979

    # drop the other five operationg power plants  without latitude and 
    # longitude (two 55MW, two 50MW, one 35MW)
    df2 = df1.dropna(subset = ['ID', 'Latitude', 'Longitude'] \
                     ).reset_index(drop = True)

    # for the planned power pants that does not have a year, use the average
    # year for the construction, permit, and pre-permit power plants
    if add_planned:
        df2.loc[(df2['Status'] == 'Construction') & np.isnan(df2['Year']) \
                , 'Year'] = np.round(np.mean(df2.loc[(df2['Status'] \
                                             == 'Construction') \
                                     & (~np.isnan(df2['Year'])), 'Year']))
        df2.loc[(df2['Status'] == 'Permitted') & np.isnan(df2['Year']) \
                , 'Year'] = np.round(np.mean(df2.loc[(df2['Status'] \
                                             == 'Permitted') \
                                     & (~np.isnan(df2['Year'])), 'Year']))
        df2.loc[(df2['Status'] == 'Pre-permit') & np.isnan(df2['Year']) \
                , 'Year'] = np.round(np.mean(df2.loc[(df2['Status'] \
                                             == 'Pre-permit') \
                                     & (~np.isnan(df2['Year'])), 'Year']))

    return df2


def read_pp3(retire):
    # Read the planned power plants from the Global Coal Power Plant Tracker
    # Retire the existing power plants in batches, starting from before 1970
    # , then <1980, <1990, <2000, <2010, <2020. To retire 
    # everything <2020 would retire all the existing power plants. The oldest
    # existing power plant in the dataset started in 1959).
    # We use batch retirement because only 28 power plants gave a planned 
    # date of retirement - and thus cannot have any impact.
    # Cooling system information will be referenced from Catherine Raptis
    # dataset from get_mixed_cooling()

    df = pd.read_excel('../Global Coal Plant Tracker July 2017a_myversion.xlsx', 
                       'Projects', 0)

    planned = ((df['Status'] == 'Operating') \
                | (df['Status'] == 'Construction') \
                | (df['Status'] == 'Permitted') \
                | (df['Status'] == 'Pre-permit')) \
             & ((df['Region'] == 'East Asia') \
                | (df['Region'] == 'SE Asia') \
                | (df['Region'] == 'South Asia'))

    df1 = pd.DataFrame(data = collections.OrderedDict( \
                          {'ID': df['Tracker ID'][planned].astype(unicode) \
                           , 'Latitude': pd.to_numeric(df['Latitude'][planned], errors = coerce) \
                           , 'Longitude': pd.to_numeric(df['Longitude'][planned], errors = coerce) \
                           , 'Year': pd.to_numeric(df['Year'][planned], errors = coerce) \
                           , 'Capacity': pd.to_numeric(df['Capacity (MW)'][planned], errors = coerce) \
                           , 'Heat_Rate': pd.to_numeric(df['Heat rate'][planned], errors = coerce) \
                           , 'Tech': df['Combustion technology'][planned].astype(unicode) \
                           , 'Region': df['Region'][planned].astype(unicode) \
                           , 'Country': df['Country'][planned].astype(unicode) \
                           , 'Province': df['Subnational unit'][planned].astype(unicode) \
                           , 'Location': df['Location'][planned].astype(unicode) \
                           , 'Status': df['Status'][planned].astype(unicode) \
                           , 'Chinese': df['Chinese name'][planned].astype(unicode) \
                           , 'Retire': pd.to_numeric(df['Planned Retire'][planned], errors = coerce)}))

    # Remove the plants that are in the retirement batch
    # retire = integer, 1970, 1980, 1990, 2000, 2010, 2020
    df1 = df1.loc[(~(df['Status']=='Operating')) | (df1['Year']>=retire), :]

    # Four of the power plants have duplicated IDs
##            Status  Capacity  Country      Region   Longitude         Tech  \
##275     Pre-permit       300    China   East Asia  107.642000  Subcritical   
##276     Pre-permit       300    China   East Asia  107.642000  Subcritical   
##2326     Operating        30    China   East Asia  113.058302  Subcritical   
##2327     Operating        30    China   East Asia  113.047455  Subcritical   
##3416     Permitted       256    India  South Asia   85.259024      Unknown   
##3417     Permitted       185    India  South Asia   85.259024  Subcritical   
##4018  Construction       600  Vietnam     SE Asia  106.528090      Unknown   
##4019  Construction       600  Vietnam     SE Asia  106.528090      Unknown   
##
##           Location   Latitude       ID  Province  Heat_Rate    Year  
##275             nan  35.709000  G104553     Gansu     8702.0  2021.0  
##276             nan  35.709000  G104553     Gansu     8702.0  2021.0  
##2326  Wangqiao Town  36.402869  G111100    Shanxi     8863.0     NaN  
##2327  Wangqiao Town  36.489669  G111100    Shanxi     8863.0     NaN  
##3416    Meramandali  20.808214  G106866    Odisha     8605.0  2019.0  
##3417    Meramandali  20.808214  G106866    Odisha     8702.0  2019.0  
##4018            nan   9.585170  G102532  Tra Vinh     8714.0  2021.0  
##4019            nan   9.585170  G102532  Tra Vinh     8714.0  2021.0  
    df1.drop_duplicates(subset=['ID'], keep='first', inplace=True)

    # the Burma power plant has a typo in latitude; used 
    # http://www.sourcewatch.org/index.php/Myeik_Than_Phyo_Thu_power_station
    # http://www.gps-coordinates.org/
    # to ascertain the correct latitude
    #df2 = df2.set_value(df2['ID'] == 'G107147', 'Latitude', 13.)
    df1.loc[df1['ID'] == 'G107147', 'Latitude'] =  13.
           
    # The Central Java power plant's locationis ascertained by internet search
    # http://www.sourcewatch.org/index.php/Jawa-8_through_Jawa-13_power_stations
    # http://www.sourcewatch.org/index.php/Cilacap_Sumber_power_station
    df1.loc[df1['ID'] == 'G111930', 'Latitude'] = -7.6832417
    df1.loc[df1['ID'] == 'G111930', 'Longitude'] = 109.096384

    # two Indian power plants have switched latitude and longitude; used
    # http://www.sourcewatch.org/index.php/Paguthan_power_station
    # to ascertain this mistake
    df1.loc[df1['ID'] == 'G107725', 'Latitude'] = 21.78
    df1.loc[df1['ID'] == 'G107726', 'Latitude'] = 21.78
    df1.loc[df1['ID'] == 'G107725', 'Longitude'] = 72.979
    df1.loc[df1['ID'] == 'G107726', 'Longitude'] = 72.979

    # drop the other five operationg power plants  without latitude and 
    # longitude (two 55MW, two 50MW, one 35MW)
    df2 = df1.dropna(subset = ['ID', 'Latitude', 'Longitude'] \
                     ).reset_index(drop = True)

    # for the planned power pants that does not have a year, use the average
    # year for the construction, permit, and pre-permit power plants
    df2.loc[(df2['Status'] == 'Construction') & np.isnan(df2['Year']) \
            , 'Year'] = np.round(np.mean(df2.loc[(df2['Status'] \
                                         == 'Construction') \
                                 & (~np.isnan(df2['Year'])), 'Year']))
    df2.loc[(df2['Status'] == 'Permitted') & np.isnan(df2['Year']) \
            , 'Year'] = np.round(np.mean(df2.loc[(df2['Status'] \
                                         == 'Permitted') \
                                 & (~np.isnan(df2['Year'])), 'Year']))
    df2.loc[(df2['Status'] == 'Pre-permit') & np.isnan(df2['Year']) \
            , 'Year'] = np.round(np.mean(df2.loc[(df2['Status'] \
                                         == 'Pre-permit') \
                                 & (~np.isnan(df2['Year'])), 'Year']))

    return df2