# coding: utf-8

from __future__ import print_function
import pandas as pd
import numpy as np

__author__ = "Margherita Di Leo"


def read_logging(file_location):
    '''
    create dataframe with info about logging, such as logging date, cat, 
    log_ID and area
    '''
    data = pd.read_csv(file_location, header=None)
    logging = pd.DataFrame([data[0],data[1],data[2],data[3],data[4]]).transpose()
    # logging.head()
    # set the column label to equal the values in the first row (index location 0)
    headers = logging.iloc[0]
    log = pd.DataFrame(logging.values[1:], columns = headers)
    del logging
    del headers
    log = log.set_index(log.iloc[:,0])
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

def read_categories(file_location):
    '''
    create dataframe with info about logging, such as logging date, cat, 
    log_ID and area
    '''
    data = pd.read_csv(file_location, header=None)
    categories = pd.DataFrame([data[0],data[1],data[2],data[3],data[4]]).transpose()
    # set the column label to equal the values in the first row (index location 0)
    headers = categories.iloc[0]
    cats = pd.DataFrame(categories.values[1:], columns = headers)
    del categories
    del headers
    cats = cats.set_index(cats.iloc[:,0])
    cats['cat'] = pd.to_numeric(cats['cat'])
    return cats

#-----------------------------------------------------------------------
    
def read_ndvi(file_location):
    '''
    create time series of NDVI values for patches 
    '''
    data = pd.read_csv(file_location, header=None)
    df = data.iloc[:,5:].transpose()
    df = df.replace('*', np.nan)
    new_df0 = []
    for item in df[0]:
        stringa = item.split('_')
        year, month, day = stringa[-4],stringa[-3],stringa[-2]
        new_df0.append(year+"-"+month+"-"+day)
    df[0] = pd.to_datetime(new_df0)
    for i in range(df.shape[1]):
        df[i] = pd.to_numeric(df[i])
    df[0] = pd.to_datetime(df[0]) # I have to do it twice - first time 
    #is because otherwise it would give an error when transforming to numeric
    #df.info()
    #df.dtypes
    #df.describe()
    cats = read_categories(file_location)
    df_headers = cats['cat']
    headers=pd.concat([pd.Series(['date']), df_headers])
    del cats
    del df_headers
    df.columns = headers
    ts = df.set_index(df.iloc[:,0])
    del ts['date'] # duplicate column as is also index
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

#-----------------------------------------------------------------------

def read_deltas(deltas_file, file_location):
    '''
    Load deltas and index according to categories
    '''
    deltas = (pd.read_csv(deltas_file, header=None)).T
    deltas[0] = pd.to_datetime(deltas[0])
    for i in range(deltas.shape[1]):
        deltas[i] = pd.to_numeric(deltas[i])
    deltas[0] = pd.to_datetime(deltas[0])
    deltas=deltas.set_index(deltas[0])
    del deltas[0]
    #deltas.info()
    #deltas.dtypes
    #deltas.describe()
    logging = read_logging(file_location)
    deltas_headers = logging['cat']
    del logging
    deltas.columns = deltas_headers
    del deltas_headers
    return deltas

#-----------------------------------------------------------------------

def read_valid(file_location, cat):
    '''
    Read validation data
    '''
    data = pd.read_csv(file_location, header=None, low_memory=False)
    df = data.iloc[:,6:].transpose()
    df = df.replace('*', np.nan)
    new_df0 = []
    for item in df[0]:
        stringa = item.split('_')
        year, month, day = stringa[-4],stringa[-3],stringa[-2]
        new_df0.append(year+"-"+month+"-"+day)
    dates = pd.to_datetime(new_df0)
    series = pd.to_numeric(df[cat])
    cats = data[0]
    ts = pd.Series(series.values, index=dates)
    return ts
