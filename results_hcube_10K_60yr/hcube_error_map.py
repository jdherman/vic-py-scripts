import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
from mapformat import mapformat

filename = 'vic_error_9p_10K.txt'

m = mapformat()

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

x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90.5, 89.5, 1.0)
x,y = np.meshgrid(x,y)
x,y = m(x,y)

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90.0 - 0.5)
    ilon = int(lon[i] - 0.5)
    array[ilat,ilon] = min_error[i]*100

zero = 0.9*np.array([1,0,0]).reshape(1,3)
ice = np.loadtxt('cmaps/ice.txt')/255;
ice = np.concatenate((zero,ice[:-1,:]), axis=0)
ice = mpl.colors.ListedColormap(ice)

array_mask = np.ma.masked_where(np.isnan(array),array)
print np.shape(array_mask)
m.pcolormesh(x,y,array_mask,vmin=0.0,vmax=5.0, cmap=cm.jet, rasterized=True, edgecolor='0.6', linewidth=0)
cbar = m.colorbar()
cbar.solids.set_edgecolor("face")
cbar.set_ticks([0,1,2,3,4,5])
plt.title("VIC - Minimum Error")
plt.show()
