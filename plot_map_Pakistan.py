import pylab
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib import colors
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes

params = {'backend': 'ps',
          'axes.labelsize': 20,
          'grid.linewidth': 0.2,
          'font.size': 20,
          'legend.fontsize': 16,
          'legend.frameon': False,
          'xtick.labelsize': 16,
          'xtick.direction': 'in',
          'ytick.labelsize': 16,
          'ytick.direction': 'out',
          'savefig.bbox': 'tight',
          'text.usetex': False}
pylab.rcParams.update(params)

dir_shp = '~/Research/PECS/Data/shapefiles/GIS/PAK_adm'
dir_fig = '~/Research/PECS/Figures'

### Read the boundary
lonlat = np.loadtxt('%s/lon_lat_Pakistan.txt' % (dir_shp))
maxlon = 78.75 
minlon = 60.25
maxlat = 37.75
minlat = 23.25

pak_bnd = Dataset('%s/Pakistan_mask_0.5deg.nc' % (dir_shp)).variables['Band1'][:]
pak_mask = np.ma.masked_equal(pak_bnd,0).mask

fig = plt.figure()
ax = fig.add_subplot(111)
M = Basemap(resolution='l', llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon)
M.arcgisimage(service='World_Shaded_Relief')
M.drawmapboundary(fill_color='#80cdc1')
M.plot(lonlat[:,0], lonlat[:,1], lw=1.25, color='k', alpha=0.7)
M.scatter(67.3695, 24.7854, marker='*', s=100, color='darkred', zorder=6)             # Location of powerplant A
M.scatter(70.1736, 24.4338, marker='*', s=100, color='darkred', zorder=6)             # Location of powerplant B
M.scatter(70.3151, 24.8408, marker='*', s=100, color='darkred', zorder=6)             # Location of powerplant C
M.scatter(70.3151, 24.8408, marker='*', s=100, color='darkred', zorder=6)             # Location of powerplant D
M.scatter(73.2359, 30.7196, marker='*', s=100, color='darkred', zorder=6)             # Location of powerplant E
M.scatter(70.1790, 24.6970, marker='*', s=100, color='darkred', zorder=6)             # Location of powerplant F
M.scatter(66.6944, 24.9057, marker='*', s=100, color='darkred', zorder=6)             # Location of powerplant G
M.plot(lonlat[:,0], lonlat[:,1], lw=1.25, color='k', alpha=0.7, zorder=5)
M.drawcoastlines()
M.drawrivers(color='dodgerblue', linewidth=1.0, zorder=4)
fig.text(0.15, 0.34, 'Iran', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
fig.text(0.15, 0.49, 'Afghanistan', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
fig.text(0.65, 0.32, 'India', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
fig.text(0.38, 0.41, 'Pakistan', size=18, va="baseline", ha="left", fontweight='medium', color='#343837', fontstyle='italic')
fig.text(0.2, 0.15, 'Arabian Sea', size=12, va="baseline", ha="left", fontweight='medium', color='white', fontstyle='italic')
fig.text(0.41, 0.16, 'A', size=10, va="center", ha="center", fontweight='semibold', color='black')
fig.text(0.54, 0.14, 'B', size=10, va="center", ha="center", fontweight='semibold', color='black')
fig.text(0.54, 0.215, 'C/D', size=10, va="center", ha="center", fontweight='semibold', color='black')
fig.text(0.66, 0.53, 'E', size=10, va="center", ha="center", fontweight='semibold', color='black')
fig.text(0.52, 0.185, 'F', size=10, va="center", ha="center", fontweight='semibold', color='black')
fig.text(0.38, 0.2, 'G', size=10, va="center", ha="center", fontweight='semibold', color='black')

axins = zoomed_inset_axes(ax, 0.1, 2)
axins.set_xlim(55, 135)
axins.set_ylim(7, 54)

plt.xticks(visible=False)
plt.yticks(visible=False)

M2 = Basemap(llcrnrlat=7, urcrnrlat=54, llcrnrlon=55, urcrnrlon=135)
M2.arcgisimage(service='World_Shaded_Relief')
M2.drawcountries(color='white', linewidth=0.3)
M2.drawcoastlines(color='white', linewidth=0.3)
M2.plot(lonlat[:,0], lonlat[:,1], lw=1.0, color='k', alpha=0.7, zorder=5)

plt.savefig('%s/Pakistan_map.pdf' % (dir_fig))
