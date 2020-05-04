# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 18:16:53 2020

@author: bydd1
"""

import matplotlib.pyplot as plt 
import matplotlib as mpl 
# mpl.rcParams['font.weight'] = 'bold'
# plt.rcParams["axes.labelweight"] = 'bold'
# mpl.rcParams['font.stretch'] = 'condensed'
# mpl.rcParams.update({'font.weight' : 'normal'})
# mpl.rcParams['font.family'] = 'serif'

mpl.rcParams.update(mpl.rcParamsDefault)
x = [1,2,5,6,8]
y = [18, 23, 13,61, 12]
plt.plot(x,y)
plt.title('eat shit')
plt.text(x = 3, y = 40, s = 'get fucked')
print(mpl.rcParams['font.weight'])
print(mpl.rcParams['axes.labelweight'])
print(mpl.rcParams['font.family'])