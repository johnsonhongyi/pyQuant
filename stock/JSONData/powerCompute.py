# -*- coding:utf-8 -*-
import sys

sys.path.append("..")

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels import regression
from pylab import plt, mpl
from matplotlib.dates import num2date, date2num
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import datetime
from JohhnsonUtil import commonTips as cct
from JSONData import tdx_data_Day as tdd
from JSONData import get_macd_kdj_rsi as getab
from JohhnsonUtil import zoompan
from JohhnsonUtil import LoggerFactory as LoggerFactory
import time
log = LoggerFactory.getLogger("PowerCompute")
# log.setLevel(LoggerFactory.INFO)

if not cct.isMac():
    def set_ctrl_handler():
        import win32api
        import thread
        # def doSaneThing(sig, func=None):
        # '''忽略所有KeyCtrl'''
        # return True
        # win32api.SetConsoleCtrlHandler(doSaneThing, 1)

        def handler(dwCtrlType, hook_sigint=thread.interrupt_main):
            # print ("ctrl:%s"%(dwCtrlType))
            if dwCtrlType == 0:  # CTRL_C_EVENT
                hook_sigint()
                # raise KeyboardInterrupt("CTRL-C!")
                return 1  # don't chain to the next handler
            return 0  # chain to the next handler

        win32api.SetConsoleCtrlHandler(handler, 1)


    set_ctrl_handler()

if cct.isMac():
    mpl.rcParams['font.sans-serif'] = ['STHeiti']
    mpl.rcParams['axes.unicode_minus'] = False
else:
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False


# import signal
# def signal_handler(sig, frame):
#     print('Received signal {signal}'.format(signal=sig))
#
# signal.signal(signal.SIGINT, signal_handler)
# print('Press the stop button.')
# signal.pause()
# ȡ�ù�Ʊ�ļ۸�
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
            mid = (lo + hi) / 2
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
                antialiased=True, )
            vline_hi = Line2D(
                xdata=(t, t), ydata=(box_h, hi),
                color=color,
                linewidth=linewidth,
                antialiased=True, )
            rect = Rectangle(
                xy=(t - OFFSET, box_l),
                width=width,
                height=height,
                facecolor=color,
                edgecolor=color, )
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
    # data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
    data = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
    for i in range(len(bars)):
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
    # this will allow to remove the gap between the days, when plotting the
    # data
    data2 = np.hstack([np.arange(data[:, 0].size)[:, np.newaxis], data[:, 1:]])
    # print len(bars),len(date),len(data),len(data2)
    # print data2
    # plot the data
    # figWidth = len(data) * width
    # fig = plt.figure(figsize=(figWidth, 5))
    # fig = plt.figure(figsize=(16, 10))
    # ax = fig.add_axes([0.05, 0.1, 0.9, 0.9])
    # customization of the axis
    #
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
    if div_n > 0 and allc / div_n > 12:
        div_n = allc / 12
    ax.set_xticks(range(0, len(bars.index), div_n))
    new_xticks = [bars.index[d] for d in ax.get_xticks()]
    ax.set_xticklabels(new_xticks, rotation=30, horizontalalignment='right')
    # ax.set_xticklabels(new_xticks, rotation=30, horizontalalignment='right')

    # fig.autofmt_xdate()
    ax.autoscale_view()
    # Create the candle sticks
    fooCandlestick(ax, data2, width=width, colorup='r', colordown='g')


def twoLineCompute(code, df=None, start=None, end=None, ptype='low'):
    # ptype='low'
    # ptype='high'
    if df is None:
        # df = ts.get_hist_data(code,start=start)
        df = tdd.get_tdx_append_now_df_api(
            code, start, end).sort_index(ascending=True)
    else:
        df = df.sort_index(ascending=True)
        df = df[df.index >= start]
    series = df[ptype]

    # pd.rolling_min(df.low,window=len(series)/8).unique()

    def get_Top(df, ptype):
        if len(df) < 30:
            period_type = 'd'
        elif len(df) > 30 and len(df) < 120:
            period_type = 'w'
        elif int(len(df)) / 20 > 20:
            total = int(len(df) / 20 / 20)
            period_type = '%sm' % total if total > 0 else 1
        else:
            period_type = 'm'
        log.info("period:%s" % period_type)
        df.index = pd.to_datetime(df.index)
        if ptype == 'high':
            dfw = df[ptype].resample(period_type, how='max')
            # price=dfw.min()
            # idx = dfw[dfw == price].index.values[0]
            ##dd = dfw[dfw.index >= idx]
        else:
            dfw = df[ptype].resample(period_type, how='min')
            # price=dfw.max()
            # idx = dfw[dfw == price].index.values[0]
            ##dd = dfw[dfw.index >= idx]
        dd = dfw.dropna()
        all = len(dd)
        log.info("all:%s" % (all))
        mlist = []
        if all > 60:
            step = 0.1
        else:
            step = 0.2
        if ptype == 'high':
            nrange = np.arange(all, 1, -step)
        else:
            nrange = np.arange(1, all, step)

        for x in nrange:
        # for x in np.arange(1, all, step):
            if ptype == 'high':
                mlist = pd.rolling_max(dd, window=all / x).unique()
            else:
                mlist = pd.rolling_min(dd, window=all / x).unique()
            if len(mlist) > 2:
                if  str(mlist[0]).strip() == ('nan'):
                # if str(mlist[0]).find('nan') >0 :print "N"
                    mlist = mlist[1:]
                # ra = all / x
                # print mlist
                break
        # print LIS(mlist)
        return mlist

    # map(lambda x: x/10.0, range(5, 50, 15))
    mlist = get_Top(df, ptype)
    # for p in mlist:
    # idx=df[df[ptype]==p].index.values[0]
    # print p,str(idx)[:10]
    return mlist


def get_linear_model_status(code, df=None, dtype='d', type='m', start=None, end=None, days=1, filter='n',
                            dl=None, countall=True, ptype='low',power=True):

    # if code == "600760":
    # log.setLevel(LoggerFactory.DEBUG)
    # else:
    # log.setLevel(LoggerFactory.ERROR)
    if start is not None and end is None and filter == 'y':
        # if code not in ['999999','399006','399001']:
        # index_d,dl=tdd.get_duration_Index_date(dt=start)
        # log.debug("index_d:%s dl:%s"%(str(index_d),dl))
        # else:
        # index_d=cct.day8_to_day10(start)
        # log.debug("index_d:%s"%(index_d))
        index_d = cct.day8_to_day10(start)
        start = tdd.get_duration_price_date(code, ptype=ptype, dt=start, df=df,dl=dl,power=power)
        log.debug("start is not None start: %s  index_d:%s" % (start, index_d))
    elif end is not None and filter == 'y':
        df = tdd.get_tdx_append_now_df_api(code, start=start, end=end,df=df,dl=dl,power=power).sort_index(ascending=True)
        index_d = cct.day8_to_day10(start)
        start = tdd.get_duration_price_date(code, ptype=ptype, dt=start, df=df,dl=dl, power=power)
        df = df[df.index >= start]
        if len(df) > 2 and dl is None:
            if df.index.values[0] < index_d:
                df = df[df.index >= index_d]
    if dl is not None:
        # if ptype == 'low' and code == '999999':
        #     log.setLevel(LoggerFactory.DEBUG)
        # else:
        #     log.setLevel(LoggerFactory.ERROR)
        if power:
            start, index_d, df = tdd.get_duration_price_date(
                code, ptype=ptype, dl=dl, filter=False, df=df,power=power)
        else:
            start, index_d = tdd.get_duration_price_date(
                code, ptype=ptype, dl=dl, filter=False, df=df,power=power)
        # print start,index_d,ptype
        log.debug("dl not None code:%s start: %s  index_d:%s" % (code, start, index_d))

    if len(df) > 0 and  df is not None:
        df = df.sort_index(ascending=True)
        df = df[df.index >= start]
        # if start and index_d and len(df) > 2 and filter == 'y':
        #     if df.index.values[0] < index_d:
        #         df = df[df.index >= index_d]
        #         
                # if len(df) > 2 and start is not None and filter == 'y':
                #     if df.index.values[0] < index_d:
                #         df = df[df.index >= index_d]
                #         print df[:1]
                # start = tdd.get_duration_date(
                # code, ptype=ptype, dl=dl)
                # start = tdd.get_duration_price_date(code,ptype='low',dl=dl)
                # filter = 'y'
                # print start,ptype

    if len(df) ==0 or df is None :
        if start is not None and len(start) > 8 and int(start[:4]) > 2500:
            log.warn("code:%s ERROR:%s" % (code, start))
            start = '2016-01-01'
        # df = tdd.get_tdx_append_now_df(code,ptype, start, end).sort_index(ascending=True)
        df = tdd.get_tdx_append_now_df_api(
            code, start,end).sort_index(ascending=True)
        # if (start is not None or dl is not None) and filter=='y':
        # print "code:",start
        if start is None:
            start = df.index.values[0]
        if len(df) > 2 and dl is None and start is not None and filter == 'y':
            # print code,ptype,start,df.index.values[0],index_d
            # print "df:%s code:%s"%(len(df),code)`
            if df.index.values[0] < index_d:
                df = df[df.index >= index_d]

    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(
            df, dtype).sort_index(ascending=True)

    # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)

    def get_linear_model_ratio(asset, type='M', nowP=None):
        duration = asset[-1:].index.values[0]
        # log.debug("duration:%s" % duration)
        # log.debug("duration:%s" % cct.get_today_duration(duration))
        asset = asset.dropna()
        X = np.arange(len(asset))
        x = sm.add_constant(X)
        model = regression.linear_model.OLS(asset.astype(float), x).fit()
        a = model.params[0]
        b = model.params[1]
        # log.debug("X:%s a:%0.1f b:%0.1f" % (len(asset), a, b))
        # if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 1500:
        Y = np.append(X, X[-1] + int(days))
        # else:
        # Y = X
        # log.debug("X:%s Y:%s" % (X[-1], Y[-1]))
        # print ("X:%s" % (X[-1]))
        Y_hat = X * b + a
        # log.debug("Y_hat:%s" % Y_hat[-1])
        # Y_hat_t = Y * b + a
        # log.info("Y_hat:%s " % (Y_hat))
        # log.info("asset:%s " % (asset.values))
        if a != 0:
            ratio = b / a * 100
        else:
            ratio = 0
        operation = 0
        # log.debug("line_now:%s src:%s" % (Y_hat[-1], Y_hat[0]))
        if Y_hat[-1] > Y_hat[0]:
            if type.upper() == 'M':
                Y_Future = X * b + a
                # Y_Future = Y * b + a
                # ratio = b/a*100
                # log.info("Type:M ratio: %0.1f %0.1f Y_Mid: %0.1f" %
                # (b, ratio, Y_Future[-1]))
                # diff = asset.iat[-1] - Y_hat[-1]
                # if diff > 0:
                # return True, len(asset), diff
                # else:
                # return False, len(asset), diff
            elif type.upper() == 'L':
                i = (asset.values.T - Y_hat).argmin()
                c_low = X[i] * b + a - asset.values[i]
                Y_Future = X * b + a - c_low
                # Y_Future = Y * b + a - c_low
                # log.info("Type:L b: %0.1f ratio:%0.1f Y_Mid: %0.1f" %
                # (b, ratio, Y_Future[-1]))
                # diff = asset.iat[-1] - Y_hatlow[-1]
                # if asset.iat[-1] - Y_hatlow[-1] > 0:
                # return True, len(asset), diff
                # else:
                # return False, len(asset), diff
            elif type.upper() == 'H':
                i = (asset.values.T - Y_hat).argmax()
                c_high = X[i] * b + a - asset.values[i]
                # Y_hathigh = X * b + a - c_high
                Y_Future = X * b + a - c_high
                # Y_Future = Y * b + a - c_high
                # log.info("Type:H ratio: %0.1f %0.1f Y_Mid: %0.1f" %
                # (b, ratio, Y_Future[-1]))
            if nowP is not None:
                diff = nowP - Y_Future[-1]
            else:
                diff = asset[-1] - Y_Future[-1]
            if diff > 0:
                operation += 1
                # log.info("Type: %s UP !!! Y_Future: %0.1f b:%0.1f ratio:%0.1f " % (
                # type.upper(), Y_Future[-1], b, ratio))
                # else:
                # operation -=1
                # log.info("Type: %s Down Y_Future: %0.1f b:%0.1f ratio:%0.1f" % (
                # type.upper(), Y_Future[-1], b, ratio))
            return operation, ratio
        else:
            if type.upper() == 'M':
                Y_Future = X * b + a
                # Y_Future = Y * b + a
                # ratio = b/a*100
                # log.info("Type:M ratio: %0.1f %0.1f Y_Mid: %0.1f" %
                # (b, ratio, Y_Future[-1]))
            elif type.upper() == 'L':
                i = (asset.values.T - Y_hat).argmin()
                c_low = X[i] * b + a - asset.values[i]
                Y_Future = X * b + a - c_low
                # Y_Future = Y * b + a - c_low
                # log.info("Type:L b: %0.1f ratio:%0.1f Y_Mid: %0.1f" %
                # (b, ratio, Y_Future[-1]))
                # diff = asset.iat[-1] - Y_hatlow[-1]
                # if asset.iat[-1] - Y_hatlow[-1] > 0:
                # return True, len(asset), diff
                # else:
                # return False, len(asset), diff
            elif type.upper() == 'H':
                i = (asset.values.T - Y_hat).argmax()
                c_high = X[i] * b + a - asset.values[i]
                # Y_hathigh = X * b + a - c_high
                Y_Future = X * b + a - c_high
                # Y_Future = Y * b + a - c_high
                # log.info("Type:H ratio: %0.1f %0.1f Y_Mid: %0.1f" %
                # (b, ratio, Y_Future[-1]))
            if nowP is not None:
                diff = nowP - Y_Future[-1]
            else:
                diff = asset[-1] - Y_Future[-1]
            # log.info("as:%s Y:%s" % (asset[-1], Y_Future[-1]))
            if diff > 0:
                # operation += 1
                pass
                # log.info("Type: %s UP !!! Y_Future: %0.1f b:%0.1f ratio:%0.1f " % (
                # type.upper(), Y_Future[-1], b, ratio))
            else:
                operation -= 1
                # log.info("Type: %s Down Y_Future: %0.1f b:%0.1f ratio:%0.1f" % (
                # type.upper(), Y_Future[-1], b, ratio))
            return operation, ratio
            # log.debug("Line down !!! d:%s" % Y_hat[0])
            # print("Line down !!! d:%s nowp:%s" % (round(Y_hat[1],2),asset[-1:].values[0]))
            # return -3, round(ratio, 2)
            # 

    df = df.fillna(0)
    if len(df) > 1 + days:
        if days != 0:
            asset = df[:-days]
        else:
            asset = df
    else:
        asset = df
    if len(asset) > 1:
        operationcount = 0
        ratio_l = []
        if countall:
            # for co in ['high', 'close', 'low']:
            for co in ['low', 'high', 'close']:
                for d_type in ['H', 'M', 'L']:
                    assetratio = asset[co]
                    nowpratio = df[co][-days] if len(df) > 1 + days else None
                    # print assetratio,nowpratio
                    op, ratio = get_linear_model_ratio(assetratio, d_type, nowpratio)
                    ratio_l.append(round(ratio, 2))
                    operationcount += op
        else:
            assetratio = asset['close']
            nowpratio = df['close'][-days] if len(df) > 1 + days else None
            op, ratio = get_linear_model_ratio(assetratio, type, nowpratio)
            ratio_l.append(round(ratio, 2))
            operationcount += op

            # log.info("op:%s min:%s ratio_l:%s" %
            # (operationcount, min(ratio_l), ratio_l))
            # 
        return operationcount, min(ratio_l), df[:1].index.values[0], [len(df),df[:1]]

    elif len(asset) == 1:
        ## log.error("powerCompute code:%s"%(code))
        if ptype == 'high':
            if df.close[-1] >= df.high[-1] * 0.99 and df.close[-1] >= df.open[-1]:
                return 12, 0, df.index.values[0], [len(df),df[:1]]

            elif df.close[-1] > df.open[-1]:
                if df.close[-1] > df.high[-1] * 0.97:
                    if len(df) > 2 and df.close[-1] > df.close[-2]:
                        return 10, 0, df.index.values[0], [len(df),df[:1]]
                    else:
                        return 11, 0, df.index.values[0], [len(df),df[:1]]
                else:
                    return 9, 0, df.index.values[0], [len(df),df[:1]]
            else:
                if len(df) >= 2:
                    if df.close[-1] > df.close[-2] * 1.01:
                        return 9, 0, df.index.values[0], [len(df),df[:1]]
                    elif df.close[-1] > df.close[-2]:
                        return 8, 0, df.index.values[0], [len(df),df[:1]]
                    elif df.low[-1] > df.low[-2]:
                        return 6, 0, df.index.values[0], [len(df),df[:1]]
                    else:
                        return 3, 0, df.index.values[0], [len(df),df[:1]]
                else:
                    return 1, 0, df.index.values[0], [len(df),df[:1]]
        else:
            return -10, 0, df.index.values[0], [len(df),df[:1]]
    else:
        ## log.error("code:%s %s :%s" % (code, ptype,len(df)))
        if ptype == 'high':
            ## log.warn("df is None,start:%s index:%s" % (start, index_d))
            return 13, 1, cct.get_today(), [len(df),df[:1]]
        else:
            return -10, -10, cct.get_today(), [len(df),df[:1]]




    #     return operationcount, min(ratio_l), df[:1].index.values[0], [len(df),df[:1]]
    # elif len(asset) == 1:
    #     ## log.error("powerCompute code:%s"%(code))
    #     if ptype == 'high':
    #         if df.close[-1] >= df.high[-1] * 0.99 and df.close[-1] >= df.open[-1]:
    #             return 12, 0, df.index.values[0], [len(df),df[:1]]

    #         elif df.close[-1] > df.open[-1]:
    #             if df.close[-1] > df.high[-1] * 0.97:
    #                 if len(df) > 2 and df.close[-1] > df.close[-2]:
    #                     return 10, 0, df.index.values[0], [len(df),df[:1]]
    #                 else:
    #                     return 11, 0, df.index.values[0], [len(df),df[:1]]
    #             else:
    #                 return 9, 0, df.index.values[0], [len(df),df[:1]]
    #         else:
    #             if len(df) >= 2:
    #                 if df.close[-1] > df.close[-2] * 1.01:
    #                     return 9, 0, df.index.values[0], [len(df),df[:1]]
    #                 elif df.close[-1] > df.close[-2]:
    #                     return 8, 0, df.index.values[0], [len(df),df[:1]]
    #                 elif df.low[-1] > df.low[-2]:
    #                     return 6, 0, df.index.values[0], [len(df),df[:1]]
    #                 else:
    #                     return 3, 0, df.index.values[0], [len(df),df[:1]]
    #             else:
    #                 return 1, 0, df.index.values[0], [len(df),df[:1]]
    #     else:
    #         return -10, 0, df.index.values[0], [len(df),df[:1]]
    # else:
    #     ## log.error("code:%s %s :%s" % (code, ptype,len(df)))
    #     if ptype == 'high':
    #         ## log.warn("df is None,start:%s index:%s" % (start, index_d))
    #         return 13, 1, cct.get_today(), [len(df),df[:1]]
    #     else:
    #         return -10, -10, cct.get_today(), [len(df),df[:1]]


def get_linear_model_candles(code, ptype='low', dtype='d', start=None, end=None, filter='n',
                             df=None, dl=None,days=1):
    if start is not None and filter == 'y':
        if code not in ['999999', '399006', '399001']:
            index_d, dl = tdd.get_duration_Index_date(dt=start)
            log.debug("index_d:%s dl:%s" % (str(index_d), dl))
        else:
            index_d = cct.day8_to_day10(start)
            log.debug("index_d:%s" % (index_d))
        start = tdd.get_duration_price_date(code, ptype=ptype, dt=index_d, power=True)
        log.debug("start:%s" % (start))

    if start is None and df is None and dl is not None:
        start = cct.last_tddate(dl)
        # print start
        df = tdd.get_tdx_append_now_df_api(code, start=start, end=end).sort_index(ascending=True)

    if df is None:
        df = tdd.get_tdx_append_now_df_api(
            code, start=start, end=end).sort_index(ascending=True)
        start = df.index.values[0]
    else:
        df = df.sort_index(ascending=True)
    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(
            df, dtype).sort_index(ascending=True)

    asset = df[ptype]
    # log.info("df:%s" % asset[:1])
    asset = asset.dropna()
    dates = asset.index

    '''
    if not code.startswith('999') and not code.startswith('399'):
        # print "code:",code
        if code[:1] in ['5', '6', '9']:
            code2 = '999999'
        elif code[:2] in ['30']:
            # print "cyb"
            code2 = '399006'
        else:
            code2 = '399001'
        df1 = tdd.get_tdx_append_now_df_api(
            code2, ptype, start, end).sort_index(ascending=True)
        # df1 = tdd.get_tdx_append_now_df(code2, ptype, start, end).sort_index(ascending=True)
        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(
                df1, dtype).sort_index(ascending=True)
        asset1 = df1.loc[df.index, ptype]
        startv = asset1[:1]
        # asset_v=asset[:1]
        # print startv,asset_v
        asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
    else:
        if code.startswith('399001'):
            code2 = '999999'
        elif code.startswith('399006'):
            code2 = '399005'
        else:
            code2 = '399001'
        df1 = tdd.get_tdx_append_now_df_api(
            code2, ptype, start, end).sort_index(ascending=True)
        # print df1[:1]
        # df1 = tdd.get_tdx_append_now_df(code2, ptype, start, end).sort_index(ascending=True)
        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(
                df1, dtype).sort_index(ascending=True)
        if len(df) < len(df1):
            asset1 = df1.loc[df.index, ptype]
            startv = asset1[:1]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
        else:
            df = df.loc[df1.index]
            df = df.dropna()
            asset = df[ptype]
            asset = asset.dropna()
            dates = asset.index
            asset1 = df1[ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 2))
    '''

    fig = plt.figure(figsize=(10, 6))
    plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95,
                        top=0.95, wspace=0.15, hspace=0.25)
    ax = fig.add_subplot(111)
    Candlestick(ax, df)

    # print len(df),len(asset)

    def setRegLinearPlt(asset, xaxis=None, status=None):
        X = np.arange(len(asset))
        if xaxis is not None:
            X = X + xaxis
        x = sm.add_constant(X)
        model = regression.linear_model.OLS(asset, x).fit()
        a = model.params[0]
        b = model.params[1]
        # log.info("a:%s b:%s" % (a, b))
        # log.info("X:%s a:%s b:%s" % (len(asset), a, b))
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
        status_n = Y_hat[-1] > Y_hat[0]
        if status is not None:
            if status_n and status:
                return status_n
            elif not status_n and not status:
                return status_n
        plt.plot(X, Y_hat, 'k', alpha=0.9)
        plt.plot(X, Y_hatlow, 'r', alpha=0.9)
        plt.plot(X, Y_hathigh, 'r', alpha=0.9)
        # print 'hat:%0.2f'%(Y_hat[-1])
        if status_n:
            directionX = 0.8
            directionY = 0.9
            directColor = 'r'
        else:
            directionX = 0.8
            directionY = 0.1
            # directColor = 'cyan' m
            directColor = 'g'
        plt.annotate('Hat:%0.2f' % (Y_hat[-1]), (X[-1], Y_hat[-1]),
                     # xytext=(0.8, 0.9),
                     xytext=(directionX, directionY),
                     textcoords='axes fraction',
                     # arrowprops=dict(facecolor='white', shrink=0.05),
                     # xytext=(directionX,directionY),
                     # textcoords='offset points',
                     # arrowprops=dict(arrowstyle="->"),
                     arrowprops=dict(facecolor=directColor, shrink=0.02, headwidth=5, width=1),
                     fontsize=14, color=directColor,
                     horizontalalignment='right', verticalalignment='bottom')

        return status_n

    def setBollPlt(code, df, ptype='low', start=None, status=None):
        if start is None:
            dt = tdd.get_duration_price_date(code, ptype=ptype, dl=60, df=df, power=True)
        else:
            dt = tdd.get_duration_price_date(code, ptype=ptype, dt=start, df=df, power=True)
        assetL = df[df.index >= dt][ptype]
        if len(assetL) == 1:
            mlist = twoLineCompute(code, df=df, start=start, ptype=ptype)
            if len(mlist) > 0:
                sp = mlist[0]
                idx = df[df[ptype] == sp].index.values[-1]
                print "New %s  %s !!! start:%s" % (ptype, assetL[-1], idx)
            else:
                idx = assertL.index[-1]
                print "NTop %s  %s !!! start:%s" % (ptype, assetL[-1], idx)
            assetL = df[df.index >= idx][ptype]
            dt = idx
            # return False
        # if ptype == 'high':
        # xaxisInit = len(df[df.index > dt])
        # else:
        # xaxisInit = len(df[df.index < dt])
        xaxisInit = len(df[df.index < dt])
        # print assertL[-1],assert[0]
        setRegLinearPlt(assetL, xaxis=xaxisInit, status=status)
        op, ra, st, dss = get_linear_model_status(code, df=df[df.index >= dt], start=dt, filter='y', ptype=ptype,days=days)
        print "%s op:%s ra:%s days:%s  start:%s" % (code, op, str(ra), str(dss[0]), st)

    status = setRegLinearPlt(asset)
    # if filter == 'n':
    setBollPlt(code, df, 'low', start, status=status)
    setBollPlt(code, df, 'high', start, status=status)
    # pass
    # eval("df.%s"%ptype).ewm(span=20).mean().plot(style='k')
    eval("df.%s" % 'close').plot(style='k')
    roll_mean = pd.rolling_mean(df.high, window=10)
    plt.plot(roll_mean, 'b')
    # print roll_mean[-1]
    # plt.legend(["MA:10"+str(roll_mean[-1]], fontsize=12,loc=2)

    plt.ylabel('Price', fontsize=12)
    if 'name' in df.columns:
        plt.title(
            df.name.values[-1:][0] + " " + code + " | " + str(dates[-1])[:11] + " | " + "MA:%0.2f" % (roll_mean[-1]),
            fontsize=12)
    else:
        plt.title(code + " | " + str(dates[-1])[:11] + " | " + "MA:%0.2f" % (roll_mean[-1]), fontsize=12)
    # plt.title(code + " | " + str(dates[-1])[:11], fontsize=14)
    fib = cct.getFibonacci(len(asset) * 5, len(asset))
    plt.legend(["Now:%s" % df.close[-1], "Hi:%s" % df.high[-1], "Lo:%0.2f" % (asset.iat[-1]), "day:%s" %
                len(asset), "fib:%s" % (fib)], fontsize=12, loc=8)
    plt.grid(True)
    if filter:

        for type in ['high', 'low']:
            dt = tdd.get_duration_price_date(code, ptype=type, dt=start, df=df, power=True)
            mlist = twoLineCompute(code, df=df, start=dt, ptype=type)
            if len(mlist) > 1:
                log.info("mlist:%s" % mlist)
                sa = round(mlist[0], 2)
                sb = round(mlist[-1], 2)
                X = np.arange(len(df))
                aid = df[df[type] == sa].index.values[-1][:10]
                ida = len(df[df.index <= aid])
                aX = X[ida - 1]

                bid = df[df[type] == mlist[-1]].index.values[-1][:10]
                # print df[df[type] == sb].index.values
                idb = len(df[df.index <= bid])
                bX = X[idb - 1]
                if sa < sb:
                    # print "Gold Line"
                    Xa = X[ida - 1:]
                    Xb = Xa - Xa[0]
                    # sb=(bX - aX)*b + sa
                    b = (sb - sa) / (bX - aX)
                    Yhat = Xb * b + sa

                else:
                    # print "Down Line"
                    # Xa=X[ida:idb - 1]
                    Xa = X[ida - 1:]
                    Xb = Xa - Xa[0]
                    # sb=(bX - aX)*b+sa
                    if (bX - aX) > 0:
                        b = (sb - sa) / (bX - aX)
                    else:
                        b = 0
                    Ylist = Xb * b + sa
                    Yhat = []
                    st = sb * 0.618
                    for v in Ylist:
                        if v >= st:
                            Yhat.append(v)
                        else:
                            break
                    Xa = Xa[:len(Yhat)]
                log.info("aX:%s sa:%s bx:%s sb:%s" % (aX, sa, bX, sb))
                log.info("Xa:%s Yhat" % (Xa[:1]))
                # ax.plot([aX,bX],[sa,sb],'k--')
                # print Yhat[0],Yhat[-1],sa,sb,Xa[0],ida,Xb[0]
                ax.plot(Xa, Yhat, 'k--')

                # else:
                # print "Mlist:%s" % (mlist)

    # plt.legend([code]);
    # plt.legend([code, 'Value center line', 'Value interval line']);
    # fig=plt.fig()
    # fig.figsize = [14,8]
    # scale = 1.1
    zp = zoompan.ZoomPan()
    figZoom = zp.zoom_factory(ax, base_scale=1.1)
    figPan = zp.pan_factory(ax)
    plt.xticks(rotation=15, horizontalalignment='center')
    # plt.setp( axs[1].xaxis.get_majorticklabels(), rotation=70 )
    plt.show(block=False)
    return df


def powerCompute_df(df, dtype='d', end=None, dl=None, filter='y',talib=False):
    ts=time.time()
    if isinstance(df, list):
        code_l = df
        statuslist = True
    else:
        code_l = df.index.tolist()
        statuslist = False
    dm = tdd.get_sina_data_df(code_l)
    if statuslist:
        df = dm
    for code in code_l:
        if statuslist:
            start = None
        else:
            if dl is None:
                start = df.loc[code, 'date']
                start = cct.day8_to_day10(start)
                # filter = 'y'
                # print start
            else:
                start = None
        start = cct.day8_to_day10(start)
        end = cct.day8_to_day10(end)
        if code in dm.index:
            dz = dm.loc[code].to_frame().T
        else:
            dz = tdd.get_sina_data_df(code)
#        tdx_df = tdd.get_tdx_power_now_df(code, start=start, end=end, type='f', df=None, dm=dz, dl=dl*2)
        tdx_df = tdd.get_tdx_append_now_df_api(code, start=start, end=end, type='f', df=None, dm=dz, dl=dl*2)
        # print tdx_df
        opc = 0
        stl = ''
        rac = 0
        # fib = []
        fibl = '0'
        fib = '0'
        # sep = '|'
        for ptype in ['low', 'high']:
            op, ra, st, daysData  = get_linear_model_status(
                code, df=tdx_df, dtype=dtype, start=start, end=end, dl=dl, filter=filter, ptype=ptype)
            # fib.append(str(daysData[0]))
            opc += op
            rac += ra
            if ptype == 'low':
                stl = st
                fibl = str(daysData[0])
            else:
                fib = str(daysData[0])
        # fibl = sep.join(fib)
        
        tdx_df,operation = getab.Get_BBANDS(tdx_df, dtype='d')
        # opc +=operation
        # if opc > 21:
        #     opc = 21
        # log.debug( "opc:%s op:%s"%(opc,operation))
        
        # df.loc[code,'ma5'] = daysData[1].ma5d[0]
        # print tdx_df[:1].ma5d[0],daysData[1].ma5d[0]
        if len(tdx_df) > 0 and 'ma5d' in tdx_df.columns:
            if tdx_df[:1].ma5d[0] is not None and tdx_df[:1].ma5d[0] != 0:
                df.loc[code,'ma5d'] = round(float(tdx_df[:1].ma5d[0]),2)
            if tdx_df[:1].ma10d[0] is not None and tdx_df[:1].ma10d[0] != 0:
                df.loc[code,'ma10d'] = round(float(tdx_df[:1].ma10d[0]),2)
        df.loc[code, 'op'] = opc
        df.loc[code, 'ra'] = rac
        df.loc[code, 'fib'] = fib
        df.loc[code, 'fibl'] = fibl
        df.loc[code, 'ldate'] = stl
        df.loc[code, 'boll'] = operation

        tdx_df,opkdj = getab.Get_KDJ(tdx_df, dtype='d')
        tdx_df,opmacd = getab.Get_MACD_OP(tdx_df, dtype='d')
        tdx_df,oprsi = getab.Get_RSI(tdx_df, dtype='d')
        opma = getab.algoMultiDay(tdx_df)
        df.loc[code, 'kdj'] = opkdj
        df.loc[code, 'macd'] = opmacd
        df.loc[code, 'rsi'] = oprsi
        df.loc[code, 'ma'] = opma
        # df = getab.Get_BBANDS(df, dtype='d')
        #'volume', 'ratio', 'counts','ldate' -> 'ma','macd','rsi','kdj'
        df=df.fillna(0)
        # df = df.drop_duplicates()
    print "P:%0.2f"%(time.time()-ts),    
    return df


def computeRolling_min(series):
    pd.rolling_min(df.low, window=len(series) / 8).unique()


def parseArgmain():
    # from ConfigParser import ConfigParser
    # import shlex
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('code', type=str, nargs='?', help='999999')
    parser.add_argument('start', nargs='?', type=str, help='20150612')
    parser.add_argument('end', nargs='?', type=str, help='20160101')
    parser.add_argument('-d', action="store", dest="dtype", type=str, nargs='?', choices=['d', 'w', 'm'], default='d',
                        help='DateType')
    parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['f', 'b'], default='f',
                        help='Price Forward or back')
    parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['high', 'low', 'close'], default='low',
                        help='price type')
    parser.add_argument('-f', action="store", dest="filter", type=str, choices=['y', 'n'], default='n',
                        help='find duration low')
    parser.add_argument('-l', action="store", dest="dl", type=int, default=None,
                        help='dl')
    parser.add_argument('-dl', action="store", dest="days", type=int, default=1,
                        help='days')
    parser.add_argument('-m', action="store", dest="mpl", type=str, default='y',
                        help='mpl show')
    return parser


def maintest(code, start=None, type='m', filter='y'):
    import timeit
    run = 1
    strip_tx = timeit.timeit(lambda: get_linear_model_status(
        code, start=start, type=type, filter=filter), number=run)
    print("ex Read:", strip_tx)


if __name__ == "__main__":
    # print get_linear_model_status('600671', filter='y', dl=10, ptype='low')
    # print get_linear_model_status('600671', filter='y', dl=10, ptype='high')
    # print get_linear_model_status('600671', filter='y', start='20160329', ptype='low')
    # print get_linear_model_status('600671', filter='y', start='20160329', ptype='high')
    # print get_linear_model_status('999999', filter='y', dl=30, ptype='high')
    # print get_linear_model_status('999999', filter='y', dl=30, ptype='low')
    # print powerCompute_df(['000938','002171'], dtype='d',end=None, dl=21, filter='y')
    # # print powerCompute_df(['601198', '002791', '000503'], dtype='d', end=None, dl=30, filter='y')
    # print get_linear_model_status('999999', filter='y', dl=34, ptype='low', days=1)
    # print get_linear_model_status('399006', filter='y', dl=34, ptype='low', days=1)
    # sys.exit()
    if cct.isMac():
        cct.set_console(80, 19)
    else:
        cct.set_console(80, 19)
    parser = parseArgmain()
    parser.print_help()
    while 1:
        try:
            # log.setLevel(LoggerFactory.INFO)
            # log.setLevel(LoggerFactory.DEBUG)
            code = raw_input("code:")
            args = parser.parse_args(code.split())
            if len(str(args.code)) == 6:
                if args.start is not None and len(args.start) < 4:
                    args.dl = int(args.start)
                    args.start = None
                # ptype='f', df=None, dtype='d', type='m', start=None, end=None, days=1, filter='n'):
                # print args.end
                # op, ra, st = get_linear_model_status(args.code, dtype=args.dtype, start=cct.day8_to_day10(
                #      args.start), end=cct.day8_to_day10(args.end), filter=args.filter, dl=args.dl)
                # print "code:%s op:%s ra:%s  start:%s" % (code, op, ra, st)
                start = cct.day8_to_day10(args.start)
                end = cct.day8_to_day10(args.end)
                if args.mpl == 'y':
                    get_linear_model_candles(args.code, dtype=args.dtype, start=start, end=end, ptype=args.ptype,
                                             filter=args.filter, dl=args.dl,days=args.days)
                else:
                    args.filter = 'y'
                    for ptype in ['low', 'high']:
                        op, ra, st, daysData  = get_linear_model_status(args.code, dtype=args.dtype, start=start, end=end,
                                                                   days=args.days, ptype=ptype, filter=args.filter,
                                                                   dl=args.dl)
                        print "%s op:%s ra:%s days:%s  start:%s" % (args.code, op, str(ra), str(daysData[0]), st)
                        # op, ra, st, daysData  = get_linear_model_status(args.code, dtype=args.dtype, start=cct.day8_to_day10(
                        # args.start), end=cct.day8_to_day10(args.end), filter=args.filter, dl=args.dl)
                # print "code:%s op:%s ra/days:%s  start:%s" % (code, op, str(ra) + '/' + str(daysData[0]), st)
                cct.sleep(0.1)
                # ts=time.time()
                # time.sleep(5)
                # print "%0.5f"%(time.time()-ts)
            elif code == 'q':
                sys.exit(0)
            elif code == 'h' or code == 'help':
                parser.print_help()
            else:
                print "code error"
        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
        except (IOError, EOFError, Exception) as e:
            print "Error", e
            # sys.exit(0)
    # log.setLevel(LoggerFactory.DEBUG)
    log.setLevel(LoggerFactory.INFO)

    # st=get_linear_model_status('300380',start='2016-01-28',type='h',filter='y')
    st = get_linear_model_status('300380')
    # st=get_linear_model_status('300380',start='2016-01-28',filter='y')
    # maintest('002189',start='2016-01-28',type='h',filter='y')
    print "M:"
    # st=get_linear_model_status('002189',start='2016-01-28',filter='y')
    # maintest('002189',start='2016-01-28',filter='y')
    print "L"
    # st=get_linear_model_status('002189',start='2016-01-28',type='l',filter='y')
    # maintest('002189',start='2016-01-28',type='l',filter='y')
    # cct.set_console(100, 15)
