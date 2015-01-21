import scrapy
import re
import time
from scrapy.http import Request

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['weibo.com', 'sina.com.cn']

    def start_requests(self):
        username = 'bird'
        url = "https://tw.yahoo.com"
        # url = 'http://login.sina.com.cn/sso/prelogin.php?entry=miniblog&callback=sinaSSOController.preloginCallBack&user=%s&client=ssologin.js(v1.3.14)&_=%s'  % (username, str(time.time()).replace('.', ''))
        print url
        print Request(url=url, method='get').body
        return [Request(url=url, method='get', callback=self.parse_item)]
        

    def parse_item(self, response):
        print response.body
        hxs = HtmlXPathSelector(response)
        i = SrcItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i

        print hxs.select("//div[@class='country_code']/text()").extract()[0]

Ex = ExampleSpider()
Ex.start_requests()

