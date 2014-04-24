from __future__ import division
import numpy as np
import os
import math
import sys

filenum = int(sys.argv[1])
mpisize = int(sys.argv[2])

PATH = '/u/sciteam/jdh33/scratch/vic_hypercube_output_10K'
LL = np.loadtxt('%s/global_soils_default.txt' % PATH);
LL = LL[:,2:4]

OBS = np.loadtxt('%s/VIC_GRDC_Monthly_Climatology.txt' % PATH, delimiter=',', skiprows=1)

# Calculate and save the sum and max errors, along with size of set.
matrix_to_save = np.hstack((LL[:,0:2], np.zeros((LL[:,1].size, 8), float)))
matrix_to_save[:, 2:10] = np.NaN

for i in xrange(0, LL[:,0].size):
    
    output_filename = '%s' % PATH + '/file_' + '%d' % filenum + '/txt/hcube_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'
    
    # if(i % 100 == 0):
    #     print 'Job ' + '%d' % filenum + ': ' + '%d' % i + '/15836'
    
    if(os.path.isfile(output_filename)):
        try:
            output = np.loadtxt(output_filename)
        except:
            pass

        
        current_obs = OBS[np.where((OBS[:,0] == LL[i,0]) & (OBS[:,1] == LL[i,1])), 2:15]

        if (current_obs.size > 0) and (np.sum(current_obs) > 0):
            error_values = np.zeros((output[:,0].size, 1), float)

            for j in xrange(0, error_values.size):
                error_values[j] = math.fabs(np.sum(current_obs) - np.sum(output[j,:]))/np.sum(current_obs)

            num_solutions = output[:,0].size
            min_error = np.min(error_values)
            average = np.mean(error_values)
            max_error = np.max(error_values)

            twenty = error_values[error_values < 0.2].size/error_values.size
            ten = error_values[error_values < 0.1].size/error_values.size
            five = error_values[error_values < 0.05].size/error_values.size
            one = error_values[error_values < 0.01].size/error_values.size

            matrix_to_save[i,2:10] = [num_solutions, min_error, average, max_error, twenty, ten, five, one];

np.savetxt('%s' % PATH + '/vic_10K_error_measures/vic_error_9p_10K_' + '%d' % filenum + '.txt', matrix_to_save);