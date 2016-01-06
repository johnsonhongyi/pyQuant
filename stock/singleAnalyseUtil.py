# -*- coding: UTF-8 -*-
import datetime
import sys
import time
import types

import pandas as pd
import tushare as ts
# print sys.path

import JSONData.fundflowUtil as ffu
import JohhnsonUtil.johnson_cons as ct
import JohhnsonUtil.commonTips as cct
from JSONData import realdatajson as rd
import JohhnsonUtil.emacount as ema
from JohhnsonUtil import LoggerFactory

log = LoggerFactory.getLogger("SingleAU")

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


# def get_today():
#     TODAY = datetime.date.today()
#     today = TODAY.strftime('%Y-%m-%d')
#     return today


def time_sleep(timemin):
    time1 = time.time()
    time.sleep(timemin)
    return True


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


def f_print(lens, datastr):
    data = ('{0:%s}' % (lens)).format(str(datastr))
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
        url = ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW[market]
        log.debug("ffurl:%s" % url)
        ff = ffu.get_dfcfw_fund_flow(url)
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


def get_hot_countNew(changepercent):
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
        url = ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW[market]
        log.debug("ffurl:%s" % url)
        print (u"crashT:%s crash<-%s:%s" % (f_print(4, len(crashTen)), changepercent, f_print(4, len(crash)))),
        ff = ffu.get_dfcfw_fund_flow(url)
        if len(ff) > 0:
            zlr = float(ff['zlr'])
            zzb = float(ff['zzb'])
            # zt=str(ff['time'])
            print (u"流入: %s亿 比: %s%%" % (f_print(4, zlr), f_print(4, zzb)))

        allTop = allTop.append(df, ignore_index=True)

    df = allTop
    count = len(df.index)
    top = df[df['percent'] > changepercent]['code']
    topTen = df[df['percent'] > 9.9]['code']
    crashTen = df[df['percent'] < -9.8]['code']
    crash = df[df['percent'] < -changepercent]['code']
    print (
        u" \tA:%s topT:%s top>%s:%s" % (
            f_print(4, count), f_print(3, len(topTen)), changepercent, f_print(4, len(top)))),
    print (u"crashT:%s crash<-%s:%s" % (f_print(3, len(crashTen)), changepercent, f_print(4, len(crash)))),
    ff = ffu.get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_ALL)
    if len(ff) > 0:
        zlr = float(ff['zlr'])
        zzb = float(ff['zzb'])
        zt = str(ff['time'])
        print (u"流入: %s亿 占比: %s%% %s" % (f_print(4, zlr), f_print(4, zzb), f_print(4, zt)))
    ff = ffu.get_dfcfw_fund_SHSZ(ct.DFCFW_ZS_SHSZ)
    hgt = ffu.get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
    log.debug("shzs:%s" % ff)
    log.debug("hgt:%s" % hgt)
    if len(ff) > 0:
        print ("\tSH: %s u:%s vo: %s sz: %s u:%s vo: %s" % (
            f_print(4, ff['scent']), f_print(4, ff['sup']), f_print(5, ff['svol']), f_print(4, ff['zcent']),
            f_print(4, ff['zup']),
            f_print(5, ff['zvol']))),
    if len(hgt) > 0:
        print ("hgt: %s ggt: %s" % (f_print(5, hgt['hgt']), f_print(5, hgt['ggt'])))

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
                get_hot_countNew(3)
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

            int_time = cct.get_now_time_int()
            if cct.get_work_time():
                if int_time < 1000:
                    time.sleep(60)
                else:
                    time.sleep(120)
            else:
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
