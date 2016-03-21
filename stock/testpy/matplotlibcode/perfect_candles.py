import datetime

import matplotlib.pyplot as plt
import numpy as np
import tushare as ts
from matplotlib.dates import num2date, date2num
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle


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

def perfectCandles():
    def fooCandlestick(ax, quotes, width=0.5, colorup='k', colordown='r',
                       alpha=1.0):
        OFFSET = width / 2.0
        linewidth = width * 2
        print width
        lines = []
        boxes = []
        for q in quotes:
            # t, op, cl, hi, lo = q[:5]
            t, op, hi, lo, cl = q[:5]

            box_h = max(op, cl)
            box_l = min(op, cl)
            height = box_h - box_l

            if cl >= op:
                color = colorup
            else:
                color = colordown

            vline_lo = Line2D(
                xdata=(t, t), ydata=(lo, box_l),
                color=color,
                linewidth=linewidth,
                antialiased=True, )
            vline_hi = Line2D(
                xdata=(t, t), ydata=(box_h, hi),
                color=color,
                linewidth=linewidth,
                antialiased=True, )
            rect = Rectangle(
                xy=(t - OFFSET, box_l),
                width=width,
                height=height,
                facecolor=color,
                edgecolor=color, )
            rect.set_alpha(alpha)
            lines.append(vline_lo)
            lines.append(vline_hi)
            boxes.append(rect)
            ax.add_line(vline_lo)
            ax.add_line(vline_hi)
            ax.add_patch(rect)
        ax.autoscale_view()

        return lines, boxes

    bars = ts.get_hist_data('cyb', start="2015-01-01").sort_index(ascending=True)

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
    candlestickWidth = 0.5
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
    ax.set_xticklabels(new_xticks, rotation=30, horizontalalignment='right')
    # fig.autofmt_xdate()
    ax.autoscale_view()
    # ax.set_xticks(data2[ndays[1], 0])
    # ax.set_xticklabels(xdays, rotation=45, horizontalalignment='right')

    ax.set_ylabel('Quotes', size=10)
    # Set limits to the high and low of the data set
    # ax.set_ylim([min(data[:, 4]), max(data[:, 3])])

    # Create the candle sticks
    # candlestick_ohlc(ax, data2, width=candlestickWidth, colorup='r', colordown='g')
    fooCandlestick(ax, data2, width=candlestickWidth, colorup='r', colordown='g')
    plt.title('code' + " | " + str(bars.index[-1])[:11], fontsize=14)
    plt.legend(['code', str(bars.index[-1])[:11]], fontsize=12)
    plt.show()


def Candlestick(ax, bars=None, quotes=None, width=0.5, colorup='k', colordown='r', alpha=1.0):
    def fooCandlestick(ax, quotes, width=0.5, colorup='k', colordown='r',
                       alpha=1.0):
        OFFSET = width / 2.0
        linewidth = width * 2
        lines = []
        boxes = []
        for q in quotes:
            # t, op, cl, hi, lo = q[:5]
            t, op, hi, lo, cl = q[:5]

            box_h = max(op, cl)
            box_l = min(op, cl)
            height = box_h - box_l

            if cl >= op:
                color = colorup
            else:
                color = colordown

            vline_lo = Line2D(
                xdata=(t, t), ydata=(lo, box_l),
                color=color,
                linewidth=linewidth,
                antialiased=True, )
            vline_hi = Line2D(
                xdata=(t, t), ydata=(box_h, hi),
                color=color,
                linewidth=linewidth,
                antialiased=True, )
            rect = Rectangle(
                xy=(t - OFFSET, box_l),
                width=width,
                height=height,
                facecolor=color,
                edgecolor=color, )
            rect.set_alpha(alpha)
            lines.append(vline_lo)
            lines.append(vline_hi)
            boxes.append(rect)
            ax.add_line(vline_lo)
            ax.add_line(vline_hi)
            ax.add_patch(rect)
        ax.autoscale_view()

        return lines, boxes

    date = date2num(bars.index.to_datetime().to_pydatetime())
    openp = bars['open']
    closep = bars['close']
    highp = bars['high']
    lowp = bars['low']
    # volume = bars['volume']
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
    # creation of new data by replacing the time array with equally spaced values.
    # this will allow to remove the gap between the days, when plotting the data
    data2 = np.hstack([np.arange(data[:, 0].size)[:, np.newaxis], data[:, 1:]])
    # print data2
    # plot the data
    # figWidth = len(data) * width
    # fig = plt.figure(figsize=(figWidth, 5))
    # fig = plt.figure(figsize=(16, 10))
    # ax = fig.add_axes([0.05, 0.1, 0.9, 0.9])
    # customization of the axis

    '''
    #custom color
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(
        axis='both', direction='out', width=2, length=8, labelsize=12, pad=8)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    '''

    ax.grid(True, color='w')
    # ax.yaxis.label.set_color("w")
    # ax.spines['bottom'].set_color("#5998ff")
    # ax.spines['top'].set_color("#5998ff")
    # ax.spines['left'].set_color("#5998ff")
    # ax.spines['right'].set_color("#5998ff")
    # ax.tick_params(axis='y', colors='w')
    # import matplotlib.ticker as mticker
    # plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    # ax.tick_params(axis='x', colors='w')
    # plt.ylabel('Stock price and Volume')

    # set the ticks of the x axis only when starting a new day
    # (Also write the code to set a tick for every whole hour)
    div_n = len(ax.get_xticks())
    allc = len(bars.index)
    # lastd = bars.index[-1]
    if allc / div_n > 12:
        div_n = allc / 12
    ax.set_xticks(range(0, len(bars.index), div_n))
    new_xticks = [bars.index[d] for d in ax.get_xticks()]
    ax.set_xticklabels(new_xticks, rotation=30, horizontalalignment='right')
    # fig.autofmt_xdate()
    ax.autoscale_view()
    # Create the candle sticks
    fooCandlestick(ax, data2, width=width, colorup='r', colordown='g')


df = ts.get_hist_data('sh', start='2015-10-01').sort_index(ascending=True)
fig = plt.figure(figsize=(8, 5), facecolor='#07000d')
plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95, wspace=0.15, hspace=0.25)
ax = fig.add_subplot(111, axisbg='#07000d')
Candlestick(ax, df)
plt.show()
