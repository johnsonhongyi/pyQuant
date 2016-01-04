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
from JSONData import realdatajson as rd
import JohhnsonUtil.emacount as ema


try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


def get_today():
    TODAY = datetime.date.today()
    today = TODAY.strftime('%Y-%m-%d')
    return today


def time_sleep(timemin):
    time1 = time.time()
    time.sleep(timemin)
    return True


def get_now_time_int():
    now_t = datetime.datetime.now().strftime("%H%M")
    return int(now_t)


def get_now_time():
    # now = time.time()
    now = time.localtime()
    # d_time=time.strftime("%Y-%m-%d %H:%M:%S",now)
    d_time = time.strftime("%H:%M", now)
    return d_time


def get_work_time():
    now_t = str(get_now_time()).replace(':', '')
    # now_t = int(now_t)
    if (now_t > '1131' and now_t < '1300') or (now_t < '0920' or now_t > '1502'):
        # return False
        return True
    else:
        return True


def get_work_time_now():
    now_t = str(get_now_time()).replace(':', '')
    # now_t = int(now_t)
    if (now_t > '1131' and now_t < '1300') or (now_t < '0915' or now_t > '1502'):
        # return False
        return False
    else:
        return True


def get_work_time_ratio():
    now = time.localtime()
    ymd = time.strftime("%Y:%m:%d:", now)
    hm1 = '09:30'
    hm2 = '13:00'
    all_work_time = 14400
    d1 = datetime.datetime.now()
    now_t = int(datetime.datetime.now().strftime("%H%M"))
    # d2 = datetime.datetime.strptime('201510111011','%Y%M%d%H%M')
    if now_t < 1130:
        d2 = datetime.datetime.strptime(ymd + hm1, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        ratio_t = round(ds / all_work_time, 3)

    elif now_t > 1130 and now_t < 1300:
        ratio_t = 0.5
    elif now_t >1501:
        ratio_t = 1.0
    else:
        d2 = datetime.datetime.strptime(ymd + hm2, '%Y:%m:%d:%H:%M')
        ds = float((d1 - d2).seconds)
        ratio_t = round((ds+7200) / all_work_time, 3)
    return ratio_t



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
    data = ('{0:%s}' % (lens)).format(datastr)
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
