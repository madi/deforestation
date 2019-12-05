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
file_location = '/storage/leomarg/Documents/v5/results/ndvi_big_areas1.csv'
national_park_file='/storage/leomarg/Documents/v5/results/national_park_NDVI_clean.csv'
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
    np_smooth = GaussianFilter(np_interp)
    np_smooth_gauss = pd.DataFrame(np_smooth, index=ts_interp.index)
    # Plot 
    plt.figure(1, figsize=(12,8))
    plt.scatter(series.index, series, c='r', label='TS original')
    plt.scatter(n_p.index, n_p, c='g', label='NP original')
    plt.plot(ts_interp, 'm', label='TS interp')
    plt.plot(ts_smooth_gauss, 'r', label='TS Gauss')
    plt.plot(np_smooth_gauss, 'g', label='Natural Park Gauss')
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
    plt.plot(ts_interp, 'm', label='TS interp')
    plt.plot(ts_smooth_sg, 'r', label='TS Savitzky Golay')
    plt.plot(np_smooth_sg, 'g', label='Natural Park S-G')
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


if method == 'gauss':
    plotGauss (ts_interp, np_interp)
    #plotGauss (series_r, np_r)
elif method == 'sg':
    #plotSG (ts_interp, np_interp)
    plotSG (series_r, np_r)
else:
    print ("Method not available")


