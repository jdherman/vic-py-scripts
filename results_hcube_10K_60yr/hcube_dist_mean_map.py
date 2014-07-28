import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
from mapformat import mapformat

filename = 'distribution-means/vic_hcube_param_mean_mon.txt'

m = mapformat()

# Set up the color data
data = np.transpose(np.loadtxt(filename))
lat = data[0] 
lon = data[1]

p2 = data[2]

array = np.empty((180,360))
array[:] = np.NAN;

x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90.5, 89.5, 1.0)
x,y = np.meshgrid(x,y)
x,y = m(x,y)

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90.0 - 0.5)
    ilon = int(lon[i] - 0.5)
    array[ilat,ilon] = p2[i]

zero = np.array([0.97,0.6,0.6]).reshape(1,3)
ice = np.loadtxt('cmaps/ice.txt')/255;
ice = np.concatenate((zero,ice[:-1,:]), axis=0)
ice = mpl.colors.ListedColormap(ice)

array_mask = np.ma.masked_where(np.isnan(array),array)

m.pcolormesh(x,y,array_mask,vmin=0.0,vmax=1.0, cmap=ice, rasterized=True, edgecolor='0.6', linewidth=0)
cbar = m.colorbar()
cbar.solids.set_edgecolor("face")
plt.title("VIC - Ann10monR75")
plt.show()
