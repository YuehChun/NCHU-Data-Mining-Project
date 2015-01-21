import scrapy
class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['jadopado.com']

    def start_requests(self):
    	print(Request(url='http://jadopado.com/', cookies={'customer_country_code': 'AE'}))
        yield Request(url='http://jadopado.com/', cookies={'customer_country_code': 'AE'})

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        print hxs.select("//div[@class='country_code']/text()").extract()[0]

Ex = ExampleSpider()
Ex.parse()