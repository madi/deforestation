# coding: utf-8

__author__ = "Margherita Di Leo"

'''
Makes a plot for each time series
'''


#from plot_utils import *
from load_data import *
import os




######### Change paths according to locations in your machine ##########
file_location = '/storage/leomarg/Documents/v5/results/ndvi_big_areas_clean.csv'
#national_park_file='/home/leomarg/national_park.csv'
#dest_folder='/home/leomarg/tmp1/'
########################################################################

cats = read_categories(file_location)
#ts = read_ndvi(file_location)
#national_park = read_nat_park(national_park_file)

#for item in cats.index:
    #plotTimeSeries(item, log, ts, national_park, dest_folder)
    
for cat in cats.index:
    cmd = ('python3 differences.py --c %s' %cat)
    os.popen(cmd)


