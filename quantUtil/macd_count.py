# -*- coding: utf-8 -*-
"""
@author: yucezhe
@contact: QQ:2089973054 email:xjc@yucezhe.com
"""
# %matplotlib inline
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
# ========== 从原始csv文件中导入股票数据，以浦发银行sh600000为例

# 导入数据 - 注意：这里请填写数据文件在您电脑中的路径
# stock_data = pd.read_csv('stock data/sh600000.csv', parse_dates=[1])
df=ts.get_hist_data('000030',start='2015-10-01',end ='2015-11-16')

# 将数据按照交易日期从远到近排
stock_data=df.sort_index(axis=0, by=None, ascending=True)
print (stock_data.head(5))
# inplace=True

# ========== 计算移动平均线

# 分别计算5日、20日、60日的移动平均线
ma_list = [5, 20, 60]

# 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
for ma in ma_list:
    stock_data['MA_' + str(ma)] = pd.rolling_mean(stock_data['close'], ma)
    stock_data['MA_' + str(ma)].plot()

# 计算指数平滑移动平均线EMA
for ma in ma_list:
    stock_data['EMA_' + str(ma)] = pd.ewma(stock_data['close'], span=ma)
    stock_data['EMA_' + str(ma)].plot()
# 将数据按照交易日期从近到远排序
# stock_data.sort('date', ascending=False, inplace=True)

# ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
# stock_data.to_csv('sh600000_ma_ema.csv', index=False)
# stock_data['']plot()
plt.xticks( rotation=-30, ha='right')
plt.show()