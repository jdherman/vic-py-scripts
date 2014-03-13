import netCDF4 as nc
import numpy as np
import os
import sys
import time
import IO
import datetime

#Read in the defaults soils file
soils_file = '/u/sciteam/nchaney/projects/PSU_AERO_PU/1.0deg/global_soils_default.txt'
data = np.loadtxt(soils_file,usecols=(2,3)).T
lat = data[0]
lon = data[1]
minlat = -89.5
minlon = 0.5
nlat = 180
nlon = 360
res = 1.0
pcts = np.array([1,5,10,25,50,75,90,95,99])
npcts = pcts.size

#Create Metrics for grid
Output = {}

#For each cell, read in the acceptable soil file
ncells = lat.size
icell = 0
while icell < ncells:


 print icell,lat[icell],lon[icell]
 ilat = int((lat[icell] - minlat)/res)
 ilon = int((lon[icell] - minlon)/res)
 #Open file
 file = '/u/sciteam/nchaney/projects/PSU_AERO_PU/ANALYISIS/OUTPUT/cell_lat_%.6f_long_%.6f.nc' % (lat[icell],lon[icell])
 if os.path.exists(file) == False:
  icell = icell + 1
  continue
 fp = nc.Dataset(file,'r',format='NETCDF4')
 for var in fp.variables.keys():
   if var not in Output.keys():
    Output[var] = -9.99e+08*np.ones((npcts,nlat,nlon))
    #Output[grpn][var] = np.ones((nlat,nlon))
   Output[var][:,ilat,ilon] = fp.variables[var][:]
   #print Output[grpn][var][ilat,ilon]
 
 #Close the files
 fp.close()

 icell = icell + 1

#Output data
dims = {}
dims['minlat'] = minlat #-89.8750
dims['minlon'] = minlon #0.1250
dims['nlat'] = nlat #720
dims['nlon'] = nlon #1440
dims['res'] = res
dims['maxlat'] = dims['minlat'] + dims['res']*(dims['nlat']-1)
dims['maxlon'] = dims['minlon'] + dims['res']*(dims['nlon']-1)
dims['undef'] = -9.99e+08
vars = Output.keys()
for var in vars:
 file = 'METRICS/PCT_CVS.nc'
 vars_info = vars
 tstep = 'years'
 fp = IO.Create_NETCDF_File(dims,file,vars,vars_info,datetime.datetime(1990,1,1),tstep,npcts)
 for var in vars:
  fp.variables[var][:] = Output[var].astype(np.float32)
 fp.close()

#Write out the variable names
#fp = open('METRICS/var_names.txt','w')
#for grp in Output:
# fp.write('%s\n' % grp)
#fp.close()

