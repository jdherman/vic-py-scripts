from __future__ import division
import numpy as np
import os
import math
import sys

LL = np.loadtxt('global_soils_default.txt');
LL = LL[:,2:4]

for i in xrange(0, LL[:,0].size):

    param_filename = 'params_below_5percent_error/params_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'
    if not os.path.isfile(param_filename):
        print 'Skipping ... ' + str(i)
        continue
    if(i % 100 == 0):
        print 'Cell: ' + '%d' % i + '/15836'
    
    matrix_to_save = np.array([])
    params = np.loadtxt(param_filename, ndmin = 2)        

    if(params.shape[0] < 100):
        matrix_to_save = params
    else:
        indexlist = np.arange(params[:,0].size)
        np.random.shuffle(indexlist)
        matrix_to_save = params[indexlist[0:100],:]

    np.savetxt('params_below_5percent_error_max_100/params_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt', matrix_to_save)
