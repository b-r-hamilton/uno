import numpy as np
import string
import sys, os #, cdtime, cdutil, cdms2, MV2, time, datetime
from netCDF4 import Dataset 
#====================================================================

#====================================================================

directories = [r'D:\SNOMELT', r'D:/QRUNOFF']
var_names = ['QSNOMELT', 'QRUNOFF']

for i in range(len(directories)): 
    d = directories[i]
    v = var_names[i]
    
    file_name = 'b.e11.BLMTRC5CN.f19_g16.001.clm2.h0.' + v + '.085001-184912.nc'
    f = Dataset(os.path.join(d, file_name))
    VAR1=f.variables[v]
    
    lat = f.variables['lat'][:]
    lon = f.variables['lon'][:]
    time = f.variables['time'][:]
    #====================================================================
    
    # Save only U.S. 
    latbounds = [25 , 55]
    lonbounds = [250 , 300] # degrees east ? 
    
    # latitude lower and upper index
    latli = np.argmin( np.abs( lat - latbounds[0] ) )
    latui = np.argmin( np.abs( lat - latbounds[1] ) ) 
    
    # longitude lower and upper index
    lonli = np.argmin( np.abs( lon - lonbounds[0] ) )
    lonui = np.argmin( np.abs( lon - lonbounds[1] ) )  
    
    # Air (time, latitude, longitude) 
    USsubset = f.variables[v][ : , latli:latui , lonli:lonui ] 
        
    # Test size of array
    
    #=======================================36=============================
    # (850-1850)
    #====================================================================
    
    
    #Load input data 
    
    nTEMP100_1=np.zeros((13,12000, 16, 20)) #, dtype=float32) # pre-set size of array (ensemble size, time, lat, lon)
    
    this_index = 2
    
    while this_index <= 13:
        
        	if (this_index) <= 9:
        		file_name = os.path.join(d,"b.e11.BLMTRC5CN.f19_g16.00" + str(this_index) + ".clm2.h0." +v +".085001-184912.nc")
        	else:
        		file_name =os.path.join(d, "b.e11.BLMTRC5CN.f19_g16.0" + str(this_index) + ".clm2.h0." + v +".085001-184912.nc")
        
        	f = Dataset(file_name)
        
        	VAR1=f.variables[v][:,latli:latui , lonli:lonui]
        	VAR1=np.squeeze(VAR1)
        
        	nTEMP100_1[this_index-1]=np.float32(VAR1[:,:,:])
        
        	this_index+=1
    
    
    #====================================================================
    
    # Compute Ensemble Means & Save
    
    #====================================================================
    
    
    ENS_MEAN_1=np.average(nTEMP100_1[1:12,:,:,:],axis=0)
    
    print("Averaged ensemble members 1!")
    
    np.save(v + '_LME_USA_ENSMEAN_850-1850.npy',ENS_MEAN_1)    
    
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

