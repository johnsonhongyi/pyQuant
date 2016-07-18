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
from JohhnsonUtil import LoggerFactory as LoggerFactory
# cct.set_ctrl_handler()
if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))

    log = LoggerFactory.getLogger('SinaMarket')
    # log.setLevel(LoggerFactory.DEBUG)
    if cct.isMac():
        width, height = 122, 16
        cct.set_console(width, height)
    else:
        width, height = 122, 18
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
    while 1:
        try:
            # df = rl.get_sina_all_json_dd(vol, type)
            # if len(df) > cut_num:
            #     df = df[:cut_num]
            #     print len(df),
            # top_now = rl.get_sina_dd_count_price_realTime(df)
            # print len(top_now)
            
            top_now = tdd.getSinaAlldf(market='cyb', vol=ct.json_countVol, type=ct.json_countType)
            time_Rt = time.time()
            time_d = time.time()
            if time_d - time_s > delay_time:
                status_change = True
                time_s = time.time()
                top_all = pd.DataFrame()

            else:
                status_change = False
            if len(top_now) > 10 and len(top_now.columns) > 4:
                top_now = top_now[top_now.trade >= top_now.high * 0.98]
                if 'percent' in top_now.columns.values:
                    top_now = top_now[top_now['percent'] >= 0]

                if len(top_all) == 0 and len(lastpTDX_DF) == 0:
                    time_Rt = time.time()
                    top_all,lastpTDX_DF = tdd.get_append_lastp_to_df(top_now)
                elif len(top_all) == 0 and len(lastpTDX_DF) > 0:
                    time_Rt = time.time()
                    top_all = tdd.get_append_lastp_to_df(top_now,lastpTDX_DF)
                    # dd=dd.fillna(0)
                else:
                    for symbol in top_now.index:

                        # code = rl._symbol_to_code(symbol)
                        if symbol in top_all.index:
                            # if top_all.loc[symbol,'diff'] == 0:
                            # print "code:",symbol
                            count_n = top_now.loc[symbol, 'counts']
                            count_a = top_all.loc[symbol, 'counts']
                            top_now.loc[symbol, 'diff'] = count_n - count_a
                            if status_change:
                                # top_all.loc[symbol] = top_now.loc[symbol]
                                top_all.loc[symbol,['name', 'percent', 'diff', 'counts', 'trade', 'high', 'open', 'low', 'ratio', 'volume',
                               'prev_p']] = top_now.loc[symbol,['name', 'percent', 'diff', 'counts', 'trade', 'high', 'open', 'low', 'ratio', 'volume',
                               'prev_p']]
                            else:
                                top_all.loc[symbol, ['percent', 'diff']] = top_now.loc[symbol, ['percent', 'diff']]
                                # top_all.loc[symbol, 'trade':] = top_now.loc[symbol, 'trade':]
                                top_all.loc[symbol,['trade', 'high', 'open', 'low', 'ratio', 'volume',
                               'prev_p']] = top_now.loc[symbol,['trade', 'high', 'open', 'low', 'ratio', 'volume',
                               'prev_p']]
                                # top_all.loc[symbol,['percent','diff','trade','high','open','low','ratio']]=top_now.loc[symbol,['percent','diff','trade','high','open','low','ratio']]
                                # else:
                                # top_all.loc[symbol,['percent','trade','high','open','low','ratio']]=top_now.loc[symbol,['percent','diff','trade','high','open','low','ratio']]
                                # top_all.loc[symbol]=top_now.loc[symbol]?
                                # top_all.loc[symbol,'diff']=top_now.loc[symbol,'counts']-top_all.loc[symbol,'counts']

                                # else:
                                # value=top_all.loc[symbol,'diff']

                        else:
                            top_all.append(top_now.loc[symbol])
                # top_all=top_all.sort_values(by=['diff','percent','counts'],ascending=[0,0,1])
                # top_all=top_all.sort_values(by=['diff','ratio','percent','counts'],ascending=[0,1,0,1])
                # top_all=top_all.sort_values(by=['diff','percent','counts','ratio'],ascending=[0,0,1,1])

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
                        top_all = top_all[top_all.trade > top_all.lastp]
                        top_all = top_all[top_all.trade > top_all.lhigh]
 
                    if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 931:
                        top_all['percent']= (map(lambda x, y: round((x-y)/y*100,1) if int(y) > 0 else 0, top_all.trade, top_all.lastp))

                    # top_all = top_all[top_all.prev_p >= top_all.lhigh]
                    # top_all = top_all.loc[:,
                              # ['name', 'percent', 'ma5d','diff', 'counts', 'volume', 'trade', 'prev_p', 'ratio']]
                    if cct.get_now_time_int() > 1030 and cct.get_now_time_int() < 1400:           
                        top_all = top_all[(top_all.volume > ct.VolumeMinR) & (top_all.volume < ct.VolumeMaxR)]

                top_all = top_all.sort_values(by=ct.Monitor_sort_count, ascending=[0,0, 0, 0, 1])
                # top_all = top_all.sort_values(by=['diff', 'counts', 'volume', 'ratio'], ascending=[0, 0, 0, 1])
                # top_all=top_all.sort_values(by=['percent','diff','counts','ratio'],ascending=[0,0,1,1])
                if cct.get_now_time_int() > 930 and 'lastp' in top_all.columns: 
                
                    top_all = top_all[top_all.trade > top_all.lastp]

                cct.set_console(width, height,title=['G:%s' % len(top_all), 'zxg: %s' % (blkname)])
 


                top_temp = top_all[:ct.PowerCount].copy()
                top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl)
                
                print "G:%s Rt:%0.1f dT:%s " % (len(top_all),float(time.time() - time_Rt),cct.get_time_to_date(time_s))

               
                if 'op' in top_temp.columns:
                    # top_temp = top_temp.sort_values(by=['ra','percent','counts'],ascending=[0, 0,0])
                    top_temp = top_temp.sort_values(by=ct.Monitor_sort_op,
                                        ascending=ct.Monitor_sort_op_key)

                    # top_temp = top_temp.sort_values(by=['op','ra','diff', 'percent', 'ratio'], ascending=[0,0,0, 0, 1])
                if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 935:
                    top_temp = top_temp.loc[:,ct.Monitor_format_trade]
                else:
                    top_temp = top_temp.loc[:,ct.Monitor_format_trade]
                print rl.format_for_print(top_temp[:10])
                
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
                        cct.sleep(random.randint(0, 30))
                        top_all = pd.DataFrame()
                        time_s = time.time()
                        break
            else:
                # break
                # cct.sleep(5)
                st = raw_input("status:[go(g),clear(c),quit(q,e),W(w),Wa(a)]:")
                if len(st) == 0:
                    status = False
                elif st.lower() == 'g' or st.lower() == 'go':
                    status = True
                    for code in top_all[:10].index:
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
                        cct.write_to_blocknew(block_path, codew[:10])
                        # cct.write_to_blocknew(all_diffpath, codew)
                    else:
                        cct.write_to_blocknew(block_path, codew[:10], False)
                        # cct.write_to_blocknew(all_diffpath, codew, False)
                    print "wri ok:%s" % block_path
                    # cct.sleep(2)
                else:
                    sys.exit(0)

        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # cct.sleep(1)
            # if success > 3:
            #     raw_input("Except")
            #     sys.exit(0)
            # st=raw_input("status:[go(g),clear(c),quit(q,e)]:")
            st = raw_input("status:[go(g),clear(c),quit(q,e),W(w),Wa(a)]:")

            if len(st) == 0:
                status = False
            elif st.lower() == 'g' or st.lower() == 'go':
                status = True
            elif st.lower() == 'clear' or st.lower() == 'c':
                top_all = pd.DataFrame()
                status = False
            elif st.lower() == 'w' or st.lower() == 'a':
                # base_path=r"E:\DOC\Parallels\WinTools\zd_pazq\T0002\blocknew\\"
                # block_path=base_path+'064.blk'
                # all_diffpath=base_path+'\065.blk'
                codew = top_temp[:10].index.tolist()
                if st.lower() == 'a':
                    cct.write_to_blocknew(block_path, codew)
                    # cct.write_to_blocknew(all_diffpath,codew)
                else:
                    cct.write_to_blocknew(block_path, codew, False)
                    # cct.write_to_blocknew(all_diffpath,codew,False)
                print "wri ok:%s" % block_path
                # cct.sleep(5)
            else:
                sys.exit(0)
        except (IOError, EOFError) as e:
            print "Error", e
            sleeptime=random.randint(5, 15)
            print "Error2sleep:%s"%(sleeptime)
            cct.sleep(sleeptime)
            # traceback.print_exc()
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
