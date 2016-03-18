# THIS VERSION IS FOR PYTHON 2 #
import urllib2
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc,candlestick2_ohlc,volume_overlay
import matplotlib
import pylab
matplotlib.rcParams.update({'font.size': 9})
import tushare as ts
# eachStock = 'EBAY','TSLA','AAPL'

def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi

def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def computeMACD(x, slow=26, fast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow
def graphData_candles(stock,MA1,MA2):
    '''
        Use this to dynamically pull a stock:
    '''
    try:
        print 'Currently Pulling',stock
        print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
        # urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=10y/csv'
        bars = ts.get_hist_data(stock,start='2015-01-01')
        stockFile =[]
    except Exception,e:
        print str(e), 'failed to pull pricing data'
    try:   
        bars=bars.sort_index(ascending=True)
        # bars.reset_index(inplace=True)
        # bars.plot()
        # bars.date=bars.date.astype(datetime.datetime)
        # bars['date']=bars['date'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
        # import pandas as pd
        # bars['date2']=bars['date'].apply(lambda date: mdates.date2num(datetime.datetime.strptime(date,'%Y-%m-%d')))
        # print "a:",type(bars.date[:1])
        # bars.plot()
        # bars['date']=bars['date'].apply(lambda date: mdates.date2num(datetime.datetime.strptime(date,'%Y-%m-%d')))
        # date=mdates.strpdate2num('%Y-%m-%d')bars.date.values
        date=mdates.date2num(bars.index.to_datetime().to_pydatetime())
        # print date
        openp=bars['open']
        closep=bars['close']
        highp=bars['high']
        lowp=bars['low']
        volume=bars['volume']
        
        Av1 = movingaverage(closep, MA1)
        Av2 = movingaverage(closep, MA2)
        newAr = zip(
            date,
            openp,
            highp,
            lowp,
            closep,
            volume)
        SP = len(date[MA2-1:])
        # print "sp:",SP    
        fig = plt.figure(facecolor='#07000d')
        # print len(bars['open'])
        
        ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
        # candlestick2_ohlc(ax1, openp[-SP:],highp[-SP:],lowp[-SP:],closep[-SP:], width=.6, colorup='#53c156', colordown='#ff1717')
        # volume_overlay(ax1, openp[-SP:], closep[-SP:], volume[-SP:], colorup='k', colordown='r', width=4, alpha=1.0)
        # candlestick_ohlc(ax1, newAr[-SP:], width=.6, colorup='#53c156', colordown='#ff1717')
        candlestick_ohlc(ax1, newAr[-SP:], width=.6, colorup='#ff1717', colordown='#53c156')
        
        # fig = figure() 
        # ax = fig.add_subplot(111) 
        # candlestick2(ax,bars['open'],bars['close'],bars['high'],bars['low'],width=.5,colorup='g',colordown='r',alpha=1)
        # ax.set_xticks(arange(0,len(bars))) 
        # ax.set_xticklabels(bars.index,rotation=70)
  
        # div_n=len(ax1.get_xticks())
        # print "t_x:",div_n,len(bars) % div_n,len(bars),ax1.get_xticks()
        # ax1.set_xticks(range(0,len(bars.index),div_n))
        # new_xticks = [bars.index[d] for d in ax1.get_xticks()]
        # ax1.set_xticklabels(new_xticks,rotation=30, horizontalalignment='center')
        
        # idx_a=range(len(bars.index) - 1)
        # print idx_a,idx_a,len(idx_a)

        Label1 = str(MA1)+' SMA'
        Label2 = str(MA2)+' SMA'
        ax1.plot(date[-SP:],Av1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
        ax1.plot(date[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
        
        ax1.grid(True, color='w')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel('Stock price and Volume')

        maLeg = plt.legend(loc=9, ncol=2, prop={'size':7},
                   fancybox=True, borderaxespad=0.)
        maLeg.get_frame().set_alpha(0.4)
        textEd = pylab.gca().get_legend().get_texts()
        pylab.setp(textEd[0:5], color = 'w')

        volumeMin = 0
        
        ax0 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
        rsi = rsiFunc(closep)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        
        ax0.plot(date[-SP:], rsi[-SP:], rsiCol, linewidth=1.5)
        ax0.axhline(70, color=negCol)
        ax0.axhline(30, color=posCol)
        ax0.fill_between(date[-SP:], rsi[-SP:], 70, where=(rsi[-SP:]>=70), facecolor=negCol, edgecolor=negCol, alpha=0.5)
        ax0.fill_between(date[-SP:], rsi[-SP:], 30, where=(rsi[-SP:]<=30), facecolor=posCol, edgecolor=posCol, alpha=0.5)
        ax0.set_yticks([30,70])
        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        plt.ylabel('RSI')

        ax1v = ax1.twinx()
        ax1v.fill_between(date[-SP:],volumeMin, volume[-SP:], facecolor='#00ffe8', alpha=.4)
        ax1v.axes.yaxis.set_ticklabels([])
        ax1v.grid(False)
        ###Edit this to 3, so it's a bit larger
        ax1v.set_ylim(0, 3*volume.max())
        ax1v.spines['bottom'].set_color("#5998ff")
        ax1v.spines['top'].set_color("#5998ff")
        ax1v.spines['left'].set_color("#5998ff")
        ax1v.spines['right'].set_color("#5998ff")
        ax1v.tick_params(axis='x', colors='w')
        ax1v.tick_params(axis='y', colors='w')
        ax2 = plt.subplot2grid((6,4), (5,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
        fillcolor = '#00ffe8'
        nslow = 26
        nfast = 12
        nema = 9
        emaslow, emafast, macd = computeMACD(closep)
        ema9 = ExpMovingAverage(macd, nema)
        ax2.plot(date[-SP:], macd[-SP:], color='#4ee6fd', lw=2)
        ax2.plot(date[-SP:], ema9[-SP:], color='#e1edf9', lw=1)
        ax2.fill_between(date[-SP:], macd[-SP:]-ema9[-SP:], 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)

        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        plt.ylabel('MACD', color='w')
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))
        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)

        plt.suptitle(stock.upper(),color='w')

        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        
        # ax1.annotate('Big news!',(date[510],Av1[510]),
            # xytext=(0.8, 0.9), textcoords='axes fraction',
            # arrowprops=dict(facecolor='white', shrink=0.05),
            # fontsize=14, color = 'w',
            # horizontalalignment='right', verticalalignment='bottom')

        plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
        plt.show()
        # fig.savefig('example.png',facecolor=fig.get_facecolor())
           
    except Exception,e:
        print 'main loop',str(e)
        
def graphData(stock,MA1,MA2):
    '''
        Use this to dynamically pull a stock:
    '''
    try:
        print 'Currently Pulling',stock
        print str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
        # urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=10y/csv'
        bars = ts.get_hist_data(stock,start='2015-08-01')
        stockFile =[]
    except Exception,e:
        print str(e), 'failed to pull pricing data'
    try:   
        bars=bars.sort_index(ascending=True)
        # bars.reset_index(inplace=True)
        # bars.plot()
        # bars.date=bars.date.astype(datetime.datetime)
        # bars['date']=bars['date'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
        # import pandas as pd
        # bars['date2']=bars['date'].apply(lambda date: mdates.date2num(datetime.datetime.strptime(date,'%Y-%m-%d')))
        # print "a:",type(bars.date[:1])
        # bars.plot()
        # bars['date']=bars['date'].apply(lambda date: mdates.date2num(datetime.datetime.strptime(date,'%Y-%m-%d')))
        # date=mdates.strpdate2num('%Y-%m-%d')bars.date.values
        # date=mdates.date2num(bars.index.to_datetime().to_pydatetime())
        date=bars.index
        openp=bars['open']
        closep=bars['close']
        highp=bars['high']
        lowp=bars['low']
        volume=bars['volume']
        
        Av1 = movingaverage(closep, MA1)
        Av2 = movingaverage(closep, MA2)
        # newAr = zip(
            # date,
            # openp,
            # highp,
            # lowp,
            # closep,
            # volume)
        SP = len(date[MA2-1:])
        print "sp:",SP
        fig = plt.figure(facecolor='#07000d')
        ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
        candlestick2_ohlc(ax1, openp[-SP:],highp[-SP:],lowp[-SP:],closep[-SP:], width=1, colorup='#ff1717', colordown='#53c156', alpha=1.0)
        # volume_overlay(ax1, openp[-SP:], closep[-SP:], volume[-SP:], colorup='k', colordown='r', width=4, alpha=1.0)
        # fig = figure() 
        # ax = fig.add_subplot(111) 
        # candlestick2(ax,bars['open'],bars['close'],bars['high'],bars['low'],width=.5,colorup='g',colordown='r',alpha=1)
        # ax.set_xticks(arange(0,len(bars))) 
        # ax.set_xticklabels(bars.index,rotation=70)
  
        div_n=len(ax1.get_xticks())
        print "t_x:",div_n,len(bars) % div_n,len(bars),ax1.get_xticks()
        ax1.set_xticks(range(0,len(date[-SP:]),div_n))
        xticks=ax1.get_xticks()
        print "xticks:",xticks,len(date[-SP:])
        new_xticks = [date[-SP:][d] for d in xticks ]
        ax1.set_xticklabels(new_xticks,rotation=30, horizontalalignment='center')
        
        idx_a=range(len(date[-SP:]))
        print len(idx_a),len(Av1[-SP:])
    
        Label1 = str(MA1)+' SMA'
        Label2 = str(MA2)+' SMA'
        ax1.plot(idx_a,Av1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
        ax1.plot(idx_a,Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
        
        ax1.grid(True, color='w')
        # ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        # plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel('Stock price and Volume')

        maLeg = plt.legend(loc=9, ncol=2, prop={'size':7},
                   fancybox=True, borderaxespad=0.)
        maLeg.get_frame().set_alpha(0.4)
        textEd = pylab.gca().get_legend().get_texts()
        pylab.setp(textEd[0:5], color = 'w')

        volumeMin = 0
        
        ax0 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
        rsi = rsiFunc(closep)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        
        ax0.plot(idx_a, rsi[-SP:], rsiCol, linewidth=1.5)
        ax0.axhline(70, color=negCol)
        ax0.axhline(30, color=posCol)
        ax0.fill_between(idx_a, rsi[-SP:], 70, where=(rsi[-SP:]>=70), facecolor=negCol, edgecolor=negCol, alpha=0.5)
        ax0.fill_between(idx_a, rsi[-SP:], 30, where=(rsi[-SP:]<=30), facecolor=posCol, edgecolor=posCol, alpha=0.5)
        ax0.set_yticks([30,70])
        ax0.yaxis.label.set_color("w")
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.tick_params(axis='y', colors='w')
        ax0.tick_params(axis='x', colors='w')
        plt.ylabel('RSI')

        ax1v = ax1.twinx()
        ax1v.fill_between(idx_a,volumeMin, volume[-SP:], facecolor='#00ffe8', alpha=.4)
        ax1v.axes.yaxis.set_ticklabels([])
        ax1v.grid(False)
        ###Edit this to 3, so it's a bit larger
        ax1v.set_ylim(0, 3*volume.max())
        ax1v.spines['bottom'].set_color("#5998ff")
        ax1v.spines['top'].set_color("#5998ff")
        ax1v.spines['left'].set_color("#5998ff")
        ax1v.spines['right'].set_color("#5998ff")
        ax1v.tick_params(axis='x', colors='w')
        ax1v.tick_params(axis='y', colors='w')
        ax2 = plt.subplot2grid((6,4), (5,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
        fillcolor = '#00ffe8'
        nslow = 26
        nfast = 12
        nema = 9
        emaslow, emafast, macd = computeMACD(closep)
        ema9 = ExpMovingAverage(macd, nema)
        ax2.plot(idx_a, macd[-SP:], color='#4ee6fd', lw=2)
        ax2.plot(idx_a, ema9[-SP:], color='#e1edf9', lw=1)
        ax2.fill_between(idx_a, macd[-SP:]-ema9[-SP:], 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)

        # plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w')
        plt.ylabel('MACD', color='w')
        # ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))
        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)

        plt.suptitle(stock.upper(),color='w')

        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        
        # ax1.annotate('Big news!',(date[510],Av1[510]),
            # xytext=(0.8, 0.9), textcoords='axes fraction',
            # arrowprops=dict(facecolor='white', shrink=0.05),
            # fontsize=14, color = 'w',
            # horizontalalignment='right', verticalalignment='bottom')

        plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
        plt.show()
        # fig.savefig('example.png',facecolor=fig.get_facecolor())
           
    except Exception,e:
        print 'main loop',str(e)

# while True:
    # stock = raw_input('Stock to plot: ')
graphData('601998',10,60)
# graphData_candles('601998',10,60)