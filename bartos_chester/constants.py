# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 14:12:38 2017

@author: wangy

Some constants
  rho_w - density of water (10^3 kg/m^3)
  c_pw - heat capacity of water (4.184 kJ/kg/oC)
  h_fg - latent heat of vaporization of water (2.45 MJ/kg)
  k - psychrometric constant (0.000662 oC-1)
  B - molecular weight ratio of water to air * 1000 (621.9907 g/kg) 
  js_per_mw - conversion factor from MW to J/s
"""

rho_w = 1000.
c_pw = 4.184 * 10**3 # http://www.ce.utexas.edu/prof/Novoselac/classes/ARE383/Handouts/F01_06SI.pdf
                     # "specific enthalpy" at 1oC
h_fg = 2.45
k = 0.000662
B = 621.9907
j_per_mwh = 3.6e+09