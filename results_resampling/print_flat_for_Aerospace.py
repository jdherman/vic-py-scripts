from netCDF4 import Dataset
import numpy as np

root_grp = Dataset('frequency_nse.nc')

# dimensions: lon, lat, t
lat = root_grp.variables['lat']
lon = root_grp.variables['lon']

# variables: evapmean, evapmin, evapmax, qsurfmean, qsurfmin, qsurfmax, sm1mean, sm1min, sm1max
fill = root_grp.variables['qsurfmin']._FillValue
qsurfmin = root_grp.variables['qsurfmin'][0]
sm1min = root_grp.variables['sm1min'][0]

for i in xrange(0, lat.size):
  for j in xrange(0, lon.size):

    if qsurfmin[i,j] != fill:
      a = qsurfmin[i,j]
      b = sm1min[i,j]
      print '%0.1f,%0.1f,%0.5f,%0.5f' % (lat[i], lon[j], max(a, 1.0), max(b, 1.0))
