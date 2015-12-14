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

from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas as pd
import cons as ct
import singleAnalyseUtil as sl

import json
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


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


def get_sina_all_dd(vol='0', type='0', retry_count=3, pause=0.001):
    if len(vol) != 1 or len(type) != 1:
        return None
    else:
        print ("Vol:%s  Type:%s" % (ct.DD_VOL_List[vol], ct.DD_TYPE_List[type]))
    # symbol = _code_to_symbol(code)
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            ct._write_console()
            url = get_sina_url(vol, type)
            # url= ct.SINA_DD_VRatio % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'],ct.DD_VOL_List[vol], ct.DD_TYPE_List[type])
            page = urllib2.urlopen(url)
            html_doc = page.read()
            # print (html_doc)
            # soup = BeautifulSoup(html_doc,fromEncoding='gb18030')
            # print html_doc
            pageCount = re.findall('fillCount\"\]\((\d+)', html_doc, re.S)
            if len(pageCount) > 0:
                start_t = time.time()
                pageCount = pageCount[0]
                if int(pageCount) > 100:
                    if int(pageCount) > 10000:
                        print "BigBig:", pageCount
                        pageCount = '10000'

                    print "AllBig:", pageCount
                    html_doc = urllib2.urlopen(get_sina_url(vol, type, pageCount=pageCount)).read()
                    print (time.time() - start_t)

            soup = BeautifulSoup(html_doc, "lxml")
            print (time.time() - start_t)
            alldata = {}
            dict_data = {}
            # print soup.find_all('div',id='divListTemplate')

            row = soup.find_all('div', id='divListTemplate')
            sdata = []
            if len(row) >= 1:
                '''
                colums:CHN name

                '''
                for tag in row[0].find_all('tr', attrs={"class": True}):
                    # print tag
                    th_cells = tag.find_all('th')
                    td_cells = tag.find_all('td')
                    m_name = th_cells[0].find(text=True)
                    m_code = th_cells[1].find(text=True)
                    print m_code
                    m_time = th_cells[2].find(text=True)
                    # m_detail=(th_cells[4]).find('a')["href"]   #detail_url
                    m_price = td_cells[0].find(text=True)
                    m_vol = float(td_cells[1].find(text=True).replace(',', '')) * 100
                    m_pre_p = td_cells[2].find(text=True)
                    m_status_t = th_cells[3].find(text=True)
                    if m_status_t in ct.STATUS_DD.keys():
                        m_status = ct.STATUS_DD[m_status_t]
                        # print m_status
                    sdata.append({'code': m_code, 'time': m_time, 'vol': m_vol, 'price': m_price, 'pre_p': m_pre_p,
                                  'status': m_status, 'name': m_name})
            df = DataFrame(sdata, columns=['code', 'time', 'vol', 'price', 'pre_p', 'status', 'name'])
            # for row in soup.find_all('tr',attrs={"class":"gray","class":""}):
            return df
        except Exception as e:
            print "Except-Sina:", (e)
            traceback.print_exc()
        # else:
        #     return df
        raise IOError(ct.NETWORK_URL_ERROR_MSG)


if __name__ == "__main__":

    # get_sina_json_url()
    df=get_sina_all_json_dd(type='2')
    sys.exit(0)
    vol = '0'
    type = '2'
    code_a = []


    def get_code_g():
        start_t = time.time()
        data = get_sina_all_dd(vol, type)
        interval = (time.time() - start_t)
        df = data[(data['status'] == 'up')]['code'].value_counts()[:8]
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
