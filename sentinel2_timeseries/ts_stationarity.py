import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from load_data import *
from stationarity_test import *


######### Change paths according to locations in your machine ##########
file_location = '/home/leomarg/ndvi_big_areas_v4.csv'
national_park_file='/home/leomarg/national_park_v4_1.csv'
########################################################################


cat = 3

ts = read_ndvi(file_location)
n_p = read_nat_park(national_park_file)

series = ts[cat]

np_upsampled = n_p[1].resample('D')
np_interp = np_upsampled.interpolate(method = 'linear')

ts_upsampled = series.resample('D')
ts_interp = ts_upsampled.interpolate(method = 'linear')

test_stationarity(ts_interp)

diff = ts_interp - np_interp

plt.figure
plt.hist(diff)
plt.title("Stats of difference index for cat %s" %(cat))
plt.show()
