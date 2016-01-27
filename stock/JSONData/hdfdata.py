# -*- coding:utf-8 -*-
import tushare as ts
import pandas as pd
# import pandas.io.pytables
code='601608'
df=ts.get_hist_data('601608')
store=pd.HDFStore('store.h5')
store[code]=df
print store