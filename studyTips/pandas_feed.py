import datetime

from pandas.io import data

from pyalgotrade import strategy
from pyalgotrade import barfeed
from pyalgotrade import bar


# Example BarFeed for dataframes with data for a single instrument.
class DataFrameBarFeed(barfeed.BaseBarFeed):
    def __init__(self, dataframe, instrument, frequency):
        super(DataFrameBarFeed, self).__init__(frequency)
        self.registerInstrument(instrument)
        self.__df = dataframe
        self.__instrument = instrument
        self.__next = 0

    def reset(self):
        super(DataFrameBarFeed, self).reset()
        self.__next = 0

    def peekDateTime(self):
        return self.getCurrentDateTime()

    def getCurrentDateTime(self):
        ret = None
        if not self.eof():
            rowkey = self.__df.index[self.__next]
            ret = rowkey.to_datetime()
        return ret

    def barsHaveAdjClose(self):
        return True

    def getNextBars(self):
        ret = None
        if not self.eof():
            # Convert the dataframe row into a bar.BasicBar
            rowkey = self.__df.index[self.__next]
            row = self.__df.ix[rowkey]
            bar_dict = {
                self.__instrument: bar.BasicBar(
                    rowkey.to_datetime(),
                    row["Open".lower()],
                    row["High".lower()],
                    row["Low".lower()],
                    row["Close".lower()],
                    row["Volume".lower()],
                    # row["Adj Close".lower()],
                    row["Close".lower()],
                    self.getFrequency()
                )
            }
            ret = bar.Bars(bar_dict)
            self.__next += 1
        return ret

    def eof(self):
        return self.__next >= len(self.__df.index)

    def start(self):
        pass

    def stop(self):
        pass

    def join(self):
        pass

class MyStrategy(strategy.BacktestingStrategy):
    def onBars(self, bars):
        for instrument in bars.getInstruments():
            bar = bars[instrument]
            self.info("%s: %s %s %s %s %s %s" % (
                instrument,
                bar.getOpen(),
                bar.getHigh(),
                bar.getLow(),
                bar.getClose(),
                bar.getAdjClose(),
                bar.getVolume(),
            ))


def main():
    instrument = 'orcl'
    import tushare as ts
    # df = data.DataReader(instrument, 'yahoo', datetime.datetime(2011,1,1), datetime.datetime(2012,1,1))
    df = ts.get_hist_data('000001',start='2015-01-01').sort_index(ascending=True)
    df.index = df.index.to_datetime()
    # df.index = df.index.index.to_datetime().to_pydatetime()
    feed = DataFrameBarFeed(df, instrument, barfeed.Frequency.DAY)
    myStrategy = MyStrategy(feed)
    myStrategy.run()


if __name__ == "__main__":
    main()