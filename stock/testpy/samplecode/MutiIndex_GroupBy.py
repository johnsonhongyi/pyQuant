#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-14 10:47:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import numpy as np
import pandas as pd
import datetime as DT
import datetime

# https://stackoverflow.com/questions/15799162/resampling-within-a-pandas-multiindex

def day8_to_day10(start,sep='-'):
    if start:
        start = str(start)
        if len(start) == 8:
            start = start[:4] + sep + start[4:6] + sep + start[6:]
            return start
    return start

def get_today(sep='-'):
    TODAY = datetime.date.today()
    fstr = "%Y" + sep + "%m" + sep + "%d"
    today = TODAY.strftime(fstr)
    return today


multiIndex_func={'close': 'min', 'low': 'min', 'volume': 'sum'}
def using_Grouper_eval(df, freq='5T', col='low', closed='right', label='right'):
    func ={}
    if isinstance(col, list):
        for k in col:
            if k in multiIndex_func.keys():
                func[k] = multiIndex_func[k]
    else:
        if col in multiIndex_func.keys():
            func[col] = multiIndex_func[col]
    print col,func
    level_values = df.index.get_level_values
    return eval("(df.groupby([level_values(i) for i in [0]]+[pd.Grouper(freq=freq, level=-1,closed='%s',label='%s')]).agg(%s))" % (closed, label, func))
    # return (df.groupby([level_values(i) for i in [0]] +[pd.Grouper(freq=freq, level=-1)]).agg({'low':'min','close':'mean','volume':'sum'}))

def get_date_range_freq():
    date_range = pd.date_range(start = '5/3/2005', periods =5+1, freq='1D')
    new_date_range = pd.date_range(date_range.min(), date_range.max(), freq='30 min')

def using_Grouper(df, freq='5T', col='low', closed='right', label='right'):
    func ={}
    if isinstance(col, list):
        for k in col:
            if k in multiIndex_func.keys():
                func[k] = multiIndex_func[k]
    else:
        if col in multiIndex_func.keys():
            func[col] = multiIndex_func[col]
    print col,func
    level_values = df.index.get_level_values
    return (df.groupby([level_values(i) for i in [0]] + [pd.Grouper(freq=freq, level=-1, closed=closed, label=label)]).agg(func))
    # +[pd.Grouper(freq=freq, level=-1)])['low','close','volume'].agg(['min','mean','sum']))
    # +[pd.Grouper(freq=freq, level=-1)]).mean())
    # .resample('30T', how={'low': 'min', 'close':'mean', 'volume': 'sum'}))

def select_multiIndex_index(df, index='ticktime', start=None, end=None, datev=None):
    if start is not None and len(start) < 10:
        if datev is None:
            start = get_today() + ' ' + start
        else:
            start = day8_to_day10(datev) + ' ' + start
        if end is None:
            end = start
    else:
        if end is None:
            end = start
    if end is not None and len(end) < 10:
        if datev is None:
            end = get_today() + ' ' + end
            if start is None:
                start = get_today(sep='-')+' '+'09:30:00'
        else:
            end = day8_to_day10(datev) + ' ' + end
            if start is None:
                start = day8_to_day10(datev)+' '+'09:30:00'
    else:
        if start is None:
            if end is None:
                start = get_today(sep='-')+' '+'09:30:00'
                end = get_today(sep='-')+' '+'09:45:00'
            else:
                start = end
    df = df[(df.index.get_level_values('ticktime') >= start) & (df.index.get_level_values('ticktime') <= end)]
    return df

import numpy as np
def maxdrawdown(arr):
    i = np.argmax((np.maximum.accumulate(arr) - arr)/np.maximum.accumulate(arr)) # end of the period
    j = np.argmax(arr[:i]) # start of period
    return (1-arr[i]/arr[j])

# pd.expanding_max(df.close,min_periods=10)
# pd.expanding_min(df.close,min_periods=10)

# def select_multiIndex_index(df, index='ticktime', start=None, end=None,datev=None):
#     if start is not None and len(start) < 10:
#         if datev is None:
#             start = get_today() + ' ' + start
#         else:
#             start = day8_to_day10(datev) + ' ' + start
#         if end is None:
#             end = start
#     else:
#         if end is None:
#             end = start
#     if end is not None and len(end) < 10:
#         if datev is None:
#             end = get_today() + ' ' + end
#             if start is None:
#                 start = get_today(sep='-')
#         else:
#             end = day8_to_day10(datev) + ' ' + end
#             if start is None:
#                 start = day8_to_day10(datev)
#     else:
#         if start is None:
#             start = end
#     df = df[(df.index.get_level_values('ticktime') >= start) & (df.index.get_level_values('ticktime') <= end)]
#     return df
    
    
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
tpp = '/Volumes/RamDisk/sina_MultiIndex_data.h5'
# tpp = '/Users/Johnson/Desktop/sina_MultiIndex_data-0717.h5'
time_s = time.time()
spp = pd.HDFStore(tpp)
df = spp.all_10.copy()
spp.close()
# print (df).loc['600999'][:10]
print "t0:%0.3f" % (time.time() - time_s)
# starttime = '2017-07-01 09:25:00'
# endtime = '2017-07-17 09:45:00'
# df = select_multiIndex_index(df, index='ticktime', end=endtime)
time_s = time.time()
# top_temp[:1][['high','nhigh','low','nlow','close','nclose','llastp']]

# df = select_multiIndex_index(df, index='ticktime', start='2017-07-01 09:25:00',end='2017-07-17 09:45:00')
df = select_multiIndex_index(df, index='ticktime', start=None,end=None)
dd = using_Grouper(df, freq='5T')
print "select1 count:%s :%0.3f" % (len(dd),time.time() - time_s)
# print select_multiIndex_index(dd, start=endtime)[:2]
print "sel:",df.loc['000002'][:2]
print "5t",dd.loc['000002'][:5]
print df.loc['000001'][:2]
time_s = time.time()
dz = df.groupby(level=[0]).min()
print "5t_t2:1count:%s :%0.2f" % (len(dz),time.time() - time_s)
print ".loc:",dz.loc['000001']
time_s = time.time()
df = using_Grouper_eval(df, freq='5T', col=['low','close'])
print "5t_t2 count:%s :%0.2f" % (len(df),time.time() - time_s)
print df.loc['000001'][:2]
time_s = time.time()
dd =  df.groupby(level=[0]).apply(lambda x: x[-1:])
print "last_t3 count:%s :%0.2f" % (len(dd),time.time() - time_s)
print dd[:4]


def using_reset_index(df):
    df = df.reset_index(level=[0, 1])
    return df.groupby(['State', 'City']).resample('2D').sum()


def using_stack(df):
    # http://stackoverflow.com/a/15813787/190597
    return (df.unstack(level=[0, 1])
              .resample('2D').sum()
              .stack(level=[2, 1])
              .swaplevel(2, 0))


def make_orig():
    values_a = range(16)
    values_b = range(10, 26)
    states = ['Georgia'] * 8 + ['Alabama'] * 8
    cities = ['Atlanta'] * 4 + ['Savanna'] * 4 + ['Mobile'] * 4 + ['Montgomery'] * 4
    dates = pd.DatetimeIndex([DT.date(2012, 1, 1) + DT.timedelta(days=i) for i in range(4)] * 4)
    df = pd.DataFrame(
        {'value_a': values_a, 'value_b': values_b},
        index=[states, cities, dates])
    df.index.names = ['State', 'City', 'Date']
    return df


def make_df(N):
    dates = pd.date_range('2000-1-1', periods=N)
    states = np.arange(50)
    cities = np.arange(10)
    index = pd.MultiIndex.from_product([states, cities, dates],
                                       names=['State', 'City', 'Date'])
    df = pd.DataFrame(np.random.randint(10, size=(len(index), 2)), index=index,
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
