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

dir = '/home/geovault-02/sdee/CCSM_Mississippi/ENSEMBLE/PREC/'

# Control

# name1=dir + 'b.e11.B1850C5CN.f19_g16.0850cntl.001.cam.h0.TREFHT.085001-184912.nc'
# name2=dir + 'b.e11.B1850C5CN.f19_g16.0850cntl.001.cam.h0.TREFHT.185001-200512.nc'

# Ensemble Members (001-010)

name1=dir + 'b.e11.BLMTRC5CN.f19_g16.001.cam.h0.PRECL.085001-184912.nc'
name2=dir + 'b.e11.BLMTRC5CN.f19_g16.001.cam.h0.PRECL.185001-200512.nc'

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
IPtosVar1 = f1('PRECL', latitude=(-90.,90.),longitude=(0.,360.))
IPtosVar2 = f2('PRECL', latitude=(-90.,90.),longitude=(0.,360.))

lons, lats = IPtosVar1.getLongitude().getValue(), IPtosVar1.getLatitude().getValue()

cdutil.setTimeBoundsMonthly(IPtosVar1,stored=0)#,time= (start_time_tos, end_time_tos, 'co'))
cdutil.setTimeBoundsMonthly(IPtosVar2,stored=0)#,time= (start_time2_tos, end_time2_tos, 'co'))

# the annualcycle 
# tosMean1=cdutil.YEAR(IPtosVar1(time= (start_time_tos, end_time_tos, 'co')))
# tosMean2=cdutil.YEAR(IPtosVar2(time= (start_time2_tos, end_time2_tos, 'co')))


tos_total=MV2.concatenate((IPtosVar1,IPtosVar2))
SST_full=np.array(tos_total)
SST_full.shape
#======================================================================

cd /home/geovault-02/sdee/CCSM_Mississippi/ENSEMBLE/PREC/
np.save('CESM_PRECL_absolute_85001-200512_EXP001_monthly.npy',SST_full)

#======================================================================



