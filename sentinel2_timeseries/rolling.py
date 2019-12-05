

import pandas as pd
import numpy as np
from scipy import *
from scipy.signal import *
import matplotlib.pyplot as plt
from load_data import *


######### Change paths according to locations in your machine ##########
file_location = '/home/leomarg/ndvi_big_areas.csv'
national_park_file='/home/leomarg/national_park.csv'
dest_folder='/home/leomarg/tmp/'
########################################################################


cat = 3

ts = read_ndvi(file_location)
n_p = read_nat_park(national_park_file)
log = read_logging(file_location)

series = ts[cat]

np_upsampled = n_p[1].resample('D')
np_interp = np_upsampled.interpolate(method = 'linear')

ts_upsampled = series.resample('D')
ts_interp = ts_upsampled.interpolate(method = 'linear')


series_r = ts_interp.rolling(30).median()
np_r = np_interp.rolling(30).median()

#series_r = ts_interp.rolling(10).median()
#np_r = np_interp.rolling(10).median()

plt.figure;
#plt.plot(series_r, 'm');
plt.plot(ts_interp, 'r');
#lt.plot(np_r, 'g');
plt.plot(np_interp, 'b');
plt.xticks(rotation=45);
#plt.title("Smoothing of NP time series by rolling median")
plt.grid()
plt.show()
