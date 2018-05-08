# -*- coding:utf-8 -*-
# !/usr/bin/env python

import gc
import random
import re
import sys
import time
import pandas as pd
import dfgui
import JohhnsonUtil.johnson_cons as ct
import singleAnalyseUtil as sl
from JSONData import powerCompute as pct
from JSONData import stockFilter as stf
from JSONData import realdatajson as rl
from JSONData import tdx_data_Day as tdd
from JSONData import LineHistogram as lhg
from JohhnsonUtil import LoggerFactory as LoggerFactory
from JohhnsonUtil import commonTips as cct

# from logbook import Logger,StreamHandler,SyslogHandler
# from logbook import StderrHandler


# def parseArgmain():
    # import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument('dt', type=str, nargs='?', help='20150612')
    # return parser



log = LoggerFactory.getLogger('sina_Market-DurationSZ')
# log.setLevel(LoggerFactory.DEBUG)
# handler=StderrHandler(format_string='{record.channel}: {record.message) [{record.extra[cwd]}]')
# log.level = log.debug
# error_handler = SyslogHandler('Sina-M-Log', level='ERROR')

width, height = 154, 21
def set_duration_console(du_date):
    if cct.isMac():
        cct.set_console(width, height)
    else:
        cct.set_console(width, height, title=str(du_date))
status = False
vol = ct.json_countVol
type = ct.json_countType
success = 0
top_all = pd.DataFrame()
time_s = time.time()
delay_time = 720000
# delay_time = cct.get_delay_time()
First = True
blkname = '062.blk'
block_path = tdd.get_tdx_dir_blocknew() + blkname
status_change = False
lastpTDX_DF = pd.DataFrame()
# dl=30
ptype='low'
# op, ra, duration_date, days = pct.get_linear_model_status('999999', filter='y', dl=dl, ptype=ptype, days=1)
duration_date = int(ct.duration_date * 1.4)
#    duration_date = 120
# duration_date = 300
du_date = duration_date
newdays = 5
end_date = None
ptype = 'low'
filter = 'y'
percent_status = 'n'
if len(str(duration_date)) < 4:
    # duration_date = tdd.get_duration_price_date('999999', dl=duration_date, end=end_date, ptype='dutype')
    du_date = tdd.get_duration_Index_date('999999',dl=duration_date)
    if cct.get_today_duration(du_date) <=3:
        duration_date = 5
        print ("duaration: %s duration_date:%s" %(cct.get_today_duration(du_date),duration_date))
    log.info("duaration: %s duration_date:%s" %(cct.get_today_duration(du_date),duration_date))
set_duration_console(du_date)
# all_diffpath = tdd.get_tdx_dir_blocknew() + '062.blk'
parser=cct.MoniterArgmain()
parserDuraton=cct.DurationArgmain()
while 1:
    try:
        # df = sina_data.Sina().all
        top_now = tdd.getSinaAlldf(market='cx', vol=ct.json_countVol, type=ct.json_countType)

        top_dif = top_now
        # top_now.to_hdf("testhdf5", 'marketDD', format='table', complevel=9)
        now_count = len(top_now)
        radio_t = cct.get_work_time_ratio()
        # top_now = top_now[top_now.buy > 0]
        time_Rt = time.time()
        time_d = time.time()
        if time_d - time_s > delay_time:
            status_change = True
            time_s = time.time()
            top_all = pd.DataFrame()
        else:
            status_change = False
        # print ("Buy>0:%s" % len(top_now[top_now['buy'] > 0])),
        if len(top_now) > 10 or cct.get_work_time():
            time_Rt = time.time()
            if len(top_all) == 0 and len(lastpTDX_DF) == 0:
                time_Rt = time.time()
                top_all,lastpTDX_DF = tdd.get_append_lastp_to_df(top_now, lastpTDX_DF=None, dl=duration_date,end=end_date,ptype=ptype,filter=filter, power=True, lastp=False,newdays=newdays)
                log.debug("len:%s"%(len(top_all)))
                # codelist = top_all.index.tolist()
                # log.info('toTDXlist:%s' % len(codelist))
                # # tdxdata = tdd.get_tdx_all_day_LastDF(codelist,dt=duration_date,ptype=ptype)
                # # print "duration_date:%s ptype=%s filter:%s"%(duration_date, ptype,filter)
                # # tdxdata = tdd.get_tdx_exp_all_LastDF(codelist, dt=duration_date, end=end_date,ptype=ptype,filter=filter)
                # power=True
                # tdxdata = tdd.get_tdx_exp_all_LastDF_DL(codelist, dt=duration_date, end=end_date,ptype=ptype,filter=filter,power=True)
                # log.debug("TdxLastP: %s %s" % (len(tdxdata), tdxdata.columns.values))
                # tdxdata.rename(columns={'low': 'llow'}, inplace=True)
                # tdxdata.rename(columns={'high': 'lhigh'}, inplace=True)
                # tdxdata.rename(columns={'close': 'lastp'}, inplace=True)
                # tdxdata.rename(columns={'vol': 'lvol'}, inplace=True)
                # if power:
                #     tdxdata = tdxdata.loc[:, ['llow', 'lhigh', 'lastp', 'lvol', 'date','ra','op','fib','ldate']]
                #     # print tdxdata[(tdxdata.op >15) | (tdxdata.op <3)]
                #     # print len(tdxdata[(tdxdata.op >12)]),
                # else:
                #     tdxdata = tdxdata.loc[:, ['llow', 'lhigh', 'lastp', 'lvol', 'date']]
                # log.debug("TDX Col:%s" % tdxdata.columns.values)
                # top_all = top_all.merge(tdxdata, left_index=True, right_index=True, how='left')
                # lastpTDX_DF = tdxdata
                # log.info('Top-merge_now:%s' % (top_all[:1]))
                # top_all = top_all[top_all['llow'] > 0]

            elif len(top_all) == 0 and len(lastpTDX_DF) > 0:
                top_all = top_now
                top_all = top_all.merge(lastpTDX_DF, left_index=True, right_index=True, how='left')
                # lastpTDX_DF=tdxdata
                log.info('Top-merge_now:%s' % (top_all[:1]))
                top_all = top_all[top_all['llow'] > 0]

            else:
                if 'couts' in top_now.columns.values:
                    if not 'couts' in top_all.columns.values:
                        top_all['couts'] = 0
                        top_all['prev_p'] = 0
                for symbol in top_now.index:
                    if 'couts' in top_now.columns.values:
                        top_all.loc[symbol, ct.columns_now] = top_now.loc[symbol, ct.columns_now]
                    else:
                        # top_now.loc[symbol, 'diff'] = round(
                        # ((float(top_now.loc[symbol, 'buy']) - float(
                        # top_all.loc[symbol, 'lastp'])) / float(top_all.loc[symbol, 'lastp']) * 100),
                        # 1)
                        top_all.loc[symbol, 'trade':'low'] = top_now.loc[symbol, 'trade':'low']
                        # top_all.loc[symbol, 'buy'] = top_now.loc[symbol, 'buy']
            # top_all = top_all[top_all.buy > 0]
            top_dif = top_all.copy()
            log.debug('top_dif:%s'%(len(top_dif)))
            if 'trade' in top_dif.columns:
                top_dif['buy'] = (
                    map(lambda x, y: y if int(x) == 0 else x, top_dif['buy'].values, top_dif['trade'].values))

            #判断主升
            # log.debug('top_dif:%s'%(len(top_dif)))
            if ct.checkfilter and cct.get_now_time_int() > 915 and cct.get_now_time_int() < ct.checkfilter_end_timeDu:
                top_dif = top_dif[top_dif.buy >= top_dif.llastp * ct.changeRatio]
                log.debug('top_dif:%s'%(len(top_dif)))
                top_dif = top_dif[top_dif.buy >= top_dif.lhigh * ct.changeRatio]
                log.debug('top_dif:%s'%(len(top_dif)))

            if cct.get_now_time_int() > 915:
                top_dif = top_dif[top_dif.buy > 0]

            log.debug('top_dif:%s'%(len(top_dif)))
            top_dif['diff'] = (
                map(lambda x, y: round((x - y) / y * 100, 1), top_dif['buy'].values, top_dif['lastp'].values))
            # print top_dif.loc['600610',:]
            # top_dif = top_dif[top_dif.trade > 0]
            # if cct.get_now_time_int() >< 932:

            # top_dif = top_dif[top_dif.low > 0]
            # log.debug("top_dif.low > 0:%s" % (len(top_dif)))
                # top_dif.loc['600610','volume':'lvol']
            top_dif['volume'] = (
                map(lambda x, y: round(x / y / radio_t, 1), top_dif.volume.values, top_dif.lvol.values))

            # if 'op' in top_dif.columns:
            #     top_dif=top_dif[top_dif.op >12]
            #     print "op:",len(top_dif),


            # top_dif = top_dif[top_dif.volume < 100]
            # print top_dif.loc['002504',:]

            # if filter == 'y':
            #     top_dif = top_dif[top_dif.date >= cct.day8_to_day10(duration_date)]

            # log.info('dif1-filter:%s' % len(top_dif))
            # print top_dif.loc['600533',:]
            # log.info(top_dif[:1])
            # top_dif = top_dif[top_dif.buy > top_dif.llastp]
            # top_dif = top_dif[top_dif.buy > top_dif.lhigh]
            # log.debug('dif2:%s' % len(top_dif))
            # top_dif['volume'] = top_dif['volume'].apply(lambda x: round(x / radio_t, 1))
            # log.debug("top_diff:vol")
            #

            if len(top_dif) == 0:
                print "No G,DataFrame is Empty!!!!!!"
            else:
                log.debug('dif6 vol:%s' % (top_dif[:1].volume))
                log.debug('dif6 vol>lvol:%s' % len(top_dif))

                # top_dif = top_dif[top_dif.buy >= top_dif.open*0.99]
                # log.debug('dif5 buy>open:%s'%len(top_dif))
                # top_dif = top_dif[top_dif.trade >= top_dif.buy]
                # df['volume']= df['volume'].apply(lambda x:x/100)

                # goldstock = len(top_dif[top_dif.buy >= top_dif.lhigh * 0.99])
                goldstock = len(top_dif[(top_dif.buy >= top_dif.lhigh * 0.99) & (top_dif.buy >= top_dif.llastp * 0.99)])
                ## goldstock=len(top_dif[top_dif.buy >(top_dif.high-top_dif.low)/2])
                if ptype == 'low':
                    top_dif = top_dif[top_dif.lvol > ct.LvolumeSize]
                    if cct.get_now_time_int() > 1100 and cct.get_now_time_int() < 1330:
                        # if cct.get_now_time_int() > 931 and cct.get_work_time():
                        top_dif = top_dif[(top_dif.volume > ct.VolumeMinR) & (top_dif.volume < ct.VolumeMaxR)]
                    # top_dif = top_dif[top_dif.lvol > 12000]
                    if 'couts' in top_dif.columns.values:
                        top_dif = top_dif.sort_values(by=['diff', 'percent', 'volume', 'couts', 'ratio'],
                                                      ascending=[0, 0, 0, 1, 1])
                    else:
                        top_dif = top_dif.sort_values(by=['diff', 'percent', 'ratio'], ascending=[0, 0, 1])
                else:
                    # top_dif['diff'] = top_dif['diff'].apply(lambda x: x * 2 if x > 0 else x)
                    top_dif = top_dif[top_dif.lvol > ct.LvolumeSize]
                    top_dif['diff']=top_dif['diff'].apply(lambda x:x*2 if x < 0 else x )
                    if 'couts' in top_dif.columns.values:
                        top_dif = top_dif.sort_values(by=['diff', 'percent', 'volume', 'couts', 'ratio'],
                                                      ascending=[1, 0, 0, 1, 1])
                    else:
                        top_dif = top_dif.sort_values(by=['diff', 'percent', 'ratio'], ascending=[1, 0, 1])

                # top_all=top_all.sort_values(by=['percent','diff','couts','ratio'],ascending=[0,0,1,1])
                # print rl.format_for_print(top_dif[:10])
                # top_dd = pd.concat([top_dif[:5],top_temp[:3],top_dif[-3:],top_temp[-3:]], axis=0)
                if percent_status == 'y' and (
                        cct.get_now_time_int() > 915 and cct.get_now_time_int() < 1505) and ptype == 'low':
                    top_dif = top_dif[top_dif.percent >= 0]
                    top_temp = stf.filterPowerCount(top_dif,ct.PowerCount)
                    top_end = top_dif[-5:].copy()
                    top_temp = pct.powerCompute_df(top_temp,dl=ct.PowerCountdl,talib=True,newdays=newdays)
                    top_end = pct.powerCompute_df(top_end,dl=ct.PowerCountdl,talib=True,newdays=newdays)

                # elif percent_status == 'y' and cct.get_now_time_int() > 935 and ptype == 'high' :
                elif ptype == 'low':
                    # top_dif = top_dif[top_dif.percent >= 0]
                    top_temp = stf.filterPowerCount(top_dif,ct.PowerCount)
                    top_end = top_dif[-5:].copy()
                    top_temp = pct.powerCompute_df(top_temp,dl=ct.PowerCountdl,talib=True,newdays=newdays)
                    top_end = pct.powerCompute_df(top_end,dl=ct.PowerCountdl,talib=True,newdays=newdays)
                else:
                    # top_dif = top_dif[top_dif.percent >= 0]
                    top_end = top_dif[:5].copy()
                    top_temp = top_dif[-ct.PowerCount:].copy()
                    top_temp = pct.powerCompute_df(top_temp, dl=ct.PowerCountdl,talib=True,newdays=newdays)
                    top_end = pct.powerCompute_df(top_end, dl=ct.PowerCountdl,talib=True,newdays=newdays)

                print ("N:%s K:%s %s G:%s" % (
                    now_count, len(top_all[top_all['buy'] > 0]),
                    len(top_now[top_now['volume'] <= 0]), goldstock)),
                print "Rt:%0.1f dT:%s N:%s" % (float(time.time() - time_Rt), cct.get_time_to_date(time_s),cct.get_now_time())
                cct.set_console(width, height,
                                title=[du_date, 'dT:%s' % cct.get_time_to_date(time_s), 'G:%s' % goldstock,
                                       'zxg: %s' % (blkname)])

                top_temp = stf.getBollFilter(df=top_temp, boll=ct.bollFilter)
                if 'op' in top_temp.columns:
                    # top_temp = top_temp.sort_values(by=ct.Duration_sort_op,
                    #             ascending=ct.Duration_sort_op_key)

                    # top_temp=top_temp[top_temp.op >12]
                    # top_temp = top_temp.sort_values(by=['ra', 'op'],ascending=[0, 0])[:10]

                    # top_temp = top_temp.sort_values(by=['diff', 'op', 'ra', 'percent', 'ratio'],
                                                    # ascending=[0, 0, 0, 0, 1])[:10]


                    # top_temp = top_temp.sort_values(by=['op','ra','diff', 'percent', 'ratio'], ascending=[0,0,0, 0, 1])[:10]
                    # top_temp = top_temp.sort_values(by=['op','ldate','ra','diff', 'percent', 'ratio'], ascending=[0,0,0,0, 0, 1])[:10]
                    if cct.get_now_time_int() > ct.checkfilter_end_timeDu and duration_date > ct.duration_date_sort:
                        top_temp = top_temp.sort_values(by=ct.Duration_percent_op,
                                    ascending=ct.Duration_percent_op_key)
                    else:
                        top_temp = top_temp.sort_values(by=ct.Duration_percentdn_op,
                                    ascending=ct.Duration_percentdn_op_key)

                if cct.get_now_time_int() > 915 and cct.get_now_time_int() < 935:
                    # top_temp = top_temp[ (top_temp['ma5d'] > top_temp['ma10d']) & (top_temp['buy'] > top_temp['ma10d']) ][:10]

                    top_dd =  cct.combine_dataFrame(top_temp[:10], top_end,append=True, clean=True)
                    top_dd = top_dd.drop_duplicates()
                    top_dd = top_dd.loc[:,ct.Duration_format_buy]
                else:
                    # top_temp = top_temp[ (top_temp['ma5d'] > top_temp['ma10d']) & (top_temp['trade'] > top_temp['ma10d']) ][:10]
                    # top_temp = top_temp[top_temp['trade'] > top_temp['ma10d']]

                    top_dd =  cct.combine_dataFrame(top_temp[:10], top_end,append=True, clean=True)
                    top_dd = top_dd.drop_duplicates()
                    top_dd = top_dd.loc[:,ct.Duration_format_trade]
                print rl.format_for_print(top_dd)
                dfgui.show(top_dif)
            # if cct.get_now_time_int() < 930 or cct.get_now_time_int() > 1505 or (cct.get_now_time_int() > 1125 and cct.get_now_time_int() < 1505):
            # print rl.format_for_print(top_dif[-10:])
            # print top_all.loc['000025',:]
            # print "staus",status

            if status:
                for code in top_dd[:10].index:
                    code = re.findall('(\d+)', code)
                    if len(code) > 0:
                        code = code[0]
                        kind = sl.get_multiday_ave_compare_silent(code)
                        # print top_all[top_all.low.values==0]

                        # else:
                        #     print "\t No RealTime Data"
        else:
            print "\tNo Data"
        int_time = cct.get_now_time_int()
        if cct.get_work_time():
            if int_time < 926:
                cct.sleep(120)
            elif int_time < 930:
                cct.sleep((930 - int_time) * 60)
                # top_all = pd.DataFrame()
                time_s = time.time()
            else:
                cct.sleep(120)
        elif cct.get_work_duration():
            while 1:
                cct.sleep(120)
                if cct.get_work_duration():
                    print ".",
                    cct.sleep(120)
                else:
                    # top_all = pd.DataFrame()
                    cct.sleeprandom(60)
                    time_s = time.time()
                    print "."
                    break
        else:
            raise KeyboardInterrupt("StopTime")
    except (KeyboardInterrupt) as e:
        st = raw_input("status:[go(g),clear(c),[d 20150101 [l|h]|[y|n|pn|py],quit(q),W(a),sh]:")
        if len(st) == 0:
            status = False
        elif st.lower() == 'r':
            end = True
            while end:
                cmd = (raw_input('DEBUG[top_dif,top_now,e|q]:'))
                if cmd == 'e' or cmd == 'q' or len(cmd) == 0:
                    break
                else:
                    print eval(cmd)
                    # raise KeyboardInterrupt("StopTime")
        elif st.lower() == 'g' or st.lower() == 'go':
            status = True
            for code in top_dd[:10].index:
                code = re.findall('(\d+)', code)
                if len(code) > 0:
                    code = code[0]
                    kind = sl.get_multiday_ave_compare_silent(code)
        elif st.lower() == 'clear' or st.lower() == 'c':
            top_all = pd.DataFrame()
            time_s = time.time()
            status = False
        elif st.startswith('d') or st.startswith('dt'):
            # dl = st.split()
            args = parserDuraton.parse_args(st.split()[1:])
            if len(str(args.start)) > 0:
                end_date=args.end
                duration_date=args.start
                if len(str(duration_date)) < 4:
                    du_date = tdd.get_duration_Index_date('999999',dl=int(duration_date))
                    # print duration_date
                    ct.PowerCountdl = duration_date
                set_duration_console(du_date)
                time_s = time.time()
                status = False
                top_all = pd.DataFrame()
                lastpTDX_DF = pd.DataFrame()

        elif st.lower() == 'w' or st.lower() == 'a':
            # if ptype == 'low':
                # codew = (top_dd[:10].index).tolist()
            # else:
                # codew = (top_dd[-10:].index).tolist()
            if st.lower() == 'a':
                codew = (top_dd.index[:ct.writeCount]).tolist()
                cct.write_to_blocknew(block_path, codew)
                # sl.write_to_blocknew(all_diffpath, codew)
            else:
                codew = (top_dd.index[:ct.writeCount]).tolist()
                cct.write_to_blocknew(block_path, codew, False)
                # sl.write_to_blocknew(all_diffpath, codew, False)
            print "wri ok:%s" % block_path
            cct.sleeprandom(120)
        elif st.startswith('sh'):
            while 1:
                input = raw_input("code:")
                if len(input) >= 6:
                    args = parser.parse_args(input.split())
                    if len(str(args.code)) == 6:
                        # print args.code
                        if args.code in top_temp.index.values:
                            lhg.get_linear_model_histogram(args.code, start=top_temp.loc[args.code, 'date'],
                                                           end=args.end, vtype=args.vtype,
                                                           filter=args.filter)
                elif input.startswith('q'):
                    break
                else:
                    pass
        else:
            sys.exit(0)
    except (IOError, EOFError, Exception) as e:
        print "Error", e
        #traceback.print_exc()
        cct.sleeprandom(120)

'''
{symbol:"sz000001",code:"000001",name:"平安银行",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"12.36",sell:"12.36",settlement:"12.34",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:7.133,pb:1.124,mktcap:17656906.355526,nmc:14566203.350486,turnoverratio:0},
{symbol:"sz000002",code:"000002",name:"万  科Ａ",trade:"0.00",pricechange:"0.000",changepercent:"0.000",buy:"0.00",sell:"0.00",settlement:"24.43",open:"0.00",high:"0.00",low:"0",volume:0,amount:0,ticktime:"09:17:55",per:17.084,pb:3.035,mktcap:26996432.575,nmc:23746405.928119,turnoverratio:0},

python -m cProfile -s cumulative timing_functions.py
http://www.jb51.net/article/63244.htm

'''
