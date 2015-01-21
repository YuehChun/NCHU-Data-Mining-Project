from scrapy import Spider, Item, Field
from scrapy import Selector
from scrapy.selector import HtmlXPathSelector
import time

class Post(Item):
    title = Field()

class BlogSpider(Spider):
    name, start_urls = 'cwb', ['http://www.cwb.gov.tw/V7/forecast/taiwan/inc/city/Keelung_City.htm']
    print (time.strftime("%d/%m/%Y"))
    def parse(self, response):
        sel = Selector(response)
        DayList = sel.xpath("//td[@class='num']")
        for DL in DayList : 
            # self.log("result: %s" % DL.xpath(".//img/@title").extract()[0])
            AllTitle = DL.xpath(".//img/@title").extract()[0]

            # self.log("result: %s" % DL.xpath("string()").extract()[0])
            AllTemp = DL.xpath("string()").extract()[0].replace("\n","").replace("\t","").split("~")
            MinTemp = int(AllTemp[0])
            MaxTemp = int(AllTemp[1])

            print AllTitle            
            
