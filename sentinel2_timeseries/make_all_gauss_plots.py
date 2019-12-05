# coding: utf-8

__author__ = "Margherita Di Leo"


from load_data import *
import os


######### Change paths according to locations in your machine ##########
file_location = '/home/leomarg/ndvi_big_areas_v4.csv'
# Also change dest_folder in filtering_methods.py
########################################################################

log = read_logging(file_location)


for cat in log.index:
    cmd = "python filtering_methods.py --c %s --m gauss" %(cat)
    os.system(cmd)
