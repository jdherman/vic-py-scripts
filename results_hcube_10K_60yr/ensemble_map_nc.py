import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap,shiftgrid
import matplotlib as mpl
from mapformat import mapformat
from netCDF4 import Dataset

root_grp = Dataset('climatology-nc/vic_LHS_climatology_cells.nc')
vic_runoff = root_grp.variables['vic_runoff']
lat = root_grp.variables['latitude'][:]
lon = root_grp.variables['longitude'][:]

ensemble = 5000
month = 7

m = mapformat()
array = np.empty((180,360))
array[:] = np.NAN;

x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90, 91, 1.0)

for i in xrange(0, lat.size):
    ilat = int(lat[i] + 90.0)
    ilon = int(lon[i] - 0.5)
    if ilon < 179 or ilon > 181: # HACK: to avoid date-line wraparound problem
      array[ilat,ilon] = vic_runoff[i,ensemble,month]

array, x = shiftgrid(180, array, x)
array_mask = np.ma.masked_invalid(array)
x,y = np.meshgrid(x,y)
x,y = m(x,y)

rbb = np.loadtxt('cmaps/runoff-brownblue.txt')/255;
rbb = mpl.colors.ListedColormap(rbb)

m.pcolormesh(x,y,array_mask,vmin=0.0,vmax=100.0, cmap=rbb, rasterized=False, edgecolor='0.6', linewidth=0)
cbar = m.colorbar()
cbar.solids.set_edgecolor("face")
cbar.set_ticks([0,100])
plt.title("VIC Runoff (mm/month)")
plt.show()

