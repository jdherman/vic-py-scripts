import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

m = mapformat()

# Set up the color data

array = np.empty((180,360))
array[:] = np.NAN;

x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90.5, 89.5, 1.0)
x,y = np.meshgrid(x,y)
x,y = m(x,y)


pnum = [158,680]#,120,191,251, 430, 603, 329, 220, 871]
data = np.empty((0,2))
for p in pnum:
  data = np.loadtxt('gensets/paramset_' + str(p) + '.txt')

  lat = data[:,0] 
  lon = data[:,1]

  for i in xrange(0, lat.size):
      ilat = int(lat[i] + 90.0 - 0.5)
      ilon = int(lon[i] - 0.5)
      array[ilat,ilon] = pnum.index(p)
    
array[array == 0] = np.NaN
#m.contourf(x, y, array, np.arange(-1.0, 1.05, 0.1), cmap=cm.jet_r)
m.imshow(array,interpolation='nearest',vmin=0.0,vmax=10.0, cmap=cm.get_cmap('Set1', 10))
m.colorbar()
plt.title("VIC - AAA")
plt.show()
