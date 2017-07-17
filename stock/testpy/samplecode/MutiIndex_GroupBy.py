#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-14 10:47:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import numpy as np
import pandas as pd
import datetime as DT


def using_Grouper_eval(df,freq='5T',col='low',func={'close':'min','low':'min','volume':'sum'}):
    level_values = df.index.get_level_values
    return eval("(df.groupby([level_values(i) for i in [0]]+[pd.Grouper(freq=freq, level=-1)]).agg(%s))"%(func))
    # return (df.groupby([level_values(i) for i in [0]] +[pd.Grouper(freq=freq, level=-1)]).agg({'low':'min','close':'mean','volume':'sum'}))

def using_Grouper(df,freq='5T'):
    level_values = df.index.get_level_values
    return (df.groupby([level_values(i) for i in [0]] +[pd.Grouper(freq=freq, level=-1)]).agg({'close':'mean','low':'min','volume':'sum'}))
                       # +[pd.Grouper(freq=freq, level=-1)])['low','close','volume'].agg(['min','mean','sum']))
                       # +[pd.Grouper(freq=freq, level=-1)]).mean())
    # .resample('30T', how={'low': 'min', 'close':'mean', 'volume': 'sum'}))

# https://stackoverflow.com/questions/23966152/how-to-create-a-group-id-based-on-5-minutes-interval-in-pandas-timeseries
# df.groupby(pd.TimeGrouper('5Min'))['val'].apply(lambda x: len(x) > 3)
#  df.groupby(pd.TimeGrouper('5Min'))['val'].mean()
# time
# 2014-04-03 16:00:00    14390.000000
# 2014-04-03 16:05:00    14394.333333
# 2014-04-03 16:10:00    14396.500000
# new = df.groupby(pd.TimeGrouper('5Min'),as_index=False).apply(lambda x: x['val'])
# >>> df['period'] = new.index.get_level_values(0)
# >>> df

#                      id    val  period
# time
# 2014-04-03 16:01:53  23  14389       0
# 2014-04-03 16:01:54  28  14391       0 
# 2014-04-03 16:05:55  24  14393       1
# 2014-04-03 16:06:25  23  14395       1
# 2014-04-03 16:07:01  23  14395       1
# 2014-04-03 16:10:09  23  14395       2
# 2014-04-03 16:10:23  26  14397       2
# 2014-04-03 16:10:57  26  14397       2
# 2014-04-03 16:11:10  26  14397       2
# 
# 
# Doctstring for TimeGrouper:

# Docstring for resample:class TimeGrouper@21

# TimeGrouper(self, freq = 'Min', closed = None, label = None,
# how = 'mean', nperiods = None, axis = 0, fill_method = None,
# limit = None, loffset = None, kind = None, convention = None, base = 0,
# **kwargs)

# Custom groupby class for time-interval grouping

# Parameters
# ----------
# freq : pandas date offset or offset alias for identifying bin edges
# closed : closed end of interval; left or right
# label : interval boundary to use for labeling; left or right
# nperiods : optional, integer
# convention : {'start', 'end', 'e', 's'}
#     If axis is PeriodIndex

# Notes
# -----
# Use begin, end, nperiods to generate intervals that cannot be derived
# directly from the associated object

import time
time_s=time.time()
tpp='/Volumes/RamDisk/sina_MultiIndex_data.h5'
spp=pd.HDFStore(tpp)
df=spp.all_10.copy()
spp.close()
# print (df).loc['600999'][:10]
print "t0:%0.3f"%(time.time()-time_s)
print using_Grouper(df, freq='15T').loc['600999']
print "t1:%0.3f"%(time.time()-time_s)
print using_Grouper_eval(df, freq='15T', col='low').loc['600999']
print "t2:%0.2f"%(time.time()-time_s)


def using_reset_index(df):
    df = df.reset_index(level=[0, 1])
    return df.groupby(['State','City']).resample('2D').sum()

def using_stack(df):
    # http://stackoverflow.com/a/15813787/190597
    return (df.unstack(level=[0,1])
              .resample('2D').sum()
              .stack(level=[2,1])
              .swaplevel(2,0))

def make_orig():
    values_a = range(16)
    values_b = range(10, 26)
    states = ['Georgia']*8 + ['Alabama']*8
    cities = ['Atlanta']*4 + ['Savanna']*4 + ['Mobile']*4 + ['Montgomery']*4
    dates = pd.DatetimeIndex([DT.date(2012,1,1)+DT.timedelta(days = i) for i in range(4)]*4)
    df = pd.DataFrame(
        {'value_a': values_a, 'value_b': values_b},
        index = [states, cities, dates])
    df.index.names = ['State', 'City', 'Date']
    return df

def make_df(N):
    dates = pd.date_range('2000-1-1', periods=N)
    states = np.arange(50)
    cities = np.arange(10)
    index = pd.MultiIndex.from_product([states, cities, dates], 
                                       names=['State', 'City', 'Date'])
    df = pd.DataFrame(np.random.randint(10, size=(len(index),2)), index=index,
                      columns=['value_a', 'value_b'])
    return df

# df = make_orig()
# print(using_Grouper(df))
# yields

#                                value_a  value_b
# State   City       Date                        
# Alabama Mobile     2012-01-01       17       37
#                    2012-01-03       21       41
#         Montgomery 2012-01-01       25       45
#                    2012-01-03       29       49
# Georgia Atlanta    2012-01-01        1       21
#                    2012-01-03        5       25
#         Savanna    2012-01-01        9       29
#                    2012-01-03       13       33
# Here is a benchmark comparing using_Grouper, using_reset_index, using_stack on a 5000-row DataFrame:

# In [30]: df = make_df(10)

# In [34]: len(df)
# Out[34]: 5000

# In [32]: %timeit using_Grouper(df)
# 100 loops, best of 3: 6.03 ms per loop

# In [33]: %timeit using_stack(df)
# 10 loops, best of 3: 22.3 ms per loop

# In [31]: %timeit using_reset_index(df)
# 1 loop, best of 3: 659 ms per loop
