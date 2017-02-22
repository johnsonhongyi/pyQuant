# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
from JohhnsonUtil import commonTips as cct
import JohhnsonUtil.johnson_cons as ct
def getBollFilter(df=None,boll=1):
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