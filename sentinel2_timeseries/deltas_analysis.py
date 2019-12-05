# coding: utf-8

__author__ = "Margherita Di Leo"

import pandas as pd
import numpy as np
from load_data import *
from time_reference import *
import matplotlib.pyplot as plt

'''
Usage:
python3 deltas_analysis.py
'''

######### Change paths according to locations in your machine ##########
file_location = '/storage/leomarg/Documents/v5/results/nbr_big_areas_clean.csv'
deltas_file='/storage/leomarg/Documents/v5/results_postp/rolling_deltas_big_areas_NBR.csv'
#dest_deltas='/home/leomarg/rolling_deltas_T.csv'
#dest_csv='/home/leomarg/rolling_tstar.csv'
########################################################################

logging = read_logging(file_location)
ts = read_ndvi(file_location) 
deltas = read_deltas(deltas_file, file_location)

## Export deltas transposed
## saving file in order to have a more readable version
#deltas.to_csv(dest_deltas) 

cat=4 # this doesn't matter. I only need the index for any ts
series = ts[cat]
ts_upsampled = series.resample('D')
ts_interp = ts_upsampled.interpolate(method = 'linear')

#tstar_list = []
#for cat in logging.index:
    #tx = central_point(logging.loc[cat].Log_before, 
                       #logging.loc[cat].Log_after)
    #tx_date = get_date(tx)
    ##tx_date = logging.loc[cat].Log_before
    #t_star = (ts_interp.index - tx_date).astype('timedelta64[D]')
    #tstar_list.append(t_star)

#tstar = pd.DataFrame(tstar_list, index=ts.columns, columns=ts_interp.index).T

## Export tstar
#tstar.to_csv(dest_csv)

#fig = plt.figure()
#ax1 = fig.add_subplot(111)
#for i in (range(deltas.shape[1])):
    #ax1.plot(tstar.iloc[:,i], deltas.iloc[:,i], 
    #c='grey', linestyle='-', label=i)
#plt.axvline(x=0, color='k', linestyle='--')
#plt.axhline(y=0, color='k', linestyle='--')
#ax1.set_xlabel('T*=T-Tx: Day, normalized at the intermediate point between Log_after and Log_before')
#ax1.set_ylabel('Difference index')
#plt.suptitle('Difference Index')
#plt.title('Differences between the time series and the National Park, normalized against logging time')
#plt.grid(True)
#plt.show()

deltas_flat = deltas.sum(axis=1, skipna=True) 
# devo sommare i delta che corrispondono allo stesso tstar.

logmax = logging['Log_before'].max()
logmin = logging['Log_after'].min()

fig2 = plt.figure()
ax1 = fig2.add_subplot(111)
plt.axis([np.min(deltas.index), np.max(deltas.index), 2 * np.min(deltas_flat), 2 * np.max(deltas_flat)])
plt.axhline(y=0, color='k', linestyle='--')
plt.axvspan(logmin, logmax, alpha=0.25, color='grey')
plt.axvline(x=logmin, color='m', linestyle='--')
plt.axvline(x=logmax, color='m', linestyle='--')
plt.scatter(deltas.index, deltas_flat)
plt.xticks(rotation=45)
ax1.set_xlabel('Absolute time')
ax1.set_ylabel('Cumulative sum of delta between time series and National Park')
plt.title('Cumulative sum of Difference Index')
plt.grid()
plt.show()






