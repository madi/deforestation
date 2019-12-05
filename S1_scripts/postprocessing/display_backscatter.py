# coding: utf-8

'''
Example
python3 display_backscatter.py 50
where 50 is the category number
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import *
from scipy.signal import *
import sys

__author__ = "Margherita Di Leo"


# TODO: Modify the graph adding a new subplot to display like pol and 
# cross pol in the same figure

# TODO: Plot separate average for before and after logging date, as 
# horizontal line

#pol = "vv"
pol = "vh"

if pol == "vh":
    file_location = "/media/madi/TOSHIBA EXT/S1/output/files/backscatter_big_areas_cross3.csv"
    national_park = "/media/madi/TOSHIBA EXT/S1/output/files/national_park_cross.csv"
elif pol == "vv":
    file_location = "/media/madi/TOSHIBA EXT/S1/output/files/backscatter_big_areas_like2.csv"
    national_park = "/media/madi/TOSHIBA EXT/S1/output/files/national_park_like.csv"
else:
    print("Specify polarization")



# Categories are numbers that represent the logged areas in the dataset
# Category you want to display the backscatter signal for

#cat = 8
cat = int(sys.argv[1])

# Load and tidy up backscatter data of logged areas
data = pd.read_csv(file_location, header=None)

df = data.iloc[:,5:].transpose()
df = df.replace('*', np.nan)
new_df0 = []
for item in df[0]:
    stringa = item.split('_')
    year, month, day = stringa[-7],stringa[-6],stringa[-5]
    new_df0.append(year+"-"+month+"-"+day)
df[0] = pd.to_datetime(new_df0)
for i in range(df.shape[1]):
    df[i] = pd.to_numeric(df[i])
df[0] = pd.to_datetime(df[0]) 

#-----------------------------------------------------------------------

categories = pd.DataFrame([data[0],data[1],data[2],data[3],data[4]]).transpose()
headers = categories.iloc[0]
cats = pd.DataFrame(categories.values[1:], columns = headers)
del categories
del headers
cats = cats.set_index(cats.iloc[:,0])
cats['cat'] = pd.to_numeric(cats['cat'])
cats['log_ID'] = pd.to_numeric(cats['log_ID'])
cats['Log_after'] = pd.to_datetime(cats['Log_after'], format='%d.%m.%Y')
cats['Log_before'] = pd.to_datetime(cats['Log_before'], format='%d.%m.%Y')
cats['App_area_h'] = pd.to_numeric(cats['App_area_h'])

#-----------------------------------------------------------------------

df_headers = cats['cat']
headers=pd.concat([pd.Series(['date']), df_headers])
del df_headers
df.columns = headers

# Time series of backscatter values
ts = df.set_index(df.iloc[:,0])
del ts['date'] # duplicate column as is also index

#-----------------------------------------------------------------------

# Load backscatter data from National Park

data_np = pd.read_csv(national_park, skiprows=1, header=None, sep="|")
data_np = data_np.dropna(how='any', axis=0)

dates1 = []
for item in (data_np[1][:]):
    item2 = item.split(" ")
    year,month,day = item2[0].split('-')
    date = year+"-"+month+"-"+day
    dates1.append(date)

dates1 = pd.to_datetime(dates1)

# National Park Backscatter
npbs = pd.to_numeric(data_np[3])
npbs = npbs.replace('*', np.nan)
npbs = pd.DataFrame(npbs)
npbs.set_index(dates1)
npbs_r = npbs.rolling(10).median()

#-----------------------------------------------------------------------

# Backscatter Means of time series

bs_means = np.mean(ts, axis=1)
bs_means_r = bs_means.rolling(10).median()

# plot

series = ts[cat]
series = series.dropna(how = 'any', axis = 0)
series_r = series.rolling(10).median()
dates3 = series.index

fig=plt.figure(figsize=(16,4))
ax1=fig.add_subplot(111)
#ax1.plot(ts.index, bs_means_r, color='red')
ax1.set_xlabel('Date')
ax1.set_ylabel('$\overline{\gamma^o}$ [dB]')
ax1.plot(dates3, series_r, color='blue')
ax1.plot(dates1, npbs_r, color='green')

vline=cats['Log_after']['cat'==cat]
plt.axvline(x=vline, color='k', linestyle='--')

# fig.legend(['Average backscatter in logged area',
            # 'Backscatter signal in Cat %s' %(cat), 
            # 'Backscatter signal in National Park' ],loc=1)
fig.legend(['Backscatter signal in Cat %s' %(cat), 
            'Backscatter signal in National Park' ],loc=1)


lid=cats.log_ID[cat-1]
after=str(cats.Log_after[cat-1]).split( )[0]
before=str(cats.Log_before[cat-1]).split( )[0]
area=cats.App_area_h[cat-1]

plt.title('Site ID %.f of area %.2f Ha, \
           \n \
           logging activity registered after %s and before %s' %(
           lid, area, after, before) )

plt.show()

plt.close()




