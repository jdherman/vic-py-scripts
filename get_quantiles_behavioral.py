import numpy as np
from scipy import stats
import netCDF4 as nc
import os

#Read in the observations
LL = np.loadtxt('global_soils_default.txt');
LL = LL[:,2:4]
fdir = 'results_hcube_10K_60yr/'

matrix_to_save = np.hstack((LL, np.empty((LL.shape[0], 9), float)))
matrix_to_save[:,2:11] = np.NaN
param_mins = np.transpose(np.array([-3.0, -3.0, -1.0, 0.2, 0.1, 0.1, -1.0, 1.0, 2.0]))
param_maxes = np.transpose(np.array([0.0, 0.0, 1.69897, 1.0, 3.0, 3.0, 1.0, 30.0, 4.0]))

for i in xrange(0, LL.shape[0]):

  if(i % 100 == 0):
    print 'Cell: ' + '%d' % i + '/15836'

  lat = LL[i,0]
  lon = LL[i,1]

  filename = '%s' % fdir + '/params_below_5percent_error/params_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'

  if(os.path.isfile(filename)):
      try:
          params = np.loadtxt(filename, ndmin = 2)
      except:
          pass

      if(params.shape[0] > 5):

        idx = np.int_(params[:,0]*50 + params[:,1])

        file = '%s' % fdir + 'ensemble-stats-nc/cell_lat_%.6f_long_%.6f.nc' % (lat,lon)
        fp = nc.Dataset(file,'r')
        Q1 = fp.groups['DAILY'].groups['Q'].variables['p1'][idx]     
        Q99 = fp.groups['DAILY'].groups['Q'].variables['p99'][idx]   

        # normalize the parameter values
        for j in range(0, params.shape[0]):
          params[j,2:] = (params[j,2:] - param_mins)/(param_maxes - param_mins)
        # calculate empirical cdf values
        for k in range(2, params.shape[1]):
          rho,p = stats.spearmanr(params[:,k],Q99) # OR Q99
          if p < 0.01:
            matrix_to_save[i,k] = rho
          else:
            matrix_to_save[i,k] = 0

        fp.close()

np.savetxt('vic_hcube_spearman_p99.txt', matrix_to_save)
