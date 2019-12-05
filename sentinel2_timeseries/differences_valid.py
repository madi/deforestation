# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from load_data import *
import argparse
import os



'''
Usage example:
python3 differences.py --c 4 
'''

######### Change paths according to locations in your machine ##########
file_location_ndvi = '/media/madi/TOSHIBA EXT/S2_Bialo/validation/ndvi_change.csv'
#file_location_nbr = '/media/madi/TOSHIBA EXT/S2_Bialo/validation/nbr_change.csv'
national_park_ndvi='/media/madi/TOSHIBA EXT/S2_Bialo/S2_results_v5/results/national_park_NDVI_clean.csv'
dest_folder='/media/madi/TOSHIBA EXT/S2_Bialo/validation/ndvi_diff_plots/'
# Sentinel 1
file_location_bs = "/media/madi/TOSHIBA EXT/S1/output/files/backscatter_change_pwr.csv"
national_park_bs = "/media/madi/TOSHIBA EXT/S1/output/files/national_park_cross.csv"
#script_location = '/media/madi/TOSHIBA\ EXT/S1/S1_scripts/validation/'
########################################################################

parser = argparse.ArgumentParser(description = 'Plot differences \
between a time series and reference undisturbed ndvi (natural park)   \
Usage example:                                                 \
python3 differences.py --c 4 ')

parser.add_argument('--c', dest = "cat",
help = "Category. ")

args = parser.parse_args()

cat = int(args.cat)

w = 60 # window for rolling calculation

#-----------------------------------------------------------------------

def read_valid_bs(file_location, cat):
    '''
    Read validation data
    '''
    data = pd.read_csv(file_location, header=None, low_memory=False)
    df = data.iloc[:,4:].transpose()
    df = df.replace('*', np.nan)
    new_df0 = []
    for item in df[0]:
        stringa = item.split('_')
        year, month, day = stringa[-7],stringa[-6],stringa[-5]
        new_df0.append(year+"-"+month+"-"+day)
    dates = pd.to_datetime(new_df0)
    series = pd.to_numeric(df[cat])
    cats = data[0]
    ts = pd.Series(series.values, index=dates)
    return ts

#-----------------------------------------------------------------------

# NDVI National Park
n_p = read_nat_park(national_park_ndvi)
np_upsampled = n_p[1].resample('D')
np_interp = np_upsampled.interpolate(method = 'linear')
np_r = np_interp.rolling(w).quantile(0.7)

# NDVI time series
series_ndvi = read_valid(file_location_ndvi, cat)
ts_upsampled_ndvi = series_ndvi.resample('D')
ts_interp_ndvi = ts_upsampled_ndvi.interpolate(method = 'linear')
series_r_ndvi = ts_interp_ndvi.rolling(w).quantile(0.7) 
diff_rolling_ndvi = series_r_ndvi - np_r

#-----------------------------------------------------------------------

# Backscatter time series
ts_bs = read_valid_bs(file_location_bs, cat)
# Backscatter Means of time series
bs_means = ts_bs.resample('D').mean()
bs_means_r = bs_means.rolling(10).median()

#-----------------------------------------------------------------------

# Backscatter from National Park
data_np = pd.read_csv(national_park_bs, skiprows=1, header=None, sep="|")
data_np = data_np.dropna(how='any', axis=0)

dates1 = []
for item in (data_np[1][:]):
    item2 = item.split(" ")
    year,month,day = item2[0].split('-')
    date = year+"-"+month+"-"+day
    dates1.append(date)

dates1 = pd.to_datetime(dates1)

# National Park Backscatter
npbs = pd.to_numeric(data_np[3])
npbs = npbs.replace('*', np.nan)
npbs = pd.DataFrame(npbs)
npbs.set_index(dates1)
npbs_r = npbs.rolling(10).median()

#-----------------------------------------------------------------------

# Plot Backscatter + NDVI

series_bs = ts_bs
series_bs = series_bs.dropna(how = 'any', axis = 0)
series_r = series_bs.rolling(10).median()
dates3 = series_bs.index

# Figure (Both NDVI and Backscatter)
fig, ax = plt.subplots(2, figsize=(20, 15), sharex=True)
plt.suptitle('Signals for Cat %s' %cat, \
             fontsize=18, fontweight='bold')
ax[0].set_title('Difference Index NDVI')
ax[0].plot(diff_rolling_ndvi, 'm', label='Difference Index')
ax[0].axhline(y=0, color='k', linestyle='--')
ax[0].fill_between(diff_rolling_ndvi.index, diff_rolling_ndvi, where=diff_rolling_ndvi>=0, \
                interpolate=True, color='blue')
ax[0].fill_between(diff_rolling_ndvi.index, diff_rolling_ndvi, where=diff_rolling_ndvi<=0, \
                interpolate=True, color='red')
ax[0].grid()
ax[1].set_title('Backscatter')
ax[1].set_xlabel('Date')
ax[1].set_ylabel('$\overline{\gamma^o}$ [dB]')
ax[1].plot(dates3, series_r, color='blue')
ax[1].plot(dates1, npbs_r, color='green')
fig.legend(['Backscatter signal in Cat %s' %(cat), 
            'Backscatter signal in National Park' ],loc=1)
plt.xticks(rotation=45)
plt.grid()
plt.show()
# plt.savefig(dest_folder+'NDVI_Backscatter_for_Cat_%s.png' %cat)
plt.close('all')

#-----------------------------------------------------------------------

# # NBR
# series_nbr = read_valid(file_location_nbr, cat)
# ts_upsampled_nbr = series_nbr.resample('D')
# ts_interp_nbr = ts_upsampled_nbr.interpolate(method = 'linear')
# series_r_nbr = ts_interp_nbr.rolling(w).quantile(0.7) 
# # diff_rolling_nbr = series_r_nbr - np_r

# # Figure (Both NDVI and NBR)
# fig, ax = plt.subplots(2, figsize=(20, 15), sharex=True)
# plt.suptitle('Difference between signals for Cat %s and National Park' %cat, \
             # fontsize=18, fontweight='bold')
# ax[0].set_title('NDVI')
# ax[0].plot(diff_rolling_ndvi, 'm', label='Difference')
# ax[0].axhline(y=0, color='k', linestyle='--')
# ax[0].fill_between(diff_rolling_ndvi.index, diff_rolling_ndvi, where=diff_rolling_ndvi>=0, \
                # interpolate=True, color='blue')
# ax[0].fill_between(diff_rolling_ndvi.index, diff_rolling_ndvi, where=diff_rolling_ndvi<=0, \
                # interpolate=True, color='red')
# ax[0].grid()
# ax[1].set_title('NBR')
# ax[1].plot(diff_rolling_nbr, 'm', label='Difference')
# ax[1].axhline(y=0, color='k', linestyle='--')
# ax[1].fill_between(diff_rolling_nbr.index, diff_rolling_nbr, where=diff_rolling_nbr>=0, \
                # interpolate=True, color='blue')
# ax[1].fill_between(diff_rolling_nbr.index, diff_rolling_nbr, where=diff_rolling_nbr<=0, \
                # interpolate=True, color='red')
# plt.xticks(rotation=45)
# plt.grid()
# #plt.show()
# plt.savefig(dest_folder+'NDVI_NBR_for_Cat_%s.png' %cat)
# plt.close('all')

#-----------------------------------------------------------------------

# # Figure (only NDVI)
# fig, ax = plt.subplots(figsize=(20, 5))
# plt.title('Difference between NDVI signals for Cat %s and National Park' %cat, \
             # fontsize=18)
# ax.plot(diff_rolling_ndvi, 'm', label='Difference')
# ax.axhline(y=0, color='k', linestyle='--')
# ax.fill_between(diff_rolling_ndvi.index, diff_rolling_ndvi, where=diff_rolling_ndvi>=0, \
                # interpolate=True, color='blue')
# ax.fill_between(diff_rolling_ndvi.index, diff_rolling_ndvi, where=diff_rolling_ndvi<=0, \
                # interpolate=True, color='red')

# plt.xticks(rotation=45)
# plt.grid()
# # plt.show()
# plt.savefig(dest_folder+'NDVI_for_Cat_%s.png' %cat)
# plt.close('all')

#-----------------------------------------------------------------------

# # Make plot for backscatter from Sentinel 1

# cmd = "python3 "+script_location+"time_series.py "+str(cat)
# os.system(cmd)
    
