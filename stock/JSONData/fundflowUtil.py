#-*- coding:utf-8 -*-

import re
import sys,time
sys.path.append("..")
import JohhnsonUtil.commonTips as cct
import JohhnsonUtil.johnson_cons as ct
import JohhnsonUtil.LoggerFactory as LoggerFactory
import tdx_data_Day as tdd
log = LoggerFactory.getLogger("FundFlow")
# log.setLevel(LoggerFactory.DEBUG)
import traceback
from bs4 import BeautifulSoup

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
        log.info("Fund_f NO Url:%s"%url)
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
        # print "Fund:Null%s %s"%(data,url)
        log.info("Fund_f NO Url:%s"%url)
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
            log.debug("type:%s radio_t:%s"%(type(dd['svol']),radio_t))
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
        log.info("Fund_f NO Url:%s"%url)
    return dd

def get_zs_VolRatio():
    list=['000001','399001']
    # list=['000001','399001','399006','399005']
    df = tdd.get_tdx_all_day_LastDF(list,type=1)
    if not len(df)==len(list):
        return ''
    return df

    
def get_lhb_dd(retry_count=3, pause=0.001):
    # symbol = _code_to_symbol(code)
    lhburl='http://data.eastmoney.com/stock/tradedetail.html'
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
            abc= (soup.find_all('table',type="tab1"))
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
            alldata = {}
            dict_data = {}
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
                    m_vol = float(td_cells[1].find(text=True).replace(',', '')) * 100
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
            df = DataFrame(sdata, columns=['code', 'time', 'vol', 'price', 'pre_p', 'status', 'name'])
            # for row in soup.find_all('tr',attrs={"class":"gray","class":""}):
        except Exception as e:
            print "Except:", (e)
        else:
            return df
        traceback.print_exc()
        raise IOError(ct.NETWORK_URL_ERROR_MSG.decode('utf8').encode('gbk'))
    
if __name__ == "__main__":
    # ff = get_dfcfw_fund_flow(ct.DFCFW_FUND_FLOW_URL % ct.SINA_Market_KEY_TO_DFCFW['sh'])
    # print "%.1f" % (float(ff['zzb']))
    # print ff
    #
    # # pp=get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
    # # for x in pp.keys():
    # #     print pp[x]
    #
    
    get_lhb_dd()
    
    # pp=get_dfcfw_fund_SHSZ(ct.DFCFW_ZS_SHSZ)
    # print pp
    # print get_zs_VolRatio()
    # a='abc'
    # print isinstance(a,str)
    
    # pp=get_dfcfw_fund_HGT(ct.DFCFW_FUND_FLOW_HGT)
    # for x in pp.keys():
    #     print pp[x]