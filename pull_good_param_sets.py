from __future__ import division
import numpy as np
import os
import math
import sys

PATH = '/u/sciteam/jdh33/scratch/vic_hypercube_output_10K'

LL = np.loadtxt('%s/global_soils_default.txt' % PATH);
LL = LL[:,2:4]

ERROR_THRESHOLD = int(sys.argv[1])/100
icell = int(sys.argv[2])
mpisize = int(sys.argv[3])
num_files = 200

OBS = np.loadtxt('%s/VIC_GRDC_Monthly_Climatology.txt' % PATH, delimiter=',', skiprows=1)

i = icell
matrix_to_save = []
matrix_to_save = np.array(matrix_to_save)
current_obs = OBS[np.where((OBS[:,0] == LL[i,0]) & (OBS[:,1] == LL[i,1])), 2:15]

# if(i % 100 == 0):
#     print 'Cell: ' + '%d' % i + '/15836'

for filenum in xrange(0, num_files):

    output_filename = '%s' % PATH + 'file_' + '%d' % filenum + '/txt/hcube_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'
    param_filename = '/u/sciteam/jdh33/projects/VIC/vic_hypercube_9_50_' + '%d' % filenum + '.txt'
    params = np.loadtxt(param_filename)        
    
    if(os.path.isfile(output_filename)):
        try:
            output = np.loadtxt(output_filename)
        except:
            pass

        if (current_obs.size > 0) and (np.sum(current_obs) > 0):
            error_values = np.zeros(output[:,0].size, float)

            for j in xrange(0, error_values.size):
                error_values[j] = math.fabs(np.sum(current_obs) - np.sum(output[j,:]))/np.sum(current_obs)

            idx = np.flatnonzero(error_values < ERROR_THRESHOLD)

            if(idx.size > 0):
                idx = np.reshape(idx, (idx.shape[0], 1))
                params_to_save = np.hstack((filenum*np.ones((idx.shape[0], 1)), idx, params[idx[:,0],:]))
                if(matrix_to_save.size == 0):
                    matrix_to_save = params_to_save
                else:
                    matrix_to_save = np.vstack((matrix_to_save, params_to_save))

if(matrix_to_save.size > 0):
    np.savetxt('%s' % PATH + 'params_below_' + '%d' % int(sys.argv[1]) + 'percent_error/params_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt', matrix_to_save)
