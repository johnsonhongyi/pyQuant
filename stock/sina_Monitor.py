# -*- coding:utf-8 -*-
# !/usr/bin/env python

# import sys
# reload(sys)
# sys.setdefaultencoding('gbk')

#
# reload(sys)
#
# sys.setdefaultencoding('utf-8')
url_s = "http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=0&type=1"
url_b = "http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=100000&type=0"
# status_dict = {u"???": "normal", u"??": "up", u"??": "down"}
status_dict = {u"mid": "normal", u"buy": "up", u"sell": "down"}
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

import JohnsonUtil.commonTips as cct
import JohnsonUtil.johnson_cons as ct
import singleAnalyseUtil as sl

from JSONData import tdx_data_Day as tdd
from JSONData import powerCompute as pct
from JSONData import stockFilter as stf
from JohnsonUtil import LoggerFactory as LoggerFactory
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
                    print(eval(cmd))
                print ''
            except Exception, e:
                print e
                # evalcmd(dir_mo)
                # break


if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))
    # log = LoggerFactory.getLogger('SinaMarket')
    # log.setLevel(LoggerFactory.DEBUG)

    from docopt import docopt
    log = LoggerFactory.log
    args = docopt(cct.sina_doc, version='SinaMarket')

    if args['-d'] == 'debug':
        log_level = LoggerFactory.DEBUG
    elif args['-d'] == 'info':
        log_level = LoggerFactory.INFO
    else:
        log_level = LoggerFactory.ERROR
    log.setLevel(log_level)

    if cct.isMac():
        width, height = 176, 22
        cct.set_console(width, height)
    else:
        width, height = 176, 22
        cct.set_console(width, height)
        # cct.terminal_positionKey_triton

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
    st_key_sort = '4'
    # st_key_sort = '3 1'
    # st_key_sort = '8'
    resample = 'd'
    market_sort_value, market_sort_value_key = ct.get_market_sort_value_key(
        st_key_sort)
    # st_key_sort = '9'
    # st_key_sort = '7'
    # st_key_sort = ct.sort_value_key_perd23
    st = None
    while 1:
        try:
            # df = rl.get_sina_all_json_dd(vol, type)
            # if len(df) > cut_num:
            #     df = df[:cut_num]
            #     print len(df),
            # top_now = rl.get_sina_dd_count_price_realTime(df)
            # print len(top_now)
            if st is None and st_key_sort in ['2', '3']:
                st_key_sort = '%s %s' % (
                    st_key_sort.split()[0], cct.get_index_fibl())
            time_Rt = time.time()
            # top_now = tdd.getSinaAlldf(market='??,rzrq',filename='yqbk', vol=ct.json_countVol, vtype=ct.json_countType)
            # top_now = tdd.getSinaAlldf(
                # market='all', vol=ct.json_countVol, vtype=ct.json_countType)
            # top_now = tdd.getSinaAlldf(market='??',filename='yqbk', vol=ct.json_countVol, vtype=ct.json_countType,trend=False)

            # top_now = tdd.getSinaAlldf(market='all', vol=ct.json_countVol, vtype=ct.json_countType)
            top_now = tdd.getSinaAlldf(market='rzrq', vol=ct.json_countVol, vtype=ct.json_countType)
            # top_now = tdd.getSinaAlldf(market='??¹?060',filename='cxg', vol=ct.json_countVol, vtype=ct.json_countType)

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
                    top_all, lastpTDX_DF = tdd.get_append_lastp_to_df(
                        top_now, resample=resample)
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
                    top_all = cct.combine_dataFrame(
                        top_all, top_now, col='couts', compare='dff')

                # top_all=top_all.sort_values(by=['dff','percent','couts'],ascending=[0,0,1])
                # top_all=top_all.sort_values(by=['dff','ratio','percent','couts'],ascending=[0,1,0,1])
                # top_all=top_all.sort_values(by=['dff','percent','couts','ratio'],ascending=[0,0,1,1])

                # top_all[(top_all.upperT > 3) & (top_all.top10 >2) &(top_all.close > top_all.upper*0.98) & (top_all.close < top_all.upper *1.05)]
                # top_all[(top_all.upperT > 3) & (top_all.top10 >2) &(top_all.close > top_all.upper*0.98) & (top_all.close < top_all.upper *1.05) &(top_all.lastp1d > top_all.upper)].name
                # cct.write_to_blocknew(block_path, dd.index.tolist())
                # writecode = "cct.write_to_blocknew(block_path, dd.index.tolist())"
                top_bak = top_all
                # market_sort_value, market_sort_value_key = ct.get_market_sort_value_key(st_key_sort, top_all=top_all)
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
                        map(lambda x, y: round(x / y / radio_t, 1), top_all['volume'].values, top_all.lvol.values))

                    # if cct.get_now_time_int() > 915:
                    # top_all = top_all[top_all.open > top_all.lasth1d]
                    # top_all = top_all[top_all.low > top_all.llow * ct.changeRatio]
                    # top_all = top_all[top_all.trade > top_all.lhigh * ct.changeRatio]

                    # if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 926:
                    #     top_all['percent'] = (map(lambda x, y: round(
                    #         (x - y) / y * 100, 1) if int(y) > 0 else 0, top_all.trade, top_all.llastp))

                    # top_all = top_all[top_all.prev_p >= top_all.lhigh]
                    # top_all = top_all.loc[:,
                    # ['name', 'percent', 'ma5d','dff', 'couts', 'volume', 'trade', 'prev_p', 'ratio']]
                    # if cct.get_now_time_int() > 1030 and cct.get_now_time_int() < 1400:
                    #     top_all = top_all[(top_all.volume > ct.VolumeMinR) & (
                    #         top_all.volume < ct.VolumeMaxR)]

                    
                if st_key_sort.split()[0] in ['4','9'] and 915 < cct.get_now_time_int() < 930:
                # if  915 < cct.get_now_time_int() < 930:
                    top_all['dff'] = (map(lambda x, y: round((x - y) / y * 100, 1),
                                          top_all['buy'].values, top_all['llastp'].values))
                    top_all['dff2'] = (map(lambda x, y: round((x - y) / y * 100, 1),
                                           top_all['buy'].values, top_all['lastp'].values))
               
                elif st_key_sort.split()[0] in ['4','9'] and 926 < cct.get_now_time_int() < 1455 and 'lastbuy' in top_all.columns:
                # elif 926 < cct.get_now_time_int() < 1455 and 'lastbuy' in top_all.columns:

                    top_all['dff'] = (map(lambda x, y: round((x - y) / y * 100, 1),
                                          top_all['buy'].values, top_all['lastbuy'].values))
                    top_all['dff2'] = (map(lambda x, y: round((x - y) / y * 100, 1),
                                           top_all['buy'].values, top_all['lastp'].values))
                    # if len(top_all[top_all.lastbuy < 0]) > 0 or len(top_all[top_all.dff < -10]) >0 :
                    #     print top_all.loc['600313'].lastbuy,top_all.loc['600313'].buy,top_all.loc['600313'].lastp
                else:
                    top_all['dff'] = (map(lambda x, y: round((x - y) / y * 100, 1),
                                          top_all['buy'].values, top_all['lastp'].values))
                    if 'lastbuy' in top_all.columns:
                        top_all['dff2'] = (map(lambda x, y: round((x - y) / y * 100, 1),
                                               top_all['buy'].values, top_all['lastbuy'].values))
                top_all = top_all.sort_values(
                    by=['dff', 'percent', 'volume', 'couts', 'ratio'], ascending=[0, 0, 0, 1, 1])

#                    by=ct.Monitor_sort_count, ascending=[0, 0, 0, 0, 1])
                # top_all = top_all.sort_values(by=['dff', 'couts', 'volume', 'ratio'], ascending=[0, 0, 0, 1])
                # top_all=top_all.sort_values(by=['percent','dff','couts','ratio'],ascending=[0,0,1,1])
                # if cct.get_now_time_int() > 930 and 'llastp' in top_all.columns:
                #     top_all = top_all[top_all.trade >= top_all.llastp * ct.changeRatio]

                cct.set_console(width, height, title=[
                                'G:%s' % len(top_all), '%s ZXG' % (blkname)])

                # if len(top_all[top_all.dff > 0]) == 0:
                #     top_all['dff'] = (map(lambda x, y: round((x - y) / y * 100, 1),

                # top_temp = top_all[ ((top_all.lastdu > 5) & (top_all.lastdu < 15)) & (top_all.fib > 1) & ( (top_all.volume > 1.2) & (top_all.volume < 3)) & (top_all.vchange < 120) &( (top_all.op > 0) & (top_all.op < 80))]
                # top_temp = top_all[(top_all.top10 >0) & (top_all.topR >0) &(top_all.boll >1) &(top_all.df2 >1)]

                # top_temp = top_all[(top_all.fib >= 1) & ((top_all.lastdu > 5) | ((top_all.vchange > 30) & (top_all.vchange < 100)))]
                # top_temp = top_all.copy()
                # top_temp =  top_all[(top_all.boll < 1) &(top_all.df2 >0) &(top_all.close > top_all.max5)]

                # '''


                st_key_sort_status=['4','x2','3'] 

                # if st_key_sort == '8':
                # if st_key_sort.split()[0] != '4':
                if st_key_sort.split()[0] not in st_key_sort_status:
                    top_temp=top_all.copy()

                elif cct.get_now_time_int() > 830 and cct.get_now_time_int() <= 935:
                    #lastl1d
                    # top_temp = top_all[(top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d) & (top_all.close > top_all.lastp1d)]
                    #lastp1d TopR 1
                    # top_temp = top_all[(top_all.low > top_all.lasth1d) & (top_all.lasth1d > top_all.lasth2d) & (top_all.close > top_all.lastp1d)]
                    
                    # 
                    # top_temp = top_all[(top_all.close / top_all.hmax > 1.1) & (top_all.close / top_all.hmax < 1.5)] 
                    top_temp = top_all[ (top_all.lastdu > 6 ) & (top_all.low > top_all.lasth1d) & (top_all.close > top_all.lastp1d)]
                    # top_now.loc['002761'].    
                    # top_temp =  top_all[( ((top_all.top10 >0) | (top_all.boll >0)) & (top_all.lastp1d > top_all.ma5d) & (top_all.close > top_all.lastp1d))]
                    # top_temp =  top_all[((top_all.lastp1d < top_all.ma5d) & (top_all.close > top_all.lastp1d))]
                    # top_temp =  top_all[((top_all.topR < 2) & (top_all.close > top_all.upper) & (top_all.close > top_all.lastp1d))]
                    # top_temp =  top_all[((top_all.topR >0) & (top_all.top10 >1) &   (top_all.close > top_all.upper) & (top_all.close > top_all.ma5d))]
                    # top_temp =  top_all[((top_all.boll >0) & (top_all.close > top_all.lastp1d))]

                    # top_all[(top_all.low >= top_all.nlow)& (top_all.high > top_all.nhigh)]
                elif cct.get_now_time_int() > 935 and cct.get_now_time_int() <= 1450:

                    # top_temp =  top_all[ ( (top_all.lastp1d > top_all.lastp2d) &(top_all.close >top_all.lastp1d )) | ((top_all.low >= top_all.nlow)) & ((top_all.lastp1d > top_all.ma5d)  & (top_all.close > top_all.ma5d) &(top_all.close > top_all.lastp1d))]

                    # top_temp =  top_all[ ((top_all.top10 >0) | (top_all.boll >0))  & (top_all.lastp1d > top_all.ma5d)  & ((top_all.low > top_all.lastl1d) | (top_all.low == top_all.open))]
                    # top_temp =  top_all[ ( (top_all.lastp1d > top_all.ma5d) ) ]
                    # top_temp =  top_all[(top_all.topR < 2)  & (top_all.close > top_all.upper) & ((top_all.low > top_all.lastp1d) | (top_all.low == top_all.open))]
                    # top_temp =  top_all[((top_all.topR >0) & (top_all.top10 >1) &   (top_all.close > top_all.upper) & (top_all.low > top_all.lastl1d) & (top_all.close > top_all.ma5d) )]
                    # top_temp =  top_all[(top_all.boll >0)  & ((top_all.low > top_all.upper) | (top_all.low == top_all.open))]
                    # top_temp =  top_all[(top_all.boll >0)  & ((top_all.low > top_all.lastp1d) | (top_all.low == top_all.open))]
                    # top_temp =  top_all[(top_all.topR < 2) & (top_all.close >= top_all.nhigh) & ((top_all.low > top_all.lastp1d) | (top_all.low == top_all.open))]
                    
                    if 'nlow' in top_all.columns:

                        # if st_key_sort == '4':
                        if st_key_sort.split()[0]  in st_key_sort_status :
                            # ???
                            # top_temp = top_all[ (top_all.topR > 0) & ((top_all.close >= top_all.nclose)) & ((top_all.open > top_all.lastp1d)) & (top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d) & (top_all.open >= top_all.nlow) ]

                            # top_temp = top_all[ ((top_all.lastp1d > top_all.ma5d) & (top_all.lastp2d > top_all.ma5d) & (top_all.close > top_all.ma5d) & (top_all.ma5d > top_all.ma10d)) & ((top_all.close >= top_all.nclose)) & ((top_all.open > top_all.lastp1d)) & (top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d) & (top_all.open >= top_all.nlow) ]

                            # 3?ma5?ģ?ma5d>ma10d,open???
                            # top_temp = top_all[ ((top_all.lastp1d > top_all.ma5d) & (top_all.lastp2d > top_all.ma5d) & (top_all.close > top_all.ma5d) \
                                # & (top_all.ma5d > top_all.ma10d)) & (top_all.open >= top_all.nlow) & ((top_all.lastp1d > top_all.ene) & (top_all.close >= top_all.ene)) ]

                            # max5>hmax,low>last1d,per1d,2d,3d>-1,per1d >ma51d...

                            # top_temp = top_all[((top_all.max5 > top_all.hmax) & (top_all.ma5d > top_all.ma10d)) & (top_all.low > top_all.lastl1d)
                            #                    & (top_all.low > top_all.lastl1d) & ( ((top_all.per1d > 0) | (top_all.lastp1d > top_all.ma51d)) \
                            #                     & ((top_all.per2d > 0) | (top_all.lastp2d > top_all.ma52d)) \
                            #                     & ((top_all.per3d > 0) | (top_all.lastp3d > top_all.ma53d)) )]

                            # max5 < top_all.hmax ,??ת???
                            # top_temp = top_all[((top_all.max5 < top_all.hmax) & ((top_all.close > top_all.hmax) | (top_all.close > top_all.max5)) )]
                            # top_temp = top_all[ (top_all.max5 < top_all.hmax) & ((top_all.close > top_all.hmax) | (top_all.close > top_all.max5))
                            #             & (top_all.low > top_all.ma51d) 
                            #             & (((top_all.per1d > 0) | (top_all.lastp1d > top_all.ma10d))
                            #             & ((top_all.per2d > 0) | (top_all.lastp2d > top_all.ma10d))
                            #             & ((top_all.per3d > 0) | (top_all.lastp3d > top_all.ma10d)))]

                            #topR and nlow > lastp1d
                            # top_temp = top_all[(top_all.low >= top_all.lasth1d) & (top_all.nlow > top_all.lastp1d) & (top_all.close > top_all.nclose) ]
                            
                           
                            # top_temp = top_all[(top_all.close / top_all.hmax > 1.1) & (top_all.close / top_all.hmax < 1.5)] 
                            # top_temp = top_all[(top_all.topU > 0) & (top_all.close > top_all.ene) & (top_all.low > top_all.lastl1d)] 
                            # top_temp = top_all[(top_all.topU > 0) & (top_all.close > top_all.ene)] 
                            

                            #TopR跳空
                            # top_temp = top_all[(top_all.topU > 0) & (top_all.close > top_all.ene)  & (top_all.topR > 0)]   #20210323
                            
                            # top_temp = top_all[ (top_all.topR > 0)] 
                            # 20210803 mod ral
                            # top_temp = top_all[top_all.close > top_all.ma20d]
                            # top_temp = top_all[(top_all.close > top_all.ma20d) & (top_all.close > top_all.max5)]
                            # top_temp = top_all[(top_all.close > top_all.ma20d) & (top_all.close >= top_all.ene)]
                            
                            #221018change
                            # top_temp = top_all[(top_all.close > top_all.ma10d) & ((top_all.close >= top_all.hmax) | (top_all.up5 > 2) | (top_all.perc3d > 3)) ]
                            #221018 振幅大于6 or 跳空 or 连涨 or upper or 大于hmax or 大于max5
                            # top_temp = top_all[ ((top_all.lastdu > 6 ) & (top_all.perc3d > 2)) | (top_all.topU > 0) | (top_all.topR > 0) | (top_all.close > top_all.hmax) | (top_all.close > top_all.max5)]
                            #20221116 
                            top_temp = top_all[ ((top_all.lastdu > 3 ) & (top_all.low <= top_all.ma5d * 1.01) & (top_all.low >= top_all.ma5d))  | (top_all.topR > 0) | (top_all.close > top_all.hmax)  ]
                            

                            # & (top_all.close >= top_all.hmax) & (top_all.hmax >= top_all.max5) 
                            #主升浪
                            # top_temp = top_all[(top_all.topU > 0) & ( (top_all.close > top_all.max5) | (top_all.close > top_all.hmax) ) & (top_all.topR > 0)] 
                            top_temp = top_temp[ (~top_temp.index.str.contains('688')) & (~top_temp.name.str.contains('ST'))]

                            # top_all[ (~top_all.index.str.contains('688'))  &(top_all.topU > 0)]  

                            # top_temp = top_all[ ((top_all.lastp1d > top_all.ma5d) & (top_all.lastp2d > top_all.ma5d) & (top_all.close > top_all.ma5d) \
                            # & (top_all.ma5d > top_all.ma10d)) & (top_all.open >= top_all.nlow) & ((top_all.lastp1d > top_all.ene) & (top_all.close >= top_all.ene)) ]

                        else:
                            #
                            # top_temp = top_all[ ((top_all.close >= top_all.ene)) & (top_all.close >= top_all.upper) & (top_all.topR > 0) & (top_all.top10 >= 0) ]

                            # 3?ma5?ģ?ma5d>ma10d,close > ene,lastp1d>ene
                            # top_temp = top_all[ ((top_all.lastp1d > top_all.ma5d) & (top_all.lastp2d > top_all.ma5d) & (top_all.close > top_all.ma5d) & (top_all.ma5d > top_all.ma10d)) & ((top_all.close >= top_all.ene)) & (top_all.close >= top_all.upper) & (top_all.topR > 0) & (top_all.top10 >= 0) ]
                            # top_temp = top_all[ ((top_all.lastp1d > top_all.ma5d) & (top_all.lastp2d > top_all.ma5d) & (top_all.close > top_all.ma5d) \
                                # & (top_all.ma5d > top_all.ma10d)) & ((top_all.lastp1d > top_all.ene) & (top_all.close >= top_all.ene))  & (top_all.topR > 0) & (top_all.top10 > 0) ]

                            # max5 > hmax(30)???
                            # top_temp = top_all[((top_all.max5 > top_all.hmax) & ( top_all.open >= top_all.nlow) &( top_all.close > top_all.lastp1d)) ]
                            # top_temp = top_all[((top_all.max5 > top_all.hmax))]

                            # max5>hmax,low>last1d,per1d,2d,3d>-1,per1d >ma51d...
                            # top_temp=top_all[((top_all.max5 > top_all.hmax) & (top_all.ma5d > top_all.ma10d)) & (top_all.low > top_all.ma51d)
                            #                     & (((top_all.per1d > 0) | (top_all.lastp1d > top_all.ma10d))
                            #                     & ((top_all.per2d > 0) | (top_all.lastp2d > top_all.ma10d))
                            #                     & ((top_all.per3d > 0) | (top_all.lastp3d > top_all.ma10d)))]

                            #topR and 
                            # top_temp = top_all[(top_all.low > top_all.lasth1d) & (top_all.close > top_all.lastp1d) & (top_all.close > top_all.ma10d)]
                            # top_temp = top_temp[~top_temp.name.str.contains('ST')]
                            # top_temp = top_all[(top_all.topU > 0) & (top_all.close > top_all.ene) & (top_all.lastp1d > top_all.ene) & (top_all.topR > 0)] 
                           
                            #TopU > upper
                            # top_temp = top_all[(top_all.topU > 0) & (top_all.close > top_all.ene)]   #20210323
                            # top_temp = top_all[ (top_all.topR > 0)] 
                            
                            #221018
                            # MA5 > ene and topU > upper
                            # top_temp = top_all[(top_all.topU > 0) & (top_all.close > top_all.ene) & (top_all.ma5d > top_all.ene)  ] 
                            #20221116 
                            top_temp = top_all[ ((top_all.lastdu > 3 ) & (top_all.low <= top_all.ma5d * 1.01) & (top_all.low >= top_all.ma5d))  | (top_all.topR > 0) | (top_all.close > top_all.hmax)  ]
                            


                            #221018 振幅大于6 or 跳空 or 连涨 or upper or 大于hmax or 大于max5
                            # top_temp = top_all[ ((top_all.lastdu > 6 ) & (top_all.perc3d > 2)) | (top_all.topU > 0) | (top_all.topR > 0) | (top_all.close > top_all.hmax) | (top_all.close > top_all.max5)]

                            #主升浪
                            # top_temp = top_all[(top_all.topU > 0) & ( (top_all.close > top_all.max5) | (top_all.close > top_all.hmax) )] 

                            top_temp = top_temp[ (~top_temp.index.str.contains('688')) & (~top_temp.name.str.contains('ST'))]

                            # ???ne??죬???Ϲ죬һ????գ?һ???ͣ
                        # top_temp = top_all[  (top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d) & (top_all.low >= top_all.nlow) & ((top_all.open >= top_all.nlow *0.998) & (top_all.open <= top_all.nlow*1.002)) ]
                        # top_temp = top_all[ (top_all.volume >= 1.2 ) & (top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d) & (top_all.low >= top_all.nlow) & ((top_all.open >= top_all.nlow *0.99) & (top_all.open <= top_all.nlow*1.01)) ]
                    else:
                        # top_temp=top_all[((top_all.close > top_all.ma51d)) & (
                        #     top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d)]
                    
                        #TopR跳空
                        # top_temp = top_all[(top_all.topU > 0) & (top_all.close > top_all.ene)  & (top_all.topR > 0)] 
                        # top_temp = top_all[ (top_all.topR > 0)] 

                        # MA5 > ene and topU > upper
                        top_temp = top_all[(top_all.topU > 0) & (top_all.close > top_all.ene) & (top_all.ma5d > top_all.ene)  ] # & (top_all.topR > 0)] 

                        top_temp = top_temp[ (~top_temp.index.str.contains('688')) & (~top_temp.name.str.contains('ST'))]
                        # top_temp = top_all[  (top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d) & (top_all.low >= top_all.nlow) & ((top_all.open >= top_all.nlow *0.998) & (top_all.open <= top_all.nlow*1.002)) ]
                        # top_temp = top_all[ (top_all.volume >= 1.2 ) & (top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d) & (top_all.close > top_all.lastp1d)]
                else:

                    if st_key_sort.split()[0] == '4':  #20210323   跳空缺口,max5 大于 hmax 或者 max5上轨
                        # top_temp = top_all[(top_all.topR > 0) & ( (top_all.max5 > top_all.hmax) | (top_all.max5 > top_all.upper) )] 
                        top_temp = top_all[(top_all.close > top_all.ma20d) & (top_all.close >= top_all.ene)]

                    else:

                        top_temp=top_all.copy()
                    # top_temp = top_temp[ (~top_temp.index.str.contains('688')) & (~top_temp.name.str.contains('ST'))]



                    
                if st_key_sort.split()[0] == 'x':
                    top_temp = top_temp[top_temp.topR != 0]


                # '''

                # if cct.get_now_time_int() > 830 and cct.get_now_time_int() <= 935:
                #     top_temp = top_all[ ((top_all.topU > 0 ) | (top_all.top10 > 0) | (top_all.topR > 0) | (top_all.top0 > 0)) & (top_all.lastl1d > top_all.ma5d)]
                # elif cct.get_now_time_int() > 935 and cct.get_now_time_int() <= 1100:
                #     if 'nlow' in top_all.columns:
                #         top_temp = top_all[ ((top_all.topU > 0 ) | (top_all.top10 > 0) | (top_all.topR > 0) | (top_all.top0 > 0)) & ((top_all.lastl1d > top_all.ma5d) &  (top_all.low >= top_all.ma5d) & (top_all.low >= top_all.nlow))]
                #     else:
                #          top_temp = top_all[ ((top_all.topU > 0 ) | (top_all.top10 > 0) | (top_all.topR > 0) | (top_all.top0 > 0)) & ((top_all.lastl1d > top_all.ma5d) &  (top_all.low >= top_all.ma5d))]
                #         # top_temp = top_all[ (top_all.volume >= 1.2 ) & (top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d) & ((top_all.lastl1d > top_all.ma5d) &  (top_all.low >= top_all.ma5d))]
                # else:
                #     # top_temp = top_all[ (top_all.volume >= 1.2 ) & (top_all.low >= top_all.lastl1d) & (top_all.lasth1d > top_all.lasth2d) & ((top_all.lastl1d > top_all.ma5d) &  (top_all.low >= top_all.ma5d))]
                #     if 'nlow' in top_all.columns:
                #         top_temp = top_all[ ((top_all.topU > 0 ) | (top_all.top10 > 0) | (top_all.topR > 0) | (top_all.top0 > 0)) & ((top_all.lastl1d > top_all.ma5d) &  (top_all.low >= top_all.ma5d) & (top_all.low >= top_all.nlow))]
                #     else:
                #          top_temp = top_all[ ((top_all.topU > 0 ) | (top_all.top10 > 0) | (top_all.topR > 0) | (top_all.top0 > 0)) & ((top_all.lastl1d > top_all.ma5d) &  (top_all.low >= top_all.ma5d))]

                # dd =top_all[(top_all.boll >0) &(top_all.df2 >0) &(top_all.low >= top_all.ma20d) &(top_all.low <= top_all.ma20d *1.05)]

                # if cct.get_now_time_int() > 925 and cct.get_now_time_int() <= 1450:
                #     if 'nlow' in top_temp.columns:                #                           top_all['buy'].values, top_all['lastp'].values))
                #         # top_temp = top_temp[(top_temp.open > top_temp.lastp1d) & ((top_temp.low >= top_temp.nlow) | (top_temp.low > top_temp.lastl1d))]
                #         # top_temp = top_temp[(top_temp.low > top_temp.lastl1d) & ((top_temp.low >= top_temp.nlow) | (top_temp.low > top_temp.lastp1d))]
                #         top_temp = top_temp[(top_temp.low > top_temp.lastl1d) & (top_temp.low >= top_temp.nlow) & (top_temp.top10 > 0)]
                #     else:
                #         if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 925:
                #             # top_temp = top_temp[(top_temp.close > top_temp.lastp1d) & (top_temp.low > top_temp.lastl1d)]
                #             # top_temp = top_temp[(top_temp.close > top_temp.lastp1d) & (top_temp.close > top_temp.lastl1d)]
                #             top_temp = top_temp[(top_temp.low > top_temp.lastl1d)  & (top_temp.top10 > 0)]
                #         else:
                #             # top_temp = top_temp[(top_temp.close > top_temp.lastp1d) & (top_temp.low > top_temp.lastl1d)]
                #             top_temp = top_temp[(top_temp.low > top_temp.lastl1d) & (top_temp.low >= top_temp.nlow) & (top_temp.top10 > 0)]

                # top_temp = stf.filterPowerCount(top_temp,ct.PowerCount,down=True)

                top_end=top_all[-int((ct.PowerCount) / 10):].copy()
                top_temp=pct.powerCompute_df(top_temp, dl=ct.PowerCountdl)
                top_end=pct.powerCompute_df(top_end, dl=ct.PowerCountdl)
                goldstock=len(top_all[(
                    top_all.buy >= top_all.lhigh * 0.99) & (top_all.buy >= top_all.llastp * 0.99)])

                top_all=tdd.get_powerdf_to_all(top_all, top_temp)

                # top_temp = stf.getBollFilter(df=top_temp, boll=ct.bollFilter, duration=ct.PowerCountdl, filter=False)
                # top_temp = stf.getBollFilter(df=top_temp, boll=ct.bollFilter, duration=ct.PowerCountdl, filter=False, ma5d=False, dl=14, percent=False, resample='d')
                # top_temp = stf.getBollFilter(df=top_temp, boll=ct.bollFilter, duration=ct.PowerCountdl, filter=True, ma5d=True, dl=14, percent=False, resample=resample)
                
                top_temp=stf.getBollFilter(
                    df=top_temp, resample=resample, down=True)
                top_end=stf.getBollFilter(
                    df=top_end, resample=resample, down=True)

                nhigh = top_temp[top_temp.close > top_temp.nhigh] if 'nhigh'  in top_temp.columns else []
                nlow = top_temp[top_temp.close > top_temp.nlow] if 'nhigh'  in top_temp.columns else []
                print "G:%s Rt:%0.1f dT:%s N:%s T:%s nh:%s nlow:%s" % (goldstock, float(time.time() - time_Rt), cct.get_time_to_date(time_s), cct.get_now_time(), len(top_temp),len(nhigh),len(nlow))

                top_temp=top_temp.sort_values(by=(market_sort_value),
                                                ascending=market_sort_value_key)
                ct_MonitorMarket_Values=ct.get_Duration_format_Values(
                    ct.Monitor_format_trade, market_sort_value[:2])

                if len(st_key_sort.split()) < 2:
                    f_sort=(st_key_sort.split()[0] + ' f ')
                else:
                    if st_key_sort.find('f') > 0:
                        f_sort=st_key_sort
                    else:
                        f_sort=' '.join(x for x in st_key_sort.split()[
                                          :2]) + ' f ' + ' '.join(x for x in st_key_sort.split()[2:])

                market_sort_value2, market_sort_value_key2=ct.get_market_sort_value_key(
                    f_sort, top_all=top_all)
                
                # ct_MonitorMarket_Values2=ct.get_Duration_format_Values(
                #     ct.Monitor_format_trade, market_sort_value2[:2])

                top_temp2=top_end.sort_values(
                    by=(market_sort_value2), ascending=market_sort_value_key2)

                ct_MonitorMarket_Values=ct.get_Duration_format_Values(
                    ct_MonitorMarket_Values, replace='b1_v', dest='volume')
                ct_MonitorMarket_Values=ct.get_Duration_format_Values(
                    ct_MonitorMarket_Values, replace='fibl', dest='top10')

                # ct_MonitorMarket_Values2=ct.get_Duration_format_Values(
                #     ct_MonitorMarket_Values2, replace='b1_v', dest='volume')
                # ct_MonitorMarket_Values2=ct.get_Duration_format_Values(
                #     ct_MonitorMarket_Values2, replace='fibl', dest='top10')



                if 'nhigh' in top_all.columns:
                    ct_MonitorMarket_Values = ct.get_Duration_format_Values(
                        ct_MonitorMarket_Values, replace='df2', dest='nhigh')
                    # ct_MonitorMarket_Values2 = ct.get_Duration_format_Values(
                    #             ct_MonitorMarket_Values2, replace='df2', dest='nhigh')
                else:
                    ct_MonitorMarket_Values = ct.get_Duration_format_Values(
                        ct_MonitorMarket_Values, replace='df2', dest='high')

                    # ct_MonitorMarket_Values2 = ct.get_Duration_format_Values(
                    #             ct_MonitorMarket_Values2, replace='df2', dest='high')

                # loc ral
                # top_temp[:5].loc[:,['name','ral']


                # if st_key_sort == '1' or st_key_sort == '7':
                if st_key_sort == '1':
                    top_temp=top_temp[top_temp.per1d < 8]

                top_dd=cct.combine_dataFrame(
                    top_temp.loc[:, ct_MonitorMarket_Values][:10], top_temp2.loc[:, ct_MonitorMarket_Values][:5], append=True, clean=True)
                # print cct.format_for_print(top_dd)

                # table,widths = cct.format_for_print(top_dd[:10],widths=True)
                table, widths=cct.format_for_print(
                    top_dd.loc[[col for col in top_dd[:9].index if col in top_temp[:10].index]], widths=True)

                print table
                cct.counterCategory(top_temp)
                print cct.format_for_print(top_dd[-4:], header=False, widths=widths)

                # print cct.format_for_print(top_temp.loc[:, ct_MonitorMarket_Values][:10])
                # print cct.format_for_print(top_temp2.loc[:, ct_MonitorMarket_Values2][:3])
                # print cct.format_for_print(top_temp.loc[:, ct.Sina_Monitor_format][:10])

                # print cct.format_for_print(top_all[:10])
                # print "staus",status
                if status:
                    for code in top_all[:10].index:
                        code=re.findall('(\d+)', code)
                        if len(code) > 0:
                            code=code[0]
                            kind=sl.get_multiday_ave_compare_silent(code)
                top_all=top_bak
                del top_bak
                gc.collect()

            else:
                print "no data"

            int_time=cct.get_now_time_int()
            if cct.get_work_time():
                if int_time < ct.open_time:
                    top_all=pd.DataFrame()
                    cct.sleep(ct.sleep_time)
                elif int_time < 930:
                    cct.sleep((930 - int_time) * 55)
                    time_s=time.time()
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
                        time_s=time.time()
                        print "."
                        break
            # old while
            # int_time = cct.get_now_time_int()
            # if cct.get_work_time():
            #     if int_time < 930:
            #         while 1:
            #             cct.sleep(60)
            #             if cct.get_now_time_int() < 930:
            #                 cct.sleep(60)
            #                 print ".",
            #             else:
            #                 top_all = pd.DataFrame()
            #                 time_s = time.time()
            #                 print "."
            #                 break
            #     else:
            #         cct.sleep(60)
            # elif cct.get_work_duration():
            #     while 1:
            #         cct.sleep(60)
            #         if cct.get_work_duration():
            #             print ".",
            #             cct.sleep(60)
            #         else:
            #             print "."
            #             cct.sleeprandom(60)
            #             top_all = pd.DataFrame()
            #             time_s = time.time()
            #             break
            else:
                raise KeyboardInterrupt("StopTime")

        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # cct.sleep(1)
            # if success > 3:
            #     raw_input("Except")
            # st=raw_input("status:[go(g),clear(c),quit(q,e)]:")
            st=cct.cct_raw_input(ct.RawMenuArgmain() % (market_sort_value))

            if len(st) == 0:
                status=False
            elif (len(st.split()[0]) == 1 and st.split()[0].isdigit()) or st.split()[0].startswith('x'):
                st_l=st.split()
                st_k=st_l[0]
                if st_k in ct.Market_sort_idx.keys() and len(top_all) > 0:
                    st_key_sort=st
                    market_sort_value, market_sort_value_key=ct.get_market_sort_value_key(
                        st_key_sort, top_all=top_all)
                else:
                    log.error("market_sort key error:%s" % (st))
                    cct.sleeprandom(5)

            elif st.lower() == 'g' or st.lower() == 'go':
                status=True
            elif st.lower() == 'clear' or st.lower() == 'c':
                top_all=pd.DataFrame()
                cct.GlobalValues().setkey('lastbuylogtime', 1)
                # cct.set_clear_logtime()
                status=False
            elif st.startswith('w') or st.startswith('a'):
                args=cct.writeArgmain().parse_args(st.split())
                codew=stf.WriteCountFilter(top_temp, writecount=args.dl)
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
                dir_mo=eval(cct.eval_rule)
                evalcmd(dir_mo)
            elif st.startswith('q') or st.startswith('e'):
                print "exit:%s" % (st)
                sys.exit(0)
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
