# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 18:07:20 2017

@author: wangy

Varying Assumptions about the Water Use Process
"""

true_eff = [1, 0] # if 1 - use Coal Power Plant Tracker Dataset; if 0 -
                  # use Catherine Raptis Dataset

# Fraction of heat loss to flue gas
k_os = [.06, .12, .25]

# Whether non-cooling water are additional to cooling water use
noncool = [True, False]

# Varying Assumptions for Cooling Tower Parameters
n_cc = [3., 5., 20.]
approach = [4., 6., 8.]

# Environmental flow prefixes and suffixes
eflow = [['q90_q50', ''], ['vmf', ''], ['shiftfdc','_emc1'] \
         , ['shiftfdc','_emc2'], ['shiftfdc','_emc3'], ['shiftfdc','_emc4'] \
         , ['shiftfdc','_emc5'], ['shiftfdc','_emc6']]

# Varying Assumptions for Once-through Parameters
# -- maximum permissible temperature rise within the condenser (oC)
dT_max = [5., 14., 25.]
