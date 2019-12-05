# coding: utf-8

__author__ = "Margherita Di Leo"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from SG_filter import *


def plotTimeSeries(cat, log, ts, national_park, dest_folder):
    cat = int(cat) #added because of stupid error
    log_ID = log['log_ID'][log.cat==cat][0]
    vline1 = log['Log_after'][log.cat==cat][0]
    vline2 = log['Log_before'][log.cat==cat][0]
    plt.figure
    # TODO add interp here because removed from filter
    # or uncomment from S-G_filter.py
    #interp_ts = interp_ts.interpolate(method='linear', limit=14)
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
    plt.show() 
    #plt.savefig(dest_folder+"NDVI time series for log ID %s (cat %s)" %(log_ID,cat))
    plt.close('all')
    return 0

#-----------------------------------------------------------------------

def plotDiff(log, ts, national_park, dest_folder):
    plt.figure(figsize=(12,8))
    np_filtered = SGFilter(national_park[1])
    for cat in log.index:
        cat = int(cat) #added because of stupid error
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
    plt.show()
    #plt.savefig(dest_folder+"NDVI deviation from reference National Park")
    plt.close('all')
    return 0

#-----------------------------------------------------------------------
