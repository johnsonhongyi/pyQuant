#coding=utf-8
import datetime
import os
import time

import numpy as np
import pandas as pd
import talib as ta
import tushare as ts
import tdx_data_Day as tdd

#http://blog.sina.com.cn/s/blog_620987bf0102vlmz.html
#获取股票列表
#code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,总股本(万) totalAssets,总资产(万)liquidAssets,流动资产
# fixedAssets,固定资产 reserved,公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率 timeToMarket,上市日期
def Get_Stock_List():
    df = ts.get_stock_basics().head(10)
#     print (df)
    return df

def Get_BBANDS(df,dtype='d'):
    upperband,middleband,lowerband=ta.BBANDS(np.array(df['close']),timeperiod=20,nbdevdn=2,matype=0)
    df['upbb%s'%dtype] = pd.Series(upperband,index=df.index)
    df['midb%s'%dtype] = pd.Series(middleband,index=df.index)
    df['lowb%s'%dtype] = pd.Series(lowerband,index=df.index)
    return df
    
#修改了的函数，按照多个指标进行分析

#按照MACD，KDJ等进行分析
def Get_TA(df,dtype='d'):
    df = df.sort_index(ascending=True)
    if dtype != 'd':
        df['ma5%s'%dtype] = pd.rolling_mean(df.close,5)
        df['ma10%s'%dtype] = pd.rolling_mean(df.close,10)
        df['ma20%s'%dtype] = pd.rolling_mean(df.close,20)
    
    operate_array1=[]
    operate_array2=[]
    operate_array3=[]
# index,0 - 6 date：日期 open：开盘价 high：最高价 close：收盘价 low：最低价 volume：成交量 price_change：价格变动 p_change：涨跌幅
# 7-12 ma5：5日均价 ma10：10日均价 ma20:20日均价 v_ma5:5日均量v_ma10:10日均量 v_ma20:20日均量
    dflen = df.shape[0]
    print dflen
    if dflen>34:
        try:
            (df,operate1) = Get_MACD(df,dtype)
            (df,operate2) = Get_KDJ(df,dtype)
            (df,operate3) = Get_RSI(df,dtype)
        except Exception as e:
             # Write_Blog(e,Dist)
             print "error:%s"%e
             pass
    else:
        operate1=-9
        operate2=-9
        operate3=-9
    # print len(df),operate1
    operate_array1.append(operate1)
    operate_array2.append(operate2)
    operate_array3.append(operate3)

        
    df['MACD%s'%dtype]=pd.Series(operate_array1,index=df.index)
    df['KDJ%s'%dtype]=pd.Series(operate_array2,index=df.index)
    df['RSI%s'%dtype]=pd.Series(operate_array3,index=df.index)
    
    df = Get_BBANDS(df,dtype)
    
    return df



#通过MACD判断买入卖出
def Get_MACD(df,dtype='d'):
    #参数12,26,9
    macd, macdsignal, macdhist = ta.MACD(np.array(df['close']), fastperiod=12, slowperiod=26, signalperiod=9)

    SignalMA5 = ta.MA(macdsignal, timeperiod=5, matype=0)
    SignalMA10 = ta.MA(macdsignal, timeperiod=10, matype=0)
    SignalMA20 = ta.MA(macdsignal, timeperiod=20, matype=0)
    #13-15 DIFF  DEA  DIFF-DEA
    df['diff%s'%dtype]=pd.Series(macd,index=df.index) #DIFF 13 
    df['dea%s'%dtype]=pd.Series(macdsignal,index=df.index)#DEA  14 
    df['ddea%s'%dtype]=pd.Series(macdhist,index=df.index)#DIFF-DEA  15
    dflen = df.shape[0]
    MAlen = len(SignalMA5)
    operate = 0
    #2个数组 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
    #待修改
    diff=df.loc[df.index[-1],'diff%s'%dtype]
    diff2=df.loc[df.index[-2],'diff%s'%dtype]
    dea=df.loc[df.index[-1],'dea%s'%dtype]
    dea2=df.loc[df.index[-2],'dea%s'%dtype]

    if diff >0:
        if dea >0:
            if diff > dea and diff2 <= dea2:
                operate = operate + 10#买入
    else:
        if dea <0:
            if diff == dea2 :
                operate = operate - 10#卖出

    #3.DEA线与K线发生背离，行情反转信号。
    ma5 =  df.loc[df.index[-1],'ma5%s'%dtype]   #7
    ma10 =  df.loc[df.index[-1],'ma10%s'%dtype] #8
    ma20 =  df.loc[df.index[-1],'ma20%s'%dtype]  #9
    
    if ma5 >= ma10 and ma10 >= ma20:#K线上涨
        if SignalMA5[MAlen-1]<=SignalMA10[MAlen-1] and SignalMA10[MAlen-1]<=SignalMA20[MAlen-1]: #DEA下降
            operate = operate - 1
    elif ma5 <= ma10 and ma10 <= ma20:#K线下降
        if SignalMA5[MAlen-1]>=SignalMA10[MAlen-1] and SignalMA10[MAlen-1]>=SignalMA20[MAlen-1]: #DEA上涨
            operate = operate + 1


    #4.分析MACD柱状线，由负变正，买入信号。
    diffdea = df.loc[df.index[-1],'ddea%s'%dtype]
    # diffdea2 = df.loc[df.index[-2],'macdhist%s'%dtype]
    
    if diffdea >0 and dflen >30 :
        for i in range(1,26):
            if df.loc[df.index[-1-i],'ddea%s'%dtype] <=0:#
                operate = operate + 5
                break
            #由正变负，卖出信号
    if diffdea <0 and dflen >30 :
        dayl = 26 if len(df) >26 else len(df)
        for i in range(1,):
            if df.loc[df.index[-1-i],'ddea%s'%dtype] >=0:#
                operate = operate - 5
                break

    return (df,operate)



#通过KDJ判断买入卖出
def Get_KDJ(df,dtype='d'):
    #参数9,3,3
    slowk, slowd = ta.STOCH(np.array(df['high']), np.array(df['low']), np.array(df['close']), fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    slowkMA5 = ta.MA(slowk, timeperiod=5, matype=0)
    slowkMA10 = ta.MA(slowk, timeperiod=10, matype=0)
    slowkMA20 = ta.MA(slowk, timeperiod=20, matype=0)
    slowdMA5 = ta.MA(slowd, timeperiod=5, matype=0)
    slowdMA10 = ta.MA(slowd, timeperiod=10, matype=0)
    slowdMA20 = ta.MA(slowd, timeperiod=20, matype=0)

    #16-17 K,D
    df['slowk%s'%dtype]=pd.Series(slowk,index=df.index) #K
    df['slowd%s'%dtype]=pd.Series(slowd,index=df.index)#D
    dflen = df.shape[0]
    MAlen = len(slowkMA5)
    operate = 0
    
    kdjk=df.loc[df.index[-1],'slowk%s'%dtype]
    kdjk2=df.loc[df.index[-2],'slowk%s'%dtype]
    kdjd=df.loc[df.index[-1],'slowd%s'%dtype]
    kdjd2=df.loc[df.index[-2],'slowd%s'%dtype]
    
    ma5=df.loc[df.index[-1],'ma5%s'%dtype]
    ma10=df.loc[df.index[-1],'ma10%s'%dtype]
    ma20=df.loc[df.index[-1],'ma20%s'%dtype]
    #1.K线是快速确认线——数值在90以上为超买，数值在10以下为超卖；D大于80时，行情呈现超买现象。D小于20时，行情呈现超卖现象。
    if kdjk>=90:
        operate = operate - 3
    elif kdjk<=10:
        operate = operate + 3

    if kdjd>=80:
        operate = operate - 3
    elif kdjd<=20:
        operate = operate + 3

    #2.上涨趋势中，K值大于D值，K线向上突破D线时，为买进信号。#待修改
    if kdjk> kdjd and kdjk2 <=kdjd2:
        operate = operate + 10
    #下跌趋势中，K小于D，K线向下跌破D线时，为卖出信号。#待修改
    elif kdjk< kdjd and kdjk2>=kdjd2:
        operate = operate - 10


    #3.当随机指标与股价出现背离时，一般为转势的信号。
    if ma5>=ma10 and ma10>=ma20:#K线上涨
        if (slowkMA5[MAlen-1]<=slowkMA10[MAlen-1] and slowkMA10[MAlen-1]<=slowkMA20[MAlen-1]) or \
           (slowdMA5[MAlen-1]<=slowdMA10[MAlen-1] and slowdMA10[MAlen-1]<=slowdMA20[MAlen-1]): #K,D下降
            operate = operate - 1
    elif ma5<=ma10 and ma10<=ma20:#K线下降
        if (slowkMA5[MAlen-1]>=slowkMA10[MAlen-1] and slowkMA10[MAlen-1]>=slowkMA20[MAlen-1]) or \
           (slowdMA5[MAlen-1]>=slowdMA10[MAlen-1] and slowdMA10[MAlen-1]>=slowdMA20[MAlen-1]): #K,D上涨
            operate = operate + 1
    return (df,operate)


#通过RSI判断买入卖出
def Get_RSI(df,dtype='d'):
    #参数14,5
    slowreal = ta.RSI(np.array(df['close']), timeperiod=14)
    fastreal = ta.RSI(np.array(df['close']), timeperiod=5)

    slowrealMA5 = ta.MA(slowreal, timeperiod=5, matype=0)
    slowrealMA10 = ta.MA(slowreal, timeperiod=10, matype=0)
    slowrealMA20 = ta.MA(slowreal, timeperiod=20, matype=0)
    fastrealMA5 = ta.MA(fastreal, timeperiod=5, matype=0)
    fastrealMA10 = ta.MA(fastreal, timeperiod=10, matype=0)
    fastrealMA20 = ta.MA(fastreal, timeperiod=20, matype=0)
    #18-19 慢速real，快速real
    df['slowreal%s'%dtype]=pd.Series(slowreal,index=df.index) #慢速real 18
    df['fastreal%s'%dtype]=pd.Series(fastreal,index=df.index)#快速real 19
    dflen = df.shape[0]
    MAlen = len(slowrealMA5)
    operate = 0
    
    slow=df.loc[df.index[-1],'slowreal%s'%dtype]
    slow2=df.loc[df.index[-2],'slowreal%s'%dtype]
    fast=df.loc[df.index[-1],'fastreal%s'%dtype]
    fast2=df.loc[df.index[-2],'fastreal%s'%dtype]
    #RSI>80为超买区，RSI<20为超卖区
    if slow>80 or fast>80:
        operate = operate - 2
    elif slow<20 or fast<20:
        operate = operate + 2

    #RSI上穿50分界线为买入信号，下破50分界线为卖出信号
    if (slow2 <=50 and slow >50) or (fast2<=50 and fast>50):
        operate = operate + 4
    elif (slow2>=50 and slow<50) or (fast2>=50 and fast<50):
        operate = operate - 4

    ma5=df.loc[df.index[-1],'ma5%s'%dtype]
    ma10=df.loc[df.index[-1],'ma10%s'%dtype]
    ma20=df.loc[df.index[-1],'ma20%s'%dtype]
    
    #RSI掉头向下为卖出讯号，RSI掉头向上为买入信号
    if ma5 >=ma10 and ma10>=ma20:#K线上涨
        if (slowrealMA5[MAlen-1]<=slowrealMA10[MAlen-1] and slowrealMA10[MAlen-1]<=slowrealMA20[MAlen-1]) or \
           (fastrealMA5[MAlen-1]<=fastrealMA10[MAlen-1] and fastrealMA10[MAlen-1]<=fastrealMA20[MAlen-1]): #RSI下降
            operate = operate - 1
    elif ma5<=ma10 and ma10<=ma20:#K线下降
        if (slowrealMA5[MAlen-1]>=slowrealMA10[MAlen-1] and slowrealMA10[MAlen-1]>=slowrealMA20[MAlen-1]) or \
           (fastrealMA5[MAlen-1]>=fastrealMA10[MAlen-1] and fastrealMA10[MAlen-1]>=fastrealMA20[MAlen-1]): #RSI上涨
            operate = operate + 1

    #慢速线与快速线比较观察，若两线同向上，升势较强；若两线同向下，跌势较强；若快速线上穿慢速线为买入信号；若快速线下穿慢速线为卖出信号
    if fast> slow and fast2<=slow2:
        operate = operate + 10
    elif fast< slow and fast2>=slow2:
        operate = operate - 10
    return (df,operate)

def Output_Csv(df,Dist):
    TODAY = datetime.date.today()
    CURRENTDAY=TODAY.strftime('%Y-%m-%d')
#     reload(sys)
#     sys.setdefaultencoding( "gbk" )
    print ("write csv")
    df.to_csv(Dist+CURRENTDAY+'stock-macd-kdj.csv',encoding='gbk')#选择保存



def Close_machine():
    o="c:\\windows\\system32\\shutdown -s"#########
    os.system(o)#########


#日志记录
def Write_Blog(strinput,Dist):
    TODAY = datetime.date.today()
    CURRENTDAY=TODAY.strftime('%Y-%m-%d')
    TIME = time.strftime("%H:%M:%S")
    print ("Blog")
    #写入本地文件
    fp = open(Dist+'blog.txt','a')
    fp.write('------------------------------\n'+CURRENTDAY +" "+TIME+" "+ strinput+'  \n')
    fp.close()
    time.sleep(1)

if __name__ == '__main__':
    # df = Get_Stock_List()
    # Dist = 'E:\\Quant\\'
    # df = Get_TA(df,Dist)
    # df = ts.get_hist_data('sh')
    code='600702'
    df = tdd.get_tdx_append_now_df_api(code,start='2015-01-01').sort_index(ascending=True)
    print df[-1:]
    # df = Get_BBANDS(df)
    df = Get_TA(df)
    # for dtype in ['w','m']:
    # for dtype in ['w']:
        # df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True).set_index('date')
        # df = Get_TA(df,dtype)
    # print df.columns
    colmdw=[ u'name',u'code', u'open', u'high', u'low', u'close',
      u'ma5d',u'ma5w', u'ma10d',u'ma10w', u'ma20d',u'ma20w',u'MACDd',u'MACDw', u'KDJd',u'KDJw', u'RSId', u'RSIw',
      u'upbbd', u'midbd']
    colmd=[ u'name',u'code', u'open', u'high', u'low', u'close',
      u'ma5d', u'ma10d', u'ma20d',u'MACDd', u'KDJd', u'RSId',
      u'upbbd', u'midbd']
    colmaw=[ u'name',u'code', u'open', u'high', u'low', u'close',
      u'ma5d', u'ma10d', u'ma20d',u'MACDd',u'MACDw', u'KDJd',u'KDJw', u'RSId', u'RSIw',
      u'upbbd',  u'upbbw', u'midbd', u'midbw',]
    print ("df:"),df.loc[df.index[-1]:,colmd]
    col=[u'code', u'open', u'high', u'low', u'close', u'vol', u'amount', u'name',
          u'ma5d', u'ma10d', u'ma20d', u'diffd', u'dead', u'ddead', u'slowkd',
          u'slowdd', u'slowreald', u'fastreald', u'MACDd', u'KDJd', u'RSId',
          u'upbbd', u'midbd', u'lowbd']
    # time.sleep(1)
    # Close_machine()