from __future__ import division
import numpy as np
import os
import math
import sys
from scipy.spatial.distance import pdist
from scipy.stats import scoreatpercentile

LL = np.loadtxt('global_soils_default.txt');
LL = LL[:,2:4]

matrix_to_save = np.hstack((LL, np.empty((LL.shape[0], 8), float)))
matrix_to_save[:,2:10] = np.NaN

# PARAMS: b_infilt, Ds, Dsmax, Ws, layer2depth, layer3depth
param_mins = np.transpose(np.array([0.001, 0.001, 0.1, 0.2, 0.1, 0.1]))
param_maxes = np.transpose(np.array([1.0, 1.0, 50.0, 1.0, 3.0, 3.0]))

for i in xrange(0, LL.shape[0]):
    
    if(i % 100 == 0):
        print 'Cell: ' + '%d' % i + '/15836'

    filename = 'params_below_5percent_error/params_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'

    if(os.path.isfile(filename)):
        try:
            params = np.loadtxt(filename, ndmin = 2)
        except:
            pass

        if(params.shape[0] > 1):

            for j in range(0, params.shape[0]):
                params[j,:] = (params[j,:] - param_mins)/(param_maxes - param_mins)

            dists = pdist(params, 'euclidean').flatten()
            dists = np.sort(dists)
            matrix_to_save[i,2] = np.amax(dists)
            matrix_to_save[i,3] = np.mean(dists)
            matrix_to_save[i,4] = np.median(dists)
            matrix_to_save[i,5] = np.amin(dists)
            matrix_to_save[i,6] = scoreatpercentile(dists, 25)
            matrix_to_save[i,7] = scoreatpercentile(dists, 75)
            matrix_to_save[i,8] = scoreatpercentile(dists, 90)
            matrix_to_save[i,9] = scoreatpercentile(dists, 95)

            # Normalize by max possible distance (6 parameters - sqrt(n))
            matrix_to_save[i,2:10] = matrix_to_save[i,2:10]/math.sqrt(6)

np.savetxt('vic_hcube_norm_distance_stats.txt', matrix_to_save)