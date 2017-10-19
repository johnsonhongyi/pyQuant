import sys,logging
stdout=sys.stdout
sys.path.append('../../')
import JSONData.tdx_data_Day as tdd
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick
from matplotlib.finance import volume_overlay3
from matplotlib.dates import num2date
from matplotlib.dates import date2num
import matplotlib.mlab as mlab
import datetime



stock_code = '000002'
start = None
end= None
dl=60
df = tdd.get_tdx_append_now_df_api(code=stock_code, start=start, end=end, dl=dl).sort_index(ascending=True)
# print df.close.T
fig = plt.figure() 

# ax = fig.add_subplot(211, sharex=None, sharey=None) 
ax = fig.add_subplot(211) 
ax.plot(df.close)
ax.set_xticklabels(df.index)
plt.xticks(rotation=30, horizontalalignment='center')
# plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95, wspace=0.15, hspace=0.25)

pad = 0.25
yl = ax.get_ylim()
ax.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])
# ax2 = ax.twinx()
ax2 = fig.add_subplot(211,sharex=ax)
# ax2.set_position(matplotlib.transforms.Bbox([[0.125,0.1],[0.9,0.32]]))

# ax2.bar([x for x in range(len(df.index))],df.vol)
volume = np.asarray(df.vol)
pos = df['open']-df['close']<0
neg = df['open']-df['close']>=0
idx = df.reset_index().index
ax2.bar(idx[pos],volume[pos],color='red',width=1,align='center')
ax2.bar(idx[neg],volume[neg],color='green',width=1,align='center')
# plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95, wspace=0.15, hspace=0.25)

# ax2 = ax.twinx() 
# width = 0.4
# df.vol.plot(kind='bar', color='red', ax=ax, width=width, position=1, sharex=False, sharey=False)
# df.vol.plot(kind='bar', color='red', ax=ax, width=width, position=1)
# df.close.plot(kind='bar', color='blue', ax=ax2, width=width, position=0, sharex=False, sharey=False)

ax_2 = fig.add_subplot(212, sharex=ax, sharey=None) 
ax_22 = ax_2.twinx()
ax_2.plot([1, 3, 5, 7, 9])
ax_22.plot([1.0/x for x in [1, 3, 5, 7, 9]])
ax_2.set_xlabel("AX2 X Lablel")
ax_2.set_ylabel("AX2 Y Lablel")
ax_22.set_ylabel("AX2_Twin Y Lablel")

# ax_2 = fig.add_subplot(223, sharex=None, sharey=None) 
# ax_22 = ax_2.twinx()
# ax_2.plot([100, 300, 500, 700, 900])
# ax_22.plot([x*x for x in [100, 300, 500, 700, 900]])
# ax_2.set_xlabel("AX3 X Lablel")
# ax_2.set_ylabel("AX3 Y Lablel")
# ax_22.set_ylabel("AX3_Twin Y Lablel")

# ax_2 = fig.add_subplot(224, sharex=None, sharey=None) 
# ax_22 = ax_2.twinx()
# ax_2.set_xlabel("AX4 X Lablel")
# ax_2.set_ylabel("AX4 Y Lablel")
# ax_22.set_ylabel("AX4_Twin Y Lablel")

# ax.set_xlabel("Alphabets")
# ax.set_ylabel('Amount')
# ax2.set_ylabel('Price')

plt.subplots_adjust(wspace=0.8, hspace=0.8)
# plt.savefig("t1.png", dpi=300)
plt.show()


'''
show price and vol
datafile = 'data.csv'
r = mlab.csv2rec(datafile, delimiter=';')

# the dates in my example file-set are very sparse (and annoying) change the dates to be sequential
for i in range(len(r)-1):
    r['date'][i+1] = r['date'][i] + datetime.timedelta(days=1)

stock_code = '000002'
start = None
end= None
dl=60
df = tdd.get_tdx_append_now_df_api(code=stock_code, start=start, end=end, dl=dl).sort_index(ascending=True)
# r = r.reset_index()
date = df.index.to_datetime().to_pydatetime()
import pdb;pdb.set_trace();
candlesticks = zip(date2num(date),df['open'],df['high'],df['low'],df['close'],df['vol'])

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
pos = df['open']-df['close']<0
neg = df['open']-df['close']>0
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

# plt.ion()
plt.show()
'''