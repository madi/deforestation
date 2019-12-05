# coding: utf-8

import pandas as pd
import numpy as np
from scipy import *
from scipy.signal import *




def GaussianFilter(data):
    n = data.shape[0]
    # construct a n-point Gaussian filter with standard deviation = 4
    filt = gaussian(n, std = 4) 
    # normalize the filter through dividing by the sum of its elements
    filt /= sum(filt)
    # pad data on both sides with half the filter length 
    padded = concatenate((data[0]*ones(n//2), data, data[n-1]*ones(n//2)))
    # convolve the data with the filter
    #print 'len(padded) ', len(padded) 
    #print 'len(filt) ', len(filt) 
    smooth = convolve(padded, filt, mode='valid') 
    #mode='same' returns a vector that has as many elements as the original
    #set. mode='valid' retains only elements that have full overlap between
    #the data and the filter 
    return smooth
