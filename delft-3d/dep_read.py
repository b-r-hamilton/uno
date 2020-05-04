# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:17:48 2020

@author: bydd1
"""

path = r'D:\Delft3D\oxbow5\depth_fill_1.dep'

import numpy as np 

dep = np.genfromtxt(path)
#dep = np.asarray(dep)

dep[dep == -999] = np.nan
dep = - dep
#plt.pcolormesh(dep)
dep[np.isnan(dep)] = -999

new_path = r'D:\Delft3D\oxbow5\depth_neg.dep'

np.savetxt(new_path, dep, delimiter = '  ')

