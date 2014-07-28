from __future__ import division
import numpy as np
from mpl_toolkits.basemap import Basemap

def mapformat():

  m = Basemap(projection='robin', lon_0=0,resolution='c')
  # resolution c, l, i, h, f in that order

  m.drawmapboundary(fill_color='white', zorder=-1)
  m.fillcontinents(color='0.8', lake_color='white', zorder=0)

  m.drawcoastlines(color='0.6', linewidth=0.5)
  m.drawcountries(color='0.6', linewidth=0.5)

  m.drawparallels(np.arange(-90.,91.,30.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5')
  m.drawmeridians(np.arange(0., 360., 60.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5')

  return m
