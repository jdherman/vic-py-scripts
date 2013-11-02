import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap, shiftgrid
from matplotlib.backends import backend_agg as agg # raster backend

filename = 'vic_error_9p_1K.txt'

# Set up the color data
data = np.transpose(np.loadtxt(filename))
lat = data[0] 
lon = data[1]
min_error = data[2]
avg_error = data[3] # calculated wrong ... don't use.
max_error = data[4]
twenty = data[5]
ten = data[6]
five = data[7]
one = data[8]

array = np.empty((180,360))
array[:] = np.NAN;

# x = np.arange(0.5, 360.5, 1.0)
# y = np.arange(-90.5, 89.5, 1.0)
# x,y = np.meshgrid(x,y)
# x,y = m(x,y)

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90 - 0.5)
    ilon = int(lon[i] - 0.5)
    array[ilat,ilon] = five[i]*100
    
array[array == 0] = np.NaN
array,lons = shiftgrid(180., array, np.arange(0,360), start=False)

#INSIDE LOOP...

for ll in xrange(-180,180):
  # Set up the map
  # lat_ts is the latitude of true scale.
  # resolution = 'c' means use crude resolution coastlines.
  # m = Basemap(projection='merc',llcrnrlat=-65,urcrnrlat=80,\
  #            llcrnrlon=0,urcrnrlon=360,lat_ts=0,resolution='c')

  m = Basemap(projection='ortho', lon_0=ll, lat_0=20, resolution='c')
  m.shadedrelief(scale=0.1)
  m.drawcoastlines(color='0.4')
  m.drawcountries(color='0.4')
  #m.fillcontinents(color='white',lake_color='gray')
  m.drawparallels(np.arange(-90.,91.,30.))
  m.drawmeridians(np.arange(0., 360., 60.))
  m.drawmapboundary(fill_color='0.8')

  nx = int((m.xmax-m.xmin)/50000.)+1; ny = int((m.ymax-m.ymin)/50000.)+1
  Tarray = m.transform_scalar(array, np.arange(-180,180), np.arange(-90,90), nx,ny)
  #m.contourf(x, y, array, np.arange(-1.0, 1.05, 0.1), cmap=cm.jet_r)
  m.imshow(Tarray,interpolation='nearest',vmin=0.0,vmax=5.0, cmap=cm.jet_r)
  m.colorbar()
  plt.savefig("figures/globeframes/frame{0}".format(str(ll+180).rjust(3, "0")))
  plt.clf()