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
from bs4 import BeautifulSoup
import urllib2
from pandas import Series,DataFrame
import re
import johnson_cons as ct
import time
import singleAnalyseUtil as sl
import realdatajson as rl
import pandas as pd
import traceback
import sys

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
    status=False
    vol = '0'
    type = '2'
    cut_num=10000
    success=0
    top_all=pd.DataFrame()
    time_s=time.time()
    delay_time=300
    while 1:
        try:
            df=rl.get_sina_all_json_dd(vol,type)
            print len(df)

            if len(df) >cut_num:
                df=df[:cut_num]
                # print len(df)
            top_now = rl.get_sina_dd_count_price_realTime(df)
            # print len(top_now)
            if len(top_now)>10 and len(top_now.columns)>4:
                top_now = top_now[top_now.trade >= top_now.high*0.98]
                time_d=time.time()
                if 'percent' in top_now.columns.values:
                    top_now=top_now[top_now['percent']>0]
                if len(top_all) == 0:
                    top_all = top_now
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
                            if count_n>count_a:
                                top_now.loc[symbol,'diff']=count_n-count_a
                                if time_d-time_s>delay_time:
                                    # print "change:",time.time()-time_s
                                    top_all.loc[symbol]=top_now.loc[symbol]
                                else:
                                    top_all.loc[symbol,'diff':]=top_now.loc[symbol,'diff':]
                            else:
                                top_all.loc[symbol,'percent':]=top_now.loc[symbol,'percent':]
                            # top_all.loc[symbol]=top_now.loc[symbol]?
                            # top_all.loc[symbol,'diff']=top_now.loc[symbol,'counts']-top_all.loc[symbol,'counts']

                            # else:
                                # value=top_all.loc[symbol,'diff']

                        else:
                            top_all.append(top_now.loc[symbol])
                # top_all=top_all.sort_values(by=['diff','percent','counts'],ascending=[0,0,1])
                # top_all=top_all.sort_values(by=['diff','ratio','percent','counts'],ascending=[0,1,0,1])
                top_all=top_all.sort_values(by=['diff','percent','counts','ratio'],ascending=[0,0,1,1])
                if time_d-time_s>delay_time:
                    time_s=time.time()

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

            else:
                print "no data"
            time.sleep(60)

        except (KeyboardInterrupt) as e:
            # print "key"
            print "KeyboardInterrupt:", e
            # time.sleep(1)
            # if success > 3:
            #     raw_input("Except")
            #     sys.exit(0)
            st=raw_input("status:[go(g),clear(c),quit(q,e)]:")
            if len(st)==0:
                status=False
            elif st=='g' or st=='go':
                status = True
            elif st=='clear' or st=='c':
                top_all=pd.DataFrame()
                status=False
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

