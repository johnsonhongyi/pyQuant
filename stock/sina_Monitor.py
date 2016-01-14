#-*- coding:utf-8 -*-
#!/usr/bin/env python


# import sys
#
# reload(sys)
#
# sys.setdefaultencoding('utf-8')
url_s="http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=0&type=1"
url_b="http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=100000&type=0"
status_dict={u"中性盘":"normal",u"买盘":"up",u"卖盘":"down"}
url_real_sina="http://finance.sina.com.cn/realstock/"
url_real_sina_top="http://vip.stock.finance.sina.com.cn/mkt/#stock_sh_up"
url_real_east="http://quote.eastmoney.com/sz000004.html"
import re
import sys
import time
import urllib2

import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame

import JohhnsonUtil.johnson_cons as ct
import JohhnsonUtil.commonTips as cct
from JSONData import realdatajson as rl
import singleAnalyseUtil as sl
from JSONData import tdx_data_Day as tdd
from JohhnsonUtil import LoggerFactory as LoggerFactory
import gc

def downloadpage(url):
    fp = urllib2.urlopen(url)
    data = fp.read()
    fp.close()
    return data

def parsehtml(data):
    soup = BeautifulSoup(data)
    for x in soup.findAll('a'):
        print x.attrs['href']

def html_clean_content(soup):
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    soup.prettify()
    reg1 = re.compile("<[^>]*>")  #剔除空行空格
    content = reg1.sub('',soup.prettify())
    print content

def get_sina_url(vol='0', type='0',pageCount='100'):
    # if len(pageCount) >=1:
    url=ct.SINA_DD_VRatio_All%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'],pageCount,ct.DD_VOL_List[vol], type)
    # print url
    return url

def get_sina_all_dd(vol='0', type='0', retry_count=3, pause=0.001):
    if len(vol) != 1 or len(type) != 1:
        return None
    else:
        print ("Vol:%s  Type:%s"%(ct.DD_VOL_List[vol],ct.DD_TYPE_List[type]))
    # symbol = _code_to_symbol(code)
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            ct._write_console()
            url=get_sina_url(vol,type)
            # url= ct.SINA_DD_VRatio % (ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'],ct.DD_VOL_List[vol], ct.DD_TYPE_List[type])
            page = urllib2.urlopen(url)
            html_doc = page.read()
            # print (html_doc)
            # soup = BeautifulSoup(html_doc,fromEncoding='gb18030')
            # print html_doc
            pageCount=re.findall('fillCount\"\]\((\d+)',html_doc,re.S)
            if len(pageCount) > 0:
                start_t=time.time()
                pageCount=pageCount[0]
                if int(pageCount) > 100:
                    if int(pageCount) >10000:
                        print "BigBig:",pageCount
                        pageCount='10000'

                    print "AllBig:",pageCount
                    html_doc=urllib2.urlopen(get_sina_url(vol,type,pageCount=pageCount)).read()
                    print (time.time()-start_t)

            soup = BeautifulSoup(html_doc,"lxml")
            print (time.time()-start_t)
            # abc= (soup.find_all('script',type="text/javascript"))
            # print(len(abc))
            # print (abc[4].text).strip().find('window["fillCount"]')
            # print abc[4].contents


            # pageCount= soup.find_all(string=re.compile('fillCount\"\]\((\d+)'))
            # pageCount=re.findall('(\d+)',pageCount[0])

            # sys.exit(0)
            # print soup.find_all('__stringHtmlPages')

            # sys.exit(0)

            # soup = BeautifulSoup(html_doc.decode('gb2312','ignore'))
            # print soup.find_all('div', id="divListTemplate")
            # for i in soup.find_all('tr',attrs={"class": "gray"."class":""}):
            alldata={}
            dict_data={}
            # print soup.find_all('div',id='divListTemplate')

            row = soup.find_all('div',id='divListTemplate')
            sdata=[]
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
                for tag in row[0].find_all('tr',attrs={"class":True}):
                    # print tag
                    th_cells = tag.find_all('th')
                    td_cells = tag.find_all('td')
                    m_name=th_cells[0].find(text=True)
                    m_code=th_cells[1].find(text=True)
                    m_time=th_cells[2].find(text=True)
                    # m_detail=(th_cells[4]).find('a')["href"]   #detail_url
                    m_price=td_cells[0].find(text=True)
                    m_vol=float(td_cells[1].find(text=True).replace(',',''))*100
                    m_pre_p=td_cells[2].find(text=True)
                    m_status_t=th_cells[3].find(text=True)
                    if m_status_t in status_dict.keys():
                        m_status = status_dict[m_status_t]
                        # print m_status
                    sdata.append({'code':m_code,'time':m_time,'vol':m_vol,'price':m_price,'pre_p':m_pre_p,'status':m_status,'name':m_name})
                    # sdata.append({'code':m_code,'time':m_time,'vol':m_vol,'price':m_price,'pre_p':m_pre_p,'detail':m_detail,'status':m_status,'name':m_name})
                    # print sdata
                    # print m_name
                    # break
            # pd = DataFrame(sdata,columns=['code','time','vol','price','pre_p','detail','status','name'])
            df = DataFrame(sdata,columns=['code','time','vol','price','pre_p','status','name'])
            # for row in soup.find_all('tr',attrs={"class":"gray","class":""}):
        except Exception as e:
            print "Except:",(e)
        else:
            return df
        raise IOError(ct.NETWORK_URL_ERROR_MSG)

if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))

    log = LoggerFactory.getLogger('SinaMarket')
    # log.setLevel(LoggerFactory.DEBUG)
    
    cct.set_console()
    status=False
    vol = '0'
    type = '2'
    cut_num=20000
    success=0
    top_all=pd.DataFrame()
    time_s=time.time()
    delay_time=3600
    base_path = tdd.get_tdx_dir()
    block_path = tdd.get_tdx_dir_blocknew() + '064.blk'
    while 1:
        try:
            df=rl.get_sina_all_json_dd(vol,type)
            if len(df) >cut_num:
                df=df[:cut_num]
                print len(df),
            top_now = rl.get_sina_dd_count_price_realTime(df)
            # print len(top_now)
            time_d = time.time()
            if time_d - time_s > delay_time:
                status_change = True
                time_s = time.time()
                top_all=pd.DataFrame()

            else:
                status_change = False
            if len(top_now)>10 and len(top_now.columns)>4:
                top_now = top_now[top_now.trade >= top_now.high*0.98]
                if 'percent' in top_now.columns.values:
                    top_now=top_now[top_now['percent']>0]
                if len(top_all) == 0:
                    top_all = top_now
                    time_s=time.time()
                    # dd=dd.fillna(0)
                else:
                    for symbol in top_now.index:

                        # code = rl._symbol_to_code(symbol)
                        if symbol in top_all.index :
                            # if top_all.loc[symbol,'diff'] == 0:
                            # print "code:",symbol
                            count_n=top_now.loc[symbol,'counts']
                            count_a=top_all.loc[symbol,'counts']
                            # print count_n,count_a
                            if not count_n==count_a:
                                top_now.loc[symbol,'diff']=count_n-count_a
                                if status_change:
                                    # print "change:",time.time()-time_s
                                    top_all.loc[symbol]=top_now.loc[symbol]
                            else:
                                top_all.loc[symbol,['percent','diff']]=top_now.loc[symbol,['percent','diff']]
                                top_all.loc[symbol,'trade':]=top_now.loc[symbol,'trade':]
                                    # top_all.loc[symbol,['percent','diff','trade','high','open','low','ratio']]=top_now.loc[symbol,['percent','diff','trade','high','open','low','ratio']]
                            # else:
                                # top_all.loc[symbol,['percent','trade','high','open','low','ratio']]=top_now.loc[symbol,['percent','diff','trade','high','open','low','ratio']]
                            # top_all.loc[symbol]=top_now.loc[symbol]?
                            # top_all.loc[symbol,'diff']=top_now.loc[symbol,'counts']-top_all.loc[symbol,'counts']

                            # else:
                                # value=top_all.loc[symbol,'diff']

                        else:
                            top_all.append(top_now.loc[symbol])
                # top_all=top_all.sort_values(by=['diff','percent','counts'],ascending=[0,0,1])
                # top_all=top_all.sort_values(by=['diff','ratio','percent','counts'],ascending=[0,1,0,1])
                # top_all=top_all.sort_values(by=['diff','percent','counts','ratio'],ascending=[0,0,1,1])
                
                top_bak=top_all
                codelist = top_all.index.tolist()
                if len(codelist)>0:
                    log.info('toTDXlist:%s' % len(codelist))
                    tdxdata = tdd.get_tdx_all_day_LastDF(codelist)
                    log.debug("TdxLastP: %s %s" % (len(tdxdata), tdxdata.columns.values))
                    tdxdata.rename(columns={'low': 'llow'}, inplace=True)
                    tdxdata.rename(columns={'high': 'lhigh'}, inplace=True)
                    tdxdata.rename(columns={'close': 'lastp'}, inplace=True)
                    tdxdata.rename(columns={'vol': 'lvol'}, inplace=True)
                    tdxdata = tdxdata.loc[:, ['llow', 'lhigh', 'lastp', 'lvol', 'date']]
                    # data.drop('amount',axis=0,inplace=True)
                    log.debug("TDX Col:%s" % tdxdata.columns.values)
                    # df_now=top_all.merge(data,on='code',how='left')
                    # df_now=pd.merge(top_all,data,left_index=True,right_index=True,how='left')
                    top_all = top_all.merge(tdxdata, left_index=True, right_index=True, how='left')
                    log.info('Top-merge_now:%s' % (top_all[:1]))
                    top_all = top_all[top_all['llow'] > 0]
                    log.info("df:%s"%top_all[:1])
                    radio_t = cct.get_work_time_ratio()
                    log.debug("Second:vol/vol/:%s" % radio_t)
                    # top_dif['volume'] = top_dif['volume'].apply(lambda x: round(x / radio_t, 1))
                    log.debug("top_diff:vol")
                    top_all['volume'] = (
                        map(lambda x, y: round(x / y / radio_t, 1), top_all['volume'].values, top_all['lvol'].values))
                    
                    # top_all = top_all[top_all.prev_p >= top_all.lhigh]
                    top_all=top_all.loc[:,['name','percent','diff','counts','volume','trade','prev_p','ratio']]
                
                print "G:%s"%len(top_all)
                top_all=top_all.sort_values(by=['diff','counts','volume','ratio'],ascending=[0,0,0,1])
                # top_all=top_all.sort_values(by=['percent','diff','counts','ratio'],ascending=[0,0,1,1])



                # print top_all
                # print pt.PrettyTable([''] + list(top_all.columns))
                # print tbl.tabulate(top_all,headers='keys', tablefmt='psql')
                # print tbl.tabulate(top_all,headers='keys', tablefmt='orgtbl')
                # print rl.format_for_print(top_all)
                # print top_all[:10]
                print rl.format_for_print(top_all[:10])
                # print "staus",status
                if status:
                    for code in top_all[:10].index:
                        code=re.findall('(\d+)',code)
                        if len(code)>0:
                            code=code[0]
                            kind=sl.get_multiday_ave_compare_silent(code)
                top_all=top_bak
                del top_bak
                gc.collect()

            else:
                print "no data"
            int_time = cct.get_now_time_int()
            if cct.get_work_time():
                if int_time < 930:
                    while 1:
                        time.sleep(60)
                        if cct.get_now_time_int() < 931:
                            time.sleep(60)
                            print ".",
                        else:
                            top_all=pd.DataFrame()
                            print "."
                            break
                else:
                    time.sleep(60)
            elif cct.get_work_duration():
                while 1:
                    time.sleep(60)
                    if cct.get_work_duration():
                        print ".",
                        time.sleep(60)
                    else:
                        break
            else:
                # break
                # time.sleep(5)
                st = raw_input("status:[go(g),clear(c),quit(q,e),W(w),Wa(a)]:")
                if len(st) == 0:
                    status = False
                elif st == 'g' or st == 'go':
                    status = True
                    for code in top_all[:10].index:
                        code = re.findall('(\d+)', code)
                        if len(code) > 0:
                            code = code[0]
                            kind = sl.get_multiday_ave_compare_silent(code)
                elif st == 'clear' or st == 'c':
                    top_all = pd.DataFrame()
                    status = False
                elif st == 'w' or st == 'a':
                    codew = (top_all.index).tolist()
                    if st == 'a':
                        cct.write_to_blocknew(block_path, codew[:20])
                        # cct.write_to_blocknew(all_diffpath, codew)
                    else:
                        cct.write_to_blocknew(block_path, codew[:20], False)
                        # cct.write_to_blocknew(all_diffpath, codew, False)
                    print "wri ok:%s"%block_path
                    # time.sleep(2)
                else:
                    sys.exit(0)

        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # time.sleep(1)
            # if success > 3:
            #     raw_input("Except")
            #     sys.exit(0)
            # st=raw_input("status:[go(g),clear(c),quit(q,e)]:")
            st = raw_input("status:[go(g),clear(c),quit(q,e),W(w),Wa(a)]:")

            if len(st)==0:
                status=False
            elif st=='g' or st=='go':
                status = True
            elif st=='clear' or st=='c':
                top_all=pd.DataFrame()
                status=False
            elif st == 'w' or st == 'a':
                # base_path=r"E:\DOC\Parallels\WinTools\zd_pazq\T0002\blocknew\\"
                # block_path=base_path+'064.blk'
                # all_diffpath=base_path+'\065.blk'
                codew=top_all[:20].index.tolist()
                if st=='a':
                    cct.write_to_blocknew(block_path,codew)
                    # cct.write_to_blocknew(all_diffpath,codew)
                else:
                    cct.write_to_blocknew(block_path,codew,False)
                    # cct.write_to_blocknew(all_diffpath,codew,False)
                print "wri ok"
                # time.sleep(5)
            else:
                sys.exit(0)
        except (IOError, EOFError) as e:
            print "Error",e

            # traceback.print_exc()
            # raw_input("Except")


    # sl.get_code_search_loop()
    # print data.describe()
    # while 1:
    #     intput=raw_input("code")
    #     print
    # pd = DataFrame(data)
    # print pd
    # parsehtml("""
    # <a href="www.google.com"> google.com</a>
    # <A Href="www.pythonclub.org"> PythonClub </a>
    # <A HREF = "www.sina.com.cn"> Sina </a>
    # """)

