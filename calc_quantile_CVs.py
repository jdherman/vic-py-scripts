import netCDF4 as nc
import numpy as np
import scipy.stats
import os
import sys
import time

rank = int(sys.argv[1])
size = int(sys.argv[2])
pcts = np.array([1,5,10,25,50,75,90,95,99])

#Read in the defaults soils file
soils_file = '/u/sciteam/nchaney/projects/PSU_AERO_PU/1.0deg/global_soils_default.txt'
data = np.loadtxt(soils_file,usecols=(2,3)).T
lat = data[0]
lon = data[1]

#For each cell, read in the acceptable soil file
icell = rank
ncells = lat.size
ncores = size
while icell < ncells:

 #Open file
 file = '/scratch/sciteam/nchaney/data/PSU_AERO_PU/1.0deg/HC_Output/ENSEMBLES_DATASET/cell_lat_%.6f_long_%.6f.nc' % (lat[icell],lon[icell])
 if os.path.exists(file) == False:
  icell = icell + ncores
  continue
 fp = nc.Dataset(file,'r',format='NETCDF4')
 print icell,lat[icell],lon[icell]
 
 #Open output file
 file = '/u/sciteam/nchaney/projects/PSU_AERO_PU/ANALYISIS/OUTPUT/cell_lat_%.6f_long_%.6f.nc' % (lat[icell],lon[icell])
 fp_out = nc.Dataset(file,'w',format='NETCDF4')
 fp_out.createDimension('npcts',pcts.size)

 #Add the pcts info
 fp_out.createVariable('pcts','f4',('npcts'))
 fp_out.variables['pcts'][:] = pcts
 
 #Add the info 
 vars = fp.variables.keys()
 for var in vars:
  #Extract all data for the variable
  data = fp.variables[var][:]
  #Compute the metrics (percentiles cv)
  nens = data.shape[0]
  pcts_info = {}
  for pct in pcts:
   pcts_info[pct] = []
  #Calculate the percentiles
  for iens in xrange(nens):
   data_ens = data[iens,:]
   for pct in pcts:
    pcts_info[pct].append(scipy.stats.scoreatpercentile(data_ens,pct))
  #Calculate the cvs per percentile
  cvs = []
  for pct in pcts_info:
   cvs.append(np.std(pcts_info[pct])/np.mean(pcts_info[pct]))
  cvs = np.array(cvs)
  #Create variable
  fp_out.createVariable(var,'f4',('npcts'))
  #Write variable
  fp_out.variables[var][:] = cvs
 
 #Close the files
 fp.close()
 fp_out.close()

 icell = icell + ncores
