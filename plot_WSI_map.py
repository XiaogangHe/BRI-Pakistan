import pylab
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
sys.path.append('~/PythonModules')   
from util import day2month                                                
from scipy import stats
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
from matplotlib import colors
from matplotlib import cm

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

### Functions

def linear_fit(syear, eyear, y):
    x = np.arange(syear, eyear+1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    y_fit = intercept + slope*x

    return slope, intercept, p_value, y_fit

def custom_div_cmap(numcolors=11, name='custom_div_cmap',
                    mincol='blue', midcol='white', maxcol='red'):
    """ Create a custom diverging colormap with three colors
    
    Default is blue to white to red with 11 colors.  Colors can be specified
    in any way understandable by matplotlib.colors.ColorConverter.to_rgb()
    """

    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list(name=name,
                                             colors =[mincol, midcol, maxcol],
                                             N=numcolors)
    return cmap

def imshow_Pakistan(data, vmin=None, vmax=None, norm=None, cmap=None, ticks=None, title=None, fig_name=None):
    fig = plt.figure()
    M = Basemap(resolution='l', llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon)
    M.fillcontinents(color='#D6D5D5')
    M.drawmapboundary(fill_color='#80cdc1')
    M.drawcountries(color='white', linewidth=1.25)
    lons_map, lats_map = M(lon-0.25, lat+0.25)
    cs = M.pcolormesh(lons_map, lats_map, data[::-1], vmin=vmin, vmax=vmax, norm=norm, cmap=cmap, zorder=4)
    M.scatter(67.3695, 24.7854, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant A
    M.scatter(70.1736, 24.4338, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant B
    M.scatter(70.3151, 24.8408, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant C
    M.scatter(70.3151, 24.8408, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant D
    M.scatter(73.2359, 30.7196, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant E
    M.scatter(70.1790, 24.6970, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant F
    M.scatter(66.6944, 24.9057, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant G
    M.plot(lonlat[:,0], lonlat[:,1], lw=1.25, color='k', alpha=0.7, zorder=7)
    M.drawcoastlines()
    cbar = M.colorbar(cs, ticks=ticks, location='right', pad="5%", size="3%", extend='both')
    fig.text(0.14, 0.32, 'Iran', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
    fig.text(0.2, 0.6, 'Afghanistan', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
    fig.text(0.6, 0.3, 'India', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
    fig.text(0.15, 0.15, 'Arabian Sea', size=12, va="baseline", ha="left", fontweight='medium', color='white', fontstyle='italic')
    fig.text(0.13, 0.8, model.upper(), size=22, va="baseline", ha="left", fontweight='medium', color='#343837')
    #plt.title(title)

    plt.savefig('%s/%s_%s.pdf' % (dir_fig, fig_name, model))
    plt.show()

def imshow_Pakistan_hatch(data, lons_sig_arr, lats_sig_arr, vmin=None, vmax=None, norm=None, cmap=None, ticks=None, title=None, fig_name=None):
    fig = plt.figure()
    M = Basemap(resolution='l', llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon)
    M.fillcontinents(color='#D6D5D5')
    M.drawmapboundary(fill_color='#80cdc1')
    M.drawcountries(color='white', linewidth=1.25)
    lons_map, lats_map = M(lon-0.25, lat+0.25)
    cs = M.pcolormesh(lons_map, lats_map, data[::-1], vmin=vmin, vmax=vmax, norm=norm, cmap=cmap, zorder=4)
    lons_sig_arr, lats_sig_arr = M.shiftdata(lons_sig_arr, lats_sig_arr)
    M.scatter(lons_sig_arr, lats_sig_arr, marker='.', s=50, color='coral', latlon=True, zorder=6)  
    M.scatter(67.3695, 24.7854, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant A
    M.scatter(70.1736, 24.4338, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant B
    M.scatter(70.3151, 24.8408, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant C
    M.scatter(70.3151, 24.8408, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant D
    M.scatter(73.2359, 30.7196, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant E
    M.scatter(70.1790, 24.6970, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant F
    M.scatter(66.6944, 24.9057, marker='*', s=200, color='#343837', zorder=5)             # Location of powerplant G
    M.plot(lonlat[:,0], lonlat[:,1], lw=1.25, color='k', alpha=0.7, zorder=7)
    M.drawcoastlines()
    cbar = M.colorbar(cs, ticks=ticks, location='right', pad="5%", size="3%", extend='both')

    fig.text(0.14, 0.32, 'Iran', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
    fig.text(0.2, 0.6, 'Afghanistan', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
    fig.text(0.6, 0.3, 'India', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
    fig.text(0.15, 0.15, 'Arabian Sea', size=12, va="baseline", ha="left", fontweight='medium', color='white', fontstyle='italic')
    fig.text(0.13, 0.8, model.upper(), size=22, va="baseline", ha="left", fontweight='medium', color='#343837')
    #plt.title(title)

    plt.savefig('%s/%s_%s.pdf' % (dir_fig, fig_name, model))
    plt.show()

dir_wsi = '~/Research/PECS/Data/Pakistan/WSI'
dir_shp = '~/Research/PECS/Data/shapefiles/GIS/PAK_adm'
dir_fig = '~/Research/PECS/Figures'

models = ['gfdl-esm2m', 'ipsl-cm5a-lr', 'miroc-esm-chem', 'noresm1-m', 'hadgem2-es']

### Read the boundary
lonlat = np.loadtxt('%s/lon_lat_Pakistan.txt' % (dir_shp))
maxlon = 78.75 
minlon = 60.25
maxlat = 37.75
minlat = 23.25

pak_bnd = Dataset('%s/Pakistan_mask_0.5deg.nc' % (dir_shp)).variables['Band1'][:]
pak_mask = np.ma.masked_equal(pak_bnd,0).mask

### Historical
wsi_hist_gfdl = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[0])).variables['wsi'][:]
wsi_hist_ipsl = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[1])).variables['wsi'][:]
wsi_hist_miro = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[2])).variables['wsi'][:]
wsi_hist_nore = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[3])).variables['wsi'][:]
wsi_hist_hadg = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[4])).variables['wsi'][:]

### SSP2
wsi_ssp2_gfdl = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[0])).variables['wsi'][:]
wsi_ssp2_ipsl = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[1])).variables['wsi'][:]
wsi_ssp2_miro = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[2])).variables['wsi'][:]
wsi_ssp2_nore = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[3])).variables['wsi'][:]
wsi_ssp2_hadg = Dataset('%s/SSP2/pakistan_wsi_%s_ssp2_rcp6p0_2005_2055.nc' % (dir_wsi, models[4])).variables['wsi'][:]

model = models[4]
data = wsi_ssp2_hadg
data_2010s = data[1:11]      ### 2006-2015 as 2010s
data_2050s = data[-10:]
wsi_ratio = 100*(data_2050s.mean(0)-data_2010s.mean(0))/data_2010s.mean(0)

slp_ssp2 = np.array([linear_fit(2006, 2055, data[1:,i,j])[0] for i in range(30) for j in range(38)]).reshape(30,38)
pva_ssp2 = np.array([linear_fit(2006, 2055, data[1:,i,j])[2] for i in range(30) for j in range(38)]).reshape(30,38)

slp_ssp2_mask = np.ma.array(slp_ssp2, mask=np.resize(pak_mask, slp_ssp2.shape))
pva_ssp2_mask = np.ma.array(pva_ssp2, mask=np.resize(pak_mask, pva_ssp2.shape))

lat = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[0])).variables['lat'][:]
lon = Dataset('%s/Historical/pakistan_wsi_%s_hist_hist_1971_2004.nc' % (dir_wsi, models[0])).variables['lon'][:]
lons, lats = np.meshgrid(lon, lat)

### Spatial map of WSI
fig = plt.figure()
M = Basemap(resolution='l', llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon)
M.fillcontinents(color='#D6D5D5')
M.drawmapboundary(fill_color='#80cdc1')
M.drawcountries(color='white', linewidth=1.25)
M.plot(lonlat[:,0], lonlat[:,1], lw=1.25, color='k', alpha=0.7)
lons_map, lats_map = M(lon-0.25, lat+0.25)
cs = M.pcolormesh(lons_map, lats_map, data_2010s.mean(0), vmin=0, vmax=1, cmap='Spectral_r', zorder=4)
M.scatter(67.3695, 24.7854, marker='*', s=200, color='black', zorder=6)             # Location of powerplant A
M.scatter(70.1736, 24.4338, marker='*', s=200, color='black', zorder=6)             # Location of powerplant B
M.scatter(70.3151, 24.8408, marker='*', s=200, color='black', zorder=6)             # Location of powerplant C
M.scatter(70.3151, 24.8408, marker='*', s=200, color='black', zorder=6)             # Location of powerplant D
M.scatter(73.2359, 30.7196, marker='*', s=200, color='black', zorder=6)             # Location of powerplant E
M.scatter(70.1790, 24.6970, marker='*', s=200, color='black', zorder=6)             # Location of powerplant F
M.scatter(66.6944, 24.9057, marker='*', s=200, color='black', zorder=6)             # Location of powerplant G
M.plot(lonlat[:,0], lonlat[:,1], lw=1.25, color='k', alpha=0.7, zorder=5)
M.drawcoastlines()
cbar = M.colorbar(cs, location='right', pad="5%", size="3%", extend='both')
fig.text(0.14, 0.32, 'Iran', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
fig.text(0.2, 0.6, 'Afghanistan', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
fig.text(0.6, 0.3, 'India', size=18, va="baseline", ha="left", fontweight='medium', color='grey', fontstyle='italic')
fig.text(0.15, 0.15, 'Arabian Sea', size=12, va="baseline", ha="left", fontweight='medium', color='white', fontstyle='italic')
fig.text(0.13, 0.8, model.upper(), size=22, va="baseline", ha="left", fontweight='medium', color='#343837')
#plt.title(model.upper(), fontsize=22)
plt.savefig('%s/wsi_ssp2_2010s_%s_7plants.pdf' % (dir_fig, model))
plt.show()

### WSI relative change map
var_min = -90
var_max = 90
bnd = np.linspace(var_min, var_max, 10)   ### 10 ticks on the colorbar, should be even
cmap_div = custom_div_cmap(numcolors=11, mincol=cm.PiYG(255), maxcol=cm.PiYG(0), midcol='#f0f0f0')    ### for contribution
norm = colors.BoundaryNorm(bnd, cmap_div.N)
ticks = np.linspace(var_min, var_max, 10)
imshow_Pakistan(wsi_ratio[::-1], vmin=var_min, vmax=var_max, norm=norm, cmap=cmap_div, ticks=ticks, fig_name='wsi_ssp2_changes_2050s_2010s_7plants')

### WSI trend map

sig_mask = np.ma.masked_greater_equal(pva_ssp2, 0.05).mask
sig_lats = np.ma.array(lats, mask=np.resize(sig_mask, lats.shape)).compressed()
sig_lons = np.ma.array(lons, mask=np.resize(sig_mask, lons.shape)).compressed()

slp_min = -0.007
slp_max = 0.007
slp_bnd = np.linspace(slp_min, slp_max, 8)   ### 10 ticks on the colorbar, should be even
slp_cmap = custom_div_cmap(numcolors=11, mincol='#2887a1', maxcol='#A16928', midcol='#f0f0f0')
slp_norm = colors.BoundaryNorm(slp_bnd, slp_cmap.N)
slp_ticks = np.linspace(slp_min, slp_max, 8)
imshow_Pakistan_hatch(slp_ssp2_mask[::-1], sig_lons, sig_lats, vmin=slp_min, vmax=slp_max, norm=slp_norm, cmap=slp_cmap, ticks=slp_ticks, fig_name='wsi_ssp2_trend_sig_2006_2055_7plants')
