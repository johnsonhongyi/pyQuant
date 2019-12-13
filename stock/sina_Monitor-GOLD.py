# -*- coding:utf-8 -*-
# !/usr/bin/env python


# import sys
#
# reload(sys)
#
# sys.setdefaultencoding('utf-8')

# import random
import re
import sys
import time
# import urllib2

# from pandas import DataFrame
import pandas as pd
import JohnsonUtil.johnson_cons as ct
import JohnsonUtil.commonTips as cct
import singleAnalyseUtil as sl

from JSONData import tdx_data_Day as tdd
from JSONData import powerCompute as pct
from JSONData import stockFilter as stf
from JohnsonUtil import LoggerFactory as LoggerFactory

# log = LoggerFactory.getLogger('SinaMonitor-Gold')

# import json
# try:
#     from urllib.request import urlopen, Request
# except ImportError:
#     from urllib2 import urlopen, Request

url_s = "http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=0&type=1"
url_b = "http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=100000&type=0"
url_real_sina = "http://finance.sina.com.cn/realstock/"
url_real_sina_top = "http://vip.stock.finance.sina.com.cn/mkt/#stock_sh_up"
url_real_east = "http://quote.eastmoney.com/sz000004.html"


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
    url = ct.SINA_DD_VRatio_All % (
        ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'], pageCount, ct.DD_VOL_List[vol], type)
    print url
    return url

    # print len(data),len(df)
    # for ix in df.index:
    #     code = re.findall('(\d+)', ix)
    #     if len(code) > 0:
    #         code = code[0]
    #         status = sl.get_multiday_ave_compare_silent(code)
    #         if status:
    #             code_g[code]= df.loc[ix,'name']
    # interval = (time.time() - start_t)
    # print "time:", interval


def evalcmd(dir_mo):
    end = True
    import readline
    # import rlcompleter
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

    # width, height = 132, 18
    if cct.isMac():
        width, height = 160, 16
        cct.set_console(width, height)
    else:
        width, height = 160, 20
        cct.set_console(width, height)

    # cct.set_console(width, height)
    # log.setLevel(LoggerFactory.DEBUG)
    status = False
    vol = ct.json_countVol
    type = ct.json_countType
    top_all = pd.DataFrame()
    code_a = {}
    success = 0
    time_s = time.time()
    # delay_time = 3600
    delay_time = cct.get_delay_time()
    # base_path = tdd.get_tdx_dir()
    # block_path = tdd.get_tdx_dir_blocknew() + '065.blk'
    blkname = '065.blk'
    block_path = tdd.get_tdx_dir_blocknew() + blkname
    lastpTDX_DF = pd.DataFrame()
    parser = cct.MoniterArgmain()
    parserDuraton = cct.DurationArgmain()

    market_sort_value, market_sort_value_key = ct.get_market_sort_value_key(
        ct.sort_value_key_perd)

    while 1:
        try:
            time_Rt = time.time()
            market_blk = 'captops'
            top_now = tdd.getSinaAlldf(
                market=market_blk, vol=ct.json_countVol, vtype=ct.json_countType)
            # print top_now
            # print top_now.columns
            time_d = time.time()
            if time_d - time_s > delay_time:
                status_change = True
                time_s = time.time()
                top_all = pd.DataFrame()

            else:
                status_change = False
            if len(top_now) > 10 and len(top_now.columns) > 4:
                # if 'percent' in top_now.columns.values:
                #     top_now=top_now[top_now['percent']>0]
                if 'trade' in top_now.columns:
                    top_now['buy'] = (
                        map(lambda x, y: y if int(x) == 0 else x, top_now['buy'].values, top_now['trade'].values))

                if len(top_all) == 0 and len(lastpTDX_DF) == 0:
                    cct.get_terminal_Position(position=sys.argv[0])

                    # time_Rt = time.time()
                    top_all, lastpTDX_DF = tdd.get_append_lastp_to_df(top_now)
                elif len(top_all) == 0 and len(lastpTDX_DF) > 0:
                    # time_Rt = time.time()
                    top_all = tdd.get_append_lastp_to_df(top_now, lastpTDX_DF)
                    # top_all = top_all.merge(lastpTDX_DF, left_index=True, right_index=True, how='left')
                    # top_all = top_all[top_all['llow'] > 0]
                else:
                    # top_now = top_now[top_now.trade >= top_now.high * 0.98]
                    # for symbol in top_now.index:
                    #     # code = rl._symbol_to_code(symbol)
                    #     if symbol in top_all.index:

                    #         top_all.loc[symbol,['name', 'percent', 'dff', 'couts', 'trade', 'high', 'open', 'low', 'ratio', 'volume',
                    #        'prev_p']] = top_now.loc[symbol,['name', 'percent', 'dff', 'couts', 'trade', 'high', 'open', 'low', 'ratio', 'volume',
                    #        'prev_p']]

                    #     else:
                    #         top_all.append(top_now.loc[symbol])
                    top_all = cct.combine_dataFrame(top_all, top_now, col=None)

                # top_bak = top_all
                # top_all['buy'] = (
                    # map(lambda x, y: y if int(x) == 0 else x, top_all['buy'].values, top_all['trade'].values))
                codelist = top_all.index.tolist()
                if len(codelist) > 0:
                    # log.info('toTDXlist:%s' % len(codelist))
                    # top_all = tdd.get_append_lastp_to_df(top_all)
                    # log.info("df:%s" % top_all[:1])
                    radio_t = cct.get_work_time_ratio()
                    log.debug("Second:vol/vol/:%s" % radio_t)
                    # top_all['volume'] = top_all['volume'].apply(lambda x: round(x / radio_t, 1))
                    log.debug("top_diff:vol")
                    top_all['volume'] = (
                        map(lambda x, y: round(x / y / radio_t, 1), top_all['volume'].values, top_all['lvol'].values))
                    top_all['dff'] = (
                        map(lambda x, y: round(((float(x) - float(y)) / float(y) * 100), 1), top_all['buy'].values, top_all['lastp'].values))
                    if cct.get_now_time_int() > 915 and cct.get_now_time_int() < ct.checkfilter_end_time:
                        top_all = top_all[top_all.low >
                                          top_all.llow * ct.changeRatio]
                        # top_all = top_all[top_all.trade > top_all.lhigh * ct.changeRatio]

                    if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 926:
                        top_all['percent'] = (map(lambda x, y: round((x - y) / y * 100, 1)
                                                  if int(y) > 0 else 0, top_all.trade, top_all.llastp))
                    # if cct.get_now_time_int() > 930 and 'lastp' in top_all.columns:
                    #     top_all = top_all[top_all.trade >= top_all.llastp]
                    # top_all = top_all.loc[:,
                        # ['name', 'percent', 'ma5d','dff', 'couts', 'volume', 'trade', 'prev_p', 'ratio']]
                    # if cct.get_now_time_int() > 1030 and cct.get_now_time_int() < 1400:
                        # top_all = top_all[(top_all.volume > ct.VolumeMinR) & (top_all.volume < ct.VolumeMaxR)]

                # top_all = top_all.sort_values(by=[ 'couts', 'dff','volume', 'ratio'], ascending=[0, 0, 0, 1])
                top_all = top_all.sort_values(
                    by=ct.Monitor_sort_count, ascending=[0, 0, 0, 0, 1])
                # top_all = top_all.sort_values(by=[ 'couts'], ascending=[0])
                # top_all=top_all.sort_values(by=['dff','percent','couts','ratio'],ascending=[0,0,1,1])

                # top_all=top_all.sort_values(by=['dff','couts'],ascending=[0,0])
                # top_all=top_all.sort_values(by=['dff','percent','couts','ratio'],ascending=[0,0,1,1])

                # print top_all
                # print pt.PrettyTable([''] + list(top_all.columns))
                # print tbl.tabulate(top_all,headers='keys', tablefmt='psql')
                # print tbl.tabulate(top_all,headers='keys', tablefmt='orgtbl')
                # print cct.format_for_print(top_all)
                # print top_all[:10]

                top_temp = stf.filterPowerCount(top_all, ct.PowerCount)
                top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl)
                goldstock = len(top_all[(
                    top_all.buy >= top_all.lhigh * 0.99) & (top_all.buy >= top_all.llastp * 0.99)])
                # print "G:%s Rt:%0.1f dT:%s N:%s" % (len(top_all),float(time.time() -
                # time_Rt),cct.get_time_to_date(time_s),cct.get_now_time())
                cct.set_console(width, height,
                                title=['dT:%s' % cct.get_time_to_date(time_s), 'G:%s' % len(top_all), 'zxg: %s' % (blkname + '-' + market_blk)])

                top_all = tdd.get_powerdf_to_all(top_all, top_temp)
                top_temp = stf.getBollFilter(df=top_temp, boll=1)
                print "G:%s Rt:%0.1f dT:%s N:%s T:%s" % (goldstock, float(time.time() - time_Rt), cct.get_time_to_date(time_s), cct.get_now_time(), len(top_temp))
                if 'op' in top_temp.columns:
                    # top_temp = top_temp.sort_values(by=['ra','op','couts'],ascending=[0, 0,0])
                    # top_temp = top_temp.sort_values(by=['dff', 'op', 'ra', 'percent', 'ratio'],
                    # top_temp = top_temp.sort_values(by=ct.Monitor_sort_op,
                                    # ascending=ct.Monitor_sort_op_key)
                    # top_temp = top_temp.sort_values(by=ct.Duration_percentdn_ra,
                                    # ascending=ct.Duration_percentdn_ra_key)
                    # top_temp = top_temp.sort_values(by=ct.Duration_percent_op,
                    #                 ascending=ct.Duration_percent_op_key)
                    top_temp = top_temp.sort_values(by=(market_sort_value),
                                                    ascending=market_sort_value_key)
                    # top_temp = top_temp.sort_values(by=['op','ra','dff', 'percent', 'ratio'], ascending=[0,0,0, 0, 1])
                # if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 935:
                #     top_temp = top_temp.loc[:,ct.Monitor_format_trade]
                # else:
                #     top_temp = top_temp.loc[:,ct.Monitor_format_trade]
                ct_MonitorMarket_Values = ct.get_Duration_format_Values(
                    ct.Monitor_format_trade, market_sort_value[:2])
                print cct.format_for_print(top_temp.loc[:, ct_MonitorMarket_Values][:10])

                # print cct.format_for_print(top_all[:10])
                if status:
                    for code in top_all[:10].index:
                        code = re.findall('(\d+)', code)
                        if len(code) > 0:
                            code = code[0]
                            kind = sl.get_multiday_ave_compare_silent(code)
            else:
                # print top_now[:10]
                print "\tNo data"
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
                        cct.sleeprandom(60)
                        top_all = pd.DataFrame()
                        time_s = time.time()
                        print "."
                        break
            else:
                raise KeyboardInterrupt("StopTime")

        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # success+=1
            # cct.sleep(1)
            # if success > 3:
            # st=raw_input("status:[go(g),clear(c),quit(q,e)]:")
            st = cct.cct_raw_input(ct.RawMenuArgmain() % (market_sort_value))

            if len(st) == 0:
                status = False
            elif (len(st.split()[0]) == 1 and st.split()[0].isdigit()) or st.split()[0].startswith('x'):
                st_l = st.split()
                st_k = st_l[0]
                if st_k in ct.Market_sort_idx.keys() and len(top_all) > 0:
                    st_key_sort = st
                    market_sort_value, market_sort_value_key = ct.get_market_sort_value_key(
                        st_key_sort, top_all=top_all)
                else:
                    log.error("market_sort key error:%s" % (st))
                    cct.sleeprandom(5)

            # elif st.startswith('d') or st.startswith('dt'):
            #     # dl = st.split()
            #     args = parserDuraton.parse_args(st.split()[1:])
            #     if len(str(args.start)) > 0:
            #         end_date=args.end
            #         duration_date=args.start
            #         if len(str(duration_date)) < 4:
            #             du_date = tdd.get_duration_Index_date('999999',dl=int(duration_date))
            #             # print duration_date
            #             ct.PowerCountdl = duration_date
            #         set_duration_console(du_date)
            #         time_s = time.time()
            #         status = False
            #         top_all = pd.DataFrame()
            #         lastpTDX_DF = pd.DataFrame()

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
                sys.exit(0)
            else:
                print "input error:%s" % (st)

        except (IOError, EOFError) as e:
            print "Error", e
            import traceback
            traceback.print_exc()
            cct.sleeprandom(ct.duration_sleep_time / 2)
            # raw_input("Except")

            # http://stackoverflow.com/questions/17709270/i-want-to-create-a-column-of-value-count-in-my-pandas-dataframe
            # df['couts'] = df.groupby(['Color'])['Value'].transform('count')
            #
            # For example,
            #
            # In [102]: df = pd.DataFrame({'Color': 'Red Red Blue'.split(), 'Value': [100, 150, 50]})
            #
            # In [103]: df
            # Out[103]:
            #   Color  Value
            # 0   Red    100
            # 1   Red    150
            # 2  Blue     50
            #
            # In [104]: df['couts'] = df.groupby(['Color'])['Value'].transform('count')
            #
            # In [105]: df
            # Out[105]:
            #   Color  Value  count
            # 0   Red    100       2
            # 1   Red    150       2
            # 2  Blue     50       1
            #
            # Note that transform('count') ignores NaNs. If you want to count NaNs, use transform(len)
