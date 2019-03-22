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
import os
import time

import pandas as pd
sys.path.append("..")
# import JohnsonUtil.johnson_cons as ct
from JohnsonUtil import LoggerFactory
from JohnsonUtil import commonTips as cct
from JohnsonUtil import johnson_cons as ct
# try:
#     from urllib.request import urlopen, Request
# except ImportError:
#     from urllib2 import urlopen, Request

# log=LoggerFactory.getLogger('wencaiData')
log = LoggerFactory.log
# curl 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=index_rewrite&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E9%9B%84%E5%AE%89' -H 'Cookie: v=AZaxA_wZ09rYlOd-tO91dApK4U2ZN9pxLHsO1QD_gnkUwzj_aMcqgfwLXuTQ'

import requests
from lxml import etree
def post_login(login_url='http://upass.10jqka.com.cn/login',header=None,url=None):
	res_keep=requests.Session()#保持Cookie不变，然后再次访问这个页面
	ex_html=res_keep.get(login_url,headers=header).text
	html=etree.HTML(ex_html)
	value=html.xpath('//div[@class="box"]/form/input/@value')
	postData = {
		'act': "login_submit",
		'isiframe': "1",
		'view': "iwc_quick",
		'rsa_version': "default_2",
		'redir': "http://www.iwencai.com/user/pop-logined",
		'uname': "OuY03m5D1ojuPmpTAbgkpcm0dod5fMbU8jVOwd17WCPEW0pz52RyEcXU+2ZLiBmP+5jckGeUR5ba/fDjkUaPVaisn9Je4l7+JPv3iX/VS4erW25ueJEoVszK9kM3oF2mT3lraObawMclBteFcfwWHyWhsW7YmN19cgOdsQWWWno=",
		'passwd': "IVORnBZ0Pdi+ix+ehVqiCdYTWCkGBy/kYEeTyTmi+5QBiL8SvYZZg3LLVzzfeMbOWaR/rK4Aoc80kSpqCIETfN3EmhA1CKK9ukI0TImlm8ASlqqz/lUq0lm5LwuMRdBjcD3hoP4RnvDc+W2+ng4XA31YsG6pBo+YF5IHcIxaScU=",
		'captchaCode': "",
		'longLogin': "on",
		}
	getData = {
		'v': 'AZaxA_wZ09rYlOd-tO91dApK4U2ZN9pxLHsO1QD_gnkUwzj_aMcqgfwLXuTQ'
		}

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Connection': 'keep-alive', 'v': 'AZaxA_wZ09rYlOd-tO91dApK4U2ZN9pxLHsO1QD_gnkUwzj_aMcqgfwLXuTQ'}
	wencairoot = 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%s'
	url = wencairoot % ('中国联通')			
	res_post=res_keep.post(login_url,data=postData,headers=header)#使用构建好的postdata重新登录发送post请求,用之前的res_keep进行post请求

	respond=res_keep.get(url,headers=header).text#获取到成绩页面源代码,用之前的res_keep进行get请求
	return respond


def post_login2(root='http://upass.10jqka.com.cn/login', url=None):
    import urllib2
    import urllib
    postData = {
        'act': "login_submit",
        'isiframe': "1",
        'view': "iwc_quick",
        'rsa_version': "default_2",
        'redir': "http://www.iwencai.com/user/pop-logined",
        'uname': "OuY03m5D1ojuPmpTAbgkpcm0dod5fMbU8jVOwd17WCPEW0pz52RyEcXU+2ZLiBmP+5jckGeUR5ba/fDjkUaPVaisn9Je4l7+JPv3iX/VS4erW25ueJEoVszK9kM3oF2mT3lraObawMclBteFcfwWHyWhsW7YmN19cgOdsQWWWno=",
        'passwd': "IVORnBZ0Pdi+ix+ehVqiCdYTWCkGBy/kYEeTyTmi+5QBiL8SvYZZg3LLVzzfeMbOWaR/rK4Aoc80kSpqCIETfN3EmhA1CKK9ukI0TImlm8ASlqqz/lUq0lm5LwuMRdBjcD3hoP4RnvDc+W2+ng4XA31YsG6pBo+YF5IHcIxaScU=",
        'captchaCode': "",
        'longLogin': "on",
    }
    getData = {
        'v': 'AZaxA_wZ09rYlOd-tO91dApK4U2ZN9pxLHsO1QD_gnkUwzj_aMcqgfwLXuTQ'
    }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive', 'v': 'AZaxA_wZ09rYlOd-tO91dApK4U2ZN9pxLHsO1QD_gnkUwzj_aMcqgfwLXuTQ'}
    from cookielib import CookieJar
    # cookie = CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    cookie = CookieJar()
    #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler=urllib2.HTTPCookieProcessor(cookie)
    #通过handler来构建opener
    opener = urllib2.build_opener(handler)
    #此处的open方法同urllib2的urlopen方法，也可以传入request
    # response = opener.open(root)
    # for item in cookie:
	   #  print 'Name = '+item.name
	   #  print 'Value = '+item.value
    # import ipdb;ipdb.set_trace()

    data_encoded = urllib.urlencode(postData).encode()
    # data_encoded = urllib.parse.urlencode(postData).encode()
    # url = 'http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s'
    # url = 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=index_rewrite&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s'
    wencairoot = 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%s'
    url = wencairoot % ('中国联通')
    # for ck in cookie:
        # print ck
    # print ":"
    try:
        response = opener.open(root, data_encoded)
        content = response.read()
        # count = re.findall('\[[A-Za-z].*\]', data, re.S)
        status = response.getcode()
        for ck in cookie:
            print ck
        print "\t:"
        # cookie["session"]["u_name_wc"] = "mx_149958484"

        import ipdb;ipdb.set_trace()

        if status == 200:
            # response = opener.open(url, data=headers)
            response = opener.open(url)
            page = response.read()
            print page
#            for ck in cookie:
#                print ck
    except urllib2.HTTPError, e:
        print e.code
    # f= response.read().decode("utf8")
    # outfile =open("rel_ip.txt","w")
    # print >> outfile , "%s"   % ( f)
    # 打印响应的信息
    # info = response.info()
    # print info
    # get_wencai_Market_url(url=None)


def retry_post_data(root='http://upass.10jqka.com.cn/login', key='国企改革'):
    url = 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=index_rewrite&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s'
    urldata = url % (key)
    import urllib2
    import urllib
    # postData = {
    # 'act':"login_submit",
    # 'isiframe':"1",
    # 'view':"iwc_quick",
    # 'rsa_version':"default_2",
    # 'redir':"http://www.iwencai.com/user/pop-logined",
    # 'uname':"OuY03m5D1ojuPmpTAbgkpcm0dod5fMbU8jVOwd17WCPEW0pz52RyEcXU+2ZLiBmP+5jckGeUR5ba/fDjkUaPVaisn9Je4l7+JPv3iX/VS4erW25ueJEoVszK9kM3oF2mT3lraObawMclBteFcfwWHyWhsW7YmN19cgOdsQWWWno=",
    # 'passwd':"IVORnBZ0Pdi+ix+ehVqiCdYTWCkGBy/kYEeTyTmi+5QBiL8SvYZZg3LLVzzfeMbOWaR/rK4Aoc80kSpqCIETfN3EmhA1CKK9ukI0TImlm8ASlqqz/lUq0lm5LwuMRdBjcD3hoP4RnvDc+W2+ng4XA31YsG6pBo+YF5IHcIxaScU=",
    # 'captchaCode':"",
    # 'longLogin':"on",
    # }
    # getData = {
    #  'v':'AZaxA_wZ09rYlOd-tO91dApK4U2ZN9pxLHsO1QD_gnkUwzj_aMcqgfwLXuTQ'
    # }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': 'keep-alive', 'v': 'AZaxA_wZ09rYlOd-tO91dApK4U2ZN9pxLHsO1QD_gnkUwzj_aMcqgfwLXuTQ'}
    from cookielib import CookieJar
    cj = CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # data_encoded = urllib.urlencode(postData)
    # url = 'http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s'

    for ck in cj:
        print ck
    print ":"
    try:
        response = opener.open(root, data_encoded)
        content = response.read()
        # count = re.findall('\[[A-Za-z].*\]', data, re.S)
        status = response.getcode()
        for ck in cj:
            print ck
        print "\t:"
        # cj["session"]["u_name_wc"] = "mx_149958484"
        if status == 200:
            response = opener.open(url, data=headers)
            page = response.read()
            print page
#            for ck in cj:
#                print ck
    except urllib2.HTTPError, e:
        print e.code
    # f= response.read().decode("utf8")
    # outfile =open("rel_ip.txt","w")
    # print >> outfile , "%s"   % ( f)
    # 打印响应的信息
    # info = response.info()
    # print info
    # get_wencai_Market_url(url=None)


import js2py
import string


def js2py_test(url):
    # jsurl = 'http://s.thsi.cn/js/chameleon/chameleon.min.1515059.js'
    jsurl = 'http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E5%9B%BD%E4%BC%81%E6%94%B9%E9%9D%A9'
    x = """pyimport urllib;
           var result = urllib.urlopen('%s').read();
           console.log(result)
           console.log(result.length)
        """ % (jsurl)
    js2py.eval_js(x)


global null, wencai_count, pct_status
pct_status = True
config_ini = cct.get_ramdisk_dir() + os.path.sep + 'h5config.txt'
fname = 'wencai_count'
null = None
wencai_count = cct.get_config_value_wencai(config_ini, fname)
# wencai_count = cct.get_config_value_wencai(config_ini,fname,1,update=True)

# cct.get_config_value_wencai(config_ini,fname)


def get_wencai_Market_url(filter='国企改革', perpage=1, url=None, pct=False, monitor=False,):
    urllist = []
    if len(filter) == 0 :
         log.error('filter is %s'%(filter))
         return pd.DataFrame()
    if len(filter) > 2 and len(filter.split(',')) < 2:
    # if isinstance(filter.split(','), str):
    	filter = '题材是%s'%(filter)
    global null, wencai_count, pct_status
    if pct is not None:
        pct_status = pct
    df = pd.DataFrame()

    # if ((pct_status) or  ( pct_status and not(925 < cct.get_now_time_int() < ct.wencai_end_time)) ) and url == None and cct.get_config_value_wencai(config_ini,fname) < 1:
    
    if wencai_count < 1 and (monitor or ((pct_status) or (not pct_status and (925 < cct.get_now_time_int() < ct.wencai_end_time))) and url == None and cct.get_config_value_wencai(config_ini, fname) < 1):
        time_s = time.time()
        duratime = cct.get_config_value_wencai(
            config_ini, fname, currvalue=time_s, xtype='time', update=False)
        if duratime < ct.wencai_delay_time:
            sleep_t = ct.wencai_delay_time - duratime
            log.error('timelimit:%s' % (sleep_t))
            time.sleep(sleep_t)
        log.info("duratime:%s", duratime)
        duratime = cct.get_config_value_wencai(
            config_ini, fname, currvalue=time.time(), xtype='time', update=True)
        # wencairoot = 'http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s'
        wencairoot = 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%s'
        url = wencairoot % (filter)
        log.debug("url:%s" % (url))
        # url = ct.get_url_data_R % (market)

        cache_root = "http://www.iwencai.com/stockpick/cache?token=%s&p=1&perpage=%s&showType="
        cache_ends = "[%22%22,%22%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22]"
#        url="http://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E6%9C%89%E8%89%B2+%E7%85%A4%E7%82%AD"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Connection': 'keep-alive',
                   'Cookie': 'v=AZaxA_wZ09rYlOd-tO91dApK4U2ZN9pxLHsO1QD_gnkUwzj_aMcqgfwLXuTQ', }
        data = cct.get_url_data(url, retry_count=1, headers=headers)

        if data is None or (len(data) < 10 or len(re.findall('系统判断您访问次数过多'.decode('utf8'), data))):
            wencai_count += 1
            cct.get_config_value_wencai(
                config_ini, fname, currvalue=wencai_count, update=True)
            # log.error("acces deny:%s %s"%('系统判断您访问次数过多',data))
            log.error("acces deny:%s %s" % ('系统判断您访问次数过多', url))
            return df
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
        log.info("net time:%s" % (time.time() - time_s))

        if len(count) == 1:
            cacheurl = cache_root % (count[0], perpage)
            cacheurl = cacheurl + cache_ends
            headers['Referer'] = cacheurl
            log.info(cacheurl)
            time_s = time.time()

            if perpage > 1000:
                html = cct.get_url_data(
                    cacheurl, retry_count=1, headers=headers, timeout=30)
            else:
                html = cct.get_url_data(
                    cacheurl, retry_count=1, headers=headers, timeout=10)
            # js2py_test(cacheurl)

            # count = re.findall('"(\d{6})\.S', data, re.S)
            # count = re.findall('result":(\[[\D\d]+\]),"oriColPos', data, re.S)
            # count = re.findall('result":(\[[\D\d]+\]),"oriIndexID', data, re.S)
#            html = data.decode('unicode-escape')
#            html = data.decode('unicode-escape')

            # href = re.findall('(http:\/\/[\D\d]+)";', html, re.S)
            # if len(href) >0:
            #     html = cct.get_url_data(href[0])

            count = re.findall(
                '(\[\["[0-9]{6}\.S[HZ][\D\d]+\]\]),"oriIndexID', html, re.S)
            # dr = re.compile(r'<[^>]+>',re.S)
            # json_d = dr.sub('',html)
            # jsobj = json.loads(json_d)
            # atext = jsobj['data']['data']['tableTempl']
            # alist = atext.split('\n\n\n\n\n')
            # blist = alist.split('\n\n\n')

            # count = grep_stock_codes.findall(data,re.S)
            if len(count) == 0:
                log.info("count: len:%s url:%s" % (len(count), url))

            log.info(time.time() - time_s)
            singlecode = []
            singlelist = []
            singlelist_category = []

            # print "count:",count
            # import ipdb;ipdb.set_trace()
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
                key_t = []

                for xcode in result:
                    # print xcode
                    code_t = []
                    for x in xcode:
                        # print x
                        if isinstance(x, list):
                            # print "list:",x
                            key_t = []
                            for y in x:
                                if isinstance(y, dict):
                                    # pass
                                    keylist = ['URL', 'PageRawTitle']
                                    for key in y.keys():
                                        if key in keylist:
                                            if key == 'URL':
                                                urls = str(y[key]).replace(
                                                    '\\', '').strip().decode('unicode-escape')
                                                if urls[-20] not in urllist:
                                                    urllist.append(urls[-20])
                                                    log.info(urls),
#                                                    log.info( urls)
                                                else:
                                                    break
                                            else:
                                                urls = str(y[key]).decode(
                                                    'unicode-escape')
                                                key_t.append(urls)
#                                                key_t.append(urls)
                                                log.info(urls),
                                # else:
                                    # print str(y).decode('unicode-escape'),
                        else:
                            code_t.append(str(x).decode('unicode-escape'))
#                            code_t.append(str(x))
                            log.debug(str(x).decode('unicode-escape')),
#                            log.info(str(x)),
#                    log.info( key_t)
                    if len(code_t) > 4:
                        code = code_t[0]
                        name = code_t[1]
                        trade = code_t[2]
                        trade = '0' if trade == '--' else trade
                        percent = code_t[3]
                        percent = '0' if percent == '--' else percent

                        # index = code_t[4]
                        category = ";".join(
                            x for x in code_t[4].split(';')[:3])
                        category = category[:15] if len(
                            category) > 15 else category
                        if len(key_t) > 0:
                            # print key_t[0]
                            title1 = key_t[0]
                            if len(key_t) > 1:
                                title2 = key_t[1]
                            else:
                                title2 = None
                            dlist.append({'code': code, 'name': name, 'trade': trade, 'percent': percent,
                                          'category': category, 'tilte1': title1, 'tilte2': title2})
                        else:
                            dlist.append(
                                {'code': code, 'name': name, 'trade': trade, 'percent': percent, 'category': category})
                    # print ''
                # df = pd.DataFrame(dt_list, columns=ct.TDX_Day_columns)
                # df = pd.DataFrame(dlist, columns=['category','code','name','trade','percent','tilte1','tilte2'])
                    else:
                        if len(code_t) > 0 and code_t[0].endswith(('SZ', 'SH')):
                            singlecode.append(code_t[0].split('.')[0])
                            singlelist.append({'code': code_t[0].split(
                                '.')[0], 'name': code_t[1], 'trade': code_t[2], 'percent': code_t[3]})
                if len(singlecode) > 0:
                    # codestring = '300377%2C300363%2C300360'
                    codestring = string.join(singlecode, '%2C')
                    wencaisingleroot = 'http://www.iwencai.com/diag/block-detail?pid=8153&codes=%s'
                    end_root = '&codeType=stock&info=%7B%22view%22%3A%7B%22nolazy%22%3A1%2C%22parseArr%22%3A%7B%22_v%22%3A%22new%22%2C%22dateRange%22%3A%5B%5D%2C%22staying%22%3A%5B%5D%2C%22queryCompare%22%3A%5B%5D%2C%22comparesOfIndex%22%3A%5B%5D%7D%2C%22asyncParams%22%3A%7B%22tid%22%3A137%7D%7D%7D'
                    wencaisingleurl = wencaisingleroot % (
                        codestring) + end_root
                    html_json = cct.get_url_data(
                        wencaisingleurl, retry_count=1, headers=headers, timeout=10)
                    dr = re.compile(r'<[^>]+>', re.S)
                    json_d = dr.sub('', html_json)
                    jsobj = json.loads(json_d)
                    # import ipdb;ipdb.set_trace()
                    atext = jsobj['data']['data']['tableTempl']
                    alist = atext.split('\n\n\n\n\n')
                    alist_data = alist[1:]
                    for al in alist_data:
                        blist = al.split('\n\n\n')
                        if len(blist) > 0:
                            sin_category = blist[-1].replace(
                                u'\u66f4\u591a', '')
                            for code in singlelist:
                                if code['code'] == blist[0].split('\n')[-1]:
                                    sin_category = ";".join(
                                        x for x in sin_category.split(';')[:3])
                                    sin_category = sin_category[:15] if len(
                                        sin_category) > 15 else sin_category
                                    code['category'] = sin_category
                                    singlelist_category.append(code)
                                    break
                if len(dlist) == 0:
                    if len(singlelist_category) > 0:
                        dlist = singlelist_category
                df = pd.DataFrame(dlist, columns=[
                                  'code', 'name', 'trade', 'percent', 'category', 'tilte1', 'tilte2'])
                # if len(dlist) > 0 and 'tilte1' in (dlist[0].keys()) :
                #     df = pd.DataFrame(dlist, columns=['code','name','trade','percent','category','tilte1','tilte2'])
                # else:
                #     df = pd.DataFrame(dlist, columns=['code','name','trade','percent','category'])
                df['code'] = (map(lambda x: x[:6], df['code']))
                if len(df) > 0:
                    df.percent = df.percent.astype(float)
                    df = df.sort_values(by='percent', ascending=[0])
                # df = df.set_index('code')
            # print type(count[0])
            # print type(list(count[0]))
            # print count[0].decode('unicode-escape')

            if len(df) == 0:
                log.error('df 0 filter:%s df is None:%s' % (filter,url))
        else:
            log.error('count is 0')

    return df


def get_codelist_df(codelist):
    wcdf = pd.DataFrame()
    time_s = time.time()
    if len(codelist) > 30:
        # num=int(len(codeList)/cpu_count())
        div_list = cct.get_div_list(codelist, int(len(codelist) / 30 + 1))
        # print "ti:",time.time()-time_s
#        cnamelist =[]
        for li in div_list:
            cname = ",".join(x.encode('utf8') for x in li)
#            cnamelist.append(cname)
            wcdf_t = get_wencai_Market_url(cname, len(li))
            wcdf = wcdf.append(wcdf_t)
#        results = cct.to_mp_run_async(get_wencai_Market_url, cnamelist,30)
#        for res in results:
#            wcdf = wcdf.append(res)
        print ("Wcai:%.2f" % (time.time() - time_s)),
        # print results
    else:
        cname = ",".join(x.encode('utf8') for x in codelist)
        wcdf = get_wencai_Market_url(cname, len(codelist))
#        wcdf = wcdf.append(wcdf_t)
    if len(wcdf) != len(codelist):
        log.warn("wcdf:%s" % (len(wcdf)))
    return wcdf


def get_wencai_data(dm, market='wencai', days=120, pct=True):
    #    if isinstance(codelist,list):
    global wencai_count
    global pct_status
    pct_status = pct

    if len(dm) > 1:
        # code_l = []
        # wcd_o = get_write_wencai_market_to_csv(market=market)
        # for co in codelist:
        #     if co not in wcd_o.code.values:
        #         code_l.append(co)
        # if len(code_l) > 0:
        #     wcd_d = get_codelist_df(code_l)
        #     get_write_wencai_market_to_csv(wcd_d,market=market)

        df = get_write_wencai_market_to_csv(
            None, market, renew=True, days=days)
        if df is not None and len(df) > 0:
            #            if  set(codelist) <= set(df.name.values):
            #            if  set(dm.index) <= set(df.code.values) :
            #            if  len(dm) - len(set(dm.index) & set(df.index.values)) < 10 :
            # drop_cxg = cct.GlobalValues().getkey('dropcxg')
            wencai_drop = cct.GlobalValues().getkey('wencai_drop')

            if wencai_drop is not None and len(wencai_drop) > 3:
                return_status = True
            else:
                return_status = False

            dratio = cct.get_diff_dratio(df.index, dm.index)
            # if return_status or dratio < 0.01:
            if return_status:
                if 'code' in df.columns:
                    df = df.set_index('code')
                    df = df.drop_duplicates()
                return df
            else:
                # diffcode = map( lambda x: x,set(dm.index) - (set(dm.index) & set(df.code.values)))
                diff_code = [x for x in set(
                    dm.index) - (set(dm.index) & set(df.index.values))]
                dm.drop([col for col in dm.index if col not in diff_code],
                        axis=0, inplace=True)

    # if len(drop_cxg) >0:
                # for x in diff_code:
                #     if not x in df.code.values:
                #         print x,dm[x],

        if wencai_count < 1:
            # if (pct and cct.get_now_time_int() < 940) or not pct:
            wcd_d = get_codelist_df(dm.tolist())
            if wcd_d is not None and len(wcd_d) > 0:
                log.error("dratio:%s diff:%s dm:%s err:%s" %
                          (dratio, len(diff_code), len(dm), wencai_count))
                df = get_write_wencai_market_to_csv(
                    wcd_d, market=market, renew=True, days=days)
        # else:
            # dm['category'] = 0

    else:
        df = get_wencai_Market_url(dm.name)
    if df is not None and 'code' in df.columns:
        df = df.set_index('code')
    if df is not None and len(df) > 1:
        df = df.drop_duplicates()
        df['category'] = df['category'].apply(lambda x:str(x).replace('\n',''))

    return df


def get_wencai_filepath(market):
    path_sep = os.path.sep
    baser = os.getcwd().split('stock')[0]
    base = baser + path_sep + 'stock' + path_sep + \
        'JohnsonUtil' + path_sep + 'wencai' + path_sep
    filepath = base + market + '.csv'
    return filepath


def get_write_wencai_market_to_csv(df=None, market='wcbk', renew=False, days=60):

    def wencaiwrite_to_csv(df, filename, renew=False):
        if df is None or len(df) == 0:
            log.warn("df is write None")
        else:
            # category = ";".join(x for x in code_t[4].split(';')[:3])
            # category = category[:15] if len(category) > 15 else category
            if 'category' in df.columns:
                df = df.fillna('--')
                df = df[~(df.category == '--')]
                # df['category'] = (map(lambda x: ';'.join(str(x).split(';')[:3]),df['category']))
        if df is not None and len(df) > 0 and 'code' in df.columns:
            df.drop_duplicates('code', inplace=True)
            df = df.set_index('code')

            if 'category' in df.columns and (str(df[:1].category.values).find(';') > 0 or len((df[:1].category.values) == 0)):
                if not renew and os.path.exists(filepath):
                    df.to_csv(filename, mode='a',
                              encoding='utf8', header=False)
                else:
                    df.to_csv(filename, mode='w', encoding='utf8')
        else:
            # log.warn("df.columns:%s"%(df))
            return df
#        log.warn("Wr%s :%s"%(market,len(df)))
        print ("wencaimarket :%s" % (len(df))),
        # df.reset_index(inplace=True)
        return df

    filepath = get_wencai_filepath(market)
    if os.path.exists(filepath):

        if df is not None and len(df) > 10 and isinstance(df, pd.DataFrame) and renew and cct.creation_date_duration(filepath) > days:
            df = wencaiwrite_to_csv(df, filepath, renew)
        else:
            dfz = pd.read_csv(filepath, dtype={'code': str}, encoding='utf8')
            # re.match('[ \u4e00 -\u9fa5]+',code)

            # if 'category' in dfz.columns:
            #     # dfz = dfz.fillna('--')
            #     dfz['category'] = dfz['category'].apply(lambda x: x if len(str(x)) > 8 else '---')
            #     # dfz = dfz[~(dfz.category == '--')]
            #     dfzcount = len(dfz[~(dfz.category == '---')])
            # else:
            #     dfzcount = len(dfz)
            dfzcount = len(dfz)
            dfdrop = dfz.drop_duplicates()
            if dfzcount <> len(dfdrop):
                wencaiwrite_to_csv(dfdrop, filepath, True)
                dfz = dfdrop
            if isinstance(df, pd.DataFrame) and len(df) > 0 and len(dfz) != len(df):
                #                if 'category' in df.columns and str(df[:1].category.values).find(';') > 0:
                if 'category' in df.columns and (str(df[:1].category.values).find(';') > 0 or len((df[:1].category.values) == 0)):
                    dd = pd.DataFrame()
                    for code in df.code.values:
                        if not code in dfz.code.values:
                            dd = dd.append(df[df.code == code])
                    if len(dd) > 0:
                        wencaiwrite_to_csv(dd, filepath)
                        df = pd.read_csv(filepath, dtype={
                                         'code': str}, encoding='utf8')
                    else:
                        df = dfz

            else:
                df = dfz
            # df = pd.read_csv(filepath,dtype={'code':str})
#            if len(df) == 0:
#                df = wencaiwrite_to_csv(df, filepath)
    else:
        df = wencaiwrite_to_csv(df, filepath)
    if df is not None and len(df) > 1:
        df = df.drop_duplicates()
    else:
        log.error('wencaiErr:%s' % (market))
    if df is not None and 'code' in df.columns:
        df = df.set_index('code')
        if 'category' in df.columns:
            df = df.fillna('--')
            df['category'] = (map(lambda x: ';'.join(
                str(x).split(';')[:3]), df['category']))
            df['category'] = df['category'].apply(lambda x:str(x).replace('\n',''))
    return df


def get_wcbk_df(filter='混改', market='nybk', perpage=1000, days=120, monitor=False):
    fpath = get_wencai_filepath(market)
    # import pdb; pdb.set_trace()

    if os.path.exists(fpath) and os.path.getsize(fpath) > 200 and 0 <= cct.creation_date_duration(fpath) <= days:
        df = get_write_wencai_market_to_csv(
            None, market, renew=True, days=days)
    else:
        df = get_wencai_Market_url(filter, perpage, monitor=monitor)
        df = get_write_wencai_market_to_csv(df, market, renew=True, days=days)
    if 'code' in df.columns:
        df = df.set_index('code')
    return df


def wencaisinglejson():
    jsonda = r'''{"success":true,"message":"","data":{"show_type":"table","data":{"titleProcess":[[],[],[],[],[],[]],"staticList":0,"isNoSeq":true,"normalCodes":["300377","300363","300360"],"block_title":"\u57fa\u672c\u6982\u51b5","tableTempl":"<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:975px;\">\n<thead>\n<tr>\n<th>\n<span\n                                    class=\"th_words\">\u80a1\u7968\u4ee3\u7801<\/span><\/th>\n<th>\n<span\n                                    class=\"th_words\">\u80a1\u7968\u7b80\u79f0<\/span><\/th>\n<th>\n<span\n                                    class=\"th_words\">\u6240\u5c5e\u884c\u4e1a<\/span><\/th>\n<th>\n<span\n                                    class=\"th_words\">\u57ce\u5e02<\/span><\/th>\n<th>\n<span\n                                    class=\"th_words\">\u4e3b\u8425\u4ea7\u54c1\u540d\u79f0<\/span><\/th>\n<th>\n<span\n                                    class=\"th_words\">\u6240\u5c5e\u6982\u5ff5<\/span><\/th>\n<\/tr>\n<\/thead>\n<tbody>\n<tr class=\"even_row\">\n<td width=\"66\" colnum=\"0\"\n                            class=\"item\">\n<div class=\"em\">300363<\/div>\n<\/td>\n<td width=\"67\" colnum=\"1\"\n                            class=\"item\">\n<div class=\"em alignCenter graph\"><a target=\"_blank\" href=\"\/stockpick\/search?tid=stockpick&qs=stockpick_diag&ts=1&w=300363\">\u535a\u817e\u80a1\u4efd<\/a><\/div>\n<\/td>\n<td width=\"79\" colnum=\"2\"\n                            class=\"item\">\n<div class=\"em\"><a target=\"_blank\" href=\"http:\/\/www.iwencai.com\/stockpick\/search?typed=0&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E5%90%8C%E8%8A%B1%E9%A1%BA%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E5%8C%85%E5%90%AB%E5%8C%96%E5%AD%A6%E5%88%B6%E8%8D%AF\">\u5316\u5b66\u5236\u836f<\/a><\/div>\n<\/td>\n<td width=\"55\" colnum=\"3\"\n                            class=\"item\">\n<div class=\"em alignLeft\"><a target=\"_blank\" href=\"\/stockpick\/search?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E5%9F%8E%E5%B8%82%E4%B8%BA%E9%95%BF%E5%AF%BF%E5%8C%BA\" substr=\"\u957f\u5bff\u533a\" fullstr=\"\u957f\u5bff\u533a\" title=\"\u957f\u5bff\u533a\">\u957f\u5bff\u533a<\/a><\/div>\n<\/td>\n<td width=\"309\" colnum=\"4\"\n                            class=\"item sortCol\">\n<div class=\"em split\"><a href=\"\" class=\"ml5 moreSplit fr\" num=\"1\">\u66f4\u591a<\/a><span class=\"fl\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E7%99%8C\">\u6297\u764c<\/a>\u3011;<\/span><span class=\"fl\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E8%89%BE%E6%BB%8B%E7%97%85\">\u6297\u827e\u6ecb\u75c5<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E4%B8%99%E5%9E%8B%E8%82%9D%E7%82%8E\">\u6297\u4e19\u578b\u809d\u708e<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E8%8F%8C\">\u6297\u83cc<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E7%96%9F%E7%96%BE\">\u6297\u759f\u75be<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E7%B3%96%E5%B0%BF%E7%97%85\">\u6297\u7cd6\u5c3f\u75c5<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%BA%BB%E9%86%89%E5%9E%8B%E9%95%87%E7%97%9B\">\u9ebb\u9189\u578b\u9547\u75db<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%99%8D%E8%A1%80%E8%84%82\">\u964d\u8840\u8102<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E5%8C%BB%E8%8D%AF%E4%B8%AD%E9%97%B4%E4%BD%93\">\u533b\u836f\u4e2d\u95f4\u4f53<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E4%B8%AD%E9%97%B4%E4%BD%93\">\u4e2d\u95f4\u4f53<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%87%8D%E7%A3%85%E8%8D%AF%E7%89%A9\">\u91cd\u78c5\u836f\u7269<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E7%97%85%E6%AF%92%E8%8D%AF\">\u6297\u75c5\u6bd2\u836f<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E7%B3%96%E5%B0%BF%E7%97%85%E8%8D%AF\">\u6297\u7cd6\u5c3f\u75c5\u836f<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%99%8D%E8%A1%80%E8%84%82%E8%8D%AF\">\u964d\u8840\u8102\u836f<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E7%99%8C%E8%8D%AF\">\u6297\u764c\u836f<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%BA%BB%E9%86%89%E5%9E%8B%E9%95%87%E7%97%9B%E8%8D%AF\">\u9ebb\u9189\u578b\u9547\u75db\u836f<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%8A%97%E8%8F%8C%E8%8D%AF\">\u6297\u83cc\u836f<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E5%85%B6%E4%BB%96%E8%8D%AF\">\u5176\u4ed6\u836f<\/a>\u3011<\/span><\/div>\n<\/td>\n<td width=\"314\" colnum=\"5\"\n                            class=\"item\">\n<div class=\"em alignCenter split\"><a href=\"\" class=\"ml5 moreSplit fr\" num=\"3\">\u66f4\u591a<\/a><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E7%94%9F%E7%89%A9%E5%8C%BB%E8%8D%AF\">\u751f\u7269\u533b\u836f<\/a> ;<\/span><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E5%BA%9F%E5%93%81%E5%9B%9E%E6%94%B6\">\u5e9f\u54c1\u56de\u6536<\/a> ;<\/span><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E6%B7%B1%E8%82%A1%E9%80%9A\">\u6df1\u80a1\u901a<\/a> ;<\/span><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E5%88%9B%E6%96%B0%E8%8D%AF\">\u521b\u65b0\u836f<\/a> ;<\/span><span class=\"fl hidden\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E6%8A%97%E8%89%BE%E6%BB%8B%E7%97%85\">\u6297\u827e\u6ecb\u75c5<\/a>\n<\/span><\/div>\n<\/td>\n<\/tr>\n<tr class=\"odd_row\">\n<td width=\"66\" colnum=\"0\"\n                            class=\"item\">\n<div class=\"em\">300377<\/div>\n<\/td>\n<td width=\"67\" colnum=\"1\"\n                            class=\"item\">\n<div class=\"em alignCenter graph\"><a target=\"_blank\" href=\"\/stockpick\/search?tid=stockpick&qs=stockpick_diag&ts=1&w=300377\">\u8d62\u65f6\u80dc<\/a><\/div>\n<\/td>\n<td width=\"79\" colnum=\"2\"\n                            class=\"item\">\n<div class=\"em\"><a target=\"_blank\" href=\"http:\/\/www.iwencai.com\/stockpick\/search?typed=0&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E5%90%8C%E8%8A%B1%E9%A1%BA%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E5%8C%85%E5%90%AB%E8%AE%A1%E7%AE%97%E6%9C%BA%E5%BA%94%E7%94%A8\">\u8ba1\u7b97\u673a\u5e94\u7528<\/a><\/div>\n<\/td>\n<td width=\"55\" colnum=\"3\"\n                            class=\"item\">\n<div class=\"em alignLeft\"><a target=\"_blank\" href=\"\/stockpick\/search?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E5%9F%8E%E5%B8%82%E4%B8%BA%E6%B7%B1%E5%9C%B3%E5%B8%82\" substr=\"\u6df1\u5733\u5e02\" fullstr=\"\u6df1\u5733\u5e02\" title=\"\u6df1\u5733\u5e02\">\u6df1\u5733\u5e02<\/a><\/div>\n<\/td>\n<td width=\"309\" colnum=\"4\"\n                            class=\"item sortCol\">\n<div class=\"em split\"><a href=\"\" class=\"ml5 moreSplit fr\" num=\"1\">\u66f4\u591a<\/a><span class=\"fl\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%9C%8D%E5%8A%A1%E8%B4%B9\">\u670d\u52a1\u8d39<\/a>\u3011;<\/span><span class=\"fl\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E5%AE%9A%E5%88%B6%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91\">\u5b9a\u5236\u8f6f\u4ef6\u5f00\u53d1<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E5%AE%9A%E5%88%B6%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91%E5%92%8C%E9%94%80%E5%94%AE%E4%B8%9A%E5%8A%A1\">\u5b9a\u5236\u8f6f\u4ef6\u5f00\u53d1\u548c\u9500\u552e\u4e1a\u52a1<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%87%91%E8%9E%8D%E8%BD%AF%E4%BB%B6\">\u91d1\u878d\u8f6f\u4ef6<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E8%B5%84%E4%BA%A7%E7%AE%A1%E7%90%86%E4%B8%9A%E5%8A%A1\">\u8d44\u4ea7\u7ba1\u7406\u4e1a\u52a1<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E8%B5%84%E4%BA%A7%E7%AE%A1%E7%90%86%E8%BD%AF%E4%BB%B6\">\u8d44\u4ea7\u7ba1\u7406\u8f6f\u4ef6<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E8%B5%84%E4%BA%A7%E6%89%98%E7%AE%A1%E8%BD%AF%E4%BB%B6\">\u8d44\u4ea7\u6258\u7ba1\u8f6f\u4ef6<\/a>\u3011<\/span><\/div>\n<\/td>\n<td width=\"314\" colnum=\"5\"\n                            class=\"item\">\n<div class=\"em alignCenter split\"><a href=\"\" class=\"ml5 moreSplit fr\" num=\"3\">\u66f4\u591a<\/a><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E4%BA%92%E8%81%94%E7%BD%91%E9%87%91%E8%9E%8D\">\u4e92\u8054\u7f51\u91d1\u878d<\/a> ;<\/span><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD\">\u4eba\u5de5\u667a\u80fd<\/a> ;<\/span><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E7%A5%A8%E4%BA%A4%E6%89%80\">\u7968\u4ea4\u6240<\/a> ;<\/span><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E5%9B%BD%E4%BA%A7%E6%9B%BF%E4%BB%A3\">\u56fd\u4ea7\u66ff\u4ee3<\/a> ;<\/span><span class=\"fl hidden\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E9%87%91%E8%9E%8D%E7%A7%91%E6%8A%80\">\u91d1\u878d\u79d1\u6280<\/a> ;<\/span><span class=\"fl hidden\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E6%B7%B1%E8%82%A1%E9%80%9A\">\u6df1\u80a1\u901a<\/a> ;<\/span><span class=\"fl hidden\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E5%8C%BA%E5%9D%97%E9%93%BE\">\u533a\u5757\u94fe<\/a> ;<\/span><span class=\"fl hidden\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E5%8C%BA%E5%9D%97%E9%93%BE%E5%82%A8%E5%A4%87\">\u533a\u5757\u94fe\u50a8\u5907<\/a>\n<\/span><\/div>\n<\/td>\n<\/tr>\n<tr class=\"even_row\">\n<td width=\"66\" colnum=\"0\"\n                            class=\"item\">\n<div class=\"em\">300360<\/div>\n<\/td>\n<td width=\"67\" colnum=\"1\"\n                            class=\"item\">\n<div class=\"em alignCenter graph\"><a target=\"_blank\" href=\"\/stockpick\/search?tid=stockpick&qs=stockpick_diag&ts=1&w=300360\">\u70ac\u534e\u79d1\u6280<\/a><\/div>\n<\/td>\n<td width=\"79\" colnum=\"2\"\n                            class=\"item\">\n<div class=\"em\"><a target=\"_blank\" href=\"http:\/\/www.iwencai.com\/stockpick\/search?typed=0&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E5%90%8C%E8%8A%B1%E9%A1%BA%E4%BA%8C%E7%BA%A7%E8%A1%8C%E4%B8%9A%E5%8C%85%E5%90%AB%E7%94%B5%E6%B0%94%E8%AE%BE%E5%A4%87\">\u7535\u6c14\u8bbe\u5907<\/a><\/div>\n<\/td>\n<td width=\"55\" colnum=\"3\"\n                            class=\"item\">\n<div class=\"em alignLeft\"><a target=\"_blank\" href=\"\/stockpick\/search?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E5%9F%8E%E5%B8%82%E4%B8%BA%E6%9D%AD%E5%B7%9E%E5%B8%82\" substr=\"\u676d\u5dde\u5e02\" fullstr=\"\u676d\u5dde\u5e02\" title=\"\u676d\u5dde\u5e02\">\u676d\u5dde\u5e02<\/a><\/div>\n<\/td>\n<td width=\"309\" colnum=\"4\"\n                            class=\"item sortCol\">\n<div class=\"em split\"><a href=\"\" class=\"ml5 moreSplit fr\" num=\"1\">\u66f4\u591a<\/a><span class=\"fl\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E4%B8%89%E7%9B%B8%E7%94%B5%E5%AD%90%E5%BC%8F%E7%94%B5%E8%83%BD%E8%A1%A8\">\u4e09\u76f8\u7535\u5b50\u5f0f\u7535\u80fd\u8868<\/a>\u3011;<\/span><span class=\"fl\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E5%8D%95%E7%9B%B8%E6%99%BA%E8%83%BD%E7%94%B5%E8%83%BD%E8%A1%A8\">\u5355\u76f8\u667a\u80fd\u7535\u80fd\u8868<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E5%8D%95%E7%9B%B8%E7%94%B5%E5%AD%90%E5%BC%8F%E7%94%B5%E8%83%BD%E8%A1%A8\">\u5355\u76f8\u7535\u5b50\u5f0f\u7535\u80fd\u8868<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%87%87%E9%9B%86%E5%99%A8\">\u91c7\u96c6\u5668<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E4%B8%93%E5%8F%98%E7%BB%88%E7%AB%AF\">\u4e13\u53d8\u7ec8\u7aef<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%85%8D%E5%8F%98%E7%BB%88%E7%AB%AF\">\u914d\u53d8\u7ec8\u7aef<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%9B%86%E4%B8%AD%E5%99%A8%E7%94%B5%E8%83%BD%E8%A1%A8%E8%BD%AF%E4%BB%B6\">\u96c6\u4e2d\u5668\u7535\u80fd\u8868\u8f6f\u4ef6<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E7%94%B5%E8%83%BD%E8%AE%A1%E9%87%8F%E7%AE%B1\">\u7535\u80fd\u8ba1\u91cf\u7bb1<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E7%94%B5%E8%83%BD%E8%A1%A8%E8%BD%AF%E4%BB%B6\">\u7535\u80fd\u8868\u8f6f\u4ef6<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E9%9B%86%E4%B8%AD%E5%99%A8\">\u96c6\u4e2d\u5668<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E4%B8%89%E7%9B%B8%E6%99%BA%E8%83%BD%E7%94%B5%E8%83%BD%E8%A1%A8\">\u4e09\u76f8\u667a\u80fd\u7535\u80fd\u8868<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E7%94%B5%E8%83%BD%E8%A1%A8\">\u7535\u80fd\u8868<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90%E5%95%86\">\u7cfb\u7edf\u96c6\u6210\u5546<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E7%94%A8%E7%94%B5%E4%BF%A1%E6%81%AF%E9%87%87%E9%9B%86%E7%B3%BB%E7%BB%9F\">\u7528\u7535\u4fe1\u606f\u91c7\u96c6\u7cfb\u7edf<\/a>\u3011;<\/span><span class=\"fl hidden\">\u3010<a target=\"_blank\" href=\"\/stockpick\/search?querytype=&searchfilter=&tid=stockpick&w=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81%E5%90%8D%E7%A7%B0%E5%8C%85%E5%90%AB%E6%99%BA%E8%83%BD%E7%94%B5%E8%A1%A8\">\u667a\u80fd\u7535\u8868<\/a>\u3011<\/span><\/div>\n<\/td>\n<td width=\"314\" colnum=\"5\"\n                            class=\"item\">\n<div class=\"em alignCenter split\"><a href=\"\" class=\"ml5 moreSplit fr\" num=\"3\">\u66f4\u591a<\/a><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E7%89%A9%E8%81%94%E7%BD%91\">\u7269\u8054\u7f51<\/a> ;<\/span><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E8%83%BD%E6%BA%90%E4%BA%92%E8%81%94%E7%BD%91\">\u80fd\u6e90\u4e92\u8054\u7f51<\/a> ;<\/span><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E5%90%88%E5%90%8C%E8%83%BD%E6%BA%90%E7%AE%A1%E7%90%86\">\u5408\u540c\u80fd\u6e90\u7ba1\u7406<\/a> ;<\/span><span class=\"fl\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E5%8F%82%E8%82%A1360\">\u53c2\u80a1360<\/a> ;<\/span><span class=\"fl hidden\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E6%99%BA%E8%83%BD%E8%A1%A8\">\u667a\u80fd\u8868<\/a> ;<\/span><span class=\"fl hidden\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E6%99%BA%E8%83%BD%E7%94%B5%E7%BD%91\">\u667a\u80fd\u7535\u7f51<\/a> ;<\/span><span class=\"fl hidden\"><a target=\"_blank\" href=\"\/stockpick\/search?ts=1&f=1&qs=gnsy&querytype=&tid=stockpick&w=%E6%89%80%E5%B1%9E%E6%A6%82%E5%BF%B5%E5%8C%85%E5%90%AB%E5%BA%94%E7%94%A8%E5%B1%82\">\u5e94\u7528\u5c42<\/a>\n<\/span><\/div>\n<\/td>\n<\/tr>\n<\/tbody>\n<\/table>"},"pid":"8153","title":"\u57fa\u672c\u6982\u51b5"}}'''
    import json
    # obj = json.dumps(jsonda)
    obj = json.loads(jsonda)
    print "obj:", obj['data']
    import ipdb;ipdb.set_trace()


if __name__ == '__main__':
    # df = get_sina_all_json_dd('0', '3')
    # df=get_sina_Market_json('cyb')
    # _get_sina_json_dd_url()
    # print sina_json_Big_Count()
    # print getconfigBigCount(write=True)
    # sys.exit(0)
    log.setLevel(LoggerFactory.DEBUG)
    post_login()
    # wencaisinglejson()
    # print get_wencai_Market_url(filter='国企改革',perpage=1000,pct=True)
    # print get_wencai_Market_url(filter='国企改革',perpage=1000,pct=False)
#    df = get_wencai_Market_url('湖南发展,天龙集团,浙报传媒,中珠医疗,多喜爱',500)
#    type='TMT'
#    type='国企改革'

    df = get_wencai_Market_url('OLED',200)
    # df = get_wencai_Market_url('赢时胜,博腾股份,炬华科技',500,single=True)

    # df = get_wcbk_df(filter='OLED', market='oled')
    # df =  get_wcbk_df(filter='新股与次新股',market='cxg')
    # df =  get_wcbk_df(filter='雄安特区',market='xatq')
    # df =  get_wcbk_df(filter='新能源',market='xny')
    # df =  get_wcbk_df(filter='全部股票概念',market='wencai',perpage=4000)

    # get_wencai_data('沧州明珠', 'wencai',days='N')
    # print df.shape, df[:5]
    import ipdb;ipdb.set_trace()

    # df = get_wencai_Market_url('农业',10000)
#    df = get_write_wencai_market_to_csv(df,'wcbk')

    # df = get_wcbk_df('混改')

#    print write_wencai_market_to_csv(df)[:2]
    df = get_codelist_df(['贝通信','太阳电缆','杭州解百'])
    import ipdb;ipdb.set_trace()

    # df = get_codelist_df([u'\u7ef4\u5b8f\u80a1\u4efd', u'\u6d77\u987a\u65b0\u6750', u'\u6da6\u6b23\u79d1\u6280', u'\u84dd\u6d77\u534e\u817e', u'\u5149\u529b\u79d1\u6280'])
    # df = df.sort_values(by='percent',ascending=[0]) if len(df) > 0 else df
    # if 'percent' in df.columns:
    #     df.percent = df.percent.astype(float)
#    df = df.sort_values(by='percent',ascending=[0])

    # print "%s %s"%(type,len(df))
    # print "%s "%(df[:5])
    # import dfgui
    # dfgui.show(df)
    # get_wencai_Market_url()
    sys.exit()
