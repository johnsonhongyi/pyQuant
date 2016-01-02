# -*- encoding: utf-8 -*-
import datetime
import os
import platform
import re
import time
from multiprocessing.pool import ThreadPool, cpu_count

from stock.JohhnsonUtil import johnson_cons as ct

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


def get_os_path_sep():
    return os.path.sep


def get_today():
    TODAY = datetime.date.today()
    today = TODAY.strftime('%Y-%m-%d')
    return today


def get_now_time():
    # now = time.time()
    now = time.localtime()
    # d_time=time.strftime("%Y-%m-%d %H:%M:%S",now)
    d_time = time.strftime("%H:%M", now)
    return d_time


def get_url_data(url):
    # headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive'}
    req = Request(url, headers=headers)
    fp = urlopen(req, timeout=5)
    data = fp.read()
    fp.close()
    return data


def get_div_list(ls, n):
    # if isinstance(codeList, list) or isinstance(codeList, set) or isinstance(codeList, tuple) or isinstance(codeList, pd.Series):

    if not isinstance(ls, list) or not isinstance(n, int):
        return []
    ls_len = len(ls)
    if n <= 0 or 0 == ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = (ls_len / n) + 1
        k = ls_len % n
        ls_return = []
        for i in xrange(0, (n - 1) * j, j):
            ls_return.append(ls[i:i + j])
        ls_return.append(ls[(n - 1) * j:])
        return ls_return


def to_mp_run(cmd, urllist):
    # n_t=time.time()
    pool = ThreadPool(cpu_count())
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
    # print "time:MP", (time.time() - n_t)
    return results


def to_mp_run_async(cmd, urllist):
    # n_t=time.time()
    pool = ThreadPool(cpu_count())
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
    # print "time:MP", (time.time() - n_t)
    return results


def to_mp_run_op(cmd, urllist, arg=1):
    # n_t=time.time()
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
        result = pool.apply_async(cmd, (code, arg))
        results.append(result)
    pool.close()
    pool.join()
    # print "time:MP", (time.time() - n_t)
    return results


def _get_url_data_old(url):
    # headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive'}
    req = Request(url, headers=headers)
    fp = urlopen(req, timeout=5)
    data = fp.read()
    fp.close()
    return data


def _get_url_data(url):
    # headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive'}
    data = requests.get(url, headers=headers)
    # fp = urlopen(req, timeout=5)
    # data = fp.read()
    # fp.close()
    return data.text


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
            return 'sh%s' % code if code[:1] in ['5', '6'] else 'sz%s' % code


def symbol_to_code(symbol):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST[code]
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
