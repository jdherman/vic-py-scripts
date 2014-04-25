from __future__ import division
from netCDF4 import Dataset
import numpy as np
import os
import math

PATH = '.'
LL = np.loadtxt('%s/global_soils_default.txt' % PATH);
LL = LL[:,2:4]
OBS = np.loadtxt('%s/VIC_GRDC_Monthly_Climatology.txt' % PATH, delimiter=',', skiprows=1)

# NC file setup
root_grp = Dataset('vic_LHS_climatology.nc', 'w', format='NETCDF4')
root_grp.description = 'Results from VIC 10K Latin Hypercube ensemble, 60-year simulation on Blue Waters'

# dimensions
root_grp.createDimension('lat', 180)
root_grp.createDimension('lon', 360)
root_grp.createDimension('month', 12)
ensemble = root_grp.createDimension('ensemble', 10000)

# variables
latitudes = root_grp.createVariable('latitude', 'f4', ('lat',))
longitudes = root_grp.createVariable('longitude', 'f4', ('lon',))
vic_runoff = root_grp.createVariable('vic_runoff', 'f4', ('lat', 'lon', 'ensemble', 'month',), fill_value=-9999.0)
obs_runoff = root_grp.createVariable('obs_runoff', 'f4', ('lat', 'lon', 'month'))
annual_error = root_grp.createVariable('annual_error', 'f4', ('lat', 'lon', 'ensemble',))
monthly_error = root_grp.createVariable('monthly_error', 'f4', ('lat', 'lon', 'ensemble', 'month',))

vic_runoff.units = 'mm/month'
obs_runoff.units = 'mm/month'
annual_error.units = '%'
monthly_error.units = '%'

# set the variables we know first
latitudes = np.arange(-90.5, 89.5, 1.0)
longitudes = np.arange(0.5, 360.5, 1.0)

# keep values in memory until ready to write a big chunk to NC file
temp_vic = np.zeros((180, 360, len(ensemble), 12), float)
temp_obs = np.zeros((180, 360, 12), float)
temp_annual_err = np.zeros((180, 360, len(ensemble)), float)
temp_monthly_err = np.zeros((180, 360, len(ensemble), 12), float)

for lati, lat in enumerate(latitudes):
  for loni, lon in enumerate(longitudes):

    # grab the index of the 0-15836 list of grid cells
    i = np.where((np.floor(LL[:,0]) == np.floor(lat)) & (np.floor(LL[:,1]) == np.floor(lon)))

    # if this is one of our land surface grid cells...
    if(np.size(i) > 0):
      current_obs = OBS[np.where((np.floor(OBS[:,0]) == np.floor(lat)) & (np.floor(OBS[:,1]) == np.floor(lon))), 2:15]
      current_obs = np.squeeze(current_obs)

      if(current_obs.size > 0):
        temp_obs[lati,loni,:] = current_obs

      for filenum in xrange(0,200):

        output_filename = '%s' % PATH + '/txt/file_' + '%d' % filenum + '/txt/hcube_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'
      
        if(os.path.isfile(output_filename)):
          try:
              output = np.loadtxt(output_filename)
          except:
              pass

          # write the VIC output data
          ensemble_start = filenum*50
          temp_vic[lati,loni, filenum*50:(filenum+1)*50 ,:] = output # ensembles x months

# also get error values -- ignore for right now
# for j in xrange(0, len(ensemble)):
#   temp_annual_err[:,:,j] = 100*np.fabs(np.sum(temp_obs, axis=2) - np.sum(vic_runoff[j,:,:,:], axis=0))/np.sum(obs_runoff, axis=0)

#   for m in xrange(0, 12):
#     temp_monthly_err[:,:,j,m] = 100*np.fabs(obs_runoff[m,:,:] - vic_runoff[j,m,:,:])/obs_runoff[m,:,:]

vic_runoff = temp_vic
obs_runoff = temp_obs
# annual_error = temp_annual_err
# monthly_error = temp_monthly_err

root_grp.close()