import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

root_grp = Dataset('frequency_nse.nc')
# dimensions: lon, lat, t
# variables: lon, lat, t, evapmean, evapmin, evapmax, qsurfmean, qsurfmin, qsurfmax, sm1mean, sm1min, sm1max

var = root_grp.variables['sm1min']

m = Basemap(llcrnrlat=-89.5,urcrnrlat=89.5,\
            llcrnrlon=0.5,urcrnrlon=359.5,resolution='c')
#m.drawcoastlines(color='0.2')
m.drawcountries(color='0.4')
#m.fillcontinents(color='white',lake_color='gray')
#m.drawparallels(np.arange(-90.,91.,30.), labels=[1,0,0,1])
#m.drawmeridians(np.arange(0., 360., 60.), labels=[1,0,0,1])
m.drawmapboundary(fill_color='0.8')
m.shadedrelief(scale=0.1, origin='lower')
    
#m.contourf(x, y, array, np.arange(-1.0, 1.05, 0.1), cmap=cm.jet_r)
m.imshow(var[0],interpolation='nearest',vmin=0.0,vmax=20.0, cmap=cm.jet_r)
m.colorbar()
plt.title("VIC - Fraction Below 20% Error")
plt.show()

print var[0]

# #make plots
# #sm1
# plot_variables(0,20,'sm1')
# #evap
# plot_variables(0,20,'evap')
# #qsurf
# plot_variables(0,5,'qsurf')
