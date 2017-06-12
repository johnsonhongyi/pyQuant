# -*- coding:utf-8 -*-
import tushare as ts
# import sys
# sys.path.append("..")
# from JohhnsonUtil import commonTips as cct

import pandas as pd
import tables
#import pandas.io.pytables
code='601608'
# df=get_kdate_data('601608')
df= ts.get_today_ticks('601608')
# .sort_index(ascending=True).dropna()
print df[:1]
store=pd.HDFStore('store.h5',mode='w',format='table', complevel=9, complib='blosc')
# df.index=df.index.astype('datetime64')
# store[code]=df
# df.to_hdf('store.h5','sz'+code,mode='w',format='table',complevel=9, complib='blosc',data_columns=df.columns)
# store=pd.HDFStore('store.h5',mode='r',format='table')

store.put('sz'+code,df)
# h5f = pd.HDFStore('store.h5',mode='r')
dd=store.select('sz'+code)
print dd[:5]


import sys
sys.exit(0)


#write
store=pd.HDFStore("./data/Minutes.h5","a", complevel=9, complib='zlib')
store.put("Year2015", dfMinutes, format="table", append=True, data_columns=['dt','code'])
# read
store=pd.HDFStore("./data/Minutes.h5","r")
store.select("Year2015", where=['dt<Timestamp("2015-01-07")','code=="000570"'])

df_tl.to_hdf('STORAGE2.h5','table',append=True,mode='w',data_columns=['A'])

pd.read_hdf('STORAGE2.h5','table',where='A>2')


'''
import tables
import tstables
import pandas.io.data as web
from datetime import *

# Create a class to describe the table structure. The column "timestamp" is required, and must be
# in the first position (pos=0) and have the type Int64.
class prices(tables.IsDescription):
    timestamp = tables.Int64Col(pos=0)
    price = tables.Float64Col(pos=1)
    # open = tables.Float64Col(pos=1)
    # high = tables.Float64Col(pos=2)
    # close = tables.Float64Col(pos=3)

code='601608'    
f = tables.open_file('tstable.h5','w', complevel=9, complib='blosc')

# This creates the time series, which is just a group called 'EURUSD' in the root of the HDF5 file.
tst = f.create_ts('/',code,prices)

# start = datetime(2010,1,1)
# end = datetime(2014,5,2)

# euro = web.DataReader("DEXUSEU", "fred", start, end)
# euro = get_kdate_data(code).loc[:,['open','high','close']].sort_index(ascending=True).dropna()
# df = get_kdate_data(code).loc[:,['open']].sort_index(ascending=True).dropna()
# print df[:1]
df = ts.get_today_ticks('601608').loc[:,['time','price']]
today=cct.get_today()
df['time']=df['time'].apply(lambda x:today+'-'+str(x))
df=df.set_index('time').sort_index(ascending=True).dropna()
print df[:1]
df.index=df.index.astype('datetime64')
tst.append(df)
f.flush() 

# Now, read in a month of data
# read_start_dt = datetime(2014,1,1)
# read_end_dt = datetime(2014,1,31)

# jan = ts.read_range(read_start_dt,read_end_dt)
'''