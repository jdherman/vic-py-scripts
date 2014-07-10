from __future__ import division
import numpy as np
import statsmodels.api as sm
from scipy import stats
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

error_to_save = np.hstack((lats, lons, np.empty((lats.shape[0], 4), float)))
error_to_save[:,2:9] = np.NaN

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

    r_num = np.sum(np.multiply(np.subtract(vic_runoff,np.reshape(np.mean(vic_runoff,axis=1),(10000,1))),np.subtract(obs_runoff,np.mean(obs_runoff))),axis=1)
    r_den1 = np.sqrt(np.sum(np.power(np.subtract(vic_runoff,np.reshape(np.mean(vic_runoff,axis=1),(10000,1))),2),axis=1))
    r_den2 = np.sqrt(np.sum(np.power(np.subtract(obs_runoff,np.mean(obs_runoff)),2)))
    r = np.divide(r_num,np.multiply(r_den1,r_den2))

    a = np.std(vic_runoff,axis=1)/np.std(obs_runoff)
    B = np.mean(vic_runoff,axis=1)/np.mean(obs_runoff)
    kge = 1 - np.sqrt(np.power(r-1,2) + np.power(a-1,2) + np.power(B-1,2))

    kge = np.reshape(kge,(10000,))
    ann_err = np.reshape(ann_err, (10000,))
    r = np.reshape(r, (10000,))
    a = np.reshape(a, (10000,))

    ann20 = kge[(ann_err < 20)].size/kge.size
    ann10 = kge[(ann_err < 10)].size/kge.size
    ann10monR50 = kge[(r > 0.5) & (ann_err < 10)].size/kge.size
    ann10monR75 = kge[(r > 0.75) & (ann_err < 10)].size/kge.size
    error_to_save[i,2:6] = [ann20, ann10, ann10monR50, ann10monR75];
        
np.savetxt('vic_error_9p_10k.txt', error_to_save)

fp_obs.close()
