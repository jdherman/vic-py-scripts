from __future__ import division
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mapformat import mapformat
from mpl_toolkits.basemap import Basemap
from matplotlib.backends import backend_svg as svg

hydrofile = 'aero_min_revisit_rates.csv'
data = np.transpose(np.loadtxt(hydrofile, delimiter=','))
lat = data[0] 
lon = data[1]
qsurf = data[2]
sm1 = data[3]
m = mapformat()

redblue = mpl.colors.ListedColormap(np.loadtxt('cmaps/redblue.txt')/255)
x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90.5, 89.5, 1.0)
x,y = np.meshgrid(x,y)
x,y = m(x,y)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# First grab the (-4/+2) recovery scenario coverage deficit

formulation = 4 # without end-of-life
percentileix = 2 # 2 = max revisit, 5 = avg revisit, 6 = 90% revisit, 7 = 95% revisit
d = 2

aerofile = './drones/aero_coverage_f%d_d%d.csv' % (formulation,d)

data = np.transpose(np.loadtxt(aerofile, delimiter=','))
a_lat = data[0]
a_lon = data[1]
a_lon[a_lon < 0] += 360 # convert to [0,360] grid
revisit = data[percentileix]/60

array_rec = np.empty((180,360))
array_rec[:] = np.NAN;

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90.0 - 0.5)
    ilon = int(lon[i] - 0.5)
    idx = np.where((np.floor(a_lat) == np.floor(lat[i])) & (np.floor(a_lon) == np.floor(lon[i])))
    array_rec[ilat,ilon] = max(revisit[idx] - qsurf[i], 0.001)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Then get the original deficit from the full constellation

aerofile = 'aero_coverage_f1.csv'

data = np.transpose(np.loadtxt(aerofile, delimiter=','))
a_lat = data[0]
a_lon = data[1]
a_lon[a_lon < 0] += 360 # convert to [0,360] grid
max_revisit = data[2]/60
avg_revisit = data[5]/60
ninety_revisit = data[6]/60

array_fc = np.empty((180,360))
array_fc[:] = np.NAN;

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90.0 - 0.5)
    ilon = int(lon[i] - 0.5)
    idx = np.where((np.floor(a_lat) == np.floor(lat[i])) & (np.floor(a_lon) == np.floor(lon[i])))
    array_fc[ilat,ilon] = max(max_revisit[idx] - qsurf[i], 0.001)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# then make the plot - percentage difference between the two

array = (1 - (array_rec)/(array_fc))*100
array_mask = np.ma.masked_where(np.isnan(array),array)

#print np.min(np.min(array_mask))
m.pcolormesh(x,y,array_mask,vmin=-50,vmax=50, cmap=redblue, rasterized=True, edgecolor='0.6', linewidth=0)
cbar = m.colorbar()
cbar.solids.set_edgecolor("face")
cbar.set_ticks([-100,-50,0,50,100])
plt.title("% Improvement")
plt.show()
