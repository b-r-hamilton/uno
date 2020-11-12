# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 13:18:32 2020

@author: bydd1
"""

import os
import geopandas as gpd
from osgeo import gdal 
import numpy as np 

os.chdir(r'D:\DEM\NHDPLUS\HRNHDPlusRasters1203')

file = gdal.Open('hydrodem.tif')
channel = np.array(file.GetRasterBand(1).ReadAsArray())