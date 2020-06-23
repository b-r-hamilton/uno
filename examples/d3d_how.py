# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 13:06:07 2020

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

os.chdir(r'D:\Delft3D\op')

bct = delft3d.TimeSeriesFile('bound_cond.bct')
data = bct.data

ts0 = bct.data[0].time_series
ts1 = bct.data[1].time_series


fsa = pd.read_csv(r'C:\Users\bydd1\OneDrive\Documents\Research\Code for Babes\Delft3D-Toolbox\doc\example\flow_series_A.csv', index_col=0)
fsa.index = pd.to_datetime(fsa.index)


#%%
timesteps = 300
mu = 0
sigma = np.sqrt(5)
xv = np.linspace(-3*sigma**2, 3*sigma**2, timesteps)
f = [(2 * np.pi) * np.exp((-1/2)*((x - mu) / sigma)**2) for x in xv]
target = 0.3
factor = target / max(f)
f = np.multiply(f, factor)
f = np.add(f, 1)

front = np.ones(200)
back = np.ones(50)

f = np.concatenate((front, f, back), axis = 0)



#%%

start = pd.Timestamp('2020-05-15')
end = pd.Timestamp('2020-05-31')
t = np.linspace(start.value, end.value, len(f))
t = pd.to_datetime(t)
t = t.round("min")

df = pd.DataFrame(data = {'current':f}, index = t)

bct.set_time_series(0, '2020-05-15', df, df)
bct.to_file('bound_cond.bct')

import matplotlib.pyplot as plt
plt.figure()
plt.plot(t,f)
#%%
# run single simulation
path = 'trial1.mdf'
#sim.run('trial1.mdf') 