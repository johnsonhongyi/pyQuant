# -*- encoding: utf-8 -*-

import argparse
import datetime
import os
import platform
import re
import sys
import time,random
from compiler.ast import flatten
from multiprocessing.pool import ThreadPool, cpu_count

import pandas as pd
import trollius as asyncio
from trollius.coroutines import From

from LoggerFactory import log
import johnson_cons as ct
import socket

# log = Log.getLogger('root')

# log.setLevel(Log.DEBUG)
# import numba as nb


try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import requests
requests.adapters.DEFAULT_RETRIES = 0

# sys.path.append("..")
# sys.path.append("..")
# print sys.path
# from JSONData import tdx_data_Day as tdd

# def get_os_system():
#     os_sys = get_sys_system()
#     os_platform = get_sys_platform()
#     if os_sys.find('Darwin') == 0:
#         log.info("Mac:%s" % os_platform)
#         return 'mac'

#     elif os_sys.find('Win') == 0:
#         log.info("Windows:%s" % os_sys)
#         if os_platform.find('XP'):
#             return 'win'
#     else:
#         return 'other'
win10Lengend = r'D:\Program\gfzq'
win10Lixin = r'C:\zd_zszq'
win7rootAsus = r'D:\Program Files\gfzq'
win7rootXunji = r'E:\DOC\Parallels\WinTools\zd_pazq'
win7rootList = [win10Lixin,win7rootAsus,win7rootXunji,win10Lengend]
macroot = r'/Users/Johnson/Documents/Johnson/WinTools/zd_pazq'
xproot = r'E:\DOC\Parallels\WinTools\zd_pazq'
ramdisk_root = r'/Volumes/RamDisk'
path_sep = os.path.sep
def get_tdx_dir():
    os_sys = get_sys_system()
    os_platform = get_sys_platform()
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
                    log.info("%s : path:%s" % (os_platform,basedir))
                    break
    if not os.path.exists(basedir):
        log.error("basedir not exists")
    return basedir

def get_ramdisk_path(filename):
    if filename:
        basedir = ramdisk_root.replace('/', path_sep).replace('\\',path_sep)
        if filename.find(basedir) >= 0:
            log.info("file:%s"%(filename))
            return filename

        if not os.path.exists(basedir):
            log.error("basedir not exists")
            return None

        if not filename.endswith('h5'):
            filename = filename + '.h5'

        file_path = basedir  + path_sep + filename 
        # for root in win7rootList:
        #     basedir = root.replace('/', path_sep).replace('\\',path_sep)  # 如果你的安装路径不同,请改这里
        #     if os.path.exists(basedir):
        #         log.info("%s : path:%s" % (os_platform,basedir))
        #         break
    return file_path    
# get_ramdisk_path('/Volumes/RamDisk/top_now.h5')

from numba.decorators import autojit
def run_numba(func):
    funct = autojit(lambda:func)
    return funct

def get_work_path(base,dpath,fname):
    baser = os.getcwd().split(base)[0]
    base = baser  + base + path_sep + dpath + path_sep
    filepath = base + fname
    return filepath

def get_rzrq_code(market='all'):

    baser = os.getcwd().split('stock')[0]
    base = baser  + 'stock' +path_sep + 'JohhnsonUtil' + path_sep
    szrz = base + 'szrzrq.csv'
    shrz = base + 'shrzrq.csv'
    if market in ['all','sz','sh']:
        dfsz = pd.read_csv(szrz,dtype={'code':str},encoding = 'gbk')
        if market == 'sz':
            return dfsz
        dfsh = pd.read_csv(shrz,dtype={'code':str},encoding ='gbk')
        dfsh = dfsh.loc[:,['code','name']]
        if market == 'sh':
            return dfsh
        dd = dfsz.append(dfsh,ignore_index=True)
    elif market == 'cx':
        cxzx = base +  'cxgzx.csv'
        dfot = pd.read_csv(cxzx,dtype={'code':str},sep='\t',encoding ='gbk')
        dd = dfot.loc[:,['code','name']]
    else:
        cxzx = base +  market + '.csv'
        dfot = pd.read_csv(cxzx,dtype={'code':str},sep='\t',encoding ='gbk')
        dd = dfot.loc[:,['code','name']]
    print "rz:%s"%(len(dd)),
    return dd

def get_tushare_market(market='zxb',renew=False,days=5):
    def tusharewrite_to_csv(market,filename,days):
        import tushare as ts
        if market == 'zxb':
            df = ts.get_sme_classified()
        elif market == 'captops':
            df = ts.cap_tops(days).loc[:,['code','name']]
            if days != 10:
                initda = days * 2
                df2 = ts.inst_tops(initda).loc[:,['code','name']]
                df = df.append(df2)
                df.drop_duplicates('code',inplace=True)
        else:
            log.warn('market not found')
            return pd.DataFrame()
        if len(df)>0:
            df = df.set_index('code')
        else:
            log.warn("get error")
        df.to_csv(filename,encoding='gbk')
        log.warn("update %s :%s"%(market,len(df))),
        df.reset_index(inplace=True)
        return df

    baser = os.getcwd().split('stock')[0]
    base = baser  + 'stock' +path_sep + 'JohhnsonUtil' + path_sep
    filepath = base + market+'.csv'
    if os.path.exists(filepath):
        if renew and creation_date_duration(filepath) > 0:
            df = tusharewrite_to_csv(market, filepath, days)
        else:
            df = pd.read_csv(filepath,dtype={'code':str},encoding = 'gbk')
            # df = pd.read_csv(filepath,dtype={'code':str})
            if len(df) == 0:
                df = tusharewrite_to_csv(market, filepath ,days)
    else:
        df = tusharewrite_to_csv(market, filepath , days)

    return df

sina_doc="""sina_Johnson.

Usage:
  sina_cxdn.py
  sina_cxdn.py --debug

Options:
  -h --help     Show this screen.
  --debug    Debug [default:False].
"""

def sys_default_utf8(default_encoding='utf-8'):
    #import sys
#    default_encoding = 'utf-8'
    if sys.getdefaultencoding() != default_encoding:
        reload(sys)
        sys.setdefaultencoding(default_encoding)

sys_default_utf8()

def get_tdx_dir_blocknew():
    blocknew_path = get_tdx_dir() + r'/T0002/blocknew/'.replace('/', path_sep).replace('\\', path_sep)
    return blocknew_path


def isMac():
    if get_sys_system().find('Darwin') == 0:
        return True
    else:
        return False

def check_chinese(checkstr):
    status = re.match('[ \u4e00 -\u9fa5]+',checkstr) == None
    return status
# def whichEncode(text):
#   text0 = text[0]
#   try:
#     text0.decode('utf8')
#   except Exception, e:
#     if "unexpected end of data" in str(e):
#       return "utf8"
#     elif "invalid start byte" in str(e):
#       return "gbk_gb2312"
#     elif "ascii" in str(e):
#       return "Unicode"
#   return "utf8"
def getCoding(strInput):
    '''
    获取编码格式
    '''
    if isinstance(strInput, unicode):
        return "unicode"
    try:
        strInput.decode("utf8")
        return 'utf8'
    except:
        pass
    try:
        strInput.decode("gbk")
        return 'gbk'
    except:
        pass
    try:
        strInput.decode("utf16")
        return 'utf16'
    except:
        pass

def tran2UTF8(strInput):
    '''
    转化为utf8格式
    '''
    strCodingFmt = getCoding(strInput)
    if strCodingFmt == "utf8":
        return strInput
    elif strCodingFmt == "unicode":
        return strInput.encode("utf8")
    elif strCodingFmt == "gbk":
        return strInput.decode("gbk").encode("utf8")

def tran2GBK(strInput):
    '''
    转化为gbk格式
    '''
    strCodingFmt = getCoding(strInput)
    if strCodingFmt == "gbk":
        return strInput
    elif strCodingFmt == "unicode":
        return strInput.encode("gbk")
    elif strCodingFmt == "utf8":
        return strInput.decode("utf8").encode("gbk")



def creation_date_duration(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    # if platform.system() == 'Windows':
    #     return os.path.getctime(path_to_file)
    # else:
    #     stat = os.stat(path_to_file)
    #     try:
    #         return stat.st_birthtime
    #     except AttributeError:
    #         # We're probably on Linux. No easy way to get creation dates here,
    #         # so we'll settle for when its content was last modified.
    #         return stat.st_mtime
    dt = os.path.getmtime(path_to_file)
    dtm = datetime.date.fromtimestamp(dt)
    today = datetime.date.today()
    return (today - dtm).days

def set_ctrl_handler():
    # os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'
    import win32api,thread
    # def doSaneThing(sig, func=None):
        # '''忽略所有KeyCtrl'''
        # return True
    # win32api.SetConsoleCtrlHandler(doSaneThing, 1)
    def handler(dwCtrlType, hook_sigint=thread.interrupt_main):
        print ("ctrl:%s"%(dwCtrlType))
        if dwCtrlType == 0: # CTRL_C_EVENT
            # hook_sigint()
            # raise KeyboardInterrupt("CTRL-C!")
            return 1 # don't chain to the next handler
        return 0 # chain to the next handler
    win32api.SetConsoleCtrlHandler(handler, 1)

def set_console(width=80, height=15, color=3, title=None):
    # mode con cp select=936
    # os.system("mode con: cols=%s lines=%s"%(width,height))
    # print os.path.splitext(sys.argv[0])
    if title is None:
        filename = (os.path.basename(sys.argv[0]))
    elif isinstance(title, list):
        filename = (os.path.basename(sys.argv[0]))
        for cname in title:
            # print cname
            filename = filename + ' ' + str(cname)
            # print filename
    else:
        filename = (os.path.basename(sys.argv[0])) + ' ' + title
    if isMac():
        # os.system('printf "\033]0;%s\007"'%(filename))
        if title is None:
            os.system('printf "\e[8;%s;%st"' % (height, width))
        # printf "\033]0;%s sin ZL: 356.8 To:183 D:3 Sh: 1.73%  Vr:3282.4-3339.7-2.6%  MR: 4.3 ZL: 356.8\007"
        filename = filename.replace('%', '!')
        os.system('printf "\033]0;%s\007"' % (filename))
    else:
        # os.system('title=%s' % sys.argv[0])
        os.system('title=%s' % filename)
        # os.system('mode %s,%s'%(width,height))
    # printf "\033]0;My Window title\007”
    # os.system('color %s'%color)
    # set_ctrl_handler()

def timeit_time(cmd, num=5):
    import timeit
    time_it = timeit.timeit(lambda: cmd, number=num)
    print ("timeit:%s" % time_it)


def get_delay_time():
    delay_time = 8000
    return delay_time

def cct_raw_input(sts):
    # print sts
    try:
        st = raw_input(sts)
    except (KeyboardInterrupt) as e:
        inputerr = cct_raw_input(" Break: ")
#        if inputerr == 'e' or inputerr == 'q':
#            return 'e'
            # raise Exception('raw interrupt')
        if len(inputerr) > 0:
            return inputerr
        else:
            return ''
    except (IOError, EOFError, Exception) as e:
        print "cct_raw_input:ExceptionError", e
    return st

# eval_rule = "[elem for elem in dir() if not elem.startswith('_') and not elem.startswith('ti')]"
# eval_rule = "[elem for elem in dir() if not elem.startswith('_')]"
eval_rule = "[elem for elem in dir() if elem.startswith('top') or elem.startswith('block') or elem.startswith('du') ]"

# import readline
# import rlcompleter, readline
# readline.set_completer(completer.complete)
# readline.parse_and_bind('tab:complete')

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                # self.matches = [s for s in self.options
                #                     if s and s.startswith(text)]
                self.matches = [s for s in self.options
                                   if text in s]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None



def cct_eval(cmd):
    try:
        st = eval(cmd)
    except (Exception) as e:
        st = ''
        print e
    return st
def sleep(timet,catch=True):
    times=time.time()
    try:
        for _ in range(int(timet)*2):
            if int(time.time()-times) >= int(timet):
                break
            time.sleep(0.5)
    except (KeyboardInterrupt) as e:
        # raise KeyboardInterrupt("CTRL-C!")
        # print "Catch KeyboardInterrupt"
        if catch:
            raise KeyboardInterrupt("Sleep Time")
        else:
            pass
        # raise Exception("code is None")
    # print time.time()-times
def sleeprandom(timet):
    now_t = get_now_time_int()
    if now_t > 915 and now_t < 926:
        sleeptime=random.randint(10/3, 10)
    else:
        sleeptime=random.randint(timet/3, timet)
    print "Error2sleep:%s"%(sleeptime)
    sleep(sleeptime,False)

def get_cpu_count():
    return cpu_count()


def get_os_path_sep():
    return os.path.sep


def day8_to_day10(start):
    if start:
        start = str(start)
        if len(start) == 8:
            start = start[:4] + '-' + start[4:6] + '-' + start[6:]
            return start
    return start


def get_time_to_date(times, format='%H:%M'):
    # time.gmtime(times) 世界时间
    # time.localtime(times) 本地时间
    return time.strftime(format, time.localtime(times))


def get_today(sep='-'):
    TODAY = datetime.date.today()
    fstr = "%Y" + sep + "%m" + sep + "%d"
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

def get_work_day_status():
    today = datetime.datetime.today().date()
    day_n = int(today.strftime("%w"))
    if day_n >0 and day_n < 6:
        return True
    else:
        return False
    # return str(today)

def last_tddate(days=1):
    # today = datetime.datetime.today().date() + datetime.timedelta(-days)
    today = datetime.datetime.today().date()
    log.debug("today:%s " % (today))
    # return str(today)
    def get_work_day(today):
        day_n = int(today.strftime("%w"))
        if day_n == 0:
            lastd = today + datetime.timedelta(-2)
            log.debug("0:%s" % lastd)
        elif day_n == 1 :
            lastd = today + datetime.timedelta(-3)
            log.debug("1:%s" % lastd)
        else:
            lastd = today + datetime.timedelta(-1)
            log.debug("2-6:%s" % lastd)
        return lastd
        # if days==0:
        # return str(lasd)
    lastday=today
    for x in range(days):
        # print x
        lastday = get_work_day(today)
        today = lastday
    return str(lastday)

    '''
    oday = lasd - datetime.timedelta(days)
    day_n = int(oday.strftime("%w"))
    # print oday,day_n
    if day_n == 0:
        # print day_last_week(-2)
        return str(datetime.datetime.today().date() + datetime.timedelta(-2))
    elif day_n == 6:
        return str(datetime.datetime.today().date() + datetime.timedelta(-1))
    else:
        return str(oday)
    '''

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
    today = int(date.strftime("%w"))
    if today > 0 and today < 6 and date not in holiday:
        return False
    else:
        return True


def testdf(df):
    if df is not None and len(df) > 0:
        pass
    else:
        pass


def testdf2(df):
    if df is not None and not df.empty:
        pass
    else:
        pass


def get_today_duration(datastr,endday=None):
    if endday:
        today = datetime.datetime.strptime(day8_to_day10(endday), '%Y-%m-%d').date()
    else:
        today = datetime.date.today()
    last_day = datetime.datetime.strptime(datastr, '%Y-%m-%d').date()
    duration_day = (today - last_day).days
    return int(duration_day)

def get_now_time():
    # now = time.time()
    # now = time.localtime()
    # # d_time=time.strftime("%Y-%m-%d %H:%M:%S",now)
    # d_time = time.strftime("%H:%M", now)
    d_time = datetime.datetime.now().strftime("%H:%M")

    return d_time

def get_now_time_int():
    now_t = datetime.datetime.now().strftime("%H%M")
    return int(now_t)


def get_work_time():
    now_t = str(get_now_time()).replace(':', '')
    now_t = int(now_t)
    if not get_work_day_status():
        return False
    if (now_t > 1130 and now_t < 1300) or now_t < 915 or now_t > 1502:
        # return False
        return False
    else:
        # if now_t > 1300 and now_t <1302:
            # sleep(random.randint(5, 120))
        return True

def get_work_hdf_status():
    now_t = str(get_now_time()).replace(':', '')
    now_t = int(now_t)
    if not get_work_day_status():
        return False
    # if (now_t > 1130 and now_t < 1300) or now_t < 915 or now_t > 1502:
    if 915 < now_t < 1502:
        # return False
        return True
    return False

def get_work_duration():
    int_time = get_now_time_int()
    # now_t = int(now_t)
    if get_work_day_status() and (int_time > 800 and int_time < 915) or (int_time > 1130 and int_time < 1300):
    # if (int_time > 830 and int_time < 915) or (int_time > 1130 and int_time < 1300) or (int_time > 1500 and int_time < 1510):
        # return False
        return True
    else:
        return False




def get_work_time_ratio():
    initx=6.5
    stepx=0.5
    init=0
    initAll=10
    now = time.localtime()
    ymd = time.strftime("%Y:%m:%d:", now)
    hm1 = '09:30'
    hm2 = '13:00'
    all_work_time = 14400
    d1 = datetime.datetime.now()
    now_t = int(datetime.datetime.now().strftime("%H%M"))
    # d2 = datetime.datetime.strptime('201510111011','%Y%M%d%H%M')
    if now_t > 915 and now_t <= 930:
        d2 = datetime.datetime.strptime(ymd + '09:29', '%Y:%m:%d:%H:%M')
        d1 = datetime.datetime.strptime(ymd + '09:30', '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        init +=1
        ratio_t = round(ds / all_work_time/(initx+init*stepx)*initAll, 3)
    elif now_t > 930 and now_t <= 1000:
        d2 = datetime.datetime.strptime(ymd + hm1, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        init +=1
        ratio_t = round(ds / all_work_time/(initx+init*stepx)*initAll, 3)
    elif now_t > 1000 and now_t <= 1030:
        d2 = datetime.datetime.strptime(ymd + hm1, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        init +=2
        ratio_t = round(ds / all_work_time/(initx+init*stepx)*initAll, 3)
    elif now_t > 1030 and now_t <= 1100:
        d2 = datetime.datetime.strptime(ymd + hm1, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        init +=3
        ratio_t = round(ds / all_work_time/(initx+init*stepx)*initAll, 3)
    elif now_t > 1100 and now_t <= 1130:
        d2 = datetime.datetime.strptime(ymd + hm1, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        init +=4
        ratio_t = round(ds / all_work_time/(initx+init*stepx)*initAll, 3)
    elif now_t > 1130 and now_t < 1300:
        init +=4
        ratio_t = 0.5/(initx+init*stepx)*initAll
    elif now_t >= 1500 or now_t < 930:
        ratio_t = 1.0
    elif now_t > 1300 and now_t <= 1330:
        d2 = datetime.datetime.strptime(ymd + hm2, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        init +=5
        ratio_t = round((ds + 7200) / all_work_time/(initx+init*stepx)*initAll, 3)
    elif now_t > 1330 and now_t <= 1400:
        d2 = datetime.datetime.strptime(ymd + hm2, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        init +=6
        ratio_t = round((ds + 7200) / all_work_time/(initx+init*stepx)*initAll, 3)
    elif now_t > 1400 and now_t <= 1430:
        d2 = datetime.datetime.strptime(ymd + hm2, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        init +=7
        ratio_t = round((ds + 7200) / all_work_time/(initx+init*stepx)*initAll, 3)
    else:
        d2 = datetime.datetime.strptime(ymd + hm2, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        ratio_t = round((ds + 7200) / all_work_time, 3)

    return ratio_t


def get_url_data_R(url):
    # headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive'}
    req = Request(url, headers=headers)
    try:
        fp = urlopen(req, timeout=10)
        data = fp.read()
        fp.close()
    # except (HTTPError, URLError) as error:
        # log.error('Data of %s not retrieved because %s\nURL: %s', name, error, url)
    except (socket.timeout,socket.error) as e:
    # print data.encoding
        data = ''
        log.error('socket timed out - URL %s', url)
    else:
        log.info('Access successful.')
    return data


def get_url_data(url,retry_count=3,pause=0.05):
#    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive'}

    for _ in range(retry_count):
        time.sleep(pause)
        try:
            data = requests.get(url, headers=headers, timeout=10)
        except (socket.timeout,socket.error) as e:
            data = ''
            log.error('socket timed out - URL %s', url)
        except Exception as e:
                print(e)
        else:
            log.info('Access successful.')
        # print data.text
        # fp = urlopen(req, timeout=5)
        # data = fp.read()
        # fp.close()
        # print data.encoding
            return data.text
    #     else:
    #         return df
    print "url:%s"%(url)
    sleeprandom(10)
    raise IOError(ct.NETWORK_URL_ERROR_MSG)

def get_div_list(ls, n):
    # if isinstance(codeList, list) or isinstance(codeList, set) or
    # isinstance(codeList, tuple) or isinstance(codeList, pd.Series):

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


def to_mp_run_async(cmd, urllist, *args):
    # n_t=time.time()
    # print "mp_async:%s" % len(urllist),
    pool = ThreadPool(cpu_count())
#    print cpu_count()
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
        result = pool.apply_async(cmd, (code,) + args).get()
#            print code,
        results.append(result)
    pool.close()
    pool.join()
    # results = flatten(map(lambda x: x.get(), results))
    # results = flatten( results)
    # print "time:MP", (time.time() - n_t)
    return results


def f_print(lens, datastr,type=None):
    data = ('{0:%s}' % (lens)).format(str(datastr))
    if type is not None:
        if type == 'f':
            return float(data)
    else:
        return data


def read_last_lines(filename, lines=1):
    # print the last line(s) of a text file
    """
    Argument filename is the name of the file to print.
    Argument lines is the number of lines to print from last.
    """
    block_size = 1024
    block = ''
    nl_count = 0
    start = 0
    fsock = file(filename, 'rU')
    try:
        # seek to end
        fsock.seek(0, 2)
        # get seek position
        curpos = fsock.tell()
        # print curpos
        while (curpos > 0):  # while not BOF
            # seek ahead block_size+the length of last read block
            curpos -= (block_size + len(block));
            if curpos < 0: curpos = 0
            fsock.seek(curpos)
            # read to end
            block = fsock.read()
            nl_count = block.count('\n')
            # if read enough(more)
            if nl_count >= lines: break
        # get the exact start position
        for n in range(nl_count - lines ):
            start = block.find('\n', start) + 1
    finally:
        fsock.close()
    return block[start:]


def _write_to_csv(df, filename, indexCode='code'):
    TODAY = datetime.date.today()
    CURRENTDAY = TODAY.strftime('%Y-%m-%d')
    #     reload(sys)
    #     sys.setdefaultencoding( "gbk" )
    df = df.drop_duplicates(indexCode)
    # df = df.set_index(indexCode)
    # print df[['code','name']]
    df.to_csv(CURRENTDAY + '-' + filename + '.csv',
              encoding='gbk', index=False)  # 选择保存
    print("write csv:%s"%(CURRENTDAY + '-' + filename + '.csv'))
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


def code_to_index(code):
    if not code.startswith('999') or not code.startswith('399'):
        if code[:1] in ['5', '6', '9']:
            code2 = '999999'
        elif code[:1] in ['3']:
            code2 = '399006'
        else:
            code2 = '399001'
    return code2


def code_to_symbol(code):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST_TDX[code]
    else:
        if len(code) != 6:
            return ''
        else:
            return 'sh%s' % code if code[:1] in ['5', '6', '9'] else 'sz%s' % code


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
    # index_list = ['1999999','47#IFL0',  '0399006', '27#HSI']
    # index_list = ['1999999','47#IFL0', '27#HSI',  '0399006']
    index_list = ['1999999','47#IFL0', '27#HSI',  '0159915']
    def writeBlocknew(p_name, data, append=True):
        if append:
            fout = open(p_name, 'rb+')
            # fout = open(p_name)
            flist_t = fout.readlines()
            # flist_t = file(p_name, mode='rb+', buffering=None)
            flist=[]
            # errstatus=False
            for code in flist_t:
                if len(code) <= 6 or len(code) > 12:
                    continue
                if not code.endswith('\r\n'):
                    if len(code) <= 6:
                        # errstatus = True
                        continue
                    else:
                        # errstatus = True
                        code = code+'\r\n'
                flist.append(code)
            for co in index_list:
                inx = (co) + '\r\n'
                if inx not in flist:
                    flist.insert(index_list.index(co), inx)
            # if errstatus:
            fout.close()
            fout = open(p_name, 'wb+')
            for code in flist:
                fout.write(code)

            # if not str(flist[-1]).endswith('\r\n'):
                # print "File:%s end not %s"%(p_name[-7:],str(flist[-1]))
            # print "flist", flist
        else:
            fout = open(p_name, 'rb+')
            flist_t = fout.readlines()
            flist=[]
            # flist_t = file(p_name, mode='rb+', buffering=None)
            if len(flist_t) > 4:
                # errstatus=False
                for code in flist_t:
                    if not code.endswith('\r\n'):
                        if len(code) <= 6:
                            # errstatus = True
                            continue
                        else:
                            # errstatus = True
                            code = code+'\r\n'
                    flist.append(code)
                # if errstatus:
                fout.close()
                if p_name.find('066.blk') > 0:
                    writecount = ct.writeblockbakNum
                else:
                    writecount = 9
                flist=flist[:writecount]

                for co in index_list:
                    inx = (co) + '\r\n'
                    if inx not in flist:
                        flist.insert(index_list.index(co), inx)
                # print flist
                fout = open(p_name, 'wb+')
                for code in flist:
                    fout.write(code)
            else:
                fout.close()
                fout = open(p_name, 'wb+')
                # index_list.reverse()
                for i in index_list:
                    raw = (i) + '\r\n'
                    fout.write(raw)

        # x=0
        for i in data:
            # print type(i)
            # if append and len(flist) > 0:
            #     raw = code_to_tdxblk(i).strip() + '\r\n'
            #     if len(raw) > 8 and not raw in flist:
            #         fout.write(raw)
            # else:
            raw = code_to_tdxblk(i) + '\r\n'
            if len(raw) > 8 and not raw in flist:
                fout.write(raw)
                # raw = pack('IfffffII', t, i[2], i[3], i[4], i[5], i[6], i[7], i[8])
        fout.flush()
        fout.close()
    blockNew= get_tdx_dir_blocknew() + 'zxg.blk'
    blockNewStart = get_tdx_dir_blocknew() + '066.blk'
    # writeBlocknew(blockNew, data)
    p_data=['zxg','069','068','067','061']
    if len(p_name) < 5:
        if p_name in p_data:
            p_name = get_tdx_dir_blocknew() + p_name +'.blk'
            print "p_name:%s"%(p_name)
        else:
            print 'p_name is not ok'
            return None

    if p_name.find('061.blk') > 0 or p_name.find('062.blk') > 0 or p_name.find('063.blk') > 0:
        writeBlocknew(p_name, data, append)
        writeBlocknew(blockNew, data)
        writeBlocknew(blockNewStart, data,append)
        print "write to zxg and 066:%s:%s"%(p_name,len(data))
    elif p_name.find('065.blk') > 0:
        writeBlocknew(p_name, data, append)
        writeBlocknew(blockNew,data,append)
        writeBlocknew(blockNewStart, data,append)
        print "write to %s:%s"%(p_name,len(data))
    elif p_name.find('068.blk')  > 0 or p_name.find('069.blk') > 0:

        writeBlocknew(p_name, data, append)
        print "write to %s:%s"%(p_name,len(data))
    else:
        writeBlocknew(p_name, data, append)
        writeBlocknew(blockNew, data)
        # writeBlocknew(blockNewStart, data[:ct.writeCount - 1])
        writeBlocknew(blockNewStart, data,append)
        print "write to other and start:%s :%s"%(p_name,len(data))


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

def getFibonacci(num,days=None):
    res = [0, 1]
    a = 0
    b = 1
    for i in range(0, num):
        if i == a + b:
            res.append(i)
            a, b = b, a + b
    if days is None:
        return res
    else:
        fib = days
        for x in res:
            if days <= x:
                fib = x
                break
        return fib

# def getFibonacciCount(num,days):
    # fibl = getFibonacci(num)
    # fib = days
    # for x in fibl:
        # if days < x:
            # fib = x
            # break
    # return fib

def varname(p):
    import inspect
    import re
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
          return m.group(1)

def varnamestr(obj, namespace=globals()):
    # namestr(a, globals())
    if isinstance(namespace,dict):
        n_list = [name for name in namespace if namespace[name] is obj]
    else:
        log.error("namespce not dict")
        return None
        # n_list = [name for name in namespace if id(name) == id(obj)]

    for n in n_list:
        if n.startswith('_'):
            continue
        else:
            return n
    return None

def get_stock_tdx_period_to_type(stock_data, type='w'):
    period_type = type
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

def MoniterArgmain():

    parser = argparse.ArgumentParser()
    # parser = argparse.ArgumentParser(description='LinearRegression Show')
    parser.add_argument('code', type=str, nargs='?', help='999999')
    parser.add_argument('start', nargs='?', type=str, help='20150612')
    # parser.add_argument('e', nargs='?',action="store", dest="end", type=str, help='end')
    parser.add_argument('end', nargs='?', type=str, help='20160101')
    parser.add_argument('-d', action="store", dest="dtype", type=str, nargs='?', choices=['d', 'w', 'm'], default='d',
                        help='DateType')
    parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['f', 'b'], default='f',
                        help='Price Forward or back')
    # parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low','open','close'], default='close',
    parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low', 'close'], default='close',
                        help='type')
    parser.add_argument('-f', action="store", dest="filter", type=str, choices=['y', 'n'], default='n',
                        help='find duration low')
    return parser

# def writeArgmainParser(args,defaul_all=30):
#     # from ConfigParser import ConfigParser
#     # import shlex
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument('code', type=str, nargs='?', help='w or a or all')
#     parser.add_argument('dl', nargs='?', type=str, help='1,5,10',default=ct.writeCount)
#     parser.add_argument('end', nargs='?', type=str, help='1,5,10',default=None)
#     arg_t = parser.parse_args(args)
#     if arg_t.dl == 'all':
#         # print arg_t.dl
#         arg_t.dl = defaul_all
#     # print arg_t.dl
#     return arg_t

def writeArgmain():
    # from ConfigParser import ConfigParser
    # import shlex
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('code', type=str, nargs='?', help='w or a or all')
    parser.add_argument('dl', nargs='?', type=str, help='1,5,10',default=ct.writeCount)
    parser.add_argument('end', nargs='?', type=str, help='1,5,10',default=None)
    # if parser.code == 'all':
    #     print parser.dl
    # parser.add_argument('end', nargs='?', type=str, help='20160101')
    # parser.add_argument('-d', action="store", dest="dtype", type=str, nargs='?', choices=['d', 'w', 'm'], default='d',
    #                     help='DateType')
    # parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['f', 'b'], default='f',
    #                     help='Price Forward or back')
    # parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['high', 'low', 'close'], default='low',
    #                     help='price type')
    # parser.add_argument('-f', action="store", dest="filter", type=str, choices=['y', 'n'], default='n',
    #                     help='find duration low')
    # parser.add_argument('-l', action="store", dest="dl", type=int, default=None,
    #                     help='dl')
    # parser.add_argument('-dl', action="store", dest="days", type=int, default=1,
    #                     help='days')
    # parser.add_argument('-m', action="store", dest="mpl", type=str, default='y',
    #                     help='mpl show')
    return parser

def DurationArgmain():
    parser = argparse.ArgumentParser()
    # parser = argparse.ArgumentParser(description='LinearRegression Show')
    # parser.add_argument('code', type=str, nargs='?', help='999999')
    parser.add_argument('start', nargs='?', type=str, help='20150612')
    # parser.add_argument('e', nargs='?',action="store", dest="end", type=str, help='end')
    parser.add_argument('end', nargs='?', type=str, help='20160101')
    # parser.add_argument('-d', action="store", dest="dtype", type=str, nargs='?', choices=['d', 'w', 'm'], default='d',
    #                     help='DateType')
    # parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['f', 'b'], default='f',
    #                     help='Price Forward or back')
    # parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low','open','close'], default='close',
    # parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low', 'close'], default='close',
    # help='type')
    parser.add_argument('-f', action="store", dest="filter", type=str, choices=['y', 'n'], default='n',
                        help='filter low')
    return parser

def LineArgmain():
    # from ConfigParser import ConfigParser
    # import shlex
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--start', type=int, dest='start',
    # help='Start date', required=True)
    # parser.add_argument('-e', '--end', type=int, dest='end',
    # help='End date', required=True)
    # parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
    # help='Enable debug info')
    # parser.add_argument('foo', type=int, choices=xrange(5, 10))
    # args = parser.parse_args()
    # print args.square**2
    parser = argparse.ArgumentParser()
    # parser = argparse.ArgumentParser(description='LinearRegression Show')
    parser.add_argument('code', type=str, nargs='?', help='999999')
    parser.add_argument('start', nargs='?', type=str, help='20150612')
    # parser.add_argument('e', nargs='?',action="store", dest="end", type=str, help='end')
    parser.add_argument('end', nargs='?', type=str, help='20160101')
    parser.add_argument('-d', action="store", dest="dtype", type=str, nargs='?', choices=['d', 'w', 'm'], default='d',
                        help='DateType')
    parser.add_argument('-p', action="store", dest="ptype", type=str, choices=['f', 'b'], default='f',
                        help='Price Forward or back')
    # parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low','open','close'], default='close',
    parser.add_argument('-v', action="store", dest="vtype", type=str, choices=['high', 'low', 'close'], default='close',
                        help='type')
    parser.add_argument('-f', action="store", dest="filter", type=str, choices=['y', 'n'], default='y',
                        help='find duration low')
    # parser.add_argument('-help',type=str,help='Price Forward or back')
    # args = parser.parse_args()
    # args=parser.parse_args(input)
    # parser = parseArgmain()
    # args = parser.parse_args(num_input.split())

    # def getArgs():
    # parse=argparse.ArgumentParser()
    # parse.add_argument('-u',type=str)
    # parse.add_argument('-d',type=str)
    # parse.add_argument('-o',type=str)
    # args=parse.parse_args()
    # return vars(args)
    # if args.verbose:
    # logger.setLevel(logging.DEBUG)
    # else:
    # logger.setLevel(logging.ERROR)
    return parser

def sort_by_value(df,column='dff',file=None,count=5,num=5,asc=0):
    """[summary]

    [description]

    Arguments:
        df {dataframe} -- [description]

    Keyword Arguments:
        column {str} -- [description] (default: 'dff' or ['dff',])
        file {[type]} -- [description] (default: {069})
        count {number} -- [description] (default: {5})
        num {number} -- [description] (default: {5})
        asc {number} -- [description] (default: {1} or [0,1])

    Returns:
        [type] -- [description]
    """
    if not isinstance(column, list):
        dd = df.sort_values(by=[column],ascending=[asc])
    else:
        dd = df.sort_values(by=column,ascending=asc)
    if file is None:
        if num >0:
            print dd.iloc[0:num,0:10]
            print dd.iloc[0:num,31:40]
            print dd.iloc[0:num,-15:-4]
        else:
            print dd.iloc[num::,0:10]
            print dd.iloc[0:num,31:40]
            print dd.iloc[num::,-15:-4]
        return dd
    else:
        if str(count) == 'all':
            write_to_blocknew(file, dd.index.tolist(), append=True)
        else:
            write_to_blocknew(file, dd.index.tolist()[:int(count)], append=True)
        print "file:%s"%(file)
if __name__ == '__main__':
    # print get_run_path()
    # print get_work_time_ratio()
    # print typeday8_to_day10(None)
    # write_to_blocknew('abc', ['300380','601998'], append=True)
    print get_work_day_status()
    print get_work_duration()
    print get_today_duration('2017-01-01','20170504')
    # print get_tushare_market(market='captops', renew=True,days=10).shape
    # print get_rzrq_code()[:3]
    # times =1483686638.0
    # print get_time_to_date(times, format='%Y-%m-%d')
    for x in range(1,120,5):
        times=time.time()
        print sleep(x)
        print time.time()-times
    print get_work_time_ratio()
    print getCoding(u'啊中国'.encode("utf16"))
    print get_today_duration('2017-01-06')
    print last_tddate(2)
    print get_work_day_status()
    import sys
    sys.exit(0)
    print get_rzrq_code('cxgzx')[:3]
    print get_rzrq_code('cx')[:3]
    print get_now_time_int()
    print get_now_time()
    print get_work_time_ratio()
    print get_work_day_status()
    print last_tddate(days=3)
    for x in range(0, 4, 1):
        print x
        print last_tddate(x)
        # print last_tddate(2)
    # print get_os_system()
    set_console()
    set_console(title=['G','dT'])
    raw_input("a")
    # print System.IO.Path
    # print workdays('2010-01-01','2010-05-01')
