#-*- coding:utf-8 -*-

import re
import sys
sys.path.append("..")
import JohhnsonUtil.commonTips as cct
import JohhnsonUtil.johnson_cons as ct

def get_dfcfw_fund_flow(url):
    data = cct.get_url_data_R(url)
    # vollist=re.findall('{data:(\d+)',code)
    vol_l=re.findall('\"([\d\D]+?)\"',data)
    dd={}
    if len(vol_l)==2:
        data=vol_l[0].split(',')
        dd['zlr'] = round(float(data[0]), 1)
        dd['zzb'] = round(float(data[1]), 1)
        dd['sjlr'] = round(float(data[2]), 1)
        dd['sjzb'] = round(float(data[3]), 1)
        dd['time']=vol_l[1]
    else:
        print "Fund:is null%s"%url
    return dd

def get_dfcfw_fund_HGT(url):
    data = cct.get_url_data_R(url)
    # vollist=re.findall('{data:(\d+)',code)
    vol_l=re.findall('\"([\d\D]+?)\"',data)
    dd={}
    # print vol_l
    if len(vol_l)==1:
        data=vol_l[0].split(',')
        dd['ggt']=data[0]
        dd['hgt']=data[6]
        # dd['zzb']=data[1]
        # dd['sjlr']=data[2]
        # dd['sjzb']=data[3]
        # dd['time']=vol_l[1]
    else:
        print "Fund:Null%s %s"%(data,url)
    return dd

def get_dfcfw_fund_SHSZ(url):
    data = cct.get_url_data_R(url)
    # vollist=re.findall('{data:(\d+)',code)
    vol_l=re.findall('\"([\d\D]+?)\"',data)
    dd={}
    # print vol_l
    # print len(vol_l)
    if len(vol_l)==2:
        # for x in range(len(vol_l):
        data=vol_l[0].split(',')
        dd['svol']=round(float(data[3])/100000000,2)
        dd['scent']=data[5]
        dd['sup']=data[6].split('|')[0]
        data2=vol_l[1].split(',')
        dd['zvol']=round(float(data2[3])/100000000,2)
        dd['zcent']=data2[5]
        dd['zup']=data2[7].split('|')[0]
        # dd['zzb']=data[1]
        # dd['sjlr']=data[2]
        # dd['sjzb']=data[3]
        # dd['time']=vol_l[1]
    else:
        print "Fund:Null:%s url:%s"%(data,url)
    return dd


if __name__ == "__main__":
    ff = get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW['sh'])
    print "%.1f" % (float(ff['zzb']))
    print ff

    # pp=get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
    # for x in pp.keys():
    #     print pp[x]

    pp=get_dfcfw_fund_SHSZ(ct.DFCFW_ZS_SHSZ)
    print pp