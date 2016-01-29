# -*- encoding: utf-8 -*-
import datetime
import os,sys
import platform
import re
import time
from compiler.ast import flatten
from multiprocessing.pool import ThreadPool, cpu_count

import trollius as asyncio
from trollius.coroutines import From
import johnson_cons as ct
import pandas as pd
# log = log.getLogger('commonTipss')


try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import requests

def set_console(width=80,height=15,color=3):
    # mode con cp select=936
    # os.system("mode con: cols=%s lines=%s"%(width,height))
    os.system('title=%s'%sys.argv[0])
    # os.system('color %s'%color)
    pass

# @property
def get_delay_time():
    delay_time=7200
    return delay_time
    
def get_cpu_count():
    return cpu_count()

def get_os_path_sep():
    return os.path.sep

def day8_to_day10(start):
    if start:
        start=str(start)
        if len(start)==8:
            start=start[:4]+'-'+start[4:6]+'-'+start[6:]
            return start
    return None

def get_time_to_date(times,format='%H:%M'):
    #time.gmtime(times) 世界时间
    # time.localtime(times) 本地时间
    return time.strftime(format,time.localtime(times))
    
def get_today(sep='-'):
    TODAY = datetime.date.today()
    fstr="%Y"+sep+"%m"+sep+"%d"
    today = TODAY.strftime(fstr)
    return today

    
# from dateutil import rrule

# def workdays(start, end, holidays=0, days_off=None):
    # start=datetime.datetime.strptime(start,'%Y-%m-%d')
    # end=datetime.datetime.strptime(end,'%Y-%m-%d')
    # if days_off is None:
        # days_off = 0, 6
    # workdays = [x for x in range(7) if x not in days_off]
    # print workdays
    # days = rrule.rrule(rrule.DAILY, start, until=end, byweekday=workdays)
    # return days
    return days.count() - holidays
    
    
def last_tddate(days=0):
    today = datetime.datetime.today().date() + datetime.timedelta(-1)
    day_n=int(today.strftime("%w"))
    # print today,day_n
    if day_n == 0:
        lasd=datetime.datetime.today().date() + datetime.timedelta(-2)
    elif day_n == 1:
        lasd=datetime.datetime.today().date() + datetime.timedelta(-3)
    elif day_n == 6:
        lasd=datetime.datetime.today().date() + datetime.timedelta(-1)
    else:
        lasd=today
    oday = lasd - datetime.timedelta(days)
    day_n=int(oday.strftime("%w"))
    if day_n == 0:
        # print day_last_week(-2)
        return str(datetime.datetime.today().date() + datetime.timedelta(-2))
    elif day_n == 6:
        return str(datetime.datetime.today().date() + datetime.timedelta(-1))
    else:
        return str(oday)

# def is_holiday(date):
#     if isinstance(date, str):
#         date = datetime.datetime.strptime(date, '%Y-%m-%d')
#     today=int(date.strftime("%w"))
#     if today > 0 and today < 6 and date not in holiday:
#         return False
#     else:
#         return True
        
def day_last_week(days=-7):
    lasty = datetime.datetime.today().date() + datetime.timedelta(days)
    return str(lasty)

def is_holiday(date):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    today=int(date.strftime("%w"))
    if today > 0 and today < 6 and date not in holiday:
        return False
    else:
        return True
        
def get_today_duration(datastr):
    today = datetime.date.today()
    last_day = datetime.datetime.strptime(datastr,'%Y-%m-%d').date()
    duration_day=(today-last_day).days
    return int(duration_day)
    
def get_now_time_int():
    now_t = datetime.datetime.now().strftime("%H%M")
    return int(now_t)


def get_work_time():
    now_t = str(get_now_time()).replace(':', '')
    now_t = int(now_t)
    if (now_t > 1131 and now_t < 1300) or now_t < 916 or now_t > 1502:
        # return False
        return False
    else:
        return True


def get_work_duration():
    int_time = get_now_time_int()
    # now_t = int(now_t)
    if (int_time > 830 and int_time <916) or (int_time > 1130 and int_time <1300 ):
        # return False
        return True
    else:
        return False

def get_now_time():
    # now = time.time()
    now = time.localtime()
    # d_time=time.strftime("%Y-%m-%d %H:%M:%S",now)
    d_time = time.strftime("%H:%M", now)
    return d_time

def get_work_time_ratio():
    now = time.localtime()
    ymd = time.strftime("%Y:%m:%d:", now)
    hm1 = '09:30'
    hm2 = '13:00'
    all_work_time = 14400
    d1 = datetime.datetime.now()
    now_t = int(datetime.datetime.now().strftime("%H%M"))
    # d2 = datetime.datetime.strptime('201510111011','%Y%M%d%H%M')
    if now_t>930 and now_t < 1131:
        d2 = datetime.datetime.strptime(ymd + hm1, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        ratio_t = round(ds / all_work_time, 3)

    elif now_t > 1130 and now_t < 1300:
        ratio_t = 0.5
    elif now_t >1500 or now_t <930:
        ratio_t = 1.0
    else:
        d2 = datetime.datetime.strptime(ymd + hm2, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        ratio_t = round((ds+7200) / all_work_time, 3)
    return ratio_t

def get_url_data_R(url):
    # headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive'}
    req = Request(url, headers=headers)
    fp = urlopen(req, timeout=5)
    data = fp.read()
    fp.close()
    return data


def get_url_data(url):
    # headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive'}
    data = requests.get(url, headers=headers,timeout=10)
    # fp = urlopen(req, timeout=5)
    # data = fp.read()
    # fp.close()
    return data.text

def get_div_list(ls, n):
    # if isinstance(codeList, list) or isinstance(codeList, set) or isinstance(codeList, tuple) or isinstance(codeList, pd.Series):

    if not isinstance(ls, list) or not isinstance(n, int):
        return []
    ls_len = len(ls)
    if n <= 0 or 0 == ls_len:
        return []
    if n > ls_len:
        return ls
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        # j = (ls_len / n) + 1
        j = (ls_len / n)
        k = ls_len % n
        # print "K:",k
        ls_return = []
        z = 0
        for i in xrange(0, (n - 1) * j, j):
            if z < k:
                # if i==0:
                #     z+=1
                #     ls_return.append(ls[i+z*1-1:i+j+z*1])
                #     print i+z*1-1,i+j+z*1
                # else:
                z += 1
                ls_return.append(ls[i + z * 1 - 1:i + j + z * 1])
                # print i+z*1-1,i+j+z*1
            else:
                ls_return.append(ls[i + k:i + j + k])
                # print i+k,i + j+k
        # print (n - 1) * j+k,len(ls)
        ls_return.append(ls[(n - 1) * j + k:])
        return ls_return


def to_asyncio_run(urllist, cmd):
    results = []

    # print "asyncio",
    @asyncio.coroutine
    def get_loop_cmd(cmd, url_s):
        loop = asyncio.get_event_loop()
        result = yield From(loop.run_in_executor(None, cmd, url_s))
        results.append(result)

    threads = []
    for url_s in urllist:
        threads.append(get_loop_cmd(cmd, url_s))
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.wait(threads))
    return results


def to_mp_run(cmd, urllist):
    # n_t=time.time()
    print "mp:%s" % len(urllist),

    pool = ThreadPool(cpu_count())
    # pool = ThreadPool(4)
    # print cpu_count()
    # pool = multiprocessing.Pool(processes=8)
    # for code in codes:
    #     results=pool.apply_async(sl.get_multiday_ave_compare_silent_noreal,(code,60))
    # result=[]
    results = pool.map(cmd, urllist)
    # for code in urllist:
    # result.append(pool.apply_async(cmd,(code,)))

    pool.close()
    pool.join()
    results = flatten(results)
    # print "time:MP", (time.time() - n_t)
    return results


def to_mp_run_async(cmd, urllist,*args):
    # n_t=time.time()
    # print "mp_async:%s" % len(urllist),
    pool = ThreadPool(cpu_count())
    # print arg
    # print cpu_count()
    # pool = multiprocessing.Pool(processes=8)
    # for code in codes:
    #     results=pool.apply_async(sl.get_multiday_ave_compare_silent_noreal,(code,60))
    # result=[]
    # results = pool.map(cmd, urllist)
    # for code in urllist:
    # result.append(pool.apply_async(cmd,(code,)))
    results = []
    for code in urllist:
        # result = pool.apply_async(cmd, (code, arg))
        # arg=(code)+','+(args)
        # print arg
        result = pool.apply_async(cmd,(code,)+args).get()
        results.append(result)
    pool.close()
    pool.join()
    # results = flatten(map(lambda x: x.get(), results))
    # results = flatten( results)
    # print "time:MP", (time.time() - n_t)
    return results

def f_print(lens, datastr):
    data = ('{0:%s}' % (lens)).format(str(datastr))
    return data

def _write_to_csv(df, filename, indexCode='code'):
    TODAY = datetime.date.today()
    CURRENTDAY = TODAY.strftime('%Y-%m-%d')
    #     reload(sys)
    #     sys.setdefaultencoding( "gbk" )
    df = df.drop_duplicates(indexCode)
    df = df.set_index(indexCode)
    df.to_csv(CURRENTDAY + '-' + filename + '.csv', encoding='gbk', index=False)  # 选择保存
    print ("write csv")
    # df.to_csv(filename, encoding='gbk', index=False)

def code_to_tdxblk(code):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST[code]
    else:
        if len(code) != 6:
            return ''
        else:
            return '1%s' % code if code[:1] in ['5', '6'] else '0%s' % code

def code_to_symbol(code):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST[code]
    else:
        if len(code) != 6:
            return ''
        else:
            return 'sh%s' % code if code[:1] in ['5', '6','9'] else 'sz%s' % code


def symbol_to_code(symbol):
    """
        生成symbol代码标志
    """
    if symbol in ct.INDEX_LABELS:
        return ct.INDEX_LIST[symbol]
    else:
        if len(symbol) != 8:
            return ''
        else:
            return re.findall('(\d+)', symbol)[0]


def code_to_tdx_blk(code):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST[code]
    else:
        if len(code) != 6:
            return ''
        else:
            return '1%s' % code if code[:1] in ['5', '6'] else '0%s' % code

def write_to_blocknew(p_name, data, append=True):
    if append:
        fout = open(p_name, 'ab+')
        flist = fout.readlines()
    else:
        fout = open(p_name, 'wb')
    # x=0
    for i in data:
        # print type(i)
        if append and len(flist) > 0:
            wstatus = True
            for ic in flist:
                # print code_to_tdxblk(i),ic
                if code_to_tdxblk(i).strip() == ic.strip():
                    wstatus = False
            if wstatus:
                # if x==0:
                #     x+=1
                #     raw='\r\n'+code_to_tdxblk(i)+'\r\n'
                # else:
                raw = code_to_tdxblk(i) + '\r\n'
                fout.write(raw)
        else:
            raw = code_to_tdxblk(i) + '\r\n'
            fout.write(raw)

            # raw = pack('IfffffII', t, i[2], i[3], i[4], i[5], i[6], i[7], i[8])
    ## end for
    fout.close()

def get_sys_platform():
    return platform.platform()


def get_sys_system():
    return platform.system()


def get_run_path():
    path = os.getcwd()
    alist = path.split('stock')
    if len(alist) > 0:
        path = alist[0]
        # os_sep=get_os_path_sep()
        path = path + 'stock' + get_os_path_sep()
    else:
        print "error"
        raise TypeError('log path error.')
    return path

def get_stock_tdx_period_to_type(stock_data,type='w'):
    period_type= type
    #转换周最后一日变量
    stock_data.index = pd.to_datetime(stock_data.index)
    period_stock_data = stock_data.resample(period_type,how='last')
    #周数据的每日change连续相乘
    # period_stock_data['percent']=stock_data['percent'].resample(period_type,how=lambda x:(x+1.0).prod()-1.0)
    #周数据open等于第一日
    period_stock_data['open']=stock_data['open'].resample(period_type,how='first')
    #周high等于Max high
    period_stock_data['high']=stock_data['high'].resample(period_type,how='max')
    period_stock_data['low']=stock_data['low'].resample(period_type,how='min')
    #volume等于所有数据和
    period_stock_data['amount']=stock_data['amount'].resample(period_type,how='sum')
    period_stock_data['vol']=stock_data['vol'].resample(period_type,how='sum')
    #计算周线turnover,【traded_market_value】 流通市值【market_value】 总市值【turnover】 换手率，成交量/流通股本
    # period_stock_data['turnover']=period_stock_data['vol']/(period_stock_data['traded_market_value'])/period_stock_data['close']
    #去除无交易纪录
    period_stock_data=period_stock_data[period_stock_data['code'].notnull()]
    period_stock_data.reset_index(inplace=True)
    return period_stock_data

    

if __name__ == '__main__':
    # print get_run_path()
    # print get_work_time_ratio()
    print last_tddate(0)
    # print workdays('2010-01-01','2010-05-01')
