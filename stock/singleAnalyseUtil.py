# -*- coding: UTF-8 -*-
import tushare as ts
import emacount as ema
import time
import types

def time_sleep(timemin):
    time1 = time.time()
    time.sleep(timemin)
    return True

def get_all_toplist():
    # gold = {}
    # goldl = []
    df = ts.get_today_all()
    top = df[df['changepercent'] >6 ]
    top = top[top['changepercent'] <10]
    # logging.info("top:", len(top['code']))
    list =top['code']
    print len(list)
    return list

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
        if not type(td)==types.NoneType:
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
        if not type(td)==types.NoneType:
            ep = td['amount'].sum() / td['volume'].sum()
            ep_list.append(ep)
            # print ("D: %s P: %s" % (da[-5:], ep))
    ave = ema.less_average(ep_list)
    if len(dtick.index) > 0:
        ep = dtick['amount'].sum() / dtick['volume'].sum()
        p_now = dtick['price'].values[0] * 100
        if p_now > ave and ep > ave:
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

def get_today_tick_ave(code, ave=None):
    try:
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
            df=ts.get_realtime_quotes(code)
            print "name:%s op:%s  price:%s"%(df['name'].values[0],df['open'].values[0],df['price'].values[0])
    except (IOError, EOFError, KeyboardInterrupt) as e:
        print("Except:%s"%(e))
        # print "IOError"


def get_now_time():
    now = time.time()
    now = time.localtime(now)
    # d_time=time.strftime("%Y-%m-%d %H:%M:%S",now)
    d_time = time.strftime("%H:%M", now)
    return d_time


def get_work_time():
    now_t = str(get_now_time()).replace(':', '')
    # now_t = int(now_t)
    if (now_t > '1131' and now_t < '1301') or (now_t < '0925' or now_t > '1502'):
        return False
    else:
        return True


def get_hot_count(changepercent):
    df = ts.get_today_all()
    top = df[df['changepercent'] > changepercent]['code']
    topTen = df[df['changepercent'] > 9.9]['code']
    crashTen = df[df['changepercent'] < -9.8]['code']
    crash = df[df['changepercent'] < -changepercent]['code']

    # top=df[ df['changepercent'] <6]
    print ("topT: %s top>%s: %s" % (len(topTen), changepercent, len(top))),
    print ("crashT: %s crash<-%s: %s" % (len(crashTen), changepercent, len(crash)))
    return top


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)


# signal.signal(signal.SIGINT, signal_handler)
# print 'Press Ctrl+C'
# signal.pause()
def handle_ctrl_c(signal, frame):
    print "Got ctrl+c, going down!"
    sys.exit(0)


def get_hot_loop(timedelay):
    if get_now_time():
        get_hot_count(3)
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
    while 1:
        try:
            if not status:
                get_hot_loop(180)
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
                        ave=get_code_search_loop(num_input, code, dayl=days, ave=ave)
                    code = num_input

        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:",e
            status = not status
            num_input = ''
            ave = None
            code=''
        except (IOError, EOFError) as e:
            print "Except",e
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
