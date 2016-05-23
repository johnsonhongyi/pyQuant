# -*- coding:utf-8 -*-
# !/usr/bin/env python

import gc
import random
import re
import sys
import time

import pandas as pd

import JohhnsonUtil.johnson_cons as ct
import LineHistogram as lhg
import singleAnalyseUtil as sl
from JSONData import powerCompute as pct
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd
from JohhnsonUtil import LoggerFactory as LoggerFactory
from JohhnsonUtil import commonTips as cct


if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))
    # StreamHandler(sys.stdout).push_application()
    log = LoggerFactory.getLogger('Autodata')
    # log.setLevel(LoggerFactory.DEBUG)
    # handler=StderrHandler(format_string='{record.channel}: {record.message) [{record.extra[cwd]}]')
    # log.level = log.debug
    # error_handler = SyslogHandler('Sina-M-Log', level='ERROR')

    try:
        if cct.get_work_day_status() and cct.get_now_time_int >1505 :
            tdx_data=tdd.get_tdx_all_day_DayL_DF(market='cyb', dayl=1)
            if len(tdx_data) < 1:
                raise KeyboardInterrupt("StopTime")
            else:
                print tdx_data[-2:]
            code='300366'
            
    except (KeyboardInterrupt) as e:
        pass    
    except (IOError, EOFError, Exception) as e:
        print "Error", e
        #traceback.print_exc()
        sleeptime=random.randint(5, 15)
        print "Error2sleep:%s"%(sleeptime)
        cct.sleep(sleeptime)

'''
{symbol:"sz000001",code:"000001",name:"平安银行",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"12.36",sell:"12.36",settlement:"12.34",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:7.133,pb:1.124,mktcap:17656906.355526,nmc:14566203.350486,turnoverratio:0},
{symbol:"sz000002",code:"000002",name:"万  科Ａ",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"0.00",sell:"0.00",settlement:"24.43",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:17.084,pb:3.035,mktcap:26996432.575,nmc:23746405.928119,turnoverratio:0},

python -m cProfile -s cumulative timing_functions.py
http://www.jb51.net/article/63244.htm

'''
