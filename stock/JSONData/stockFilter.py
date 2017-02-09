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
    if cct.get_now_time_int() > 915 and cct.get_now_time_int() <= 1445:
        df = df[df.buy > df.hmax * ct.changeRatio]
    # elif cct.get_now_time_int() > 945 and cct.get_now_time_int() <= 1100:
    #     df = df[df.buy > df.cmean * ct.changeRatio]
    # else:
    #     df = df[df.buy > df.lmin]
    if 'boll' in df.columns:
        return df[df.boll >= boll]
    else:
        print "boll not in columns"
        df['boll'] = 0
        return df
