# -*- coding:utf-8 -*-
import re
import sys
import time
sys.path.append("..")
import JohhnsonUtil.commonTips as cct
import JohhnsonUtil.johnson_cons as ct
import JohhnsonUtil.LoggerFactory as LoggerFactory
import tdx_data_Day as tdd
log = LoggerFactory.getLogger("thsDataUtil")
# log.setLevel(LoggerFactory.INFO)
# log.setLevel(LoggerFactory.DEBUG)
import traceback
'''
涨跌幅:
desc:
http://q.10jqka.com.cn/interface/stock/gn/gainerzdf/desc/1/quote/quote
asc:
http://q.10jqka.com.cn/interface/stock/gn/gainerzdf/asc/1/quote/quote

净流入:
http://q.10jqka.com.cn/interface/stock/gn/jlr/desc/1/quote/quote
http://q.10jqka.com.cn/interface/stock/gn/jlr/desc/1/quote/quote

'''