# -*- coding:utf-8 -*-
"""
交易数据接口 
Created on 2014/07/31
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
"""
from __future__ import division

import json
import math
import time

import lxml.html
import pandas as pd
from lxml import etree
from pandas.compat import StringIO

import stock.JohhnsonUtil.johnson_cons as ct

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

from stock.JohhnsonUtil.LoggerFactory import *

log=getLogger('Realdata')

from stock.JSONData.prettytable import *

def set_default_encode(code='utf-8'):
        import sys
        reload(sys)
        sys.setdefaultencoding(code)
        print (sys.getdefaultencoding())
        print (sys.stdout.encoding)


# print pt.PrettyTable([''] + list(df.columns))
def format_for_print(df):
    table = PrettyTable([''] + list(df.columns))
    for row in df.itertuples():
        table.add_row(row)
    return str(table)


def format_for_print2(df):
    table = PrettyTable(list(df.columns))
    for row in df.itertuples():
        table.add_row(row[1:])
    return str(table)


def _parsing_Market_price_json(url):
    """
           处理当日行情分页数据，格式为json
     Parameters
     ------
        pageNum:页码
     return
     -------
        DataFrame 当日所有股票交易数据(DataFrame)
    """
    # ct._write_console()
    # url="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=50&sort=changepercent&asc=0&node=sh_a&symbol="
    # request = Request(ct.SINA_DAY_PRICE_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
    #                              ct.PAGES['jv'], pageNum))
    request = Request(url)
    text = urlopen(request, timeout=10).read()
    if text == 'null':
        return None
    reg = re.compile(r'\,(.*?)\:')
    text = reg.sub(r',"\1":', text.decode('gbk') if ct.PY3 else text)
    text = text.replace('"{symbol', '{"symbol')
    text = text.replace('{symbol', '{"symbol"')
    text = text.replace('changepercent', 'percent')
    text = text.replace('turnoverratio', 'ratio')
    # print text
    if ct.PY3:
        jstr = json.dumps(text)
    else:
        jstr = json.dumps(text, encoding='GBK')
    js = json.loads(jstr)
    # print js
    # df = pd.DataFrame(pd.read_json(js, dtype={'code':object}),columns=ct.MARKET_COLUMNS)
    # log.debug("Market json:%s"%js[:280])
    df = pd.DataFrame(pd.read_json(js, dtype={'code': object}),
                      columns=ct.SINA_Market_COLUMNS)
    # print df[:1]
    # df = df.drop('symbol', axis=1)
    df = df.ix[df.volume >= 0]
    # print type(df)
    # print df[:1],len(df.index)
    return df


def _get_sina_Market_url(market='sh_a', count=None, num='1000'):
    if count == None:
        url = ct.JSON_Market_Center_CountURL % (market)
        # print url
        data = cct.get_url_data(url)
        # print data
        count = re.findall('(\d+)', data, re.S)
        urllist = []

        if len(count) > 0:
            count = count[0]
            if int(count) >= int(num):
                page_count = int(math.ceil(int(count) / int(num)))
                for page in range(1, page_count + 1):
                    # print page
                    url = ct.JSON_Market_Center_RealURL % (page, num, market)
                    # print "url",url
                    urllist.append(url)

            else:
                url = ct.JSON_Market_Center_RealURL % ('1', count, market)
                urllist.append(url)
    # print "%s count: %s"%(market,count),

    # print urllist[0],
    return urllist


def get_sina_Market_json(market='sh_a',showtime=True,num='2000', retry_count=3, pause=0.001):
    start_t = time.time()
    # url="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=50&sort=changepercent&asc=0&node=sh_a&symbol="
    # SINA_REAL_PRICE_DD = '%s%s/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=%s&sort=changepercent&asc=0&node=%s&symbol=%s'
    """
        一次性获取最近一个日交易日所有股票的交易数据
    return
    -------
      DataFrame
           属性：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率
    """
    # ct._write_head()
    if market=='all':
        url_list=[]
        for m in ct.SINA_Market_KEY.values():
            list=_get_sina_Market_url(m, num=num)
            for l in list:url_list.append(l)
        # print url_list
    else:
        url_list=_get_sina_Market_url(ct.SINA_Market_KEY[market], num=num)

    # print url_list
    # print "url:",url_list
    df = pd.DataFrame()
    # data['code'] = symbol
    # df = df.append(data, ignore_index=True)

    results = cct.to_mp_run(_parsing_Market_price_json, url_list)

    if len(results)>0:
        df = df.append(results, ignore_index=True)
        df['volume']= df['volume'].apply(lambda x:x/100)
        df['ratio']=df['ratio'].apply(lambda x:round(x,1))
        df['percent']=df['percent'].apply(lambda x:round(x,1))
        df=df.drop_duplicates()
        # print df[:1]
    # for url in url_list:
    #     # print url
    #     data = _parsing_Market_price_json(url)
    #     # print data[:1]
    #     df = df.append(data, ignore_index=True)
    #     # break

    if df is not None:
        # for i in range(2, ct.PAGE_NUM[0]):
        #     newdf = _parsing_dayprice_json(i)
        #     df = df.append(newdf, ignore_index=True)
        # print len(df.index)
        if showtime: print ("Market-df:%s time: %s" % (format((time.time() - start_t), '.1f'), cct.get_now_time()))
        # print type(df)
        return df
    else:
        if showtime:print ("no data Market-df:%s" % (format((time.time() - start_t), '.2f')))
        return []


def _get_sina_json_dd_url(vol='0', type='3', num='10000', count=None):
    urllist = []
    if count == None:
        url = ct.JSON_DD_CountURL % (ct.DD_VOL_List[vol], type)
        # print url
        data = cct.get_url_data(url)
        # return []
        # print data.find('abc')
        count = re.findall('(\d+)', data, re.S)
        if len(count) > 0:
            count = count[0]
            print ("Big:%s"%(count)),
            if int(count) >= int(num):
                page_count = int(math.ceil(int(count) / int(num)))
                for page in range(1, page_count + 1):
                    # print page
                    url = ct.JSON_DD_Data_URL_Page % ('10000', page, ct.DD_VOL_List[vol], type)
                    urllist.append(url)
            else:
                url = ct.JSON_DD_Data_URL_Page % (count, '1', ct.DD_VOL_List[vol], type)
                urllist.append(url)
    else:
        url = ct.JSON_DD_CountURL % (ct.DD_VOL_List[vol], type)
        # print url
        data = cct.get_url_data(url)
        # print data
        count_now = re.findall('(\d+)', data, re.S)
        urllist = []
        if count < count_now:
            count_diff = int(count_now) - int(count)
            if int(math.ceil(int(count_diff) / 10000)) >= 1:
                page_start = int(math.ceil(int(count) / 10000))
                page_end = int(math.ceil(int(count_now) / 10000))
                for page in range(page_start, page_end + 1):
                    # print page
                    url = ct.JSON_DD_Data_URL_Page % ('10000', page, ct.DD_VOL_List[vol], type)
                    urllist.append(url)
            else:
                page = int(math.ceil(int(count_now) / 10000))
                url = ct.JSON_DD_Data_URL_Page % ('10000', page, ct.DD_VOL_List[vol], type)
                urllist.append(url)
    # print "url:",urllist[:0]
    return urllist





def _parsing_sina_dd_price_json(url):
    """
           处理当日行情分页数据，格式为json
     Parameters
     ------
        pageNum:页码
     return
     -------
        DataFrame 当日所有股票交易数据(DataFrame)
    """
    ct._write_console()
    # request = Request(ct.SINA_DAY_PRICE_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
    #                              ct.PAGES['jv'], pageNum))
    # request = Request(url)
    # text = urlopen(request, timeout=10).read()
    text = cct.get_url_data(url)
    if len(text) < 10:
        return ''
    reg = re.compile(r'\,(.*?)\:')
    text = reg.sub(r',"\1":', text.decode('gbk') if ct.PY3 else text)
    text = text.replace('"{symbol', '{"code')
    text = text.replace('{symbol', '{"code"')

    if ct.PY3:
        jstr = json.dumps(text)
    else:
        jstr = json.dumps(text, encoding='GBK')
    js = json.loads(jstr)
    df = pd.DataFrame(pd.read_json(js, dtype={'code': object}),
                      columns=ct.DAY_REAL_DD_COLUMNS)
    df = df.drop('symbol', axis=1)
    df = df.ix[df.volume > 0]
    # print ""
    # print df['name'][len(df.index)-1:],len(df.index)
    return df


def get_sina_all_json_dd(vol='0', type='3', num='10000', retry_count=3, pause=0.001):
    start_t = time.time()
    # url="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=50&sort=changepercent&asc=0&node=sh_a&symbol="
    # SINA_REAL_PRICE_DD = '%s%s/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=%s&sort=changepercent&asc=0&node=%s&symbol=%s'
    """
        一次性获取最近一个日交易日所有股票的交易数据
    return
    -------
      DataFrame
           属性：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率
    """
    # ct._write_head()
    url_list = _get_sina_json_dd_url(vol, type, num)
    df = pd.DataFrame()
    # data['code'] = symbol
    # df = df.append(data, ignore_index=True)

    data = cct.to_mp_run(_parsing_sina_dd_price_json, url_list)
    # data='null'
    # print len('null')
    # print len(data)
    if len(data)>0:
        df = df.append(data, ignore_index=True)
    # print "df",df.empty
    # for url in url_list:
    #     # print url
    #     data = _parsing_sina_dd_price_json(url)
    #     df=df.append(data,ignore_index=True)

    if not df.empty:
        # for i in range(2, ct.PAGE_NUM[0]):
        #     newdf = _parsing_dayprice_json(i)
        #     df = df.append(newdf, ignore_index=True)
        # print len(df.index)
        print (" json-df: %0.2f"%((time.time() - start_t))),
        return df
    else:
        print
        print ("no data  json-df: %0.2f"%((time.time() - start_t)))
        return ''


def _today_ticks(symbol, tdate, pageNo, retry_count, pause):
    ct._write_console()
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            html = lxml.html.parse(ct.TODAY_TICKS_URL % (ct.P_TYPE['http'],
                                                         ct.DOMAINS['vsf'], ct.PAGES['t_ticks'],
                                                         symbol, tdate, pageNo
                                                         ))
            res = html.xpath('//table[@id=\"datatbl\"]/tbody/tr')
            if ct.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>' % sarr
            sarr = sarr.replace('--', '0')
            df = pd.read_html(StringIO(sarr), parse_dates=False)[0]
            df.columns = ct.TODAY_TICK_COLUMNS
            df['pchange'] = df['pchange'].map(lambda x: x.replace('%', ''))
        except Exception as e:
            print(e)
        else:
            return df
    raise IOError(ct.NETWORK_URL_ERROR_MSG)


def _get_index_url(index, code, qt):
    if index:
        url = ct.HIST_INDEX_URL % (ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                                   code, qt[0], qt[1])
    else:
        url = ct.HIST_FQ_URL % (ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                                code, qt[0], qt[1])
    return url


def _get_hists(symbols, start=None, end=None,
               ktype='D', retry_count=3,
               pause=0.001):
    """
    批量获取历史行情数据，具体参数和返回数据类型请参考get_hist_data接口
    """
    df = pd.DataFrame()
    if isinstance(symbols, list) or isinstance(symbols, set) or isinstance(symbols, tuple) or isinstance(symbols,
                                                                                                         pd.Series):
        for symbol in symbols:
            data = get_hist_data(symbol, start=start, end=end,
                                 ktype=ktype, retry_count=retry_count,
                                 pause=pause)
            data['code'] = symbol
            df = df.append(data, ignore_index=True)
        return df
    else:
        return None

def get_sina_dd_count_price_realTime(df='',mtype='all'):
    '''
    input df count and merge price to df
    '''
    if len(df)==0:
        df = get_sina_all_json_dd('0','4')
    if len(df)>0:
        df['counts']=df.groupby(['code'])['code'].transform('count')
        # df=df[(df['kind'] == 'U')]
        df=df.sort_values(by='counts',ascending=0)
        df=df.drop_duplicates('code')
        # df=df[df.price >df.prev_price]
        df=df.loc[:,['code','name','counts']]
        # dz.loc['sh600110','counts']=dz.loc['sh600110'].values[1]+3
        df=df.set_index('code')
        df=df.iloc[0:,0:2]
        df['diff']=0

        dp=get_sina_Market_json(mtype)
        if len(dp)>10:
            dp=dp.dropna('index')
            dp=dp.drop_duplicates('code')
            dm=pd.merge(df,dp,on='name',how='left')
            # dm=dm.drop_duplicates('code')
            dm=dm.set_index('code')
            dm=dm.dropna('index')
            dm.loc[dm.percent>9.9,'percent']=10
            # print dm[-1:]
            dm=dm.loc[:,ct.SINA_DD_Clean_Count_Columns]
            # print dm[-1:]
        else:
            dm=df
    else:
        dm=''
    return dm
def get_sina_tick_js_LastPrice(symbols):
    symbols_list=''
    if len(symbols) == 0:
        return ''
    if isinstance(symbols, list) or isinstance(symbols, set) or isinstance(symbols, tuple) or isinstance(symbols, pd.Series):
        for code in symbols:
            symbols_list += cct.code_to_symbol(code) + ','
    else:
        symbols_list = cct.code_to_symbol(symbols)
    # print symbol_str
    url="http://hq.sinajs.cn/list=%s"%(symbols_list)
    # print url
    data = cct.get_url_data(url)
    # vollist=re.findall('{data:(\d+)',code)
    # print data
    ulist=data.split(";")
    price_dict={}
    for var in range(0,len(ulist)-1):
        # print var
        if len(ulist)==2:
            code=symbols
        else:
            code=symbols[var]
        tempData = re.search('''(")(.+)(")''', ulist[var]).group(2)
        stockInfo = tempData.split(",")
        # stockName   = stockInfo[0]  #名称
        # stockStart  = stockInfo[1]  #开盘
        stockLastEnd= stockInfo[2]  #昨收盘
        # stockCur    = stockInfo[3]  #当前
        # stockMax    = stockInfo[4]  #最高
        # stockMin    = stockInfo[5]  #最低
        # price_dict[code]=stockLastEnd
        price_dict[code]=float(stockLastEnd)

        # stockUp     = round(float(stockCur) - float(stockLastEnd), 2)
        # stockRange  = round(float(stockUp) / float(stockLastEnd), 4) * 100
        # stockVolume = round(float(stockInfo[8]) / (100 * 10000), 2)
        # stockMoney  = round(float(stockInfo[9]) / (100000000), 2)
        # stockTime   = stockInfo[31]
        # dd={}
    return price_dict


# def get_sina_tick_jscct.code(code):
#     symbol=cct.code_to_symbol(code)
#     url="http://hq.sinajs.cn/list=%s"%(symbol)
#     data=sl.get_url_data(url)
#     # vollist=re.findall('{data:(\d+)',code)
#     tempData = re.search('''(")(.+)(")''', data).group(2)
#     stockInfo = tempData.split(",")
#     # stockName   = stockInfo[0]  #名称
#     # stockStart  = stockInfo[1]  #开盘
#     stockLastEnd= stockInfo[2]  #昨收盘
#     # stockCur    = stockInfo[3]  #当前
#     # stockMax    = stockInfo[4]  #最高
#     # stockMin    = stockInfo[5]  #最低
#     # stockUp     = round(float(stockCur) - float(stockLastEnd), 2)
#     # stockRange  = round(float(stockUp) / float(stockLastEnd), 4) * 100
#     # stockVolume = round(float(stockInfo[8]) / (100 * 10000), 2)
#     # stockMoney  = round(float(stockInfo[9]) / (100000000), 2)
#     # stockTime   = stockInfo[31]
#     '''
#     http://hq.sinajs.cn/list=sz002399,sh601919
#     '''
#     return stockLastEnd

def get_market_LastPrice_sina_js(codeList):
    # time_s=time.time()
    if isinstance(codeList, list) or isinstance(codeList, set) or isinstance(codeList, tuple) or isinstance(codeList, pd.Series):
        if len(codeList)>200:
            # num=int(len(codeList)/cpu_count())
            div_list = cct.get_div_list(codeList, 100)
            # print "ti:",time.time()-time_s
            results = cct.to_mp_run(get_sina_tick_js_LastPrice, div_list)
            # print results
        else:
            results=get_sina_tick_js_LastPrice(codeList)
        # print "time:",time.time()-time_s
        return results
    else:
        print "codeL not list"
        # return get_sina_tick_js_LastPrice(codeList)

# 'code': code, 'date':get_today() , 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
#              'vol'


# def get_market_LastPrice_TDX(market='all'):
#         time_s=time.time()
#         results=to_mp_run(tdd.get_tdx_all_day_LastDF,market)
#         print "timeTDX:",time.time()-time_s
#         return results
#     else:
#         print "codeL not list"

def get_market_price_sina_dd_realTime(dp='',vol='0',type='3'):
    '''
    input df count and merge price to df
    '''

    if len(dp)==0:
            dp=get_sina_Market_json()
    if len(dp)>10:
        # df=df.dropna('index')
        # df=df.drop_duplicates('code')
        # dm=pd.merge(df,dp,on='name',how='left')
        # print(type(dp))
        dp=dp.drop_duplicates('code')
        log.info("Market_realTime:%s"%len(dp))
        # dp=dp.set_index('code')
        dp=dp.dropna('index')
        # dp=dp.loc[:,'trade':].astype(float)
        log.debug("DP:%s" % dp[:1])
        if dp[:1].buy.values <> 0 and dp[:1].percent.values == 0 and dp[:1].close.values <> 0:
            dp['percent'] = (map(lambda x, y: round((x - y) / y * 100, 1), dp['buy'].values, dp['close'].values))

        dp.loc[dp.percent>9.9,'percent']=10
        dp['diff']=0
        df=get_sina_all_json_dd(vol,type)
        if len(df)>10:
            # df['counts']=0
            df['counts']=df.groupby(['code'])['code'].transform('count')
            # df=df[(df['kind'] == 'U')]
            df=df.sort_values(by='counts',ascending=0)
            df=df.drop_duplicates('code')
            # df=df[df.price >df.prev_price]
            df=df.loc[:,['name','counts','kind']]
            # print df[df.counts>0][:2]
            dm=pd.merge(dp,df,on='name',how='left')
            log.info("dmMerge:%s"%dm[:1])
            # print dm[dm.counts>0][:2]
            dm.counts=dm.counts.fillna(0)
            dm.counts=dm.counts.astype(int)
            dm=dm.drop_duplicates('code')
            dm=dm.set_index('code')
            # print dm.sort_values(by=['counts','percent','diff','ratio'],ascending=[0,0,0,1])[:2]
            # dm=dm.fillna(int(0))
            # dm.ratio=dm.ratio
            dm=dm.loc[:,ct.SINA_Market_Clean_UP_Columns]

        else:
            dp=dp.set_index('code')
            dm=dp.loc[:,ct.SINA_Market_Clean_Columns]
                    # ['name','buy','diff','percent','ratio','high','open','volume','low','counts']
                    #['name','buy','diff','percent','trade','high','ratio','volume','counts']

    else:
        dm=''
    # print type(dm)
    return dm




if __name__ == '__main__':
    # df = get_sina_all_json_dd('0', '3')
    df=get_sina_Market_json('all')
    print len(df)
    # df=get_market_price_sina_dd_realTime(df,'0','1')
    # df=get_sina_dd_count_price_realTime()
    # df=df.drop_duplicates('code')
    # df=df.set_index('code')
    # _write_to_csv(df,'readdata3')
    # print ""
    # print format_for_print(df[:10])
    # print df[df.index=='601919']
    # print len(df)
    # print "\033[1;37;4%dm%s\033[0m" % (1 > 0 and 1 or 2, get_sina_tick_jscct.code('002399'))
    # print get_sina_tick_js_LastPrice('002399')
    # print "ra:",sl.get_work_time_ratio()
    # dd = get_sina_tick_js_LastPrice(['002399','002399','601919','601198'])
    # print(type(dd))
    import sys

    sys.exit(0)
    # up= df[df['trade']>df['settlement']]
    # print up[:2]
    # df=get_sina_all_json_dd(type='3')
    # print df[:10]
    # df=get_sina_Market_url()
    # for x in df:print ":",x
    df = pd.DataFrame()
    # dz=get_sina_Market_json('sz_a')
    # ds=get_sina_Market_json('sh_a')
    dc = get_sina_Market_json('all')
    # df=df.append(dz,ignore_index=True)
    # df=df.append(ds,ignore_index=True)
    df = df.append(dc, ignore_index=True)
    # df=df[df['changepercent']<5]
    # df = df[df['changepercent'] > 0.2]

    # dd=df[(df['open'] <= df['low']) ]
    # dd=df[(df['open'] <= df['low']) ]
    print df[:2], len(df.index)
    # da[da['changepercent']<9.9].
    # dd=df[(df['open'] <= df['low']) ]
    # dd=df[(df['open'] <= df['low']) ]
    # dd[dd['trade'] >= dd['high']*0.99]
    # sys.exit(0)
