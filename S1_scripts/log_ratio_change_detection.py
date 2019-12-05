
from plot_utils import *

import gdal
import numpy as np
import pandas as pd
import time, os, glob
import matplotlib.pylab as plt
from plot_utils import *

pol="vv"

datadirectory="/media/madi/TOSHIBA EXT/S1/S1_db"


if pol=="vv":
    datefile="/media/madi/TOSHIBA EXT/S1/S1_files/S1_db_vv.dates"
    imagefile="/media/madi/TOSHIBA EXT/S1/S1_db/s1_db_stack_vv.vrt"
    dest_folder="/media/madi/TOSHIBA EXT/S1/output"
elif pol=="vh":
    datefile="/media/madi/TOSHIBA EXT/S1/S1_files/S1_db_vh.dates"
    imagefile="/media/madi/TOSHIBA EXT/S1/S1_db/s1_db_stack_vh.vrt"
    dest_folder="/media/madi/TOSHIBA EXT/S1/output"
else:
    print("Data for selected polarization are not available.")


os.chdir(datadirectory)
os.getcwd()
glob.glob("*.vrt")

# Read from the dates file the dates in the time series and make a pandas date index

dates=open(datefile).readlines()
tindex=pd.DatetimeIndex(dates)

# print(dates)
# print(tindex)

# Image data

img=gdal.Open(imagefile)

# # Print look-up table date <-> band

# j=1
# print('Bands and dates for ', imagefile)
# for i in tindex:
    # print("{:4d} {}".format(j, i.date()), end=' ')
    # j+=1
    # if j%5==1:print()


bandn_r=194 # 2017-07-06
bandn_n=229 # 2018-07-01

raster_r=img.GetRasterBand(bandn_r).ReadAsArray() # reference
raster_n=img.GetRasterBand(bandn_i).ReadAsArray() # newer

raster_logratio = np.log10(raster_n/raster_r)

showLogRatioChange(raster_logratio,tindex,bandn_r,bandn_n)

'''
In the log-ratio image, unchanged features have intermediate gray tones 
(gray value around zero) while change features are either bright white 
or dark black. Black features indicate areas where radar brightness
decreased while in white areas, the brightness has increased. 
'''
