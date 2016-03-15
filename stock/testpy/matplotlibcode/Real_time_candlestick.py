#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo, candlestick,\
     plot_day_summary, candlestick2


# make plot interactive in order to update
plt.ion()

class Candleplot:
    def __init__(self):
        fig, self.ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)

    def update(self, quotes, clear=False):

        if clear:
            # clear old data
            self.ax.cla()

        # axis formatting
        self.ax.xaxis.set_major_locator(mondays)
        self.ax.xaxis.set_minor_locator(alldays)
        self.ax.xaxis.set_major_formatter(weekFormatter)

        # plot quotes
        candlestick(self.ax, quotes, width=0.6)

        # more formatting
        self.ax.xaxis_date()
        self.ax.autoscale_view()
        plt.setp( plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

        # use draw() instead of show() to update the same window
        plt.draw()


# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = ( 2004, 2, 1)
date2 = ( 2004, 4, 12 )
date3 = ( 2004, 5, 1 )

mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays    = DayLocator()              # minor ticks on the days
weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
dayFormatter = DateFormatter('%d')      # e.g., 12

quotes = quotes_historical_yahoo('INTC', date1, date2)

plot = Candleplot()
plot.update(quotes)

raw_input('Hit return to add new data to old plot')

new_quotes = quotes_historical_yahoo('INTC', date2, date3)

plot.update(new_quotes, clear=False)

raw_input('Hit return to replace old data with new')

plot.update(new_quotes, clear=True)

raw_input('Finished')

# Basically, I used plt.ion() to turn on interactive mode so that the plot can be updated while the program continues running. To update the data, there seem to be two options. (1) You can just call candlestick() again with the new data, which will add it to the plot without affecting the previously plotted data. This might be preferable for adding one or more new candles to the end; just pass a list containing the new candles. (2) Use ax.cla() (clear axis) to remove all the previous data before passing the new data. This would be preferable if you want a moving window, e.g. plot only the last 50 candles, since just adding new candles to the end will cause more and more candles to accumulate in the plot. Likewise if you want to update the last candle before it closes, you should clear the old data first. Clearing the axis will also clear some of the formatting, so functions should be set up to repeat the formatting of the axis after ax.cla() is called.