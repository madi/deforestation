# coding: utf-8

# DEPRECATED

__author__ = "Margherita Di Leo"

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
#import argparse

#parser = argparse.ArgumentParser(description = "Plots NDVI time series \
                                 #for a given cat number ")
#parser.add_argument("--cat", dest = "cat",
                                 #help = "category number (cat). Note that \
                                 #cat differs from log_ID - check lookup table")
#args = parser.parse_args()

#cat = int(args.cat)

######### Change paths according to locations in your machine ##########
file_location = '/home/leomarg/ndvi_big_areas.csv'
logging_file='/home/leomarg/logging_points.csv'
national_park_file='/home/leomarg/national_park_wo_loss_scl_NDVI.csv'
########################################################################

data = pd.read_csv(file_location, header=None)

del data[4]
del data[3]
del data[2]
del data[1]
del data[0]

df = data.transpose()
#df.head()
#df.info()

df = df.replace('*', np.nan)

new_df0 = []
for item in df[0]:
    year, month, day = [e for n, e in enumerate(item.split('_')) if n in (4, 5, 6)]
    new_df0.append(year+"-"+month+"-"+day)

df[0] = pd.to_datetime(new_df0)

for i in range(df.shape[1]):
    df[i] = pd.to_numeric(df[i])
    
df[0] = pd.to_datetime(df[0]) # yes I have to do it twice - first time 
#is because otherwise it would give an error when transforming to numeric

#df.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 31 entries, 0 to 30
Columns: 443 entries, 0 to 442
dtypes: datetime64[ns](1), float64(442)
memory usage: 107.5 KB
'''
#df.dtypes

#df.describe()
'''
             1          2          3          4          5          6    \
count  29.000000  30.000000  30.000000  29.000000  30.000000  28.000000   
mean    0.729802   0.752629   0.725683   0.727035   0.667920   0.662057   
std     0.160298   0.157551   0.184334   0.130105   0.080612   0.076364   
min     0.388105   0.355681   0.142499   0.346999   0.457691   0.386338   
25%     0.662404   0.728096   0.661661   0.681395   0.619931   0.648854   
50%     0.767619   0.815156   0.807728   0.765910   0.671833   0.675417   
75%     0.850955   0.857363   0.843864   0.820392   0.720106   0.712065   
max     0.890762   0.900370   0.873969   0.866324   0.817232   0.755102   

             7          8          9          10     ...            433  \
count  30.000000  29.000000  30.000000  30.000000    ...      29.000000   
mean    0.678781   0.531065   0.695885   0.695025    ...       0.788623   
std     0.101475   0.098649   0.118679   0.082228    ...       0.153196   
min     0.409751   0.299973   0.374224   0.465839    ...       0.333522   
25%     0.649557   0.481149   0.681105   0.640243    ...       0.790489   
50%     0.704813   0.566589   0.723502   0.705248    ...       0.850254   
75%     0.741177   0.586174   0.766979   0.747862    ...       0.887943   
max     0.825378   0.746879   0.837646   0.836991    ...       0.908193   

             434        435        436        437        438        439  \
count  29.000000  29.000000  27.000000  29.000000  29.000000  30.000000   
mean    0.723911   0.747818   0.746130   0.610972   0.682073   0.716137   
std     0.124788   0.140752   0.167468   0.133906   0.169562   0.142030   
min     0.403098   0.399691   0.267570   0.324641   0.098232   0.376185   
25%     0.689113   0.677120   0.677138   0.558348   0.604672   0.653489   
50%     0.771552   0.790534   0.794987   0.651652   0.727168   0.788998   
75%     0.813065   0.856344   0.870512   0.708745   0.806431   0.816925   
max     0.849430   0.891586   0.895565   0.774677   0.854441   0.844290   

             440        441        442  
count  30.000000  30.000000  30.000000  
mean    0.604705   0.536874   0.644650  
std     0.121421   0.120148   0.190737  
min     0.193592   0.218661   0.036645  
25%     0.578194   0.495712   0.617358  
50%     0.621857   0.564937   0.721960  
75%     0.682272   0.602336   0.753719  
max     0.752747   0.741667   0.815418  
'''

# create time series indexing by date
ts = df.set_index(df.ix[:,0])
#ts.index


# Adding vertical line to plot
logging = pd.read_csv(logging_file, header=0)

#logging.head()
'''
 cat  log_ID   Log_after  Log_before
0    1     342  10.01.2018  08.05.2018
1    2     342  10.01.2018  08.05.2018
2    3     343  10.01.2018  08.05.2018
3    4     344  10.01.2018  08.05.2018
4    5     345  10.01.2018  08.05.2018
'''

# indexing by cat (pivot)
log=logging.set_index('cat')

#log.head()
'''
     log_ID   Log_after  Log_before
cat                                
1       342  10.01.2018  08.05.2018
2       342  10.01.2018  08.05.2018
3       343  10.01.2018  08.05.2018
4       344  10.01.2018  08.05.2018
5       345  10.01.2018  08.05.2018
'''

# convert dates to datetime
log['Log_after'] = pd.to_datetime(log['Log_after'])
log['Log_before'] = pd.to_datetime(log['Log_before'])

#log.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 442 entries, 1 to 442
Data columns (total 3 columns):
log_ID        442 non-null int64
Log_after     442 non-null datetime64[ns]
Log_before    442 non-null datetime64[ns]
dtypes: datetime64[ns](2), int64(1)
memory usage: 13.8 KB
'''

national_park = pd.read_csv(national_park_file, header=0, sep='|')
national_park['start'] = pd.to_datetime(national_park['start'])
national_park=national_park.set_index('start')

# TODO: insert loop over cat
for item in log.index:
    cat = item

    log_ID = log['log_ID'][cat]

    vline1 = log['Log_after'][cat]
    vline2 = log['Log_before'][cat]

    plt.figure()
    plt.plot(ts[cat], marker='o', color='blue')
    plt.plot(national_park, marker='o', color='green', \
    label='National Park average NDVI')
    plt.legend()


    xposition = [vline1, vline2]
    for xc in xposition:
        plt.axvline(x=xc, color='k', linestyle='--')

    plt.grid(True)
    plt.title("NDVI time series for log ID %s (cat %s)" %(log_ID,cat))
    plt.show() 
    #plt.savefig("NDVI time series for log ID %s (cat %s)" %(log_ID,cat))



