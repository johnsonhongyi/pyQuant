# -*- coding: UTF-8 -*-
import datetime
import random
import sys
import time
import types

import pandas as pd
import tushare as ts
# print sys.path
import JSONData.fundflowUtil as ffu
import JohnsonUtil.johnson_cons as ct
import JohnsonUtil.commonTips as cct
from JSONData import realdatajson as rd
from JSONData import powerCompute as pct
from JSONData import get_macd_kdj_rsi as getab
from JSONData import tdx_data_Day as tdd
from JSONData import sina_data
import JohnsonUtil.emacount as ema
from JohnsonUtil import LoggerFactory
# log = LoggerFactory.getLogger("SingleSAU")
# log.setLevel(LoggerFactory.DEBUG)

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


# def get_today():
#     TODAY = datetime.date.today()
#     today = TODAY.strftime('%Y-%m-%d')
#     return today

global fibcount, except_count
fibcount = 0
except_count = 0


def time_sleep(timemin):
    # time1 = time.time()
    time.sleep(timemin)
    return True


def evalcmd(dir_mo):
    end = True
    import readline
    # import rlcompleter
    # readline.set_completer(cct.MyCompleter(dir_mo).complete)
    readline.parse_and_bind('tab:complete')
    while end:
        # cmd = (cct.cct_raw_input(" ".join(dir_mo)+": "))
        cmd = (cct.cct_raw_input(": "))
        # cmd = (cct.cct_raw_input(dir_mo.append(":")))
        # if cmd == 'e' or cmd == 'q' or len(cmd) == 0:
        if cmd == 'e' or cmd == 'q':
            break
        elif len(cmd) == 0:
            continue
        else:
            try:
                print eval(cmd)
                print ''
            except Exception, e:
                print e
                evalcmd(dir_mo)
                break


def get_all_toplist():
    # gold = {}
    # goldl = []
    df = ts.get_today_all()
    top = df[df['changepercent'] > 6]
    top = top[top['changepercent'] < 10]
    list = top.index
    print len(list)
    return list


def _write_to_csv(df, filename, indexCode='code'):
    TODAY = datetime.date.today()
    CURRENTDAY = TODAY.strftime('%Y-%m-%d')
    #     reload(sys)
    #     sys.setdefaultencoding( "gbk" )
    df = df.drop_duplicates(indexCode)
    df = df.set_index(indexCode)
    df.to_csv(CURRENTDAY + '-' + filename + '.csv',
              encoding='gbk', index=False)  # 选择保存
    print("write csv")

    # df.to_csv(filename, encoding='gbk', index=False)


def get_multiday_ave_compare(code, dayl='10'):
    dtick = ts.get_today_ticks(code)
    d_hist = ema.getdata_ema_trend(code, dayl, 'd')
    # print d_hist
    day_t = ema.get_today()
    if d_hist is not None:
        if day_t in d_hist.index:
            dl = d_hist.drop(day_t).index
        else:
            dl = d_hist.index
    else:
        return 0
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
            print("D: %s P: %s" % (da[-5:], ep))

    ave = ema.less_average(ep_list)
    if len(dtick.index) > 0:
        ep = dtick['amount'].sum() / dtick['volume'].sum()
        p_now = dtick['price'].values[0] * 100
        if p_now > ave and ep > ave:
            print("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" %
                  (code, ep, p_now, ave, cct.get_now_time()))
        elif p_now > ave and ep < ave:
            print("gold:%s ep:%s UP:%s! A:%s %s !" %
                  (code, ep, p_now, ave, cct.get_now_time()))
        elif p_now < ave and ep > ave:
            print("down:%s ep:%s Dow:%s? A:%s %s ?" %
                  (code, ep, p_now, ave, cct.get_now_time()))
        else:
            print("DOWN:%s ep:%s now:%s??? A:%s %s ???" %
                  (code, ep, p_now, ave, cct.get_now_time()))
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
            print("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" %
                  (code, ep, p_now, ave, get_now_time()))
            # elif p_now > ave and ep < ave:
            #     print ("gold:%s ep:%s UP:%s! A:%s %s !" % (code, ep, p_now, ave, get_now_time()))
            # elif p_now < ave and ep > ave:
            #     print ("down:%s ep:%s Dow:%s? A:%s %s ?" % (code, ep, p_now, ave, get_now_time()))
            return True
        else:
            if p_now < ave and ep < ave:
                print("DOWN:%s ep:%s now:%s??? A:%s %s ???" %
                      (code, ep, p_now, ave, get_now_time()))
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
                    print("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" %
                          (code, ep, p_now, ave, get_now_time()))
                elif p_now > ave and ep < ave:
                    print("gold:%s ep:%s UP:%s! A:%s %s !" %
                          (code, ep, p_now, ave, get_now_time()))
                elif p_now < ave and ep > ave:
                    print("down:%s ep:%s Dow:%s? A:%s %s ?" %
                          (code, ep, p_now, ave, get_now_time()))
                else:
                    print("DOWN:%s ep:%s now:%s??? A:%s %s ???" %
                          (code, ep, p_now, ave, get_now_time()))
            else:
                if ep > ave:
                    print("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" %
                          (code, ep, p_now, ave, get_now_time()))
                else:
                    print("down:%s ep:%s now:%s??? A:%s %s ?" %
                          (code, ep, p_now, ave, get_now_time()))

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
                    print("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" %
                          (code, ep, p_now, ave, get_now_time()))
                elif p_now > ave and ep < ave:
                    print("gold:%s ep:%s UP:%s! A:%s %s !" %
                          (code, ep, p_now, ave, get_now_time()))
                elif p_now < ave and ep > ave:
                    print("down:%s ep:%s Dow:%s? A:%s %s ?" %
                          (code, ep, p_now, ave, get_now_time()))
                else:
                    print("DOWN:%s ep:%s now:%s??? A:%s %s ???" %
                          (code, ep, p_now, ave, get_now_time()))
            else:
                if ep > ave:
                    print("GOLD:%s ep:%s UP:%s!!! A:%s %s !!!" %
                          (code, ep, p_now, ave, get_now_time()))
                else:
                    print("down:%s ep:%s now:%s??? A:%s %s ?" %
                          (code, ep, p_now, ave, get_now_time()))

        else:
            df = ts.get_realtime_quotes(code)
            print "name:%s op:%s  price:%s" % (df['name'].values[0], df['open'].values[0], df['price'].values[0])
        # print df
        return df
    except (IOError, EOFError, KeyboardInterrupt) as e:
        print("Except:%s" % (e))
        # print "IOError"


def f_print(lens, datastr,color=None):
    # if lens < len(str(datastr)):
        # log.warn("str:%s f_print:%s %s"%(datastr,lens,len(str(datastr))))
    lenf = '{0:>%s}' % (lens)
    data = lenf.format(datastr)
    # print("\033[1;31;40m您输入的帐号或密码错误！\033[0m")  
    # \033[5;31;42m
    # https://www.cnblogs.com/hellojesson/p/5961570.html
    """数值表示的参数含义：
    # 显示方式: 0（默认值）、1（高亮）、22（非粗体）、4（下划线）、24（非下划线）、 5（闪烁）、25（非闪烁）、7（反显）、27（非反显）
    # 前景色: 30（黑色）、31（红色）、32（绿色）、 33（黄色）、34（蓝色）、35（洋 红）、36（青色）、37（白色）
    # 背景色: 40（黑色）、41（红色）、42（绿色）、 43（黄色）、44（蓝色）、45（洋 红）、46（青色）、47（白色）

    # 常见开头格式：
    # \033[0m            默认字体正常显示，不高亮
    # \033[32;0m       红色字体正常显示
    # \033[1;32;40m  显示方式: 高亮    字体前景色：绿色  背景色：黑色
    # \033[0;31;46m  显示方式: 正常    字体前景色：红色  背景色：青色
    """
    # data = "\033[1;31;40m%s\033[0m"%(data)
    # color_dic = {31:'47',32:'40'}
    color_dic = {31:'47',32:'47',35:'47'}
    if color is not None:
        if color <> 31:
            # if color == 32:
                # color = 35
            flash = 5
        else:
            flash = 1
        data = "\033[%s;%s;%sm%s\033[0m"%(flash,color,color_dic[color],data)
    return data


def fibonacciCount(code, dl=60, start=None, days=0):
    fibl = []
    if not isinstance(code, list):
        codes = [code]
    else:
        codes = code
    for code in codes:
        df = tdd.get_tdx_append_now_df_api(code, dl=dl)
        for ptype in ['low', 'high']:
            if ptype == 'low':
                op, ra, st, daysData = pct.get_linear_model_status(
                    code, df=df, filter='y', dl=dl, ptype=ptype, days=days)
                dd, boll = getab.Get_BBANDS(df, days=days)
            else:
                # df = tdd.get_tdx_append_now_df_api(code,dl=dl)
                op, ra, st, daysData = pct.get_linear_model_status(
                    code, df=df, filter='y', dl=dl, ptype=ptype, days=days)
                dd, boll = getab.Get_BBANDS(df, dtype='d')
            fib = cct.getFibonacci(300, daysData[0])
            # log.debug('st:%s days:%s fib:%s'%(st,days,fib))
            # print "%s op:%s ra:%s days:%s fib:%s %s" % (code, op,
            # ra,days,fib, st)
            if not daysData[1].ma5d[0]:
                daysData[1].ma5d[0] = 0
            fibl.append(
                [code, op, ra, [daysData[0], int(daysData[1].ma5d[0])], fib, st ])
    return fibl

# global cumin_index 
# cumin_index = {}
top_Ten_Dropcxg=[]
def get_hot_countNew(changepercent, rzrq, fibl=None, fibc=10):
    global fibcount
    INDEX_LIST_TDX = {'999999':'sh', '399001':'sz', '399006':'cyb'}
    # {v: k for k, v in m.items()}
    # >>> zip(m.values(), m.keys())
    # mi = dict(zip(m.values(), m.keys()))
    if fibcount == 0 or fibcount >= fibc:
        if fibcount >= fibc:
            fibcount = 1
        else:
            fibcount += 1
        if fibl is not None:
            int = 0
            for f in fibl:
                code, op, ra, daysData, fib, st = f[
                    0], f[1], f[2], f[3], f[4], f[5] 
                # cumin_index[INDEX_LIST_TDX[code]]=cumin
                int += 1
                if int % 2 != 0:
                    print "%s op:%s ra:%s d:%s fib:%s m5:%s  %s" % (code, f_print(3, op), f_print(5, ra), f_print(2, daysData[0]), f_print(3, fib), f_print(4, daysData[1]), st),
                else:
                    print "%s op:%s ra:%s d:%s fib:%s m5:%s " % (st, f_print(3, op), f_print(5, ra), f_print(2, daysData[0]), f_print(3, fib), f_print(4, daysData[1]))

    else:
        fibcount += 1
    allTop = pd.DataFrame()
    indexKeys = ['sh', 'sz', 'cyb']
    ffindex = ffu.get_dfcfw_fund_flow('all')

    ffall = {}
    ffall['zlr'] = 0
    ffall['zzb'] = 0

    for market in indexKeys:
        # market = ct.SINA_Market_KEY()
        #        df = rd.get_sina_Market_json(market, False)
        df = sina_data.Sina().market(market)
        # count=len(df.index)
        # log.info("market:%s" % df[:1])
        df = df.dropna()
        df = df[df.close > 0]
        if 'percent' not in df.columns:
            df['percent'] = map(lambda x, y: round(
                (x - y) / y * 100, 1), df.close.values, df.llastp.values)
        
        if 'percent' in df.columns.values:
            # and len(df[:20][df[:20]['percent']>0])>3:
            # if 'code' in df.columns:
            #     top = df[df['percent'] > changepercent]
            #     topTen = df[df['percent'] > 9.9]
            #     crashTen = df[df['percent'] < -9.8]
            #     crash = df[df['percent'] < -changepercent]
            # else:
            top = df[df['percent'] > changepercent]
            topTen = df[df['percent'] > 9.9]
            dropcode = [ x for x in topTen.index.tolist() if x not in top_Ten_Dropcxg]
            if len(dropcode) >0:
                topT_l = tdd.get_tdx_exp_all_LastDF_DL(dropcode, dt=ct.duration_date_l,newdays=10,showRunTime=False)
                if isinstance(topT_l, pd.DataFrame):
                    top_Ten_Dropcxg.extend(topT_l.index.tolist())  
            crashTen = df[df['percent'] < -9.8]
            crash = df[df['percent'] < -changepercent]
        else:
            log.info("market No Percent:%s" % df[:1])
            top = '0'
            topTen = '0'
            crashTen = '0'
            crash = '0'
        # top=df[ df['changepercent'] <6]
        # print("\033[1;31;40m您输入的帐号或密码错误！\033[0m")  
        print(
            "%s topT: %s top>%s: %s" % (
                f_print(4, market), f_print(3, len(topTen)), changepercent, f_print(4, len(top)))),
        # url = ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW[market]
        # log.debug("ffurl:%s" % url)
        print(u"crashT:%s crash<-%s:%s" %
              (f_print(4, len(crashTen)), changepercent, f_print(4, len(crash)))),
        # print(u"-5:%s" %
        #       (f_print(4, len(crash[crash < -5])))),
        ff = ffindex[market]
        if len(ff) > 0:
            zlr = float(ff['zlr'])
            zzb = float(ff['zzb'])
            ffall['zlr'] = ffall['zlr'] + zlr
            ffall['zzb'] = ffall['zzb'] + zzb
            # zt=str(ff['time'])
            # modfprint=lambda x:f_print(4,x) if x>0 else "-%s"%(f_print(4,str(x).replace('-','')))
            # print modfprint(zlr)
            # print (u"流入: %s亿 比: %s%%" % (modfprint(zlr), modfprint(zzb))),
            print(u"流入: %s亿 比: %s%% " % (f_print(6, zlr,32), f_print(4, zzb,32))),
            if ff['close'] == 0:
                _percent = 0
            else:
                _percent = round((ff['close']-ff['lastp'])*100/ff['close'],2)
            # print (u" %s"%(f_print(2,cumin_index[market],31))),
            print(u"%s %s%% %s%s" % (f_print(7, ff['close']),f_print(4,_percent,31), f_print(1, '!' if ff['open'] > ff[
                'lastp'] else '?'), f_print(2, '!!' if ff['close'] > ff['lastp'] else '??',32)))
        allTop = allTop.append(df.reset_index(), ignore_index=True)
        allTop = allTop.drop_duplicates()
    df = allTop
    df  = tdd.get_single_df_lastp_to_df(
                        df.set_index('code'),resample='d')    
    count = len(df.index)
    top = df[df['percent'] > changepercent]
    topTen = df[df['percent'] >= 9.9]
    if 'max5' in df.columns: 
        top_Max = (df[(df.close >= df.hmax) & (df.close >= df.max5)])

        # top_low = len(df[df.low < df.min5])
        top_min = (df[(df.close <= df.lmin) & (df.close <= df.min5)])
        cct.GlobalValues().setkey('top_max',top_Max)
        cct.GlobalValues().setkey('top_min',top_min)

    else:
        top_Max = []
        top_low = 0
        top_min = []

    topTen = str(len(topTen)) +'('+str(len(top_Ten_Dropcxg))+')' +'(H:'+str(len(top_Max))+')'
    # print "top_Ten_Dropcxg:%s",top_Ten_Dropcxg
    crashTen = df[df['percent'] < -9.8]
    crashTen = str(len(crashTen)) +'(L:'+str(len(top_min))+')'

    crash = df[df['percent'] < -changepercent]
    print(
        u"A:%s topT:%s top>%s:%s" % (
            f_print(4, count), f_print(3, (topTen),31), changepercent, f_print(4, len(top),31))),
    print(u"crashT:%s crash<-%s:%s" %
          (f_print(3, (crashTen),32), changepercent, f_print(4, len(crash),31))),
    print(u"-5:%s" %
          (f_print(4, len(crash[crash.percent < -5]),32))),
    # ff = ffu.get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_ALL)
    ffall['time'] = ff['time']
    ff = ffall
    zzb = 0
    if len(ff) > 0:
        zlr = round(float(ff['zlr']), 1)
        zzb = round(float(ff['zzb']) / 3, 1)
        zt = str(ff['time'])
        print(u"流入: %s亿 占比: %s%% %s" %
              (f_print(4, zlr,31), f_print(4, zzb,31), f_print(4, zt)))

    ff = ffu.get_dfcfw_fund_SHSZ()
    hgt = ffu.get_dfcfw_fund_HGT()
    szt = ffu.get_dfcfw_fund_HGT(url=ct.DFCFW_FUND_FLOW_SZT)
    log.debug("shzs:%s hgt:%s" % (ff,hgt))
    # if len(ff) > 0:
    #     print ("\tSH: %s u:%s vo: %s sz: %s u:%s vo: %s" % (
    #         f_print(4, ff['scent']), f_print(4, ff['sup']), f_print(5, ff['svol']), f_print(4, ff['zcent']),
    #         f_print(4, ff['zup']),
    #         f_print(5, ff['zvol']))),
    bigcount = rd.getconfigBigCount(count=None, write=True)

    if len(ff) > 0:
        print(u"\tSh: %s Vr:%s Sz: %s Vr:%s " % (
            f_print(4, ff['scent']), f_print(5, ff['svol'],31), f_print(4, ff['zcent']), f_print(5, ff['zvol'],31))),
        print(u'B:%s-%s V:%s' % (bigcount[0], bigcount[2], f_print(4,bigcount[1])))
    else:
        print(u"\tSh: \t%s Vr:  \t%s Sz: \t%s Vr: \t%s ") % (0, 0, 0, 0),
        print(u'B:%s-%s V:%s' % (bigcount[0], bigcount[2], f_print(4,bigcount[1])))

    if len(hgt) > 0:
        print("\tHgt: %s Ggt: %s Sgt: %s Gst: %s SSVol:%s" %
              (hgt['hgt'], hgt['ggt'], szt['hgt'], szt['ggt'],f_print(5, ff['allvol'],31)))
    else:
        print("\tHgt: \t%s Ggt: \t%s Sgt: %s Gst: %s" % (0, 0, 0, 0))
        
    if len(rzrq) > 0:
        if 'shrz' not in rzrq.keys() and 'szrz' not in rzrq.keys():
            rzrq['shrz'] = 0
            rzrq['szrz'] = 0
        shpcent = round((rzrq['shrz'] / rzrq['sh'] * 100),
                        1) if rzrq['sh'] > 0 else '?'
        szpcent = round((rzrq['szrz'] / rzrq['sz'] * 100),
                        1) if rzrq['sz'] > 0 else '?'
        print(u"\tSh: %s rz:%s :%s%% sz: %s rz:%s :%s%% All: %s diff: %s亿" % (
            f_print(5, rzrq['sh']), f_print(4, rzrq['shrz']), shpcent, f_print(
                5, rzrq['sz']), f_print(4, rzrq['szrz']),
            szpcent, f_print(4, rzrq['all'],31), f_print(5, rzrq['dff'],31)))
    # print "bigcount:",bigcount

    cct.set_console(width, height,
                    title=['B:%s-%s V:%s' % (bigcount[0], bigcount[2], bigcount[1]), 'ZL: %s' % (zlr if len(ff) > 0 else 0),
                           'To:%s' % len(topTen), 'D:%s' % len(
                        crash), 'Sh: %s ' % ff['scent'] if len(ff) > 0 else '?', 'Vr:%s%% ' % ff['svol'] if len(ff) > 0 else '?',
                        'MR: %s' % zzb, 'ZL: %s' % (zlr if len(ff) > 0 else '?')],closeTerminal=False)
    log.debug("set_console:bigcount[0]%s  bigcount[2]:%s" % (bigcount[0], bigcount[2]))


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
    if cct.get_work_time():
        if code == num_input:
            get_today_tick_ave(code, ave)
        else:
            ave = get_multiday_ave_compare(num_input, dayl)
    time.sleep(timed)
    return ave


if __name__ == '__main__':
    # get_multiday_ave_compare('601198')
    from docopt import docopt
    log = LoggerFactory.log
    args = docopt(cct.sina_doc, version='sina_cxdn')
    # print args,args['-d']
    if args['-d'] == 'debug':
        log_level = LoggerFactory.DEBUG
    elif args['-d'] == 'info':
        log_level = LoggerFactory.INFO
    else:
        log_level = LoggerFactory.ERROR
    # log_level = LoggerFactory.DEBUG if args['-d']  else LoggerFactory.ERROR
    log.setLevel(log_level)

#    log.setLevel(LoggerFactory.DEBUG)
    # print len(sys.argv)
    if cct.isMac():
        width, height = 108, 15
        cct.set_console(width, height)
    else:
        width, height = 108, 15
        cct.set_console(width, height)

    if len(sys.argv) == 2:
        status = True
        num_input = sys.argv[1]
        # print num_input
    elif (len(sys.argv) > 2):
        pass
    else:
        status = False
        num_input = ''

    status = False
    code = ''
    ave = None
    days = '10'
    success = 0
    rzrq = ffu.get_dfcfw_rzrq_SHSZ()
    dl = 34
    fibc = 3
    fibl = fibonacciCount(['999999', '399001', '399006'], dl=dl)
    percentDuration = 2
    cct.get_terminal_Position(position=sys.argv[0])
    from JSONData import stockFilter as stf
    blkname = '068.blk'
    block_path = tdd.get_tdx_dir_blocknew() + blkname
    while 1:
        try:
            if not status:
                if len(fibl) == 0 or fibcount >= fibc:
                    # print "change FibDiff"
                    fibcount = 0
                    fibl = fibonacciCount(
                        ['999999', '399001', '399006'], dl=dl)
                if len(rzrq) == 0 or rzrq['sh'] == 0 or rzrq['sz'] == 0 or rzrq['all'] == 0:
                    # if rzrq['shrz'] == 0 or rzrq['szrz'] == 0 or rzrq['dff'] == 0 or rzrq['all'] == 0:
                    #     log.warn("rzrq 0")
                    rzrq = ffu.get_dfcfw_rzrq_SHSZ()
                log.info('start get_hot_count')
                get_hot_countNew(percentDuration, rzrq, fibl, fibc)
                fibcount += 1
            if status:
                # status=True
                if not num_input:
                    num_input = raw_input("please input code:")
                    if num_input == 'ex' or num_input == 'qu' \
                            or num_input == 'q' or num_input == "e":
                        sys.exit()
                    # str.isdigit()是用来判断字符串是否纯粹由数字组成
                    elif not num_input or not len(num_input) == 6:
                        print("Please input 6 code:or exit")
                        num_input = ''
                if num_input:
                    if ave == None:
                        ave = get_code_search_loop(num_input, code, dayl=days)
                    else:
                        ave = get_code_search_loop(
                            num_input, code, dayl=days, ave=ave)
                    code = num_input
                    
            # int_time = cct.get_now_time_int()
            # if cct.get_work_time():
            #     if 930 < int_time < 1000:
            #         cct.sleep(45)
            #     else:
            #         cct.sleep(ct.duration_sleep_time)
                    
            int_time = cct.get_now_time_int()
            if cct.get_work_time():
                log.debug('into get_work_time:%s'%(int_time))
                if 915 < int_time < 926:
                    while 1:
                        cct.sleeprandom(15)
                        break
                elif int_time < 930:
                    while 1:
                        cct.sleep(60)
                        if cct.get_now_time_int() < 931:
                            cct.sleep(60)
                            print ".",
                        else:
                            # cct.sleep(random.randint(0, 30))
                            # print "."
                            fibcount = 0
                            break
                else:
                    cct.sleep(60)
            elif cct.get_work_duration():
                log.debug('into work_duration:%s'%(int_time))
                while 1:
                    if cct.get_work_duration():
                        print ".",
                        cct.sleep(60)
                    else:
                        print "#"
                        cct.sleep(random.randint(0, 30))
                        top_all = pd.DataFrame()
                        fibcount = 0
                        break

            else:
                log.debug('into clean_duration:%s'%(int_time))
                if (cct.get_now_time_int() > 1502 and cct.get_now_time_int() < 1800):
                    while 1:
                        if cct.get_now_time_int() > 1502 and cct.get_now_time_int() < 1510:
                            print ".",
                            cct.sleep(60)
                        elif cct.get_now_time_int() < 1800:
                            print ".",
                            print "write dm to file"
                            if cct.get_work_day_status():
                                tdd.Write_market_all_day_mp('all')
                                top_temp = cct.GlobalValues().getkey('top_max')
                                codew = stf.WriteCountFilter(top_temp, writecount='all')
                                cct.write_to_blocknew(block_path,codew,append=False,doubleFile=False)
                            break
                        else:
                            print "."


	                
                raise KeyboardInterrupt("Stop Time")
                # st = cct.cct_raw_input("status:[go(g),clear(c),quit(q,e)]:")
                # if len(st) == 0:
                #     status = False
                # elif st.lower() == 'g' or st.lower() == 'go':
                #     status = True
                #     num_input = ''
                #     ave = None
                #     code = ''
                # elif len(st) == 6:
                #     status = True
                #     num_input = st
                #     ave = None
                #     code = ''
                # else:
                #     sys.exit(0)
        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e

            st = cct.cct_raw_input("status:[go(g),clear(c),quit(q,e)]:")
            if len(st) == 0:
                status = False
            elif st.lower() == 'g' or st.lower() == 'go':
                status = True
                num_input = ''
                ave = None
                code = ''
            elif st.lower() == 'c' or st.lower() == 'C':
                rzrq = {}
            elif st.startswith('w') or st.startswith('a'):
                args = cct.writeArgmain().parse_args(st.split())
                top_temp = cct.GlobalValues().getkey('top_max')
                codew = stf.WriteCountFilter(
                    top_temp, writecount=args.dl)
                if args.code == 'a':
                    cct.write_to_blocknew(block_path,codew,doubleFile=False)
                    # sl.write_to_blocknew(all_diffpath, codew)
                else:
                    cct.write_to_blocknew(block_path,codew, False,doubleFile=False)
                    # sl.write_to_blocknew(all_diffpath, codew, False)
                print ("wri ok:%s" % block_path)


            elif len(st) == 6:
                status = True
                num_input = st
                ave = None
                code = ''
            elif st.lower() == 'r':
                dir_mo = eval(cct.eval_rule)
                evalcmd(dir_mo)
            elif st.startswith('q') or st.startswith('e'):
                print "exit:%s" % (st)
                sys.exit(0)
            else:
                print "input error:%s" % (st)
                # cct.sleep(0.5)
                # if success > 3:
                #     raw_input("Except")
                #     sys.exit(0)

        except (IOError, EOFError) as e:
            print "SingleError", e
            # traceback.print_exc()
#            sleeptime=random.randint(5, 15)
            cct.sleeprandom(30)
#            print "Error2sleep:%s"%(sleeptime)
        except Exception as e:
            log.error("Error Exception:%s"%(e))
            import traceback
            traceback.print_exc()
            # global except_count
            except_count += 1
            if except_count < 4:
                cct.sleeprandom(ct.duration_sleep_time / 2)
            else:
                print "except_count >3"
                cct.sleeprandom(ct.duration_sleep_time * 2)
                # sys.exit(0)
        # finally:
        #     cct.sleeprandom(ct.duration_sleep_time/2)
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
