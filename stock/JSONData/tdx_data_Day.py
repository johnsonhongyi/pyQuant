# -*- encoding: utf-8 -*-
# !/usr/bin/python
from __future__ import division

import os
import sys
import time
from struct import *

import numpy as np
import pandas as pd
from pandas import Series
sys.path.append("..")
from JSONData import realdatajson as rl
from JohhnsonUtil import LoggerFactory
from JohhnsonUtil import commonTips as cct
from JohhnsonUtil import johnson_cons as ct
import tushare as ts

# import datetime
# import logbook


# log=logbook.Logger('TDX_day')
log = LoggerFactory.getLogger('TDX_Day')
# log.setLevel(LoggerFactory.DEBUG)
# log.setLevel(LoggerFactory.INFO)

path_sep = os.path.sep


def get_tdx_dir():
    os_sys = cct.get_sys_system()
    os_platform = cct.get_sys_platform()
    if os_sys.find('Darwin') == 0:
        log.info("DarwinFind:%s" % os_sys)
        basedir = r'/Users/Johnson/Documents/Johnson/WinTools/zd_pazq'.replace('/', path_sep).replace('\\',
                                                                                                      path_sep)  # 如果你的安装路径不同,请改这里
        log.info("Mac:%s" % os_platform)

    elif os_sys.find('Win') == 0:
        log.info("Windows:%s" % os_sys)
        if os_platform.find('XP'):
            log.info("XP:%s" % os_platform)
            basedir = r'E:\DOC\Parallels\WinTools\zd_pazq'.replace('/', path_sep).replace('\\',
                                                                                          path_sep)  # 如果你的安装路径不同,请改这里
        else:
            log.info("Win7O:" % os_platform)
            basedir = r'E:\DOC\Parallels\WinTools\zd_pazq'.replace('/', path_sep).replace('\\',
                                                                                          path_sep)  # 如果你的安装路径不同,请改这里
    return basedir


def get_tdx_dir_blocknew():
    blocknew_path = get_tdx_dir() + r'/T0002/blocknew/'.replace('/', path_sep).replace('\\', path_sep)
    return blocknew_path


basedir = get_tdx_dir()
# path_sep = os.path.sep
# exp_dir = get_tdx_dir() + r'/T0002/export/'
blocknew = r'/Users/Johnson/Documents/Johnson/WinTools/zd_pazq/T0002/blocknew'
# blocknew = 'Z:\Documents\Johnson\WinTools\zd_pazq\T0002\blocknew'
# exp_dir    = basedir + r'\T0002\export_back'
lc5_dir_sh = basedir + r'\Vipdoc\sh\fzline'
# lc5_dir_sh =  r'D:\2965\ydzqwsjy\Vipdoc\sh\fzline'
lc5_dir_sz = basedir + r'\Vipdoc\sz\fzline'
lc5_dir = basedir + r'\Vipdoc\%s\fzline'
day_dir = basedir + r'\Vipdoc\%s\lday/'
day_dir_sh = basedir + r'\Vipdoc\sh\lday/'
day_dir_sz = basedir + r'/Vipdoc/sz/lday/'
exp_path = basedir + "/T0002/export/".replace('/', path_sep).replace('\\', path_sep)
day_path = {'sh': day_dir_sh, 'sz': day_dir_sz}


# stkdict = {}  # 存储股票ID和上海市、深圳市的对照

# code_u = 'sz002399'


# http://www.douban.com/note/504811026/
def get_tdx_Exp_day_to_df(code, type='f', start=None, end=None, dt=None):
    # start=cct.day8_to_day10(start)
    # end=cct.day8_to_day10(end)
    # day_path = day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
    code_u = cct.code_to_symbol(code)
    log.info("code:%s code_u:%s" % (code, code_u))
    if type == 'f':
        file_path = exp_path + 'forwardp' + path_sep + code_u.upper() + ".txt"
    elif type == 'b':
        file_path = exp_path + 'backp' + path_sep + code_u.upper() + ".txt"
    else:
        return ''
    log.info("daypath:%s" % file_path)
    # p_day_dir = day_path.replace('/', path_sep).replace('\\', path_sep)
    # p_exp_dir = exp_dir.replace('/', path_sep).replace('\\', path_sep)
    # print p_day_dir,p_exp_dir
    if not os.path.exists(file_path):
        # ds = Series(
        #     {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
        #      'vol': 0})
        ds = pd.DataFrame()
        log.info("file_path:not exists")
        return ds
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
        tvol = round(float(a[5]) / 10, 2)
        amount = round(float(a[6].replace('\r\n', '')), 1)  # int
        # tpre = int(a[7])  # back
        if int(amount) == 0:
            continue
        dt_list.append(
            {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose, 'amount': amount,
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
    # print "time:",(time.time()-time_s)*1000
    return df


INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sz399300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006'}


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
    else:
        tdx_last_day = None
        duration = 1
    log.info("tdx_last_day:%s" % tdx_last_day)
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
            dm = rl.get_sina_Market_json('all').set_index('code')
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
            log.debug("df[-3:]:%s" % (df[-3:]))
            df['name'] = dm.loc[code, 'name']
        log.debug("df:%s" % df[-3:])
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


def get_duration_price_date(code, ptype='low', dt=None, dl=34, df=''):
    if len(df) == 0:
        df = get_tdx_day_to_df(code).sort_index(ascending=False)
        log.info("code:%s" % (df[:1].index))
        # print "df",len(df)
    if dt != None:
        dz = df[df.index >= dt]
        if len(dz) == 0:
            # print code,df[:1].index.values[0]
            return df[:1].index.values[0]
    else:
        if len(df) > int(dl):
            dz = df[:int(dl)]
        else:
            dz = df
    if ptype == 'high':
        lowp = dz.low.max()
    else:
        lowp = dz.low.min()
    lowdate = dz[dz.low == lowp].index.values[0]
    log.info("date:%s %s:%s" % (lowdate, ptype, lowp))
    return lowdate


def get_tdx_exp_low_or_high_price(code, dt=None, ptype='low', dl=20):
    '''
    :param code:999999
    :param dayl:Duration Days
    :param type:TDX type
    :param dt:  Datetime
    :param ptype:low or high
    :return:Series or df
    '''
    dt = cct.day8_to_day10(dt)
    df = get_tdx_Exp_day_to_df(code, dt=dt).sort_index(ascending=False)
    # if df is not None and df.empty:
    #     dd = Series(
    #         {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
    #          'vol': 0})
    #     return dd
    if not df.empty:
        if dt is not None:
            dz = df[df.index >= dt]
            if dz.empty:
                dd = Series(
                    {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
                     'vol': 0})
                return dd
        else:
            if len(df) > int(dl):
                dz = df[:int(dl)]
            else:
                dz = df
        if ptype == 'high':
            lowp = dz.low.max()
        else:
            lowp = dz.low.min()
        dt = dz[dz.low == lowp].index.values[0]
        log.info("date:%s %s:%s" % (dt, ptype, lowp))
        dd = df[df.index <= dt]
        if len(dd) > 0:
            dd = dd[:1]
            dt = dd.index.values[0]
            dd = dd.T[dt]
            dd['date'] = dt
    else:
        log.debug("no < dt:NULL")
        dd = Series(
            {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
             'vol': 0})
    return dd


def get_tdx_day_to_df_last(code, dayl=1, type=0, dt=None, ptype='low'):
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
    elif dayl == 1 and dt is not None:
        log.info("dt:%s" % (dt))
        dt_list = []
        if len(str(dt)) == 8:
            dt = cct.day8_to_day10(dt)
        fileSize = os.path.getsize(file_path)
        if fileSize < 32: print "why", code
        b = fileSize
        ofile.seek(-fileSize, 2)
        no = int(fileSize / e)
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
            if tdate < dt:
                break
        df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
        df = df.set_index('date')
        dt = get_duration_price_date(code, ptype=ptype, dt=dt, df=df)
        log.info('last_dt:%s' % dt)
        dd = df[df.index <= dt]
        if len(dd) > 0:
            dd = dd[:1]
            dt = dd.index.values[0]
            dd = dd.T[dt]
            dd['date'] = dt
        else:
            log.debug("no < dt:NULL")
            dd = Series(
                {'code': code, 'date': cct.get_today(), 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
                 'vol': 0})
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
def get_tdx_all_day_LastDF(codeList, type=0, dt=None):
    time_t = time.time()
    # df = rl.get_sina_Market_json(market)
    # code_list = np.array(df.code)
    # if type==0:
    #     results = cct.to_mp_run(get_tdx_day_to_df_last, codeList)
    # else:
    if len(str(dt)) != 8:
        dt = get_duration_price_date('999999', dl=dt)
        log.info("LastDF:%s" % dt)
    results = cct.to_mp_run_async(get_tdx_day_to_df_last, codeList, 1, type, dt)
    # print results
    df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    df = df.set_index('code')
    df.loc[:, 'open':] = df.loc[:, 'open':].astype(float)
    # df.vol = df.vol.apply(lambda x: x / 100)
    log.info("get_to_mp:%s" % (len(df)))
    log.info("TDXTime:%s" % (time.time() - time_t))
    if dt != None:
        print ("TDX:%0.2f" % (time.time() - time_t)),
    return df


def get_tdx_exp_all_LastDF(codeList, dt=None):
    time_t = time.time()
    # df = rl.get_sina_Market_json(market)
    # code_list = np.array(df.code)
    # if type==0:
    #     results = cct.to_mp_run(get_tdx_day_to_df_last, codeList)
    # else:
    if len(str(dt)) != 8:
        dt = get_duration_price_date('999999', dl=dt)
        log.info("LastDF:%s" % dt)
    results = cct.to_mp_run_async(get_tdx_exp_low_or_high_price, codeList, dt)
    # print results
    df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    df = df.set_index('code')
    df.loc[:, 'open':] = df.loc[:, 'open':].astype(float)
    # df.vol = df.vol.apply(lambda x: x / 100)
    log.info("get_to_mp:%s" % (len(df)))
    log.info("TDXTime:%s" % (time.time() - time_t))
    if dt != None:
        print ("TDX:%0.2f" % (time.time() - time_t)),
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


if __name__ == '__main__':
    import sys

    # list=['000001','399001','399006','399005']
    # df = get_tdx_all_day_LastDF(list,type=1)
    # print df
    # get_tdx_append_now_df('999999')
    # sys.exit(0)
    time_s = time.time()
    df = get_tdx_Exp_day_to_df('999999')
    print df[:1]
    # df = get_tdx_day_to_df_last('999999', dt=20160101)
    # print df
    df = get_tdx_exp_low_or_high_price('603377', dt=20160101)
    # print len(df), df

    # tdxdata = get_tdx_all_day_LastDF(['999999', '601998'], dt=2000)
    # # tdxdata = get_tdx_all_day_LastDF(['999999','601998'])
    # print tdxdata

    tdxdata = get_tdx_exp_all_LastDF(['999999', '603377', '000503'], dt=30)
    # tdxdata = get_tdx_all_day_LastDF(['999999','601998'])
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
