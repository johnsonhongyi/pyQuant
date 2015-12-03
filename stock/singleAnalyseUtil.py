# -*- coding: UTF-8 -*-
import tushare as ts
import emacount as ema
import time


def time_sleep(timemin):
    time1 = time.time()
    time.sleep(timemin)
    return True


def get_single_ave_compare(code, dayl='10'):
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
        if len(td) > 0:
            ep = td['amount'].sum() / td['volume'].sum()
            ep_list.append(ep)
            print ("D: %s P: %s" % (da[-5:], ep))
    total_ave = ema.less_average(ep_list)
    if len(dtick.index) > 0:
        ep = dtick['amount'].sum() / dtick['volume'].sum()
        if ep >= total_ave:
            # gold[code]=d_hist
            # goldl.append(code)
            print ("Gold: %s ep:%s ave:%s %s" % (code, ep, total_ave, get_now_time()))
        else:
            print ("Fail: %s ep:%s ave:%s %s" % (code, ep, total_ave, get_now_time()))
    return total_ave


def get_single_tick_ave(code, ave=None):
    dtick = ts.get_today_ticks(code)
    if len(dtick.index) > 0:
        ep = dtick['amount'].sum() / dtick['volume'].sum()
        print ("Code: %s ep:%s :%s %s" % (code, ep, ave, get_now_time()))
    else:
        print "tick null"


def get_now_time():
    now = time.time()
    now = time.localtime(now)
    # d_time=time.strftime("%Y-%m-%d %H:%M:%S",now)
    d_time = time.strftime("%H:%M", now)
    return d_time


def get_work_time():
    now_t = get_now_time().replace(':', '')
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
    get_hot_count(3)
    time.sleep(timedelay)


import sys


def get_code_search_loop(num_input, code, timed=60, dayl='10', ave=None):
    # if not status:
    #
    if get_work_time():
        if code == num_input:
            get_single_tick_ave(code, ave)
        else:
            ave = get_single_ave_compare(num_input, dayl)
    time.sleep(timed)
    return ave


if __name__ == '__main__':
    # get_single_ave_compare('601198')
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
    days = '10'
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
                        get_code_search_loop(num_input, code, dayl=days, ave=ave)
                    code = num_input

        except (IOError, EOFError, KeyboardInterrupt):
            # print "key"
            print ""
            status = not status
            num_input = ''
            ave = None
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
