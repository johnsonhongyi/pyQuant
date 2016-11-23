# -*- coding: utf-8 -*-


from feedutil import dataFramefeed
import sys
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
log = LoggerFactory.getLogger("powerTech")
log.setLevel(LoggerFactory.INFO)

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
def get_linear_model_ratio(asset, type='M', nowP=None,days=1,only=False):
    # duration = asset[-1:].index.values[0]
    # log.debug("duration:%s" % duration)
    # # log.debug("duration:%s" % cct.get_today_duration(duration))
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
        log.info("status up np:%0.2f now:%.2f head:%.2f dt:%s"%(asset[-1],Y_hat[-1],Y_hat[0],asset.index[-1]))
        price_status = stock_up
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
            log.info("mid:%.2f"%(Y_Future[-1]))
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
            log.info("Bottom:%.2f"%(Y_Future[-1]))

        elif type.upper() == 'H':
            i = (asset.values.T - Y_hat).argmax()
            c_high = X[i] * b + a - asset.values[i]
            # Y_hathigh = X * b + a - c_high
            Y_Future = X * b + a - c_high
            # Y_Future = Y * b + a - c_high
            # log.info("Type:H ratio: %0.1f %0.1f Y_Mid: %0.1f" %
            # (b, ratio, Y_Future[-1]))
            log.info("Top:%.2f"%(Y_Future[-1]))

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
        return operation, ratio,price_status
    else:
        log.info("status down np:%0.2f now:%.2f head:%.2f dt:%s"%(asset[-1],Y_hat[-1],Y_hat[0],asset.index[-1]))
        price_status = stock_down

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
        return operation, ratio,price_status
        # log.debug("Line down !!! d:%s" % Y_hat[0])
        # print("Line down !!! d:%s nowp:%s" % (round(Y_hat[1],2),asset[-1:].values[0]))
        # return -3, round(ratio, 2)
        #

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

if __name__ == "__main__":
    # df = tdd.get_tdx_append_now_df_api('399006',start=20160912)
    df = tdd.get_tdx_append_now_df_api('399006',dl=30)
    # print df[-1:]
    # print get_linear_model_status('000002',dl=60)
    print get_linear_model_ratio(df.close,type='H',days=0,only=True)
    print get_linear_model_ratio(df.close,type='M',days=1,only=True)
    print get_linear_model_ratio(df.close,type='L',days=1,only=True)
