# -*- coding:utf-8 -*-
# !/usr/bin/env python

import gc
import random
import re
import sys
import time
import urllib2

import pandas as pd
# from bs4 import BeautifulSoup
from pandas import DataFrame
# import sys
# print sys.path

import JohhnsonUtil.johnson_cons as ct
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd
from JSONData import powerCompute as pct
from JSONData import stockFilter as stf
from JohhnsonUtil import LoggerFactory
from JohhnsonUtil import commonTips as cct
import singleAnalyseUtil as sl
from JSONData import LineHistogram as lhg
# from logbook import Logger,StreamHandler,SyslogHandler
# from logbook import StderrHandler


if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))
    # StreamHandler(sys.stdout).push_application()
    log = LoggerFactory.getLogger('SinaMarket')
    # log=LoggerFactory.JohnsonLoger('SinaMarket').setLevel(LoggerFactory.DEBUG)
    # log.setLevel(LoggerFactory.DEBUG)


    if cct.isMac():
        width, height = 158, 16
        cct.set_console(width, height)
    else:
        width, height = 158, 18
        cct.set_console(width, height)
    status = False
    vol = ct.json_countVol
    type = ct.json_countType
    # cut_num=10000
    success = 0
    top_all = pd.DataFrame()
    time_s = time.time()
    # delay_time = 7200
    delay_time = cct.get_delay_time()
    First = True
    # base_path = tdd.get_tdx_dir()
    # block_path = tdd.get_tdx_dir_blocknew() + '063.blk'
    blkname = '068.blk'
    block_path = tdd.get_tdx_dir_blocknew() + blkname
    lastpTDX_DF = pd.DataFrame()
    # all_diffpath = tdd.get_tdx_dir_blocknew() + '062.blk'
    while 1:
        try:
            # df = rl.get_sina_Market_json('all')
            # top_now = rl.get_market_price_sina_dd_realTime(df, vol, type)
            top_now = tdd.getSinaAlldf(market='all', vol=ct.json_countVol, type=ct.json_countType)            
            # print top_now.loc['601900',:]
            df_count = len(top_now)
            now_count = len(top_now)
            radio_t = cct.get_work_time_ratio()
            time_Rt = time.time()
            time_d = time.time()
            if time_d - time_s > delay_time:
                status_change = True
                log.info("chane clear top")
                time_s = time.time()
                top_all = pd.DataFrame()

            else:
                status_change = False
            # print ("Buy>0:%s"%len(top_now[top_now['buy'] > 0])),
            log.info("top_now['buy']:%s" % (top_now[:2]['buy']))
            log.info("top_now.buy[:30]>0:%s" % len(top_now[:30][top_now[:30]['buy'] > 0]))
            if len(top_now) > 10 or cct.get_work_time():
                # if len(top_now) > 10 or len(top_now[:10][top_now[:10]['buy'] > 0]) > 3:
                # if len(top_now) > 10 and not top_now[:1].buy.values == 0:
                #     top_now=top_now[top_now['percent']>=0]
                if 'trade' in top_now.columns:
                    top_now['buy'] = (
                        map(lambda x, y: y if int(x) == 0 else x, top_now['buy'].values, top_now['trade'].values))
                time_Rt = time.time()
                if len(top_all) == 0 and len(lastpTDX_DF) == 0:
                    time_Rt = time.time()
                    top_all,lastpTDX_DF = tdd.get_append_lastp_to_df(top_now)
                elif len(top_all) == 0 and len(lastpTDX_DF) > 0:
                    time_Rt = time.time()
                    top_all = tdd.get_append_lastp_to_df(top_now,lastpTDX_DF)
                else:
                    if 'counts' in top_now.columns.values:
                        if not 'counts' in top_all.columns.values:
                            top_all['counts'] = 0
                            top_all['prev_p'] = 0
                    
                    for symbol in top_now.index:
                        # code = rl._symbol_to_code(symbol)
                        if symbol in top_all.index and top_now.loc[symbol, 'buy'] <> 0:
                            # top_now.loc[symbol, 'diff'] = round(((float(top_now.loc[symbol, 'buy']) - float(top_all.loc[symbol, 'lastp'])) / float(top_all.loc[symbol, 'lastp']) * 100), 1)
                            if 'counts' in top_now.columns.values:
                                    top_all.loc[symbol, 'trade':'prev_p'] = top_now.loc[symbol, 'trade':'prev_p']
                            else:
                                top_all.loc[symbol, 'trade':'low'] = top_now.loc[symbol, 'trade':'low']

                # top_all=top_all.sort_values(by=['diff','percent','counts'],ascending=[0,0,1])
                # top_all=top_all.sort_values(by=['diff','ratio','percent','counts'],ascending=[0,1,0,1])

                # top_all = top_all[top_all.open>=top_all.low*0.99]
                # top_all = top_all[top_all.buy >= top_all.open*0.99]
                # top_all = top_all[top_all.trade >= top_all.low*0.99]
                # top_all = top_all[top_all.trade >= top_all.high*0.99]
                # top_all = top_all[top_all.buy >= top_all.llastp]
                # top_all = top_all[top_all.percent >= 0]
                
                # if cct.get_now_time_int() < 1500:
                top_all['diff'] = (
                    map(lambda x, y: round((x - y) / y * 100, 1), top_all['buy'].values, top_all['lastp'].values))
                top_dif = top_all                
                log.info('dif1:%s' % len(top_dif))
                if cct.get_now_time_int() > 915 and cct.get_now_time_int() < ct.checkfilter_end_time:
                    top_dif=top_dif[top_dif.lvol > ct.LvolumeSize]
                    log.info(top_dif[:1])
                    top_dif = top_dif[top_dif.buy > top_dif.llastp * ct.changeRatio]
                    log.debug('dif2:%s' % len(top_dif))
                # log.debug('dif2:%s' % top_dif[:1])
                if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 925:
                    top_dif['percent']= (map(lambda x, y: round((x-y)/y*100,1) if int(y) > 0 else 0, top_dif.buy, top_dif.llastp))

                # if top_dif[:1].llow.values <> 0:
                if len(top_dif[:5][top_dif[:5]['low'] > 0]) > 3:
                    log.debug('diff2-0-low>0')
                    top_dif = top_dif[top_dif.low >= top_dif.llow]
                    log.debug('diff2-1:%s' % len(top_dif))
                    if cct.get_now_time_int() > 915:
                        top_dif = top_dif[top_dif.buy > top_dif.llastp * ct.changeRatio]
                        top_dif = top_dif[top_dif.buy > top_dif.lhigh * ct.changeRatio]
                        # top_dif = top_dif[top_dif.low >= top_dif.llastp]
                        # top_dif = top_dif[top_dif.open >= top_dif.llastp]
                    # top_dif = top_dif[top_dif.low >= top_dif.lhigh]

                    # if cct.get_work_time() and cct.get_now_time_int() > 930:
                    # top_dif = top_dif[top_dif.percent >= 0]
                    log.debug("dif5-percent>0:%s" % len(top_dif))

                    # if len(top_dif[:5][top_dif[:5]['volume'] > 0]) > 3:
                    log.debug("Second:vol/vol/:%s" % radio_t)
                    # top_dif['volume'] = top_dif['volume'].apply(lambda x: round(x / radio_t, 1))
                    top_dif['volume'] = (
                        map(lambda x, y: round(x / y / radio_t, 1), top_dif['volume'].values, top_dif['lvol'].values))
                    # top_dif = top_dif[top_dif.volume > 0.5]


                    # if cct.get_now_time_int() > 1030 and cct.get_now_time_int() < 1400:
                        # top_dif = top_dif[(top_dif.volume > ct.VolumeMinR) & (top_dif.volume < ct.VolumeMaxR)]
                
                if len(top_dif) == 0:
                    print "No G,DataFrame is Empty!!!!!!"

                log.debug('dif6 vol:%s' % (top_dif[:1].volume.values))

                log.debug('dif6 vol>lvol:%s' % len(top_dif))

                # top_dif = top_dif[top_dif.buy >= top_dif.open*0.99]
                # log.debug('dif5 buy>open:%s'%len(top_dif))
                # top_dif = top_dif[top_dif.trade >= top_dif.buy]

                # df['volume']= df['volume'].apply(lambda x:x/100)


                if 'counts' in top_dif.columns.values:
                    top_dif = top_dif.sort_values(by=ct.MonitorMarket_sort_count,
                                                  ascending=[0, 0, 0, 1, 1])
                else:
                    # print "Good Morning!!!"
                    top_dif = top_dif.sort_values(by=['diff', 'percent', 'ratio'], ascending=[0, 0, 1])

                # top_all=top_all.sort_values(by=['percent','diff','counts','ratio'],ascending=[0,0,1,1])

                top_temp = top_dif[:ct.PowerCount].copy()
                top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl)
                goldstock = len(top_dif[(top_dif.buy >= top_dif.lhigh * 0.99) & (top_dif.buy >= top_dif.llastp * 0.99)])

                print ("A:%s N:%s K:%s %s G:%s" % (
                    df_count, now_count, len(top_all[top_all['buy'] > 0]),
                    len(top_now[top_now['volume'] <= 0]), goldstock)),
                print "Rt:%0.1f dT:%s N:%s" % (float(time.time() - time_Rt), cct.get_time_to_date(time_s),cct.get_now_time())
                cct.set_console(width, height,
                    title=['dT:%s' % cct.get_time_to_date(time_s), 'G:%s' % len(top_dif), 'zxg: %s' % (blkname)])
              
                top_temp = stf.getBollFilter(df=top_temp, boll=ct.bollFilter)
                if 'op' in top_temp.columns:

                    # top_temp = top_temp.sort_values(by=['ra', 'op','percent'],ascending=[0, 0,0])

                    # top_temp = top_temp.sort_values(by=ct.MonitorMarket_sort_op,
                                                    # ascending=ct.MonitorMarket_sort_op_key)
                    top_temp = top_temp.sort_values(by=ct.Duration_percent_op,
                                        ascending=ct.Duration_percent_op_key)                                
                    # top_temp = top_temp.sort_values(by=['op','ra','diff', 'percent', 'ratio'], ascending=[0,0,0, 0, 1])
                if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 935:
                    top_temp = top_temp.loc[:,ct.MonitorMarket_format_buy]
                else:
                    top_temp = top_temp.loc[:,ct.MonitorMarket_format_buy]
                print rl.format_for_print(top_temp[:10])                
                
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
                if int_time < 925:
                    cct.sleep(ct.sleep_time)
                elif int_time < 930:
                    cct.sleep((930 - int_time) * 60)
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
                raise KeyboardInterrupt("StopTime")
        except (KeyboardInterrupt) as e:
            # print "key"
            # print "KeyboardInterrupt:", e
            # cct.sleep(1)
            # if success > 3:
            #     raw_input("Except")
            #     sys.exit(0)
            st = raw_input("status:[go(g),clear(c),quit(q,e),W(w),Wa(a)]:")
            if len(st) == 0:
                status = False
            elif st.lower() == 'r':
                end = True
                while end:
                    cmd=(raw_input('DEBUG[top_dif,top_dd,e|q]:'))
                    if cmd =='e' or cmd=='q' or len(cmd)==0:
                        break
                    else:
                        print eval(cmd)                
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
            elif st.lower() == 'w' or st.lower() == 'a':
                codew = (top_temp.index).tolist()
                if st.lower() == 'a':
                    cct.write_to_blocknew(block_path, codew[:ct.writeCount])
                    # cct.write_to_blocknew(all_diffpath, codew)
                else:
                    cct.write_to_blocknew(block_path, codew[:ct.writeCount], False)
                    # cct.write_to_blocknew(all_diffpath, codew, False)
                print "wri ok:%s" % block_path
                cct.sleeprandom(120)

            elif st.startswith('sh'):
                code = st.split()[1]
                # lhg.get_linear_model_histogram(code, args.ptype, args.dtype, start, end, args.vtype, args.filter)
                lhg.get_linear_model_histogram(code, start=top_temp.loc[code, 'ldate'], vtype='close', filter='y')
                # raise KeyboardInterrupt()
                while 1:
                    st = raw_input("code:")
                    if len(str(st)) == 6:
                        code = st
                        lhg.get_linear_model_histogram(code, start=top_temp.loc[code, 'ldate'], vtype='close',
                                                             filter='y')
                    elif st.lower() == 'q':
                        break
                    else:
                        pass
            else:
                sys.exit(0)
        except (IOError, EOFError, Exception) as e:
            print "Error", e

            #traceback.print_exc()
            cct.sleeprandom(120)
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
