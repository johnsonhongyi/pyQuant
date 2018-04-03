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


def getBollFilter(df=None, boll=6, duration=ct.PowerCountdl, filter=True, ma5d=True, dl=14, percent=False, resample='d', ene=False,down=False,indexdff=True):

    # drop_cxg = cct.GlobalValues().getkey('dropcxg')
    # if len(drop_cxg) >0:
        # log.info("stf drop_cxg:%s"%(len(drop_cxg)))
        # drop_cxg = list(set(drop_cxg))
        # drop_t = [ co for co in drop_cxg if co in df.index]
        # if len(drop_t) > 0:
            # df = df.drop(drop_t,axis=0)top
            # log.error("stf drop_cxg:%s"%(len(drop_t)))
    time_s=time.time()
    df['upper'] = map(lambda x: round((1 + 11.0 / 100) * x, 1), df.ma10d)
    df['lower'] = map(lambda x: round((1 - 9.0 / 100) * x, 1), df.ma10d)
    df['ene'] = map(lambda x, y: round((x + y) / 2, 1), df.upper, df.lower)

    if df is None:
        print "dataframe is None"
        return None
    else:
        df.loc[df.percent >= 9.94, 'percent'] = 10
        if resample in ['d', 'w']:
            df.loc[df.per1d >= 9.94, 'per1d'] = 10
            df['percent'] = df['percent'].apply(lambda x: round(x, 1))
            # time_ss = time.time()
            perc_col = [co for co in df.columns if co.find('perc') == 0 ]
            per_col = [co for co in df.columns if co.find('per') == 0]
            # per_col = list(set(per_col) - set(perc_col) - set(['per1d', 'perlastp']))
            per_col = list(set(per_col) - set(perc_col) - set(['per1d', 'perlastp']))

            perc_col.remove('percent')
            # da, down_zero, down_dn, percent_l = 1, 0, 0, 2
            # da, down_zero, down_dn, percent_l = 1, 0, -1, 1
            # df['perc_n'] = map((lambda h, lh, l, ll, c, lc: (1 if (h - lh) > 0 else down_dn) + (1 if c - lc > 0 else down_dn) + (1 if (l - ll) > 0 else down_dn) + (2 if (c - lh) > 0 else down_zero) + (2 if (l - lc) > 0 else down_zero) + (0 if (h - lc) > 0 else down_dn)), df['high'], df['lasth%sd' % da], df['low'], df['lastl%sd' % da], df['close'],df['lastp%sd' % da])
            # df['perc_n'] = map((lambda c, lc: (1 if (c - lc) > 0 else down_zero) + (1 if (c - lc) / lc * 100 > 3 else down_zero) +
            # (down_dn if (c - lc) / lc * 100 < -3 else down_zero)), df['close'], df['lastp%sd' % da])
            
            idx_rnd = random.randint(0, len(df) - 10)

            # print "idx_rnd",idx_rnd,df.ix[idx_rnd].lastp0d ,df.ix[idx_rnd].close,df.ix[idx_rnd].lastp0d != df.ix[idx_rnd].close
            if cct.get_work_time() or df.ix[idx_rnd].lastp0d <> df.ix[idx_rnd].close:
                nowd, per1d = 0, 1
                if 'nlow' in df.columns:
                    df['perc_n'] = map(cct.func_compute_percd2, df['close'],df['llastp'],df['open'], df['lasth%sd' % (nowd)], df['lastl%sd' % (nowd)], df['nhigh'], df['nlow'])
                else:
                    df['perc_n'] = map(cct.func_compute_percd2, df['close'],df['llastp'],df['open'], df['lasth%sd' % (nowd)], df['lastl%sd' % (nowd)], df['high'], df['low'])
            else:
                nowd, per1d = 1, 2
                # print  df['per%sd' % da+1], df['lastp%sd' % (da)], df['lasth%sd' % (da)], df['lastl%sd' % (da)], df['high'], df['low']
                df['perc_n'] = map(cct.func_compute_percd2, df['close'],df['llastp'],df['open'], df['lasth%sd' % (nowd)], df['lastl%sd' % (nowd)], df['high'], df['low'])

            for co in perc_col:
                df[co] = (df[co] + df['perc_n']).map(lambda x: int(x))

            for co in per_col:
                df[co] = (df[co] + df['percent']).map(lambda x: int(x))

            # print "percT:%.2f"%(time.time()-time_ss)



    if 'fib' not in df.columns:
        df['fib'] = 0
    # else:

    co2int = ['boll','op','ratio','fib','fibl']
    co2int.extend([co for co in df.columns.tolist() if co.startswith('perc') and co.endswith('d')])
    for co in co2int:
        df[co] = df[co].astype(int)

    if down:
        if 'nlow' in df.columns:
            if 'max5' in df.columns:
                df = df[ (df.hmax >= df.ene) & (df.nlow >= df.low) & (df.low <> df.high) & (((df.low < df.hmax) & (df.high > df.cmean))  | (df.high > df.max5))]
            else:
                df = df[ (df.hmax >= df.ene) & (df.nlow >= df.low) & (df.low <> df.high) & (((df.low < df.hmax) & (df.high > df.cmean)))]
        else:
            df = df[ (df.hmax >= df.ene) & (df.low <> df.high) & (((df.low < df.hmax) & (df.close > df.cmean))  | (df.high > df.cmean))]
        return df

    if 'b1_v' in df.columns and 'nvol' in df.columns:
        df = df[(df.b1_v > 0) | (df.nvol > 0)]

    radio_t = cct.get_work_time_ratio()
    df['lvolr%s' % (resample)] = df['volume']
    df['volume'] = (map(lambda x, y: round(x / y / radio_t, 1), df.nvol.values, df.lvolume.values))

    if (cct.get_now_time_int() > 915 and cct.get_now_time_int() < 926):
        df['b1_v'] = df['volume']
    else:
        dd = df[df.percent < 10]
        dd['b1_v'] = dd['volume']
        df = cct.combine_dataFrame(df, dd.loc[:, ['b1_v']])
        # print "t:%0.2f"%(time.time()-time_ss)

    market_key = cct.GlobalValues().getkey('market_key')
    market_value = cct.GlobalValues().getkey('market_value')

    if market_key is not None and market_key == '3':

        market_value = int(market_value)
        log.info("stf market_key:%s" % (market_key))
        idx_k = cct.get_col_in_columns(df, 'perc%sd', market_value)
        df = df[df["perc%sd" % (idx_k)] >= idx_k]
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

    filter_up = 'ma5d'
    filter_dn = 'ma10d'
    if filter_up in df.columns:
        if filter_dn in df.columns:
            if market_key is not None and market_key == '3':
                df = df[ (df.buy >= df[filter_up])  & (df.buy * 1.02 >= df[filter_dn] * ct.changeRatio) ]
            else:
                df = df[(df.buy >= df[filter_up])]
        else:
            df = df[df.buy >= df[filter_up] * ct.changeRatio]

        # df = df[(df.lvolume > df.lvol * 0.9) & (df.lvolume > df.lowvol * 1.1)]

    # if 'nlow' in df.columns and 932 < cct.get_now_time_int() < 1030:
    
    if not ene:
#        df = df[ ((df.buy > df.ene) & (df['lvolr%s' % (resample)] > 1.2)) | ((df.buy > df.upper) & (df.nclose > df.cmean))]
        if 'nclose' in df.columns:
            # df = df[ ((df.buy > df.ene) ) | ((df.buy > df.upper) & ( df.nclose > df.cmean))]
            df = df[((df['nclose'] > df['ene'] * ct.changeRatio) & (df['percent'] > -3) & (df.volume > 1.5)) |
                               ((df['nclose'] > df['upper'] * ct.changeRatio) & (df['buy'] > df['upper'] * ct.changeRatioUp)) | ((df['llastp'] > df['upper']) & (df['nclose'] > df['upper']))]
        else:
            df = df[ ((df.buy > df.ene) ) | ((df.buy > df.upper) & (df.close > df.cmean))]
       


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
                    df['stdv'] = map(lambda x, y: round(x / y * 100, 1), df.nstd, df.open)

                # top_temp[:40][['nstd','stdv','name','volume','dff','percent']]
                # top_temp.loc['603363'][['nstd','stdv','name','volume','high','nhigh','percent','open','nclose']]

                # df['stdv'] = map(lambda x, y, z: round(z / (x / y * 100), 1), df.nstd, df.open, df.volume)

                # df.loc['002906'][['open','nclose','close','ncloseRatio','nopenRatio','low','nlow']]

                df = df[(df.low > df.upper) | (((df.nopenRatio <= df.nclose) & (df.low >= df.nlow) & (df.close >= df.ncloseRatio)) |
                         ((df.nopenRatio <= df.nclose) & (df.close >= df.ncloseRatio) & (df.high >= df.nhigh)))]
                # else:
                # df = df[(((df.low >= df.nlow) & (df.close >= ncloseRatio)) | ((df.close >= ncloseRatio) & (df.close > nhighRatio)))]
            else:
                df = df[((df.low >= df.nlow) & (df.close > df.llastp * ct.changeRatio))]
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

            # filter

            if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 1000:
                df = df[(df.buy > df.hmax * ct.changeRatio) | (df.buy < df.lmin * ct.changeRatioUp) | (df.per3d > 2)]
                # df = df[(df.buy > df.hmax * ct.changeRatio) & (df.low > df.llastp)]
                # df = df[(df.buy > df.cmean * ct.changeRatioUp) | (df.open > df.llastp)]
                # df = df[df.buy > df.cmean]

            elif cct.get_now_time_int() > 1000 and cct.get_now_time_int() <= 1430:
                df = df[(df.buy > df.hmax * ct.changeRatio) | (df.buy < df.lmin * ct.changeRatioUp) | (df.per3d > 2)]
                # df = df[(df.buy > df.hmax * ct.changeRatio) | (df.low > df.llastp)]
                # df = df[(df.buy > df.hmax * ct.changeRatio) & (df.low > df.llastp)]

                # df = df[(df.buy > df.cmean * ct.changeRatioUp) | (df.open > df.llastp)]
                # df = df[df.buy > df.cmean]
            else:
                df = df[(df.buy > df.hmax * ct.changeRatio) | (df.buy < df.lmin * ct.changeRatioUp) | (df.per3d > 5)]

                # df = df[(df.buy > df.hmax * ct.changeRatio) | (df.low > df.llastp)]
                # df = df[(df.buy > df.hmax * ct.changeRatio) & (df.low > df.llastp)]

                # df = df[(df.buy > df.cmean * ct.changeRatioUp) | (df.open > df.llastp)]
                # df = df[df.buy > df.cmean]

            # if ma5d:
            #     # op, ra, st, days = pct.get_linear_model_status('999999', filter='y', dl=dl, ptype='low')
            #     oph, rah, sth, daysh = pct.get_linear_model_status('999999', filter='y', dl=dl, ptype='high')
            #     # fibl = str(days[0])
            #     fibh = str(daysh[0])
            #     # if 1 < fibl < dl / 2 and fibh > dl / 3:
            #     if fibh > dl / 3:
            #         df = df[ ((df.ma5d * ct.changeRatio < df.low) & (df.low < df.ma5d * (2 - ct.changeRatio))) | ((df.percent > 1) & (df.volume > 3))]
            # print df.loc['000801']

            if 'vstd' in df.columns:
                # df = df[(df.lvol * df.volume > (df.vstd + df.lvol)) | ((df.percent > -10) & (df.hv / df.lv > 1.5))]
                # dd = df.loc['000760'] dd.hv/dd.lv,dd.volume
                df['hvRatio'] = map(lambda x, y: round(x / y / cct.get_work_time_ratio(), 1), df.hv, df.lv)
                df['volRatio'] = (map(lambda x, y: round(x / y / radio_t, 1), df.nvol.values, df.lv.values))

                # df = df[(df.lvol * df.volume > (df.vstd + df.lvol)) | ((df.percent > -5) & (df.hv / df.lv > 3))]

                # if 1000 < cct.get_now_time_int() < 1450:
                #     df = df[ (3 < df.ratio) & (df.ratio < 20)]
                if 'nclose' in df.columns:
                    # df = df[((df.hvRatio > df.volRatio) & ((df.buy > df.lastp) & (df.nclose > df.lastp))) | ((
                    df = df[( ((df.buy > df.lastp) & (df.nclose > df.lastp))) | ((
                        (df.percent > -5) & ((df.vstd + df.lvol) * 1.2 < df.nvol) & (df.nvol > (df.vstd + df.lvol))))]
                else:
                    # df = df[((df.hvRatio > df.volRatio) & ((df.buy > df.lastp))) | ((
                    df = df[( ((df.buy > df.lastp))) | ((
                        (df.percent > -5) & ((df.vstd + df.lvol) * 1.2 < df.nvol) & (df.nvol > (df.vstd + df.lvol))))]
                # [dd.lvol * dd.volume > (dd.vstd + dd.lvol) | dd.lvol * dd.volume >(dd.ldvolume + dd.vstd]
            # print df.loc['000801']

            if percent:
                # if cct.get_now_time_int() > 930 and cct.get_now_time_int() <= 1430:
                #     df = df[(df.volume > 1.5 * cct.get_work_time_ratio()) & (df.percent > -5)]
                # df = df[(df.lvolume > df.lvol * 0.9) & (df.lvolume > df.lowvol * 1.1)]
                if 'stdv' in df.columns and 926 < cct.get_now_time_int():
                    df = df[((df.volume > 2 * cct.get_work_time_ratio()) & (df.percent > -3)) | ((df.stdv < 1) &
                                                                                                 (df.percent > 2)) | ((df.lvolume > df.lvol * 0.9) & (df.lvolume > df.lowvol * 1.1))]
                    df_index = tdd.getSinaIndexdf()
                    df_index['volume'] = (map(lambda x, y: round(x / y / radio_t, 1), df_index.nvol.values, df_index.lvolume.values))
                    index_vol = df_index.loc['999999'].volume
                    index_percent = df_index.loc['999999'].percent
                    # df = df[((df.percent > -3) | (df.volume > index_vol)) & (df.percent > index_percent)]
                    df = df[((df.percent > -3) | (df.volume > index_vol)) & (df.percent > index_percent)]

                else:
                    df = df[((df.volume > 1.2 * cct.get_work_time_ratio()) & (df.percent > -3))
                            | ((df.lvolume > df.lvol * 0.8) & (df.lvolume > df.lowvol * 1.1))]



                # df = df[((df['buy'] >= df['ene'])) | ((df['buy'] < df['ene']) & (df['low'] > df['lower'])) | ((df['buy'] > df['upper']) & (df['low'] > df['upper']))]
                # df = df[(( df['ene'] * ct.changeRatio < df['open']) & (df['buy'] > df['ene'] * ct.changeRatioUp)) | ((df['low'] > df['upper']) & (df['close'] > df['ene']))]
                

                # import ipdb;ipdb.set_trace()

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
            if 'boll' in df.columns:
                if 915 < cct.get_now_time_int() < 950:
                    # df = df[(df.boll >= boll) | ((df.percent > percent_l) & (df.op > 4)) | ((df.percent > percent_l) & (df.per3d > per3d_l))]
                    # df = df[((df.percent > percent_l) & (df.op > 4)) | ((df.percent > percent_l) & (df.per3d > per3d_l))]
                    pass
                elif 950 < cct.get_now_time_int() < 1501:
                    # df = df[(df.boll >= boll) | ((df.low <> 0) & (df.open == df.low) & (((df.percent > percent_l) & (df.op > op_l)) | ((df.percent > percent_l) & (df.per3d > per3d_l))))]
                    # df = df[(df.boll >= boll) & ((df.low <> 0) & (df.open >= df.low *
                    # ct.changeRatio) & (((df.percent > percent_l)) | ((df.percent >
                    # percent_l) & (df.per3d > per3d_l))))]
                    df = df[(df.boll >= boll)]
                # else:
            # df = df[(df.boll >= boll) | ((df.low <> 0) & (df.open == df.low) &
            # (((df.percent > percent_l) & (df.op > op_l)) | ((df.percent > percent_l)
            # & (df.per3d > per3d_l))))]

        # if 945 < cct.get_now_time_int() and market_key is None:
        #     df.loc[df.percent >= 9.94, 'percent'] = -10

    else:
        # df['upper'] = map(lambda x: round((1 + 11.0 / 100) * x, 1), df.ma10d)
        # df['lower'] = map(lambda x: round((1 - 9.0 / 100) * x, 1), df.ma10d)
        # df['ene'] = map(lambda x, y: round((x + y) / 2, 1), df.upper, df.lower)
        # df = df[((df['buy'] >= df['ene'])) | ((df['buy'] < df['ene']) & (df['low'] > df['lower'])) | ((df['buy'] > df['upper']) & (df['low'] > df['upper']))]
        # df = df[(( df['ene'] * ct.changeRatio < df['open']) & (df['buy'] > df['ene'] * ct.changeRatioUp)) | ((df['low'] > df['upper']) & (df['close'] > df['ene']))]
        if 'nclose' in df.columns:
            # df = df[((df['nclose'] > df['ene'] * ct.changeRatio) & (df['percent'] > -3) & (df.volume > 1.5)) |
            #         ((df['nclose'] > df['upper'] * ct.changeRatio) & (df['buy'] > df['upper'] * ct.changeRatioUp)) | ((df['llastp'] > df['upper']) & (df['nclose'] > df['upper']))]
            df = df[(df.nclose > df.cmean)]
        else:
            df = df[(df.buy > df.cmean)]
    print ("bo:%0.1f"%(time.time()-time_s)),
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
    if str(writecount) <> 'all':
        if end is None and int(writecount) > 0:
            if int(writecount) < 100 and len(df) > 0 and 'percent' in df.columns:
                codel = df.index[:int(writecount)].tolist()
                # dd=df[df.percent == 10]
                # df_list=dd.index.tolist()
                # for co in df_list:
                #     if co not in codel:
                #         codel.append(co)
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
        codel = df.index.tolist()
    return codel
