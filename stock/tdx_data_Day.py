#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division
# import getopt
from struct import *
import os, time
import pandas as pd
from pandas import Series
import realdatajson as rl
import johnson_cons as ct
import numpy as np
from datetime import date
import platform
import LoggerFactory
# import logbook


# log=logbook.Logger('TDX_day')
log=LoggerFactory.getLogger('TDX_Day')
# log.level='info'

def get_today():
    TODAY = date.today()
    today = TODAY.strftime('%Y-%m-%d')
    return today

path_sep = os.path.sep
os_platform=platform.platform()
os_sys=platform.system()
if os_sys.find('Darwin')==0:
    log.info("DarwinFind:%s"%os_sys)
    basedir = r'/Users/Johnson/Documents/Johnson/WinTools/zd_pazq'  # 如果你的安装路径不同,请改这里
elif os_sys.find('Win')==0:
    log.info("Windows:%s"%os_sys)
    if os_platform.find('XP'):
        log.info("XP:%s"%os_platform)
        basedir = r'E:\DOC\Parallels\WinTools\zd_pazq'  # 如果你的安装路径不同,请改这里
    else:
        log.info("Win7O:"%os_platform)
        basedir = r'E:\DOC\Parallels\WinTools\zd_pazq'  # 如果你的安装路径不同,请改这里

exp_dir = basedir + r'/T0002/export/'
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

day_path = {'sh': day_dir_sh, 'sz': day_dir_sz}

stkdict = {}  # 存储股票ID和上海市、深圳市的对照

code_u = 'sz002399'


# http://www.douban.com/note/504811026/

def get_tdx_day_to_df_dict(code):
    # time_s=time.time()
    code_u = rl._code_to_symbol(code)
    day_path = day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
    p_day_dir = day_path.replace('/', path_sep).replace('\\', path_sep)
    # p_exp_dir=exp_dir.replace('/',path_sep).replace('\\',path_sep)
    # print p_day_dir,p_exp_dir
    file_path = p_day_dir + code_u + '.day'
    if not os.path.exists(file_path):
        ds=Series(
            {'code': code, 'date':get_today() , 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
             'vol': 0})
        return ds
    ofile = open(file_path, 'rb')
    buf = ofile.read()
    ofile.close()
    # ifile=open(p_exp_dir+code_u+'.txt','w')
    num = len(buf)
    # print num
    no = int(num / 32)
    # print no
    b = 0
    e = 32
    dict_t = []
    for i in xrange(no):
        a = unpack('IIIIIfII', buf[b:e])
        # tdate=str(a[0])
        tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
        topen = str(a[1] / 100.0)
        thigh = str(a[2] / 100.0)
        tlow = str(a[3] / 100.0)
        tclose = str(a[4] / 100.0)
        amount = str(a[5] / 10.0)
        tvol = str(a[6])  # int
        tpre = str(a[7])  # back
        # line=str(a[0])+' '+str(a[1]/100.0)+' '+str(a[2]/100.0)+' '+str(a[3]/100.0)+\
        # ' '+str(a[4]/100.0)+' '+str(a[5]/10.0)+' '+str(a[6])+' '+str(a[7])+' '+'\n'
        # print line
        # list_t.append(tdate,topen,thigh,tlow,tclose,tvolp,tvol,tpre)
        # dict_t[tdate]={'date':tdate,'open':topen,'high':thigh,'low':tlow,'close':tclose,'volp':tvolp,'vol':tvol,'pre':tpre}
        dict_t.append(
            {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose, 'amount': amount,
             'vol': tvol, 'pre': tpre})
        b = b + 32
        e = e + 32
    # df=pd.DataFrame.from_dict(dict_t,orient='index')
    df = pd.DataFrame(dict_t, columns=ct.TDX_Day_columns)
    df = df.set_index('date')
    return {code: df}


def get_tdx_day_to_df(code):
    # time_s=time.time()
    # print code
    code_u = rl._code_to_symbol(code)
    day_path = day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
    p_day_dir = day_path.replace('/', path_sep).replace('\\', path_sep)
    p_exp_dir = exp_dir.replace('/', path_sep).replace('\\', path_sep)
    # print p_day_dir,p_exp_dir
    file_path = p_day_dir + code_u + '.day'
    if not os.path.exists(file_path):
        ds=Series(
            {'code': code, 'date':get_today() , 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
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
        topen = str(a[1] / 100.0)
        thigh = str(a[2] / 100.0)
        tlow = str(a[3] / 100.0)
        tclose = str(a[4] / 100.0)
        amount = str(a[5] / 10.0)
        tvol = str(a[6])  # int
        tpre = str(a[7])  # back
        dt_list.append(
            {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose, 'amount': amount,
             'vol': tvol, 'pre': tpre})
        b = b + 32
        e = e + 32
    df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
    df = df.set_index('date')
    # print "time:",(time.time()-time_s)*1000
    return df


def get_tdx_day_to_df_last(code, dayl=1):
    code_u = rl._code_to_symbol(code)
    day_path = day_dir % 'sh' if code[:1] in ['5', '6', '9'] else day_dir % 'sz'
    p_day_dir = day_path.replace('/', path_sep).replace('\\', path_sep)
    # p_exp_dir=exp_dir.replace('/',path_sep).replace('\\',path_sep)
    # print p_day_dir,p_exp_dir
    file_path = p_day_dir + code_u + '.day'
    if not os.path.exists(file_path):
        ds=Series(
            {'code': code, 'date':get_today() , 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'amount': 0,
             'vol': 0})
        return ds
    ofile = file(file_path, 'rb')
    b = 0
    e = 32
    if dayl == 1:
        fileSize = os.path.getsize(file_path)
        if fileSize<32:print "why",code
        ofile.seek(-e, 2)
        buf=ofile.read()
        ofile.close()
        a = unpack('IIIIIfII', buf[b:e])
        tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
        topen = str(a[1] / 100.0)
        thigh = str(a[2] / 100.0)
        tlow = str(a[3] / 100.0)
        tclose = str(a[4] / 100.0)
        amount = str(a[5] / 10.0)
        tvol = str(a[6])  # int
        # tpre = str(a[7])  # back
        dt_list=Series(
            {'code': code, 'date': tdate, 'open': topen, 'high': thigh, 'low': tlow, 'close': tclose, 'amount': amount,
             'vol': tvol})
        return dt_list
    else:
        dt_list=[]
        fileSize = os.path.getsize(file_path)
        day_cout = abs(e * dayl)
        # print day_cout
        if day_cout > fileSize:
            b=fileSize
            ofile.seek(-fileSize, 2)
            no=int(fileSize/e)
        else:
            no=dayl
            b=day_cout
            ofile.seek(-day_cout,2)
        # print no,b,day_cout,fileSize
        buf=ofile.read()
        # print repr(buf)
        # df=pd.DataFrame()
        for i in xrange(no):
            a = unpack('IIIIIfII', buf[-e:b])
            tdate = str(a[0])[:4] + '-' + str(a[0])[4:6] + '-' + str(a[0])[6:8]
            topen = str(a[1] / 100.0)
            thigh = str(a[2] / 100.0)
            tlow = str(a[3] / 100.0)
            tclose = str(a[4] / 100.0)
            amount = str(a[5] / 10.0)
            tvol = str(a[6])  # int
            # tpre = str(a[7])  # back
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
def get_tdx_all_day_LastDF(codeList):
    time_t = time.time()
    # df = rl.get_sina_Market_json(market)
    # code_list = np.array(df.code)
    results = rl.to_mp_run(get_tdx_day_to_df_last, codeList)
    df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    df = df.set_index('code')
    df.loc[:,'open':] =df.loc[:,'open':].astype(float)
    df.vol=df.vol.apply(lambda x:x/100)
    log.info("get_to_mp:%s"%(len(df)))

    # print len(df)
    # print "<2015-08-25",len(df[(df.date< '2015-08-25')])
    # print "06-25-->8-25'",len(df[(df.date< '2015-08-25')&(df.date > '2015-06-25')])
    log.info("TDXTime:%s" %(time.time() - time_t))
    return df

def get_tdx_all_day_DayL_DF(market='cyb',dayl=1):
    time_t = time.time()
    df = rl.get_sina_Market_json(market)
    code_list = np.array(df.code)
    log.info('code_list:%s'%len(code_list))
    results = rl.to_mp_run_op(get_tdx_day_to_df_last, code_list,dayl)
    log.info("get_to_mp_op:%s"%(len(results)))
    # df = pd.DataFrame(results, columns=ct.TDX_Day_columns)
    # df = df.set_index('code')
    # print df[:1]

    # print len(df),df[:1]
    # print "<2015-08-25",len(df[(df.date< '2015-08-25')])
    # print "06-25-->8-25'",len(df[(df.date< '2015-08-25')&(df.date > '2015-06-25')])
    print "t:", time.time() - time_t
    return results

def usage(p):
    print """
python %s [-t txt|zip] stkid [from] [to]
-t txt 表示从txt files 读取数据，否则从zip file 读取(这也是默认方式)
for example :
python %s 999999 20070101 20070302
python %s -t txt 999999 20070101 20070302
    """ % (p, p, p)


if __name__ == '__main__':
    # df = get_tdx_day_to_df_last('601198',1)
    # print df
    import sys

    # sys.exit(0)
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


    # results = rl.to_mp_run_op(get_tdx_day_to_df_last,code_list,2)
    # df=pd.DataFrame((x.get() for x in results),columns=ct.TDX_Day_columns)
    # print df[:1]

    # get_tdx_allday_lastDF()

    # results=rl.to_mp_run(get_tdx_day_to_df,code_list)
    # print results[:2]
    # print len(results)
    df = rl.get_sina_Market_json('all')
    print(len(df))
    code_list = np.array(df.code)
    get_tdx_all_day_LastDF(code_list)
    get_tdx_all_day_DayL_DF('all')
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
