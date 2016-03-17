# coding:utf-8
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, date2num
from matplotlib.finance import candlestick_ohlc

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# http://www.cnblogs.com/hhh5460/p/5120079.html

code = '600028'  # 600028 是"中国石化"的股票代码
# ticker += '.ss'   # .ss 表示上证 .sz表示深证
import tushare as ts

date1 = (2016, 1, 1)  # 起始日期，格式：(年，月，日)元组
date2 = (2016, 1, 19)  # 结束日期，格式：(年，月，日)元组

mondays = WeekdayLocator(MONDAY)  # 主要刻度
alldays = DayLocator()  # 次要刻度
# weekFormatter = DateFormatter('%b %d')     # 如：Jan 12
mondayFormatter = DateFormatter('%m-%d-%Y')  # 如：2-29-2015
dayFormatter = DateFormatter('%d')  # 如：12

# quotes = quotes_historical_yahoo_ohlc(ticker, date1, date2)
frame = ts.get_hist_data(
    code, start='2016-01-01', end='2016-01-19').sort_index(ascending=True)

quotes = zip(
    date2num(frame.index.to_datetime().to_pydatetime()),
    frame['open'],
    frame['close'],
    frame['high'],
    frame['low'],
    frame['volume'])
if len(quotes) == 0:
    raise SystemExit

N = len(quotes)
ind = np.arange(N)  # the evenly spaced plot indices


def format_date(x, pos=None):
    thisind = np.clip(int(x + 0.5), 0, N - 1)
    return (frame.index.to_datetime()[thisind]).strftime('%Y-%m-%d')


fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)

# ax.xaxis.set_major_locator(mondays)
# ax.xaxis.set_minor_locator(alldays)
# ax.xaxis.set_major_formatter(mondayFormatter)
# ax.xaxis.set_minor_formatter(dayFormatter)

# plot_day_summary(ax, quotes, ticksize=3)
candlestick_ohlc(ax, quotes, width=0.6, colorup='r', colordown='g')

ax.xaxis_date()
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
# ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.autofmt_xdate()

# next we'll write a custom formatter


fig, ax = plt.subplots()
print ind
ax.plot(ind, frame.close, 'o-')
# xt_labels = [frame.index[i] for i in ind]
# print xt_labels
# ax.set_xticklabels(xt_labels, rotation=15, horizontalalignment='right')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
# plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
fig.autofmt_xdate()

ax.grid(True)
plt.title(u'中国石化 600028')
plt.show()
