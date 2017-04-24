import scrapy
import urllib
class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    start_urls = (
        'https://bj.lianjia.com',)
    def start_requests(self):
        url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F'
        return [scrapy.FormRequest(url,meta = {'cookiejar' : 1},callback=self.post_login)]
    def post_login(self,response):
        urls = "https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F"
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

        r_headers = response.headers['Set-Cookie'].split(';')[0].split('=')

        cookies = {r_headers[0]: r_headers[1]}
        print cookies
        Lt = response.xpath('//input[@name="lt"]/@value').extract()[0]
        print Lt
        execution = response.xpath('//input[@name="execution"]/@value').extract()[0]
        print execution
        formdata = {
            'username': 'username',
            'password': 'password',
            #'service': 'http://bj.lianjia.com/',
            # 'isajax': 'true',
            #'remember': 1,
            'execution': execution,
            '_eventId': 'submit',
            'lt': Lt,
            'verifyCode': '',
            'redirect': '',
        }
        return [scrapy.FormRequest(
            url='https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F',
            meta={'cookiejar': response.meta['cookiejar']},
            #cookies=cookies,
            formdata=formdata,
            headers=headers,
            callback=self.after_login
            )]
    def after_login(self,response):
        if  response.body:
            yield scrapy.Request('http://user.lianjia.com',meta={'cookiejar': response.meta['cookiejar']},callback=self.parse_page)
    def parse_page(self, response):
        print response.body