
from plot_utils import *
from lee_filter import *

import gdal
import numpy as np
import pandas as pd
import time, os, glob
import matplotlib.pylab as plt
import matplotlib.animation

pol="vh"

datadirectory="/media/madi/TOSHIBA EXT/S1/S1_cropped"


if pol=="vv":
    datefile="/media/madi/TOSHIBA EXT/S1/S1_files/S1_vv.dates"
    imagefile="/media/madi/TOSHIBA EXT/S1/S1_cropped/s1_stack_vv.vrt"
    dest_folder="/media/madi/TOSHIBA EXT/S1/output"
elif pol=="vh":
    datefile="/media/madi/TOSHIBA EXT/S1/S1_files/S1_vh.dates"
    imagefile="/media/madi/TOSHIBA EXT/S1/S1_cropped/s1_stack_vh.vrt"
    dest_folder="/media/madi/TOSHIBA EXT/S1/output"
else:
    print("Data for selected polarization are not available.")


os.chdir(datadirectory)
os.getcwd()
glob.glob("*.vrt")

# Read from the dates file the dates in the time series and make a pandas date index

dates=open(datefile).readlines()
tindex=pd.DatetimeIndex(dates)

# Image data

img=gdal.Open(imagefile)

bandn=499

raster=img.GetRasterBand(bandn).ReadAsArray()

# showImage(raster, tindex, bandn, 0., 0.1)

# showNormImg(raster, tindex, bandn, 0., 0.1)

plotLee(raster)
