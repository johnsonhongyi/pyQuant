# -*- coding:utf8 -*-
"""
交易数据接口
Created on 2014/07/31
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
"""
from __future__ import division

import json
import math
import re
import sys
import time

import pandas as pd
sys.path.append("..")
# import JohhnsonUtil.johnson_cons as ct
from JohhnsonUtil import LoggerFactory
from JohhnsonUtil import commonTips as cct
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

log=LoggerFactory.getLogger('wencaiData')


def post_login(root='http://upass.10jqka.com.cn/login'):
    postData = {
    'act':"login_submit",
    'isiframe':"1",
    'view':"iwc_quick",
    'rsa_version':"default_2",
    'redir':"http://www.iwencai.com/user/pop-logined",
    'uname':"OuY03m5D1ojuPmpTAbgkpcm0dod5fMbU8jVOwd17WCPEW0pz52RyEcXU+2ZLiBmP+5jckGeUR5ba/fDjkUaPVaisn9Je4l7+JPv3iX/VS4erW25ueJEoVszK9kM3oF2mT3lraObawMclBteFcfwWHyWhsW7YmN19cgOdsQWWWno=",
    'passwd':"IVORnBZ0Pdi+ix+ehVqiCdYTWCkGBy/kYEeTyTmi+5QBiL8SvYZZg3LLVzzfeMbOWaR/rK4Aoc80kSpqCIETfN3EmhA1CKK9ukI0TImlm8ASlqqz/lUq0lm5LwuMRdBjcD3hoP4RnvDc+W2+ng4XA31YsG6pBo+YF5IHcIxaScU=",
    'captchaCode':"",
    'longLogin':"on",
    }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Connection': 'keep-alive'}
    from cookielib import CookieJar
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    data_encoded = urllib.urlencode(postData)
    url = 'http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s'
    url = url%('国企改革')
    for ck in cj:
        print ck
    print ":"
    try:
        response = opener.open(root,data_encoded)
        content = response.read()
        # count = re.findall('\[[A-Za-z].*\]', data, re.S)
        status = response.getcode()
        # print content
        for ck in cj:
            print ck
        print ":"
        # cj["session"]["u_name_wc"] = "mx_149958484"
        if status == 200:
            response = opener.open(url)
            page =  response.read()
            print page
            for ck in cj:
                print ck
    except  urllib2.HTTPError, e:
         print e.code
    # f= response.read().decode("utf8")
    # outfile =open("rel_ip.txt","w")
    # print >> outfile , "%s"   % ( f)
    #打印响应的信息
    # info = response.info()
    # print info
    # get_wencai_Market_url(url=None)

global null
null = None
def get_wencai_Market_url(filter='国企改革',perpage=1,url=None,):
    urllist = []
    global null
    df = pd.DataFrame()
    if url == None:
        time_s = time.time()
        wencairoot = 'http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s'
        url = wencairoot%(filter)
        log.info("url:%s"%(url))
        # url = ct.get_url_data_R % (market)
        # print url
        cache_root="http://www.iwencai.com/stockpick/cache?token=%s&p=1&perpage=%s&showType="
        cache_ends = "[%22%22,%22%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22]"
        data = cct.get_url_data(url)
        # print data
        # count = re.findall('(\d+)', data, re.S)
        # "token":"dcf3d42bbeeb32718a243a19a616c217"
        # log.info("data:%s"%(data.decode('unicode-escape')))
        # log.info("data:%s"%(data))
        # count = re.findall('token":"([\D\d].*)"', data, re.S)
        count = re.findall('token":"([\D\d]+?)"', data, re.S)
        codelist = []
        grep_stock_codes = re.compile('"(\d{6})\.S')
        # response = requests.get(all_stock_codes_url)
        # stock_codes = grep_stock_codes.findall(response.text)
        # print data
        log.info( time.time()-time_s)
        # print count
        if len(count) == 1:
            cacheurl = cache_root % (count[0],perpage)
            cacheurl =  cacheurl + cache_ends
            log.info( cacheurl)
            time_s = time.time()
            html = cct.get_url_data(cacheurl)
            # count = re.findall('"(\d{6})\.S', data, re.S)
            # count = re.findall('result":(\[[\D\d]+\]),"oriColPos', data, re.S)
            # count = re.findall('result":(\[[\D\d]+\]),"oriIndexID', data, re.S)
#            html = data.decode('unicode-escape')
#            html = data.decode('unicode-escape')
            count = re.findall('(\[\["[0-9]{6}\.S[HZ][\D\d]+\]\]),"oriIndexID', html, re.S)
            # count = grep_stock_codes.findall(data,re.S)
            log.info("count:%s len:%s"%(count,len(count)))
            # print html

            log.info( time.time()-time_s)
            if len(count) > 0:
                # import ast
                # result = eval(count[0].replace('null','None'))
                result = eval(count[0])
                # result = ast.literal_eval(count[0])
                # import json
                # obj = json.loads(data)
                # print "obj:",obj
                # print result,len(result)
                # print result[1]
                urllist = []
                dlist = []
                key_t=[]
                for xcode in result:
                    # print xcode
                    code_t =[]
                    for x in xcode:
                        # print x
                        if isinstance(x, list):
                            # print "list:",x
                            key_t=[]
                            for y in x:
                                if isinstance(y, dict):
                                    # pass
                                    keylist=['URL','PageRawTitle']
                                    for key in y.keys():
                                        if key in keylist:
                                            if key == 'URL':
                                                urls = str(y[key]).replace('\\','').strip().decode('unicode-escape')
                                                if urls[-20] not in urllist:
                                                    urllist.append(urls[-20])
                                                    log.info( urls),
#                                                    log.info( urls)
                                                else:
                                                    break
                                            else:
                                                urls = str(y[key]).decode('unicode-escape')
                                                key_t.append(urls)
#                                                key_t.append(urls)
                                                log.info( urls),
                                # else:
                                    # print str(y).decode('unicode-escape'),
                        else:
                            code_t.append(str(x).decode('unicode-escape'))
#                            code_t.append(str(x))
                            log.info(str(x).decode('unicode-escape')),
#                            log.info(str(x)),
                    log.info( key_t)
                    ''' ['600172.SH', '\xe9\xbb\x84\xe6\xb2\xb3\xe6\x97\x8b\xe9\xa3\x8e',
                     '17.41', '1.221', '5', '2345', '\xe4\xb8\x8a\xe6\xb5\xb7', '4423704']
                      ['\xe5\xa4\x9a\xe5\xae\xb6\xe6\x9c\xba\xe6\x9e\x84 \xe7\x9c\x8b\xe5\xa5\xbd\xe6\x9c\xba\xe6\xa2\xb0\xe8\xa1\x8c\xe4\xb8\x9a',
                      '\xe5\xb8\x82\xe5\x9c\xba\xe5\x9b\x9e\xe8\xb0\x83\xe6\x98\x8e\xe6\x98\xbe \xe8\xb6\x85\xe8\xb7\x8c\xe4\xbd\x8e\xe4\xbc\xb0\xe5\x80\xbc\xe8\x82\xa1\xe7\xa5\xa8\xe5\x80\xbc\xe5\xbe\x97\xe5\x85\xb3\xe6\xb3\xa8', '40\xe8\x82\xa1\xe8\xbf\x9e\xe7\xbb\xad\xe8\xb5\xb0\xe5\x87\xba\xe9\x87\x91\xe5\x8f\x89 \xe7\x9f\xad\xe7\xba\xbf\xe4\xb8\x8a\xe6\xb6\xa8\xe6\x9c\x89\xe6\x9c\x9b',
                      '\xe4\xb8\x8b\xe5\x91\xa841\xe5\x8f\xaa\xe9\x99\x90\xe5\x94\xae\xe8\x82\xa1\xe8\xa7\xa3\xe7\xa6\x81 \xe4\xb8\xad\xe9\x92\xa8\xe9\xab\x98\xe6\x96\xb0\xe8\xa7\xa3\xe7\xa6\x81\xe8\xbe\xbe50.4\xe4\xba\xbf\xe5\x85\x83',
                      '\xe5\x95\x86\xe4\xb8\x9a\xe6\x96\xb0\xe9\xa3\x8e\xe5\x8f\xa3\xe5\xb7\xb2\xe8\x87\xb3 \xe5\xae\xb6\xe7\x94\xb5\xe4\xbc\x81\xe4\xb8\x9a\xe8\xbf\x9b\xe5\x86\x9b\xe6\x9c\xba\xe5\x99\xa8\xe4\xba\xba\xe9\xa2\x86\xe5\x9f\x9f', '\xe4\xb8\x80\xe9\x98\xb3\xe7\xa9\xbf\xe4\xb8\x89\xe7\xba\xbf\xe7\x9a\x84\xe8\x82\xa1\xe7\xa5\xa8\xe4\xb8\x8a\xe6\xb6\xa8\xe6\xa6\x82\xe7\x8e\x87\xe5\xa6\x82\xe4\xbd\x95?']'''
                    if len(code_t) > 4:
                        code = code_t[0]
                        name = code_t[1]
                        trade = code_t[2]
                        percent = code_t[3]
                        # index = code_t[4]
                        index = ";".join(x for x in code_t[4].split(';')[:3])
                        if len(key_t) > 0:
                            # print key_t[0]
                            title1 = key_t[0]
                            if len(key_t) > 1:
                                title2 = key_t[1]
                            else:
                                title2 = None
                            dlist.append({'code': code, 'name': name, 'trade': trade, 'percent': percent, 'index': index, 'tilte1': title1,'tilte2': title2})
                        else:
                            dlist.append({'code': code, 'name': name, 'trade': trade, 'percent': percent, 'index': index})
                    # print ''
                # df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
                # df = pd.DataFrame(dlist, columns=['index','code','name','trade','percent','tilte1','tilte2'])
                if len(dlist) > 0 and 'tilte1' in (dlist[0].keys()) :
                    df = pd.DataFrame(dlist, columns=['code','name','trade','percent','index','tilte1','tilte2'])
                else:
                    df = pd.DataFrame(dlist, columns=['code','name','trade','percent','index'])
                df['code'] = (map(lambda x: x[:6],df['code']))
                df = df.set_index('code')
            # print type(count[0])
            # print type(list(count[0]))
            # print count[0].decode('unicode-escape')
    return df

def get_codelist_df(codelist):
    wcdf = pd.DataFrame()
    time_s = time.time()
    if len(codelist)>30:
        # num=int(len(codeList)/cpu_count())
        div_list = cct.get_div_list(codelist, int(len(codelist)/30+1))
        # print "ti:",time.time()-time_s
#        cnamelist =[]
        for li in div_list:
            cname = ",".join(x for x in li)
#            cnamelist.append(cname)
            wcdf_t = get_wencai_Market_url(cname,len(li))
            wcdf = wcdf.append(wcdf_t)
#        results = cct.to_mp_run_async(get_wencai_Market_url, cnamelist,30)
#        for res in results:
#            wcdf = wcdf.append(res)
        print ("wenc:%s"%(time.time()-time_s)),
        # print results
    else:
        cname = ",".join(x for x in codelist)
        wcdf = get_wencai_Market_url(cname,len(codelist))
#        wcdf = wcdf.append(wcdf_t)

    return wcdf
if __name__ == '__main__':
    # df = get_sina_all_json_dd('0', '3')
    # df=get_sina_Market_json('cyb')
    # _get_sina_json_dd_url()
    # print sina_json_Big_Count()
    # print getconfigBigCount(write=True)
    # sys.exit(0)
    # post_login()
#    log.setLevel(LoggerFactory.INFO)
#    df = get_wencai_Market_url(filter='国企改革',perpage=1000)
    # df = get_wencai_Market_url('瑞丰高材,太阳电缆,杭州解百',500)
    df = get_codelist_df([u'\u7ef4\u5b8f\u80a1\u4efd', u'\u6d77\u987a\u65b0\u6750', u'\u6da6\u6b23\u79d1\u6280', u'\u84dd\u6d77\u534e\u817e', u'\u5149\u529b\u79d1\u6280', u'\u805a\u9686\u79d1\u6280', u'\u539a\u666e\u80a1\u4efd', u'\u534e\u94ed\u667a\u80fd', u'\u7530\u4e2d\u7cbe\u673a', u'\u60e0\u4f26\u6676\u4f53', u'\u8d62\u5408\u79d1\u6280', u'\u5eb7\u62d3\u7ea2\u5916', u'\u5c71\u6cb3\u836f\u8f85', u'\u5168\u4fe1\u80a1\u4efd', u'\u4e50\u51ef\u65b0\u6750', u'\u5eb7\u65af\u7279', u'\u9e4f\u8f89\u80fd\u6e90', u'\u4e2d\u6cf0\u80a1\u4efd', u'\u91d1\u77f3\u4e1c\u65b9', u'\u56db\u901a\u65b0\u6750', u'\u7ea2\u76f8\u7535\u529b', u'\u535a\u4e16\u79d1', u'\u4f0a\u4e4b\u5bc6', u'\u6b63\u4e1a\u79d1\u6280', u'\u5b9d\u8272\u80a1\u4efd', u'\u98de\u51ef\u6750\u6599', u'\u8fea\u745e\u533b\u7597', u'\u8d62\u65f6\u80dc', u'\u6c47\u4e2d\u80a1\u4efd', u'\u535a\u817e\u80a1\u4efd', u'\u4e1c\u534e\u6d4b\u8bd5', u'\u4e1c\u571f\u79d1\u6280', u'\u91d1\u5361\u80a1\u4efd', u'\u592a\u7a7a\u677f\u4e1a', u'\u8054\u521b\u4e92\u8054', u'\u6da6\u548c\u8f6f\u4ef6', u'\u65b0\u6587\u5316', u'\u5b9c\u5b89\u79d1\u6280', u'\u65cb\u6781\u4fe1\u606f', u'\u6676\u76db\u673a\u7535', u'\u5929\u5c71\u751f\u7269', u'\u90a6\u8baf\u6280\u672f', u'\u5409\u827e\u79d1\u6280', u'\u4e2d\u9645\u88c5\u5907', u'\u540c\u6709\u79d1\u6280', u'\u5bcc\u6625\u901a\u4fe1', u'\u5229\u4e9a\u5fb7', u'\u5b89\u79d1\u745e', u'\u6e29\u5dde\u5b8f\u4e30', u'\u901a\u5149\u7ebf\u7f06', u'\u9686\u534e\u8282\u80fd', u'\u7cbe\u953b\u79d1\u6280', u'\u5f00\u5c71\u80a1\u4efd', u'\u91d1\u4fe1\u8bfa', u'\u745e\u4e30\u9ad8\u6750', u'\u98de\u529b\u8fbe', u'\u91d1\u529b\u6cf0', u'\u6b63\u6d77\u78c1\u6750', u'\u91d1\u8fd0\u6fc0\u5149', u'\u7535\u79d1\u9662', u'\u6d77\u4f26\u54f2', u'\u94c1\u6c49\u751f\u6001', u'\u4e2d\u6d77\u8fbe', u'\u9e3f\u7279\u7cbe\u5bc6', u'\u6717\u6e90\u80a1\u4efd', u'\u96f7\u66fc\u80a1\u4efd', u'\u79c0\u5f3a\u80a1\u4efd', u'\u65b0\u7814\u80a1\u4efd', u'\u6052\u6cf0\u827e\u666e', u'\u795e\u96fe\u73af\u4fdd', u'\u745e\u51cc\u80a1\u4efd', u'\u65b0\u56fd\u90fd', u'\u6613\u4e16\u8fbe', u'\u987a\u7f51\u79d1\u6280', u'\u5411\u65e5\u8475', u'\u65b0\u5f00\u6e90', u'\u897f\u90e8\u7267\u4e1a', u'\u632f\u82af\u79d1\u6280', u'\u5c24\u6d1b\u5361', u'\u667a\u4e91\u80a1\u4efd', u'\u6613\u8054\u4f17', u'\u56fd\u8054\u6c34\u4ea7', u'\u5eb7\u829d\u836f\u4e1a', u'\u5965\u514b\u80a1\u4efd', u'\u6613\u6210\u65b0\u80fd', u'\u5f53\u5347\u79d1\u6280', u'\u5929\u9f99\u96c6\u56e2', u'\u4e2d\u80fd\u7535\u6c14', u'\u4e07\u987a\u80a1\u4efd', u'\u9f0e\u9f99\u80a1\u4efd', u'\u53f0\u57fa\u80a1\u4efd', u'\u534e\u529b\u521b\u901a', u'\u4e5d\u6d32\u7535\u6c14', u'\u4e2d\u79d1\u7535\u6c14', u'\u94a2\u7814\u9ad8\u7eb3', u'\u540c\u82b1\u987a', u'\u4e2d\u5143\u80a1\u4efd', u'\u4ebf\u7eac\u9502\u80fd', u'\u7acb\u601d\u8fb0', u'\u5929\u6d77\u9632\u52a1'])
    df = df.sort_values(by='percent',ascending=[0])
    print df[:10],len(df)
    # get_wencai_Market_url()
    sys.exit()