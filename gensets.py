from __future__ import division
import numpy as np
import os
import math

LL = np.loadtxt('global_soils_default.txt');
LL = LL[:,2:4]

num_sets = 1000
num_sets_per_file = 50
# 6477 cells total that made it to this point

# each parameter set (0-999) has a list of LL points to save (for which it satisfies 5% error)
ll_to_save = [[] for i in range(num_sets)]

for i in xrange(0, LL[:,0].size):

    param_filename = 'params_below_5percent_error/params_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'
    if not os.path.isfile(param_filename):
        continue
    if(i % 100 == 0):
        print 'Cell: ' + '%d' % i + '/15836'
    
    params = np.loadtxt(param_filename, ndmin = 2)    

    for p in xrange(0, num_sets):
        nfile = math.floor(p/50)
        nline = p % 50   

        if [nfile, nline] in params[:,0:2].tolist():
            ll_to_save[p].append([LL[i,0], LL[i,1]])

# then save them all
for p in xrange(0, num_sets):
    np.savetxt('gensets/paramset_' + str(p) + '.txt', np.array(ll_to_save[p]))