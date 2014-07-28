from __future__ import division
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap, interp, maskoceans
from mapformat import mapformat
import matplotlib.mlab as mlab

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
a_max_revisit = data[2]/60
avg_revisit = data[5]/60
ninety_revisit = data[6]/60

interp_factor = 1;

x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90.5, 89.5, 1.0)
x2 = np.arange(0.5, 360.5, 1.0/interp_factor)
y2 = np.arange(-90.5, 89.5, 1.0/interp_factor)

max_revisit = np.zeros((lat.size,))
for i in xrange(0, lat.size):
    max_revisit[i] = np.max(a_max_revisit[np.where((np.floor(a_lat) == np.floor(lat[i])) & (np.floor(a_lon) == np.floor(lon[i])))], 0.001)

array = mlab.griddata(lon, lat, max_revisit-qsurf, x2, y2)
print array.shape
x2,y2 = np.meshgrid(x2,y2)


array_mask = np.empty((180, 360))
array_mask[:] = np.NAN

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90.0 - 0.5)
    ilon = int(lon[i] - 0.5)
    idx = np.where((np.floor(a_lat) == np.floor(lat[i])) & (np.floor(a_lon) == np.floor(lon[i])))
    array_mask[ilat,ilon] = max(a_max_revisit[idx] - qsurf[i], 0.001)

array = np.ma.masked_where(np.isnan(array_mask),array)
# array_mask = interp(array_mask, x, y, x2, y2, masked=True, order = 0)
# array_mask = maskoceans(x2,y2,array_mask,resolution='c')

#m.contourf(x, y, array, np.arange(-1.0, 1.05, 0.1), cmap=cm.jet_r)
ice = mpl.colors.ListedColormap(np.loadtxt('cmaps/ice.txt')/255)
fire = mpl.colors.ListedColormap(np.loadtxt('cmaps/fire.txt')/255)
fireflipsqrt = mpl.colors.ListedColormap(np.sqrt(np.flipud(np.loadtxt('cmaps/fire.txt')))/np.sqrt(255))
fire2 = mpl.colors.ListedColormap(np.power(np.loadtxt('cmaps/fire.txt'),1.5)/np.power(255,1.5))

# NOTE: if you mask before contouring, it chews out a lot of the points. How to mask after??

# m.pcolormesh(x2,y2,array_mask,vmin=0.0,vmax=7.0, cmap=fire2, rasterized=True, edgecolor='0.6', linewidth=0)
m.contourf(x2,y2,array, np.arange(1, 8.5, 0.5), latlon=True, cmap=fire2, rasterized=False, edgecolor='0.6', linewidth=0)
cbar = m.colorbar()
cbar.solids.set_edgecolor("face")
cbar.set_ticks([0,1,2,3,4,5,6,7])
plt.title("Deficit (hrs): F3 with Max Revisit")
plt.show()
