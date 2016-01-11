#-*- coding:utf-8 -*-

import re
import sys
sys.path.append("..")
import JohhnsonUtil.commonTips as cct
import JohhnsonUtil.johnson_cons as ct
import JohhnsonUtil.LoggerFactory as LoggerFactory
import tdx_data_Day as tdd
log = LoggerFactory.getLogger("FundFlow")
# log.setLevel(LoggerFactory.DEBUG)

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
        log.info("D0:%s"%data[0])
        log.debug("hgt:%s"%re.findall(ur'([\d.]+)([\u4e00-\u9fa5]+)',data[0].decode('utf8')))
        dd['ggt']=data[0].decode('utf8')
        dd['hgt']=data[6].decode('utf8')
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
        data2=vol_l[1].split(',')
        if len(data[3]) >2:
            dd['svol']=round(float(data[3])/100000000,1)
            dd['zvol']=round(float(data2[3])/100000000,1)
        else:
            dd['svol']=data[3]
            dd['zvol']=data2[3]
            # print data[3],data2[3]
        dd['scent']=data[5]
        dd['sup']=data[6].split('|')[0]
        dd['zcent']=data2[5]
        dd['zup']=data2[7].split('|')[0]
        df=get_zs_VolRatio()
        if len(df['amount'])>0:
            radio_t = cct.get_work_time_ratio()
            # print radio_t
            # print df.loc['999999','amount']
            # print type(dd['svol'])
            log.debug("type:%s"%type(dd['svol']))
            if isinstance(dd['svol'],str) and dd['svol'].find('-')==0:
                log.info("svol:%s"%dd['svol'])
            else:
                dd['svol']="%s->%s"%((dd['svol'],round(dd['svol']/(df.loc['999999','amount']/10000000)/radio_t,1)))
                dd['zvol']="%s->%s"%((dd['zvol'],round(dd['zvol']/(df.loc['399001','amount']/10000000)/radio_t,1)))
        # dd['zzb']=data[1]
        # dd['sjlr']=data[2]
        # dd['sjzb']=data[3]
        # dd['time']=vol_l[1]

    else:
        print "Fund:Null:%s url:%s"%(data,url)
    return dd

def get_zs_VolRatio():
    list=['000001','399001']
    # list=['000001','399001','399006','399005']
    df = tdd.get_tdx_all_day_LastDF(list,type=1)
    if not len(df)==len(list):
        return ''
    return df

if __name__ == "__main__":
    # ff = get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW['sh'])
    # print "%.1f" % (float(ff['zzb']))
    # print ff
    #
    # # pp=get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
    # # for x in pp.keys():
    # #     print pp[x]
    #
    pp=get_dfcfw_fund_SHSZ(ct.DFCFW_ZS_SHSZ)
    print pp
    print get_zs_VolRatio()
    a='abc'
    print isinstance(a,str)
    # pp=get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
    # for x in pp.keys():
    #     print pp[x]