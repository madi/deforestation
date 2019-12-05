# coding: utf-8

__author__ = "Margherita Di Leo"

'''
Export data (deltas = differences between time series and reference 
in National Park) on a csv file 
The time series are smoothed with S-G filter

Usage:
python3 export_deltas.py
'''

import pandas as pd
import numpy as np
from time_reference import *
from SG_filter import *
import csv
from plot_utils import *
from load_data import *


######### Change paths according to locations in your machine ##########
file_location = '/storage/leomarg/Documents/v5/results/ndvi_big_areas_clean.csv'
national_park_file = '/storage/leomarg/Documents/v5/results/national_park_NDVI_clean.csv'
dest_csv = '/storage/leomarg/Documents/v5/results_postp/deltas_big_areas_NDVI.csv'
#########################################################################

cats = read_categories(file_location)
ts = read_ndvi(file_location)
national_park = read_nat_park(national_park_file)

# Export data (deltas = differences between time series and reference 
# in National Park) on a csv file 
np_filtered = SGFilter(national_park[1])
with open(dest_csv, mode='w') as deltas:
    deltas_writer = csv.writer(deltas, delimiter=',', quotechar='"', \
                               quoting=csv.QUOTE_MINIMAL)
    deltas_writer.writerow(np_filtered.index)
    for cat in cats.index:
        cat = int(cat)
        #if (cat==238 or cat==257):
            #delta = np.empty([len(ts[cat])])
            #delta.fill(np.nan)
        #else:
        #print "ts", ts[cat]
        ts_filtered = SGFilter(ts[cat])
        #print ("ts_filtered", ts_filtered)
        delta = ts_filtered - np_filtered
        #print ("cat", cat)
        #print ("delta", delta)
        deltas_writer.writerow(delta)

deltas.close()
