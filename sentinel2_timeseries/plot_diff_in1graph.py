# coding: utf-8

__author__ = "Margherita Di Leo"

'''
Usage:
python3 plot_diff_in1graph.py
'''

import pandas as pd
import numpy as np
from time_reference import *
from SG_filter import *
import csv
from plot_utils import *
from load_data import *


######### Change paths according to locations in your machine ##########
file_location = '/home/leomarg/ndvi_big_areas.csv'
national_park_file='/home/leomarg/national_park.csv'
dest_folder='/home/leomarg/tmp/'
########################################################################

log = read_logging(file_location)
ts = read_ndvi(file_location)
national_park = read_nat_park(national_park_file)

plotDiff(log, ts, national_park, dest_folder)
