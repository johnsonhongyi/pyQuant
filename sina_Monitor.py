#-*- coding:utf-8 -*-
#!/usr/bin/env python


# import sys
#
# reload(sys)
#
# sys.setdefaultencoding('utf-8')
url_s="http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=0&type=1"
url_b="http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_all.php?num=100&page=1&sort=ticktime&asc=0&volume=500000&type=0"
status={u"中性盘":"normal",u"买盘":"up",u"卖盘":"down"}

from bs4 import BeautifulSoup
import urllib2
from pandas import Series,DataFrame

def downloadpage(url):
    fp = urllib2.urlopen(url)
    data = fp.read()
    fp.close()
    return data

def parsehtml(data):
    soup = BeautifulSoup(data)
    for x in soup.findAll('a'):
        print x.attrs['href']

def jd(url):
    page = urllib2.urlopen(url)
    html_doc = page.read()
    # print (html_doc)
    # soup = BeautifulSoup(html_doc,fromEncoding='gb18030')
    soup = BeautifulSoup(html_doc,"lxml")
    # soup = BeautifulSoup(html_doc.decode('gb2312','ignore'))
    # print soup.find_all('div', id="divListTemplate")
    # for i in soup.find_all('tr',attrs={"class": "gray"."class":""}):
    alldata={}
    dict_data={}
    # print soup.find_all('div',id='divListTemplate')

    row = soup.find_all('div',id='divListTemplate')
    sdata={}
    if len(row) >= 1:
        firstCells = row[0].find('tr')
        th_cells = firstCells.find_all('th')
        td_cells = firstCells.find_all('td')
        m_name=th_cells[0].find(text=True)
        m_code=th_cells[1].find(text=True)
        m_time=th_cells[2].find(text=True)
        m_status=th_cells[3].find(text=True)
        m_detail=th_cells[4].find(text=True)
        m_price=td_cells[0].find(text=True)
        m_vol=td_cells[1].find(text=True)
        m_pre_p=td_cells[2].find(text=True)
        # print "m_name:",m_name,m_pre_p
            # for tag in row.find_all('tr',attrs={"class":"gray","class":""}):
        for tag in row[0].find_all('tr',attrs={"class":True}):
            # print tag
            th_cells = tag.find_all('th')
            td_cells = tag.find_all('td')

            m_name=th_cells[0].find(text=True)
            m_code=th_cells[1].find(text=True)
            m_time=th_cells[2].find(text=True)
            m_detail=th_cells[4].find(text=True)
            m_price=td_cells[0].find(text=True)
            m_vol=td_cells[1].find(text=True)
            m_pre_p=td_cells[2].find(text=True)
            m_status_t=th_cells[3].find(text=True)
            if m_status_t in status.keys():
                m_status = status[m_status_t]
                # print m_status
            sdata[m_code] = {'code':m_code,'time':m_time,'vol':m_vol,'price':m_price,'pre_p':m_pre_p,'detail':m_detail,'vol':m_vol,'status':m_status,'name':m_name}
            # print sdata
            # print m_name
            # break
    obj3 = Series(sdata)
    print obj3.index
    # print obj3['sz002029']
    print "done"
    # for row in soup.find_all('tr',attrs={"class":"gray","class":""}):
    #     print row
    #     for tag in row.find_all('tr'):
    #         # print tag
    #         th_cells = tag.find_all('th')
    #         td_cells = tag.find_all('td')
    #
    #         print len(th_cells)
    #         print len(td_cells)
    #         # if len(th_list) == 3:
    #
    #         # print "####"
    #         # for th in tag.find_all('th'):
    #         #     print th
    #
    #         m_name=th_cells[0].find(text=True)
    #         m_code=th_cells[1].find(text=True)
    #         m_time=th_cells[2].find(text=True)
    #         m_status=th_cells[3].find(text=True)
    #         m_detail=th_cells[4].find(text=True)
    #         m_price=td_cells[0].find(text=True)
    #         m_vol=td_cells[1].find(text=True)
    #         m_pre_p=td_cells[2].find(text=True)
    #         print m_code
        # break
        # print "i:  ",i
        # one = i.find_all('a')
        # two = i.find_all('li')
        # print ("%s %s" % (one,two))

if __name__ == "__main__":
    # parsehtml(downloadpage(url_s))
    jd(url_b)
    # parsehtml("""
    # <a href="www.google.com"> google.com</a>
    # <A Href="www.pythonclub.org"> PythonClub </a>
    # <A HREF = "www.sina.com.cn"> Sina </a>
    # """)

