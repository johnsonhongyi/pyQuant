# -*- coding:utf-8 -*-
import sys
sys.path.append("..")

import numpy as np
import statsmodels.api as sm
from statsmodels import regression
from JohhnsonUtil import LoggerFactory as LoggerFactory
from JohhnsonUtil import commonTips as cct

log = LoggerFactory.getLogger("PowerCompute")
# log.setLevel(LoggerFactory.DEBUG)
from JSONData import tdx_data_Day as tdd

if not cct.isMac():
    def set_ctrl_handler():
        import win32api, thread
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


def get_linear_model_status(code, ptype='f', df=None, dtype='d', type='m', start=None, end=None, days=1, filter='n',dl=None):
    # log.setLevel(LoggerFactory.DEBUG)
    # if code == "600760":
        # log.setLevel(LoggerFactory.DEBUG)
    # else:
        # log.setLevel(LoggerFactory.ERROR)
    if start is not None and end is None and filter=='y':
        # if code not in ['999999','399006','399001']:
            # index_d,dl=tdd.get_duration_Index_date(dt=start)
            # log.debug("index_d:%s dl:%s"%(str(index_d),dl))
        # else:
            # index_d=cct.day8_to_day10(start)
            # log.debug("index_d:%s"%(index_d))
        index_d = cct.day8_to_day10(start)
        start = tdd.get_duration_price_date(code,ptype='low',dt=start)
        log.debug("start: %s  index_d:%s"%(start,index_d))
    
    if dl is not None:
        start,index_d = tdd.get_duration_price_date(code,ptype='low',dl=dl,filter=False)
        # start = tdd.get_duration_price_date(code,ptype='low',dl=dl)
        # filter = 'y'
        
    if df is None:
        # df = tdd.get_tdx_append_now_df(code,ptype, start, end).sort_index(ascending=True)
        df = tdd.get_tdx_append_now_df_api(code, ptype, start, end).sort_index(ascending=True)
        # if (start is not None or dl is not None) and filter=='y':
        if dl is None and start is not None  and filter=='y':
            # print df.index.values[0],index_d
            if df.index.values[0] < index_d:
                df = df[df.index > index_d]
    if not dtype == 'd':
        df = tdd.get_tdx_stock_period_to_type(df, dtype).sort_index(ascending=True)
    # df = tdd.get_tdx_Exp_day_to_df(code, 'f').sort_index(ascending=True)
    def get_linear_model_ratio(asset,type='M'):
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
        # if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 1500:
        Y = np.append(X,X[-1]+int(days))
        # else:
            # Y = X
        log.debug("X:%s Y:%s" % (X[-1],Y[-1]))
        # print ("X:%s" % (X[-1]))
        Y_hat = X * b + a
        log.debug("Y_hat:%s"%Y_hat)
        # Y_hat_t = Y * b + a
        # log.info("Y_hat:%s " % (Y_hat))
        # log.info("asset:%s " % (asset.values))
        ratio = b/a*100
        operation=0
        log.debug("line_now:%s src:%s"%(Y_hat[-1],Y_hat[0]))
        if Y_hat[-1] > Y_hat[0]:
            log.debug("u-Y_hat[-1]:%0.1f" % (Y_hat[-1]))
            log.debug("price:%0.1f" % asset.iat[-1])
            log.debug("u:%0.1f" % Y_hat[0])
            log.debug("price:%0.1f" % asset.iat[0])
            if type.upper() == 'M':
                Y_Future = X * b +a
                # Y_Future = Y * b + a 
                # ratio = b/a*100
                log.info("Type:M ratio: %0.1f %0.1f Y_Mid: %0.1f"%(b,ratio,Y_Future[-1]))
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
                log.info("Type:L b: %0.1f ratio:%0.1f Y_Mid: %0.1f"%(b,ratio,Y_Future[-1]))
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
                log.info("Type:H ratio: %0.1f %0.1f Y_Mid: %0.1f"%(b,ratio,Y_Future[-1]))
            # diff = asset[-1] - Y_Future[-1]
            # log.debug("asset:%s Y_Future:%s"%(asset[-1],Y_Future[-1]))
            diff = asset[-1] - Y_Future[-1]
            log.info("as:%s Y:%s"%(asset[-1] ,Y_Future[-1]))
            if diff > 0:
                operation +=1
                log.info("Type: %s UP !!! Y_Future: %0.1f b:%0.1f ratio:%0.1f "%(type.upper(),Y_Future[-1],b,ratio))
            else:
                # operation -=1
                log.info("Type: %s Down Y_Future: %0.1f b:%0.1f ratio:%0.1f"%(type.upper(),Y_Future[-1],b,ratio))
            return operation,ratio
        else:
            log.debug("Line down !!! d:%s" % Y_hat[0])
            # print("Line down !!! d:%s nowp:%s" % (round(Y_hat[1],2),asset[-1:].values[0]))
            return -1, round(ratio,2)
    if len(df) > 1:
        operationcount=0
        ratio_l=[]
        for co in ['high','close','low']:
            for dt in ['H','M','L']:
                op,ratio=get_linear_model_ratio(df[co],dt)
                ratio_l.append(round(ratio,2))
                operationcount +=op
        log.info("op:%s min:%s ratio_l:%s"%(operationcount,min(ratio_l),ratio_l))
        # print ("Code:%s start:%s df-s:%s  end:%s"%(code,start,df[:1].index.values[0],df[-1:].index.values[0]))
        # log.info("Code:%s start:%s df-s:%s  end:%s"%(code,start,df[:1].index.values[0],df[-1:].index.values[0]))
        return operationcount,min(ratio_l),df[:1].index.values[0]
    elif len(df) == 1:
        # log.error("powerCompute code:%s"%(code))
        return -9,0,df.index.values[0]
    else:
        log.error("code:%s Low :%s"%(code,len(df)))
        return -9,-9,cct.get_today()
        

def powerCompute_df(df,dtype='d',end=None,dl=None,filter='y'):
    code_l = df.index.tolist()
    # dtype=dtype
    # df['op']
    for code in code_l:
        if dl is None:
            start=df.loc[code,'date']
            start=cct.day8_to_day10(start)
        else:
            start = None
                
        # end=cct.day8_to_day10(end)
        op,ra,st=get_linear_model_status(code, dtype=dtype, start=cct.day8_to_day10(start), end=cct.day8_to_day10(end),dl=dl,filter=filter)
        df.loc[code,'op']=op
        df.loc[code,'ra']=ra
        # if dl is not None:
            # df.loc[code,'ldate'] = st
        df.loc[code,'ldate'] = st
    return df

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
    parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['f', 'b'], default='f',
                        help='Price Forward or back')
    parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low', 'close'], default='close',
                        help='type')
    parser.add_argument('-f', action="store", dest="filter", type=str, choices=['y', 'n'], default='n',
                        help='find duration low')
    parser.add_argument('-l', action="store", dest="dl", type=str, default=None,
                        help='days')
    return parser

def maintest(code,start=None,type='m',filter='y'):
    import timeit
    run=1
    strip_tx = timeit.timeit(lambda : get_linear_model_status(code, start=start,type=type,filter=filter), number=run)
    print("ex Read:", strip_tx)
if __name__ == "__main__":
    parser = parseArgmain()
    while 1:
        try:    
            # log.setLevel(LoggerFactory.INFO)
            # log.setLevel(LoggerFactory.DEBUG)
            code = raw_input("code:")
            args = parser.parse_args(code.split())
            if len(str(args.code)) == 6:
             # ptype='f', df=None, dtype='d', type='m', start=None, end=None, days=1, filter='n'):
                # print args.end
          
                op,ra,st=get_linear_model_status(args.code, dtype=args.dtype, start=cct.day8_to_day10(args.start), end=cct.day8_to_day10(args.end), filter=args.filter,dl=args.dl)
                print "code:%s op:%s ra:%s  start:%s"%(code,op,ra,st)
                cct.sleep(0.1)
                # ts=time.time()
                # time.sleep(5)
                # print "%0.5f"%(time.time()-ts)
            elif code=='q':
                sys.exit(0)
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

