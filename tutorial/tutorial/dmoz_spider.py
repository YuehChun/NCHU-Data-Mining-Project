from scrapy.spider import Spider
from scrapy.selector import Selector

from tutorial.items import DmozItem

class DmozSpider(Spider):
    name = "dmoz"   #給 Spider 取個名子
    allowed_domains = ["dmoz.org"]  #要抓的Domain
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",  #要抓的網址
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"  
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li')
        items = []
        for site in sites:
            item = DmozItem() #之前 Step2 定義的 Item
            item['title'] = site.xpath('a/text()').extract() #用 Xpath 抓指定的資料
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            items.append(item)
        return items