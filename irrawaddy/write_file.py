# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:30:50 2020
Script to write "long" version of irrawaddy file
@author: bydd1
"""
import pandas as pd 
import os 
import numpy as np 

dire = r'C:\Users\bydd1\Downloads'
file = r'irrawaddy stage sediment2.xlsx'

start = 1966
end = 2018 
total = end - start + 1 #number of iterations

year = []
month = []
day = []
stage = []
discharge = []

for y in range(total):
    
    head = 4 + y*37
    # if y + 1966 == 1997:
    #     head + 1
        
    x_stage = pd.read_excel(os.path.join(dire, file), sheet_name = 0,
                      header = head, index_col = 0, 
                      nrows = 31)
        
    x_disc = pd.read_excel(os.path.join(dire, file), sheet_name = 1,
                      header = head, index_col = 0, 
                      nrows = 31)
    
    x_stage = x_stage.rename(columns=lambda x: x.strip())
    x_disc = x_disc.rename(columns=lambda x: x.strip())
    
    for i in x_stage.columns:
        
        m = x_stage.columns.tolist().index(i)
        
        for j in x_stage.index:
            
            dis = x_disc[i][j]
            sta = x_stage[i][j]

            if type(dis) == str or type(sta) == str:
                if type(dis) == str: 
                    print('sed at ' + str(y + 1966) + ',' +str(m) + ',' + str(d))
                if type(sta) == str:
                    print('sta at ' + str(y + 1966) + ',' +str(m) + ',' + str(d))
            if sta < 0: 
                print('negative sta'+ str(y + 1966) + ',' +str(m) + ',' + str(d))
            if dis < 0 :
                print('negative dis' + str(y + 1966) + ',' +str(m) + ',' + str(d))
            if sta > 5000:
                print('large sta at' + str(y + 1966) + ',' +str(m) + ',' + str(d))
            if sta < 1000:
                print('small sta at ' + str(y + 1966) + ',' +str(m) + ',' + str(d))
            
            if not np.isnan(dis):
                if sta == 'nan':
                    sta = np.nan
                d = j 
                year.append(y + 1966)
                month.append(m)
                day.append(d)
                discharge.append(dis)
                stage.append(sta)
                

#%%
dec = []


for y in np.unique(year):
    fraction = 1 / year.count(y)
    dec = dec + np.arange(y,y + 1,fraction).tolist()
        
            
    
#%%
df = pd.DataFrame({'year' : year,
                   'month' : [m + 1 for m in month],
                   'day' : day,
                   'decimal' : dec, 
                   'sed_dis [kg/sec]' : discharge, 
                   'stage [cm]' : stage
                   })

#%%
save_path = os.path.join(dire, 'irrawaddy_formatted.xlsx')
df.to_excel(save_path)
        
        