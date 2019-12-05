# coding: utf-8

__author__ = "Margherita Di Leo"

import pandas as pd
import numpy as np



def diff_rolling(series, n_p):
    np_upsampled = n_p[1].resample('D')
    np_interp = np_upsampled.interpolate(method = 'linear')
    w = 60 # window for rolling calculation
    np_r = np_interp.rolling(w).quantile(0.7)
    #series = ts[cat]
    ts_upsampled = series.resample('D')
    ts_interp = ts_upsampled.interpolate(method = 'linear')
    series_r = ts_interp.rolling(w).quantile(0.7) #.shift(-w//2+1)
    np_r = np_interp.rolling(w).quantile(0.7) #.shift(-w//2+1)
    diff_rolling = series_r - np_r
    #diff_interp = ts_interp - np_interp
    return diff_rolling


def diff_interp(series, n_p):
    np_upsampled = n_p[1].resample('D')
    np_interp = np_upsampled.interpolate(method = 'linear')
    w = 60 # window for rolling calculation
    np_r = np_interp.rolling(w).quantile(0.7)
    #series = ts[cat]
    ts_upsampled = series.resample('D')
    ts_interp = ts_upsampled.interpolate(method = 'linear')
    series_r = ts_interp.rolling(w).quantile(0.7) #.shift(-w//2+1)
    np_r = np_interp.rolling(w).quantile(0.7) #.shift(-w//2+1)
    #diff_rolling = series_r - np_r
    diff_interp = ts_interp - np_interp
    return diff_interp
