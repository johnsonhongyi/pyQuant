# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
from JohhnsonUtil import commonTips as cct
import JohhnsonUtil.johnson_cons as ct
import time
def getBollFilter(df=None,boll=1,duration=14):
    #return boll > int
    if df is None:
        print "dataframe is None"
        return None
    else:
        df.loc[df.percent>=9.9,'percent']=10
    if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 945:
        df = df[df.buy > df.hmax * ct.changeRatio]
    elif cct.get_now_time_int() > 945 and cct.get_now_time_int() <= 1445:
        df = df[df.buy > df.cmean * ct.changeRatio]
    # else:
    #     df = df[df.buy > df.lmin]
    # ra * fibl + rah*fib +ma +kdj+rsi
#    time_s = time.time()
    # df['diff'] = (map(lambda x, y: round((x - y) / y * 100, 1), df['buy'].values, df['lastp'].values))
    # a = range(1,4)
    # b = range(3,6)
    # c = range(2,5)
    # (map(lambda ra,fibl,rah:(ra * fibl + rah),\
    #                      a,b,c ))

#    df['diff'] = (map(lambda ra, fibl,rah,:round(float(ra) * float(fibl) + float(rah),2),df['ra'].values, df['fibl'].values,df['rah'].values))

#    df['diff'] = (map(lambda ra, fibl,rah,fib,ma,kdj,rsi:round(ra * fibl + rah*fib +ma +kdj+rsi),\
#                         df['ra'].values, df['fibl'].astype(float).values,df['rah'].values,df['fib'].astype(float).values,df['ma'].values,\
#                         df['kdj'].values,df['rsi'].values))
    df['diff2'] = df['diff']
    df['diff'] = (map(lambda ra, fibl,rah,fib,ma,kdj,rsi:round(ra * fibl + rah*(abs(duration-fibl))/fib +ma +kdj+rsi),\
                         df['ra'].values, df['fibl'].astype(float).values,df['rah'].values,df['fib'].astype(float).values,df['ma'].values,\
                         df['kdj'].values,df['rsi'].values))
#    print "map time:%s"%(round((time.time()-time_s),2))
    if 'ma5d' in df.columns:
        df = df[df.buy > df.ma5d * ct.changeRatio]
    if 'boll' in df.columns:
        return df[df.boll >= boll]
    else:
        print "boll not in columns"
        df['boll'] = 0
        return df

def WriteCountFilter(df,op='op'):
    codel = []
    if len(df) > 0 and 'percent' in df.columns:
        dd =  df[df.percent == 10]
        if op=='op' and len(dd) > ct.writeCount:
            codel = dd.index.tolist()
        else:
            codel = df.index[:ct.writeCount].tolist()
    else:
        print "writeCount DF is None"
    return codel