import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

file = 'vic_timing_10_mean_std.txt'

# Set up the map
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.
m = Basemap(projection='merc',llcrnrlat=-65,urcrnrlat=80,\
            llcrnrlon=0,urcrnrlon=360,lat_ts=0,resolution='c')
m.drawcoastlines(color='0.3')
#m.fillcontinents(color='white',lake_color='gray')
m.drawparallels(np.arange(-90.,91.,30.), labels=[1,0,0,1])
m.drawmeridians(np.arange(0., 360., 60.), labels=[1,0,0,1])
m.drawmapboundary(fill_color='0.55')


# Set up the color data
data = np.transpose(np.loadtxt(file))
lat = data[0] 
lon = data[1]
mean_timing = data[2]
std_timing = data[3]
array = np.empty((180,360))
array[:] = np.NAN;

x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90.5, 89.5, 1.0)
x,y = np.meshgrid(x,y)
x,y = m(x,y)

for i in xrange(0, mean_timing.size):
    ilat = int(lat[i] + 90.0 - 0.5)
    ilon = int(lon[i] - 0.5)
    array[ilat,ilon] = mean_timing[i]
    
print np.nanmax(mean_timing)
    
array[array < -1] = -1
m.contourf(x, y, array, np.arange(0, 42, 1.0), cmap=cm.jet_r)
m.colorbar()
plt.title("VIC - Mean Timing per evaluation (seconds)")
plt.show()
