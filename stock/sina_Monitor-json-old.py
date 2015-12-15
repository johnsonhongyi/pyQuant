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
import real_data

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
    type = '2'
    code_a = []
    def get_code_g():
        start_t = time.time()
        data = real_data.get_sina_all_json_dd(vol,type)
        interval = (time.time() - start_t)
        df = data[(data['kind'] == 'U')]['code'].value_counts()[:10]
        # print ""
        print "interval:", interval
        print df
        code_g = []
        for code in df.index:
            code = re.findall('(\d+)', code)
            if len(code) > 0:
                code = code[0]
                status = sl.get_multiday_ave_compare_silent(code)
                if status:
                    code_g.append(code)
        return code_g


    while 1:
        try:
            cd = get_code_g()
            if len(code_a) == 0:
                code_a = cd
            else:
                for code in cd:
                    if code in cd:
                        print "duble:code%s", code
                    else:
                        code_a.append(code)
            time.sleep(60)



        except (IOError, EOFError, KeyboardInterrupt) as e:
            # print "key"
            print "expect:", e
            status = not status
            code_a = []
