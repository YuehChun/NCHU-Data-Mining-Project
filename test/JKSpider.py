from scrapy.spider import BaseSpider
from BeautifulSoup import BeautifulSoup as BS 
from scrapy.selector import HtmlXPathSelector

from tutorial.items import TutorialItem
def getname():
    return uuid.uuid1( ).hex()

class JKSpider(BaseSpider):
    name='joke'
    allowed_domains=["qiushibaike.com"]
    start_urls=[
    "http://www.qiushibaike.com/month?slow",
    ]

    def parse(self,response):
        root=BS(response.body)
        items=[]
        x=HtmlXPathSelector(response)
    
        y=x.select("//div[@class='content' and @title]/text()").extract()
        for i in y:
            item=TutorialItem()
            item["content"]=i
            items.append(item)
            
        return items