# coding=utf-8
import numpy as np
import pandas as pd
import talib as ta
import tushare as ts


def get_BBANDS_Status(df):
    if len(df) < 20:
        print "Data no 20 day"
        return ''
    df = df.sort_index(axis=0, by=None, ascending=True)
    upperband, middleband, lowerband = ta.BBANDS(np.array(df['close']), timeperiod=20, nbdevdn=2, matype=0)
    df['upperband'] = pd.Series(upperband, index=df.index)  # K
    df['middleband'] = pd.Series(middleband, index=df.index)  # D
    df['lowerband'] = pd.Series(lowerband, index=df.index)  # D
    df = df.sort_index(axis=0, by=None, ascending=False)
    # df = df.dropna()
    # print df[:10]

    return df


def get_KDJ_Status(df):
    # 参数9,3,3
    df = df.sort_index()

    slowk, slowd = ta.STOCH(np.array(df['high']), np.array(df['low']), np.array(df['close']), fastk_period=9,
                            slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    # slowkMA5 = ta.MA(slowk, timeperiod=5, matype=0)
    # slowkMA10 = ta.MA(slowk, timeperiod=10, matype=0)
    # slowkMA20 = ta.MA(slowk, timeperiod=20, matype=0)
    # slowdMA5 = ta.MA(slowd, timeperiod=5, matype=0)
    # slowdMA10 = ta.MA(slowd, timeperiod=10, matype=0)
    # slowdMA20 = ta.MA(slowd, timeperiod=20, matype=0)

    # 16-17 K,D
    df['slowk'] = pd.Series(slowk, index=df.index)  # K
    df['slowd'] = pd.Series(slowd, index=df.index)  # D
    # df=df.dropna()
    df.sort_index(ascending=False, inplace=True)
    return df

def Get_MACD_Cross(df):
    # 参数12,26,9
    macd, macdsignal, macdhist = ta.MACD(np.array(df['close']), fastperiod=12, slowperiod=26, signalperiod=9)

    SignalMA5 = ta.MA(macdsignal, timeperiod=5, matype=0)
    SignalMA10 = ta.MA(macdsignal, timeperiod=10, matype=0)
    SignalMA20 = ta.MA(macdsignal, timeperiod=20, matype=0)
    # 13-15 DIFF  DEA  DIFF-DEA
    df['macd'] = pd.Series(macd, index=df.index)  # DIFF
    df['macdsignal'] = pd.Series(macdsignal, index=df.index)  # DEA
    df['macdhist'] = pd.Series(macdhist, index=df.index)  # DIFF-DEA
    dflen = df.shape[0]
    MAlen = len(SignalMA5)
    operate = 0
    # 2个数组 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
    # 待修改
    if df.iat[(dflen - 1), 13] > df.iat[(dflen - 1), 14] and df.iat[(dflen - 2), 13] <= df.iat[(dflen - 2), 14]:
        operate = operate + 1
    else:
        operate = operate - 1

    # name   | couts | diff | trade |  high | percent |  open |  ratio
    # name  trade   buy  percent  open  high   low    volume  ticktime ratio
    # 'name', 'trade', 'buy', 'percent', 'open', 'high', 'low', 'volume', 'ticktime', 'ratio']

    # 3.DEA线与K线发生背离，行情反转信号。
    if df.iat[(dflen - 1), 7] >= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] >= df.iat[(dflen - 1), 9]:  # K线上涨
        if SignalMA5[MAlen - 1] <= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] <= SignalMA20[MAlen - 1]:  # DEA下降
            operate = operate - 1
    elif df.iat[(dflen - 1), 7] <= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] <= df.iat[(dflen - 1), 9]:  # K线下降
        if SignalMA5[MAlen - 1] >= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] >= SignalMA20[MAlen - 1]:  # DEA上涨
            operate = operate + 1

    # 4.分析MACD柱状线，由负变正，买入信号。
    if df.iat[(dflen - 1), 15] > 0 and dflen > 30:
        for i in range(1, 26):
            if df.iat[(dflen - 1 - i), 15] <= 0:  #
                operate = operate + 5
                break
                # 由正变负，卖出信号
    if df.iat[(dflen - 1), 15] < 0 and dflen > 30:
        for i in range(1, 26):
            if df.iat[(dflen - 1 - i), 15] >= 0:  #
                operate = operate - 5
                break

    return (df, operate)

    return df


def Get_MACD_ZeroUP(df):
    # 参数12,26,9
    macd, macdsignal, macdhist = ta.MACD(np.array(df['close']), fastperiod=12, slowperiod=26, signalperiod=9)

    SignalMA5 = ta.MA(macdsignal, timeperiod=5, matype=0)
    SignalMA10 = ta.MA(macdsignal, timeperiod=10, matype=0)
    SignalMA20 = ta.MA(macdsignal, timeperiod=20, matype=0)
    # 13-15 DIFF  DEA  DIFF-DEA
    df['macd'] = pd.Series(macd, index=df.index)  # DIFF
    df['macdsignal'] = pd.Series(macdsignal, index=df.index)  # DEA
    df['macdhist'] = pd.Series(macdhist, index=df.index)  # DIFF-DEA
    dflen = df.shape[0]
    MAlen = len(SignalMA5)
    operate = 0
    # 2个数组 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
    # 待修改
    if df.iat[(dflen - 1), 13] > 0:
        if df.iat[(dflen - 1), 14] > 0:
            if df.iat[(dflen - 1), 13] > df.iat[(dflen - 1), 14] and df.iat[(dflen - 2), 13] <= df.iat[(dflen - 2), 14]:
                operate = operate + 10  # 买入
    else:
        if df.iat[(dflen - 1), 14] < 0:
            if df.iat[(dflen - 1), 13] == df.iat[(dflen - 2), 14]:
                operate = operate - 10  # 卖出

    # 3.DEA线与K线发生背离，行情反转信号。
    if df.iat[(dflen - 1), 7] >= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] >= df.iat[(dflen - 1), 9]:  # K线上涨
        if SignalMA5[MAlen - 1] <= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] <= SignalMA20[MAlen - 1]:  # DEA下降
            operate = operate - 1
    elif df.iat[(dflen - 1), 7] <= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] <= df.iat[(dflen - 1), 9]:  # K线下降
        if SignalMA5[MAlen - 1] >= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] >= SignalMA20[MAlen - 1]:  # DEA上涨
            operate = operate + 1

    # 4.分析MACD柱状线，由负变正，买入信号。
    if df.iat[(dflen - 1), 15] > 0 and dflen > 30:
        for i in range(1, 26):
            if df.iat[(dflen - 1 - i), 15] <= 0:  #
                operate = operate + 5
                break
                # 由正变负，卖出信号
    if df.iat[(dflen - 1), 15] < 0 and dflen > 30:
        for i in range(1, 26):
            if df.iat[(dflen - 1 - i), 15] >= 0:  #
                operate = operate - 5
                break

    return (df, operate)

    return df


def Get_KDJ(df):
    # 参数9,3,3
    slowk, slowd = ta.STOCH(np.array(df['high']), np.array(df['low']), np.array(df['close']), fastk_period=9,
                            slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    slowkMA5 = ta.MA(slowk, timeperiod=5, matype=0)
    slowkMA10 = ta.MA(slowk, timeperiod=10, matype=0)
    slowkMA20 = ta.MA(slowk, timeperiod=20, matype=0)
    slowdMA5 = ta.MA(slowd, timeperiod=5, matype=0)
    slowdMA10 = ta.MA(slowd, timeperiod=10, matype=0)
    slowdMA20 = ta.MA(slowd, timeperiod=20, matype=0)

    # 16-17 K,D
    df['slowk'] = pd.Series(slowk, index=df.index)  # K
    df['slowd'] = pd.Series(slowd, index=df.index)  # D
    dflen = df.shape[0]
    MAlen = len(slowkMA5)
    operate = 0
    # 1.K线是快速确认线——数值在90以上为超买，数值在10以下为超卖；D大于80时，行情呈现超买现象。D小于20时，行情呈现超卖现象。
    if df.iat[(dflen - 1), 16] >= 90:
        operate = operate - 3
    elif df.iat[(dflen - 1), 16] <= 10:
        operate = operate + 3

    if df.iat[(dflen - 1), 17] >= 80:
        operate = operate - 3
    elif df.iat[(dflen - 1), 17] <= 20:
        operate = operate + 3

    # 2.上涨趋势中，K值大于D值，K线向上突破D线时，为买进信号。#待修改
    if df.iat[(dflen - 1), 16] > df.iat[(dflen - 1), 17] and df.iat[(dflen - 2), 16] <= df.iat[(dflen - 2), 17]:
        operate = operate + 10
    # 下跌趋势中，K小于D，K线向下跌破D线时，为卖出信号。#待修改
    elif df.iat[(dflen - 1), 16] < df.iat[(dflen - 1), 17] and df.iat[(dflen - 2), 16] >= df.iat[(dflen - 2), 17]:
        operate = operate - 10

    # 3.当随机指标与股价出现背离时，一般为转势的信号。
    if df.iat[(dflen - 1), 7] >= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] >= df.iat[(dflen - 1), 9]:  # K线上涨
        if (slowkMA5[MAlen - 1] <= slowkMA10[MAlen - 1] and slowkMA10[MAlen - 1] <= slowkMA20[MAlen - 1]) or \
                (slowdMA5[MAlen - 1] <= slowdMA10[MAlen - 1] and slowdMA10[MAlen - 1] <= slowdMA20[MAlen - 1]):  # K,D下降
            operate = operate - 1
    elif df.iat[(dflen - 1), 7] <= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] <= df.iat[(dflen - 1), 9]:  # K线下降
        if (slowkMA5[MAlen - 1] >= slowkMA10[MAlen - 1] and slowkMA10[MAlen - 1] >= slowkMA20[MAlen - 1]) or \
                (slowdMA5[MAlen - 1] >= slowdMA10[MAlen - 1] and slowdMA10[MAlen - 1] >= slowdMA20[MAlen - 1]):  # K,D上涨
            operate = operate + 1

    return (df, operate)


# 通过RSI判断买入卖出
def Get_RSI(df):
    # 参数14,5
    slowreal = ta.RSI(np.array(df['close']), timeperiod=14)
    fastreal = ta.RSI(np.array(df['close']), timeperiod=5)

    slowrealMA5 = ta.MA(slowreal, timeperiod=5, matype=0)
    slowrealMA10 = ta.MA(slowreal, timeperiod=10, matype=0)
    slowrealMA20 = ta.MA(slowreal, timeperiod=20, matype=0)
    fastrealMA5 = ta.MA(fastreal, timeperiod=5, matype=0)
    fastrealMA10 = ta.MA(fastreal, timeperiod=10, matype=0)
    fastrealMA20 = ta.MA(fastreal, timeperiod=20, matype=0)
    # 18-19 慢速real，快速real
    df['slowreal'] = pd.Series(slowreal, index=df.index)  # 慢速real 18
    df['fastreal'] = pd.Series(fastreal, index=df.index)  # 快速real 19
    dflen = df.shape[0]
    MAlen = len(slowrealMA5)
    operate = 0
    # RSI>80为超买区，RSI<20为超卖区
    if df.iat[(dflen - 1), 18] > 80 or df.iat[(dflen - 1), 19] > 80:
        operate = operate - 2
    elif df.iat[(dflen - 1), 18] < 20 or df.iat[(dflen - 1), 19] < 20:
        operate = operate + 2

    # RSI上穿50分界线为买入信号，下破50分界线为卖出信号
    if (df.iat[(dflen - 2), 18] <= 50 and df.iat[(dflen - 1), 18] > 50) or (
                    df.iat[(dflen - 2), 19] <= 50 and df.iat[(dflen - 1), 19] > 50):
        operate = operate + 4
    elif (df.iat[(dflen - 2), 18] >= 50 and df.iat[(dflen - 1), 18] < 50) or (
                    df.iat[(dflen - 2), 19] >= 50 and df.iat[(dflen - 1), 19] < 50):
        operate = operate - 4

    # RSI掉头向下为卖出讯号，RSI掉头向上为买入信号
    if df.iat[(dflen - 1), 7] >= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] >= df.iat[(dflen - 1), 9]:  # K线上涨
        if (slowrealMA5[MAlen - 1] <= slowrealMA10[MAlen - 1] and slowrealMA10[MAlen - 1] <= slowrealMA20[MAlen - 1]) or \
                (fastrealMA5[MAlen - 1] <= fastrealMA10[MAlen - 1] and fastrealMA10[MAlen - 1] <= fastrealMA20[
                        MAlen - 1]):  # RSI下降
            operate = operate - 1
    elif df.iat[(dflen - 1), 7] <= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] <= df.iat[(dflen - 1), 9]:  # K线下降
        if (slowrealMA5[MAlen - 1] >= slowrealMA10[MAlen - 1] and slowrealMA10[MAlen - 1] >= slowrealMA20[MAlen - 1]) or \
                (fastrealMA5[MAlen - 1] >= fastrealMA10[MAlen - 1] and fastrealMA10[MAlen - 1] >= fastrealMA20[
                        MAlen - 1]):  # RSI上涨
            operate = operate + 1

    # 慢速线与快速线比较观察，若两线同向上，升势较强；若两线同向下，跌势较强；若快速线上穿慢速线为买入信号；若快速线下穿慢速线为卖出信号
    if df.iat[(dflen - 1), 19] > df.iat[(dflen - 1), 18] and df.iat[(dflen - 2), 19] <= df.iat[(dflen - 2), 18]:
        operate = operate + 10
    elif df.iat[(dflen - 1), 19] < df.iat[(dflen - 1), 18] and df.iat[(dflen - 2), 19] >= df.iat[(dflen - 2), 18]:
        operate = operate - 10
    return (df, operate)

if __name__ == '__main__':
    df=ts.get_hist_data('601198')
    db = get_BBANDS_Status(df)
    print db[:1]
    db = get_KDJ_Status(db)
    print db[:1]
