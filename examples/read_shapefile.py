# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:59:57 2020

@author: bydd1
"""
import geopandas
import matplotlib.pyplot as plt 
import cartopy 
import cartopy.crs as ccrs 

plt.figure()
ax = plt.subplot(projection = ccrs.PlateCarree())
ax.coastlines()
path = r'D:\Shapefiles\Mississippi\mississippi.shp'
shp = geopandas.read_file(path)

shp.plot(linewidth = 0.1, alpha = 0.8, ax = ax)


import pyproj

plt.figure()
plt.subplot(projection = ccrs.PlateCarree())
ax.coastlines()
path2 = r'D:\Shapefiles\Miss_RiverBasin\Miss_RiverBasin.shp'
shp2 = geopandas.read_file(path2)
shp2 =shp2.to_crs("EPSG:4326")
shp2.plot(ax = ax)