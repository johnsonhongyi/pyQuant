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
import realdatajson

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


if __name__ == "__main__":

    status=True
    vol = '0'
    type = '4'
    top_now=pd.DataFrame()
    code_a={}
    def get_code_g():
        start_t = time.time()
        df = realdatajson.get_sina_all_json_dd(vol,type)
        interval = (time.time() - start_t)
        # print type(data)
        # print data
        code_g = {}
        if len(df) >=1:
            # return []
            # df = data
            # df['count'] = data[(data['kind'] == 'U')]['code'].value_counts()
            # print(len(df))
            df['counts']=df.groupby(['code'])['code'].transform('count')
            df=df[(df['kind'] == 'U')]
            df=df.sort_values(by='counts',ascending=0)
            df=df.drop_duplicates('code')[:10]
            df=df.set_index('code')
            # print len(data),len(df)
            print "interval:", interval
            print df.iloc[0:,0:1]
            for ix in df.index:
                # print (df.iloc[i,0])
                code = re.findall('(\d+)', ix)
                # print "code",code
                if len(code) > 0:
                    code = code[0]
                    status = sl.get_multiday_ave_compare_silent(code)
                    if status:
                        code_g[code]= df.loc[ix].values
        return code_g


    while 1:
        try:
            cd = get_code_g()
            if len(code_a) == 0:
                code_a = cd
            else:
                for code in cd.keys():
                    if code in code_a.keys():
                        print "duble:code%s %s"%(code,cd[code])
                    else:
                        code_a[code]=cd[code]
            time.sleep(60)



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