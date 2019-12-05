# coding: utf-8

import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

def SGFilter(timeseries, wnds=[15, 9], orders=[3, 6], debug=False): 
    '''
    Savitzky Golay Filter
    Source:
    https://gis.stackexchange.com/questions/173721/reconstructing-modis-time-series-applying-savitzky-golay-filter-with-python-nump
    wnds=[15, 9], orders=[3, 6]
    '''                                    
    interp_ts = pd.Series(timeseries)
    #interp_ts = interp_ts.interpolate(method='linear', limit=14)
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
