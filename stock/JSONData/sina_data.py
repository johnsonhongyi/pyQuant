# -*- encoding: utf-8 -*-

import json
import os
import re
import time
import sys
sys.path.append("..")
import pandas as pd
import requests

from JohhnsonUtil import johnson_cons as ct
from JohhnsonUtil import commonTips as cct
from JohhnsonUtil import LoggerFactory
import trollius as asyncio
from trollius.coroutines import From

log = LoggerFactory.getLogger('Sina_data')

class StockCode:
    def __init__(self):
        self.start_t = time.time()
        self.STOCK_CODE_PATH = 'stock_codes.conf'
        self.stock_code_path = self.stock_code_path()
        if not os.path.exists(self.stock_code_path):
            print ("update stock_codes.conf")
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
        # self.grep_stock_detail = re.compile(r'(\d+)=([^\S][^,]+?)%s' % (r',([\.\d]+)' * 29,))   #\n特例A (4)
        self.grep_stock_detail = re.compile(r'(\d+)=([^\n][^,]+.)%s' % (r',([\.\d]+)' * 29,))  # 去除\n特例A(3356)
        # self.grep_stock_detail = re.compile(r'(00\d{4}|30\d{4}|60\d{4})=([^\n][^,]+.)%s' % (r',([\.\d]+)' * 29,))   #去除\n特例A(股票2432)
        self.sina_stock_api = 'http://hq.sinajs.cn/?format=text&list='
        self.stock_data = []
        self.stock_codes = []
        self.stock_with_exchange_list = []
        self.max_num = 850
        self.stockcode = StockCode()
        self.stock_code_path = self.stockcode.stock_code_path
        self.stock_codes = self.stockcode.get_stock_codes()
        self.load_stock_codes()
        self.stock_with_exchange_list = list(
            map(lambda stock_code: ('sh%s' if stock_code.startswith(('5', '6', '9')) else 'sz%s') % stock_code,
                self.stock_codes))

        self.stock_list = []
        self.request_num = len(self.stock_with_exchange_list) // self.max_num
        for range_start in range(self.request_num):
            num_start = self.max_num * range_start
            num_end = self.max_num * (range_start + 1)
            request_list = ','.join(self.stock_with_exchange_list[num_start:num_end])
            self.stock_list.append(request_list)

    def load_stock_codes(self):
        with open(self.stock_code_path) as f:
            self.stock_codes = json.load(f)['stock']

    # def get_stocks_by_range(self, index):
    #
    #     response = requests.get(self.sina_stock_api + self.stock_list[index])
    #     self.stock_data.append(response.text)
    @property
    def all(self):
        return self.get_stock_data()

    @asyncio.coroutine
    def get_stocks_by_range(self, index):

        loop = asyncio.get_event_loop()
        response = yield From(loop.run_in_executor(None, requests.get, (self.sina_stock_api + self.stock_list[index])))
        # response = yield (requests.get(self.sina_stock_api + self.stock_list[index]))
        # print response.text
        self.stock_data.append(response.text)
        # Return(self.stock_data.append(response.text))

    def get_stock_data(self):
        threads = []
        for index in range(self.request_num):
            threads.append(self.get_stocks_by_range(index))
            # log.debug("url:%s"%self.sina_stock_api + self.stock_list[index])
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(threads))
        return self.format_response_data()

    # def get_stock_data(self):
    #     threads = []
    #     for index in range(self.request_num):
    #         threads.append(index)
    #
    #     # cct.to_mp_run(self.get_stocks_by_range, threads)
    #
    #     return self.format_response_data()

    def format_response_data(self):
        stocks_detail = ''.join(self.stock_data)
        result = self.grep_stock_detail.finditer(stocks_detail)
        # stock_dict = dict()
        list_s = []
        for stock_match_object in result:
            stock = stock_match_object.groups()
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
                 'bid1_volume': int(stock[11]),
                 'bid1': float(stock[12]),
                 'bid2_volume': int(stock[13]),
                 'bid2': float(stock[14]),
                 'bid3_volume': int(stock[15]),
                 'bid3': float(stock[16]),
                 'bid4_volume': int(stock[17]),
                 'bid4': float(stock[18]),
                 'bid5_volume': int(stock[19]),
                 'bid5': float(stock[20]),
                 'ask1_volume': int(stock[21]),
                 'ask1': float(stock[22]),
                 'ask2_volume': int(stock[23]),
                 'ask2': float(stock[24]),
                 'ask3_volume': int(stock[25]),
                 'ask3': float(stock[26]),
                 'ask4_volume': int(stock[27]),
                 'ask4': float(stock[28]),
                 'ask5_volume': int(stock[29]),
                 'ask5': float(stock[30])})

        # df = pd.DataFrame.from_dict(stock_dict,columns=ct.SINA_Total_Columns)
        df = pd.DataFrame(list_s, columns=ct.SINA_Total_Columns)
        df = df.drop_duplicates('code')
        df = df.loc[:, ct.SINA_Total_Columns_Clean]
        df = df.fillna(0)
        print ("Market-df:%s %s time: %s" % (
        format((time.time() - self.stockcode.start_t), '.3f'), len(df), cct.get_now_time()))
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
    sina = Sina()
    # sina.
    df = sina.all
    print time.time() - times
    print len(df.index)
    print df[:4]
    print df[df.code == '000024']
    print df[df.code == '002788']
    print df[df.code == '150027']
    print df[df.code == '200024']
    # print df.code
    # print len(df.index)

    # print df[df.low.values <> df.high.values].iloc[:1,:8]
