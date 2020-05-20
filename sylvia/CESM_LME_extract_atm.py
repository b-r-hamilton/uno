
# ssh -Y -l sylviad data-access.ucar.edu
# ssh -Y -l sylviad casper.ucar.edu
ssh -Y -l sylviad casper01.ucar.edu

cd /glade/scratch/sylviad


/glade/p/cesm/community/cesmLME/

# Rivers:
#/glade/p/cesm/community/cesmLME/CESM-CAM5-LME/rof/proc/tseries/monthly/QCHANR/

# Atm:

#/glade/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/ocn/proc/tseries/monthly

# /glade/collections/cdg/data/cesmLE/CESM-CAM5-BGC-LE/ocn/proc/tseries/monthly/DIC
#====================================================================
execdav
#====================================================================
module load python/2.7.15
ncar_pylib
ipython
#====================================================================

# - Set up script to pull data from GLADE
# - VARIABLES FOR SAM: (LME)

#/glade/campaign/cesm/collections/cesmLME/CESM-CAM5-LME/atm/proc/tseries/monthly/TREFHT

# ATMOSPHERE

#     - [X] Temperature (TREFT)
#     - [X] Precipitation (PRECT) m/s Total (convective and large-scale) precipitation rate (liq + ice)
#     - [X] SNOWHLND (Water equivalent snow depth)

# LAND:
#     - [ ] Soil liquid water (SOILLIQ) kg/m2
#     - [ ] Soil ice (SOILICE) kg/m2

#     - [ ] Runoff (QRUNOFF) mm/s total runoff
#     - [ ] Snow melt (QMELT) mm/s [QMELT_H2OTR]
#     - [ ] evaporation (QSOIL) mm/s Ground evaporation (soil/snow evaporation + soil/snow sublimation - dew)


# RIVER:
#     - [X] River Flow: LIQ (QCHANR) m3/s

# OTHER: 
#     - [X] Lat lon time

#====================================================================
#====================================================================

import numpy as np
import string
import sys, os#, cdtime, cdutil, cdms2, MV2, time, datetime
import netCDF4
#====================================================================

#====================================================================

dir='/glade/p/cesm/community/cesmLME/CESM-CAM5-LME/atm/proc/tseries/monthly/TREFHT/'

# from netCDF4 import Dataset
file_name=dir+'b.e11.BLMTRC5CN.f19_g16.002.cam.h0.TREFHT.185001-200512.nc'
f = netCDF4.Dataset(file_name)
VAR1=f.variables['TREFHT']

lat = f.variables['lat'][:]
lon = f.variables['lon'][:]
time = f.variables['time'][:]
#====================================================================

# Save only U.S. 
latbounds = [ 25 , 55]
lonbounds = [250 , 300] # degrees east ? 

# latitude lower and upper index
latli = np.argmin( np.abs( lat - latbounds[0] ) )
latui = np.argmin( np.abs( lat - latbounds[1] ) ) 

# longitude lower and upper index
lonli = np.argmin( np.abs( lon - lonbounds[0] ) )
lonui = np.argmin( np.abs( lon - lonbounds[1] ) )  

# Air (time, latitude, longitude) 
USsubset = f.variables['TREFHT'][ : , latli:latui , lonli:lonui ] 
# Test size of array

#=======================================36=============================
# (850-1850)
#====================================================================

dir='/glade/p/cesm/community/cesmLME/CESM-CAM5-LME/atm/proc/tseries/monthly/PRECT/'

#Load input data 

nTEMP100_1=np.zeros((13,12000, 16, 20)) #, dtype=float32) # pre-set size of array (ensemble size, time, lat, lon)

this_index = 2

while this_index <= 13:
	if (this_index) <= 9:
		file_name = dir+"b.e11.BLMTRC5CN.f19_g16.00" + str(this_index) + ".cam.h0.PRECT.085001-184912.nc"
	else:
		file_name = dir+"b.e11.BLMTRC5CN.f19_g16.0" + str(this_index) + ".cam.h0.PRECT.085001-184912.nc"

	f = netCDF4.Dataset(file_name)

	VAR1=f.variables['PRECT'][:,latli:latui , lonli:lonui]
	VAR1=np.squeeze(VAR1)

	nTEMP100_1[this_index-1]=np.float32(VAR1[:,:,:])

	this_index+=1


#====================================================================
# 1850-2005
#====================================================================

dir='/glade/p/cesm/community/cesmLME/CESM-CAM5-LME/atm/proc/tseries/monthly/PRECT/'

#Load input data (850-1850)

nTEMP100_2=np.zeros((13,1872, 16, 20)) #, dtype=float32) # pre-set size of array (ensemble size, time, lat, lon)

this_index = 2

while this_index <= 13:
	if (this_index) <= 9:
		file_name = dir+"b.e11.BLMTRC5CN.f19_g16.00" + str(this_index) + ".cam.h0.PRECT.185001-200512.nc"
	else:
		file_name = dir+"b.e11.BLMTRC5CN.f19_g16.0" + str(this_index) + ".cam.h0.PRECT.185001-200512.nc"

	f = netCDF4.Dataset(file_name)

	VAR2=f.variables['PRECT'][:,latli:latui , lonli:lonui]
	VAR2=np.squeeze(VAR2)

	nTEMP100_2[this_index-1]=np.float32(VAR2[:,:,:])

	this_index+=1

#====================================================================

# Compute Ensemble Means & Save

#====================================================================

#ENS_MEAN_1=np.average(nTEMP100_1[0:33,:,:,:],axis=0)
cd /glade/scratch/sylviad/

ENS_MEAN_1=np.average(nTEMP100_1[1:12,:,:,:],axis=0)

print("Averaged ensemble members 1!")

np.save('PRECT_LME_USA_ENSMEAN_850-1850_V2.npy',ENS_MEAN_1)

ENS_MEAN_2=np.average(nTEMP100_2[1:12,:,:,:],axis=0)

print("Averaged ensemble members 2!")


np.save('PRECT_LME_USA_ENSMEAN_1850-2005_V2.npy',ENS_MEAN_2)


#====================================================================
lat = f.variables['lat'][:]
lon = f.variables['lon'][:]
time = f.variables['time'][:]


uslat = f.variables['lat'][latli:latui]
uslon = f.variables['lon'][lonli:lonui]


# RSYNC FROM SERVER
np.save('NA_ATM_LME_lats.npy',np.array(uslat))
np.save('NA_ATM_LME_lons.npy',np.array(uslon))
#====================================================================

rsync -va --ignore-existing sylviad@cheyenne.ucar.edu:/glade/scratch/sylviad/ /rdf/sd75/sylvia/CESM/RIVERS/

