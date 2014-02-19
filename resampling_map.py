import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

filename = 'vic_error_9p_1K.txt'

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
    array[ilat,ilon] = twenty[i]*100
    
array[array == 0] = np.NaN
#m.contourf(x, y, array, np.arange(-1.0, 1.05, 0.1), cmap=cm.jet_r)
m.imshow(array,interpolation='nearest',vmin=0.0,vmax=5.0, cmap=cm.jet_r)
m.colorbar()
plt.title("VIC - Fraction Below 20% Error")
plt.show()
