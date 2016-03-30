# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 11:12:36 2015

@author: Alex
"""

from pyalgotrade import strategy
from pyalgotrade import barfeed
from pyalgotrade import bar




# Example BarFeed for dataframes with data for a single instrument.
class DataFrameBarFeed(barfeed.BaseBarFeed):
    """
    Expects a pandas dataframe in the following format:
    Open, High, Low, Close in that order as float64
    datetime64[ns] as dataframe index,
    check dataframe with df.dtypes.
    """
    def __init__(self, dataframe, instrument, frequency):
        super(DataFrameBarFeed, self).__init__(frequency)
        self.registerInstrument(instrument)
        #make a list of lists containing all information for fast iteration
        self.__df = dataframe.values.tolist()
        self.__instrument = instrument
        self.__next = 0
        self.__len = len(self.__df)

    
    def setUseAdjustedValues(self, useAdjusted):
        #does this have a function? I still have to use adjusted closes below twice
        return False
    
    def reset(self):
        super(DataFrameBarFeed, self).reset()
        self.__next = 0

    def peekDateTime(self):
        return self.getCurrentDateTime()

    def getCurrentDateTime(self):
        if not self.eof():
            rowkey = self.__df[self.__next][5]
            #rowkey does not need to call todatetime, it should already be in that format
        return rowkey

    def barsHaveAdjClose(self):
        return False

    def getNextBars(self):
        ret = None
        if not self.eof():
            # Convert the list of lists into a bar.BasicBar
            # iteration through list of lists is 4x faster then using a dataframe because
            # a lot of functions get called every iteration
            bar_dict = {
                self.__instrument: bar.BasicBar(
                    self.__df[self.__next][5],
                    self.__df[self.__next][0],
                    self.__df[self.__next][1],
                    self.__df[self.__next][2],
                    self.__df[self.__next][3],
                    self.__df[self.__next][4],
                    #is there another class I can use besides BasicBar that does 
                    #not need an adjusted close(i.e. forex)?
                    #unused data will slow down the script
                    #dirty fix: use close as adjusted close
                    self.__df[self.__next][3],
                    self.getFrequency()
                )
            }
            ret = bar.Bars(bar_dict)
            self.__next += 1
        return ret

    def eof(self):
        #any particular reason to not get len() upon init? 
        #would prob. be faster for multiple requests, about -7ms
        return self.__next >= self.__len

    def start(self):
        pass

    def stop(self):
        pass

    def join(self):
        pass


class MyStrategy(strategy.BacktestingStrategy):
    def onBars(self, bars):
        self.count = 0
        for instrument in bars.getInstruments():
            bar = bars[instrument]
            self.count+=1
            #self.info("%s: %s %s %s %s %s %s" % (
            #    instrument,
            #    bar.getOpen(),
            #    bar.getHigh(),
            #    bar.getLow(),
            #    bar.getClose(),
            #    bar.getAdjClose(),
            #    bar.getVolume(),
            #))
            
            #Do something for the benchmark:
            datasum=bar.getOpen()+bar.getHigh()+bar.getLow()+bar.getClose()+bar.getVolume()

"""
Preparation:
read csv into pandas dataframe,
make a new row with the timestamp values,
feed it into pyalgotrade with DataFrameBarFeed.
It will automatically convert it to a list of lists and integrate it into pyalgotrade.
Needs to be done once, and can be used may times i.e. for the optimizer.

"""
from pandas import  read_csv
#pandas will, for most datetime formats, automatically recognize it from the first line, and use it as index
df = read_csv("tickstory_EURUSD_1 Min.csv", parse_dates=[0], infer_datetime_format=True, index_col=0)
#we need the index as a colum
df["Index"] = df.index
instrument = 'eurusd'
#Frequency.MINUTE does not work... and does NOT give back an error neither!
#Dirty fix: use DAY instead (may not work as intended)
feed = DataFrameBarFeed(df, instrument, barfeed.Frequency.DAY) 


def main():
    
    myStrategy = MyStrategy(feed)
    myStrategy.run()

if __name__ == "__main__":
    main()