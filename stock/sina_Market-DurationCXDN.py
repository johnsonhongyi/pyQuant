# -*- coding: utf-8 -*-
# !/usr/bin/env python
#import gc
#import random
import re
import sys
import time

import pandas as pd
import JohhnsonUtil.johnson_cons as ct
import singleAnalyseUtil as sl
from JSONData import powerCompute as pct
from JSONData import stockFilter as stf
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd
from JSONData import LineHistogram as lhg
from JohhnsonUtil import LoggerFactory as LoggerFactory
from JohhnsonUtil import commonTips as cct

# from logbook import Logger,StreamHandler,SyslogHandler
# from logbook import StderrHandler


# def parseArgmain():
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('dt', type=str, nargs='?', help='20150612')
# return parser
def quit(signum, frame):
    print 'You choose to stop me.'
    sys.exit()


def evalcmd(dir_mo):
    end = True
    import readline
    import rlcompleter
    # readline.set_completer(cct.MyCompleter(dir_mo).complete)
    readline.parse_and_bind('tab:complete')
    while end:
        # cmd = (cct.cct_raw_input(" ".join(dir_mo)+": "))
        cmd = (cct.cct_raw_input(": "))
        # cmd = (cct.cct_raw_input(dir_mo.append(":")))
        # if cmd == 'e' or cmd == 'q' or len(cmd) == 0:
        if str(cmd) == 'e' or str(cmd) == 'q':
            break
        elif len(cmd) == 0:
            # print ".",
            continue
        else:
            try:
                if not cmd.find(' =') < 0:
                    exec(cmd)
                else:
                    print eval(cmd)
                print ''
            except Exception, e:
                print e
                # else:
                # print evalcmd(dir_mo)
                # print ''
                # evalcmd(dir_mo)
                # break

if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))
    # StreamHandler(sys.stdout).push_application()
    # log = LoggerFactory.getLogger('root')
    # args = docopt(__doc__,argv=None, help=False, version=None, options_first=False)
    from docopt import docopt
    log = LoggerFactory.log
    args = docopt(cct.sina_doc, version='sina_cxdn')
    # print args,args['-d']
    if args['-d'] == 'debug':
        log_level = LoggerFactory.DEBUG
    elif args['-d'] == 'info':
        log_level = LoggerFactory.INFO
    else:
        log_level = LoggerFactory.ERROR
    # log_level = LoggerFactory.DEBUG if args['-d']  else LoggerFactory.ERROR
    log.setLevel(log_level)

    # if log_level == LoggerFactory.DEBUG:
    # handler=StderrHandler(format_string='{record.channel}: {record.message) [{record.extra[cwd]}]')
    # log.level = log.debug
    # error_handler = SyslogHandler('Sina-M-Log', level='ERROR')

    width, height = 174, 21

    def set_duration_console(duration_date):
        if cct.isMac():
            cct.set_console(width, height)
        else:
            cct.set_console(width, height, title=str(duration_date))
    status = False
    vol = ct.json_countVol
    type = ct.json_countType
    success = 0
    top_all = pd.DataFrame()
    time_s = time.time()
    delay_time = 720000
    # delay_time = cct.get_delay_time()
    First = True
    # blkname = '062.blk'
    blkname = '061.blk'
    block_path = tdd.get_tdx_dir_blocknew() + blkname
    status_change = False
    lastpTDX_DF = pd.DataFrame()
    # dl=60
    ptype = 'high'
    # op, ra, duration_date, days = pct.get_linear_model_status('999999', filter='y', dl=dl, ptype=ptype, days=1)
    # duration_date = ct.duration_date
    duration_date = ct.duration_date_up
    # duration_date = 30
    du_date = duration_date
    # resample = ct.resample_dtype
    resample = 'd'
    newdays = 18
    # print cct.last_tddate(2)
    # end_date = cct.last_tddate(days=int(duration_date/4))
    end_date = cct.last_tddate(days=ct.lastdays)
    ptype = 'high'
    filter = 'y'
    if len(str(duration_date)) < 4:
        # duration_date = tdd.get_duration_price_date('999999', dl=duration_date, end=end_date, ptype='dutype')
        du_date = tdd.get_duration_Index_date('999999', dl=duration_date)
        if cct.get_today_duration(du_date) <= 3:
            duration_date = 5
            print("duaration: %s duration_date:%s" % (cct.get_today_duration(du_date), duration_date))
        log.info("duaration: %s duration_date:%s" % (cct.get_today_duration(du_date), duration_date))
    set_duration_console(du_date)
    percent_status = 'n'
    # all_diffpath = tdd.get_tdx_dir_blocknew() + '062.blk'
    parser = cct.MoniterArgmain()
    parserDuraton = cct.DurationArgmain()
    market_sort_value, market_sort_value_key = ct.get_market_sort_value_key(ct.sort_value_key_perd)
    while 1:
        try:
            '''
            # df = sina_data.Sina().all
            df = rl.get_sina_Market_json('cyb')
            # df = rl.get_sina_Market_json('sz')
            top_now = rl.get_market_price_sina_dd_realTime(df, vol, type)
            # top_dif = top_now
            # top_now.to_hdf("testhdf5", 'marketDD', format='table', complevel=9)
            '''
            # top_now = tdd.getSinaAlldf(market='cx', vol=ct.json_countVol, vtype=ct.json_countType)
            # top_now = tdd.getSinaAlldf(market='央企',filename='yqg', vol=ct.json_countVol, vtype=ct.json_countType)
            # top_now = tdd.getSinaAlldf(market=u'一带一路',filename='ydyl', vol=ct.json_countVol, vtype=ct.json_countType)
            # top_now = tdd.getSinaAlldf(market='次新股',filename='cxg', vol=ct.json_countVol, vtype=ct.json_countType)
            time_Rt = time.time()
            top_now = tdd.getSinaAlldf(market='雄安新区', filename='xaxq', vol=ct.json_countVol, vtype=ct.json_countType)
#            top_now = tdd.getSinaAlldf(market=u'京津冀', filename='beijing', vol=ct.json_countVol, vtype=ct.json_countType)
            # top_now = tdd.getSinaAlldf(market='sh', vol=ct.json_countVol, vtype=ct.json_countType)

            now_count = len(top_now)
            radio_t = cct.get_work_time_ratio()
            # top_now = top_now[top_now.buy > 0]
            time_d = time.time()
            if time_d - time_s > delay_time:
                status_change = True
                time_s = time.time()
                top_all = pd.DataFrame()
            else:
                status_change = False
            # print ("Buy>0:%s" % len(top_now[top_now['buy'] > 0])),
            if len(top_now) > 10 or cct.get_work_time():
                time_Rt = time.time()
                if len(top_all) == 0 and len(lastpTDX_DF) == 0:
                    cct.get_terminal_Position(position=sys.argv[0])

                    time_Rt = time.time()
                    top_all, lastpTDX_DF = tdd.get_append_lastp_to_df(
                        top_now, lastpTDX_DF=None, dl=duration_date, end=end_date, ptype=ptype, filter=filter, power=False, lastp=False, newdays=newdays, resample=resample)

                elif len(top_all) == 0 and len(lastpTDX_DF) > 0:
                    time_Rt = time.time()
                    top_all = top_now
                    top_all = top_all.merge(lastpTDX_DF, left_index=True, right_index=True, how='left')
                    top_all = top_all[top_all['llow'] > 0]

                else:
                    if 'couts' in top_now.columns.values:
                        if not 'couts' in top_all.columns.values:
                            top_all['couts'] = 0
                            top_all['prev_p'] = 0

                    top_all = cct.combine_dataFrame(top_all, top_now, col=None)

                top_dif = top_all.copy()
                if 'trade' in top_dif.columns:
                    top_dif['buy'] = (map(lambda x, y: y if int(x) == 0 else x,
                                          top_dif['buy'].values, top_dif['trade'].values))
                if ct.checkfilter and cct.get_now_time_int() > 915 and cct.get_now_time_int() < ct.checkfilter_end_timeDu:
                    top_dif = top_dif[top_dif.low > top_dif.llow * ct.changeRatio]
                    # top_dif = top_dif[top_dif.buy >= top_dif.lhigh * ct.changeRatio]

#                if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 926:
#                    top_dif['percent']= (map(lambda x, y: round((x-y)/y*100,1) if int(y) > 0 else 0, top_dif.buy, top_dif.llastp))

                if cct.get_now_time_int() > 915:
                    top_dif = top_dif[top_dif.buy > 0]

                top_dif['dff'] = (
                    map(lambda x, y: round((x - y) / y * 100, 1), top_dif['buy'].values, top_dif['lastp'].values))
                # print top_dif.loc['600610',:]
                # top_dif = top_dif[top_dif.trade > 0]
                # if cct.get_now_time_int() > 932:

                # top_dif = top_dif[top_dif.low > 0]
                # log.debug("top_dif.low > 0:%s" % (len(top_dif)))
                # top_dif.loc['600610','volume':'lvol']
                top_dif['volume'] = (map(lambda x, y: round(x / y / radio_t, 1), top_dif.volume.values, top_dif.lvol.values))

                # if 'op' in top_dif.columns:
                #     top_dif=top_dif[top_dif.op >12]
                #     print "op:",len(top_dif),

                # top_dif = top_dif[top_dif.volume < 100]
                # print top_dif.loc['002504',:]

                # if filter == 'y':
                #     top_dif = top_dif[top_dif.date >= cct.day8_to_day10(duration_date)]
                # log.info('dif1-filter:%s' % len(top_dif))

                # print top_dif.loc['600533',:]
                # log.info(top_dif[:1])
                # top_dif = top_dif[top_dif.buy > top_dif.lhigh]
                # log.debug('dif2:%s' % len(top_dif))
                # top_dif['volume'] = top_dif['volume'].apply(lambda x: round(x / radio_t, 1))
                # log.debug("top_diff:vol")
                # top_dif = top_dif[top_dif.volume > 1]

                if len(top_dif) == 0:
                    print "No G,DataFrame is Empty!!!!!!"
                else:
                    log.debug('dif6 vol:%s' % (top_dif[:1].volume))
                    log.debug('dif6 vol>lvol:%s' % len(top_dif))

                    # top_dif = top_dif[top_dif.buy >= top_dif.open*0.99]
                    # log.debug('dif5 buy>open:%s'%len(top_dif))
                    # top_dif = top_dif[top_dif.trade >= top_dif.buy]
                    # df['volume']= df['volume'].apply(lambda x:x/100)

                    goldstock = len(top_dif[(top_dif.buy >= top_dif.lhigh * 0.99)
                                            & (top_dif.buy >= top_dif.llastp * 0.99)])
                    ## goldstock=len(top_dif[top_dif.buy >(top_dif.high-top_dif.low)/2])
                    if ptype == 'low':
                        top_dif = top_dif[top_dif.lvol > ct.LvolumeSize]
                        if cct.get_now_time_int() > 925 and cct.get_work_time():
                            top_dif = top_dif[(top_dif.volume > ct.VolumeMinR) & (top_dif.volume < ct.VolumeMaxR)]
                        # top_dif = top_dif[top_dif.lvol > 12000]
                        if 'couts' in top_dif.columns.values:
                            top_dif = top_dif.sort_values(by=['dff', 'percent', 'volume', 'couts', 'ratio'],
                                                          ascending=[0, 0, 0, 1, 1])
                        else:
                            top_dif = top_dif.sort_values(by=['dff', 'percent', 'ratio'], ascending=[0, 0, 1])
                    else:
                        # top_dif['dff'] = top_dif['dff'].apply(lambda x: x * 2 if x > 0 else x)
                        top_dif = top_dif[top_dif.lvol > ct.LvolumeSize]
                        top_dif['dff'] = top_dif['dff'].apply(lambda x: x * 2 if x < 0 else x)
                        if 'couts' in top_dif.columns.values:
                            top_dif = top_dif.sort_values(by=['dff', 'percent', 'volume', 'couts', 'ratio'],
                                                          ascending=[1, 0, 0, 1, 1])
                        else:
                            top_dif = top_dif.sort_values(by=['dff', 'percent', 'ratio'], ascending=[1, 0, 1])

                    # top_all=top_all.sort_values(by=['percent','dff','couts','ratio'],ascending=[0,0,1,1])
                    # print rl.format_for_print(top_dif[:10])
                    # top_dd = pd.concat([top_dif[:5],top_temp[:3],top_dif[-3:],top_temp[-3:]], axis=0)
                    if percent_status == 'y' and (
                            cct.get_now_time_int() > 935 or cct.get_now_time_int() < 900) and ptype == 'low':
                        top_dif = top_dif[top_dif.percent >= 0]
                        top_temp = top_dif[:ct.PowerCount].copy()
                        top_end = top_dif[-5:].copy()
                        top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl, talib=True, newdays=newdays)
                        top_end = pct.powerCompute_df(top_end, dl=ct.PowerCountdl, talib=True, newdays=newdays)

                    # elif percent_status == 'y' and cct.get_now_time_int() > 935 and ptype == 'high' :
                    elif ptype == 'low':
                        # top_dif = top_dif[top_dif.percent >= 0]
                        top_temp = top_dif[:ct.PowerCount].copy()
                        top_end = top_dif[-5:].copy()
                        top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl, talib=True, newdays=newdays)
                        top_end = pct.powerCompute_df(top_end, dl=ct.PowerCountdl, talib=True, newdays=newdays)
                    else:
                        # top_dif = top_dif[top_dif.percent >= 0]
                        top_end = top_dif[:5].copy()
                        top_temp = top_dif[-ct.PowerCount:].copy()
                        top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl, talib=True, newdays=newdays)
                        top_end = pct.powerCompute_df(top_end, dl=ct.PowerCountdl, talib=True, newdays=newdays)

                    cct.set_console(width, height,
                                    title=[du_date, 'dT:%s' % cct.get_time_to_date(time_s), 'G:%s' % goldstock,
                                           'zxg: %s' % (blkname)])
                    # print len(top_all),top_all.shape
                    top_all = tdd.get_powerdf_to_all(top_all, top_temp)
                    top_all = tdd.get_powerdf_to_all(top_all, top_end)
                    top_temp = stf.getBollFilter(df=top_temp, boll=ct.bollFilter,
                                                 duration=ct.PowerCountdl, filter=True, percent=True, resample=resample)
                    print("N:%s K:%s %s G:%s" % (
                        now_count, len(top_all[top_all['buy'] > 0]),
                        len(top_now[top_now['volume'] <= 0]), goldstock)),
                    print "Rt:%0.1f dT:%s N:%s T:%s %s%%" % (float(time.time() - time_Rt), cct.get_time_to_date(time_s), cct.get_now_time(), len(top_temp), round(len(top_temp) / float(ct.PowerCount) * 100, 1))
                    # top_end = stf.getBollFilter(df=top_end, boll=ct.bollFilter,duration=ct.PowerCountdl,filter=False)
                    if 'op' in top_temp.columns:
                        # if ptype == 'low':
                        #     top_temp = top_temp.sort_values(by=ct.Duration_sort_op,
                        #                 ascending=ct.Duration_sort_op_key)
                        # else:
                        #     top_temp = top_temp.sort_values(by=ct.Duration_sort_high_op,
                        #                 ascending=ct.Duration_sort_high_op_key)
                        # top_temp=top_temp[top_temp.op >12]
                        # top_temp = top_temp.sort_values(by=['ra', 'op'],ascending=[0, 0])[:10]

                        # top_temp = top_temp.sort_values(by=['dff', 'op', 'ra', 'percent', 'ratio'],
                        #                                 ascending=[0, 0, 0, 0, 1])[:10]

                        # top_temp = top_temp.sort_values(by=['op', 'ra', 'dff', 'percent', 'ratio'],
                        #                                 ascending=[0, 0, 0, 0, 1])[:10]
                        # top_temp = top_temp.sort_values(by=['op','ldate','ra','dff', 'percent', 'ratio'], ascending=[0,0,0,0, 0, 1])[:10]

                        # if duration_date > ct.duration_date_sort:

                        # if (cct.get_now_time_int() > ct.checkfilter_end_timeDu and
                        # int(duration_date) > int(ct.duration_date_sort)) or int(duration_date) <
                        # 6:
                        if cct.get_now_time_int() > ct.checkfilter_end_timeDu and (int(duration_date) > int(ct.duration_date_sort) or int(duration_date) < ct.duration_diff):
                            top_temp = top_temp.sort_values(by=(market_sort_value),
                                                            ascending=market_sort_value_key)
                        else:
                            top_temp = top_temp.sort_values(by=(market_sort_value),
                                                            ascending=market_sort_value_key)

                    if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 935:
                        # top_temp = top_temp[top_temp['buy'] > top_temp['ma10d']]
                        # top_temp = top_temp[top_temp['ma5d'] > top_temp['ma10d']][:10]
                        # top_temp = top_temp[ (top_temp['ma5d'] > top_temp['ma10d']) & (top_temp['buy'] > top_temp['ma10d']) ][:10]
                        top_dd = pd.concat([top_temp[:10], top_end], axis=0)
                        # top_dd = top_dd.drop_duplicates()
                        ct_Duration_format_Values = ct.get_Duration_format_Values(ct.Duration_format_buy, market_sort_value[:])
                        top_dd = top_dd.loc[:, ct_Duration_format_Values]
                    else:
                        # top_temp = top_temp[top_temp['trade'] > top_temp['ma10d']]
                        # top_temp = top_temp[top_temp['ma5d'] > top_temp['ma10d']][:10]
                        # top_temp = top_temp[ (top_temp['ma5d'] > top_temp['ma10d']) & (top_temp['trade'] > top_temp['ma10d']) ][:10]

                        top_dd = pd.concat([top_temp[:10], top_end], axis=0)
                        ct_Duration_format_Values = ct.get_Duration_format_Values(ct.Duration_format_trade, market_sort_value[:])
                        top_dd = top_dd.loc[:, ct_Duration_format_Values]

                    print rl.format_for_print(top_dd)
                # if cct.get_now_time_int() < 930 or cct.get_now_time_int() > 1505 or (cct.get_now_time_int() > 1125 and cct.get_now_time_int() < 1505):
                # print rl.format_for_print(top_dif[-10:])
                # print top_all.loc['000025',:]
                # print "staus",status

                if status:
                    for code in top_dd[:10].index:
                        code = re.findall('(\d+)', code)
                        if len(code) > 0:
                            code = code[0]
                            kind = sl.get_multiday_ave_compare_silent(code)
                            # print top_all[top_all.low.values==0]

                            # else:
                            #     print "\t No RealTime Data"
            else:
                print "\tNo Data"
            int_time = cct.get_now_time_int()
            if cct.get_work_time():
                if int_time < ct.open_time:
                    cct.sleep(ct.sleep_time)
                elif int_time < 930:
                    cct.sleep((930 - int_time) * 55)
                    # top_all = pd.DataFrame()
                    time_s = time.time()
                else:
                    cct.sleep(ct.duration_sleep_time)
            elif cct.get_work_duration():
                while 1:
                    cct.sleep(ct.duration_sleep_time)
                    if cct.get_work_duration():
                        print ".",
                        cct.sleep(ct.duration_sleep_time)
                    else:
                        # top_all = pd.DataFrame()
                        cct.sleeprandom(60)
                        time_s = time.time()
                        print "."
                        break
            else:
                raise KeyboardInterrupt("StopTime")
        except (KeyboardInterrupt) as e:
            # st = cct.cct_raw_input("status:[go(g),clear(c),[d 20150101 [l|h]|[y|n|pn|py],quit(q),W(a),sh]:")
            st = cct.cct_raw_input(ct.RawMenuArgmain() % (market_sort_value))
            if len(st) == 0:
                status = False
            elif len(st.split()[0]) == 1 and st.split()[0].isdigit():
                st_l = st.split()
                st_k = st_l[0]
                if st_k in ct.Market_sort_idx.keys() and len(top_all) > 0:
                    market_sort_value, market_sort_value_key = ct.get_market_sort_value_key(st, top_all=top_all)
                else:
                    log.error("market_sort key error:%s" % (st))
                    cct.sleeprandom(5)
            elif st.lower() == 'r':
                dir_mo = eval(cct.eval_rule)
                evalcmd(dir_mo)

            elif st.lower() == 'g' or st.lower() == 'go':
                status = True
                for code in top_dd[:10].index:
                    code = re.findall('(\d+)', code)
                    if len(code) > 0:
                        code = code[0]
                        kind = sl.get_multiday_ave_compare_silent(code)
            elif st.lower() == 'clear' or st.lower() == 'c':
                top_all = pd.DataFrame()
                time_s = time.time()
                status = False
            elif st.startswith('d') or st.startswith('dt'):
                args = parserDuraton.parse_args(st.split()[1:])
                if len(str(args.start)) > 0:
                    if args.end:
                        end_date = args.end
                    duration_date = args.start.strip()
                    if len(str(duration_date)) < 4:
                        du_date = tdd.get_duration_Index_date('999999', dl=int(duration_date))
                        ct.PowerCountdl = int(duration_date)
                    set_duration_console(du_date)
                    top_all = pd.DataFrame()
                    time_s = time.time()
                    status = False
                    lastpTDX_DF = pd.DataFrame()

            elif st.startswith('w') or st.startswith('a'):
                args = cct.writeArgmain().parse_args(st.split())
                codew = stf.WriteCountFilter(top_temp, duration=duration_date, writecount=args.dl, end=args.end)
                if args.code == 'a':
                    cct.write_to_blocknew(block_path, codew)
                    # sl.write_to_blocknew(all_diffpath, codew)
                else:
                    cct.write_to_blocknew(block_path, codew, False)
                    # sl.write_to_blocknew(all_diffpath, codew, False)
                print "wri ok:%s" % block_path
                cct.sleeprandom(ct.duration_sleep_time / 2)
            elif st.startswith('sh'):
                while 1:
                    input = raw_input("code:")
                    if len(input) >= 6:
                        args = parser.parse_args(input.split())
                        if len(str(args.code)) == 6:
                            # print args.code
                            if args.code in top_temp.index.values:
                                lhg.get_linear_model_histogram(args.code, start=top_temp.loc[args.code, 'date'],
                                                               end=args.end, vtype=args.vtype,
                                                               filter=args.filter)
                    elif input.startswith('q'):
                        break
                    else:
                        pass
            elif st.startswith('q') or st.startswith('e'):
                print "exit:%s" % (st)
            else:
                print "input error:%s" % (st)
        except (IOError, EOFError, Exception) as e:
            print "Error", e
            import traceback
            traceback.print_exc()
            cct.sleeprandom(ct.duration_sleep_time / 2)

'''
{symbol:"sz000001",code:"000001",name:"平安银行",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"12.36",sell:"12.36",settlement:"12.34",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:7.133,pb:1.124,mktcap:17656906.355526,nmc:14566203.350486,turnoverratio:0},
{symbol:"sz000002",code:"000002",name:"万  科Ａ",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"0.00",sell:"0.00",settlement:"24.43",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:17.084,pb:3.035,mktcap:26996432.575,nmc:23746405.928119,turnoverratio:0},

python -m cProfile -s cumulative timing_functions.py
http://www.jb51.net/article/63244.htm

'''
