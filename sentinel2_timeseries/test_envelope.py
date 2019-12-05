# coding: utf-8

from __future__ import print_function
import pandas as pd
import numpy as np
from scipy import *
from scipy.signal import *
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from load_data import *


######### Change paths according to locations in your machine ##########
file_location = '/home/leomarg/ndvi_big_areas_v4.csv'
national_park_file='/home/leomarg/national_park_v4_1.csv'
dest_folder='/home/leomarg/tmp/'
########################################################################


cat = 4

ts = read_ndvi(file_location)
n_p = read_nat_park(national_park_file)
log = read_logging(file_location)

series = ts[cat]
ts_upsampled = series.resample('7D')
ts_interp = ts_upsampled.interpolate(method = 'linear')

# noisy vector of values

s=ts_interp

q_u = zeros(s.shape)
q_l = zeros(s.shape)

#Prepend the first value of (s) to the interpolating values. 
#This forces the model to use the same starting point for both the upper 
#and lower envelope models

u_x = [0,]
u_y = [s[0],]

l_x = [0,]
l_y = [s[0],]

#Detect peaks and troughs and mark their location in u_x,u_y,l_x,l_y respectively

for k in xrange(1,len(s)-1):
    if (sign(s[k]-s[k-1])==1) and (sign(s[k]-s[k+1])==1):
        u_x.append(k)
        u_y.append(s[k])
    if (sign(s[k]-s[k-1])==-1) and ((sign(s[k]-s[k+1]))==-1):
        l_x.append(k)
        l_y.append(s[k])

#Append the last value of (s) to the interpolating values. 
#This forces the model to use the same ending point for both the upper 
#and lower envelope models.

u_x.append(len(s)-1)
u_y.append(s[-1])

l_x.append(len(s)-1)
l_y.append(s[-1])

#Fit suitable models to the data. 

u_p = interp1d(u_x,u_y, kind = 'linear',bounds_error = False, fill_value=0.0)
l_p = interp1d(l_x,l_y,kind = 'linear',bounds_error = False, fill_value=0.0)

#Evaluate each model over the domain of (s)

for k in xrange(0,len(s)):
    q_u[k] = u_p(k)
    q_l[k] = l_p(k)
    
q_u_series = pd.Series(q_u, index=s.index)
q_l_series = pd.Series(q_l, index=s.index)

#Plot 
plt.figure
plt.plot(s)
plt.plot(q_u_series,'r')
plt.plot(q_l_series,'g')
plt.grid(True)
plt.xticks(rotation=45)
plt.show()
