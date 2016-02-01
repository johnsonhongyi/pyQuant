# -*- coding:utf-8 -*-
import tushare as ts
import pandas as pd
import tables
#import pandas.io.pytables
code='601608'
df=ts.get_hist_data('601608')
# store=pd.HDFStore('store.h5',mode='w',format='table', complevel=9, complib='blosc')
df.index=df.index.astype('datetime64')
# store[code]=df
df.to_hdf('store.h5','sz'+code,mode='w',format='table', complevel=9, complib='blosc',data_columns=df.columns)
# store=pd.HDFStore('store.h5',mode='r',format='table')

h5f = tables.open_file('store.h5')
# dd=h5f.select('sz'+code)
print dd[:1]


import sys
sys.exit(0)

import tables
import tstables
import pandas.io.data as web
from datetime import *

# Create a class to describe the table structure. The column "timestamp" is required, and must be
# in the first position (pos=0) and have the type Int64.
class prices(tables.IsDescription):
    timestamp = tables.Int64Col(pos=0)
    open = tables.Float64Col(pos=1)
    high = tables.Float64Col(pos=2)
    close = tables.Float64Col(pos=3)

code='601608'    
f = tables.open_file('eurusd.h5','w', complevel=9, complib='blosc')

# This creates the time series, which is just a group called 'EURUSD' in the root of the HDF5 file.
ts = f.create_ts('/',code,prices)

start = datetime(2010,1,1)
end = datetime(2014,5,2)

# euro = web.DataReader("DEXUSEU", "fred", start, end)
euro = tss.get_hist_data(code).loc[:,['open','high','close']].sort_index(ascending=True).dropna()
euro.index=euro.index.astype('datetime64')
print euro[:1]
ts.append(euro)
f.flush() 

# Now, read in a month of data
read_start_dt = datetime(2014,1,1)
read_end_dt = datetime(2014,1,31)

jan = ts.read_range(read_start_dt,read_end_dt)