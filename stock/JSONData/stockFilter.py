# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
from JohnsonUtil import commonTips as cct
import JohnsonUtil.johnson_cons as ct
from JSONData import powerCompute as pct
# from JSONData import tdx_data_Day as tdd
from JSONData import get_macd_kdj_rsi as getab
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


def getBollFilter(df=None, boll=6, duration=ct.PowerCountdl, filter=True, ma5d=True, dl=14, percent=False, resample='d'):

    # drop_cxg = cct.GlobalValues().getkey('dropcxg')
    # if len(drop_cxg) >0:
        # log.info("stf drop_cxg:%s"%(len(drop_cxg)))
        # drop_cxg = list(set(drop_cxg))
        # drop_t = [ co for co in drop_cxg if co in df.index]
        # if len(drop_t) > 0:
            # df = df.drop(drop_t,axis=0)top
            # log.error("stf drop_cxg:%s"%(len(drop_t)))
    if df is None:
        print "dataframe is None"
        return None
    else:
        df.loc[df.percent >= 9.94, 'percent'] = 10
        if resample == 'd':
            df.loc[df.per1d >= 9.94, 'per1d'] = 10
            df['percent'] = df['percent'].apply(lambda x: round(x, 1))
            # time_ss = time.time()
            perc_col = [co for co in df.columns if co.find('perc') > -1]
            per_col = [co for co in df.columns if co.find('per') > -1]
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
                df['perc_n'] = map(cct.func_compute_percd, df['close'], df['per%sd' % per1d], df['lastp%sd' %
                                                                                                 (nowd)], df['lasth%sd' % (nowd)], df['lastl%sd' % (nowd)], df['high'], df['low'])
            else:
                nowd, per1d = 1, 2
                # print  df['per%sd' % da+1], df['lastp%sd' % (da)], df['lasth%sd' % (da)], df['lastl%sd' % (da)], df['high'], df['low']
                df['perc_n'] = map(cct.func_compute_percd, df['close'], df['per%sd' % per1d], df['lastp%sd' %
                                                                                                 (nowd)], df['lasth%sd' % (nowd)], df['lastl%sd' % (nowd)], df['high'], df['low'])

            for co in perc_col:
                df[co] = (df[co] + df['perc_n']).map(lambda x: x)

            for co in per_col:
                df[co] = (df[co] + df['percent']).map(lambda x: x)
            # print "percT:%.2f"%(time.time()-time_ss)
    if 'fib' not in df.columns:
        df['fib'] = 0
    else:
        co2int = ['op', 'fibl']
        co2int.extend([co for co in df.columns.tolist() if co.startswith('perc') and co.endswith('d')])
        for co in co2int:
            df[co] = df[co].astype(int)

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
        log.info("stf market_key:%s"%(market_key))
        df = df[df["perc%sd"%(market_value)] >= market_value]
        # log.error("perc%sd"%(market_value))

    # df['df2'] = (map(lambda x, y, z: w=round((x - y) / z * 100, 1), df.high.values, df.low.values, df.llastp.values))
    # df['df2'] = (map(func_compute_df2, df.close.values, df.llastp.values,df.high.values, df.low.values,df.ratio.values))
    # df['df2'] = (map(func_compute_df2, df.close.values, df.llastp.values,df.high.values, df.low.values))

    if 'ma5d' in df.columns:
        if 'ma20d' in df.columns:
            df = df[(df.buy > df.ma20d) & (df.ma5d >= df.ma20d)]
        else:
            df = df[df.buy > df.ma5d * ct.changeRatio]

    # if 'nlow' in df.columns and 932 < cct.get_now_time_int() < 1030:

    if 'nlow' in df.columns and 945 < cct.get_now_time_int():
        # for col in ['nhigh', 'nclose', 'nlow','nstd']:
        #     df[col] = df[col].apply(lambda x: round(x, 2))
        if 'nhigh' in df.columns and 'nclose' in df.columns:
            if cct.get_now_time_int() > ct.nlow_limit_time:
                df = df[(df.low >= df.nlow) & ((df.open > df.llastp * ct.changeRatio) & (df.nclose > df.llastp * ct.changeRatio)) &
                        (((df.low >= df.nlow) & (df.close >= df.nclose)) | ((df.close >= df.nclose) & (df.close > df.nhigh * ct.changeRatio) & (df.high >= df.nhigh)))]
            else:
                df = df[((df.open > df.llastp * ct.changeRatio) & (df.close > df.llastp * ct.changeRatio)) &
                        (((df.low >= df.nlow) & (df.close >= df.nclose)) | ((df.close >= df.nclose) & (df.close > df.nhigh * ct.changeRatio)))]
        else:
            df = df[((df.low >= df.nlow) & (df.close > df.llastp))]

    if filter:

        if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 1000:
            df = df[df.buy > df.hmax * ct.changeRatio]
            # df = df[df.buy > df.cmean * ct.changeRatioUp ]
            # df = df[df.buy > df.cmean]

        elif cct.get_now_time_int() > 1000 and cct.get_now_time_int() <= 1430:
            df = df[df.buy > df.hmax * ct.changeRatio]
            # df = df[df.buy > df.cmean * ct.changeRatioUp]
            # df = df[df.buy > df.cmean]
        else:
            df = df[df.buy > df.hmax * ct.changeRatio]
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
            df = df[(df.lvol * df.volume > (df.vstd + df.lvol)) |
                    ((df.percent > -10) & (df.hv / df.lv > 1.2))]

            # df = df[(df.lvol * df.volume > (df.vstd + df.lvol)) | ((df.percent > -5) & (df.hv/df.lv > 3))]
            # [dd.lvol * dd.volume > (dd.vstd + dd.lvol) | dd.lvol * dd.volume >(dd.ldvolume + dd.vstd]
        # print df.loc['000801']

        if percent:
            if cct.get_now_time_int() > 930 and cct.get_now_time_int() <= 1400:
                df = df[(df.volume > 1.5 * cct.get_work_time_ratio())
                        | (df.percent > 0)]
            # df = df[(df.per1d > 9) | (df.per2d > 4) | (df.per3d > 6)]
            df = df[(df.per1d > 0) | (df.per2d > 4) | (df.per3d > 6)]
        # time_ss=time.time()
        # codel = df.index.tolist()
        # dm = tdd.get_sina_data_df(codel)
        # results = cct.to_mp_run_async(getab.Get_BBANDS, codel,'d',5,duration,dm)
        # bolldf = pd.DataFrame(results, columns=['code','boll'])
        # bolldf = bolldf.set_index('code')
        # df = cct.combine_dataFrame(df, bolldf)
        # print "bollt:%0.2f"%(time.time()-time_ss),
        per3d_l = 2
        percent_l = 0
        op_l = 3
        # if 'boll' in df.columns:
        #     if 915 < cct.get_now_time_int() < 926:
        #         # df = df[(df.boll >= boll) | ((df.percent > percent_l) & (df.op > 4)) | ((df.percent > percent_l) & (df.per3d > per3d_l))]
        #         # df = df[((df.percent > percent_l) & (df.op > 4)) | ((df.percent > percent_l) & (df.per3d > per3d_l))]
        #         pass
        #     elif 926 < cct.get_now_time_int() < 1501:
        #         df = df[(df.boll >= boll) | ((df.low <> 0) & (df.open == df.low) & (((df.percent > percent_l) & (df.op > op_l)) | ((df.percent > percent_l) & (df.per3d > per3d_l))))]
        #     else:
        # df = df[(df.boll >= boll) | ((df.low <> 0) & (df.open == df.low) &
        # (((df.percent > percent_l) & (df.op > op_l)) | ((df.percent > percent_l)
        # & (df.per3d > per3d_l))))]

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
                # dd = df[df.percent == 10]
                # df_list = dd.index.tolist()
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
