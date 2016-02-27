# -*- coding:utf-8 -*-
# ������Ҫ�õ��Ŀ�
# %matplotlib inline
import os
import sys

sys.path.append("..")
import numpy as np
import statsmodels.api as sm
from statsmodels import regression
from JohhnsonUtil import LoggerFactory as LoggerFactory
from JohhnsonUtil import commonTips as cct

log = LoggerFactory.getLogger(os.path.basename(sys.argv[0]))
# log.setLevel(LoggerFactory.DEBUG)
from JSONData import tdx_data_Day as tdd


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


def get_linear_model_status(code, ptype='f', df=None, dtype='d', type='m', start=None, end=None, days=1, filter='n'):
    if start is not None and filter=='y':
        if code not in ['999999','399006','399001']:
            index_d,dl=tdd.get_duration_Index_date(dt=start)
            log.debug("index_d:%s dl:%s"%(str(index_d),dl))
        else:
            index_d=cct.day8_to_day10(start)
            log.debug("index_d:%s"%(index_d))
        start=tdd.get_duration_price_date(code,ptype='low',dt=index_d)
        log.debug("start: %s"%(start))
    if df is None:
        # df = tdd.get_tdx_append_now_df(code,ptype, start, end).sort_index(ascending=True)
        df = tdd.get_tdx_append_now_df_api(code, ptype, start, end).sort_index(ascending=True)
    log.info("Code:%s start:%s end:%s"%(code,start,df[-1:].index.values[0]))
    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)
    # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
    def get_linear_model_ratio(asset):
        log.info("asset:%s" % asset[-1:])
        duration=asset[-1:].index.values[0]
        log.debug("duration:%s"%duration)
        log.debug("duration:%s"%cct.get_today_duration(duration))
        # log.debug("duration:%s"%cct.get_duration_date(duration))
        asset = asset.dropna()
        X = np.arange(len(asset))
        x = sm.add_constant(X)
        model = regression.linear_model.OLS(asset, x).fit()
        a = model.params[0]
        b = model.params[1]
        log.info("X:%s a:%0.1f b:%0.1f" % (len(asset), a, b))
        Y=np.append(X,X[-1]+int(days))
        log.debug("X:%s Y:%s" % (X[-1],Y[-1]))
        # print ("X:%s" % (X[-1]))
        Y_hat = X * b + a
        # Y_hat_t = Y * b + a
        # log.info("Y_hat:%s " % (Y_hat))
        # log.info("asset:%s " % (asset.values))
        ratio = b/a*100
        operation=0
        if Y_hat[-1] > Y_hat[1]:
            log.debug("u-Y_hat[-1]:%0.1f" % (Y_hat[-1]))
            log.debug("price:%0.1f" % asset.iat[-1])
            log.debug("u:%0.1f" % Y_hat[1])
            log.debug("price:%0.1f" % asset.iat[1])
            if type.upper() == 'M':
                Y_Future = Y * b + a 
                # ratio = b/a*100
                log.info("ratio: %0.1f %0.1f Y_Mid: %0.1f"%(b,ratio,Y_Future[-1]))
                # diff = asset.iat[-1] - Y_hat[-1]
                # if diff > 0:
                    # return True, len(asset), diff
                # else:
                    # return False, len(asset), diff
            elif type.upper() == 'L':
                i = (asset.values.T - Y_hat).argmin()
                c_low = X[i] * b + a - asset.values[i]
                # Y_hatlow = X * b + a - c_low
                Y_Future = Y * b + a - c_low
                log.info("b: %0.1f ratio:%0.1f Y_Mid: %0.1f"%(b,ratio,Y_Future[-1]))
                # diff = asset.iat[-1] - Y_hatlow[-1]
                # if asset.iat[-1] - Y_hatlow[-1] > 0:
                    # return True, len(asset), diff
                # else:
                    # return False, len(asset), diff
            elif type.upper() == 'H':
                i = (asset.values.T - Y_hat).argmax()
                c_high = X[i] * b + a - asset.values[i]
                # Y_hathigh = X * b + a - c_high
                Y_Future = Y * b + a - c_high
                log.info("ratio: %0.1f %0.1f Y_Mid: %0.1f"%(b,ratio,Y_Future[-1]))
            diff = asset[-1] - Y_Future[-1]
            # print ("as:%s Y:%s"%(asset[-1] ,Y_Future[-1]))
            if diff > 0:
                operation +=1
                log.info("UP !!%s Y_Future: %0.1f b:%0.1f ratio:%0.1f "%(type.upper(),Y_Future[-1],b,ratio))
            else:
                log.info("Down %s Y_Future: %0.1f b:%0.1f ratio:%0.1f"%(type.upper(),Y_Future[-1],b,ratio))
            return operation,ratio
        else:
            log.debug("down !!! d:%s" % Y_hat[1])
            print("down !!! d:%s" % Y_hat[1])
            return 0, 0
    # print "high:",
    operationcount=0
    ratio_l=[]
    for co in ['high','close','low']:
        # for co in ['high','close','low']:
        op,ratio=get_linear_model_ratio(df[co])
        ratio_l.append(round(ratio,2))
        operationcount +=op
    log.info("op:%s min:%s ratio_l:%s"%(operationcount,min(ratio_l),ratio_l))
    return operationcount,ratio.min()


def parseArgmain():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('code', type=str, nargs='?', help='999999')
    parser.add_argument('start', nargs='?', type=str, help='20150612')
    parser.add_argument('end', nargs='?', type=str, help='20160101')
    parser.add_argument('-d', action="store", dest="dtype", type=str, nargs='?', choices=['d', 'w', 'm'], default='d',
                        help='DateType')
    parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['f', 'b'], default='f',
                        help='Price Forward or back')
    return parser

def maintest(code,start=None,type='m',filter='y'):
    import timeit
    run=1
    strip_tx = timeit.timeit(lambda : get_linear_model_status(code, start=start,type=type,filter=filter), number=run)
    print("ex Read:", strip_tx)
if __name__ == "__main__":

    print "H"
    # log.setLevel(LoggerFactory.DEBUG)
    log.setLevel(LoggerFactory.INFO)
    # st=get_linear_model_status('300380',start='2016-01-28',type='h',filter='y')
    st = get_linear_model_status('000025')
    # st=get_linear_model_status('300380',start='2016-01-28',filter='y')
    # maintest('002189',start='2016-01-28',type='h',filter='y')
    print "M:"
    # st=get_linear_model_status('002189',start='2016-01-28',filter='y')
    # maintest('002189',start='2016-01-28',filter='y')
    print "L"
    # st=get_linear_model_status('002189',start='2016-01-28',type='l',filter='y')
    # maintest('002189',start='2016-01-28',type='l',filter='y')
    # cct.set_console(100, 15)

