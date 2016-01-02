# -*- coding:utf-8 -*-
# SINA_DD_VRatio_10 = '%s%s/quotes_service/view/%s?num=100&page=1&sort=ticktime&asc=0&volume=0&type=%s'
# # SINA_DD_VRatio_10 = 'http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=0&type=2'
# INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb']
# INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sz399300',
#               'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006'}
# P_TYPE = {'http': 'http://', 'ftp': 'ftp://'}

import time

import lxml.html
import pandas as pd
from lxml import etree
from pandas.compat import StringIO

from stock.JohhnsonUtil import johnson_cons as ct

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


# def _code_to_symbol(code):
#     """
#         生成symbol代码标志
#     """
#     if code in ct.INDEX_LABELS:
#         return ct.INDEX_LIST[code]
#     else:
#         if len(code) != 6 :
#             return ''
#         else:
#             return 'sh%s'%code if code[:1] in ['5', '6', '9'] else 'sz%s'%code

def get_sina_code_dd(code=None, date=None, retry_count=3, pause=0.001):
    """
        获取sina大单数据
    Parameters
    ------
        code:string
                  股票代码 e.g. 600848
        date:string
                  日期 format：YYYY-MM-DD
        retry_count : int, 默认 3
                  如遇网络等问题重复执行的次数
        pause : int, 默认 0
                 重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
     return
     -------
        DataFrame 当日所有股票交易数据(DataFrame)
              属性:股票代码    股票名称    交易时间    价格    成交量    前一笔价格    类型（买、卖、中性盘）
    """

    if code is None or len(code) != 6:
        return None
    symbol = _code_to_symbol(code)
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            if date == None:
                re = Request(ct.SINA_DD_Now % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd'],
                                               symbol))
            else:
                re = Request(ct.SINA_DD % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd'],
                                           symbol, date))
            lines = urlopen(re, timeout=10).read()
            lines = lines.decode('GBK')
            if len(lines) < 100:
                return None
            df = pd.read_csv(StringIO(lines), names=ct.SINA_DD_COLS,
                             skiprows=[0])
            if df is not None:
                df['code'] = df['code'].map(lambda x: x[2:])
        except Exception as e:
            print(e)
        else:
            return df
    raise IOError(ct.NETWORK_URL_ERROR_MSG)


def get_sina_all_dd(vol='0', type='0', retry_count=3, pause=0.001):
    """
        获取sina全部大单数据
    Parameters
    ------
        volume:string
                  股票代码 e.g. 0=400,1=1k,2=2k,3=5k,4=1w
        type:string
                  日期 e.g. 0=5T,1=10,2=20,3=50,4=100T
        retry_count : int, 默认 3
                  如遇网络等问题重复执行的次数
        pause : int, 默认 0
                 重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
     return
     -------
        DataFrame 当日所有股票交易数据(DataFrame)
              属性:股票代码    股票名称    交易时间    价格    成交量    前一笔价格    类型（买、卖、中性盘）
    """
    if len(vol) != 1 or len(type) != 1:
        return None
    # symbol = _code_to_symbol(code)
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            ct._write_console()
            print (ct.DD_VOL_List[vol], ct.DD_TYPE_List[type])
            # print(ct.SINA_DD_VRatio % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'],
                                              # ct.DD_VOL_List[vol], ct.DD_TYPE_List[type]))
            print ct.SINA_DD_VRatio % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'],ct.DD_VOL_List[vol], ct.DD_TYPE_List[type])
            html = lxml.html.parse(ct.SINA_DD_VRatio % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'],
                                              ct.DD_VOL_List[vol], ct.DD_TYPE_List[type]))
            # else:
            #     re = Request(ct.SINA_DD % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd'],
            #                                symbol, date))
            # lines = urlopen(re, timeout=10).read()
            # lines = lines.decode('GBK')
            # if len(lines) < 100:
            #     return None
            # df = pd.read_csv(StringIO(lines), names=ct.SINA_DD_COLS,
            #                  skiprows=[0])
            # parser = etree.HTMLParser()
            # //div[@class="main"]/div[@class="divList"]/table/tbody/tr
            # //div[@class="main"]/div[@id="divListTemplate"]/table/tbody/tr
            # tree= etree.parse(StringIO.StringIO(html), parser)
            res = html.xpath('//div[@class="main"]/div[@id="divListTemplate"]/table/tbody/tr')
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
                print sarr
            # sarr = ''.join(sarr)
            # sarr = '<table>%s</table>'%sarr
            # sarr = sarr.replace('--', '0')
            # df = pd.read_html(StringIO(sarr), parse_dates=False)[0]
            # df.columns = ct.TODAY_TICK_COLUMNS
            # df['pchange'] = df['pchange'].map(lambda x : x.replace('%', ''))
            df=None
            # if df is not None:
            #     df['code'] = df['code'].map(lambda x: x[2:])
        except Exception as e:
            print(e)
        else:
            return df
    raise IOError(ct.NETWORK_URL_ERROR_MSG)


if __name__ == '__main__':
    # code = '601198'
    # date = 'now'

    df = get_sina_all_dd()
    print (df)
