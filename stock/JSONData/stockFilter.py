# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
from JohhnsonUtil import commonTips as cct
import JohhnsonUtil.johnson_cons as ct
from JSONData import powerCompute as pct
import pandas as pd
from JohhnsonUtil import LoggerFactory
log = LoggerFactory.log
import time


def getBollFilter(df=None, boll=6, duration=ct.PowerCountdl, filter=True, ma5d=True, dl=14, percent=False, resample='d'):

    # drop_cxg = cct.GlobalValues().getkey('dropcxg')
    # if len(drop_cxg) >0:
        # log.info("stf drop_cxg:%s"%(len(drop_cxg)))
        # drop_cxg = list(set(drop_cxg))
        # drop_t = [ co for co in drop_cxg if co in df.index]
        # if len(drop_t) > 0:
            # df = df.drop(drop_t,axis=0)
            # log.error("stf drop_cxg:%s"%(len(drop_t)))
    if df is None:
        print "dataframe is None"
        return None
    else:
        df.loc[df.percent >= 9.94, 'percent'] = 10
        if resample == 'd':
            df.loc[df.per1d >= 9.94, 'per1d'] = 10
            df['percent'] = df['percent'].apply(lambda x:round(x,1))
    radio_t = cct.get_work_time_ratio()
    df['lvolr%s'%(resample)] = df['volume']
    df['volume'] = (map(lambda x, y: round(x / y / radio_t, 1), df.nvol.values, df.lvolume.values))
            
    if 'ma5d' in df.columns:
        df = df[df.buy > df.ma5d * ct.changeRatio]

    if filter:

        if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 1000:
            # df = df[df.buy > df.cmean * ct.changeRatioUp ]
            df = df[df.buy > df.hmax * ct.changeRatio]

        elif cct.get_now_time_int() > 1000 and cct.get_now_time_int() <= 1430:
            df = df[df.buy > df.cmean]
        else:
            df = df[df.buy > df.hmax * ct.changeRatio]

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
            # df = df[df.oph > 10]
        if 'boll' in df.columns:
            if 915 < cct.get_now_time_int() < 926:
                df = df[(df.boll >= boll) | ((df.percent > 6) & (df.op > 4)) | ((df.per3d > 6) & (df.op > 4))]

            elif 926 < cct.get_now_time_int() < 1501:
                df = df[(df.boll >= boll) | ((df.low <> 0) & (df.open == df.low) & (((df.percent > 6) & (df.op > 4)) | ((df.per3d > 6) & (df.op > 4))))]

            else:
                df = df[(df.boll >= boll) | ((df.low <> 0) & (df.open == df.low) & (((df.percent > 6) & (df.op > 4)) | ((df.per3d > 6) & (df.op > 4))))]

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
            writecount = int(writecount)
            if writecount < 100 and len(df) > 0 and 'percent' in df.columns:
                codel = df.index[:writecount].tolist()
                dd = df[df.percent == 10]
                df_list = dd.index.tolist()
                for co in df_list:
                    if co not in codel:
                        codel.append(co)
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
