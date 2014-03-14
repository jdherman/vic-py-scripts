from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap, shiftgrid
from matplotlib.backends import backend_agg as agg # raster backend

hydrofile = 'aero_min_revisit_rates.csv'
aerofile = 'aero_coverage_f1.csv'

# Set up the color data
data = np.transpose(np.loadtxt(hydrofile, delimiter=','))
lat = data[0] 
lon = data[1]
qsurf = data[2]
sm1 = data[3]

data = np.transpose(np.loadtxt(aerofile, delimiter=','))
a_lat = data[0]
a_lon = data[1]
a_lon[a_lon < 0] += 360 # convert to [0,360] grid
max_revisit = data[2]/60

array = np.empty((180,360))
array[:] = np.NAN;

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90 - 0.5)
    ilon = int(lon[i] - 0.5)
    idx = np.where((np.floor(a_lat) == np.floor(lat[i])) & (np.floor(a_lon) == np.floor(lon[i])))
    array[ilat,ilon] = max(max_revisit[idx] - qsurf[i], 0.001)
    
array[array == 0] = np.NaN
#array,lons = shiftgrid(180., array, np.arange(0,360), start=False)
fire = mpl.colors.ListedColormap(np.loadtxt('cmaps/fire.txt')/255)
fireflipsqrt = mpl.colors.ListedColormap(np.sqrt(np.flipud(np.loadtxt('cmaps/fire.txt')))/np.sqrt(255))
fire2 = mpl.colors.ListedColormap(np.power(np.loadtxt('cmaps/fire.txt'),1.5)/np.power(255,1.5))

#INSIDE LOOP...

for ll in xrange(-180,180):
  # Set up the map
  # lat_ts is the latitude of true scale.
  # resolution = 'c' means use crude resolution coastlines.
  # m = Basemap(projection='merc',llcrnrlat=-65,urcrnrlat=80,\
  #            llcrnrlon=0,urcrnrlon=360,lat_ts=0,resolution='c')

  m = Basemap(projection='ortho', lon_0=ll, lat_0=20, resolution='c')
  m.drawmapboundary(fill_color=np.array([52,152,219])/255, zorder=-1)
  m.fillcontinents(color='0.85', lake_color=np.array([52,152,219])/255, zorder=0)
  #m.drawcoastlines(color='0.6', linewidth=0.5)
  m.drawcountries(color='0.6', linewidth=0.5)
  m.drawparallels(np.arange(-90.,91.,30.), dashes=[1,0], linewidth=0.5, color='0.3')
  m.drawmeridians(np.arange(0., 360., 60.), dashes=[1,0], linewidth=0.5, color='0.3')

  x = np.arange(0.5, 360.5, 1.0)
  y = np.arange(-90.5, 89.5, 1.0)
  x,y = np.meshgrid(x,y)
  x,y = m(x,y)

  array_mask = np.ma.masked_where(np.isnan(array),array)
  # remove points outside projection limb.
  # array_mask = np.ma.masked_where(np.logical_or(x > 1.e10, y > 1.e10), array_mask)

  m.pcolor(x,y,array_mask,vmin=0.0,vmax=7.0, cmap=fire2)
  cbar = m.colorbar()
  cbar.set_ticks([0,1,2,3,4,5,6,7])
  plt.title("Coverage Deficit: Surface Runoff (hrs)")
  plt.savefig("figures/globeframes_covdef/frame{0}".format(str(ll+180).rjust(3, "0")))
  plt.clf()
