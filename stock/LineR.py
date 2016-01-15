#-*- coding:utf-8 -*-
# 导入需要用到的库
# %matplotlib inline
from statsmodels import regression
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import math
from datetime import datetime as dt
from matplotlib.colors import LogNorm
from pylab import *
from mpl_toolkits.mplot3d.axes3d import Axes3D
import tushare as ts
from JohhnsonUtil import LoggerFactory as LoggerFactory
log = LoggerFactory.getLogger('LineR')
log.setLevel(LoggerFactory.DEBUG)
from JSONData import tdx_data_Day as tdd

# 取得股票的价格
# start = '2015-09-05'
# end = '2016-01-04'
start = '2015-06-05'
end = '2016-01-13'
code_n='002399'
asset = ts.get_hist_data(code_n)['close'].sort_index(ascending=True)
# asset = tdd.get_tdx_day_to_df(code_n)['close'].sort_index(ascending=True)
log.info("df:%s"%asset[:1])
asset = asset.dropna()
dates = asset.index

# 画出价格随时间变化的图像
_, ax = plt.subplots()

ax.plot(asset)
ticks = ax.get_xticks()
ax.set_xticklabels([dates[i] for i in ticks[:-1]]) # Label x-axis with dates

# 拟合
X = np.arange(len(asset))
x = sm.add_constant(X)
model = regression.linear_model.OLS(asset, x).fit()
a = model.params[0]
b = model.params[1]
log.info("a:%s b:%s"%(a,b))
print ("X:%s a:%s b:%s"%(len(asset),a,b))
Y_hat = X * b + a

#真实值-拟合值，差值最大最小作为价值波动区间
# 向下平移
i = (asset.values.T-Y_hat).argmin()
c_low = X[i] * b + a-asset.values[i]
Y_hatlow = X * b + a-c_low

# 向上平移
i = (asset.values.T-Y_hat).argmax()
c_high = X[i] * b + a-asset.values[i]
Y_hathigh = X * b + a-c_high

plt.plot(X, Y_hat, 'k', alpha=0.9);
plt.plot(X, Y_hatlow, 'r', alpha=0.9);
plt.plot(X, Y_hathigh, 'r', alpha=0.9);
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price',fontsize=18)
plt.title('Value center',fontsize=18)
plt.legend([code_n, 'Value center line','Value interval line']);



_, ax = plt.subplots(figsize = [18,8])
ax.plot(asset)
ticks = ax.get_xticks()
ax.set_xticklabels([dates[i] for i in ticks[:-1]])
#plt.plot(X, Y_hat, 'k', alpha=0.9)
n = 5
d = (-c_high+c_low)/n
c = c_high
while c<=c_low:
    Y = X * b + a-c
    plt.plot(X, Y, 'r', alpha=0.9);
    c = c+d
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price',fontsize=18)
plt.title('Value center quantile',fontsize=18)
plt.legend([code_n, 'Value center line','Quantile line'])



#将Y-Y_hat股价偏离中枢线的距离单画出一张图显示，对其边界线之间的区域进行均分，大于0的区间为高估，小于0的区间为低估，0为价值中枢线。
_, ax = plt.subplots(figsize = [18,8])
distance = (asset.values.T-Y_hat)
# distance = (asset.values.T-Y_hat)[0]
ax.plot(distance)
ticks = ax.get_xticks()
ax.set_xticklabels([dates[i] for i in ticks[:-1]])
n = 5
d = (-c_high+c_low)/n
c = c_high
while c<=c_low:
    Y = X * b + a-c
    plt.plot(X, Y-Y_hat, 'r', alpha=0.9);
    c = c+d
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price-center price',fontsize=18)
plt.title('Value center quantile',fontsize=18)
plt.legend([code_n, 'Value center line','Quantile line'])

#统计出每个区域内各股价的频数，得到直方图，为了更精细的显示各个区域的频数，这里将整个边界区间分成100份。

_, ax = plt.subplots(figsize = [18,8])
log.info("assert:len:%s %s"%(len(asset.values.T-Y_hat),(asset.values.T-Y_hat)[0]))
distance = (asset.values.T-Y_hat)
# distance = (asset.values.T-Y_hat)[0]
pd.Series(distance).plot(kind='hist', stacked=True, bins=100)
plt.xlabel('Undervalue ------------------------------------------> Overvalue',fontsize=18)
plt.ylabel('Frequency',fontsize=18)
plt.title('Undervalue & Overvalue Statistical Chart',fontsize=18)
# plt.legend(['300006.XSHE', 'Value center line','Quantile line'])
plt.show()