# coding: utf-8

# DEPRECATED

__author__ = "Margherita Di Leo"

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from scipy.signal import savgol_filter
import csv

######### Change paths according to locations in your machine ##########
file_location = '/home/leomarg/ndvi_big_areas1.csv'
logging_file='/home/leomarg/logging_points.csv'
national_park_file='/home/leomarg/national_park_wo_loss_scl_NDVI_1.csv'
dest_folder='/mnt/cidstorage/cid_bulk_22/cid-bulk22/Shared/projectData/CANHEMON/tmp/Margherita/v3/S-G_filter/'
dest_csv='/home/leomarg/deltas.csv'
########################################################################


def SGFilter(timeseries, wnds=[15, 9], orders=[3, 6], debug=False): 
    '''
    Savitzky Golay Filter
    Source:
    https://gis.stackexchange.com/questions/173721/reconstructing-modis-time-series-applying-savitzky-golay-filter-with-python-nump
    wnds=[15, 9], orders=[3, 6]
    '''                                    
    interp_ts = pd.Series(timeseries)
    interp_ts = interp_ts.interpolate(method='linear', limit=14)
    smooth_ts = interp_ts                                                                                              
    wnd, order = wnds[0], orders[0]
    # larger wnd -> smoother
    # wnd must be odd
    # smaller order -> smoother
    # order must be set in a range from 2 to 4
    # in the second iteration, a smaller wnd and a larger order of the polynomial are set
    # in Chen et al 2004, Authors suggest wnds=[15, 9], orders=[3, 6]
    # wnd=2*m ; optimal m=4 (but wnd must be odd, so wnd=9) and d=6
    F = 1e8 
    W = None
    it = 0                                                                                                             
    while True:
        smoother_ts = savgol_filter(smooth_ts, window_length=wnd, polyorder=order)                                     
        diff = smoother_ts - interp_ts
        sign = diff > 0                                                                                                                       
        if W is None:
            W = 1 - np.abs(diff) / np.max(np.abs(diff)) * sign                                                         
            wnd, order = wnds[1], orders[1]                                                                            
        fitting_score = np.sum(np.abs(diff) * W)                                                                       
        #print it, ' : ', fitting_score
        if fitting_score > F:
            break
        else:
            F = fitting_score
            it += 1        
        smooth_ts = smoother_ts * sign + interp_ts * (1 - sign)
    if debug:
        return smooth_ts, interp_ts
    return smooth_ts

#-----------------------------------------------------------------------

def plotTimeSeries(cat):
    log_ID = log['log_ID'][cat]
    vline1 = log['Log_after'][cat]
    vline2 = log['Log_before'][cat]
    plt.figure
    ts_filtered = SGFilter(ts[cat])
    np_filtered = SGFilter(national_park[1])
    plt.plot(ts_filtered, marker='o', color='blue')
    plt.plot(np_filtered, marker='o', color='green', label='National Park average NDVI')
    #plt.legend(loc='lower left')
    xposition = [vline1, vline2]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.axvspan(vline1, vline2, alpha=0.5, color='grey')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.title("NDVI time series for log ID %s (cat %s)" %(log_ID,cat))
    #plt.show() 
    plt.savefig(dest_folder+"NDVI time series for log ID %s (cat %s)" %(log_ID,cat))
    plt.close('all')

#-----------------------------------------------------------------------

def plotDiff():
    plt.figure(figsize=(12,8))
    np_filtered = SGFilter(national_park[1])
    for cat in log.index:
        ts_filtered = SGFilter(ts[cat])
        delta=(ts_filtered-np_filtered.transpose()).transpose()
        plt.plot(delta, color='magenta')
    #plt.plot(np_filtered, marker='o', color='green')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel(r"$\Delta = TS_i - NP$", rotation=0, position=(-0.1,0.5))
    plt.title("NDVI time series deviation from reference National Park")
    # horizontal line
    plt.axhline(y=0, color='green', linestyle='--') 
    #plt.show()
    plt.savefig("NDVI deviation from reference National Park")
    plt.close('all')
    


### Read and tidy up data
########################################################################
#### Time Series ####
data = pd.read_csv(file_location, header=None)
del data[4]
del data[3]
del data[2]
del data[1]
del data[0]
df = data.transpose()
df = df.replace('*', np.nan)
new_df0 = []
for item in df[0]:
    year, month, day = [e for n, e in enumerate(item.split('_')) if n in (4, 5, 6)]
    new_df0.append(year+"-"+month+"-"+day)

df[0] = pd.to_datetime(new_df0)
for i in range(df.shape[1]):
    df[i] = pd.to_numeric(df[i])

df[0] = pd.to_datetime(df[0]) # I have to do it twice - first time 
#is because otherwise it would give an error when transforming to numeric
#df.info()
#df.dtypes
#df.describe()
# create time series indexing by date
ts = df.set_index(df.ix[:,0])
#ts.index

########################################################################
#### Logging ####
# Load and tidy up data about logging
logging = pd.read_csv(logging_file, header=0)
#logging.head()
# indexing by cat (primary key/pivot)
log=logging.set_index('cat')
#log.head()
# convert dates to datetime
log['Log_after'] = pd.to_datetime(log['Log_after'], format='%d.%m.%Y')
log['Log_before'] = pd.to_datetime(log['Log_before'], format='%d.%m.%Y')
#log.info()

########################################################################
#### National Park ####
# Load and tidy up data about National Park
# Unused columns deleted by hand
national_park = pd.read_csv(national_park_file, skiprows=1, header=None)
national_park[0] = pd.to_datetime(national_park[0])
national_park=national_park.set_index(0)
national_park[1] = pd.to_numeric(national_park[1])
national_park = national_park.replace('*', np.nan)
# national_park.index

########################################################################
# What would you like to do? Uncomment the code snippet that applies

# loop over cat and make plot
#for item in log.index:
    #plotTimeSeries(item)
  
# plot one time series
#cat = 243
#plotTimeSeries(cat)

# plot differences all in one graph
#plotDiff()

# Export data (deltas = differences between time series and reference 
# in National Park) on a csv file 
#np_filtered = SGFilter(national_park[1])
#with open(dest_csv, mode='w') as deltas:
    #deltas_writer = csv.writer(deltas, delimiter=',', quotechar='"', \
                               #quoting=csv.QUOTE_MINIMAL)
    #deltas_writer.writerow(np_filtered.index)
    #for cat in log.index:
        #ts_filtered = SGFilter(ts[cat])
        #delta = ts_filtered - np_filtered
        #deltas_writer.writerow(delta)

#deltas.close()
########################################################################

