# coding: utf-8

__author__ = "Margherita Di Leo"

import pandas as pd
import numpy as np
from time_reference import *
from SG_filter import *
import csv
from plot_utils import *
from load_data import *


######### Change paths according to locations in your machine ##########
file_location = '/storage/leomarg/Documents/v5/results/ndvi_big_areas1.csv'
national_park_file='/storage/leomarg/Documents/v5/results/national_park_NDVI_clean.csv'
dest_folder='/home/leomarg/tmp1'
########################################################################

log = read_logging(file_location)
ts = read_ndvi(file_location)
national_park = read_nat_park(national_park_file)

cat = 74
plotTimeSeries(cat, log, ts, national_park, dest_folder)


