# coding: utf-8

__author__ = "Margherita Di Leo"

import pandas as pd
import numpy as np
from time_reference import *
import csv
from plot_utils import *
from load_data import *

'''
Export data (deltas = differences between time series and reference 
in National Park) on a csv file 
The time series are smoothed with rolling quantile(0.7)

Usage:
python3 export_rolling_deltas.py
'''


######### Change paths according to locations in your machine ##########
file_location = '/storage/leomarg/Documents/v5/results/nbr_big_areas_clean.csv'
national_park_file='/storage/leomarg/Documents/v5/results/national_park_NBR_clean.csv'
dest_csv='/storage/leomarg/Documents/v5/results_postp/rolling_deltas_big_areas_NBR.csv'
#########################################################################

ts = read_ndvi(file_location)
n_p = read_nat_park(national_park_file)
cats = read_categories(file_location)

# Export data (deltas = differences between time series and reference 
# in National Park) on a csv file 

np_upsampled = n_p[1].resample('D')
np_interp = np_upsampled.interpolate(method = 'linear')
w = 60 # window for rolling calculation
np_r = np_interp.rolling(w).quantile(0.7)


#np_filtered = SGFilter(national_park[1])
with open(dest_csv, mode='w') as deltas:
    deltas_writer = csv.writer(deltas, delimiter=',', quotechar='"', \
                               quoting=csv.QUOTE_MINIMAL)
    deltas_writer.writerow(np_r.index)
    for cat in cats.index:
        cat = int(cat)
        series = ts[cat]
        #print(series)
        ts_upsampled = series.resample('D')
        ts_interp = ts_upsampled.interpolate(method = 'linear')
        #print(ts_interp)
        series_r = ts_interp.rolling(w).quantile(0.7) 
        delta = series_r - np_r
        #print(delta)
        deltas_writer.writerow(delta)

deltas.close()
