#-*- coding:utf-8 -*-

import re
import sys
import time
sys.path.append("..")
import JohnsonUtil.commonTips as cct
import JohnsonUtil.johnson_cons as ct
import JohnsonUtil.LoggerFactory as LoggerFactory
import tdx_data_Day as tdd
from sina_data import *
# log = LoggerFactory.getLogger("FundFlow")
log = LoggerFactory.log
# log.setLevel(LoggerFactory.INFO)
# log.setLevel(LoggerFactory.DEBUG)
# from bs4 import BeautifulSoup


sinaheader = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Host': 'vip.stock.finance.sina.com.cn',
            'Referer':'http://vip.stock.finance.sina.com.cn',
            'Connection': 'keep-alive',
            }
def get_dfcfw_fund_flow_old(market):
    if market.startswith('http'):
        single = True
        url = market
    else:
        single = False
        url = ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW[market]
        log.info("url:%s"%(url))
    data = cct.get_url_data_R(url)
    # vollist=re.findall('{data:(\d+)',code)
    vol_l = re.findall('\"([\d\D]+?)\"', data)
    dd = {}
    if len(vol_l) == 2:
        data = vol_l[0].split(',')
        dd['zlr'] = round(float(data[0]), 1)
        dd['zzb'] = round(float(data[1]), 1)
        dd['sjlr'] = round(float(data[2]), 1)
        dd['sjzb'] = round(float(data[3]), 1)
        dd['time'] = vol_l[1]
    else:
        dd['zlr'] = 0.0
        dd['zzb'] = 0.0
        dd['sjlr'] = 0.0
        dd['sjzb'] = 0.0
        dd['time'] = 0.0
        log.error("Fund_f NO Url:%s" % url)
    if not single:
        url = ct.SINA_JSON_API_URL % ct.INDEX_LIST[market]
        data = cct.get_url_data_R(url,headers=sinaheader)
        vol_l = re.findall('\"([\d\D]+?)\"', data)
        if len(vol_l) == 1:
            data = vol_l[0].split(',')
            try:
                dd['open'] = round(float(data[1]), 2)
                dd['lastp'] = round(float(data[2]), 2)
                dd['close'] = round(float(data[3]), 2)
                dd['high'] = round(float(data[4]), 2)
                dd['low'] = round(float(data[5]), 2)
                dd['vol'] = round(float(data[8]) / 100000, 1)
                dd['amount'] = round(float(data[9]) / 100000000, 1)
            except Exception, e:
                print e
                return dd
            else:
                pass
            finally:
                pass

        # 1592652100,32691894461
        # 215722046, 207426675004
    return dd


def get_dfcfw_fund_flow(market):
    #outdata 
    indexall = ['sh','sz','cyb']
    if market.startswith('http'):
        single = True
        url = market
    else:
        single = False
        if market == "all":
            indexcode = ct.SINA_Market_KEY_TO_DFCFW_New['sh']+','+ct.SINA_Market_KEY_TO_DFCFW_New['sz']+','+ct.SINA_Market_KEY_TO_DFCFW_New['cyb']
        else:
            indexall = [market]
            indexcode = ct.SINA_Market_KEY_TO_DFCFW_New[market]
        url = ct.DFCFW_FUND_FLOW_URL_New % indexcode
        log.info("url:%s"%(url))
    data = cct.get_url_data_R(url,timeout=20).split('=')
    # vollist=re.findall('{data:(\d+)',code)
    # vol_l = []
    if len(data) > 1:
        # vol_l = re.findall('\"([\d\D]+?)\"', data[1])
        data_s = data[1].replace("\"","")
    else:
        data_s = ''
        # data_s = data[1]
    dk = {}
    start_inx = 0
    for i in range(len(indexall)):
        dd = {}
        # start_inx = start_inx + i * 24
        # end_inx = start_inx + (i+1)*24
        if len(data_s) > 0:
            data = data_s.split(',')

            dd['zlr'] = round(float(data[5+i*25] if data[5+i*25] != '-' else 0)/10000, 1)
            dd['zzb'] = round(float(data[23+i*25].replace("%","")), 1)
            dd['sjlr'] = round(float(data[9+i*25])/10000, 1)
            dd['sjzb'] = round(float(data[10+i*25].replace("%","")), 1)
            dd['time'] = data[24+i*25].split(" ")[1][:5]
            # print dd['time']
        else:
            dd['zlr'] = 0.0
            dd['zzb'] = 0.0
            dd['sjlr'] = 0.0
            dd['sjzb'] = 0.0
            dd['time'] = 0.0
            log.error("Fund_f NO Url:%s" % url)
        if not single:
            url = ct.SINA_JSON_API_URL % ct.INDEX_LIST[indexall[i]]
            data = cct.get_url_data_R(url,timeout=20,headers=sinaheader)
            vol_l = re.findall('\"([\d\D]+?)\"', data)
            if len(vol_l) == 1:
                data = vol_l[0].split(',')
                try:
                    dd['open'] = round(float(data[1]), 2)
                    dd['lastp'] = round(float(data[2]), 2)
                    dd['close'] = round(float(data[3]), 2)
                    dd['high'] = round(float(data[4]), 2)
                    dd['low'] = round(float(data[5]), 2)
                    dd['vol'] = round(float(data[8]) / 100000, 1)
                    dd['amount'] = round(float(data[9]) / 100000000, 1)
                except Exception, e:
                    print e
                    return dd
                else:
                    pass
                finally:
                    pass
        dk[indexall[i]] = dd
                # 1592652100,32691894461
                # 215722046, 207426675004
    return dk


def get_dfcfw_fund_flow2020(market):
    indexall = ['sh','sz','cyb']
    url = ''
    if market == "all":
        single = False
        url = ct.DFCFW_FUND_FLOW_URL_2020All
    else:
        log.error("market is not all")
    log.info("url:%s"%(url))
    data = cct.get_url_data_R(url,timeout=20).split('=')
    # vollist=re.findall('{data:(\d+)',code)
    # vol_l = []

    if len(data) > 0:
        # vol_l = re.findall('\"([\d\D]+?)\"', data[1])
        # ['jQuery18308448273886036106_1606189025852({"rc":0,"rt":11,"svr":182994506,"lt":1,"full":1,\
        # "data":{"total":3,"diff":[{"f62":-9060049408.0,"f184":-4.05},{"f62":-9359993344.0,"f184":-3.16},{"f62":-3487613184.0,"f184":-3.08}]}});']
        data_s = eval(re.findall('{[\d\D]*}', data[0])[0])
        data_s = data_s['data']['diff']
    else:
        data_s = ''
        # data_s = data[1]
    dk = {}
    start_inx = 0
    for i in range(len(indexall)):
        dd = {}
        # start_inx = start_inx + i * 24
        # end_inx = start_inx + (i+1)*24

        if len(data_s) > 0:
            data = (data_s[i])
            # [{'f184': -4.05, 'f62': -9060049408.0}, \
            # {'f184': -3.16, 'f62': -9359993344.0}, {'f184': -3.08, 'f62': -3487613184.0}]
            dd['zlr'] = round(float(data['f62'])/1000/1000/100, 1)
            dd['zzb'] = round(float(data['f184']), 1)
            dd['sjlr'] = 0
            dd['sjzb'] = 0
            dd['time'] = cct.get_now_time_int()

            # dd['zlr'] = round(float(data[5+i*25] if data[5+i*25] != '-' else 0)/10000, 1)
            # dd['zzb'] = round(float(data[23+i*25].replace("%","")), 1)
            # dd['sjlr'] = round(float(data[9+i*25])/10000, 1)
            # dd['sjzb'] = round(float(data[10+i*25].replace("%","")), 1)
            # dd['time'] = data[24+i*25].split(" ")[1][:5]
            # print dd['time']
        else:
            dd['zlr'] = 0.0
            dd['zzb'] = 0.0
            dd['sjlr'] = 0.0
            dd['sjzb'] = 0.0
            dd['time'] = 0.0
            log.error("Fund_f NO Url:%s" % url)
        if not single:
            url = ct.SINA_JSON_API_URL % ct.INDEX_LIST[indexall[i]]
            data = cct.get_url_data_R(url,timeout=20,headers=sinaheader)
            vol_l = re.findall('\"([\d\D]+?)\"', data)
            if len(vol_l) == 1:
                data = vol_l[0].split(',')
                try:
                    dd['open'] = round(float(data[1]), 2)
                    dd['lastp'] = round(float(data[2]), 2)
                    dd['close'] = round(float(data[3]), 2)
                    dd['high'] = round(float(data[4]), 2)
                    dd['low'] = round(float(data[5]), 2)
                    dd['vol'] = round(float(data[8]) / 100000, 1)
                    dd['amount'] = round(float(data[9]) / 100000000, 1)
                except Exception, e:
                    print e
                    return dd
                else:
                    pass
                finally:
                    pass
        dk[indexall[i]] = dd
                # 1592652100,32691894461
                # 215722046, 207426675004
    return dk

def get_dfcfw_fund_HGT(url=ct.DFCFW_FUND_FLOW_HGSZT2021):
    data = cct.get_url_data_R(url,timeout=15)
    # "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=P.%28x%29,%28x%29,%28x%29|0000011|3990012|3990012,0000011,HSI5,BK07071,MK01461,MK01441,BK08041&sty=SHSTD|SZSTD|FCSHSTR&st=z&sr=&p=&ps=&cb=&js=var%20muXWEC=%28{data:[%28x%29]}%29&token=1942f5da9b46b069953c873404aad4b5"
    "http://push2.eastmoney.com/api/qt/kamt/get?fltt=2&fields1=f1,f3&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery112308976712127389186_1628752728202&_=1628752728203"
    log.info("url:%s" % url)

    # vollist=re.findall('{data:(\d+)',code)
    # re.findall('"data":{[\D\d]+.', data)[0]
    # re.findall('"data":{[\D\d]+.', data)[0].replace("});",'')
    vol_l = re.findall('\"([\d\D]+?)\"', data)
    dd = {}
    # print vol_l
    if len(vol_l) == 1:
        data = vol_l[0].split(',')
        log.info("D0:%s" % data[0])
        log.debug("hgt:%s" % re.findall(r'([\d.]+)([\u4e00-\u9fa5]+)', data[0].decode('utf8')))
        dd['ggt'] = data[0].decode('utf8')
        dd['hgt'] = data[6].decode('utf8')
        # dd['zzb']=data[1]
        # dd['sjlr']=data[2]
        # dd['sjzb']=data[3]
        # dd['time']=vol_l[1]
    else:
        # print "Fund:Null%s %s"%(data,url)
        log.info("Fund_f NO Url:%s" % url)
    return dd

HGZS_LIST = {'bei': ['hk2sh','hk2sz'],'nan': ['sh2hk','sz2hk']}

# url=ct.DFCFW_FUND_FLOW_HGSZT2021   http://data.eastmoney.com/hsgtcg/ http://data.eastmoney.com/hsgtcg/lz.html
HGZS_URL_LIST = {'bei':"http://push2.eastmoney.com/api/qt/kamt/get?fltt=2&fields1=f1,f3&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery112308976712127389186_1628752728202&_=1628752728203",
        'nan':"http://push2.eastmoney.com/api/qt/kamt/get?fltt=2&fields1=f2,f4&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery1123011359186010295064_1628755572432&_=1628755572433"}

def get_dfcfw_fund_HGSZ2021(market='bei'):
    data = cct.get_url_data_R(HGZS_URL_LIST[market],timeout=15)
    # "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=P.%28x%29,%28x%29,%28x%29|0000011|3990012|3990012,0000011,HSI5,BK07071,MK01461,MK01441,BK08041&sty=SHSTD|SZSTD|FCSHSTR&st=z&sr=&p=&ps=&cb=&js=var%20muXWEC=%28{data:[%28x%29]}%29&token=1942f5da9b46b069953c873404aad4b5"
    #beixiang
    "http://push2.eastmoney.com/api/qt/kamt/get?fltt=2&fields1=f1,f3&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery112308976712127389186_1628752728202&_=1628752728203"
    #nanxiang
    # "http://push2.eastmoney.com/api/qt/kamt/get?fltt=2&fields1=f2,f4&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery1123011359186010295064_1628755572432&_=1628755572433"
    log.info("url:%s" % HGZS_URL_LIST[market])

    # vollist=re.findall('{data:(\d+)',code)
    # re.findall('"data":{[\D\d]+.', data)[0]
    # re.findall('"data":{[\D\d]+.', data)[0].replace("});",'')

    data_ = re.findall('"data":{[\D\d]+.', data)[0].replace("});",'').replace('"data":','')

    js_data = json.loads(data_)
    dd = {}

    # [u'hk2sz', u'hk2sh']
    if len(js_data) == 2:
        # hg2sh = js_data['hk2sh']

        dd['hgt'] = round(js_data[HGZS_LIST[market][0]]['dayNetAmtIn']/10000,2)
        dd['ggt'] = round(js_data[HGZS_LIST[market][1]]['dayNetAmtIn']/10000,2)

        # dd['zzb']=data[1]
        # dd['sjlr']=data[2]
        # dd['sjzb']=data[3]
        # dd['time']=vol_l[1]
    else:
        # print "Fund:Null%s %s"%(data,url)
        log.info("Fund_f NO Url:%s" % url)
    return dd

def get_dfcfw_fund_SHSZ(url=ct.DFCFW_ZS_SHSZ):
#    sina = Sina()
    dd = Sina().get_stock_code_data('999999,399001',index=True)

#    sh =  dd[dd.index == '000001']
    if 'amount' not in dd.columns:
        if 'turnover' in dd.columns:
            dd.rename(columns={'turnover': 'amount'}, inplace=True)
    sh =  dd[dd.index == '999999']
    if len(sh) >0 and not sh.name.values[0] == '上证指数':
        log.error('sh data is error')
    sz = dd[dd.index == '399001']
    if len(sh) == 0 or len(sz) == 0:
        data = cct.get_url_data_R(url,timeout=15)
        log.info("url:%s"%(url))
        # vollist=re.findall('{data:(\d+)',code)
        vol_l = re.findall('\"([\d\D]+?)\"', data)
        dd = {}
        # print vol_l
        # print len(vol_l)
        if len(vol_l) == 2:
            # for x in range(len(vol_l):
            data = vol_l[0].split(',')
            data2 = vol_l[1].split(',')
            # print data[3],data2[3],len(data[3]),len(data2[3])
            if len(data[3]) > 2 and len(data2[3]) > 2 :
                dd['svol'] = round(float(data[3]) / 100000000, 1)
                dd['zvol'] = round(float(data2[3]) / 100000000, 1)
            else:
                dd['svol'] = data[3]
                dd['zvol'] = data2[3]
                # print data[3],data2[3]
            dd['scent'] = data[5]
            dd['sup'] = data[6].split('|')[0]
            dd['zcent'] = data2[5]
            dd['zup'] = data2[7].split('|')[0]
            df = get_zs_VolRatio()
            if len(df['amount']) > 0:
                radio_t = cct.get_work_time_ratio()
                # print df.loc['999999','amount']
                # print type(dd['svol'])
                log.debug("type:%s radio_t:%s" % (type(dd['svol']), radio_t))
                if isinstance(dd['svol'], str) and dd['svol'].find('-') == 0:
                    log.info("svol:%s" % dd['svol'])
                else:
                    svol_r = round(
                        dd['svol'] / (df.loc['999999', 'amount'] / 10000000) / radio_t, 1)
                    svol_v = round(
                        svol_r * (df.loc['999999', 'amount'] / 10000000), 1)
                    zvol_r = round(
                        dd['zvol'] / (df.loc['399001', 'amount'] / 10000000) / radio_t, 1)
                    zvol_v = round(
                        svol_r * (df.loc['399001', 'amount'] / 10000000), 1)
                    dd['allvol'] = "%s-%s-%s" % (dd['svol']+dd['zvol'], svol_v+zvol_v, round((svol_r+zvol_r)/2,1))
                    dd['svol'] = "%s-%s-%s" % ((dd['svol'], svol_v, svol_r))
                    dd['zvol'] = "%s-%s-%s" % ((dd['zvol'], zvol_v, zvol_r))
            # dd['zzb']=data[1]
            # dd['sjlr']=data[2]
            # dd['sjzb']=data[3]
            # dd['time']=vol_l[1]

        else:
            log.info("Fund_f NO Url:%s" % url)
    else:
        dd = {}
        # print vol_l
        # print len(vol_l)
        #var C1Cache={quotation:["0000011,上证指数,3113.18,121762623488,4.41,0.14%,463|197|656|143,536|280|1187|217","3990012,
        #深证成指,9816.71,145863270400,-10.08,-0.10%,463|197|656|143,536|280|1187|217"]}
        if len(sh) == 1 and len(sz) == 1:
            dd['svol'] = round(float(sh.amount) / 100000000, 1)
            dd['zvol'] = round(float(sz.amount) / 100000000, 1)
                # print data[3],data2[3]
            dd['scent'] = str(round((sh.close[0] - sh.llastp[0]) / sh.llastp[0] *100,2))+'%'
            dd['sup'] = round((sh.close[0] - sh.llastp[0]),2)
            dd['zcent'] = str(round((sz.close[0] - sz.llastp[0]) / sz.llastp[0] *100,2))+ '%'
            dd['zup'] = round((sz.close[0] - sz.llastp[0]),2)
            df = get_zs_VolRatio()
            if len(df['amount']) > 0:
                radio_t = cct.get_work_time_ratio()
                # print type(dd['svol'])
                svol_r = round(
                    dd['svol'] / (df.loc['999999', 'amount'] / 100000000) / radio_t, 1)
                svol_v = round(
                    svol_r * (df.loc['999999', 'amount'] / 100000000), 1)
                zvol_r = round(
                    dd['zvol'] / (df.loc['399001', 'amount'] / 100000000) / radio_t, 1)
                zvol_v = round(
                    svol_r * (df.loc['399001', 'amount'] / 100000000), 1)
                dd['allvol'] = "%s-%s-%s" % (dd['svol']+dd['zvol'], svol_v+zvol_v, round((svol_r+zvol_r)/2,1))
                dd['svol'] = "%s-%s-%s" % ((dd['svol'], svol_v, svol_r))
                dd['zvol'] = "%s-%s-%s" % ((dd['zvol'], zvol_v, zvol_r))
    return dd


# global rzrqCount
# rzrqCount = 1

def get_dfcfw_rzrq_SHSZ2(url=ct.DFCFW_RZYE2sh):
    data = {}
    log.info("rzrq:%s"%(url))
    dd = pd.DataFrame()
    # rzdata = cct.get_url_data(url)
    #shrzrq2
    rzdata = cct.get_url_data_R(ct.DFCFW_RZYE2sh)
    # rzdata = rzdata.replace('var HIoUWbQY=','')
    # rz_dic = re.findall('{"result"[\D\d]+?}', rzdata.encode('utf8'))
    rz_dic = re.findall('{"result":[\D\d]+.', rzdata.encode('utf8'))[0]
    rz_dic = rz_dic.replace(';', '')
    # ct.DFCFW_RZYE2sh
    rzdata_dic=json.loads(rz_dic)
    rzdata_list=(rzdata_dic['result']['data'])
    df=pd.DataFrame(rzdata_list,columns=ct.dfcfw_rzye_columns2sh)
    # ['DIM_DATE','RZYEZB', 'RQCHL10D', 'RQCHL3D', 'RQYE', 'RQMCL', 'RQYL', 'R]
    # df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
    # rz_dic = re.findall('{"tdate"[\D\d]+?}', rzdata.encode('utf8'))
    df.rename(columns={'DIM_DATE': 'tdate'}, inplace=True)
    # RZYE->rzye_hs rzye_h none rzye_h none
    df.rename(columns={'RZYE': 'sh'}, inplace=True)
    # df.rename(columns={'rzye_h': 'sh'}, inplace=True)
    # df.rename(columns={'rzye_h': 'sz'}, inplace=True)
    df.tdate=df.tdate.apply(lambda x: x[:10])
    df = df.set_index('tdate')
    dd = df.loc[:,['sh']]




    #szrzrq
    rzdata = cct.get_url_data_R(ct.DFCFW_RZYE2sz)
    # rzdata = rzdata.replace('var HIoUWbQY=','')
    # rz_dic = re.findall('{"result"[\D\d]+?}', rzdata.encode('utf8'))
    rz_dic = re.findall('{"result":[\D\d]+.', rzdata.encode('utf8'))[0]
    rz_dic = rz_dic.replace(';', '')

    # ct.DFCFW_RZYE2sh
    rzdata_dic=json.loads(rz_dic)
    rzdata_list=(rzdata_dic['result']['data'])
    df=pd.DataFrame(rzdata_list,columns=ct.dfcfw_rzye_columns2sh)
    # ['DIM_DATE','RZYEZB', 'RQCHL10D', 'RQCHL3D', 'RQYE', 'RQMCL', 'RQYL', 'R]
    # df.index = pd.to_datetime(df.index,format='%Y-%m-%d')

    # rz_dic = re.findall('{"tdate"[\D\d]+?}', rzdata.encode('utf8'))
    df.rename(columns={'DIM_DATE': 'tdate'}, inplace=True)
    # RZYE->rzye_hs rzye_h none rzye_h none
    df.rename(columns={'RZYE': 'sz'}, inplace=True)
    # df.rename(columns={'rzye_h': 'sh'}, inplace=True)
    # df.rename(columns={'rzye_h': 'sz'}, inplace=True)
    df.tdate=df.tdate.apply(lambda x: x[:10])
    df = df.set_index('tdate')
    dd = cct.combine_dataFrame(dd,df.loc[:,['sz']])
    df = dd

    df['sh'] = df['sh'].apply(lambda x:round((float(x)/1000/1000/100),2))
    df['sz'] = df['sz'].apply(lambda x:round((float(x)/1000/1000/100),2))
    df['all'] = map(lambda x, y: round(
                x+y, 1), df.sh.values, df.sz.values)
    # data=get_tzrq(url,today)
    # yestoday = cct.last_tddate(1)
    # log.debug(today)
    # beforeyesterday =  cct.last_tddate(days=2)

    def get_days_data(days=1,df=None):
            rzrq_status = 1
            # data=''
            da = 0
            i = 0
            data2 = ''
            while rzrq_status:
                for x in range(days, 10):
                    yestoday = cct.last_tddate(x)
                    if yestoday in df.index:
                        data2 = df.loc[yestoday]
                        # log.info("yestoday:%s data:%s" % (yestoday, data2))
                        break
                        # print da
                    else:
                        log.error("%s:None" % (yestoday))
                rzrq_status = 0
            return data2
            
    data1 = get_days_data(1,df)
    data2 = get_days_data(2,df)
    
    # data = df.loc[yestoday]
    # data2 = df.loc[beforeyesterday]
    # log.info("data1:%s,data2:%s", data1, data2)
    if len(data2) > 0:
        # print data1
        data['all'] = round(data1.loc['all'], 2)
        data['sh'] = round(data1.loc['sh'], 2)
        data['sz'] = round(data1.loc['sz'], 2)
        data['dff'] = round(data1.loc['all'] - data2.loc['all'], 2)
        data['shrz'] = round(data1.loc['sh'] - data2.loc['sh'], 2)
        data['szrz'] = round(data1.loc['sz'] - data2.loc['sz'], 2)
    else:
        log.error("df.index:%s"%(df.index.values[0]))
        data['dff'] = 'error'
        data['all'] = 0
        data['sh'] = 0
        data['sz'] = 0
        data['shrz'] = 0
        data['szrz'] = 0
    if len(data) == 0:
        log.error("Fund_f NO Url:%s" % url)

    return data


def get_dfcfw_rzrq_SHSZ2_(url=ct.DFCFW_RZYE2):
    #all back
    data = {}
    log.info("rzrq:%s"%(ct.DFCFW_RZYE))

    # rzdata = cct.get_url_data(url)
    rzdata = cct.get_url_data_R(url)

    # ct.DFCFW_RZYE2
    rzdata_dic=json.loads(rzdata)
    rzdata_list=(rzdata_dic['result']['data'])
    df=pd.DataFrame(rzdata_list,columns=ct.dfcfw_rzye_columns2)
    # ['DIM_DATE','RZYEZB', 'RQCHL10D', 'RQCHL3D', 'RQYE', 'RQMCL', 'RQYL', 'R]
    # df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
    df.rename(columns={'DIM_DATE': 'tdate'}, inplace=True)
    # RZYE->rzye_hs rzye_h none rzye_h none
    df.rename(columns={'RZYE': 'all'}, inplace=True)
    # df.rename(columns={'rzye_h': 'sh'}, inplace=True)
    # df.rename(columns={'rzye_h': 'sz'}, inplace=True)
    df.tdate=df.tdate.apply(lambda x: x[:10])
    df = df.set_index('tdate')

    import ipdb;ipdb.set_trace()

    # ct.DFCFW_RZYE
    # rzdata = rzdata.replace(':"-"',':0.1')
    # rz_dic = re.findall('{"tdate"[\D\d]+?}', rzdata.encode('utf8'))
    # rzdict=[eval(x) for x in rz_dic ]
    # df=pd.DataFrame(rzdict,columns=ct.dfcfw_rzye_columns)
    # df.tdate=df.tdate.apply(lambda x: x[:10])
    # df = df.set_index('tdate')
    # # df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
    # df.rename(columns={'rzye_hs': 'all'}, inplace=True)
    # df.rename(columns={'rzye_h': 'sh'}, inplace=True)
    # df.rename(columns={'rzye_s': 'sz'}, inplace=True)



    df['all'] = df['all'].apply(lambda x:round((x/1000/1000/100),2))
    df['sh'] = df['sh'].apply(lambda x:round((x/1000/1000/100),2))
    df['sz'] = df['sz'].apply(lambda x:round((x/1000/1000/100),2))
    # data=get_tzrq(url,today)
    # yestoday = cct.last_tddate(1)
    # log.debug(today)
    # beforeyesterday =  cct.last_tddate(days=2)

    def get_days_data(days=1,df=None):
            rzrq_status = 1
            # data=''
            da = 0
            i = 0
            data2 = ''
            while rzrq_status:
                for x in range(days, 20):
                    yestoday = cct.last_tddate(x)
                    if yestoday in df.index:
                        data2 = df.loc[yestoday]
                        # log.info("yestoday:%s data:%s" % (yestoday, data2))
                        break
                        # print da
                    else:
                        log.error("%s:None" % (yestoday))
                rzrq_status = 0
            return data2
            
    data1 = get_days_data(1,df)
    data2 = get_days_data(2,df)
    
    # data = df.loc[yestoday]
    # data2 = df.loc[beforeyesterday]
    # log.info("data1:%s,data2:%s", data1, data2)
    if len(data2) > 0:
        # print data2
        print data1
        data['all'] = round(data1.loc['all'], 2)
        data['sh'] = round(data1.loc['sh'], 2)
        data['sz'] = round(data1.loc['sz'], 2)
        data['dff'] = round(data1.loc['all'] - data2.loc['all'], 2)
        data['shrz'] = round(data1.loc['sh'] - data2.loc['sh'], 2)
        data['szrz'] = round(data1.loc['sz'] - data2.loc['sz'], 2)
    else:
        log.error("df.index:%s"%(df.index.values[0]))
        data['dff'] = 'error'
        data['all'] = 0
        data['sh'] = 0
        data['sz'] = 0
        data['shrz'] = 0
        data['szrz'] = 0
    if len(data) == 0:
        log.error("Fund_f NO Url:%s" % url)
    return data

def get_dfcfw_rzrq_SHSZ(url=ct.DFCFW_RZYE):
    data = {}
    log.info("rzrq:%s"%(ct.DFCFW_RZYE))

    # rzdata = cct.get_url_data(url)
    # rzdata = cct.get_url_data_R(url,timeout=10)
    rzdata = cct.get_url_data(url,timeout=10)


    rz_dic = re.findall('"data":([\D\d]+.}])', rzdata.encode('utf8'))[0]
    # rz_dic = rz_dic.replace(';', '')

    # ct.DFCFW_RZYE2sh
    rzdata_dic=json.loads(rz_dic)
    
    df=pd.DataFrame(rzdata_dic,columns=ct.dfcfw_rzye_col2022)
   

    # rzdata_list=(rzdata_dic['result']['data'])
    # df=pd.DataFrame(rzdata_list,columns=ct.dfcfw_rzye_col2022)


    # rzdata = rzdata.replace(':"-"',':0.1')
    # rz_dic = re.findall('{"tdate"[\D\d]+?}', rzdata.encode('utf8'))
    
    # rzdict=[eval(x) for x in rz_dic ]
    # df=pd.DataFrame(rzdict,columns=ct.dfcfw_rzye_columns)
    # df.tdate=df.tdate.apply(lambda x: x[:10])
    # df = df.set_index('tdate')
    # df.index = pd.to_datetime(df.index,format='%Y-%m-%d')
    # df.rename(columns={'rzye_hs': 'all'}, inplace=True)
    # df.rename(columns={'rzye_h': 'sh'}, inplace=True)
    # df.rename(columns={'rzye_s': 'sz'}, inplace=True)

    df.rename(columns={'RZYE': 'all'}, inplace=True)
    df.rename(columns={'H_RZYE': 'sh'}, inplace=True)
    df.rename(columns={'H_RQYL': 'sz'}, inplace=True)
    df['DIM_DATE'] = df['DIM_DATE'].apply(lambda x:x[:10])
    df=df.set_index('DIM_DATE')

    df['all'] = df['all'].apply(lambda x:round((x/1000/1000/100),2))
    df['sh'] = df['sh'].apply(lambda x:round((x/1000/1000/100),2))
    df['sz'] = df['sz'].apply(lambda x:round((x/1000/1000/1),2))
    # data=get_tzrq(url,today)
    # yestoday = cct.last_tddate(1)
    # log.debug(today)
    # beforeyesterday =  cct.last_tddate(days=2)

    def get_days_data(days=1,df=None):
            rzrq_status = 1
            # data=''
            da = 0
            i = 0
            data2 = ''
            while rzrq_status:
                for x in range(days, 20):
                    yestoday = cct.last_tddate(x)
                    if yestoday in df.index:
                        data2 = df.loc[yestoday]
                        # log.info("yestoday:%s data:%s" % (yestoday, data2))
                        break
                        # print da
                    else:
                        log.error("%s:None" % (yestoday))
                rzrq_status = 0
            return data2



    
    # data = df.loc[yestoday]
    # data2 = df.loc[beforeyesterday]
    # log.info("data1:%s,data2:%s", data1, data2)
    if len(df) > 0:
        data1 = get_days_data(1,df)
        data2 = get_days_data(2,df)
        # print data1
        data['all'] = round(data1.loc['all'], 2)
        data['sh'] = round(data1.loc['sh'], 2)
        data['sz'] = round(data1.loc['sz'], 2)
        data['dff'] = round(data1.loc['all'] - data2.loc['all'], 2)
        data['shrz'] = round(data1.loc['sh'] - data2.loc['sh'], 2)
        data['szrz'] = round(data1.loc['sz'] - data2.loc['sz'], 2)
    else:
        log.debug("df is None:%s"%(url))
        data['dff'] = 'error'
        data['all'] = 0
        data['sh'] = 0
        data['sz'] = 0
        data['shrz'] = 0
        data['szrz'] = 0
    if len(data) == 0:
        log.error("Fund_f NO Url:%s" % url)
    return data


def get_dfcfw_rzrq_SHSZ_Outdate(url=ct.DFCFW_RZRQ_SHSZ):
    data = {}
    log.info("http://data.eastmoney.com/rzrq/total.html")
    ct.DFCFW_RZYE
    def get_tzrq(url, today):
        global rzrqCount
        url = url % today
        if rzrqCount < 3:
            data = cct.get_url_data(url)
            # data = cct.get_url_data_R(url)
            if len(data) < 1:
                rzrqCount +=1
                vol_l =[]
            # vollist=re.findall('{data:(\d+)',code)
            else:
                vol_l = re.findall('\"([\d\D]+?)\"', data)
        else:
            vol_l = []
        # print vol_l
        dd = {}
        # print vol_l
        # print len(vol_l)
        if len(vol_l) == 3:
            data = vol_l[0].split(',')
            data2 = vol_l[1].split(',')
            dataall = vol_l[2].split(',')
            dd['sh'] = round(
                float(data[5]) / 100000000, 1) if len(data[5]) > 0 else 0
            dd['sz'] = round(
                float(data2[5]) / 100000000, 1) if len(data2[5]) > 0 else 0
            dd['all'] = round(
                float(dataall[5]) / 100000000, 1) if len(dataall[5]) > 0 else 0
        return dd

    def get_days_data(days=1):
        rzrq_status = 1
        # data=''
        da = 0
        i = 0
        while rzrq_status:
            for x in range(days, 20):
                yestoday = cct.last_tddate(x).replace('-', '/')
                data2 = get_tzrq(url, yestoday)
                log.info("yestoday:%s data:%s" % (yestoday, data2))
                if len(data2) > 0:
                    i += 1
                    # if da ==days and days==0:
                    # i +=1
#                    if i >= days-1:
                    break
                    # elif da > days:
                        # break
                # else:    da+=1
                    # print da
                else:
                    log.info("%s:%s" % (yestoday, data2))
            rzrq_status = 0
        return data2

    # today=cct.last_tddate().replace('-','/')
    # data=get_tzrq(url,today)
    data = get_days_data(1)
    # log.debug(today)
    data2 = get_days_data(2)
    log.info("data:%s,data2:%s", data, data2)
    if len(data2) > 0:
        # print data2
        data['dff'] = round(data['all'] - data2['all'], 2)
        data['shrz'] = round(data['sh'] - data2['sh'], 2)
        data['szrz'] = round(data['sz'] - data2['sz'], 2)
    else:
        data['dff'] = 'error'
    if len(data) == 0:
        log.info("Fund_f NO Url:%s" % url)
    return data


def get_zs_VolRatio():
    ilist = ['999999', '399001']
    # list=['000001','399001','399006','399005']
    df = tdd.get_tdx_all_day_LastDF(ilist)
    if not len(df) == len(ilist):
        return ''
    return df


def get_lhb_dd(retry_count=3, pause=0.001):
    # symbol = _code_to_symbol(code)
    lhburl = 'http://data.eastmoney.com/stock/tradedetail.html'
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            ct._write_console()
            html_doc = cct.get_url_data_R(lhburl)
            # print html_doc
            # page = urllib2.urlopen()
            # html_doc = page.read()
            # print (html_doc)
            # soup = BeautifulSoup(html_doc,fromEncoding='gb18030')
            # print html_doc
            # pageCount = re.findall('fillCount\"\]\((\d+)', html_doc, re.S)
            # if len(pageCount) > 0:
                # start_t = time.time()
                # pageCount = pageCount[0]
                # if int(pageCount) > 100:
                    # if int(pageCount) > 10000:
                        # print "BigBig:", pageCount
                        # pageCount = '10000'

                    # print "AllBig:", pageCount
                    # html_doc = urllib2.urlopen(get_sina_url(vol, type, pageCount=pageCount)).read()
                    # print (time.time() - start_t)

            soup = BeautifulSoup(html_doc, "lxml")
            # print (time.time() - start_t)
            abc = (soup.find_all('table', type="tab1"))
            # abc= (soup.find_all('h101',type="class"))
             # <thead class="h101">
            print(len(abc))
            # print (abc[4].text).strip().find('window["fillCount"]')
            # print abc[4].contents

            # pageCount= soup.find_all(string=re.compile('fillCount\"\]\((\d+)'))
            # pageCount=re.findall('(\d+)',pageCount[0])

            # sys.exit(0)
            # print soup.find_all('__stringHtmlPages')

            sys.exit(0)

            # soup = BeautifulSoup(html_doc.decode('gb2312','ignore'))
            # print soup.find_all('div', id="divListTemplate")
            # for i in soup.find_all('tr',attrs={"class": "gray"."class":""}):
            # alldata = {}
            # dict_data = {}
            # print soup.find_all('div',id='divListTemplate')

            row = soup.find_all('div', id='divListTemplate')
            sdata = []
            if len(row) >= 1:
                '''
                colums:CHN name

                '''
                # firstCells = row[0].find('tr')
                # th_cells = firstCells.find_all('th')
                # td_cells = firstCells.find_all('td')
                # m_name=th_cells[0].find(text=True)
                # m_code=th_cells[1].find(text=True)
                # m_time=th_cells[2].find(text=True)
                # m_status=th_cells[3].find(text=True)
                # m_detail=th_cells[4].find(text=True)
                # m_price=td_cells[0].find(text=True)
                # m_vol=td_cells[1].find(text=True)
                # m_pre_p=td_cells[2].find(text=True)
                # print "m_name:",m_name,m_pre_p
                for tag in row[0].find_all('tr', attrs={"class": True}):
                    # print tag
                    th_cells = tag.find_all('th')
                    td_cells = tag.find_all('td')
                    m_name = th_cells[0].find(text=True)
                    m_code = th_cells[1].find(text=True)
                    m_time = th_cells[2].find(text=True)
                    # m_detail=(th_cells[4]).find('a')["href"]   #detail_url
                    m_price = td_cells[0].find(text=True)
                    m_vol = float(
                        td_cells[1].find(text=True).replace(',', '')) * 100
                    m_pre_p = td_cells[2].find(text=True)
                    m_status_t = th_cells[3].find(text=True)
                    if m_status_t in status_dict.keys():
                        m_status = status_dict[m_status_t]
                        # print m_status
                    sdata.append({'code': m_code, 'time': m_time, 'vol': m_vol, 'price': m_price, 'pre_p': m_pre_p,
                                  'status': m_status, 'name': m_name})
                    # sdata.append({'code':m_code,'time':m_time,'vol':m_vol,'price':m_price,'pre_p':m_pre_p,'detail':m_detail,'status':m_status,'name':m_name})
                    # print sdata
                    # print m_name
                    # break
            # pd = DataFrame(sdata,columns=['code','time','vol','price','pre_p','detail','status','name'])
            df = DataFrame(
                sdata, columns=['code', 'time', 'vol', 'price', 'pre_p', 'status', 'name'])
            # for row in soup.find_all('tr',attrs={"class":"gray","class":""}):
        except Exception as e:
            print "Except:", (e)
            import traceback
            traceback.print_exc()
        else:
            return df
        # raise IOError(ct.NETWORK_URL_ERROR_MSG.decode('utf8').encode('gbk'))

def dfcf_yyb_data():
    url = 'http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/YYBJXMX/GetYYBJXMX?tkn=eastmoney&salesCode=80035417&tdir=&dayNum=&startDateTime=2016-03-22&endDateTime=2017-03-22&sortfield=&sortdirec=1&pageNum=1&pageSize=50&cfg=yybjym'


if __name__ == "__main__":
    # ff = get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW['sh'])
    # print "%.1f" % (float(ff['zzb']))
    # print ff
    #
#    pp=get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
    log.setLevel(LoggerFactory.DEBUG)
    # print get_dfcfw_rzrq_SHSZ(url=ct.DFCFW_RZRQ_SHSZ)
    # print get_dfcfw_rzrq_SHSZ2_()
    rzrq = get_dfcfw_rzrq_SHSZ()
    print rzrq
    # rzrq2 = get_dfcfw_rzrq_SHSZ2()
    # print rzrq2
    # import ipdb;ipdb.set_trace()
    print get_dfcfw_fund_HGSZ2021()
    print get_dfcfw_fund_HGSZ2021('nan')
    indexKeys = [ 'sh','sz', 'cyb']
    ffindex = get_dfcfw_fund_flow2020('all')
    # ffindex = get_dfcfw_fund_flow('all')
    print ffindex
    # print get_dfcfw_fund_SHSZ()
    print "hgt:",get_dfcfw_fund_HGT()
    print "szt:",get_dfcfw_fund_HGT(url=ct.DFCFW_FUND_FLOW_SZT)
    sys.exit(0)
    # for x in pp.keys():
    # print pp[x]
    #get_dfcfw_fund_HGT
    print get_dfcfw_fund_HGT(url=ct.DFCFW_FUND_FLOW_HGT)
    print get_dfcfw_fund_HGT(url=ct.DFCFW_FUND_FLOW_SZT)
    # print get_dfcfw_fund_flow('sz')
    print get_dfcfw_fund_flow('all')
    # print dd
    # print get_dfcfw_fund_SHSZ()
    # print df

    # get_lhb_dd()

    # pp=get_dfcfw_fund_SHSZ(ct.DFCFW_ZS_SHSZ)
    # print pp
    # print get_zs_VolRatio()
    # a='abc'
    # print isinstance(a,str)

    # pp=get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
    # for x in pp.keys():
    #     print pp[x]
