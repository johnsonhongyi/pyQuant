from matplotlib.finance import *
from pylab import plt
import tushare as ts
r = ts.get_hist_data('601998').loc[:,['open','close','high','low','volume']]

https://pythonprogramming.net/?completed=/advanced-matplotlib-graphing-charting-tutorial/

'''
# ds, opens, closes, highs, lows, volumes = zip(*data)
ds, opens, closes, highs, lows, volumes = r.index.values,r['open'].values,r['close'].values,r['high'].values,r['low'].values,r['volume'].values
# print ds
# Create figure
fig = plt.figure()
ax1 = fig.add_subplot(111)
# Plot the candlestick
candles = candlestick2(ax1, opens, closes, highs, lows,
                       width=1, colorup='g')

# Add a seconds axis for the volume overlay
ax2 = ax1.twinx()

# Plot the volume overlay
bc = volume_overlay(ax2, opens, closes, volumes, colorup='g', alpha=0.5, width=1)
ax2.add_collection(bc)
plt.show()

import sys
sys.exit(0)
'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick
from matplotlib.finance import volume_overlay3
from matplotlib.dates import num2date
from matplotlib.dates import date2num
import matplotlib.mlab as mlab
import datetime

# datafile = 'data.csv'
# r = mlab.csv2rec(datafile, delimiter=';')
r = ts.get_hist_data('601998').loc[:,['open','close','high','low','volume']]
print r[:1]
# the dates in my example file-set are very sparse (and annoying) change the dates to be sequential
# for i in range(len(r)-1):
    # r['date'][i+1] = r['date'][i] + datetime.timedelta(days=1)

# candlesticks = zip(r.index.values,r['open'].values,r['close'].values,r['high'].values,r['low'].values,r['volume'].values)
candlesticks = r
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_ylabel('Quote ($)', size=20)
candlestick(ax, candlesticks,width=1,colorup='g', colordown='r')

# shift y-limits of the candlestick plot so that there is space at the bottom for the volume bar chart
pad = 0.25
yl = ax.get_ylim()
ax.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])

# create the second axis for the volume bar-plot
ax2 = ax.twinx()


# set the position of ax2 so that it is short (y2=0.32) but otherwise the same size as ax
ax2.set_position(matplotlib.transforms.Bbox([[0.125,0.1],[0.9,0.32]]))

# get data from candlesticks for a bar plot
dates = [x[0] for x in candlesticks]
dates = np.asarray(dates)
volume = [x[5] for x in candlesticks]
volume = np.asarray(volume)

# make bar plots and color differently depending on up/down for the day
pos = r['open']-r['close']<0
neg = r['open']-r['close']>0
ax2.bar(dates[pos],volume[pos],color='green',width=1,align='center')
ax2.bar(dates[neg],volume[neg],color='red',width=1,align='center')

#scale the x-axis tight
ax2.set_xlim(min(dates),max(dates))
# the y-ticks for the bar were too dense, keep only every third one
yticks = ax2.get_yticks()
ax2.set_yticks(yticks[::3])

ax2.yaxis.set_label_position("right")
ax2.set_ylabel('Volume', size=20)

# format the x-ticks with a human-readable date. 
xt = ax.get_xticks()
new_xticks = [datetime.date.isoformat(num2date(d)) for d in xt]
ax.set_xticklabels(new_xticks,rotation=45, horizontalalignment='right')

# plt.hold(True)
plt.ion()
plt.show()