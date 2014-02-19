import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

hydrofile = 'aero_min_revisit_rates.csv'
aerofile = 'aero_coverage_f3.csv'
# Set up the map
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.
# m = Basemap(projection='merc',llcrnrlat=-65,urcrnrlat=80,\
#            llcrnrlon=0,urcrnrlon=360,lat_ts=0,resolution='c')
m = Basemap(llcrnrlat=-89.5,urcrnrlat=89.5,\
            llcrnrlon=0.5,urcrnrlon=359.5,resolution='c')
#m.drawcoastlines(color='0.2')
m.drawcountries(color='0.4')
#m.fillcontinents(color='white',lake_color='gray')
#m.drawparallels(np.arange(-90.,91.,30.), labels=[1,0,0,1])
#m.drawmeridians(np.arange(0., 360., 60.), labels=[1,0,0,1])
m.drawmapboundary(fill_color='0.8')
m.shadedrelief(scale=0.1, origin='lower')
# Set up the color data
data = np.transpose(np.loadtxt(hydrofile, delimiter=','))
lat = data[0] 
lon = data[1]
evap = data[2]
qsurf = data[3]
sm1 = data[4]
resample = data[5]

data = np.transpose(np.loadtxt(aerofile, delimiter=','))
a_lat = data[0]
a_lon = data[1]
a_lon[a_lon < 0] += 360 # convert to [0,360] grid
max_revisit = data[2]/60

array = np.empty((180,360))
array[:] = np.NAN;

x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90.5, 89.5, 1.0)
x,y = np.meshgrid(x,y)
x,y = m(x,y)

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90.0 - 0.5)
    ilon = int(lon[i] - 0.5)
    idx = np.where((np.floor(a_lat) == np.floor(lat[i])) & (np.floor(a_lon) == np.floor(lon[i])))
    array[ilat,ilon] = max(max_revisit[idx] - qsurf[i], 0.001)
    
array[array == 0] = np.NaN
#m.contourf(x, y, array, np.arange(-1.0, 1.05, 0.1), cmap=cm.jet_r)
ice = mpl.colors.ListedColormap(np.loadtxt('cmaps/ice.txt')/255)
fire = mpl.colors.ListedColormap(np.loadtxt('cmaps/fire.txt')/255)
fireflipsqrt = mpl.colors.ListedColormap(np.sqrt(np.loadtxt('cmaps/fire.txt'))/np.sqrt(255))
fire2 = mpl.colors.ListedColormap(np.power(np.loadtxt('cmaps/fire.txt'),1.5)/np.power(255,1.5))

m.imshow(array,interpolation='nearest',vmin=0.0,vmax=4.0, cmap=fire2)
cbar = m.colorbar()
cbar.solids.set_edgecolor("face")
cbar.set_ticks([0,0.5,1,1.5,2,2.5,3,3.5,4])
plt.title("CovDef qsurf f3")
plt.show()
