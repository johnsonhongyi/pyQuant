# -*- coding: utf-8 -*-
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross,highlow
#from pyalgotrade import technical
#from pyalgotrade.technical import vwap
from pyalgotrade.stratanalyzer import sharpe
from pandas import DataFrame

from compiler.ast import flatten
import numpy as np
from pyalgotrade.broker.fillstrategy import DefaultStrategy
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade.technical import bollinger
import sys
sys.path.append("..")
from JSONData import tdx_data_Day as tdd
from JSONData import powerCompute as pct
class BBands(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, bBandsPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.0002))
        self.__position = None
        self.setUseAdjustedValues(False)
        self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 2)

    def getBollingerBands(self):
        return self.__bbands

    def onBars(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        if lower is None:
            return
#        if self.__position is not None:
#            if not self.__position.exitActive() and cross.cross_below(self.__ma1, self.__ma2) > 0:
#                self.__position.exitMarket()
#                self.info("sell %s" % (bars.getDateTime()))
#        
#        if self.__position is None:
#            if self.buyCon1() and self.buyCon2():
#                shares = int(self.getBroker().getCash() * 0.2 / bars[self.__instrument].getPrice())
#                self.__position = self.enterLong(self.__instrument, shares)
##                print bars[self.__instrument].getDateTime(), bars[self.__instrument].getPrice()
#                self.info("buy %s" % (bars.getDateTime()))
        shares = self.getBroker().getShares(self.__instrument)
        bar = bars[self.__instrument]
        if shares == 0 and bar.getClose() < lower:
#            sharesToBuy = int(self.getBroker().getCash(False) / bar.getClose())
            sharesToBuy = int(self.getBroker().getCash() * 0.2 / bars[self.__instrument].getPrice())
            self.__position = self.enterLong(self.__instrument, sharesToBuy)
            self.marketOrder(self.__instrument, sharesToBuy)
            self.info("A:%s BUY at ￥%.2f" % (self.getBroker().getEquity() , bar.getClose()))
        elif shares > 0 and bar.getClose() > upper:
            self.marketOrder(self.__instrument, -1*shares)
            self.info("A:%s BUY at ￥%.2f" % (self.getBroker().getEquity() , bar.getClose()))
            
class thrSMA_dayinfo(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, short_l, mid_l, long_l, up_cum):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.0002))
        self.__position = None
        self.setUseAdjustedValues(False)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__malength1 = int(short_l)
        self.__malength2 = int(mid_l)
        self.__malength3 = int(long_l)
        self.__circ = int(up_cum)
        
        self.__ma1 = ma.SMA(self.__prices, self.__malength1)
        self.__ma2 = ma.SMA(self.__prices, self.__malength2)
        self.__ma3 = ma.SMA(self.__prices, self.__malength3)
        
        self.__datetime = feed[instrument].getDateTimes()
        self.__open = feed[instrument].getOpenDataSeries()
        self.__high = feed[instrument].getHighDataSeries()
        self.__low = feed[instrument].getLowDataSeries()
        self.__close = feed[instrument].getCloseDataSeries()
        
    def getPrice(self):
        return self.__prices

    def getSMA(self):
        return self.__ma1,self.__ma2, self.__ma3

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOK(self):
        pass

    def onExitOk(self, position):
        self.__position = None
        #self.info("long close")

    def onExitCanceled(self, position):
        self.__position.exitMarket()
        
    def buyCon1(self):
        if cross.cross_above(self.__ma1, self.__ma2) > 0:
            return True

    def buyCon2(self):
        m1 = 0
        m2 = 0
        for i in range(self.__circ):
            if self.__ma1[-i-1] > self.__ma3[-i-1]:
                m1 += 1
            if self.__ma2[-i-1] > self.__ma3[-i-1]:
                m2 += 1

        if m1 >= self.__circ and m2 >= self.__circ:
            return True
    
    def sellCon1(self):
        if cross.cross_below(self.__ma1, self.__ma2) > 0:
            return True
            

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
#        self.dayInfo(bars[self.__instrument])
        
        if self.__ma2[-1]is None:
            return 
            
        if self.__position is not None:
            if not self.__position.exitActive() and cross.cross_below(self.__ma1, self.__ma2) > 0:
                self.__position.exitMarket()
                self.info("sell %s" % (bars.getDateTime()))
        
        if self.__position is None:
            if self.buyCon1() and self.buyCon2():
                shares = int(self.getBroker().getCash() * 0.2 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares)
#                print bars[self.__instrument].getDateTime(), bars[self.__instrument].getPrice()
                self.info("buy %s" % (bars.getDateTime()))
                
    def dayInfo(self, bar):
        try:
            self.__openD[-1]
        except AttributeError:
            self.__openD = []
            self.__highD = []
            self.__lowD = []
            self.__closeD = []
            self.__upper_limit = []
            self.__lower_limit = []
            
        if len(self.__datetime) < 2:
            self.__openD.append(bar.getOpen())
            self.__highD.append(self.__high[-1])
            self.__lowD.append(self.__low[-1])
            self.__closeD.append(self.__close[-1])                              
            return
            
        # if another day
        if self.__datetime[-1].date() != self.__datetime[-2].date():
            self.__openD.append(bar.getOpen())
            self.__highD.append(self.__high[-1])
            self.__lowD.append(self.__low[-1])
            self.__closeD.append(self.__close[-1]) 
            self.__upper_limit.append(round(round(self.__closeD[-2] * 1.1 * 1000) / 10) / 100)
            self.__lower_limit.append(round(round(self.__closeD[-2] * 0.9 * 1000) / 10) / 100) 
#            print self.__datetime[-1].date(), self.__datetime[-2].date(), self.__openD[-1]
                             
        elif self.__datetime[-1].date() == self.__datetime[-2].date():
            if self.__high[-1] > self.__highD[-1]:
                self.__highD[-1] = self.__high[-1]
            
            if self.__low[-1] < self.__lowD[-1]:
                self.__lowD[-1] = self.__low[-1]            
            self.__closeD[-1] = self.__close[-1]

class thrSMA(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, short_l, mid_l, long_l, up_cum):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.0002))
        self.__position = None
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__malength1 = int(short_l)
        self.__malength2 = int(mid_l)
        self.__malength3 = int(long_l)
        self.__circ = int(up_cum)
        
        self.__ma1 = ma.SMA(self.__prices, self.__malength1)
        self.__ma2 = ma.SMA(self.__prices, self.__malength2)
        self.__ma3 = ma.SMA(self.__prices, self.__malength3)
        
    def getPrice(self):
        return self.__prices

    def getSMA(self):
        return self.__ma1,self.__ma2, self.__ma3

    def onEnterCanceled(self, position):
        self.__position = None

    def onEnterOK(self):
        pass

    def onExitOk(self, position):
        self.__position = None
        #self.info("long close")

    def onExitCanceled(self, position):
        self.__position.exitMarket()
        
    def buyCon1(self):
        if cross.cross_above(self.__ma1, self.__ma2) > 0:
            return True

    def buyCon2(self):
        m1 = 0
        m2 = 0
        for i in range(self.__circ):
            if self.__ma1[-i-1] > self.__ma3[-i-1]:
                m1 += 1
            if self.__ma2[-i-1] > self.__ma3[-i-1]:
                m2 += 1

        if m1 >= self.__circ and m2 >= self.__circ:
            return True
    
    def sellCon1(self):
        if cross.cross_below(self.__ma1, self.__ma2) > 0:
            return True
            

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        
        if self.__ma2[-1]is None:
            return 
            
        if self.__position is not None:
            if not self.__position.exitActive() and cross.cross_below(self.__ma1, self.__ma2) > 0:
                self.__position.exitMarket()
                self.info("sell %s" % (bars.getDateTime()))
        
        if self.__position is None:
            if self.buyCon1() and self.buyCon2():
                shares = int(self.getBroker().getCash() * 0.2 / bars[self.__instrument].getPrice())
                self.__position = self.enterLong(self.__instrument, shares)
                print bars[self.__instrument].getDateTime(), bars[self.__instrument].getPrice()
                self.info("buy %s" % (bars.getDateTime()))
                
class turtle(strategy.BacktestingStrategy):
    def __init__(self,feed,instrument,N1,N2):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__feed = feed
        self.__position = None
        self.setUseAdjustedValues(False)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__high = highlow.High(self.__prices,N1,3)
        self.__low = highlow.Low(self.__prices,N2,3)
        self._count =0
        
        self.__info = DataFrame(columns={'date','id','action','instrument','quantity','price'})   #交易记录信息
        self.__info_matrix = []
   #手动增加日志信息，以获取数据，备网页显示,先单个交易的信息，多个交易暂时未写,从order中获取
    def addInfo(self,order):
        __date = order.getSubmitDateTime()  #时间
        __action = order.getAction()    #动作
        __id = order.getId()  #订单号
        __instrument = order.getInstrument()
        __quantity = order.getQuantity()  #数量
        __price = order.getAvgFillPrice()
        self.__info_matrix.append([__date,__id,__action,__instrument,__quantity,__price])
    
    #有多重实现方式和存储方式，考虑到组合数据，最终选用dataFrame且ID默认，因为或存在一日多单
    def getInfo(self):
        _matrix = np.array(self.__info_matrix).reshape((len(self.__info_matrix),6))
        return DataFrame({'date':_matrix[:,0],'id':_matrix[:,1],'action':_matrix[:,2],'instrument':_matrix[:,3],'quantity':_matrix[:,4],'price':_matrix[:,5]}) 
    #返回某一instrument的时间序列
    def getDateTimeSeries(self,instrument=None):   #海龟交易法和vwamp方法不一样，一个instrument为数组，一个为值
        if instrument is None:
            return self.__feed[self.__instrument].getPriceDataSeries().getDateTimes()
        return self.__feed[instrument].getPriceDataSeries().getDateTimes()
        
    def getHigh(self):
        return self.__high
        
    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at ￥%.2f" % (execInfo.getPrice()))
        self.addInfo(position.getEntryOrder())   #在此处添加信息
        
    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at ￥%.2f" % (execInfo.getPrice()))
        self.addInfo(position.getExitOrder())  #在此处添加信息
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        #若使用self__high[-1]这种值的话，不能是none,self.__high[0:0]为取前一日的  #也可以self.__high.__len__()！=3
            if self.__high.__len__() is not 3:   
                return
            bar = bars[self.__instrument]
            # If a position was not opened, check if we should enter a long position.
            #如果不设定high的长度为3的话，可能取不到-3的值
            if self.__position is None or not self.__position.isOpen() :  
                #判定今天价比昨日的最高价高，昨天价比前天的最高价低
                if self.__prices[-1]>self.__high[-2] and self.__prices[-2]<self.__high[-3]:
                    shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                    # Enter a buy market order. The order is good till canceled.
                    self.__position = self.enterLong(self.__instrument, shares, True)  #多种实现方式，为记录信息简要写于一处
                  
            # Check if we have to exit the position.
            elif not self.__position.exitActive() and self.__prices[-1]<self.__low[-2] and self.__prices[-2]>self.__low[-3]:
                self.__position.exitMarket()
              



from pyalgotrade import plotter
#import plotterK
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns,sharpe,drawdown,trades
from datetime import datetime
from matplotlib.pyplot import plot 
from compiler.ast import flatten
# import constant as ct
import pandas as pd 
import json
# import pyalg_utils
# import data,data_sql
from feedutil import dataFramefeed
import tushare as ts

        
def turtle_test(code,start=None):
#    dat = ts.get_h_data(code,start=start)
    dat = tdd.get_tdx_append_now_df_api('002648',start=start)
    dat.rename(columns={'vol': 'volume'}, inplace=True)
#    dat = dat.sort('date', ascending=False)
    feed = dataFramefeed.Feed()
    feed.addBarsFromDataFrame("orcl", dat)

    # Evaluate the strategy with the feed's bars.
    #myStrategy = pyalg_test.SMACrossOver(feed, "orcl", 20)
    pars=[2, 20, 60, 10]
#    myStrategy = thrSMA_dayinfo(feed, "orcl",*pars)
    myStrategy = BBands(feed, "orcl",20)
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy)
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())  
    
#    if dataString =='pyalg_util':
#        ds = pyalg_utils.dataSet(myStrategy)   #抽取交易数据集语句，若使用系统自带画图功能则不需要该项
    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())
    
#    if dataString =='pyalg_util':
#        rs = ds.getDefault()       #获取默认的交易信息，dic格式
#        plot(rs["cumulativeReturns"][:,0],rs["cumulativeReturns"][:,1])  #简单作图示例
     
    plt.plot()


if __name__ == '__main__':
    #vwap(True)
    code='000002'
    turtle_test(code,'2015-01-01')
