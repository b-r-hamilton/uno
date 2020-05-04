# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:33:48 2020

@author: bydd1
"""
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import os 
import copy
import datetime as dt


#%%
dire = r'C:\Users\bydd1\Downloads'
save_path = os.path.join(dire, 'irrawaddy_formatted.xlsx')

df = pd.read_excel(save_path, index_col = 0)
df['dates'] = pd.to_datetime(df.drop(columns=['decimal', 'sed_dis [kg/sec]', 'stage [cm]']))
df = df.dropna()
df = df.reset_index()

df_mon_resample = df.resample('M', on = 'dates').mean()
df_ann_resample = df.resample('A', on = 'dates').mean()
#%%

sta_mean = df.groupby(df.dates.dt.month)['stage [cm]'].transform('mean')
sta_std = df.groupby(df.dates.dt.month)['stage [cm]'].transform('std')
dis_mean = df.groupby(df.dates.dt.month)['sed_dis [kg/sec]'].transform('mean')
dis_std = df.groupby(df.dates.dt.month)['sed_dis [kg/sec]'].transform('std')

df['dis_sca'] = (df['stage [cm]'] - sta_mean) / sta_std
df['sta_sca'] = (df['sed_dis [kg/sec]'] - dis_mean) / dis_std
#%%

def plot_year(dataframe, year, vals, title):
    plt.figure(1)
    df_sub = dataframe[dataframe.year == year]
    plt.figure()
    num_subplots = len(vals)
    
    for i in range(len(vals)):
        plt.subplot(num_subplots, 1, i + 1)
        plt.plot(df_sub['dates'], df_sub[vals[i]])
    
    plt.suptitle(title)

year = 2008
plot_year(df, year, ['sed_dis [kg/sec]', 'stage [cm]'], str(year))

#%%

plt.figure(3)
plt.plot(df['dates'], df['dis_sca'])
plt.plot(df['dates'], df['sta_sca'])
plt.title('Z-scores')
plt.legend(['discharge', 'stage'])
#%%

plt.figure(4)
df_sub1 = df[df['year'] == 2015]
plt.subplot(2,1,1)
plt.plot(df_sub1['dates'], df_sub1['dis_sca'])
plt.plot(df_sub1.dates, df_sub1.sta_sca)
plt.xlabel('time')
plt.subplot(2,1,2)
plt.legend(['sed discharge', 'stage'])
plt.ylabel('z-score')

df_sub2 = df[df['year'] == 1987]
plt.subplot(2,1,2)
plt.plot(df_sub2['dates'], df_sub2['dis_sca'])
plt.plot(df_sub2.dates, df_sub2.sta_sca)
plt.xlabel('time')
plt.subplot(2,1,2)
plt.legend(['sed discharge', 'stage'])
plt.ylabel('z-score')

#%%
august_df = df[df['month'] == 8]
august_df = august_df.resample('A', on = 'dates').min()
plt.figure(5)
plt.plot(august_df['year'], august_df.sta_sca, '.-')
plt.vlines([1974, 1997, 2004, 2015, 2016], ymin = -2, ymax = 0.5, color = 'green')
plt.vlines([1972, 1979, 1982, 1983, 1986, 1987], ymin = -2, ymax =0.5, color = 'red')
plt.xlabel('year')
plt.ylabel('Z-score of stage')
plt.title('annual min August discharge, standardized')