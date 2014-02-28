from __future__ import division
import numpy as np
import os
import math
import sys
from scipy.spatial.distance import pdist
from pylab import *

LL = np.loadtxt('global_soils_default.txt');
LL = LL[:,2:4]

matrix_to_save = np.hstack((LL, np.empty((LL.shape[0], 8), float)))
matrix_to_save[:,2:10] = np.NaN

# PARAMS: b_infilt, Ds, Dsmax, Ws, layer2depth, layer3depth
param_mins = np.transpose(np.array([0.001, 0.001, 0.1, 0.2, 0.1, 0.1]))
param_maxes = np.transpose(np.array([1.0, 1.0, 50.0, 1.0, 3.0, 3.0]))

# Three subplots sharing both x/y axes
f, subaxes = plt.subplots(10, 10, sharex=True, sharey=True)

plotnum = 0

for i in xrange(0, LL.shape[0], 30):
    
    if(plotnum > 99):
        break

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
                params[j,:] = (params[j,:] - param_mins)/(param_maxes - param_mins)

            titlestring = 'Lat: %.3f, Lon: %.3f' % (LL[i,0], LL[i,1])
            curr_ax = subaxes[plotnum/10, plotnum%10]
            curr_ax.boxplot(params,0)
            plotnum += 1
            print plotnum

tight_layout(pad=0, h_pad=0, w_pad=0)
setp([a.get_yticklabels() for a in f.axes], visible=False)
show()