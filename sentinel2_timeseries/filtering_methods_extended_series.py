# coding: utf-8

from __future__ import print_function
import pandas as pd
import numpy as np
from scipy import *
from scipy.signal import *
import matplotlib.pyplot as plt
from load_data import *
from SG_filter import *
from Gaussian_filter import *
import argparse



'''
Usage example:
python3 filtering_methods.py --c 4 --m sg
(category = 4, method = Savitzky Golay)

valgrind --leak-check=yes python filtering_methods.py --c 163 --m sg
'''


######### Change paths according to locations in your machine ##########
file_location = '/home/leomarg/ndvi_big_areas_v4.csv'
national_park_file='/home/leomarg/national_park_v4_1.csv'
dest_folder='/home/leomarg/tmp/'
########################################################################



parser = argparse.ArgumentParser(description = 'Plot result of \
different filtering methods.                                   \
Usage example:                                                 \
python3 filtering_methods.py --c 4 --m sg                       \
(category = 4, method = Savitzky Golay)')

parser.add_argument('--c', dest = "cat",
help = "Category. ")

parser.add_argument('--m', dest = "method",
help = "Filter method. Available: gauss, sg (Savitzky Golay).")

args = parser.parse_args()

cat = int(args.cat)
method = args.method

ts = read_ndvi(file_location)
n_p = read_nat_park(national_park_file)
log = read_logging(file_location)




def plotGauss (ts_interp, np_interp):
    log_ID = log['log_ID'][log.cat==cat][0]
    vline1 = log['Log_after'][log.cat==cat][0]
    vline2 = log['Log_before'][log.cat==cat][0]
    ts_smooth = GaussianFilter(ts_interp)
    ts_smooth_gauss = pd.DataFrame(ts_smooth, index=ts_interp.index)
    #print 'len(ts_smooth_gauss) ', len(ts_smooth_gauss)
    #print ts_smooth_gauss
    np_smooth = GaussianFilter(np_interp)
    np_smooth_gauss = pd.DataFrame(np_smooth, index=ts_interp.index)
    # Plot 
    plt.figure(1, figsize=(12,8))
    plt.scatter(series.index, series, c='r', label='TS original')
    plt.scatter(n_p.index, n_p, c='g', label='NP original')
    plt.plot(ts_interp.loc['2016-12-06':'2019-01-07'], 'm', label='TS interp')
    plt.plot(ts_smooth_gauss.loc['2016-12-06':'2019-01-07'], 'r', label='TS Gauss')
    plt.plot(np_smooth_gauss.loc['2016-12-06':'2019-01-07'], 'g', label='Natural Park Gauss')
    xposition = [vline1, vline2]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.axvspan(vline1, vline2, alpha=0.5, color='grey')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.title("Gaussian Filter applied to cat %s" %(cat))
    plt.legend(loc='upper left')
    plt.show()
    #plt.savefig(dest_folder+"Gaussian Filter applied to log ID %s (cat %s)" %(log_ID,cat))
    plt.close('all')
    return 0
    


def plotSG (ts_interp, np_interp):
    log_ID = log['log_ID'][log.cat==cat][0]
    vline1 = log['Log_after'][log.cat==cat][0]
    vline2 = log['Log_before'][log.cat==cat][0]
    np_smooth_sg = SGFilter(np_interp)
    ts_smooth_sg = SGFilter(ts_interp)
    # Plot 
    plt.figure(1, figsize=(12,8))
    plt.scatter(series.index, series, c='r', label='TS original')
    plt.scatter(n_p.index, n_p, c='g', label='NP original')
    plt.plot(ts_interp.loc['2016-12-06':'2019-01-07'], 'm', label='TS interp')
    plt.plot(ts_smooth_sg.loc['2016-12-06':'2019-01-07'], 'r', label='TS Savitzky Golay')
    plt.plot(np_smooth_sg.loc['2016-12-06':'2019-01-07'], 'g', label='Natural Park S-G')
    xposition = [vline1, vline2]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')
    plt.axvspan(vline1, vline2, alpha=0.5, color='grey')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.title("Savitzky Golay Filter applied to cat %s" %(cat))
    plt.legend(loc='upper left')
    plt.show()
    #plt.savefig(dest_folder+"Savitzky Golay Filter applied to log ID %s (cat %s)" %(log_ID,cat))
    plt.close('all')
    return 0



#cat = 163
series = ts[cat]

np_upsampled = n_p[1].resample('D')
np_interp = np_upsampled.interpolate(method = 'linear')

ts_upsampled = series.resample('D')
ts_interp = ts_upsampled.interpolate(method = 'linear')

series_r = ts_interp.rolling(60).quantile(0.7)
np_r = np_interp.rolling(60).quantile(0.7)

# Extending the time series to left (pre)
pre_values=series_r.loc['2016-12-06':'2018-11-27'].values
#pre_index = pd.date_range(start='2014-12-08', end='2016-11-29', freq='D')
pre_index = pd.date_range(start='2014-12-08', end='2016-11-28', freq='D')
pre_series=pd.Series(pre_values, index=pre_index)

# Extending the National Park time series to left
pre_values_np=np_r.loc['2016-12-06':'2018-11-27'].values
pre_np=pd.Series(pre_values_np, index=pre_index)

# Extending the time series to right (post)
post_values=ts_interp.loc['2016-01-10':'2018-11-27'].values
#post_index = pd.date_range(start='2019-01-08', periods=104, freq='D')
post_index = pd.date_range(start='2019-01-08', periods=len(post_values), freq='D')
post_series=pd.Series(post_values, index=post_index)

# Extending the National Park time series to left
post_values_np=np_interp.loc['2016-01-10':'2018-11-27'].values
post_np=pd.Series(post_values_np, index=post_index)

# Put all together
new_series = pre_series.append(ts_interp)
ts_extended=new_series.append(post_series)

new_np = pre_np.append(np_interp)
np_extended=new_np.append(post_np)

if method == 'gauss':
    #plotGauss (ts_interp, np_interp)
    plotGauss (ts_extended, np_extended)
elif method == 'sg':
    #plotSG (ts_interp, np_interp)
    plotSG (ts_extended, np_extended)
else:
    print ("Method not available")


