# -*- encoding: utf-8 -*-
# !/usr/bin/python
from __future__ import division

import os
import sys
sys.path.append("..")
import time
from struct import *
import numpy as np
import pandas as pd
from pandas import Series

from JSONData import realdatajson as rl
from JSONData import wencaiData as wcd
from JohhnsonUtil import LoggerFactory
from JohhnsonUtil import commonTips as cct
from JohhnsonUtil import johnson_cons as ct
import tushare as ts
import sina_data
# import numba as nb
# import datetime
# import logbook

# log=logbook.Logger('TDX_day')
log = LoggerFactory.getLogger('TDX_Day')
# log.setLevel(LoggerFactory.DEBUG)
# log.setLevel(LoggerFactory.INFO)
# log.setLevel(LoggerFactory.WARNING)
# log.setLevel(LoggerFactory.ERROR)

path_sep = os.path.sep
newdaysinit = 30
changedays=0
global initTdxdata,initTushareCsv
initTdxdata = 0
initTushareCsv = 0
atomStockSize = 50
# win7rootAsus = r'D:\Program Files\gfzq'
# win10Lengend = r'D:\Program\gfzq'
# win7rootXunji = r'E:\DOC\Parallels\WinTools\zd_pazq'
# win7rootList = [win7rootAsus,win7rootXunji,win10Lengend]
# macroot = r'/Users/Johnson/Documents/Johnson/WinTools/zd_pazq'
# xproot = r'E:\DOC\Parallels\WinTools\zd_pazq'

def get_tdx_dir():
    return cct.get_tdx_dir()
#     os_sys = cct.get_sys_system()
#     os_platform = cct.get_sys_platform()
#     if os_sys.find('Darwin') == 0:
#         log.info("DarwinFind:%s" % os_sys)
#         basedir = macroot.replace('/', path_sep).replace('\\',path_sep)
#         log.info("Mac:%s" % os_platform)

#     elif os_sys.find('Win') == 0:
#         log.info("Windows:%s" % os_sys)
#         if os_platform.find('XP') == 0:
#             log.info("XP:%s" % os_platform)
#             basedir = xproot.replace('/', path_sep).replace('\\',path_sep)  # 如果你的安装路径不同,请改这里
#         else:
#             log.info("Win7O:%s" % os_platform)
#             for root in win7rootList:
#                 basedir = root.replace('/', path_sep).replace('\\',path_sep)  # 如果你的安装路径不同,请改这里
#                 if os.path.exists(basedir):
#                     log.info("%s : path:%s" % (os_platform,basedir))
#                     break
#     if not os.path.exists(basedir):
#         log.error("basedir not exists")
#     return basedir

def get_tdx_dir_blocknew():
    return cct.get_tdx_dir_blocknew()
#     blocknew_path = get_tdx_dir() + r'/T0002/blocknew/'.replace('/', path_sep).replace('\\', path_sep)
#     return blocknew_path

basedir = get_tdx_dir()
blocknew = get_tdx_dir_blocknew()
# blocknew = r'/Users/Johnson/Documents/Johnson/WinTools/zd_pazq/T0002/blocknew'
# blocknew = 'Z:\Documents\Johnson\WinTools\zd_pazq\T0002\blocknew'
lc5_dir_sh = basedir + r'\Vipdoc\sh\fzline'
lc5_dir_sz = basedir + r'\Vipdoc\sz\fzline'
lc5_dir = basedir + r'\Vipdoc\%s\fzline'
day_dir = basedir + r'\Vipdoc\%s\lday/'
day_dir_sh = basedir + r'\Vipdoc\sh\lday/'
day_dir_sz = basedir + r'/Vipdoc/sz/lday/'
exp_path = basedir + "/T0002/export/".replace('/', path_sep).replace('\\', path_sep)
day_path = {'sh': day_dir_sh, 'sz': day_dir_sz}

# http://www.douban.com/note/504811026/
def get_code_file_path(code,type='f'):
    if code == None:
        raise Exception("code is None")
    # os.path.getmtime(ff)
    code_u = cct.code_to_symbol(code)
    if type == 'f':
        file_path = exp_path + 'forwardp' + path_sep + code_u.upper() + ".txt"
    elif type == 'b':
        file_path = exp_path + 'backp' + path_sep + code_u.upper() + ".txt"
    else:
        return None

    return file_path


# @nb.autojit
def get_tdx_Exp_day_to_df(code, start=None, end=None, dl=None,newdays = None,type='f'):
    start=cct.day8_to_day10(start)
    end=cct.day8_to_day10(end)
    if dl is not None and dl < 70:
        tdx_max_int = dl
    else:
        tdx_max_int = ct.tdx_max_int
    max_int_end = 3 if int(tdx_max_int) > 5 else int(tdx_max_int/2)
    if newdays is not None:
        newstockdayl = newdays
    else:
        newstockdayl = newdaysinit
    # day_path = day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
    code_u = cct.code_to_symbol(code)
    log.debug("code:%s code_u:%s" % (code, code_u))
    if type == 'f':
        file_path = exp_path + 'forwardp' + path_sep + code_u.upper() + ".txt"
    elif type == 'b':
        file_path = exp_path + 'backp' + path_sep + code_u.upper() + ".txt"
    else:
        return None
    # print file_path
    log.debug("daypath:%s" % file_path)
    # p_day_dir = day_path.replace('/', path_sep).replace('\\', path_sep)
    # p_exp_dir = exp_dir.replace('/', path_sep).replace('\\', path_sep)
    # print p_day_dir,p_exp_dir
    if not os.path.exists(file_path):
        # ds = Series(
        #     {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
        #      'vol': 0})
        global initTdxdata
        ds = pd.DataFrame()
        if initTdxdata == 0:
            log.error("file_path:not exists code:%s"%(code))
        initTdxdata += 1
        # ds.index = '2016-01-01'
        # ds = ds.fillna(0)
        return ds
    # ofile = open(file_path, 'rb')
    if start is None and dl is None:
        ofile = open(file_path, 'rb')
        buf = ofile.readlines()
        ofile.close()
        num = len(buf)
#        no = num - 1
        no = num
        dt_list = []
        for i in xrange(no):
            a = buf[i].split(',')
            # 01/15/2016,27.57,28.15,26.30,26.97,714833.15,1946604544.000
            # da=a[0].split('/')
            tdate = a[0]
            if len(tdate) != 10:
                continue
            # tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
            # tdate=dt.strftime('%Y-%m-%d')
            topen = float(a[1])
            thigh = float(a[2])
            tlow = float(a[3])
            tclose = float(a[4])
            # tvol = round(float(a[5]) / 10, 2)
            tvol = float(a[5])
            amount = round(float(a[6].replace('\r\n', '')), 1)  # int
            # tpre = int(a[7])  # back
            if int(topen) == 0 or int(amount) == 0:
                continue
            dt_list.append(
                {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose,
                 'amount': amount,
                 'vol': tvol})
            # if dt is not None and tdate < dt:
            #     break
        df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
        # df.sort_index(ascending=False, inplace=True)
        if start is not None and end is not None:
            df = df[(df.date >= start) & (df.date <= end)]
        elif end is not None:
            df = df[df.date <= end]
        elif start is not None:
            df = df[df.date >= start]
        # df['ma5d'] = df.close.rolling(window=5,center=False).mean()
        # df['ma10d'] = df.close.rolling(window=10,center=False).mean()
        # df['ma20d'] = df.close.rolling(window=20,center=False).mean()
        # df['ma60d'] = df.close.rolling(window=60,center=False).mean()
        if len(df) > 0:
            df.drop_duplicates('date',inplace=True)
            df = df.set_index('date')
            df = df.sort_index(ascending=True)
            df['ma5d'] = pd.rolling_mean(df.close,5)
            df['ma10d'] = pd.rolling_mean(df.close,10)
            df['ma20d'] = pd.rolling_mean(df.close,20)
            df['ma60d'] = pd.rolling_mean(df.close,60)
            # df['hmax'] = df.high[-tdx_max_int:].max()
            df['hmax'] = df.close[-tdx_max_int:-max_int_end].max()
            df['lmin'] = df.low[-tdx_max_int:-max_int_end].min()
            df['cmean'] = df.close[-tdx_max_int:-max_int_end].mean()
            df = df.fillna(0)
            df = df.sort_index(ascending=False)
        return df
    elif dl is not None and int(dl) == 1:
        fileSize = os.path.getsize(file_path)
        if fileSize < atomStockSize * newstockdayl:
            return Series()
        data = cct.read_last_lines(file_path, int(dl) + 3)
        data_l = data.split('\n')
        dt_list = Series()
        data_l.reverse()
        log.debug("day 1:%s"%data_l)
        for line in data_l:
            a = line.split(',')
            # 01/15/2016,27.57,28.15,26.30,26.97,714833.15,1946604544.000
            # da=a[0].split('/')
            log.debug("day 1 len(a):%s a:%s"%(len(a),a))
            if len(a) == 7:
                tdate = a[0]
                if len(tdate) !=10:
                    continue
                log.debug("day 1 tdate:%s"%tdate)
                # tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
                # tdate=dt.strftime('%Y-%m-%d')
                topen = float(a[1])
                thigh = float(a[2])
                tlow = float(a[3])
                tclose = float(a[4])
                # tvol = round(float(a[5]) / 10, 2)
                tvol = float(a[5])
                amount = round(float(a[6].replace('\r\n', '')), 1)  # int
                # tpre = int(a[7])  # back
                if int(topen) == 0 or int(amount) == 0:
                    continue
                dt_list = Series(
                    {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose,
                     'amount': amount,
                     'vol': tvol})
                break
            else:
                continue
                # if dt is not None and tdate < dt:
                #     break
        # df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
        # df = df.set_index('date')
        return dt_list

    else:
        fileSize = os.path.getsize(file_path)
        # if dl  is  None:
        #     newstockdayl = 30
        #     # print "60"
        # else:
        #     newstockdayl = 60
        if fileSize < atomStockSize * newstockdayl:
            return Series()
        if start is None:
            if dl is None:
                dl = 60
        else:
            dl = int(cct.get_today_duration(start) * 5 / 7)
            log.debug("start:%s dl:%s"%(start,dl))
        data = cct.read_last_lines(file_path, int(dl) + 5)
        dt_list = []
        data_l = data.split('\n')
        data_l.reverse()
        for line in data_l:
            a = line.split(',')
            # 01/15/2016,27.57,28.15,26.30,26.97,714833.15,1946604544.000
            # da=a[0].split('/')
            if len(a) == 7:
                tdate = a[0]
                if len(tdate) !=10:
                    continue
                # tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
                # tdate=dt.strftime('%Y-%m-%d')
                topen = float(a[1])
                thigh = float(a[2])
                tlow = float(a[3])
                tclose = float(a[4])
                tvol = round(float(a[5]), 2)
                amount = round(float(a[6].replace('\r\n', '')), 1)  # int
                # tpre = int(a[7])  # back
                if int(topen) == 0 or int(amount) == 0:
                    continue
                dt_list.append(
                    {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose,
                     'amount': amount,
                     'vol': tvol})
            else:
                continue
                # if dt is not None and tdate < dt:
                #     break
        df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
        # df.sort_index(ascending=False, inplace=True)
        if start is not None and end is not None:
            df = df[(df.date >= start) & (df.date <= end)]
            # print df
        elif end is not None:
            df = df[df.date <= end]
        elif start is not None:
            df = df[df.date >= start]
#        print start,dl,len(df)
        if len(df) > 0:
            df.drop_duplicates('date',inplace=True)
            df = df.set_index('date')
            df = df.sort_index(ascending=True)
            df['ma5d'] = pd.rolling_mean(df.close,5)
            df['ma10d'] = pd.rolling_mean(df.close,10)
            df['ma20d'] = pd.rolling_mean(df.close,20)
            df['ma60d'] = pd.rolling_mean(df.close,60)
            # df['hmax'] = df.high[-tdx_max_int:].max()
            df['hmax'] = df.close[-tdx_max_int:-max_int_end].max()
            df['lmin'] = df.low[-tdx_max_int:-max_int_end].min()
            df['cmean'] = df.close[-tdx_max_int:-max_int_end].mean()
            df = df.fillna(0)
            df = df.sort_index(ascending=False)
        return df


INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sz399300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006'}


# def get_tdx_append_now_df_api(code, start=None, end=None, type='f'):

#     # start=cct.day8_to_day10(start)
#     # end=cct.day8_to_day10(end)
#     # print start,end
#     df = get_tdx_Exp_day_to_df(code, type, start, end).sort_index(ascending=True)
#     # print df.index.values[:1],df.index.values[-1:]
#     today = cct.get_today()

#     if len(df) > 0:
#         tdx_last_day = df.index[-1]
#     else:
#         tdx_last_day = start
#     duration = cct.get_today_duration(tdx_last_day)
#     log.debug("duration:%s"%duration)
#     log.debug("tdx_last_day:%s" % tdx_last_day)
#     index_status = False
#     code_t=None
#     if code == '999999':
#         code = 'sh'
#         index_status = True
#     elif code.startswith('399'):
#         index_status = True
#         for k in INDEX_LIST.keys():
#             if INDEX_LIST[k].find(code) > 0:
#                 code = k
#     log.debug("duration:%s" % duration)
#     if end is not None:
#         # print end,df.index[-1]
#         if len(df)==0:
#             return df
#         if end <= df.index[-1]:
#             # print(end, df.index[-1])
#             # return df
#             duration = 0
#         else:
#             today = end

#     if duration >= 1:
#         if index_status:
#             code_t = INDEX_LIST[code][2:]
#         try:
#             ds = ts.get_hist_data(code, start=tdx_last_day, end=today)
#             # ds = ts.get_h_data('000001', start=tdx_last_day, end=today,index=index_status)
#             # df.index = pd.to_datetime(df.index)
#         except (IOError, EOFError, Exception) as e:
#             print "Error Duration:", e
#             cct.sleep(2)
#             ds = ts.get_h_data(code_t, start=tdx_last_day, end=today, index=index_status)
#             df.index = pd.to_datetime(df.index)
#         if ds is not None and len(ds) > 1:
#             if len(df) > 0:
#                 lends = len(ds)
#             else:
#                 lends = len(ds) + 1
#             ds = ds[:lends - 1]
#             if index_status:
#                 if code == 'sh':
#                     code = '999999'
#                 else:
#                     code = code_t
#                 ds['code'] = code
#             else:
#                 ds['code'] = code
#             # ds['vol'] = 0
#             ds = ds.loc[:, ['code', 'open', 'high', 'low', 'close', 'volume', 'amount']]
#             # ds.rename(columns={'volume': 'amount'}, inplace=True)
#             ds.rename(columns={'volume': 'vol'}, inplace=True)
#             ds.sort_index(ascending=True, inplace=True)
#             log.debug("ds:%s" % ds[:1])
#             df = df.append(ds)
#             # pd.concat([df,ds],axis=0, join='outer')
#             # result=pd.concat([df,ds])

#         if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 1510:
#             log.debug("get_work_time:work")
#             if end is None:
#                 # dm = rl.get_sina_Market_json('all').set_index('code')
#                 if index_status:
#                     log.debug("code:%s code_t:%s"%(code,code_t))
#                     dm = sina_data.Sina().get_stock_code_data(code_t,index=index_status)
#                     dm.code = code
#                     dm = dm.set_index('code')
#                 else:
#                     dm = sina_data.Sina().get_stock_code_data(code,index=index_status).set_index('code')
#                 log.debug("dm:%s now:%s"%(len(dm),dm))
#                 if dm is not None and df is not None and not dm.empty  and not df.empty:
#                     # dm=dm.drop_duplicates()
#                     # log.debug("not None dm:%s" % dm[-1:])
#                     dm.rename(columns={'volume': 'amount', 'turnover': 'vol'}, inplace=True)
#                     c_name=dm.loc[code,['name']].values[0]
#                     dm_code = (dm.loc[:, ['open', 'high', 'low', 'close', 'amount','vol']])
#                     log.debug("dm_code:%s" % dm_code)
#                     dm_code['amount'] = round(float(dm_code['amount']) / 100, 2)
#                     dm_code['code'] = code
#                     # dm_code['vol'] = 0
#                     dm_code['date']=today
#                     dm_code = dm_code.set_index('date')
#                     # dm_code.name = today
#                     # log.debug("dm_code_index:%s"%(dm_code))
#                     log.debug("df.open:%s dm.open%s"%(df.open[-1],round(dm.open[-1],2)))

#                     if df.open[-1] != round(dm.open[-1],2):
#                         df = df.append(dm_code)
#                     df['name']=c_name
#                     log.debug("c_name:%s df.name:%s"%(c_name,df.name[-1]))
#                     # log.debug("df[-3:]:%s" % (df[-2:]))
#                     # df['name'] = dm.loc[code, 'name']

#     if not 'name' in df.columns:
#         if index_status:
#             if code_t is None:
#                 code_t = INDEX_LIST[code][2:]
#             log.debug("code:%s code_t:%s"%(code,code_t))
#             dm = sina_data.Sina().get_stock_code_data(code_t,index=index_status)
#             dm.code = code
#             dm = dm.set_index('code')
#         else:
#             dm = sina_data.Sina().get_stock_code_data(code,index=index_status).set_index('code')
#         log.debug("dm:%s now:%s"%(len(dm),dm))
#         if dm is not None and not dm.empty:
#             c_name=dm.loc[code,['name']].values[0]
#             df['name']=c_name
#             log.debug("c_name:%s df.name:%s"%(c_name,df.name[-1:]))
#         log.debug("df:%s" % df[-3:])
#         # print df
#     # return df

def get_tdx_append_now_df_api(code, start=None, end=None, type='f',df=None,dm=None,dl=None,power=True,newdays=None):

    start=cct.day8_to_day10(start)
    end=cct.day8_to_day10(end)

    if df is None:
        df = get_tdx_Exp_day_to_df(code, start=start, end=end,dl=dl,newdays=newdays).sort_index(ascending=True)
    else:
        df = df.sort_index(ascending=True)
    index_status = False
    code_t=code
    if code == '999999':
        # code_t=code
        code = 'sh'
        index_status = True
    elif code.startswith('399'):
        index_status = True
        for k in INDEX_LIST.keys():
            if INDEX_LIST[k].find(code) > 0:
                code = k
    if index_status:
        df[code] = code_t
        # code = code_t
    if not power:
        return df


    today = cct.get_today()
    if len(df) > 0 :
        tdx_last_day = df.index[-1]
    else:
        if start is not None:
            tdx_last_day = start
        else:
            tdx_last_day = None
#            log.warn("code :%s start is None and DF is None"%(code))
    if tdx_last_day is not None:
        duration = cct.get_today_duration(tdx_last_day)
    else:
        duration = 1
    log.debug("duration:%s"%duration)
    log.debug("tdx_last_day:%s" % tdx_last_day)
    log.debug("duration:%s" % duration)
    if end is not None:
        # print end,df.index[-1]
        if len(df)==0:
            return df
        if end <= df.index[-1]:
            # print(end, df.index[-1])
            # return df
            duration = 0
        else:
            today = end
#    print cct.last_tddate(duration)
#    if duration >= 1 and (tdx_last_day != cct.last_tddate(1) or cct.get_now_time_int() > 1530):
    if duration > 1 and (tdx_last_day != cct.last_tddate(1)):
        import urllib2
        if index_status:
            code_t = INDEX_LIST[code][2:]
        try:
            ds = ts.get_hist_data(code, start=tdx_last_day, end=today)
            ds['volume']=ds.volume.apply(lambda x: x * 100)
            # ds = ts.get_h_data('000001', start=tdx_last_day, end=today,index=index_status)
            # df.index = pd.to_datetime(df.index)
        except (IOError, EOFError, Exception,urllib2.URLError) as e:
            print "Error Duration:", e,
            print "code:%s"%(code)
            cct.sleep(0.1)
            ds = ts.get_h_data(code_t, start=tdx_last_day, end=today, index=index_status)
            df.index = pd.to_datetime(df.index)
        if ds is not None and len(ds) > 1:
            if len(df) > 0:
                lends = len(ds)
            else:
                lends = len(ds) + 1
            ds = ds[:lends - 1]
            if index_status:
                if code == 'sh':
                    code_ts = '999999'
                else:
                    code_ts = code_t
                ds['code'] = int(code_ts)
            else:
                ds['code'] = code
            # print ds[:1]
#            ds['volume']=ds.volume.apply(lambda x: x * 100)
            if not 'amount' in ds.columns:
                ds['amount']=map(lambda x,y,z:round((y+z)/2*x,2),ds.volume,ds.high,ds.low)
            ds = ds.loc[:, ['code', 'open', 'high', 'low', 'close', 'volume', 'amount']]
            # ds.rename(columns={'volume': 'amount'}, inplace=True)
            ds.rename(columns={'volume': 'vol'}, inplace=True)
            ds.sort_index(ascending=True, inplace=True)
            # log.debug("ds:%s" % ds[:1])
            ds = ds.fillna(0)
            df = df.append(ds)
            if (len(ds) == 1 and ds.index.values[0] != cct.get_today()) or len(ds) > 1:
                if index_status:
                    sta=write_tdx_tushare_to_file(code_ts,df=df)
                else:
                    sta=write_tdx_tushare_to_file(code,df=df)
#            if not sta:
#                log.warn("write %s error."%(code))
    if cct.get_now_time_int() > 830 and cct.get_now_time_int() < 930:
        log.debug("now > 830 and <930 return")
        df = df.sort_index(ascending=True)
        df['ma5d'] = pd.rolling_mean(df.close,5)
        df['ma10d'] = pd.rolling_mean(df.close,10)
        df['ma20d'] = pd.rolling_mean(df.close,20)
        df['ma60d'] = pd.rolling_mean(df.close,60)
        df=df.fillna(0)
        df = df.sort_index(ascending=False)
        return df
#    print df.index.values,code
    if dm is None and end is None:
        # if dm is None and today != df.index[-1]:
        # log.warn('today != end:%s'%(df.index[-1]))
        if index_status:
            log.debug("code:%s code_t:%s" % (code, code_t))
            if code_t is None:
                code_t = INDEX_LIST[code][2:]

            dm = sina_data.Sina().get_stock_code_data(code_t,index=index_status)
            dm.code = code
            dm = dm.set_index('code')
        else:
            dm = sina_data.Sina().get_stock_code_data(code).set_index('code')
    if duration == 0:
        writedm = False
    else:
        writedm = True
    if df is not None and len(df) >0:
        if df.index.values[-1] == today:
            if dm is not None and not isinstance(dm,Series):
                dz = dm.loc[code].to_frame().T
            if index_status:
                vol_div = 1000
            else:
                vol_div = 10
            if dz.open.values == df.open[-1] and 'volume' in dz.columns and int(df.vol[-1]/vol_div) == int(dz.volume.values/vol_div):
                df = df.sort_index(ascending=True)
                df['ma5d'] = pd.rolling_mean(df.close,5)
                df['ma10d'] = pd.rolling_mean(df.close,10)
                df['ma20d'] = pd.rolling_mean(df.close,20)
                df['ma60d'] = pd.rolling_mean(df.close,60)
                df=df.fillna(0)
                df = df.sort_index(ascending=False)
                return df
            else:
                writedm = True

    if not writedm and cct.get_now_time_int() > 1530 or cct.get_now_time_int() < 925:
        return df

    if dm is not None and df is not None and not dm.empty and len(df) >0:
        dm.rename(columns={'volume': 'vol', 'turnover': 'amount'}, inplace=True)
        # dm.rename(columns={'volume': 'amount', 'turnover': 'vol'}, inplace=True)
        c_name = dm.loc[code, ['name']].values[0]
#        dm_code = (dm.loc[:, ['open', 'high', 'low', 'close', 'amount', 'vol']])
        dm_code = (dm.loc[code, ['open', 'high', 'low', 'close', 'amount', 'vol']]).to_frame().T
        log.debug("dm_code:%s" % dm_code)
        # dm_code['amount'] = round(float(dm_code['amount']), 2)
        if index_status:
            if code == 'sh':
                code_ts = '999999'
            else:
                code_ts = code_t
            dm_code['code'] = code_ts
        else:
            dm_code['code'] = code
        dm_code['date'] = today
        dm_code = dm_code.set_index('date')
        # log.debug("df.open:%s dm.open%s" % (df.open[-1], round(dm.open[-1], 2)))
        # print df.close[-1],round(dm.close[-1],2)
        if end is None and ((df is not None and df.empty) or (round(df.open[-1],2) != round(dm.open[-1], 2)) or (round(df.close[-1],2) != round(dm.close[-1],2))):
            if dm.open[0] > 0 and len(df) >0:
                if dm_code.index == df.index[-1]:
                    log.debug("app_api_dm.Index:%s df:%s"%(dm_code.index.values,df.index[-1]))
                    df = df.drop(dm_code.index)
                df = df.append(dm_code)
                # df = df.astype(float)
            # df=pd.concat([df,dm],axis=0, ignore_index=True).set
        df['name'] = c_name
        log.debug("c_name:%s df.name:%s" % (c_name, df.name[-1]))

        # if not 'name' in df.columns:
        #     if index_status:
        #         if code_t is None:
        #             code_t = INDEX_LIST[code][2:]
        #         log.debug("code:%s code_t:%s"%(code,code_t))
        #         dm = sina_data.Sina().get_stock_code_data(code_t,index=index_status)
        #         dm.code = code
        #         dm = dm.set_index('code')
        #     else:
        #         dm = sina_data.Sina().get_stock_code_data(code,index=index_status).set_index('code')
        #     log.debug("dm:%s now:%s"%(len(dm),dm))
        #     if dm is not None and not dm.empty:
        #         c_name=dm.loc[code,['name']].values[0]
        #         df['name']=c_name
        #         log.debug("c_name:%s df.name:%s"%(c_name,df.name[-1:]))
        #     log.debug("df:%s" % df[-3:])
        # print df
    if len(df) > 0:
        df = df.sort_index(ascending=True)
        df['ma5d'] = pd.rolling_mean(df.close,5)
        df['ma10d'] = pd.rolling_mean(df.close,10)
        df['ma20d'] = pd.rolling_mean(df.close,20)
        df['ma60d'] = pd.rolling_mean(df.close,60)
        df=df.fillna(0)
        df = df.sort_index(ascending=False)
    if end is None and writedm and len(df) > 0:
        if cct.get_now_time_int() < 900 or cct.get_now_time_int() > 1505:
            if index_status:
                if code == 'sh':
                    code_ts = '999999'
                else:
                    code_ts = code_t
                sta=write_tdx_sina_data_to_file(code_ts,df=df)
            else:
                sta=write_tdx_sina_data_to_file(code,df=df)

    return df


def get_tdx_append_now_df_api_tofile(code,dm=None,newdays=1, start=None, end=None, type='f',df=None,dl=2,power=True):

    start=cct.day8_to_day10(start)
    end=cct.day8_to_day10(end)

    if df is None:
        df = get_tdx_Exp_day_to_df(code, start=start, end=end,dl=dl,newdays=newdays).sort_index(ascending=True)
    else:
        df = df.sort_index(ascending=True)
    index_status = False
    code_t=code
    if code == '999999':
        # code_t=code
        code = 'sh'
        index_status = True
    elif code.startswith('399'):
        index_status = True
        for k in INDEX_LIST.keys():
            if INDEX_LIST[k].find(code) > 0:
                code = k
    if index_status:
        df[code] = code_t
        # code = code_t
    if not power:
        return df


    today = cct.get_today()
    if len(df) > 0 :
        tdx_last_day = df.index[-1]
    else:
        if start is not None:
            tdx_last_day = start
        else:
            tdx_last_day = None
#            log.warn("code :%s start is None and DF is None"%(code))
    if tdx_last_day is not None:
        duration = cct.get_today_duration(tdx_last_day)
    else:
        duration = 1
    log.debug("duration:%s"%duration)
    log.debug("tdx_last_day:%s" % tdx_last_day)
    log.debug("duration:%s" % duration)
    if end is not None:
        # print end,df.index[-1]
        if len(df)==0:
            return df
        if end <= df.index[-1]:
            # print(end, df.index[-1])
            # return df
            duration = 0
        else:
            today = end
#    print cct.last_tddate(duration)
#    if duration >= 1 and (tdx_last_day != cct.last_tddate(1) or cct.get_now_time_int() > 1530):
    if duration > 1 and (tdx_last_day != cct.last_tddate(1)):
        if index_status:
            code_t = INDEX_LIST[code][2:]
        try:
            ds = ts.get_hist_data(code, start=tdx_last_day, end=today)
            if ds is None:
                return df
            ds['volume']=ds.volume.apply(lambda x: x * 100)
            # ds = ts.get_h_data('000001', start=tdx_last_day, end=today,index=index_status)
            # df.index = pd.to_datetime(df.index)
        except (IOError, EOFError, Exception) as e:
            print "Error Duration:", e,
            print "code:%s"%(code)
            cct.sleep(0.1)
            ds = ts.get_h_data(code_t, start=tdx_last_day, end=today, index=index_status)
            df.index = pd.to_datetime(df.index)
        if ds is not None and len(ds) >= 1:
            if len(df) > 0:
                lends = len(ds)
            else:
                lends = len(ds) + 1
            ds = ds[:lends - 1]
            if index_status:
                if code == 'sh':
                    code_ts = '999999'
                else:
                    code_ts = code_t
                ds['code'] = int(code_ts)
            else:
                ds['code'] = code
            # print ds[:1]
#            ds['volume']=ds.volume.apply(lambda x: x * 100)
            if not 'amount' in ds.columns:
                ds['amount']=map(lambda x,y,z:round((y+z)/2*x,2),ds.volume,ds.high,ds.low)
            ds = ds.loc[:, ['code', 'open', 'high', 'low', 'close', 'volume', 'amount']]
            # ds.rename(columns={'volume': 'amount'}, inplace=True)
            ds.rename(columns={'volume': 'vol'}, inplace=True)
            ds.sort_index(ascending=True, inplace=True)
            # log.debug("ds:%s" % ds[:1])
            ds = ds.fillna(0)
            df = df.append(ds)
            if (len(ds) == 1 and ds.index.values[0] != cct.get_today()) or len(ds) > 1:
                if index_status:
                    sta=write_tdx_tushare_to_file(code_ts,df=df)
                else:
                    sta=write_tdx_tushare_to_file(code,df=df)
#            if not sta:
#                log.warn("write %s error."%(code))
    if cct.get_now_time_int() > 900 and cct.get_now_time_int() < 930 and len(df) > 0:
        log.debug("now > 830 and <930 return")
        df = df.sort_index(ascending=True)
        df['ma5d'] = pd.rolling_mean(df.close,5)
        df['ma10d'] = pd.rolling_mean(df.close,10)
        df['ma20d'] = pd.rolling_mean(df.close,20)
        df['ma60d'] = pd.rolling_mean(df.close,60)
        df=df.fillna(0)
        df = df.sort_index(ascending=False)
        return df
#    print df.index.values,code
    if dm is None and end is None:
        # if dm is None and today != df.index[-1]:
        # log.warn('today != end:%s'%(df.index[-1]))
        if index_status:
            log.debug("code:%s code_t:%s" % (code, code_t))
            if code_t is None:
                code_t = INDEX_LIST[code][2:]

            dm = sina_data.Sina().get_stock_code_data(code_t,index=index_status)
            dm.code = code
            dm = dm.set_index('code')
        else:
            dm = sina_data.Sina().get_stock_code_data(code).set_index('code')
    if len(df) !=0 and duration == 0:
        writedm = False
    else:
        writedm = True
    if df is not None and len(df) >0:
        if df.index.values[-1] == today:
            if dm is not None and not isinstance(dm,Series):
                dz = dm.loc[code].to_frame().T
            if index_status:
                vol_div = 1000
            else:
                vol_div = 10
            if round(dz.open.values,1) == round(df.open[-1],1) and 'volume' in dz.columns and int(df.vol[-1]/vol_div) == int(dz.volume.values/vol_div):
                df = df.sort_index(ascending=True)
                df['ma5d'] = pd.rolling_mean(df.close,5)
                df['ma10d'] = pd.rolling_mean(df.close,10)
                df['ma20d'] = pd.rolling_mean(df.close,20)
                df['ma60d'] = pd.rolling_mean(df.close,60)
                df=df.fillna(0)
                df = df.sort_index(ascending=False)
                return df
            else:
                writedm = True

    if not writedm and cct.get_now_time_int() > 1530 or cct.get_now_time_int() < 925:
        return df

#    if dm is not None and df is not None and not dm.empty and len(df) >0:
    if dm is not None and not dm.empty :
        dm.rename(columns={'volume': 'vol', 'turnover': 'amount'}, inplace=True)
        # dm.rename(columns={'volume': 'amount', 'turnover': 'vol'}, inplace=True)
        c_name = dm.loc[code, ['name']].values[0]
        dm_code = (dm.loc[code, ['open', 'high', 'low', 'close', 'amount', 'vol']]).to_frame().T
        log.debug("dm_code:%s" % dm_code)
        # dm_code['amount'] = round(float(dm_code['amount']), 2)
        if index_status:
            if code == 'sh':
                code_ts = '999999'
            else:
                code_ts = code_t
            dm_code['code'] = code_ts
        else:
            dm_code['code'] = code
        dm_code['date'] = today
        dm_code = dm_code.set_index('date')
        # log.debug("df.open:%s dm.open%s" % (df.open[-1], round(dm.open[-1], 2)))
        # print df.close[-1],round(dm.close[-1],2)
        if end is None and ((df is not None and df.empty) or (round(df.open[-1],2) != round(dm.open[-1], 2)) or (round(df.close[-1],2) != round(dm.close[-1],2))):
            if dm.open[0] > 0 and len(df) >0:
                if dm_code.index[-1] == df.index[-1]:
                    log.debug("app_api_dm.Index:%s df:%s"%(dm_code.index.values,df.index[-1]))
                    df = df.drop(dm_code.index)
                df = df.append(dm_code)
            elif len(dm) != 0  and len(df) == 0:
                df = dm_code
                # df = df.astype(float)
            # df=pd.concat([df,dm],axis=0, ignore_index=True).set
        df['name'] = c_name
        log.debug("c_name:%s df.name:%s" % (c_name, df.name[-1]))

    if len(df) > 5:
        df = df.sort_index(ascending=True)
        df['ma5d'] = pd.rolling_mean(df.close,5)
        df['ma10d'] = pd.rolling_mean(df.close,10)
        df['ma20d'] = pd.rolling_mean(df.close,20)
        df['ma60d'] = pd.rolling_mean(df.close,60)
        df=df.fillna(0)
        df = df.sort_index(ascending=False)
    if writedm and len(df) > 0:
        if cct.get_now_time_int() < 900 or cct.get_now_time_int() > 1505:
            if index_status:
                sta=write_tdx_sina_data_to_file(code_ts,df=df)
            else:
                sta=write_tdx_sina_data_to_file(code,df=df)

    return df

def write_tdx_tushare_to_file(code,df=None,start=None,type='f'):
#    st=time.time()
#    pname = 'sdata/SH601998.txt'
    if df is None:
        ldatedf = get_tdx_Exp_day_to_df(code,dl=1)
        if len(ldatedf) > 0:
            lastd = ldatedf.date
        else:
            return False
        # today = cct.get_today()
        # duration = cct.get_today_duration(tdx_last_day)
        if lastd == cct.last_tddate(1):
            return False
        df = get_tdx_append_now_df_api(code,start=start)

    if len(df) == 0:
        return False
    code_u = cct.code_to_symbol(code)
    log.debug("code:%s code_u:%s" % (code, code_u))
    if type == 'f':
        file_path = exp_path + 'forwardp' + path_sep + code_u.upper() + ".txt"
    elif type == 'b':
        file_path = exp_path + 'backp' + path_sep + code_u.upper() + ".txt"
    else:
        return None

    fsize = os.path.getsize(file_path)
    limitpo = fsize if fsize < 150 else 150

    if not os.path.exists(file_path) or os.path.getsize(file_path) < limitpo:
#        log.warn("not path:%s"%(file_path))
        return False
#    else:
#        print "no"

#    print file_path
    fo = open(file_path, "r+")
#    os.path.getsize(file_path)
#    print fo.tell()
#    fo.seek(-limitpo,2)
#    print fo.readlines()

    fo.seek(-limitpo,2)
    plist=[]
    line = True
    while line:
        tmpo=fo.tell()
        line=fo.readline()
        alist = line.split(',')
        if len(alist) == 7 :
            if len(alist[0]) !=10 :
                continue
            tvol = round(float(alist[5]),0)
            tamount = round(float(alist[6].replace('\r\n', '')),0)
#            print int(tamount)
            if fsize > 600 and (int(tvol) == 0 or int(tamount) == 0):
                continue
#            print line,tmpo
            if tmpo not in plist:
                plist.append(tmpo)
#                break
    if len(plist) == 0:
        raise Exception("data position is None")
    po=plist[-1]
    fo.seek(po)
    dater= fo.read(10)
    df = df[df.index >= dater]
    if len(df) >= 1:
        df=df.fillna(0)
        df.sort_index(ascending=True,inplace=True)
        fo.seek(po)
        for date in df.index:
            td=df.loc[date,['open','high','close','low','vol','amount']]
            if td.open > 0 and td.high > 0 and td.low > 0 and td.close >0:
                tdate = str(date)[:10]
                topen = str(td.open)
                thigh = str(td.high)
                tlow = str(td.low)
                tclose = str(td.close)
                # tvol = round(float(a[5]) / 10, 2)
                tvol = str(td.vol)
                amount = str(td.amount)
                tdata = tdate+','+topen+','+thigh+','+tlow+','+tclose+','+tvol+','+amount+'\r\n'
                fo.write(tdata)
        fo.close()
        return True
    fo.close()
    return "NTrue"

def write_tdx_sina_data_to_file(code,dm=None,df=None,dl=2,type='f'):
#    ts=time.time()
#    if dm is None:
#        dm = get_sina_data_df(code)
#    if df is None:
#        dz = dm.loc[code].to_frame().T
#        df = get_tdx_append_now_df_api2(code,dl=dl,dm=dz,newdays=5)

#    if df is None or len(df) == 0:
#        return False
    code_u = cct.code_to_symbol(code)
    log.debug("code:%s code_u:%s" % (code, code_u))
    if type == 'f':
        file_path = exp_path + 'forwardp' + path_sep + code_u.upper() + ".txt"
    elif type == 'b':
        file_path = exp_path + 'backp' + path_sep + code_u.upper() + ".txt"
    else:
        return None



    if not os.path.exists(file_path) and len(df) > 0:
        fo = open(file_path, "w+")
#        return False
    else:
        fo = open(file_path, "r+")

    fsize = os.path.getsize(file_path)
    limitpo = fsize if fsize < 150 else 150

    if limitpo > 40:
        fo.seek(-limitpo,2)
        plist=[]
        line = True
        while line:
            tmpo=fo.tell()
            line=fo.readline()
            alist = line.split(',')
            if len(alist) == 7 :
                if len(alist[0]) !=10 :
                    continue
                tvol = round(float(alist[5]),0)
                tamount = round(float(alist[6].replace('\r\n', '')),0)
    #            print int(tamount)
                if fsize > 600 and (int(tvol) == 0 or int(tamount) == 0):
                    continue
    #            print line,tmpo
                if tmpo not in plist:
                    plist.append(tmpo)
    #                break
        if len(plist) == 0:
            raise Exception("data position is None")
        po=plist[-1]
        fo.seek(po)
        dater= fo.read(10)
        df = df[df.index >= dater]

    if len(df) >= 1:
        df=df.fillna(0)
        df.sort_index(ascending=True,inplace=True)
        if limitpo > 40:
            fo.seek(po)
        for date in df.index:
            td=df.loc[date,['open','high','close','low','vol','amount']]
            tdate = date
            if len(tdate) !=10:
                continue
            topen = str(td.open)
            thigh = str(td.high)
            tlow = str(td.low)
            tclose = str(td.close)
            # tvol = round(float(a[5]) / 10, 2)
            tvol = str(td.vol)
            amount = str(td.amount)
            tdata = tdate+','+topen+','+thigh+','+tlow+','+tclose+','+tvol+','+amount+'\r\n'
            fo.write(tdata)
        fo.close()
        return True
    fo.flush()
    fo.close()
    return "NTrue"

def Write_market_all_day_mp(market='all'):
    sh_index = '601998'
    dd = get_tdx_Exp_day_to_df(sh_index,dl=1)
    # print dt,dd.date
    if len(dd) > 0:
        duration = cct.get_today_duration(dd.date)
        if duration == 0:
            print "Duration:%s is OK"%(duration)
            return False

        # fpath =  get_code_file_path(sh_index)
        # mtime = os.path.getmtime(fpath)
        # dt = cct.get_time_to_date(mtime,'%Y-%m-%d')
        # if dt == dd.date:
        #     hs = cct.get_time_to_date(mtime,'%H%M')
        #     # print hs
        #     if hs > 1500:
        #         print "Data is out:%s"%(dd.close)
        #         return False


    # import sys;sys.exit(0)
    # start=dd.date
    # index_ts = ts.get_hist_data('sh',start=start)
    if market == 'all':
        mlist = ['sh','sz']
    else:
        mlist =[market]
    # if len(index_ts) > 1:
    #     print "start:%s"%(start),
    result =[]
    for mk in mlist:
        time_t = time.time()
        df = rl.get_sina_Market_json(mk)
        df = df[df.buy > 0]
        print ("market:%s A:%s"%(mk,len(df))),
        code_list = df.code.tolist()
        dm = get_sina_data_df(code_list)
        log.info('code_list:%s' % len(code_list))
    #        write_tdx_tushare_to_file(sh_index,index_ts)
#        get_tdx_append_now_df_api2(code,dl=dl,dm=dz,newdays=5)
        results = cct.to_mp_run_async(get_tdx_append_now_df_api_tofile,code_list,dm,5)
        # for code in code_list:
        #    print "code:%s "%(code),
        #    res=get_tdx_append_now_df_api_tofile(code,dm,5)
           # print "status:%s"%(res)
        #            results.append(res)
        print "t:",round(time.time() - time_t,2)
#        result.append(results)
#    results = list(set(result))
#    print "market:%s is succ result:%s"%(market,results),
#    print "t:", time.time() - time_t,
    if market == 'all':
#        write_tdx_tushare_to_file(sh_index,index_ts)
        for inx in ['999999','399006','399005','399001']:
            get_tdx_append_now_df_api_tofile(inx)
        print "Index Wri ok",
    print "All is ok"
    return results

def get_tdx_write_now_file_api(code, type='f',dm=None):
    #no use
    #no use
    #no use
    dt_list=[]
    dt_list.append(get_tdx_day_to_df_last(code, dayl=1, type=0, dt=None, ptype='close', dl=None))
    df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
    df = df.set_index('date')
    # print df
    today = cct.get_today()
    if len(df) == 1:
        tdx_last_day = df.index[-1]
        # print tdx_last_day
    else:
        log.error("error for read tdx last df")
        return False
    duration = cct.get_today_duration(tdx_last_day)
    log.debug("duration:%s"%duration)
    log.debug("tdx_last_day:%s" % tdx_last_day)
    index_status = False
    code_t=None
    if code == '999999':
        code = 'sh'
        index_status = True
    elif code.startswith('399'):
        index_status = True
        for k in INDEX_LIST.keys():
            if INDEX_LIST[k].find(code) > 0:
                code = k
    log.debug("duration:%s" % duration)

    if duration > 1:
        if index_status:
            code_t = INDEX_LIST[code][2:]
        try:
            ds = ts.get_hist_data(code, start=tdx_last_day, end=today)
            # ds = ts.get_h_data('000001', start=tdx_last_day, end=today,index=index_status)
            # df.index = pd.to_datetime(df.index)
        except (IOError, EOFError, Exception) as e:
            print "Error Duration:", e
            cct.sleep(2)
            ds = ts.get_h_data(code_t, start=tdx_last_day, end=today, index=index_status)
            df.index = pd.to_datetime(df.index)
        if ds is not None and len(ds) > 1:
            if len(df) > 0:
                lends = len(ds)
            else:
                lends = len(ds) + 1
            ds = ds[:lends - 1]
            if index_status:
                if code == 'sh':
                    code_ts = '999999'
                else:
                    code_ts = code_t
                ds['code'] = code_ts
            else:
                ds['code'] = code
            # ds['vol'] = 0
            # ds.rename(columns={'turnover': 'amount'}, inplace=True)
            ds = ds.loc[:, ['code', 'open', 'high', 'low', 'close', 'volume', 'amount']]
            # ds.rename(columns={'volume': 'amount'}, inplace=True)
            ds.rename(columns={'volume': 'vol'}, inplace=True)
            ds['vol'] = round(float(ds['vol']) * 100)
            # ds['amount'] = round(float(ds['vol']) * ds['close'] / 10)
            ds.sort_index(ascending=True, inplace=True)
            # log.debug("ds:%s" % ds[:1])
            df = df.append(ds)


    if cct.get_now_time_int() > 830 and cct.get_now_time_int() < 930:
        log.debug("now > 830 and <930 return")
        return df
    if dm is None:
        # if dm is None and today != df.index[-1]:
        # log.warn('today != end:%s'%(df.index[-1]))
        if index_status:
            log.debug("code:%s code_t:%s" % (code, code_t))
            if code_t is None:
                code_t = INDEX_LIST[code][2:]

            dm = sina_data.Sina().get_stock_code_data(code_t,index=index_status)
            dm.code = code
            dm = dm.set_index('code')
        else:
            dm = sina_data.Sina().get_stock_code_data(code).set_index('code')

    if dm is not None and df is not None and not dm.empty:
        # dm.rename(columns={'volume': 'amount', 'turnover': 'vol'}, inplace=True)
        dm.rename(columns={'volume': 'vol', 'turnover': 'amount'}, inplace=True)
        c_name = dm.loc[code, ['name']].values[0]
        dm_code = (dm.loc[:, ['open', 'high', 'low', 'close', 'amount', 'vol']])
        log.debug("dm_code:%s" % dm_code)
        # dm_code['amount'] = round(float(dm_code['amount']) / 100, 2)
        if index_status:
            if code == 'sh':
                code_ts = '999999'
            else:
                code_ts = code_t
            dm_code['code'] = code_ts
        else:
            dm_code['code'] = code
        dm_code['date'] = today
        dm_code = dm_code.set_index('date')

        # if (df is not None and df.empty) or (df.open[-1] != round(dm.open[-1], 2) and end is None):
        #     if dm.open[0] > 0:
        #         df = df.append(dm_code)
        #         df = df.astype(float)
        if ((df is not None and df.empty) or (round(df.open[-1],2) != round(dm.open[-1], 2)) or (round(df.close[-1],2) != round(dm.close[-1],2))):
            if dm.open[0] > 0:
                if dm_code.index == df.index[-1]:
                    log.error("app_api_dm.Index:%s df:%s"%(dm_code.index.values,df.index[-1]))
                    df = df.drop(dm_code.index)
                df = df.append(dm_code)

            # df=pd.concat([df,dm],axis=0, ignore_index=True).set
        df['name'] = c_name
        log.debug("c_name:%s df.name:%s" % (c_name, df.name[-1]))

    if len(df) > 0:
        df = df.sort_index(ascending=True)
        df['ma5d'] = pd.rolling_mean(df.close,5)
        df['ma10d'] = pd.rolling_mean(df.close,10)
        df['ma20d'] = pd.rolling_mean(df.close,20)
        df['ma60d'] = pd.rolling_mean(df.close,60)
    # df['ma5d'].fillna(0)
    # df['ma10d'].fillna(0)
    # df['ma20d'].fillna(0)
    # df['ma60d'].fillna(0)
        df=df.fillna(0)
        df = df.sort_index(ascending=False)

    return df

def get_tdx_append_now_df_api2(code, start=None, end=None, type='f',df=None,dm=None,dl=None,power=True,newdays=None):

    start=cct.day8_to_day10(start)
    end=cct.day8_to_day10(end)

    if df is None:
        df = get_tdx_Exp_day_to_df(code, start=start, end=end,dl=dl,newdays=newdays).sort_index(ascending=True)
    else:
        df = df.sort_index(ascending=True)

    if not isinstance(dm,Series):
        dm = dm.loc[code].to_frame().T

    if dm.open.values == df.open[-1] and int(df.vol[-1]) == int(dm.volume.values):
        return False
    index_status = False
    code_t=code
    if code == '999999':
        # code_t=code
        code = 'sh'
        index_status = True
    elif code.startswith('399'):
        index_status = True
        for k in INDEX_LIST.keys():
            if INDEX_LIST[k].find(code) > 0:
                code = k
    if index_status:
        df[code] = code_t
        # code = code_t
    if not power:
        return df
    today = cct.get_today()
    if isinstance(df, Series):
        tdx_last_day = df.date
    elif  len(df) > 0:
        tdx_last_day = df.index[-1]
    else:
        if start is not None:
            tdx_last_day = start
        else:
            tdx_last_day = None
    if tdx_last_day is not None:
        duration = cct.get_today_duration(tdx_last_day)
    else:
        duration = 10
    log.debug("duration:%s"%duration)
    log.debug("tdx_last_day:%s" % tdx_last_day)
    log.debug("duration:%s" % duration)
    if end is not None:
        if len(df)==0:
            return df
        if end <= df.index[-1]:
            duration = 0
        else:
            today = end
#    print cct.last_tddate(duration)

    if cct.get_now_time_int() > 900 and cct.get_now_time_int() < 915:
        log.debug("now > 830 and <930 return")
        df = df.sort_index(ascending=True)
        df['ma5d'] = pd.rolling_mean(df.close,5)
        df['ma10d'] = pd.rolling_mean(df.close,10)
        df['ma20d'] = pd.rolling_mean(df.close,20)
        df['ma60d'] = pd.rolling_mean(df.close,60)
        df=df.fillna(0)
        df = df.sort_index(ascending=False)
        return df

    if dm is None and end is None:
        # if dm is None and today != df.index[-1]:
        # log.warn('today != end:%s'%(df.index[-1]))
        if index_status:
            log.debug("code:%s code_t:%s" % (code, code_t))
            if code_t is None:
                code_t = INDEX_LIST[code][2:]

            dm = sina_data.Sina().get_stock_code_data(code_t,index=index_status)
            dm.code = code
            dm = dm.set_index('code')
        else:
            dm = sina_data.Sina().get_stock_code_data(code).set_index('code')

    if dm is not None and df is not None and not dm.empty and len(df) >0:
        dm.rename(columns={'volume': 'vol', 'turnover': 'amount'}, inplace=True)
        # dm.rename(columns={'volume': 'amount', 'turnover': 'vol'}, inplace=True)
        c_name = dm.loc[code, ['name']].values[0]
        dm_code = (dm.loc[:, ['open', 'high', 'low', 'close', 'amount', 'vol']])
        log.debug("dm_code:%s" % dm_code)
        # dm_code['amount'] = round(float(dm_code['amount']), 2)
        if index_status:
            if code == 'sh':
                code_ts = '999999'
            else:
                code_ts = code_t
            dm_code['code'] = code_ts
        else:
            dm_code['code'] = code
        dm_code['date'] = today
        dm_code = dm_code.set_index('date')
        # log.debug("df.open:%s dm.open%s" % (df.open[-1], round(dm.open[-1], 2)))
        # print df.close[-1],round(dm.close[-1],2)
        if not isinstance(df,Series):
            if end is None and ((df is not None and df.empty) or (round(df.open[-1],2) != round(dm.open[-1], 2)) or (round(df.close[-1],2) != round(dm.close[-1],2))):
                if dm.open[0] > 0 and len(df) >0:
                    if dm_code.index == df.index[-1] and df.vol[-1] != dm_code.vol.values:
                        log.debug("app_api_dm.Index:%s df:%s"%(dm_code.index.values,df.index[-1]))
#                        writestatus = True
                        df = df.drop(dm_code.index)
                    df = df.append(dm_code)
        else:
            if end is None and ((df is not None and df.empty) or (round(df.open,2) != round(dm.open, 2)) or (round(df.close,2) != round(dm.close,2))):
                if dm.open.values > 0 and len(df) >0:
                    if dm_code.index == df.date:
                        log.debug("app_api_dm.Index:%s df:%s"%(dm_code.index.values,df.index[-1]))
                        df = dm_code
                    else:
                        df = df.append(dm_code)
    if cct.get_now_time_int() < 900 or cct.get_now_time_int() > 1505:
        sta=write_tdx_sina_data_to_file(code,df=df)
    return sta

def get_tdx_power_now_df(code, start=None, end=None, type='f',df=None,dm=None,dl=None):
    if code == '999999' or code.startswith('399'):
        # if dl is not None and start is None:
            # start=get_duration_Index_date(code, dt=dl)
        if start is None and dl is not None:
            start=cct.last_tddate(days=dl)
        df=get_tdx_append_now_df_api(code, start=start, end=end, type=type,df=df,dm=dm)
        return df
    start=cct.day8_to_day10(start)
    end=cct.day8_to_day10(end)
    if df is None:
        df = get_tdx_Exp_day_to_df(code, type=type, start=start, end=end, dl=dl).sort_index(ascending=True)
        if len(df) > 0:
            df['vol'] =  map(lambda x: round(x*10, 1), df.vol.values)
        else:
            log.warn("%s df is Empty"%(code))
        if end is not None:
            return df
    else:
        df = df.sort_index(ascending=True)
    today = cct.get_today()
    if dm is None and (today != df.index[-1] or df.vol[-1] < df.vol[-2] * 0.8)and (cct.get_now_time_int() < 830 or cct.get_now_time_int() > 930):
        # log.warn('today != end:%s'%(df.index[-1]))
        dm = sina_data.Sina().get_stock_code_data(code).set_index('code')

    if dm is not None and df is not None and not dm.empty:
        # dm.rename(columns={'volume': 'amount', 'turnover': 'vol'}, inplace=True)
        dm.rename(columns={'volume': 'vol', 'turnover': 'amount'}, inplace=True)
        c_name=dm.loc[code,['name']].values[0]
        dm_code = (dm.loc[:, ['open', 'high', 'low', 'close', 'amount','vol']])
        log.debug("dm_code:%s" % dm_code)
        # dm_code['amount'] = round(float(dm_code['amount']) / 100, 2)
        dm_code['code'] = code
        # dm_code['vol'] = 0
        dm_code['date']=today
        dm_code = dm_code.set_index('date')
        log.debug("df.code:%s"%(code))
        log.debug("df.open:%s dm.open%s"%(df.open[-1],round(dm.open[-1],2)))
        # print df.close[-1],round(dm.close[-1],2)
        # if df.close[-1] != round(dm.close[-1], 2) and end is None:

        # if (df is not None and df.empty) or (df.open[-1] != round(dm.open[-1], 2) and end is None):
        #     # print (dm),(df)
        #     if dm.open[0] > 0:
        #         df = df.append(dm_code)
        #         df = df.astype(float)
        if end is None and ((df is not None and df.empty) or (round(df.open[-1],2) != round(dm.open[-1], 2)) or (round(df.close[-1],2) != round(dm.close[-1],2))):
            if dm.open[0] > 0:
                if dm_code.index == df.index[-1]:
                    log.debug("app_api_dm.Index:%s df:%s"%(dm_code.index.values,df.index[-1]))
                    df = df.drop(dm_code.index)
                df = df.append(dm_code)

            # print dm
            # df=pd.concat([df,dm],axis=0, ignore_index=True).set
            # print df
        df['name']=c_name
        log.debug("c_name:%s df.name:%s"%(c_name,df.name[-1]))
    if len(df) > 0:
        df = df.sort_index(ascending=True)
        df['ma5d'] = pd.rolling_mean(df.close,5)
        df['ma10d'] = pd.rolling_mean(df.close,10)
        df['ma20d'] = pd.rolling_mean(df.close,20)
        df['ma60d'] = pd.rolling_mean(df.close,60)
        # df['ma5d'].fillna(0)
        # df['ma10d'].fillna(0)
        # df['ma20d'].fillna(0)
        # df['ma60d'].fillna(0)
        df=df.fillna(0)
        df = df.sort_index(ascending=False)
    return df

def get_sina_data_df(code):
    index_status=False
    if isinstance(code, list):
        dm = sina_data.Sina().get_stock_list_data(code).set_index('code')
    else:
        dm = sina_data.Sina().get_stock_code_data(code,index=index_status).set_index('code')
    return dm


def getSinaJsondf(market='cyb',vol=ct.json_countVol,type=ct.json_countType):
    df = rl.get_sina_Market_json(market)
    top_now = rl.get_market_price_sina_dd_realTime(df, vol, type)
    return top_now

def getSinaAlldf(market='cyb',vol=ct.json_countVol,type=ct.json_countType,filename='mnbk'):

    if market == 'rzrq':
        df = cct.get_rzrq_code()
    elif market == 'cx':
        df = cct.get_rzrq_code(market)
    elif market == 'zxb':
        df = cct.get_tushare_market(market, renew=True,days=60)
    elif market == 'captops':
        global initTushareCsv
        if initTushareCsv == 0:
            initTushareCsv += 1
            df = cct.get_tushare_market(market=market, renew=True,days=10)
        else:
            df = cct.get_tushare_market(market, renew=False, days = 10)

    elif market in ['sh','sz','cyb','all']:
        df = rl.get_sina_Market_json(market)
    else:
        df = wcd.get_wcbk_df(filter=market,market=filename,perpage=1000,days=5)
    # codelist=df.code.tolist()
    # cct._write_to_csv(df,'codeall')
    # top_now = get_mmarket='all'arket_price_sina_dd_realTime(df, vol, type)
#    df =  df.dropna()

    if len(df) > 0 and 'code' in df.columns:
#        codelist = df.code.tolist()
        df = df.set_index('code')
    else:
        df = rl.get_sina_Market_json(market)
#        codelist = df.code.tolist()
        df = df.set_index('code')
        log.error("get_sina_Market_json %s : %s"%(market,len(df)))
    if cct.get_now_time_int() > 915:
#        df = df[(df.buy > 0) & (df.open != df.buy)]
        if 'buy' in df.columns:
            df = df[(df.buy > 0)]
    codelist = df.index.tolist()
    # index_status=False
    # if isinstance(codelist, list):
    time_s=time.time()
    dm = sina_data.Sina().get_stock_list_data(codelist)
    # if cct.get_work_time() or (cct.get_now_time_int() > 915) :
    dm['percent'] = map(lambda x,y: round((x-y)/y*100, 1), dm.close.values,dm.llastp.values)
    log.info("dm percent:%s"%(dm[:1]))
    # dm['volume'] = map(lambda x: round(x / 100, 1), dm.volume.values)
    dm['trade'] = dm['close']
    if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 925:
        # print dm[dm.code=='000001'].b1
        # print dm[dm.code=='000001'].a1
        # print dm[dm.code=='000001'].a1_v
        # print dm[dm.code=='000001'].b1_v
        dm['volume'] = map(lambda x: x, dm.b1_v.values)
        # print dm[dm.code=='000001'].volume
    # print dm[dm.code == '002474'].volume
    # print 'ratio' in dm.columns
    # print time.time()-time_s
    if (len(df) != len(dm)) or len(df) < 10 or len(dm) < 10:
        log.error("len(df):%s dm:%s"%(len(df),len(dm)))
    # print dm.columns,df.columns
    # print dm[:1],df[:1]
    # dm['ratio'] = map(lambda x: round(df[df.index == x].ratio.values, 1), dm['code'].values)
        dm['ratio'] = 0
    else:
        dm=pd.merge(dm,df.loc[:,['name','ratio']],on='name',how='left')
        dm=dm.drop_duplicates('code')
    # print dz[:1].ratio
    # dm['ratio'] = map(lambda x: round(df[df.code == x].ratio, 1) if len(df[df.code == x].ratio) > 0 else 0, dm['code'].values)
    # print len(dm)
    # dm = dz
    # print dm.ratio[0],dm.name[0]
    # print time.time()-time_s
    if cct.get_now_time_int() > 935:
        top_now = rl.get_market_price_sina_dd_realTime(dm, vol, type)
    else:
        dm =  dm.set_index('code')
        top_now = dm
        top_now['counts'] = 0
        top_now['diff'] = 0
        top_now['prev_p'] = 0

    # print top_now[:1].b1_v
    # print len(top_now),len(dm)
    # print top_now.loc[top_now.index == '300076',['b1_v','a1_v','trade','buy','b1','a1']]
    # print top_now.loc[top_now.index == '300004',['b1_v','a1_v','trade','buy','b1','a1']]
    # print top_now.loc[top_now.index == '300228',['b1_v','a1_v','trade','buy','b1','a1']]

    # if initTdxdata > 0 and cct.get_now_time_int() > 916 and cct.get_now_time_int() <=926:
    #     top_diff = top_now[(top_now.b1_v > top_now.a1_v) & (top_now.buy >= top_now.llastp * 0.99)]
    # elif initTdxdata > 0 and cct.get_now_time_int() > 926:
    #     top_diff = top_now[(top_now.b1_v > top_now.a1_v) & (top_now.trade >= top_now.buy) & (top_now.buy >= top_now.llastp * 0.99)]
    # else:
    #     initTdxdata +=1
    #     top_diff = top_now
    top_diff = top_now
    print "b1>%s:%s:%s"%(initTdxdata,len(top_diff),round(time.time()-time_s,1)),
    return top_diff

'''
def get_tdx_append_now_df(code, type='f', start=None, end=None):
    # start=cct.day8_to_day10(start)
    # end=cct.day8_to_day10(end)
    df = get_tdx_Exp_day_to_df(code, type, start, end).sort_index(ascending=True)
    # print df[:1]
    if not end == None:
        if not end == df.index[-1]:
            print(end, df.index[-1])
        return df
    today = cct.get_today()
    if len(df) > 0:
        tdx_last_day = df.index[-1]
        duration = cct.get_today_duration(tdx_last_day)
        log.debug("duration:%s"%duration)
    else:
        tdx_last_day = None
        duration = 1
    log.debug("tdx_last_day:%s" % tdx_last_day)
    index_status = False
    if code == '999999':
        code = 'sh'
        index_status = True
    elif code.startswith('399'):
        index_status = True
        for k in INDEX_LIST.keys():
            if INDEX_LIST[k].find(code) > 0:
                code = k

    log.debug("duration:%s" % duration)
    if duration >= 1:
        ds = ts.get_hist_data(code, start=tdx_last_day, end=today)
        if ds is not None and len(ds) > 1:
            ds = ds[:len(ds) - 1]
            ds['code'] = code
            ds['vol'] = 0
            ds = ds.loc[:, ['code', 'open', 'high', 'low', 'close', 'vol', 'volume']]
            ds.rename(columns={'volume': 'amount'}, inplace=True)
            ds.sort_index(ascending=True, inplace=True)
            log.debug("ds:%s" % ds[:1])
            df = df.append(ds)
            # pd.concat([df,ds],axis=0, join='outer')
            # result=pd.concat([df,ds])
        if cct.get_work_time() and not index_status:
            dm = rl.get_sina_Market_json('all',showtime=False).set_index('code')
            # dm=dm.drop_duplicates()
            log.debug("dm:%s" % dm[-1:])
            dm.rename(columns={'volume': 'amount', 'trade': 'close'}, inplace=True)
            # c_name=dm.loc[code,['name']]
            dm_code = dm.loc[code, ['open', 'high', 'low', 'close', 'amount']]
            log.debug("dm_code:%s" % dm_code['amount'])
            dm_code['amount'] = round(float(dm_code['amount']) / 100, 2)
            dm_code['code'] = code
            dm_code['vol'] = 0
            # dm_code['date']=today
            dm_code.name = today
            df = df.append(dm_code)
            # df['name']=c_name
            # log.debug("c_name:%s"%(c_name))
            log.debug("df[-3:]:%s" % (df[-2:]))
            df['name'] = dm.loc[code, 'name']
        log.debug("df:%s" % df[-2:])
    return df
'''

# def get_tdx_day_to_df_dict(code):
#     # time_s=time.time()
#     code_u = cct.code_to_symbol(code)
#     day_path = day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
#     p_day_dir = day_path.replace('/', path_sep).replace('\\', path_sep)
#     # p_exp_dir=exp_dir.replace('/',path_sep).replace('\\',path_sep)
#     # print p_day_dir,p_exp_dir
#     file_path = p_day_dir + code_u + '.day'
#     if not os.path.exists(file_path):
#         ds = Series(
#             {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
#              'vol': 0})
#         return ds
#     ofile = open(file_path, 'rb')
#     buf = ofile.read()
#     ofile.close()
#     # ifile=open(p_exp_dir+code_u+'.txt','w')
#     num = len(buf)
#     # print num
#     no = int(num / 32)
#     # print no
#     b = 0
#     e = 32
#     dict_t = []
#     for i in xrange(no):
#         a = unpack('IIIIIfII', buf[b:e])
#         # tdate=str(a[0])
#         tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
#         topen = float(a[1] / 100.0)
#         thigh = float(a[2] / 100.0)
#         tlow = float(a[3] / 100.0)
#         tclose = float(a[4] / 100.0)
#         amount = float(a[5] / 10.0)
#         tvol = int(a[6])  # int
#         tpre = int(a[7])  # back
#         # line=str(a[0])+' '+str(a[1]/100.0)+' '+str(a[2]/100.0)+' '+str(a[3]/100.0)+\
#         # ' '+str(a[4]/100.0)+' '+str(a[5]/10.0)+' '+str(a[6])+' '+str(a[7])+' '+'\n'
#         # print line
#         # list_t.append(tdate,topen,thigh,tlow,tclose,tvolp,tvol,tpre)
#         # dict_t[tdate]={'date':tdate,'open':topen,'high':thigh,'low':tlow,'close':tclose,'volp':tvolp,'vol':tvol,'pre':tpre}
#         dict_t.append(
#             {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose, 'amount': amount,
#              'vol': tvol, 'pre': tpre})
#         b = b + 32
#         e = e + 32
#     # df=pd.DataFrame.from_dict(dict_t,orient='index')
#     df = pd.DataFrame(dict_t, columns=ct.TDX_Day_columns)
#     df = df.set_index('date')
#     return {code: df}


def get_tdx_day_to_df(code):
    """
        获取个股历史交易记录
    Parameters
    ------
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取到API所提供的最早日期数据
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取到最近一个交易日数据
      ktype：string
                  数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率
    """
    # time_s=time.time()
    # print code
    code_u = cct.code_to_symbol(code)
    day_path = day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
    p_day_dir = day_path.replace('/', path_sep).replace('\\', path_sep)
    # p_exp_dir = exp_dir.replace('/', path_sep).replace('\\', path_sep)
    # print p_day_dir,p_exp_dir
    file_path = p_day_dir + code_u + '.day'
    if not os.path.exists(file_path):
        ds = Series(
            {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
             'vol': 0})
        return ds

    ofile = open(file_path, 'rb')
    buf = ofile.read()
    ofile.close()
    num = len(buf)
    no = int(num / 32)
    b = 0
    e = 32
    dt_list = []
    for i in xrange(no):
        a = unpack('IIIIIfII', buf[b:e])
        # dt=datetime.date(int(str(a[0])[:4]),int(str(a[0])[4:6]),int(str(a[0])[6:8]))
        tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
        # tdate=dt.strftime('%Y-%m-%d')
        topen = float(a[1] / 100.0)
        thigh = float(a[2] / 100.0)
        tlow = float(a[3] / 100.0)
        tclose = float(a[4] / 100.0)
        amount = float(a[5] / 10.0)
        tvol = int(a[6])  # int
        tpre = int(a[7])  # back
        dt_list.append(
            {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose, 'amount': amount,
             'vol': tvol, 'pre': tpre})
        b = b + 32
        e = e + 32
    df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
    df = df.set_index('date')
    # print "time:",(time.time()-time_s)*1000
    return df


def get_duration_Index_date(code='999999', dt=None, ptype='low',dl=None,power=False):
    if dt is not None:
        if len(str(dt)) < 8:
            dl = int(dt)+changedays
            # df = get_tdx_day_to_df(code).sort_index(ascending=False)
            df = get_tdx_append_now_df_api(code,power=power).sort_index(ascending=False)
            dt = get_duration_price_date(code, dt=dt,ptype=ptype,df=df)
            dt = df[df.index <= dt].index.values[changedays]
            log.info("LastDF:%s,%s" % (dt,dl))
        else:
            if len(str(dt)) == 8: dt = cct.day8_to_day10(dt)
            # df = get_tdx_day_to_df(code).sort_index(ascending=False)
            df = get_tdx_append_now_df_api(code,start=dt,power=power).sort_index(ascending=False)
            # dl = len(get_tdx_Exp_day_to_df(code, start=dt)) + changedays
            dl = len(df) + changedays
            dt = df[df.index <= dt].index.values[changedays]
            log.info("LastDF:%s,%s" % (dt,dl))
        return dt,dl
    if dl is not None:
        # dl = int(dl)
        df = get_tdx_append_now_df_api(code,start=dt,dl=dl,power=power).sort_index(ascending=False)
        # print df
        # dl = len(get_tdx_Exp_day_to_df(code, start=dt)) + changedays
        # print df[:dl].index,dl
        dt = df[:dl].index[-1]
        log.info("dl to dt:%s" % (dt))
        return dt
    return None,None


def get_duration_date(code, ptype='low', dt=None, df=None, dl=None):
    if df is None:
        df = get_tdx_day_to_df(code).sort_index(ascending=False)
        # log.debug("code:%s" % (df[:1].index))
    else:
        df = df.sort_index(ascending=False)
    if dt != None:
        if len(str(dt)) == 10:
            dz = df[df.index >= dt]
            if dl is not None:
                if len(dz) < int(dl) - changedays:
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
                else:
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
        elif len(str(dt)) == 8:
            dt=cct.day8_to_day10(dt)
            dz = df[df.index >= dt]
            if dl is not None:
                if len(dz) < int(dl) - changedays:
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
                else:
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
        else:
            if len(df) > int(dt):
                dz = df[:int(dt)]
            else:
                dz = df
    elif dl is not None:
        if len(df) > int(dl):
            dz = df[:int(dl)]
        else:
            dz = df
        return dz.index[-1]
    else:
        dz=df
    if ptype == 'high':
        lowp = dz.close.max()
        lowdate = dz[dz.close == lowp].index.values[-1]
        log.debug("high:%s"%lowdate)
    elif ptype == 'close':
        lowp = dz.close.min()
        lowdate = dz[dz.close == lowp].index.values[-1]
        log.debug("high:%s" % lowdate)
    else:
        lowp = dz.low.min()
        lowdate = dz[dz.low == lowp].index.values[-1]
        log.debug("low:%s" % lowdate)
    # if ptype == 'high':
    #     lowp = dz.close.max()
    #     lowdate = dz[dz.close == lowp].index.values[0]
    #     log.debug("high:%s"%lowdate)
    # else:
    #     lowp = dz.close.min()
    #     lowdate = dz[dz.close == lowp].index.values[0]
    #     log.debug("low:%s"%lowdate)
    log.debug("date:%s %s:%s" % (lowdate, ptype, lowp))
    return lowdate


def get_duration_price_date(code, ptype='low', dt=None, df=None, dl=None, end=None, vtype=None, filter=True,
                            power=False):
    # if code == "600760":
        # log.setLevel(LoggerFactory.DEBUG)
    # else:u
        # log.setLevel(LoggerFactory.ERROR)
    # if ptype == 'low' and code == '999999':
    #     log.setLevel(LoggerFactory.DEBUG)
    # else:
    #     log.setLevel(LoggerFactory.ERROR)
    if df is None:
        # df = get_tdx_day_to_df(code).sort_index(ascending=False)
        if power:
            df = get_tdx_append_now_df_api(code, start=dt,end=end,dl=dl).sort_index(ascending=False)
        else:
            df = get_tdx_Exp_day_to_df(code, start=dt, end=end,dl=dl).sort_index(ascending=False)
    else:
        df = df.sort_index(ascending=False)
        # log.debug("code:%s" % (df[:1].index))
    if dt != None:
        if len(str(dt)) == 10:
            dz = df[df.index >= dt]
            if dl is not None:
                if len(dz) < int(dl) - changedays:
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
                else:
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
        elif len(str(dt)) == 8:
            dt=cct.day8_to_day10(dt)
            dz = df[df.index >= dt]
            if len(dz) > 0 and dl is not None:
                if len(dz) < int(dl) - changedays:
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
                else:
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
            else:
                # log.error("code:%s dt:%s no data"%(code,dt))
                if not filter:
                    index_d = df.index[0]

        else:
            if len(df) > int(dt):
                dz = df[:int(dt)]
            else:
                dz = df
    elif dl is not None:
        if len(df) > int(dl):
            dz = df[:int(dl)]
        else:
            dz = df
        if not filter:
            index_d = dz[:1].index.values[0]
    else:
        dz=df
    if len(dz) > 0:
        if ptype == 'high':
            lowp = dz.close.max()
            lowdate = dz[dz.close == lowp].index.values[-1]
            log.debug("high:%s" % lowdate)
        elif ptype == 'close':
            lowp = dz.close.min()
            lowdate = dz[dz.close == lowp].index.values[-1]
            log.debug("high:%s" % lowdate)
        else:
            lowp = dz.low.min()
            lowdate = dz[dz.low == lowp].index.values[-1]
            log.debug("low:%s" % lowdate)
        log.debug("date:%s %s:%s" % (lowdate, ptype, lowp))
    else:
        lowdate = df.index[0]
    # if ptype == 'high':
    #     lowp = dz.close.max()
    #     lowdate = dz[dz.close == lowp].index.values[0]
    #     log.debug("high:%s"%lowdate)
    # else:
    #     lowp = dz.close.min()
    #     lowdate = dz[dz.close == lowp].index.values[0]
    #     log.debug("low:%s"%lowdate)
    if filter:
        return lowdate
    elif not power:
        return lowdate,index_d
    else:
        return lowdate, index_d, df

def get_tdx_exp_low_or_high_price(code, dt=None, ptype='close', dl=None,end=None):
    '''
    :param code:999999
    :param dayl:Duration Days
    :param type:TDX type
    :param dt:  Datetime
    :param ptype:low or high
    :return:Series or df
    '''
    # dt = cct.day8_to_day10(dt)
    if dt is not None and dl is not None:
        # log.debug("dt:%s dl:%s"%(dt,dl))
        df = get_tdx_Exp_day_to_df(code, start=dt, dl=dl,end=end).sort_index(ascending=False)
        if df is not None and not df.empty:
            if len(str(dt)) == 10:
                dz = df[df.index >= dt]
                # if dz.empty:
                    # dd = Series(
                        # {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
                         # 'vol': 0})
                    # return dd
                if len(dz) < abs(int(dl) - changedays):
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
                if isinstance(dz, Series):
                    # dz=pd.DataFrame(dz)
                    # dz=dz.set_index('date')
                    return dz

            else:
                if len(df) > int(dl):
                    dz = df[:int(dl)]
                else:
                    dz = df
            if dz is not None and not dz.empty:
                if ptype == 'high':
                    lowp = dz.close.max()
                    lowdate = dz[dz.close == lowp].index.values[-1]
                    log.debug("high:%s" % lowdate)
                elif ptype == 'close':
                    lowp = dz.close.min()
                    lowdate = dz[dz.close == lowp].index.values[-1]
                    log.debug("close:%s" % lowdate)
                else:
                    lowp = dz.low.min()
                    lowdate = dz[dz.low == lowp].index.values[-1]
                    log.debug("low:%s" % lowdate)

                log.debug("date:%s %s:%s" % (lowdate, ptype, lowp))
                # log.debug("date:%s %s:%s" % (dt, ptype, lowp))
                dd = df[df.index == lowdate]
                if len(dd) > 0:
                    dd = dd[:1]
                    dt = dd.index.values[0]
                    dd = dd.T[dt]
                    dd['date'] = dt
            else:
                dd = Series()

        else:
            log.warning("code:%s no < dt:NULL" % (code))
            dd = Series()
            # dd = Series(
            #     {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
            #      'vol': 0})
        return dd
    else:
        dd = get_tdx_Exp_day_to_df(code, dl=1)
        return dd

def get_tdx_exp_low_or_high_power(code, dt=None, ptype='close', dl=None,end=None,power=False,lastp=False,newdays=None):
    '''
    :param code:999999
    :param dayl:Duration Days
    :param type:TDX type
    :param dt:  Datetime
    :param ptype:low or high
    :return:Series or df
    '''
    # dt = cct.day8_to_day10(dt)
    if dt is not None or dl is not None:
        # log.debug("dt:%s dl:%s"%(dt,dl))
        df = get_tdx_Exp_day_to_df(code, start=dt, dl=dl,end=end,newdays=newdays).sort_index(ascending=False)
        if df is not None and len(df) > 0:

            if power:
                from JSONData import powerCompute as pct
                dtype='d'
                opc = 0
                stl = ''
                rac = 0
                # fib = []
                # sep = '|'
                fibl = '0'
                fib = '0'
                for pty in ['low', 'high']:
                    op, ra, st, daysData  = pct.get_linear_model_status(
                        code, df=df, dtype=dtype, start=dt, end=end, dl=dl, filter='y', ptype=pty,power=False)
                    opc += op
                    rac += ra
                    if ptype == 'low':
                        stl = st
                        fibl = str(daysData[0])
                    else:
                        fib = str(daysData[0])
                # df.loc[code,'ma5'] = daysData[1].ma5d[0]
                # print tdx_df[:1].ma5d[0],daysData[1].ma5d[0]
#                if 'ma5d' in df.columns and 'ma10d' in df.columns:
#                    if df[:1].ma5d[0] is not None and df[:1].ma5d[0] != 0:
#                        df.loc[code,'ma5d'] = round(float(df[:1].ma5d[0]),2)
#                    if df[:1].ma10d[0] is not None and df[:1].ma10d[0] != 0:
#                        df.loc[code,'ma10d'] = round(float(df[:1].ma10d[0]),2)
                df['op'] = opc
                df['ra'] = rac
                df['fib'] = fib
                df['fibl'] = fibl
                df['ldate'] = stl
                # df = df.fillna(0)
                # print df[:1]
            if lastp:
                dd = df[:1]
                dt = dd.index.values[0]
                dd = dd.T[dt]
                dd['date'] = dt
                if 'ma5d' in df.columns and 'ma10d' in df.columns:
                    if df[:1].ma5d[0] is not None and df[:1].ma5d[0] != 0:
                        dd['ma5d'] = round(float(df[:1].ma5d[0]),2)
                    if df[:1].ma10d[0] is not None and df[:1].ma10d[0] != 0:
                        dd['ma10d'] = round(float(df[:1].ma10d[0]),2)
                return dd

            if len(str(dt)) == 10:
                dz = df[df.index >= dt]
                # if dz.empty:
                    # dd = Series(
                        # {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
                         # 'vol': 0})
                    # return dd
                if len(dz) < abs(int(dl) - changedays):
                    if len(df) > int(dl):
                        dz = df[:int(dl)]
                    else:
                        dz = df
                if isinstance(dz, Series):
                    # dz=pd.DataFrame(dz)
                    # dz=dz.set_index('date')
                    return dz

            else:
                if len(df) > int(dl):
                    dz = df[:int(dl)]
                else:
                    dz = df
            if dz is not None and not dz.empty:
                if ptype == 'high':
                    lowp = dz.close.max()
                    lowdate = dz[dz.close == lowp].index.values[-1]
                    log.debug("high:%s" % lowdate)
                elif ptype == 'close':
                    lowp = dz.close.min()
                    lowdate = dz[dz.close == lowp].index.values[-1]
                    log.debug("close:%s" % lowdate)
                else:
                    lowp = dz.close.min()
                    lowdate = dz[dz.close == lowp].index.values[-1]
                    log.debug("low:%s" % lowdate)

                log.debug("date:%s %s:%s" % (lowdate, ptype, lowp))
                # log.debug("date:%s %s:%s" % (dt, ptype, lowp))
                dd = df[df.index == lowdate].copy()
                if ptype == 'high':
                    lowp = dz.low.min()
                    dd.low =  lowp
                else:
                    highp = dz.high.max()
                    dd.high =  highp
                    # print dd.high
                if len(dd) > 0:
                    dd = dd[:1]
                    dt = dd.index.values[0]
                    dd = dd.T[dt]
                    dd['date'] = dt
                    # print dd
                if 'ma5d' in df.columns and 'ma10d' in df.columns:
                    if df[:1].ma5d[0] is not None and df[:1].ma5d[0] != 0:
                        dd['ma5d'] = round(float(df[:1].ma5d[0]),2)
                    if df[:1].ma10d[0] is not None and df[:1].ma10d[0] != 0:
                        dd['ma10d'] = round(float(df[:1].ma10d[0]),2)
            else:
                dd = Series()

        else:
            log.debug("code:%s no < dt:NULL" % (code))
            dd = Series()
            # dd = Series(
            #     {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
            #      'vol': 0})
        return dd
    else:
        dd = get_tdx_Exp_day_to_df(code, dl=1)
        return dd

def get_tdx_day_to_df_last(code, dayl=1, type=0, dt=None, ptype='close', dl=None,newdays=None):
    '''
    :param code:999999
    :param dayl:Duration Days
    :param type:TDX type
    :param dt:  Datetime
    :param ptype:low or high
    :return:Series or df
    '''
    # dayl=int(dayl)
    # type=int(type)
    # print "t:",dayl,"type",type
    if newdays is not None:
        newstockdayl = newdays
    else:
        newstockdayl = newdaysinit
    if not type == 0:
        f = (lambda x: str((1000000 - int(x))) if x.startswith('0') else x)
        code = f(code)
    code_u = cct.code_to_symbol(code)
    day_path = day_dir % 'sh' if code.startswith(('5', '6', '9')) else day_dir % 'sz'
    p_day_dir = day_path.replace('/', path_sep).replace('\\', path_sep)
    # p_exp_dir=exp_dir.replace('/',path_sep).replace('\\',path_sep)
    # print p_day_dir,p_exp_dir
    file_path = p_day_dir + code_u + '.day'
    if not os.path.exists(file_path):
        ds = Series(
            {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
             'vol': 0})
        return ds
    ofile = file(file_path, 'rb')
    b = 0
    e = 32
    if dayl == 1 and dt == None:
        log.debug("%s" % (dayl == 1 and dt == None))
        fileSize = os.path.getsize(file_path)
        if fileSize < 32: print "why", code
        ofile.seek(-e, 2)
        buf = ofile.read()
        ofile.close()
        a = unpack('IIIIIfII', buf[b:e])
        tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
        topen = float(a[1] / 100.0)
        thigh = float(a[2] / 100.0)
        tlow = float(a[3] / 100.0)
        tclose = float(a[4] / 100.0)
        amount = float(a[5] / 10.0)
        tvol = int(a[6])  # int
        # tpre = int(a[7])  # back
        dt_list = Series(
            {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose, 'amount': amount,
             'vol': tvol})
        return dt_list
    elif dayl == 1 and dt is not None and dl is not None:
        log.debug("dt:%s" % (dt))
        dt_list = []
        # if len(str(dt)) == 8:
            # dt = cct.day8_to_day10(dt)
        # else:
            # dt=get_duration_price_date(code, ptype=ptype, dt=dt)
            # print ("dt:%s"%dt)
        fileSize = os.path.getsize(file_path)
        if fileSize < 32: print "why", code
        b = fileSize
        ofile.seek(-fileSize, 2)
        no = int(fileSize / e)
        if no < newstockdayl:
            return Series()
        # print no,b,day_cout,fileSize
        buf = ofile.read()
        ofile.close()
        # print repr(buf)
        # df=pd.DataFrame()
        for i in xrange(no):
            a = unpack('IIIIIfII', buf[-e:b])
            tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
            topen = float(a[1] / 100.0)
            thigh = float(a[2] / 100.0)
            tlow = float(a[3] / 100.0)
            tclose = float(a[4] / 100.0)
            amount = float(a[5] / 10.0)
            tvol = int(a[6])  # int
            # tpre = int(a[7])  # back
            dt_list.append({'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose,
                            'amount': amount, 'vol': tvol})
            # print series
            # dSeries.append(series)
            # dSeries.append(Series({'code':code,'date':tdate,'open':topen,'high':thigh,'low':tlow,'close':tclose,'amount':amount,'vol':tvol,'pre':tpre}))
            b = b - 32
            e = e + 32
            # print tdate,dt
            if tdate < dt:
                # print "why"
                break
        df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
        # print "len:%s %s"%(len(df),fileSize)
        df = df.set_index('date')
        dt = get_duration_price_date(code, ptype=ptype, dt=dt, df=df,dl=dl)
        log.debug('last_dt:%s' % dt)
        dd = df[df.index == dt]
        if len(dd) > 0:
            dd = dd[:1]
            dt = dd.index.values[0]
            dd = dd.T[dt]
            dd['date'] = dt
        else:
            log.warning("no < dt:NULL")
            dd = Series()
            # dd = Series(
                # {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
                 # 'vol': 0})
        return dd
    else:
        dt_list = []
        fileSize = os.path.getsize(file_path)
        # print fileSize
        day_cout = abs(e * int(dayl))
        # print day_cout
        if day_cout > fileSize:
            b = fileSize
            ofile.seek(-fileSize, 2)
            no = int(fileSize / e)
        else:
            no = int(dayl)
            b = day_cout
            ofile.seek(-day_cout, 2)
        # print no,b,day_cout,fileSize
        buf = ofile.read()
        ofile.close()
        # print repr(buf)
        # df=pd.DataFrame()
        for i in xrange(no):
            a = unpack('IIIIIfII', buf[-e:b])
            tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
            topen = float(a[1] / 100.0)
            thigh = float(a[2] / 100.0)
            tlow = float(a[3] / 100.0)
            tclose = float(a[4] / 100.0)
            amount = float(a[5] / 10.0)
            tvol = int(a[6])  # int
            # tpre = int(a[7])  # back
            dt_list.append({'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose,
                            'amount': amount, 'vol': tvol})
            # print series
            # dSeries.append(series)
            # dSeries.append(Series({'code':code,'date':tdate,'open':topen,'high':thigh,'low':tlow,'close':tclose,'amount':amount,'vol':tvol,'pre':tpre}))
            b = b - 32
            e = e + 32
        df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
        df = df.set_index('date')
        return df


#############################################################
# usage 使用说明
#
#############################################################
def get_tdx_all_day_LastDF(codeList, type=0, dt=None, ptype='close'):
    time_t = time.time()
    # df = rl.get_sina_Market_json(market)
    # code_list = np.array(df.code)
    # if type==0:
    #     results = cct.to_mp_run(get_tdx_day_to_df_last, codeList)
    # else:
    if dt is not None:
        if len(str(dt)) != 8:
            df = get_tdx_day_to_df('999999').sort_index(ascending=False)
            dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
            dt = df[df.index <= dt ].index.values[changedays]
            dl = len(df[df.index >= dt ])
            log.info("LastDF:%s" % dt)
        else:
            # dt = int(dt)+10
            df = get_tdx_day_to_df('999999').sort_index(ascending=False)
            dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
            dt = df[df.index <= dt ].index.values[changedays]
            dl = len(df[df.index >= dt ])
            log.info("LastDF:%s" % dt)
    else:
        dl=None
    results = cct.to_mp_run_async(get_tdx_day_to_df_last, codeList, 1, type, dt,ptype,dl)
    # results=[]
    # for code in codeList:
        # results.append(get_tdx_day_to_df_last(code, 1, type, dt,ptype))


    df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    df = df.set_index('code')
    df.loc[:, 'open':] = df.loc[:, 'open':].astype(float)
    # df.vol = df.vol.apply(lambda x: x / 100)
    log.info("get_to_mp:%s" % (len(df)))
    log.info("TDXTime:%s" % (time.time() - time_t))
    if dt != None:
        print ("TDX:%0.2f" % (time.time() - time_t)),
    return df

def get_append_lastp_to_df(top_all,lastpTDX_DF=None,dl=ct.PowerCountdl,end=None,ptype='low',filter='y',power=True,lastp=True,newdays=None):
    codelist = top_all.index.tolist()
    log.info('toTDXlist:%s' % len(codelist))
    # print codelist[5]
    if lastpTDX_DF is None or len(lastpTDX_DF) == 0:
        # tdxdata = get_tdx_all_day_LastDF(codelist) '''only get lastp no powerCompute'''
        tdxdata = get_tdx_exp_all_LastDF_DL(codelist,dt=dl,end=end,ptype=ptype,filter=filter,power=power,lastp=lastp,newdays=newdays)
        # tdxdata.rename(columns={'close': 'llow'}, inplace=True)
        tdxdata.rename(columns={'open': 'lopen'}, inplace=True)
        tdxdata.rename(columns={'high': 'lhigh'}, inplace=True)
        tdxdata.rename(columns={'close': 'lastp'}, inplace=True)
        # tdxdata.rename(columns={'low': 'lastp'}, inplace=True)
        tdxdata.rename(columns={'low': 'llow'}, inplace=True)
        tdxdata.rename(columns={'vol': 'lvol'}, inplace=True)
#        if power:
#            tdxdata = tdxdata.loc[:, ['llow', 'lhigh', 'lastp', 'lvol', 'date','ra','op','fib','fibl','ma5d','ma10d','ldate']]
#            # print len(tdxdata[tdxdata.op >15]),
#        else:
#            tdxdata = tdxdata.loc[:, ['llow', 'lhigh', 'lastp', 'lvol','ma5d','ma10d','date']]
#            # tdxdata = tdxdata.loc[
#            #     :, ['llow', 'lhigh', 'lastp', 'lvol', 'date']]
        log.debug("TDX Col:%s" % tdxdata.columns.values)
    else:
        tdxdata = lastpTDX_DF
    log.debug("TdxLastP: %s %s" %
              (len(tdxdata), tdxdata.columns.values))
        # :, ['llow', 'lhigh', 'lastp', 'lvol','ma5d', 'date']]
    # data.drop('amount',axis=0,inplace=True)
    # df_now=top_all.merge(data,on='code',how='left')
    # df_now=pd.merge(top_all,data,left_index=True,right_index=True,how='left')
    top_all = top_all.merge(
        tdxdata, left_index=True, right_index=True, how='left')
    # log.info('Top-merge_now:%s' % (top_all[:1]))
    top_all = top_all[top_all['llow'] > 0]
    if lastpTDX_DF is None:
        return top_all,tdxdata
    else:
        return top_all

def get_tdx_exp_all_LastDF(codeList, dt=None,end=None,ptype='low',filter='n'):
    time_t = time.time()
    # df = rl.get_sina_Market_json(market)
    # code_list = np.array(df.code)
    # if type==0:
    #     results = cct.to_mp_run(get_tdx_day_to_df_last, codeList)
    # else:
    if dt is not None and filter == 'n':
        if len(str(dt)) < 8 :
            dl = int(dt)+changedays
            df = get_tdx_Exp_day_to_df('999999',end=end).sort_index(ascending=False)
            dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
            dt = df[df.index <= dt].index.values[changedays]
            log.info("LastDF:%s,%s" % (dt,dl))
        else:
            if len(str(dt)) == 8: dt = cct.day8_to_day10(dt)
            df = get_tdx_Exp_day_to_df('999999',end=end).sort_index(ascending=False)
            dl = len(df[df.index >=dt]) + changedays
            dt = df[df.index <= dt].index.values[changedays]
            log.info("LastDF:%s,%s" % (dt,dl))
            #results = cct.to_mp_run_async(get_tdx_exp_low_or_high_price, codeList, dt, ptype, dl,end)
            # results = get_tdx_exp_low_or_high_price(codeList[0], dt,ptype,dl)
        results=[]
        for code in codeList:
            results.append(get_tdx_exp_low_or_high_price(code, dt, ptype, dl))
    elif dt is not None:
        if len(str(dt)) < 8 :
            dl = int(dt)
            df = get_tdx_Exp_day_to_df('999999',end=end).sort_index(ascending=False)
            dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
            dt = df[df.index <= dt].index.values[0]
            log.info("LastDF:%s,%s" % (dt,dl))
        else:
            if len(str(dt)) == 8: dt = cct.day8_to_day10(dt)
            dl = len(get_tdx_Exp_day_to_df('999999',start=dt,end=end).sort_index(ascending=False))
            # dl = len(ts.get_hist_data('sh', start=dt))
            log.info("LastDF:%s,%s" % (dt,dl))
        results = cct.to_mp_run_async(get_tdx_exp_low_or_high_price, codeList, dt, ptype, dl,end)
        # print dt,ptype,dl,end
        # for code in codelist:
        #     print code
        #     print get_tdx_exp_low_or_high_price('600654', dt, ptype, dl,end)

    else:
        # results = cct.to_mp_run_async(get_tdx_exp_low_or_high_price,codeList)
        results = cct.to_mp_run_async(get_tdx_Exp_day_to_df, codeList, 'f', None, None, None, 1)

    # print results
    df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    df = df.set_index('code')
    df.loc[:, 'open':] = df.loc[:, 'open':].astype(float)
    # df.vol = df.vol.apply(lambda x: x / 100)
    log.info("get_to_mp:%s" % (len(df)))
    log.info("TDXTime:%s" % (time.time() - time_t))
    if dt != None:
        print ("TDXE:%0.2f" % (time.time() - time_t)),
    return df

def get_tdx_exp_all_LastDF_DL(codeList, dt=None,end=None,ptype='low',filter='n',power=False,lastp=False,newdays=None):
    time_t = time.time()
    # df = rl.get_sina_Market_json(market)
    # code_list = np.array(df.code)
    # if type==0:
    #     results = cct.to_mp_run(get_tdx_day_to_df_last, codeList)
    # else:
    if dt is not None and filter == 'n':
        if len(str(dt)) < 8 :
            dl = int(dt)
            dt = None
            # df = get_tdx_Exp_day_to_df('999999',end=end).sort_index(ascending=False)
            # dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
            # dt = df[df.index <= dt].index.values[changedays]
            log.info("LastDF:%s,%s" % (dt,dl))
        else:
            if len(str(dt)) == 8:
                dt = cct.day8_to_day10(dt)
                df = get_tdx_Exp_day_to_df('999999',end=end).sort_index(ascending=False)
                dl = len(df[df.index >=dt])
            elif len(str(dt)) == 10:
                df = get_tdx_Exp_day_to_df('999999',end=end).sort_index(ascending=False)
                dl = len(df[df.index >=dt])
            else:
                log.warning('dt :%s error dl=60,dt->None'%(dt))
                dl = 30
                dt = None
            log.info("LastDF:%s,%s" % (dt,dl))
        results = cct.to_mp_run_async(get_tdx_exp_low_or_high_power, codeList, dt, ptype, dl,end,power,lastp,newdays)
        # results = get_tdx_exp_low_or_high_price(codeList[0], dt,ptype,dl)
#        results=[]
#        for code in codeList:
#            print code
#            results.append(get_tdx_exp_low_or_high_price(code, dt, ptype, dl))
    elif dt is not None:
        if len(str(dt)) < 8 :
            dt = int(dt)
            dl = dt
            # dt = None
            # df = get_tdx_Exp_day_to_df('999999',end=end).sort_index(ascending=False)
            # dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
            # dt = df[df.index <= dt].index.values[0]
            dt=get_duration_Index_date('999999',dl=dt)
            log.info("LastDF:%s,%s" % (dt,dl))
        else:
            if len(str(dt)) == 8:
                dt = cct.day8_to_day10(dt)
                df = get_tdx_Exp_day_to_df('999999',end=end).sort_index(ascending=False)
                dl = len(df[df.index >=dt])
            elif len(str(dt)) == 10:
                df = get_tdx_Exp_day_to_df('999999',end=end).sort_index(ascending=False)
                dl = len(df[df.index >=dt])
            else:
                log.warning('dt :%s error dl=60,dt->None'%(dt))
                dl = 30
                dt = None
            log.info("LastDF:%s,%s" % (dt,dl))
        results = cct.to_mp_run_async(get_tdx_exp_low_or_high_power, codeList, dt, ptype, dl,end,power,lastp,newdays)
#        results=[]
#        for code in codeList:
#            print code
#            results.append(get_tdx_exp_low_or_high_power(code,dt,ptype,dl,end,power,lastp))
        # print dt,ptype,dl,end
        # for code in codelist:
        #     print code
        #     print get_tdx_exp_low_or_high_price('600654', dt, ptype, dl,end)

    else:
        # results = cct.to_mp_run_async(get_tdx_exp_low_or_high_price,codeList)
        dl = None
        results = cct.to_mp_run_async(get_tdx_Exp_day_to_df, codeList, 'f', None, None, None, 1)

    # print results
    df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    df = df.dropna(how='all')
    if len(df) > 0:
        df = df.set_index('code')
        df.loc[:, 'open':'amount'] = df.loc[:, 'open':'amount'].astype(float)
    # df.vol = df.vol.apply(lambda x: x / 100)
    log.info("get_to_mp:%s" % (len(df)))
    log.info("TDXTime:%s" % (time.time() - time_t))
    # if power and 'op' in df.columns:
    #     df=df[df.op >10]
    #     df=df[df.ra < 11]
        # print "op:",len(df),
    if dl != None:
        print ("TDXE:%0.2f" % (time.time() - time_t)),
    return df

def get_tdx_all_StockList_DF(code_list, dayl=1, type=0):
    time_t = time.time()
    # df = rl.get_sina_Market_json(market)
    # code_list = np.array(df.code)
    # log.info('code_list:%s' % len(code_list))
    results = cct.to_mp_run_async(get_tdx_day_to_df_last, code_list, dayl, type)
    log.info("get_to_mp_op:%s" % (len(results)))
    # df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    # df = df.set_index('code')
    # print df[:1]
    print "t:", time.time() - time_t
    return results


def get_tdx_all_day_DayL_DF(market='cyb', dayl=1):
    time_t = time.time()
    df = rl.get_sina_Market_json(market)
    code_list = np.array(df.code)
    log.info('code_list:%s' % len(code_list))
    results = cct.to_mp_run_async(get_tdx_day_to_df_last, code_list, dayl)
    log.info("get_to_mp_op:%s" % (len(results)))
    # df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    # df = df.set_index('code')
    # print df[:1]

    # print len(df),df[:1]
    # print "<2015-08-25",len(df[(df.date< '2015-08-25')])
    # print "06-25-->8-25'",len(df[(df.date< '2015-08-25')&(df.date > '2015-06-25')])
    print "t:", time.time() - time_t
    return results



def get_tdx_search_day_DF(market='cyb'):
    time_t = time.time()
    df = rl.get_sina_Market_json(market)
    code_list = np.array(df.code)
    log.info('code_list:%s' % len(code_list))
    results = cct.to_mp_run(get_tdx_day_to_df, code_list)
    log.info("get_to_mp_op:%s" % (len(results)))
    # df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    # df = df.set_index('code')
    # print df[:1]

    # print len(df),df[:1]
    # print "<2015-08-25",len(df[(df.date< '2015-08-25')])
    # print "06-25-->8-25'",len(df[(df.date< '2015-08-25')&(df.date > '2015-06-25')])
    print "t:", time.time() - time_t
    return results


def get_tdx_stock_period_to_type(stock_data, type='w'):
    period_type = type
    # 转换周最后一日变量
    stock_data.index = pd.to_datetime(stock_data.index,format='%Y-%m-%d')
    period_stock_data = stock_data.resample(period_type, how='last')
    # 周数据的每日change连续相乘
    # period_stock_data['percent']=stock_data['percent'].resample(period_type,how=lambda x:(x+1.0).prod()-1.0)
    # 周数据open等于第一日
    period_stock_data['open'] = stock_data['open'].resample(period_type, how='first')
    # 周high等于Max high
    period_stock_data['high'] = stock_data['high'].resample(period_type, how='max')
    period_stock_data['low'] = stock_data['low'].resample(period_type, how='min')
    # volume等于所有数据和
    period_stock_data['amount'] = stock_data['amount'].resample(period_type, how='sum')
    period_stock_data['vol'] = stock_data['vol'].resample(period_type, how='sum')
    # 计算周线turnover,【traded_market_value】 流通市值【market_value】 总市值【turnover】 换手率，成交量/流通股本
    # period_stock_data['turnover']=period_stock_data['vol']/(period_stock_data['traded_market_value'])/period_stock_data['close']
    # 去除无交易纪录
    period_stock_data = period_stock_data[period_stock_data['code'].notnull()]
    # period_stock_data.reset_index(inplace=True)
    # period_stock_data.set_index('date',inplace=True)
    period_stock_data.index = map(lambda x:str(x)[:10],period_stock_data.index)
    # print period_stock_data[:1].index
    return period_stock_data


def usage(p=None):
    import timeit
#     print """
# python %s [-t txt|zip] stkid [from] [to]
# -t txt 表示从txt files 读取数据，否则从zip file 读取(这也是默认方式)
# for example :
# python %s 999999 20070101 20070302
# python %s -t txt 999999 20070101 20070302
#     """ % (p, p, p)
    status=None
    run=1
    df = rl.get_sina_Market_json('cyb')
    df = df.set_index('code')
    codelist = df.index.tolist()
    duration_date=20160101
    ptype='low'
    dt = duration_date
    # codeList='999999'
    print ""
    for x in xrange(1):
        if len(str(dt)) != 8:
                df = get_tdx_day_to_df('999999').sort_index(ascending=False)
                dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
                dt = df[df.index <= dt ].index.values[changedays]
                log.info("LastDF:%s" % dt)
        else:
            dt = int(dt)+changedays
        # print dt
        # top_now = rl.get_market_price_sina_dd_realTime(df, vol, type)
        # get_tdx_exp_all_LastDF_DL(codelist,dt=duration_date,ptype=ptype)
        split_t = timeit.timeit(lambda : get_tdx_exp_all_LastDF_DL(codelist,dt=duration_date,ptype=ptype), number=run)
        # split_t = timeit.timeit(lambda : get_tdx_all_day_LastDF(codelist,dt=duration_date,ptype=ptype), number=run)
        # split_t = timeit.timeit(lambda: get_tdx_day_to_df_last(codeList, 1, type, dt,ptype),number=run)
        print("df Read:", split_t)

        dt = duration_date
        if len(str(dt)) != 8:
                dl = int(dt)+changedays
                df = get_tdx_day_to_df('999999').sort_index(ascending=False)
                dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
                dt = df[df.index <= dt].index.values[changedays]
                log.info("LastDF:%s" % dt)
        else:
            df = get_tdx_day_to_df('999999').sort_index(ascending=False)
            dl = len(get_tdx_Exp_day_to_df('999999', start=dt)) + changedays
            dt = cct.day8_to_day10(dt)

        # print dt,dl
        # strip_tx = timeit.timeit(lambda: get_tdx_exp_low_or_high_price(codeList, dt, ptype, dl), number=run)
        strip_tx = timeit.timeit(lambda : get_tdx_exp_all_LastDF_DL(codelist, dt=duration_date, ptype=ptype), number=run)
        # strip_tx = timeit.timeit(lambda : get_tdx_exp_all_LastDF(codelist, dt=duration_date, ptype=ptype), number=run)
        print("ex Read:", strip_tx)

def write_to_all():
    st = cct.cct_raw_input("will to Write Y or N:")
    if str(st) == 'y':
        Write_market_all_day_mp('all')
    else:
        print "not write"

def python_resample(qs, xs, rands):
    n = qs.shape[0]
    lookup = np.cumsum(qs)
    results = np.empty(n)

    for j in range(n):
        for i in range(n):
            if rands[j] < lookup[i]:
                results[j] = xs[i]
                break
    return results

def testnumba(number=500):
    import timeit

    n = 100
    xs = np.arange(n, dtype=np.float64)
    qs = np.array([1.0/n,]*n)
    rands = np.random.rand(n)
    from numba.decorators import autojit
    print timeit.timeit(lambda:python_resample(qs, xs, rands),number=number)
    # print timeit.timeit(lambda:cct.run_numba(python_resample(qs, xs, rands)),number=number)
    print timeit.timeit(lambda:autojit(lambda:python_resample(qs, xs, rands)),number=number)
    # print timeit.timeit(lambda:cct.run_numba(python_resample(qs, xs, rands)),number=number)
if __name__ == '__main__':
    import sys
    import timeit
    # testnumba(1000)
    # n = 100
    # xs = np.arange(n, dtype=np.float64)
    # qs = np.array([1.0/n,]*n)
    # rands = np.random.rand(n)
    # print python_resample(qs, xs, rands)

    # print get_tdx_Exp_day_to_df('999999',end=None).sort_index(ascending=False).shape
    # print sina_data.Sina().get_stock_code_data('300006').set_index('code')
#    dd=rl.get_sina_Market_json('cyb').set_index('code')
#    codelist= dd.index.tolist()
#    df = get_tdx_exp_all_LastDF(codelist, dt=30,end=20160401, ptype='high', filter='y')
    # print write_tdx_sina_data_to_file('300583')
    # print get_tdx_Exp_day_to_df('300583',dl=2,newdays=1)

    # write_to_all()
#    print get_tdx_append_now_df_api('600760')[:3]
    # print get_tdx_append_now_df_api('000411')[:3]
    # print get_tdx_Exp_day_to_df('300311',dl=2)[:2]
    # usage()

    # print get_tdx_append_now_df_api_tofile('300583')
    # sys.exit(0)
#    print getSinaAlldf('cx')
#    print get_tdx_exp_low_or_high_power('603585',dl=10,ptype='low')
#    code=['603878','300575']
#    dm = get_sina_data_df(code)
#    code='603878'

    market = cct.cct_raw_input("write all data [all,cyb,sh,sz] :")
    if market in  ['all','sh','sz','cyb']:
        Write_market_all_day_mp(market)
    else:
        print "market is None "


#    print get_tdx_append_now_df_api2('603878',dl=2,dm=dm,newdays=5)
#    print write_tdx_sina_data_to_file('999999',dm)
    code = '999999'
#    print get_sina_data_df(code).index
#    print get_tdx_Exp_day_to_df(code,dl=2)
#    print df.date
    sys.exit(0)

    # print get_tdx_append_now_df_api(code,dl=30)
    # ldatedf = get_tdx_Exp_day_to_df(code,dl=1)
    # lastd = ldatedf.date
    # today = cct.get_today()
    # duration = cct.get_today_duration(lastd)
    # print cct.last_tddate(1)
    print write_tdx_tushare_to_file(code)
    # print lastd,duration,today
#    300035,300047,300039

    # print get_tdx_append_now_df_api(code,dl=30)[:2]
#    print df
#    print write_tdx_tushare_to_file(code,None)
    sys.exit(0)
#
    df= get_tdx_exp_all_LastDF_DL(codeList = codelist, dt=30, end=None, ptype='low', filter='y', power=True)
    # print df[:1]
    sys.exit(0)
    #
    # print get_tdx_write_now_file_api('999999', type='f')
    time_s=time.time()
    print get_tdx_exp_all_LastDF_DL(codeList = [u'000034', u'300290', u'300116', u'300319', u'300375', u'300519'], dt='2016101', end='2016-06-23', ptype='low', filter='n', power=True)
    print "T1:",round(time.time()-time_s,2)
    time_s=time.time()
    print get_tdx_exp_all_LastDF_DL(codeList = [u'300102', u'300290', u'300116', u'300319', u'300375', u'300519'], dt='2016101', end='2016-06-23', ptype='high', filter='n', power=True)
    print "T2:",round(time.time()-time_s,2)

    sys.exit(0)
    print "index_Date:",get_duration_Index_date('999999',dl=3)
    print get_duration_price_date('999999', dl=30, ptype='low', filter=False,power=True)
    print get_duration_price_date('399006', dl=30, ptype='high', filter=False,power=True)
    # print get_duration_price_date('999999', dl=30, ptype='high', filter=False,power=True)
    sys.exit(0)
    # print get_duration_price_date('999999',ptype='high',dt='2015-01-01')
    # print get_duration_price_date('999999',ptype='low',dt='2015-01-01')
    # df = get_tdx_Exp_day_to_df('300311')
    # print get_tdx_stock_period_to_type(df)
    # print get_sina_data_df(['601998','000503'])
    df=get_tdx_power_now_df('000001', start='20160329',end='20160401', type='f', df=None, dm=None)
    print "a",(df)
    print "b",get_tdx_exp_low_or_high_price('999999', dt='20160101',end='20160401', ptype='low',dl=5)
    sys.exit(0)
    # df = get_tdx_exp_all_LastDF(['600000', '603377', '601998', '002504'], dt=20160301,end=20160401, ptype='low', filter='y')
    # list=['000001','399001','399006','399005']
    # df = get_tdx_all_day_LastDF(list,type=1)
    # print df
    '''
    index_d,dl=get_duration_Index_date(dt='20160101')
    print index_d
    get_duration_price_date('000935',ptype='low',dt=index_d)
    df= get_tdx_append_now_df('99999').sort_index(ascending=True)
    print df[-2:]
    '''
    '''
    # df = get_tdx_exp_low_or_high_price('600000', dt='20160304')
    # df,inx = get_duration_price_date('600000',dt='20160301',filter=False)
    df = get_tdx_append_now_df_api('300502',start='2016-03-03')
    # df= get_tdx_append_now_df_api('999999',start='2016-02-01',end='2016-02-27')
    print "a:%s"%df
    # print df[df.index == '2015-02-27']
    # print df[-2:]
    '''
    time_s = time.time()
    # df = get_tdx_Exp_day_to_df('999999')
    # dd = get_tdx_stock_period_to_type(df)
    # df = get_tdx_exp_all_LastDF( ['999999', '603377','603377'], dt=30,ptype='high')
    # df = get_tdx_exp_all_LastDF(['600000', '603377', '601998', '002504'], dt=20160329,end=None, ptype='low', filter='y')
    # print df
    sys.exit(0)
    # tdxdata = get_tdx_all_day_LastDF(['999999', '603377','603377'], dt=30,ptype='high')
    # print get_tdx_Exp_day_to_df('999999').sort_index(ascending=False)[:1]

    # tdxdata = get_tdx_exp_all_LastDF(['999999', '601998', '300499'], dt=20120101, ptype='high')

    print get_tdx_exp_low_or_high_price('600610',dl=30)
    # main_test()
    sys.exit()

    # df = get_tdx_day_to_df_last('999999', dt=30,ptype='high')
    # print df
    # df = get_tdx_exp_low_or_high_price('603377', dt=20160101)
    # print len(df), df
    tdxdata = get_tdx_all_day_LastDF(['999999','601998'])
    # print tdxdata
    # sys.exit(0)

    tdxdata = get_tdx_exp_all_LastDF(['600610', '603377', '000503'], dt=30)
    # tdxdata = get_tdx_all_day_LastDF(['999999','601998'],dt=30)
    print tdxdata

    # dt=get_duration_price_date('999999')
    # print dt

    print "t:", time.time() - time_s
    # df.sort_index(ascending=True,inplace=True)
    # df.index=df.index.apply(lambda x:datetime.time)

    # df.index = pd.to_datetime(df.index)
    # dd = get_tdx_stock_period_to_type(df)
    # print "t:",time.time()-time_s
    # print len(dd)
    # print dd[-1:]

    # df= get_tdx_all_StockList_DF(list,1,1)
    # print df[:6]


    sys.exit(0)
    time_t = time.time()
    # df = get_tdx_allday_lastDF()
    # print "date<2015-08-25:",len(df[(df.date< '2015-08-25')])
    # df= df[(df.date< '2015-08-25')&(df.date > '2015-06-25')]
    # print "2015-08-25-2015-06-25",len(df)
    # print df[:1]
    # print (time.time() - time_t)

    # import sys
    # sys.exit(0)

    # df = rl.get_sina_Market_json('all')
    # code_list = np.array(df.code)
    # print len(code_list)


    # results = cct.to_mp_run_op(get_tdx_day_to_df_last,code_list,2)
    # df=pd.DataFrame((x.get() for x in results),columns=ct.TDX_Day_columns)
    # print df[:1]

    # get_tdx_allday_lastDF()

    # results=cct.to_mp_run(get_tdx_day_to_df,code_list)
    # print results[:2]
    # print len(results)
    # df = rl.get_sina_Market_json('all')
    # print(len(df))
    # code_list = np.array(df.code)
    # get_tdx_all_day_LastDF(code_list)
    # get_tdx_all_day_DayL_DF('all')
    # time.sleep(5)
    # print len(df)
    # df=df.drop_duplicates()
    # print(len(df))
    # for x in df.index:
    #     print df[df.index==x]
    # df=get_tdx_all_day_DayL_DF('all',20)
    # print len(df)
    # dd=pd.DataFrame()
    # for res in df:
    #     print res.get()[:1]
    #     # dd.concat
    #     pass
    # for x in results:
    # print x[:1]
    # df=pd.DataFrame(results,columns=ct.TDX_Day_columns)
    # print df[:1]
    # for res in results:
    #     print res.get()
    # df=pd.DataFrame(results,)
    # for x in  results:
    #     print x
    # for code in results:
    #     print code[:2]
    #     print type(code)
    #     break
    print (time.time() - time_t)

    # print code_list
    # df=get_tdx_day_to_df('002399')
    # print df[-1:]

    # print df[:1]
    # df=get_tdx_day_totxt('002399')
    # print df[:1]
    #
    # df=get_tdx_day_to_df('000001')
    # print df[:1]
    #
    # df=get_tdx_day_totxt('000001')
    # print df[:1]
    #
    # df=get_tdx_day_to_df('600018')
    # df=get_tdx_day_totxt('600018')
    #
    # import tushare as ts
    # print len(df),df[:1]

    # print df[df.]
    # code_stop=[]
    # for code in results:
    #     dt=code.values()[0]
    #     if dt[-1:].index.values < '2015-08-25':
    #         code_stop.append(code.keys())
    # print "stop:",len(code_stop)
    # pprint.pprint(df)


    """
    python readtdxlc5.py 999999 20070101 20070131

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "ht:", ["help", "type="])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(0)
    l_type = 'zip'  # default type is zipfiles!
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
            sys.exit(1)
        elif opt in ("-t", "--type"):
            l_type = arg
    if len(args) < 1:
        print 'You must specified the stock No.!'
        usage(sys.argv[0])
        sys.exit(1)
    """
