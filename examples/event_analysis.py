#Usage: determine behavior of environmental gridded datasets x months before specified events
#Inputs: list of python datetime objects, dictionary with environmental gridded data (of same format)
#Outputs: trend images

from netCDF4 import Dataset
from pydap.client import open_url
import datetime as dt
import time as pytime 
import numpy as np
import matplotlib.pyplot as plt

url = 'http://psl.noaa.gov/thredds/dodsC/Datasets/20thC_ReanV3/Monthlies/'

# surface air mean temp, surface air max temp, surface air min temp,
var = ['2mMO/air.2m.mon.mean.nc', '2mMO/tmax.2m.mon.mean.nc', '2mMO/tmin.2m.mon.mean.nc', 'miscMO/cldwtr.eatm.mon.mean.nc']

#find the closest value to some specified value in an array 
def find_closest_val(val, arr):
    if isinstance(val, dt.datetime):
        diff = [(abs(x - val)).total_seconds() for x in arr]
    else: 
        diff = [abs(x - val) for x in arr]
    index = diff.index(min(diff))
    return index    

dic = {}
init = False
start_time = pytime.time()
bbox = {'lat' : [16, 54],
        'lon' : [-136, -62]}

flag = False
for i in range(len(bbox['lon'])):
    val = bbox['lon'][i]
    if val < 0:
        bbox['lon'][i] = 180 + val
        
if bbox['lon'][0] > bbox['lon'][1]: [bbox['lon'][1], bbox['lon'][0]]

print( bbox)

#%%

for v in var:
    print(v)
    print(str(pytime.time() - start_time) + ' seconds elapsed')
    url = url + v
    x = open_url(url)
    not_var = ['lat', 'lon', 'time', 'time_bnds']

    if not init:
        init = True

        for n in not_var:
            if n not in ['time_bnds', 'time']:
                dic[n] = x[n][:].data

            if n == 'time':
                conv_time = []
                origin = dt.datetime(1800, 1, 1)
                time = x['time'][:].data
                for t in time:
                    t_0 = origin + dt.timedelta(hours = t)
                    conv_time.append(t_0)
                dic['time'] = conv_time
                
        bbox_ind = {}
        for pair in bbox:
            bbox_ind[pair] = [find_closest_val(x, dic[pair]) for x in bbox[pair]]
        
        for name in ['lat', 'lon']:
            dic[name] = dic[name][bbox_ind[name][0]:bbox_ind[name][1]]
        
    keys = list(x.keys())
    name = [k for k in keys if k not in not_var][0]
    length = x[name].shape[0] #temporal length
    start = 0
    stop = 10
    
    
    
    new_data = np.asarray(x[name][start:stop, bbox_ind['lat'][0]:bbox_ind['lat'][1], bbox_ind['lon'][0]:bbox_ind['lon'][1]].data)[0]
    data = new_data
    
    print(str(pytime.time() - start_time) + ' seconds elapsed')

    while stop < length:
        print('data at ' +str(start) +' to ' +str(stop) +' out of ' +str(len(dic['time'])) + ' gathered, ' + str(pytime.time() - start_time) + ' seconds elapsed')
        start = stop
        stop = stop + 10
        new_data = np.asarray(x[name][start:stop, bbox_ind['lat'][0]:bbox_ind['lat'][1], bbox_ind['lon'][0]:bbox_ind['lon'][1]].data)[0]
        data = np.concatenate((data, new_data), axis = 0)

    if stop != length - 1:
        new_data = np.asarray(x[name][start:stop, bbox_ind['lat'][0]:bbox_ind['lat'][1], bbox_ind['lon'][0]:bbox_ind['lon'][1]].data)[0]
        data = np.concatenate((data, new_data), axis = 0)

#%%
plt.figure()
ax = plt.subplot(projection = ccrs.PlateCarree())
plt.pcolormesh(dic['lon'], dic['lat'], data[0, :, :])
ax.coastlines()
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')