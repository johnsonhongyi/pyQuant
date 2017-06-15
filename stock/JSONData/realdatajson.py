# -*- coding:utf8 -*-
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
import re
import sys
import time

import lxml.html
import pandas as pd
from lxml import etree
from pandas.compat import StringIO
sys.path.append("..")
import JohhnsonUtil.johnson_cons as ct
from JohhnsonUtil import LoggerFactory
from JSONData.prettytable import *
from JohhnsonUtil import commonTips as cct
import tdx_hdf5_api as h5a

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

# log=LoggerFactory.getLogger('Realdata')
log = LoggerFactory.log
# log.setLevel(LoggerFactory.INFO)
# log=LoggerFactory.JohnsonLoger('Realdata')


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
    # url='http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=20&sort=changepercent&asc=0&node=cyb&symbol='
    text = cct.get_url_data_R(url)
    # text = cct.get_url_data(url)
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
        # jstr = json.dumps(text, encoding='GBK')
        jstr = json.dumps(text,encoding='GBK')
    js = json.loads(jstr)
    # df = pd.DataFrame(pd.read_json(js, dtype={'code':object}),columns=ct.MARKET_COLUMNS)
    # log.debug("Market json:%s"%js[:1])
    df = pd.DataFrame(pd.read_json(js, dtype={'code': object}),
                      columns=ct.SINA_Market_COLUMNS)
    # print df[:1]
    # df = df.drop('symbol', axis=1)
    df = df.ix[df.volume >= 0]
    # print type(df)
    # print df[-2:-1],len(df.index)
    # print df.loc['300208',['name']]
    return df


def _get_sina_Market_url(market='sh_a', count=None, num='1000'):
    num = str(num)
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


def get_sina_Market_json(market='all', showtime=True, num='100', retry_count=3, pause=0.001):
    start_t = time.time()
#    http://qt.gtimg.cn/q=sz000858,sh600199
#    http://blog.csdn.net/ustbhacker/article/details/8365756
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

    h5_fname = 'get_sina_all_ratio'
    # h5_table = 'all'
    h5_table = 'all'+'_'+str(num)

    # if market == 'all':
    limit_time = ct.sina_dd_limit_time
    h5 = h5a.load_hdf_db(h5_fname, table=h5_table,limit_time=limit_time)
    if h5 is not None and len(h5) > 0 and 'timel' in h5.columns:
        o_time = h5[h5.timel <> 0].timel
        if len(h5) < 500:
            log.error("h5 not full data")
            o_time = []
        if len(o_time) > 0:
            o_time = o_time[0]
            l_time = time.time() - o_time
            # return_hdf_status = not cct.get_work_day_status()  or not cct.get_work_time() or (cct.get_work_day_status() and cct.get_work_time() and l_time < limit_time)
            return_hdf_status = not cct.get_work_time() or (cct.get_work_time() and l_time < limit_time)
            if return_hdf_status:
                log.info("load hdf data:%s %s %s"%(h5_fname,h5_table,len(h5)))
                dd = None
                if market == 'all':
                    co_inx = [inx for inx in h5.index if str(inx).startswith(('6','30','00'))]
                elif market == 'sh':
                    co_inx = [inx for inx in h5.index if str(inx).startswith(('6'))]
                elif market == 'sz':
                    co_inx = [inx for inx in h5.index if str(inx).startswith(('00'))]
                elif market == 'cyb':
                    co_inx = [inx for inx in h5.index if str(inx).startswith(('30'))]
                else:
                    log.error('market is not Find:%s'%(market))
                dd = h5.loc[co_inx]
                if len(dd) > 100:
                    log.info("return sina_ratio:%s"%(len(dd)))
                    return dd
    # else:

#    market = 'all'
    if market=='all':
        url_list=[]
        # for m in ct.SINA_Market_KEY.values():
        for m in ['sh_a','sz_a']:
            list=_get_sina_Market_url(m, num=num)
            for l in list:url_list.append(l)
        # print url_list
    else:
        url_list=_get_sina_Market_url(ct.SINA_Market_KEY[market], num=num)
        # print url_list
    log.debug("Market_jsonURL: %s" % url_list[0])
    # print url_list
    # print "url:",url_list
    df = pd.DataFrame()
    # data['code'] = symbol
    # df = df.append(data, ignore_index=True)

    # results = cct.to_mp_run(_parsing_Market_price_json, url_list)
    results = cct.to_asyncio_run(url_list, _parsing_Market_price_json)
    if len(results)>0:
        df = df.append(results, ignore_index=True)
        # df['volume']= df['volume'].apply(lambda x:x/100)
        # print df.columns
        if 'ratio' in df.columns:
            df['ratio']=df['ratio'].apply(lambda x:round(x,1))
        df['percent']=df['percent'].apply(lambda x:round(x,1))
#        if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 926:
#            df = df[(df.buy > 0)]
#        else:
#            df = df[(df.trade > 0)]
        # print df[:1]
    # for url in url_list:
    #     # print url
    #     data = _parsing_Market_price_json(url)
    #     # print data[:1]
    #     df = df.append(data, ignore_index=True)
    #     # break

    if df is not None and len(df) > 0:
        # for i in range(2, ct.PAGE_NUM[0]):
        #     newdf = _parsing_dayprice_json(i)
        #     df = df.append(newdf, ignore_index=True)
        # print len(df.index)

        # print type(df)
        if 'code' in df.columns:
            df=df.drop_duplicates('code')
            df = df.set_index('code')
        if market == 'all':
            append_status = False
        else:
            append_status = True

        h5 = h5a.write_hdf_db(h5_fname, df, table=h5_table,append=append_status)
        if showtime: print ("Market-df:%s %s" % (format((time.time() - start_t), '.1f'), len(df))),

        return df
    else:
        if showtime:print ("no data Market-df:%s" % (format((time.time() - start_t), '.2f')))
        return []
from configobj import ConfigObj
import os
# http://www.cnblogs.com/qq78292959/archive/2013/07/25/3213939.html
def getconfigBigCount(count=None,write=False):
    conf_ini = cct.get_work_path('stock','JSONData','count.ini')
    # print os.chdir(os.path.dirname(sys.argv[0]))
    # print (os.path.dirname(sys.argv[0]))
    # log.setLevel(LoggerFactory.INFO)
    if os.path.exists(conf_ini):
        log.info("file ok:%s"%conf_ini)
        config = ConfigObj(conf_ini,encoding='UTF8')
        if config['BigCount']['type2'] > 0:
            big_last= int(config['BigCount']['type2'])
            if count is None:
                big_now = int(sina_json_Big_Count())
            else:
                big_now = int(count)
            ratio_t=cct.get_work_time_ratio()
            bigRt=round( big_now / big_last / ratio_t, 1)
            big_v=int(bigRt*int(config['BigCount']['type2']))
            # print big_now,big_last,bigRt
            int_time=cct.get_now_time_int()
            # print int_time
            if write and (int_time < 915 or int_time > 1500 ) and big_now > 0 and big_last != big_now :
                # print write,not cct.get_work_time(),big_now > 0,big_last != big_now
                log.info("big_now update:%s last:%s"%(big_now,big_last))
                config['BigCount']['type2'] = big_now
                rt=float(config['BigCount']['ratio'])
                # if  rt != bigRt:
                log.info("bigRt:%s"%bigRt)
                config['BigCount']['ratio'] = bigRt
                config.write()
                return [big_now,bigRt,big_v]
            else:
                log.info("not work:%s ra:%s"%(big_now,bigRt))
                return [big_now,bigRt,big_v]
    else:
        config = ConfigObj(conf_ini,encoding='UTF8')
        config['BigCount'] = {}
        config['BigCount']['type2'] = sina_json_Big_Count()
        config['BigCount']['ratio'] = 0
        config.write()
    big_v= 0
    cl=[config['BigCount']['type2'],config['BigCount']['ratio'],0]
    return cl

def sina_json_Big_Count(vol='1', type='0', num='10000'):
    url = ct.JSON_DD_CountURL % (ct.DD_VOL_List[vol], type)
    log.info("Big_Count_url:%s"%url)
    data = cct.get_url_data(url)
    count = re.findall('(\d+)', data, re.S)
    log.debug("Big_Count_count:%s"%count)
    if len(count) > 0:
        count = count[0]
    else:
        count = 0
    return count

def _get_sina_json_dd_url(vol='0', type='0', num='10000', count=None):
    urllist = []
    vol = str(vol)
    type = str(type)
    num = str(num)
    if count == None:
        url = ct.JSON_DD_CountURL % (ct.DD_VOL_List[vol], type)
        log.info("_json_dd_url:%s"%url)
        data = cct.get_url_data(url)
        # return []
        # print data.find('abc')
        count = re.findall('(\d+)', data, re.S)
        log.debug("_json_dd_url_count:%s"%count)
        # print count
        if len(count) > 0:
            count = count[0]
            bigcount=getconfigBigCount(count,write=False)
            print ("Big:%s V:%s "%(bigcount[0],bigcount[1])),
            if int(count) >= int(num):
                page_count = int(math.ceil(int(count) / int(num)))
                for page in range(1, page_count + 1):
                    # print page
                    url = ct.JSON_DD_Data_URL_Page % (int(num), page, ct.DD_VOL_List[vol], type)
                    urllist.append(url)
            else:
                url = ct.JSON_DD_Data_URL_Page % (count, '1', ct.DD_VOL_List[vol], type)
                urllist.append(url)
        else:
            log.error("url Count error:%s"%(url))
            return []
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
    # print(len(text))
    # return text
    if len(text) < 10:
        return ''
    reg = re.compile(r'\,(.*?)\:')
    text = reg.sub(r',"\1":', text.decode('gbk') if ct.PY3 else text)
    text = text.replace('"{symbol', '{"code')
    text = text.replace('{symbol', '{"code"')

    if ct.PY3:
        jstr = json.dumps(text)
    else:
        # jstr = json.dumps(text, encoding='GBK')
        jstr = json.dumps(text)
    js = json.loads(jstr)
    df = pd.DataFrame(pd.read_json(js, dtype={'code': object}),
                      columns=ct.DAY_REAL_DD_COLUMNS)
    df = df.drop('symbol', axis=1)
    df = df.ix[df.volume > 0]
    # print ""
    # print df['name'][len(df.index)-1:],len(df.index)
    return df


def get_sina_all_json_dd(vol='0', type='0', num='10000', retry_count=3, pause=0.001):
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

    h5_fname = 'get_sina_all_dd'
    h5_table = 'all'+'_'+ct.DD_VOL_List[str(vol)]+'_'+str(num)
    limit_time = ct.sina_dd_limit_time
    h5 = h5a.load_hdf_db(h5_fname, table=h5_table,limit_time=limit_time)
    if h5 is not None and not h5.empty and 'timel' in h5.columns:
       o_time = h5[h5.timel <> 0].timel
       if len(o_time) > 0:
           o_time = o_time[0]
           l_time = time.time() - o_time

           return_hdf_status = not cct.get_work_time() or (cct.get_work_time() and l_time < limit_time)
           if return_hdf_status:
               log.info("load hdf data:%s %s %s"%(h5_fname,h5_table,len(h5)))
               return h5

    # ct._write_head()
    url_list = _get_sina_json_dd_url(vol, type, num)
    # print url_list
    df = pd.DataFrame()
    # data['code'] = symbol
    # df = df.append(data, ignore_index=True)
    if len(url_list)>0:
        log.info("json_dd_url:%s"%url_list[0])
        data = cct.to_asyncio_run(url_list, _parsing_sina_dd_price_json)
    # data = cct.to_mp_run(_parsing_sina_dd_price_json, url_list)
    # data = cct.to_mp_run_async(_parsing_sina_dd_price_json, url_list)

    # if len(url_list)>cct.get_cpu_count():
    #     divs=cct.get_cpu_count()
    # else:
    #     divs=len(url_list)
    #
    # if len(url_list)>=divs:
    #     print len(url_list),
    #     dl=cct.get_div_list(url_list,divs)
    #     data=cct.to_mp_run_async(cct.to_asyncio_run,dl,_parsing_sina_dd_price_json)
    # else:
    #     data=cct.to_asyncio_run(url_list,_parsing_sina_dd_price_json)

        if len(data)>0:
            df = df.append(data, ignore_index=True)
#            log.debug("dd.columns:%s" % df.columns.values)
            #['code' 'name' 'ticktime' 'price' 'volume' 'prev_price' 'kind']
            log.debug("get_sina_all_json_dd:%s" % df[:1])

        if df is not None and not df.empty:
            # for i in range(2, ct.PAGE_NUM[0]):
            #     newdf = _parsing_dayprice_json(i)
            #     df = df.append(newdf, ignore_index=True)
            df['couts']=df.groupby(['code'])['code'].transform('count')
            # df=df[(df['kind'] == 'U')]
            df=df.sort_values(by='couts',ascending=0)
            time_drop=time.time()
            df=df.drop_duplicates('code')
            print "djdf:%0.1f"%(time.time()-time_drop),
            # df=df[df.price >df.prev_price]
            log.info("sina-DD:%s" % df[:1])
#            df = df.loc[:, ['code','name', 'couts', 'kind', 'prev_price']]
#            print df.columns
            df = df.loc[:, ['code','name', 'couts', 'kind', 'prev_price','ticktime']]
            df.code=df.code.apply(lambda x:str(x).replace('sh','') if str(x).startswith('sh') else str(x).replace('sz',''))
            if len(df) > 0:
                df = df.set_index('code')
                h5 = h5a.write_hdf_db(h5_fname, df, table=h5_table,append=False)
                log.info("get_sina_all_json_dd:%s"%(len(df)))
            print (" dd-df:%0.2f" % ((time.time() - start_t))),
            return df
        else:
            print
            print ("no data  json-df:%0.2f"%((time.time() - start_t))),
            return ''
    else:
        print ("Url None json-df:%0.2f "%((time.time() - start_t))),
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

def get_sina_dd_count_price_realTime(df='',table='all',vol='0',type='0'):
    '''
    input df count and merge price to df
    '''
#    if table <> 'all':
#        log.error("check market is not all")

    if len(df)==0:
        # df = get_sina_all_json_dd('0')
        df = get_sina_all_json_dd(vol,type)

    if len(df)>0:
        df['couts']=df.groupby(['code'])['code'].transform('count')
        # df=df[(df['kind'] == 'U')]
        df=df.sort_values(by='couts',ascending=0)
        time_drop=time.time()
        df=df.drop_duplicates('code')
        print "ddf:%0.1f"%(time.time()-time_drop),
        # df=df[df.price >df.prev_price]
        df = df.loc[:, ['code', 'name', 'couts', 'prev_price']]
        log.info("df.market:%s" % df[:1])

        # dz.loc['sh600110','couts']=dz.loc['sh600110'].values[1]+3
        df=df.set_index('code')
        # df=df.iloc[0:,0:2]
        df['dff']=0

        dp=get_sina_Market_json(table)
        log.info("dp.market:%s" % dp[:1])
        if len(dp)>10:
            dp=dp.dropna('index')
            time_drop=time.time()
            dp=dp.drop_duplicates('code')
            print "ddp:%0.1f"%(time.time()-time_drop),
            log.info("dp to dm.market:%s" % dp[:1])
            dm=pd.merge(df,dp,on='name',how='left')
            # dm=dm.drop_duplicates('code')
            dm=dm.set_index('code')
            dm=dm.dropna('index')
            log.info("dm.market2:%s" % dm[:1])
            # dm.loc[dm.percent>9.9,'percent']=10
            # print dm[-1:]
            dm=dm.loc[:,ct.SINA_DD_Clean_Count_Columns]
            dm.prev_price=dm.prev_price.fillna(0.0)
            dm.rename(columns={'prev_price': 'prev_p'}, inplace=True)

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

def get_market_price_sina_dd_realTime(dp='',vol='0',type='0'):
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
#        dp=dp.drop_duplicates('code')
        log.info("Market_realTime:%s"%len(dp))
        # dp=dp.set_index('code')
        dp=dp.fillna(0)
        dp=dp.dropna('index')
        # if dp[:1].volume.values >0:
        # log.debug("dp.volume>0:%s"%dp[:1].volume.values)
        # dp['volume']=dp['volume'].apply(lambda x:round(x/100,1))
        # dp=dp.loc[:,'trade':].astype(float)
        log.info("DP:%s" % dp[:1].open)

        # if len(dp[:10][dp[:10]['buy'] > 0]) > 2 and len(dp[:10][dp[:10]['percent'] == 0]) > 2:
        #     if 'close' in dp.columns:
        #         if len(dp[:5][dp[:5]['close'] > 0]) > 2:
        #             dp['percent'] = (map(lambda x, y: round((x - y) / y * 100, 1), dp['buy'].values, dp['close'].values))
        #             log.info("DP-1-percent==0:%s" % dp[:1].percent)

        # dp.loc[dp.percent>9.9,'percent']=10

        dp['dff']=0
        df=get_sina_all_json_dd(vol,type)
        if len(df)>10:

            # print df[df.couts>0][:2]
            dm = cct.combine_dataFrame(dp,df)
            log.info("top_now:main:%s subobject:%s dm:%s "%(len(dp),len(df),len(dm)))
#            dm=pd.merge(dp,df,on='name',how='left')
            log.debug("dmMerge:%s"%dm.columns)
            # print dm[dm.couts>0][:2]
            dm.couts=dm.couts.fillna(0)
            dm.prev_price=dm.prev_price.fillna(0.0)
            dm.couts=dm.couts.astype(int)
#            dm=dm.drop_duplicates('code')
#            dm=dm.set_index('code')
            dm.rename(columns={'prev_price': 'prev_p'}, inplace=True)
            # print dm.sort_values(by=['couts','percent','dff','ratio'],ascending=[0,0,0,1])[:2]
            # dm=dm.fillna(int(0))
            # dm.ratio=dm.ratio
            # dm=dm.loc[:,ct.SINA_Market_Clean_UP_Columns]
        else:
            dp=dp.set_index('code')
            dp['couts'] = 0
            dp['prev_p'] = 0
            dm = dp
            # dm=dp.loc[:,ct.SINA_Market_Clean_Columns]
            # dm=dp.loc[:,ct.SINA_Market_Clean_UP_Columns]
            # dm['prev_p']=0.0
                    # ['name','buy','dff','percent','ratio','high','open','volume','low','couts']
                    #['name','buy','dff','percent','trade','high','ratio','volume','couts']

    else:
        dm=''
    # print type(dm)
    return dm





if __name__ == '__main__':
    import sys
    # log.setLevel(LoggerFactory.DEBUG)
    # df = get_sina_all_json_dd('0', '3')
    # df = get_market_price_sina_dd_realTime(dp='', vol='1', type='0')
    # print df
    # df = get_sina_all_json_dd(1,0,num=10000)
    # print len(df)
    for mk in ['sz','cyb','sh']:
        df=get_sina_Market_json(mk,num=100)
        print "mk:\t",len(df)
    import tushare as ts
    s_t=time.time()
    df = ts.get_today_all()
    print "len:%s,time:%0.2f"%(len(df),time.time()-s_t)
    print df[:1]
    # _get_sina_json_dd_url()
    # print sina_json_Big_Count()
    # print getconfigBigCount(write=True)
    sys.exit(0)
    # post_login()
    # get_wencai_Market_url(filter='热门股')
    df = get_sina_Market_json('all')
    print df[df.code == '600581']
    print df[:1],df.shape
    sys.exit()
    top_now = get_market_price_sina_dd_realTime(df, '2', type)
    print top_now[:1]
    # _parsing_Market_price_json('cyb')
    # sys.exit(0)
    # dd = get_sina_all_json_dd('0', '4')
    dd = get_sina_all_json_dd('2')
    print ""
    print dd[:2]
    df = get_sina_dd_count_price_realTime(dd)
    # df = get_sina_all_json_dd('0', '1')
    print len(df)
    print df[:2]
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
