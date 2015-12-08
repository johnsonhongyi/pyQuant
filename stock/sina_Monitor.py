#-*- coding:utf-8 -*-
#!/usr/bin/env python


# import sys
#
# reload(sys)
#
# sys.setdefaultencoding('utf-8')
url_s="http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=0&type=1"
url_b="http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=100000&type=0"
status={u"中性盘":"normal",u"买盘":"up",u"卖盘":"down"}

from bs4 import BeautifulSoup
import urllib2
from pandas import Series,DataFrame
import sys,re,time
import cons as ct
import time


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
    url=ct.SINA_DD_VRatio_All%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], ct.PAGES['sinadd_all'],pageCount,ct.DD_VOL_List[vol], ct.DD_TYPE_List[type])
    # print url
    return url

def get_sina_all_dd(vol='0', type='0', retry_count=3, pause=0.001):
    if len(vol) != 1 or len(type) != 1:
        return None
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
                    if pageCount >5000:
                        print "BigBig:",pageCount
                        pageCount='5000'

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
                    if m_status_t in status.keys():
                        m_status = status[m_status_t]
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
    start_t= time.time()
    data=get_sina_all_dd('3')
    interval=(time.time() - start_t)
    # print ""
    print "interval:",interval
    print data[:2]
    print data.describe()
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

