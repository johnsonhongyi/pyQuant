# -*- coding: UTF-8 -*-
import tushare as ts
import emacount as ema
import time
import types
import realdatajson as rd
import johnson_cons as ct
import pandas as pd
import datetime
import sys, traceback
import fundflowUtil as ffu

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


def time_sleep(timemin):
    time1 = time.time()
    time.sleep(timemin)
    return True


def get_now_time_num():
    now_t = datetime.datetime.now().strftime("%H%M")
    return int(now_t)


def get_now_time():
    now = time.time()
    now = time.localtime(now)
    # d_time=time.strftime("%Y-%m-%d %H:%M:%S",now)
    d_time = time.strftime("%H:%M", now)
    return d_time


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


def get_work_time():
    now_t = str(get_now_time()).replace(':', '')
    # now_t = int(now_t)
    if (now_t > '1131' and now_t < '1300') or (now_t < '0924' or now_t > '1502'):
        # return False
        return True
    else:
        return True


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


def get_all_toplist():
    # gold = {}
    # goldl = []
    df = ts.get_today_all()
    top = df[df['changepercent'] > 6]
    top = top[top['changepercent'] < 10]
    # logging.info("top:", len(top['code']))
    list = top['code']
    print len(list)
    return list


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


def get_multiday_ave_compare(code, dayl='10'):
    dtick = ts.get_today_ticks(code)
    d_hist = ema.getdata_ema_trend(code, dayl, 'd')
    # print d_hist
    day_t = ema.get_today()
    if day_t in d_hist.index:
        dl = d_hist.drop(day_t).index
    else:
        dl = d_hist.index
    # print dl
    # print dl
    ep_list = []
    for da in dl.values:
        # print da
        td = ts.get_tick_data(code, da)
        # print td
        if not type(td) == types.NoneType:
            ep = td['amount'].sum() / td['volume'].sum()
            ep_list.append(ep)
            print ("D: %s P: %s" % (da[-5:], ep))
    ave = ema.less_average(ep_list)
    if len(dtick.index) > 0:
        ep = dtick['amount'].sum() / dtick['volume'].sum()
        p_now = dtick['price'].values[0] * 100
        if p_now > ave and ep > ave:
            print ("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" % (code, ep, p_now, ave, get_now_time()))
        elif p_now > ave and ep < ave:
            print ("gold:%s ep:%s UP:%s! A:%s %s !" % (code, ep, p_now, ave, get_now_time()))
        elif p_now < ave and ep > ave:
            print ("down:%s ep:%s Dow:%s? A:%s %s ?" % (code, ep, p_now, ave, get_now_time()))
        else:
            print ("DOWN:%s ep:%s now:%s??? A:%s %s ???" % (code, ep, p_now, ave, get_now_time()))
    return ave


def get_multiday_ave_compare_silent(code, dayl='10'):
    dtick = ts.get_today_ticks(code)
    d_hist = ema.getdata_ema_trend_silent(code, dayl, 'd')
    # print d_hist
    day_t = ema.get_today()
    if day_t in d_hist.index:
        dl = d_hist.drop(day_t).index
    else:
        dl = d_hist.index
    # print dl
    # print dl
    ep_list = []
    for da in dl.values:
        # print code,da
        td = ts.get_tick_data(code, da)
        # print td
        if not type(td) == types.NoneType:
            ep = td['amount'].sum() / td['volume'].sum()
            ep_list.append(ep)
            # print ("D: %s P: %s" % (da[-5:], ep))
    ave = ema.less_average(ep_list)
    if len(dtick.index) > 0:
        ep = dtick['amount'].sum() / dtick['volume'].sum()
        p_now = dtick['price'].values[0] * 100
        if p_now > ave or ep > ave:
            print ("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" % (code, ep, p_now, ave, get_now_time()))
            # elif p_now > ave and ep < ave:
            #     print ("gold:%s ep:%s UP:%s! A:%s %s !" % (code, ep, p_now, ave, get_now_time()))
            # elif p_now < ave and ep > ave:
            #     print ("down:%s ep:%s Dow:%s? A:%s %s ?" % (code, ep, p_now, ave, get_now_time()))
            return True
        else:
            if p_now < ave and ep < ave:
                print ("DOWN:%s ep:%s now:%s??? A:%s %s ???" % (code, ep, p_now, ave, get_now_time()))
            return False
            # return ave


def get_yestoday_tick_status(code, ave=None):
    try:
        dn = get_realtime_quotes(code)

        dtick = ts.get_today_ticks(code)
        # try:
        if len(dtick.index) > 0:
            p_now = dtick['price'].values[0] * 100
            ep = dtick['amount'].sum() / dtick['volume'].sum()
            if not ave == None:
                if p_now > ave and ep > ave:
                    print ("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" % (code, ep, p_now, ave, get_now_time()))
                elif p_now > ave and ep < ave:
                    print ("gold:%s ep:%s UP:%s! A:%s %s !" % (code, ep, p_now, ave, get_now_time()))
                elif p_now < ave and ep > ave:
                    print ("down:%s ep:%s Dow:%s? A:%s %s ?" % (code, ep, p_now, ave, get_now_time()))
                else:
                    print ("DOWN:%s ep:%s now:%s??? A:%s %s ???" % (code, ep, p_now, ave, get_now_time()))
            else:
                if ep > ave:
                    print ("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" % (code, ep, p_now, ave, get_now_time()))
                else:
                    print ("down:%s ep:%s now:%s??? A:%s %s ?" % (code, ep, p_now, ave, get_now_time()))

        else:
            df = ts.get_realtime_quotes(code)
            print "name:%s op:%s  price:%s" % (df['name'].values[0], df['open'].values[0], df['price'].values[0])
    except (IOError, EOFError, KeyboardInterrupt) as e:
        print("Except:%s" % (e))
        # print "IOError"


def get_today_tick_ave(code, ave=None):
    try:
        dtick = ts.get_today_ticks(code)
        df = dtick
        if len(dtick.index) > 0:
            p_now = dtick['price'].values[0] * 100
            ep = dtick['amount'].sum() / dtick['volume'].sum()
            if not ave == None:
                if p_now > ave and ep > ave:
                    print ("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" % (code, ep, p_now, ave, get_now_time()))
                elif p_now > ave and ep < ave:
                    print ("gold:%s ep:%s UP:%s! A:%s %s !" % (code, ep, p_now, ave, get_now_time()))
                elif p_now < ave and ep > ave:
                    print ("down:%s ep:%s Dow:%s? A:%s %s ?" % (code, ep, p_now, ave, get_now_time()))
                else:
                    print ("DOWN:%s ep:%s now:%s??? A:%s %s ???" % (code, ep, p_now, ave, get_now_time()))
            else:
                if ep > ave:
                    print ("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" % (code, ep, p_now, ave, get_now_time()))
                else:
                    print ("down:%s ep:%s now:%s??? A:%s %s ?" % (code, ep, p_now, ave, get_now_time()))

        else:
            df = ts.get_realtime_quotes(code)
            print "name:%s op:%s  price:%s" % (df['name'].values[0], df['open'].values[0], df['price'].values[0])
        # print df
        return df
    except (IOError, EOFError, KeyboardInterrupt) as e:
        print("Except:%s" % (e))
        # print "IOError"


def f_print(len, datastr):
    data = ('{0:%s}' % (len)).format(datastr)
    return data


def get_hot_count(changepercent):
    allTop = pd.DataFrame()
    for market in ct.SINA_Market_KEY:
        df = rd.get_sina_Market_json(market, False)
        # count=len(df.index)
        # print df[:1]
        top = df[df['percent'] > changepercent]['code']
        topTen = df[df['percent'] > 9.9]['code']
        crashTen = df[df['percent'] < -9.8]['code']
        crash = df[df['percent'] < -changepercent]['code']
        # top=df[ df['changepercent'] <6]

        print (
            "%s topT: %s top>%s: %s " % (
                f_print(4, market), f_print(3, len(topTen)), changepercent, f_print(4, len(top)))),
        ff = ffu.get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW[market])
        if len(ff) > 0:
            zlr = float(ff['zlr'])
            zzb = float(ff['zzb'])
            # zt=str(ff['time'])
            print (u"crashT:%s crash<-%s:%s 流入: %0.1f亿 比: %0.1f%%" % (
                f_print(4, len(crashTen)), changepercent, f_print(4, len(crash)), zlr, zzb))
        else:
            print (u"crashT:%s crash<-%s:%s 流入: %0.1f亿 比: %0.1f%% %s" % (
                f_print(4, len(crashTen)), changepercent, f_print(4, len(crash))))

        allTop = allTop.append(df, ignore_index=True)

    df = allTop
    count = len(df.index)
    top = df[df['percent'] > changepercent]['code']
    topTen = df[df['percent'] > 9.9]['code']
    crashTen = df[df['percent'] < -9.8]['code']
    crash = df[df['percent'] < -changepercent]['code']
    print (
        u"\t\tA:%s topT:%s top>%s:%s" % (
            f_print(4, count), f_print(3, len(topTen)), changepercent, f_print(4, len(top)))),
    ff = ffu.get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_ALL)
    if len(ff) > 0:
        zlr = float(ff['zlr'])
        zzb = float(ff['zzb'])
        zt = str(ff['time'])
        print (u"crashT:%s crash<-%s:%s 流入: %0.1f亿 占比: %0.1f%% %s" % (
            f_print(3, len(crashTen)), changepercent, f_print(4, (len(crash))), zlr, zzb, zt))
    else:
        print (u"crashT:%s crash<-%s:%s" % (f_print(3, len(crashTen)), changepercent, f_print(4, len(crash))))
    return allTop


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)


# signal.signal(signal.SIGINT, signal_handler)
# print 'Press Ctrl+C'
# signal.pause()
def handle_ctrl_c(signal, frame):
    print "Got ctrl+c, going down!"
    sys.exit(0)


def get_hot_loop(timedelay, percent=3):
    if get_now_time():
        df = get_hot_count(percent)
        # _write_to_csv(df,'tick-data')
        # print ""
    time.sleep(timedelay)


import sys


def get_code_search_loop(num_input, code='', timed=60, dayl='10', ave=None):
    # if not status:
    #
    if get_work_time():
        if code == num_input:
            get_today_tick_ave(code, ave)
        else:
            ave = get_multiday_ave_compare(num_input, dayl)
    time.sleep(timed)
    return ave


if __name__ == '__main__':
    # get_multiday_ave_compare('601198')
    # print len(sys.argv)
    if len(sys.argv) == 2:
        status = True
        num_input = sys.argv[1]
        # print num_input
    elif (len(sys.argv) > 2):
        pass
    else:
        status = False
        num_input = ''

    code = ''
    ave = None
    days = '20'
    success = 0
    while 1:
        try:
            if not status:
                get_hot_loop(120, 3)
            if status:
                # status=True
                if not num_input:
                    num_input = raw_input("please input code:")
                    if num_input == 'ex' or num_input == 'qu' \
                            or num_input == 'q' or num_input == "e":
                        sys.exit()
                    elif not num_input or not len(num_input) == 6:  # str.isdigit()是用来判断字符串是否纯粹由数字组成
                        print ("Please input 6 code:or exit")
                        num_input = ''
                if num_input:
                    if ave == None:
                        ave = get_code_search_loop(num_input, code, dayl=days)
                    else:
                        ave = get_code_search_loop(num_input, code, dayl=days, ave=ave)
                    code = num_input

        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e

            st = raw_input("status:[go(g),clear(c),quit(q,e)]:")
            if len(st) == 0:
                status = False
            elif st == 'g' or st == 'go':
                status = True
                num_input = ''
                ave = None
                code = ''
            else:
                sys.exit(0)
                # time.sleep(0.5)
                # if success > 3:
                #     raw_input("Except")
                #     sys.exit(0)

        except (IOError, EOFError) as e:
            print "Error", e
            # traceback.print_exc()
            # raw_input("Except")
            # num_input=num_input
            # print "status:",status
            # handle_ctrl_c()
            # raise
            # except (Exception, KeyboardInterrupt):
            #     # print "key"
            #     print "a"
            #     status=not status
            #     num_input=''
            # finally:
            #     print "fina"
