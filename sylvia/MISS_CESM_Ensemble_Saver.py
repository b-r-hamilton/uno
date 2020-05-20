# Calculate Ensemble Mean SST anomalies for ALL of TREFT

# Sylvia Dee
# this script identifies years in which a volcanic eruption occurred 
# and plots SSS, SST anomalies across each eruption.

# Import modules
import cdms2, cdutil
import numpy as np
import numpy.ma as ma
from os import listdir, chdir
from os.path import isfile, join
import string
import sys


from pydap.client import open_url  
from pylab import *

import sys, os, cdtime, cdutil, cdms2, vcs, MV2, time, datetime
import numpy as np
import matplotlib.pyplot as plt
from math import exp

from regrid2 import Regridder
from vcsaddons import EzTemplate
#======================================================================

# Get CESM New Runs:

dir = '/home/geovault-02/sdee/CCSM_Mississippi/ENSEMBLE/SOIL/'

# Control

# name1=dir + 'b.e11.B1850C5CN.f19_g16.0850cntl.001.cam.h0.TREFHT.085001-184912.nc'
# name2=dir + 'b.e11.B1850C5CN.f19_g16.0850cntl.001.cam.h0.TREFHT.185001-200512.nc'

# Ensemble Members (001-010)

name1=dir + 'b.e11.BLMTRC5CN.f19_g16.010.clm2.h0.SOILLIQ.085001-184912.nc'
name2=dir + 'b.e11.BLMTRC5CN.f19_g16.010.clm2.h0.SOILLIQ.185001-200512.nc'

#======================================================================

# Open data file
f1 = cdms2.open(name1)
cdms2.axis.latitude_aliases.append("Y") 
cdms2.axis.longitude_aliases.append("X")
cdms2.axis.time_aliases.append("T")

f2 = cdms2.open(name2)
cdms2.axis.latitude_aliases.append("Y") 
cdms2.axis.longitude_aliases.append("X")
cdms2.axis.time_aliases.append("T")
# get the start and end time steps 
start_time_tos = f1.getAxis('time').asRelativeTime()[0]
end_time_tos = f1.getAxis('time').asRelativeTime()[-1]

start_time2_tos = f2.getAxis('time').asRelativeTime()[0]
end_time2_tos = f2.getAxis('time').asRelativeTime()[-1]

# extract Indo-Pacific region data
IPtosVar1 = f1('SOILLIQ', latitude=(20.,50.),longitude=(230.,300.))
IPtosVar2 = f2('SOILLIQ', latitude=(20.,50.),longitude=(230.,300.))


lons, lats = IPtosVar2.getLongitude().getValue(), IPtosVar2.getLatitude().getValue()

cdutil.setTimeBoundsMonthly(IPtosVar1,stored=0)#,time= (start_time_tos, end_time_tos, 'co'))
cdutil.setTimeBoundsMonthly(IPtosVar2,stored=0)#,time= (start_time2_tos, end_time2_tos, 'co'))
# the annualcycle 
# tosMean1=cdutil.YEAR(IPtosVar1(time= (start_time_tos, end_time_tos, 'co')))
# tosMean2=cdutil.YEAR(IPtosVar2(time= (start_time2_tos, end_time2_tos, 'co')))


tos_total=MV2.concatenate((IPtosVar1,IPtosVar2))
SST_full=np.array(tos_total)
SST_full.shape
#======================================================================

cd /home/geovault-02/sdee/CCSM_Mississippi/ENSEMBLE/SOIL/
np.save('SOIL_lats.npy',lats)
np.save('SOIL_lons.npy',lons)
np.save('CESM_SOILLIQ_USA_absolute_85001-200512_EXP010_monthly.npy',SST_full)

#======================================================================
# #======================================================================

# import numpy as np
# import numpy.ma as ma

# from pydap.client import open_url  
# from pylab import *
# # Save the anomalies for ENSEMBLE MEAN!
# #======================================================================
# # 0. Load all data sets

# cd /home/geovault-02/sdee/PALMYRA/

# SST01=np.load('CESM_TREFT_absolute_85001-200512_EXP001.npy')
# SST02=np.load('CESM_TREFT_absolute_85001-200512_EXP002.npy')
# SST03=np.load('CESM_TREFT_absolute_85001-200512_EXP003.npy')
# SST04=np.load('CESM_TREFT_absolute_85001-200512_EXP004.npy')
# SST05=np.load('CESM_TREFT_absolute_85001-200512_EXP005.npy')
# SST06=np.load('CESM_TREFT_absolute_85001-200512_EXP006.npy')
# SST07=np.load('CESM_TREFT_absolute_85001-200512_EXP007.npy')
# SST08=np.load('CESM_TREFT_absolute_85001-200512_EXP008.npy')
# SST09=np.load('CESM_TREFT_absolute_85001-200512_EXP009.npy')
# SST10=np.load('CESM_TREFT_absolute_85001-200512_EXP010.npy')
# #======================================================================
# # 1. Compute anomalies....

# SSTA1=np.ma.anomalies(SST01, axis=0) 
# SSTA2=np.ma.anomalies(SST02, axis=0)
# SSTA3=np.ma.anomalies(SST03, axis=0)
# SSTA4=np.ma.anomalies(SST04, axis=0)
# SSTA5=np.ma.anomalies(SST05, axis=0)
# SSTA6=np.ma.anomalies(SST06, axis=0)
# SSTA7=np.ma.anomalies(SST07, axis=0)
# SSTA8=np.ma.anomalies(SST08, axis=0)
# SSTA9=np.ma.anomalies(SST09, axis=0)
# SSTA10=np.ma.anomalies(SST10, axis=0)

# #======================================================================
# # 2. Average all ensemble members.

# all_ens=([SSTA1,SSTA2,SSTA3,SSTA4,SSTA5,SSTA6,SSTA7,SSTA8,SSTA9,SSTA10])
# average_ens=np.mean( np.array(all_ens), axis=0 )
# np.save('CESM_TREFT_ensemble_member_mean_anomalies_85001-200512.npy',average_ens)
# #======================================================================


