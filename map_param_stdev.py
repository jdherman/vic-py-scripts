import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
import math

filename = 'vic_hcube_param_stdevs.txt'

# Set up the map
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.
# m = Basemap(projection='merc',llcrnrlat=-65,urcrnrlat=80,\
#            llcrnrlon=0,urcrnrlon=360,lat_ts=0,resolution='c')
m = Basemap(llcrnrlat=-89.5,urcrnrlat=89.5,\
            llcrnrlon=0.5,urcrnrlon=359.5,resolution='c')
m.drawcoastlines(color='0.3')
#m.fillcontinents(color='white',lake_color='gray')
#m.drawparallels(np.arange(-90.,91.,30.), labels=[1,0,0,1])
#m.drawmeridians(np.arange(0., 360., 60.), labels=[1,0,0,1])
m.drawmapboundary(fill_color='0.55')

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
    array[ilat,ilon] = p1[i]
    
# array[array == 0] = np.NaN
m.imshow(array,interpolation='nearest',vmin=0.0,vmax=1/math.sqrt(12), cmap=cm.jet)
m.colorbar()
plt.title("VIC - Std. Dev. of layer3depth parameter")
plt.show()
