from __future__ import division
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
from mapformat import mapformat

hydrofile = 'aero_min_revisit_rates.csv'
aerofile = 'aero_coverage_f3.csv'

m = mapformat()

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
avg_revisit = data[5]/60
ninety_revisit = data[6]/60

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
    cd = qsurf[i] #max(max_revisit[idx] - qsurf[i], 0.001)
    if cd < 4:
      array[ilat,ilon] = cd
    
#m.contourf(x, y, array, np.arange(-1.0, 1.05, 0.1), cmap=cm.jet_r)
ice = mpl.colors.ListedColormap(np.loadtxt('cmaps/ice.txt')/255)
fire = mpl.colors.ListedColormap(np.loadtxt('cmaps/fire.txt')/255)
fireflipsqrt = mpl.colors.ListedColormap(np.sqrt(np.flipud(np.loadtxt('cmaps/fire.txt')))/np.sqrt(255))
fire2 = mpl.colors.ListedColormap(np.power(np.loadtxt('cmaps/fire.txt'),1.5)/np.power(255,1.5))

array_mask = np.ma.masked_where(np.isnan(array),array)

m.pcolormesh(x,y,array_mask,vmin=1.0,vmax=4.0, cmap=fireflipsqrt, rasterized=True, edgecolor='0.6', linewidth=0)
cbar = m.colorbar()
cbar.solids.set_edgecolor("face")
cbar.set_ticks([1,2,3,4])
plt.title("Target Frequency (hours)")
plt.show()
