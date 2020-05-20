# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:27:31 2020

@author: bydd1
"""


from netCDF4 import Dataset 
import numpy as np 
import os
import matplotlib.pyplot as plt 
import time as pytime #this isnt necessary, I just like to time my programs

import cartopy 
import cartopy.crs as ccrs 




#find the closest value to some specified value in an array 
def find_closest_val(val, arr):
    diff = [abs(x - val) for x in arr]
    index = diff.index(min(diff))
    return index     


start_time = pytime.time()

folder = r'D:\PHYDA' #folder holding just PHYDA files
files = os.listdir(folder) #list all files in folder 
path1 = os.path.join(folder, files[0]) #create a path for the first file 
x = Dataset(path1) #open the netcdf file 

print('---METADATA---')
print(x) #print metadata

#if you want to learn more about any of the dimensions or variables,
#you can type into the console['var_name_in_apostrophes'] and it will print details
#or you can just do this: 
print('')
print('')
print('here is information about pdsi')
print(x['pdsi_mn'])


#get parameters! 
lat = x['lat'][:].data
lon = x['lon'][:].data
time = x['time'][:].data

#get data!
pdsi_mn = x['pdsi_mn'][:].data

subset = pdsi_mn[1000:1200, :, :] #subset your data temporally

#find latitude indices 
lat_given = [-20, 80]
index1_lat = find_closest_val(lat_given[0], lat)
index2_lat = find_closest_val(lat_given[1], lat)

#find longitude indices
lon_given = [200, 250]
index1_lon = find_closest_val(lon_given[0], lon)
index2_lon = find_closest_val(lon_given[1], lon)

#subset and temporally average your data
subset2 = subset[:, index1_lat:index2_lat, index1_lon:index2_lon]
mean = np.mean(subset2, axis = 0)

#plot your data! 
fig = plt.figure(figsize = (10, 2))
ax = plt.subplot(projection = ccrs.PlateCarree())
ax.coastlines()
mesh = plt.contourf(lon[index1_lon:index2_lon], lat[index1_lat:index2_lat], 
                      mean, cmap = 'coolwarm')
plt.xlabel('lon')
plt.ylabel('lat')
plt.title('PDSI averaged between 1000-1200AD')
plt.colorbar(mesh)

#plt.savefig(r'C:\Users\bydd1\Downloads\test.pdf')
print('completion time = ' + str(pytime.time() - start_time) + ' seconds')
