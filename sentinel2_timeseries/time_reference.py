# coding: utf-8

__author__ = "Margherita Di Leo"

import pandas as pd
import numpy as np


def create_dates():
    start_date = pd.to_datetime('2015-06-23', format='%Y-%m-%d')
    end_date = pd.to_datetime('2019-01-10', format='%Y-%m-%d')
    days = pd.date_range(start_date, end_date, freq='D')
    dates = pd.Series(range(len(days)), index=days)
    return dates 

def central_point(date1, date2):
    '''
    Returns central point in time
    '''
    dates = create_dates()
    dates_user = [date1, date2]
    dates_user.sort()
    central_day = (((dates_user[1]-dates_user[0])/2)+dates_user[0]).normalize()
    central_n = dates[[central_day]][0]
    return central_n
    
def get_date(number):
    '''
    Given a number between 0 and 1297 returns the corresponding date
    0 = 2015-06-23; 1297 = 2019-01-10
    '''
    dates = create_dates()
    date = dates[dates == number].index[0]
    return date



## Test

# central point between 2 dates
# central_point('2019-01-01', '2019-01-10')
# 1283

# get_date(1283)
# Timestamp('2018-12-27 00:00:00', offset='D')




