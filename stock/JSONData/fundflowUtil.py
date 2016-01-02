#-*- coding:utf-8 -*-

import re

import stock.JohhnsonUtil.commonTips as cct
import stock.JohhnsonUtil.johnson_cons as ct

def get_dfcfw_fund_flow(url):
    data = cct.get_url_data(url)
    # vollist=re.findall('{data:(\d+)',code)
    vol_l=re.findall('\"([\d\D]+?)\"',data)
    dd={}
    if len(vol_l)==2:
        data=vol_l[0].split(',')
        dd['zlr']=data[0]
        dd['zzb']=data[1]
        dd['sjlr']=data[2]
        dd['sjzb']=data[3]
        dd['time']=vol_l[1]
    return dd







if __name__ == "__main__":
    ff = get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW['sh'])
    print "%.1f"%(float(ff['zzb']))