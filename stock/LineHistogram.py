# -*- coding:utf-8 -*-
# 导入需要用到的库
# %matplotlib inline
import sys
import time
from multiprocessing import Process

import numpy as np
import pandas as pd
import statsmodels.api as sm
from pylab import plt
from sklearn.linear_model import LinearRegression
from statsmodels import regression

from JohhnsonUtil import LoggerFactory as LoggerFactory
from JohhnsonUtil import commonTips as cct
from JohhnsonUtil import zoompan

log = LoggerFactory.getLogger('Linehistogram')
# log.setLevel(LoggerFactory.DEBUG)
from JSONData import tdx_data_Day as tdd


# 取得股票的价格
# start = '2015-09-05'
# end = '2016-01-04'
# start = '2015-06-05'
# end = '2016-01-13'
# code = '300191'
# code = '000738'

def LIS(X):
    N = len(X)
    P = [0] * N
    M = [0] * (N + 1)
    L = 0
    for i in range(N):
        lo = 1
        hi = L
        while lo <= hi:
            mid = (lo + hi) // 2
            if (X[M[mid]] < X[i]):
                lo = mid + 1
            else:
                hi = mid - 1

        newL = lo
        P[i] = M[newL - 1]
        M[newL] = i

        if (newL > L):
            L = newL

    S = []
    pos = []
    k = M[L]
    for i in range(L - 1, -1, -1):
        S.append(X[k])
        pos.append(k)
        k = P[k]
    return S[::-1], pos[::-1]


def get_linear_model_status(code, ptype='f', dtype='d',type='l', start=None, end=None):
    df = tdd.get_tdx_append_now_df(code, ptype, start, end).sort_index(ascending=True)
    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)
    # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
    asset = df['close']
    log.info("df:%s" % asset[:1])
    asset = asset.dropna()
    X = np.arange(len(asset))
    x = sm.add_constant(X)
    model = regression.linear_model.OLS(asset, x).fit()
    a = model.params[0]
    b = model.params[1]
    log.info("X:%s a:%s b:%s" % (len(asset), a, b))
    Y_hat = X * b + a
    if Y_hat[-1] > Y_hat[1]:
        log.debug("u:%s" % Y_hat[-1])
        log.debug("price:" % asset.iat[-1])
        if type.upper() == 'M':
            diff = asset.iat[-1] - Y_hat[-1]
            if diff > 0:
                return True, len(asset), diff
            else:
                return False, len(asset), diff
        elif type.upper() == 'L':
            i = (asset.values.T - Y_hat).argmin()
            c_low = X[i] * b + a - asset.values[i]
            Y_hatlow = X * b + a - c_low
            diff = asset.iat[-1] - Y_hatlow[-1]
            if asset.iat[-1] - Y_hatlow[-1] > 0:
                return True, len(asset), diff
            else:
                return False, len(asset), diff
    else:
        log.debug("d:%s" % Y_hat[1])
        return False, 0, 0
    return False, 0, 0


def get_linear_model_histogram(code, ptype='f', dtype='d', start=None, end=None,vtype='close'):
    # 399001','cyb':'zs399006','zxb':'zs399005
    # code = '999999'
    # code = '601608'
    # code = '000002'
    # asset = ts.get_hist_data(code)['close'].sort_index(ascending=True)
    # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
    # vtype='close'
    df = tdd.get_tdx_append_now_df(code, ptype, start, end).sort_index(ascending=True)
    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)
    asset = df[vtype]
    log.info("df:%s" % asset[:1])
    asset = asset.dropna()
    dates = asset.index

    if not code.startswith('999') or not code.startswith('399'):
        if code[:1] in ['5', '6','9']:
            code2='999999'
        elif code[:1] in ['3']:
            code2='399006'
        else:
            code2='399001'
        df1 = tdd.get_tdx_append_now_df(code2, ptype, start, end).sort_index(ascending=True)
        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(df1, dtype).sort_index(ascending=True)
        asset1 = df1.loc[asset.index,vtype]
        startv=asset1[:1]
        # asset_v=asset[:1]
        # print startv,asset_v
        asset1=asset1.apply(lambda x:round( x/asset1[:1],2))
        # print asset1[:4]
    
    # 画出价格随时间变化的图像
    # _, ax = plt.subplots()
    # fig = plt.figure()
    fig = plt.figure(figsize=(16, 10))
    # fig = plt.figure(figsize=(16, 10), dpi=72)

    # plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95, wspace=0.15, hspace=0.25)
    # set (gca,'Position',[0,0,512,512])
    # fig.set_size_inches(18.5, 10.5)
    # fig=plt.fig(figsize=(14,8))
    ax1 = fig.add_subplot(321)
    # asset=asset.apply(lambda x:round( x/asset[:1],2))
    ax1.plot(asset)
    # ax1.plot(asset1,'-r', linewidth=2)
    ticks = ax1.get_xticks()
    ax1.set_xticklabels([dates[i] for i in ticks[:-1]])  # Label x-axis with dates

    # 拟合
    X = np.arange(len(asset))
    x = sm.add_constant(X)
    model = regression.linear_model.OLS(asset, x).fit()
    a = model.params[0]
    b = model.params[1]
    # log.info("a:%s b:%s" % (a, b))
    log.info("X:%s a:%s b:%s" % (len(asset), a, b))
    Y_hat = X * b + a

    # 真实值-拟合值，差值最大最小作为价值波动区间
    # 向下平移
    i = (asset.values.T - Y_hat).argmin()
    c_low = X[i] * b + a - asset.values[i]
    Y_hatlow = X * b + a - c_low

    # 向上平移
    i = (asset.values.T - Y_hat).argmax()
    c_high = X[i] * b + a - asset.values[i]
    Y_hathigh = X * b + a - c_high
    plt.plot(X, Y_hat, 'k', alpha=0.9);
    plt.plot(X, Y_hatlow, 'r', alpha=0.9);
    plt.plot(X, Y_hathigh, 'r', alpha=0.9);
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price', fontsize=14)
    plt.title(code, fontsize=14)
    plt.grid(True)

    # plt.legend([code]);
    # plt.legend([code, 'Value center line', 'Value interval line']);
    # fig=plt.fig()
    # fig.figsize = [14,8]
    scale = 1.1
    zp = zoompan.ZoomPan()
    figZoom = zp.zoom_factory(ax1, base_scale=scale)
    figPan = zp.pan_factory(ax1)

    ax2 = fig.add_subplot(323)
    ticks = ax2.get_xticks()
    ax2.set_xticklabels([dates[i] for i in ticks[:-1]])
    # plt.plot(X, Y_hat, 'k', alpha=0.9)
    n = 5
    d = (-c_high + c_low) / n
    c = c_high
    while c <= c_low:
        Y = X * b + a - c
        plt.plot(X, Y, 'r', alpha=0.9);
        c = c + d
    # asset=asset.apply(lambda x:round(x/asset[:1],2))
    ax2.plot(asset)
    # ax2.plot(asset1,'-r', linewidth=2)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price', fontsize=14)
    plt.grid(True)

    # plt.title(code, fontsize=14)
    # plt.legend([code])

    # 将Y-Y_hat股价偏离中枢线的距离单画出一张图显示，对其边界线之间的区域进行均分，大于0的区间为高估，小于0的区间为低估，0为价值中枢线。
    ax3 = fig.add_subplot(322)
    # distance = (asset.values.T - Y_hat)
    distance = (asset.values.T-Y_hat)[0]
    if code.startswith('999') or code.startswith('399'):
        ax3.plot(asset)
        plt.plot(distance)
        ticks = ax3.get_xticks()
        ax3.set_xticklabels([dates[i] for i in ticks[:-1]])
        n = 5
        d = (-c_high + c_low) / n
        c = c_high
        while c <= c_low:
            Y = X * b + a - c
            plt.plot(X, Y - Y_hat, 'r', alpha=0.9);
            c = c + d
        ax3.plot(asset)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Price-center price', fontsize=14)
        plt.grid(True)
    else:
        as3=asset.apply(lambda x:round(x/asset[:1],2))
        ax3.plot(as3)
        ax3.plot(asset1,'-r', linewidth=2)
        plt.grid(True)
        zp3 = zoompan.ZoomPan()
        figZoom = zp3.zoom_factory(ax3, base_scale=scale)
        figPan = zp3.pan_factory(ax3)
    # plt.title(code, fontsize=14)
    # plt.legend([code])

    
    
    # 统计出每个区域内各股价的频数，得到直方图，为了更精细的显示各个区域的频数，这里将整个边界区间分成100份。

    ax4 = fig.add_subplot(325)
    log.info("assert:len:%s %s" % (len(asset.values.T - Y_hat), (asset.values.T - Y_hat)[0]))
    # distance = map(lambda x:int(x),(asset.values.T - Y_hat)/Y_hat*100)
    # now_distanse=int((asset.iat[-1]-Y_hat[-1])/Y_hat[-1]*100)
    # log.debug("dis:%s now:%s"%(distance[:2],now_distanse))
    # log.debug("now_distanse:%s"%now_distanse)
    distance = (asset.values.T - Y_hat)
    now_distanse = asset.iat[-1] - Y_hat[-1]
    # distance = (asset.values.T-Y_hat)[0]
    pd.Series(distance).plot(kind='hist', stacked=True, bins=100)
    # plt.plot((asset.iat[-1].T-Y_hat),'b',alpha=0.9)
    plt.axvline(now_distanse, hold=None, label="1", color='red')
    # plt.axhline(now_distanse,hold=None,label="1",color='red')
    # plt.axvline(asset.iat[0],hold=None,label="1",color='red',linestyle="--")
    plt.xlabel('Undervalue ------------------------------------------> Overvalue', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    # plt.title('Undervalue & Overvalue Statistical Chart', fontsize=14)
    plt.legend([code, asset.iat[-1]])
    plt.grid(True)

    # plt.show()
    # import os
    # print(os.path.abspath(os.path.curdir))


    ax5 = fig.add_subplot(326)
    # fig.figsize=(5, 10)
    log.info("assert:len:%s %s" % (len(asset.values.T - Y_hat), (asset.values.T - Y_hat)[0]))
    # distance = map(lambda x:int(x),(asset.values.T - Y_hat)/Y_hat*100)
    distance = (asset.values.T - Y_hat) / Y_hat * 100
    now_distanse = ((asset.iat[-1] - Y_hat[-1]) / Y_hat[-1] * 100)
    log.debug("dis:%s now:%s" % (distance[:2], now_distanse))
    log.debug("now_distanse:%s" % now_distanse)
    # n, bins = np.histogram(distance, 50)
    # print n, bins[:2]
    pd.Series(distance).plot(kind='hist', stacked=True, bins=100)
    # plt.plot((asset.iat[-1].T-Y_hat),'b',alpha=0.9)
    plt.axvline(now_distanse, hold=None, label="1", color='red')
    # plt.axhline(now_distanse,hold=None,label="1",color='red')
    # plt.axvline(asset.iat[0],hold=None,label="1",color='red',linestyle="--")
    plt.xlabel('Undervalue ------------------------------------------> Overvalue', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    # plt.title('Undervalue & Overvalue Statistical Chart', fontsize=14)
    plt.legend([code, asset.iat[-1]])
    plt.grid(True)

    ax6 = fig.add_subplot(324)
    h = df.loc[:, ['open', 'close', 'high', 'low']]
    highp = h['high'].values
    lowp = h['low'].values
    openp = h['open'].values
    closep = h['close'].values
    lr = LinearRegression()
    x = np.atleast_2d(np.linspace(0, len(closep), len(closep))).T
    lr.fit(x, closep)
    LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
    xt = np.atleast_2d(np.linspace(0, len(closep) + 200, len(closep) + 200)).T
    yt = lr.predict(xt)
    bV = []
    bP = []
    for i in range(1, len(highp) - 1):
        if highp[i] <= highp[i - 1] and highp[i] < highp[i + 1] and lowp[i] <= lowp[i - 1] and lowp[i] < lowp[i + 1]:
            bV.append(lowp[i])
            bP.append(i)

    d, p = LIS(bV)

    idx = []
    for i in range(len(p)):
        idx.append(bP[p[i]])
    lr = LinearRegression()
    X = np.atleast_2d(np.array(idx)).T
    Y = np.array(d)
    lr.fit(X, Y)
    estV = lr.predict(xt)
    ax6.plot(closep, linewidth=2)
    ax6.plot(idx, d, 'ko')
    ax6.plot(xt, estV, '-r', linewidth=3)
    ax6.plot(xt, yt, '-g', linewidth=3)
    plt.grid(True)

    # plt.tight_layout()
    zp2 = zoompan.ZoomPan()
    figZoom = zp2.zoom_factory(ax6, base_scale=scale)
    figPan = zp2.pan_factory(ax6)
    plt.show()

def get_linear_model_histogramDouble(code, ptype='f', dtype='d', start=None, end=None,vtype='close',filter='n'):
    # 399001','cyb':'zs399006','zxb':'zs399005
    # code = '999999'
    # code = '601608'
    # code = '000002'
    # asset = ts.get_hist_data(code)['close'].sort_index(ascending=True)
    # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
    # vtype='close'
    # if vtype == 'close' or vtype==''
        # ptype=

    if start is not None and filter=='y':
        if code not in ['999999','399006','399001']:
            index_d,dl=tdd.get_duration_Index_date(dt=start)
            log.debug("index_d:%s dl:%s"%(str(index_d),dl))
        else:
            index_d=cct.day8_to_day10(start)
            log.debug("index_d:%s"%(index_d))
        start=tdd.get_duration_price_date(code,ptype='low',dt=index_d)
        log.debug("start:%s"%(start))
    log.debug("start:%s" % (start))

    df = tdd.get_tdx_append_now_df(code, ptype, start, end).sort_index(ascending=True)
    log.debug("df:%s" % (len(df)))

    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)
    asset = df[vtype]
    log.info("df:%s" % asset[:1])
    asset = asset.dropna()
    dates = asset.index
    if not code.startswith('999') or not code.startswith('399'):
        if code[:1] in ['5', '6','9']:
            code2='999999'
        elif code[:1] in ['3']:
            code2='399006'
        else:
            code2='399001'
        df1 = tdd.get_tdx_append_now_df(code2, ptype, start, end).sort_index(ascending=True)
        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(df1, dtype).sort_index(ascending=True)
        asset1 = df1.loc[asset.index,vtype]
        startv=asset1[:1]
        # asset_v=asset[:1]
        # print startv,asset_v
        asset1=asset1.apply(lambda x:round( x/asset1[:1],2))
        # print asset1[:4]
    # 画出价格随时间变化的图像
    # _, ax = plt.subplots()
    # fig = plt.figure()
    fig = plt.figure(figsize=(16, 10))
    # fig = plt.figure(figsize=(16, 10), dpi=72)

    # plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95, wspace=0.15, hspace=0.25)
    # set (gca,'Position',[0,0,512,512])
    # fig.set_size_inches(18.5, 10.5)
    # fig=plt.fig(figsize=(14,8))
    ax1 = fig.add_subplot(321)
    # asset=asset.apply(lambda x:round( x/asset[:1],2))
    ax1.plot(asset)
    # ax1.plot(asset1,'-r', linewidth=2)
    ticks = ax1.get_xticks()
    ax1.set_xticklabels([dates[i] for i in ticks[:-1]])  # Label x-axis with dates

    # 拟合
    X = np.arange(len(asset))
    x = sm.add_constant(X)
    model = regression.linear_model.OLS(asset, x).fit()
    a = model.params[0]
    b = model.params[1]
    # log.info("a:%s b:%s" % (a, b))
    log.info("X:%s a:%s b:%s" % (len(asset), a, b))
    Y_hat = X * b + a

    # 真实值-拟合值，差值最大最小作为价值波动区间
    # 向下平移
    i = (asset.values.T - Y_hat).argmin()
    c_low = X[i] * b + a - asset.values[i]
    Y_hatlow = X * b + a - c_low

    # 向上平移
    i = (asset.values.T - Y_hat).argmax()
    c_high = X[i] * b + a - asset.values[i]
    Y_hathigh = X * b + a - c_high
    plt.plot(X, Y_hat, 'k', alpha=0.9);
    plt.plot(X, Y_hatlow, 'r', alpha=0.9);
    plt.plot(X, Y_hathigh, 'r', alpha=0.9);
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price', fontsize=14)
    plt.title(code, fontsize=14)
    plt.grid(True)

    # plt.legend([code]);
    # plt.legend([code, 'Value center line', 'Value interval line']);
    # fig=plt.fig()
    # fig.figsize = [14,8]
    scale = 1.1
    zp = zoompan.ZoomPan()
    figZoom = zp.zoom_factory(ax1, base_scale=scale)
    figPan = zp.pan_factory(ax1)

    ax2 = fig.add_subplot(323)
    ticks = ax2.get_xticks()
    ax2.set_xticklabels([dates[i] for i in ticks[:-1]])
    # plt.plot(X, Y_hat, 'k', alpha=0.9)
    n = 5
    d = (-c_high + c_low) / n
    c = c_high
    while c <= c_low:
        Y = X * b + a - c
        plt.plot(X, Y, 'r', alpha=0.9);
        c = c + d
    # asset=asset.apply(lambda x:round(x/asset[:1],2))
    ax2.plot(asset)
    # ax2.plot(asset1,'-r', linewidth=2)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price', fontsize=14)
    plt.grid(True)

    # plt.title(code, fontsize=14)
    # plt.legend([code])

    # 将Y-Y_hat股价偏离中枢线的距离单画出一张图显示，对其边界线之间的区域进行均分，大于0的区间为高估，小于0的区间为低估，0为价值中枢线。
    ax3 = fig.add_subplot(322)
    # distance = (asset.values.T - Y_hat)
    distance = (asset.values.T-Y_hat)[0]
    if code.startswith('999') or code.startswith('399'):
        ax3.plot(asset)
        plt.plot(distance)
        ticks = ax3.get_xticks()
        ax3.set_xticklabels([dates[i] for i in ticks[:-1]])
        n = 5
        d = (-c_high + c_low) / n
        c = c_high
        while c <= c_low:
            Y = X * b + a - c
            plt.plot(X, Y - Y_hat, 'r', alpha=0.9);
            c = c + d
        ax3.plot(asset)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Price-center price', fontsize=14)
        plt.grid(True)
    else:
        as3=asset.apply(lambda x:round(x/asset[:1],2))
        ax3.plot(as3)
        ax3.plot(asset1,'-r', linewidth=2)
        plt.grid(True)
        zp3 = zoompan.ZoomPan()
        figZoom = zp3.zoom_factory(ax3, base_scale=scale)
        figPan = zp3.pan_factory(ax3)
    # plt.title(code, fontsize=14)
    # plt.legend([code])

    
    
    # 统计出每个区域内各股价的频数，得到直方图，为了更精细的显示各个区域的频数，这里将整个边界区间分成100份。

    ax4 = fig.add_subplot(325)
    log.info("assert:len:%s %s" % (len(asset.values.T - Y_hat), (asset.values.T - Y_hat)[0]))
    # distance = map(lambda x:int(x),(asset.values.T - Y_hat)/Y_hat*100)
    # now_distanse=int((asset.iat[-1]-Y_hat[-1])/Y_hat[-1]*100)
    # log.debug("dis:%s now:%s"%(distance[:2],now_distanse))
    # log.debug("now_distanse:%s"%now_distanse)
    distance = (asset.values.T - Y_hat)
    now_distanse = asset.iat[-1] - Y_hat[-1]
    # distance = (asset.values.T-Y_hat)[0]
    pd.Series(distance).plot(kind='hist', stacked=True, bins=100)
    # plt.plot((asset.iat[-1].T-Y_hat),'b',alpha=0.9)
    plt.axvline(now_distanse, hold=None, label="1", color='red')
    # plt.axhline(now_distanse,hold=None,label="1",color='red')
    # plt.axvline(asset.iat[0],hold=None,label="1",color='red',linestyle="--")
    plt.xlabel('Undervalue ------------------------------------------> Overvalue', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    # plt.title('Undervalue & Overvalue Statistical Chart', fontsize=14)
    plt.legend([code, asset.iat[-1]])
    plt.grid(True)

    # plt.show()
    # import os
    # print(os.path.abspath(os.path.curdir))


    ax5 = fig.add_subplot(326)
    # fig.figsize=(5, 10)
    log.info("assert:len:%s %s" % (len(asset.values.T - Y_hat), (asset.values.T - Y_hat)[0]))
    # distance = map(lambda x:int(x),(asset.values.T - Y_hat)/Y_hat*100)
    distance = (asset.values.T - Y_hat) / Y_hat * 100
    now_distanse = ((asset.iat[-1] - Y_hat[-1]) / Y_hat[-1] * 100)
    log.debug("dis:%s now:%s" % (distance[:2], now_distanse))
    log.debug("now_distanse:%s" % now_distanse)
    # n, bins = np.histogram(distance, 50)
    # print n, bins[:2]
    pd.Series(distance).plot(kind='hist', stacked=True, bins=100)
    # plt.plot((asset.iat[-1].T-Y_hat),'b',alpha=0.9)
    plt.axvline(now_distanse, hold=None, label="1", color='red')
    # plt.axhline(now_distanse,hold=None,label="1",color='red')
    # plt.axvline(asset.iat[0],hold=None,label="1",color='red',linestyle="--")
    plt.xlabel('Undervalue ------------------------------------------> Overvalue', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    # plt.title('Undervalue & Overvalue Statistical Chart', fontsize=14)
    plt.legend([code, asset.iat[-1]])
    plt.grid(True)

    ax6 = fig.add_subplot(324)
    h = df.loc[:, ['open', 'close', 'high', 'low']]
    highp = h['high'].values
    lowp = h['low'].values
    openp = h['open'].values
    closep = h['close'].values
    lr = LinearRegression()
    x = np.atleast_2d(np.linspace(0, len(closep), len(closep))).T
    lr.fit(x, closep)
    LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
    xt = np.atleast_2d(np.linspace(0, len(closep) + 200, len(closep) + 200)).T
    yt = lr.predict(xt)
    bV = []
    bP = []
    for i in range(1, len(highp) - 1):
        if highp[i] <= highp[i - 1] and highp[i] < highp[i + 1] and lowp[i] <= lowp[i - 1] and lowp[i] < lowp[i + 1]:
            bV.append(lowp[i])
            bP.append(i)

    d, p = LIS(bV)

    idx = []
    for i in range(len(p)):
        idx.append(bP[p[i]])
    lr = LinearRegression()
    X = np.atleast_2d(np.array(idx)).T
    Y = np.array(d)
    lr.fit(X, Y)
    estV = lr.predict(xt)
    ax6.plot(closep, linewidth=2)
    ax6.plot(idx, d, 'ko')
    ax6.plot(xt, estV, '-r', linewidth=3)
    ax6.plot(xt, yt, '-g', linewidth=3)
    plt.grid(True)

    # plt.tight_layout()
    zp2 = zoompan.ZoomPan()
    figZoom = zp2.zoom_factory(ax6, base_scale=scale)
    figPan = zp2.pan_factory(ax6)
    plt.show()
def parseArgmain():
    # from ConfigParser import ConfigParser
    # import shlex
    import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--start', type=int, dest='start',
    # help='Start date', required=True)
    # parser.add_argument('-e', '--end', type=int, dest='end',
    # help='End date', required=True)
    # parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
    # help='Enable debug info')
    # parser.add_argument('foo', type=int, choices=xrange(5, 10))
    # args = parser.parse_args()
    # print args.square**2
    parser = argparse.ArgumentParser()
    # parser = argparse.ArgumentParser(description='LinearRegression Show')
    parser.add_argument('code', type=str, nargs='?', help='999999')
    parser.add_argument('start', nargs='?', type=str, help='20150612')
    # parser.add_argument('e', nargs='?',action="store", dest="end", type=str, help='end')
    parser.add_argument('end', nargs='?', type=str, help='20160101')
    parser.add_argument('-d', action="store", dest="dtype", type=str, nargs='?', choices=['d', 'w', 'm'], default='d',
                        help='DateType')
    parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['f', 'b'], default='f',
                        help='Price Forward or back')
    # parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low','open','close'], default='close',
    parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low','close'], default='close',
                        help='type')
    parser.add_argument('-f', action="store", dest="filter", type=str, choices=['y', 'n'], default='n',
                        help='find duration low')                              
    # parser.add_argument('-help',type=str,help='Price Forward or back')
    # args = parser.parse_args()
    # args=parser.parse_args(input)
    return parser
    # def getArgs():
    # parse=argparse.ArgumentParser()
    # parse.add_argument('-u',type=str)
    # parse.add_argument('-d',type=str)
    # parse.add_argument('-o',type=str)
    # args=parse.parse_args()
    # return vars(args)
    # if args.verbose:
    # logger.setLevel(logging.DEBUG)
    # else:
    # logger.setLevel(logging.ERROR)


if __name__ == "__main__":
    # status=get_linear_model_status('601198')
    # print status
    # get_tdx_and_now_data('002399')
    # sys.exit(0)

    # args=main(raw_input('input').split())
    # print (args.d)
    # sys.exit()

    cct.set_console(100, 15)
    num_input = ''
    if len(sys.argv) == 2:
        num_input = sys.argv[1]
    elif (len(sys.argv) > 2):
        print ("argv error")
        sys.exit(0)

    # else:
    #     print ("please input code:")
    #     sys.exit(0)
    # num_input = '601608'
    # num_input=raw_input("Please input code:")
    parser = parseArgmain()
    parser.print_help()
    while 1:
        try:
            if not len(num_input) == 6:
                num_input = raw_input("please input code:")
                if len(num_input) > 0:
                    args = parser.parse_args(num_input.split())
                    num_input = args.code
                    # print args.code,args.ptype,args.dtype,
                    start = cct.day8_to_day10(args.start)
                    end = cct.day8_to_day10(args.end)
                    # print start,end
                if num_input == 'ex' or num_input == 'qu' \
                        or num_input == 'q' or num_input == "e":
                    sys.exit()
                elif len(num_input) == 6:
                    code = args.code
                    # print code, args.ptype, args.dtype, start, end
                    # get_linear_model_histogram(code, args.ptype, args.dtype, start, end,args.vtype)
                    # queue = Queue()
                    p = Process(target=get_linear_model_histogramDouble,
                                args=(code, args.ptype, args.dtype, start, end, args.vtype, args.filter,))
                    # multiprocessing.Process(target=get_linear_model_histogramDouble,args=(code, args.ptype, args.dtype, start, end,args.vtype,args.filter))
                    p.daemon = True
                    p.start()
                    p.join()

                    # import threading
                    # t = threading.Thread(name='tmp',target=get_linear_model_histogramDouble,args=(code, args.ptype, args.dtype, start, end,args.vtype,args.filter,))
                    # t.setDaemon(True)
                    # t.start()

                    time.sleep(5)
                    num_input = ''

                    #         else:
                    #             get_linear_model_histogram(code,args.dtype,args.start)
                    #     elif args.end:
                    #         get_linear_model_histogram(code,args.dtype,end=args.end)
                    #     else:
                    #         get_linear_model_histogram(code,args.dtype)
                    # num_input = ''
                    # elif len(num_input) == 6:
                    # get_linear_model_histogram(num_input)
                    # elif len(num_input) == 8:
                    # data=num_input.split(' ')
                    # if len(data)>2:
                    # code=data[0]
                    # type=data[1]
                    # if type in ['d','w','m']:
                    # get_linear_model_histogram(code,type)
                    # num_input = ''
                    # elif len(num_input) > 8:
                    # data=num_input.split(' ')
                    # if len(data)==3:
                    # code=data[0]
                    # type=data[1]
                    # start=data[2]
                    # if type in ['d','w','m']:
                    # get_linear_model_histogram(code,type)
                    # num_input = ''
                    # else:
                    # get_linear_model_histogram(code)
                    # else:
                    # get_linear_model_histogram(num_input)
                    # num_input = ''
        except (KeyboardInterrupt) as e:
            print "KeyboardInterrupt:", e
            st = raw_input("status:[go(g),clear(c),quit(q,e)]:")
            if st == 'q' or st == 'e':
                sys.exit(0)
            else:
            	num_input=''
        except (IOError, EOFError, Exception) as e:
            print "Error:", e
            import traceback
            traceback.print_exc()
            # st = raw_input("status:[go(g),clear(c),quit(q,e)]:")
            # if st == 'q' or st == 'e':
            #     sys.exit(0)
            # else:
            num_input=''
