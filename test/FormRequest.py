import scrapy
from scrapy.http import FormRequest

class myspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["www.example.com"]

    def start_requests(self):
        return [ FormRequest("https://www.google.com.tw/search",
                     formdata={'q': 'foo'},
                     callback=self.parse) ]


MS = myspiderSpider()
print(MS.start_requests())