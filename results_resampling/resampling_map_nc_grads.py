import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import numpy as np
import grads
from mpl_toolkits.basemap import cm
ga = grads.GrADS(Bin='grads',Window=False,Echo=False)
def plot_variables(vmin,vmax,var):

 #min
 plt.figure(figsize=(17,8.5))
 levels = np.linspace(vmin,vmax,100)
 norm = mpl.colors.Normalize(vmin=np.min(levels),vmax=np.max(levels),clip=False)
 ga.imshow('smth9(%smin)' % var,interpolation='nearest',norm=norm,cmap=plt.cm.jet)
 plt.title('%s - minimum' % var,fontsize=20)
 file = '/home/ice/nchaney/Dropbox/BlueWaters/RESAMPLING/%smin.png' % var
 plt.savefig(file)
 os.system('convert %s -trim %s' % (file,file))

 #mean
 plt.figure(figsize=(17,8.5))
 levels = np.linspace(vmin,vmax,100)
 norm = mpl.colors.Normalize(vmin=np.min(levels),vmax=np.max(levels),clip=False)
 ga.imshow('smth9(%smean)' % var,interpolation='nearest',norm=norm,cmap=plt.cm.jet)
 plt.title('%s - mean' % var,fontsize=20)
 file = '/home/ice/nchaney/Dropbox/BlueWaters/RESAMPLING/%smean.png' % var
 plt.savefig(file)
 os.system('convert %s -trim %s' % (file,file))

 #smax
 plt.figure(figsize=(17,8.5))
 levels = np.linspace(vmin,vmax,100)
 norm = mpl.colors.Normalize(vmin=np.min(levels),vmax=np.max(levels),clip=False)
 ga.imshow('smth9(%smax)' % var,interpolation='nearest',norm=norm,cmap=plt.cm.jet)
 plt.title('%s - maximum' % var,fontsize=20)
 file = '/home/ice/nchaney/Dropbox/BlueWaters/RESAMPLING/%smax.png' % var
 plt.savefig(file)
 os.system('convert %s -trim %s' % (file,file))

metric = 'nse'
file = 'OUTPUT/frequency_nse.nc'
ga("sdfopen %s" % file)

#make plots
#sm1
plot_variables(0,20,'sm1')
#evap
plot_variables(0,20,'evap')
#qsurf
plot_variables(0,5,'qsurf')
