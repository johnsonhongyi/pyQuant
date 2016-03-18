import matplotlib

import matplotlib.pyplot as plt
import tushare as ts
from matplotlib.finance import candlestick2_ohlc

code = 'sz'
# r = ts.get_hist_data(code, start='2016-01-01')
r = ts.get_hist_data(code, start='2016-01-01')
r.sort_index(ascending=True, inplace=True)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_ylabel('Quote ($)', size=20)
candlestick2_ohlc(ax, r.open, r.high, r.low, r.close,
                  width=1, colorup='g', colordown='r')

pad = 0.25
yl = ax.get_ylim()
ax.set_ylim(yl[0] - (yl[1] - yl[0]) * pad, yl[1])
# ax.set_xlim(min(r.index),max(r.index))
# ax.set_xticks(range(0,len(r.index)))
# create the second axis for the volume bar-plot
# ax.xaxis_date()
# print ax.get_xticks()

# xt = ax.get_xticks()[:-1]
# new_xticks = [r.index[d] for d in xt]
# new_xticks.append(r.index[-1])
# ax.set_xticklabels(new_xticks,rotation=15, horizontalalignment='right')
div_n = len(ax.get_xticks())
print "t_x:", div_n, len(r) % div_n

ax.set_xticks(range(0, len(r.index), div_n))
new_xticks = [r.index[d] for d in ax.get_xticks()]
ax.set_xticklabels(new_xticks, rotation=30, horizontalalignment='center')
# ax.set_xticklabels([r.index[index] for index in ax.get_xticks()[::2]],rotation=30)

ax.autoscale_view()
plt.legend([code, r.index[-1]], fontsize=12)

ax2 = ax.twinx()
# print ax.get_xticks()
# set the position of ax2 so that it is short (y2=0.32) but otherwise the
# same size as ax
ax2.set_position(matplotlib.transforms.Bbox([[0.125, 0.1], [0.9, 0.32]]))
# ax2.fill_between(r.index,0, r.volume, facecolor='#00ffe8', alpha=.4)
# ax2.set_ylim(0, 1.5*r.volume.max())

# get data from candlesticks for a bar plot
# dates = date2num(r.index.to_datetime().to_pydatetime())
# dates = r.index
# volume = r.volume
# volume = np.asarray(volume)

# make bar plots and color differently depending on up/down for the day
pos = r[r['open'] < r['close']]
pos_idx = pos.index
# neg = r[r['open'] > r['close']]
# neg_idx = neg.index

# the y-ticks for the bar were too dense, keep only every third one
yticks = ax2.get_yticks()
# xlim = ax.get_xlim()
# print ax.get_xlims()
idx_a = []
idx_b = []
for i in range(0, len(r.index) - 1):
    if r.index[i] in pos_idx:
        idx_a.append(i)
    else:
        idx_b.append(i)
# print idx_a,idx_b
# ax.set_xticks(range(0,len(r.index)))
# ax.set_xticklabels([r.index[index] for index in ax.get_xticks()],rotation=30)
# print pos_idx
# print volume[pos_idx]
# ax2.bar(pos_idx,volume[pos_idx],color='green',width=1,align='center')
# ax2.bar(pos_idx,volume[pos_idx],color='green',width=1,align='center')
ax2.bar(idx_a, r.volume[idx_a], color='green', width=1, align='center')
ax2.bar(idx_b, r.volume[idx_b], color='red', width=1, align='center')

# ax2.set_yticks(yticks[::2])
ax2.yaxis.set_label_position("right")
ax2.set_ylabel('Volume', size=20)

# format the x-ticks with a human-readable date.
# plt.ion()
plt.show()
