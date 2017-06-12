from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import DateFormatter
from matplotlib.finance import candlestick

# http://matplotlib.org/users/event_handling.html
# https://www.zhihu.com/question/27295034/answer/83433300

# set datafile separator ","
# everyNth(countColumn, labelColumnNum, N) = ( (int(column(countColumn)) % N == 0) ? stringcolumn(labelColumnNum) : "" ) 
# set xtics rotate 90
# plot "head.dat" using 0:2:4:3:5:xticlabels(everyNth(0, 1, 5)) notitle with candlesticks

class Chart3(object):
    def __init__(self, data, maxt=10):
        self.maxt = maxt
        self.data = data
        self.result = data[:self.maxt]

        # Parse the data columns
        self.tdata = [r[0] for r in self.result]
        self.sdata = [r[4] for r in self.result]
        self.mdata = [r[3] for r in self.result]

        # Initialize plot frame
        # xfmt = DateFormatter('%Y-%m-%d %H:%M')
        xfmt = DateFormatter('%Y-%m-%d')
        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(bottom=0.2)
        self.ax.xaxis.set_major_formatter(xfmt)
        self.ax.xaxis_date()
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='center')
        self.animate()

    def plot(self):
        if len(self.tdata) > self.maxt:  # roll the arrays
            self.tdata = self.tdata[-self.maxt:]
            self.sdata = self.sdata[-self.maxt:]
            self.mdata = self.mdata[-self.maxt:]
            self.result = self.result[-self.maxt:]

        # Plot the next set of line data
        line_min = Line2D(self.tdata, self.sdata, color='r')
        self.ax.add_line(line_min)
        line_max = Line2D(self.tdata, self.mdata, color='g')
        self.ax.add_line(line_max)

        # Plot the next set of candlestick data
        candlestick(self.ax, self.result, width=60 / 86400.0,  colorup='g', colordown='r')

        # Update the x-axis time date and limits
        if len(self.tdata) > 1:
            self.ax.set_xlim(self.tdata[0], self.tdata[-1])

        # Update the y-axis limits
        self.ax.set_ylim(min(self.sdata) * 0.99, max(self.mdata) * 1.01)

    def update_prices(self, cnt):
        """
        adds a data point from data to result list for plotting
        @return:
        """
        results = self.data[self.maxt + cnt]  # add another point of data
        t = (results[0])
        if self.tdata[-1] != t:
            trade = results
            self.result.append([t, trade[1], trade[2], trade[3], trade[4], trade[5], trade[6]])
            self.tdata.append(self.result[-1][0])
            self.sdata.append(self.result[-1][4])
            self.mdata.append(self.result[-1][3])

    def update_plot(self, i):
        try:
            self.update_prices(cnt=i)
            self.plot()
        except:
            pass

    def animate(self):
        # With try ... except in update_plot()
        # anim = animation.FuncAnimation(fig=self.fig, func=self.update_plot, interval=1000)

        # Without try ... except in update_plot()
        anim = animation.FuncAnimation(fig=self.fig, func=self.update_plot, interval=1000,
                                       frames=len(self.data)-self.maxt, repeat=False)
        plt.show()

if __name__ == "__main__":
    testData = [
        [735265.79166666663, 21.901, 21.901, 21.901, 21.901, 21.901, 0],
        [735265.79305555555, 21.901, 21.901, 21.901, 21.901, 21.901, 0],
        [735265.79236111115, 21.901, 21.901, 21.901, 21.901, 21.901, 0],
        [735265.79374999995, 21.9, 21.901, 21.901, 21.9, 21.9005, 11.65],
        [735265.79444444447, 21.901, 21.939, 21.939, 21.901, 21.91525, 23.23606],
        [735265.79513888888, 21.94, 21.95, 21.9703, 21.94, 21.953781250000002, 172.91374199999998],
        [735265.79583333328, 21.96, 21.99, 21.99, 21.96, 21.973333333333336, 142.974981],
        [735265.7965277778, 21.995, 21.995, 21.997, 21.995, 21.995533333333338, 36.541180000000004],
        [735265.7972222222, 21.9703, 21.995, 22.0, 21.9703, 21.993162500000004, 18.305711],
        [735265.79791666672, 21.9999, 21.86, 22.0, 21.86, 21.93492, 103.2468273],
        [735265.79861111112, 21.9045, 21.9045, 21.9045, 21.9045, 21.9045, 2.43879],
        [735265.79930555553, 21.929, 21.861, 21.99, 21.86, 21.92566666666666, 2.838343],
        [735265.80000000005, 21.9241, 21.899, 21.9241, 21.899, 21.907366666666665, 10.0],
        [735265.80069444445, 21.861, 21.86, 21.861, 21.86, 21.860888888888887, 111.367172],
        [735265.80138888885, 21.86, 21.861, 21.861, 21.86, 21.8604, 78.36582],
        [735265.80208333337, 21.861, 21.862, 21.862, 21.859, 21.860483333333335, 112.842532],
        [735265.80277777778, 21.862, 21.863, 21.88, 21.862, 21.8694, 83.64361899999999],
        [735265.80347222218, 21.88, 21.88, 21.88, 21.88, 21.88, 7.46027],
        [735265.8041666667, 21.88, 21.9256, 21.9256, 21.88, 21.9104, 7.06897],
        [735265.8048611111, 21.9256, 21.9256, 21.9256, 21.9256, 21.9256, 0.339032],
        [735265.8055555555, 21.9256, 21.9256, 21.9256, 21.9256, 21.9256, 2.024438],
        [735265.80625000002, 21.88, 21.88, 21.881, 21.88, 21.880249999999997, 25.00003],
        [735265.80694444443, 21.92, 21.92, 21.92, 21.92, 21.92, 0],
        [735265.80763888895, 21.92, 21.92, 21.92, 21.92, 21.92, 0],
        [735265.80833333335, 21.91, 21.92, 21.92, 21.91, 21.915, 80.0],
        [735265.80902777775, 21.881, 21.92, 21.92, 21.881, 21.907, 43.913890200000004],
        [735265.80972222227, 21.914, 22.0, 22.0, 21.914, 21.973115625, 368.000066],
        [735265.81041666667, 21.93, 21.93, 21.93, 21.93, 21.93, 0],
        [735265.81111111108, 21.9, 21.93, 21.93, 21.9, 21.9225, 15.475088999999999],
        [735265.8118055556, 21.93, 22.0, 22.0, 21.91, 21.97401, 56.620048589999996]
    ]

    chart = Chart3(data=testData)