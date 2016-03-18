from matplotlib import scale as mscale

from matplotlib import ticker as mticker
from matplotlib import transforms as mtransforms
from matplotlib.dates import num2date


class SegmentLocator(mticker.Locator):
    def __init__(self, x, gap, nbins=5):
        self.nbins = nbins
        self.x = x
        self.gap = gap
        self.segments = []
        for segment in np.split(x, np.where(np.diff(x) > self.gap)[0] + 1):
            self.segments.append((segment[0], segment[-1]))

    def __call__(self):
        loc = []
        for vmin, vmax in self.segments:
            nlocator = mticker.MaxNLocator(nbins=self.nbins)
            loc.append(nlocator.bin_boundaries(vmin, vmax))
        locs = np.concatenate(loc)
        return locs


class SegmentTransform(mtransforms.Transform):
    def __init__(self, x1, x2):
        mtransforms.Transform.__init__(self)
        self.x1 = x1
        self.x2 = x2

    def transform(self, a):
        return np.interp(a, self.x1, self.x2)

    def inverted(self):
        return SegmentTransform(self.x2, self.x1)


class SegmentScale(mscale.ScaleBase):
    name = "segment"

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self)
        self.x1 = kwargs["x"]
        self.gap = kwargs["gap"]
        self.x2 = np.zeros_like(self.x1)
        self.x2[1:] = np.diff(self.x1)
        np.clip(self.x2[1:], 0, self.gap, self.x2[1:])
        np.cumsum(self.x2, out=self.x2)

    def get_transform(self):
        return SegmentTransform(self.x1, self.x2)

    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(SegmentLocator(self.x1, self.gap))


def mscale_test():
    mscale.register_scale(SegmentScale)

    x = np.r_[np.arange(0, 10, 0.1), np.arange(
        50, 70, 0.1), np.arange(100, 120, 0.1)]
    y = np.sin(x)

    pos = np.where(np.abs(np.diff(x)) > 1.0)[0] + 1
    x2 = np.insert(x, pos, np.nan)
    y2 = np.insert(y, pos, np.nan)

    plt.plot(x2, y2)
    plt.xscale("segment", x=x, gap=2.0)
    plt.xlim(0, 120)
    ax = plt.gca()
    xlabels = ax.get_xticklabels()
    for label in xlabels:
        label.set_rotation(45)
    plt.show()


import numpy as np
import matplotlib.finance as finance
import matplotlib.pyplot as plt
# from querymongodb import Querymongodb
from matplotlib.dates import date2num
import tushare as ts

# conn = Querymongodb(db='stock', collection='indexes',
#                     code='000001',
#                     start='2015-10-1T0:0:0.000Z',
#                     end='2016-1-12T0:0:0.00Z')
# df = conn.get_df()
# df.index = df.date
# df.sort_index(ascending=True, inplace=True)
# df['date'] = df.date.map(date2num)
# df = df[['date', 'Open', 'High', 'Low', 'Close']]

df = ts.get_hist_data('sz', start='2016-01-01')
df.sort_index(ascending=True, inplace=True)
dates = df.index
df.index = df.index.to_datetime()
df['date'] = df.index.map(date2num)
df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
# [enter image description here][1]quotes:
# [(735879.0, 3156.075, 3172.281, 3133.127, 3143.357),
# (735880.0, 3146.644, 3192.717, 3137.788, 3183.152),
# (735883.0, 3193.54, 3318.714, 3188.407, 3287.662), ...]
quotes = map(tuple, df.values.tolist())

N = len(quotes)
ind = np.arange(N)


def format_date_date2num(x, pos=None):
    thisind = np.clip(int(x + 0.5), 0, N - 1)
    print x, pos, thisind, (df.index[thisind])
    if not num2date(x).strftime('%Y-%m-%d') in dates:
        print "empty date:%s" % (num2date(x).strftime('%Y-%m-%d'))
        # return ''
    # return df.index[thisind].strftime('%Y-%m-%d')
    # return(df.index[thisind]).strftime('%Y-%m-%d')
    return num2date(x).strftime('%Y-%m-%d')


def format_date(x, pos=None):
    print x, pos
    print dates[x]
    return dates[x]


fig, ax = plt.subplots()

finance.candlestick_ohlc(ax, quotes, width=0.6, colorup='g', colordown='r')
# ax.set_xticks(range(0, len(df) - 1))
# new_xticks = [dates[d] for d in ax.get_xticks()]
# ax.set_xticklabels(new_xticks, rotation=70)
# print ax.get_xticks()
ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_date_date2num))
fig.autofmt_xdate()

plt.grid(True)
plt.show()
