# -*- coding: utf-8 -*-

import pickle
import time as pytime
import numpy as np
import os 
from netCDF4 import Dataset
import matplotlib.pyplot as plt 
import datetime as dt 
import pandas as pd 

folder = r'D:\CDS River Discharge\Data'
files = os.listdir(folder)
x = Dataset(os.path.join(folder, files[0]))

lat = x['lat'][:].data
lon = x['lon'][:].data

point = [42.046361, -71.910833]
def find_closest_val(val, arr):
    diff = [abs(x - val) for x in arr]
    index = diff.index(min(diff))
    return index    

def convert_datetime(val):
    origin = dt.datetime(1979, 1, 1)
    date = origin + dt.timedelta(hours = val)
    return date

ind = [find_closest_val(point[0], lat), find_closest_val(point[1], lon)]
plt.figure()
plt.pcolormesh(lon, lat, x['dis24'][0, :, :].data, cmap = 'coolwarm')
plt.plot(point[1], point[0], '.', markersize = 14)

time = []
values = []
for f in files:
    x = Dataset(os.path.join(folder, f))
    time.append(convert_datetime(x['time'][:].data[0]))
    val = x['dis24'][0, ind[0], ind[1]].data

    values.append(val)
    

    
values = np.squeeze(values)
data = pd.DataFrame({'time' : time, 
                    'discharge' : values})

#%%
data2 = data.resample('M', on='time').mean()
data2.to_excel(r'C:\Users\bydd1\Downloads\cds_copernicus_gfas_singlepoint.xlsx')