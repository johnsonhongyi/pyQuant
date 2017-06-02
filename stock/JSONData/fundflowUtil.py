#-*- coding:utf-8 -*-

import re
import sys
import time
sys.path.append("..")
import JohhnsonUtil.commonTips as cct
import JohhnsonUtil.johnson_cons as ct
import JohhnsonUtil.LoggerFactory as LoggerFactory
import tdx_data_Day as tdd
from sina_data import *
# log = LoggerFactory.getLogger("FundFlow")
log = LoggerFactory.log
# log.setLevel(LoggerFactory.INFO)
# log.setLevel(LoggerFactory.DEBUG)
# from bs4 import BeautifulSoup
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
        data = cct.get_url_data_R(url)
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
            dd['zlr'] = round(float(data[5+i*25])/10000, 1)
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
            data = cct.get_url_data_R(url,timeout=20)
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
def get_dfcfw_fund_HGT(url=ct.DFCFW_FUND_FLOW_HGT):
    data = cct.get_url_data_R(url,timeout=15)
    "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=P.%28x%29,%28x%29,%28x%29|0000011|3990012|3990012,0000011,HSI5,BK07071,MK01461,MK01441,BK08041&sty=SHSTD|SZSTD|FCSHSTR&st=z&sr=&p=&ps=&cb=&js=var%20muXWEC=%28{data:[%28x%29]}%29&token=1942f5da9b46b069953c873404aad4b5"
    log.info("url:%s" % url)
    # vollist=re.findall('{data:(\d+)',code)
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


def get_dfcfw_fund_SHSZ(url=ct.DFCFW_ZS_SHSZ):
#    sina = Sina()
    dd = Sina().get_stock_code_data('999999,399001',index=True)
#    sh =  dd[dd.index == '000001']
    sh =  dd[dd.index == '999999']
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
                # print radio_t
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
            dd['svol'] = round(float(sh.turnover) / 100000000, 1)
            dd['zvol'] = round(float(sz.turnover) / 100000000, 1)
                # print data[3],data2[3]
            dd['scent'] = str(round((sh.close[0] - sh.llastp[0]) / sh.llastp[0] *100,2))+'%'
            dd['sup'] = round((sh.close[0] - sh.llastp[0]),2)
            dd['zcent'] = str(round((sz.close[0] - sz.llastp[0]) / sz.llastp[0] *100,2))+ '%'
            dd['zup'] = round((sz.close[0] - sz.llastp[0]),2)
            df = get_zs_VolRatio()
            if len(df['amount']) > 0:
                radio_t = cct.get_work_time_ratio()
                # print radio_t
                # print df.loc['999999','amount']
                # print type(dd['svol'])
                svol_r = round(
                    dd['svol'] / (df.loc['999999', 'amount'] / 10000000) / radio_t, 1)
                svol_v = round(
                    svol_r * (df.loc['999999', 'amount'] / 10000000), 1)
                zvol_r = round(
                    dd['zvol'] / (df.loc['399001', 'amount'] / 10000000) / radio_t, 1)
                zvol_v = round(
                    svol_r * (df.loc['399001', 'amount'] / 10000000), 1)
                dd['svol'] = "%s-%s-%s" % ((dd['svol'], svol_v, svol_r))
                dd['zvol'] = "%s-%s-%s" % ((dd['zvol'], zvol_v, zvol_r))
    return dd


def get_dfcfw_rzrq_SHSZ(url=ct.DFCFW_RZRQ_SHSZ):
    data = {}
    log.info("http://data.eastmoney.com/rzrq/total.html")

    def get_tzrq(url, today):
        url = url % today
        data = cct.get_url_data(url)
        # data = cct.get_url_data_R(url)
        # vollist=re.findall('{data:(\d+)',code)
        vol_l = re.findall('\"([\d\D]+?)\"', data)
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
    list = ['000001', '399001']
    # list=['000001','399001','399006','399005']
    df = tdd.get_tdx_all_day_LastDF(list, type=1)
    if not len(df) == len(list):
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
    # pp=get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
#    print get_dfcfw_rzrq_SHSZ(url=ct.DFCFW_RZRQ_SHSZ)
    print get_dfcfw_fund_SHSZ()
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
