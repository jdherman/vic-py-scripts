import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
from mapformat import mapformat

filename = 'vic_hcube_param_cdfdist_monthly.txt'

m = mapformat()
pname = ['b_infilt', 'Ds', 'Dsmax', 'Ws', 'layer2depth', 'layer3depth', 'rmin', 'expt', 'Ksat']

# b_infilt -3.0 0.0
# Ds -3.0 0.0
# Dsmax -1.0 1.69897
# Ws 0.2 1.0
# layer2depth 0.1 3.0
# layer3depth 0.1 3.0
# rmin -1.0 1.0
# expt 1.0 30.0
# Ksat 2.0 4.0

# Set up the color data
data = np.transpose(np.loadtxt(filename))
lat = data[0] 
lon = data[1]
data = data[2:]
# the others are the parameters in order (0-9)

array = np.empty((180,360))
array[:] = np.NAN;

x = np.arange(0.5, 360.5, 1.0)
y = np.arange(-90.5, 89.5, 1.0)
x,y = np.meshgrid(x,y)
x,y = m(x,y)

fire = np.loadtxt('cmaps/fire.txt')/255;
fire = mpl.colors.ListedColormap(fire)

for p in xrange(0,len(pname)):

  for i in xrange(0, lat.size):
      ilat = int(lat[i] + 90.0 - 0.5)
      ilon = int(lon[i] - 0.5)
      array[ilat,ilon] = data[p,i]

  array_mask = np.ma.masked_where(np.isnan(array),array)
  m.pcolormesh(x,y,array_mask,vmin=0.0,vmax=0.5, cmap=fire, rasterized=True, edgecolor='0.6', linewidth=0)
  cbar = m.colorbar()
  cbar.solids.set_edgecolor("face")
  cbar.set_ticks([0,0.1,0.2,0.3,0.4,0.5])
  plt.title(pname[p])
  plt.savefig('figures/cdfdist_monthly/p%d' % p + '_%s' % pname[p] + '.svg')