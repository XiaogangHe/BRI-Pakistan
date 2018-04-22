# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 18:44:15 2017

@author: wangy

Source of water use data for dry-cooling: Zhang (2016) Revealing Water Stress 
by the Thermal Power Industry in China Based on a High Spatial Resolution
Water Withdrawal and Consumption Inventory
"""
def air(capacity):
    
    hr_to_sec = 3600.

    if capacity < 300.: 
        wi = 0.59 / hr_to_sec
    elif capacity <= 600.:
        wi = (0.417*(600.-capacity)+0.334*(capacity-300.))/(600.-300.) \
             /hr_to_sec
    elif capacity <= 1000.:
        wi = (0.334*(1000.-capacity)+0.31*(capacity-600.))/(1000.-600.) \
             /hr_to_sec
    else:
        wi = 0.31 / hr_to_sec

    return wi