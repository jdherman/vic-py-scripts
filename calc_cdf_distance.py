from __future__ import division
import numpy as np
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt
import time

LL = np.loadtxt('global_soils_default.txt');
LL = LL[:,2:4]
fdir = 'results_hcube_10K_60yr'

matrix_to_save = np.hstack((LL, np.empty((LL.shape[0], 9), float)))
matrix_to_save[:,2:11] = np.NaN

# PARAMS: b_infilt, Ds, Dsmax, Ws, layer2depth, layer3depth, rmin, expt, Ksat
param_mins = np.transpose(np.array([-3.0, -3.0, -1.0, 0.2, 0.1, 0.1, -1.0, 1.0, 2.0]))
param_maxes = np.transpose(np.array([0.0, 0.0, 1.69897, 1.0, 3.0, 3.0, 1.0, 30.0, 4.0]))

# b_infilt -3.0 0.0
# Ds -3.0 0.0
# Dsmax -1.0 1.69897
# Ws 0.2 1.0
# layer2depth 0.1 3.0
# layer3depth 0.1 3.0
# rmin -1.0 1.0
# expt 1.0 30.0
# Ksat 2.0 4.0

# import and normalize the initial parameter values
nbins = 100
x = np.linspace(0,1,num=nbins)
iparams = np.loadtxt('param_samples/vic_LHS_params_10k.txt')
iecdf = np.zeros((nbins,iparams.shape[1]))
pecdf = np.zeros((nbins,iparams.shape[1]))

for i in range(0, iparams.shape[0]):
    iparams[i,:] = (iparams[i,:] - param_mins)/(param_maxes - param_mins)
for j in range(0, iparams.shape[1]):
    ecdf = sm.distributions.ECDF(iparams[:,j])
    iecdf[:,j] = ecdf(x)

# plt.step(x,iecdf[:,8])
# plt.show()


for i in xrange(0, LL.shape[0]):
    
    if(i % 100 == 0):
        print 'Cell: ' + '%d' % i + '/15836'

    filename = '%s' % fdir + '/params_below_5percent_error/params_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'

    if(os.path.isfile(filename)):
        try:
            params = np.loadtxt(filename, ndmin = 2)
        except:
            pass

        if(params.shape[0] > 5):

            # normalize the parameter values
            for j in range(0, params.shape[0]):
                params[j,2:] = (params[j,2:] - param_mins)/(param_maxes - param_mins)
            # calculate empirical cdf values
            for k in range(2, params.shape[1]):
                ecdf = sm.distributions.ECDF(params[:,k])
                pecdf[:,k-2] = ecdf(x)
                y = np.absolute(iecdf[:,k-2]-pecdf[:,k-2])
                matrix_to_save[i,k] = np.trapz(y,x)
                
np.savetxt('vic_hcube_param_cdfdist.txt', matrix_to_save)