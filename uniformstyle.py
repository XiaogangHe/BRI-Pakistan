# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 20:17:41 2017

@author: wangy
"""
import matplotlib as mpl

def uniformstyle():
    mpl.rcParams['figure.figsize'] = 10, 8 # change some settings from ggplot
    mpl.rcParams['xtick.labelsize'] = 9
    mpl.rcParams['ytick.labelsize'] = 9
    mpl.rcParams['axes.labelsize'] = 9
    mpl.rcParams['legend.fontsize'] = 9
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = ['Helvetica']