# -*- coding: utf-8 -*-
from __future__ import print_function, division
from __future__ import unicode_literals
from collections import OrderedDict

import numpy as np
import pandas as pd
import datetime as dt
import seaborn as sns

import tushare as ts
from bokeh.charts import Bar, output_file, show

cls = ts.get_industry_classified()
stk = ts.get_stock_basics()
cls = cls.set_index('code')

tcls = cls[['c_name']]
tstk = stk[['pe', 'pb', 'esp', 'bvps']]

df = tcls.join(tstk, how='inner')
clist = [df.ix[i]['c_name'] for i in xrange(3)]

def neq(a, b, eps=1e-6):
    return abs(a - b) > eps

tdf = df.loc[df['c_name'].isin(clist) & neq(df['pe'], 0.0) & \
        neq(df['pb'], 0.0) & neq(df['esp'], 0.0) & \
        neq(df['bvps'], 0.0)]

col_mapping = {'pe' : u'P/E',
        'pb' : u'P/BV',
        'esp' : u'EPS',
        'bvps' : u'BVPS'}
tdf.rename(columns=col_mapping, inplace=True)

sns.pairplot(tdf, hue='c_name', size=2.5)