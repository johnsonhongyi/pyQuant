#-*- coding: UTF-8 -*-
'''
Created on 2015-3-1
@author: Casey
'''
import urllib
import re
import sys
# from setting import params
import urllib2
from DBOperator import *

dbOperator = DBOperator()
table = "stock_quote_yahoo"
'''查找指定日期股票流量'''
def isStockExitsInDate(table, stock, date):
    sql = "select * from " + table + " where code = '%d' and date='%s'" % (stock, date)
    n = dbOperator.execute(sql)
    if n >= 1:
        return True

def getHistoryStockData(code, dataurl):
    try:
        r = urllib2.request.Request(dataurl)
        try:
            stdout = urllib2.request.urlopen(r, data=None, timeout=3)
        except Exception as e:
            print (">>>>>> Exception: " +str(e))
            return None

        stdoutInfo = stdout.read().decode(params.codingtype).encode('utf-8')
        tempData = stdoutInfo.replace('"', '')
        stockQuotes = []
        if tempData.find('404') != -1:  stockQuotes = tempData.split("\n")

        stockDetail = {}
        for stockQuote in stockQuotes:
            stockInfo = stockQuote.split(",")
            if len(stockInfo) == 7 and stockInfo[0]!='Date':
                if not isStockExitsInDate(table, code, stockInfo[0]):
                   stockDetail["date"] = stockInfo[0]
                   stockDetail["open"]  = stockInfo[1]  #开盘
                   stockDetail["high"]    = stockInfo[2]  #最高
                   stockDetail["low"]    = stockInfo[3]  #最低
                   stockDetail["close"] = stockInfo[4]  #收盘
                   stockDetail["volume"] = stockInfo[5]  #交易量
                   stockDetail["adj_close"] = stockInfo[6] #收盘adj价格
                   stockDetail["code"] = code        #代码
                   dbOperator.insertIntoDB(table, stockDetail)
        result = tempData
    except Exception as err:
        print (">>>>>> Exception: " + str(dataurl) + " " + str(err))
    else:
        return result
    finally:
        None

def get_stock_history():
    #沪市2005-2015历史数据
    for code in range(601999, 602100):
        dataUrl = "http://ichart.yahoo.com/table.csv?s=%d.SS&a=01&b=01&c=2005&d=01&e=01&f=2015&g=d" % code
        print (getHistoryStockData(code, dataUrl ))


    #深市2005-2015历史数据
    for code in range(1, 1999):
        dataUrl = "http://ichart.yahoo.com/table.csv?s=%06d.SZ&a=01&b=01&c=2005&d=01&e=01&f=2015&g=d" % code
        print (getHistoryStockData(code, dataUrl))


    #中小板股票
    for code in range(2001, 2999):
        dataUrl = "http://ichart.yahoo.com/table.csv?s=%06d.SZ&a=01&b=01&c=2005&d=01&e=01&f=2015&g=d" % code
        print (getHistoryStockData(code, dataUrl))


    #创业板股票
    for code in range(300001, 300400):
        dataUrl = "http://ichart.yahoo.com/table.csv?s=%d.SZ&a=01&b=01&c=2005&d=01&e=01&f=2015&g=d" % code
        print (getHistoryStockData(code, dataUrl))


def main():
    "main function"

    dbOperator.connDB()
    get_stock_history()
    dbOperator.closeDB()

if __name__ == '__main__':
    main()