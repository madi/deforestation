# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from load_data import *
import argparse



'''
Usage example:
python3 differences.py --c 4 
'''

######### Change paths according to locations in your machine ##########
# file_location = '/storage/leomarg/Documents/v5/results/nbr_big_areas_clean.csv'
# national_park_file='/storage/leomarg/Documents/v5/results/national_park_NBR_clean.csv'
# dest_folder='/storage/leomarg/Documents/v5/results_postp/ndvi_diff_plots/'
file_location = '/media/madi/TOSHIBA EXT/S2_Bialo/validation/ndvi_change.csv'
national_park_file='/media/madi/TOSHIBA EXT/S2_Bialo/S2_results_v5/results/national_park_NDVI_clean.csv'
dest_folder='/media/madi/TOSHIBA EXT/S2_Bialo/validation/ndvi_diff_plots/'
########################################################################

parser = argparse.ArgumentParser(description = 'Plot differences \
between a time series and reference undisturbed ndvi (natural park)   \
Usage example:                                                 \
python3 differences.py --c 4 ')

parser.add_argument('--c', dest = "cat",
help = "Category. ")

args = parser.parse_args()

cat = int(args.cat)

ts = read_ndvi(file_location)
n_p = read_nat_park(national_park_file)
log = read_logging(file_location)

np_upsampled = n_p[1].resample('D')
np_interp = np_upsampled.interpolate(method = 'linear')

w = 60 # window for rolling calculation
np_r = np_interp.rolling(w).quantile(0.7)


series = ts[cat]

ts_upsampled = series.resample('D')
ts_interp = ts_upsampled.interpolate(method = 'linear')


series_r = ts_interp.rolling(w).quantile(0.7) #.shift(-w//2+1)
np_r = np_interp.rolling(w).quantile(0.7) #.shift(-w//2+1)

diff_rolling = series_r - np_r
diff_interp = ts_interp - np_interp

vline1 = log['Log_after'][log.cat==cat][0]
vline2 = log['Log_before'][log.cat==cat][0]
xposition = [vline1, vline2]
    

fig, ax = plt.subplots()
plt.title('Difference between time series for patch %s and undisturbed area' %cat)
#plt.plot(diff_interp, 'r', label='diff interp')
plt.plot(diff_rolling, 'm', label='diff rolling')
plt.axhline(y=0, color='k', linestyle='--')
plt.xticks(rotation=45)
for xc in xposition:
    plt.axvline(x=xc, color='k', linestyle='--')
plt.axvspan(vline1, vline2, alpha=0.5, color='grey')


ax.fill_between(diff_rolling.index, diff_rolling, where=diff_rolling>=0, \
                interpolate=True, color='blue')
ax.fill_between(diff_rolling.index, diff_rolling, where=diff_rolling<=0, \
                interpolate=True, color='red')

plt.grid()
plt.show()
#plt.savefig(dest_folder+'Difference between time series for patch %s and undisturbed area' %cat)
plt.close('all')

    
    
