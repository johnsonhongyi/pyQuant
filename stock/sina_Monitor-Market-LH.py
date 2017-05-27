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
# from pandas import DataFrame
# import sys
# print sys.path

import JohhnsonUtil.johnson_cons as ct
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd
from JSONData import powerCompute as pct
from JSONData import stockFilter as stf
from JSONData import wencaiData as wcd
from JohhnsonUtil import LoggerFactory
from JohhnsonUtil import commonTips as cct
import singleAnalyseUtil as sl

# from logbook import Logger,StreamHandler,SyslogHandler
# from logbook import StderrHandler

def downloadpage(url):
    fp = urllib2.urlopen(url)
    data = fp.read()
    fp.close()
    return data


def parsehtml(data):
    soup = BeautifulSoup(data)
    for x in soup.findAll('a'):
        print x.attrs['href']


def html_clean_content(soup):
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    soup.prettify()
    reg1 = re.compile("<[^>]*>")  # 剔除空行空格
    content = reg1.sub('', soup.prettify())
    print content


def get_sina_url(vol='0', type='0', pageCount='100'):
    # if len(pageCount) >=1:
    url = ct.SINA_DD_VRatio_All % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES[
                                   'sinadd_all'], pageCount, ct.DD_VOL_List[vol], type)
    # print url
    return url

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
        elif len(cmd)==0:
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
    # log = LoggerFactory.getLogger('SinaMarket')
    # pd.options.mode.chained_assignment = None
    from docopt import docopt
    log = LoggerFactory.log
    args = docopt(cct.sina_doc, version='sina_cxdn')
    log_level = LoggerFactory.DEBUG if args['--debug'] else LoggerFactory.ERROR
    log.setLevel(log_level)    
    # log=LoggerFactory.JohnsonLoger('SinaMarket').setLevel(LoggerFactory.DEBUG)
    # log.setLevel(LoggerFactory.DEBUG)
    if cct.isMac():
        width, height = 174, 16
        cct.set_console(width, height)
    else:
        width, height = 174, 18
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
    # block_path = tdd.get_tdx_dir_blocknew() + '067.blk'
    # blkname = '067.blk'
    blkname = '063.blk'
    block_path = tdd.get_tdx_dir_blocknew() + blkname
    lastpTDX_DF = pd.DataFrame()
    duration_date = ct.duration_date
    end_date = cct.last_tddate(days=3)
    # all_diffpath = tdd.get_tdx_dir_blocknew() + '062.blk'
    market_sort_value = ct.Market_sort_idx['2']
    while 1:
        try:
            # top_now = tdd.getSinaAlldf(market='sh', vol=ct.json_countVol, type=ct.json_countType)
            time_Rt = time.time()
            top_now = tdd.getSinaAlldf(market='次新股',filename='cxg', vol=ct.json_countVol, type=ct.json_countType)
            # print top_now.loc['300208','name']
            df_count = len(top_now)
            now_count = len(top_now)
            radio_t = cct.get_work_time_ratio()
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
            log.info("top_now.buy[:30]>0:%s" %
                     len(top_now[:30][top_now[:30]['buy'] > 0]))
            if len(top_now) > 10 or cct.get_work_time():
                # if len(top_now) > 10 or len(top_now[:10][top_now[:10]['buy'] > 0]) > 3:
                # if len(top_now) > 10 and not top_now[:1].buy.values == 0:
                #     top_now=top_now[top_now['percent']>=0]
                if 'trade' in top_now.columns:
                    top_now['buy'] = (map(lambda x, y: y if int(x) == 0 else x, top_now['buy'].values, top_now['trade'].values))

                if len(top_all) == 0 and len(lastpTDX_DF) == 0:
                    cct.get_terminal_Position(position=sys.argv[0])

                    # time_Rt = time.time()
                    top_all,lastpTDX_DF = tdd.get_append_lastp_to_df(top_now,end=end_date,dl=duration_date)
                elif len(top_all) == 0 and len(lastpTDX_DF) > 0:
                    # time_Rt = time.time()
                    top_all = tdd.get_append_lastp_to_df(top_now,lastpTDX_DF)



                else:
                    if 'couts' in top_now.columns.values:
                        if not 'couts' in top_all.columns.values:
                            top_all['couts'] = 0
                            top_all['prev_p'] = 0
                    # for symbol in top_now.index:
                    #     if symbol in top_all.index and top_now.loc[symbol, 'buy'] <> 0:
                    #         if 'couts' in top_now.columns.values:
                    #             top_all.loc[symbol, 'buy':'prev_p'] = top_now.loc[
                    #                 symbol, 'buy':'prev_p']
                    #         else:
                    #             top_all.loc[symbol, 'buy':'low'] = top_now.loc[
                    #                 symbol, 'buy':'low']
                    top_all=cct.combine_dataFrame(top_all,top_now, col=None)
                top_dif = top_all.copy()
                
                top_dif=top_dif[top_dif.lvol > ct.LvolumeSize]
                # if top_dif[:1].llow.values <> 0:
                # if not (cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 925):
                if len(top_dif[:5][top_dif[:5]['buy'] > 0]) > 3:
                    log.debug('diff2-0-buy>0')
                    if cct.get_now_time_int() > 915 and cct.get_now_time_int() < ct.checkfilter_end_time:
                        top_dif = top_dif[top_dif.low > top_dif.llow * ct.changeRatio]
                    log.debug('dif4 open>low0.99:%s' % len(top_dif))
                    # top_dif['buy'] = (map(lambda x, y: y if int(x) == 0 else x, top_dif['buy'].values, top_dif['trade'].values))
                    # if 'volumn' in top_dif.columns and 'lvol' in top_dif.columns:
                top_dif['volume'] = (map(lambda x, y: round(x / y / radio_t, 1),top_dif['volume'], top_dif['lvol']))


                # if 'lastp' in top_dif.columns and 'buy' in top_dif.columns:
                top_dif['dff']=map(lambda x, y: round((x - y)/y * 100, 1),top_dif['buy'].values,top_dif['lastp'].values)
               
                if len(top_dif) == 0:
                    print "No G,DataFrame is Empty!!!!!!"
                else:
                    # top_dif = top_dif[top_dif.buy >= top_dif.open*0.99]
                    # log.debug('dif5 buy>open:%s'%len(top_dif))
                    # top_dif = top_dif[top_dif.trade >= top_dif.buy]

                    # df['volume']= df['volume'].apply(lambda x:x/100)

                    # if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 926:
                        # top_dif['percent']= (map(lambda x, y: round((x-y)/y*100,1) if int(y) > 0 else 0, top_dif.buy, top_dif.llastp))

                    if 'couts' in top_dif.columns.values:
                        top_dif = top_dif.sort_values(by=ct.Monitor_sort_count,ascending=[0, 0, 0, 1, 0])
                    else:
                        # print "Good Morning!!!"
                        top_dif = top_dif.sort_values(
                            by=['dff', 'percent', 'ratio'], ascending=[0, 0, 1])

                    # top_all=top_all.sort_values(by=['percent','dff','couts','ratio'],ascending=[0,0,1,1])

                    top_temp = top_dif[:ct.PowerCount].copy()
                    top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl,talib=True)
                    goldstock = len(top_dif[(top_dif.buy >= top_dif.lhigh * 0.99) & (top_dif.buy >= top_dif.llastp * 0.99)])

                    cct.set_console(width, height,
                        title=['dT:%s' % cct.get_time_to_date(time_s), 'G:%s' % len(top_dif), 'zxg: %s' % (blkname)])

                    top_all = tdd.get_powerdf_to_all(top_all,top_temp)
                    # top_temp = stf.getBollFilter(df=top_temp, boll=ct.bollFilter,duration=ct.PowerCountdl)
                    top_temp = stf.getBollFilter(df=top_temp, boll=-10,duration=ct.PowerCountdl)
                    print("A:%s N:%s K:%s %s G:%s" % (
                        df_count, now_count, len(top_all[top_all['buy'] > 0]),
                        len(top_now[top_now['volume'] <= 0]), goldstock)),
                    # print "Rt:%0.3f" % (float(time.time() - time_Rt))
                    print "Rt:%0.1f dT:%s N:%s T:%s %s%%" % (float(time.time() - time_Rt), cct.get_time_to_date(time_s),cct.get_now_time(),len(top_temp),round(len(top_temp)/now_count*100,1))
                    if 'op' in top_temp.columns:

                        if duration_date > ct.duration_date_sort:
                            top_temp = top_temp.sort_values(by=eval(market_sort_value),
                                        ascending=eval(market_sort_value+'_key'))
                        else:
                            top_temp = top_temp.sort_values(by=eval(market_sort_value),
                                        ascending=eval(market_sort_value+'_key'))
                    # if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 935:
                    #     # top_temp = top_temp[ (top_temp['ma5d'] > top_temp['ma10d']) & (top_temp['buy'] > top_temp['ma10d']) ]
                    #     top_temp = top_temp.loc[:,ct.MonitorMarket_format_buy]
                    # else:
                    #     # top_temp = top_temp[ (top_temp['ma5d'] > top_temp['ma10d']) & (top_temp['buy'] > top_temp['ma10d']) ]
                    #     top_temp = top_temp.loc[:,ct.MonitorMarket_format_buy]
                    print rl.format_for_print(top_temp.loc[:,ct.MonitorMarket_format_buy][:10])

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
                    cct.sleep((929 - int_time) * 60)
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
#                import sys
#                sys.exit(0)
                raise KeyboardInterrupt("Stop")
        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # cct.sleep(1)
            # if success > 3:
            #     raw_input("Except")
            #     sys.exit(0)
            st = cct.cct_raw_input(ct.RawMenuArgmain()%(market_sort_value))

            if len(st) == 0:
                status = False
            elif len(st) == 1 and st.isdigit():
                if st in ct.Market_sort_idx.keys():
                    market_sort_value = ct.Market_sort_idx[st]
                else:
                    log.error("market_sort key error:%s"%(st))
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
                # args = cct.writeArgmainParser(st.split())
                codew = stf.WriteCountFilter(top_temp,writecount=args.dl)
                if args.code == 'a':
                    # cct.write_to_blocknew(block_path, codew[:ct.writeCount])
                    cct.write_to_blocknew(block_path, codew)
                    # cct.write_to_blocknew(all_diffpath, codew)
                else:
                    # cct.write_to_blocknew(block_path, codew[:ct.writeCount], False)
                    cct.write_to_blocknew(block_path, codew, False)
                    # cct.write_to_blocknew(all_diffpath, codew, False)
                print "wri ok:%s" % block_path
                cct.sleeprandom(ct.duration_sleep_time/2)

                # cct.sleep(2)
            else:
                print "input error:%s"%(st)
                sys.exit(0)
        except (IOError, EOFError, Exception) as e:
            print "Error::", e
            import traceback
            traceback.print_exc()
            cct.sleeprandom(ct.duration_sleep_time/2)
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
