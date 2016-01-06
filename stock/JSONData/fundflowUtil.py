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
        dd['zlr']=data[0]
        dd['zzb']=data[1]
        dd['sjlr']=data[2]
        dd['sjzb']=data[3]
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
'var zjlx_detail="1,BK0707,8161420,-7933677,28635070464,-25143861760,52979125760,-54192905984,58718659584,-60057660928,42739257600,-43677684480,227742.85,349120.87,-121378.02,-133900.13,-93842.69,1.24%,1.90%,-0.66%,-0.73%,-0.51%,2016-01-06 15:22:09"'
'var quote_zjl={rank:["14.40亿元,90.60亿元,105亿元,1,1416.00亿元,2500亿元,-4.97亿元,134.97亿元,130亿元,1,1795.70亿元,3000亿元"],pages:1}'

'var C1Cache={quotation:["0000011,上证指数,3361.84,285243224064,74.13,2.25%,1003|91|31|86,1535|194|62|185","3990012,深证成指,11724.88,414256857088,256.82,2.24%,1003|91|31|86,1535|194|62|185"]}'



if __name__ == "__main__":
    # ff = get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW['sh'])
    # print "%.1f"%(float(ff['zzb']))
    
    # pp=get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
    # for x in pp.keys():
    #     print pp[x]

    pp=get_dfcfw_fund_SHSZ(ct.DFCFW_ZS_SHSZ)
    print pp