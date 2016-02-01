# -*- coding:utf-8 -*-
# !/usr/bin/env python


# import sys
#
# reload(sys)
#
# sys.setdefaultencoding('utf-8')

import re
import sys
import time
# import urllib2

# from pandas import DataFrame
import pandas as pd
import JohhnsonUtil.johnson_cons as ct
import JohhnsonUtil.commonTips as cct
import singleAnalyseUtil as sl
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd
from JohhnsonUtil import LoggerFactory as LoggerFactory
import gc

log = LoggerFactory.getLogger('SinaMonitor-Gold')

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


if __name__ == "__main__":

    cct.set_console()
    # log.setLevel(LoggerFactory.DEBUG)
    status = False
    vol = '0'
    type = '2'
    top_all = pd.DataFrame()
    code_a = {}
    success = 0
    time_s = time.time()
    # delay_time = 3600
    delay_time = cct.get_delay_time()
    base_path = tdd.get_tdx_dir()
    block_path = tdd.get_tdx_dir_blocknew() + '065.blk'
    # all_diffpath = tdd.get_tdx_dir_blocknew() + '062.blk'

    while 1:
        try:
            df = rl.get_sina_all_json_dd(vol, type)
            top_now = rl.get_sina_dd_count_price_realTime(df)
            # print type(top_now)
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
                if len(top_all) == 0:
                    top_all = top_now
                    # dd=dd.fillna(0)
                else:
                    top_now = top_now[top_now.trade >= top_now.high * 0.98]
                    for symbol in top_now.index:
                        # code = rl._symbol_to_code(symbol)
                        if symbol in top_all.index:
                            # print top_all.iloc[symbol]
                            # print top_now[symbol]
                            # if top_all.loc[symbol,'diff'] == 0:
                            # print "code:",symbol
                            count_n = top_now.loc[symbol, 'percent']
                            count_a = top_all.loc[symbol, 'percent']
                            top_now.loc[symbol, 'diff'] = count_n - count_a
                            if status_change:
                                top_all.loc[symbol] = top_now.loc[symbol]
                            else:
                                top_all.loc[symbol, ['percent', 'diff']] = top_now.loc[symbol, ['percent', 'diff']]
                                top_all.loc[symbol, 'trade':] = top_now.loc[symbol, 'trade':]
                                # if not count_n==count_a:
                                # top_now.loc[symbol,'diff']=round((count_n-count_a),1)
                                # if status_change:
                                # top_all.loc[symbol]=top_now.loc[symbol]
                                # else:
                                # top_all.loc[symbol,'diff':]=top_now.loc[symbol,'diff':]
                                # else:
                                # top_all.loc[symbol,'counts':]=top_now.loc[symbol,'counts':]

                        else:
                            top_all.append(top_now.loc[symbol])

                top_bak = top_all
                codelist = top_all.index.tolist()
                if len(codelist) > 0:
                    log.info('toTDXlist:%s' % len(codelist))
                    tdxdata = tdd.get_tdx_all_day_LastDF(codelist)
                    log.debug("TdxLastP: %s %s" % (len(tdxdata), tdxdata.columns.values))
                    tdxdata.rename(columns={'low': 'llow'}, inplace=True)
                    tdxdata.rename(columns={'high': 'lhigh'}, inplace=True)
                    tdxdata.rename(columns={'close': 'lastp'}, inplace=True)
                    tdxdata.rename(columns={'vol': 'lvol'}, inplace=True)
                    tdxdata = tdxdata.loc[:, ['llow', 'lhigh', 'lastp', 'lvol', 'date']]
                    # data.drop('amount',axis=0,inplace=True)
                    log.debug("TDX Col:%s" % tdxdata.columns.values)
                    # df_now=top_all.merge(data,on='code',how='left')
                    # df_now=pd.merge(top_all,data,left_index=True,right_index=True,how='left')
                    top_all = top_all.merge(tdxdata, left_index=True, right_index=True, how='left')
                    log.info('Top-merge_now:%s' % (top_all[:1]))
                    top_all = top_all[top_all['llow'] > 0]
                    log.info("df:%s" % top_all[:1])
                    radio_t = cct.get_work_time_ratio()
                    log.debug("Second:vol/vol/:%s" % radio_t)
                    # top_dif['volume'] = top_dif['volume'].apply(lambda x: round(x / radio_t, 1))
                    log.debug("top_diff:vol")
                    top_all['volume'] = (
                        map(lambda x, y: round(x / y / radio_t, 1), top_all['volume'].values, top_all['lvol'].values))

                    top_all = top_all[top_all.prev_p >= top_all.lhigh]
                    top_all = top_all.loc[:,
                              ['name', 'percent', 'diff', 'counts', 'volume', 'trade', 'prev_p', 'ratio']]

                print "G:%s dt:%s " % (len(top_all),cct.get_time_to_date(time_s))                
                top_all = top_all.sort_values(by=['diff', 'counts', 'volume', 'ratio'], ascending=[0, 0, 0, 1])
                # top_all=top_all.sort_values(by=['diff','percent','counts','ratio'],ascending=[0,0,1,1])

                # top_all=top_all.sort_values(by=['diff','counts'],ascending=[0,0])
                # top_all=top_all.sort_values(by=['diff','percent','counts','ratio'],ascending=[0,0,1,1])


                # print top_all
                # print pt.PrettyTable([''] + list(top_all.columns))
                # print tbl.tabulate(top_all,headers='keys', tablefmt='psql')
                # print tbl.tabulate(top_all,headers='keys', tablefmt='orgtbl')
                # print rl.format_for_print(top_all)
                # print top_all[:10]
                print rl.format_for_print(top_all[:10])
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
                        time.sleep(60)
                        if cct.get_now_time_int() < 931:
                            time.sleep(60)
                            print ".",
                        else:
                            top_all = pd.DataFrame()
                            time_s = time.time()
                            print "."
                            break
                else:
                    time.sleep(60)
            elif cct.get_work_duration():
                while 1:
                    time.sleep(60)
                    if cct.get_work_duration():
                        print ".",
                        time.sleep(60)
                    else:
                        top_all = pd.DataFrame()
                        time_s = time.time()
                        print "."
                        break
            else:
                # break
                # time.sleep(5)
                st = raw_input("status:[go(g),clear(c),quit(q,e),W(w),Wa(a)]:")
                if len(st) == 0:
                    status = False
                elif st == 'g' or st == 'go':
                    status = True
                    for code in top_all[:10].index:
                        code = re.findall('(\d+)', code)
                        if len(code) > 0:
                            code = code[0]
                            kind = sl.get_multiday_ave_compare_silent(code)
                elif st == 'clear' or st == 'c':
                    top_all = pd.DataFrame()
                    status = False
                elif st == 'w' or st == 'a':
                    codew = (top_all.index).tolist()
                    if st == 'a':
                        cct.write_to_blocknew(block_path, codew[:20])
                        # cct.write_to_blocknew(all_diffpath, codew)
                    else:
                        cct.write_to_blocknew(block_path, codew[:20], False)
                        # cct.write_to_blocknew(all_diffpath, codew, False)
                    print "wri ok:%s" % block_path
                    # time.sleep(2)
                else:
                    sys.exit(0)



        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # success+=1
            # time.sleep(1)
            # if success > 3:
            # st=raw_input("status:[go(g),clear(c),quit(q,e)]:")
            st = raw_input("status:[go(g),clear(c),quit(q,e),W(w),Wa(a)]:")

            if len(st) == 0:
                # top_all=pd.DataFrame()
                status = False
            elif st == 'g' or st == 'go':
                status = True
            elif st == 'clear' or st == 'c':
                top_all = pd.DataFrame()
                status = False
            elif st == 'w' or st == 'a':
                # base_path=r"E:\DOC\Parallels\WinTools\zd_pazq\T0002\blocknew\\"
                # block_path=base_path+'065.blk'
                # all_diffpath=base_path+'\062.blk'
                codew = top_all[:20].index.tolist()
                if st == 'a':
                    cct.write_to_blocknew(block_path, codew)
                    # cct.write_to_blocknew(all_diffpath,codew)
                else:
                    cct.write_to_blocknew(block_path, codew, False)
                    # cct.write_to_blocknew(all_diffpath,codew,False)
                print "wri ok:%s" % block_path

                # time.sleep(5)

            else:
                sys.exit(0)

        except (IOError, EOFError) as e:
            print "Error", e
            # traceback.print_exc()
            # raw_input("Except")


            # http://stackoverflow.com/questions/17709270/i-want-to-create-a-column-of-value-count-in-my-pandas-dataframe
            # df['counts'] = df.groupby(['Color'])['Value'].transform('count')
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
            # In [104]: df['counts'] = df.groupby(['Color'])['Value'].transform('count')
            #
            # In [105]: df
            # Out[105]:
            #   Color  Value  count
            # 0   Red    100       2
            # 1   Red    150       2
            # 2  Blue     50       1
            #
            # Note that transform('count') ignores NaNs. If you want to count NaNs, use transform(len)
