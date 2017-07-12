# -*- coding:utf-8 -*-
# !/usr/bin/env python


# import sys
#
# reload(sys)
#
# sys.setdefaultencoding('utf-8')
url_s = "http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=0&type=1"
url_b = "http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=100000&type=0"
status_dict = {u"中性盘": "normal", u"买盘": "up", u"卖盘": "down"}
url_real_sina = "http://finance.sina.com.cn/realstock/"
url_real_sina_top = "http://vip.stock.finance.sina.com.cn/mkt/#stock_sh_up"
url_real_east = "http://quote.eastmoney.com/sz000004.html"
import gc
import random
import re
import sys
import time

import pandas as pd
# from bs4 import BeautifulSoup
# from pandas import DataFrame

import JohhnsonUtil.commonTips as cct
import JohhnsonUtil.johnson_cons as ct
import singleAnalyseUtil as sl
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd
from JSONData import powerCompute as pct
from JSONData import stockFilter as stf
from JohhnsonUtil import LoggerFactory as LoggerFactory
# cct.set_ctrl_handler()


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
    log = LoggerFactory.getLogger('SinaMarket')
    # log.setLevel(LoggerFactory.DEBUG)
    if cct.isMac():
        width, height = 166, 16
        cct.set_console(width, height)
    else:
        width, height = 166, 18
        cct.set_console(width, height)

    # cct.set_console(width, height)
    # if cct.isMac():
    #     cct.set_console(108, 16)
    # else:
    #     cct.set_console(100, 16)
    status = False
    vol = ct.json_countVol
    type = ct.json_countType
    cut_num = 1000000
    success = 0
    top_all = pd.DataFrame()
    time_s = time.time()
    # delay_time = 7200
    delay_time = cct.get_delay_time()
    # base_path = tdd.get_tdx_dir()
    # block_path = tdd.get_tdx_dir_blocknew() + '064.blk'
    blkname = '064.blk'
    block_path = tdd.get_tdx_dir_blocknew() + blkname
    lastpTDX_DF = pd.DataFrame()
    market_sort_value, market_sort_value_key = ct.get_market_sort_value_key('8')
    while 1:
        try:
            # df = rl.get_sina_all_json_dd(vol, type)
            # if len(df) > cut_num:
            #     df = df[:cut_num]
            #     print len(df),
            # top_now = rl.get_sina_dd_count_price_realTime(df)
            # print len(top_now)

            time_Rt = time.time()
            top_now = tdd.getSinaAlldf(
                market='all', vol=ct.json_countVol, vtype=ct.json_countType)
            time_d = time.time()
            if time_d - time_s > delay_time:
                status_change = True
                time_s = time.time()
                top_all = pd.DataFrame()

            else:
                status_change = False
            if len(top_now) > 10 and len(top_now.columns) > 4:
               # top_now = top_now[top_now.trade >= top_now.high * 0.98]
               # if 'percent' in top_now.columns.values:
                   # top_now = top_now[top_now['percent'] >= 0]

                if len(top_all) == 0 and len(lastpTDX_DF) == 0:
                    cct.get_terminal_Position(position=sys.argv[0])

                    time_Rt = time.time()
                    top_all, lastpTDX_DF = tdd.get_append_lastp_to_df(top_now)
                elif len(top_all) == 0 and len(lastpTDX_DF) > 0:
                    time_Rt = time.time()
                    top_all = tdd.get_append_lastp_to_df(top_now, lastpTDX_DF)
                    # dd=dd.fillna(0)
                else:
                    # for symbol in top_now.index:
                    #     if symbol in top_all.index:
                    #         count_n = top_now.loc[symbol, 'couts']
                    #         count_a = top_all.loc[symbol, 'couts']
                    #         top_now.loc[symbol, 'dff'] = count_n - count_a
                    #         if status_change:
                    #             # top_all.loc[symbol] = top_now.loc[symbol]
                    #             top_all.loc[symbol, ['name', 'percent', 'dff', 'couts', 'trade', 'high', 'open', 'low', 'ratio', 'volume',
                    #                                  'prev_p']] = top_now.loc[symbol, ['name', 'percent', 'dff', 'couts', 'trade', 'high', 'open', 'low', 'ratio', 'volume',
                    #                                                                    'prev_p']]
                    #         else:
                    #             top_all.loc[symbol, ['percent', 'dff']] = top_now.loc[
                    #                 symbol, ['percent', 'dff']]
                    #             # top_all.loc[symbol, 'trade':] = top_now.loc[symbol, 'trade':]
                    #             top_all.loc[symbol, ['trade', 'high', 'open', 'low', 'ratio', 'volume',
                    #                                  'prev_p']] = top_now.loc[symbol, ['trade', 'high', 'open', 'low', 'ratio', 'volume',
                    #                                                                    'prev_p']]
                    #     else:
                    #         top_all.append(top_now.loc[symbol])
                    top_all = cct.combine_dataFrame(top_all, top_now, col='couts', compare='dff')

                # top_all=top_all.sort_values(by=['dff','percent','couts'],ascending=[0,0,1])
                # top_all=top_all.sort_values(by=['dff','ratio','percent','couts'],ascending=[0,1,0,1])
                # top_all=top_all.sort_values(by=['dff','percent','couts','ratio'],ascending=[0,0,1,1])

                top_bak = top_all
                codelist = top_all.index.tolist()
                if len(codelist) > 0:
                    # log.info('toTDXlist:%s' % len(codelist))
                    # tdxdata = tdd.get_tdx_all_day_LastDF(codelist)
                    # log.debug("TdxLastP: %s %s" % (len(tdxdata), tdxdata.columns.values))
                    # tdxdata.rename(columns={'low': 'llow'}, inplace=True)
                    # tdxdata.rename(columns={'high': 'lhigh'}, inplace=True)
                    # tdxdata.rename(columns={'close': 'lastp'}, inplace=True)
                    # tdxdata.rename(columns={'vol': 'lvol'}, inplace=True)
                    # tdxdata = tdxdata.loc[:, ['llow', 'lhigh', 'lastp', 'lvol', 'date']]
                    # # data.drop('amount',axis=0,inplace=True)
                    # log.debug("TDX Col:%s" % tdxdata.columns.values)
                    # # df_now=top_all.merge(data,on='code',how='left')
                    # # df_now=pd.merge(top_all,data,left_index=True,right_index=True,how='left')
                    # top_all = top_all.merge(tdxdata, left_index=True, right_index=True, how='left')
                    # log.info('Top-merge_now:%s' % (top_all[:1]))
                    # top_all = top_all[top_all['llow'] > 0]
                    # log.info("df:%s" % top_all[:1])
                    radio_t = cct.get_work_time_ratio()
                    log.debug("Second:vol/vol/:%s" % radio_t)
                    # top_dif['volume'] = top_dif['volume'].apply(lambda x: round(x / radio_t, 1))
                    log.debug("top_diff:vol")
                    top_all['volume'] = (
                        map(lambda x, y: round(x / y / radio_t, 1), top_all['volume'].values, top_all['lvol'].values))

                    if cct.get_now_time_int() > 915:
                        top_all = top_all[top_all.low > top_all.llow * ct.changeRatio]
                        # top_all = top_all[top_all.trade > top_all.lhigh * ct.changeRatio]

                    # if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 926:
                    #     top_all['percent'] = (map(lambda x, y: round(
                    #         (x - y) / y * 100, 1) if int(y) > 0 else 0, top_all.trade, top_all.llastp))

                    # top_all = top_all[top_all.prev_p >= top_all.lhigh]
                    # top_all = top_all.loc[:,
                        # ['name', 'percent', 'ma5d','dff', 'couts', 'volume', 'trade', 'prev_p', 'ratio']]
                    if cct.get_now_time_int() > 1030 and cct.get_now_time_int() < 1400:
                        top_all = top_all[(top_all.volume > ct.VolumeMinR) & (
                            top_all.volume < ct.VolumeMaxR)]

                top_all = top_all.sort_values(
                    by=ct.Monitor_sort_count, ascending=[0, 0, 0, 0, 1])
                # top_all = top_all.sort_values(by=['dff', 'couts', 'volume', 'ratio'], ascending=[0, 0, 0, 1])
                # top_all=top_all.sort_values(by=['percent','dff','couts','ratio'],ascending=[0,0,1,1])
                if cct.get_now_time_int() > 930 and 'llastp' in top_all.columns:

                    top_all = top_all[top_all.trade >= top_all.llastp * ct.changeRatio]

                cct.set_console(width, height, title=[
                                'G:%s' % len(top_all), 'zx %s' % (blkname)])

                if len(top_all[top_all.dff > 0]) == 0:
                    top_all['dff'] = (map(lambda x, y: round((x - y) / y * 100, 1),
                                          top_all['buy'].values, top_all['lastp'].values))

                top_temp = top_all[:ct.PowerCount].copy()
                top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl)
                goldstock = len(top_all[(top_all.buy >= top_all.lhigh * 0.99) & (top_all.buy >= top_all.llastp * 0.99)])

                top_all = tdd.get_powerdf_to_all(top_all, top_temp)

                top_temp = stf.getBollFilter(df=top_temp, boll=ct.bollFilter, duration=ct.PowerCountdl, filter=False)
                print "G:%s Rt:%0.1f dT:%s N:%s T:%s" % (goldstock, float(time.time() - time_Rt), cct.get_time_to_date(time_s), cct.get_now_time(), len(top_temp))
                if 'op' in top_temp.columns:
                    # top_temp = top_temp.sort_values(by=['ra','percent','couts'],ascending=[0, 0,0])

                    # top_temp = top_temp.sort_values(by=ct.Monitor_sort_op,
                                                    # ascending=ct.Monitor_sort_op_key)

                    # top_temp = top_temp.sort_values(by=ct.Duration_percent_op,
                                        # ascending=ct.Duration_percent_op_key)
                    top_temp = top_temp.sort_values(by=(market_sort_value),
                                                    ascending=market_sort_value_key)

                    # top_temp = top_temp.sort_values(by=['op','ra','dff', 'percent', 'ratio'], ascending=[0,0,0, 0, 1])
                # if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 935:
                #     top_temp = top_temp.loc[:, ct.Monitor_format_trade]
                # else:
                #     top_temp = top_temp.loc[:, ct.Monitor_format_trade]
                ct_MonitorMarket_Values = ct.get_Duration_format_Values(ct.Monitor_format_trade, market_sort_value[:2])
                print rl.format_for_print(top_temp.loc[:, ct_MonitorMarket_Values][:10])  
                # print rl.format_for_print(top_temp.loc[:, ct.Sina_Monitor_format][:10])

                # print rl.format_for_print(top_all[:10])
                # print "staus",status
                if status:
                    for code in top_all[:10].index:
                        code = re.findall('(\d+)', code)
                        if len(code) > 0:
                            code = code[0]
                            kind = sl.get_multiday_ave_compare_silent(code)
                top_all = top_bak
                del top_bak
                gc.collect()

            else:
                print "no data"
            int_time = cct.get_now_time_int()
            if cct.get_work_time():
                if int_time < 930:
                    while 1:
                        cct.sleep(60)
                        if cct.get_now_time_int() < 931:
                            cct.sleep(60)
                            print ".",
                        else:
                            top_all = pd.DataFrame()
                            time_s = time.time()
                            print "."
                            break
                else:
                    cct.sleep(60)
            elif cct.get_work_duration():
                while 1:
                    cct.sleep(60)
                    if cct.get_work_duration():
                        print ".",
                        cct.sleep(60)
                    else:
                        print "."
                        cct.sleeprandom(60)
                        top_all = pd.DataFrame()
                        time_s = time.time()
                        break
            else:
                raise KeyboardInterrupt("StopTime")

        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # cct.sleep(1)
            # if success > 3:
            #     raw_input("Except")
            # st=raw_input("status:[go(g),clear(c),quit(q,e)]:")
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

            elif st.lower() == 'g' or st.lower() == 'go':
                status = True
            elif st.lower() == 'clear' or st.lower() == 'c':
                top_all = pd.DataFrame()
                status = False
            elif st.startswith('w') or st.startswith('a'):
                args = cct.writeArgmain().parse_args(st.split())
                codew = stf.WriteCountFilter(top_temp, writecount=args.dl)
                if args.code == 'a':
                    cct.write_to_blocknew(block_path, codew)
                    # cct.write_to_blocknew(all_diffpath,codew)
                else:
                    cct.write_to_blocknew(block_path, codew, False)
                    # cct.write_to_blocknew(all_diffpath,codew,False)
                print "wri ok:%s" % block_path
                cct.sleeprandom(ct.duration_sleep_time / 2)
                # cct.sleep(5)
            elif st.lower() == 'r':
                dir_mo = eval(cct.eval_rule)
                evalcmd(dir_mo)
            elif st.startswith('q') or st.startswith('e'):
                print "exit:%s" % (st)
            else:
                print "input error:%s" % (st)
        except (IOError, EOFError) as e:
            print "IOError,EOFError", e
            cct.sleeprandom(ct.duration_sleep_time / 2)
            # raw_input("Except")
        except Exception as e:
            print "other Error", e
            import traceback
            traceback.print_exc()
            cct.sleeprandom(ct.duration_sleep_time / 2)
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
