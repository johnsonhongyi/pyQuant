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
import traceback
# import urllib2

# from pandas import DataFrame
import pandas as pd
import johnson_cons as ct
import singleAnalyseUtil as sl
import realdatajson as rl
import types
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

    status=True
    vol = '0'
    type = '3'
    top_all=pd.DataFrame()
    code_a={}
    while 1:
        try:
            top_now = rl.get_json_dd_code_realTime(vol,type)
            # print type(top_now)
            if len(top_now)>10:
                if len(top_all) == 0:
                    top_all = top_now
                    # dd=dd.fillna(0)
                else:
                    for symbol in top_now.index:

                        # code = rl._symbol_to_code(symbol)
                        if symbol in top_all.index :
                            # if top_all.loc[symbol,'diff'] == 0:
                            # print "code:",symbol
                            # print top_now.loc[symbol,'counts']
                            # print top_all.loc[symbol,'counts']
                            top_all.loc[symbol,'diff']=top_now.loc[symbol,'counts']-top_all.loc[symbol,'counts']
                            # else:
                                # value=top_all.loc[symbol,'diff']

                        else:
                            top_all.append(top_now.loc[symbol])
                top_all=top_all.sort_values(by=['diff','counts'],ascending=[0,0])
                # print top_all
                # print pt.PrettyTable([''] + list(top_all.columns))
                # print tbl.tabulate(top_all,headers='keys', tablefmt='psql')
                # print tbl.tabulate(top_all,headers='keys', tablefmt='orgtbl')
                # print rl.format_for_print(top_all)
                # print top_all[:10]
                print rl.format_for_print(top_all[:10])
            else:
                print top_now
                print "no data"
            time.sleep(90)



        except (IOError, EOFError, KeyboardInterrupt) as e:
            # print "key"
            print "expect:", e
            status = not status
            code_a = []
    # http://stackoverflow.com/questions/17709270/i-want-to-create-a-column-of-value-counts-in-my-pandas-dataframe
# df['Counts'] = df.groupby(['Color'])['Value'].transform('count')
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
# In [104]: df['Counts'] = df.groupby(['Color'])['Value'].transform('count')
#
# In [105]: df
# Out[105]:
#   Color  Value  Counts
# 0   Red    100       2
# 1   Red    150       2
# 2  Blue     50       1
#
# Note that transform('count') ignores NaNs. If you want to count NaNs, use transform(len)