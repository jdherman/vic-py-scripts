from __future__ import division
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mapformat import mapformat
from mpl_toolkits.basemap import Basemap
from matplotlib.backends import backend_svg as svg

hydrofile = 'aero_min_revisit_rates.csv'
data = np.transpose(np.loadtxt(hydrofile, delimiter=','))
lat = data[0] 
lon = data[1]
qsurf = data[2]
sm1 = data[3]
m = mapformat()

fire2 = mpl.colors.ListedColormap(np.power(np.loadtxt('cmaps/fire.txt'),1.5)/np.power(255,1.5))

formulation = 4 # without end-of-life
percentileix = 2 # 2 = max revisit, 5 = avg revisit, 6 = 90% revisit, 7 = 95% revisit

for d in xrange(1,11):
  aerofile = './drones/aero_coverage_f%d_d%d.csv' % (formulation,d)

  data = np.transpose(np.loadtxt(aerofile, delimiter=','))
  a_lat = data[0]
  a_lon = data[1]
  a_lon[a_lon < 0] += 360 # convert to [0,360] grid
  revisit = data[percentileix]/60

  array = np.empty((180,360))
  array[:] = np.NAN;

  x = np.arange(0.5, 360.5, 1.0)
  y = np.arange(-90.5, 89.5, 1.0)
  x,y = np.meshgrid(x,y)
  x,y = m(x,y)

  for i in xrange(0, lat.size):
      ilat = int(lat[i] + 90.0 - 0.5)
      ilon = int(lon[i] - 0.5)
      idx = np.where((np.floor(a_lat) == np.floor(lat[i])) & (np.floor(a_lon) == np.floor(lon[i])))
      array[ilat,ilon] = max(revisit[idx] - qsurf[i], 0.001)

  array_mask = np.ma.masked_where(np.isnan(array),array)

  m.pcolormesh(x,y,array_mask,vmin=0.0,vmax=7.0, cmap=fire2, rasterized=True, edgecolor='0.6', linewidth=0)
  cbar = m.colorbar()
  cbar.solids.set_edgecolor("face")
  cbar.set_ticks([0,1,2,3,4,5,6,7])
  plt.title("Deficit (hrs): F3 with Max Revisit")

  outfile = "./figures/drones/covdef_qsurf_f%d_d%d.svg" % (formulation,d)
  plt.savefig(outfile, format="svg")
