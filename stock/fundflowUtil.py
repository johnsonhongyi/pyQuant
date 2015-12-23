#-*- coding:utf-8 -*-

import johnson_cons as ct
import singleAnalyseUtil as sl
import re

def get_dfcfw_fund_flow(url):
    data=sl.get_url_data(url)
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
    ff=get_dfcfw_fund_flow()
    print "%.1f"%(float(ff['zzb']))