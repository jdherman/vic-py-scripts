from __future__ import division
import numpy as np
import os
import math
import sys

LL = np.loadtxt('global_soils_default.txt');
LL = LL[:,2:4]
num_files = 200

# Calculate and save the sum and max errors, along with size of set.
matrix_to_save = np.hstack((LL[:,0:2], np.zeros((LL[:,1].size, 7), float)))
matrix_to_save[:, 2:9] = np.NaN

all_error_values = np.zeros((20, LL[:,1].size, 10), float)

for i in xrange(0, num_files):
    all_error_values[i,:,:] = np.loadtxt('vic_1K_error_measures/vic_error_9p_1K_' + '%d' % i + '.txt')

for i in xrange(0, LL[:,0].size):

    if(i % 100 == 0):
        print i
    
    current_values = all_error_values[np.where((all_error_values[:,:,0] == LL[i,0]) & (all_error_values[:,:,1] == LL[i,1]))]

    min_error = np.min(current_values[:,3])
    average = np.sum(current_values[:,2]*current_values[:,4])/num_files
    max_error = np.max(current_values[:,5])

    twenty = np.sum(current_values[:,2]*current_values[:,6])/np.sum(current_values[:,2])
    ten = np.sum(current_values[:,2]*current_values[:,7])/np.sum(current_values[:,2])
    five = np.sum(current_values[:,2]*current_values[:,8])/np.sum(current_values[:,2])
    one = np.sum(current_values[:,2]*current_values[:,9])/np.sum(current_values[:,2])

    matrix_to_save[i, 2:9] = [min_error, average, max_error, twenty, ten, five, one];

np.savetxt('vic_error_9p_10K.txt', matrix_to_save);