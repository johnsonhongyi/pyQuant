 # -*- coding:utf-8 -*-
 #
import sys
from JSONData import powerCompute as pct
from JSONData import LineHistogram as lht
from JSONData import wencaiData as wcd
from JSONData import get_macd_kdj_rsi as getab
import JohnsonUtil.johnson_cons as ct
from JohnsonUtil import commonTips as cct
from JohnsonUtil import LoggerFactory as LoggerFactory
log = LoggerFactory.log


import argparse
def parseArgmain():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('code', type=str, nargs='?', help='999999')
        parser.add_argument('start', nargs='?', type=str, help='20150612')
        parser.add_argument('end', nargs='?', type=str, help='20160101')
        parser.add_argument('-d', action="store", dest="dtype", type=str, nargs='?', choices=['d', 'w', 'm'], default='d',help='DateType')
        parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['f', 'b'], default='f',help='Price Forward or back')
        parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['high', 'low', 'close'], default='low',help='price type')
        parser.add_argument('-f', action="store", dest="filter", type=str, choices=['y', 'n'], default='y',help='find duration low')
        parser.add_argument('-l', action="store", dest="dl", type=int, default=ct.linePowerCountdl,help='dl default=%s'%(ct.linePowerCountdl))
        parser.add_argument('-da', action="store", dest="days", type=int, default=ct.Power_last_da,help='days')
        parser.add_argument('-m', action="store", dest="mpl", type=str, default='y',help='mpl show')
        parser.add_argument('-i', action="store", dest="line", type=str, choices=['y', 'n'], default='y', help='LineHis show')
        parser.add_argument('-w', action="store", dest="wencai", type=str, choices=['y', 'n'], default='n',help='WenCai Search')
        return parser
    except Exception, e:
        # print 'Eerror:',e
        pass
        # raise "Error"
    else:
        # print 'Eerror:'
        pass
    finally:
        # print 'Eerror:'
        pass


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
    # print powerCompute_df(['300134','002171'], dtype='d',end=None, dl=10, filter='y')
    # # print powerCompute_df(['601198', '002791', '000503'], dtype='d', end=None, dl=30, filter='y')
    # print get_linear_model_status('999999', filter='y', dl=34, ptype='low', days=1)
    # print pct.get_linear_model_status('601519', filter='y', dl=34, ptype='low', days=1)
    # sys.exit()
    import re
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
            # if not code.lower() == 'q' and not code.lower() == 'quit' and not code.lower() == 'exit' and not code == 'q' and not code == 'e' and not str(args.code) == 'None' and (args.wencai == 'y' or re.match('[a-zA-Z]+',code) is not None  or re.match('[ \u4e00 -\u9fa5]+',code) == None ):

            if not code.lower() == 'q' and not code.lower() == 'quit' and not code.lower() == 'exit' and not code == 'q' and not code == 'e' \
                and not str(args.code) == 'None' and (args.wencai == 'y' and (re.match('[a-zA-Z]+',code) is  None  and re.match(ur"[\u4e00-\u9fa5]+",code) is not None ) ):
                df  = wcd.get_wencai_Market_url(code,200,pct=False)
                print df.shape,df[:8]
                if len(df) == 1:
                    if re.match('[ \u4e00 -\u9fa5]+',code) == None:
                        args.code = df.code.values[0]
                    start = cct.day8_to_day10(args.start)
                    end = cct.day8_to_day10(args.end)
                    args.filter = 'y'
                    for ptype in ['low', 'high']:
                        op, ra, st, days = pct.get_linear_model_status(args.code,df=None, dtype=args.dtype, start=start, end=end,
                                                                   days=args.days, ptype=ptype, filter=args.filter,
                                                                   dl=args.dl)
                        # print "%s op:%s ra:%s days:%s  start:%s" % (args.code, op, str(ra), str(days[0]), st)
                        print "op:%s ra:%s days:%s  start:%s" % (op, str(ra), str(days[0]), st)


            elif len(str(args.code)) == 6:
                if args.start is not None and len(args.start) <= 4:
                    args.dl = int(args.start)
                    args.start = None
                start = cct.day8_to_day10(args.start)
                end = cct.day8_to_day10(args.end)
                df = None
                if args.line == 'y' and args.mpl == 'y':
                    code = args.code
                    args.filter = 'n'
                    df=lht.get_linear_model_histogramDouble(code, dtype=args.dtype, start=start, end=end,filter=args.filter, dl=args.dl)
                    # candlestick_powercompute(code,start, end)

                    # op, ra, st, days = pct.get_linear_model_status(code,df=df, start=start, end=end, filter=args.filter)
                    # print "%s op:%s ra:%s  start:%s" % (code, op, ra, st)
                    # print "op:%s ra:%s  start:%s" % (op, ra, st)
                    args.filter = 'y'
                    for ptype in ['low', 'high']:
                        op, ra, st, days = pct.get_linear_model_status(args.code,df=df, dtype=args.dtype, start=start, end=end,
                                                                   days=args.days, ptype=ptype, filter=args.filter,
                                                                   dl=args.dl)
                        # print "%s op:%s ra:%s days:%s  start:%s" % (args.code, op, str(ra), str(days[0]), st)
                        print "op:%s ra:%s days:%s  start:%s" % (op, str(ra), str(days[0]), st)
                        if ptype == 'low':
                            ral = ra
                            opl = op
                            stl = st
                            fibl = int(days[0])
                        else:
                            oph = op
                            rah = ra
                            fib = int(days[0])
                            ra = ral

                    # p=multiprocessing.Process(target=get_linear_model_histogramDouble,args=(code, args.ptype, args.dtype, start, end,args.vtype,args.filter,))
                    # p.daemon = True
                    # p.start()
                    # p.join()
                    # time.sleep(6)
                    # num_input = ''
                # else:
                #     code = args.code
                #     if len(code) == 6:
                #         start = cct.day8_to_day10(args.start)
                #         end = cct.day8_to_day10(args.end)
                #         get_linear_model_histogramDouble(code, args.ptype, args.dtype, start, end, args.vtype)
                #         # get_linear_model_histogramDouble(code, args.ptype, args.dtype, start, end, args.vtype)
                #         # candlestick_powercompute(code,start, end)
                #         op, ra, st, days = pct.get_linear_model_status(code, start=start, end=end, filter=args.filter)
                #         print "code:%s op:%s ra:%s  start:%s" % (code, op, ra, st)

                if args.mpl == 'y':
                    # from multiprocessing import Process
                    # p = Process(target=pct.get_linear_model_candles, args=(args.code,args.ptype,args.dtype, start, end,args.filter,df,args.dl,args.days,))
                    #   # (args.code,args.ptype,args.dtype, start, end,args.filter,df,args.dl,args.days)
                    # p.start()
                    # p.join()
                    pct.get_linear_model_candles(args.code, dtype=args.dtype, start=start, end=end, ptype=args.ptype,
                                             filter=args.filter,df=df,dl=args.dl,days=args.days)
                else:
                    args.filter = 'y'
                    for ptype in ['low', 'high']:
                        op, ra, st, days = pct.get_linear_model_status(args.code,df=df, dtype=args.dtype, start=start, end=end,
                                                                   days=args.days, ptype=ptype, filter=args.filter,
                                                                   dl=args.dl)
                        # print "%s op:%s ra:%s days:%s  start:%s" % (args.code, op, str(ra), str(days[0]), st)
                        print "op:%s ra:%s days:%s  start:%s" % (op, str(ra), str(days[0]), st)
                        if ptype == 'low':
                            ral = ra
                            opl = op
                            stl = st
                            fibl = (days[0])
                        else:
                            oph = op
                            rah = ra
                            fib = (days[0])
                            ra = ral
                        # op, ra, st, days = get_linear_model_status(args.code, dtype=args.dtype, start=cct.day8_to_day10(
                        # args.start), end=cct.day8_to_day10(args.end), filter=args.filter, dl=args.dl)
                # print "code:%s op:%s ra/days:%s  start:%s" % (code, op, str(ra) + '/' + str(days), st)
                # 'ra * fibl + rah*(abs(int(%s)-fibl))/fib +ma +kdj+rsi'
                boll,kdj,macd,rsi,ma,bollCT = getab.get_All_Count(args.code,dl=args.dl,start=start, end=end,days=ct.Power_Ma_Days,lastday=args.days)
                # print ""
                # print "ral,opl,fibl,oph,rah,fib,kdj,macd,rsi,ma=",ral,opl,fibl,oph,rah,fib,kdj,macd,rsi,ma
                # ra, fibl,rah,fib,ma,kdj,rsi
                # for x in [boll,kdj,macd,rsi,ma,bollCT,ra,fibl,rah,`]:
                #     print type(x),x
                # print args.dl,ra,fibl,rah,op
                # print ra * fibl + rah*(abs(int(args.dl)-fibl))/fib +ma +kdj+rsi

                diff=eval(ct.powerdiff%(ct.linePowerCountdl))
                print "Diff:%.1f"%(diff)
                cct.sleep(0.1)
                # ts=time.time()
                # time.sleep(5)
                # print "%0.5f"%(time.time()-ts)
            elif code.lower() == 'q' or code.lower() == 'quit' or code.lower() =='exit':
                sys.exit(0)

            elif code == 'h' or code == 'help':
                parser.print_help()
            else:
                pass
        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
        except (IOError, EOFError, Exception) as e:
            # print "Error", e
            import traceback
            traceback.print_exc()
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











    # elif len(num_input) == 6:
    #                 code = args.code
    #                 # print code, args.ptype, args.dtype, start, end
    #                 lht.get_linear_model_histogramDouble(code, args.ptype, args.dtype, start, end, args.vtype, args.filter)
    #                 # candlestick_powercompute(code,start, end)
    #                 op, ra, st, days = pct.get_linear_model_status(code, start=start, end=end, filter=args.filter)
    #                 print "code:%s op:%s ra:%s  start:%s" % (code, op, ra, st)
    #                 # p=multiprocessing.Process(target=get_linear_model_histogramDouble,args=(code, args.ptype, args.dtype, start, end,args.vtype,args.filter,))
    #                 # p.daemon = True
    #                 # p.start()
    #                 # p.join()
    #                 # time.sleep(6)
    #                 num_input = ''

    #         else:
    #             code = args.code
    #             if len(code) == 6:
    #                 start = cct.day8_to_day10(args.start)
    #                 end = cct.day8_to_day10(args.end)
    #                 get_linear_model_histogramDouble(code, args.ptype, args.dtype, start, end, args.vtype)
    #                 # get_linear_model_histogramDouble(code, args.ptype, args.dtype, start, end, args.vtype)
    #                 # candlestick_powercompute(code,start, end)
    #                 op, ra, st, days = pct.get_linear_model_status(code, start=start, end=end, filter=args.filter)
    #                 print "code:%s op:%s ra:%s  start:%s" % (code, op, ra, st)