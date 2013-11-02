from __future__ import division
import numpy as np
import os
import math
import sys
from scipy.spatial.distance import pdist
from scipy.stats import scoreatpercentile

LL = np.loadtxt('global_soils_default.txt');
LL = LL[:,2:4]

matrix_to_save = np.hstack((LL, np.empty((LL.shape[0], 6), float)))
matrix_to_save[:,2:10] = np.NaN

# PARAMS: b_infilt, Ds, Dsmax, Ws, layer2depth, layer3depth
param_mins = np.transpose(np.array([0.001, 0.001, 0.1, 0.2, 0.1, 0.1]))
param_maxes = np.transpose(np.array([1.0, 1.0, 50.0, 1.0, 3.0, 3.0]))

b_infilt -3.0 0.0
Ds -3.0 0.0
Dsmax -1.0 1.69897
Ws 0.2 1.0
layer2depth 0.1 3.0
layer3depth 0.1 3.0
rmin -1.0 1.0
expt 1.0 30.0
Ksat 3.0 5.0

for i in xrange(0, LL.shape[0]):
    
    if(i % 100 == 0):
        print 'Cell: ' + '%d' % i + '/15836'

    filename = 'params_below_5percent_error/params_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'

    if(os.path.isfile(filename)):
        try:
            params = np.loadtxt(filename, ndmin = 2)
        except:
            pass

        if(params.shape[0] > 5):

            for j in range(0, params.shape[0]):
                params[j,2:] = (params[j,2:] - param_mins)/(param_maxes - param_mins)

            for j in range(2, params.shape[1]):
                matrix_to_save[i,2+j] = np.std(params[:,j])

np.savetxt('vic_hcube_param_stdevs.txt', matrix_to_save)