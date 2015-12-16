#coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function, division
from collections import OrderedDict

import pandas as pd
import tushare as ts
from bokeh.charts import Histogram, output_file, show

def set_default_encode(code='utf-8'):
        import sys
        reload(sys)
        sys.setdefaultencoding(code)
        print (sys.getdefaultencoding())
        print (sys.stdout.encoding)

set_default_encode()
sh = ts.get_hist_data('sh')
sz = ts.get_hist_data('sz')
zxb = ts.get_hist_data('zxb')
cyb = ts.get_hist_data('cyb')

df = pd.concat([sh['close'], sz['close'], zxb['close'], cyb['close']], \
        axis=1, keys=['sh', 'sz', 'zxb', 'cyb'])

fst_idx = -700
distributions = OrderedDict(sh=list(sh['close'][fst_idx:]), cyb=list(cyb['close'][fst_idx:]), sz=list(sz['close'][fst_idx:]), zxb=list(zxb['close'][fst_idx:]))
df = pd.DataFrame(distributions)

col_mapping = {'sh': u'沪指',
        'zxb': u'中小板',
        'cyb': u'创业版',
        'sz': u'深指'}
df.rename(columns=col_mapping, inplace=True)

print (df[:5])
output_file("histograms.html")
hist = Histogram(df, bins=50, density=False, legend="top_right")
show(hist)