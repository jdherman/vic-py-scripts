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

cdfdist_to_save = np.hstack((lats, lons, np.empty((lats.shape[0], 9), float)))
cdfdist_to_save[:,2:11] = np.NaN
spearman_to_save = np.hstack((lats, lons, np.empty((lats.shape[0], 9), float)))
spearman_to_save[:,2:11] = np.NaN
error_to_save = np.hstack((lats, lons, np.empty((lats.shape[0], 5), float)))
error_to_save[:,2:7] = np.NaN

# PARAMS: b_infilt, Ds, Dsmax, Ws, layer2depth, layer3depth, rmin, expt, Ksat
param_mins = np.transpose(np.array([-3.0, -3.0, -1.0, 0.2, 0.1, 0.1, -1.0, 1.0, 2.0]))
param_maxes = np.transpose(np.array([0.0, 0.0, 1.69897, 1.0, 3.0, 3.0, 1.0, 30.0, 4.0]))

# import and normalize the initial parameter values
nbins = 100
x = np.linspace(0,1,num=nbins)
iparams = np.loadtxt('param_samples/vic_LHS_params_10k.txt')
iecdf = np.zeros((nbins,iparams.shape[1]))
pecdf1 = np.zeros((nbins,iparams.shape[1]))
pecdf2 = np.zeros((nbins,iparams.shape[1]))

for i in range(0, iparams.shape[0]):
    iparams[i,:] = (iparams[i,:] - param_mins)/(param_maxes - param_mins)
for j in range(0, iparams.shape[1]):
    ecdf = sm.distributions.ECDF(iparams[:,j])
    iecdf[:,j] = ecdf(x)

for i in xrange(0, lats.shape[0]):
    
    if(i % 100 == 0):
        print 'Cell: ' + '%d' % i + '/15836'

    obs_runoff = fp_obs.variables['obs_runoff'][i,:] # 1 x 12
    vic_runoff = fp_obs.variables['vic_runoff'][i,:,:] # 10,000 x 12

    # obs_runoff = np.log(obs_runoff)
    # vic_runoff = np.log(vic_runoff)

    if np.ma.count(obs_runoff) == 0: # ignore masked fill_values
        continue

    vic_ann_sum = np.reshape(np.sum(vic_runoff,axis=1),(10000,1))
    obs_sum = np.sum(obs_runoff)
    ann_err = 100*np.absolute((vic_ann_sum - obs_sum)/obs_sum)

    nse_num = np.sum(np.power(np.subtract(vic_runoff,obs_runoff),2),axis=1)
    nse_den = np.sum(np.power(np.subtract(obs_runoff,np.mean(obs_runoff)),2))
    nse = 1 - np.divide(nse_num,nse_den)
    idx1 = np.where(ann_err < 10)
    idx2 = np.where((ann_err < 10) & (nse > 0.75))

    ann_err = np.reshape(ann_err, (10000,))
    zero = nse[(nse > 0.0) & (ann_err < 10)].size/nse.size
    five = nse[(nse > 0.5) & (ann_err < 10)].size/nse.size
    seventyfive = nse[(nse > 0.75) & (ann_err < 10)].size/nse.size
    eight = nse[(nse > 0.8) & (ann_err < 10)].size/nse.size
    nine = nse[(nse > 0.9) & (ann_err < 10)].size/nse.size

    error_to_save[i,2:7] = [zero, five, seventyfive, eight, nine]

    # vic_ratio = np.divide(vic_runoff,vic_ann_sum)
    # obs_ratio = np.divide(obs_runoff,obs_sum)
    # mon_err = 100*np.max(np.absolute(np.subtract(vic_ratio,obs_ratio)),axis=1)

    # ann_err = np.reshape(ann_err, (10000,))
    # twenty = mon_err[(mon_err < 20) & (ann_err < 10)].size/mon_err.size
    # ten = mon_err[(mon_err < 10) & (ann_err < 10)].size/mon_err.size
    # five = mon_err[(mon_err < 5) & (ann_err < 10)].size/mon_err.size
    # one = mon_err[(mon_err < 1) & (ann_err < 10)].size/mon_err.size

    # twenty = mon_err[mon_err < 20].size/mon_err.size
    # ten= mon_err[mon_err < 10].size/mon_err.size
    # five = mon_err[mon_err < 5].size/mon_err.size
    # one = mon_err[mon_err < 1].size/mon_err.size

    # error_to_save[i,2:9] = [np.min(mon_err), np.mean(mon_err), np.max(mon_err), twenty, ten, five, one];

    if idx1[0].size > 0:
        params1 = iparams[idx1,:]
        params2 = iparams[idx2,:]
        # cdf distance calculations
        for k in range(0, params1.shape[1]):
            ecdf1 = sm.distributions.ECDF(params1[:,k])
            pecdf1[:,k] = ecdf1(x)
            ecdf2 = sm.distributions.ECDF(params2[:,k])
            pecdf2[:,k] = ecdf2(x)
            y = np.absolute(pecdf1[:,k]-pecdf2[:,k])
            cdfdist_to_save[i,k+2] = np.trapz(y,x)

        # spearman with behavioral parameters and daily quantiles
        file = '%s' % fdir + 'ensemble-stats-nc/cell_lat_%.6f_long_%.6f.nc' % (lats[i],lons[i])
        fp = nc.Dataset(file,'r')
        Q1 = fp.groups['DAILY'].groups['Q'].variables['p1'][idx2]     
        Q99 = fp.groups['DAILY'].groups['Q'].variables['p99'][idx2]   
        fp.close()

        for k in range(0, params2.shape[1]):
          rho,p = stats.spearmanr(params2[:,k],Q99) # OR Q99
          if p < 0.01:
            spearman_to_save[i,k+2] = rho
          else:
            spearman_to_save[i,k+2] = 0
        
np.savetxt('vic_hcube_param_cdfdist_monthly.txt', cdfdist_to_save)
np.savetxt('vic_hcube_param_spearman_monthly.txt', spearman_to_save)
np.savetxt('vic_error_9p_10k_monthly_nse.txt', error_to_save)

fp_obs.close()
