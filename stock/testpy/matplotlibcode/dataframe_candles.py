import os
import numpy as np
import pandas as pd
from pandas.io.data import DataReader
# import mysql.connector
# from pandas.io.sql import frame_query
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc

df = pd.DataFrame()
symbols = ['GOOG','AAPL']

for symbol in symbols:
    ClosingPrice = DataReader(symbol, 'yahoo', datetime(2015,11,1), datetime(2015,11,30))
    ClosingPrice = ClosingPrice.reset_index()
    ClosingPrice['Symbol'] = symbol
    df = df.append(ClosingPrice)

def createchart(name):

    df4 = (df.loc[df['Symbol']==name])
    df4['date2num']=df4['Date'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
    cols = df4.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df4 = df4[cols]
    df4 = df4.drop('Date',1)
    quotes = np.array(df4)

    fig, (ax1,ax2)=plt.subplots(2,1,sharex=True,figsize=(8,6),gridspec_kw=dict(height_ratios=[3.236,1]))
    candlestick_ohlc(ax1, quotes, width = 0.6, colorup = 'g', colordown = 'r')
    ax1.set_ylabel('Stock Price')
    ax1.set_title(name+ " Stock Price")
    ax1.grid(True)
    ax1.xaxis_date()

    ax2.bar(quotes[:,0]-0.25,quotes[:,5],width = 0.5)
    ax2.set_ylabel('Volume')
    ax2.axes.yaxis.set_ticklabels([])
    ax2.grid(True)
    ax2.autoscale_view()
    plt.subplots_adjust(left=.09, bottom =.15, right = .94, top = 0.94, wspace = .2, hspace = 0.0)
    plt.setp(plt.gca().get_xticklabels(),rotation = 45)
    plt.show()
    return

# Stockname = str(raw_input("Please enter the stock you want to examine: "))
createchart('AAPL')