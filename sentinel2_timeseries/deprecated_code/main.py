# coding: utf-8

# DEPRECATED

__author__ = "Margherita Di Leo"

import pandas as pd
import numpy as np
from time_reference import *
from SG_filter import *
import csv
from plot_utils import *


######### Change paths according to locations in your machine ##########
file_location = '/home/leomarg/ndvi_big_areas1.csv'
national_park_file='/home/leomarg/national_park_wo_loss_scl_NDVI_1.csv'
dest_folder='/mnt/cidstorage/cid_bulk_22/cid-bulk22/Shared/projectData/CANHEMON/tmp/Margherita/v3/tmp/'
dest_csv='/mnt/cidstorage/cid_bulk_22/cid-bulk22/Shared/projectData/CANHEMON/tmp/Margherita/v3/tmp/deltas.csv'
########################################################################

def read_logging(data):
    '''
    create dataframe with info about logging, such as logging date, cat, 
    log_ID and area
    '''
    logging = pd.DataFrame([data[0],data[1],data[2],data[3],data[4]]).transpose()
    # logging.head()
    # set the column label to equal the values in the first row (index location 0)
    headers = logging.iloc[0]
    log = pd.DataFrame(logging.values[1:], columns = headers)
    del logging
    del headers
    log = log.set_index(log.ix[:,0])
    log['cat'] = pd.to_numeric(log['cat'])
    log['log_ID'] = pd.to_numeric(log['log_ID'])
    log['Log_after'] = pd.to_datetime(log['Log_after'], format='%d.%m.%Y')
    log['Log_before'] = pd.to_datetime(log['Log_before'], format='%d.%m.%Y')
    log['App_area_h'] = pd.to_numeric(log['App_area_h'])
    #log.dtypes
    #log.index.get_values()
    #log.columns
    # Index([u'cat', u'log_ID', u'Log_after', u'Log_before', u'App_area_h'], dtype='object', name=0)
    return log

#-----------------------------------------------------------------------
    
def read_ndvi(data):
    '''
    create time series of NDVI values for patches 
    '''
    df = data.iloc[:,5:].transpose()
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
    logging = read_logging(data)
    df_headers = logging['cat']
    headers=pd.concat([pd.Series(['date']), df_headers])
    del logging
    del df_headers
    df.columns = headers
    ts = df.set_index(df.ix[:,0])
    return ts

#-----------------------------------------------------------------------

def read_nat_park(national_park_file):
    '''
    Load and tidy up data about National Park
    '''
    national_park = pd.read_csv(national_park_file, skiprows=1, header=None)
    national_park[0] = pd.to_datetime(national_park[0])
    national_park=national_park.set_index(0)
    national_park[1] = pd.to_numeric(national_park[1])
    national_park = national_park.replace('*', np.nan)
    # national_park.index
    return national_park

########################################################################

# Main
data = pd.read_csv(file_location, header=None)

# Logging
logging = read_logging(data)
# logging[logging.cat==2]
# logging[logging.cat==2].Log_before[0]
# ts[2]
# logging[logging.cat==2].Log_after[0]
# Timestamp('2017-08-31 00:00:00')
# logging[logging.cat==2].Log_before[0]
# Timestamp('2018-01-10 00:00:00')
# central_point(logging[logging.cat==2].Log_after[0],logging[logging.cat==2].Log_before[0])
# 734
# get_date(734)
# Timestamp('2017-06-26 00:00:00', offset='D')

# NDVI time series
ts = read_ndvi(data)

# National Park reference data
national_park = read_nat_park(national_park_file)

cat=2
plotTimeSeries(cat, logging, ts, national_park, dest_folder)





#
