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
import powerTech as ptc

class BBands(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, bBandsPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.getBroker().setFillStrategy(DefaultStrategy(None))
        self.getBroker().setCommission(TradePercentage(0.0002))
        self.__position = None
        self.bBandsPeriod = bBandsPeriod
#        self.setUseAdjustedValues(False)
        self.close = feed[instrument].getCloseDataSeries()
        self.open = feed[instrument].getOpenDataSeries()
        self.high = feed[instrument].getHighDataSeries()
        self.low = feed[instrument].getLowDataSeries()
        self.datetime = feed[instrument].getDateTimes()
        self.volume = feed[instrument].getVolumeDataSeries()
        self.feed = feed.get_dataFrame()
        # self.__bollinger = bollinger.BollingerBands(self.__close, self.bBandsPeriod,2)
        # self.__UpperBand = self.__bollinger.getUpperBand()
        # self.__LowerBand = self.__bollinger.getLowerBand()
        # self.feed = feed[instrument].getCloseDataSeries()
#        self.bar = feed[instrument].getClose()
        self.op = []
        self.ra = []
        self.boll = []
        self.macd = []
        self.rsi = []
        self.kdj = []
        self.rsi = []
        self.ma = []
    def getBollingerBands(self):
        return self.__bbands

    def getFeed(self,dt=None):
        df = self.feed
        dd = df[df.index <= str(dt)]
        # print "df:%s dt:%s"%(len(dd),dt)
        return dd
    def get_max_min(self):
        self.info("op:%s %s :%s"%(max(self.op),min(self.op), list(set(self.op))))
        self.info("ra:%s %s :%s"%(max(self.ra),min(self.ra),list(set(self.ra))))
        self.info("boll:%s %s :%s"%(max(self.boll),min(self.boll),list(set(self.boll))))
        self.info("kdj:%s %s :%s"%(max(self.kdj),min(self.kdj),list(set(self.kdj))))
        self.info("macd:%s %s :%s"%(max(self.macd),min(self.macd),list(set(self.macd))))
        self.info("ma:%s %s :%s"%(max(self.ma),min(self.ma),list(set(self.ma))))
    # def getclose(self):
    #     return self.feed[-1]

    def buyCon1(self):
        #        if cross.cross_above(self.__ma1, self.__ma2) > 0:
        #        if self.bar[-1]  > self.upper:
        #            return True
        #         df,op=getab.Get_BBANDS(self.getFeed(self.__datetime[-1]))
        #         self.oplist.append(op)
        #         if op > 6:
        #             return True
        #         elif op > 20:
        #             return False
        #         elif op < 0:
        #             return False
        #         else:
        #             return True
        op,ra,fib,fibl,ldate,boll,kdj,macd,rsi,ma = ptc.get_power_status(self.__instrument,
                                                                         self.getFeed(self.datetime[-1]),dl=30)
        print ("op:%s ra:%0.2f ma:%s macd:%s rsi:%s kdj:%s boll:%s close:%s dt:%s ld:%s"%(op,ra,ma,macd,rsi,kdj,boll,self.close[-1],str(self.datetime[-1])[:10],ldate))
        self.op.append(op)
        self.ra.append(ra)
        self.boll.append(boll)
        self.kdj.append(kdj)
        self.macd.append(macd)
        self.ma.append(ma)
        self.rsi.append(rsi)
        buyC2 = self.buyCon2()
        if buyC2 == 1:
            # print op,ra,fib,fibl,ldate,boll,kdj,macd,rsi,ma,str(self.__datetime[-1])[:10]
            # if fib < 3:
            # if ma > 0 and macd > -2 and rsi > 0 and kdj > 0 :
            # if ma > 0 and macd > -2  :
            if op > 0 :
                self.info("boll:%s ra:%s rsi:%s kdj:%s ldate:%s"%(boll,ra,rsi,kdj,ldate))
                return 1
            # return 1
                # else:
                #     print fib
                # if ma > 0 and macd <-10 and rsi > 0 and kdj > 0 and boll > 6:
                #     return True
        elif buyC2 == 0:
            # if kdj < 0 and ma < 0 and rsi < 0 and boll < 16:
            return 0
        else:
            return 2

    def buyCon2(self):
        lastp = self.close[-2]
        lasto = self.open[-2]
        lasth = self.high[-2]
        lastl = self.low[-2]
        nowp = self.close[-1]
        nowo = self.open[-1]
        nowh = self.high[-1]
        nowl = self.low[-1]
        print nowp,nowo,nowh,nowl
        if nowp == nowo and nowh == nowl:
            return 2

        if self.ra[-1] > 0 and nowh >= lasth * 0.99:
            # if nowo > lastp and nowh > lasth:
            self.info("buy")
            return 1
        else:
            # if nowo < lastp and nowh < lasth:
            if len(self.kdj) > 1 and (self.kdj[-2] >0 and self.kdj[-1] < 0) and nowo < lastp and nowh < lasth and nowp < lastp:
                self.info("sell")
                return 0
        return 2
#        if self.bar[-1] < self.middle:
#            return True
#        m1 = 0
#        m2 = 0
#        for i in range(self.__circ):
#            if self.__ma1[-i-1] > self.__ma3[-i-1]:
#                m1 += 1
#            if self.__ma2[-i-1] > self.__ma3[-i-1]:
#                m2 += 1
#
#        if m1 >= self.__circ and m2 >= self.__circ:
#            return True

    def sellCon1(self):
        if cross.cross_below(self.__ma1, self.__ma2) > 0:
            return True

    def onBars(self, bars):
#        lower = self.__bbands.getLowerBand()[-1]
#        upper = self.__bbands.getUpperBand()[-1]
#        if lower is None:
#            return
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
        closeDs = self.close
        from pyalgotrade.talibext import indicator
#        self.upper, self.middle, self.lower = indicator.BBANDS(closeDs, self.bBandsPeriod,timeperiod=2)
        import talib as ta
        self.upper, self.middle, self.lower=ta.BBANDS(np.array(closeDs),timeperiod=self.bBandsPeriod,nbdevdn=2,matype=0)
#        self.upper, self.middle, self.lower=ta.BBANDS(np.array(closeDs),timeperiod=self.bBandsPeriod,nbdevdn=2,matype=0)
        if str(self.lower[-1]) == 'nan':
            return
#        if self.__position is not None:
##            if not self.__position.exitActive() and cross.cross_below(self.__ma1, self.__ma2) > 0:
#            if not self.__position.exitActive():
#                self.__position.exitMarket()
#                self.info("sell %s" % (bars.getDateTime()))
#
#        if self.__position is None:
#            if self.buyCon1() and self.buyCon2():
#                shares = int(self.getBroker().getCash() * 0.2 / bars[self.__instrument].getPrice())
#                self.__position = self.enterLong(self.__instrument, shares)
#                self.info("buy %s" % (bars.getDateTime()))
        shares = self.getBroker().getShares(self.__instrument)
        bar = bars[self.__instrument]
        # print bar.getOpen(),bar.getHigh(),str(self.__datetime[-1])[:10], self.__volume[-1]
        # self.getFeed((self.__datetime[-1]))
        # 2016-11-09,24.43,26.64,24.35,26.30,401716139,10484546560.00
        # 2016-11-10,26.00,28.28,25.58,26.56,243030035,6611047424.00
        # 2016-11-11,26.15,26.77,25.70,25.99,95846280,2495707392.00
        # 2016-11-14,26.23,26.25,25.31,25.70,87878021,2254786304.00
        # 2016-11-15,25.60,27.80,25.46,26.94,148588573,3965893632.00
        # 2016-11-16,26.64,27.22,26.09,26.68,82711700,2204526848.00
#        print bar.getClose(),self.upper[-1],self.middle[-1],self.lower[-1]
#         if shares == 0 and bar.getClose() > self.upper[-1]:
        if shares == 0 and self.buyCon1() == 1:
#            print bar.getOpen()
 #           sharesToBuy = int(self.getBroker().getCash(False) / bar.getClose())
            sharesToBuy = int(self.getBroker().getCash() * 0.2 / bars[self.__instrument].getPrice())
            self.__position = self.enterLong(self.__instrument, sharesToBuy)
            self.marketOrder(self.__instrument, sharesToBuy)
            self.info("A:%.2f Dt:%s  BUY at ￥%.2f up:%0.2f mid:%0.2f lower:%0.2f" % (self.getBroker().getEquity() ,str(self.datetime[-1])[:10], bar.getClose(),self.upper[-1],self.middle[-1],self.lower[-1]))
        # elif shares > 0 and bar.getClose() < self.upper[-1]:
        elif shares > 0 and self.buyCon1() == 0:
            self.marketOrder(self.__instrument, -1*shares)
            self.info("A:%.2f Dt:%s SELL at ￥%.2f up:%0.2f mid:%0.2f lower:%0.2f" % (self.getBroker().getEquity() ,str(self.datetime[-1])[:10], bar.getClose(),self.upper[-1],self.middle[-1],self.lower[-1]))
        # self.info("op:%s %s"%(max(self.oplist),min(self.oplist)))
#        if len(self.upper) >0 :
#            self.info( "up:%s mid:%s low:%s"%( self.upper[-1],self.middle[-1],self.lower[-1]))

#        shares = self.getBroker().getShares(self.__instrument)
#        bar = bars[self.__instrument]
#        if shares == 0 and bar.getClose() < lower:
#     #           sharesToBuy = int(self.getBroker().getCash(False) / bar.getClose())
#            sharesToBuy = int(self.getBroker().getCash() * 0.2 / bars[self.__instrument].getPrice())
#            self.__position = self.enterLong(self.__instrument, sharesToBuy)
#            self.marketOrder(self.__instrument, sharesToBuy)
#            self.info("A:%s BUY at ￥%.2f" % (self.getBroker().getEquity() , bar.getClose()))
#        elif shares > 0 and bar.getClose() > upper:
#            self.marketOrder(self.__instrument, -1*shares)
#            self.info("A:%s BUY at ￥%.2f" % (self.getBroker().getEquity() , bar.getClose()))


class BBands_old(strategy.BacktestingStrategy):
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
    def buyCon1(self):
        pass

    def buyCon2(self):
        pass
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
# from feedutil import dataFramefeed
# import tushare as ts


def turtle_test(code,start=None,plot=True):
    feed = ptc.get_tdx_barfeed(code,start)
    #myStrategy = pyalg_test.SMACrossOver(feed, "orcl", 20)
    pars=[2, 20, 60, 10]
#    myStrategy = thrSMA_dayinfo(feed, "orcl",*pars)
    myStrategy = BBands(feed, code,20)
    # Attach a returns analyzers to the strategy.
#    returnsAnalyzer = returns.Returns()
#    myStrategy.attachAnalyzer(returnsAnalyzer)



#    if dataString =='pyalg_util':
#        ds = pyalg_utils.dataSet(myStrategy)   #抽取交易数据集语句，若使用系统自带画图功能则不需要该项
    from pyalgotrade.stratanalyzer import returns
    from pyalgotrade.stratanalyzer import sharpe
    from pyalgotrade.stratanalyzer import drawdown
    from pyalgotrade.stratanalyzer import trades

    retAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(retAnalyzer)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    myStrategy.attachAnalyzer(sharpeRatioAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    myStrategy.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    myStrategy.attachAnalyzer(tradesAnalyzer)

        # Attach the plotter to the strategy.
#    plt = plotter.StrategyPlotter(myStrategy)
    # Plot the simple returns on each bar.


    if plot:
        plt = plotter.StrategyPlotter(myStrategy, True, True, True)
        plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", retAnalyzer.getReturns())

    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

#    if dataString =='pyalg_util':
#        rs = ds.getDefault()       #获取默认的交易信息，dic格式
#        plot(rs["cumulativeReturns"][:,0],rs["cumulativeReturns"][:,1])  #简单作图示例

    #夏普率
    sharp = sharpeRatioAnalyzer.getSharpeRatio(0.05)
    #最大回撤
    maxdd = drawDownAnalyzer.getMaxDrawDown()
    #收益率
    return_ = retAnalyzer.getCumulativeReturns()[-1]
    #收益曲线
    return_list = []
    for item in retAnalyzer.getCumulativeReturns():
        return_list.append(item)

    print "Sharpe ratio: %.2f maxdown:%.2f%%  return:%.2f%%" %(sharp,maxdd*100,return_*100)
    myStrategy.get_max_min()
    plt.plot()


#    if plot:
#        plt = plotter.StrategyPlotter(strat, True, True, True)
#
#    strat.run()
#
#    if plot:
#        plt.plot()






if __name__ == '__main__':
    #vwap(True)
    code='999999'
    turtle_test(code,'2016-01-01')
