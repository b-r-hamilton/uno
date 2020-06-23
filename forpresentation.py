# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:32:17 2020

@author: bydd1
"""

import pickle 
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs 
import pandas as pd
import numpy as np
import datetime as dt
#%%

path = r'D:\CDS River Discharge\Pickles\compressed_ra_recint.pickle'
dic = pickle.load(open(path, "rb" ) )
mean = dic['mean_annual']
lat = dic['lat']
lon = dic['lon']

lat_bounds = [41, 27]
lon_bounds = [-96, -81]

#find the closest value to some specified value in an array 
def find_closest_val(val, arr):
    diff = [abs(x - val) for x in arr]
    index = diff.index(min(diff))
    return index     

new_lat = [find_closest_val(x, lat) for x in lat_bounds]
new_lon = [find_closest_val(x, lon) for x in lon_bounds]
    
plt.figure(figsize = (10, 10))
ax = plt.subplot(projection = ccrs.PlateCarree())
ax.coastlines()
mesh = plt.pcolormesh(lon[new_lon[0]:new_lon[1]], lat[new_lat[0]:new_lat[1]], 
               mean[new_lat[0]:new_lat[1], new_lon[0]:new_lon[1]], cmap = 'coolwarm')
plt.colorbar(mesh)
gl = ax.gridlines(draw_labels = True)
gl.xlabels_top = False
gl.ylabels_right = False



#%%


path = r'C:\Users\bydd1\OneDrive\Documents\Research\CESM Formatted_new\timeseries.csv'
x = pd.read_csv(path)
time = x['time']
temp =x['temp']
window_size = 100

mu = np.mean(temp)
z = [val - mu for val in temp]
z = pd.Series(z)
windows = z.rolling(window_size)
moving_averages = windows.mean()

fig = plt.figure(figsize = (14, 5))
plt.plot(time, moving_averages, linewidth = 8)
y1 = np.nanmin(moving_averages)
y2 = np.nanmax(moving_averages)
plt.fill_between(x = [1000, 1200], y1 = y1, y2 = y2, color ='lightslategray', alpha = 0.3)
plt.fill_between(x = [1600, 1800], y1 = y1, y2 = y2, color ='lightslategray', alpha = 0.3)
plt.ylabel('Temperature Anomaly (deg C)')
plt.xlabel('Year AD')
#plt.text(x = 1075, y = -0.10, s = 'MCA', fontsize = 15)
#plt.text(x = 1675, y = 0.10, s = 'LIA', fontsize = 15)

plt.savefig(r'C:\Users\bydd1\Downloads\tempfig.png', transparent = True)
#%%
path = r'D:\Data\river data\VicksburgHistoricStage.xlsx'
x = pd.read_excel(path, skiprows = 11, skipfooter = 1)
x = x.rename(columns={"Date / Time": "date", "Stage (Ft)":"stage"})
new = []
for val in x['stage']:
    if val == 'M':
        val = np.nan
    val = float(val)
    new.append(val)
x['stage'] = new
x['stage'] = pd.to_numeric(x['stage'])
x = x.resample(rule = 'A', on = 'date').mean()

#%%
date = x.index.tolist()
date = pd.to_datetime(date)
stage = x['stage'].tolist()

#%%

fig = plt.figure(figsize = (15, 4))
fig.patch.set_facecolor('slategray')
ax = plt.subplot()
ax.set_facecolor('lightslategray')
ax.grid()

plt.plot(date[:-1], stage[:-1], linewidth = 5, alpha = 0.8)
flood_dates = [dt.datetime(1927, 5, 1), dt.datetime(1979, 4, 12), 
               dt.datetime(1974, 4, 14), dt.datetime(1961, 2, 20), dt.datetime(1982, 3, 1), 
               dt.datetime(2011, 5, 1)]
damage = ['$5 billion', '$1.7 billion', '$45 million', '$50 million', '$1.2 billion', '$3 billion']
plt.vlines(x = flood_dates, ymin = 0, ymax = 45, color = 'darkorange')
plt.xlabel('year', fontsize = 15)
plt.ylabel('stage (ft)', fontsize = 15)
plt.legend(['stage', 'economic loss'], loc = 'lower left')

for i in range(len(damage)):
    y = 30
    x = flood_dates[i] + dt.timedelta(days = -60)
    s = damage[i]
    plt.text(x, y, s, rotation = 270, fontsize = 12, color = 'white')
    
plt.suptitle('Stage Data from Vicksburg, MS')
plt.title('Data provided by weather.gov and USGS')

plt.savefig(r'C:\Users\bydd1\Downloads\new_figure.pdf')
#%%
average = 
for i in range(0, 13):
    print(i)
