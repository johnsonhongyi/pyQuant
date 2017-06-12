# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import cookielib
import time
import re
#获取Cookiejar对象（存在本机的cookie消息）
cookie = cookielib.CookieJar()
#自定义opener,并将opener跟CookieJar对象绑定
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#安装opener,此后调用urlopen()时都会使用安装过的opener对象
urllib2.install_opener(opener)
opener.handle_open["http"][0].set_http_debuglevel(1)
# from cookielib import CookieJar
# cj = CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))





home_url = 'http://bj.lianjia.com/'
auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F'
chengjiao_url = 'http://bj.lianjia.com/chengjiao/'


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'passport.lianjia.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}
# 获取lianjia_uuid
req = urllib2.Request('http://bj.lianjia.com/')

# user_agent ="Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 BIDUBrowser/6.x Safari/537.31"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
req.add_header("User-Agent", user_agent)
# cookie ="t=*************************"#设定cookie的内容
# request.add_header("Cookie", cookie)
conn = opener.open(req)
print "info",conn.info()
feeddata = conn.read()
# print "first:",feeddata

# opener.open(req)



# 初始化表单
req = urllib2.Request(auth_url, headers=headers)
# req.add_header("User-Agent", user_agent)
result = opener.open(req)
#result = urllib2.urlopen(req)
# print(cookie)
# 获取cookie和lt值

# lianjia_uuid = ''
# for index, ck in enumerate(cookie):
#     print '[',index, ']',ck;
#     if str(ck).find('lianjia_uuid') > 0:
#         print "find"
#         pattern = re.compile(r'lianjia_uuid=(.*)')
#         # print str(ck).split()[1]
#         lianjia_uuid = pattern.findall(str(ck).split()[1])[0]
#         break

# print "uuid:",cookie['lianjia_uuid']
# print "set:",result.info().getheader('Set-Cookie').split(';')
if result.info().getheader('Set-Cookie')!=None:                               #判断是否存在Set-Cookie，有的话，将cookie保存起来
    pattern = re.compile(r'JSESSIONID=(.*)')
    jsessionid = pattern.findall(result.info().getheader('Set-Cookie').split(';')[0])[0]
else:
   print 'got no cookie'
# pattern = re.compile(r'lianjia_uuid=(.*)')
# print "UUID:",pattern.findall(result.info().getheader('lianjia_uuid'))
# print result.info().getheader('lianjia_uuid')
# html_content = urllib2.urlopen(auth_url,timeout=5).read()
# html_content = urllib2.urlopen(req).read()
# html_content = result.read()

import gzip,StringIO

compressedData = result.read()
compressedStream=StringIO.StringIO(compressedData)
gzipper=gzip.GzipFile(fileobj=compressedStream)
html_content=gzipper.read()


# print html_content[:10]
# html_content = result.read()
# print len(html_content) #unicode(html_content)
pattern = re.compile(r'value=\"(LT-.*)\"')
# print pattern.findall(html_content)
lt = pattern.findall(html_content)[0]
pattern = re.compile(r'name="execution" value="(.*)"')
execution = pattern.findall(html_content)[0]
print "lt:%s ex:%s"%(lt,execution)
# print(cookie)
# opener.open(lj_uuid_url)
# print(cookie)
# opener.open(api_url)
# print(cookie)

# data
data = {
    'username': '13901298957',
    'password': 'plokijuh',
    # 'service': 'http://bj.lianjia.com/',
    # 'isajax': 'true',
    # 'remember': 1,
    'execution': execution,
    # 'execution': 'e1s1',
    '_eventId': 'submit',
    'lt': lt,
    # 'lt': 'LT-18387201-NSAetZiXuY0TS6F4XXS9HnHFxdVSvq-www.lianjia.com',
    'verifyCode': '',
    'redirect': '',
}
# urllib进行编码
post_data=urllib.urlencode(data)
# header
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Content-Length': '152',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'passport.lianjia.com',
    'Origin': 'https://passport.lianjia.com',
    'Pragma': 'no-cache',
    'Referer': 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest',
}

headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'bj.lianjia.com',
    'Pragma': 'no-cache',
    'Referer': 'https://passport.lianjia.com/cas/xd/api?name=passport-lianjia-com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}
req = urllib2.Request(auth_url, post_data, headers)
# req.add_header("User-Agent", user_agent)
try:
    result = opener.open(req)
#    result = urllib2.urlopen(req)
    # print result.info()
    # print result.read()
    # print cookie
except urllib2.HTTPError, e:
    print e.getcode()
    print e.reason
    print e.geturl()
    print "-------------------------!!!!!!!!!!!!!!!!!"
    print e.info()
    print(e.geturl())
    # req = urllib2.Request(e.geturl())
    # result = opener.open(req)
    # req = urllib2.Request(chengjiao_url)
    # result = opener.open(req).read()
    # print "!!!!",(result),"!!!!!!!"