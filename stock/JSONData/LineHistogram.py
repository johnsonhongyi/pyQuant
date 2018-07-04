# -*- coding:utf-8 -*-
# 导入需要用到的库
# %matplotlib inline
import datetime
import sys

import numpy as np
import pandas as pd
from statsmodels import api as sm
from matplotlib.dates import num2date, date2num
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib import transforms
from pylab import plt, mpl
from sklearn.linear_model import LinearRegression
from statsmodels import regression

import powerCompute as pct
from JohnsonUtil import LoggerFactory as LoggerFactory
from JohnsonUtil import commonTips as cct
from JohnsonUtil import zoompan

# log = LoggerFactory.getLogger('Linehistogram')
log = LoggerFactory.log
# log.setLevel(LoggerFactory.DEBUG)
from JSONData import tdx_data_Day as tdd

if cct.isMac():
    # mpl.rcParams['font.sans-serif'] = ['STHeiti']
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
else:
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False


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


# def get_linear_model_status(code, ptype='low', dtype='d', type='l', start=None, end=None):
#     # df = tdd.get_tdx_append_now_df(code, ptype, start, end).sort_index(ascending=True)
#     df = tdd.get_tdx_append_now_df_api(code, start, end).sort_index(ascending=True)
#     # print start,end,df.index.values[:1],df.index.values[-1:]
#     if len(df) < 2:
#         return False, 0, 0
#     if not dtype == 'd':
#         df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)
#     # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
#     asset = df['close']
#     log.info("df:%s" % asset[:1])
#     asset = asset.dropna()
#     X = np.arange(len(asset))
#     x = sm.add_constant(X)
#     model = regression.linear_model.OLS(asset, x).fit()
#     a = model.params[0]
#     b = model.params[1]
#     log.info("X:%s a:%s b:%s" % (len(asset), a, b))
#     Y_hat = X * b + a
#     if Y_hat[-1] > Y_hat[1]:
#         log.debug("u:%s" % Y_hat[-1])
#         log.debug("price:" % asset.iat[-1])
#         if type.upper() == 'M':
#             diff = asset.iat[-1] - Y_hat[-1]
#             if diff > 0:
#                 return True, len(asset), diff
#             else:
#                 return False, len(asset), diff
#         elif type.upper() == 'L':
#             i = (asset.values.T - Y_hat).argmin()
#             c_low = X[i] * b + a - asset.values[i]
#             Y_hatlow = X * b + a - c_low
#             diff = asset.iat[-1] - Y_hatlow[-1]
#             if asset.iat[-1] - Y_hatlow[-1] > 0:
#                 return True, len(asset), diff
#             else:
#                 return False, len(asset), diff
#     else:
#         log.debug("d:%s" % Y_hat[1])
#         return False, 0, 0
#     return False, 0, 0


def get_linear_model_histogramDouble(code, ptype='low', dtype='d', start=None, end=None, vtype='f', filter='n',
                                     df=None,dl=None):
    # 399001','cyb':'zs399006','zxb':'zs399005
    # code = '999999'
    # code = '601608'
    # code = '000002'
    # asset = get_kdate_data(code)['close'].sort_index(ascending=True)
    # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
    # ptype='close'
    # if ptype == 'close' or ptype==''
    # ptype=
    if start is not None and filter == 'y':
        if code not in ['999999', '399006', '399001']:
            index_d, dl = tdd.get_duration_Index_date(dt=start)
            log.debug("index_d:%s dl:%s" % (str(index_d), dl))
        else:
            index_d = cct.day8_to_day10(start)
            log.debug("index_d:%s" % (index_d))
        start = tdd.get_duration_price_date(code, ptype='low', dt=index_d)
        log.debug("start:%s" % (start))

    if start is None and df is None and dl is not None:
        start = cct.last_tddate(dl)
        # print start
        df = tdd.get_tdx_append_now_df_api(code, start=start, end=end).sort_index(ascending=True)


    if df is None:
        # df = tdd.get_tdx_append_now_df(code, ptype, start, end).sort_index(ascending=True)
        df = tdd.get_tdx_append_now_df_api(code, start, end).sort_index(ascending=True)
    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)

    asset = df[ptype].round(2)
    log.info("df:%s" % asset[:1])
    asset = asset.dropna()
    dates = asset.index

    if not code.startswith('999') and not code.startswith('399'):
        # print "code:",code
        if code[:1] in ['5', '6', '9']:
            code2 = '999999'
        elif code[:2] in ['30']:
            # print "cyb"
            code2 = '399006'
        else:
            code2 = '399001'
        df1 = tdd.get_tdx_append_now_df_api(code2, start, end).sort_index(ascending=True)
        # df1 = tdd.get_tdx_append_now_df(code2, ptype, start, end).sort_index(ascending=True)
        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(df1, dtype).sort_index(ascending=True)
            # if len(asset) < len(df1):
            # asset1 = df1.loc[asset.index, ptype]
            # else:
            # asset1 = df1.loc[asset.index, ptype]
        # startv = asset1[:1]
        # asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
        # print asset[:1].index[0] , df1[:1].index[0]
        if asset[:1].index[0] > df1[:1].index[0]:
            asset1 = df1.loc[asset.index, ptype]
            startv = asset1[:1]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
        else:
            df = df[df.index >= df1.index[0]]
            asset = df[ptype]
            asset = asset.dropna()
            dates = asset.index
            asset1 = df1.loc[df.index, ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))

    else:
        if code.startswith('399001'):
            code2 = '399006'
        elif code.startswith('399006'):
            code2 = '399005'
        else:
            code2 = '399006'
        if code2.startswith('3990'):
            df1 = tdd.get_tdx_append_now_df_api(code2, start, end).sort_index(ascending=True)
            if len(df1) < int(len(df) / 4):
                code2 = '399001'
                df1 = tdd.get_tdx_append_now_df_api(code2, start, end).sort_index(ascending=True)

        # df1 = tdd.get_tdx_append_now_df(code2, ptype, start, end).sort_index(ascending=True)
        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(df1, dtype).sort_index(ascending=True)
        if len(asset) < len(df1):
            asset1 = df1.loc[asset.index, ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
        else:

            df = df[df.index >= df1.index[0]]
            asset = df[ptype]
            asset = asset.dropna()
            dates = asset.index
            asset1 = df1.loc[df.index, ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
    # print len(df),len(asset),len(df1),len(asset1)

    if end is not None:
        # print asset[-1:]
        asset = asset[:-1]
        dates = asset.index
        asset1 = asset1[:-1]
        asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))

    # 画出价格随时间变化的图像
    # _, ax = plt.subplots()
    # fig = plt.figure()
    fig = plt.figure(figsize=(16, 10))
    # fig = plt.figure(figsize=(16, 10), dpi=72)
    # fig.autofmt_xdate() #(no fact)

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
    # start, end = ax1.get_xlim()
    # print start, end, len(asset)
    # print ticks, ticks[:-1]
    # (ticks[:-1] if len(asset) > end else np.append(ticks[:-1], len(asset) - 1))

    ax1.set_xticklabels([dates[int(i)] for i in (np.append(ticks[:-1], len(asset) - 1))],
                        rotation=15)  # Label x-axis with dates
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
    # plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.title(code + " | " + str(dates[-1])[:11], fontsize=14)
    plt.legend([asset.iat[-1]], fontsize=12, loc=4)
    plt.grid(True)


    # #plot volume
    # pad = 0.25
    # yl = ax1.get_ylim()
    # ax1.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])
    # axx = ax1.twinx()
    # axx.set_position(transforms.Bbox([[0.125,0.1],[0.9,0.32]]))
    # volume = np.asarray(df.vol)
    # pos = df['open']-df['close']<0
    # neg = df['open']-df['close']>=0
    # idx = np.asarray([x for x in range(len(df))])
    # axx.bar(idx[pos],volume[pos],color='red',width=1,align='center')
    # axx.bar(idx[neg],volume[neg],color='green',width=1,align='center')

    
    # plt.legend([code]);
    # plt.legend([code, 'Value center line', 'Value interval line']);
    # fig=plt.fig()
    # fig.figsize = [14,8]
    scale = 1.1
    zp = zoompan.ZoomPan()
    figZoom = zp.zoom_factory(ax1, base_scale=scale)
    figPan = zp.pan_factory(ax1)

    # 将Y-Y_hat股价偏离中枢线的距离单画出一张图显示，对其边界线之间的区域进行均分，大于0的区间为高估，小于0的区间为低估，0为价值中枢线。
    ax3 = fig.add_subplot(322)
    # distance = (asset.values.T - Y_hat)
    distance = (asset.values.T - Y_hat)[0]
    # if code.startswith('999') or code.startswith('399'):
    if len(asset) > len(df1):
        ax3.plot(asset)
        plt.plot(distance)
        ticks = ax3.get_xticks()
        ax3.set_xticklabels([dates[int(i)] for i in (np.append(ticks[:-1], len(asset) - 1))], rotation=15)
        n = 5
        d = (-c_high + c_low) / n
        c = c_high
        while c <= c_low:
            Y = X * b + a - c
            plt.plot(X, Y - Y_hat, 'r', alpha=0.9);
            c = c + d
        ax3.plot(asset)
        ## plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price-center price', fontsize=14)
        plt.grid(True)
    else:
        as3 = asset.apply(lambda x: round(x / asset[:1], 2))
        ax3.plot(as3)
        ticks = ax3.get_xticks()
        ax3.plot(asset1, '-r', linewidth=2)

        # show volume bar !!!
        # assvol = df.loc[asset.index]['vol']
        # assvol = assvol.apply(lambda x: round(x / assvol[:1], 2))
        # ax3.plot(assvol, '-g', linewidth=0.5)


        ax3.set_xticklabels([dates[int(i)] for i in (np.append(ticks[:-1], len(asset) - 1))], rotation=15)
        plt.grid(True)
        zp3 = zoompan.ZoomPan()
        figZoom = zp3.zoom_factory(ax3, base_scale=scale)
        figPan = zp3.pan_factory(ax3)
    # plt.title(code, fontsize=14)
    if 'name' in df.columns:
        plt.legend([df.name.values[-1:][0], df1.name.values[-1:][0]], loc=0)
    else:
        plt.legend([code, code2], loc=0)

    ax2 = fig.add_subplot(323)
    # ax2.plot(asset)
    # ticks = ax2.get_xticks()
    ax2.set_xticklabels([dates[int(i)] for i in (np.append(ticks[:-1], len(asset) - 1))], rotation=15)
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
    # plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.grid(True)

    # plt.title(code, fontsize=14)
    # plt.legend([code])



    if len(df) > 10:
        ax6 = fig.add_subplot(324)
        h = df.loc[:, ['open', 'close', 'high', 'low']]
        highp = h['high'].values
        lowp = h['low'].values
        openp = h['open'].values
        closep = h['close'].values
        # print len(closep)
        lr = LinearRegression()
        x = np.atleast_2d(np.linspace(0, len(closep), len(closep))).T
        lr.fit(x, closep)
        LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
        xt = np.atleast_2d(np.linspace(0, len(closep) + 200, len(closep) + 200)).T
        yt = lr.predict(xt)
        bV = []
        bP = []
        for i in range(1, len(highp) - 1):
            if highp[i] <= highp[i - 1] and highp[i] < highp[i + 1] and lowp[i] <= lowp[i - 1] and lowp[i] < lowp[
                        i + 1]:
                bV.append(lowp[i])
                bP.append(i)
            else:
                bV.append(lowp[i-1])
                bP.append(i-1)
        if len(bV) > 0 :

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
    plt.xlabel('Undervalue ------------------------------------------> Overvalue', fontsize=12)
    plt.ylabel('Frequency', fontsize=14)
    # plt.title('Undervalue & Overvalue Statistical Chart', fontsize=14)
    plt.legend([code, asset.iat[-1], str(dates[-1])[5:11]], fontsize=12)
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
    plt.ylabel('Frequency', fontsize=12)
    # plt.title('Undervalue & Overvalue Statistical Chart', fontsize=14)
    plt.legend([code, asset.iat[-1]], fontsize=12)
    plt.grid(True)

    # plt.ion()
    plt.show(block=False)
    # print plt.get_backend()
    # plt.show()
    return df


def get_linear_model_histogram(code, ptype='low', dtype='d', start=None, end=None, vtype='f', filter='n',
                               df=None):
    # 399001','cyb':'zs399006','zxb':'zs399005
    # code = '999999'
    # code = '601608'
    # code = '000002'
    # asset = get_kdate_data(code)['close'].sort_index(ascending=True)
    # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
    # ptype='close'
    # if ptype == 'close' or ptype==''
    # ptype=

    if start is not None and filter == 'y':
        if code not in ['999999', '399006', '399001']:
            index_d, dl = tdd.get_duration_Index_date(dt=start)
            log.debug("index_d:%s dl:%s" % (str(index_d), dl))
        else:
            index_d = cct.day8_to_day10(start)
            log.debug("index_d:%s" % (index_d))
        start = tdd.get_duration_price_date(code, ptype='low', dt=index_d)
        log.debug("start:%s" % (start))
    if df is None:
        # df = tdd.get_tdx_append_now_df(code, ptype, start, end).sort_index(ascending=True)
        df = tdd.get_tdx_append_now_df_api(code, start, end).sort_index(ascending=True)
    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)
    asset = df[ptype]
    log.info("df:%s" % asset[:1])
    asset = asset.dropna()
    dates = asset.index

    if not code.startswith('999') and not code.startswith('399'):
        # print "code:",code
        if code[:1] in ['5', '6', '9']:
            code2 = '999999'
        elif code[:2] in ['30']:
            # print "cyb"
            code2 = '399006'
        else:
            code2 = '399001'
        df1 = tdd.get_tdx_append_now_df_api(code2, start, end).sort_index(ascending=True)
        # df1 = tdd.get_tdx_append_now_df(code2, ptype, start, end).sort_index(ascending=True)
        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(df1, dtype).sort_index(ascending=True)
            # if len(asset) < len(df1):
            # asset1 = df1.loc[asset.index, ptype]
            # else:
            # asset1 = df1.loc[asset.index, ptype]
        # startv = asset1[:1]
        # asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
        # print asset[:1].index[0] , df1[:1].index[0]
        if asset[:1].index[0] > df1[:1].index[0]:
            asset1 = df1.loc[asset.index, ptype]
            startv = asset1[:1]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
        else:
            df = df[df.index >= df1.index[0]]
            asset = df[ptype]
            asset = asset.dropna()
            dates = asset.index
            asset1 = df1.loc[df.index, ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))

    else:
        if code.startswith('399001'):
            code2 = '999999'
        elif code.startswith('399006'):
            code2 = '399005'
        else:
            code2 = '399001'
        df1 = tdd.get_tdx_append_now_df_api(code2, start, end).sort_index(ascending=True)
        # print df1[:1]
        # df1 = tdd.get_tdx_append_now_df(code2, ptype, start, end).sort_index(ascending=True)
        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(df1, dtype).sort_index(ascending=True)
        if len(asset) < len(df1):
            asset1 = df1.loc[asset.index, ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
        else:

            df = df[df.index >= df1.index[0]]
            asset = df[ptype]
            asset = asset.dropna()
            dates = asset.index
            asset1 = df1.loc[df.index, ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
    # print len(df),len(asset),len(df1),len(asset1)

    if end is not None:
        # print asset[-1:]
        asset = asset[:-1]
        dates = asset.index
        asset1 = asset1[:-1]
        asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))

    # 画出价格随时间变化的图像
    # _, ax = plt.subplots()
    # fig = plt.figure()
    fig = plt.figure(figsize=(16, 5))
    # fig = plt.figure(figsize=(16, 10), dpi=72)
    # fig.autofmt_xdate() #(no fact)

    # plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95, wspace=0.15, hspace=0.25)
    # set (gca,'Position',[0,0,512,512])
    # fig.set_size_inches(18.5, 10.5)
    # fig=plt.fig(figsize=(14,8))
    ax1 = fig.add_subplot(121)
    # asset=asset.apply(lambda x:round( x/asset[:1],2))
    ax1.plot(asset)
    # ax1.plot(asset1,'-r', linewidth=2)
    ticks = ax1.get_xticks()
    # start, end = ax1.get_xlim()
    # print start, end, len(asset)
    # print ticks, ticks[:-1]
    # (ticks[:-1] if len(asset) > end else np.append(ticks[:-1], len(asset) - 1))
    ax1.set_xticklabels([dates[int(i)] for i in (np.append(ticks[:-1], len(asset) - 1))],
                        rotation=15)  # Label x-axis with dates
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
    # plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.title(code + " | " + str(dates[-1])[:11], fontsize=14)
    plt.legend([asset.iat[-1]], fontsize=12, loc=4)
    plt.grid(True)

    # plt.legend([code]);
    # plt.legend([code, 'Value center line', 'Value interval line']);
    # fig=plt.fig()
    # fig.figsize = [14,8]
    scale = 1.1
    zp = zoompan.ZoomPan()
    figZoom = zp.zoom_factory(ax1, base_scale=scale)
    figPan = zp.pan_factory(ax1)

    # 将Y-Y_hat股价偏离中枢线的距离单画出一张图显示，对其边界线之间的区域进行均分，大于0的区间为高估，小于0的区间为低估，0为价值中枢线。
    ax3 = fig.add_subplot(122)
    # distance = (asset.values.T - Y_hat)
    distance = (asset.values.T - Y_hat)[0]
    # if code.startswith('999') or code.startswith('399'):
    if len(asset) > len(df1):
        ax3.plot(asset)
        plt.plot(distance)
        ticks = ax3.get_xticks()
        ax3.set_xticklabels([dates[int(i)] for i in (np.append(ticks[:-1], len(asset) - 1))], rotation=15)
        n = 5
        d = (-c_high + c_low) / n
        c = c_high
        while c <= c_low:
            Y = X * b + a - c
            plt.plot(X, Y - Y_hat, 'r', alpha=0.9);
            c = c + d
        ax3.plot(asset)
        ## plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price-center price', fontsize=14)
        plt.grid(True)
    else:
        as3 = asset.apply(lambda x: round(x / asset[:1], 2))
        ax3.plot(as3)
        ax3.plot(asset1, '-r', linewidth=2)

        # assvol = df.loc[asset.index]['vol']
        # assvol = assvol.apply(lambda x: round(x / assvol[:1], 2))
        # ax3.plot(assvol, '-g', linewidth=2)

        plt.grid(True)
        zp3 = zoompan.ZoomPan()
        figZoom = zp3.zoom_factory(ax3, base_scale=scale)
        figPan = zp3.pan_factory(ax3)
    # plt.title(code, fontsize=14)
    if 'name' in df.columns:
        plt.legend([df.name[-1], df1.name[-1]], loc=0)
    else:
        plt.legend([code, code2], loc=0)
    plt.show(block=False)
    # print plt.get_backend()
    # plt.show()


def Candlestick(ax, bars=None, quotes=None, width=0.5, colorup='k', colordown='r', alpha=1.0):
    def fooCandlestick(ax, quotes, width=0.5, colorup='k', colordown='r',
                       alpha=1.0):
        OFFSET = width / 2.0
        linewidth = width * 2
        lines = []
        boxes = []
        for q in quotes:
            # t, op, cl, hi, lo = q[:5]
            t, op, hi, lo, cl = q[:5]

            box_h = max(op, cl)
            box_l = min(op, cl)
            height = box_h - box_l

            if cl >= op:
                color = colorup
            else:
                color = colordown

            vline_lo = Line2D(
                xdata=(t, t), ydata=(lo, box_l),
                color=color,
                linewidth=linewidth,
                antialiased=True,
            )
            vline_hi = Line2D(
                xdata=(t, t), ydata=(box_h, hi),
                color=color,
                linewidth=linewidth,
                antialiased=True,
            )
            rect = Rectangle(
                xy=(t - OFFSET, box_l),
                width=width,
                height=height,
                facecolor=color,
                edgecolor=color,
            )
            rect.set_alpha(alpha)
            lines.append(vline_lo)
            lines.append(vline_hi)
            boxes.append(rect)
            ax.add_line(vline_lo)
            ax.add_line(vline_hi)
            ax.add_patch(rect)
        ax.autoscale_view()

        return lines, boxes

    date = date2num(bars.index.to_datetime().to_pydatetime())
    openp = bars['open']
    closep = bars['close']
    highp = bars['high']
    lowp = bars['low']
    # volume = bars['volume']
    data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
    for i in range(len(bars) - 1):
        data = np.append(
            data, [[date[i], openp[i], highp[i], lowp[i], closep[i], ]], axis=0)
    data = np.delete(data, 0, 0)
    # determine number of days and create a list of those days
    # print np.unique(np.trunc(data[:, 0]))
    ndays = np.unique(np.trunc(data[:, 0]), return_index=True)
    xdays = []
    for n in np.arange(len(ndays[0])):
        xdays.append(datetime.date.isoformat(num2date(data[ndays[1], 0][n])))
    # creation of new data by replacing the time array with equally spaced values.
    # this will allow to remove the gap between the days, when plotting the data
    data2 = np.hstack([np.arange(data[:, 0].size)[:, np.newaxis], data[:, 1:]])
    # print data2
    # plot the data
    # figWidth = len(data) * width
    # fig = plt.figure(figsize=(figWidth, 5))
    # fig = plt.figure(figsize=(16, 10))
    # ax = fig.add_axes([0.05, 0.1, 0.9, 0.9])
    # customization of the axis

    '''
    #custom color
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(
        axis='both', direction='out', width=2, length=8, labelsize=12, pad=8)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    '''

    # ax.grid(True, color='w')
    # ax.yaxis.label.set_color("w")
    # ax.spines['bottom'].set_color("#5998ff")
    # ax.spines['top'].set_color("#5998ff")
    # ax.spines['left'].set_color("#5998ff")
    # ax.spines['right'].set_color("#5998ff")
    # ax.tick_params(axis='y', colors='w')
    # import matplotlib.ticker as mticker
    # plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    # ax.tick_params(axis='x', colors='w')
    # plt.ylabel('Stock price and Volume')

    # set the ticks of the x axis only when starting a new day
    # (Also write the code to set a tick for every whole hour)
    div_n = len(ax.get_xticks())
    allc = len(bars.index)
    # lastd = bars.index[-1]
    if allc / div_n > 12:
        div_n = allc / 12
    ax.set_xticks(range(0, len(bars.index), div_n))
    new_xticks = [bars.index[d] for d in ax.get_xticks()]
    ax.set_xticklabels(new_xticks, rotation=30, horizontalalignment='right')
    # fig.autofmt_xdate()
    # ax.autoscale_view()
    #plot volume
    pad = 0.25
    yl = ax.get_ylim()
    ax.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])
    axx = ax.twinx()
    axx.set_position(transforms.Bbox([[0.125,0.1],[0.9,0.32]]))
    volume = np.asarray(df.vol)
    pos = df['open']-df['close']<0
    neg = df['open']-df['close']>=0
    idx = np.asarray([x for x in range(len(dates))])
    # print len(dates),len(df),ax.get_xlim(),ax.get_xticks()
    axx.bar(idx[pos],volume[pos],color='red',width=1,align='center')
    axx.bar(idx[neg],volume[neg],color='green',width=1,align='center')


    # Create the candle sticks
    fooCandlestick(ax, data2, width=width, colorup='r', colordown='g')


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
    parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['f', 'b'], default='f',
                        help='Price Forward or back')
    # parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low','open','close'], default='close',
    parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['high', 'low', 'close'], default='low',
                        help='type')
    parser.add_argument('-f', action="store", dest="filter", type=str, choices=['y', 'n'], default='n',
                        help='find duration low')
    # parser.add_argument('-help',type=str,help='Price Forward or back')
    # args = parser.parse_args()
    # args=parser.parse_args(input)
    # parser = parseArgmain()
    # args = parser.parse_args(num_input.split())

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
    return parser


if __name__ == "__main__":
    # matplotlib.use('WXAgg')
    #     plt.interactive(True)
    # status=get_linear_model_status('601198')
    # print status
    # get_tdx_and_now_data('002399')
    # sys.exit(0)

    # args=main(cct.cct_raw_input('input').split())
    # print (args.d)
    # sys.exit()
    if cct.isMac():
        cct.set_console(80, 16)
    else:
        cct.set_console(80, 16)
    num_input = ''
    parser = parseArgmain()
    if len(sys.argv) == 2:
        num_input = sys.argv[1]
        args = parser.parse_args(num_input.split())
    elif len(sys.argv) > 2:
        num_input = sys.argv[1]
        args = parser.parse_args(sys.argv[1:])
    else:
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
                    sys.exit(0)
                elif num_input == 'h' or num_input == 'help':
                    parser.print_help()
                elif len(num_input) == 6:
                    code = args.code
                    # print code, args.ptype, args.dtype, start, end
                    get_linear_model_histogramDouble(code, args.ptype, args.dtype, start, end, args.vtype, args.filter)
                    # candlestick_powercompute(code,start, end)
                    op, ra, st, days = pct.get_linear_model_status(code, start=start, end=end, filter=args.filter)
                    print "code:%s op:%s ra:%s  start:%s" % (code, op, ra, st)
                    # p=multiprocessing.Process(target=get_linear_model_histogramDouble,args=(code, args.ptype, args.dtype, start, end,args.vtype,args.filter,))
                    # p.daemon = True
                    # p.start()
                    # p.join()
                    # time.sleep(6)
                    num_input = ''

            else:
                code = args.code
                if len(code) == 6:
                    start = cct.day8_to_day10(args.start)
                    end = cct.day8_to_day10(args.end)
                    get_linear_model_histogramDouble(code, args.ptype, args.dtype, start, end, args.vtype)
                    # get_linear_model_histogramDouble(code, args.ptype, args.dtype, start, end, args.vtype)
                    # candlestick_powercompute(code,start, end)
                    op, ra, st, days = pct.get_linear_model_status(code, start=start, end=end, filter=args.filter)
                    print "code:%s op:%s ra:%s  start:%s" % (code, op, ra, st)
                    # get_linear_model_status(code, dtype=args.dtype, start=start, end=end, filter=args.filter,dl=args.dl)
                sys.exit(0)

        except (KeyboardInterrupt) as e:
            print "KeyboardInterrupt:", e
            st = cct.cct_raw_input("status:[go(g),clear(c),quit(q,e)]:")
            if st == 'q' or st == 'e':
                sys.exit(0)
            else:
                num_input = ''
        except (IOError, EOFError, Exception) as e:
            print "Exception:", e
            import traceback

            traceback.print_exc()
            # st = cct.cct_raw_input("status:[go(g),clear(c),quit(q,e)]:")
            # if st == 'q' or st == 'e':
            #     sys.exit(0)
            # else:
            num_input = ''
