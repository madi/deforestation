# coding: utf-8

'''
Example
python3 time_series.py 50
where 50 is the category number
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import *
from scipy.signal import *
import sys
from stationarity_test import *

__author__ = "Margherita Di Leo"


file_location = "/media/madi/TOSHIBA EXT/S1/output/files/backscatter_change_pwr.csv"
national_park = "/media/madi/TOSHIBA EXT/S1/output/files/national_park_cross.csv"
dest_folder = "/media/madi/TOSHIBA EXT/S1/output/figures/validation2/"

# Category you want to display the backscatter signal for

#cat = 18373
cat = int(sys.argv[1])

def read_valid(file_location, cat):
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

ts = read_valid(file_location, cat)

#-----------------------------------------------------------------------

# Load backscatter data from National Park

data_np = pd.read_csv(national_park, skiprows=1, header=None, sep="|")
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

# Backscatter Means of time series

#bs_means = np.mean(ts, axis=1) 
bs_means = ts.resample('D').mean()
bs_means_r = bs_means.rolling(10).median()

# plot

series = ts
series = series.dropna(how = 'any', axis = 0)
series_r = series.rolling(10).median()
dates3 = series.index

fig=plt.figure(figsize=(16,4))
ax1=fig.add_subplot(111)
#ax1.plot(ts.index, bs_means_r, color='red')
ax1.set_xlabel('Date')
ax1.set_ylabel('$\overline{\gamma^o}$ [dB]')
ax1.plot(dates3, series_r, color='blue')
ax1.plot(dates1, npbs_r, color='green')
fig.legend(['Backscatter signal in Cat %s' %(cat), 
            'Backscatter signal in National Park' ],loc=1)
plt.xticks(rotation=45)
plt.grid()
#plt.show()
plt.savefig(dest_folder+'Backscatter_signal_for_Cat_%s.png' %cat)
plt.close()

# Stationarity test

# ts_upsampled = series.resample('D')
# ts_interp = ts_upsampled.interpolate(method = 'linear')
# test_stationarity(ts_interp)




