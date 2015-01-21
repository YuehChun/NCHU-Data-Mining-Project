from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.spider import BaseSpider

class DeltaItem(Item):
    title = Field()
    link = Field()
    desc = Field()


class DmozSpider(BaseSpider):
    name = "delta"
    allowed_domains = ["delta.com"]
    start_urls = []

    def parse(self, response):
        yield FormRequest.from_response(response,
                                        formname='flightSearchForm',
                                        formdata={'departureCity[0]': 'JFK',
                                                  'destinationCity[0]': 'SFO',
                                                  'departureDate[0]': '07.20.2013',
                                                  'departureDate[1]': '07.28.2013'},
                                        callback=self.parse1)

    def parse1(self, response):
        print response.status

    def hello(self,):
        print "hello"

DS = DmozSpider()
DS.parse("http://www.delta.com")