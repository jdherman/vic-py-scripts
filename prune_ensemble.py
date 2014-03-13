import netCDF4 as nc
import numpy as np
import os
import sys
import time

rank = int(sys.argv[1])
size = int(sys.argv[2])

#Read in the defaults soils file
soils_file = '/u/sciteam/nchaney/projects/PSU_AERO_PU/1.0deg/global_soils_default.txt'
data = np.loadtxt(soils_file,usecols=(2,3)).T
lat = data[0]
lon = data[1]
nlines = 50
nt = 184088

#Retrieve the variable names
file = '/scratch/sciteam/jdh33/vic_hypercube_output/file_%d/nc/hcube_lat_%.6f_long_%.6f.nc4' % (0,lat[0],lon[0])
fp = nc.Dataset(file,'r')
vars = fp.variables.keys()
fp.close()

#For each cell, read in the acceptable soil file
icell = rank
ncells = lat.size
ncores = size
while icell < ncells:

 file = '/scratch/sciteam/jdh33/vic_hypercube_output/params_below_5percent_error/params_lat_%.6f_long_%.6f.txt' % (lat[icell],lon[icell])
 output = {}
 if os.path.exists(file):
  tic = time.clock()
  print icell,lat[icell],lon[icell]
  data = np.loadtxt(file)
  if data.size < 12:
   icell = icell + size
   continue
  #Open output file to store the behavioral parameters
  file_out = '/scratch/sciteam/nchaney/data/PSU_AERO_PU/1.0deg/HC_Output/ENSEMBLES_DATASET/cell_lat_%.6f_long_%.6f.nc' % (lat[icell],lon[icell])
  fp_out = nc.Dataset(file_out,'w',format='NETCDF4')

  #Extract n random simulations
  maxn = 100
  if data.shape[0] > maxn: ensembles = np.random.choice(np.arange(data.shape[0]),maxn,replace=False)
  else: ensembles = np.arange(data.shape[0])
  nens = ensembles.size
  data = data[ensembles,:]

  #Create dimensions
  fp_out.createDimension('nt',nt)
  fp_out.createDimension('nens',nens)

  #Load all the data for a given variables
  nfiles = 20
  tic = time.clock()
  for var in vars:
   output = []
   for ifile in np.arange(nfiles):
    idx = np.where(data[:,0] == ifile)[0]
    ensembles = data[idx,1].astype(int)
    file = '/scratch/sciteam/jdh33/vic_hypercube_output/file_%d/nc/hcube_lat_%.6f_long_%.6f.nc4' % (ifile,lat[icell],lon[icell])
    if os.path.exists(file) == False: continue #SKIP IF FILE IS CORRUPTED
    if ensembles.size == 0: continue #SKIP IF THE NUMBER OF ENSEMBLES IS 0
    fp = nc.Dataset(file,'r')
    vars = fp.variables.keys()
    for iens in ensembles:
     output.append(fp.variables[var][iens,:])
    fp.close()

   #Turn into array
   output = np.array(output)

   #Output the array
   fp_out.createVariable(var,'f4',('nens','nt'),zlib=True,chunksizes=(1,nt))
   fp_out.variables[var][:] = output
  print icell,time.clock() - tic

  #Close the output file
  fp_out.close()

 icell = icell + ncores
