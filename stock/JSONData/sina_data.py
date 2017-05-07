# -*- encoding: utf-8 -*-

import json
import os
import re
import sys
import time

sys.path.append("..")
import pandas as pd
import requests

from JohhnsonUtil import johnson_cons as ct
from JohhnsonUtil import commonTips as cct
from JohhnsonUtil import LoggerFactory
import trollius as asyncio
from trollius.coroutines import From
log = LoggerFactory.getLogger('Sina_data')
# log.setLevel(LoggerFactory.DEBUG)


class StockCode:
    def __init__(self):
        self.start_t = time.time()
        self.STOCK_CODE_PATH = 'stock_codes.conf'
        self.stock_code_path = self.stock_code_path()
        if not os.path.exists(self.stock_code_path) or cct.creation_date_duration(self.stock_code_path) > 120:
            print ("days:%s update stock_codes.conf"%(cct.creation_date_duration(self.stock_code_path)))
            self.get_stock_codes(True)

        self.stock_codes = None

    def stock_code_path(self):
        return os.path.join(os.path.dirname(__file__), self.STOCK_CODE_PATH)

    def update_stock_codes(self):
        """获取所有股票 ID 到 all_stock_code 目录下"""
        all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
        grep_stock_codes = re.compile('~(\d+)`')
        response = requests.get(all_stock_codes_url)
        all_stock_codes = grep_stock_codes.findall(response.text)
        # print len(all_stock_codes)

        with open(self.stock_code_path, 'w') as f:
            f.write(json.dumps(dict(stock=all_stock_codes)))

    # @property
    def get_stock_codes(self, realtime=False):
        """获取所有股票 ID 到 all_stock_code 目录下"""
        if realtime:
            all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
            grep_stock_codes = re.compile('~(\d+)`')
            response = requests.get(all_stock_codes_url)
            stock_codes = grep_stock_codes.findall(response.text)
            print len(stock_codes)
            with open(self.stock_code_path, 'w') as f:
                f.write(json.dumps(dict(stock=stock_codes)))
            return stock_codes
        else:
            with open(self.stock_code_path) as f:
                self.stock_codes = json.load(f)['stock']
                return self.stock_codes


# -*- encoding: utf-8 -*-


class Sina:
    """新浪免费行情获取"""

    def __init__(self):
        # self.grep_stock_detail = re.compile(r'(\d+)=([^\S][^,]+?)%s' %
        # (r',([\.\d]+)' * 29,))   #\n特例A (4)
        self.grep_stock_detail = re.compile(
            r'(\d+)=([^\n][^,]+.)%s' % (r',([\.\d]+)' * 29,))  # 去除\n特例A(3356)
        # self.grep_stock_detail = re.compile(r'(00\d{4}|30\d{4}|60\d{4})=([^\n][^,]+.)%s' % (r',([\.\d]+)' * 29,))   #去除\n特例A(股票2432)
        # ^(?!64)\d+$
        # self.grep_stock_detail = re.compile(r'([0][^0]\d+.)=([^\n][^,]+.)%s'
        # % (r',([\.\d]+)' * 29,))  # 去除\n特例A(股票2432)
        self.sina_stock_api = 'http://hq.sinajs.cn/?format=text&list='
        self.stock_data = []
        self.stock_codes = []
        self.stock_with_exchange_list = []
        self.max_num = 850
        self.start_t = time.time()
        self.dataframe = pd.DataFrame()
        self.index_status = False

    def load_stock_codes(self):
        with open(self.stock_code_path) as f:
            self.stock_codes = json.load(f)['stock']

    # def get_stocks_by_range(self, index):
    #
    #     response = requests.get(self.sina_stock_api + self.stock_list[index])
    #     self.stock_data.append(response.text)
    @property
    def all(self):
        self.stockcode = StockCode()
        self.stock_code_path = self.stockcode.stock_code_path
        self.stock_codes = self.stockcode.get_stock_codes()
        self.load_stock_codes()
        self.stock_codes = [elem for elem in self.stock_codes if elem.startswith(('6','30','00'))]
        # self.stock_with_exchange_list = list(
            # map(lambda stock_code: ('sh%s' if stock_code.startswith(('5', '6', '9')) else 'sz%s') % stock_code,
                # self.stock_codes))
        self.stock_with_exchange_list = list(
            map(lambda stock_code: ('sh%s' if stock_code.startswith(('6')) else 'sz%s') % stock_code,
                self.stock_codes))
        self.stock_list = []
        self.request_num = len(self.stock_with_exchange_list) // self.max_num
        for range_start in range(self.request_num):
            num_start = self.max_num * range_start
            num_end = self.max_num * (range_start + 1)
            request_list = ','.join(
                self.stock_with_exchange_list[num_start:num_end])
            self.stock_list.append(request_list)
        # print len(self.stock_with_exchange_list), num_end
        if len(self.stock_with_exchange_list) > num_end:
            request_list = ','.join(
                self.stock_with_exchange_list[num_end:])
            self.stock_list.append(request_list)
            self.request_num += 1
        # a = 0
        # for x in range(self.request_num):
        #     print x
        #     i = len(self.stock_list[x].split(','))
        #     print i
        #     a += i
        #     print a
        log.debug('all:%s' % len(self.stock_list))
        # log.error('all:%s req:%s' %
        #           (len(self.stock_list), len(self.stock_list)))
        return self.get_stock_data()

    def market(self,market):
        if market in ['all']:
            return self.all
        else:
            self.stockcode = StockCode()
            self.stock_code_path = self.stockcode.stock_code_path
            self.stock_codes = self.stockcode.get_stock_codes()
            self.load_stock_codes()
            # print type(self.stock_codes)
            # self.stock_with_exchange_list = list(
                # map(lambda stock_code: ('sh%s' if stock_code.startswith(('5', '6', '9')) else 'sz%s') % stock_code,
                    # self.stock_codes))        elif market == 'cyb':
            # print len(self.stock_codes)
            # self.stock_codes = [elem for elem in self.stock_codes if elem.startswith(('6','30','00'))]
            # print len(self.stock_codes)
            if market == 'sh':
                self.stock_codes = [elem for elem in self.stock_codes if elem.startswith('6')]
                self.stock_with_exchange_list = list(
                    map(lambda stock_code: ('sh%s') % stock_code,
                        self.stock_codes))
            elif market == 'sz':
                self.stock_codes = [elem for elem in self.stock_codes if elem.startswith('00')]
                self.stock_with_exchange_list = list(
                    map(lambda stock_code: ('sz%s' ) % stock_code,
                        self.stock_codes))
            elif market == 'cyb':
                self.stock_codes = [elem for elem in self.stock_codes if elem.startswith('30')]
                self.stock_with_exchange_list = list(
                    map(lambda stock_code: ('sz%s' )% stock_code,
                        self.stock_codes))
            self.stock_list = []
            self.request_num = len(self.stock_with_exchange_list) // self.max_num
            for range_start in range(self.request_num):
                num_start = self.max_num * range_start
                num_end = self.max_num * (range_start + 1)
                request_list = ','.join(
                    self.stock_with_exchange_list[num_start:num_end])
                self.stock_list.append(request_list)
            # print len(self.stock_with_exchange_list), num_end
            # if self.request_num == 0:
            #     num_end = self.max_num
            if self.request_num > 0 and len(self.stock_with_exchange_list) > num_end:
                request_list = ','.join(
                    self.stock_with_exchange_list[num_end:])
                self.stock_list.append(request_list)
                self.request_num += 1
            else:
                request_list = ','.join(
                    self.stock_with_exchange_list)
                self.stock_list.append(request_list)
            # a = 0
            # for x in range(self.request_num):
            #     print x
            #     i = len(self.stock_list[x].split(','))
            #     print i
            #     a += i
            #     print a
            print ('all:%s' % len(self.stock_codes)),
            # log.error('all:%s req:%s' %
            #           (len(self.stock_list), len(self.stock_list)))
            return self.get_stock_data()        
    # def get_url_data_R(url):
    #     # headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    #                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #                'Connection': 'keep-alive'}
    #     req = Request(url, headers=headers)
    #     fp = urlopen(req, timeout=5)
    #     data = fp.read()
    #     fp.close()
    #     return data

    @asyncio.coroutine
    def get_stocks_by_range(self, index):

        loop = asyncio.get_event_loop()
        # response = yield From(loop.run_in_executor(None,self.get_url_data_R,
        # (self.sina_stock_api + self.stock_list[index])))
        response = yield From(loop.run_in_executor(None, requests.get, (self.sina_stock_api + self.stock_list[index])))
        # response = yield (requests.get(self.sina_stock_api + self.stock_list[index]))
        # log.debug("url:%s"%(self.sina_stock_api + self.stock_list[index]))
        log.debug("res_encoding:%s" % response.encoding)
        self.stock_data.append(response.text)
        # Return(self.stock_data.append(response.text))

    def get_stock_data(self, retry_count=3, pause=0.01):
        threads = []
        for index in range(self.request_num):
            threads.append(self.get_stocks_by_range(index))
            log.debug("url:%s  len:%s" %
                      (self.sina_stock_api, len(self.stock_list[index])))
        if self.request_num == 0:
            threads.append(self.get_stocks_by_range(0))
        for _ in range(retry_count):
            time.sleep(pause)
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.wait(threads))
            log.debug('get_stock_data_loop')
            return self.format_response_data()

        raise IOError(ct.NETWORK_URL_ERROR_MSG)

    # def get_stock_data(self):
    #     threads = []
    #     for index in range(self.request_num):
    #         threads.append(index)
    #
    #     # cct.to_mp_run(self.get_stocks_by_range, threads)
    #
    #     return self.format_response_data()

    def get_stock_code_data(self, code, index=False):
        code_t =  code.split(',')
        if len(code_t) > 1:
            code = code_t
#        self.stock_codes = code
        # self.stock_with_exchange_list = list(
        #     map(lambda stock_code: ('sh%s' if stock_code.startswith(('5', '6', '9')) else 'sz%s') % stock_code,
        #         ulist))
        if index:
            self.index_status = index
            if isinstance(code, list):
                code_l =[]
                for x in code:
                    if x.startswith('999'):
                        code_l.append(str(1000000-int(x)).zfill(6))
                    else:
                        code_l.append(x)
                self.stock_codes = map(lambda stock_code: (
                'sh%s' if stock_code.startswith(('0')) else 'sz%s') % stock_code, code_l)

            else:
                if isinstance(code,str) and code.startswith('999'):
                    code = '000001'
                self.stock_codes = map(lambda stock_code: (
                    'sh%s' if stock_code.startswith(('0')) else 'sz%s') % stock_code, code.split())
        else:
            self.stock_codes = map(lambda stock_code: ('sh%s' if stock_code.startswith(
                ('5', '6', '9')) else 'sz%s') % stock_code, code.split())
        self.url = self.sina_stock_api + ','.join(self.stock_codes)
        log.info("stock_list:%s" % self.url[:20])
        response = requests.get(self.url)
        self.stock_data.append(response.text)
        self.dataframe = self.format_response_data()
        # self.get_tdx_dd()
        return self.dataframe

    def get_stock_list_data(self, ulist):
        self.stock_data = []
        if len(ulist) > self.max_num:
            # print "a"
            self.stock_list = []
            self.stock_with_exchange_list = list(
                map(lambda stock_code: ('sh%s' if stock_code.startswith(('5', '6', '9')) else 'sz%s') % stock_code,
                    ulist))
            self.request_num = len(
                self.stock_with_exchange_list) // self.max_num
            for range_start in range(self.request_num):
                num_start = self.max_num * range_start
                num_end = self.max_num * (range_start + 1)
                request_list = ','.join(
                    self.stock_with_exchange_list[num_start:num_end])
                self.stock_list.append(request_list)
            if len(self.stock_with_exchange_list) > num_end:
                request_list = ','.join(
                    self.stock_with_exchange_list[num_end:])
                self.stock_list.append(request_list)
                self.request_num += 1

            log.debug('all:%s' % len(self.stock_list))
            return self.get_stock_data()
        else:
            self.stock_codes = ulist
            # self.stock_with_exchange_list = list(
            #     map(lambda stock_code: ('sh%s' if stock_code.startswith(('5', '6', '9')) else 'sz%s') % stock_code,
            #         ulist))
            self.stock_codes = map(lambda stock_code: ('sh%s' if stock_code.startswith(
                ('5', '6', '9')) else 'sz%s') % stock_code, ulist)
            self.url = self.sina_stock_api + ','.join(self.stock_codes)
            log.info("stock_list:%s" % self.url[:30])
            response = requests.get(self.url)
            self.stock_data.append(response.text)
            self.dataframe = self.format_response_data()
        # self.get_tdx_dd()
        return self.dataframe

    # def get_tdx_dd(self):
    #     df = tdd.get_tdx_all_day_LastDF(self.stock_codes)
        # print df

    def format_response_data(self):
        stocks_detail = ''.join(self.stock_data)
        # print stocks_detail
        result = self.grep_stock_detail.finditer(stocks_detail)
        # stock_dict = dict()
        list_s = []
        for stock_match_object in result:
            stock = stock_match_object.groups()
            # print stock
            # fn=(lambda x:x)
            # list.append(map(fn,stock))
            # df = pd.DataFrame(list,columns=ct.SINA_Total_Columns)
            #     list_s.append({'code'})
            list_s.append(
                {'code': stock[0],
                 'name': stock[1],
                 'open': float(stock[2]),
                 'close': float(stock[3]),
                 'now': float(stock[4]),
                 'high': float(stock[5]),
                 'low': float(stock[6]),
                 'buy': float(stock[7]),
                 'sell': float(stock[8]),
                 'volume': int(stock[9]),
                 'turnover': float(stock[10]),
                 # 'amount': float(stock[10]),
                 'b1_v': int(stock[11]),
                 'b1': float(stock[12]),
                 'b2_v': int(stock[13]),
                 'b2': float(stock[14]),
                 'b3_v': int(stock[15]),
                 'b3': float(stock[16]),
                 'b4_v': int(stock[17]),
                 'b4': float(stock[18]),
                 'b5_v': int(stock[19]),
                 'b5': float(stock[20]),
                 'a1_v': int(stock[21]),
                 'a1': float(stock[22]),
                 'a2_v': int(stock[23]),
                 'a2': float(stock[24]),
                 'a3_v': int(stock[25]),
                 'a3': float(stock[26]),
                 'a4_v': int(stock[27]),
                 'a4': float(stock[28]),
                 'a5_v': int(stock[29]),
                 'a5': float(stock[30])})
#        print list_s
        # df = pd.DataFrame.from_dict(stock_dict,columns=ct.SINA_Total_Columns)
        df = pd.DataFrame(list_s, columns=ct.SINA_Total_Columns)
        # if self.index_status and cct.get_work_time():
        # if self.index_status:
        # if cct.get_work_time() or (cct.get_now_time_int() > 915) :
        # df = df.drop('close', axis=1)
        df.rename(columns={'close': 'llastp'}, inplace=True)
        if (cct.get_now_time_int() > 915 and cct.get_now_time_int() < 931):
#            df.rename(columns={'buy': 'close'}, inplace=True)
            df['close']=df['buy']
            df['low']=df['buy']
        elif (cct.get_now_time_int() > 830 and cct.get_now_time_int() < 915):
#            df.rename(columns={'buy': 'close'}, inplace=True)
            df['buy']=df['llastp']
            df['close']=df['buy']
            df['low']=df['buy']
        else:
            df.rename(columns={'now': 'close'}, inplace=True)
        df = df.drop_duplicates('code')
        # df = df.loc[:, ct.SINA_Total_Columns_Clean]
        # df = df.loc[:, ct.SINA_Total_Columns]
        # df.rename(columns={'turnover': 'amount'}, inplace=True)
        df = df.fillna(0)
        df = df.sort_values(by='code', ascending=0)
        # print ("Market-df:%s %s time: %s" % (
        # format((time.time() - self.start_t), '.3f'), len(df),
        # cct.get_now_time()))
        return df
        # df = pd.DataFrame.from_dict(stock_dict, orient='columns',
        #                             columns=['name', 'open', 'close', 'now', 'high', 'low', 'buy', 'sell', 'turnover',
        #                                      'volume', 'bid1_volume', 'bid1', 'bid2_volume', 'bid2', 'bid3_volume',
        #                                      'bid3', 'bid4_volume', 'bid4', 'bid5_volume', 'bid5', 'ask1_volume',
        #                                      'ask1', 'ask2_volume', 'ask2', 'ask3_volume', 'ask3', 'ask4_volume',
        #                                      'ask4', 'ask5_volume', 'ask5'])
        # return stock_dict


if __name__ == "__main__":
    times = time.time()
    # sina = Sina()
    # print len(df)
    # code='601198'
    # df = sina.get_stock_list_data(['300134', '601998', '999999']).set_index('code')
    # df = sina.get_stock_code_data('000001',index=True).set_index('code')
#    print sina.get_stock_code_data('399006,999999',index=True)
    log.setLevel(LoggerFactory.DEBUG)
    for ma in ['sh','sz','cyb','all']:
        print ma
        df = Sina().market(ma)
        # print len(sina.all)
        print len(df)
        print df[df.code == '600581']
        # print sina.get_stock_code_data('999999',index=True)
        # df = sina.get_stock_list_data(['600629', '000507']).set_index('code')
        # df = sina.get_stock_code_data('002775',index=False).set_index('code')
        print len(df)
    # print df.loc['300380']
    # list=['000001','399001','399006','399005']
    # df=sina.get_stock_list_data(list)
    # print time.time() - times
    # print len(df.index)
    # print df[:4]
    # print df[df.code == '000024']
    # print df[df.code == '002788']
    # print df[df.code == '150027']
    # print df[df.code == '200024']
    # print df.code
    # print len(df.index)

    # print df[df.low.values <> df.high.values].iloc[:1,:8]
