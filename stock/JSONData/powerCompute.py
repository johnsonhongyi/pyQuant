# -*- encoding: utf-8 -*-
import sys
sys.path.append("..")

import numpy as np
import pandas as pd
from statsmodels import regression
import statsmodels.api as sm
from pylab import plt, mpl
from matplotlib.dates import num2date, date2num
from matplotlib.lines import Line2D
from matplotlib import transforms
from matplotlib.patches import Rectangle
import datetime
from JohnsonUtil import commonTips as cct
from JohnsonUtil import johnson_cons as ct
from JSONData import tdx_data_Day as tdd
from JSONData import get_macd_kdj_rsi as getab
from JSONData import wencaiData as wcd
from JSONData import tdx_hdf5_api as h5a
from JohnsonUtil import zoompan
from JohnsonUtil import LoggerFactory as LoggerFactory
import time
# log = LoggerFactory.getLogger("PowerCompute")
log = LoggerFactory.log
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
    # mpl.rcParams['font.sans-serif'] = ['STHeiti']
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
else:
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

# print mpl.rcParams

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
        # ax.autoscale_view()

        return lines, boxes

    date = date2num(bars.index.to_datetime().to_pydatetime())
    # date = date2num(pd.to_datetime(bars.index).to_pydatetime())
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
    # ax.autoscale_view()
    # Create the candle sticks
    fooCandlestick(ax, data2, width=width, colorup='r', colordown='g')


def twoLineCompute(code, df=None, start=None, end=None, ptype='low'):
    """[summary]

    [find low list and high list]

    Arguments:
        code {[type]} -- [description]

    Keyword Arguments:
        df {[type]} -- [description] (default: {None})
        start {[type]} -- [description] (default: {None})
        end {[type]} -- [description] (default: {None})
        ptype {str} -- [description] (default: {'low'})

    Returns:
        [list] -- [description]
    """
    # ptype='low'
    # ptype='high'
    if df is None:
        # df = get_kdate_data(code,start=start)
        df = tdd.get_tdx_append_now_df_api(
            code, start, end).sort_index(ascending=True)
    else:
        df = df.sort_index(ascending=True)
        df = df[df.index >= start]
    series = df[ptype]

    # pd.rolling_min(df.low,window=len(series)/8).unique()

    def get_Top(df, ptype):
        """[summary]

        [description]

        Arguments:
            df {[type]} -- [description]
            ptype {[type]} -- [ohlc]

        Returns:
            [list] -- [description]
        """
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
                mlist = pd.rolling_max(dd, window=int(all / x)).unique()
            else:
                mlist = pd.rolling_min(dd, window=int(all / x)).unique()
            if len(mlist) > 2:
                if str(mlist[0]).strip() == ('nan'):
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


def get_linear_model_status_LSH(code, ptype='low', dtype='d', type='l', start=None, end=None):
    """[summary]

    [description]

    Arguments:
        code {[type]} -- [description]

    Keyword Arguments:
        ptype {str} -- [description] (default: {'low'})
        dtype {str} -- [description] (default: {'d'})
        type {str} -- [description] (default: {'l'})
        start {[type]} -- [description] (default: {None})
        end {[type]} -- [description] (default: {None})

    Returns:
        bool -- [description]
    """
    # df = tdd.get_tdx_append_now_df(code, ptype, start, end).sort_index(ascending=True)
    df = tdd.get_tdx_append_now_df_api(
        code, start, end).sort_index(ascending=True)
    # print start,end,df.index.values[:1],df.index.values[-1:]
    if len(df) < 2:
        return False, 0, 0
    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(
            df, dtype).sort_index(ascending=True)
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


def get_linear_model_status(code, df=None, dtype='d', type='m', start=None, end=None, days=1, filter='n',
                            dl=None, countall=True, ptype='low', power=True):

    # if code == "600760":
    # log.setLevel(LoggerFactory.DEBUG)
    # else:
    # log.setLevel(LoggerFactory.ERROR)

    index_d = None
    days = days if days <> 0 else 1
    if start is not None and end is None and filter == 'y':
        # if code not in ['999999','399006','399001']:
        # index_d,dl=tdd.get_duration_Index_date(dt=start)
        # log.debug("index_d:%s dl:%s"%(str(index_d),dl))
        # else:
        # index_d=cct.day8_to_day10(start)
        # log.debug("index_d:%s"%(index_d))
        index_d = cct.day8_to_day10(start)
        start = tdd.get_duration_price_date(
            code, ptype=ptype, dt=start, df=df, dl=dl, power=power)
        log.debug("start is not None start: %s  index_d:%s" % (start, index_d))
    elif end is not None and filter == 'y':
        df = tdd.get_tdx_append_now_df_api(
            code, start=start, end=end, df=df, dl=dl, power=power).sort_index(ascending=True)
        index_d = cct.day8_to_day10(start)
        start = tdd.get_duration_price_date(
            code, ptype=ptype, dt=start, df=df, dl=dl, power=power)
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
                code, ptype=ptype, dl=dl, filter=False, df=df, power=power)
        else:
            start, index_d = tdd.get_duration_price_date(
                code, ptype=ptype, dl=dl, filter=False, df=df, power=power)
        # print start,index_d,ptype
        log.debug("dl not None code:%s start: %s  index_d:%s" %
                  (code, start, index_d))
    if start != index_d and start == cct.get_today():
        return -11, -11, cct.get_today(), [0, pd.DataFrame()]
    if df is not None and len(df) > 0:
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

    if df is None or len(df) == 0:
        if start is not None and len(start) > 8 and int(start[:4]) > 2500:
            log.warn("code:%s ERROR:%s" % (code, start))
            start = '2016-01-01'
        # df = tdd.get_tdx_append_now_df(code,ptype, start, end).sort_index(ascending=True)
        df = tdd.get_tdx_append_now_df_api(
            code, start, end).sort_index(ascending=True)
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

    def get_linear_model_ratio(asset, nowP=None):
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
        Y_FutureM = X * b + a
        log.debug("mid:%.2f" % (Y_FutureM[-1]))

        i = (asset.values.T - Y_hat).argmin()
        c_low = X[i] * b + a - asset.values[i]
        Y_FutureL = X * b + a - c_low
        log.debug("Bottom:%.2f" % (Y_FutureL[-1]))

        i = (asset.values.T - Y_hat).argmax()
        c_high = X[i] * b + a - asset.values[i]
        Y_FutureH = X * b + a - c_high

        log.debug("Top:%.2f" % (Y_FutureH[-1]))

        if nowP is not None:
            diff = nowP - Y_FutureM[-1]
            diff_h = nowP - Y_FutureH[-1]
            diff_l = nowP - Y_FutureL[-1]
        else:
            diff = asset[-1] - Y_FutureM[-1]
            diff_h = asset[-1] - Y_FutureH[-1]
            diff_l = asset[-1] - Y_FutureL[-1]

        if Y_hat[-1] > Y_hat[0]:
            if diff > 0:
                operation += 1
            # else:
                # operation -= 1
            if diff_h > 0:
                operation += 1
            # else:
                # operation -= 1
            if diff_l > 0:
                operation += 1
            # else:
                # operation -= 1
        else:
            if diff > 0:
                operation -= 1
            # else:
                # operation += 1
            if diff_h > 0:
                operation -= 1
            # else:
                # operation += 1
            if diff_l > 0:
                operation -= 1
            # else:
                # operation += 1
        return operation, ratio

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
#        idx = days if days <> 0 else 1
        if countall:
            for co in ['low', 'high', 'close']:
                assetratio = asset[co]
                nowpratio = df[co][-days] if len(df) > 1 + days else None
                # print assetratio,nowpratio
                op, ratio = get_linear_model_ratio(assetratio, nowpratio)
                ratio_l.append(round(ratio, 2))
                operationcount += op
        else:
            assetratio = asset['close']
            nowpratio = df['close'][-days] if len(df) > 1 + days else None
            op, ratio = get_linear_model_ratio(assetratio, nowpratio)
            ratio_l.append(round(ratio, 2))
            operationcount += op

            # log.info("op:%s min:%s ratio_l:%s" %
            # (operationcount, min(ratio_l), ratio_l))
        return operationcount, min(ratio_l), df[:1].index.values[0], [len(df), df[:1]]

    elif len(asset) == 1:
        ## log.error("powerCompute code:%s"%(code))
        if ptype == 'high':
            if df.close[-1] >= df.high[-1] * 0.99 and df.close[-1] >= df.open[-1]:
                return 12, 10, df.index.values[0], [len(df), df[:1]]

            elif df.close[-1] > df.open[-1]:
                if df.close[-1] > df.high[-1] * 0.97:
                    if len(df) > 2 and df.close[-1] > df.close[-2]:
                        return 10, 10, df.index.values[0], [len(df), df[:1]]
                    else:
                        return 11, 10, df.index.values[0], [len(df), df[:1]]
                else:
                    return 9, 10, df.index.values[0], [len(df), df[:1]]
            else:
                if len(df) >= 2:
                    if df.close[-1] > df.close[-2] * 1.01:
                        return 9, 10, df.index.values[0], [len(df), df[:1]]
                    elif df.close[-1] > df.close[-2]:
                        return 8, 10, df.index.values[0], [len(df), df[:1]]
                    elif df.low[-1] > df.low[-2]:
                        return 6, 9, df.index.values[0], [len(df), df[:1]]
                    else:
                        return 3, 8, df.index.values[0], [len(df), df[:1]]
                else:
                    return 1, 7, df.index.values[0], [len(df), df[:1]]
        else:
            return -10, -10, df.index.values[0], [len(df), df[:1]]
    else:
        ## log.error("code:%s %s :%s" % (code, ptype,len(df)))
        if ptype == 'high':
            ## log.warn("df is None,start:%s index:%s" % (start, index_d))
            return 13, 11, cct.get_today(), [len(df), df[:1]]
        else:
            return -10, -10, cct.get_today(), [len(df), df[:1]]

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
                             df=None, dl=None, days=1, opa=False):
    if start is not None and filter == 'y':
        if code not in ['999999', '399006', '399001']:
            index_d, dl = tdd.get_duration_Index_date(dt=start)
            log.debug("index_d:%s dl:%s" % (str(index_d), dl))
        else:
            index_d = cct.day8_to_day10(start)
            log.debug("index_d:%s" % (index_d))
        start = tdd.get_duration_price_date(
            code, ptype=ptype, dt=index_d, power=True)
        log.debug("start:%s" % (start))

    if start is None and df is None and dl is not None:
        start = cct.last_tddate(dl)
        # print start
        df = tdd.get_tdx_append_now_df_api(
            code, start=start, end=end).sort_index(ascending=True)

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

    fig = plt.figure(figsize=(10, 6))
    # plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95,
    #                     top=0.95, wspace=0.15, hspace=0.25)
    # ax = fig.add_subplot(111)
    ax = plt.subplot2grid((10, 1), (0, 0), rowspan=8, colspan=1)
    Candlestick(ax, df)

    # print len(df),len(asset)

    def setRegLinearPlt(asset, xaxis=None, status=None):
        if len(asset) < 2:
            return None
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
            directionY = 0.5
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
                     arrowprops=dict(facecolor=directColor,
                                     shrink=0.02, headwidth=5, width=1),
                     fontsize=14, color=directColor,
                     horizontalalignment='right', verticalalignment='bottom')

        return status_n

    def setBollPlt(code, df, ptype='low', start=None, status=None, opa=False):
        if start is None:
            dt = tdd.get_duration_price_date(
                code, ptype=ptype, dl=60, df=df, power=True)
        else:
            dt = tdd.get_duration_price_date(
                code, ptype=ptype, dt=start, df=df, power=True)
        assetL = df[df.index >= dt][ptype]
        if len(assetL) == 1:
            mlist = twoLineCompute(code, df=df, start=start, ptype=ptype)
            if len(mlist) > 0:
                sp = mlist[0]
                idx = df[df[ptype] == sp].index.values[-1]
                print "New %s  %s !!! start:%s" % (ptype, assetL[-1], idx)
            else:
                idx = assetL.index[-1]
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
        if opa:
            op, ra, st, dss = get_linear_model_status(
                code, df=df[df.index >= dt], start=dt, filter='y', ptype=ptype, days=days)
            # print "%s op:%s ra:%s days:%s  start:%s" % (code, op, str(ra),
            # str(dss[0]), st)
            print "op:%s ra:%s days:%s  start:%s" % (op, str(ra), str(dss[0]), st)

    status = setRegLinearPlt(asset)
    # if filter == 'n':
    setBollPlt(code, df, 'low', start, status=status, opa=opa)
    setBollPlt(code, df, 'high', start, status=status, opa=opa)
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
            df.name.values[-1:][0] + " " + code + " | " +
            str(dates[-1])[:11] + " | " + "MA:%0.2f" % (roll_mean[-1]),
            fontsize=12)
    else:
        plt.title(code + " | " + str(dates[-1])[:11] +
                  " | " + "MA:%0.2f" % (roll_mean[-1]), fontsize=12)
    # plt.title(code + " | " + str(dates[-1])[:11], fontsize=14)
    fib = cct.getFibonacci(len(asset) * 5, len(asset))
    plt.legend(["Now:%s" % df.close[-1], "Hi:%s" % df.high[-1], "Lo:%0.2f" % (asset.iat[-1]), "day:%s" %
                len(asset), "fib:%s" % (fib)], fontsize=12, loc=0)
    plt.grid(True)
    if filter:

        for type in ['high', 'low']:
            dt = tdd.get_duration_price_date(
                code, ptype=type, dt=start, df=df, power=True)
            mlist = twoLineCompute(code, df=df, start=dt, ptype=type)
            if len(mlist) > 1:
                log.info("mlist:%s" % mlist)
                sa = round(mlist[0], 2)
                sb = round(mlist[-1], 2)
                X = np.arange(len(df))
                df[type] = df[type].apply(lambda x: round(x, 2))
                aid = df[df[type] == sa].index.values[-1][:10] if str(sa) <> 'nan' else df.index.values[0][:10]
                ida = len(df[df.index <= aid])
                aX = X[ida - 1]

                bid = df[df[type] == sb].index.values[-1][:10] if str(sb) <> 'nan' else df.index.values[-1][:10]
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
    #
    #plot volume
    plt.xticks(rotation=15, horizontalalignment='center')

    '''
    #old
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
    ax.autoscale_view()
    '''

    plt.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95, wspace=0.15, hspace=0.00)
    plt.setp(ax.get_xticklabels(), visible=False)
    yl = ax.get_ylim()
    ax2 = plt.subplot2grid((10, 1), (8, 0), rowspan=2, colspan=1,sharex=ax)
    # ax2.set_position(mat.transforms.Bbox([[0.125,0.1],[0.9,0.32]]))
    volume = np.asarray(df.amount)
    pos = df['open']-df['close']<0
    neg = df['open']-df['close']>=0
    if 'date' in df.columns:
        df = df.drop(['date'],axis=1)
    idx = df.reset_index().index
    ax2.bar(idx[pos],volume[pos],color='red',width=1,align='center')
    ax2.bar(idx[neg],volume[neg],color='green',width=1,align='center')
    yticks = ax2.get_yticks()
    ax2.set_yticks(yticks[::3])
    # plt.tight_layout()
    # plt.subplots_adjust(hspace=0.00, bottom=0.08)
    plt.xticks(rotation=15, horizontalalignment='center')


    assvol = df['vol']
    # assvol = assvol.apply(lambda x: round(x / assvol[:1]*asset[:1], 2))
    assvol = assvol.apply(lambda x: round(x / assvol[:1]+asset[:1], 2))
    ax.plot(assvol, '-g', linewidth=0.5)
    # print assvol

    zp = zoompan.ZoomPan()
    figZoom = zp.zoom_factory(ax, base_scale=1.1)
    figPan = zp.pan_factory(ax)
    # plt.xticks(rotation=30, horizontalalignment='center')
    # plt.setp( axs[1].xaxis.get_majorticklabels(), rotation=70 )
    plt.show(block=False)
    return df

global Power_CXG_Error, drop_cxg, wencai_drop
Power_CXG_Error = 0
drop_cxg = []
wencai_drop = []


def powerCompute_df(df, dtype='d', end=None, dl=ct.PowerCountdl, filter='y', talib=False, newdays=None, days=0,index=False):
    ts = time.time()

    if isinstance(df, list):
        h5_combine_status = False
        code_l = df
        statuslist = True
    else:
        code_l = df.index.tolist()
        h5_combine_status = True
        statuslist = False

    # if '999999' not in code_l:
    #     code_l.append('999999')
    #     code_l.append('399001')

    # code_src = code_l
    global Power_CXG_Error, drop_cxg, wencai_drop
#    drop_cxg

    h5_fname = 'powerCompute'
    h5_table = dtype + '_' + str(dl) + '_' + filter + '_' + 'all'
    power_columns = ['ra', 'op', 'category', 'ma', 'rsi', 'kdj',
                     'boll', 'rah', 'df2b','fib', 'fibl', 'macd', 'vstd', 'oph', 'lvolume']
    # [['ma' ,'rsi' ,'kdj' ,'boll', 'ra','rah', 'df2b' ,'fibl','fib' ,'macd' ,'oph']]
    # [['ma' ,'rsi' ,'kdj' ,'boll', 'ra',rah', 'df2b' ,'fibl','fib' ,'macd' ,'vstd', 'oph']]

    h5 = h5a.load_hdf_db(h5_fname, h5_table, code_l=code_l, limit_time=ct.h5_power_limit_time)
    
    if h5 is not None:
        log.info("power hdf5 data:%s" % (len(h5)))
        if h5_combine_status:
            # if (not (915 < cct.get_now_time_int() < 935) or not cct.get_work_day_status())  and h5_combine_status:
            #            df_co = df.columns
            #            h5_co = h5.columns
            #            status = len(set(power_columns) & set(df_co)) - len(power_columns) == 0
            #            if status:

#            h5 = h5[(h5.op <> 0) & (h5.ra <> 0) & (h5.df2b <> 0 )]
            h5 = h5[(h5.df2b <> 0 ) & (h5.ra <> 0 ) & (h5.boll <> 0 )]
            h5 = h5.drop(
                [inx for inx in h5.columns if inx not in power_columns], axis=1)

            code_l = list(set(code_l) - set(h5.index))
            df = cct.combine_dataFrame(df, h5, col=None)
            if len(code_l) == 0:
                log.info("return df:%s h5:%s diff 0:%s" %
                         (len(df), len(h5), len(code_l)))
                return df
            else:
                # if len(drop_cxg) <> 0 and ((not (915 < cct.get_now_time_int() < 932)) or not cct.get_work_day_status()):
                if len(drop_cxg) <> 0 and (not cct.get_work_day_status()):
                    log.info(
                        "code_l not none:%s and drop_cxg <> 0 and not 915-932" % (code_l))
                    temp_l = list(set(code_l) - set(drop_cxg))
                    drop_t = [co for co in drop_cxg if co in df.index]
                    if len(temp_l) <> 0:
                        code_l = temp_l
                        # drop_cxg = []
                    else:
                        df = df.drop(drop_t, axis=0)
                        log.info("return2 drop(drop_t):%s drop_t:%s diff 0:%s" % (
                            len(df), len(drop_cxg), len(drop_t)))
                        return df
            log.info("add power hdf5 code_l:%s" % (len(code_l)))
            print("intP:%s"%(len(code_l))),
        else:
            if index and len(h5) == len(code_l):

                h5 = h5[ (h5.fibl <> h5.fib) & ((h5.fibl <> 0 ) | (h5.fib <> 0 ))]
                temp_l = list(set(code_l) - set(h5.index))

                if len(temp_l) == 0:
                    return h5
                else:
                    code_l = temp_l
    else:
        #        log.info("init power hdf5")
        if len(code_l) > 50:
            print("intP:%s"%(len(code_l))),
#    if not isinstance(df,list) and 'boll' in df.columns:
#            if 'time' in df.columns:
#                # if df[:1].boll.values <> 0 and time.time()- df[df.time <> 0].time[0] < ct.power_update_time:
#                if not cct.get_work_time() and len(df[df.time <> 0]) > 0 and df[:1].boll.values <> 0 and time.time() - df[df.time <> 0].time[0] < ct.power_update_time:
#                    print "PcA:%0.2f"%(time.time()-ts),
#                    return df
#            else:
#                if len(df) > 0 and df[:1].boll.values <> 0:
#                    print "PcA:%0.2f"%(time.time()-ts),
#                    return df

    # else:
    #         if  len(dm) - len(set(dm.index) & set(df.code.values)) < 10 :
    #             if 'code' in df.columns:
    #                 df = df.set_index('code')
    #                 df = df.drop_duplicates()
    #                 return df
    #         else:
    #             # diffcode = map( lambda x: x,set(dm.index) - (set(dm.index) & set(df.code.values)))
    #             diff_code = [x for x in set(dm.index) - (set(dm.index) & set(df.code.values))]
    #             dm.drop([col for col in dm.index if col not in diff_code], axis=0, inplace=True)

    if len(code_l) > 0:
        dm = tdd.get_sina_data_df(code_l)
        if statuslist:
            if h5 is not None and len(h5) >0:
                df = h5
            else:
                df = dm

    #    cname = ",".join(x for x in dm.name)
        n_code = [n for n in dm.index if n.startswith(('30', '60', '00'))]
        if len(n_code) > 1:
            dmname = dm.loc[n_code].name
            wcdf = wcd.get_wencai_data(dmname, 'wencai',days='N')
        else:
            wcdf = None
        wcdf_code = None if wcdf is None else wcdf.index.tolist()
        # col_co = df.columns.tolist()
        # col_co.extend([ 'ra', 'op', 'fib', 'ma5d', 'ma10d', 'ldate', 'hmax', 'lmin', 'cmean'])
        # print col_ra_op,col_co
        # df = df.loc[:,col_ra_op]
        co_dif = [co for co in ['ra', 'op', 'fib', 'fibl'] if co not in df.columns.tolist()]
        if len(co_dif) > 0:
            for co in list(co_dif):
                df[co] = 0

        for code in code_l:

            # if 'boll' in df.loc[code].index:
            #     if 'time' in df.columns and len(df[df.time <> 0]) > 0 and df[:1].boll.values <> 0 and time.time() - df[df.time <> 0].time[0] < ct.power_update_time:
            #         continue
                # elif df.loc[code].boll <> 0:
                #     continue

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
                # log.info("dz:%s"%(dm.loc[code]))
                dz = dm.loc[code].to_frame().T
                # if len(dz) > 1:
                #     dz=dz.to_frame()[0].T
                # else:
                #     dz=dz.to_frame().T
            else:
                dz = tdd.get_sina_data_df(code)

            if index and 'cumin' not in df.columns:
                df['cumin'] = 0

            if len(dz) > 0 and (index or dz.buy.values > 0 or dz.sell.values > 0):
                tdx_df = tdd.get_tdx_append_now_df_api(
                    code, start=start, end=end, type='f', df=None, dm=dz, dl=dl, newdays=5)

                tdx_df = tdx_df.fillna(0)
                tdx_df = tdx_df.sort_index(ascending=True)

                # if len(df) > days + 1 and days != 0:
                #     # log.info("tdx_df:%s"%(len(tdx_df)))
                #     tdx_df = tdx_df[:-days]
                #     # log.info("tdx_df:%s"%(len(tdx_df)))
                tdx_days = len(tdx_df)
                # if 8 < tdx_days < ct.cxg_limit_days:

                if code in df.index and "per3d" in df.columns and df.loc[code].per3d > 20 and 8 < tdx_days:
                    # print code,df.loc[code].per2d
                    if tdx_days > 6:
                        top_count = 0
                        for day in range(len(tdx_df), 0, -1):
                            #                        for day in range(len(tdx_df)):
                            # tmpdf=pd.DataFrame(df.loc[:,column][-days-2:-1-day], columns=[column])
                            # c_open = df.open.values[-days]
                            c_high = tdx_df.high.values[-day]
                            c_low = tdx_df.low.values[-day]
        #                    print c_high,c_low
                            if int(c_high) <> 0 and c_high == c_low:
                                top_count += 1
                            else:
                                if day == 1 and (915 < cct.get_now_time_int() < 932 and cct.get_work_day_status()):
                                    # if day == 1 and
                                    # cct.get_work_day_status():
                                    c_buy = dz.buy.values[-1]
                                    c_close_l = tdx_df.close.values[-2]
                                    c_percent = round(
                                        (c_buy - c_close_l) / c_close_l * 100, 2)
                                    # if 0 < c_percent < 9.9:
                                    if 0 < c_percent:
                                        break
                                else:
                                    if tdx_days - day < 3:
                                        top_count += 1
                                        continue
                                    else:
                                        break
        #                            log.info('code:%s c_high <> c_low:top :%s'%(code,tdx_days - day))
                    else:
                        top_count = len(tdx_df)

                    if top_count == len(tdx_df):
                        drop_cxg.append(code)
                        if Power_CXG_Error < 2:
                            log.error('CXG Good:%s' % (code))
                        continue
                elif tdx_days <= 8:
                    drop_cxg.append(code)
                    continue

            else:
                df.loc[code, 'op'] = 1
                df.loc[code, 'ra'] = 1
                df.loc[code, 'fib'] = 1
                df.loc[code, 'fibl'] = 1
                df.loc[code, 'ldate'] = 1
                df.loc[code, 'boll'] = 1
                df.loc[code, 'kdj'] = 1
                df.loc[code, 'macd'] = 1
                df.loc[code, 'rsi'] = 1
                df.loc[code, 'ma'] = 1
                df.loc[code, 'oph'] = 1
                df.loc[code, 'rah'] = 1
                continue
    #        tdx_df = tdd.get_tdx_power_now_df(code, start=start, end=end, type='f', df=None, dm=dz, dl=dl*2)
            opc = 0
            stl = ''
            rac = 0
            # fib = []
            fibl = 0
            fib = 0
            if len(tdx_df) < 2:
                continue
            # sep = '|'
            for ptype in ['low', 'high']:
                op, ra, st, daysData = get_linear_model_status(
                    code, df=tdx_df, dtype=dtype, start=start, end=end,days=days, dl=dl, filter=filter, ptype=ptype)
                # opc += op
                # rac += ra

                if ptype == 'low':
                    ral = ra
                    opl = op
                    stl = st
                    # fibl = str(daysData[0])
                    fibl = int(daysData[0])
                else:
                    oph = op
                    rah = ra
                    # fib = str(daysData[0])
                    fib = int(daysData[0])
            # fibl = sep.join(fib)

            tdx_df, operation = getab.Get_BBANDS(tdx_df, dtype='d',lastday=days)
            # opc +=operation
            # if opc > 21:
            #     opc = 21
            # log.debug( "opc:%s op:%s"%(opc,operation))

            # df.loc[code,'ma5'] = daysData[1].ma5d[0]
            # print tdx_df[:1].ma5d[0],daysData[1].ma5d[0]
            if len(tdx_df) > 0 and 'ma5d' in tdx_df.columns:
                if tdx_df[:1].ma5d[0] is not None and tdx_df[:1].ma5d[0] != 0:
                    df.loc[code, 'ma5d'] = round(float(tdx_df[:1].ma5d[0]), 2)
                if tdx_df[:1].ma10d[0] is not None and tdx_df[:1].ma10d[0] != 0:
                    df.loc[code, 'ma10d'] = round(
                        float(tdx_df[:1].ma10d[0]), 2)
            df.loc[code, 'op'] = opl
            df.loc[code, 'ra'] = ral
            df.loc[code, 'oph'] = oph
            df.loc[code, 'rah'] = rah
            df.loc[code, 'fib'] = fib
            df.loc[code, 'fibl'] = fibl
            # df.fibl.astype(float)
            df.loc[code, 'ldate'] = stl
            df.loc[code, 'boll'] = operation
            df.loc[code,'cumin'] = tdx_df.cumin[-1]

            tdx_df, opkdj = getab.Get_KDJ(tdx_df, dtype='d',lastday=days)
            tdx_df, opmacd = getab.Get_MACD_OP(tdx_df, dtype='d',lastday=days)
            tdx_df, oprsi = getab.Get_RSI(tdx_df, dtype='d',lastday=days)
            # opma = getab.algoMultiDay_trends(tdx_df
            opma = getab.algoMultiDay(tdx_df)
            volstd = getab.powerStd(code=code, df=tdx_df, ptype='vol',lastday=days)
            df.loc[code, 'kdj'] = opkdj
            df.loc[code, 'macd'] = opmacd
            df.loc[code, 'rsi'] = oprsi
            df.loc[code, 'ma'] = opma
            df.loc[code, 'vstd'] = volstd
            df.loc[code, 'lvolume'] = tdx_df.vol[1]

            if wcdf_code is not None and code in wcdf_code:
                df.loc[code, 'category'] = wcdf.loc[code, 'category']
            else:
                wencai_drop.append(code)
                log.warn("code not in wcdf:%s" % (code))
            # else:
                # df.loc[code,'category'] = 0

            # df = getab.Get_BBANDS(df, dtype='d')
            #'volume', 'ratio', 'couts','ldate' -> 'ma','macd','rsi','kdj'
            # df = df.drop_duplicates()
        df = df.fillna(0)

        # df['df2b'] = (map(lambda ra, fibl,rah,fib,ma,kdj,rsi:round(eval(ct.powerdiff%(ct.PowerCountdl)),1),\
        #                  df['ra'].values, df['fibl'].values,df['rah'].values,df['fib'].values,df['ma'].values,\
        #                  df['kdj'].values,df['rsi'].values))
#        if "fib" not in df.columns:
#            df['fib'] = 0
        def compute_df2(df):
           df['df2b'] = (map(lambda ra, fibl, rah, fib, ma, kdj, rsi: (eval(ct.powerdiff % (dl))),
                     df['ra'].values, df['fibl'].values, df[
                         'rah'].values, df['fib'].values, df['ma'].values,
                     df['kdj'].values, df['rsi'].values))
           df['df2b'] = df['df2b'].apply(lambda x:round(x,1))
           return df

        if len(df) <> len(code_l):
            dd = df.loc[code_l]
            dd = compute_df2(dd)
            df = cct.combine_dataFrame(df, dd, col=None)
        else:
            df = compute_df2(df)
        # df = df.replace(np.inf,0)
        # df = df.replace(-np.inf,0)
        # df = df.fillna(0)

    if len(drop_cxg) > 0:
        drop_cxg = list(set(drop_cxg))
        code_l = [co for co in code_l if co not in drop_cxg]
        drop_t = [co for co in drop_cxg if co in df.index]
        if len(drop_t) > 0:
            Power_CXG_Error += 1
            df = df.drop(drop_t, axis=0)
            cct.GlobalValues()
            cct.GlobalValues().setkey('dropcxg', drop_cxg)
            cct.GlobalValues().setkey('Power_CXG_Error', Power_CXG_Error)

            if Power_CXG_Error < 2:
                log.error("Drop_cxg open!!! drop_t:%s %s" %
                          (drop_t, len(drop_cxg)))
    if len(wencai_drop) > 0:
        cct.GlobalValues().setkey('wencai_drop', wencai_drop)

    # print "global:%s"%(cct.GlobalValues().getkey('dropcxg'))

    h5 = h5a.write_hdf_db(h5_fname, df.loc[code_l], table=h5_table, append=True)

    print "Power:%0.2f" % (time.time() - ts),

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
    # op, ra, st, days = get_linear_model_status('999999', filter='y', dl=14, ptype='low')
    # print days[0]

    # print get_linear_model_status('600671', filter='y', dl=10, ptype='high')
    # print get_linear_model_status('600671', filter='y', start='20160329', ptype='low')
    # print get_linear_model_status('600671', filter='y', start='20160329', ptype='high')
    # print get_linear_model_status('999999', filter='y', dl=30, ptype='high')
    # print get_linear_model_status('999999', filter='y', dl=30, ptype='low')
    # powerCompute_df(top_temp,dl=ct.PowerCountdl,talib=True)

    # import sina_data
    # codelist = sina_data.Sina().market('cyb').code.tolist()

    # df = powerCompute_df(['603689', '300506', '002171'], days=ct.Power_last_da, dtype='d', end=None, dl=ct.PowerCountdl, talib=True, filter='y')
#    df = powerCompute_df(['603689', '300506', '002171'], days=3, dtype='d', end=None, dl=ct.PowerCountdl, talib=True, filter='y')
    # df = powerCompute_df(['999999','399006'], days=0, dtype='d', end=None, dl=ct.PowerCountdl, talib=True, filter='y')
    df = powerCompute_df(['999999','399006','399001'], days=0, dtype='d', end=None, dl=ct.PowerCountdl, talib=True, filter='y',index=True)

    print "\n",cct.format_for_print(df.loc[:,['ra', 'op', 'ma', 'rsi', 'kdj',
                     'boll', 'rah', 'df2b', 'fibl', 'macd', 'vstd', 'oph', 'lvolume']])
    # print "\n",df.fibl,df.fib
    print "\n",cct.format_for_print(df.loc[:,['op','boll','ma','kdj','macd','ldate','fibl','fib','timel']])
    # import ipdb;ipdb.set_trace()

    # powerCompute_df(codelist, dtype='d',end=None, dl=ct.PowerCountdl, talib=True,filter='y')

    # # print powerCompute_df(['601198', '002791', '000503'], dtype='d', end=None, dl=30, filter='y')
    # print get_linear_model_status('999999', filter='y', dl=34, ptype='low', days=1)
    # print get_linear_model_status('399006', filter='y', dl=34, ptype='low',
    # days=1)
    sys.exit()
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
                if args.start is not None and len(args.start) <= 4:
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
                                             filter=args.filter, dl=args.dl, days=args.days)
                else:
                    args.filter = 'y'
                    for ptype in ['low', 'high']:
                        op, ra, st, daysData = get_linear_model_status(args.code, dtype=args.dtype, start=start, end=end,
                                                                       days=args.days, ptype=ptype, filter=args.filter,
                                                                       dl=args.dl)
                        # print "%s op:%s ra:%s days:%s  start:%s" %
                        # (args.code, op, str(ra), str(daysData[0]), st)
                        print "op:%s ra:%s days:%s  start:%s" % (op, str(ra), str(daysData[0]), st)
                        # op, ra, st, daysData  = get_linear_model_status(args.code, dtype=args.dtype, start=cct.day8_to_day10(
                        # args.start), end=cct.day8_to_day10(args.end), filter=args.filter, dl=args.dl)
                # print "code:%s op:%s ra/days:%s  start:%s" % (code, op,
                # str(ra) + '/' + str(daysData[0]), st)
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
