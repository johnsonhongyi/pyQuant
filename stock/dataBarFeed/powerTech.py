# -*- coding: utf-8 -*-


import sys
from feedutil import dataFramefeed
sys.path.append("..")
from JSONData import tdx_data_Day as tdd
from JSONData import powerCompute as pct
from JSONData import get_macd_kdj_rsi as getab
from JohhnsonUtil import commonTips as cct
from JohhnsonUtil import LoggerFactory as LoggerFactory
import numpy as np
# import pandas as pd
import statsmodels.api as sm
from statsmodels import regression
# log = LoggerFactory.getLogger("powerTech")
log = LoggerFactory.log
# log.setLevel(LoggerFactory.INFO)
log.setLevel(LoggerFactory.WARN)

def get_tdx_barfeed(code,start=None):

    df = tdd.get_tdx_append_now_df_api(code,start=start)
    df.rename(columns={'vol': 'volume'}, inplace=True)
    df = df.sort_index(ascending=True)
    barfeed = dataFramefeed.Feed()
    barfeed.addBarsFromDataFrame(code, df)
    # print barfeed.get_dataFrame()
    return barfeed

def get_power_status(code,tdx_df=None,dtype='d',start=None, end=None, filter='y',
                            dl=60,ptype='low'):
    opc,rac=0,0
    fib = 0
    # for ptype in ['low', 'high']:
    for ptype in ['low']:
            op, ra, st, daysData  = pct.get_linear_model_status(
                code, df=tdx_df, dtype=dtype, start=start, end=end, dl=dl, filter=filter, ptype=ptype)
            # fib.append(str(daysData[0]))
            opc += op
            # print ra
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

    tdx_df,opkdj = getab.Get_KDJ(tdx_df, dtype='d')
    tdx_df,opmacd = getab.Get_MACD_OP(tdx_df, dtype='d')
    tdx_df,oprsi = getab.Get_RSI(tdx_df, dtype='d')
    opma = getab.algoMultiDay(tdx_df)
    # df = getab.Get_BBANDS(df, dtype='d')
    #'volume', 'ratio', 'counts','ldate' -> 'ma','macd','rsi','kdj'
    return int(opc),(rac),int(fib),int(fibl),stl,int(operation),int(opkdj),int(opmacd),int(oprsi),int(opma)

# status
stock_up = 1
stock_down = 0

def get_duration_filter(code, df=None, dtype='d', start=None, end=None,dl=None, filter=True,ptype='low',power=True):
    if start is not None and end is None and filter:
        index_d = cct.day8_to_day10(start)
        start = tdd.get_duration_price_date(code, ptype=ptype, dt=start, df=df,dl=dl,power=power)
        log.debug("start is not None start: %s  index_d:%s" % (start, index_d))
    elif end is not None and filter:
        df = tdd.get_tdx_append_now_df_api(code, start=start, end=end,df=df,dl=dl,power=power).sort_index(ascending=True)
        index_d = cct.day8_to_day10(start)
        start = tdd.get_duration_price_date(code, ptype=ptype, dt=start, df=df,dl=dl, power=power)
        df = df[df.index >= start]
        if len(df) > 2 and dl is None:
            if df.index.values[0] < index_d:
                df = df[df.index >= index_d]
    if dl is not None:
        if power:
            start, index_d, df = tdd.get_duration_price_date(
                code, ptype=ptype, dl=dl, filter=False, df=df,power=True)
        else:
            start, index_d = tdd.get_duration_price_date(
                code, ptype=ptype, dl=dl, filter=False, df=df,power=False)
        log.debug("dl not None code:%s start: %s  index_d:%s" % (code, start, index_d))

    if len(df) > 0 and  df is not None:
        df = df.sort_index(ascending=True)
        df = df[df.index >= start]

    if len(df) ==0 or df is None :
        if start is not None and len(start) > 8 and int(start[:4]) > 2500:
            log.warn("code:%s ERROR:%s" % (code, start))
            start = '2016-01-01'
        df = tdd.get_tdx_append_now_df_api(
            code, start,end).sort_index(ascending=True)
        if start is None:
            start = df.index.values[0]
        if len(df) > 2 and dl is None and start is not None and filter:
            if df.index.values[0] < index_d:
                df = df[df.index >= index_d]

    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(
            df, dtype).sort_index(ascending=True)
    return df

def get_linear_model_ratio(asset, type='M', nowP=None,days=1,only=False):
    asset = asset.sort_index(ascending=True)
    price_status = stock_down
    if only and days > 0:
        asset = asset[:-days]
    asset = asset.dropna()
    X = np.arange(len(asset))
    x = sm.add_constant(X)
    model = regression.linear_model.OLS(asset.astype(float), x).fit()
    a = model.params[0]
    b = model.params[1]
    Y = np.append(X, X[-1] + int(days))
    Y_hat = X * b + a
    if a != 0:
        ratio = b / a * 100
    else:
        ratio = 0
    operation = 0
    if Y_hat[-1] > Y_hat[0]:
        log.info("status up np:%0.2f now:%.2f head:%.2f dt:%s"%(asset[-1],Y_hat[-1],Y_hat[0],asset.index[-1]))
        price_status = stock_up
        if type.upper() == 'M':
            Y_Future = X * b + a
            log.info("mid:%.2f"%(Y_Future[-1]))
        elif type.upper() == 'L':
            i = (asset.values.T - Y_hat).argmin()
            c_low = X[i] * b + a - asset.values[i]
            Y_Future = X * b + a - c_low
            log.info("Bottom:%.2f"%(Y_Future[-1]))

        elif type.upper() == 'H':
            i = (asset.values.T - Y_hat).argmax()
            c_high = X[i] * b + a - asset.values[i]
            Y_Future = X * b + a - c_high
            log.info("Top:%.2f"%(Y_Future[-1]))

        if nowP is not None:
            diff = nowP - Y_Future[-1]
        else:
            diff = asset[-1] - Y_Future[-1]
        if diff > 0:
            operation += 1
        return operation, ratio,price_status
    else:
        log.info("status down np:%0.2f now:%.2f head:%.2f dt:%s"%(asset[-1],Y_hat[-1],Y_hat[0],asset.index[-1]))
        price_status = stock_down

        if type.upper() == 'M':
            Y_Future = X * b + a
        elif type.upper() == 'L':
            i = (asset.values.T - Y_hat).argmin()
            c_low = X[i] * b + a - asset.values[i]
            Y_Future = X * b + a - c_low
        elif type.upper() == 'H':
            i = (asset.values.T - Y_hat).argmax()
            c_high = X[i] * b + a - asset.values[i]
            Y_Future = X * b + a - c_high
        if nowP is not None:
            diff = nowP - Y_Future[-1]
        else:
            diff = asset[-1] - Y_Future[-1]
        if diff > 0:
            # operation += 1
            pass
        else:
            operation -= 1
        return operation, ratio,price_status


def get_linear_model_rule(code,df=None,dl=30,type='M', nowP=None,days=1,only=False,ptype='low'):

    # if isinstance(code,str) or isinstance(code,int):
    dd = []
    if ptype == 'high':
        dd = get_duration_filter(code,df=df,dl=dl,ptype=ptype)
        if len(dd) == 1:
            df = get_duration_filter(code,df=df,dl=dl,ptype='low')
        else:
            df = dd
    else:
        df = get_duration_filter(code,df=df,dl=dl,ptype=ptype)

    if len(df) < 2:
        return 10,10,10,len(df)


    if ptype == 'high':
        if len(dd) == 1:
            statusdl = len(dd)
        else:
            statusdl  = len(df)
    else:
        statusdl = len(df)

    operation = 0
    price_status = stock_down
    for co in ['low', 'high', 'close']:
        asset = df[co]
        asset = asset.sort_index(ascending=True)
        # df = asset.copy()
        if only and days > 0:
            asset = asset[:-days]
        asset = asset.dropna()
        X = np.arange(len(asset))
        x = sm.add_constant(X)
        model = regression.linear_model.OLS(asset.astype(float), x).fit()
        a = model.params[0]
        b = model.params[1]
        Y = np.append(X, X[-1] + int(days))
        Y_hat = X * b + a
        if a != 0:
            ratio = b / a * 100
        else:
            ratio = 0

        Y_FutureM = X * b + a
        log.debug("mid:%.2f"%(Y_FutureM[-1]))

        i = (asset.values.T - Y_hat).argmin()
        c_low = X[i] * b + a - asset.values[i]
        Y_FutureL = X * b + a - c_low
        log.debug("Bottom:%.2f"%(Y_FutureL[-1]))

        i = (asset.values.T - Y_hat).argmax()
        c_high = X[i] * b + a - asset.values[i]
        Y_FutureH = X * b + a - c_high

        log.debug("Top:%.2f"%(Y_FutureH[-1]))

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
            if diff_h > 0 :
                operation += 1
            if diff_l > 0 :
                operation += 1
            log.debug("status up nowp:%0.2f nY_hat:%.2f head:%.2f dt:%s"%(asset[-1],Y_hat[-1],Y_hat[0],asset.index[-1]))
            price_status = stock_up
        else:
            if statusdl > 1 and diff < 0:
                operation -= 1
            if statusdl > 1 and diff_h < 0 :
                operation -= 1
            if statusdl > 1 and diff_l < 0 :
                operation -= 1
                # log.debug("status down nowp:%0.2f nY_hat:%.2f head:%.2f dt:%s"%(asset[-1],Y_hat[-1],Y_hat[0],asset.index[-1]))
                # log.debug("nowdfp:%.2f start:%s end:%s"%(df[-1],asset.index[0],asset.index[-1]))
                # log.debug("Yhat ra:%0.2f X:%s b:%.3f a:%.2f c_low:%.2f c_high:%.2f dt:%s"%(ratio,[-1],b,a,c_low,c_high,asset.index[0]))

    # return price_status,round(ratio,2),statusdl
    return operation,round(ratio,2),price_status,statusdl

def get_linear_model_status(code, df=None, dtype='d', type='m', start=None, end=None, days=1, filter='n',
                            dl=None, countall=True, ptype='low',power=True):

    if start is not None and end is None and filter == 'y':
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
        if power:
            start, index_d, df = tdd.get_duration_price_date(
                code, ptype=ptype, dl=dl, filter=False, df=df,power=power)
        else:
            start, index_d = tdd.get_duration_price_date(
                code, ptype=ptype, dl=dl, filter=False, df=df,power=power)
        log.debug("dl not None code:%s start: %s  index_d:%s" % (code, start, index_d))

    if len(df) > 0 and  df is not None:
        df = df.sort_index(ascending=True)
        df = df[df.index >= start]

    if len(df) ==0 or df is None :
        if start is not None and len(start) > 8 and int(start[:4]) > 2500:
            log.warn("code:%s ERROR:%s" % (code, start))
            start = '2016-01-01'
        df = tdd.get_tdx_append_now_df_api(
            code, start,end).sort_index(ascending=True)
        if start is None:
            start = df.index.values[0]
        if len(df) > 2 and dl is None and start is not None and filter == 'y':
            if df.index.values[0] < index_d:
                df = df[df.index >= index_d]

    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(
            df, dtype).sort_index(ascending=True)


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
        # ratio_l = []
        if countall:
            assetratio = asset
            nowpratio = df['close'][-days] if len(df) > 1 + days else None
            # print assetratio
            op, ratio_l,status,sdl= get_linear_model_rule(code,df=assetratio, nowP=nowpratio,ptype=ptype)
            # print op,ratio,status,sdl
            # ratio_l.append(round(ratio, 2))
            operationcount += op
        else:
            assetratio = asset
            nowpratio = df['close'][-days] if len(df) > 1 + days else None
            op, ratio_l,status,sdl = get_linear_model_rule(code,df=assetratio, nowP=nowpratio,ptype=ptype)
            # ratio_l.append(round(ratio, 2))
            operationcount += op

        return operationcount, (ratio_l), df[:1].index.values[0], [len(df),df[:1]]

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
        if ptype == 'high':
            return 13, 1, cct.get_today(), [len(df),df[:1]]
        else:
            return -10, -10, cct.get_today(), [len(df),df[:1]]

def get_diff_index(code,df=None,start=None,end=None,dl=None,dtype='d',ptype='close'):
    df = get_duration_filter(code,df=df,dl=dl,ptype=ptype)

    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)

    if dl is not None and len(df) > dl:
        df = df[-dl:]
        # print df.index[0]
    asset = df[ptype]

    # log.info("df:%s" % asset[:1])
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
        start = asset.index[0]
        # print start,end
        df1 = tdd.get_tdx_append_now_df_api(code2,start=start,end=end).sort_index(ascending=True)
        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(df1, dtype).sort_index(ascending=True)
        # print df1,asset
        if asset[:1].index[0] > df1[:1].index[0]:
            asset1 = df1.loc[asset.index, ptype]
            # startv = asset1[:1]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 3))
        else:
            df = df[df.index >= df1.index[0]]
            asset = df[ptype]
            asset = asset.dropna()
            # dates = asset.index
            asset1 = df1.loc[df.index, ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 3))

    else:
        if code.startswith('399001'):
            code2 = '399006'
        elif code.startswith('399006'):
            code2 = '399005'
        else:
            code2 = '399006'
        if code2.startswith('3990'):
            start = asset.index[0]
            df1 = tdd.get_tdx_append_now_df_api(code2, start=start,end=end).sort_index(ascending=True)
            if len(df1) < int(len(df) / 4):
                code2 = '399001'
                df1 = tdd.get_tdx_append_now_df_api(code2, start=start,end=end).sort_index(ascending=True)

        if not dtype == 'd':
            df1 = tdd.get_tdx_stock_period_to_type(df1, dtype).sort_index(ascending=True)
        if len(asset) < len(df1):
            asset1 = df1.loc[asset.index, ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 3))
        else:

            df = df[df.index >= df1.index[0]]
            asset = df[ptype]
            asset = asset.dropna()
            # dates = asset.index
            asset1 = df1.loc[df.index, ptype]
            asset1 = asset1.apply(lambda x: round(x / asset1[:1], 3))
    # log.info("code2:%s"%(code2))
    asset2 = asset.apply(lambda x: round(x / asset[:1], 3))
    # print asset.index[-1],asset1.index[-1]
    log.info("code:%s codeR:%s index:%s coden:%s codeRn:%s indexn:%s"%(round(asset[0],2),asset2[0],asset1[0],round(asset[-1],2),round(asset2[-1],2),asset1[-1]))

    return round(asset2[-1],3),round(asset1[-1],3)
    # return False
def LDS( A ):
    m = [0] * len( A ) # starting with m = [1] * len( A ) is not necessary
    for x in range( len( A ) - 2, -1, -1 ):
        for y in range( len( A ) - 1, x, -1 ):
          if m[x] <= m[y] and A[x] > A[y]:
            m[x] = m[y] + 1 # or use m[x]+=1

    #===================================================================
    # Use the following snippet or the one line below to get max_value
    # max_value=m[0]
    # for i in range(m):
    #  if max_value < m[i]:
    #    max_value = m[i]
    #===================================================================
    max_value = max( m )

    result = []
    for i in range( len( m ) ):
        if max_value == m[i]:
          result.append( A[i] )
          max_value -= 1

    return result

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


def detect_peaks_lis(df):
    h = df.loc[:, ['open', 'close', 'high', 'low']]
    highp = h['high'].values
    lowp = h['low'].values
    openp = h['open'].values
    closep = h['close'].values
    # print len(closep)
    # lr = LinearRegression()
    # x = np.atleast_2d(np.linspace(0, len(closep), len(closep))).T
    # lr.fit(x, closep)
    # LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)
    # xt = np.atleast_2d(np.linspace(0, len(closep) + 200, len(closep) + 200)).T
    # yt = lr.predict(xt)
    bV = []
    bP = []
    for i in range(1, len(highp) - 1):
        if highp[i] <= highp[i - 1] and highp[i] < highp[i + 1] and lowp[i] <= lowp[i - 1] and lowp[i] < lowp[
                    i + 1]:
            bV.append(lowp[i])
            bP.append(i)

    d, p = LIS(bV)

    idx = []
    for i in range(len(p)):
        idx.append(bP[p[i]])

    return d,idx

def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None):

    """Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`

    The function can handle NaN's

    See this IPython Notebook [1]_.

    References
    ----------
    .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    Examples
    --------
    # >>> from detect_peaks import detect_peaks
    # >>> x = np.random.randn(100)
    # >>> x[60:81] = np.nan
    # >>> # detect all peaks and plot data
    # >>> ind = detect_peaks(x, show=True)
    # >>> print(ind)
    #
    # >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    # >>> # set minimum peak height = 0 and minimum peak distance = 20
    # >>> detect_peaks(x, mph=0, mpd=20, show=True)
    #
    # >>> x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
    # >>> # set minimum peak distance = 2
    # >>> detect_peaks(x, mpd=2, show=True)
    #
    # >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    # >>> # detection of valleys instead of peaks
    # >>> detect_peaks(x, mph=0, mpd=20, valley=True, show=True)
    #
    # >>> x = [0, 1, 1, 0, 1, 1, 0]
    # >>> # detect both edges
    # >>> detect_peaks(x, edge='both', show=True)
    #
    # >>> x = [-2, 1, -2, 2, 1, 1, 3, 0]
    # >>> # set threshold = 2
    # >>> detect_peaks(x, threshold = 2, show=True)
    """

    # intx = x.values
    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
        # print x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    print ind
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if not valley and ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        from pylab import plt
        print x ,x[ind]
        # fig = plt.figure(figsize=(4,4))
        # ax = fig.add_subplot(111)
        # plt.plot(x, mph, mpd, threshold, edge, valley, ax, ind)
        # plt.plot(x,ind)

        # ax.plot(intx,'k', alpha=0.9)
        # ax.annotate(r'xx',xy = (ind,intx[ind]))
        # ax.plot([ind,intx[ind]],'k')
        plt.plot(x,'b-')
        plt.plot(ind,x[ind],'r*',markersize=9)
        # plt.axes()
        plt.show(block=True)

    return ind,x[ind]


if __name__ == "__main__":
    # df = tdd.get_tdx_append_now_df_api('399006',start=20160912)
#    df = tdd.get_tdx_append_now_df_api('399006',dl=30)
    # print df[-1:]
    code = '002024'
    # code = '999999'
    df = tdd.get_tdx_append_now_df_api(code,dl=30).sort_index(ascending=True)
    # ind = detect_peaks(df.close, mph=0,mpd=10,edge='falling',show=True)
    print detect_peaks(df.close, mph=0,mpd=2,valley=False,show=True)
    print detect_peaks(df.close, mph=0,mpd=2,valley=True,show=True)
    print LDS(df.close)
    # print detect_peaks(df.close, mph=0,mpd=3,threshold=0,valley=False,show=False)
    print detect_peaks_lis(df)
    # ind = detect_peaks(df.close,show=True)
    # print get_diff_index(code,dl=10)
    # print get_linear_model_status(code,dl=30,days=1)
    # print get_linear_model_status(code,dl=30,days=1,ptype='high')
    print get_linear_model_rule(code,days=1,dl=10,only=False,ptype='low')
    print get_linear_model_rule(code,days=1,dl=10,only=False,ptype='high')

    # print get_duration_filter(code,dl=20,ptype='low')[-1:]
#    print get_linear_model_rule(df.close,type='M',days=1,only=True)
#    print get_linear_model_rule(df.close,type='L',days=0,only=True)
