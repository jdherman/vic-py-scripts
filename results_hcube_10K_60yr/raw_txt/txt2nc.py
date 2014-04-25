from __future__ import division
from netCDF4 import Dataset
import numpy as np
import os
import math

PATH = '/u/sciteam/jdh33/scratch/vic_hypercube_output_10K'
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
root_grp.createDimension('params', 9)

# variables
latitudes = root_grp.createVariable('latitude', 'f4', ('lat,'))
longitudes = root_grp.createVariable('longitude', 'f4', ('lon,'))
vic_runoff = root_grp.createVariable('vic_runoff', 'f4', ('ensemble', 'month', 'lat', 'lon',))
obs_runoff = root_grp.createVariable('obs_runoff', 'f4', ('month', 'lat', 'lon',))
annual_error = root_grp.createVariable('annual_error', 'f4', ('ensemble', 'lat', 'lon',))
monthly_error = root_grp.createVariable('monthly_error', 'f4', ('ensemble', 'month', 'lat', 'lon',))

# set the variables we know first
latitudes = np.arange(-90.5, 89.5, 1.0)
longitudes = np.arange(0.5, 360.5, 1.0)

for lati, lat in enumerate(latitudes):
  for loni, lon in enumerate(longitudes):
    
    # grab the index of the 0-15836 list of grid cells
    i = np.where((np.floor(LL[:,0]) == np.floor(lat)) & (np.floor(LL[:,1]) == np.floor(lon)))
    current_obs = OBS[np.where((OBS[:,0] == LL[i,0]) & (OBS[:,1] == LL[i,1])), 2:15]
    obs_runoff[:,lati,loni] = current_obs

    for filenum in xrange(0,200):

      output_filename = '%s' % PATH + '/file_' + '%d' % filenum + '/txt/hcube_lat_' + '%.6f' % LL[i,0] + '_long_' + '%.6f' % LL[i,1] + '.txt'
    
      if(os.path.isfile(output_filename)):
        try:
            output = np.loadtxt(output_filename)
        except:
            pass

        # write the VIC output data
        ensemble_start = filenum*50
        vic_runoff[ensemble_start:(ensemble_start+50),:,lati,loni] = np.transpose(output) # ensembles x months

# also get error values
for j in xrange(0, len(ensemble)):
  annual_error[j,:,:] = math.fabs(np.sum(obs_runoff, axis=0) - np.sum(vic_runoff[j,:,:,:], axis=0))/np.sum(obs_runoff, axis=0)

  for m in xrange(0, 12):
    monthly_error[j,m,:,:] = math.fabs(obs_runoff[m,:,:] - vic_runoff[j,m,:,:])/obs_runoff[m,:,:]


root_grp.close()