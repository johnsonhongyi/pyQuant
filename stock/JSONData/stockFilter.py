# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
from JohnsonUtil import commonTips as cct
import JohnsonUtil.johnson_cons as ct
from JSONData import powerCompute as pct
# from JSONData import tdx_data_Day as tdd
from JSONData import get_macd_kdj_rsi as getab
from JSONData import tdx_data_Day as tdd
import pandas as pd
from JohnsonUtil import LoggerFactory
log = LoggerFactory.log
import time
import random

# def func_compute_df2(c,lc,lp,h,l,b1_v):


def func_compute_df2(c, lc, h, l):
    if h - l == 0:
        du_p = 0.1
    else:
        du_p = round((h - l) / lc * 100, 1)
    mean_p = round((h + l) / 2, 1)
    if c < mean_p and c < lc:
        du_p = -du_p
    return du_p


def filterPowerCount(df, count=200, down=False, duration=2):

    nowint = cct.get_now_time_int()
    df.sort_values('percent', ascending=False, inplace=True)
    top_temp = df[:count].copy()

    if 915 < nowint <= 945:
        if nowint <= 935:
            top_temp = df[(df.buy > df.llastp) | (
                df.percent > df['per%sd' % (duration)])]
        else:
            top_temp = df[((df.open > df.llastp) & (df.low >= df.llastp)) | (
                df.percent > df['per%sd' % (duration)])]
        if len(top_temp) > 0:
            return top_temp
        else:
            log.error("915 open>llastp is None")
            return df[:count].copy()

    if 930 < nowint <= 945:
        top_high = df[((df.open > df.llastp) & (df.low >= df.llastp))]
    elif 945 < nowint:
        if 'nlow' in df.columns:
            # top_high = df[ (df.nlow >= df.llastp) | (df.close >= df.nlow)]
            top_high = df[((df.nlow >= df.llastp) & (df.nlow >= df.low)) | (
                (df.nlow <= df.low) & (df.open == df.nlow))]
        else:
            top_high = df[((df.open > df.llastp) & (df.low > df.llastp)) | (
                df.percent > df['per%sd' % (duration)])]
    else:
        top_high = None

    if top_high is not None:
        top_high['upper'] = map(lambda x: round(
            (1 + 11.0 / 100) * x, 1), top_high.ma10d)
        top_high['lower'] = map(lambda x: round(
            (1 - 9.0 / 100) * x, 1), top_high.ma10d)
        top_high['ene'] = map(lambda x, y: round(
            (x + y) / 2, 1), top_high.upper, top_high.lower)
        if 930 < nowint < 1500:
            radio_t = cct.get_work_time_ratio()
        else:
            radio_t = 1

        top_high = top_high[(((top_high.buy > top_high.ene) & (top_high.volume / radio_t > 2))) | (
            ((top_high.lastv1d > top_high.lvol * 1.5)) & (top_high.lastp1d > top_high.ene))]
        if len(top_high) > count:
            top_high = top_high[(top_high.low > top_high.ene) | (
                (top_high.percent > 1) & (top_high.volume > 2))]
        top_temp = cct.combine_dataFrame(
            top_temp, top_high, col=None, compare=None, append=True, clean=True)

    return top_temp


def compute_perd_value(df, market_value=3, col='per'):

    if market_value==None or market_value < '2':
        market_value = 3
    temp = df[df.columns[(df.columns >= '%s1d' % (col)) & (df.columns <= '%s%sd' % (col, market_value))]]

    df['%s%sd' % (col, market_value)] = temp.T.sum().apply(lambda x: round(x, 1))
    return df


def getBollFilter(df=None, boll=ct.bollFilter, duration=ct.PowerCountdl, filter=True, ma5d=True, dl=14, percent=True, resample='d', ene=False, upper=False, down=False, indexdff=True, cuminTrend=False, top10=True):

    # drop_cxg = cct.GlobalValues().getkey('dropcxg')
    # if len(drop_cxg) >0:
        # log.info("stf drop_cxg:%s"%(len(drop_cxg)))
        # drop_cxg = list(set(drop_cxg))
        # drop_t = [ co for co in drop_cxg if co in df.index]
        # if len(drop_t) > 0:
            # df = df.drop(drop_t,axis=0)top
            # log.error("stf drop_cxg:%s"%(len(drop_t)))

    # hvdu max量天数  lvdu  min天数  hv max量  lv 量
    # fib < 2 (max) fibl > 2   lvdu > 3  (hvdu > ? or volume < 5)? ene
    time_s = time.time()
    # df['upper'] = map(lambda x: round((1 + 11.0 / 100) * x, 1), df.ma10d)
    # df['lower'] = map(lambda x: round((1 - 9.0 / 100) * x, 1), df.ma10d)
    # df['ene'] = map(lambda x, y: round((x + y) / 2, 1), df.upper, df.lower)

    '''
    df = df[(df.close > df.ma20d) | (df.close > df.ene)]
    if filter:
        if 'boll' in df.columns:
            df = df[(df.boll >= boll) | (df.buy > df.upper)]
    '''

    # if 'nlow' in df.columns:
        # df = df[ ((df.nlow >= df.llastp) & (df.nlow >= df.low)) | ((df.nlow <= df.low) & (df.open == df.nlow))]
    # if cct.get_work_time() and 'df2' in df.columns:
    #     if 915 < cct.get_now_time_int() < 930:
    #         df['cumnow'] =  map(lambda x, y: 1 if x - y > 0 else 0, df.close, df.cumaxe)
    #     else:
    #         df['cumnow'] =  map(lambda x, y: 1 if x - y > 0 else 0, df.high, df.cumaxe)
    #     df['df2'] = (df['df2'] + df['cumnow']).map(lambda x: int(x))
        # df = df[df.df2 > 1]
    # else:
        # df = df[df.df2 > 0]
    radio_t = cct.get_work_time_ratio()
    df['lvolr%s' % (resample)] = df['volume']
    # df['volume'] = (map(lambda x, y: round(x / y / radio_t, 1), df.nvol.values, df.lvolume.values))
    if cct.get_now_time_int() > 1530:
        df['volume'] = (map(lambda x, y, z: round((x / y / radio_t) if z <
                                                  9.9 else (x / y), 1), df.nvol.values, df.ma5vol.values, df.percent.values))
    else:
        df['volume'] = (map(lambda x, y, z: round((x / y / radio_t) if z <
                                                  9.9 else (x / y), 1), df.nvol.values, df.lvol.values, df.percent.values))
    # df['volume'] = (map(lambda x, y,z: round((x / y / radio_t) if z < 9.9 else (x / y) , 1), df.nvol.values, df.ma5vol.values,df.percent.values))
    # df['volume'] = (map(lambda x, y: round(x / y / radio_t, 1), df.nvol.values, df.lastv1d.values))

    indexfibl = cct.GlobalValues().getkey('indexfibl')
    sort_value = cct.GlobalValues().getkey('market_sort_value')
    market_key = cct.GlobalValues().getkey('market_key')
    market_value = cct.GlobalValues().getkey('market_value')
    tdx_Index_Tdxdata = cct.GlobalValues().getkey('tdx_Index_Tdxdata')
    # if market_key is not None:
    #     market_dff = eval(ct.Market_sort_idx_perd[market_key])[0]
    # if int(market_value) > 1 and 930 < cct.get_now_time_int():

    if market_value != '1':
        df= compute_perd_value(df, market_value, 'perc')
        df= compute_perd_value(df, market_value, 'per')
        if tdx_Index_Tdxdata is not None:
            tdx_Index_Tdxdata = compute_perd_value(tdx_Index_Tdxdata,market_value,'perc')
            tdx_Index_Tdxdata = compute_perd_value(tdx_Index_Tdxdata,market_value,'per')
        if market_key == '3':
            idx_k = tdx_Index_Tdxdata['perc%sd'%(market_value)].max()
        else:
            idx_k = int(market_value) if market_value is not None else 1
    else:
        idx_k = int(market_value)

    # if sort_value <> 'percent' and (market_key in ['2', '3','5','4','6','x','x1','x2'] and market_value not in ['1']):
    if (market_key in ['1','2', '3','5','4','6','8','9','x','x1','x2']) :
    # if sort_value <> 'percent' and (market_key in ['2', '3','5','4','6','8','9','x','x1','x2']) :
        # @['5','4','6','8','x','x1','x2'] johnson_cons
        # print("sort_value:%s,market_key:%s ,market_value:%s" %
        #       (sort_value, market_key, market_value))
        if market_key is not None and market_value is not None:
            # if market_key == '3':

            if market_key == '3' and market_value not in ['1']:
                market_value= int(market_value)
                log.info("stf market_key:%s" % (market_key))
                idx_k= cct.get_col_in_columns(df, 'perc%sd', market_value)
                # filter percd > idx
                # df= df[(df[("perc%sd" % (idx_k))] >= idx_k) | (df[("perc%sd" % (idx_k))]< -idx_k)]
                df= df[(df[("perc%sd" % (idx_k))] >= idx_k) ]

            # elif market_key in ['5','6'] and market_value not in ['1']:
            #     # market_value= int(market_value)
            #     # filter percd > idx
            #     idx_k = int(market_value)
            #     df= df[ (df[("%s" % (sort_value))] <= idx_k) ]

            elif market_key in ['x2','x','x1','6'] and market_value not in ['1']:
                # market_value= int(market_value)
                # filter percd > idx
                # idx_k = int(market_value)
                if market_key in ['x2','x']:
                    df= df[ (df[("%s" % (sort_value))] >= idx_k) ]
                else:
                    df= df[ (df[("%s" % (sort_value))] <= idx_k) ]
                # if int(market_value) > 1 and 930 < cct.get_now_time_int():
                #     df= compute_perd_value(df, market_value, 'perc')
                #     df= compute_perd_value(df, market_value, 'per')

            elif market_key in ['4','8','9','5','1'] and market_value not in ['1']:
                # market_value= int(market_value)
                # filter percd > idx
                idx_k = int(market_value)
                if market_key not in ['1','5']:
                    df= df[ (df[("%s" % (sort_value))] <= idx_k) ]
                else:
                    df= df[ (df[("%s" % (sort_value))] >= idx_k) ]

            # elif market_key == '2':
            #     if int(market_value) > 1 and 915 < cct.get_now_time_int():
            #         # df['per%d'%(market_value)] = compute_perd_value(df,market_value)
            #         df= compute_perd_value(df, market_value,'per')
            #         df= compute_perd_value(df, market_value, 'perc')



    # if sort_value <> 'percent' and (market_key in ['2','3'] and market_value not in ['1'] ):
    #     if indexfibl is not None:
    #         df = df[df.fibl >= (indexfibl - 1)]
    #     else:
    #         indexfibl = 1
    #     if cuminTrend:
    #         cuminfibl = cct.GlobalValues().getkey('cuminfibl')
    #         if cuminfibl is None:
    #             cuminfibl = cct.get_index_fibl()
    # if cuminfibl > 1:
    #     df = df[df.df2 >= cuminfibl]

    #    print df.loc['300107'][['close','cumine','llastp','cumaxe','cumaxc']]
    #     df = df[ (df.cumine == df.cumaxc) | (df.close >= df.cumine) | (df.llastp >=df.cumaxc) | (df.close >= df.cumaxe) ]
    # else:
    #     upper = True

    if not down:
        if upper:
            # upper_count = len( df[ ( ( df.buy > df.upper)| ( df.lastp0d > df.upper) | ( df.lastp1d > df.upper) | ( df.lastp2d > df.upper) | ( df.lastp3d > df.upper))])
            # # ene_count = len(df[df.buy > df.upper])
            # if upper_count > 30:
            #     df = df[ (  ( df.buy > df.upper)| ( df.lastp0d > df.upper) | ( df.lastp1d > df.upper) | ( df.lastp2d > df.upper) | ( df.lastp3d > df.upper))]
            # else:
            #     df = df[ ( (( df.buy > df.ene ) ) | ( df.buy > df.upper)| ( df.lasth0d > df.upper) | ( df.lasth1d > df.upper) | ( df.lasth2d > df.upper) | ( df.lasth3d > df.upper))]
            df = df[(df.low >= df.upper) | (df.close >= df.upper) | (df.per1d >= 9.5) | (
                df.lastp1d == df.hmax) | ((df.lastp1d <> df.hmax) & (df.high > df.hmax))]
        else:
            if 935 < cct.get_now_time_int() < 1400:
                df = df[((df.buy > df.ene) | (df.llastp > df.ene) | (
                    df.llastp >= df.max5) | (df.high >= df.max5) | (df.max5 >= df.upper))]
            else:
                df = df[((df.buy > df.ene) | (df.llastp > df.ene) | (
                    df.llastp >= df.max5) | (df.high >= df.max5) | (df.max5 >= df.upper))]

    # df['cumins'] = round(cum_counts.index[0], 2)
    # df['cumine'] = round(cumdf[-1], 2)
    # df['cumax']
    # df.rename(columns={'cumin': 'df2'}, inplace=True)
    if df is None:
        print "dataframe is None"
        return None
    else:
        # top10 = df[ (df.percent >= 9.99) & (df.b1_v > df.a1_v)]

        if resample in ['d','w']:
            # if not top10 or (cct.get_now_time_int() < 950 or cct.get_now_time_int() > 1502):
            #     df.loc[((df.b1_v > df.a1_v) & (df.percent > 9)), 'percent'] = 10.1
            #     df.loc[((df.percent >= 9.97) & (df.percent < 10.1)), 'percent'] = 10

            # else:
            #     df.loc[((df.b1_v > df.a1_v) & (df.percent > 9)), 'percent'] = 10.1
            #     df.loc[((df.percent >= 9.97) & (df.percent < 10.1)), 'percent'] = 10

            # df.loc[df.per1d >= 9.99, 'per1d'] = 10
            df['percent'] = df['percent'].apply(lambda x: round(x, 2))
            # time_ss = time.time()
            perc_col = [co for co in df.columns if co.find('perc') == 0]
            per_col = [co for co in df.columns if co.find('per') == 0]
            # per_col = list(set(per_col) - set(perc_col) - set(['per1d', 'perlastp']))
            per_col = list(set(per_col) - set(perc_col) -
                           set(['per1d', 'perlastp']))

            perc_col.remove('percent')

            for co in perc_col:
                df[co] = df[co].apply(lambda x: round(x, 2))

            # da, down_zero, down_dn, percent_l = 1, 0, 0, 2
            # da, down_zero, down_dn, percent_l = 1, 0, -1, 1
            # df['perc_n'] = map((lambda h, lh, l, ll, c, lc: (1 if (h - lh) > 0 else down_dn) + (1 if c - lc > 0 else down_dn) + (1 if (l - ll) > 0 else down_dn) + (2 if (c - lh) > 0 else down_zero) + (2 if (l - lc) > 0 else down_zero) + (0 if (h - lc) > 0 else down_dn)), df['high'], df['lasth%sd' % da], df['low'], df['lastl%sd' % da], df['close'],df['lastp%sd' % da])
            # df['perc_n'] = map((lambda c, lc: (1 if (c - lc) > 0 else down_zero) + (1 if (c - lc) / lc * 100 > 3 else down_zero) +
            # (down_dn if (c - lc) / lc * 100 < -3 else down_zero)), df['close'], df['lastp%sd' % da])

            # idx_rnd = random.randint(0, len(df) - 10) if len(df) > 10 else 0

            # print "idx_rnd",idx_rnd,df.ix[idx_rnd].lastp0d ,df.ix[idx_rnd].close,df.ix[idx_rnd].lastp0d != df.ix[idx_rnd].close

            # if not upper:
            #     if cct.get_work_time() or df.ix[idx_rnd].lastp0d <> df.ix[idx_rnd].close:
            #         nowd, per1d = 0, 1
            #         if 'nlow' in df.columns:
            #             df['perc_n'] = map(cct.func_compute_percd2, df['close'], df['llastp'], df['open'],df['lasto%sd' % nowd], df['lasth%sd' %
            #                                                                                                   (nowd)], df['lastl%sd' % (nowd)], df['nhigh'], df['nlow'],df['nvol']/radio_t,df['lastv%sd'%(nowd)], df['hmax'],df['df2'])
            #         else:
            #             df['perc_n'] = map(cct.func_compute_percd2, df['close'], df['llastp'], df['open'],df['lasto%sd' % nowd], df['lasth%sd' %
            #                                                                                                   (nowd)], df['lastl%sd' % (nowd)], df['high'], df['low'],df['nvol']/radio_t,df['lastv%sd'%(nowd)], df['hmax'],df['df2'])
            #     else:
            #         nowd, per1d = 1, 2
            #         # print  df['per%sd' % da+1], df['lastp%sd' % (da)], df['lasth%sd' % (da)], df['lastl%sd' % (da)], df['high'], df['low']
            #         df['perc_n'] = map(cct.func_compute_percd2, df['close'], df['llastp'], df['open'],df['lasto%sd' % nowd], df['lasth%sd' %
            #                                                                                               (nowd)], df['lastl%sd' % (nowd)], df['high'], df['low'], df['hmax'])


            
            idx_rnd = random.randint(0, len(df) - 10) if len(df) > 10 else 0
            # if not upper:
               # if cct.get_work_time() or df.ix[idx_rnd].lastp1d <> df.ix[idx_rnd].close:
            if cct.get_work_time() :
               nowd, per1d=1, 1
               if 'nlow' in df.columns:
                   df['perc_n']=map(cct.func_compute_percd2021, df['open'], df['close'], df['nhigh'], df['nlow'], df['lasto%sd' % nowd], df['llastp'],
                                     df['lasth%sd' % (nowd)], df['lastl%sd' % (nowd)], df['ma5d'], df['ma10d'], df['nvol'] / radio_t, df['lastv%sd' % (nowd)])
               else:
                   df['perc_n']=map(cct.func_compute_percd2021, df['open'], df['close'], df['high'], df['low'], df['lasto%sd' % nowd], df['llastp'],
                                     df['lasth%sd' % (nowd)], df['lastl%sd' % (nowd)], df['ma5d'], df['ma10d'], df['nvol'] / radio_t, df['lastv%sd' % (nowd)])
            else:
               nowd, per1d=1, 1
               # print  df['per%sd' % da+1], df['lastp%sd' % (da)], df['lasth%sd' % (da)], df['lastl%sd' % (da)], df['high'], df['low']
               df['perc_n']=map(cct.func_compute_percd2021, df['open'], df['close'], df['high'], df['low'], df['lasto%sd' % nowd], df['llastp'],
                                     df['lasth%sd' % (nowd)], df['lastl%sd' % (nowd)], df['ma5d'], df['ma10d'], df['nvol'] / radio_t, df['lastv%sd' % (nowd)])

            for co in perc_col:
                df[co] = (df[co] + df['perc_n']).map(lambda x: round(x,1))
            

            # for co in per_col:
            # df[co] = (df[co] + df['percent']).map(lambda x: int(x))

            # print "percT:%.2f"%(time.time()-time_ss)
        else:
            df['percent']=(map(lambda x, y: round(
                (x - y) / y * 100, 1) if int(y) > 0 else 0, df.buy, df.lastp1d))
            # df.loc['002204'].percent
            # -15.4
            # ipdb> df.loc['002204'].ma10d
            # 3.2000000000000002
            # ipdb> df.loc['002204'].ma5d
            # 3.2999999999999998
    if 'fib' not in df.columns:
        df['fib']= 0
    # else:

    co2int= ['boll', 'op', 'ratio', 'fib', 'fibl', 'df2']
    # co2int.extend([co for co in df.columns.tolist()
    #                if co.startswith('perc') and co.endswith('d')])
    co2int.extend(['top10', 'topR'])
    co2int= [inx for inx in co2int if inx in df.columns]

    for co in co2int:
        df[co]= df[co].astype(int)

    # if down:
    #     # if 'nlow' in df.columns:
    #     #     if 'max5' in df.columns:
    #     #         # df = df[(df.hmax >= df.ene) & (df.nlow >= df.low) & (df.low <> df.high) & (((df.low < df.hmax) & (df.high > df.cmean)) | (df.high > df.max5))]
    #     #         df = df[ (((df.buy > df.ene) & (df.volume / radio_t > 1.5)) ) |  (((df.lastv1d > df.lvol * 1.5) & (df.lastv1d > df.lvol * 1.5)) & (df.lastp1d > df.ene) )]
    #     #     else:
    #     #         df = df[ (((df.buy > df.ene) & (df.volume / radio_t > 1.5)) ) |  (((df.lastv1d > df.lvol * 1.5) )  )]
    #     # else:
    #     #     # df = df[ (df.max5 >= df.ene) & (df.low <> df.high) & (((df.low < df.hmax) & (df.close > df.cmean)) | (df.high > df.cmean))]
    #     #     df = df[ (((df.buy > df.ene) & (df.volume / radio_t > 1.5)) )  | (((df.lastp1d > df.ene) ) | ((df.buy > df.max5)|(df.buy > df.ene)) | (df.max5 >= df.ene)  | (df.high > df.cmean) )]
    #     return df

    if cct.get_work_time() and 'b1_v' in df.columns and 'nvol' in df.columns:
        df= df[(df.b1_v > 0) | (df.nvol > 0)]

    if (cct.get_now_time_int() > 915 and cct.get_now_time_int() < 926):
        df['b1_v']= df['volume']
    else:
        dd= df[df.percent < 10]
        dd['b1_v']= dd['volume']
        df= cct.combine_dataFrame(df, dd.loc[:, ['b1_v']])
        # print "t:%0.2f"%(time.time()-time_ss)





        # if int(market_value) < 3 and 930 < cct.get_now_time_int():
        #     if 'nlow' in df.columns:
        #         # df = df[((df.per1d < 3) & (df.nlow >= df.llastp)) | ((df.per1d > 5) & (df.buy > df.llastp))]
        #         df = df[((df.per1d < 3) & (df.nlow >= df.llastp)) | ((df.per1d > 5) & (df.buy > df.llastp))]
        #     else:
        #         df = df[((df.per1d < 3) & (df.open > df.llastp)) | ((df.per1d > 5) & (df.buy > df.llastp))]

    # else:
    #     if 'fib' in df.columns:
    #         df = df[df.fib <= 5]

        # log.error("perc%sd"%(market_value))

    # elif market_key is not None and market_key == '2':
    #     if market_value in ['1', '2']:
    #         df['dff'] = (map(lambda x, y, z: round((x + (y if z > 20 else 3 * y)), 1), df.dff.values, df.volume.values, df.ratio.values))

    # df['df2'] = (map(lambda x, y, z: w=round((x - y) / z * 100, 1), df.high.values, df.low.values, df.llastp.values))
    # df['df2'] = (map(func_compute_df2, df.close.values, df.llastp.values,df.high.values, df.low.values,df.ratio.values))
    # df['df2'] = (map(func_compute_df2, df.close.values, df.llastp.values,df.high.values, df.low.values))


    '''
    filter_up= 'ma5d'
    filter_dn= 'ma10d'
    if ma5d and filter_up in df.columns:
        if filter_dn in df.columns:
            if market_key is not None and market_key == '3':
                df= df[(df.buy >= df[filter_up]) & (
                    df.buy * 1.02 >= df[filter_dn] * ct.changeRatio)]
            else:
                df= df[(df.buy >= df[filter_up])]
        else:
            df= df[df.buy >= df[filter_up] * ct.changeRatio]
    '''



        # df = df[(df.lvolume > df.lvol * 0.9) & (df.lvolume > df.lowvol * 1.1)]

    # if 'nlow' in df.columns and 932 < cct.get_now_time_int() < 1030:

    if ene:
        pass
        if 'nclose' in df.columns:
            # df = df[ ((df.buy > df.ene) ) | ((df.buy > df.upper) & ( df.nclose > df.cmean))]
            df= df[((df.buy > df.llastp)) | ((df['nclose'] > df['ene'] * ct.changeRatio) & (df['percent'] > -3) & (df.volume > 1.5)) |
                    ((df['nclose'] > df['upper'] * ct.changeRatio) & (df['buy'] > df['upper'] * ct.changeRatioUp)) | ((df['llastp'] > df['upper']) & (df['nclose'] > df['upper']))]
        else:
            df = df[((df.buy > df.llastp)) | ((df.buy > df.ene)) |
                    ((df.buy > df.upper) & (df.close > df.cmean))]

        if 'nlow' in df.columns and 930 < cct.get_now_time_int():
            # for col in ['nhigh', 'nclose', 'nlow','nstd']:
            #     df[col] = df[col].apply(lambda x: round(x, 2))
            if 'nhigh' in df.columns and 'nclose' in df.columns:
                # ncloseRatio = map(lambda x, y: x * ct.changeRatio if x * ct.changeRatio > y else y, df.nclose, df.nlow)
                df['ncloseRatio'] = map(lambda x: x * 0.99, df.nclose)
                df['nopenRatio'] = map(lambda x: x * 0.99, df.open)
                # nhighRatio = map(lambda x, y: x * ct.changeRatio if x * ct.changeRatio > y else y, df.nhigh, df.nclose)
                # if cct.get_now_time_int() > ct.nlow_limit_time:

                #           name   open    low   high  close  nclose   nlow  nhigh  nstd  ticktime
                # code
                # 601899  紫金矿业   4.25   4.24   4.69   4.69    4.52   4.24   4.42  0.12  15:00:00
                # 603917  合力科技  27.95  27.69  31.54  31.54   30.46  27.69  30.00  0.70  15:00:00
                # 300713   英可瑞  81.00  81.00  89.82  89.77   87.53  80.90  86.36  1.75  15:02:03
                # 000933  神火股份   9.07   9.02  10.00  10.00    9.71   9.02   9.44  0.24  15:02:03
                # 600050  中国联通   6.49   6.37   6.51   6.41    6.44   6.44   6.51  0.02  15:00:00
                # 002350  北京科锐  10.17  10.17  10.75  10.23   10.31  10.17  10.75  0.07  15:02:03
                # 603363  傲农生物  17.49  16.91  18.35  18.35   17.35  17.18  18.00  0.34  15:00:00
                # 000868  安凯客车   8.77   8.53   8.82   8.82    8.82   8.53   8.82  0.01  15:02:03
                # 002505  大康农业   2.91   2.86   2.99   2.89    2.91   2.90   2.99  0.02  15:02:03
                # 601939  建设银行   7.50   7.41   7.61   7.55    7.50   7.43   7.52  0.05  15:00:00
                # 600392  盛和资源  16.85  16.81  18.63  18.63   17.84  16.81  17.51  0.69  15:00:00 (11, 41)
                # 603676   卫信康  17.44  16.95  17.96  17.82   17.34  17.03  17.77  0.18  15:00:00
                if 'nstd' in df.columns:
                    df['stdv'] = map(lambda x, y: round(
                        x / y * 100, 1), df.nstd, df.open)

                # top_temp[:40][['nstd','stdv','name','volume','dff','percent']]
                # top_temp.loc['603363'][['nstd','stdv','name','volume','high','nhigh','percent','open','nclose']]

                # df['stdv'] = map(lambda x, y, z: round(z / (x / y * 100), 1), df.nstd, df.open, df.volume)

                # df.loc['002906'][['open','nclose','close','ncloseRatio','nopenRatio','low','nlow']]

                df = df[(df.low > df.upper) | (((df.nopenRatio <= df.nclose) & (df.low >= df.nlow) & (df.close >= df.ncloseRatio)) |
                                               ((df.nopenRatio <= df.nclose) & (df.close >= df.ncloseRatio) & (df.high >= df.nhigh)))]
                # else:
                # df = df[(((df.low >= df.nlow) & (df.close >= ncloseRatio)) | ((df.close >= ncloseRatio) & (df.close > nhighRatio)))]
            else:
                df = df[((df.low >= df.nlow) & (
                    df.close > df.llastp * ct.changeRatio))]
            # if 'nhigh' in df.columns and 'nclose' in df.columns:
            #     if cct.get_now_time_int() > ct.nlow_limit_time:
            #         df = df[(df.low >= df.nlow) & ((df.open > df.llastp * ct.changeRatio) & (df.nclose > df.llastp * ct.changeRatio)) &
            #                 (((df.low >= df.nlow) & (df.close >= df.nclose)) | ((df.close >= df.nclose) & (df.close > df.nhigh * ct.changeRatio) & (df.high >= df.nhigh)))]
            #     else:
            #         df = df[((df.open > df.llastp * ct.changeRatio) & (df.close > df.llastp * ct.changeRatio)) &
            #                 (((df.low >= df.nlow) & (df.close >= df.nclose)) | ((df.close >= df.nclose) & (df.close > df.nhigh * ct.changeRatio)))]
            # else:
            #     df = df[((df.low >= df.nlow) & (df.close > df.llastp))]

        if filter:

            if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 1000:
                df = df[((df.buy > df.llastp)) | (df.buy > df.hmax *
                                                  ct.changeRatio) | (df.buy < df.lmin * ct.changeRatioUp)]
                # df = df[(df.buy > df.hmax * ct.changeRatio) & (df.low > df.llastp)]
                # df = df[(df.buy > df.cmean * ct.changeRatioUp) | (df.open > df.llastp)]
                # df = df[df.buy > df.cmean]

            elif cct.get_now_time_int() > 1000 and cct.get_now_time_int() <= 1430:
                df = df[((df.buy > df.llastp)) | (df.buy > df.hmax *
                                                  ct.changeRatio) | (df.buy < df.lmin * ct.changeRatioUp)]
                # df = df[(df.buy > df.hmax * ct.changeRatio) | (df.low > df.llastp)]
                # df = df[(df.buy > df.hmax * ct.changeRatio) & (df.low > df.llastp)]

                # df = df[(df.buy > df.cmean * ct.changeRatioUp) | (df.open > df.llastp)]
                # df = df[df.buy > df.cmean]
            else:
                df = df[((df.buy > df.llastp)) | (df.buy > df.hmax *
                                                  ct.changeRatio) | (df.buy < df.lmin * ct.changeRatioUp)]

                # df = df[(df.buy > df.hmax * ct.changeRatio) | (df.low > df.llastp)]
                # df = df[(df.buy > df.hmax * ct.changeRatio) & (df.low > df.llastp)]

                # df = df[(df.buy > df.cmean * ct.changeRatioUp) | (df.open > df.llastp)]
                # df = df[df.buy > df.cmean]

            if 'vstd' in df.columns:
                # df = df[(df.lvol * df.volume > (df.vstd + df.lvol)) | ((df.percent > -10) & (df.hv / df.lv > 1.5))]
                # dd = df.loc['000760'] dd.hv/dd.lv,dd.volume
                df['hvRatio'] = map(lambda x, y: round(
                    x / y / cct.get_work_time_ratio(), 1), df.hv, df.lv)
                df['volRatio'] = (map(lambda x, y: round(
                    x / y / radio_t, 1), df.nvol.values, df.lv.values))

                # df = df[(df.lvol * df.volume > (df.vstd + df.lvol)) | ((df.percent > -5) & (df.hv / df.lv > 3))]

                # if 1000 < cct.get_now_time_int() < 1450:
                #     df = df[ (3 < df.ratio) & (df.ratio < 20)]
                if 'nclose' in df.columns:
                    # df = df[((df.hvRatio > df.volRatio) & ((df.buy > df.lastp) & (df.nclose > df.lastp))) | ((
                    df = df[(((df.buy > df.lastp) & (df.nclose > df.lastp))) | ((
                        (df.percent > -5) & ((df.vstd + df.lvol) * 1.2 < df.nvol) & (df.nvol > (df.vstd + df.lvol))))]
                else:
                    # df = df[((df.hvRatio > df.volRatio) & ((df.buy > df.lastp))) | ((
                    df = df[(((df.buy > df.lastp))) | ((
                        (df.percent > -5) & ((df.vstd + df.lvol) * 1.2 < df.nvol) & (df.nvol > (df.vstd + df.lvol))))]
                # [dd.lvol * dd.volume > (dd.vstd + dd.lvol) | dd.lvol * dd.volume >(dd.ldvolume + dd.vstd]
            # print df.loc['000801']

            if percent:
                pass
                '''
                if 'stdv' in df.columns and 926 < cct.get_now_time_int():
                    # df = df[((df.volume > 2 * cct.get_work_time_ratio()) & (df.percent > -3)) | ((df.stdv < 1) &
                    #                (df.percent > 2)) | ((df.lvolume > df.lvol * 0.9) & (df.lvolume > df.lowvol * 1.1))]
                    
                    df_index = tdd.getSinaIndexdf()
                    if isinstance(df_index, type(pd.DataFrame())):
                        df_index['volume'] = (map(lambda x, y: round(x / y / radio_t, 1), df_index.nvol.values, df_index.lastv1d.values))
                        index_vol = df_index.loc['999999'].volume
                        if 'percent' in df_index.columns and '999999' in df_index.index:
                            index_percent = df_index.loc['999999'].percent
                        else:
                            # import ipdb;ipdb.set_trace()
                            log.error("index_percent" is None)
                            index_percent = 0

                        index_boll = df_index.loc['999999'].boll
                        index_op = df_index.loc['999999'].op
                        # df = df[((df.percent > -3) | (df.volume > index_vol)) & (df.percent > index_percent)]
                        # df = df[((df.percent > -1) | (df.volume > index_vol * 1.5)) & (df.percent > index_percent)  & (df.boll >= index_boll)]
                        df = df[((df.percent > -1) | (df.volume > index_vol * 1.5)) & (df.percent > index_percent)]
                    else:
                        print ("df_index is Series",df_index.T)
                else:
                    df = df[((df.volume > 1.2 * cct.get_work_time_ratio()) & (df.percent > -3))]
                '''
                # df = df[((df['buy'] >= df['ene'])) | ((df['buy'] < df['ene']) & (df['low'] > df['lower'])) | ((df['buy'] > df['upper']) & (df['low'] > df['upper']))]
                # df = df[(( df['ene'] * ct.changeRatio < df['open']) & (df['buy'] > df['ene'] * ct.changeRatioUp)) | ((df['low'] > df['upper']) & (df['close'] > df['ene']))]

                # df = df[(( df['ene'] < df['open']) & (df['buy'] < df['ene'] * ct.changeRatioUp))]

                # df = df[(df.per1d > 9) | (df.per2d > 4) | (df.per3d > 6)]
                # df = df[(df.per1d > 0) | (df.per2d > 4) | (df.per3d > 6)]
            # time_ss=time.time()
            # codel = df.index.tolist()
            # dm = tdd.get_sina_data_df(codel)
            # results = cct.to_mp_run_async(getab.Get_BBANDS, codel,'d',5,duration,dm)
            # bolldf = pd.DataFrame(results, columns=['code','boll'])
            # bolldf = bolldf.set_index('code')
            # df = cct.combine_dataFrame(df, bolldf)
            # print "bollt:%0.2f"%(time.time()-time_ss),
            per3d_l = 2
            percent_l = -1
            op_l = 3
            # if 'boll' in df.columns:
            #     if 915 < cct.get_now_time_int() < 950:
            #         # df = df[(df.boll >= boll) | ((df.percent > percent_l) & (df.op > 4)) | ((df.percent > percent_l) & (df.per3d > per3d_l))]
            #         # df = df[((df.percent > percent_l) & (df.op > 4)) | ((df.percent > percent_l) & (df.per3d > per3d_l))]
            #         pass
            #     elif 950 < cct.get_now_time_int() < 1501:
            #         # df = df[(df.boll >= boll) | ((df.low <> 0) & (df.open == df.low) & (((df.percent > percent_l) & (df.op > op_l)) | ((df.percent > percent_l) & (df.per3d > per3d_l))))]
            #         # df = df[(df.boll >= boll) & ((df.low <> 0) & (df.open >= df.low *
            #         # ct.changeRatio) & (((df.percent > percent_l)) | ((df.percent >
            #         # percent_l) & (df.per3d > per3d_l))))]
            #         df = df[(df.boll >= boll)]
            #     # else:
            # df = df[(df.boll >= boll) | ((df.low <> 0) & (df.open == df.low) &
            # (((df.percent > percent_l) & (df.op > op_l)) | ((df.percent > percent_l)
            # & (df.per3d > per3d_l))))]

        # if 945 < cct.get_now_time_int() and market_key is None:
        #     df.loc[df.percent >= 9.94, 'percent'] = -10

    # else:
    #     # df['upper'] = map(lambda x: round((1 + 11.0 / 100) * x, 1), df.ma10d)
    #     # df['lower'] = map(lambda x: round((1 - 9.0 / 100) * x, 1), df.ma10d)
    #     # df['ene'] = map(lambda x, y: round((x + y) / 2, 1), df.upper, df.lower)
    #     # df = df[((df['buy'] >= df['ene'])) | ((df['buy'] < df['ene']) & (df['low'] > df['lower'])) | ((df['buy'] > df['upper']) & (df['low'] > df['upper']))]
    #     # df = df[(( df['ene'] * ct.changeRatio < df['open']) & (df['buy'] > df['ene'] * ct.changeRatioUp)) | ((df['low'] > df['upper']) & (df['close'] > df['ene']))]
    #     if 'nclose' in df.columns:
    #         # df = df[((df['nclose'] > df['ene'] * ct.changeRatio) & (df['percent'] > -3) & (df.volume > 1.5)) |
    #         #         ((df['nclose'] > df['upper'] * ct.changeRatio) & (df['buy'] > df['upper'] * ct.changeRatioUp)) | ((df['llastp'] > df['upper']) & (df['nclose'] > df['upper']))]
    #         df = df[(df.nclose > df.cmean)]
    #     else:
    #         df = df[(df.buy > df.cmean)]

    print("bo:%0.1f" % (time.time() - time_s)),

    df['ral']=(map(lambda x, y: round(
        (x + y) , 1) , df.percent, df.ral))
    # df['ra']=(map(lambda x, y: round(
    #     (x + y) , 1) , df.percent, df.ra))
    df['ra'] = df['ra'].apply(lambda x: int(x))
    return df

    # df = df[df.buy > df.cmean * ct.changeRatio]
    # else:
    #     df = df[df.buy > df.lmin]
    # ra * fibl + rah*fib +ma +kdj+rsi
#    time_s = time.time()
    # df['dff'] = (map(lambda x, y: round((x - y) / y * 100, 1), df['buy'].values, df['lastp'].values))
    # a = range(1,4)
    # b = range(3,6)
    # c = range(2,5)
    # (map(lambda ra,fibl,rah:(ra * fibl + rah),\
    #                      a,b,c ))

#    df['dff'] = (map(lambda ra, fibl,rah,:round(float(ra) * float(fibl) + float(rah),2),df['ra'].values, df['fibl'].values,df['rah'].values))

#    df['dff'] = (map(lambda ra, fibl,rah,fib,ma,kdj,rsi:round(ra * fibl + rah*fib +ma +kdj+rsi),\
#                         df['ra'].values, df['fibl'].astype(float).values,df['rah'].values,df['fib'].astype(float).values,df['ma'].values,\
#                         df['kdj'].values,df['rsi'].values))
    # df['diff2'] = df['dff'].copy()
    # pd.options.mode.chained_assignment = None
    # df.rename(columns={'dff': 'df2'}, inplace=True)
    # df['diff2'] = df['dff']

    # df['df2'] = (map(lambda ra, fibl,rah,fib,ma,kdj,rsi:round(eval(ct.powerdiff%(duration)),1),\
    #                      df['ra'].values, df['fibl'].values,df['rah'].values,df['fib'].values,df['ma'].values,\
    #                      df['kdj'].values,df['rsi'].values))


#    print "map time:%s"%(round((time.time()-time_s),2))
    # df.loc[:, ['fibl','op']] = df.loc[:, ['fibl','op']].astype(int)
    # df.loc[:, 'fibl'] = df.loc[:, 'fibl'].astype(int)

    # elif filter and cct.get_now_time_int() > 1015 and cct.get_now_time_int() <= 1445:
    #     df = df[((df.fibl < int(duration / 1.5)) &  (df.volume > 3)) | (df.percent > 3)]
    # print df
    # if 'ra' in df.columns and 'op' in df.columns:
    #     df = df[ (df.ma > 0 ) & (df.diff > 1) & (df.ra > 1) & (df.op >= 5) ]

def WriteCountFilter(df, op='op', writecount=ct.writeCount, end=None, duration=10):
    codel = []
    # market_value = cct.GlobalValues().getkey('market_value')
    # market_key = cct.GlobalValues().getkey('market_key')
    # if market_key == '2':
    #     market_value_perd = int(market_value) * 10
    if str(writecount) <> 'all':
        if end is None and int(writecount) > 0:
            if int(writecount) < 101 and len(df) > 0 and 'percent' in df.columns:
                codel = df.index[:int(writecount)].tolist()
                # market_value = cct.GlobalValues().getkey('market_value')
                # market_key = cct.GlobalValues().getkey('market_key')
                # if market_key == '2':
                #     # market_value_perd = int(market_value) * 9.8
                #     market_value_perd = 9.8
                #     dd=df[ df['per%sd'%(market_value)] > market_value_perd ]
                #     df_list=dd.index.tolist()
                #     for co in df_list:
                #         if co not in codel:
                #             codel.append(co)
            else:
                if len(str(writecount)) >= 4:
                    codel.append(str(writecount).zfill(6))
                else:
                    print "writeCount DF is None or Wri:%s" % (writecount)
        else:
            if end is None:
                writecount = int(writecount)
                if writecount > 0:
                    writecount -= 1
                codel.append(df.index.tolist()[writecount])
            else:
                writecount, end = int(writecount), int(end)

                if writecount > end:
                    writecount, end = end, writecount
                if end < -1:
                    end += 1
                    codel = df.index.tolist()[writecount:end]
                elif end == -1:
                    codel = df.index.tolist()[writecount::]
                else:
                    if writecount > 0 and end > 0:
                        writecount -= 1
                        end -= 1
                    codel = df.index.tolist()[writecount:end]
    else:
        if df is not None and len(df) > 0:
            codel = df.index.tolist()
    return codel
