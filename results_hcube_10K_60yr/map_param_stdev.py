import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
import math
import mapformat

filename = 'vic_hcube_param_stdevs.txt'

m = mapformat()

# Set up the color data
data = np.transpose(np.loadtxt(filename))
lat = data[0] 
lon = data[1]
p1 = data[2] # b_infilt
p2 = data[3] # Ds
p3 = data[4] # Dsmax
p4 = data[5] # Ws
p5 = data[6] # layer2depth
p6 = data[7] # layer3depth
p7 = data[8] # rmin
p8 = data[9] # expt
p9 = data[10] # Ksat

array = np.empty((180,360))
array[:] = np.NAN;

x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90.5, 89.5, 1.0)
x,y = np.meshgrid(x,y)
x,y = m(x,y)

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90.0 - 0.5)
    ilon = int(lon[i] - 0.5)
    array[ilat,ilon] = p9[i]

# zero = 0.9*np.array([1,0,0]).reshape(1,3)
# ice = np.loadtxt('cmaps/ice.txt')/255;
# ice = np.concatenate((zero,ice[:-1,:]), axis=0)
# ice = mpl.colors.ListedColormap(ice)
    
array_mask = np.ma.masked_where(np.isnan(array),array)

m.pcolormesh(x,y,array_mask, vmin=0.0,vmax=1/math.sqrt(12), cmap=cm.jet, rasterized=True, edgecolor='0.6', linewidth=0)
cbar = m.colorbar()
cbar.solids.set_edgecolor("face")
cbar.set_ticks([0,1/(4*math.sqrt(12)),1/(2*math.sqrt(12)),3/(4*math.sqrt(12)),1/math.sqrt(12)])
plt.title("Ksat")
plt.show()
