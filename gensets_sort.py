from __future__ import division
import numpy as np
import os
import math

num_sets = 1000
num_sets_per_file = 50
# 6476 cells total that made it to this point

# each parameter set (0-999) has a list of LL points to save (for which it satisfies 5% error)
latlon = [[] for i in range(num_sets)]
lengths = [0] * num_sets

for p in range(num_sets):
    latlon[p] = (np.loadtxt('gensets/paramset_' + str(p) + '.txt')*10).astype(int).tolist()
    lengths[p] = len(latlon[p])
    latlon[p] = [tuple(item) for item in latlon[p]]

# mush = [item for sublist in latlon for item in sublist]
# print len(set(mush))

counter = 0
cumulative = 0

while counter < 200:
    maxindex = lengths.index(max(lengths))
    cumulative += lengths[maxindex]
    print str(counter) + " " + str(maxindex) + " " + str(lengths[maxindex]) + " " + str(cumulative)

    current_max_set = set(latlon[maxindex])

    for p in range(num_sets):
        latlon[p] = [a for a in latlon[p] if a not in current_max_set]
        lengths[p] = len(latlon[p])

    counter += 1

# for i in xrange(0, LL[:,0].size):

#     param_filename = 'params_below_5percent_error/params_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'
#     if not os.path.isfile(param_filename):
#         continue
#     if(i % 100 == 0):
#         print 'Cell: ' + '%d' % i + '/15836'
    
#     params = np.loadtxt(param_filename, ndmin = 2)    

#     for p in xrange(0, num_sets):
#         nfile = math.floor(p/50)
#         nline = p % 50   

#         if [nfile, nline] in params[:,0:2].tolist():
#             ll_to_save[p].append([LL[i,0], LL[i,1]])