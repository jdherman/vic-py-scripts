from __future__ import division
import numpy as np
import netCDF4 as nc

# LL = np.loadtxt('global_soils_default.txt');
# LL = LL[:,2:4]
fdir = 'results_hcube_10K_60yr/'

file_obs = '%s' % fdir + 'climatology-nc/vic_LHS_climatology_cells_v2.nc'
fp_obs = nc.Dataset(file_obs)
lats = fp_obs.variables['latitude'][:]
lons = fp_obs.variables['longitude'][:]
lats = np.reshape(lats, (lats.shape[0],1))
lons = np.reshape(lons, (lons.shape[0],1))

mean_init = np.hstack((lats, lons, np.empty((lats.shape[0], 9), float)))
mean_init[:,2:11] = np.NaN
mean_ann = np.hstack((lats, lons, np.empty((lats.shape[0], 9), float)))
mean_ann[:,2:11] = np.NaN
mean_mon = np.hstack((lats, lons, np.empty((lats.shape[0], 9), float)))
mean_mon[:,2:11] = np.NaN

# PARAMS: b_infilt, Ds, Dsmax, Ws, layer2depth, layer3depth, rmin, expt, Ksat
param_mins = np.transpose(np.array([-3.0, -3.0, -1.0, 0.2, 0.1, 0.1, -1.0, 1.0, 2.0]))
param_maxes = np.transpose(np.array([0.0, 0.0, 1.69897, 1.0, 3.0, 3.0, 1.0, 30.0, 4.0]))

# import and normalize the initial parameter values
iparams = np.loadtxt('param_samples/vic_LHS_params_10k.txt')

for i in range(0, iparams.shape[0]):
    iparams[i,:] = (iparams[i,:] - param_mins)/(param_maxes - param_mins)

for i in xrange(0, lats.shape[0]):
    
    if(i % 100 == 0):
        print 'Cell: ' + '%d' % i + '/15836'

    obs_runoff = fp_obs.variables['obs_runoff'][i,:] # 1 x 12
    vic_runoff = fp_obs.variables['vic_runoff'][i,:,:] # 10,000 x 12

    if np.ma.count(obs_runoff) == 0: # ignore masked fill_values
        continue

    vic_ann_sum = np.reshape(np.sum(vic_runoff,axis=1),(10000,1))
    obs_sum = np.sum(obs_runoff)
    ann_err = 100*np.absolute((vic_ann_sum - obs_sum)/obs_sum)
    ann_err = np.reshape(ann_err, (10000,))

    r_num = np.sum(np.multiply(np.subtract(vic_runoff,np.reshape(np.mean(vic_runoff,axis=1),(10000,1))),np.subtract(obs_runoff,np.mean(obs_runoff))),axis=1)
    r_den1 = np.sqrt(np.sum(np.power(np.subtract(vic_runoff,np.reshape(np.mean(vic_runoff,axis=1),(10000,1))),2),axis=1))
    r_den2 = np.sqrt(np.sum(np.power(np.subtract(obs_runoff,np.mean(obs_runoff)),2)))
    r = np.divide(r_num,np.multiply(r_den1,r_den2))
    r = np.reshape(r, (10000,))

    mean_init[i,2:11] = np.mean(iparams, axis=0)
    idx1 = np.where(ann_err < 10)[0]
    idx2 = np.where((ann_err < 10) & (r > 0.75))[0]

    if idx1.size > 0:
        mean_ann[i,2:11] = np.mean(iparams[idx1,:], axis=0)
        if idx2.size > 0:
            mean_mon[i,2:11] = np.mean(iparams[idx2,:], axis=0)
        
np.savetxt('vic_hcube_param_mean_init.txt', mean_init)
np.savetxt('vic_hcube_param_mean_ann.txt', mean_ann)
np.savetxt('vic_hcube_param_mean_mon.txt', mean_mon)

fp_obs.close()

