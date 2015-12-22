#-*- coding: UTF-8 -*-
'''
Created on 2015年3月2日
@author: Casey
'''
import time
import threading
'''
上证编码：'600001' .. '602100'
深圳编码：'000001' .. '001999'
中小板：'002001' .. '002999'
创业板：'300001' .. '300400'
'''
import urllib2
from datetime import date
from db.LoggerFactory import *
from db.DBOperator import *
# from setting import *
codingtype='gbk'

class StockTencent(object):
    #数据库表
    __stockTables = {'cash':'stock_cash_tencent','quotation':'stock_quotation_tencent'}
    '''初始化'''
    def __init__(self):
       self.__logger = LoggerFactory.getLogger('StockTencent')
       self.__dbOperator = DBOperator()

    def main(self):
        self.__dbOperator.connDB()
        threading.Thread(target = self.getStockCash()).start()
        threading.Thread(target = self.getStockQuotation()).start()
        self.__dbOperator.closeDB()

    '''查找指定日期股票流量'''
    def __isStockExitsInDate(self, table, stock, date):
        sql = "select * from " + table + " where code = '%s' and date='%s'" % (stock, date)
        n = self.__dbOperator.execute(sql)
        if n >= 1:
            return True

    '''获取股票资金流明细'''
    def __getStockCashDetail(self, dataUrl):
        #读取数据
        tempData = self.__getDataFromUrl(dataUrl)

        if tempData == None:
            time.sleep(10)
            tempData = self.__getDataFromUrl(dataUrl)
            return False

        #解析资金流向数据
        stockCash = {}
        stockInfo = tempData.split('~')
        if len(stockInfo) < 13: return
        if len(stockInfo) != 0 and stockInfo[0].find('pv_none') == -1:
            table = self.__stockTables['cash']
            code = stockInfo[0].split('=')[1][2:]
            date = stockInfo[13]
            if not self.__isStockExitsInDate(table, code, date):
                stockCash['code'] = stockInfo[0].split('=')[1][2:]
                stockCash['main_in_cash']     = stockInfo[1]
                stockCash['main_out_cash']    = stockInfo[2]
                stockCash['main_net_cash']    = stockInfo[3]
                stockCash['main_net_rate']    = stockInfo[4]
                stockCash['private_in_cash']  = stockInfo[5]
                stockCash['private_out_cash'] = stockInfo[6]
                stockCash['private_net_cash'] = stockInfo[7]
                stockCash['private_net_rate'] = stockInfo[8]
                stockCash['total_cash']       = stockInfo[9]
                stockCash['name']             = stockInfo[12].decode('utf8')
                stockCash['date']             = stockInfo[13]
                #插入数据库
                self.__dbOperator.insertIntoDB(table, stockCash)

    '''获取股票交易信息明细'''
    def getStockQuotationDetail(self, dataUrl):
        tempData = self.__getDataFromUrl(dataUrl)

        if tempData == None:
            time.sleep(10)
            tempData = self.__getDataFromUrl(dataUrl)
            return False

        stockQuotation = {}
        stockInfo = tempData.split('~')
        if len(stockInfo) < 45: return
        if len(stockInfo) != 0 and stockInfo[0].find('pv_none') ==-1 and stockInfo[3].find('0.00') == -1:
            table = self.__stockTables['quotation']
            code = stockInfo[2]
            date = stockInfo[30]
            if not self.__isStockExitsInDate(table, code, date):
                stockQuotation['code']  = stockInfo[2]
                stockQuotation['name']  = stockInfo[1].decode('utf8')
                stockQuotation['price'] = stockInfo[3]
                stockQuotation['yesterday_close']   = stockInfo[4]
                stockQuotation['today_open']        = stockInfo[5]
                stockQuotation['volume']            = stockInfo[6]
                stockQuotation['outer_sell']        = stockInfo[7]
                stockQuotation['inner_buy']         = stockInfo[8]
                stockQuotation['buy_one']           = stockInfo[9]
                stockQuotation['buy_one_volume']    = stockInfo[10]
                stockQuotation['buy_two']           = stockInfo[11]
                stockQuotation['buy_two_volume']    = stockInfo[12]
                stockQuotation['buy_three']         = stockInfo[13]
                stockQuotation['buy_three_volume']  = stockInfo[14]
                stockQuotation['buy_four']          = stockInfo[15]
                stockQuotation['buy_four_volume']   = stockInfo[16]
                stockQuotation['buy_five']          = stockInfo[17]
                stockQuotation['buy_five_volume']   = stockInfo[18]
                stockQuotation['sell_one']          = stockInfo[19]
                stockQuotation['sell_one_volume']   = stockInfo[20]
                stockQuotation['sell_two']          = stockInfo[22]
                stockQuotation['sell_two_volume']   = stockInfo[22]
                stockQuotation['sell_three']        = stockInfo[23]
                stockQuotation['sell_three_volume'] = stockInfo[24]
                stockQuotation['sell_four']         = stockInfo[25]
                stockQuotation['sell_four_volume']  = stockInfo[26]
                stockQuotation['sell_five']         = stockInfo[27]
                stockQuotation['sell_five_volume']  = stockInfo[28]
                stockQuotation['datetime']          = stockInfo[30]
                stockQuotation['updown']            = stockInfo[31]
                stockQuotation['updown_rate']       = stockInfo[32]
                stockQuotation['heighest_price']    = stockInfo[33]
                stockQuotation['lowest_price']      = stockInfo[34]
                stockQuotation['volume_amout']      = stockInfo[35].split('/')[2]
                stockQuotation['turnover_rate']     = stockInfo[38]
                stockQuotation['pe_rate']           = stockInfo[39]
                stockQuotation['viberation_rate']   = stockInfo[42]
                stockQuotation['circulated_stock']  = stockInfo[43]
                stockQuotation['total_stock']       = stockInfo[44]
                stockQuotation['pb_rate']           = stockInfo[45]
                self.__dbOperator.insertIntoDB(table, stockQuotation)
    '''读取信息'''
    def __getDataFromUrl(self, dataUrl):
        r = urllib2.Request(dataUrl)
        try:
            stdout = urllib2.urlopen(r, data=None, timeout=3)
        except Exception,e:
            self.__logger.error(">>>>>> Exception: " +str(e))
            return None

        stdoutInfo = stdout.read().decode(codingtype).encode('utf-8')
        tempData = stdoutInfo.replace('"', '')
        self.__logger.debug(tempData)
        return tempData

    '''获取股票现金流量'''
    def getStockCash(self):
        self.__logger.debug("开始:收集股票现金流信息")
        try:
            #沪市股票
            for code in range(600001, 602100):
                dataUrl = "http://qt.gtimg.cn/q=ff_sh%d" % code
                self.__getStockCashDetail(dataUrl)

            #深市股票
            for code in range(1, 1999):
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d" % code
                self.__getStockCashDetail(dataUrl)

            #中小板股票
            for code in range(2001, 2999):
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d" % code
                self.__getStockCashDetail(dataUrl)

            #'300001' .. '300400'
            #创业板股票
            for code in range(300001, 300400):
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%d" % code
                self.__getStockCashDetail(dataUrl)

        except Exception as err:
            self.__logger.error(">>>>>> Exception: " +str(code) + " " + str(err))
        finally:
            None
        self.__logger.debug("结束：股票现金流收集")

    '''获取股票交易行情数据'''
    def getStockQuotation(self):
        self.__logger.debug("开始:收集股票交易行情数据")
        try:
            #沪市股票
            for code in range(600001, 602100):
                dataUrl = "http://qt.gtimg.cn/q=sh%d" % code
                self.getStockQuotationDetail(dataUrl)

            #深市股票
            for code in range(1, 1999):
                dataUrl = "http://qt.gtimg.cn/q=sz%06d" % code
                self.getStockQuotationDetail(dataUrl)

            #中小板股票
            for code in range(2001, 2999):
                dataUrl = "http://qt.gtimg.cn/q=sz%06d" % code
                self.getStockQuotationDetail(dataUrl)

            #'300001' .. '300400'
            #  创业板股票
            for code in range(300001, 300400):
                dataUrl = "http://qt.gtimg.cn/q=sz%d" % code
                self.getStockQuotationDetail(dataUrl)

        except Exception as err:
            self.__logger.error(">>>>>> Exception: " +str(code) + " " + str(err))
        finally:
            None
        self.__logger.debug("结束:收集股票交易行情数据")

if __name__ == '__main__':
    StockTencent(). main()