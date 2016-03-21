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
from JohhnsonUtil import LoggerFactory
from JohhnsonUtil import commonTips as cct
from JohhnsonUtil import johnson_cons as ct
import tushare as ts
import sina_data
# import datetime
# import logbook


# log=logbook.Logger('TDX_day')
log = LoggerFactory.getLogger('TDX_Day')
# log.setLevel(LoggerFactory.DEBUG)
# log.setLevel(LoggerFactory.INFO)
# log.setLevel(LoggerFactory.WARNING)
# log.setLevel(LoggerFactory.ERROR)

path_sep = os.path.sep
newstockdayl = 50
changedays=5

win7rootAsus = r'D:\Program Files\gfzq'
win7rootXunji = r'E:\DOC\Parallels\WinTools\zd_pazq'
win7rootList = [win7rootAsus,win7rootXunji]
macroot = r'/Users/Johnson/Documents/Johnson/WinTools/zd_pazq'
xproot = r'E:\DOC\Parallels\WinTools\zd_pazq'

def get_tdx_dir():
    os_sys = cct.get_sys_system()
    os_platform = cct.get_sys_platform()
    if os_sys.find('Darwin') == 0:
        log.info("DarwinFind:%s" % os_sys)
        basedir = macroot.replace('/', path_sep).replace('\\',path_sep)
        log.info("Mac:%s" % os_platform)

    elif os_sys.find('Win') == 0:
        log.info("Windows:%s" % os_sys)
        if os_platform.find('XP') == 0:
            log.info("XP:%s" % os_platform)
            basedir = xproot.replace('/', path_sep).replace('\\',path_sep)  # 如果你的安装路径不同,请改这里
        else:
            log.info("Win7O:%s" % os_platform)
            for root in win7rootList:
                basedir = root.replace('/', path_sep).replace('\\',path_sep)  # 如果你的安装路径不同,请改这里
                if os.path.exists(basedir):
                    break
    if not os.path.exists(basedir):
        log.error("basedir not exists")
    return basedir

def get_tdx_dir_blocknew():
    blocknew_path = get_tdx_dir() + r'/T0002/blocknew/'.replace('/', path_sep).replace('\\', path_sep)
    return blocknew_path

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
def get_tdx_Exp_day_to_df(code, type='f', start=None, end=None, dt=None, dl=None):
    # start=cct.day8_to_day10(start)
    # end=cct.day8_to_day10(end)
    # day_path = day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
    code_u = cct.code_to_symbol(code)
    log.debug("code:%s code_u:%s" % (code, code_u))
    if type == 'f':
        file_path = exp_path + 'forwardp' + path_sep + code_u.upper() + ".txt"
    elif type == 'b':
        file_path = exp_path + 'backp' + path_sep + code_u.upper() + ".txt"
    else:
        return None
    log.debug("daypath:%s" % file_path)
    # p_day_dir = day_path.replace('/', path_sep).replace('\\', path_sep)
    # p_exp_dir = exp_dir.replace('/', path_sep).replace('\\', path_sep)
    # print p_day_dir,p_exp_dir
    if not os.path.exists(file_path):
        # ds = Series(
        #     {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
        #      'vol': 0})
        ds = pd.DataFrame()
        log.error("file_path:not exists")
        return ds
    # ofile = open(file_path, 'rb')
    if dt is None and dl is None:
        ofile = open(file_path, 'rb')
        buf = ofile.readlines()
        ofile.close()
        num = len(buf)
        no = num - 1
        dt_list = []
        for i in xrange(no):
            a = buf[i].split(',')
            # 01/15/2016,27.57,28.15,26.30,26.97,714833.15,1946604544.000
            # da=a[0].split('/')
            tdate = a[0]
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
            if int(amount) == 0:
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
        df = df.set_index('date')
        df = df.sort_index(ascending=True)
        df['ma5d'] = pd.rolling_mean(df.close,5)
        df['ma10d'] = pd.rolling_mean(df.close,10)
        df['ma20d'] = pd.rolling_mean(df.close,20)
        df['ma60d'] = pd.rolling_mean(df.close,60)
        df = df.sort_index(ascending=False)
        return df
    elif int(dl) == 1:
        # fileSize = os.path.getsize(file_path)
        # if fileSize < 60 * newstockdayl:
        #     return Series()
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
            if len(a) > 5:
                tdate = a[0]
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
                if int(amount) == 0:
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
        # if fileSize < 60 * newstockdayl:
            # return Series()
        data = cct.read_last_lines(file_path, int(dl) + 2)
        dt_list = []
        data_l = data.split('\n')
        data_l.reverse()
        for line in data_l:
            a = line.split(',')
            # 01/15/2016,27.57,28.15,26.30,26.97,714833.15,1946604544.000
            # da=a[0].split('/')
            if len(a) > 5:
                tdate = a[0]
                # tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
                # tdate=dt.strftime('%Y-%m-%d')
                topen = float(a[1])
                thigh = float(a[2])
                tlow = float(a[3])
                tclose = float(a[4])
                tvol = round(float(a[5]) / 10, 2)
                amount = round(float(a[6].replace('\r\n', '')), 1)  # int
                # tpre = int(a[7])  # back
                if int(amount) == 0:
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
        # if start is not None and end is not None:
        #     df = df[(df.date >= start) & (df.date <= end)]
        # elif end is not None:
        #     df = df[df.date <= end]
        # elif start is not None:
        #     df = df[df.date >= start]
        df = df.set_index('date')
        df = df.sort_index(ascending=True)
        df['ma5d'] = pd.rolling_mean(df.close,5)
        df['ma10d'] = pd.rolling_mean(df.close,10)
        df['ma20d'] = pd.rolling_mean(df.close,20)
        df['ma60d'] = pd.rolling_mean(df.close,60)
        df = df.sort_index(ascending=False)
        return df


INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sz399300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006'}

# def get_sina_api_code_now(code):
def get_tdx_append_now_df_api(code, start=None, end=None, type='f'):

    # start=cct.day8_to_day10(start)
    # end=cct.day8_to_day10(end)
    # print start,end
    df = get_tdx_Exp_day_to_df(code, type, start, end).sort_index(ascending=True)
    # print df.index.values[:1],df.index.values[-1:]
    today = cct.get_today()
    if end is not None:
        # print end,df.index[-1]
        if len(df)==0:
            return df
        if end < df.index[-1]:
            print(end, df.index[-1])
            return df
        else:
            today = end
            # return df
            
    if len(df) > 0:
        tdx_last_day = df.index[-1]
    else:
        tdx_last_day = start
    duration = cct.get_today_duration(tdx_last_day)
    log.debug("duration:%s"%duration)
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
        if index_status:
            code_t = INDEX_LIST[code][2:]
        try:
            ds = ts.get_hist_data(code, start=tdx_last_day, end=today)
            # ds = ts.get_h_data('000001', start=tdx_last_day, end=today,index=index_status)
            # df.index = pd.to_datetime(df.index)
        except (IOError, EOFError, Exception) as e:
            print "Error duration", e
            ds = ts.get_h_data(code_t, start=tdx_last_day, end=today, index=index_status)
            df.index = pd.to_datetime(df.index)
        if len(df) > 0:
            lends = len(ds)
        else:
            lends = len(ds) + 1
        if ds is not None and len(ds) > 1:
            ds = ds[:lends - 1]
            if index_status:
                if code == 'sh':
                    code = '999999'
                else:
                    code = code_t
                ds['code'] = code
            else:
                ds['code'] = code
            # ds['vol'] = 0
            ds = ds.loc[:, ['code', 'open', 'high', 'low', 'close', 'volume', 'amount']]
            # ds.rename(columns={'volume': 'amount'}, inplace=True)
            ds.rename(columns={'volume': 'vol'}, inplace=True)
            ds.sort_index(ascending=True, inplace=True)
            log.debug("ds:%s" % ds[:1])
            df = df.append(ds)
            # pd.concat([df,ds],axis=0, join='outer')
            # result=pd.concat([df,ds])
        
        if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 1500:
            log.debug("get_work_time:work")
            # dm = rl.get_sina_Market_json('all').set_index('code')
            if index_status:
                log.debug("code:%s code_t:%s"%(code,code_t))
                dm = sina_data.Sina().get_stock_code_data(code_t,index=index_status)
                dm.code = code
                dm = dm.set_index('code')
            else:
                dm = sina_data.Sina().get_stock_code_data(code,index=index_status).set_index('code')
            log.debug("dm:%s now:%s"%(len(dm),dm))
            if dm is not None and not dm.empty:
                # dm=dm.drop_duplicates()
                # log.debug("not None dm:%s" % dm[-1:])
                dm.rename(columns={'volume': 'amount', 'turnover': 'vol'}, inplace=True)
                c_name=dm.loc[code,['name']].values[0]
                dm_code = (dm.loc[:, ['open', 'high', 'low', 'close', 'amount','vol']])
                log.debug("dm_code:%s" % dm_code)
                dm_code['amount'] = round(float(dm_code['amount']) / 100, 2)
                dm_code['code'] = code
                # dm_code['vol'] = 0
                dm_code['date']=today
                dm_code = dm_code.set_index('date')
                # dm_code.name = today
                log.debug("dm_code_index:%s"%(dm_code))
                df = df.append(dm_code)
                df['name']=c_name
                log.debug("c_name:%s df.name:%s"%(c_name,df.name[-1]))
                # log.debug("df[-3:]:%s" % (df[-2:]))
                # df['name'] = dm.loc[code, 'name']
        else:
            if index_status:
                log.debug("code:%s code_t:%s"%(code,code_t))
                dm = sina_data.Sina().get_stock_code_data(code_t,index=index_status)
                dm.code = code
                dm = dm.set_index('code')
            else:
                dm = sina_data.Sina().get_stock_code_data(code,index=index_status).set_index('code')
            log.debug("dm:%s now:%s"%(len(dm),dm))
            if dm is not None and not dm.empty:
                c_name=dm.loc[code,['name']].values[0]
                df['name']=c_name
                log.debug("c_name:%s df.name:%s"%(c_name,df.name[-1:]))
        log.debug("df:%s" % df[-3:])
        # print df
    return df
              
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


def get_duration_Index_date(code='999999', dt=None, ptype='low'):
    if dt is not None:
        if len(str(dt)) < 8:
            dl = int(dt)+changedays
            df = get_tdx_day_to_df(code).sort_index(ascending=False)
            dt = get_duration_price_date(code, dt=dt,ptype=ptype,df=df)
            dt = df[df.index <= dt].index.values[changedays]
            log.info("LastDF:%s,%s" % (dt,dl))
        else:
            if len(str(dt)) == 8: dt = cct.day8_to_day10(dt)
            df = get_tdx_day_to_df(code).sort_index(ascending=False)
            dl = len(get_tdx_Exp_day_to_df(code, start=dt)) + changedays
            dt = df[df.index <= dt].index.values[changedays]
            log.info("LastDF:%s,%s" % (dt,dl))
        return dt,dl
    return None,None

def get_duration_date(code, ptype='low', dt=None, df='',dl=None):
    if len(df) == 0:
        df = get_tdx_day_to_df(code).sort_index(ascending=False)
        log.debug("code:%s" % (df[:1].index))
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
        return dz[-1:].index.values[0]
    if ptype == 'high':
        lowp = dz.high.max()
        lowdate = dz[dz.high == lowp].index.values[0]
        log.debug("high:%s"%lowdate)
    elif ptype == 'close':
        lowp = dz.close.min()
        lowdate = dz[dz.close == lowp].index.values[0]
        log.debug("high:%s" % lowdate)
    else:
        lowp = dz.low.min()
        lowdate = dz[dz.low == lowp].index.values[0]
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

def get_duration_price_date(code, ptype='low', dt=None, df='',dl=None,vtype=None,filter=True):
    # if code == "600760":
        # log.setLevel(LoggerFactory.DEBUG)
    # else:
        # log.setLevel(LoggerFactory.ERROR)
    if len(df) == 0:
        df = get_tdx_day_to_df(code).sort_index(ascending=False)
        log.debug("code:%s" % (df[:1].index))
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
                    index_d = df[:1].index.values[0]

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
    if len(dz) > 0:
        if ptype == 'high':
            lowp = dz.high.max()
            lowdate = dz[dz.high == lowp].index.values[0]
            log.debug("high:%s" % lowdate)
        elif ptype == 'close':
            lowp = dz.close.min()
            lowdate = dz[dz.close == lowp].index.values[0]
            log.debug("high:%s" % lowdate)
        else:
            lowp = dz.low.min()
            lowdate = dz[dz.low == lowp].index.values[0]
            log.debug("low:%s" % lowdate)
        log.debug("date:%s %s:%s" % (lowdate, ptype, lowp))
    else:
        lowdate = df[:1].index.values[0]
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
    else:
        return lowdate,index_d


def get_tdx_exp_low_or_high_price(code, dt=None, ptype='close', dl=None):
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
        df = get_tdx_Exp_day_to_df(code, dt=dt, dl=dl).sort_index(ascending=False)
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

            if ptype == 'high':
                lowp = dz.close.max()
                lowdate = dz[dz.close == lowp].index.values[0]
                log.debug("high:%s" % lowdate)
            elif ptype == 'close':
                lowp = dz.close.min()
                lowdate = dz[dz.close == lowp].index.values[0]
                log.debug("close:%s" % lowdate)
            else:
                lowp = dz.low.min()
                lowdate = dz[dz.low == lowp].index.values[0]
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
            log.warning("code:%s no < dt:NULL" % (code))
            dd = Series()
            # dd = Series(
            #     {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
            #      'vol': 0})
        return dd
    else:
        dd = get_tdx_Exp_day_to_df(code, dl=1)
        return dd


def get_tdx_day_to_df_last(code, dayl=1, type=0, dt=None, ptype='close', dl=None):
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
        # if no < newstockdayl:
            # return Series()
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


def get_tdx_exp_all_LastDF(codeList, dt=None,ptype='low',filter='n'):
    time_t = time.time()
    # df = rl.get_sina_Market_json(market)
    # code_list = np.array(df.code)
    # if type==0:
    #     results = cct.to_mp_run(get_tdx_day_to_df_last, codeList)
    # else:
    if dt is not None and filter == 'n':
        if len(str(dt)) < 8 :
            dl = int(dt)+changedays
            df = get_tdx_day_to_df('999999').sort_index(ascending=False)
            dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
            dt = df[df.index <= dt].index.values[changedays]
            log.info("LastDF:%s,%s" % (dt,dl))
        else:
            if len(str(dt)) == 8: dt = cct.day8_to_day10(dt)
            df = get_tdx_day_to_df('999999').sort_index(ascending=False)
            dl = len(get_tdx_Exp_day_to_df('999999', start=dt)) + changedays
            dt = df[df.index <= dt].index.values[changedays]
            log.info("LastDF:%s,%s" % (dt,dl))
        results = cct.to_mp_run_async(get_tdx_exp_low_or_high_price, codeList, dt, ptype, dl)
        # results = get_tdx_exp_low_or_high_price(codeList[0], dt,ptype,dl)
        # results=[]
        # for code in codeList:
            # results.append(get_tdx_exp_low_or_high_price(code, dt, ptype, dl))
    elif dt is not None:
        if len(str(dt)) < 8 :
            dl = int(dt)
            df = get_tdx_day_to_df('999999').sort_index(ascending=False)
            dt = get_duration_price_date('999999', dt=dt,ptype=ptype,df=df)
            dt = df[df.index <= dt].index.values[0]
            log.info("LastDF:%s,%s" % (dt,dl))
        else:
            if len(str(dt)) == 8: dt = cct.day8_to_day10(dt)
            # df = get_tdx_day_to_df('999999').sort_index(ascending=False)
            dl = len(ts.get_hist_data('sh', start=dt))
            log.info("LastDF:%s,%s" % (dt,dl))
        results = cct.to_mp_run_async(get_tdx_exp_low_or_high_price, codeList, dt, ptype, dl)
    
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
    stock_data.index = pd.to_datetime(stock_data.index)
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
    period_stock_data.reset_index(inplace=True)
    return period_stock_data


def usage(p):
    print """
python %s [-t txt|zip] stkid [from] [to]
-t txt 表示从txt files 读取数据，否则从zip file 读取(这也是默认方式)
for example :
python %s 999999 20070101 20070302
python %s -t txt 999999 20070101 20070302
    """ % (p, p, p)
def main_test():
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
        split_t = timeit.timeit(lambda : get_tdx_all_day_LastDF(codelist,dt=duration_date,ptype=ptype), number=run)
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
        strip_tx = timeit.timeit(lambda : get_tdx_exp_all_LastDF(codelist, dt=duration_date, ptype=ptype), number=run)
        print("ex Read:", strip_tx)

if __name__ == '__main__':
    import sys
    import timeit
    print get_duration_price_date('999999',dl=30)
    print get_duration_price_date('999999',ptype='high',dt='2015-01-01')
    print get_duration_price_date('999999',ptype='low',dt='2015-01-01')
    sys.exit(0)
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
    # print sina_data.Sina().get_stock_code_data('300006').set_index('code')
    # df = get_tdx_exp_low_or_high_price('600000', dt='20160304')
    # df,inx = get_duration_price_date('600000',dt='20160301',filter=False)
    df = get_tdx_append_now_df_api('300502',start='2016-03-03')
    # df= get_tdx_append_now_df_api('999999',start='2016-02-01',end='2016-02-27')
    print "a:%s"%df
    # print df[df.index == '2015-02-27']
    # print df[-2:]
    '''
    time_s = time.time()
    df = get_tdx_Exp_day_to_df('999999')
    # print get_duration_price_date('999999',dl=100,ptype='high')
    # df = get_tdx_exp_all_LastDF( ['999999', '603377','603377'], dt=30,ptype='high')
    # df = get_tdx_exp_all_LastDF(['600000', '603377', '601998', '002504'], dt=20160304, ptype='low', filter='y')
    print df
    sys.exit(0)
    # tdxdata = get_tdx_all_day_LastDF(['999999', '603377','603377'], dt=30,ptype='high')
    # print get_tdx_Exp_day_to_df('999999').sort_index(ascending=False)[:1]

    # tdxdata = get_tdx_exp_all_LastDF(['999999', '601998', '300499'], dt=20120101, ptype='high')
    
    # print get_tdx_exp_low_or_high_price('600610',dt=20160201,dl=30)
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
