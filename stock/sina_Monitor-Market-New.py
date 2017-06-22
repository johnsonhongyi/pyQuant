# -*- coding:utf-8 -*-
# !/usr/bin/env python

import gc
import random
import re
import sys
import time

import pandas as pd
# from bs4 import BeautifulSoup

import JohhnsonUtil.johnson_cons as ct
import singleAnalyseUtil as sl
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd
from JSONData import powerCompute as pct
from JSONData import stockFilter as stf
from JohhnsonUtil import LoggerFactory as LoggerFactory
from JohhnsonUtil import commonTips as cct


# from logbook import StderrHandler
# from logbook import Logger,StreamHandler,SyslogHandler

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
        if cmd == 'e' or cmd == 'q':
            break
        elif len(cmd) == 0:
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
                # evalcmd(dir_mo)
                # break

if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))
    # StreamHandler(sys.stdout).push_application()
    # log = LoggerFactory.getLogger('SinaMarketNew')
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

    # log.setLevel(LoggerFactory.DEBUG)

    # handler=StderrHandler(format_string='{record.channel}: {record.message) [{record.extra[cwd]}]')
    # log.level=log.debug
    # error_handler = SyslogHandler('Sina-M-Log', level='ERROR')

    # width, height = 132, 18
    if cct.isMac():
        width, height = 166, 16
        cct.set_console(width, height)
    else:
        width, height = 166, 18
        cct.set_console(width, height)
    status = False
    vol = ct.json_countVol
    type = ct.json_countType
    # cut_num=10000
    success = 0
    top_all = pd.DataFrame()
    time_s = time.time()
    # delay_time = 3600
    delay_time = cct.get_delay_time()
    First = True
    # base_path = tdd.get_tdx_dir()
    # block_path = tdd.get_tdx_dir_blocknew() + '062.blk'
    blkname = '069.blk'
    block_path = tdd.get_tdx_dir_blocknew() + blkname
    lastpTDX_DF = pd.DataFrame()
    # initTdx = True
    # all_diffpath = tdd.get_tdx_dir_blocknew() + '062.blk'
    status_change = False
    market_sort_value = ct.Market_sort_idx['2']
    market_sort_value_key = eval(market_sort_value + '_key')
    while 1:
        try:
            # df = sina_data.Sina().all
            time_Rt = time.time()
            top_now = tdd.getSinaAlldf(market='cyb', vol=ct.json_countVol, vtype=ct.json_countType)
            # print top_now.loc['300208','name']
            # top_now.to_hdf("testhdf5", 'marketDD', format='table', complevel=9)
            df_count = len(top_now)
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
                # if len(top_now) > 10 and len(top_now[:20][top_now[:20]['buy'] > 0]) > 3:
                # if len(top_now) > 10 and not top_now[:1].buy.values == 0:
                #     top_now=top_now[top_now['percent']>=0]
                if 'trade' in top_now.columns:
                    top_now['buy'] = (
                        map(lambda x, y: y if int(x) == 0 else x, top_now['buy'].values, top_now['trade'].values))

                if len(top_all) == 0 and len(lastpTDX_DF) == 0:
                    cct.get_terminal_Position(position=sys.argv[0])

                    top_all, lastpTDX_DF = tdd.get_append_lastp_to_df(top_now)
                elif len(top_all) == 0 and len(lastpTDX_DF) > 0:
                    top_all = tdd.get_append_lastp_to_df(top_now, lastpTDX_DF)

                    # if len(top_all[:5][top_all[:5]['volume'] > 0]) > 3:
                    #     # top_all['volume'] = top_all['volume'].apply(lambda x: round(float(x) / radio_t, 1))
                    #     # C4 = np.asarray(map(lambda x,y: x**y, pdA.values, pdB.values))
                    #     # top_all['volume'] = round(
                    #     # top_now.loc[symbol, 'volume'] / top_all.loc[symbol, 'lvol'], 1)
                    #     top_all['volume'] = (
                    #         map(lambda x, y: round(x / y / radio_t, 1), top_all['volume'].values,
                    #             top_all['lvol'].values))
                    #     # top_all['volume']=np.asarray(map(lambda x,y: round(x/y,1), top_all['volume'].values, top_all['lvol'].values))
                    #     # print top_all[:1]
                    #     log.debug("First:vol/vol/:%s" % radio_t)

                    # import sys
                    # sys.exit(0)
                else:
                    if 'couts' in top_now.columns.values:
                        if not 'couts' in top_all.columns.values:
                            top_all['couts'] = 0
                            top_all['prev_p'] = 0
                    # for symbol in top_now.index:
                    #     # code = rl._symbol_to_code(symbol)
                    #     if symbol in top_all.index and top_now.loc[symbol, 'buy'] <> 0:
                    #         # top_now.loc[symbol, 'dff'] = round(((float(top_now.loc[symbol, 'buy']) - float(top_all.loc[symbol, 'lastp'])) / float(top_all.loc[symbol, 'lastp']) * 100), 1)
                    #         if 'couts' in top_now.columns.values:
                    #                 top_all.loc[symbol, ct.columns_now] = top_now.loc[symbol, ct.columns_now]
                    #         else:
                    #             top_all.loc[symbol, ct.columns_now] = top_now.loc[symbol, ct.columns_now]
                    top_all = cct.combine_dataFrame(top_all, top_now, col=None)

                # top_all=top_all.sort_values(by=['dff','percent','couts'],ascending=[0,0,1])
                # top_all=top_all.sort_values(by=['dff','ratio','percent','couts'],ascending=[0,1,0,1])

                # top_all = top_all[top_all.open>=top_all.low*0.99]
                # top_all = top_all[top_all.buy >= top_all.open*0.99]
                # top_all = top_all[top_all.trade >= top_all.low*0.99]
                # top_all = top_all[top_all.trade >= top_all.high*0.99]
                # top_all = top_all[top_all.buy >= top_all.llastp]
                # top_all = top_all[top_all.percent >= 0]

                # if cct.get_now_time_int() <1500:

                top_dif = top_all.copy()
                top_dif['dff'] = (map(lambda x, y: round((x - y) / y * 100, 1),
                                      top_dif['buy'].values, top_dif['lastp'].values))

                log.info('dif1:%s' % len(top_dif))
                if not (cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 925):
                    top_dif = top_dif[top_dif.lvol > ct.LvolumeSize]
                if cct.get_now_time_int() > 915 and cct.get_now_time_int() < ct.checkfilter_end_time:
                    top_dif = top_dif[top_dif.low > top_dif.llow * ct.changeRatio]
                    # top_dif = top_dif[top_dif.buy >= top_dif.lhigh * ct.changeRatio]
                log.debug('dif2:%s' % len(top_dif))

                # if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 926:
                # top_dif['percent']= (map(lambda x, y: round((x-y)/y*100,1) if int(y) > 0 else 0, top_dif.buy, top_dif.llastp))

                # if top_dif[:1].llow.values <> 0:
                if len(top_dif[:5][top_dif[:5]['buy'] > 0]) > 3:
                    log.debug('diff2-0-low>0')
                    top_dif = top_dif[top_dif.low >= top_dif.llow * ct.changeRatio]
                    log.debug('diff2-1:%s' % len(top_dif))

                    # top_dif = top_dif[top_dif.low >= top_dif.lhigh* ct.changeRatio]

                    log.debug("dif5-0-low>lhigh>0:%s" % len(top_dif))

                    # top_dif = top_dif[top_dif.percent >= 0]
                    # log.debug("dif5-percent>0:%s" % len(top_dif))

                    # top_dif = top_dif[top_dif.percent >= 0]
                    # if len(top_dif[:5][top_dif[:5]['volume'] > 0]) > 3:
                    log.debug("Second:vol/vol/:%s" % radio_t)
                    # top_dif['volume'] = top_dif['volume'].apply(lambda x: round(x / radio_t, 1))
                    log.debug("top_diff:vol")
                    top_dif['volume'] = (
                        map(lambda x, y: round(x / y / radio_t, 1), top_dif['volume'].values, top_dif['lvol'].values))
                    # top_dif = top_dif[top_dif.volume > 1]
                    if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 1030:
                        top_dif = top_dif[(top_dif.volume > ct.VolumeMinR) & (top_dif.volume < ct.VolumeMaxR)]

                if len(top_dif) == 0:
                    print "No G,DataFrame is Empty!!!!!!"
                    # top_dif = top_all

                    log.debug('dif6 vol:%s' % (top_dif[:1].volume))

                    log.debug('dif6 vol>lvol:%s' % len(top_dif))

                    # top_dif = top_dif[top_dif.buy >= top_dif.open*0.99]
                    # log.debug('dif5 buy>open:%s'%len(top_dif))
                    # top_dif = top_dif[top_dif.trade >= top_dif.buy]

                    # df['volume']= df['volume'].apply(lambda x:x/100)
                else:

                    if 'couts' in top_dif.columns.values:
                        top_dif = top_dif.sort_values(by=ct.Monitor_sort_count, ascending=[0, 0, 0, 1, 1])
                    else:
                        # print "Good Morning!!!"
                        top_dif = top_dif.sort_values(by=['dff', 'percent', 'ratio'], ascending=[0, 0, 1])

                    # top_all=top_all.sort_values(by=['percent','dff','couts','ratio'],ascending=[0,0,1,1])
                    # print rl.format_for_print(top_dif[:10])
                    top_temp = top_dif[:ct.PowerCount].copy()
                    top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl)
                    goldstock = len(top_dif[(top_dif.buy >= top_dif.lhigh * 0.99)
                                            & (top_dif.buy >= top_dif.llastp * 0.99)])

                    cct.set_console(width, height,
                                    title=['dT:%s' % cct.get_time_to_date(time_s), 'G:%s' % len(top_dif), 'zxg: %s' % (blkname)])

                    top_all = tdd.get_powerdf_to_all(top_all, top_temp)
                    top_temp = stf.getBollFilter(df=top_temp, boll=ct.bollFilter, duration=ct.PowerCountdl)
                    print("A:%s N:%s K:%s %s G:%s" % (
                        df_count, now_count, len(top_all[top_all['buy'] > 0]),
                        len(top_now[top_now['volume'] <= 0]), goldstock)),
                    # print "Rt:%0.3f" % (float(time.time() - time_Rt))
                    print "Rt:%0.1f dT:%s N:%s T:%s %s%%" % (float(time.time() - time_Rt), cct.get_time_to_date(time_s), cct.get_now_time(), len(top_temp), round(len(top_temp) / now_count * 100, 1))
                    if 'op' in top_temp.columns:

                        top_temp = top_temp.sort_values(by=eval(market_sort_value),
                                                        ascending=market_sort_value_key)
                    #     top_temp = top_temp.loc[:,ct.MonitorMarket_format_buy]
                    print rl.format_for_print(top_temp.loc[:, ct.MonitorMarket_format_buy][:10])
                    # print rl.format_for_print(top_dif[:10])
                    # print top_all.loc['000025',:]
                    # print "staus",status

                    if status:
                        for code in top_dif[:10].index:
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
                    top_all = pd.DataFrame()
                    time_s = time.time()
                else:
                    cct.sleep(60)
            elif cct.get_work_duration():
                while 1:
                    cct.sleep(60)
                    if cct.get_work_duration():
                        print ".",
                        cct.sleep(60)
                    else:
                        cct.sleeprandom(60)
                        top_all = pd.DataFrame()
                        time_s = time.time()
                        print "."
                        break
            else:
                # break
                # cct.sleep(5)
                raise KeyboardInterrupt("StopTime")
        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # cct.sleep(1)
            # if success > 3:
            #     raw_input("Except")
            #     sys.exit(0)
            st = cct.cct_raw_input(ct.RawMenuArgmain() % (market_sort_value))

            if len(st) == 0:
                status = False
            elif len(st.split()[0]) == 1 and st.split()[0].isdigit():
                st_l = st.split()
                st = st_l[0]
                if st in ct.Market_sort_idx.keys():
                    market_sort_value = ct.Market_sort_idx[st]
                    market_sort_value_key = eval(market_sort_value + '_key')
                    if len(st_l) > 1 and st_l[1] == 'f':
                        market_sort_value_key = cct.negate_boolean_list(market_sort_value_key)
                else:
                    log.error("market_sort key error:%s" % (st))
                    cct.sleeprandom(5)

            elif st.lower() == 'r':
                dir_mo = eval(cct.eval_rule)
                evalcmd(dir_mo)
            elif st.lower() == 'g' or st.lower() == 'go':
                status = True
                for code in top_dif[:10].index:
                    code = re.findall('(\d+)', code)
                    if len(code) > 0:
                        code = code[0]
                        kind = sl.get_multiday_ave_compare_silent(code)
            elif st.lower() == 'clear' or st.lower() == 'c':
                top_all = pd.DataFrame()
                status = False
            elif st.startswith('w') or st.startswith('a'):
                args = cct.writeArgmain().parse_args(st.split())
                codew = stf.WriteCountFilter(top_temp, writecount=args.dl)
                if args.code == 'a':
                    cct.write_to_blocknew(block_path, codew)
                    # sl.write_to_blocknew(all_diffpath, codew)
                else:
                    cct.write_to_blocknew(block_path, codew, False)
                    # sl.write_to_blocknew(all_diffpath, codew, False)
                print "wri ok:%s" % block_path
                cct.sleeprandom(ct.duration_sleep_time / 2)

                # cct.sleep(2)
            elif st.startswith('q') or st.startswith('e'):
                print "exit:%s" % (st)
            else:
                print "input error:%s" % (st)
        except (IOError, EOFError, Exception) as e:
            print "Error", e
            import traceback
            traceback.print_exc()
            cct.sleeprandom(ct.duration_sleep_time / 2)
            # raw_input("Except")

            # sl.get_code_search_loop()
            # print data.describe()
            # while 1:
            #     intput=raw_input("code")
            #     print
            # pd = DataFrame(data)
            # print pd
            # parsehtml("""
            # <a href="www.google.com"> google.com</a>
            # <A Href="www.pythonclub.org"> PythonClub </a>
            # <A HREF = "www.sina.com.cn"> Sina </a>
            # """)
'''
{symbol:"sz000001",code:"000001",name:"平安银行",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"12.36",sell:"12.36",settlement:"12.34",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:7.133,pb:1.124,mktcap:17656906.355526,nmc:14566203.350486,turnoverratio:0},
{symbol:"sz000002",code:"000002",name:"万  科Ａ",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"0.00",sell:"0.00",settlement:"24.43",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:17.084,pb:3.035,mktcap:26996432.575,nmc:23746405.928119,turnoverratio:0},

python -m cProfile -s cumulative timing_functions.py
http://www.jb51.net/article/63244.htm

'''
