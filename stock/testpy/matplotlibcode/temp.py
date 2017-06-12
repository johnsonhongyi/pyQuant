import datetime

import matplotlib.pyplot as plt
import numpy as np
import tushare as ts
from matplotlib.dates import num2date, date2num
from matplotlib.finance import candlestick_ohlc

# Create sample data for 5 days. Five columns: time, opening, close, high, low
# jaar = 2007
# maand = 05
# data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
# quotes = [(5, 6, 7, 4), (6, 9, 9, 6), (9, 8, 10, 8),
#           (8, 6, 9, 5), (8, 11, 13, 7)]

# for dag in range(5, 7):
#     for uur in range(9, 10):
#         for minuut in range(15):
#             numdatumtijd = date2num(
#                 datetime.datetime(jaar, maand, dag, uur, minuut))
#             koersdata = quotes[random.randint(0, 4)]
#             data = np.append(data, [
#                              [numdatumtijd, koersdata[0], koersdata[1], koersdata[2], koersdata[3], ]], axis=0)

# print len(data)
# data = np.delete(data, 0, 0)
# print len(data)
# print('Ready with building sample data')

# ax = plt.subplot(1,1,1)
# p1, = ax.plot([1,3], label="line 1")
# p2, = ax.plot([3,2,1], label="line 2")
# p3, = ax.plot([2,3,1], label="line 3")


bars = ts.get_hist_data('sh', start="2015-01-01").sort_index(ascending=True)

date = date2num(bars.index.to_datetime().to_pydatetime())
openp = bars['open']
closep = bars['close']
highp = bars['high']
lowp = bars['low']
volume = bars['volume']
data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
for i in range(len(bars) - 1):
    data = np.append(
        data, [[date[i], openp[i], highp[i], lowp[i], closep[i], ]], axis=0)
data = np.delete(data, 0, 0)
# determine number of days and create a list of those days
# print np.unique(np.trunc(data[:, 0]))
ndays = np.unique(np.trunc(data[:, 0]), return_index=True)
xdays = []
for n in np.arange(len(ndays[0])):
    xdays.append(datetime.date.isoformat(num2date(data[ndays[1], 0][n])))
# print ndays, xdays
# creation of new data by replacing the time array with equally spaced values.
# this will allow to remove the gap between the days, when plotting the data
data2 = np.hstack([np.arange(data[:, 0].size)[:, np.newaxis], data[:, 1:]])
# print data2
# plot the data
candlestickWidth = 1
figWidth = len(data) * candlestickWidth
# fig = plt.figure(figsize=(figWidth, 5))
fig = plt.figure(figsize=(16, 10))
ax = fig.add_axes([0.05, 0.1, 0.9, 0.9])
# customization of the axis

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.tick_params(
    axis='both', direction='out', width=2, length=8, labelsize=12, pad=8)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)

# set the ticks of the x axis only when starting a new day
# (Also write the code to set a tick for every whole hour)
div_n = len(ax.get_xticks())
allc = len(bars.index)
lastd = bars.index[-1]
# print "t_x:", div_n, len(bars) % div_n, len(bars), ax.get_xticks()
if allc / div_n > 20:
    div_n = allc / 20
ax.set_xticks(range(0, len(bars.index), div_n))
new_xticks = [bars.index[d] for d in ax.get_xticks()]
# if not lastd in new_xticks:
#     print "lst"
#     new_xticks.append(lastd)
# print new_xticks
ax.set_xticklabels(new_xticks, rotation=30, horizontalalignment='center')
fig.autofmt_xdate()
# ax.set_xticks(data2[ndays[1], 0])
# ax.set_xticklabels(xdays, rotation=45, horizontalalignment='right')

ax.set_ylabel('Quotes', size=10)
# Set limits to the high and low of the data set
# ax.set_ylim([min(data[:, 4]), max(data[:, 3])])
# p1,=ax.plot([5,3000], [8,4000],'k',label="line 1")
# Create the candle sticks
candlestick_ohlc(ax, data2, width=candlestickWidth, colorup='r', colordown='g')
plt.title('code' + " | " + str(bars.index[-1])[:11], fontsize=14)
plt.legend(['code', str(bars.index[-1])[:11]], fontsize=12)
# ax = plt.subplot(1,1,1)


plt.show()
