# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 19:26:03 2020

@author: bydd1
"""

import os
import delft3d
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import datetime as dt 

#%%
# supply the path of compiled Delft3D source code to create simulation runner
sim = delft3d.Simulation('C:/Program Files/Deltares/Delft3D 4.04.01/x64')

os.chdir(r'D:\Delft3D\straight')
bct = delft3d.TimeSeriesFile('bound_cond.bct')

ts0 = bct.data[0].time_series
ts1 = bct.data[1].time_series

#%%
timesteps = 200
mu = 0
sigma = np.sqrt(5)
xv = np.linspace(-3*sigma**2, 3*sigma**2, timesteps)
f = [(2 * np.pi) * np.exp((-1/2)*((x - mu) / sigma)**2) for x in xv]
target = 2


factor = target / max(f)
f = np.multiply(f, factor)

val = 1
f = np.add(f, val)

front = np.ones(25) * val 
back = np.ones(50) * val

f = np.concatenate((front, f, back), axis = 0)

f = -f


start = pd.Timestamp('2020-09-01')
end = pd.Timestamp('2020-09-30')
t = np.linspace(start.value, end.value, len(f))
t = pd.to_datetime(t)
t = t.round("min")

df = pd.DataFrame(data = {'current':f}, index = t)
df1 = pd.DataFrame(data = {'current':[-val,-val]}, index = [start, end])
bct.set_time_series(0, start, df, df)
bct.set_time_series(1, start, df1, df1)
bct.to_file('bound_cond.bct')

plt.plot(t,f)
plt.xticks(rotation = 270)