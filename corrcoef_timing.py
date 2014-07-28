from __future__ import division
import numpy as np
import statsmodels.api as sm
from scipy import stats
import netCDF4 as nc
import time

# LL = np.loadtxt('global_soils_default.txt');
# LL = LL[:,2:4]
fdir = 'results_hcube_10K_60yr/'

file_obs = '%s' % fdir + 'climatology-nc/vic_LHS_climatology_cells_v2.nc'
fp_obs = nc.Dataset(file_obs)
lats = fp_obs.variables['latitude'][:]
lons = fp_obs.variables['longitude'][:]
lats = np.reshape(lats, (lats.shape[0],1))
lons = np.reshape(lons, (lons.shape[0],1))

i = 25 # choose a grid cell with values
obs_runoff = fp_obs.variables['obs_runoff'][i,:] # 1 x 12
vic_runoff = fp_obs.variables['vic_runoff'][i,:,:] # 10,000 x 12
times = np.zeros((10,))

def vcorrcoef(X,y):
    Xm = np.reshape(np.mean(X,axis=1),(X.shape[0],1))
    ym = np.mean(y)
    r_num = np.sum((X-Xm)*(y-ym),axis=1)
    r_den = np.sqrt(np.sum((X-Xm)**2,axis=1)*np.sum((y-ym)**2))
    r = r_num/r_den
    return r

for t in xrange(0,10): # average 10 timings
    
    start = time.time()

    # r = np.zeros((10000,1))
    # for k in xrange(0,10000):
    #     r[k] = np.corrcoef(vic_runoff[k,:], obs_runoff)[0,1]

    r = vcorrcoef(vic_runoff,obs_runoff)
    end = time.time()
    times[t] = end-start

print np.mean(times)

fp_obs.close()


